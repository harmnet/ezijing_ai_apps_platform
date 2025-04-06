#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
模拟任务存储模块
用于存储和管理各种模拟任务，特别是在API调用失败时创建的模拟任务
提供统一的任务存储和查询接口，避免多个模块间的任务查询问题
"""

import time
import logging
import threading

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 线程锁，用于保护共享资源的访问
_lock = threading.Lock()

# 模拟任务存储
_MOCK_TASKS = []

def add_task(task):
    """
    添加模拟任务到存储
    :param task: 包含任务信息的字典
    :return: 任务ID
    """
    with _lock:
        if not task.get("task_id"):
            logger.warning("添加的任务没有task_id字段")
            return None
            
        task_id = task["task_id"]
        
        # 检查任务是否已存在
        existing_task = None
        for t in _MOCK_TASKS:
            if t.get("task_id") == task_id:
                existing_task = t
                break
                
        if existing_task:
            # 更新已存在的任务
            for key, value in task.items():
                existing_task[key] = value
            logger.info(f"更新已存在的模拟任务: {task_id}")
        else:
            # 添加新任务
            _MOCK_TASKS.append(task)
            logger.info(f"添加新的模拟任务: {task_id}")
            
        logger.info(f"当前模拟任务总数: {len(_MOCK_TASKS)}")
        return task_id

def get_task(task_id):
    """
    获取模拟任务
    :param task_id: 任务ID
    :return: 任务对象，如果不存在则返回None
    """
    with _lock:
        for task in _MOCK_TASKS:
            if task.get("task_id") == task_id:
                return task
        return None

def update_task(task_id, **kwargs):
    """
    更新模拟任务的属性
    :param task_id: 任务ID
    :param kwargs: 要更新的属性和值
    :return: 更新后的任务，如果任务不存在则返回None
    """
    with _lock:
        task = get_task(task_id)
        if not task:
            return None
            
        # 更新任务属性
        for key, value in kwargs.items():
            task[key] = value
            
        return task

def remove_task(task_id):
    """
    移除模拟任务
    :param task_id: 任务ID
    :return: 是否成功移除
    """
    with _lock:
        for i, task in enumerate(_MOCK_TASKS):
            if task.get("task_id") == task_id:
                _MOCK_TASKS.pop(i)
                logger.info(f"已移除模拟任务: {task_id}")
                return True
        return False

def list_tasks():
    """
    列出所有模拟任务
    :return: 模拟任务列表的副本
    """
    with _lock:
        return _MOCK_TASKS.copy()

def clean_expired_tasks(max_age_seconds=3600):
    """
    清理过期的模拟任务
    :param max_age_seconds: 最大任务存活时间（秒）
    :return: 清理的任务数量
    """
    with _lock:
        current_time = time.time()
        expired_tasks = []
        
        for task in _MOCK_TASKS:
            create_time = task.get("create_time", 0)
            if current_time - create_time > max_age_seconds:
                expired_tasks.append(task)
                
        # 移除过期任务
        for task in expired_tasks:
            _MOCK_TASKS.remove(task)
            
        if expired_tasks:
            logger.info(f"已清理 {len(expired_tasks)} 个过期模拟任务")
            
        return len(expired_tasks) 