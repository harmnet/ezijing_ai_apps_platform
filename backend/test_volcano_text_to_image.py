#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试火山引擎文生图API
测试已部署的服务类
"""

import json
from app.services.interface_volcano_text_to_images import generate_images, get_supported_sizes

def test_volcano_text_to_image_service():
    """测试火山引擎文生图服务"""
    print("开始测试火山引擎文生图服务...")
    
    # 测试图片尺寸
    print("\n1. 获取支持的图片尺寸...")
    sizes = get_supported_sizes()
    print(f"支持的尺寸: {json.dumps(sizes, ensure_ascii=False, indent=2)}")
    
    # 测试生成图片
    print("\n2. 测试生成图片...")
    prompt = "水墨山水画，中国风"
    width = 512
    height = 512
    count = 1
    
    print(f"提示词: {prompt}")
    print(f"尺寸: {width}x{height}")
    print(f"数量: {count}")
    
    # 调用服务
    result = generate_images(
        prompt=prompt,
        width=width,
        height=height,
        count=count,
        scale=3.5,
        steps=25,
        use_sr=True,
        return_url=True,
        add_watermark=False
    )
    
    # 处理结果
    print(f"\n生成结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result.get("success"):
        images = result.get("data", {}).get("images", [])
        print(f"\n成功生成 {len(images)} 张图片:")
        for i, image in enumerate(images):
            print(f"图片 {i+1} URL: {image.get('url')}")
            
        # 显示增强提示词
        enhanced_prompt = result.get("data", {}).get("enhanced_prompt", "")
        if enhanced_prompt:
            print(f"\n增强提示词: {enhanced_prompt}")
    else:
        print(f"\n生成失败: {result.get('error', {}).get('message', '未知错误')}")
    
    print("\n测试完成")

if __name__ == "__main__":
    test_volcano_text_to_image_service() 