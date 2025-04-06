#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试火山引擎图生视频API功能
"""

import os
import time
import sys
import json
from app.services.volcano_image_to_video import (
    create_image_to_video_task,
    query_video_task,
    delete_video_task,
    list_video_tasks,
    get_supported_ratios,
    get_supported_durations
)

def print_section(title):
    """打印分隔符和标题"""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "-"))
    print("=" * 50 + "\n")

def pretty_print(obj):
    """美化输出JSON对象"""
    if isinstance(obj, dict):
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(obj)

def test_create_task():
    """测试创建图生视频任务"""
    print_section("创建图生视频任务")
    
    # 测试图片URL (此处应替换为您自己的图片URL)
    image_url = "https://ark-project.tos-cn-beijing.volces.com/doc_image/i2v_foxrgirl.png"
    
    # 测试提示词
    prompt = "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动"
    
    # 创建任务
    result = create_image_to_video_task(
        image_url=image_url,
        prompt=prompt,
        ratio="16:9",
        duration=5.0
    )
    
    pretty_print(result)
    return result.get("id") if isinstance(result, dict) and "id" in result else None

def test_query_task(task_id):
    """测试查询任务状态"""
    print_section("查询任务状态")
    
    if not task_id:
        print("没有有效的任务ID可供查询")
        return
    
    # 查询任务状态
    result = query_video_task(task_id)
    pretty_print(result)
    
    # 返回任务状态
    return result.get("status") if isinstance(result, dict) and "status" in result else None

def test_list_tasks():
    """测试列出任务"""
    print_section("列出所有任务")
    
    # 列出所有任务
    result = list_video_tasks(page_num=1, page_size=5)
    pretty_print(result)

def test_delete_task(task_id):
    """测试删除任务"""
    print_section("删除任务")
    
    if not task_id:
        print("没有有效的任务ID可供删除")
        return
    
    # 删除任务
    result = delete_video_task(task_id)
    pretty_print(result)

def test_supported_params():
    """测试获取支持的参数"""
    print_section("支持的参数")
    
    print("支持的视频比例:")
    pretty_print(get_supported_ratios())
    
    print("\n支持的视频时长范围:")
    pretty_print(get_supported_durations())

def run_complete_test():
    """运行完整的测试流程"""
    # 测试支持的参数
    test_supported_params()
    
    # 创建任务
    task_id = test_create_task()
    
    if task_id:
        print(f"\n成功创建任务，任务ID: {task_id}")
        
        # 等待处理
        print("\n等待任务处理中...")
        max_checks = 10
        checks = 0
        status = None
        
        while checks < max_checks:
            checks += 1
            print(f"检查 {checks}/{max_checks}...")
            status = test_query_task(task_id)
            
            # 如果任务完成或失败，停止检查
            if status in ["succeeded", "failed"]:
                break
                
            # 等待一段时间再检查
            time.sleep(10)
        
        # 查询最终状态
        if status != "succeeded":
            print("\n最终查询任务状态...")
            test_query_task(task_id)
            
        # 列出所有任务
        test_list_tasks()
        
        # 删除任务（可选，取消注释以测试删除功能）
        # test_delete_task(task_id)
    else:
        print("任务创建失败，无法继续测试")

if __name__ == "__main__":
    run_complete_test() 