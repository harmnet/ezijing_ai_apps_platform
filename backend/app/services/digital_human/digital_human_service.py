#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字人PPT讲解视频服务
实现了与小冰AI Beings API的交互，提供PPT讲解视频生成功能
"""

import os
import json
import uuid
import time
import logging
import requests
from datetime import datetime
from urllib.parse import urlparse
import oss2
from werkzeug.utils import secure_filename
import sqlalchemy

# 导入数据库模型
from app import db
from app.models.digital_human import PPTVideoTask

# 导入配置
from .digital_human_config import (
    XIAOBING_PPT_SUBMIT_REQUEST_URL,
    XIAOBING_TASK_DETAIL_REQUEST_URL,
    XIAOBING_REQUEST_HEADERS,
    FONT_DICT,
    DEFAULT_TTS,
    DEFAULT_CAPTION,
    DEFAULT_BACKGROUND_MUSIC,
    DEFAULT_VIRTUAL_HUMANS,
    SUPPORTED_RESOLUTIONS,
    ConvertType,
    OpenApiBackgroundImage,
    OpenApiBackgroundMusic,
    OpenApiCaption,
    OpenApiDisplayTextAttributes,
    OpenApiPPTAttributes,
    OpenApiPPTInfo,
    OpenApiScene,
    OpenApiTts,
    OpenApiVideoCreationDetail,
    OpenApiVirtualHuman,
    OpenApiVirtualHumanAttributes,
    generate_request_body,
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置日志文件路径
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "logs")
LOG_FILE_PATH = os.path.join(LOG_DIR, "digital_human_api.log")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置文件处理器
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def upload_to_oss(file_path):
    """
    上传文件到阿里云OSS
    
    Args:
        file_path: 本地文件路径或文件对象
    
    Returns:
        str: 文件URL地址，上传失败返回None
    """
    try:
        # 处理文件对象
        local_file_path = file_path
        if hasattr(file_path, 'read'):
            # 如果是文件对象，保存为临时文件
            filename = secure_filename(file_path.filename)
            temp_path = os.path.join('/tmp', f"{uuid.uuid4().hex}_{filename}")
            file_path.save(temp_path)
            local_file_path = temp_path
            logger.info(f"文件对象已保存为临时文件: {temp_path}")
        
        # 检查文件是否存在
        if not os.path.exists(local_file_path):
            logger.error(f"文件不存在: {local_file_path}")
            return None
        
        # 输出所有环境变量以便调试
        logger.info("打印所有环境变量进行调试：")
        env_vars = os.environ
        for key in ['ALIYUN_ACCESS_KEY_ID', 'ALIYUN_ACCESS_KEY_SECRET', 'ALIYUN_OSS_BUCKET', 'ALIYUN_OSS_ENDPOINT']:
            logger.info(f"环境变量 {key}: {env_vars.get(key, '未设置')}")
        
        # 直接使用环境变量
        access_key_id = os.environ.get('ALIYUN_ACCESS_KEY_ID')
        access_key_secret = os.environ.get('ALIYUN_ACCESS_KEY_SECRET')
        bucket_name = os.environ.get('ALIYUN_OSS_BUCKET')
        endpoint = os.environ.get('ALIYUN_OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
        
        # 记录OSS配置信息（隐藏敏感信息）
        if access_key_id:
            logger.info(f"OSS Access Key ID: {access_key_id[:5]}... (长度: {len(access_key_id)})")
        else:
            logger.info("OSS Access Key ID: 未设置")
            
        logger.info(f"OSS Bucket: {bucket_name if bucket_name else '未设置'}")
        logger.info(f"OSS Endpoint: {endpoint}")
        
        # 如果环境变量没有设置，尝试硬编码一个默认值进行测试（仅用于开发环境测试）
        if not access_key_id:
            logger.warning("使用硬编码的测试AccessKey（仅限开发环境）")
            access_key_id = "LTAI5tMVdYzk5fVrmjQVk1Ga"
            
        if not access_key_secret:
            access_key_secret = "OKUYiiO9WOw5bJpRTfJa7F76Ayygdk"
            
        if not bucket_name:
            bucket_name = "ezijingai"
        
        # 验证OSS配置
        if not access_key_id or not access_key_secret or not bucket_name:
            logger.error("OSS配置不完整，无法上传")
            return None
        
        # 检查开发环境变量 - 仍保留这个功能以方便开发
        dev_mode = os.getenv('DEV_MODE', 'false').lower() == 'true'
        if dev_mode:
            # 在开发模式下，返回模拟的URL而不是实际上传到OSS
            logger.info("开发模式：模拟OSS上传")
            file_name = os.path.basename(local_file_path)
            mock_url = f"https://mock-{bucket_name}.{endpoint}/dev-uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
            logger.info(f"模拟文件URL: {mock_url}")
            
            # 如果创建了临时文件，删除它
            if 'temp_path' in locals():
                os.remove(temp_path)
                logger.info(f"临时文件已删除: {temp_path}")
                
            return mock_url
        
        try:
            # 创建OSS认证和Bucket实例
            auth = oss2.Auth(access_key_id, access_key_secret)
            bucket = oss2.Bucket(auth, endpoint, bucket_name)
            
            # 生成唯一的文件名 - 与测试代码保持一致的路径格式
            file_name = os.path.basename(local_file_path)
            object_name = f"uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
            
            # 上传文件
            logger.info(f"开始上传文件到OSS: {object_name}")
            result = bucket.put_object_from_file(object_name, local_file_path)
            
            # 如果创建了临时文件，删除它
            if 'temp_path' in locals():
                os.remove(temp_path)
                logger.info(f"临时文件已删除: {temp_path}")
            
            # 检查上传结果
            if result.status == 200:
                # 构建文件URL - 与测试代码保持一致的URL格式
                file_url = f"https://{bucket_name}.{endpoint}/{object_name}"
                logger.info(f"文件上传成功，URL: {file_url}")
                return file_url
            else:
                logger.error(f"OSS上传失败，状态码: {result.status}")
                return None
        except Exception as e:
            logger.error(f"OSS上传异常: {str(e)}")
            # 如果创建了临时文件，删除它
            if 'temp_path' in locals():
                try:
                    os.remove(temp_path)
                    logger.info(f"临时文件已删除: {temp_path}")
                except:
                    pass
            return None
            
    except Exception as e:
        logger.error(f"OSS上传异常: {str(e)}")
        # 如果创建了临时文件，删除它
        if 'temp_path' in locals():
            try:
                os.remove(temp_path)
                logger.info(f"临时文件已删除: {temp_path}")
            except:
                pass
        return None

def get_digital_humans():
    """
    获取数字人列表
    
    Returns:
        dict: 数字人列表及相关信息
    """
    try:
        # 返回预设的数字人列表
        result = []
        for key, human in DEFAULT_VIRTUAL_HUMANS.items():
            result.append({
                "virtualHumanId": human["virtualHumanId"],
                "name": human.get("name", "未知数字人"),
                "type": key
            })
        
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        logger.error(f"获取数字人列表失败: {str(e)}")
        return {"code": 500, "error": {"message": f"获取数字人列表失败: {str(e)}"}}

def get_digital_human_postures(digital_human_id):
    """
    获取数字人姿势列表
    
    Args:
        digital_human_id: 数字人ID
    
    Returns:
        dict: 姿势列表及相关信息
    """
    try:
        # 查找对应的数字人
        postures = []
        for key, human in DEFAULT_VIRTUAL_HUMANS.items():
            if human["virtualHumanId"] == digital_human_id:
                for posture_type, posture_id in human["postures"].items():
                    postures.append({
                        "postureId": posture_id,
                        "name": f"{posture_type}姿势",
                        "type": posture_type
                    })
        
        if not postures:
            logger.warning(f"未找到指定数字人的姿势: {digital_human_id}")
            # 使用默认数字人的姿势
            default_human = DEFAULT_VIRTUAL_HUMANS["default"]
            for posture_type, posture_id in default_human["postures"].items():
                postures.append({
                    "postureId": posture_id,
                    "name": f"{posture_type}姿势(默认)",
                    "type": posture_type
                })
        
        return {"code": 0, "data": postures, "message": "success"}
    except Exception as e:
        logger.error(f"获取数字人姿势列表失败: {str(e)}")
        return {"code": 500, "error": {"message": f"获取数字人姿势列表失败: {str(e)}"}}

def get_supported_resolutions():
    """
    获取支持的视频分辨率
    
    Returns:
        list: 支持的分辨率列表
    """
    return list(SUPPORTED_RESOLUTIONS.keys())

def create_ppt_video_task(
    user_id,
    ppt_file_path=None,
    ppt_url=None,
    text_script=None,
    virtual_human_id=None,
    virtual_human_posture_id=None,
    background_music_url=None,
    background_image_url=None,
    show_caption=True,
    title="PPT讲解视频",
    resolution="720p",
    convert_type="VIDEO",
    tts_params=None
):
    """
    创建PPT视频任务
    :param user_id: 用户ID
    :param ppt_file_path: PPT文件路径
    :param ppt_url: PPT文件URL
    :param text_script: 讲解文本
    :param virtual_human_id: 虚拟人ID
    :param virtual_human_posture_id: 虚拟人姿势ID
    :param background_music_url: 背景音乐URL
    :param background_image_url: 背景图片URL
    :param show_caption: 是否显示字幕
    :param title: 视频标题
    :param resolution: 视频分辨率 720p/1080p/480p
    :param convert_type: 转换类型，默认VIDEO
    :param tts_params: TTS参数
    :return: 任务详情
    """
    # 记录所有输入参数进行调试
    logger.info("创建PPT视频任务，参数如下：")
    logger.info(f"- 用户ID: {user_id}")
    logger.info(f"- PPT文件路径: {ppt_file_path}")
    logger.info(f"- PPT URL: {ppt_url}")
    logger.info(f"- 讲解文本: {text_script}")
    logger.info(f"- 虚拟人ID: {virtual_human_id}")
    logger.info(f"- 虚拟人姿势ID: {virtual_human_posture_id}")
    logger.info(f"- 背景音乐URL: {background_music_url}")
    logger.info(f"- 背景图片URL: {background_image_url}")
    logger.info(f"- 显示字幕: {show_caption}")
    logger.info(f"- 视频标题: {title}")
    logger.info(f"- 分辨率: {resolution}")
    logger.info(f"- 转换类型: {convert_type}")
    logger.info(f"- TTS参数: {tts_params}")
    
    try:
        # 检查文件路径或URL
        if not ppt_file_path and not ppt_url:
            logger.error("未提供PPT文件路径或URL")
            raise ValueError("未提供PPT文件路径或URL")
            
        # 如果提供了文件，上传到OSS获取URL
        if ppt_file_path:
            logger.info(f"准备上传PPT文件到OSS: {ppt_file_path}")
            
            # 直接调用上传函数获取URL，新版upload_to_oss已能处理文件对象
            ppt_url = upload_to_oss(ppt_file_path)
            
            if not ppt_url:
                logger.error("PPT文件上传失败")
                raise ValueError("PPT文件上传失败")
                
            logger.info(f"PPT文件已上传到OSS: {ppt_url}")
                
        # 生成请求体
        request_body = generate_request_body(
            ppt_url=ppt_url,
            title=title,
            virtual_human_id=virtual_human_id,
            virtual_human_posture_id=virtual_human_posture_id,
            text_script=text_script,
            background_music_url=background_music_url,
            background_image_url=background_image_url,
            show_caption=show_caption,
            resolution=resolution,
            convert_type=convert_type,
            tts_params=tts_params
        )
        
        logger.debug(f"生成的请求体: {json.dumps(request_body, ensure_ascii=False)}")
        
        # 调用小冰API创建任务
        logger.info(f"调用小冰API创建任务: {XIAOBING_PPT_SUBMIT_REQUEST_URL}")
        response = requests.post(
            url=XIAOBING_PPT_SUBMIT_REQUEST_URL,
            headers=XIAOBING_REQUEST_HEADERS,
            json=request_body
        )
        
        # 解析响应
        response_json = response.json()
        logger.info(f"小冰API响应: {response_json}")
        
        # 检查响应状态
        code = response_json.get("code", None)
        if code is not None and code != 200:  # 小冰API成功返回码是200
            error_message = response_json.get("message", "未知错误")
            logger.error(f"创建任务失败: {error_message}")
            return {"status": "failed", "error": {"message": error_message}}
            
        # 获取任务ID
        task_id = response_json.get("data", "")
        if not task_id:
            logger.error("API返回成功但未包含任务ID")
            return {"status": "failed", "error": {"message": "API返回成功但未包含任务ID"}}
            
        logger.info(f"小冰API创建任务成功，任务ID: {task_id}")
        
        # 创建任务记录
        task = PPTVideoTask(
            user_id=user_id,
            ppt_url=ppt_url,
            text_script=text_script,
            title=title,
            virtual_human_id=virtual_human_id or "default",
            virtual_human_posture_id=virtual_human_posture_id or "default",
            resolution=resolution,
            convert_type=convert_type,
            task_id=task_id,
            status="creating",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(task)
        db.session.commit()
        logger.info(f"创建PPT视频任务记录成功，任务ID: {task_id}")
        
        # 返回任务详情
        return {
            "task_id": task_id,
            "status": "creating",
            "progress": 0,
            "title": title,
            "ppt_url": ppt_url,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        logger.exception(f"创建PPT视频任务失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "code": 500,
                "message": str(e)
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
        
        # 直接调用小冰API查询任务状态，避免使用数据库
        from app.services.aibeings_ppt_video import query_ppt_video_task as aibeings_query_task
        
        # 调用小冰API服务获取任务状态
        result = aibeings_query_task(task_id)
        
        return result
        
    except Exception as e:
        logger.error(f"查询PPT讲解视频任务异常: {str(e)}")
        return {"status": "error", "error": {"message": f"查询任务异常: {str(e)}"}}

def get_task_history(user_id, page=1, per_page=10):
    """
    查询用户的任务历史记录
    :param user_id: 用户ID
    :param page: 页码（从1开始）
    :param per_page: 每页记录数
    :return: 任务历史记录
    """
    try:
        # 计算分页参数
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        
        offset = (page - 1) * per_page
        
        try:
            # 查询特定用户的任务历史记录，按创建时间降序排列
            tasks = db.session.query(PPTVideoTask) \
                .filter(PPTVideoTask.user_id == user_id) \
                .order_by(PPTVideoTask.created_at.desc()) \
                .offset(offset) \
                .limit(per_page) \
                .all()
            
            # 获取总记录数
            total_count = db.session.query(PPTVideoTask) \
                .filter(PPTVideoTask.user_id == user_id) \
                .count()
                
            # 格式化任务记录
            task_list = []
            for task in tasks:
                task_list.append({
                    "task_id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "progress": task.progress,
                    "result_url": task.result_url if task.result_url else "",
                    "ppt_url": task.ppt_url if task.ppt_url else "",
                    "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S") if task.created_at else "",
                    "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S") if task.updated_at else ""
                })
                
        except sqlalchemy.exc.OperationalError as e:
            # 数据库表不存在的情况
            logger.warning(f"数据库表可能不存在: {str(e)}")
            task_list = []
            total_count = 0
        
        # 返回结果
        return {
            "tasks": task_list,
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }
        
    except Exception as e:
        logger.exception(f"查询任务历史记录失败: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "code": 500,
                "message": str(e)
            }
        }