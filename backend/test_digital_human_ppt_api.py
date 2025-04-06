#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试数字人PPT讲解视频API接口
"""

import os
import sys
import time
import logging
import argparse
import requests
from dotenv import load_dotenv

# 设置日志级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 解析命令行参数
parser = argparse.ArgumentParser(description='测试数字人PPT讲解视频API接口')
parser.add_argument('--ppt_path', type=str, help='PPT文件路径')
parser.add_argument('--host', type=str, default='http://localhost:5000', help='API主机地址')
args = parser.parse_args()

# 确保backend目录在sys.path中
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 尝试加载环境变量
env_file = os.path.join(script_dir, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)
    logger.info(f"已加载环境变量文件: {env_file}")
else:
    logger.warning(f"找不到环境变量文件: {env_file}")

def test_get_digital_humans():
    """测试获取数字人列表API"""
    logger.info("测试获取数字人列表...")
    
    url = f"{args.host}/api/v1/digital_human/ppt/humans"
    response = requests.get(url)
    
    logger.info(f"HTTP状态码: {response.status_code}")
    result = response.json()
    logger.info(f"API响应: {result}")
    
    # 检查结果
    if result.get("code") != 0:
        logger.error(f"获取数字人列表失败: {result.get('message')}")
        return None
    
    # 返回第一个数字人ID
    if "data" in result and len(result["data"]) > 0:
        digital_human_id = result["data"][0]["virtualHumanId"]
        logger.info(f"选择数字人ID: {digital_human_id}")
        return digital_human_id
    
    return None

def test_get_digital_human_postures(digital_human_id):
    """测试获取数字人姿势列表API"""
    logger.info("测试获取数字人姿势列表...")
    
    if not digital_human_id:
        logger.error("数字人ID为空")
        return None
    
    url = f"{args.host}/api/v1/digital_human/ppt/postures/{digital_human_id}"
    response = requests.get(url)
    
    logger.info(f"HTTP状态码: {response.status_code}")
    result = response.json()
    logger.info(f"API响应: {result}")
    
    # 检查结果
    if result.get("code") != 0:
        logger.error(f"获取数字人姿势列表失败: {result.get('message')}")
        return None
    
    # 返回第一个姿势ID
    if "data" in result and len(result["data"]) > 0:
        posture_id = result["data"][0]["postureId"]
        logger.info(f"选择姿势ID: {posture_id}")
        return posture_id
    
    return None

def test_get_supported_resolutions():
    """测试获取支持的分辨率API"""
    logger.info("测试获取支持的分辨率...")
    
    url = f"{args.host}/api/v1/digital_human/ppt/resolutions"
    response = requests.get(url)
    
    logger.info(f"HTTP状态码: {response.status_code}")
    result = response.json()
    logger.info(f"API响应: {result}")
    
    # 检查结果
    if result.get("code") != 0:
        logger.error(f"获取支持的分辨率失败: {result.get('message')}")
        return None
    
    # 返回分辨率列表
    if "data" in result:
        logger.info(f"支持的分辨率: {', '.join(result['data'])}")
        return result["data"]
    
    return None

def test_create_ppt_video_task(ppt_path, digital_human_id, posture_id, resolution):
    """测试创建PPT讲解视频任务API"""
    logger.info("测试创建PPT讲解视频任务...")
    
    if not ppt_path:
        logger.error("PPT文件路径为空")
        return None
    
    if not os.path.exists(ppt_path):
        logger.error(f"PPT文件不存在: {ppt_path}")
        return None
    
    url = f"{args.host}/api/v1/digital_human/ppt/generate"
    
    # 准备请求数据
    files = {
        'ppt_file': open(ppt_path, 'rb')
    }
    
    data = {
        'text_script': "这是一个测试用PPT讲解，请欣赏以下内容。",
        'title': "测试PPT讲解视频",
        'resolution': resolution if resolution else "720p"
    }
    
    if digital_human_id:
        data['virtual_human_id'] = digital_human_id
    
    if posture_id:
        data['virtual_human_posture_id'] = posture_id
    
    logger.info(f"请求数据: {data}")
    logger.info(f"文件: {ppt_path}")
    
    # 发送请求
    response = requests.post(url, files=files, data=data)
    
    logger.info(f"HTTP状态码: {response.status_code}")
    result = response.json()
    logger.info(f"API响应: {result}")
    
    # 检查结果
    if result.get("code") != 0:
        logger.error(f"创建任务失败: {result.get('message')}")
        return None
    
    # 获取任务ID
    if "data" in result and "task_id" in result["data"]:
        task_id = result["data"]["task_id"]
        logger.info(f"任务创建成功，ID: {task_id}")
        return task_id
    
    return None

def test_query_ppt_video_task(task_id):
    """测试查询PPT讲解视频任务状态API"""
    logger.info(f"测试查询PPT讲解视频任务状态: {task_id}")
    
    if not task_id:
        logger.error("任务ID为空")
        return None
    
    url = f"{args.host}/api/v1/digital_human/ppt/task/{task_id}"
    response = requests.get(url)
    
    logger.info(f"HTTP状态码: {response.status_code}")
    result = response.json()
    logger.info(f"API响应: {result}")
    
    # 检查结果
    if result.get("code") != 0:
        logger.error(f"查询任务失败: {result.get('message')}")
        return None
    
    # 获取任务状态
    if "data" in result and "status" in result["data"]:
        status = result["data"]["status"]
        logger.info(f"任务状态: {status}")
        
        # 如果任务完成，显示视频URL
        if status == "completed" and "video_url" in result["data"]:
            video_url = result["data"]["video_url"]
            logger.info(f"视频URL: {video_url}")
        
        return status
    
    return None

def main():
    # 检查是否提供了PPT文件路径
    if not args.ppt_path:
        logger.error("请提供PPT文件路径")
        return
    
    # 获取数字人ID
    digital_human_id = test_get_digital_humans()
    
    # 获取姿势ID
    posture_id = test_get_digital_human_postures(digital_human_id)
    
    # 获取支持的分辨率
    resolutions = test_get_supported_resolutions()
    resolution = resolutions[0] if resolutions else "720p"
    
    # 创建任务
    task_id = test_create_ppt_video_task(args.ppt_path, digital_human_id, posture_id, resolution)
    
    if not task_id:
        logger.error("任务创建失败")
        return
    
    # 轮询任务状态 (最多10次，间隔5秒)
    max_polls = 10
    for i in range(max_polls):
        logger.info(f"第{i+1}次查询任务状态")
        
        status = test_query_ppt_video_task(task_id)
        
        # 如果任务已完成或失败，停止轮询
        if status in ["completed", "failed"]:
            logger.info(f"任务最终状态: {status}")
            break
        
        # 等待一段时间再次查询
        if i < max_polls - 1:
            logger.info("等待5秒后再次查询...")
            time.sleep(5)

if __name__ == "__main__":
    main()