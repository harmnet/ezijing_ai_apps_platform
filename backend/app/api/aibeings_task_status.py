#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
import time
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app

# 创建蓝图
aibeings_task_status_bp = Blueprint('aibeings_task_status', __name__)
logger = logging.getLogger(__name__)

# 模拟任务数据库
# 在实际应用中，应该使用数据库存储任务状态
TASK_DATABASE = {}

# 初始化一些测试任务
def init_sample_tasks():
    """初始化一些示例任务，用于测试"""
    if not TASK_DATABASE:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        completed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 添加一个已完成的任务
        completed_task_id = f"task_{uuid.uuid4().hex}"
        TASK_DATABASE[completed_task_id] = {
            "taskId": completed_task_id,
            "status": "Completed",
            "progress": 100,
            "createdAt": current_time,
            "completedAt": completed_time,
            "result": {
                "videoUrl": "https://example.com/sample_video.mp4",
                "previewUrl": "https://example.com/sample_thumbnail.jpg",
                "scenes": 4
            }
        }
        
        # 添加一个处理中的任务
        processing_task_id = f"task_{uuid.uuid4().hex}"
        TASK_DATABASE[processing_task_id] = {
            "taskId": processing_task_id,
            "status": "Processing",
            "progress": 65,
            "createdAt": current_time,
            "completedAt": None,
            "result": None
        }
        
        # 添加一个失败的任务
        failed_task_id = f"task_{uuid.uuid4().hex}"
        TASK_DATABASE[failed_task_id] = {
            "taskId": failed_task_id,
            "status": "Failed",
            "progress": 30,
            "createdAt": current_time,
            "completedAt": None,
            "error": "处理过程中出现错误",
            "result": None
        }
        
        logger.info(f"初始化了{len(TASK_DATABASE)}个示例任务")
        # 打印示例任务ID，方便测试
        for task_id in TASK_DATABASE.keys():
            logger.info(f"示例任务ID: {task_id}")

# 初始化示例任务
init_sample_tasks()

@aibeings_task_status_bp.route('/video/task/status', methods=['GET', 'POST'])
def get_task_status():
    """获取任务状态
    
    请求方式：
    - GET: 通过查询参数传递taskId
    - POST: 通过JSON Body传递taskId
    
    参数:
        taskId (str): 任务ID
        
    返回:
        json: 任务状态信息
    """
    task_id = None
    
    # 支持GET和POST两种请求方式
    if request.method == 'GET':
        task_id = request.args.get('taskId')
    else:  # POST
        data = request.json
        task_id = data.get('taskId') if data else None
    
    logger.info(f"接收到任务状态查询请求: taskId={task_id}")
    
    # 验证任务ID
    if not task_id:
        logger.error("缺少taskId参数")
        return jsonify({
            "error": "缺少taskId参数",
            "code": 400
        }), 400
    
    # 如果是ppt-demo API创建的任务，提供模拟状态
    if task_id.startswith("task_"):
        # 检查是否在任务数据库中
        if task_id in TASK_DATABASE:
            task_info = TASK_DATABASE[task_id]
        else:
            # 为新任务ID创建随机状态
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 随机决定任务状态
            import random
            status_options = ["Processing", "Completed", "Failed"]
            status_weights = [0.2, 0.7, 0.1]  # 权重，大部分为已完成
            status = random.choices(status_options, weights=status_weights)[0]
            
            # 根据状态设置进度
            if status == "Processing":
                progress = random.randint(10, 90)
                completed_time = None
                result = None
                error = None
            elif status == "Completed":
                progress = 100
                completed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result = {
                    "videoUrl": f"https://example.com/videos/{task_id}.mp4",
                    "previewUrl": f"https://example.com/previews/{task_id}.jpg",
                    "scenes": 4
                }
                error = None
            else:  # Failed
                progress = random.randint(10, 90)
                completed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result = None
                error = "视频生成过程中出现错误"
            
            # 创建任务信息
            task_info = {
                "taskId": task_id,
                "status": status,
                "progress": progress,
                "createdAt": current_time,
                "completedAt": completed_time
            }
            
            # 根据状态添加额外信息
            if result:
                task_info["result"] = result
            if error:
                task_info["error"] = error
            
            # 保存到任务数据库
            TASK_DATABASE[task_id] = task_info
        
        logger.info(f"返回任务状态: {task_info}")
        return jsonify(task_info)
    
    # 如果不是系统创建的任务ID格式，返回错误
    logger.error(f"无效的任务ID格式: {task_id}")
    return jsonify({
        "error": "无效的任务ID",
        "code": 404
    }), 404

@aibeings_task_status_bp.route('/video/tasks', methods=['GET'])
def list_tasks():
    """列出所有任务
    
    返回:
        json: 所有任务的列表
    """
    tasks = list(TASK_DATABASE.values())
    return jsonify({
        "total": len(tasks),
        "tasks": tasks
    })

# 添加任务到模拟数据库的函数，可被其他模块调用
def add_task_to_database(task_id, task_info):
    """将任务添加到模拟数据库中
    
    参数:
        task_id (str): 任务ID
        task_info (dict): 任务信息
    """
    TASK_DATABASE[task_id] = task_info
    logger.info(f"添加任务到数据库: {task_id}")
    return task_id 