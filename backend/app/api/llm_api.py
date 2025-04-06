import os
import json
import logging
from flask import Blueprint, request, jsonify, current_app
from ..services.llm_service import chat_completion, get_available_models

# 创建蓝图
llm_api_bp = Blueprint('llm_api', __name__)

# 设置日志
logger = logging.getLogger(__name__)

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
        "stream": false  # 可选，是否启用流式响应，默认false
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error": {
                    "message": "请求体为空或格式错误",
                    "type": "invalid_request_error",
                    "code": 400
                }
            }), 400
        
        # 获取必要参数
        model = data.get('model')
        messages = data.get('messages')
        
        # 验证必要参数
        if not model:
            return jsonify({
                "error": {
                    "message": "缺少必要参数：model",
                    "type": "invalid_request_error",
                    "code": 400
                }
            }), 400
        
        if not messages or not isinstance(messages, list):
            return jsonify({
                "error": {
                    "message": "缺少必要参数：messages 或格式错误",
                    "type": "invalid_request_error",
                    "code": 400
                }
            }), 400
        
        # 获取可选参数
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2000)
        stream = data.get('stream', False)
        
        # 调用LLM服务
        response = chat_completion(
            model_name=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        
        # 返回结果
        return jsonify(response)
        
    except Exception as e:
        logger.exception("处理对话请求时出错")
        return jsonify({
            "error": {
                "message": f"服务器处理异常: {str(e)}",
                "type": "server_error",
                "code": 500
            }
        }), 500

@llm_api_bp.route('/models', methods=['GET'])
def get_models():
    """获取可用的模型列表"""
    try:
        models = get_available_models()
        return jsonify({
            "models": models
        })
    except Exception as e:
        logger.exception("获取可用模型列表时出错")
        return jsonify({
            "error": {
                "message": f"服务器处理异常: {str(e)}",
                "type": "server_error",
                "code": 500
            }
        }), 500 