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

# 导入服务
from app.services.digital_human.digital_human_service import (
    get_digital_humans,
    get_digital_human_postures,
    get_supported_resolutions,
    create_ppt_video_task,
    query_ppt_video_task,
    get_task_history
)

# 配置日志
logger = logging.getLogger(__name__)

# 创建Blueprint
digital_human_ppt_bp = Blueprint('digital_human_ppt', __name__, url_prefix='/api/v1/digital_human/ppt')

# 允许的文件类型
ALLOWED_PPT_EXTENSIONS = {'ppt', 'pptx', 'pdf'}

# 上传文件临时保存目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'uploads')

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件类型是否允许上传"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PPT_EXTENSIONS

@digital_human_ppt_bp.route('/humans', methods=['GET'])
def api_get_digital_humans():
    """
    获取可用的数字人列表
    ---
    responses:
      200:
        description: 数字人列表
    """
    try:
        result = get_digital_humans()
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取数字人列表失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取数字人列表失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/postures/<virtual_human_id>', methods=['GET'])
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

@digital_human_ppt_bp.route('/resolutions', methods=['GET'])
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

@digital_human_ppt_bp.route('/generate', methods=['POST'])
def api_create_ppt_video_task():
    """
    创建PPT讲解视频任务
    ---
    consumes:
      - multipart/form-data
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
        # 检查请求中是否包含文件
        if 'ppt_file' not in request.files:
            return jsonify({
                "code": 400,
                "message": "请提供PPT文件",
                "data": None
            }), 400
        
        file = request.files['ppt_file']
        
        # 检查文件是否为空
        if file.filename == '':
            return jsonify({
                "code": 400,
                "message": "文件名为空",
                "data": None
            }), 400
        
        # 检查文件类型是否允许
        if not allowed_file(file.filename):
            return jsonify({
                "code": 400,
                "message": f"文件类型不允许，只支持PPT、PPTX和PDF文件",
                "data": None
            }), 400
        
        # 安全地获取文件名并添加UUID前缀以避免文件名冲突
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存文件到临时目录
        file.save(file_path)
        logger.info(f"PPT文件已保存到临时目录: {file_path}")
        
        # 获取其他参数
        text_script = request.form.get('text_script')
        virtual_human_id = request.form.get('virtual_human_id')
        virtual_human_posture_id = request.form.get('virtual_human_posture_id')
        background_music_url = request.form.get('background_music_url')
        background_image_url = request.form.get('background_image_url')
        show_caption = request.form.get('show_caption', 'true').lower() == 'true'
        title = request.form.get('title', 'PPT讲解视频')
        resolution = request.form.get('resolution', '720p')
        convert_type = request.form.get('convert_type', 'VIDEO')
        
        # 创建任务
        task_result = create_ppt_video_task(
            ppt_file_path=file_path,
            text_script=text_script,
            virtual_human_id=virtual_human_id,
            virtual_human_posture_id=virtual_human_posture_id,
            background_music_url=background_music_url,
            background_image_url=background_image_url,
            show_caption=show_caption,
            title=title,
            resolution=resolution,
            convert_type=convert_type
        )
        
        # 检查任务创建结果
        if task_result.get("status") == "failed":
            return jsonify({
                "code": 500,
                "message": task_result.get("error", {}).get("message", "任务创建失败"),
                "data": None
            }), 500
        
        return jsonify({
            "code": 0,
            "data": task_result,
            "message": "success"
        })
        
    except Exception as e:
        logger.error(f"创建PPT讲解视频任务失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"创建PPT讲解视频任务失败: {str(e)}",
            "data": None
        }), 500

@digital_human_ppt_bp.route('/task/<task_id>', methods=['GET'])
def api_query_ppt_video_task(task_id):
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

@digital_human_ppt_bp.route('/history', methods=['GET'])
def api_get_task_history():
    """
    获取PPT讲解视频任务历史记录
    ---
    parameters:
      - name: limit
        in: query
        required: false
        type: integer
        description: 每页记录数，默认10
      - name: offset
        in: query
        required: false
        type: integer
        description: 偏移量，默认0
    responses:
      200:
        description: 任务历史记录
    """
    try:
        # 获取查询参数
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        # 调用服务方法获取历史记录
        result = get_task_history(limit, offset)
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取任务历史记录失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取任务历史记录失败: {str(e)}",
            "data": None
        }), 500