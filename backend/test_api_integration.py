#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试火山引擎文生图API路由集成
"""

import os
import sys
import json
import requests
from flask import Flask, jsonify
from app.api.text_to_images_volcano import text_to_images_volcano

def create_test_app():
    """创建一个简单的Flask测试应用"""
    app = Flask(__name__)
    
    # 注册火山引擎文生图蓝图
    app.register_blueprint(text_to_images_volcano, url_prefix='/api/v1')
    
    # 添加一个简单的根路由
    @app.route('/')
    def index():
        return jsonify({
            "status": "ok",
            "message": "火山引擎文生图API测试服务器正在运行"
        })
    
    return app

def test_api_integration():
    """测试API路由集成"""
    app = create_test_app()
    
    with app.test_client() as client:
        print("开始测试API路由集成...")
        
        # 测试API信息接口
        print("\n1. 测试 API 信息接口...")
        response = client.get('/api/v1/text_to_image/volcano/info')
        print(f"状态码: {response.status_code}")
        print(f"响应数据: {json.dumps(response.get_json(), ensure_ascii=False, indent=2)}")
        
        # 测试支持的尺寸接口
        print("\n2. 测试支持的尺寸接口...")
        response = client.get('/api/v1/text_to_image/volcano/sizes')
        print(f"状态码: {response.status_code}")
        print(f"响应数据: {json.dumps(response.get_json(), ensure_ascii=False, indent=2)}")
        
        # 测试文生图接口
        print("\n3. 测试文生图接口...")
        request_data = {
            "prompt": "山水画，中国风，水墨",
            "width": 512,
            "height": 512,
            "count": 1,
            "scale": 3.5,
            "steps": 25,
            "use_sr": True,
            "return_url": True,
            "add_watermark": False
        }
        
        print(f"请求数据: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
        
        response = client.post(
            '/api/v1/text_to_image/volcano',
            json=request_data,
            content_type='application/json'
        )
        
        print(f"状态码: {response.status_code}")
        
        response_data = response.get_json()
        print(f"响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        
        # 如果成功生成图片，打印图片URL
        if response_data.get('success'):
            images = response_data.get('data', {}).get('images', [])
            print(f"\n成功生成 {len(images)} 张图片:")
            for i, image in enumerate(images):
                print(f"图片 {i+1} URL: {image.get('url')}")
        
        print("\n测试完成")

if __name__ == "__main__":
    test_api_integration() 