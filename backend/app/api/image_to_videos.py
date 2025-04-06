#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图生视频API路由
使用火山引擎ARK Runtime的图生视频功能
"""

from flask import Blueprint, request, jsonify, current_app
import traceback
from app.services.volcano_image_to_video import (
    create_image_to_video_task, 
    query_video_task, 
    delete_video_task,
    get_supported_ratios,
    get_supported_durations
)

image_to_videos = Blueprint('image_to_videos', __name__)

@image_to_videos.route('/image-to-videos/create', methods=['POST'])
def create_video_api():
    """创建图生视频任务的API端点"""
    try:
        # 获取并验证请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "缺少请求数据",
                "code": 400
            }), 400

        # 提取参数
        image_url = data.get('image_url')
        prompt = data.get('prompt')
        
        # 验证必要参数
        if not image_url:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: image_url",
                "code": 400
            }), 400
            
        if not prompt:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: prompt",
                "code": 400
            }), 400
            
        # 提取其他参数
        ratio = data.get('ratio', '16:9')
        duration = float(data.get('duration', 5.0))
        
        # 记录请求日志
        current_app.logger.info(f"创建图生视频任务请求: 提示词长度={len(prompt)}, 图片URL={image_url}")
        
        # 调用服务创建任务
        result = create_image_to_video_task(
            image_url=image_url,
            prompt=prompt,
            ratio=ratio,
            duration=duration
        )
        
        # 检查响应是否包含错误
        if result.get('status') == 'failed':
            return jsonify(result), 400
            
        # 返回成功结果
        return jsonify(result)

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"创建图生视频任务API错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@image_to_videos.route('/image-to-videos/query', methods=['GET'])
def query_video_api():
    """查询图生视频任务状态的API端点"""
    try:
        # 获取任务ID
        task_id = request.args.get('task_id')
        if not task_id:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: task_id",
                "code": 400
            }), 400
            
        # 记录请求日志
        current_app.logger.info(f"查询图生视频任务状态: task_id={task_id}")
        
        # 调用服务查询任务
        result = query_video_task(task_id)
        
        # 检查响应是否包含错误
        if result.get('status') == 'failed':
            return jsonify(result), 400
            
        # 返回查询结果
        return jsonify(result)

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"查询图生视频任务API错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@image_to_videos.route('/image-to-videos/delete', methods=['POST'])
def delete_video_api():
    """删除图生视频任务的API端点"""
    try:
        # 获取并验证请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "缺少请求数据",
                "code": 400
            }), 400

        # 提取参数
        task_id = data.get('task_id')
        
        # 验证必要参数
        if not task_id:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: task_id",
                "code": 400
            }), 400
            
        # 记录请求日志
        current_app.logger.info(f"删除图生视频任务: task_id={task_id}")
        
        # 调用服务删除任务
        result = delete_video_task(task_id)
        
        # 检查响应是否包含错误
        if result.get('status') == 'failed':
            return jsonify(result), 400
            
        # 返回成功结果
        return jsonify(result)

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"删除图生视频任务API错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@image_to_videos.route('/image-to-videos/ratios', methods=['GET'])
def get_ratios_api():
    """获取支持的视频比例API端点"""
    try:
        # 获取可用的比例列表
        ratios = get_supported_ratios()
        
        # 返回成功结果
        return jsonify({
            "status": "success",
            "ratios": ratios
        })

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"获取视频比例API错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@image_to_videos.route('/image-to-videos/durations', methods=['GET'])
def get_durations_api():
    """获取支持的视频时长范围API端点"""
    try:
        # 获取可用的时长范围
        durations = get_supported_durations()
        
        # 返回成功结果
        return jsonify({
            "status": "success",
            "durations": durations
        })

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"获取视频时长范围API错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500 