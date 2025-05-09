#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
百度数字人视频合成API接口
提供创建视频合成任务和查询任务状态的API接口
"""

from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import logging
import json

# 导入服务
from app.services.digital_human.baidu_digital_human_service import (
    submit_baidu_digital_human_video_task,
    query_baidu_digital_human_video_task,
    submit_baidu_digital_human_advanced_video_task,
    query_baidu_digital_human_advanced_video_task
)

# 配置日志
logger = logging.getLogger(__name__)

# 创建蓝图，不包含重复的url_prefix
baidu_digital_human_bp = Blueprint('baidu_digital_human', __name__)


@baidu_digital_human_bp.route('/video/submit', methods=['POST'])
def api_submit_baidu_digital_human_video_task():
    """
    提交百度数字人视频合成任务
    
    请求示例:
    {
        "text": "嗨！我是挥手问候家，为你打造专属问候，不论早晚，挥手间温暖送达！",
        "figureId": "A2A_V2-xinxin",  // 可选，默认为"A2A_V2-xinxin"
        "driveType": "TEXT",  // 可选，默认为"TEXT"
        "ttsParams": {  // 可选，有默认值
            "person": "5132", 
            "speed": "5",
            "pitch": "5",
            "volume": "5"
        },
        "videoParams": {  // 可选，有默认值
            "height": 1920,
            "width": 1080,
            "transparent": false
        },
        "autoAnimoji": true,  // 可选，默认为true
        "subtitleParams": {  // 可选，有默认值
            "enabled": false,
            "subtitlePolicy": "SRT"
        },
        "backgroundImageUrl": "",  // 可选，默认为空
        "callbackUrl": ""  // 可选，默认为空
    }
    
    成功响应示例:
    {
        "code": 0,
        "message": "视频合成任务提交成功",
        "data": {
            "taskId": "vid-qgti66nzkch2xy9h",
            "status": null,
            "failedCode": 0,
            "failedMessage": null,
            "videoUrl": null,
            "duration": 0,
            "createTime": null,
            "updateTime": null,
            "subtitleFileUrl": null
        },
        "success": true
    }
    
    失败响应示例:
    {
        "code": 400,
        "message": "请求参数错误",
        "data": null,
        "success": false
    }
    """
    try:
        # 获取请求数据
        request_data = request.get_json()
        
        # 记录请求（移除敏感信息）
        logger.info(f"收到百度数字人视频合成任务请求: {json.dumps(request_data, ensure_ascii=False)}")
        
        # 验证必要参数
        text = request_data.get('text')
        if not text:
            logger.error("缺少必要参数: text")
            return jsonify({
                "code": 400,
                "message": "缺少必要参数: text",
                "data": None,
                "success": False
            }), 400
            
        # 提取其他参数
        figure_id = request_data.get('figureId')
        drive_type = request_data.get('driveType')
        
        # 提取TTS参数
        tts_params = request_data.get('ttsParams', {})
        tts_person = tts_params.get('person')
        tts_speed = tts_params.get('speed')
        tts_volume = tts_params.get('volume')
        tts_pitch = tts_params.get('pitch')
        
        # 提取视频参数
        video_params = request_data.get('videoParams', {})
        video_width = video_params.get('width')
        video_height = video_params.get('height')
        transparent = video_params.get('transparent')
        
        # 提取其他选项
        background_image_url = request_data.get('backgroundImageUrl')
        callback_url = request_data.get('callbackUrl')
        auto_animoji = request_data.get('autoAnimoji')
        
        # 提取字幕参数
        subtitle_params = request_data.get('subtitleParams', {})
        subtitle_enabled = subtitle_params.get('enabled')
        
        # 从配置中获取API密钥（如果有）
        api_key = os.environ.get('BAIDU_DIGITAL_HUMAN_API_KEY')
        api_secret = os.environ.get('BAIDU_DIGITAL_HUMAN_API_SECRET')
        
        # 调用服务提交任务
        result = submit_baidu_digital_human_video_task(
            text=text,
            api_key=api_key,
            api_secret=api_secret,
            figure_id=figure_id,
            drive_type=drive_type,
            tts_person=tts_person,
            tts_speed=tts_speed,
            tts_volume=tts_volume,
            tts_pitch=tts_pitch,
            video_width=video_width,
            video_height=video_height,
            transparent=transparent,
            background_image_url=background_image_url,
            callback_url=callback_url,
            auto_animoji=auto_animoji,
            subtitle_enabled=subtitle_enabled
        )
        
        # 检查服务调用结果
        if result["status"] == "failed":
            error_code = result["error"].get("code", 500)
            error_message = result["error"].get("message", "未知错误")
            logger.error(f"提交百度数字人视频合成任务失败: {error_message}")
            return jsonify({
                "code": error_code,
                "message": error_message,
                "data": None,
                "success": False
            }), 200  # 即使是应用层面的错误，HTTP状态码仍返回200
            
        # 返回成功响应
        return jsonify({
            "code": 0,
            "message": "视频合成任务提交成功",
            "data": result["data"],
            "success": True
        }), 200
    except Exception as e:
        logger.error(f"提交百度数字人视频合成任务异常: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"服务异常: {str(e)}",
            "data": None,
            "success": False
        }), 500


@baidu_digital_human_bp.route('/video/query', methods=['GET'])
def api_query_baidu_digital_human_video_task():
    """
    查询百度数字人视频合成任务状态
    
    请求参数:
    - taskId: 任务ID
    
    成功响应示例:
    {
        "code": 0,
        "message": "查询成功",
        "data": {
            "taskId": "vid-qgti66nzkch2xy9h",
            "status": "SUCCESS",
            "failedCode": 0,
            "failedMessage": null,
            "videoUrl": "https://example.com/video.mp4",
            "duration": 10,
            "createTime": "2023-04-01T12:00:00Z",
            "updateTime": "2023-04-01T12:05:00Z",
            "subtitleFileUrl": null
        },
        "success": true
    }
    
    失败响应示例:
    {
        "code": 400,
        "message": "缺少任务ID",
        "data": null,
        "success": false
    }
    """
    try:
        # 获取任务ID
        task_id = request.args.get('taskId')
        
        # 验证任务ID
        if not task_id:
            logger.error("缺少必要参数: taskId")
            return jsonify({
                "code": 400,
                "message": "缺少必要参数: taskId",
                "data": None,
                "success": False
            }), 400
            
        # 记录请求
        logger.info(f"查询百度数字人视频合成任务状态，任务ID: {task_id}")
        
        # 从配置中获取API密钥（如果有）
        api_key = os.environ.get('BAIDU_DIGITAL_HUMAN_API_KEY')
        api_secret = os.environ.get('BAIDU_DIGITAL_HUMAN_API_SECRET')
        
        # 调用服务查询任务
        result = query_baidu_digital_human_video_task(
            task_id=task_id,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # 检查服务调用结果
        if result["status"] == "failed":
            error_code = result["error"].get("code", 500)
            error_message = result["error"].get("message", "未知错误")
            logger.error(f"查询百度数字人视频合成任务失败: {error_message}")
            return jsonify({
                "code": error_code,
                "message": error_message,
                "data": None,
                "success": False
            }), 200  # 即使是应用层面的错误，HTTP状态码仍返回200
            
        # 返回成功响应
        return jsonify({
            "code": 0,
            "message": "查询成功",
            "data": result["data"],
            "success": True
        }), 200
    except Exception as e:
        logger.error(f"查询百度数字人视频合成任务异常: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"服务异常: {str(e)}",
            "data": None,
            "success": False
        }), 500


@baidu_digital_human_bp.route('/video/advanced/submit', methods=['POST'])
def api_submit_baidu_digital_human_advanced_video_task():
    """
    提交百度数字人高级视频合成任务
    
    请求示例:
    {
        "figureId": "1081",
        "templateId": "t-ad4eeqsspfzwyqxyte125",
        "text": "有人说家是温馨的港湾...",
        "driveType": "TEXT",
        "title": "家装盛典福利等你来",
        "logoParams": {
            "logoUrl": "https://example.com/logo.png"
        },
        "bgmParams": {
            "bgmUrl": "https://example.com/bgm.mp3"
        },
        "materialUrl": "https://example.com/material.jpg",
        "ttsParams": {
            "person": "5132",
            "speed": "5",
            "volume": "5",
            "pitch": "5"
        },
        "videoParams": {
            "width": 1080,
            "height": 1920
        },
        "riskTip": "水印文字",
        "openingMaterial": {
            "fileUrl": "https://example.com/opening.mp4",
            "mediaType": "VIDEO"
        },
        "endingMaterial": {
            "fileUrl": "https://example.com/ending.mp4",
            "mediaType": "VIDEO"
        },
        "mashupMaterials": [
            {
                "fileUrl": "https://example.com/image1.jpg",
                "mediaType": "IMAGE"
            },
            {
                "fileUrl": "https://example.com/video1.mp4",
                "mediaType": "VIDEO"
            }
        ],
        "fissionParams": {
            "figureIds": ["1081", "1112"],
            "ttsPersons": ["4100", "5132"]
        }
    }
    
    成功响应示例:
    {
        "code": 0,
        "message": "高级视频合成任务提交成功",
        "data": {
            "taskId": "adv-qmutfwsptw57zegc-1112-4100",
            "fissionTasks": [...]
        },
        "success": true
    }
    
    失败响应示例:
    {
        "code": 400,
        "message": "请求参数错误",
        "data": null,
        "success": false
    }
    """
    try:
        # 获取请求数据
        request_data = request.get_json()
        
        # 记录详细的请求信息（移除敏感信息）
        safe_data = {k: v for k, v in request_data.items() if k != 'text'}
        logger.info(f"收到百度数字人高级视频合成任务请求: {json.dumps(safe_data, ensure_ascii=False)}")
        if 'text' in request_data:
            text_preview = request_data['text'][:50] + '...' if len(request_data['text']) > 50 else request_data['text']
            logger.info(f"请求文本内容(前50字符): {text_preview}")
        
        # 验证必要参数
        required_params = ['figureId', 'templateId', 'text']
        missing_params = [param for param in required_params if param not in request_data]
        if missing_params:
            missing_str = ', '.join(missing_params)
            logger.error(f"缺少必要参数: {missing_str}")
            return jsonify({
                "code": 400,
                "message": f"缺少必要参数: {missing_str}",
                "data": None,
                "success": False
            }), 400
                
        # 提取基本参数
        figure_id = request_data.get('figureId')
        template_id = request_data.get('templateId')
        text = request_data.get('text')
        drive_type = request_data.get('driveType')
        title = request_data.get('title')
        
        # 简单验证文本长度
        if len(text) < 5:
            logger.warning(f"文本内容过短: {len(text)}字符")
            return jsonify({
                "code": 400,
                "message": f"文本内容过短: {len(text)}字符，需要至少5个字符",
                "data": None,
                "success": False
            }), 400
        
        # 提取TTS参数
        tts_params = request_data.get('ttsParams', {})
        tts_person = tts_params.get('person')
        tts_speed = tts_params.get('speed')
        tts_volume = tts_params.get('volume')
        tts_pitch = tts_params.get('pitch')
        
        # 提取视频参数
        video_params = request_data.get('videoParams', {})
        video_width = video_params.get('width')
        video_height = video_params.get('height')
        
        # 提取其他可选参数
        logo_params = request_data.get('logoParams', {})
        logo_url = logo_params.get('logoUrl') if logo_params else None
        
        bgm_params = request_data.get('bgmParams', {})
        bgm_url = bgm_params.get('bgmUrl') if bgm_params else None
        
        material_url = request_data.get('materialUrl')
        callback_url = request_data.get('callbackUrl')
        risk_tip = request_data.get('riskTip')
        opening_material = request_data.get('openingMaterial')
        ending_material = request_data.get('endingMaterial')
        mashup_materials = request_data.get('mashupMaterials')
        fission_params = request_data.get('fissionParams')
        
        # 从配置中获取API密钥（如果有）
        api_key = os.environ.get('BAIDU_DIGITAL_HUMAN_API_KEY')
        api_secret = os.environ.get('BAIDU_DIGITAL_HUMAN_API_SECRET')
        
        # 调用服务提交任务
        result = submit_baidu_digital_human_advanced_video_task(
            figure_id=figure_id,
            template_id=template_id,
            text=text,
            tts_person=tts_person,
            video_width=video_width,
            video_height=video_height,
            api_key=api_key,
            api_secret=api_secret,
            drive_type=drive_type,
            tts_speed=tts_speed,
            tts_volume=tts_volume,
            tts_pitch=tts_pitch,
            title=title,
            logo_url=logo_url,
            bgm_url=bgm_url,
            material_url=material_url,
            callback_url=callback_url,
            risk_tip=risk_tip,
            opening_material=opening_material,
            ending_material=ending_material,
            mashup_materials=mashup_materials,
            fission_params=fission_params
        )
        
        # 检查服务调用结果
        if result["status"] == "failed":
            error_code = result["error"].get("code", 500)
            error_message = result["error"].get("message", "未知错误")
            more_detail = result["error"].get("more_detail", "")
            
            # 增强日志记录
            logger.error(f"提交百度数字人高级视频合成任务失败: 错误码={error_code}, 错误信息={error_message}")
            if more_detail:
                logger.error(f"错误详情: {more_detail}")
                
            # 记录详细的请求参数（排除敏感信息）
            safe_params = {
                'figure_id': figure_id,
                'template_id': template_id,
                'tts_person': tts_person,
                'video_width': video_width,
                'video_height': video_height,
                'material_url': material_url
            }
            logger.error(f"失败请求的参数: {json.dumps(safe_params, ensure_ascii=False)}")
            
            response_data = {
                "code": error_code,
                "message": error_message,
                "data": None,
                "success": False
            }
            
            # 针对特定错误提供更友好的提示
            if error_message == "模板校验异常":
                suggestions = f"模板ID '{template_id}' 无效或不存在。请确认模板ID是否正确，或尝试使用已知有效的模板，如't-pf4kqasspwzwyexyte121'。"
                response_data["suggestions"] = suggestions
                logger.info(f"提供模板校验异常建议: {suggestions}")
            elif error_message == "音色ID不存在":
                suggestions = f"语音合成人声ID '{tts_person}' 不存在或不受支持。请使用有效的人声ID，如'CAP_4146'。"
                response_data["suggestions"] = suggestions
                logger.info(f"提供音色ID建议: {suggestions}")
            elif error_message == "未识别错误":
                # 如果有更详细的错误信息，添加到响应中
                if more_detail:
                    response_data["more_detail"] = more_detail
                    response_data["suggestions"] = "请检查所有参数，特别是数字人ID、模板ID和TTS人声ID。"
                    
            return jsonify(response_data), 200  # 即使是应用层面的错误，HTTP状态码仍返回200
            
        # 返回成功响应
        return jsonify({
            "code": 0,
            "message": "高级视频合成任务提交成功",
            "data": result["data"],
            "success": True
        }), 200
    except Exception as e:
        logger.error(f"提交百度数字人高级视频合成任务异常: {str(e)}")
        # 记录更多异常信息
        import traceback
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        return jsonify({
            "code": 500,
            "message": f"服务异常: {str(e)}",
            "data": None,
            "success": False
        }), 500


@baidu_digital_human_bp.route('/video/advanced/query', methods=['GET'])
def api_query_baidu_digital_human_advanced_video_task():
    """
    查询百度数字人高级视频合成任务状态
    
    请求参数:
    - taskId: 任务ID
    
    成功响应示例:
    {
        "code": 0,
        "message": "查询成功",
        "data": {
            "taskId": "adv-qgti5xjyxx6e8yxu",
            "status": "GENERATING",
            "failedCode": 0,
            "failedMessage": "OK",
            "videoUrl": "",
            "duration": 20060,
            "createTime": "2024-08-06T15:17:46",
            "updateTime": "2024-08-06T15:17:46"
        },
        "success": true
    }
    
    失败响应示例:
    {
        "code": 400,
        "message": "缺少任务ID",
        "data": null,
        "success": false
    }
    """
    try:
        # 获取任务ID
        task_id = request.args.get('taskId')
        
        # 验证任务ID
        if not task_id:
            logger.error("缺少必要参数: taskId")
            return jsonify({
                "code": 400,
                "message": "缺少必要参数: taskId",
                "data": None,
                "success": False
            }), 400
            
        # 记录请求
        logger.info(f"查询百度数字人高级视频合成任务状态，任务ID: {task_id}")
        
        # 从配置中获取API密钥（如果有）
        api_key = os.environ.get('BAIDU_DIGITAL_HUMAN_API_KEY')
        api_secret = os.environ.get('BAIDU_DIGITAL_HUMAN_API_SECRET')
        
        # 调用服务查询任务
        result = query_baidu_digital_human_advanced_video_task(
            task_id=task_id,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # 检查服务调用结果
        if result["status"] == "failed":
            error_code = result["error"].get("code", 500)
            error_message = result["error"].get("message", "未知错误")
            logger.error(f"查询百度数字人高级视频合成任务失败: {error_message}")
            return jsonify({
                "code": error_code,
                "message": error_message,
                "data": None,
                "success": False
            }), 200  # 即使是应用层面的错误，HTTP状态码仍返回200
            
        # 返回成功响应
        return jsonify({
            "code": 0,
            "message": "查询成功",
            "data": result["data"],
            "success": True
        }), 200
    except Exception as e:
        logger.error(f"查询百度数字人高级视频合成任务异常: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"服务异常: {str(e)}",
            "data": None,
            "success": False
        }), 500 