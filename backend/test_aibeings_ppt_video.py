#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试小冰AI Beings PPT讲解视频服务接口
"""

import os
import sys
import time
import logging
import argparse
from dotenv import load_dotenv

# 设置日志级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 解析命令行参数
parser = argparse.ArgumentParser(description='测试小冰AI Beings PPT讲解视频服务接口')
parser.add_argument('--ppt_path', type=str, help='PPT文件路径')
parser.add_argument('--simulation', action='store_true', help='使用模拟模式')
args = parser.parse_args()

# 确保backend目录在sys.path中，以便正确导入服务模块
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, backend_dir)

# 尝试加载环境变量
env_file = os.path.join(project_root, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)
    logger.info(f"已加载环境变量文件: {env_file}")
else:
    logger.warning(f"找不到环境变量文件: {env_file}")

# 手动设置阿里云OSS环境变量（用户提供的凭证）
os.environ['ALIYUN_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY_ID'
os.environ['ALIYUN_ACCESS_KEY_SECRET'] = 'YOUR_ACCESS_KEY_SECRET'
os.environ['ALIYUN_OSS_BUCKET'] = 'ezijingai'
os.environ['ALIYUN_OSS_ENDPOINT'] = 'oss-cn-beijing.aliyuncs.com'
os.environ['ALIYUN_REGION'] = 'cn-beijing'
logger.info("已手动设置阿里云OSS环境变量")

# 设置模拟模式环境变量（如果命令行指定）
if args.simulation:
    os.environ["MOCK_API"] = "true"
    logger.info("使用模拟API模式")
else:
    os.environ["MOCK_API"] = "false"
    logger.info("使用真实API模式")

# 导入服务接口
from app.services.aibeings_ppt_video import (
    get_digital_humans,
    get_digital_human_postures,
    create_ppt_video_task,
    query_ppt_video_task,
    get_supported_resolutions
)

# 检查阿里云OSS配置
logger.info("检查阿里云OSS配置...")
access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')
access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
bucket_name = os.getenv('ALIYUN_OSS_BUCKET')

# 安全显示凭证信息
if access_key_id:
    logger.info(f"OSS Access Key ID: {access_key_id[:5]}... (长度: {len(access_key_id)})")
else:
    logger.info("OSS Access Key ID: 未设置")

if access_key_secret:
    logger.info(f"OSS Access Key Secret: {access_key_secret[:5]}... (长度: {len(access_key_secret)})")
else:
    logger.info("OSS Access Key Secret: 未设置")

logger.info(f"OSS Bucket: {bucket_name if bucket_name else '未设置'}")

if access_key_id and access_key_secret and bucket_name:
    logger.info(f"阿里云OSS配置已加载，Bucket: {bucket_name}")
else:
    logger.warning("阿里云OSS配置不完整，将使用小冰API上传功能")

def test_get_digital_humans():
    """测试获取数字人列表"""
    logger.info("测试获取数字人列表...")
    result = get_digital_humans()
    
    # 检查结果
    if "error" in result:
        logger.error(f"获取数字人列表失败: {result['error']['message']}")
        return None
    
    # 返回第一个数字人ID
    if "data" in result and len(result["data"]) > 0:
        return result["data"][0]["virtualHumanId"]
    return None

def test_get_digital_human_postures(digital_human_id):
    """测试获取数字人姿势列表"""
    logger.info("测试获取数字人姿势列表...")
    
    # 如果未提供数字人ID，使用默认ID
    if not digital_human_id:
        digital_human_id = "VHP3S1EF7"  # 默认数字人ID
        logger.info(f"使用默认数字人ID: {digital_human_id}")
    
    result = get_digital_human_postures(digital_human_id)
    
    # 检查结果
    if "error" in result:
        logger.error(f"获取数字人姿势列表失败: {result['error']['message']}")
        return None
    
    # 返回第一个姿势ID
    if "data" in result and len(result["data"]) > 0:
        return result["data"][0]["postureId"]
    return None

def test_get_supported_resolutions():
    """测试获取支持的分辨率"""
    logger.info("测试获取支持的分辨率...")
    resolutions = get_supported_resolutions()
    logger.info(f"支持的分辨率: {', '.join(resolutions)}")
    return resolutions

def test_get_supported_digital_humans():
    """测试获取支持的数字人"""
    logger.info("测试获取支持的数字人...")
    from app.services.aibeings_ppt_video import DEFAULT_VIRTUAL_HUMANS
    
    # 尝试从API获取
    result = get_digital_humans()
    humans = []
    
    if "error" not in result and "data" in result:
        humans = result["data"]
    else:
        # 使用默认数字人
        from app.services.aibeings_ppt_video import DEFAULT_VIRTUAL_HUMANS
        logger.warning("获取数字人列表失败，使用默认数字人列表")
        for key, value in DEFAULT_VIRTUAL_HUMANS.items():
            humans.append({
                "virtualHumanId": value["virtualHumanId"],
                "name": f"{'默认数字人' if key == 'default' else ('商务男士' if key == 'business_man' else '商务女士')}"
            })
    
    # 显示数字人列表
    logger.info(f"支持的数字人数量: {len(humans)}")
    for i, human in enumerate(humans):
        logger.info(f"数字人 {i+1}: ID={human['virtualHumanId']}, 名称={human.get('name', '未知')}")
    
    return humans

def main():
    # 检查是否提供了PPT文件路径
    if not args.ppt_path:
        logger.error("请提供PPT文件路径")
        return
    
    # 检查文件是否存在
    if not os.path.exists(args.ppt_path):
        logger.error(f"PPT文件不存在: {args.ppt_path}")
        return
    
    # 获取支持的数字人和分辨率
    digital_human_id = test_get_digital_humans()
    posture_id = test_get_digital_human_postures(digital_human_id)
    test_get_supported_resolutions()
    test_get_supported_digital_humans()
    
    # 使用默认数字人和姿势
    if not digital_human_id:
        digital_human_id = "VHP3S1EF7"  # 默认数字人ID
    
    if not posture_id:
        posture_id = "aMiAX96rMqNS"  # 默认姿势ID
    
    # 创建PPT讲解视频任务
    logger.info(f"使用PPT文件: {args.ppt_path}")
    logger.info("创建PPT讲解视频任务...")
    
    result = create_ppt_video_task(
        ppt_file_path=args.ppt_path,
        text_script="这是一个测试用PPT讲解，请欣赏以下内容。",
        virtual_human_id=digital_human_id,
        virtual_human_posture_id=posture_id,
        title="测试PPT讲解视频",
        resolution="720p"
    )
    
    # 检查结果
    if "status" in result and result["status"] == "failed":
        logger.error(f"创建任务失败: {result['error']['message']}")
        return
    
    # 获取任务ID
    task_id = result.get("task_id")
    if not task_id:
        logger.error("创建任务失败: 未返回任务ID")
        return
    
    logger.info(f"任务创建成功，ID: {task_id}")
    logger.info(f"任务状态: {result['status']}")
    
    # 轮询任务状态 (最多10次，间隔5秒)
    max_polls = 10
    for i in range(max_polls):
        logger.info(f"第{i+1}次查询任务状态，任务ID: {task_id}")
        
        status_result = query_ppt_video_task(task_id)
        current_status = status_result.get("status", "未知")
        
        logger.info(f"当前任务状态: {current_status}")
        
        # 如果任务已完成或失败，停止轮询
        if current_status in ["completed", "failed"]:
            logger.info(f"任务最终状态: {current_status}")
            if current_status == "completed" and "video_url" in status_result:
                logger.info(f"视频URL: {status_result['video_url']}")
            break
        
        # 等待一段时间再次查询
        logger.info("等待5秒后再次查询...")
        time.sleep(5)

if __name__ == "__main__":
    main() 