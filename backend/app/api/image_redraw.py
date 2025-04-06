#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台阿里云图片重绘API路由
处理前端发送的图片局部重绘请求，调用阿里云百炼服务对图像指定区域进行增加、修改或删除操作
"""

from flask import Blueprint, request, jsonify, current_app
import traceback
from app.services.aliyun_image_redraw import create_redraw_task, query_redraw_task

# 创建蓝图
image_redraw = Blueprint('image_redraw', __name__)

@image_redraw.route('/image_redraw/create', methods=['POST'])
def create_redraw():
    """
    创建图片局部重绘任务的API端点
    
    请求体示例:
    {
        "prompt": "一个透明玻璃花瓶放在桌子上",
        "base_image_url": "https://example.com/image.jpg",
        "mask_image_url": "https://example.com/mask.png",
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
        if 'base_image_url' not in req_data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数：base_image_url"
            }), 400
            
        if 'mask_image_url' not in req_data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数：mask_image_url"
            }), 400
            
        # 获取参数，提供默认值
        prompt = req_data.get('prompt', '')  # 允许为空，用于特定删除操作
        base_image_url = req_data.get('base_image_url')
        mask_image_url = req_data.get('mask_image_url')
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
        current_app.logger.info(f"阿里云图片重绘请求 - 提示词: {prompt}, 基础图片URL: {base_image_url}, 蒙版图片URL: {mask_image_url}")
        
        # 调用服务创建任务
        result = create_redraw_task(
            prompt=prompt,
            base_image_url=base_image_url,
            mask_image_url=mask_image_url,
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
        current_app.logger.error(f"阿里云图片重绘API异常: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@image_redraw.route('/image_redraw/query/<task_id>', methods=['GET'])
def query_redraw(task_id):
    """
    查询图片重绘任务的API端点
    
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
        current_app.logger.info(f"查询阿里云图片重绘任务 - 任务ID: {task_id}")
        
        # 调用服务查询任务
        result = query_redraw_task(task_id)
        
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
        current_app.logger.error(f"阿里云图片重绘查询API异常: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@image_redraw.route('/image_redraw/info', methods=['GET'])
def get_api_info():
    """获取API信息"""
    return jsonify({
        "success": True,
        "data": {
            "name": "阿里云图片重绘API",
            "description": "使用阿里云百炼DashScope API进行图片局部重绘操作",
            "model_version": "wanx2.1-imageedit",
            "features": [
                "支持对图像指定区域进行增加、修改或删除操作",
                "适用于换装、替换局部物件、删除干扰物等场景",
                "支持多张结果生成",
                "支持异步任务处理"
            ],
            "usage_tips": [
                "增加/修改操作提示词可描述具体动作或客观描述期望内容",
                "删除操作时，若删除区域较小可留空提示词",
                "删除区域较大时需详细描述擦除后的内容"
            ]
        }
    }) 