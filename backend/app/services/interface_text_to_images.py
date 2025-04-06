#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台文生图服务接口
实现了对MiniMax Platform API的调用，提供文本生成图片的功能

主要功能：
- 支持多种图片尺寸和长宽比
- 支持多种艺术风格
- 支持批量生成多张图片
- 支持正向和反向提示词
"""

import os
import json
import requests
from flask import current_app

# MiniMax API配置
MINIMAX_API_CONFIG = {
    "base_url": "https://api.minimax.chat/v1/image_generation",
    "model": "image-01",
    "api_key": os.environ.get("MINIMAX_API_KEY", "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLog6Hohb7lrociLCJVc2VyTmFtZSI6IuiDoeiFvuWuhyIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxODU1OTUwMjUwNTM2MDc5NDU0IiwiUGhvbmUiOiIxMzY4MTU0NDMxOSIsIkdyb3VwSUQiOiIxODU1OTUwMjUwNTI3NjkwODQ2IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDMtMjYgMTk6MTc6NDIiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.pxrEAOhsUC1wQ34o7Zkxx3ridJgrfQz8rXjdaDrv5oEC_lCrPU0ivfhoaqOZjhRz9bZFC6jDwj3uOUpc6Efii4jSXPCWEMJvuocJY7PJ_eDTcmSb8eapaAYuDzRgNqd811P_QZRiro_TtjOOUKpDs4c5eCT87fn3oo-a-gjrW4KhlP37M3vm_SLUCRhBGaeIZYLQLg9VqLs4lF9som-bykPD6nLkWvGMygUZtDGK3u-j1Jj9m9iS7732iywAJqkFwWj_x-nmn523tfT9QU2LCqMjcvLVnLJINus83ojh_oYVldJOMW5dcztrQAkZrTglTPiaz236IDduEBO4vtyKPA")
}

def get_aspect_ratio(width, height):
    """根据宽高计算长宽比"""
    if width == height:
        return "1:1"
    elif width == 1024 and height == 768:
        return "4:3"
    elif width == 768 and height == 1024:
        return "3:4"
    elif width == 1024 and height == 576:
        return "16:9"
    elif width == 576 and height == 1024:
        return "9:16"
    return "1:1"  # 默认返回1:1

def enhance_prompt_by_style(prompt, style):
    """根据风格增强提示词"""
    style_enhancements = {
        "cartoon": "cartoon style, vibrant colors, simplified shapes",
        "painting": "oil painting style, artistic, detailed brushstrokes",
        "digital": "digital art, high detail, vibrant colors, fantasy style",
        "realistic": "photorealistic, highly detailed, professional photography"
    }
    
    enhancement = style_enhancements.get(style, style_enhancements["realistic"])
    return f"{prompt}, {enhancement}"

def generate_images(prompt, negative_prompt=None, width=1024, height=1024, 
                   count=1, style="realistic"):
    """
    生成图片的主函数
    
    参数:
        prompt (str): 正向提示词
        negative_prompt (str, optional): 反向提示词
        width (int): 图片宽度
        height (int): 图片高度
        count (int): 生成图片数量
        style (str): 图片风格，可选值：realistic, cartoon, painting, digital
        
    返回:
        dict: API响应结果
    """
    try:
        # 获取长宽比
        aspect_ratio = get_aspect_ratio(width, height)
        
        # 增强提示词
        enhanced_prompt = enhance_prompt_by_style(prompt, style)
        
        # 构建请求体
        request_body = {
            "model": MINIMAX_API_CONFIG["model"],
            "prompt": enhanced_prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": count,
            "prompt_optimizer": True
        }
        
        if negative_prompt:
            request_body["negative_prompt"] = negative_prompt
            
        # 发送API请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MINIMAX_API_CONFIG['api_key']}"
        }
        
        response = requests.post(
            MINIMAX_API_CONFIG["base_url"],
            headers=headers,
            json=request_body,
            timeout=60
        )
        
        # 检查响应状态
        if response.status_code == 200:
            return response.json()
        else:
            error_message = response.json() if response.text else "未知错误"
            return {
                "error": {
                    "message": f"API调用失败: {error_message}",
                    "code": response.status_code
                }
            }
            
    except Exception as e:
        return {
            "error": {
                "message": f"服务器错误: {str(e)}",
                "code": 500
            }
        }

def get_supported_styles():
    """获取支持的图片风格列表"""
    return [
        {
            "id": "realistic",
            "name": "写实风格",
            "description": "照片级真实感，适合风景、人像等真实场景"
        },
        {
            "id": "cartoon",
            "name": "卡通风格",
            "description": "简化的形状和鲜艳的色彩，适合动漫和插画"
        },
        {
            "id": "painting",
            "name": "绘画风格",
            "description": "油画效果，富有艺术感的笔触细节"
        },
        {
            "id": "digital",
            "name": "数字艺术",
            "description": "现代数字艺术风格，适合科幻和奇幻场景"
        }
    ]

def get_supported_sizes():
    """获取支持的图片尺寸列表"""
    return [
        {
            "width": 1024,
            "height": 1024,
            "name": "1:1 方形",
            "description": "1024x1024 适合社交媒体"
        },
        {
            "width": 1024,
            "height": 768,
            "name": "4:3 横向",
            "description": "1024x768 适合电脑屏幕"
        },
        {
            "width": 768,
            "height": 1024,
            "name": "3:4 竖向",
            "description": "768x1024 适合手机屏幕"
        },
        {
            "width": 1024,
            "height": 576,
            "name": "16:9 宽屏",
            "description": "1024x576 适合视频封面"
        },
        {
            "width": 576,
            "height": 1024,
            "name": "9:16 竖屏",
            "description": "576x1024 适合手机壁纸"
        }
    ] 