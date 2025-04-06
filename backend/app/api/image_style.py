#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台阿里云图片风格调整API路由
处理前端发送的图片风格化请求，调用阿里云百炼服务进行图片风格化处理
"""

from flask import Blueprint, request, jsonify, current_app
import traceback
from app.services.aliyun_image_style import create_style_task, query_style_task

# 创建蓝图
image_style = Blueprint('image_style', __name__)

@image_style.route('/image_style/create', methods=['POST'])
def create_style():
    """
    创建图片风格调整任务的API端点
    
    请求体示例:
    {
        "prompt": "转换成法国绘本风格",
        "image_url": "https://example.com/image.jpg",
        "n": 1,
        "seed": 12345,
        "watermark": false
    }
    
    返回示例:
    {
        "success": true,
        "data": {
            "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx",
            "task_status": "PENDING",
            "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
        }
    }
    """
    try:
        # 获取请求数据
        req_data = request.get_json()
        
        if not req_data:
            return jsonify({
                "success": False,
                "error": "请求数据为空"
            }), 400
            
        # 验证必要参数
        if 'prompt' not in req_data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数：prompt"
            }), 400
            
        if 'image_url' not in req_data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数：image_url"
            }), 400
            
        # 获取参数，提供默认值
        prompt = req_data.get('prompt')
        image_url = req_data.get('image_url')
        n = int(req_data.get('n', 1))
        seed = req_data.get('seed')
        watermark = bool(req_data.get('watermark', False))
        
        # 参数验证
        if n < 1 or n > 4:
            return jsonify({
                "success": False,
                "error": "参数n的值必须在1-4之间"
            }), 400
            
        if seed is not None and (not isinstance(seed, int) or seed < 0 or seed > 2147483647):
            return jsonify({
                "success": False,
                "error": "参数seed的值必须在0-2147483647之间"
            }), 400
            
        # 记录请求信息
        current_app.logger.info(f"阿里云图片风格调整请求 - 提示词: {prompt}, 图片URL: {image_url}")
        
        # 调用服务创建任务
        result = create_style_task(
            prompt=prompt,
            image_url=image_url,
            n=n,
            seed=seed,
            watermark=watermark
        )
        
        # 如果创建成功
        if result.get('success'):
            return jsonify(result)
        else:
            # 创建失败，返回错误信息
            error_msg = result.get('error', {}).get('message', '任务创建失败')
            error_code = result.get('error', {}).get('code', 500)
            
            return jsonify({
                "success": False,
                "error": error_msg,
                "code": error_code
            }), 500
            
    except Exception as e:
        # 捕获所有异常
        current_app.logger.error(f"阿里云图片风格调整API异常: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@image_style.route('/image_style/query/<task_id>', methods=['GET'])
def query_style(task_id):
    """
    查询图片风格调整任务的API端点
    
    路径参数:
        task_id: 任务ID
    
    返回示例:
    {
        "success": true,
        "data": {
            "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx",
            "task_status": "SUCCEEDED",
            "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx",
            "image_urls": ["https://example.com/result.png"],
            "submit_time": "2025-02-21 17:56:31.786",
            "end_time": "2025-02-21 17:56:42.530"
        }
    }
    """
    try:
        if not task_id:
            return jsonify({
                "success": False,
                "error": "缺少必要参数：task_id"
            }), 400
            
        # 记录查询信息
        current_app.logger.info(f"查询阿里云图片风格调整任务 - 任务ID: {task_id}")
        
        # 调用服务查询任务
        result = query_style_task(task_id)
        
        # 返回查询结果
        if result.get('success'):
            return jsonify(result)
        else:
            # 查询失败，返回错误信息
            error_msg = result.get('error', {}).get('message', '任务查询失败')
            error_code = result.get('error', {}).get('code', 500)
            
            return jsonify({
                "success": False,
                "error": error_msg,
                "code": error_code
            }), 500
            
    except Exception as e:
        # 捕获所有异常
        current_app.logger.error(f"阿里云图片风格调整查询API异常: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@image_style.route('/image_style/info', methods=['GET'])
def get_api_info():
    """获取API信息"""
    return jsonify({
        "success": True,
        "data": {
            "name": "阿里云图片风格调整API",
            "description": "使用阿里云百炼DashScope API进行图片风格化调整",
            "model_version": "wanx2.1-imageedit",
            "features": [
                "支持全局风格化调整",
                "支持多种风格提示词",
                "支持多张结果生成",
                "支持异步任务处理"
            ]
        }
    }) 