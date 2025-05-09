#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字人PPT讲解视频API接口
提供创建PPT讲解视频任务和查询任务状态的API接口
"""

from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import logging
import uuid
from werkzeug.utils import secure_filename
import json
import requests

# 导入服务
from app.services.digital_human.digital_human_service import (
    get_digital_humans as local_get_digital_humans,
    get_digital_human_postures,
    get_supported_resolutions,
    create_ppt_video_task,
    query_ppt_video_task,
    get_task_history,
    upload_to_oss
)

# 添加导入小冰API的数字人获取函数
from app.services.aibeings_ppt_video import (
    get_digital_humans as aibeings_get_digital_humans,
    get_voice_list,
    get_digital_human_detail
)

# 配置日志
logger = logging.getLogger(__name__)

# 创建蓝图，不包含重复的url_prefix
digital_human_ppt_bp = Blueprint('digital_human_ppt', __name__)

# 允许的文件类型
ALLOWED_PPT_EXTENSIONS = {'ppt', 'pptx', 'pdf'}

# 上传文件临时保存目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'uploads')

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件类型是否允许上传"""
    # 只基于文件扩展名判断，避免内容类型判断过于严格
    try:
        # 防止无扩展名文件导致异常
        if '.' not in filename:
            logger.warning(f"文件无扩展名: {filename}")
            return False
            
        extension = filename.rsplit('.', 1)[1].lower()
        is_allowed = extension in ALLOWED_PPT_EXTENSIONS
        
        if not is_allowed:
            logger.warning(f"不支持的文件类型: {extension}, 文件名: {filename}")
        
        return is_allowed
    except Exception as e:
        logger.error(f"文件类型检查异常: {str(e)}, 文件名: {filename}")
        return False

@digital_human_ppt_bp.route('/ppt/humans', methods=['GET'])
def api_get_digital_humans():
    """
    获取可用的数字人列表
    ---
    responses:
      200:
        description: 数字人列表
    """
    try:
        # 使用小冰API获取数字人列表
        logger.info("开始从小冰API获取数字人列表")
        result = aibeings_get_digital_humans()
        
        # 如果小冰API调用失败，直接返回错误信息
        if "status" in result and result["status"] == "failed":
            error_message = result.get('error', {}).get('message', '未知错误')
            logger.error(f"小冰API获取数字人列表失败：{error_message}")
            return jsonify({
                "code": 500,
                "message": f"获取数字人列表失败: {error_message}",
                "data": None
            }), 500
            
        logger.info(f"成功获取数字人列表，返回结果")
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取数字人列表失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取数字人列表失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/postures/<virtual_human_id>', methods=['GET'])
def api_get_digital_human_postures(virtual_human_id):
    """
    获取指定数字人的姿势列表
    ---
    parameters:
      - name: virtual_human_id
        in: path
        required: true
        type: string
        description: 数字人ID
    responses:
      200:
        description: 姿势列表
    """
    try:
        result = get_digital_human_postures(virtual_human_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取数字人姿势列表失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取数字人姿势列表失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/voices', methods=['GET'])
def api_get_voice_list():
    """
    获取TTS语音列表
    
    :return: 包含所有可用TTS语音的列表，格式为：
    {
        "code": 0,
        "msg": "success",
        "data": [
            {
                "bizId": "string",
                "voiceId": "string",
                "name": "string",
                "language": "string",
                "auditionFile": "string",
                "supportInteractive": boolean
            },
            ...
        ]
    }
    """
    try:
        logger.info("正在获取语音列表...")
        result = get_voice_list()
        
        # 检查是否成功获取结果
        if "status" in result and result["status"] == "failed":
            logger.error(f"获取语音列表失败: {result['error']['message']}")
            return jsonify({
                "code": 500,
                "msg": "获取语音列表失败",
                "error": result["error"]
            }), 500
        
        # 确保兼容前端预期的数据格式
        if "data" in result:
            return jsonify({
                "code": 0,
                "msg": "success",
                "data": result["data"]
            })
        else:
            logger.warning(f"语音列表API返回格式不符合预期: {result}")
            return jsonify({
                "code": 0,
                "msg": "success",
                "data": result  # 如果没有data字段，直接返回整个结果
            })
            
    except Exception as e:
        logger.error(f"获取语音列表时发生错误: {str(e)}")
        return jsonify({
            "code": 500,
            "msg": "获取语音列表失败",
            "error": {
                "message": str(e)
            }
        }), 500

@digital_human_ppt_bp.route('/ppt/human/<biz_id>', methods=['GET'])
def api_get_digital_human_detail(biz_id):
    """
    获取指定数字人的详细信息
    ---
    parameters:
      - name: biz_id
        in: path
        required: true
        type: string
        description: 数字人业务ID
    responses:
      200:
        description: 数字人详情信息
    """
    try:
        logger.info(f"开始获取数字人详情，bizId: {biz_id}")
        if not biz_id:
            return jsonify({
                "code": 400,
                "message": "数字人ID不能为空",
                "data": None
            }), 400
            
        result = get_digital_human_detail(biz_id)
        
        # 检查结果是否有错误信息
        if "status" in result and result["status"] == "failed":
            error_message = result.get('error', {}).get('message', '未知错误')
            logger.error(f"获取数字人详情失败：{error_message}")
            return jsonify({
                "code": 500,
                "message": f"获取数字人详情失败: {error_message}",
                "data": None
            }), 500
        
        logger.info(f"成功获取数字人详情，返回结果")
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取数字人详情异常: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取数字人详情失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/resolutions', methods=['GET'])
def api_get_supported_resolutions():
    """
    获取支持的视频分辨率
    ---
    responses:
      200:
        description: 支持的分辨率列表
    """
    try:
        resolutions = get_supported_resolutions()
        return jsonify({
            "code": 0,
            "data": resolutions,
            "message": "success"
        })
    except Exception as e:
        logger.error(f"获取支持的分辨率失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取支持的分辨率失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/video', methods=['POST'])
@digital_human_ppt_bp.route('/ppt/generate', methods=['POST'])
@jwt_required()
def api_create_ppt_video_task():
    """
    创建PPT讲解视频任务
    ---
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: ppt_file
        in: formData
        required: true
        type: file
        description: PPT文件
      - name: text_script
        in: formData
        required: false
        type: string
        description: 讲解文本脚本，不提供则使用PPT备注
      - name: virtual_human_id
        in: formData
        required: false
        type: string
        description: 数字人ID，不提供则使用默认数字人
      - name: virtual_human_posture_id
        in: formData
        required: false
        type: string
        description: 数字人姿势ID，不提供则使用默认姿势
      - name: background_music_url
        in: formData
        required: false
        type: string
        description: 背景音乐URL，不提供则使用默认背景音乐
      - name: background_image_url
        in: formData
        required: false
        type: string
        description: 背景图片URL，不提供则使用白色背景
      - name: show_caption
        in: formData
        required: false
        type: boolean
        description: 是否显示字幕，默认显示
      - name: title
        in: formData
        required: false
        type: string
        description: 视频标题，默认为"PPT讲解视频"
      - name: resolution
        in: formData
        required: false
        type: string
        description: 视频分辨率，支持720p、1080p、480p，默认720p
      - name: convert_type
        in: formData
        required: false
        type: string
        description: PPT转换类型，IMG或VIDEO，默认VIDEO
    responses:
      200:
        description: 任务创建结果
    """
    try:
        # 获取当前用户ID
        current_user_id = get_jwt_identity()
        logger.info(f"接收到PPT视频任务创建请求，用户ID: {current_user_id}")
        
        logger.info(f"请求方法: {request.method}")
        
        # 检查请求内容类型
        if request.content_type and 'application/json' in request.content_type:
            logger.info("接收到JSON格式请求")
            req_json = request.json
            
            # 记录详细的请求参数
            logger.info(f"ppt_url: {req_json.get('pptUrl')}")
            logger.info(f"outputVideoName: {req_json.get('outputVideoName')}")
            logger.info(f"width: {req_json.get('width')}")
            logger.info(f"height: {req_json.get('height')}")
            logger.info(f"virtualHumanId: {req_json.get('virtualHumanId')}")
            logger.info(f"virtualHumanPostureId: {req_json.get('virtualHumanPostureId')}")
            logger.info(f"textScript: {req_json.get('textScript')}")
            logger.info(f"backgroundMusicUrl: {req_json.get('backgroundMusicUrl')}")
            logger.info(f"backgroundImageUrl: {req_json.get('backgroundImageUrl')}")
            logger.info(f"showCaption: {req_json.get('showCaption')}")
            logger.info(f"convertType: {req_json.get('convertType')}")
            
            ppt_url = req_json.get('pptUrl')
            title = req_json.get('outputVideoName')
            width = req_json.get('width', 1280)
            height = req_json.get('height', 720)
            resolution = f"{width}x{height}"
            virtual_human_id = req_json.get('virtualHumanId')
            virtual_human_posture_id = req_json.get('virtualHumanPostureId')
            text_script = req_json.get('textScript')
            background_music_url = req_json.get('backgroundMusicUrl')
            background_image_url = req_json.get('backgroundImageUrl')
            show_caption = req_json.get('showCaption', False)
            convert_type = req_json.get('convertType', 'all')
            
            # 创建PPT视频任务
            task_data = create_ppt_video_task(
                user_id=current_user_id,
                ppt_url=ppt_url,
                title=title,
                resolution=resolution,
                virtual_human_id=virtual_human_id,
                virtual_human_posture_id=virtual_human_posture_id,
                text_script=text_script,
                background_music_url=background_music_url,
                background_image_url=background_image_url,
                show_caption=show_caption,
                convert_type=convert_type
            )
            
            logger.info(f"创建任务成功，任务ID: {task_data.get('task_id')}")
            
            return jsonify({
                'code': 0,
                'data': task_data,
                'message': '创建任务成功'
            })
        else:
            logger.info("接收到Form格式请求")
            # 获取表单数据
            ppt_file = request.files.get('ppt_file')
            title = request.form.get('title')
            resolution = request.form.get('resolution')
            virtual_human_id = request.form.get('virtual_human_id')
            virtual_human_posture_id = request.form.get('virtual_human_posture_id')
            text_script = request.form.get('text_script')
            background_music_url = request.form.get('background_music_url')
            background_image_url = request.form.get('background_image_url')
            show_caption = request.form.get('show_caption', 'false').lower() == 'true'
            convert_type = request.form.get('convert_type', 'all')
            
            logger.info(f"表单数据：title={title}, resolution={resolution}, "
                      f"virtual_human_id={virtual_human_id}, virtual_human_posture_id={virtual_human_posture_id}")
            
            if ppt_file:
                logger.info(f"接收到文件: {ppt_file.filename}")
                # 创建PPT视频任务
                task_data = create_ppt_video_task(
                    user_id=current_user_id,
                    ppt_file_path=ppt_file,
                    title=title,
                    resolution=resolution,
                    virtual_human_id=virtual_human_id,
                    virtual_human_posture_id=virtual_human_posture_id,
                    text_script=text_script,
                    background_music_url=background_music_url,
                    background_image_url=background_image_url,
                    show_caption=show_caption,
                    convert_type=convert_type
                )
                
                logger.info(f"创建任务成功，任务ID: {task_data.get('task_id')}")
                
                return jsonify({
                    'code': 0,
                    'data': task_data,
                    'message': '创建任务成功'
                })
            else:
                logger.error("未接收到PPT文件")
                return jsonify({
                    'code': 1,
                    'message': '未接收到PPT文件'
                }), 400
    except Exception as e:
        logger.exception(f"创建PPT视频任务失败: {str(e)}")
        return jsonify({
            'code': 1,
            'message': f'创建任务失败: {str(e)}'
        }), 500

@digital_human_ppt_bp.route('/ppt/video/<task_id>', methods=['GET'])
@digital_human_ppt_bp.route('/ppt/video/<task_id>/status', methods=['GET'])
def api_get_ppt_video_task(task_id):
    """
    查询PPT讲解视频任务状态
    ---
    parameters:
      - name: task_id
        in: path
        required: true
        type: string
        description: 任务ID
    responses:
      200:
        description: 任务状态信息
    """
    try:
        result = query_ppt_video_task(task_id)
        return jsonify({
            "code": 0,
            "data": result,
            "message": "success"
        })
    except Exception as e:
        logger.error(f"查询任务状态失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"查询任务状态失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/task/<task_id>', methods=['GET'])
def api_get_ppt_task(task_id):
    """
    查询PPT讲解视频任务状态（新接口）
    ---
    parameters:
      - name: task_id
        in: path
        required: true
        type: string
        description: 任务ID
    responses:
      200:
        description: 任务状态信息
    """
    try:
        result = query_ppt_video_task(task_id)
        return jsonify({
            "code": 0,
            "data": result,
            "message": "success"
        })
    except Exception as e:
        logger.error(f"查询任务状态失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"查询任务状态失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/history', methods=['GET'])
@jwt_required()
def api_get_task_history():
    """获取任务历史记录"""
    try:
        # 从JWT中获取当前用户ID
        user_id = get_jwt_identity()
        logger.info(f"获取用户 {user_id} 的任务历史记录")
        
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 调用服务层函数获取历史记录
        result = get_task_history(user_id, page, per_page)
        
        # 检查是否有错误
        if result.get("status") == "failed":
            return jsonify({
                "code": result["error"].get("code", 500),
                "message": result["error"].get("message", "获取历史记录失败"),
                "data": None
            }), 500
        
        # 返回成功结果
        return jsonify({
            "code": 0,
            "message": "成功获取任务历史记录",
            "data": result
        })
    
    except Exception as e:
        logger.exception(f"获取历史记录异常: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取历史记录异常: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/upload', methods=['POST'])
def api_upload_ppt():
    """
    上传PPT文件
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        required: true
        type: file
        description: PPT文件
    responses:
      200:
        description: 上传成功，返回文件URL
    """
    try:
        # 记录请求信息
        logger.info(f"接收到PPT文件上传请求，Content-Type: {request.content_type}")
        
        # 检查是否有文件
        if 'file' not in request.files:
            logger.error("未找到上传的文件")
            return jsonify({
                "code": 400,
                "message": "未找到上传的文件",
                "data": None
            }), 400
            
        file = request.files['file']
        logger.info(f"接收到文件: {file.filename}, 类型: {file.content_type}, 大小: {file.content_length}")
        
        # 检查文件名
        if file.filename == '':
            logger.error("未选择文件")
            return jsonify({
                "code": 400,
                "message": "未选择文件",
                "data": None
            }), 400
            
        # 检查文件类型是否允许
        if not allowed_file(file.filename):
            logger.error(f"不支持的文件类型: {file.filename}")
            return jsonify({
                "code": 400,
                "message": f"不支持的文件类型，仅支持: {', '.join(ALLOWED_PPT_EXTENSIONS)}",
                "data": None
            }), 400
        
        # 记录文件信息
        logger.info(f"文件类型检查通过: {file.filename}")
            
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
        
        # 保存文件
        file.save(temp_path)
        logger.info(f"文件已保存到临时目录: {temp_path}, 大小: {os.path.getsize(temp_path)}")
        
        try:
            # 上传到OSS
            logger.info(f"开始上传文件到OSS: {temp_path}")
            url = upload_to_oss(temp_path)
            if not url:
                logger.error("文件上传到OSS失败")
                return jsonify({
                    "code": 500,
                    "message": "文件上传到OSS失败，请检查OSS配置和网络连接",
                    "data": None
                }), 500
                
            logger.info(f"文件已成功上传到OSS: {url}")
            
            # 返回成功响应
            return jsonify({
                "code": 0,
                "data": {
                    "url": url,
                    "filename": filename
                },
                "message": "文件上传成功"
            })
            
        finally:
            # 清理临时文件
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    logger.info(f"临时文件已删除: {temp_path}")
            except Exception as e:
                logger.warning(f"删除临时文件失败: {str(e)}")
                
    except Exception as e:
        logger.exception(f"文件上传过程发生异常: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"文件上传失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/ppt/submit_task', methods=['POST'])
def api_submit_ppt_video_task():
    """
    提交PPT讲解视频任务到小冰API
    ---
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            pptUrl:
              type: string
              description: PPT文件URL
            outputVideoName:
              type: string
              description: 视频标题
            width:
              type: integer
              description: 视频宽度
            height:
              type: integer
              description: 视频高度
            virtualHumanId:
              type: string
              description: 数字人ID
            virtualHumanPostureId:
              type: string
              description: 数字人姿势ID
            textScript:
              type: string
              description: 讲解文本脚本
            backgroundMusicUrl:
              type: string
              description: 背景音乐URL
            backgroundImageUrl:
              type: string
              description: 背景图片URL
            showCaption:
              type: boolean
              description: 是否显示字幕
            convertType:
              type: string
              description: PPT转换类型
    responses:
      200:
        description: 任务提交结果
    """
    try:
        # 获取请求数据
        req_json = request.json
        logger.info("接收到PPT视频任务提交请求")
        logger.info(f"请求数据: {json.dumps(req_json, ensure_ascii=False)}")
        
        # 配置小冰API请求
        api_url = "https://openapi.xiaoice.com/vh/openapi/video/task/v2/ppt/submit"
        headers = {
            "Content-Type": "application/json",
            "subscription-key": "282cd94b697e48e6aca6d20bbdaf0d0f"
        }
        
        # 发送请求到小冰API
        logger.info(f"转发请求到小冰API: {api_url}")
        response = requests.post(api_url, headers=headers, json=req_json, timeout=60)
        response.raise_for_status()
        
        # 获取API响应
        result = response.json()
        logger.info(f"小冰API响应: {json.dumps(result, ensure_ascii=False)}")
        
        # 返回API响应
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        logger.error(f"提交任务到小冰API时发生请求异常: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'提交任务失败，API请求异常: {str(e)}',
            'error': True
        }), 500
    except Exception as e:
        logger.exception(f"提交PPT视频任务失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'提交任务失败: {str(e)}',
            'error': True
        }), 500