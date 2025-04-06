#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台阿里云图片风格调整服务接口
实现了对阿里云百炼DashScope API的调用，提供图片风格化调整功能

主要功能：
- 支持根据提示词进行全局风格化调整
- 异步处理图片风格调整任务
- 查询任务进度和结果
"""

import os
import json
import requests
import base64
from flask import current_app
import re
from urllib.parse import urlparse
from app.services.aliyun_oss_service import upload_image

# 阿里云API配置
DASHSCOPE_API_CONFIG = {
    "api_key": os.environ.get("DASHSCOPE_API_KEY", "sk-0bd59db1b4454d14b499421707900051"),
    "base_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis",
    "task_url": "https://dashscope.aliyuncs.com/api/v1/tasks/",
    "model": "wanx2.1-imageedit"
}

def download_image_to_base64(image_url):
    """
    下载图片并转换为Base64编码
    
    参数:
        image_url (str): 图片URL
        
    返回:
        str: Base64编码的图片
    """
    try:
        # 检查是否为本地URL（http://localhost 或 http://127.0.0.1）
        parsed_url = urlparse(image_url)
        is_local_url = parsed_url.netloc in ['localhost', '127.0.0.1'] or parsed_url.netloc.startswith('localhost:') or parsed_url.netloc.startswith('127.0.0.1:')
        
        if is_local_url:
            # 记录日志
            current_app.logger.info(f"检测到本地URL: {image_url}，尝试下载")
            
        # 下载图片
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 转换为Base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        
        # 记录成功
        current_app.logger.info(f"图片下载成功并转换为Base64格式，大小: {len(image_base64)} 字符")
        
        return image_base64
    except Exception as e:
        current_app.logger.error(f"下载图片失败: {str(e)}")
        raise

def create_style_task(prompt, image_url, n=1, seed=None, watermark=False):
    """
    创建图片风格调整任务
    
    参数:
        prompt (str): 风格描述提示词
        image_url (str): 原始图片URL或Base64编码
        n (int): 生成图片数量，1-4
        seed (int, optional): 随机数种子
        watermark (bool): 是否添加水印
        
    返回:
        dict: API响应结果，包含任务ID
    """
    try:
        parsed_url = urlparse(image_url) if image_url.startswith('http') else None
        is_local_url = parsed_url and (parsed_url.netloc in ['localhost', '127.0.0.1'] or 
                                    parsed_url.netloc.startswith('localhost:') or 
                                    parsed_url.netloc.startswith('127.0.0.1:'))
        
        # 判断是否需要上传到OSS
        need_upload = is_local_url or not image_url.startswith('http')
        
        if need_upload:
            # 上传到OSS获取公网URL
            try:
                current_app.logger.info(f"开始上传图片到阿里云OSS: {'本地URL' if is_local_url else 'Base64数据'}")
                oss_url = upload_image(image_url)
                current_app.logger.info(f"图片已上传到OSS，公网URL: {oss_url}")
                
                # 使用OSS URL
                image_data = {
                    "base_image_url": oss_url
                }
            except Exception as e:
                current_app.logger.error(f"上传图片到OSS失败: {str(e)}")
                return {
                    "success": False,
                    "error": {
                        "message": f"上传图片到OSS失败: {str(e)}",
                        "code": 400
                    }
                }
        else:
            # 公网URL直接使用
            current_app.logger.info(f"使用公网图片URL: {image_url}")
            image_data = {
                "base_image_url": image_url
            }
            
        # 构建请求体
        request_body = {
            "model": DASHSCOPE_API_CONFIG["model"],
            "input": {
                "function": "stylization_all",
                "prompt": prompt,
                **image_data
            },
            "parameters": {
                "n": n
            }
        }
        
        # 添加可选参数
        if seed is not None:
            request_body["parameters"]["seed"] = seed
            
        if watermark is not None:
            request_body["parameters"]["watermark"] = watermark
            
        # 发送API请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DASHSCOPE_API_CONFIG['api_key']}",
            "X-DashScope-Async": "enable"
        }
        
        # 记录请求信息
        current_app.logger.info(f"发送请求到阿里云图片风格调整API，提示词: {prompt}, 请求体: {json.dumps(request_body, ensure_ascii=False)}")
        
        response = requests.post(
            DASHSCOPE_API_CONFIG["base_url"],
            headers=headers,
            json=request_body,
            timeout=60
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            current_app.logger.info(f"阿里云图片风格调整任务创建成功 - 任务ID: {result.get('output', {}).get('task_id')}, 完整响应: {json.dumps(result, ensure_ascii=False)}")
            return {
                "success": True,
                "data": {
                    "task_id": result.get("output", {}).get("task_id"),
                    "task_status": result.get("output", {}).get("task_status"),
                    "request_id": result.get("request_id")
                }
            }
        else:
            # 详细记录错误响应
            error_content = response.text
            try:
                error_json = response.json()
                error_content = json.dumps(error_json, ensure_ascii=False)
            except:
                pass
                
            current_app.logger.error(f"阿里云图片风格调整API调用失败 - 状态码: {response.status_code}, 响应: {error_content}")
            
            return {
                "success": False,
                "error": {
                    "message": f"API调用失败: 状态码 {response.status_code}, 响应: {error_content}",
                    "code": response.status_code
                }
            }
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        current_app.logger.error(f"创建阿里云图片风格调整任务异常: {str(e)}\n{error_trace}")
        return {
            "success": False,
            "error": {
                "message": f"服务器错误: {str(e)}",
                "code": 500
            }
        }

def query_style_task(task_id):
    """
    查询图片风格调整任务状态和结果
    
    参数:
        task_id (str): 任务ID
        
    返回:
        dict: 任务状态和结果
    """
    try:
        # 发送API请求
        headers = {
            "Authorization": f"Bearer {DASHSCOPE_API_CONFIG['api_key']}"
        }
        
        # 记录发送请求信息
        current_app.logger.info(f"正在请求阿里云API查询任务: {task_id}")
        
        response = requests.get(
            f"{DASHSCOPE_API_CONFIG['task_url']}{task_id}",
            headers=headers,
            timeout=60
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            # 记录完整响应以便调试
            current_app.logger.info(f"阿里云API响应: {json.dumps(result, ensure_ascii=False)}")
            
            task_status = result.get("output", {}).get("task_status")
            
            # 记录任务状态
            current_app.logger.info(f"阿里云图片风格调整任务查询 - 任务ID: {task_id}, 状态: {task_status}")
            
            # 构建返回结果
            response_data = {
                "task_id": task_id,
                "task_status": task_status,
                "request_id": result.get("request_id")
            }
            
            # 查看是否有错误信息
            error_message = result.get("output", {}).get("error", {}).get("message", "")
            error_code = result.get("output", {}).get("error", {}).get("code", "")
            if error_message or error_code:
                current_app.logger.error(f"任务失败 - 错误信息: {error_message}, 错误码: {error_code}")
                response_data["error"] = {
                    "message": error_message,
                    "code": error_code
                }
            
            # 如果任务完成，添加结果URL
            if task_status == "SUCCEEDED":
                results = result.get("output", {}).get("results", [])
                image_urls = [item.get("url") for item in results if "url" in item]
                response_data["image_urls"] = image_urls
                response_data["submit_time"] = result.get("output", {}).get("submit_time")
                response_data["end_time"] = result.get("output", {}).get("end_time")
            
            return {
                "success": True,
                "data": response_data
            }
        else:
            # 记录详细的错误响应
            error_content = response.text
            try:
                error_json = response.json()
                error_content = json.dumps(error_json, ensure_ascii=False)
            except:
                pass
                
            current_app.logger.error(f"阿里云图片风格调整任务查询失败 - 状态码: {response.status_code}, 响应: {error_content}")
            
            return {
                "success": False,
                "error": {
                    "message": f"任务查询失败: 状态码 {response.status_code}, 响应: {error_content}",
                    "code": response.status_code
                }
            }
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        current_app.logger.error(f"查询阿里云图片风格调整任务异常: {str(e)}\n{error_trace}")
        return {
            "success": False,
            "error": {
                "message": f"服务器错误: {str(e)}",
                "code": 500
            }
        } 