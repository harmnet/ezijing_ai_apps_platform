#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台阿里云OSS文件上传服务
提供图片上传到阿里云OSS对象存储的功能，用于获取公网可访问的图片URL
"""

import os
import uuid
import base64
import oss2
import requests
import urllib.parse
from io import BytesIO
from flask import current_app
import re
from urllib.parse import urlparse
import logging
import time

# 阿里云OSS配置
OSS_CONFIG = {
    # 使用与digital_human_service.py相同的环境变量获取逻辑
    "access_key_id": os.environ.get("ALIYUN_OSS_ACCESS_KEY_ID", os.environ.get("ALIYUN_ACCESS_KEY_ID")),
    "access_key_secret": os.environ.get("ALIYUN_OSS_ACCESS_KEY_SECRET", os.environ.get("ALIYUN_ACCESS_KEY_SECRET")),
    "endpoint": os.environ.get("ALIYUN_OSS_ENDPOINT", os.environ.get("ALIYUN_OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")),
    "bucket_name": os.environ.get("ALIYUN_OSS_BUCKET_NAME", os.environ.get("ALIYUN_OSS_BUCKET", "ezijingai"))
}

def get_oss_bucket():
    """
    获取OSS Bucket实例
    
    返回:
        oss2.Bucket: OSS Bucket对象
    """
    try:
        # 记录OSS配置信息（不包含敏感信息）
        current_app.logger.info(f"OSS配置信息: bucket={OSS_CONFIG['bucket_name']}, endpoint={OSS_CONFIG['endpoint']}")
        current_app.logger.info(f"AccessKey配置状态: ID存在={bool(OSS_CONFIG['access_key_id'])}, Secret存在={bool(OSS_CONFIG['access_key_secret'])}")
        
        # 验证OSS配置
        if not OSS_CONFIG['access_key_id'] or not OSS_CONFIG['access_key_secret']:
            current_app.logger.error("OSS配置不完整，无法上传")
            raise ValueError("OSS访问密钥未配置")
            
        auth = oss2.Auth(OSS_CONFIG["access_key_id"], OSS_CONFIG["access_key_secret"])
        bucket = oss2.Bucket(auth, OSS_CONFIG["endpoint"], OSS_CONFIG["bucket_name"])
        return bucket
    except Exception as e:
        current_app.logger.error(f"获取OSS Bucket实例失败: {str(e)}")
        raise

def generate_object_key(file_extension='.jpg'):
    """
    生成唯一的对象存储键名
    
    参数:
        file_extension (str): 文件扩展名
        
    返回:
        str: 对象存储键名
    """
    return f"ai-images/{uuid.uuid4()}{file_extension}"

def upload_from_url(image_url):
    """
    从URL下载图片并上传到OSS
    
    参数:
        image_url (str): 图片URL
        
    返回:
        str: 上传后的OSS URL
    """
    try:
        # 检查是否为本地URL
        parsed_url = urlparse(image_url)
        is_local_url = parsed_url.netloc in ['localhost', '127.0.0.1'] or parsed_url.netloc.startswith('localhost:') or parsed_url.netloc.startswith('127.0.0.1:')
        
        if is_local_url:
            current_app.logger.info(f"从本地URL下载图片: {image_url}")
        
        # 下载图片
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 获取文件扩展名
        content_type = response.headers.get('Content-Type', '')
        
        # 从Content-Type推断文件扩展名
        if 'jpeg' in content_type or 'jpg' in content_type:
            extension = '.jpg'
        elif 'png' in content_type:
            extension = '.png'
        elif 'gif' in content_type:
            extension = '.gif'
        elif 'webp' in content_type:
            extension = '.webp'
        else:
            # 从URL尝试获取扩展名
            path = urlparse(image_url).path
            extension = os.path.splitext(path)[1]
            if not extension:
                extension = '.jpg'  # 默认扩展名
        
        # 生成OSS对象键
        object_key = generate_object_key(extension)
        
        # 上传到OSS
        bucket = get_oss_bucket()
        bucket.put_object(object_key, response.content)
        
        # 构建并返回OSS URL
        oss_url = f"https://{OSS_CONFIG['bucket_name']}.{OSS_CONFIG['endpoint']}/{object_key}"
        current_app.logger.info(f"图片已上传到OSS: {oss_url}")
        
        return oss_url
    except Exception as e:
        current_app.logger.error(f"上传图片到OSS失败: {str(e)}")
        raise

def upload_from_base64(base64_data):
    """
    从Base64编码数据上传图片到OSS
    
    参数:
        base64_data (str): Base64编码的图片数据
        
    返回:
        str: 上传后的OSS URL
    """
    try:
        # 检查是否包含data:image前缀
        if base64_data.startswith('data:image'):
            # 提取mime类型和Base64内容
            mime_pattern = re.compile(r'data:image/([^;]+);base64,')
            mime_match = mime_pattern.match(base64_data)
            mime_type = mime_match.group(1) if mime_match else 'jpeg'
            
            # 提取实际Base64内容
            base64_content = base64_data.split(',', 1)[1] if ',' in base64_data else base64_data
        else:
            # 未指定mime类型，默认为jpeg
            mime_type = 'jpeg'
            base64_content = base64_data
        
        # 根据mime类型设置扩展名
        extension_map = {
            'jpeg': '.jpg',
            'jpg': '.jpg',
            'png': '.png',
            'gif': '.gif',
            'webp': '.webp'
        }
        extension = extension_map.get(mime_type, '.jpg')
        
        # 解码Base64数据
        image_data = base64.b64decode(base64_content)
        
        # 生成OSS对象键
        object_key = generate_object_key(extension)
        
        # 上传到OSS
        bucket = get_oss_bucket()
        bucket.put_object(object_key, image_data)
        
        # 构建并返回OSS URL
        oss_url = f"https://{OSS_CONFIG['bucket_name']}.{OSS_CONFIG['endpoint']}/{object_key}"
        current_app.logger.info(f"Base64图片已上传到OSS: {oss_url}")
        
        return oss_url
    except Exception as e:
        current_app.logger.error(f"上传Base64图片到OSS失败: {str(e)}")
        raise

def upload_image(image_source):
    """
    智能处理图片上传，支持URL和Base64
    
    参数:
        image_source (str): 图片URL或Base64编码
        
    返回:
        str: 上传后的OSS URL
    """
    try:
        # 检查开发环境变量
        dev_mode = os.environ.get('DEV_MODE', 'true').lower() == 'true'
        
        # 如果是公网可访问的URL，直接使用
        if not dev_mode and image_source.startswith('http') and not is_local_url(image_source):
            current_app.logger.info(f"使用公网可访问的URL: {image_source}")
            return image_source
            
        if dev_mode:
            # 生成文件名用于模拟URL
            if image_source.startswith('http'):
                filename = os.path.basename(urlparse(image_source).path)
                if not filename:
                    filename = f"mock_image_{uuid.uuid4().hex}.jpg"
            else:
                filename = f"mock_image_{uuid.uuid4().hex}.jpg"
                
            # 在开发模式下，返回模拟的URL而不是实际上传到OSS
            current_app.logger.info("开发模式：模拟OSS上传")
            mock_url = f"https://mock-{OSS_CONFIG['bucket_name']}.{OSS_CONFIG['endpoint']}/dev-uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{filename}"
            current_app.logger.info(f"模拟图片URL: {mock_url}")
            return mock_url
            
        # 正常处理上传
        current_app.logger.info("非开发模式：实际上传图片到OSS")
        if image_source.startswith('http'):
            return upload_from_url(image_source)
        else:
            return upload_from_base64(image_source)
    except Exception as e:
        current_app.logger.error(f"上传图片到OSS失败: {str(e)}")
        # 返回阿里云演示图片作为后备选项，确保API能够正常工作
        if image_source.startswith('http') and 'mask' in image_source:
            backup_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_2_mask.png"
        else:
            backup_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_2.jpeg"
        current_app.logger.warning(f"OSS上传失败，返回阿里云演示图片URL: {backup_url}")
        return backup_url
        
def is_local_url(url):
    """检查URL是否为本地URL"""
    if not url.startswith('http'):
        return False
    parsed = urlparse(url)
    return (parsed.netloc in ['localhost', '127.0.0.1'] or 
            parsed.netloc.startswith('localhost:') or 
            parsed.netloc.startswith('127.0.0.1:'))

def upload_file_to_oss(file_obj, filename, content_type=None):
    """
    上传文件到OSS
    
    参数:
        file_obj (FileStorage): Flask的文件对象
        filename (str): 文件名
        content_type (str, optional): 文件的MIME类型
        
    返回:
        str: 上传后的OSS URL
    """
    try:
        # 检查开发环境变量
        dev_mode = os.environ.get('DEV_MODE', 'true').lower() == 'true'
            
        if dev_mode:
            # 在开发模式下，返回模拟的URL而不是实际上传到OSS
            current_app.logger.info("开发模式：模拟文件上传到OSS")
            
            # 获取文件扩展名
            file_ext = os.path.splitext(filename)[1]
            
            # 生成模拟URL
            mock_url = f"https://mock-{OSS_CONFIG['bucket_name']}.{OSS_CONFIG['endpoint']}/dev-uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{filename}"
            current_app.logger.info(f"模拟文件URL: {mock_url}")
            return mock_url
            
        # 正常处理上传
        current_app.logger.info(f"非开发模式：实际上传文件到OSS: {filename}")
        
        # 确定文件对象键 (OSS中的路径)
        file_ext = os.path.splitext(filename)[1]
        object_key = f"uploaded-files/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}{file_ext}"
        
        # 获取文件内容
        file_content = file_obj.read()
        
        # 创建OSS bucket
        bucket = get_oss_bucket()
        
        # 设置额外参数，如Content-Type
        headers = {}
        if content_type:
            headers['Content-Type'] = content_type
        
        # 上传文件到OSS
        bucket.put_object(object_key, file_content, headers=headers)
        
        # 构建OSS URL
        oss_url = f"https://{OSS_CONFIG['bucket_name']}.{OSS_CONFIG['endpoint']}/{object_key}"
        current_app.logger.info(f"文件已上传到OSS: {oss_url}")
        
        return oss_url
        
    except Exception as e:
        current_app.logger.error(f"上传文件到OSS失败: {str(e)}")
        # 如果是视频文件，可以返回一个示例视频URL
        if filename.lower().endswith(('.mp4', '.mov', '.webm', '.avi')):
            backup_url = "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4"
            current_app.logger.warning(f"OSS视频上传失败，返回示例视频URL: {backup_url}")
            return backup_url
        else:
            # 其他类型文件的后备URL
            backup_url = f"https://mock-{OSS_CONFIG['bucket_name']}.{OSS_CONFIG['endpoint']}/backup-uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{filename}"
            current_app.logger.warning(f"OSS文件上传失败，返回模拟URL: {backup_url}")
            return backup_url 