#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台数字人PPT讲解视频服务接口
实现了对小冰AI Beings API的调用，提供生成PPT讲解视频的功能

主要功能：
- 支持提供PPT文件生成数字人讲解视频
- 支持多种数字人形象选择
- 支持自定义讲解文案
- 支持详细场景和字幕配置
- 支持任务状态查询

官方文档参考：https://aibeings-vip.xiaoice.com/developer-doc/show/155
"""

import os
import json
import requests
import uuid
import time
import logging
import base64
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
import boto3
from botocore.exceptions import NoCredentialsError

# 导入共享的模拟任务存储模块
from app.services.mock_tasks_store import add_task, get_task, update_task, list_tasks

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置日志文件路径
LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "aibeings_api_debug.log")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置文件处理器
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 加载环境变量
load_dotenv()

# 阿里云OSS配置
OSS_CONFIG = {
    "access_key_id": os.getenv("ALIYUN_ACCESS_KEY_ID", ""),
    "access_key_secret": os.getenv("ALIYUN_ACCESS_KEY_SECRET", ""),
    "bucket_name": os.getenv("ALIYUN_OSS_BUCKET", ""),
    "endpoint": os.getenv("ALIYUN_OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com"),
    "region": os.getenv("ALIYUN_REGION", "cn-beijing"),
}

# 小冰AI Beings API配置
AIBEINGS_API_CONFIG = {
    "base_url": "https://openapi.xiaoice.com/vh",  # 根据官方文档更新
    "sub_key": "282cd94b697e48e6aca6d20bbdaf0d0f",  # 用户提供的sub-key
}

# 数字人ID和姿势ID映射表
DEFAULT_VIRTUAL_HUMANS = {
    "default": {
        "virtualHumanId": "VHP3S1EF7",
        "postures": {
            "right": "aMiAX96rMqNS",  # 右侧站立姿势
            "left": "d5nJE6EI0txK"    # 左侧站立姿势
        }
    },
    "business_man": {
        "virtualHumanId": "VHFXQGGVG",
        "postures": {
            "center": "bKnPeXPndZCR"  # 中间站立姿势
        }
    },
    "business_woman": {
        "virtualHumanId": "VHT1NU4H7",
        "postures": {
            "center": "kOBCsOYhcdIi"  # 中间站立姿势
        }
    }
}

# 默认TTS语音配置
DEFAULT_TTS = {
    "voiceId": "101-master-ugdr",
    "rate": 1,
    "pitch": 1,
    "volume": 50
}

# 默认字幕配置
DEFAULT_CAPTION = {
    "topCenter": True,
    "zIndex": 60,
    "attributes": {
        "visible": True,
        "fontColor": "#FFFFFF",
        "spacing": 1,
        "italic": False,
        "underline": False,
        "bold": True,
        "y": 1000,
        "fontSize": 36
    }
}

def upload_to_oss(file_path):
    """
    上传文件到阿里云OSS
    
    :param file_path: 本地文件路径
    :return: 成功返回文件URL，失败返回None
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return None
    
    # 重新从环境变量获取配置
    access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
    bucket_name = os.getenv('ALIYUN_OSS_BUCKET')
    endpoint = os.getenv('ALIYUN_OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
    region = os.getenv('ALIYUN_REGION', 'cn-beijing')
    
    # 安全显示凭证信息
    if access_key_id:
        logger.info(f"OSS Access Key ID: {access_key_id[:5]}... (长度: {len(access_key_id)})")
    else:
        logger.info("OSS Access Key ID: 未设置")
        
    if access_key_secret:
        logger.info(f"OSS Access Key Secret: {access_key_secret[:5]}... (长度: {len(access_key_secret)})")
    else:
        logger.info("OSS Access Key Secret: 未设置")
        
    logger.info(f"OSS Bucket: {bucket_name if bucket_name else '未设置'}")
    logger.info(f"OSS Endpoint: {endpoint}")
    
    # 验证OSS配置
    if not access_key_id or not access_key_secret or not bucket_name:
        logger.error("OSS配置不完整，无法上传")
        return None
    
    # 创建OSS客户端
    try:
        import oss2
        # 使用阿里云OSS SDK代替boto3
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        
        # 生成唯一的文件名
        file_name = os.path.basename(file_path)
        object_name = f"uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
        
        # 上传文件
        logger.info(f"开始上传文件到OSS: {object_name}")
        result = bucket.put_object_from_file(object_name, file_path)
        
        if result.status == 200:
            # 生成文件URL
            file_url = f"https://{bucket_name}.{endpoint}/{object_name}"
            logger.info(f"文件上传成功，URL: {file_url}")
            return file_url
        else:
            logger.error(f"OSS上传失败，状态码: {result.status}")
            return None
            
    except ImportError:
        logger.error("未安装oss2库，尝试使用boto3")
        try:
            # 使用boto3库（可能不支持阿里云OSS的某些特性）
            s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=access_key_secret,
                endpoint_url=f"https://{endpoint}",
                region_name=region,
                config=boto3.session.Config(
                    s3={'addressing_style': 'virtual'}  # 使用虚拟主机样式
                )
            )
            
            # 生成唯一的文件名
            file_name = os.path.basename(file_path)
            object_name = f"uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
            
            # 上传文件
            logger.info(f"开始上传文件到OSS: {object_name}")
            s3_client.upload_file(file_path, bucket_name, object_name)
            
            # 生成文件URL
            file_url = f"https://{bucket_name}.{endpoint}/{object_name}"
            logger.info(f"文件上传成功，URL: {file_url}")
            return file_url
        except NoCredentialsError:
            logger.error("OSS凭证无效")
            return None
        except Exception as e:
            logger.error(f"OSS上传异常: {str(e)}")
            return None
    except Exception as e:
        logger.error(f"OSS上传异常: {str(e)}")
        return None

def upload_file(file_path):
    """
    上传文件到云存储获取URL
    
    :param file_path: 本地文件路径
    :return: 成功返回文件URL，失败返回None
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return None
    
    # 重新从环境变量获取配置
    access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
    bucket_name = os.getenv('ALIYUN_OSS_BUCKET')
    
    # 优先尝试上传到阿里云OSS
    if access_key_id and access_key_secret and bucket_name:
        logger.info("使用阿里云OSS上传文件")
        return upload_to_oss(file_path)
    else:
        # 安全显示凭证信息
        key_id_info = f"{access_key_id[:5]}..." if access_key_id else "未设置"
        secret_length = len(access_key_secret) if access_key_secret else 0
        logger.warning(f"阿里云OSS配置不完整，key_id: {key_id_info}, secret长度: {secret_length}, bucket: {bucket_name or '未设置'}")
    
    # 如果OSS配置不完整，回退到小冰API上传
    logger.info("阿里云OSS配置不完整，尝试使用小冰API上传文件")
    api_url = f"{AIBEINGS_API_CONFIG['base_url']}/video/upload"
    
    # 获取文件名和扩展名
    file_name = os.path.basename(file_path)
    _, file_extension = os.path.splitext(file_name)
    
    # 读取文件内容
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
    except Exception as e:
        logger.error(f"读取文件失败: {str(e)}")
        return None
    
    # 准备上传请求
    headers = {
        "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
    }
    
    # 创建multipart/form-data请求
    files = {
        'file': (file_name, file_content, f'application/{file_extension[1:]}')
    }
    
    try:
        logger.info(f"开始上传文件到小冰API: {file_name}")
        response = requests.post(api_url, headers=headers, files=files)
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"上传结果: {result}")
        
        if result.get("success", False) and "data" in result and "url" in result["data"]:
            file_url = result["data"]["url"]
            logger.info(f"文件上传成功，URL: {file_url}")
            return file_url
        else:
            error_msg = result.get("message", "未知错误")
            logger.error(f"文件上传失败: {error_msg}")
            return None
            
    except Exception as e:
        logger.error(f"文件上传异常: {str(e)}")
        # 模拟上传成功，返回一个假的URL用于测试
        if os.environ.get("MOCK_API", "false").lower() == "true":
            mock_url = f"https://mock-oss.example.com/ppt/{uuid.uuid4().hex}/{file_name}"
            logger.info(f"模拟上传成功，URL: {mock_url}")
            return mock_url
        return None

def get_digital_humans():
    """
    获取可用的数字人列表
    
    :return: 数字人列表
    """
    api_url = f"{AIBEINGS_API_CONFIG['base_url']}/video/queryDigitalEmployee"
    
    headers = {
        "Content-Type": "application/json",
        "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
    }
    
    # 根据官方文档设置请求体
    payload = {
        "categoryList": [],
        "modelType": "STUDIO",
        "pageIndex": 1,
        "pageSize": 50
    }
    
    try:
        logger.info(f"获取数字人列表, API URL: {api_url}")
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"成功获取数字人列表: {len(result.get('data', []))}个数字人")
        return result
    except Exception as e:
        logger.error(f"获取数字人列表失败: {str(e)}")
        # 返回错误结果
        return {
            "status": "failed",
            "error": {
                "message": f"获取数字人列表失败: {str(e)}"
            }
        }

def get_digital_human_postures(virtual_human_id):
    """
    获取指定数字人的可用姿势列表
    
    :param virtual_human_id: 数字人ID
    :return: 姿势列表
    """
    api_url = f"{AIBEINGS_API_CONFIG['base_url']}/video/queryPostureList"
    
    headers = {
        "Content-Type": "application/json",
        "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
    }
    
    # 根据官方文档设置请求体
    payload = {
        "modelId": virtual_human_id
    }
    
    try:
        logger.info(f"获取数字人姿势列表, 数字人ID: {virtual_human_id}")
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"成功获取数字人姿势列表: {len(result.get('data', []))}个姿势")
        return result
    except Exception as e:
        logger.error(f"获取数字人姿势列表失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "message": f"获取数字人姿势列表失败: {str(e)}"
            }
        }

def create_ppt_video_task(
    ppt_file_path, 
    text_script=None, 
    virtual_human_id=None,
    virtual_human_posture_id=None, 
    title="PPT讲解视频",
    resolution="1080p",
    caption_config=None,
    tts_config=None,
    single_page_seconds=5,
    virtual_human_position="right"
):
    """
    创建PPT讲解视频任务
    
    :param ppt_file_path: PPT文件路径
    :param text_script: 讲解文本脚本（可选，不提供则使用PPT备注或自动生成）
    :param virtual_human_id: 数字人ID（可选，不提供则使用默认数字人）
    :param virtual_human_posture_id: 数字人姿势ID（可选，不提供则根据位置使用默认姿势）
    :param title: 视频标题
    :param resolution: 视频分辨率，支持"720p"或"1080p"
    :param caption_config: 字幕配置（可选，不提供则使用默认配置）
    :param tts_config: TTS语音配置（可选，不提供则使用默认配置）
    :param single_page_seconds: 单页PPT显示时间（秒）
    :param virtual_human_position: 数字人位置，支持"left"、"right"、"center"
    :return: 任务创建结果
    """
    # 解析分辨率参数
    if resolution.lower() == "720p":
        width, height = 1280, 720
    else:  # 默认1080p
        width, height = 1920, 1080
    
    # 判断文件类型是否为PPT/PPTX
    file_ext = os.path.splitext(ppt_file_path)[1].lower()
    if file_ext not in ['.ppt', '.pptx']:
        error_msg = f"文件类型不支持，仅支持PPT或PPTX格式: {file_ext}"
        logger.error(error_msg)
        return {
            "status": "failed",
            "error": {
                "message": error_msg
            }
        }
    
    # 上传PPT文件获取URL
    ppt_url = upload_file(ppt_file_path)
    if not ppt_url:
        error_msg = "PPT文件上传失败"
        logger.error(error_msg)
        return {
            "status": "failed",
            "error": {
                "message": error_msg
            }
        }
    
    # 确定使用哪个数字人和姿势
    if not virtual_human_id:
        virtual_human = DEFAULT_VIRTUAL_HUMANS["default"]
        virtual_human_id = virtual_human["virtualHumanId"]
        # 根据位置选择姿势
        if not virtual_human_posture_id:
            if virtual_human_position == "left":
                virtual_human_posture_id = virtual_human["postures"].get("left")
            elif virtual_human_position == "center" and "center" in virtual_human["postures"]:
                virtual_human_posture_id = virtual_human["postures"].get("center")
            else:  # 默认右侧
                virtual_human_posture_id = virtual_human["postures"].get("right")
    
    # 设置数字人位置和大小
    if virtual_human_position == "left":
        virtual_human_attributes = {
            "width": 319,
            "height": 1536,
            "x": -53,
            "y": 346,
            "forceMattingType": 0
        }
    elif virtual_human_position == "center":
        virtual_human_attributes = {
            "width": 400,
            "height": 1080,
            "x": 760,
            "y": 346,
            "forceMattingType": 0
        }
    else:  # 默认右侧
        virtual_human_attributes = {
            "width": 344,
            "height": 1080,
            "x": 1517,
            "y": 309,
            "forceMattingType": 0
        }
    
    # 使用默认TTS配置，如果未提供
    tts = DEFAULT_TTS.copy()
    if tts_config:
        tts.update(tts_config)
    
    # 使用默认字幕配置，如果未提供
    caption = DEFAULT_CAPTION.copy()
    if caption_config:
        # 更新顶层键
        for key in caption_config:
            if key != "attributes":
                caption[key] = caption_config[key]
        
        # 更新属性键
        if "attributes" in caption_config:
            caption["attributes"].update(caption_config["attributes"])
    
    # 构建场景配置
    scene = {
        "virtualHuman": {
            "attributes": virtual_human_attributes,
            "virtualHumanId": virtual_human_id,
            "virtualHumanPostureId": virtual_human_posture_id,
            "zIndex": 20
        },
        "tts": tts,
        "caption": caption
    }
    
    # 如果提供了讲解文本，则添加到场景中
    if text_script:
        scene["voiceText"] = text_script
    
    # 构建完整请求体
    payload = {
        "outputVideoName": title,
        "width": width,
        "height": height,
        "creationDetail": {
            "scenes": [scene],
        },
        "pptInfo": {
            "pptUrl": ppt_url,
            "convertType": "VIDEO",
            "getText": True,  # 从PPT备注获取文本
            "singlePageSecond": single_page_seconds,
            "attributes": {
                "width": width,
                "height": height,
                "x": 0,
                "y": 0
            }
        }
    }
    
    # 发送API请求
    api_url = f"{AIBEINGS_API_CONFIG['base_url']}/video/pptWithModel"
    
    headers = {
        "Content-Type": "application/json",
        "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
    }
    
    try:
        logger.info(f"创建PPT讲解视频任务, API URL: {api_url}")
        logger.info(f"请求参数: 标题={title}, 数字人ID={virtual_human_id}, 分辨率={resolution}, PPT文件={os.path.basename(ppt_file_path)}")
        logger.debug(f"请求体: {json.dumps(payload)}")
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"成功创建PPT讲解视频任务: {result}")
        
        # 如果API返回成功，则添加任务到模拟任务存储
        if result.get("success", False) and "data" in result and "taskId" in result["data"]:
            task_id = result["data"]["taskId"]
            # 存储任务信息，用于后续查询
            task_data = {
                "task_id": task_id,
                "create_time": time.time(),
                "status": "processing",
                "progress": 0,
                "ppt_file": os.path.basename(ppt_file_path),
                "title": title,
                "virtual_human_id": virtual_human_id,
                "api_type": "aibeings_ppt_video"
            }
            add_task(task_data)
            
            # 返回格式化的任务创建结果
            return {
                "task_id": task_id,
                "status": "created",
                "create_time": time.time(),
                "title": title,
                "message": "PPT讲解视频任务创建成功"
            }
        else:
            error_msg = result.get("message", "未知错误") if "message" in result else "API返回结果不包含任务ID"
            logger.error(f"创建PPT讲解视频任务失败: {error_msg}")
            return {
                "status": "failed",
                "error": {
                    "message": error_msg
                }
            }
    except Exception as e:
        logger.error(f"创建PPT讲解视频任务异常: {str(e)}")
        # 创建模拟任务用于测试
        if os.environ.get("MOCK_API", "false").lower() == "true":
            logger.info("启用模拟模式，创建模拟PPT视频任务")
            return create_mock_ppt_video_task(ppt_file_path, text_script, virtual_human_id, title, resolution)
        else:
            return {
                "status": "failed",
                "error": {
                    "message": f"创建PPT讲解视频任务失败: {str(e)}"
                }
            }

def query_ppt_video_task(task_id):
    """
    查询PPT讲解视频任务状态
    
    :param task_id: 任务ID
    :return: 任务状态信息
    """
    # 如果是模拟任务，则使用模拟数据
    if task_id.startswith("mock-"):
        return query_mock_ppt_video_task(task_id)
    
    api_url = f"{AIBEINGS_API_CONFIG['base_url']}/video/task/query"
    
    headers = {
        "Content-Type": "application/json",
        "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
    }
    
    payload = {
        "taskId": task_id
    }
    
    try:
        logger.info(f"查询PPT讲解视频任务状态, 任务ID: {task_id}")
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"成功查询PPT讲解视频任务状态: {result}")
        
        # 检查API返回结果
        if result.get("success", False) and "data" in result:
            task_data = result["data"]
            
            # 任务状态映射
            api_status = task_data.get("status", "")
            # 根据API文档映射状态
            status_mapping = {
                "PENDING": "pending",     # 等待中
                "PROCESSING": "processing", # 处理中
                "FINISHED": "success",    # 完成
                "FAILED": "failed",       # 失败
                "TIMEOUT": "failed"       # 超时
            }
            status = status_mapping.get(api_status, "processing")
            
            # 计算进度
            progress = 0
            if status == "success":
                progress = 100
            elif status == "failed":
                progress = 0
            else:
                progress = task_data.get("progress", 0)
            
            # 更新本地存储的任务
            stored_task = get_task(task_id)
            if stored_task:
                stored_task["status"] = status
                stored_task["progress"] = progress
                if "url" in task_data:
                    stored_task["video_url"] = task_data["url"]
                task_id_to_update = stored_task.pop("task_id", None)
                if task_id_to_update:
                    update_task(task_id_to_update, **stored_task)
            
            # 返回统一格式的任务状态
            response_data = {
                "task_id": task_id,
                "status": status,
                "progress": progress,
                "create_time": stored_task.get("create_time", time.time()) if stored_task else time.time(),
                "message": f"任务状态: {api_status}"
            }
            
            # 如果任务完成，添加视频URL
            if status == "success" and "url" in task_data:
                response_data["video_url"] = task_data["url"]
            
            return response_data
        else:
            error_msg = result.get("message", "未知错误")
            logger.error(f"查询PPT讲解视频任务状态失败: {error_msg}")
            return {
                "status": "failed",
                "error": {
                    "message": error_msg
                }
            }
    except Exception as e:
        logger.error(f"查询PPT讲解视频任务状态异常: {str(e)}")
        # 如果API查询失败，尝试从本地存储获取任务信息
        stored_task = get_task(task_id)
        if stored_task:
            return {
                "task_id": task_id,
                "status": stored_task.get("status", "unknown"),
                "progress": stored_task.get("progress", 0),
                "create_time": stored_task.get("create_time", time.time()),
                "message": "从本地存储获取的任务状态",
                "video_url": stored_task.get("video_url", "")
            }
        else:
            return {
                "status": "failed",
                "error": {
                    "message": f"查询PPT讲解视频任务状态失败且本地无缓存: {str(e)}"
                }
            }

def create_mock_ppt_video_task(ppt_file_path, text_script=None, virtual_human_id=None, title="PPT讲解视频", resolution="1080p"):
    """
    创建一个模拟的PPT讲解视频任务，用于测试或当API不可用时
    
    :param ppt_file_path: PPT文件路径
    :param text_script: 讲解文本脚本
    :param virtual_human_id: 数字人ID
    :param title: 视频标题
    :param resolution: 视频分辨率
    :return: 包含任务ID的响应
    """
    task_id = f"mock-ppt-video-{str(uuid.uuid4())}"
    
    # 创建任务对象
    task = {
        "task_id": task_id,
        "ppt_file": os.path.basename(ppt_file_path),
        "virtual_human_id": virtual_human_id or DEFAULT_VIRTUAL_HUMANS["default"]["virtualHumanId"],
        "title": title,
        "resolution": resolution,
        "create_time": time.time(),
        "status": "pending",
        "progress": 0,
        "api_type": "aibeings_ppt_video"
    }
    
    # 将任务添加到模拟任务存储
    add_task(task)
    
    logger.info(f"创建模拟PPT讲解视频任务成功: {task_id}")
    
    # 返回任务创建结果
    return {
        "task_id": task_id,
        "status": "created",
        "create_time": time.time(),
        "title": title,
        "message": "模拟PPT讲解视频任务创建成功"
    }

def query_mock_ppt_video_task(task_id):
    """
    查询模拟PPT讲解视频任务状态
    
    :param task_id: 任务ID
    :return: 任务状态信息
    """
    task = get_task(task_id)
    
    if not task:
        logger.error(f"模拟任务不存在: {task_id}")
        return {
            "status": "failed",
            "error": {
                "message": f"任务不存在: {task_id}"
            }
        }
    
    # 模拟任务进度更新
    current_time = time.time()
    elapsed_time = current_time - task.get("create_time", current_time)
    
    # 模拟5分钟完成任务
    total_time = 300  # 300秒 = 5分钟
    
    if elapsed_time >= total_time:
        # 任务完成
        task["status"] = "success"
        task["progress"] = 100
        # 模拟视频URL
        if "video_url" not in task:
            task["video_url"] = f"https://example.com/mock-videos/{task_id}.mp4"
        
        # 更新任务状态
        task_id_to_update = task.pop("task_id", None)
        if task_id_to_update:
            update_task(task_id_to_update, **task)
    else:
        # 任务进行中
        progress = min(99, int((elapsed_time / total_time) * 100))
        task["status"] = "processing"
        task["progress"] = progress
        
        # 更新任务状态
        task_id_to_update = task.pop("task_id", None)
        if task_id_to_update:
            update_task(task_id_to_update, **task)
    
    logger.info(f"查询模拟PPT讲解视频任务: {task_id}, 状态: {task['status']}, 进度: {task['progress']}%")
    
    # 构造响应
    response = {
        "task_id": task_id,
        "status": task.get("status", "processing"),
        "progress": task.get("progress", 0),
        "create_time": task.get("create_time", current_time),
        "message": f"模拟任务状态: {task.get('status', 'processing')}"
    }
    
    # 如果任务完成，添加视频URL
    if task.get("status") == "success" and "video_url" in task:
        response["video_url"] = task["video_url"]
    
    return response

def get_supported_resolutions():
    """
    获取支持的视频分辨率
    
    :return: 支持的分辨率列表
    """
    return ["720p", "1080p"]

def get_supported_digital_humans():
    """
    获取支持的数字人列表
    
    :return: 支持的数字人列表
    """
    # 如果API获取失败，返回默认的数字人列表
    default_digital_humans = [
        {"id": DEFAULT_VIRTUAL_HUMANS["default"]["virtualHumanId"], "name": "默认数字人"},
        {"id": DEFAULT_VIRTUAL_HUMANS["business_man"]["virtualHumanId"], "name": "商务男士"},
        {"id": DEFAULT_VIRTUAL_HUMANS["business_woman"]["virtualHumanId"], "name": "商务女士"}
    ]
    
    try:
        # 尝试从API获取最新的数字人列表
        result = get_digital_humans()
        if result and "data" in result and isinstance(result["data"], list):
            return result["data"]
        else:
            logger.warning("获取数字人列表失败，使用默认数字人列表")
            return default_digital_humans
    except Exception as e:
        logger.error(f"获取数字人列表异常: {str(e)}")
        return default_digital_humans 