#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台文生图API路由（火山引擎版本）
处理前端发送的文生图请求，调用火山引擎服务生成图片
"""

from flask import Blueprint, request, jsonify, current_app
import traceback
from app.services.interface_volcano_text_to_images import (
    generate_images, 
    get_supported_sizes,
    volcano_generator
)

# 创建蓝图
text_to_images_volcano = Blueprint('text_to_images_volcano', __name__)

@text_to_images_volcano.route('/text_to_image/volcano', methods=['POST'])
def create_image():
    """
    从文本生成图片的API端点
    
    请求体示例:
    {
        "prompt": "千军万马",
        "width": 512,
        "height": 512,
        "count": 1,
        "scale": 3.5,
        "steps": 25,
        "use_sr": true,
        "return_url": true,
        "add_watermark": false
    }
    
    返回示例:
    {
        "success": true,
        "data": {
            "images": [
                {
                    "url": "https://example.com/image.png"
                }
            ],
            "request_id": "123456789",
            "enhanced_prompt": "增强后的提示词..."
        }
    }
    """
    try:
        # 获取请求数据
        req_data = request.get_json()
        
        if not req_data or 'prompt' not in req_data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数：prompt"
            }), 400
            
        # 获取参数，提供默认值
        prompt = req_data.get('prompt')
        width = int(req_data.get('width', 512))
        height = int(req_data.get('height', 512))
        count = int(req_data.get('count', 1))
        scale = float(req_data.get('scale', 3.5))
        steps = int(req_data.get('steps', 25))
        use_sr = bool(req_data.get('use_sr', True))
        return_url = bool(req_data.get('return_url', True))
        add_watermark = bool(req_data.get('add_watermark', False))
        
        # 记录请求信息
        current_app.logger.info(f"火山引擎文生图请求 - 提示词: {prompt}, 尺寸: {width}x{height}, 数量: {count}")
        
        # 调用服务生成图片
        result = generate_images(
            prompt=prompt,
            width=width,
            height=height,
            count=count,
            scale=scale,
            steps=steps,
            use_sr=use_sr,
            return_url=return_url,
            add_watermark=add_watermark
        )
        
        # 如果生成成功
        if result.get('success'):
            # 记录成功信息
            image_count = len(result.get('data', {}).get('images', []))
            current_app.logger.info(f"火山引擎文生图成功 - 生成了 {image_count} 张图片")
            return jsonify(result)
        else:
            # 生成失败，返回错误信息
            error_msg = result.get('error', {}).get('message', '图片生成失败')
            error_code = result.get('error', {}).get('code', 500)
            current_app.logger.error(f"火山引擎文生图失败 - {error_msg}")
            
            return jsonify({
                "success": False,
                "error": error_msg,
                "code": error_code
            }), 500
            
    except Exception as e:
        # 捕获所有异常
        current_app.logger.error(f"火山引擎文生图API异常: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@text_to_images_volcano.route('/text_to_image/volcano/sizes', methods=['GET'])
def get_sizes():
    """获取支持的图片尺寸"""
    try:
        sizes = get_supported_sizes()
        return jsonify({
            "success": True,
            "data": {
                "sizes": sizes
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取支持尺寸异常: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@text_to_images_volcano.route('/text_to_image/volcano/info', methods=['GET'])
def get_api_info():
    """获取API信息"""
    return jsonify({
        "success": True,
        "data": {
            "name": "火山引擎文生图API",
            "description": "使用火山引擎AI服务将文本转换为图片",
            "model_version": "general_v2.1_L",
            "max_tokens": 75,
            "features": [
                "支持自定义图片尺寸",
                "支持多张图片生成",
                "支持高清图片生成",
                "支持多参数调整"
            ]
        }
    }) 