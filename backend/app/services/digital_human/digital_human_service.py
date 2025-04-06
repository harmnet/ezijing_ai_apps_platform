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

# 导入数据库模型
from app import db
from app.models.digital_human import PPTVideoTask

# 导入配置
from .digital_human_config import (
    XIAOBING_PPT_SUBMIT_REQUEST_URL,
    XIAOBING_TASK_DETAIL_REQUEST_URL,
    XIAOBING_REQUEST_HEADERS,
    FONT_DICT,
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

# 数字人ID和姿势ID映射表
DEFAULT_VIRTUAL_HUMANS = {
    "default": {
        "virtualHumanId": "VHP3S1EF7",
        "name": "默认数字人",
        "postures": {
            "right": "aMiAX96rMqNS",  # 右侧站立姿势
            "left": "d5nJE6EI0txK"    # 左侧站立姿势
        }
    },
    "business_man": {
        "virtualHumanId": "VHFXQGGVG",
        "name": "商务男士",
        "postures": {
            "center": "bKnPeXPndZCR"  # 中间站立姿势
        }
    },
    "business_woman": {
        "virtualHumanId": "VHT1NU4H7",
        "name": "商务女士",
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
        "fontSize": 36,
        "font": FONT_DICT["Microsoft YaHei"]
    }
}

# 默认背景音乐
DEFAULT_BACKGROUND_MUSIC = {
    "mediaUrl": "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/1a1789ea-25bf-437b-acd2-fdc08a265087.MP3",
    "volume": 0.3,
    "speed": 1,
    "loop": True
}

# 支持的视频分辨率
SUPPORTED_RESOLUTIONS = {
    "720p": {"width": 1280, "height": 720},
    "1080p": {"width": 1920, "height": 1080},
    "480p": {"width": 854, "height": 480}
}

def upload_to_oss(file_path):
    """
    上传文件到阿里云OSS
    
    Args:
        file_path: 本地文件路径
    
    Returns:
        str: 文件URL地址，上传失败返回None
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return None
        
        # 获取OSS配置
        access_key_id = os.getenv('ALIYUN_OSS_ACCESS_KEY_ID')
        access_key_secret = os.getenv('ALIYUN_OSS_ACCESS_KEY_SECRET')
        bucket_name = os.getenv('ALIYUN_OSS_BUCKET_NAME', 'ezijingai')
        endpoint = os.getenv('ALIYUN_OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
        
        # 验证OSS配置
        if not access_key_id or not access_key_secret or not bucket_name:
            logger.error("OSS配置不完整，无法上传")
            return None
        
        # 创建OSS认证和Bucket实例
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        
        # 生成唯一的文件名
        file_name = os.path.basename(file_path)
        object_name = f"uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
        
        # 上传文件
        logger.info(f"开始上传文件到OSS: {object_name}")
        result = bucket.put_object_from_file(object_name, file_path)
        
        # 检查上传结果
        if result.status == 200:
            # 构建文件URL
            file_url = f"https://{bucket_name}.{endpoint}/{object_name}"
            logger.info(f"文件上传成功，URL: {file_url}")
            return file_url
        else:
            logger.error(f"OSS上传失败，状态码: {result.status}")
            return None
            
    except Exception as e:
        logger.error(f"OSS上传异常: {str(e)}")
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
    ppt_file_path,
    text_script=None,
    virtual_human_id=None,
    virtual_human_posture_id=None,
    background_music_url=None,
    background_image_url=None,
    show_caption=True,
    title="PPT讲解视频",
    resolution="720p",
    convert_type="VIDEO"
):
    """
    创建PPT讲解视频任务
    
    Args:
        ppt_file_path: PPT文件路径
        text_script: 讲解文本脚本，如果不提供则使用PPT备注
        virtual_human_id: 数字人ID，如不提供则使用默认数字人
        virtual_human_posture_id: 数字人姿势ID，如不提供则使用默认姿势
        background_music_url: 背景音乐URL，如不提供则使用默认背景音乐
        background_image_url: 背景图片URL，如不提供则使用白色背景
        show_caption: 是否显示字幕
        title: 视频标题
        resolution: 视频分辨率，支持720p、1080p、480p
        convert_type: PPT转换类型，IMG或VIDEO
    
    Returns:
        dict: 任务创建结果，包含任务ID和状态
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(ppt_file_path):
            logger.error(f"PPT文件不存在: {ppt_file_path}")
            return {"status": "failed", "error": {"message": f"PPT文件不存在: {ppt_file_path}"}}
        
        # 上传PPT文件到OSS
        ppt_url = upload_to_oss(ppt_file_path)
        if not ppt_url:
            logger.error("PPT文件上传失败")
            return {"status": "failed", "error": {"message": "PPT文件上传失败"}}
        
        # 设置默认值
        if not virtual_human_id:
            virtual_human_id = DEFAULT_VIRTUAL_HUMANS["default"]["virtualHumanId"]
        
        if not virtual_human_posture_id:
            virtual_human_posture_id = DEFAULT_VIRTUAL_HUMANS["default"]["postures"]["right"]
        
        # 设置视频分辨率
        if resolution not in SUPPORTED_RESOLUTIONS:
            logger.warning(f"不支持的分辨率: {resolution}，使用默认720p")
            resolution = "720p"
        
        video_width = SUPPORTED_RESOLUTIONS[resolution]["width"]
        video_height = SUPPORTED_RESOLUTIONS[resolution]["height"]
        
        # 创建虚拟人属性
        if resolution == "1080p":
            virtual_human_attributes = OpenApiVirtualHumanAttributes(
                width=344,
                height=1080,
                x=1517,
                y=309,
                forceMattingType=0
            )
        else:
            # 按比例缩放
            ratio = SUPPORTED_RESOLUTIONS[resolution]["width"] / 1920
            virtual_human_attributes = OpenApiVirtualHumanAttributes(
                width=int(344 * ratio),
                height=int(1080 * ratio),
                x=int(1517 * ratio),
                y=int(309 * ratio),
                forceMattingType=0
            )
        
        # 创建虚拟人对象
        virtual_human = OpenApiVirtualHuman(
            virtualHumanId=virtual_human_id,
            virtualHumanPostureId=virtual_human_posture_id,
            attributes=virtual_human_attributes,
            zIndex=20
        )
        
        # 创建TTS对象
        tts = OpenApiTts(
            voiceId=DEFAULT_TTS["voiceId"],
            rate=DEFAULT_TTS["rate"],
            pitch=DEFAULT_TTS["pitch"],
            volume=DEFAULT_TTS["volume"]
        )
        
        # 创建字幕属性和字幕对象
        caption = None
        if show_caption:
            # 按分辨率调整字幕Y坐标
            y_pos = int(1000 * (SUPPORTED_RESOLUTIONS[resolution]["height"] / 1080))
            
            display_text_attributes = OpenApiDisplayTextAttributes(
                y=y_pos,
                font=FONT_DICT["Microsoft YaHei"],
                fontSize=DEFAULT_CAPTION["attributes"]["fontSize"],
                fontColor="#FFFFFF",
                bold=DEFAULT_CAPTION["attributes"]["bold"],
                italic=DEFAULT_CAPTION["attributes"]["italic"],
                underline=DEFAULT_CAPTION["attributes"]["underline"],
                spacing=DEFAULT_CAPTION["attributes"]["spacing"],
                visible=DEFAULT_CAPTION["attributes"]["visible"]
            )
            
            caption = OpenApiCaption(
                topLeft=False,
                topRight=False,
                topCenter=True,
                zIndex=DEFAULT_CAPTION["zIndex"],
                attributes=display_text_attributes
            )
        
        # 创建背景图片对象
        background_image = None
        if background_image_url:
            background_image = OpenApiBackgroundImage(
                mediaUrl=background_image_url
            )
        
        # 创建场景对象
        scene = OpenApiScene(
            virtualHuman=virtual_human,
            tts=tts,
            backgroundImage=background_image,
            caption=caption,
            voiceText=text_script
        )
        
        # 创建背景音乐对象
        background_music = None
        if background_music_url:
            background_music = OpenApiBackgroundMusic(
                mediaUrl=background_music_url,
                volume=DEFAULT_BACKGROUND_MUSIC["volume"],
                speed=DEFAULT_BACKGROUND_MUSIC["speed"],
                loop=DEFAULT_BACKGROUND_MUSIC["loop"]
            )
        elif DEFAULT_BACKGROUND_MUSIC["mediaUrl"]:
            background_music = OpenApiBackgroundMusic(
                mediaUrl=DEFAULT_BACKGROUND_MUSIC["mediaUrl"],
                volume=DEFAULT_BACKGROUND_MUSIC["volume"],
                speed=DEFAULT_BACKGROUND_MUSIC["speed"],
                loop=DEFAULT_BACKGROUND_MUSIC["loop"]
            )
        
        # 创建视频详情对象
        video_creation_detail = OpenApiVideoCreationDetail(
            scenes=[scene],
            backgroundMusic=background_music
        )
        
        # 创建PPT属性对象
        ppt_attributes = OpenApiPPTAttributes(
            width=SUPPORTED_RESOLUTIONS[resolution]["width"],
            height=SUPPORTED_RESOLUTIONS[resolution]["height"],
            x=0,
            y=0
        )
        
        # 创建PPT信息对象
        ppt_info = OpenApiPPTInfo(
            pptUrl=ppt_url,
            convertType=ConvertType.VIDEO if convert_type == "VIDEO" else ConvertType.IMG,
            getText=(text_script is None),  # 如果没有提供文本脚本，则使用PPT备注
            singlePageSecond=5,
            attributes=ppt_attributes
        )
        
        # 生成请求体
        request_body = generate_request_body(
            outputVideoName=title,
            creationDetail=video_creation_detail,
            pptInfo=ppt_info,
            width=video_width,
            height=video_height
        )
        
        # 发送请求
        logger.info(f"发送PPT视频创建请求: {XIAOBING_PPT_SUBMIT_REQUEST_URL}")
        logger.debug(f"请求头: {XIAOBING_REQUEST_HEADERS}")
        logger.debug(f"请求体: {request_body}")
        
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
        if code is not None and code != 200:  # 小冰API成功返回码是200，而不是0
            error_message = response_json.get("message", "未知错误")
            logger.error(f"创建任务失败: {error_message}")
            return {"status": "failed", "error": {"message": error_message}}
        
        # 提取任务ID
        task_id = response_json.get("data", None)
        if not task_id:
            logger.error("未获取到任务ID")
            return {"status": "failed", "error": {"message": "未获取到任务ID"}}
        
        logger.info(f"任务创建成功，ID: {task_id}")
        
        # 创建任务记录并保存到数据库
        task_record = PPTVideoTask(
            ppt_url=ppt_url,
            text_script=text_script if text_script else "",
            title=title,
            virtual_human_id=virtual_human_id,
            virtual_human_posture_id=virtual_human_posture_id,
            resolution=resolution,
            convert_type=convert_type,
            task_id=task_id,
            status="creating",
            created_at=datetime.now()
        )
        
        db.session.add(task_record)
        db.session.commit()
        
        return {
            "status": "creating",
            "task_id": task_id,
            "created_at": datetime.now().isoformat(),
            "resolution": resolution,
            "title": title
        }
        
    except Exception as e:
        logger.error(f"创建PPT讲解视频任务异常: {str(e)}")
        return {"status": "failed", "error": {"message": f"创建任务异常: {str(e)}"}}

def query_ppt_video_task(task_id):
    """
    查询PPT讲解视频任务状态
    
    Args:
        task_id: 任务ID
    
    Returns:
        dict: 任务状态信息
    """
    try:
        if not task_id:
            logger.error("任务ID为空")
            return {"status": "failed", "error": {"message": "任务ID为空"}}
        
        # 构建请求参数
        params = {"taskId": task_id}
        
        # 发送请求
        logger.info(f"查询任务状态: {task_id}")
        response = requests.get(
            url=XIAOBING_TASK_DETAIL_REQUEST_URL,
            headers=XIAOBING_REQUEST_HEADERS,
            params=params
        )
        
        # 解析响应
        response_json = response.json()
        logger.info(f"小冰API响应: {response_json}")
        
        # 检查响应状态
        code = response_json.get("code", None)
        if code is not None and code != 200:  # 小冰API成功返回码是200，而不是0
            error_message = response_json.get("message", "未知错误")
            logger.error(f"查询任务失败: {error_message}")
            return {"status": "failed", "error": {"message": error_message}}
        
        # 提取任务信息
        task_data = response_json.get("data", {})
        if not task_data:
            logger.error("未获取到任务信息")
            return {"status": "failed", "error": {"message": "未获取到任务信息"}}
        
        # 解析任务状态
        status = task_data.get("status", None)
        if not status:
            logger.error("未获取到任务状态")
            return {"status": "failed", "error": {"message": "未获取到任务状态"}}
        
        # 转换状态为可读形式
        status_map = {
            1: "processing",   # 等待中
            2: "processing",   # 处理中
            3: "completed",    # 已完成
            4: "failed",       # 失败
            "pending": "pending",
            "running": "processing",
            "success": "completed",
            "failed": "failed"
        }
        
        status_text = status_map.get(status, "unknown")
        logger.info(f"任务状态: {status} 映射为: {status_text}")
        
        # 构建响应
        result = {"status": status_text, "task_id": task_id}
        
        # 从数据库查询任务记录
        task_record = PPTVideoTask.query.filter_by(task_id=task_id).first()
        
        # 如果任务完成，返回视频URL和更新数据库
        if status == 3 or status == "success":  # 已完成
            video_url = task_data.get("downloadUrl", "") or task_data.get("videoUrl", "")
            thumbnail_url = task_data.get("coverUrl", "") or task_data.get("videoThumbnailImageUrl", "")
            
            result["video_url"] = video_url
            result["thumbnail_url"] = thumbnail_url
            result["completed_at"] = datetime.now().isoformat()
            
            # 更新数据库记录
            if task_record and task_record.status != "completed":
                task_record.status = "completed"
                task_record.video_url = video_url
                task_record.thumbnail_url = thumbnail_url
                task_record.completed_at = datetime.now()
                db.session.commit()
                
        elif status == 4 or status == "failed":  # 失败
            error_message = task_data.get("failureReason", "未知错误") or task_data.get("error", "未知错误")
            result["error"] = {"message": error_message}
            
            # 更新数据库记录
            if task_record and task_record.status != "failed":
                task_record.status = "failed"
                db.session.commit()
        else:
            # 更新数据库中的任务状态
            if task_record and task_record.status != status_text:
                task_record.status = status_text
                db.session.commit()
        
        return result
        
    except Exception as e:
        logger.error(f"查询PPT讲解视频任务异常: {str(e)}")
        return {"status": "failed", "error": {"message": f"查询任务异常: {str(e)}"}}

def get_task_history(limit=10, offset=0):
    """
    获取任务历史记录
    
    Args:
        limit: 每页记录数
        offset: 偏移量
    
    Returns:
        dict: 包含历史记录的字典
    """
    try:
        # 查询任务记录，按创建时间降序排序
        tasks = PPTVideoTask.query.order_by(PPTVideoTask.created_at.desc()).limit(limit).offset(offset).all()
        
        # 查询总记录数
        total = PPTVideoTask.query.count()
        
        # 转换为字典列表
        task_list = [task.to_dict() for task in tasks]
        
        return {
            "code": 0,
            "data": {
                "total": total,
                "tasks": task_list
            },
            "message": "success"
        }
    except Exception as e:
        logger.error(f"获取任务历史记录异常: {str(e)}")
        return {"code": 500, "error": {"message": f"获取任务历史记录异常: {str(e)}"}}