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

# 阿里云OSS配置
OSS_CONFIG = {
    "access_key_id": os.environ.get("ALIYUN_OSS_ACCESS_KEY_ID", "LTAI5tMVdYzk5fVrmjQVk1Ga"),
    "access_key_secret": os.environ.get("ALIYUN_OSS_ACCESS_KEY_SECRET", "OKUYiiO9WOw5bJpRTfJa7F76Ayygdk"),
    "endpoint": os.environ.get("ALIYUN_OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com"),
    "bucket_name": os.environ.get("ALIYUN_OSS_BUCKET_NAME", "ezijingai")
}

def get_oss_bucket():
    """
    获取OSS Bucket实例
    
    返回:
        oss2.Bucket: OSS Bucket对象
    """
    auth = oss2.Auth(OSS_CONFIG["access_key_id"], OSS_CONFIG["access_key_secret"])
    bucket = oss2.Bucket(auth, OSS_CONFIG["endpoint"], OSS_CONFIG["bucket_name"])
    return bucket

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
    if image_source.startswith('http'):
        return upload_from_url(image_source)
    else:
        return upload_from_base64(image_source) 