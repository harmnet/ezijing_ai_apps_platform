#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台图生视频服务模块
实现基于火山引擎ARK Runtime的图生视频功能

主要功能：
- 支持使用图片和文本提示词生成视频
- 支持视频尺寸比例、时长、分辨率等自定义参数
- 支持任务状态查询和管理
"""

import os
import json
import time
import logging
import uuid
from datetime import datetime
from volcenginesdkarkruntime import Ark
from app.utils.api_key import get_api_key

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置日志文件路径
LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "image_to_video_api_debug.log")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置文件处理器
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 初始化Ark客户端
def get_ark_client():
    """
    初始化并返回Ark客户端实例
    """
    api_key = "01ce33b8-9ca8-4004-81fe-9381504f9752"  # 使用用户提供的API密钥
    logger.info(f"正在初始化Ark客户端，API密钥前5位：{api_key[:5]}...")
    
    try:
        client = Ark(api_key=api_key)
        logger.info("Ark客户端初始化成功")
        return client
    except Exception as e:
        logger.error(f"Ark客户端初始化失败: {str(e)}")
        return None

# ARK模型配置
ARK_MODEL_CONFIG = {
    "model": "doubao-seaweed-241128",  # 图生视频模型ID
}

def create_image_to_video_task(image_url, prompt, ratio="16:9", duration=5.0):
    """
    创建图生视频任务
    
    :param image_url: 图片URL
    :param prompt: 文本提示词
    :param ratio: 视频比例，默认16:9
    :param duration: 视频时长，默认5秒
    :return: 任务创建响应
    """
    logger.info(f"创建图生视频任务: 提示词={prompt}, 视频比例={ratio}, 时长={duration}秒")
    
    # 构造提示词，添加参数
    prompt_with_params = f"{prompt} --ratio {ratio} --dur {duration}"
    
    try:
        # 获取Ark客户端
        client = get_ark_client()
        if client is None:
            return {
                "status": "failed",
                "error": {
                    "message": "Ark客户端初始化失败"
                }
            }
        
        # 创建视频生成任务
        logger.info("发送图生视频请求到火山引擎ARK API")
        create_result = client.content_generation.tasks.create(
            model=ARK_MODEL_CONFIG["model"],
            content=[
                {
                    # 文本提示词与参数组合
                    "type": "text",
                    "text": prompt_with_params
                },
                {
                    # 图片URL
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        )
        
        # 记录创建结果
        logger.info(f"图生视频任务创建成功，任务ID: {create_result.id}")
        
        # 返回标准格式的响应
        return {
            "id": create_result.id,
            "model": ARK_MODEL_CONFIG["model"],
            "status": "running",
            "created_at": int(time.time()),
            "updated_at": int(time.time())
        }
    
    except Exception as e:
        logger.error(f"创建图生视频任务失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "message": f"创建图生视频任务失败: {str(e)}"
            }
        }

def query_video_task(task_id):
    """
    查询视频生成任务的状态
    
    :param task_id: 任务ID
    :return: 任务状态信息
    """
    logger.info(f"查询视频任务状态: 任务ID={task_id}")
    
    try:
        # 获取Ark客户端
        client = get_ark_client()
        if client is None:
            return {
                "status": "failed",
                "error": {
                    "message": "Ark客户端初始化失败"
                }
            }
        
        # 查询任务状态
        logger.info(f"发送查询请求到火山引擎ARK API，任务ID: {task_id}")
        get_result = client.content_generation.tasks.get(task_id=task_id)
        
        # 记录查询结果
        logger.info(f"查询成功，任务状态: {get_result.status}")
        
        # 解析视频URL（如果任务完成）
        video_url = None
        if get_result.status == "succeeded" and get_result.content:
            video_url = get_result.content.video_url
            logger.info(f"任务已完成，视频URL: {video_url}")
        
        # 返回标准格式的响应
        response = {
            "id": task_id,
            "model": ARK_MODEL_CONFIG["model"],
            "status": get_result.status,
            "created_at": get_result.created_at,
            "updated_at": get_result.updated_at
        }
        
        # 如果任务完成，添加内容和使用信息
        if get_result.status == "succeeded" and video_url:
            response["content"] = {"video_url": video_url}
            
            # 如果有使用情况信息，添加到响应中
            if get_result.usage:
                response["usage"] = {
                    "completion_tokens": get_result.usage.completion_tokens,
                    "total_tokens": get_result.usage.completion_tokens,
                }
        
        # 如果任务失败，添加失败原因
        if get_result.status == "failed" and get_result.failure_reason:
            response["failure_reason"] = get_result.failure_reason
        
        return response
    
    except Exception as e:
        logger.error(f"查询视频任务失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "message": f"查询视频任务失败: {str(e)}"
            }
        }

def delete_video_task(task_id):
    """
    删除视频生成任务
    
    :param task_id: 任务ID
    :return: 删除操作结果
    """
    logger.info(f"删除视频任务: 任务ID={task_id}")
    
    try:
        # 获取Ark客户端
        client = get_ark_client()
        if client is None:
            return {
                "status": "failed",
                "error": {
                    "message": "Ark客户端初始化失败"
                }
            }
        
        # 发送删除请求
        logger.info(f"发送删除请求到火山引擎ARK API，任务ID: {task_id}")
        client.content_generation.tasks.delete(task_id=task_id)
        
        # 记录删除成功
        logger.info(f"任务删除成功，任务ID: {task_id}")
        
        # 返回成功响应
        return {
            "status": "success",
            "message": f"任务 {task_id} 已删除"
        }
    
    except Exception as e:
        logger.error(f"删除视频任务失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "message": f"删除视频任务失败: {str(e)}"
            }
        }

def list_video_tasks(page_num=1, page_size=10, status=None, model=None, task_ids=None):
    """
    列出视频生成任务
    
    :param page_num: 页码，默认为1
    :param page_size: 每页大小，默认为10
    :param status: 按状态筛选
    :param model: 按模型筛选
    :param task_ids: 按任务ID筛选
    :return: 任务列表
    """
    logger.info(f"列出视频任务: 页码={page_num}, 每页大小={page_size}, 状态={status}, 模型={model}")
    
    try:
        # 获取Ark客户端
        client = get_ark_client()
        if client is None:
            return {
                "status": "failed",
                "error": {
                    "message": "Ark客户端初始化失败"
                }
            }
        
        # 构造查询参数
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        # 添加可选筛选条件
        if status:
            params["status"] = status
        if model:
            params["model"] = model
        if task_ids:
            params["task_ids"] = task_ids
        
        # 发送查询请求
        logger.info(f"发送任务列表查询请求到火山引擎ARK API，参数: {params}")
        list_result = client.content_generation.tasks.list(**params)
        
        # 记录查询结果
        logger.info(f"任务列表查询成功")
        
        # 将API响应对象转换为可序列化的字典
        # 注意：根据实际API返回的字段名称进行调整
        result_dict = {}
        
        # 添加基本属性
        if hasattr(list_result, 'total'):
            result_dict['total'] = list_result.total
        if hasattr(list_result, 'page_num'):
            result_dict['page_num'] = list_result.page_num
        if hasattr(list_result, 'page_size'):
            result_dict['page_size'] = list_result.page_size
            
        # 添加任务列表，根据实际返回字段名称调整
        tasks = []
        if hasattr(list_result, 'items'):
            # 如果字段名是items
            for task in list_result.items:
                tasks.append({
                    'id': task.id,
                    'model': task.model,
                    'status': task.status,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at
                })
        elif hasattr(list_result, 'data'):
            # 如果字段名是data
            for task in list_result.data:
                tasks.append({
                    'id': task.id,
                    'model': task.model,
                    'status': task.status,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at
                })
        
        result_dict['tasks'] = tasks
        
        # 返回标准格式的响应
        return result_dict
    
    except Exception as e:
        logger.error(f"列出视频任务失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "message": f"列出视频任务失败: {str(e)}"
            }
        }

def get_supported_ratios():
    """
    获取支持的视频比例列表
    :return: 支持的视频比例列表
    """
    return ["16:9", "9:16", "1:1", "4:3", "3:4"]

def get_supported_durations():
    """
    获取支持的视频时长范围
    :return: 支持的视频时长范围
    """
    return {
        "min": 1.0,
        "max": 10.0,
        "default": 5.0
    } 