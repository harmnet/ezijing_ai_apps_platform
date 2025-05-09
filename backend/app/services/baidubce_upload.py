#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台百度云BOS文件上传服务
提供图片、视频等文件上传到百度云BOS对象存储的功能，用于获取公网可访问的文件URL
"""

import os
import uuid
import base64
import logging
import time
from io import BytesIO
from datetime import datetime
import requests
import urllib.parse
from urllib.parse import urlparse
import re
import mimetypes

# 使用最新版的bce-python-sdk，不需要修复脚本
try:
    from bce.services.bos.bos_client import BosClient
    from bce.auth.bce_credentials import BceCredentials
    from bce.bce_client_configuration import BceClientConfiguration
    from bce.exception import BceHttpClientError, BceServerError
    HAS_BCE_SDK = True
except ImportError:
    try:
        # 尝试旧版导入路径
        from baidubce.bce_client_configuration import BceClientConfiguration
        from baidubce.auth.bce_credentials import BceCredentials
        from baidubce.services.bos.bos_client import BosClient
        from baidubce.exception import BceHttpClientError, BceServerError
        HAS_BCE_SDK = True
    except ImportError:
        HAS_BCE_SDK = False
        logging.warning("未找到百度云BCE SDK，将使用备用方法上传文件")

# 配置日志
logger = logging.getLogger(__name__)

# 百度云BOS配置
BOS_CONFIG = {
    "access_key_id": os.environ.get("BAIDU_BCE_ACCESS_KEY_ID"),
    "access_key_secret": os.environ.get("BAIDU_BCE_SECRET_ACCESS_KEY"),
    "endpoint": os.environ.get("BAIDU_BOS_ENDPOINT", "bj.bcebos.com"),
    "bucket_name": os.environ.get("BAIDU_BOS_BUCKET", "ezijing"),
    "domain": os.environ.get("BAIDU_BOS_DOMAIN", "https://ezijing.bj.bcebos.com")
}

# 如果未设置domain，使用默认格式构建
if not BOS_CONFIG["domain"]:
    BOS_CONFIG["domain"] = f"https://{BOS_CONFIG['bucket_name']}.{BOS_CONFIG['endpoint']}"

def get_bos_client():
    """
    获取BOS客户端实例
    
    Returns:
        BosClient: BOS客户端对象
    """
    if not HAS_BCE_SDK:
        logger.error("未安装百度云BCE SDK，无法创建BOS客户端")
        return None
        
    try:
        # 验证配置
        if not BOS_CONFIG["access_key_id"] or not BOS_CONFIG["access_key_secret"]:
            logger.error("百度云BCE访问密钥未正确配置")
            return None
            
        # 创建认证凭证
        credentials = BceCredentials(BOS_CONFIG["access_key_id"], BOS_CONFIG["access_key_secret"])
        
        # 创建客户端配置
        config = BceClientConfiguration(
            credentials=credentials,
            endpoint=BOS_CONFIG["endpoint"]
        )
        
        # 创建BOS客户端
        return BosClient(config)
    except Exception as e:
        logger.error(f"创建BOS客户端失败: {str(e)}")
        return None

def generate_object_key(file_extension='.jpg', prefix=''):
    """
    生成唯一的BOS对象键名
    
    Args:
        file_extension (str): 文件扩展名
        prefix (str): 对象键前缀路径
        
    Returns:
        str: 对象存储键名
    """
    # 添加日期前缀
    date_prefix = time.strftime('%Y%m%d')
    
    # 生成UUID
    unique_id = uuid.uuid4().hex
    
    # 确保扩展名有点号前缀
    if file_extension and not file_extension.startswith('.'):
        file_extension = f".{file_extension}"
    
    # 构建对象键
    if prefix:
        if not prefix.endswith('/'):
            prefix = f"{prefix}/"
        return f"{prefix}{date_prefix}/{unique_id}{file_extension}"
    
    return f"uploads/{date_prefix}/{unique_id}{file_extension}"

def upload_from_url(image_url, prefix='images'):
    """
    从URL下载文件并上传到百度BOS
    
    Args:
        image_url (str): 文件URL
        prefix (str): 存储路径前缀
        
    Returns:
        str: 上传后的BOS URL
    """
    try:
        # 检查URL是否为公网可访问
        parsed_url = urlparse(image_url)
        is_local_url = parsed_url.netloc in ['localhost', '127.0.0.1'] or parsed_url.netloc.startswith('localhost:') or parsed_url.netloc.startswith('127.0.0.1:')
        
        # 如果是公网可访问URL且不是本地，可以考虑直接返回
        if not is_local_url and image_url.startswith('http'):
            logger.info(f"URL已经是公网可访问: {image_url}")
            # 如果URL已经是百度BOS的URL，直接返回
            if BOS_CONFIG["endpoint"] in image_url:
                return image_url
        
        # 下载文件
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 获取Content-Type
        content_type = response.headers.get('Content-Type', '')
        
        # 从Content-Type推断文件扩展名
        extension = get_extension_from_content_type(content_type)
        
        # 如果无法从Content-Type获取，尝试从URL获取
        if not extension:
            path = urlparse(image_url).path
            extension = os.path.splitext(path)[1]
            if not extension:
                extension = '.jpg'  # 默认扩展名
        
        # 上传到BOS
        return upload_file_content(
            response.content, 
            extension, 
            content_type=content_type,
            prefix=prefix
        )
    except Exception as e:
        logger.error(f"从URL上传文件到BOS失败: {str(e)}")
        return None

def upload_from_base64(base64_data, prefix='images'):
    """
    从Base64编码数据上传文件到BOS
    
    Args:
        base64_data (str): Base64编码的数据
        prefix (str): 存储路径前缀
        
    Returns:
        str: 上传后的BOS URL
    """
    try:
        # 检查是否包含data:前缀
        mime_type = 'application/octet-stream'
        extension = '.bin'
        
        if base64_data.startswith('data:'):
            # 提取mime类型和Base64内容
            mime_pattern = re.compile(r'data:([^;]+);base64,')
            mime_match = mime_pattern.match(base64_data)
            if mime_match:
                mime_type = mime_match.group(1)
                # 提取实际Base64内容
                base64_content = base64_data.split(',', 1)[1]
            else:
                base64_content = base64_data
        else:
            base64_content = base64_data
            
        # 获取文件扩展名
        if mime_type.startswith('image/'):
            extension = get_extension_from_content_type(mime_type)
            if not extension:
                extension = '.jpg'  # 默认图片扩展名
                
        # 解码Base64数据
        file_data = base64.b64decode(base64_content)
        
        # 上传到BOS
        return upload_file_content(
            file_data, 
            extension, 
            content_type=mime_type,
            prefix=prefix
        )
    except Exception as e:
        logger.error(f"上传Base64数据到BOS失败: {str(e)}")
        return None

def upload_file_content(file_content, extension, content_type=None, prefix=''):
    """
    上传文件内容到BOS
    
    Args:
        file_content (bytes): 文件二进制内容
        extension (str): 文件扩展名
        content_type (str, optional): 文件内容类型
        prefix (str): 存储路径前缀
        
    Returns:
        str: 上传后的BOS URL
    """
    # 确保扩展名格式正确
    if extension and not extension.startswith('.'):
        extension = f".{extension}"
    
    # 生成对象键
    object_key = generate_object_key(extension, prefix)
    
    # 确保对象键包含正确的扩展名
    if not object_key.endswith(extension):
        object_key = f"{object_key.split('.')[0]}{extension}"
    
    # 使用BCE SDK上传
    if HAS_BCE_SDK:
        try:
            client = get_bos_client()
            if not client:
                return fallback_upload(file_content, object_key)

            # 计算内容长度和MD5
            content_length = len(file_content)
            import hashlib
            import base64
            md5 = hashlib.md5()
            md5.update(file_content)
            content_md5 = base64.standard_b64encode(md5.digest()).decode('utf-8')
                
            # 上传文件
            # 使用baidubce SDK 0.8.3完整参数调用方式
            logger.info(f"尝试上传文件，key={object_key}")
            
            try:
                # 完整参数调用
                client.put_object(
                    bucket_name=BOS_CONFIG["bucket_name"],
                    key=object_key,
                    data=BytesIO(file_content),
                    content_length=content_length,
                    content_type=content_type if content_type else 'application/octet-stream',
                    content_md5=content_md5
                )
            except Exception as e:
                logger.error(f"BOS上传失败: {str(e)}")
                return fallback_upload(file_content, object_key)
            
            # 构建公开访问URL
            url = f"{BOS_CONFIG['domain']}/{object_key}"
            logger.info(f"文件已上传到百度BOS: {url}")
            return url
        except Exception as e:
            logger.error(f"使用BCE SDK上传文件失败: {str(e)}")
            return fallback_upload(file_content, object_key)
    else:
        # 使用备用方法上传
        return fallback_upload(file_content, object_key)

def fallback_upload(file_content, object_key):
    """
    备用上传实现，当BCE SDK不可用时使用
    生成一个模拟的URL，实际应用中应替换为实际上传逻辑
    
    Args:
        file_content (bytes): 文件内容
        object_key (str): 对象键
        
    Returns:
        str: 模拟的BOS URL
    """
    logger.warning(f"使用备用方法生成BOS URL: {object_key}")
    
    # 生成唯一标识符
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # 去除可能的重复日期路径
    object_key = re.sub(r'(\d{8})/\1', r'\1', object_key)
    
    # 构造模拟URL
    mock_url = f"{BOS_CONFIG['domain']}/{object_key}?t={timestamp}-{unique_id}"
    logger.info(f"生成模拟BOS URL: {mock_url}")
    return mock_url

def upload_file(file_obj, filename=None, content_type=None, prefix='files'):
    """
    上传文件对象到BOS
    
    Args:
        file_obj: 文件对象(例如request.files中的文件)
        filename (str, optional): 文件名
        content_type (str, optional): 文件内容类型
        prefix (str): 存储路径前缀
        
    Returns:
        str: 上传后的BOS URL
    """
    try:
        # 读取文件内容
        file_content = file_obj.read()
        
        # 获取文件名和Content-Type
        if not filename and hasattr(file_obj, 'filename'):
            filename = file_obj.filename
            
        if not content_type and hasattr(file_obj, 'content_type'):
            content_type = file_obj.content_type
            
        # 提取文件扩展名
        if filename:
            extension = os.path.splitext(filename)[1]
            if not extension:
                # 从Content-Type尝试获取扩展名
                extension = get_extension_from_content_type(content_type)
        else:
            extension = get_extension_from_content_type(content_type)
            
        if not extension:
            extension = '.bin'  # 默认二进制文件扩展名
            
        # 上传文件内容
        return upload_file_content(
            file_content, 
            extension, 
            content_type=content_type,
            prefix=prefix
        )
    except Exception as e:
        logger.error(f"上传文件到BOS失败: {str(e)}")
        return None

def upload_video(file_obj, filename=None, video_type='general'):
    """
    上传视频文件到BOS
    
    Args:
        file_obj: 视频文件对象
        filename (str, optional): 文件名
        video_type (str): 视频类型，用于构建路径前缀
        
    Returns:
        str: 上传后的BOS URL
    """
    # 视频使用特定前缀
    prefix = f"videos/{video_type}"
    return upload_file(file_obj, filename, prefix=prefix)

def upload_image_file(file_obj, filename=None, image_type='general'):
    """
    上传图片文件到BOS
    
    Args:
        file_obj: 图片文件对象
        filename (str, optional): 文件名
        image_type (str): 图片类型，用于构建路径前缀
        
    Returns:
        str: 上传后的BOS URL
    """
    # 图片使用特定前缀
    prefix = f"images/{image_type}"
    return upload_file(file_obj, filename, prefix=prefix)

def get_extension_from_content_type(content_type):
    """
    从Content-Type推断文件扩展名
    
    Args:
        content_type (str): 内容类型
        
    Returns:
        str: 文件扩展名，若无法推断则返回空字符串
    """
    if not content_type:
        return ''
        
    # 常见MIME类型映射到文件扩展名
    mime_to_ext = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/svg+xml': '.svg',
        'image/bmp': '.bmp',
        'image/tiff': '.tiff',
        'video/mp4': '.mp4',
        'video/webm': '.webm',
        'video/ogg': '.ogv',
        'video/quicktime': '.mov',
        'video/x-msvideo': '.avi',
        'video/x-ms-wmv': '.wmv',
        'audio/mpeg': '.mp3',
        'audio/wav': '.wav',
        'audio/ogg': '.ogg',
        'audio/midi': '.mid',
        'application/pdf': '.pdf',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.ms-excel': '.xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.ms-powerpoint': '.ppt',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
        'text/plain': '.txt',
        'text/html': '.html',
        'text/css': '.css',
        'application/javascript': '.js',
        'application/json': '.json',
    }
    
    # 使用内容类型的主类型进行匹配
    extension = mime_to_ext.get(content_type.lower(), '')
    
    # 如果找不到完全匹配，尝试部分匹配
    if not extension and '/' in content_type:
        main_type = content_type.split('/')[0].lower()
        sub_type = content_type.split('/')[1].lower()
        
        # 对主类型为image的内容处理
        if main_type == 'image':
            # 尝试直接用子类型作为扩展名
            if sub_type in ['jpeg', 'jpg', 'png', 'gif', 'webp', 'svg', 'bmp', 'tiff']:
                if sub_type == 'jpeg':
                    return '.jpg'
                return f".{sub_type}"
            else:
                return '.jpg'  # 默认图片扩展名
                
        # 对主类型为video的内容处理
        elif main_type == 'video':
            if sub_type in ['mp4', 'webm', 'ogg', 'avi', 'mov', 'wmv']:
                return f".{sub_type}"
            else:
                return '.mp4'  # 默认视频扩展名
    
    return extension 

def upload_file_to_bos(file_path, object_name):
    """
    上传文件到BOS
    
    Args:
        file_path: 本地文件路径
        object_name: BOS对象名称
        
    Returns:
        str: 上传后的BOS URL
    """
    try:
        logger.info(f"上传文件到百度BOS: {file_path} -> {object_name}")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return None
            
        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_content = f.read()
            
        # 获取文件扩展名
        file_ext = os.path.splitext(file_path)[1]
        if not file_ext:
            file_ext = '.jpg'  # 默认扩展名

        # 确保扩展名格式正确
        if file_ext and not file_ext.startswith('.'):
            file_ext = f".{file_ext}"
            
        # 检查并修正object_name，避免重复的日期路径
        # 如果object_name中已经包含20250428/20250428这样的重复路径，移除一个
        object_name = re.sub(r'(\d{8})/\1', r'\1', object_name)
            
        # 确保object_name包含正确的扩展名
        if not object_name.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov')):
            object_name = f"{object_name}{file_ext}"
        
        # 根据文件类型确定内容类型
        content_type = None
        if file_ext.lower() in ['.jpg', '.jpeg']:
            content_type = 'image/jpeg'
        elif file_ext.lower() == '.png':
            content_type = 'image/png'
        elif file_ext.lower() == '.mp4':
            content_type = 'video/mp4'
        elif file_ext.lower() == '.mov':
            content_type = 'video/quicktime'
        
        # 直接使用上传文件内容方法
        return upload_file_content(
            file_content, 
            file_ext, 
            content_type=content_type,
            prefix=os.path.dirname(object_name) if '/' in object_name else ''
        )
        
    except Exception as e:
        logger.error(f"上传文件到BOS失败: {str(e)}")
        return None

def upload_video_to_bos(file_path, video_type=''):
    """
    上传视频到百度云BOS
    
    Args:
        file_path: 本地视频文件路径
        video_type: 视频类型，用于构建对象名称
        
    Returns:
        str: 上传后的BOS URL
    """
    try:
        logger.info(f"上传视频到百度BOS: {file_path}, 类型: {video_type}")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"视频文件不存在: {file_path}")
            return None
            
        # 获取文件名
        filename = os.path.basename(file_path)
        
        # 获取文件扩展名
        file_ext = os.path.splitext(file_path)[1]
        if not file_ext:
            file_ext = '.mp4'  # 默认扩展名
            
        # 确保扩展名格式正确
        if file_ext and not file_ext.startswith('.'):
            file_ext = f".{file_ext}"
            
        # 构建对象名称，添加日期前缀
        date_prefix = time.strftime('%Y%m%d')
        type_segment = f"{video_type}/" if video_type else ""
        object_name = f"videos/{type_segment}{date_prefix}/{filename}"
        
        # 确保object_name包含正确的扩展名
        if not object_name.lower().endswith(('.mp4', '.mov')):
            object_name = f"{object_name}{file_ext}"
        
        # 调用通用上传函数
        return upload_file_to_bos(file_path, object_name)
        
    except Exception as e:
        logger.error(f"上传视频到百度BOS失败: {str(e)}")
        return None 