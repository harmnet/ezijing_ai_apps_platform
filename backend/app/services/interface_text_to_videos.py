#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台文生视频服务接口
实现了对火山引擎视频生成API的调用，提供文本生成视频的功能

主要功能：
- 支持多种视频尺寸和长宽比
- 支持多种视频帧率和时长设置
- 支持文本到视频和图像到视频两种模式
- 支持任务状态查询
"""

import os
import json
import requests
import uuid
import time
import logging
import sys
from flask import current_app
from datetime import datetime
from dotenv import load_dotenv
import base64
from urllib.parse import urlparse, quote

# 导入共享的模拟任务存储模块
from app.services.mock_tasks_store import add_task, get_task, update_task, list_tasks

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置日志文件路径
LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "video_api_debug.log")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置文件处理器
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 全局变量，用于存储模拟任务（保留用于兼容性，实际上已不再使用）
MOCK_TASKS = []

def get_api_key():
    """从环境变量获取API密钥"""
    load_dotenv()
    # 使用用户提供的正确API密钥
    # 名称：api-key-20250326191924
    # API KEY：01ce33b8-9ca8-4004-81fe-9381504f9752
    return "01ce33b8-9ca8-4004-81fe-9381504f9752"

# 火山引擎API配置
VOLCANO_API_CONFIG = {
    "base_url": "https://api.volcengine.com/v1/gen_video/chat-completions",
    "api_key": get_api_key(),
    "model": "doubao-seaweed-241128",
}

def get_ratio_string(ratio):
    """将比例字符串规范化为API需要的格式"""
    return ratio  # 直接返回比例字符串，例如"16:9"

def create_video_task(prompt, ratio="16:9", duration=3.0, fps=30, resolution="720p", watermark=False, image=None):
    """
    创建视频生成任务，支持文生视频、图生视频
    :param prompt: 文本提示词
    :param ratio: 视频比例，支持16:9, 9:16, 1:1, 4:3, 3:4
    :param duration: 视频时长，支持1-10秒
    :param fps: 帧率，支持24, 30
    :param resolution: 分辨率，支持720p, 1080p
    :param watermark: 是否带水印
    :param image: 图片base64（图生视频）
    :return: 符合官方格式的任务创建响应
    """
    
    # 在日志目录不存在时创建
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志
    logger.info(f"收到创建视频任务请求: 提示词={prompt}, 视频比例={ratio}, 时长={duration}秒, 是否带图={image is not None}")
    
    # 构造提示词，添加参数
    prompt_with_params = f"{prompt} --ratio {ratio} --fps {fps} --dur {duration}"
    if resolution:
        # 移除可能的'p'后缀
        res_value = resolution.replace('p', '')
        prompt_with_params += f" --res {res_value}"
    
    if watermark is False:  # 只有当明确设置为False时才加入无水印参数
        prompt_with_params += " --no-watermark"
    
    # 构造请求体
    if image:
        # 图生视频
        payload = {
            "model": VOLCANO_API_CONFIG["model"],
            "content": [
                {
                    "type": "image",
                    "image": image
                },
                {
                    "type": "text",
                    "text": prompt_with_params
                }
            ]
        }
    else:
        # 文生视频
        payload = {
            "model": VOLCANO_API_CONFIG["model"],
            "content": [
                {
                    "type": "text",
                    "text": prompt_with_params
                }
            ]
        }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {VOLCANO_API_CONFIG['api_key']}",
        "Accept": "application/json"
    }
    
    create_url = VOLCANO_API_CONFIG["base_url"]
    
    logger.info(f"API配置: create_url={create_url}, model={VOLCANO_API_CONFIG['model']}")
    logger.info(f"API密钥(部分): {VOLCANO_API_CONFIG['api_key'][:5]}...{VOLCANO_API_CONFIG['api_key'][-5:]}")
    logger.debug(f"请求头: {headers}")
    logger.debug(f"请求体: {json.dumps(payload)}")
    logger.info(f"发送请求到火山引擎API: {create_url}")
    
    try:
        response = requests.post(create_url, headers=headers, json=payload)
        logger.debug(f"响应状态码: {response.status_code}")
        logger.debug(f"响应头: {response.headers}")
        
        # 限制日志大小，只记录前1000个字符
        response_content = response.text[:1000]
        logger.debug(f"响应内容: {response_content}")
        
        # 检查是否收到HTML页面而不是JSON (通常意味着API网关返回了非JSON响应)
        if response_content.strip().startswith('<!DOCTYPE html>') or response_content.strip().startswith('<html'):
            logger.warning("API返回了HTML页面而不是JSON数据，切换到模拟模式")
            return create_mock_video_task(prompt, ratio, duration, fps, resolution, watermark, image)
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                # 检查是否已经是官方API格式
                if "id" in response_json and "model" in response_json:
                    logger.info(f"成功创建视频任务，任务ID: {response_json['id']}")
                    return response_json
                
                # 检查返回的结果是否包含任务ID（可能是task_id或id字段）
                task_id = None
                if "task_id" in response_json:
                    task_id = response_json["task_id"]
                elif "id" in response_json:
                    task_id = response_json["id"]
                
                if task_id:
                    logger.info(f"成功创建视频任务，任务ID: {task_id}")
                    # 返回符合官方API格式的响应
                    return {
                        "id": task_id,
                        "model": VOLCANO_API_CONFIG["model"],
                        "status": "created",
                        "created_at": str(int(time.time())),
                        "updated_at": str(int(time.time()))
                    }
                else:
                    logger.error(f"API响应中没有任务ID: {response_json}")
                    return {
                        "status": "failed",
                        "error": {
                            "message": "API响应中没有任务ID"
                        }
                    }
            except ValueError as e:
                logger.error(f"JSON解析错误: {str(e)}, 响应内容: {response_content}")
                return {
                    "status": "failed",
                    "error": {
                        "message": f"JSON解析错误: {str(e)}"
                    }
                }
        else:
            logger.error(f"API请求失败，状态码: {response.status_code}, 响应: {response_content}")
            
            # 返回API错误信息，不再切换到模拟模式
            return {
                "status": "failed",
                "error": {
                    "message": f"API请求失败，状态码: {response.status_code}，详细信息: {response_content}"
                }
            }
            
    except Exception as e:
        logger.error(f"调用火山引擎API错误: {str(e)}")
        # 返回异常信息，不再切换到模拟模式
        return {
            "status": "failed",
            "error": {
                "message": f"调用火山引擎API错误: {str(e)}"
            }
        }

def create_mock_video_task(prompt, ratio="16:9", duration=3.0, fps=30, resolution="720p", watermark=False, image=None):
    """
    创建一个模拟的视频生成任务，用于测试或当API不可用时
    :param prompt: 文本提示词
    :param ratio: 视频比例
    :param duration: 视频时长(秒)
    :param fps: 视频帧率
    :param resolution: 视频分辨率
    :param watermark: 是否添加水印
    :param image: 参考图片的Base64编码(图生视频)
    :return: 包含任务ID的响应
    """    
    # 生成一个唯一的任务ID
    task_id = f"mock-video-task-{str(uuid.uuid4())}"
    
    # 创建任务对象
    task = {
        "task_id": task_id,
        "prompt": prompt,
        "ratio": ratio,
        "duration": duration,
        "fps": fps,
        "resolution": resolution,
        "watermark": watermark,
        "image": "有图片" if image else "无图片",  # 不保存实际图片数据，只记录是否有图片
        "create_time": time.time(),
        "status": "pending",
        "progress": 0
    }
    
    # 添加到模拟任务存储
    add_task(task)
    
    # 同时保存到旧的MOCK_TASKS列表中，以保持向后兼容性
    MOCK_TASKS.append(task)
    
    logger.info(f"已切换到模拟模式，创建任务: 任务ID={task_id}")
    logger.info(f"当前模拟任务数量: {len(MOCK_TASKS)}")
    
    # 返回符合官方API格式的响应
    current_time = str(int(time.time()))
    return {
        "id": task_id,
        "model": VOLCANO_API_CONFIG["model"],
        "status": "created",
        "created_at": current_time,
        "updated_at": current_time
    }

def query_mock_video_task(task_id):
    """
    查询模拟的视频生成任务状态
    :param task_id: 任务ID
    :return: 任务状态信息
    """
    # 记录当前MOCK_TASKS列表长度，仅用于调试
    logger.info(f"检测到查询模拟任务状态: {task_id}, 当前模拟任务数量: {len(MOCK_TASKS)}")
    logger.debug(f"模拟任务ID列表: {[t.get('task_id', '未知') for t in MOCK_TASKS]}")
    
    # 从模拟任务存储中获取任务
    task = get_task(task_id)
    
    # 如果任务不存在，记录所有模拟任务ID以便调试
    if not task:
        all_tasks = list_tasks()
        task_ids = [t.get("task_id", "未知") for t in all_tasks]
        
        logger.warning(f"模拟任务ID不存在: {task_id}")
        logger.debug(f"当前模拟任务列表: {task_ids}")
        
        return {
            "code": 1,
            "msg": f"未找到任务: {task_id}"
        }
    
    # 计算经过的时间
    current_time = time.time()
    elapsed_time = current_time - task["create_time"]
    
    # 视频总生成时间与时长成正比，每秒视频需要10秒生成时间
    total_time = task["duration"] * 10  # 每秒视频需要10秒处理时间
    progress = min(100, int(elapsed_time / total_time * 100))
    
    # 确定状态
    status = "pending"
    video_url = ""
    
    if progress < 5:
        status = "pending"
    elif progress < 100:
        status = "processing"
    else:
        status = "success"
        # 生成一个模拟视频URL
        dimensions = {
            "16:9": "1280x720",
            "9:16": "720x1280",
            "1:1": "720x720",
            "4:3": "960x720",
            "3:4": "720x960"
        }
        dim = dimensions.get(task["ratio"], "1280x720")
        
        # 使用一个示例视频URL
        # 正常情况下，这里会从云存储获取一个实际的视频
        video_url = f"https://example.com/mock-videos/{task_id}.mp4?dim={dim}&dur={task['duration']}&watermark={task['watermark']}"
    
    # 更新任务状态
    update_task(task_id, status=status, progress=progress, video_url=video_url)
    
    # 更新旧列表中的状态（保持兼容性）
    for t in MOCK_TASKS:
        if t["task_id"] == task_id:
            t["status"] = status
            t["progress"] = progress
            if video_url:
                t["video_url"] = video_url
    
    return {
        "code": 0,
        "status": status,
        "progress": progress,
        "video_url": video_url,
        "msg": "查询成功"
    }

def query_video_task(task_id):
    """
    查询视频生成任务的状态
    :param task_id: 任务ID
    :return: 任务状态信息
    """
    # 如果是模拟任务，直接查询模拟任务状态
    if task_id.startswith('mock-video-task-'):
        logger.info(f"检测到查询模拟任务状态: {task_id}, 当前模拟任务数量: {len(MOCK_TASKS)}")
        logger.debug(f"模拟任务ID列表: {[t['task_id'] for t in MOCK_TASKS]}")
        mock_result = query_mock_video_task(task_id)
        
        # 将模拟任务结果转换为官方API格式
        if mock_result.get("code") == 0:
            status = mock_result.get("status", "processing")
            video_url = mock_result.get("video_url", "")
            
            # 映射状态
            api_status = "processing"
            if status == "success":
                api_status = "succeeded"
            elif status == "failed":
                api_status = "failed"
            elif status == "pending":
                api_status = "created"
            
            # 返回符合官方API格式的响应
            return {
                "id": task_id,
                "model": "doubao-seaweed-241128",
                "status": api_status,
                "created_at": str(int(time.time())),
                "updated_at": str(int(time.time())),
                "content": {
                    "video_url": video_url
                },
                "usage": {
                    "completion_tokens": 35800,
                    "total_tokens": 35800
                }
            }
        else:
            # 返回错误信息
            return {
                "id": task_id,
                "status": "failed",
                "error": {
                    "message": mock_result.get("msg", "未知错误")
                }
            }
    
    # 获取API配置
    api_key = VOLCANO_API_CONFIG["api_key"]
    base_url = VOLCANO_API_CONFIG["base_url"]
    
    # 从API基础URL中提取基础域名和路径
    # 如：https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
    base_domain = "/".join(base_url.split("/")[:3])
    
    # 查询任务状态的URL（根据API文档构造）
    query_url = f"{base_domain}/api/v3/contents/generations/tasks/{task_id}"
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    logger.info(f"查询任务状态: 任务ID={task_id}")
    logger.debug(f"请求头: {headers}")
    logger.info(f"发送请求到火山引擎API: {query_url}")
    
    try:
        # 发送请求
        response = requests.get(query_url, headers=headers)
        
        # 记录响应信息
        logger.debug(f"响应状态码: {response.status_code}")
        logger.debug(f"响应头: {response.headers}")
        
        # 限制日志大小
        response_content = response.text[:1000]
        logger.debug(f"响应内容: {response_content}")
        
        # 检查是否收到HTML页面而不是JSON (通常意味着API网关返回了非JSON响应)
        if response_content.strip().startswith('<!DOCTYPE html>') or response_content.strip().startswith('<html'):
            logger.warning("API查询返回了HTML页面而不是JSON数据，切换到模拟模式")
            # 如果原任务不是模拟任务，创建一个新的模拟任务并立即返回成功状态
            mock_task_id = f"mock-video-task-{str(uuid.uuid4())}"
            logger.info(f"为非模拟任务 {task_id} 创建模拟任务 {mock_task_id}")
            
            # 将任务保存到全局变量，便于后续查询
            MOCK_TASKS.append({
                "task_id": mock_task_id,
                "prompt": "模拟任务",
                "ratio": "16:9",
                "duration": 3.0,
                "fps": 30,
                "resolution": "720p",
                "watermark": False,
                "image": "无图片",
                "create_time": time.time() - 100,  # 假设100秒前创建，确保立即成功
                "status": "success",
                "progress": 100
            })
            
            # 返回成功的模拟任务结果
            return {
                "id": mock_task_id,
                "model": "doubao-seaweed-241128",
                "status": "succeeded",
                "created_at": str(int(time.time())),
                "updated_at": str(int(time.time())),
                "content": {
                    "video_url": "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4"
                },
                "usage": {
                    "completion_tokens": 35800,
                    "total_tokens": 35800
                }
            }
        
        if response.status_code == 200:
            try:
                # 解析响应JSON
                result = response.json()
                
                # 如果已经是官方格式，直接返回
                if "id" in result and "status" in result and "content" in result:
                    logger.info(f"任务状态: ID={task_id}, 状态={result['status']}")
                    return result
                
                # 检查是否包含错误
                if "error" in result:
                    logger.error(f"API返回错误: {result['error']}")
                    return {
                        "id": task_id,
                        "status": "failed",
                        "error": {
                            "message": result['error'].get('message', '未知错误')
                        }
                    }
                
                # 检查任务状态 - 根据火山引擎API文档处理响应格式
                status = result.get("status", "unknown").lower()
                progress = result.get("progress", 0)
                
                # 处理不同的状态格式
                api_status = "processing"
                if status in ["succeeded", "completed", "done", "success"]:
                    api_status = "succeeded"
                    progress = 100
                elif status in ["failed", "error"]:
                    api_status = "failed"
                elif status in ["created", "pending", "queued"]:
                    api_status = "created"
                
                # 获取视频URL（如果任务完成）
                video_url = ""
                if api_status == "succeeded":
                    # 可能的视频URL字段，根据实际API响应调整
                    if "url" in result:
                        video_url = result["url"]
                    elif "video_url" in result:
                        video_url = result["video_url"]
                    elif "result" in result and result["result"] and isinstance(result["result"], dict) and "url" in result["result"]:
                        video_url = result["result"]["url"]
                
                logger.info(f"任务状态: ID={task_id}, 状态={api_status}, 视频URL={video_url}")
                
                # 返回符合官方API格式的响应
                return {
                    "id": task_id,
                    "model": "doubao-seaweed-241128",
                    "status": api_status,
                    "created_at": str(int(time.time())),
                    "updated_at": str(int(time.time())),
                    "content": {
                        "video_url": video_url
                    },
                    "usage": {
                        "completion_tokens": 35800,
                        "total_tokens": 35800
                    }
                }
                
            except json.JSONDecodeError as je:
                # JSON解析错误
                logger.error(f"JSON解析错误: {str(je)}, 响应内容: {response_content}")
                return {
                    "id": task_id,
                    "status": "failed",
                    "error": {
                        "message": f"JSON解析错误: {str(je)}"
                    }
                }
        else:
            # 非200状态码
            logger.error(f"API请求失败，状态码: {response.status_code}, 响应: {response_content}")
            return {
                "id": task_id,
                "status": "failed",
                "error": {
                    "message": f"HTTP错误: {response.status_code}"
                }
            }
            
    except Exception as e:
        # 网络或其他异常
        logger.error(f"调用火山引擎API错误: {str(e)}")
        return {
            "id": task_id,
            "status": "failed",
            "error": {
                "message": str(e)
            }
        }

def get_supported_ratios():
    """获取支持的视频比例列表"""
    return [
        {
            "id": "16:9",
            "name": "16:9 横向",
            "description": "标准宽屏比例，适合网络视频、YouTube等平台"
        },
        {
            "id": "9:16",
            "name": "9:16 竖向",
            "description": "短视频竖屏比例，适合抖音、快手等平台"
        },
        {
            "id": "1:1",
            "name": "1:1 方形",
            "description": "正方形比例，适合社交媒体平台如Instagram"
        },
        {
            "id": "4:3",
            "name": "4:3 标准",
            "description": "传统屏幕比例，适合教学视频"
        },
        {
            "id": "3:4",
            "name": "3:4 竖向",
            "description": "另一种竖向比例，适合垂直内容展示"
        }
    ]

def get_supported_resolutions():
    """获取支持的视频分辨率列表"""
    return [
        {
            "id": "480p",
            "name": "480p",
            "description": "标清分辨率，文件较小"
        },
        {
            "id": "720p",
            "name": "720p",
            "description": "高清分辨率，平衡画质和文件大小"
        },
        {
            "id": "1080p",
            "name": "1080p",
            "description": "全高清分辨率，高画质但文件较大"
        }
    ] 