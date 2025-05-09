#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
百度数字人基础视频合成服务
实现了与百度数字人API的交互，提供视频合成功能
"""

import os
import json
import uuid
import hmac
import hashlib
import logging
import requests
from datetime import datetime, timezone, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 百度数字人基础视频合成API地址
BAIDU_DIGITAL_HUMAN_API_BASE_URL = "https://open.xiling.baidu.com"
BAIDU_DIGITAL_HUMAN_VIDEO_SUBMIT_API = f"{BAIDU_DIGITAL_HUMAN_API_BASE_URL}/api/digitalhuman/open/v1/video/submit"
BAIDU_DIGITAL_HUMAN_VIDEO_QUERY_API = f"{BAIDU_DIGITAL_HUMAN_API_BASE_URL}/api/digitalhuman/open/v1/video/task"

# 高级视频合成API
BAIDU_DIGITAL_HUMAN_ADVANCED_VIDEO_SUBMIT_API = f"{BAIDU_DIGITAL_HUMAN_API_BASE_URL}/api/digitalhuman/open/v1/video/advanced/submit"
BAIDU_DIGITAL_HUMAN_ADVANCED_VIDEO_QUERY_API = f"{BAIDU_DIGITAL_HUMAN_API_BASE_URL}/api/digitalhuman/open/v1/video/advanced/task"

# 默认数字人配置
DEFAULT_FIGURE_ID = "A2A_V2-xinxin"  # 梓欣
DEFAULT_DRIVE_TYPE = "TEXT"
DEFAULT_TTS_PERSON = "5132"  # 度小夏
DEFAULT_TTS_SPEED = "5"
DEFAULT_TTS_VOLUME = "5"
DEFAULT_TTS_PITCH = "5"

# 百度数字人API鉴权配置
BAIDU_DIGITAL_HUMAN_APP_ID = "i-qmvk2dawwrv09"
BAIDU_DIGITAL_HUMAN_APP_KEY = "skn2z6hmea3a9gi5jniu"


def hmac_sha256(key, data):
    """
    使用HMAC-SHA256计算签名
    
    Args:
        key (str): 密钥
        data (str): 要签名的数据
        
    Returns:
        str: 签名结果（十六进制字符串）
    """
    return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()


def validate_advanced_video_params(params):
    """
    验证百度数字人高级视频合成API的参数是否合法
    
    Args:
        params (dict): 包含所有参数的字典
        
    Returns:
        tuple: (是否有效, 错误信息)
    """
    # 增强日志记录
    logger.info(f"开始验证高级视频合成参数: {json.dumps({k: v for k, v in params.items() if k != 'text'}, ensure_ascii=False)}")
    if 'text' in params:
        text_preview = params['text'][:30] + '...' if len(params['text']) > 30 else params['text']
        logger.info(f"验证参数文本内容(前30字符): {text_preview}")
    
    # 检查必须参数
    required_fields = [
        ('figure_id', '数字人ID'),
        ('template_id', '模板ID'),
        ('text', '文本内容'),
        ('tts_person', '语音合成人声ID')
    ]
    
    for field, desc in required_fields:
        if not params.get(field):
            logger.error(f"参数验证失败: 缺少必需参数 {desc} ({field})")
            return False, f"缺少参数: {desc} ({field})"
    
    # 检查文本长度（通常语音项目有文本长度限制）
    text = params.get('text', '')
    if len(text) < 5:
        logger.error(f"参数验证失败: 文本内容过短({len(text)}字符)")
        return False, f"文本内容过短: {len(text)}字符，通常需要至少5个字符"
    if len(text) > 500:
        logger.error(f"参数验证失败: 文本内容过长({len(text)}字符)")
        return False, f"文本内容过长: {len(text)}字符，通常不超过500字符"
    
    # 检查图片URL格式
    logo_url = params.get('logo_url')
    if logo_url and not (logo_url.startswith('http://') or logo_url.startswith('https://')):
        logger.error(f"参数验证失败: Logo URL格式不正确({logo_url})")
        return False, f"Logo URL格式不正确: {logo_url}"
    
    # 检查视频尺寸
    video_width = params.get('video_width')
    video_height = params.get('video_height')
    if video_width and video_height:
        if not (100 <= video_width <= 1920 and 100 <= video_height <= 1920):
            logger.error(f"参数验证失败: 视频尺寸超出范围({video_width}x{video_height})")
            return False, f"视频尺寸超出范围: {video_width}x{video_height}，通常在100-1920之间"
    
    # 检查数字人ID格式
    figure_id = params.get('figure_id')
    if figure_id and not (figure_id.isdigit() or figure_id.startswith('A2A')):
        logger.error(f"参数验证失败: 数字人ID格式不正确({figure_id})")
        return False, f"数字人ID格式不正确: {figure_id}，通常为数字或以A2A开头"
    
    # 检查模板ID格式
    template_id = params.get('template_id')
    if template_id and not template_id.startswith('t-'):
        logger.error(f"参数验证失败: 模板ID格式不正确({template_id})")
        return False, f"模板ID格式不正确: {template_id}，通常以t-开头"
    
    logger.info("参数验证通过: 所有参数符合要求")
    return True, ""


def generate_authorization():
    """
    生成百度数字人API的授权字符串
    
    Returns:
        str: 授权字符串，格式为：AppID/HMAC_SHA256(AppKey, AppID+ExpiredTime)/ExpiredTime
    """
    app_id = BAIDU_DIGITAL_HUMAN_APP_ID
    app_key = BAIDU_DIGITAL_HUMAN_APP_KEY
    
    # 计算过期时间（当前时间加1小时）
    expired_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    
    # 生成授权字符串
    authorization = f"{app_id}/{hmac_sha256(app_key, app_id + expired_time)}/{expired_time}"
    
    return authorization


def submit_baidu_digital_human_video_task(
    text,
    api_key=None,
    api_secret=None,
    figure_id=DEFAULT_FIGURE_ID,
    drive_type=DEFAULT_DRIVE_TYPE,
    tts_person=DEFAULT_TTS_PERSON,
    tts_speed=DEFAULT_TTS_SPEED,
    tts_volume=DEFAULT_TTS_VOLUME,
    tts_pitch=DEFAULT_TTS_PITCH,
    video_width=1080,
    video_height=1920,
    transparent=False,
    background_image_url=None,
    callback_url=None,
    auto_animoji=True,
    subtitle_enabled=False
):
    """
    提交百度数字人视频合成任务
    
    Args:
        text (str): 驱动数字人播报的文本
        api_key (str, optional): 百度API密钥
        api_secret (str, optional): 百度API密钥
        figure_id (str, optional): 人像ID，默认为"A2A_V2-xinxin"（梓欣）
        drive_type (str, optional): 驱动类型，默认为"TEXT"
        tts_person (str, optional): TTS发音人ID，默认为"5132"（度小夏）
        tts_speed (str, optional): 语速，默认为"5"
        tts_volume (str, optional): 音量，默认为"5"
        tts_pitch (str, optional): 语调，默认为"5"
        video_width (int, optional): 视频宽度，默认为1080
        video_height (int, optional): 视频高度，默认为1920
        transparent (bool, optional): 是否输出webm格式透明背景视频，默认为False
        background_image_url (str, optional): 背景图片URL，默认为None
        callback_url (str, optional): 回调URL，默认为None
        auto_animoji (bool, optional): 是否自动添加数字人动作，默认为True
        subtitle_enabled (bool, optional): 是否启用字幕，默认为False
        
    Returns:
        dict: 请求结果，包含任务ID等信息
    """
    try:
        # 构建请求数据
        request_data = {
            "figureId": figure_id,
            "text": text,
            "driveType": drive_type,
            "backgroundImageUrl": background_image_url if background_image_url else "",
            "ttsParams": {
                "person": tts_person,
                "speed": tts_speed,
                "pitch": tts_pitch,
                "volume": tts_volume
            },
            "videoParams": {
                "height": video_height,
                "width": video_width,
                "transparent": transparent
            },
            "autoAnimoji": auto_animoji,
            "subtitleParams": {
                "enabled": subtitle_enabled,
                "subtitlePolicy": "SRT"
            }
        }
        
        # 添加可选的回调URL
        if callback_url:
            request_data["callbackUrl"] = callback_url
            
        # 构建请求头
        headers = {
            "Content-Type": "application/json;charset=utf-8"
        }
        
        # 添加认证信息，优先使用HMAC-SHA256鉴权
        authorization = generate_authorization()
        headers["Authorization"] = authorization
        logger.info(f"使用HMAC-SHA256鉴权：{authorization[:20]}...")
            
        # 如果还提供了API密钥和密钥（兼容老的鉴权方式）
        if api_key and api_secret:
            headers["X-Bce-Auth"] = f"bce-auth-v1/{api_key}/{api_secret}"
            logger.info(f"使用X-Bce-Auth鉴权：{api_key[:5]}...")
            
        # 记录请求信息（移除敏感信息）
        log_data = request_data.copy()
        logger.info(f"提交百度数字人视频合成任务，请求参数: {json.dumps(log_data, ensure_ascii=False)}")
            
        # 发送请求
        response = requests.post(
            BAIDU_DIGITAL_HUMAN_VIDEO_SUBMIT_API,
            json=request_data,
            headers=headers
        )
        
        # 检查响应状态
        if response.status_code != 200:
            logger.error(f"百度数字人API请求失败，状态码: {response.status_code}, 响应内容: {response.text}")
            return {
                "status": "failed",
                "error": {
                    "code": response.status_code,
                    "message": f"API请求失败: {response.text}"
                }
            }
            
        # 解析响应内容
        result = response.json()
        logger.info(f"百度数字人API请求成功，响应内容: {json.dumps(result, ensure_ascii=False)}")
        
        # 检查API返回结果
        if not result.get("success") or result.get("code") != 0:
            error_message = result.get("message", {}).get("global", "未知错误")
            logger.error(f"百度数字人API返回错误: {error_message}")
            return {
                "status": "failed",
                "error": {
                    "code": result.get("code"),
                    "message": error_message
                }
            }
            
        # 返回成功结果
        return {
            "status": "success",
            "data": result.get("result", {}),
            "requestId": result.get("requestId")
        }
    except Exception as e:
        logger.error(f"提交百度数字人视频合成任务异常: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "code": 500,
                "message": f"服务异常: {str(e)}"
            }
        }


def query_baidu_digital_human_video_task(task_id, api_key=None, api_secret=None):
    """
    查询百度数字人视频合成任务状态
    
    Args:
        task_id (str): 任务ID
        api_key (str, optional): 百度API密钥
        api_secret (str, optional): 百度API密钥
        
    Returns:
        dict: 请求结果，包含任务状态等信息
    """
    try:
        # 验证任务ID
        if not task_id:
            logger.error("任务ID不能为空")
            return {
                "status": "failed",
                "error": {
                    "code": 400,
                    "message": "任务ID不能为空"
                }
            }
            
        # 构建请求参数 - 直接将taskId添加到URL中
        url = f"{BAIDU_DIGITAL_HUMAN_VIDEO_QUERY_API}?taskId={task_id}"
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json;charset=utf-8"
        }
        
        # 添加认证信息，优先使用HMAC-SHA256鉴权
        authorization = generate_authorization()
        headers["Authorization"] = authorization
        logger.info(f"使用HMAC-SHA256鉴权：{authorization[:20]}...")
            
        # 如果还提供了API密钥和密钥（兼容老的鉴权方式）
        if api_key and api_secret:
            headers["X-Bce-Auth"] = f"bce-auth-v1/{api_key}/{api_secret}"
            logger.info(f"使用X-Bce-Auth鉴权：{api_key[:5]}...")
        
        # 记录完整请求信息，便于调试
        logger.info(f"查询任务请求URL: {url}")
        logger.info(f"查询任务请求头: {headers}")
            
        # 发送请求
        response = requests.get(
            url,
            headers=headers
        )
        
        # 检查响应状态
        if response.status_code != 200:
            logger.error(f"百度数字人API查询失败，状态码: {response.status_code}, 响应内容: {response.text}")
            return {
                "status": "failed",
                "error": {
                    "code": response.status_code,
                    "message": f"API请求失败: {response.text}"
                }
            }
            
        # 解析响应内容
        result = response.json()
        logger.info(f"百度数字人API查询成功，响应内容: {json.dumps(result, ensure_ascii=False)}")
        
        # 检查API返回结果
        if not result.get("success") or result.get("code") != 0:
            error_message = result.get("message", {}).get("global", "未知错误")
            logger.error(f"百度数字人API返回错误: {error_message}")
            return {
                "status": "failed",
                "error": {
                    "code": result.get("code"),
                    "message": error_message
                }
            }
            
        # 返回成功结果
        return {
            "status": "success",
            "data": result.get("result", {}),
            "requestId": result.get("requestId")
        }
    except Exception as e:
        logger.error(f"查询百度数字人视频合成任务异常: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "code": 500,
                "message": f"服务异常: {str(e)}"
            }
        }


def submit_baidu_digital_human_advanced_video_task(
    figure_id,
    template_id,
    text,
    tts_person,
    video_width,
    video_height,
    api_key=None,
    api_secret=None,
    drive_type=DEFAULT_DRIVE_TYPE,
    tts_speed=DEFAULT_TTS_SPEED,
    tts_volume=DEFAULT_TTS_VOLUME,
    tts_pitch=DEFAULT_TTS_PITCH,
    title=None,
    logo_url=None,
    bgm_url=None,
    material_url=None,
    callback_url=None,
    risk_tip=None,
    opening_material=None,
    ending_material=None,
    mashup_materials=None,
    fission_params=None
):
    """
    提交百度数字人高级视频合成任务
    
    Args:
        figure_id (str): 人像ID
        template_id (str): 模板ID
        text (str): 驱动数字人播报的文本
        tts_person (str): TTS发音人ID
        video_width (int): 视频宽度
        video_height (int): 视频高度
        api_key (str, optional): 百度API密钥
        api_secret (str, optional): 百度API密钥
        drive_type (str, optional): 驱动类型，默认为"TEXT"
        tts_speed (str, optional): 语速，默认为"5"
        tts_volume (str, optional): 音量，默认为"5"
        tts_pitch (str, optional): 语调，默认为"5"
        title (str, optional): 视频标题
        logo_url (str, optional): logo图片URL
        bgm_url (str, optional): 背景音乐URL
        material_url (str, optional): 背景素材URL
        callback_url (str, optional): 回调URL
        risk_tip (str, optional): 水印描述
        opening_material (dict, optional): 片头背景素材
        ending_material (dict, optional): 片尾背景素材
        mashup_materials (list, optional): 合成素材列表
        fission_params (dict, optional): 裂变参数
        
    Returns:
        dict: 请求结果，包含任务ID等信息
    """
    try:
        # 参数验证
        params = {
            'figure_id': figure_id,
            'template_id': template_id,
            'text': text,
            'tts_person': tts_person,
            'video_width': video_width,
            'video_height': video_height,
            'logo_url': logo_url
        }
        is_valid, error_message = validate_advanced_video_params(params)
        if not is_valid:
            logger.error(f"百度数字人高级视频合成参数验证失败: {error_message}")
            return {
                "status": "failed",
                "error": {
                    "code": 400,
                    "message": "参数验证失败",
                    "more_detail": error_message
                }
            }
        
        # 构建请求数据
        request_data = {
            "figureId": figure_id,
            "templateId": template_id,
            "text": text,
            "driveType": drive_type,
            "ttsParams": {
                "person": tts_person,
                "speed": tts_speed,
                "pitch": tts_pitch,
                "volume": tts_volume
            },
            "videoParams": {
                "width": video_width,
                "height": video_height
            }
        }
        
        # 添加可选参数
        if title:
            request_data["title"] = title
            
        if logo_url:
            request_data["logoParams"] = {
                "logoUrl": logo_url
            }
            
        if bgm_url:
            request_data["bgmParams"] = {
                "bgmUrl": bgm_url
            }
            
        if material_url:
            request_data["materialUrl"] = material_url
            
        if callback_url:
            request_data["callbackUrl"] = callback_url
            
        if risk_tip:
            request_data["riskTip"] = risk_tip
            
        if opening_material:
            request_data["openingMaterial"] = opening_material
            
        if ending_material:
            request_data["endingMaterial"] = ending_material
            
        if mashup_materials:
            request_data["mashupMaterials"] = mashup_materials
            
        if fission_params:
            request_data["fissionParams"] = fission_params
            
        # 构建请求头
        headers = {
            "Content-Type": "application/json;charset=utf-8"
        }
        
        # 添加认证信息，优先使用HMAC-SHA256鉴权
        authorization = generate_authorization()
        headers["Authorization"] = authorization
        logger.info(f"使用HMAC-SHA256鉴权：{authorization[:20]}...")
            
        # 如果还提供了API密钥和密钥（兼容老的鉴权方式）
        if api_key and api_secret:
            headers["X-Bce-Auth"] = f"bce-auth-v1/{api_key}/{api_secret}"
            logger.info(f"使用X-Bce-Auth鉴权：{api_key[:5]}...")
            
        # 记录详细的请求信息（移除敏感信息）
        log_data = request_data.copy()
        logger.info(f"提交百度数字人高级视频合成任务，请求参数: {json.dumps(log_data, ensure_ascii=False)}")
        logger.info(f"请求头信息: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization' and k != 'X-Bce-Auth'}, ensure_ascii=False)}")
        logger.info(f"请求URL: {BAIDU_DIGITAL_HUMAN_ADVANCED_VIDEO_SUBMIT_API}")
            
        # 发送请求
        response = requests.post(
            BAIDU_DIGITAL_HUMAN_ADVANCED_VIDEO_SUBMIT_API,
            json=request_data,
            headers=headers
        )
        
        # 增强日志：记录原始响应状态和内容
        logger.info(f"百度数字人API原始响应状态码: {response.status_code}")
        logger.info(f"百度数字人API原始响应内容: {response.text}")
        
        # 检查响应状态
        if response.status_code != 200:
            logger.error(f"百度数字人高级视频API请求失败，状态码: {response.status_code}, 响应内容: {response.text}")
            # 增强日志：记录请求详情
            logger.error(f"失败请求的详细信息 - URL: {BAIDU_DIGITAL_HUMAN_ADVANCED_VIDEO_SUBMIT_API}")
            logger.error(f"失败请求的详细信息 - 请求头: {headers}")
            safe_data = {k: v for k, v in request_data.items() if k not in ["text"]}
            logger.error(f"失败请求的详细信息 - 请求体(部分): {safe_data}")
            return {
                "status": "failed",
                "error": {
                    "code": response.status_code,
                    "message": f"API请求失败: {response.text}"
                }
            }
            
        # 解析响应内容
        result = response.json()
        logger.info(f"百度数字人高级视频API请求成功，响应内容: {json.dumps(result, ensure_ascii=False)}")
        
        # 检查API返回结果
        if not result.get("success") or result.get("code") != 0:
            error_code = result.get("code")
            error_message = result.get("message", {}).get("global", "未知错误")
            
            # 增强日志：记录错误详情
            logger.error(f"百度数字人高级视频API返回错误码: {error_code}")
            logger.error(f"百度数字人高级视频API返回错误信息: {error_message}")
            logger.error(f"百度数字人高级视频API完整错误响应: {json.dumps(result, ensure_ascii=False)}")
            
            # 对特定错误进行更详细的日志记录
            if "message" in result and isinstance(result["message"], dict):
                for field, field_errors in result["message"].items():
                    if field != "global":
                        logger.error(f"字段'{field}'错误: {field_errors}")
            
            # 针对"未识别错误"提供更详细的错误信息
            if error_message == "未识别错误" and error_code == 10004:
                more_detail = "百度API返回了'未识别错误'(10004)，可能的原因包括：\n"
                more_detail += "1. 模板ID无效或不存在\n"
                more_detail += "2. 数字人ID无效或不存在\n"
                more_detail += "3. 语音合成参数（人声ID等）不正确\n"
                more_detail += "4. 图片URL无法访问或格式不正确\n"
                more_detail += "5. 文本长度不符合模板要求\n"
                more_detail += "6. API密钥权限不足\n"
                more_detail += "建议检查以上参数是否正确，尤其是模板ID和人像ID。"
                logger.error(f"百度数字人高级视频API返回错误: {error_message}")
                logger.error(more_detail)
                return {
                    "status": "failed",
                    "error": {
                        "code": error_code,
                        "message": error_message,
                        "more_detail": more_detail
                    }
                }
            elif error_code == 500:
                more_detail = "百度API返回了服务器内部错误(500)，可能的原因包括：\n"
                more_detail += "1. 百度API服务器暂时性故障\n"
                more_detail += "2. 请求参数格式错误导致服务器处理异常\n"
                more_detail += "建议稍后重试，或检查请求参数格式。"
                logger.error(f"百度数字人高级视频API返回内部错误: {error_message}")
                logger.error(more_detail)
                return {
                    "status": "failed",
                    "error": {
                        "code": error_code,
                        "message": error_message,
                        "more_detail": more_detail
                    }
                }
            elif error_code == 10008:
                more_detail = "百度API返回了权限不足错误(10008)，可能的原因包括：\n"
                more_detail += "1. API密钥权限不足，无法使用所需功能\n"
                more_detail += "2. 所选模板或数字人需要更高级别的权限\n"
                more_detail += "3. 账户余额不足或未开通相关服务\n"
                more_detail += "建议检查API密钥权限，或联系百度客服确认账户状态。"
                logger.error(f"百度数字人高级视频API返回权限错误: {error_message}")
                logger.error(more_detail)
                return {
                    "status": "failed",
                    "error": {
                        "code": error_code,
                        "message": error_message,
                        "more_detail": more_detail
                    }
                }
            elif error_code == 110:
                more_detail = "百度API返回了参数错误(110)，这通常表示：\n"
                more_detail += "1. 请求参数的格式或类型不正确\n"
                more_detail += "2. 必需参数缺失或格式错误\n"
                more_detail += "请检查所有参数的格式和类型是否符合API要求。"
                logger.error(f"百度数字人高级视频API返回参数格式错误: {error_message}")
                logger.error(more_detail)
                return {
                    "status": "failed",
                    "error": {
                        "code": error_code,
                        "message": error_message,
                        "more_detail": more_detail
                    }
                }
            else:
                logger.error(f"百度数字人高级视频API返回错误: {error_message}")
                return {
                    "status": "failed",
                    "error": {
                        "code": error_code,
                        "message": error_message
                    }
                }
            
        # 返回成功结果
        return {
            "status": "success",
            "data": result.get("result", {}),
            "requestId": result.get("requestId")
        }
    except Exception as e:
        logger.error(f"提交百度数字人高级视频合成任务异常: {str(e)}")
        # 记录更多异常信息
        import traceback
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        return {
            "status": "failed",
            "error": {
                "code": 500,
                "message": f"服务异常: {str(e)}"
            }
        }


def query_baidu_digital_human_advanced_video_task(task_id, api_key=None, api_secret=None):
    """
    查询百度数字人高级视频合成任务状态
    
    Args:
        task_id (str): 任务ID
        api_key (str, optional): 百度API密钥
        api_secret (str, optional): 百度API密钥
        
    Returns:
        dict: 请求结果，包含任务状态等信息
    """
    try:
        # 验证任务ID
        if not task_id:
            logger.error("任务ID不能为空")
            return {
                "status": "failed",
                "error": {
                    "code": 400,
                    "message": "任务ID不能为空"
                }
            }
            
        # 构建请求参数 - 直接将taskId添加到URL中
        url = f"{BAIDU_DIGITAL_HUMAN_ADVANCED_VIDEO_QUERY_API}?taskId={task_id}"
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json;charset=utf-8"
        }
        
        # 添加认证信息，优先使用HMAC-SHA256鉴权
        authorization = generate_authorization()
        headers["Authorization"] = authorization
        logger.info(f"使用HMAC-SHA256鉴权：{authorization[:20]}...")
            
        # 如果还提供了API密钥和密钥（兼容老的鉴权方式）
        if api_key and api_secret:
            headers["X-Bce-Auth"] = f"bce-auth-v1/{api_key}/{api_secret}"
            logger.info(f"使用X-Bce-Auth鉴权：{api_key[:5]}...")
        
        # 记录完整请求信息，便于调试
        logger.info(f"查询高级视频任务请求URL: {url}")
        logger.info(f"查询高级视频任务请求头: {headers}")
            
        # 发送请求
        response = requests.get(
            url,
            headers=headers
        )
        
        # 增强日志：记录原始响应状态和内容
        logger.info(f"百度数字人查询API原始响应状态码: {response.status_code}")
        logger.info(f"百度数字人查询API原始响应内容: {response.text}")
        
        # 检查响应状态
        if response.status_code != 200:
            logger.error(f"百度数字人高级视频API查询失败，状态码: {response.status_code}, 响应内容: {response.text}")
            # 增强日志：记录请求详情
            logger.error(f"失败查询的详细信息 - URL: {url}")
            logger.error(f"失败查询的详细信息 - 请求头: {headers}")
            return {
                "status": "failed",
                "error": {
                    "code": response.status_code,
                    "message": f"API请求失败: {response.text}"
                }
            }
            
        # 解析响应内容
        result = response.json()
        logger.info(f"百度数字人高级视频API查询成功，响应内容: {json.dumps(result, ensure_ascii=False)}")
        
        # 检查API返回结果
        if not result.get("success") or result.get("code") != 0:
            error_message = result.get("message", {}).get("global", "未知错误")
            logger.error(f"百度数字人高级视频API查询返回错误: {error_message}")
            # 增强日志：记录更多错误详情
            logger.error(f"百度数字人高级视频API查询错误码: {result.get('code')}")
            logger.error(f"百度数字人高级视频API完整错误响应: {json.dumps(result, ensure_ascii=False)}")
            
            # 对特定错误进行更详细的日志记录
            if "message" in result and isinstance(result["message"], dict):
                for field, field_errors in result["message"].items():
                    if field != "global":
                        logger.error(f"字段'{field}'查询错误: {field_errors}")
            
            return {
                "status": "failed",
                "error": {
                    "code": result.get("code"),
                    "message": error_message
                }
            }
            
        # 返回成功结果
        return {
            "status": "success",
            "data": result.get("result", {}),
            "requestId": result.get("requestId")
        }
    except Exception as e:
        logger.error(f"查询百度数字人高级视频合成任务异常: {str(e)}")
        return {
            "status": "failed",
            "error": {
                "code": 500,
                "message": f"服务异常: {str(e)}"
            }
        } 