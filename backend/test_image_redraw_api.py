#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试阿里云图片重绘API接口
"""

import requests
import json
import time

# 测试服务器地址
BASE_URL = "http://127.0.0.1:9000/api/v1"

def test_create_redraw_task():
    """测试创建图片重绘任务"""
    
    # 测试请求参数
    test_data = {
        "prompt": "一个透明玻璃花瓶放在桌子上",
        "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_2.jpeg",
        "mask_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_2_mask.png",
        "n": 1
    }
    
    print("正在发送创建任务请求...")
    response = requests.post(
        f"{BASE_URL}/image_redraw/create",
        json=test_data
    )
    
    print(f"状态码: {response.status_code}")
    
    # 打印响应内容
    try:
        result = response.json()
        print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("success") and "task_id" in result.get("data", {}):
            task_id = result["data"]["task_id"]
            print(f"任务ID: {task_id}")
            return task_id
        else:
            print("未能获取任务ID")
            return None
    except Exception as e:
        print(f"解析响应失败: {str(e)}")
        print(f"原始响应: {response.text}")
        return None

def test_query_redraw_task(task_id):
    """测试查询图片重绘任务"""
    
    if not task_id:
        print("缺少任务ID，无法查询")
        return
    
    print(f"正在查询任务状态，任务ID: {task_id}")
    max_attempts = 10
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        print(f"第 {attempts} 次查询...")
        
        response = requests.get(
            f"{BASE_URL}/image_redraw/query/{task_id}"
        )
        
        print(f"状态码: {response.status_code}")
        
        try:
            result = response.json()
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get("success"):
                task_status = result.get("data", {}).get("task_status")
                print(f"任务状态: {task_status}")
                
                if task_status == "SUCCEEDED":
                    print("任务已完成!")
                    image_urls = result.get("data", {}).get("image_urls", [])
                    for i, url in enumerate(image_urls):
                        print(f"结果图片 {i+1}: {url}")
                    return
                elif task_status in ["FAILED", "REJECTED"]:
                    print("任务失败!")
                    error = result.get("data", {}).get("error", {})
                    if error:
                        print(f"错误信息: {error.get('message')}, 错误码: {error.get('code')}")
                    return
            
            print(f"任务仍在处理中，等待5秒后重试...")
            time.sleep(5)
        except Exception as e:
            print(f"解析响应失败: {str(e)}")
            print(f"原始响应: {response.text}")
            time.sleep(5)
    
    print(f"超过最大查询次数 ({max_attempts})，停止查询")

def test_get_api_info():
    """测试获取API信息"""
    
    print("正在获取API信息...")
    response = requests.get(
        f"{BASE_URL}/image_redraw/info"
    )
    
    print(f"状态码: {response.status_code}")
    
    try:
        result = response.json()
        print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"解析响应失败: {str(e)}")
        print(f"原始响应: {response.text}")

if __name__ == "__main__":
    print("===== 测试阿里云图片重绘API接口 =====")
    
    # 测试获取API信息
    print("\n1. 测试获取API信息")
    test_get_api_info()
    
    # 等待用户确认
    input("\n按回车键继续测试创建任务...")
    
    # 测试创建任务
    print("\n2. 测试创建任务")
    task_id = test_create_redraw_task()
    
    if task_id:
        # 等待用户确认
        input("\n按回车键继续测试查询任务...")
        
        # 测试查询任务
        print("\n3. 测试查询任务")
        test_query_redraw_task(task_id)
    
    print("\n===== 测试完成 =====") 