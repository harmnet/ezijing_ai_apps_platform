#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
火山引擎DeepSeek R1模型流式调用API
提供REST API接口，支持流式响应
使用直接的requests库调用火山引擎API，避免OpenAI库的兼容性问题
"""

from flask import Blueprint, jsonify, request, Response, current_app
import json
import os
import sys
import time
import traceback
import logging
import requests

# 创建蓝图
bp = Blueprint('deepseek_volcano_stream', __name__, url_prefix='/deepseek_volcano')

# 配置日志记录
logger = logging.getLogger("deepseek-volcano-stream")
logger.setLevel(logging.DEBUG)

# 从环境变量获取API密钥，如果没有则使用默认值
DEFAULT_API_KEY = "03824a7c-e453-4ccd-b356-e7f80a793add"  # 这应该替换为实际使用的API密钥
API_KEY = os.environ.get("VOLCANO_API_KEY", DEFAULT_API_KEY)
API_BASE = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

# 模型配置
MODELS = {
    "deepseek-r1": {
        "id": "deepseek-r1-250120",
        "description": "DeepSeek R1-64K (火山引擎)",
        "token_limit": 65536
    },
    "deepseek-v3": {
        "id": "deepseek-v3-250324",
        "description": "DeepSeek V3-64K (火山引擎)",
        "token_limit": 65536
    }
}

@bp.route('/models', methods=['GET'])
def list_models():
    """获取可用模型列表"""
    try:
        models = []
        for model_key, config in MODELS.items():
            models.append({
                "id": model_key,
                "name": config["description"],
                "provider": "火山引擎",
                "max_tokens": config["token_limit"]
            })
        
        return jsonify({
            "status": "success",
            "data": models
        })
    except Exception as e:
        logger.error(f"获取模型列表出错: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"获取模型列表失败: {str(e)}"
        }), 500

@bp.route('/chat', methods=['POST'])
def chat():
    """聊天API，支持流式输出"""
    try:
        data = request.get_json()
        logger.info(f"接收到新的聊天请求: {json.dumps(data, ensure_ascii=False)[:200]}...")
        
        if not data or 'messages' not in data:
            logger.error("错误：请求数据格式不正确")
            return jsonify({'status': 'error', 'message': 'Invalid request format'}), 400
            
        messages = data['messages']
        
        # 获取模型ID，如果没有提供则使用默认值
        model_key = data.get('model', 'deepseek-r1')
        if model_key not in MODELS:
            return jsonify({
                'status': 'error',
                'message': f'未知模型: {model_key}'
            }), 400
        
        # 获取实际模型ID
        real_model_id = MODELS[model_key]["id"]
        
        # 检查是否为流式请求
        stream = data.get('stream', True)  # 默认为流式
        
        # 获取温度和最大令牌数
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2000)
        
        # 判断是否启用思考过程（仅对R1模型有效）
        return_reasoning = data.get('return_reasoning', model_key == "deepseek-r1")
        
        # 准备请求参数
        payload = {
            "model": real_model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # 如果是R1模型，添加思考过程参数
        if "r1" in real_model_id.lower() and return_reasoning:
            payload["return_reasoning"] = True
            logger.info("启用思考过程返回")
        
        # 如果是流式请求
        if stream:
            logger.info(f"启动流式请求, 模型: {real_model_id}")
            
            # 添加流式参数
            payload["stream"] = True
            headers["Accept"] = "text/event-stream"
            
            try:
                # 定义流式响应生成器
                def generate():
                    try:
                        # 创建流式请求
                        with requests.post(
                            API_BASE, 
                            json=payload, 
                            headers=headers, 
                            stream=True,
                            timeout=120
                        ) as response:
                            # 检查响应状态码
                            if response.status_code != 200:
                                error_msg = f"API请求失败: 状态码 {response.status_code}, 响应: {response.text}"
                                logger.error(error_msg)
                                yield f"data: {json.dumps({'error': {'message': error_msg}})}\n\n"
                                yield "data: [DONE]\n\n"
                                return
                            
                            current_reasoning = ""  # 用于累积思考过程
                            
                            # 处理流式响应
                            for line in response.iter_lines():
                                if not line:
                                    continue
                                
                                line_text = line.decode('utf-8')
                                logger.debug(f"流式数据行: {line_text[:100]}...")
                                
                                # 处理SSE格式的数据
                                if line_text.startswith("data: "):
                                    data_text = line_text[6:]
                                    
                                    # 处理思考过程数据
                                    if return_reasoning and "r1" in real_model_id.lower():
                                        try:
                                            data_json = json.loads(data_text)
                                            # 检查是否包含思考过程
                                            if "reasoning" in data_json:
                                                reasoning_text = data_json["reasoning"]
                                                if reasoning_text:
                                                    current_reasoning += reasoning_text
                                                    # 发送思考过程数据
                                                    yield f"data: {json.dumps({'reasoning': reasoning_text})}\n\n"
                                                    continue
                                        except json.JSONDecodeError:
                                            pass
                                    
                                    # 检查是否是结束标记
                                    if data_text.strip() == "[DONE]":
                                        # 如果有累积的思考过程，在结束前发送完整思考过程
                                        if current_reasoning:
                                            logger.debug(f"发送完整思考过程: {current_reasoning[:100]}...")
                                            yield f"data: {json.dumps({'full_reasoning': current_reasoning})}\n\n"
                                        
                                        yield "data: [DONE]\n\n"
                                        break
                                    
                                    # 原样传递其他SSE数据
                                    yield f"{line_text}\n\n"
                                    
                                elif line_text == "[DONE]":
                                    # 如果有累积的思考过程，在结束前发送完整思考过程
                                    if current_reasoning:
                                        logger.debug(f"发送完整思考过程: {current_reasoning[:100]}...")
                                        yield f"data: {json.dumps({'full_reasoning': current_reasoning})}\n\n"
                                    
                                    yield "data: [DONE]\n\n"
                                    break
                            
                            # 确保在任何情况下都发送结束标记
                            yield "data: [DONE]\n\n"
                        
                    except requests.exceptions.Timeout:
                        logger.error(f"请求超时: 模型={real_model_id}")
                        yield f"data: {json.dumps({'error': {'message': '请求超时，服务器未能及时响应'}})}\n\n"
                        yield "data: [DONE]\n\n"
                    except requests.exceptions.ConnectionError as e:
                        logger.error(f"连接错误: {str(e)}")
                        yield f"data: {json.dumps({'error': {'message': f'连接错误: {str(e)}'}})}\n\n"
                        yield "data: [DONE]\n\n"
                    except Exception as e:
                        logger.error(f"流式处理出错: {str(e)}")
                        logger.error(traceback.format_exc())
                        yield f"data: {json.dumps({'error': {'message': str(e)}})}\n\n"
                        yield "data: [DONE]\n\n"
                
                # 返回流式响应
                return Response(
                    generate(),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'X-Accel-Buffering': 'no'
                    }
                )
                
            except Exception as e:
                logger.error(f"流式请求初始化失败: {str(e)}")
                logger.error(traceback.format_exc())
                return jsonify({
                    'status': 'error',
                    'message': f'流式请求初始化失败: {str(e)}'
                }), 500
        
        # 非流式请求
        else:
            logger.info(f"启动普通请求, 模型: {real_model_id}")
            
            try:
                # 发送普通请求
                response = requests.post(
                    API_BASE, 
                    json=payload, 
                    headers=headers,
                    timeout=60
                )
                
                # 检查响应状态码
                if response.status_code != 200:
                    error_msg = f"API请求失败: 状态码 {response.status_code}, 响应: {response.text}"
                    logger.error(error_msg)
                    return jsonify({
                        'status': 'error',
                        'message': error_msg
                    }), 500
                
                # 解析响应JSON
                response_data = response.json()
                logger.info(f"普通请求响应: {json.dumps(response_data, ensure_ascii=False)[:200]}...")
                
                # 提取思考过程并添加到响应中（如果有）
                if return_reasoning and "r1" in real_model_id.lower() and "reasoning" in response_data:
                    reasoning_data = response_data.get("reasoning", "")
                    return jsonify({
                        'status': 'success',
                        'data': response_data,
                        'reasoning': reasoning_data
                    })
                
                return jsonify({
                    'status': 'success',
                    'data': response_data
                })
                
            except requests.exceptions.Timeout:
                error_msg = f"请求超时: 模型={real_model_id}"
                logger.error(error_msg)
                return jsonify({
                    'status': 'error',
                    'message': error_msg
                }), 504
            except requests.exceptions.ConnectionError as e:
                error_msg = f"连接错误: {str(e)}"
                logger.error(error_msg)
                return jsonify({
                    'status': 'error',
                    'message': error_msg
                }), 502
            except Exception as e:
                logger.error(f"普通请求失败: {str(e)}")
                logger.error(traceback.format_exc())
                return jsonify({
                    'status': 'error',
                    'message': f'请求失败: {str(e)}'
                }), 500
                
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 