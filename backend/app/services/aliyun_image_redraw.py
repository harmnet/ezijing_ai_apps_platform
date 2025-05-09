#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台阿里云图片重绘服务接口
实现了对阿里云百炼DashScope API的调用，提供图片局部重绘功能

主要功能：
- 支持对图像指定区域的元素进行增加、修改或删除操作
- 适用场景包括换装、替换局部物件、删除干扰物等
- 异步处理图片重绘任务
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
from app.utils.logger import get_image_redraw_logger

# 获取图像重绘专用日志记录器
image_redraw_logger = get_image_redraw_logger()

# 阿里云API配置
DASHSCOPE_API_CONFIG = {
    "api_key": os.environ.get("DASHSCOPE_API_KEY", "sk-1f4bdb8a73ee47809ee148a977c39737"),
    "base_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis",
    "task_url": "https://dashscope.aliyuncs.com/api/v1/tasks/",
    "model": "wanx2.1-imageedit"
}

def create_redraw_task(prompt, base_image_url, mask_image_url, n=1, seed=None, watermark=False):
    """
    创建图片局部重绘任务
    
    参数:
        prompt (str): 描述提示词，用于指导重绘内容
                      - 增加/修改操作：可描述具体动作("给小狗添加一顶帽子")
                                   或客观描述期望内容("一只戴着帽子的小狗")
                      - 删除操作：占据空间较少时可留空；
                               占据空间较大时需详细描述擦除后的内容
        base_image_url (str): 原始图片URL
        mask_image_url (str): 蒙版图片URL，指定需要重绘的区域
        n (int): 生成图片数量，默认为1
        seed (int, optional): 随机数种子
        watermark (bool): 是否添加水印
        
    返回:
        dict: API响应结果，包含任务ID
    """
    try:
        # 检查API密钥是否设置
        api_key = DASHSCOPE_API_CONFIG["api_key"]
        if not api_key or api_key == "sk-0bd59db1b4454d14b499421707900051":
            image_redraw_logger.warning("使用默认API密钥，建议配置自己的DASHSCOPE_API_KEY环境变量")
            
        # 记录请求参数
        image_redraw_logger.info(f"图片重绘请求参数: prompt='{prompt}', n={n}, seed={seed}, watermark={watermark}")
        image_redraw_logger.info(f"基础图片URL: {base_image_url[:50]}{'...' if len(base_image_url) > 50 else ''}")
        image_redraw_logger.info(f"蒙版图片URL: {mask_image_url[:50]}{'...' if len(mask_image_url) > 50 else ''}")
        
        # 处理基础图片
        base_image_parsed = urlparse(base_image_url) if base_image_url.startswith('http') else None
        base_is_local = base_image_parsed and (base_image_parsed.netloc in ['localhost', '127.0.0.1'] or 
                                   base_image_parsed.netloc.startswith('localhost:') or 
                                   base_image_parsed.netloc.startswith('127.0.0.1:'))
        
        # 处理蒙版图片
        mask_image_parsed = urlparse(mask_image_url) if mask_image_url.startswith('http') else None
        mask_is_local = mask_image_parsed and (mask_image_parsed.netloc in ['localhost', '127.0.0.1'] or 
                                   mask_image_parsed.netloc.startswith('localhost:') or 
                                   mask_image_parsed.netloc.startswith('127.0.0.1:'))
        
        # 判断是否需要上传到OSS
        base_need_upload = base_is_local or not base_image_url.startswith('http') or base_image_url.startswith('blob:') or 'mock-' in base_image_url
        mask_need_upload = mask_is_local or not mask_image_url.startswith('http') or mask_image_url.startswith('blob:') or 'mock-' in mask_image_url

        # 开发模式状态
        dev_mode = os.environ.get('DEV_MODE', 'true').lower() == 'true'
        image_redraw_logger.info(f"开发模式: {'启用' if dev_mode else '禁用'}")
        
        image_data = {}
        
        # 处理基础图片上传
        if base_need_upload:
            try:
                image_redraw_logger.info(f"开始上传基础图片到阿里云OSS: {'本地URL' if base_is_local else 'Base64数据'}")
                base_oss_url = upload_image(base_image_url)
                image_redraw_logger.info(f"基础图片已上传到OSS，公网URL: {base_oss_url}")
                image_data["base_image_url"] = base_oss_url
            except Exception as e:
                image_redraw_logger.error(f"上传基础图片到OSS失败: {str(e)}")
                return {
                    "success": False,
                    "error": {
                        "message": f"上传基础图片到OSS失败: {str(e)}",
                        "code": 400
                    }
                }
        else:
            image_redraw_logger.info(f"使用公网基础图片URL: {base_image_url}")
            image_data["base_image_url"] = base_image_url
        
        # 处理蒙版图片上传
        if mask_need_upload:
            try:
                image_redraw_logger.info(f"开始上传蒙版图片到阿里云OSS: {'本地URL' if mask_is_local else 'Base64数据'}")
                mask_oss_url = upload_image(mask_image_url)
                image_redraw_logger.info(f"蒙版图片已上传到OSS，公网URL: {mask_oss_url}")
                image_data["mask_image_url"] = mask_oss_url
            except Exception as e:
                image_redraw_logger.error(f"上传蒙版图片到OSS失败: {str(e)}")
                return {
                    "success": False,
                    "error": {
                        "message": f"上传蒙版图片到OSS失败: {str(e)}",
                        "code": 400
                    }
                }
        else:
            image_redraw_logger.info(f"使用公网蒙版图片URL: {mask_image_url}")
            image_data["mask_image_url"] = mask_image_url
            
        # 构建请求体
        request_body = {
            "model": DASHSCOPE_API_CONFIG["model"],
            "input": {
                "function": "description_edit_with_mask",
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
        image_redraw_logger.info(f"发送请求到阿里云图片重绘API，提示词: {prompt}, 请求体: {json.dumps(request_body, ensure_ascii=False)}")
        
        response = requests.post(
            DASHSCOPE_API_CONFIG["base_url"],
            headers=headers,
            json=request_body,
            timeout=60
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            image_redraw_logger.info(f"阿里云图片重绘任务创建成功 - 任务ID: {result.get('output', {}).get('task_id')}, 完整响应: {json.dumps(result, ensure_ascii=False)}")
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
                
            image_redraw_logger.error(f"阿里云图片重绘API调用失败 - 状态码: {response.status_code}, 响应: {error_content}")
            
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
        image_redraw_logger.error(f"创建阿里云图片重绘任务异常: {str(e)}\n{error_trace}")
        return {
            "success": False,
            "error": {
                "message": f"服务器错误: {str(e)}",
                "code": 500
            }
        }

def query_redraw_task(task_id):
    """
    查询图片重绘任务状态
    
    参数:
        task_id (str): 任务ID
        
    返回:
        dict: 任务状态信息
    """
    try:
        api_key = DASHSCOPE_API_CONFIG["api_key"]
        if not api_key or api_key == "sk-0bd59db1b4454d14b499421707900051":
            image_redraw_logger.warning("使用默认API密钥，建议配置自己的DASHSCOPE_API_KEY环境变量")
            
        # 构建请求URL
        request_url = f"{DASHSCOPE_API_CONFIG['task_url']}{task_id}"
        
        # 构建请求头
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 记录查询信息
        image_redraw_logger.info(f"查询阿里云图片重绘任务，任务ID: {task_id}")
        
        # 发送查询请求
        response = requests.get(
            request_url,
            headers=headers,
            timeout=30
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            task_status = result.get("output", {}).get("task_status")
            
            # 记录任务状态
            image_redraw_logger.info(f"阿里云图片重绘任务状态 - 任务ID: {task_id}, 状态: {task_status}")
            
            # 检查任务状态
            if task_status == "SUCCEEDED":
                results = result.get("output", {}).get("results", [])
                # 正确提取URL字段
                image_urls = [item.get("url") for item in results if "url" in item]
                image_redraw_logger.info(f"任务完成 - 生成图片数量: {len(image_urls)}")
                
                # 提取任务时间信息
                submit_time = result.get("output", {}).get("submit_time", "")
                end_time = result.get("output", {}).get("end_time", "")
                
                return {
                    "success": True,
                    "data": {
                        "task_id": task_id,
                        "task_status": task_status,
                        "request_id": result.get("request_id"),
                        "image_urls": image_urls,
                        "submit_time": submit_time,
                        "end_time": end_time
                    }
                }
            elif task_status == "FAILED":
                # 任务失败，返回错误信息
                error_code = result.get("code", -1)
                error_message = result.get("message", "任务执行失败")
                
                image_redraw_logger.error(f"任务失败 - 任务ID: {task_id}, 错误码: {error_code}, 错误信息: {error_message}")
                
                return {
                    "success": False,
                    "error": {
                        "message": error_message,
                        "code": error_code
                    }
                }
            else:
                # 任务进行中，返回状态信息
                return {
                    "success": True,
                    "data": {
                        "task_id": task_id,
                        "task_status": task_status,
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
                
            image_redraw_logger.error(f"查询阿里云图片重绘任务失败 - 状态码: {response.status_code}, 响应: {error_content}")
            
            return {
                "success": False,
                "error": {
                    "message": f"查询任务失败: 状态码 {response.status_code}, 响应: {error_content}",
                    "code": response.status_code
                }
            }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        image_redraw_logger.error(f"查询阿里云图片重绘任务异常: {str(e)}\n{error_trace}")
        
        return {
            "success": False,
            "error": {
                "message": f"服务器错误: {str(e)}",
                "code": 500
            }
        } 