#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
阿里云OSS图片上传专用模块
独立处理前端图片上传到阿里云OSS的功能
"""

import os
import uuid
import logging
import time
import oss2
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.services.aliyun_oss_service import upload_file_to_oss  # 阿里云OSS服务

# 设置日志
logger = logging.getLogger(__name__)

# 定义上传目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 创建独立蓝图，命名为aliyun_upload_bp，与其他蓝图区分开
aliyun_upload_bp = Blueprint('aliyun_upload', __name__)

def handle_image_upload():
    """
    处理图片上传到阿里云OSS的逻辑
    """
    try:
        logger.info("接收到图片上传请求 - 阿里云OSS专用路由")
        
        # 检查文件是否在请求中
        if 'image' not in request.files:
            logger.error("缺少图片文件")
            return jsonify({
                "success": False,
                "error": "请求参数错误: 缺少图片文件"
            }), 400
            
        file = request.files['image']
        if file.filename == '':
            logger.error("空的文件名")
            return jsonify({
                "success": False,
                "error": "请求参数错误: 空的文件名"
            }), 400
            
        # 检查文件类型
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            logger.error(f"不支持的文件格式: {file.filename}")
            return jsonify({
                "success": False,
                "error": "不支持的文件格式，请上传JPG、JPEG、PNG、GIF或WEBP格式的图片"
            }), 400
            
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存临时文件
        file.save(file_path)
        logger.info(f"已保存临时文件: {file_path}")
        
        # 尝试上传到阿里云OSS
        try:
            logger.info("开始上传到阿里云OSS...")
            
            # 从文件路径创建OSS bucket对象
            try:
                # 从环境变量获取OSS配置
                access_key_id = os.environ.get('ALIYUN_OSS_ACCESS_KEY_ID', os.environ.get('ALIYUN_ACCESS_KEY_ID'))
                access_key_secret = os.environ.get('ALIYUN_OSS_ACCESS_KEY_SECRET', os.environ.get('ALIYUN_ACCESS_KEY_SECRET'))
                endpoint = os.environ.get('ALIYUN_OSS_ENDPOINT', os.environ.get('ALIYUN_OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com'))
                bucket_name = os.environ.get('ALIYUN_OSS_BUCKET_NAME', os.environ.get('ALIYUN_OSS_BUCKET', 'ezijingai'))
                
                # 记录OSS配置信息（不包含敏感信息）
                logger.info(f"OSS配置信息: bucket={bucket_name}, endpoint={endpoint}")
                logger.info(f"AccessKey配置状态: ID存在={bool(access_key_id)}, Secret存在={bool(access_key_secret)}")
                
                # 创建认证和Bucket实例
                auth = oss2.Auth(access_key_id, access_key_secret)
                bucket = oss2.Bucket(auth, endpoint, bucket_name)
                
                # 确定文件对象键 (OSS中的路径)
                file_ext = os.path.splitext(filename)[1]
                object_key = f"uploaded-files/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}{file_ext}"
                
                # 直接从磁盘文件上传到OSS
                logger.info(f"从文件路径上传: {file_path} -> {object_key}")
                result = bucket.put_object_from_file(object_key, file_path)
                
                # 检查上传状态
                if result.status == 200:
                    # 构建OSS URL
                    oss_url = f"https://{bucket_name}.{endpoint}/{object_key}"
                    logger.info(f"文件直接从磁盘上传成功: {oss_url}")
                else:
                    logger.error(f"上传失败，OSS返回状态: {result.status}")
                    raise Exception(f"OSS返回非200状态: {result.status}")
            except Exception as e:
                logger.error(f"OSS直接上传异常: {str(e)}")
                # 回退到原来的方法
                logger.info("尝试使用备用上传方法...")
                # 文件读取位置重置到开始
                file.seek(0)
                oss_url = upload_file_to_oss(file, unique_filename, content_type=file.content_type)
            
            # 删除临时文件
            try:
                os.remove(file_path)
                logger.info(f"临时文件已删除: {file_path}")
            except Exception as e:
                logger.warning(f"删除临时文件失败: {str(e)}")
            
            # 返回成功响应
            logger.info(f"上传成功，OSS URL: {oss_url}")
            return jsonify({
                "success": True,
                "file": {
                    "url": oss_url
                }
            }), 200
            
        except Exception as oss_error:
            logger.error(f"上传图片到OSS失败: {str(oss_error)}")
            
            # 如果OSS上传失败，返回一个处理过的本地URL
            server_name = request.host
            protocol = 'https' if request.is_secure else 'http'
            local_url = f"{protocol}://{server_name}/uploads/{unique_filename}"
            
            logger.info(f"OSS上传失败，使用本地URL: {local_url}")
            return jsonify({
                "success": True,
                "file": {
                    "url": local_url
                }
            }), 200
    except Exception as e:
        logger.error(f"上传图片处理异常: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"服务异常: {str(e)}"
        }), 500

# 定义两个路由，都指向同一个处理函数
@aliyun_upload_bp.route('/', methods=['POST'])
def upload_image_root():
    """
    处理 /api/images/ 路径上传的请求
    """
    return handle_image_upload()

@aliyun_upload_bp.route('/upload', methods=['POST'])
def upload_image_to_aliyun():
    """
    处理 /api/images/upload 路径上传的请求
    """
    return handle_image_upload() 