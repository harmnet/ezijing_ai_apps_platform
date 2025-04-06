#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台文生图服务接口（火山引擎）
实现了对火山引擎文生图API的调用，提供文本生成图片的功能

主要功能：
- 支持自定义图片宽高
- 支持多种生成参数调整
- 支持返回图片URL或Base64
"""

import os
import json
import base64
import requests
from flask import current_app
from volcengine.visual.VisualService import VisualService

# 火山引擎API配置
VOLCANO_API_CONFIG = {
    "access_key_id": os.environ.get("VOLCANO_ACCESS_KEY_ID", "YOUR_VOLCANO_ACCESS_KEY_ID"),
    "secret_access_key": os.environ.get("VOLCANO_SECRET_ACCESS_KEY", "YOUR_VOLCANO_SECRET_ACCESS_KEY"),
    "req_key": "high_aes_general_v21_L",
    "model_version": "general_v2.1_L",
    "req_schedule_conf": "general_v20_9B_pe"
}

class VolcanoImageGenerator:
    """火山引擎文生图API封装类"""
    
    def __init__(self):
        """初始化火山引擎服务"""
        self.visual_service = VisualService()
        
        # 设置访问密钥
        self.visual_service.set_ak(VOLCANO_API_CONFIG["access_key_id"])
        self.visual_service.set_sk(VOLCANO_API_CONFIG["secret_access_key"])
    
    def generate_image(self, prompt, width=512, height=512, 
                      scale=3.5, steps=25, use_sr=True, 
                      return_url=True, add_watermark=False):
        """
        调用火山引擎API生成图片
        
        参数:
            prompt (str): 提示词
            width (int): 图片宽度 (默认512)
            height (int): 图片高度 (默认512)
            scale (float): 缩放因子 (默认3.5)
            steps (int): 生成步数 (默认25)
            use_sr (bool): 是否使用超分辨率 (默认True)
            return_url (bool): 是否返回URL (默认True)
            add_watermark (bool): 是否添加水印 (默认False)
            
        返回:
            dict: API响应结果
        """
        try:
            # 构建请求体
            request_body = {
                "req_key": VOLCANO_API_CONFIG["req_key"],
                "prompt": prompt,
                "model_version": VOLCANO_API_CONFIG["model_version"],
                "req_schedule_conf": VOLCANO_API_CONFIG["req_schedule_conf"],
                "llm_seed": -1,
                "seed": -1,
                "scale": scale,
                "ddim_steps": steps,
                "width": width,
                "height": height,
                "use_pre_llm": True,
                "use_sr": use_sr,
                "return_url": return_url,
                "logo_info": {
                    "add_logo": add_watermark,
                    "position": 0,
                    "language": 0,
                    "opacity": 0.3,
                    "logo_text_content": "紫荆AI平台生成"
                }
            }
            
            # 调用API
            response = self.visual_service.cv_process(request_body)
            
            # 处理响应
            return self._process_response(response)
            
        except Exception as e:
            current_app.logger.error(f"火山引擎文生图API调用失败: {str(e)}")
            return {
                "success": False,
                "error": {
                    "message": f"服务器错误: {str(e)}",
                    "code": 500
                }
            }
    
    def _process_response(self, response):
        """处理API响应"""
        try:
            if not isinstance(response, dict):
                try:
                    response = json.loads(response)
                except:
                    current_app.logger.error(f"无法解析API响应为JSON: {response}")
                    return {
                        "success": False,
                        "error": {
                            "message": "无法解析API响应",
                            "code": -1
                        }
                    }
                
            # 检查响应状态
            if response.get("code") == 10000:  # 成功状态码
                # 从image_urls数组中提取图片URL
                image_urls = response.get("data", {}).get("image_urls", [])
                llm_result = response.get("data", {}).get("llm_result", "")
                request_id = response.get("request_id", "")
                
                result = {
                    "success": True,
                    "data": {
                        "images": [],
                        "request_id": request_id,
                        "enhanced_prompt": llm_result
                    }
                }
                
                # 添加所有图片URL
                if image_urls:
                    for url in image_urls:
                        result["data"]["images"].append({
                            "url": url
                        })
                
                return result
            else:
                return {
                    "success": False,
                    "error": {
                        "message": response.get("message", "未知错误"),
                        "code": response.get("code", -1)
                    }
                }
                
        except Exception as e:
            current_app.logger.error(f"处理响应失败: {str(e)}")
            return {
                "success": False,
                "error": {
                    "message": f"处理响应失败: {str(e)}",
                    "code": -1
                }
            }

def get_supported_sizes():
    """获取支持的图片尺寸列表"""
    return [
        {
            "width": 512,
            "height": 512,
            "name": "1:1 标准",
            "description": "512x512 标准方形"
        },
        {
            "width": 768,
            "height": 768,
            "name": "1:1 高清",
            "description": "768x768 高清方形"
        },
        {
            "width": 512,
            "height": 768,
            "name": "2:3 竖向",
            "description": "512x768 适合手机屏幕"
        },
        {
            "width": 768,
            "height": 512,
            "name": "3:2 横向",
            "description": "768x512 适合桌面展示"
        }
    ]

# 直接实例化一个全局生成器对象
volcano_generator = VolcanoImageGenerator()

# 提供一个简便的生成图片函数接口
def generate_images(prompt, width=512, height=512, count=1, **kwargs):
    """
    生成图片的主函数
    
    参数:
        prompt (str): 提示词
        width (int): 图片宽度
        height (int): 图片高度
        count (int): 生成数量 (注：火山引擎接口每次只能生成一张图片)
        **kwargs: 其他参数
        
    返回:
        dict: API响应结果
    """
    # 目前火山引擎接口每次只能生成一张图片，忽略count参数
    result = volcano_generator.generate_image(prompt, width, height, **kwargs)
    
    # 如果成功且需要生成多张图片，则多次调用API
    if result.get("success") and count > 1 and len(result.get("data", {}).get("images", [])) > 0:
        # 继续生成剩余的图片
        for _ in range(1, count):
            next_result = volcano_generator.generate_image(prompt, width, height, **kwargs)
            if next_result.get("success"):
                # 将新生成的图片添加到结果中
                result["data"]["images"].extend(next_result.get("data", {}).get("images", []))
    
    return result 