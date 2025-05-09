#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件上传API接口模块
处理各种文件上传到百度云BOS存储的API路由
"""

import os
import uuid
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from baidubce.services.bos.bos_client import BosClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
import base64
import hashlib
from io import BytesIO
import mimetypes
import tempfile
from PIL import Image

# 导入服务
from app.services.baidubce_upload import (
    upload_file,
    upload_image_file,
    upload_video,
    upload_from_url,
    upload_from_base64
)

# 配置日志
logger = logging.getLogger(__name__)

# 创建蓝图
upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image_api():
    """
    上传图片API接口
    接受表单文件上传、URL或Base64数据
    ---
    parameters:
      - name: file
        in: formData
        type: file
        description: 要上传的图片文件
      - name: url
        in: formData
        type: string
        description: 图片URL
      - name: base64
        in: formData
        type: string
        description: Base64编码的图片数据
      - name: type
        in: formData
        type: string
        description: 图片类型，用于构建存储路径
    responses:
      200:
        description: 上传成功
        schema:
          properties:
            success:
              type: boolean
            url:
              type: string
              description: 上传后的图片URL
      400:
        description: 请求参数错误
      500:
        description: 服务器错误
    """
    try:
        user_id = get_jwt_identity()
        logger.info(f"用户[{user_id}]请求上传图片")
        
        # 获取图片类型参数，用于构建存储路径
        image_type = request.form.get('type', 'general')
        
        # 检查是否有文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                logger.info(f"开始处理文件上传，文件名: {file.filename}")
                image_url = upload_image_file(file, image_type=image_type)
                
                if image_url:
                    return jsonify({
                        "success": True,
                        "url": image_url
                    })
                else:
                    return jsonify({
                        "success": False,
                        "message": "图片上传失败"
                    }), 500
        
        # 检查是否提供URL
        elif 'url' in request.form and request.form['url']:
            url = request.form['url']
            logger.info(f"开始处理URL上传: {url[:50]}...")
            image_url = upload_from_url(url, prefix=f"images/{image_type}")
            
            if image_url:
                return jsonify({
                    "success": True,
                    "url": image_url
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "从URL上传图片失败"
                }), 500
        
        # 检查是否提供Base64数据
        elif 'base64' in request.form and request.form['base64']:
            base64_data = request.form['base64']
            logger.info("开始处理Base64图片上传")
            image_url = upload_from_base64(base64_data, prefix=f"images/{image_type}")
            
            if image_url:
                return jsonify({
                    "success": True,
                    "url": image_url
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "从Base64上传图片失败"
                }), 500
        
        # 如果没有任何有效的图片数据
        else:
            return jsonify({
                "success": False,
                "message": "未提供有效的图片数据"
            }), 400
            
    except Exception as e:
        logger.error(f"上传图片处理异常: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"上传图片处理异常: {str(e)}"
        }), 500

@upload_bp.route('/video', methods=['POST'])
@jwt_required()
def upload_video_api():
    """
    上传视频API接口
    接受表单文件上传
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: 要上传的视频文件
      - name: type
        in: formData
        type: string
        description: 视频类型，用于构建存储路径
    responses:
      200:
        description: 上传成功
        schema:
          properties:
            success:
              type: boolean
            url:
              type: string
              description: 上传后的视频URL
      400:
        description: 请求参数错误
      500:
        description: 服务器错误
    """
    try:
        user_id = get_jwt_identity()
        logger.info(f"用户[{user_id}]请求上传视频")
        
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "message": "未上传视频文件"
            }), 400
            
        file = request.files['file']
        if not file or not file.filename:
            return jsonify({
                "success": False,
                "message": "未选择视频文件"
            }), 400
            
        # 获取视频类型参数，用于构建存储路径
        video_type = request.form.get('type', 'general')
        
        logger.info(f"开始处理视频上传，文件名: {file.filename}, 类型: {video_type}")
        video_url = upload_video(file, video_type=video_type)
        
        if video_url:
            return jsonify({
                "success": True,
                "url": video_url
            })
        else:
            return jsonify({
                "success": False,
                "message": "视频上传失败"
            }), 500
            
    except Exception as e:
        logger.error(f"上传视频处理异常: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"上传视频处理异常: {str(e)}"
        }), 500

@upload_bp.route('/file', methods=['POST'])
@jwt_required()
def upload_file_api():
    """
    通用文件上传API接口
    接受任何类型的文件上传
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: 要上传的文件
      - name: prefix
        in: formData
        type: string
        description: 存储路径前缀
    responses:
      200:
        description: 上传成功
        schema:
          properties:
            success:
              type: boolean
            url:
              type: string
              description: 上传后的文件URL
      400:
        description: 请求参数错误
      500:
        description: 服务器错误
    """
    try:
        user_id = get_jwt_identity()
        logger.info(f"用户[{user_id}]请求上传文件")
        
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "message": "未上传文件"
            }), 400
            
        file = request.files['file']
        if not file or not file.filename:
            return jsonify({
                "success": False,
                "message": "未选择文件"
            }), 400
            
        # 获取存储路径前缀
        prefix = request.form.get('prefix', 'files')
        
        logger.info(f"开始处理文件上传，文件名: {file.filename}, 前缀: {prefix}")
        file_url = upload_file(file, prefix=prefix)
        
        if file_url:
            return jsonify({
                "success": True,
                "url": file_url
            })
        else:
            return jsonify({
                "success": False,
                "message": "文件上传失败"
            }), 500
            
    except Exception as e:
        logger.error(f"上传文件处理异常: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"上传文件处理异常: {str(e)}"
        }), 500

# 添加百度云BOS相关配置和函数
def get_bos_client():
    """获取百度云BOS客户端"""
    access_key_id = os.environ.get("BAIDU_BCE_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("BAIDU_BCE_SECRET_ACCESS_KEY")
    endpoint = os.environ.get("BAIDU_BOS_ENDPOINT", "bj.bcebos.com")
    
    if not access_key_id or not access_key_secret:
        raise ValueError("百度云BOS访问密钥未配置")
        
    # 创建认证凭证
    credentials = BceCredentials(access_key_id, access_key_secret)
    
    # 创建客户端配置
    config = BceClientConfiguration(
        credentials=credentials,
        endpoint=endpoint
    )
    
    # 创建BOS客户端
    return BosClient(config)

def calculate_md5(data):
    """计算二进制数据的MD5值并进行Base64编码"""
    md5 = hashlib.md5()
    md5.update(data)
    return base64.standard_b64encode(md5.digest()).decode('utf-8')

def upload_to_bos(file_data, content_type, bucket_name=None, object_key=None):
    """上传文件到百度云BOS存储
    
    Args:
        file_data: 文件二进制数据
        content_type: 文件MIME类型
        bucket_name: 存储桶名称，默认从环境变量获取
        object_key: 对象键，默认自动生成
        
    Returns:
        url: 上传成功后的URL
    """
    try:
        # 获取BOS客户端
        client = get_bos_client()
        
        # 获取bucket_name，如果未提供则使用环境变量中的值
        if not bucket_name:
            bucket_name = os.environ.get("BAIDU_BOS_BUCKET", "ezijing")
        
        # 检查存储桶是否存在
        if not client.does_bucket_exist(bucket_name):
            raise ValueError(f"存储桶 {bucket_name} 不存在")
        
        # 如果未提供对象键，则自动生成
        if not object_key:
            date_prefix = datetime.now().strftime("%Y%m%d")
            file_ext = mimetypes.guess_extension(content_type) or ""
            if not file_ext and content_type == "image/jpeg":
                file_ext = ".jpg"
            elif not file_ext and content_type == "image/png":
                file_ext = ".png"
                
            random_name = str(uuid.uuid4()).replace("-", "")
            object_key = f"uploads/{date_prefix}/{random_name}{file_ext}"
        
        # 计算MD5值
        content_md5 = calculate_md5(file_data)
        
        # 上传到BOS
        response = client.put_object(
            bucket_name=bucket_name,
            key=object_key,
            data=BytesIO(file_data),
            content_length=len(file_data),
            content_type=content_type,
            content_md5=content_md5
        )
        
        # 构建URL
        url = f"https://{bucket_name}.bj.bcebos.com/{object_key}"
        return url
    except Exception as e:
        current_app.logger.error(f"上传到百度云BOS失败: {str(e)}")
        raise e

# 添加百度云BOS上传图片接口
@upload_bp.route('/bos/image', methods=['POST'])
@jwt_required()
def upload_image_to_bos():
    """上传图片到百度云BOS存储
    
    请求参数:
        file: 图片文件
        type: 图片类型 (background|logo)
        
    返回:
        success: 是否成功
        url: 上传成功的URL
        message: 错误信息
    """
    try:
        # 检查是否存在文件
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "没有选择文件"}), 400
            
        file = request.files['file']
        
        # 检查文件是否有效
        if file.filename == '':
            return jsonify({"success": False, "message": "没有选择文件"}), 400
            
        # 获取文件类型
        file_type = request.form.get('type', 'image')
        
        # 检查文件类型和大小
        if not file.content_type.startswith('image/'):
            return jsonify({"success": False, "message": "仅支持图片文件"}), 400
            
        # 根据类型设置大小限制
        file_size_limit = 5 * 1024 * 1024  # 默认5MB
        if file_type == 'logo':
            file_size_limit = 2 * 1024 * 1024  # Logo限制2MB
            
        file_data = file.read()
        file_size = len(file_data)
        
        if file_size > file_size_limit:
            limit_mb = file_size_limit / (1024 * 1024)
            return jsonify({
                "success": False, 
                "message": f"文件大小超过限制，最大{limit_mb}MB"
            }), 400
        
        # 处理图片 - 读取图片并进行处理
        try:
            img = Image.open(BytesIO(file_data))
            
            # 检查图片格式
            img_format = img.format
            if img_format not in ['JPEG', 'PNG']:
                return jsonify({"success": False, "message": "仅支持JPG和PNG格式图片"}), 400
                
            # 获取MIME类型
            content_type = f"image/{img_format.lower()}"
            if img_format == 'JPEG':
                content_type = "image/jpeg"
            
            # 保存处理后的图片到临时内存
            output = BytesIO()
            
            # 如果是JPEG，设置质量
            if img_format == 'JPEG':
                img.save(output, format=img_format, quality=90)
            else:
                img.save(output, format=img_format)
                
            output.seek(0)
            processed_data = output.getvalue()
            
            # 上传到百度云BOS
            url = upload_to_bos(
                processed_data, 
                content_type=content_type
            )
            
            return jsonify({
                "success": True,
                "url": url,
                "message": "图片上传成功"
            })
        except Exception as img_error:
            current_app.logger.error(f"处理图片时出错: {str(img_error)}")
            return jsonify({
                "success": False,
                "message": f"处理图片时出错: {str(img_error)}"
            }), 400
    except Exception as e:
        current_app.logger.error(f"上传图片到百度云BOS时出错: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"上传失败: {str(e)}"
        }), 500 