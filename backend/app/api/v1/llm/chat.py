#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, Response
import json
import os
import sys
import traceback
from app.services.llm_service import get_api_client, MODEL_CONFIG, VolcanoAPI, SiliconFlowAPI

bp = Blueprint('llm', __name__, url_prefix='/llm')

@bp.route('/models', methods=['GET'])
def list_models():
    """获取可用模型列表"""
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
        print(f"获取模型列表出错: {str(e)}")
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
        print("\n=== 收到新的聊天请求 ===")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if not data or 'messages' not in data:
            print("错误：请求数据格式不正确")
            return jsonify({'status': 'error', 'message': 'Invalid request format'}), 400
            
        messages = data['messages']
        print(f"\n=== 处理消息 ===")
        print(f"消息数量: {len(messages)}")
        for i, msg in enumerate(messages):
            print(f"消息 {i+1}: {msg.get('role', 'unknown')} - {msg.get('content', '')[:100]}...")
        
        # 获取模型ID，如果没有提供则使用默认值
        model_id = data.get('model', 'deepseek-v3-vol')
        print(f"\n=== 使用模型 ===")
        print(f"模型ID: {model_id}")
        
        # 检查是否为流式请求
        stream = data.get('stream', False)
        print(f"流式输出: {'启用' if stream else '禁用'}")
        
        # 获取温度和最大令牌数
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        # 获取API客户端
        client, api_error = get_api_client(model_id)
        if not client:
            print(f"错误：初始化API客户端失败 - {api_error.get('error', '未知错误')}")
            return jsonify(api_error), 500
        
        # 如果请求参数中启用了流式输出
        if stream:
            print("\n=== 启用流式输出 ===")
            
            try:
                # 获取模型配置
                model_config = MODEL_CONFIG.get(model_id)
                if not model_config:
                    return jsonify({
                        'status': 'error',
                        'message': f'未知模型: {model_id}'
                    }), 400
                
                # 提取真实的模型ID
                real_model_id = model_config["model_id"]
                
                # 调用API，获取流式响应生成器
                generator = client.chat_completion(
                    messages=messages,
                    model_id=real_model_id,
                    temperature=temperature, 
                    max_tokens=max_tokens,
                    stream=True
                )
                
                # 定义流式响应函数
                def generate():
                    try:
                        # 对于返回字符串的生成器（如果是函数返回的迭代器）
                        if hasattr(generator, '__iter__'):
                            for chunk in generator:
                                # 调试日志
                                print(f"SSE数据: {chunk[:100]}...")
                                
                                # 为每个块包装data前缀，符合SSE规范
                                if isinstance(chunk, str):
                                    yield f"data: {chunk}\n\n"
                                else:
                                    # 如果是字典，转换为JSON字符串
                                    chunk_json = json.dumps(chunk, ensure_ascii=False)
                                    yield f"data: {chunk_json}\n\n"
                            
                            # 流结束时发送[DONE]标记
                            yield "data: [DONE]\n\n"
                        # 对于返回Response对象的情况
                        elif hasattr(generator, 'status_code'):
                            # 返回常规响应
                            response_data = {
                                'status': 'success',
                                'data': generator.json()
                            }
                            yield f"data: {json.dumps(response_data, ensure_ascii=False)}\n\n"
                            yield "data: [DONE]\n\n"
                    except Exception as e:
                        print(f"流式输出错误: {str(e)}")
                        error_json = json.dumps({"error": {"message": str(e)}})
                        yield f"data: {error_json}\n\n"
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
                print(f"启动流式输出失败: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'status': 'error',
                    'message': f'流式输出失败: {str(e)}'
                }), 500
        
        # 普通非流式请求处理
        print("\n=== 调用API ===")
        print(f"开始发送请求到API...")
        
        try:
            # 获取模型配置
            model_config = MODEL_CONFIG.get(model_id)
            if not model_config:
                return jsonify({
                    'status': 'error',
                    'message': f'未知模型: {model_id}'
                }), 400
            
            # 提取真实的模型ID
            real_model_id = model_config["model_id"]
            
            # 调用API客户端的聊天完成方法
            response = client.chat_completion(
                messages=messages,
                model_id=real_model_id,
                temperature=temperature, 
                max_tokens=max_tokens,
                stream=False
            )
            
            print("\n=== 解析响应数据 ===")
            print(f"响应数据: {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            # 检查是否有错误
            if "error" in response:
                error_msg = response["error"].get("message", "未知错误")
                print(f"API返回错误: {error_msg}")
                return jsonify({
                    'status': 'error',
                    'message': error_msg
                }), 500
            
            # 返回标准化的成功响应
            return jsonify({
                'status': 'success',
                'data': response
            })
                
        except Exception as e:
            print(f"\n=== 发生异常 ===")
            print(f"异常类型: {type(e).__name__}")
            print(f"异常信息: {str(e)}")
            import traceback
            print(f"堆栈跟踪:\n{traceback.format_exc()}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
            
    except Exception as e:
        print(f"\n=== 发生异常 ===")
        print(f"异常类型: {type(e).__name__}")
        print(f"异常信息: {str(e)}")
        import traceback
        print(f"堆栈跟踪:\n{traceback.format_exc()}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 