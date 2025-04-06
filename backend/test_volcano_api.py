#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试火山引擎文生图API
"""

import os
import json
from volcengine.visual.VisualService import VisualService

# 火山引擎API配置
ACCESS_KEY_ID = "YOUR_VOLCANO_ACCESS_KEY_ID"
SECRET_ACCESS_KEY = "YOUR_VOLCANO_SECRET_ACCESS_KEY"

def test_volcano_image_generation():
    """测试火山引擎文生图API"""
    print("开始测试火山引擎文生图API...")
    
    try:
        # 初始化服务
        visual_service = VisualService()
        
        # 直接设置ak和sk
        visual_service.set_ak(ACCESS_KEY_ID)
        visual_service.set_sk(SECRET_ACCESS_KEY)
        
        # 构建请求体
        request_body = {
            "req_key": "high_aes_general_v21_L",
            "prompt": "千军万马，气势磅礴，史诗般的战争场面",
            "model_version": "general_v2.1_L",
            "req_schedule_conf": "general_v20_9B_pe",
            "llm_seed": -1,
            "seed": -1,
            "scale": 3.5,
            "ddim_steps": 25,
            "width": 512,
            "height": 512,
            "use_pre_llm": True,
            "use_sr": True,
            "return_url": True,
            "logo_info": {
                "add_logo": False,
                "position": 0,
                "language": 0,
                "opacity": 0.3,
                "logo_text_content": "紫荆AI平台生成"
            }
        }
        
        print(f"请求参数: {json.dumps(request_body, ensure_ascii=False, indent=2)}")
        
        # 调用API
        print("正在调用API...")
        response = visual_service.cv_process(request_body)
        
        # 处理响应
        if not isinstance(response, dict):
            try:
                response = json.loads(response)
            except:
                print(f"响应内容: {response}")
                return
        
        print(f"API响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
        
        # 检查响应状态
        if response.get("code") == 10000:  # 成功状态码
            print("✅ API调用成功!")
            
            # 提取图片URL，从image_urls数组中获取
            image_urls = response.get("data", {}).get("image_urls", [])
            if image_urls:
                print(f"生成的图片数量: {len(image_urls)}")
                for i, url in enumerate(image_urls):
                    print(f"图片 {i+1} URL: {url}")
            else:
                print("警告: 响应中没有图片URL")
                
            # 提取LLM生成的增强提示词
            llm_result = response.get("data", {}).get("llm_result", "")
            if llm_result:
                print(f"\nLLM增强提示词: {llm_result}")
        else:
            print(f"❌ API调用失败: {response.get('message', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 发生异常: {str(e)}")
    
    print("测试完成")

if __name__ == "__main__":
    test_volcano_image_generation() 