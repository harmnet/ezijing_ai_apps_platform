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

# 也尝试V2版本的API路径
API_PATHS = {
    "query_digital_employee": [
        "/openapi/video/queryDigitalEmployee", # 已知可用的正确路径
        "/video/queryDigitalEmployee",      # 原始路径
        "/v2/video/queryDigitalEmployee",   # 可能的路径2
        "/video/v2/queryDigitalEmployee",   # 可能的路径3
        "/video/query_digital_employee"     # 可能的路径4
    ],
    "detail_digital_employee": [
        "/openapi/video/detailDigitalEmployee", # 根据用户提供的路径
        "/video/detailDigitalEmployee",         # 可能的路径1
        "/v2/video/detailDigitalEmployee",      # 可能的路径2
        "/video/v2/detailDigitalEmployee",      # 可能的路径3
    ],
    "query_posture_list": [
        "/openapi/video/queryPostureList",  # 对应正确的模式
        "/video/queryPostureList",          # 原始路径
        "/v2/video/queryPostureList",       # 可能的路径2
        "/video/v2/queryPostureList",       # 可能的路径3
        "/video/query_posture_list"         # 可能的路径4
    ],
    "query_voice_list": [
        "/openapi/customize/zero/voice-list",    # 根据用户提供的路径
        "/customize/zero/voice-list",            # 可能的路径1
        "/customize/voice-list",                 # 可能的路径2
        "/voice/list",                           # 可能的路径3
        "openapi/customize/zero/voice-list",     # 无前导斜杠版本
        "customize/zero/voice-list",             # 无前导斜杠版本
        "customize/voice-list",                  # 无前导斜杠版本
        "voice/list"                             # 无前导斜杠版本
    ]
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
    "voiceId": "181-0319jiaying-8W3y",
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
    上传文件到阿里云OSS存储获取URL
    
    :param file_path: 本地文件路径
    :return: 成功返回文件URL，失败返回None
    """
    logger.info(f"开始OSS上传流程，文件路径: {file_path}")
    
    # 首先检查文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"要上传的文件不存在: {file_path}")
        return None
        
    # 从环境变量获取OSS配置
    access_key_id = os.environ.get('ALIYUN_ACCESS_KEY_ID')
    access_key_secret = os.environ.get('ALIYUN_ACCESS_KEY_SECRET')
    bucket_name = os.environ.get('ALIYUN_OSS_BUCKET', 'ezijingai')
    endpoint = os.environ.get('ALIYUN_OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
    region = "cn-beijing"  # 默认区域
    
    # 打印OSS配置信息（去除敏感信息）
    logger.info(f"OSS配置: Access Key ID 前缀: {access_key_id[:4] if access_key_id else 'None'}")
    logger.info(f"OSS Bucket: {bucket_name}, Endpoint: {endpoint}")
    
    # 检查是否在开发模式
    dev_mode = os.environ.get('DEV_MODE', 'false').lower() == 'true'
    if dev_mode:
        logger.info("开发模式：模拟OSS上传")
        file_name = os.path.basename(file_path)
        mock_url = f"https://mock-{bucket_name}.{endpoint}/dev-uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
        logger.info(f"模拟上传成功，返回URL: {mock_url}")
        return mock_url
    
    # 如果OSS配置不完整，尝试使用默认值（仅用于开发测试）
    if not access_key_id:
        logger.warning("从环境变量获取Access Key ID失败，使用默认测试值")
        access_key_id = "LTAI5tMVdYzk5fVrmjQVk1Ga"  # 测试用
    
    if not access_key_secret:
        logger.warning("从环境变量获取Access Key Secret失败，使用默认测试值")
        access_key_secret = "OKUYiiO9WOw5bJpRTfJa7F76Ayygdk"  # 测试用
    
    # 创建OSS客户端
    try:
        logger.info("初始化OSS客户端")
        import oss2
        # 使用阿里云OSS SDK
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        
        # 获取文件基本信息
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1].lower()
        
        logger.info(f"准备上传文件: {file_name}, 大小: {file_size} 字节, 扩展名: {file_extension}")
        
        # 生成唯一的文件名
        object_name = f"uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
        
        # 针对PPT文件设置特殊的Content-Type
        headers = {}
        if file_extension == '.ppt' or file_extension == '.pptx':
            if file_extension == '.ppt':
                headers['Content-Type'] = 'application/vnd.ms-powerpoint'
            else:
                headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            logger.info(f"设置PPT文件Content-Type: {headers.get('Content-Type')}")
        
        # 上传文件
        logger.info(f"开始上传文件到OSS路径: {object_name}")
        
        # 使用异常处理增强健壮性
        try:
            # 使用带有特定头信息的上传方法
            if headers:
                result = bucket.put_object_from_file(object_name, file_path, headers=headers)
            else:
                result = bucket.put_object_from_file(object_name, file_path)
            
            logger.info(f"OSS上传完成，状态码: {result.status}")
            
            if result.status == 200:
                # 生成文件URL
                file_url = f"https://{bucket_name}.{endpoint}/{object_name}"
                logger.info(f"文件上传成功，URL: {file_url}")
                return file_url
            else:
                logger.error(f"OSS上传失败，返回状态码非200: {result.status}")
                return None
        except oss2.exceptions.OssError as oe:
            logger.error(f"OSS操作错误: {oe.code}, {oe.message}")
            return None
        except IOError as io_err:
            logger.error(f"文件IO错误: {str(io_err)}")
            return None
            
    except ImportError:
        logger.error("未安装oss2库，尝试使用boto3")
        try:
            # 尝试使用boto3库
            import boto3
            from botocore.exceptions import NoCredentialsError
            
            # 初始化S3客户端（用于访问阿里云OSS）
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
            
            # 准备上传参数
            upload_args = {
                'Bucket': bucket_name,
                'Key': object_name,
                'Filename': file_path
            }
            
            # 为PPT文件设置Content-Type
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension == '.ppt':
                upload_args['ContentType'] = 'application/vnd.ms-powerpoint'
            elif file_extension == '.pptx':
                upload_args['ContentType'] = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            
            # 上传文件
            logger.info(f"使用boto3上传文件到OSS: {object_name}")
            s3_client.upload_file(**upload_args)
            
            # 生成文件URL
            file_url = f"https://{bucket_name}.{endpoint}/{object_name}"
            logger.info(f"使用boto3上传成功，URL: {file_url}")
            return file_url
        except NoCredentialsError:
            logger.error("OSS凭证无效")
            return None
        except Exception as e:
            logger.exception(f"使用boto3上传文件异常: {str(e)}")
            return None
    except Exception as e:
        logger.exception(f"OSS上传过程中发生未预期的异常: {str(e)}")
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
    # 尝试各种可能的API路径
    headers = {
        "Content-Type": "application/json",
        "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
    }
    
    # 根据最新的官方文档设置请求体
    payload = {
        "categoryList": [],
        "modelType": "STUDIO",
        "pageIndex": 1,  # 从第1页开始
        "pageSize": 50   # 每页50条数据
    }
    
    # 尝试所有可能的API路径
    last_error = None
    for path in API_PATHS["query_digital_employee"]:
        api_url = f"{AIBEINGS_API_CONFIG['base_url']}{path}"
        try:
            logger.info(f"尝试API路径: {api_url}")
            logger.info(f"请求头: {headers}")
            logger.info(f"请求参数: {payload}")
            
            # 发送请求到实际API
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"成功获取数字人列表: {result}")
            
            # 检查结果格式
            if "data" in result and "records" in result["data"]:
                logger.info(f"成功获取数字人列表: {len(result['data']['records'])}个数字人")
            else:
                logger.warning(f"数字人列表返回格式不符合预期: {result}")
                
            return result
        except Exception as e:
            logger.warning(f"API路径 {api_url} 失败: {str(e)}")
            last_error = str(e)
            continue
    
    # 所有API路径都失败
    logger.error(f"所有API路径尝试失败，最后一个错误: {last_error}")
    return {
        "status": "failed",
        "error": {
            "message": f"获取数字人列表失败: {last_error}"
        }
    }

def get_digital_human_postures(virtual_human_id):
    """
    获取指定数字人的可用姿势列表
    
    :param virtual_human_id: 数字人ID
    :return: 姿势列表
    """
    headers = {
        "Content-Type": "application/json",
        "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
    }
    
    # 根据官方文档设置请求体
    payload = {
        "modelId": virtual_human_id
    }
    
    # 尝试所有可能的API路径
    last_error = None
    for path in API_PATHS["query_posture_list"]:
        api_url = f"{AIBEINGS_API_CONFIG['base_url']}{path}"
        try:
            logger.info(f"获取数字人姿势列表, 数字人ID: {virtual_human_id}, 尝试API路径: {api_url}")
            
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"成功获取数字人姿势列表: {result}")
            
            # 检查结果格式
            if "data" in result:
                logger.info(f"成功获取数字人姿势列表: {len(result.get('data', []))}个姿势")
            else:
                logger.warning(f"数字人姿势列表返回格式不符合预期: {result}")
                
            return result
        except Exception as e:
            logger.warning(f"API路径 {api_url} 失败: {str(e)}")
            last_error = str(e)
            continue
    
    # 所有API路径都失败
    logger.error(f"获取数字人姿势列表失败: {last_error}")
    return {
        "status": "failed",
        "error": {
            "message": f"获取数字人姿势列表失败: {last_error}"
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
        return {
            "status": "failed",
            "error": {
                "message": f"创建PPT讲解视频任务失败: {str(e)}"
            }
        }

def query_ppt_video_task(task_id):
    """
    查询PPT讲解视频任务状态
    
    Args:
        task_id (str): 任务ID
        
    Returns:
        dict: 任务状态信息
    """
    try:
        logger.info(f"查询PPT讲解视频任务状态, 任务ID: {task_id}")
        
        # 构建API请求URL，使用查询参数
        api_url = f"{AIBEINGS_API_CONFIG['base_url']}/openapi/video/task/v2/detail?taskId={task_id}"
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
        }
        
        logger.info(f"查询任务状态，请求URL: {api_url}")
        
        # 使用GET方法查询任务状态
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"查询PPT讲解视频任务状态响应: {result}")
        
        # 检查API返回结果 - 小冰API成功状态码是200
        if result.get("code") != 200:
            error_code = result.get("code", "未知错误码")
            error_msg = result.get("message", "未知错误")
            logger.error(f"查询PPT讲解视频任务状态失败: 错误码={error_code}, 错误信息={error_msg}")
            return {
                "status": "FAILED",
                "progress": 0,
                "error_message": f"API错误: {error_msg}",
                "raw_response": result
            }
        
        # 从响应中提取data部分
        data = result.get("data", {})
        
        # 直接获取任务状态
        task_status = data.get("status", "")
        logger.info(f"任务状态: {task_status}")
        
        # 状态映射
        if task_status == "finished":
            status = "COMPLETED"
            progress = 100
        elif task_status == "failed":
            status = "FAILED"
            progress = 0
        elif task_status == "processing":
            status = "RUNNING"
            # 获取进度
            progress_value = data.get("progress", 0)
            if isinstance(progress_value, float) and progress_value <= 1:
                progress = int(progress_value * 100)
            else:
                progress = int(progress_value)
        else:
            status = "PENDING"
            progress = 0
                
        # 构建响应数据
        response_data = {
            "status": status,
            "progress": progress,
            "created_at": data.get("createTime"),
            "updated_at": data.get("finishTime") or data.get("updateTime"),
            "raw_response": result
        }
        
        # 如果任务已完成，添加输出URL
        if status == "COMPLETED":
            response_data["output_url"] = data.get("videoUrl", "")
            response_data["thumbnail_url"] = data.get("videoThumbnailImageUrl", "")
            response_data["video_size"] = data.get("videoSizeBytes", 0)
            response_data["video_duration"] = data.get("videoDurationMilliseconds", 0)
            
        # 如果任务失败，添加错误信息
        if status == "FAILED":
            response_data["error_message"] = data.get("error", "未知错误")
            
        return response_data
            
    except Exception as e:
        logger.exception(f"查询PPT讲解视频任务状态异常: {str(e)}")
        return {
            "status": "error",
            "error": {
                "message": f"查询任务异常: {str(e)}"
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

def get_voice_list():
    """
    获取TTS语音列表
    
    :return: 语音列表数据或错误信息
    """
    try:
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "subscription-key": AIBEINGS_API_CONFIG["sub_key"],
            "Accept": "application/json"
        }
        
        # 使用已验证有效的API路径
        api_url = f"{AIBEINGS_API_CONFIG['base_url']}/openapi/customize/zero/voice-list"
        
        logger.info(f"获取语音列表，使用GET方法访问: {api_url}")
        logger.info(f"请求头: {headers}")
        
        # 发送GET请求到实际API
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        # 检查结果格式并记录
        if "data" in result and isinstance(result["data"], list):
            logger.info(f"成功获取语音列表: {len(result['data'])}个语音")
        else:
            logger.warning(f"语音列表返回格式不符合预期: {result}")
        
        return result
    except Exception as e:
        logger.error(f"获取语音列表失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "message": f"获取语音列表失败: {str(e)}"
            }
        }

def get_digital_human_detail(biz_id):
    """
    获取数字人详情信息
    
    :param biz_id: 数字人业务ID
    :return: 数字人详情数据或错误信息
    """
    if not biz_id:
        logger.error("获取数字人详情失败: 数字人ID不能为空")
        return {
            "status": "failed",
            "error": {
                "message": "数字人ID不能为空"
            }
        }
    
    try:
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "subscription-key": AIBEINGS_API_CONFIG["sub_key"]
        }
        
        # 设置请求参数
        payload = {
            "bizId": biz_id
        }
        
        # 尝试所有可能的API路径
        last_error = None
        for path in API_PATHS["detail_digital_employee"]:
            api_url = f"{AIBEINGS_API_CONFIG['base_url']}{path}"
            try:
                logger.info(f"尝试获取数字人详情，API路径: {api_url}")
                logger.info(f"请求头: {headers}")
                logger.info(f"请求参数: {payload}")
                
                # 发送请求到实际API
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"成功获取数字人详情: {result}")
                
                # 检查结果格式和状态码
                if result.get("code") == 200 and "data" in result:
                    logger.info(f"成功获取数字人 {biz_id} 的详情")
                    
                    # 记录一些关键信息用于调试
                    if "data" in result:
                        data = result["data"]
                        logger.info(f"虚拟人ID: {data.get('virtualHumanId', '未知')}")
                        logger.info(f"是否支持透明背景: {data.get('supportTransparency', False)}")
                        
                        # 记录语音信息
                        voice_infos = data.get("voiceInfos", [])
                        logger.info(f"支持的语音数量: {len(voice_infos)}")

                        # 获取数字人支持的语音ID
                        supported_voice_ids = data.get("supportedVoiceIds", [])
                        
                        # 如果没有直接返回支持的语音ID，且有语音列表，尝试获取支持的语音ID
                        if not supported_voice_ids and voice_infos:
                            # 尝试从数字人配置中提取支持的语音ID
                            if "voiceConfig" in data and "supportedVoiceIds" in data["voiceConfig"]:
                                supported_voice_ids = data["voiceConfig"]["supportedVoiceIds"]
                                logger.info(f"从voiceConfig中获取到支持的语音ID: {supported_voice_ids}")
                            elif "supportList" in data and "voices" in data["supportList"]:
                                supported_voice_ids = [voice.get("id") for voice in data["supportList"]["voices"] if "id" in voice]
                                logger.info(f"从supportList中获取到支持的语音ID: {supported_voice_ids}")
                            
                        # 如果有支持的语音ID列表，进行匹配
                        if supported_voice_ids:
                            logger.info(f"数字人支持的语音ID: {supported_voice_ids}")
                            # 确保数据中添加supportedVoiceIds字段，便于前端过滤
                            data["supportedVoiceIds"] = supported_voice_ids
                        
                        # 记录姿势信息
                        posture_infos = data.get("postureInfos", [])
                        logger.info(f"支持的姿势数量: {len(posture_infos)}")
                    
                    # 获取语音列表
                    if "data" in result and not result["data"].get("voiceInfos"):
                        try:
                            # 获取所有语音列表
                            voice_list_result = get_voice_list()
                            if voice_list_result and "data" in voice_list_result and isinstance(voice_list_result["data"], list):
                                result["data"]["voiceInfos"] = voice_list_result["data"]
                                logger.info(f"获取语音列表成功，添加到数字人详情")
                        except Exception as ve:
                            logger.error(f"获取语音列表失败: {str(ve)}")
                    
                    return result
                else:
                    error_msg = result.get("message", "未知错误")
                    logger.warning(f"API返回非成功状态码: {result.get('code')}, 消息: {error_msg}")
                    
                    # 如果是业务逻辑错误，也返回结果，如ID不存在等
                    if "data" in result or result.get("code") != 500:
                        return result
                    
                    last_error = f"API返回错误: {error_msg}"
                    continue
            except Exception as e:
                logger.warning(f"API路径 {api_url} 失败: {str(e)}")
                last_error = str(e)
                continue
        
        # 所有API路径都失败
        logger.error(f"所有API路径尝试失败，最后一个错误: {last_error}")
        return {
            "status": "failed",
            "error": {
                "message": f"获取数字人详情失败: {last_error}"
            }
        }
    except Exception as e:
        logger.error(f"获取数字人详情异常: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "message": f"获取数字人详情失败: {str(e)}"
            }
        } 