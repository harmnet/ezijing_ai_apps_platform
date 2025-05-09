import os
import json
import logging
import time
from flask import Blueprint, request, jsonify, current_app, Response, stream_with_context
from flask_cors import CORS
from ..services.llm_service import chat_completion, get_available_models, get_api_client, MODEL_CONFIG

# 创建蓝图
llm_api_bp = Blueprint('llm_api', __name__, url_prefix='/api/v1/llm')
CORS(llm_api_bp)

# 配置日志
logger = logging.getLogger('llm-api')
logger.setLevel(logging.DEBUG)

# 定义stream_response函数，将响应数据格式化为SSE格式
def stream_response(data):
    """格式化流式响应为SSE格式"""
    if isinstance(data, dict):
        # 如果是字典，转换为JSON字符串
        json_data = json.dumps(data, ensure_ascii=False)
        return f"data: {json_data}\n\n"
    # 如果已经是字符串，直接返回
    return f"data: {data}\n\n"

@llm_api_bp.route('/chat', methods=['POST'])
def chat():
    """
    与大语言模型进行对话
    ---
    请求参数:
    {
        "model": "qwen-max",  # 模型名称，如 qwen-max, deepseek-v3-sf 等
        "messages": [  # 消息历史
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好，有什么可以帮助你的吗？"},
            {"role": "user", "content": "请帮我写一篇关于AI的文章"}
        ],
        "temperature": 0.7,  # 可选，控制输出的随机性，默认0.7
        "max_tokens": 2000,  # 可选，最大输出token数，默认2000
        "stream": false,  # 可选，是否启用流式响应，默认false
        "stream_options": {  # 可选，流式选项
            "include_usage": false  # 可选，是否包含token统计，默认false
        }
    }
    """
    try:
        # 获取请求数据
        data = request.json
        
        # 记录请求信息
        logger.info(f"收到聊天请求，IP: {request.remote_addr}")
        logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
        logger.info(f"请求头: {dict(request.headers)}")
        
        # 提取必需参数
        model = data.get('model', 'deepseek-r1-vol')  # 默认使用R1模型
        messages = data.get('messages', [])
        temperature = float(data.get('temperature', 0.7))
        max_tokens = int(data.get('max_tokens', 1000))
        
        # 明确转换stream为布尔值，并确保正确解析
        stream_raw = data.get('stream', False)
        logger.info(f"原始stream参数值: {stream_raw}, 类型: {type(stream_raw)}")
        
        # 强制转换为布尔值，处理各种可能的输入
        if isinstance(stream_raw, str):
            stream = stream_raw.lower() == 'true'
        elif isinstance(stream_raw, (int, float)):
            stream = bool(stream_raw)
        else:
            stream = bool(stream_raw)
            
        logger.info(f"转换后stream值: {stream}, 类型: {type(stream)}")
        
        # 检查Accept头是否要求流式响应
        accept_header = request.headers.get('Accept', '')
        if 'text/event-stream' in accept_header:
            logger.info(f"检测到Accept: text/event-stream头，强制启用流式响应")
            stream = True
        
        # 获取流式选项
        stream_options = data.get('stream_options', {})
        
        # 详细记录请求参数
        logger.info(f"请求参数详情: 模型={model}, 温度={temperature}, 最大tokens={max_tokens}, 流式={stream}")
        logger.info(f"请求模式: {'流式' if stream else '非流式'}, 消息数量: {len(messages)}")
        if stream:
            logger.info(f"流式选项: {json.dumps(stream_options, ensure_ascii=False)}")
        
        # 参数验证
        if not messages:
            logger.warning("请求中没有提供消息内容")
            return jsonify({
                "status": "error",
                "message": "消息不能为空"
            }), 400
        
        # 获取API客户端
        client, api_error = get_api_client(model)
        if not client:
            logger.error(f"获取API客户端失败: {api_error}")
            return jsonify({
                "status": "error",
                "message": api_error.get('error', '获取API客户端失败')
            }), 500
        
        # 获取模型配置和真实模型ID
        model_config = MODEL_CONFIG.get(model)
        if not model_config:
            logger.error(f"未知模型: {model}")
            return jsonify({
                "status": "error",
                "message": f"未知模型: {model}"
            }), 400
        
        real_model_id = model_config["model_id"]
        logger.info(f"实际使用模型ID: {real_model_id}")
        
        # 调用API - 处理流式和非流式请求
        try:
            # 流式响应处理
            if stream:
                logger.info(f"准备处理流式请求，模型: {model}, 实际模型ID: {real_model_id}")
                
                # 创建流式响应
                def generate_stream():
                    try:
                        logger.info(f"开始生成流式响应，使用client.chat_stream方法...")
                        
                        # 直接使用client的chat_stream方法获取流式生成器
                        stream_gen = client.chat_stream(
                            model=real_model_id,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            stream_options=stream_options
                        )
                        
                        logger.info(f"已获取流式生成器，开始处理数据块...")
                        
                        # 遍历生成器，将每个块转为SSE格式
                        chunk_count = 0
                        for chunk in stream_gen:
                            chunk_count += 1
                            if chunk_count <= 3 or chunk_count % 10 == 0:
                                logger.debug(f"数据块 #{chunk_count}: {json.dumps(chunk, ensure_ascii=False)[:100]}...")
                            
                            if chunk:
                                # 将JSON对象转为字符串
                                chunk_str = json.dumps(chunk, ensure_ascii=False)
                                # 返回SSE格式数据
                                yield f"data: {chunk_str}\n\n"
                        
                        # 发送结束标记
                        logger.info(f"流式生成完成，共处理{chunk_count}个块，发送结束标记")
                        yield "data: [DONE]\n\n"
                        
                    except Exception as e:
                        logger.exception(f"流式输出处理异常: {str(e)}")
                        error_json = json.dumps({
                            "error": {
                                "message": f"流式处理异常: {str(e)}",
                                "type": "server_error",
                                "code": 500
                            }
                        })
                        yield f"data: {error_json}\n\n"
                        yield "data: [DONE]\n\n"
                
                # 设置SSE所需的响应头
                response = Response(
                    stream_with_context(generate_stream()),
                    status=200,
                    mimetype='text/event-stream'
                )
                
                # 确保设置正确的头信息
                response.headers['Content-Type'] = 'text/event-stream'
                response.headers['Cache-Control'] = 'no-cache'
                response.headers['Connection'] = 'keep-alive'
                response.headers['X-Accel-Buffering'] = 'no'
                response.headers['Access-Control-Allow-Origin'] = '*'
                
                logger.info(f"返回流式响应，HEAD: {dict(response.headers)}")
                return response
                
            else:
                # 非流式请求处理
                logger.info(f"执行普通非流式请求，模型: {model}, 实际模型ID: {real_model_id}")
                
                # 调用API客户端
                start_time = time.time()
                logger.info(f"调用model.chat方法，参数: model={real_model_id}, messages={len(messages)}项, temperature={temperature}, max_tokens={max_tokens}")
                
                response = client.chat(
                    model=real_model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                duration = time.time() - start_time
                logger.info(f"API请求完成，耗时: {duration:.2f}秒")
                
                # 记录响应信息
                if isinstance(response, dict) and "error" in response:
                    logger.error(f"API返回错误: {response['error']}")
                    return jsonify({
                        "status": "error",
                        "message": response["error"].get("message", "API调用失败")
                    }), 500
                
                # 记录成功响应
                tokens_info = response.get("usage", {})
                logger.info(f"请求成功，tokens使用: {tokens_info}")
                
                # 返回标准化的成功响应
                logger.info("返回非流式响应结果")
                return jsonify({
                    "status": "success",
                    "data": response
                })
                
        except Exception as e:
            logger.exception(f"API调用失败: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"API调用失败: {str(e)}"
            }), 500
        
    except Exception as e:
        logger.exception("处理对话请求时出错")
        return jsonify({
            "status": "error",
            "message": f"服务器处理异常: {str(e)}"
        }), 500

@llm_api_bp.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    与大语言模型进行流式对话 - 专用流式接口
    ---
    请求参数与chat接口相同，但此接口始终返回流式响应
    """
    try:
        # 获取请求数据
        data = request.json
        
        # 强制启用流式传输
        data['stream'] = True
        if 'stream_options' not in data:
            data['stream_options'] = {"include_usage": True}
            
        # 记录请求信息
        logger.info(f"收到流式聊天请求，IP: {request.remote_addr}")
        logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
        logger.info(f"请求头: {dict(request.headers)}")
        
        # 提取必需参数
        model = data.get('model', 'deepseek-r1-vol')  # 默认使用R1模型
        messages = data.get('messages', [])
        temperature = float(data.get('temperature', 0.7))
        max_tokens = int(data.get('max_tokens', 1000))
        stream_options = data.get('stream_options', {"include_usage": True})
        
        # 详细记录请求参数
        logger.info(f"流式请求参数: 模型={model}, 温度={temperature}, 最大tokens={max_tokens}")
        logger.info(f"流式选项: {json.dumps(stream_options, ensure_ascii=False)}")
        
        # 参数验证
        if not messages:
            logger.warning("请求中没有提供消息内容")
            return jsonify({
                "status": "error",
                "message": "消息不能为空"
            }), 400
        
        # 获取API客户端
        client, api_error = get_api_client(model)
        if not client:
            logger.error(f"获取API客户端失败: {api_error}")
            return jsonify({
                "status": "error",
                "message": api_error.get('error', '获取API客户端失败')
            }), 500
        
        # 获取模型配置和真实模型ID
        model_config = MODEL_CONFIG.get(model)
        if not model_config:
            logger.error(f"未知模型: {model}")
            return jsonify({
                "status": "error",
                "message": f"未知模型: {model}"
            }), 400
        
        real_model_id = model_config["model_id"]
        logger.info(f"实际使用模型ID: {real_model_id}")
        
        # 创建流式响应函数
        def generate_stream():
            try:
                logger.info(f"开始生成流式响应，使用client.chat_stream方法...")
                
                # 直接使用client的chat_stream方法获取流式生成器
                stream_gen = client.chat_stream(
                    model=real_model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream_options=stream_options
                )
                
                logger.info(f"已获取流式生成器，开始处理数据块...")
                
                # 遍历生成器，将每个块转为SSE格式
                chunk_count = 0
                for chunk in stream_gen:
                    chunk_count += 1
                    if chunk_count <= 3 or chunk_count % 10 == 0:
                        logger.debug(f"数据块 #{chunk_count}: {json.dumps(chunk, ensure_ascii=False)[:100]}...")
                    
                    if chunk:
                        # 将JSON对象转为字符串
                        chunk_str = json.dumps(chunk, ensure_ascii=False)
                        # 返回SSE格式数据
                        yield f"data: {chunk_str}\n\n"
                
                # 发送结束标记
                logger.info(f"流式生成完成，共处理{chunk_count}个块，发送结束标记")
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                logger.exception(f"流式输出处理异常: {str(e)}")
                error_json = json.dumps({
                    "error": {
                        "message": f"流式处理异常: {str(e)}",
                        "type": "server_error",
                        "code": 500
                    }
                })
                yield f"data: {error_json}\n\n"
                yield "data: [DONE]\n\n"
        
        # 创建响应对象
        response = Response(
            stream_with_context(generate_stream()),
            mimetype='text/event-stream'
        )
        
        # 设置SSE响应所需的头信息
        response.headers['Content-Type'] = 'text/event-stream'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Connection'] = 'keep-alive'
        response.headers['X-Accel-Buffering'] = 'no'
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        logger.info(f"返回流式响应，HEAD: {dict(response.headers)}")
        return response
        
    except Exception as e:
        logger.exception("处理流式对话请求时出错")
        return jsonify({
            "status": "error",
            "message": f"服务器处理异常: {str(e)}"
        }), 500

@llm_api_bp.route('/models', methods=['GET'])
def get_models():
    """获取可用的模型列表"""
    try:
        models = []
        for model_id, config in MODEL_CONFIG.items():
            models.append({
                "id": model_id,
                "name": config["description"],
                "provider": config["provider"],
                "max_tokens": config["token_limit"]
            })
        
        return jsonify({
            "status": "success",
            "data": {
                "models": models
            }
        })
    except Exception as e:
        logger.exception("获取可用模型列表时出错")
        return jsonify({
            "status": "error",
            "message": f"获取模型列表失败: {str(e)}"
        }), 500 