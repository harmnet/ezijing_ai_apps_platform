#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志工具模块
提供统一的日志记录功能
"""

import os
import logging
from logging.handlers import RotatingFileHandler

# 创建默认的logger对象
logger = logging.getLogger('app')
# 创建图像重绘专用logger对象
image_redraw_logger = logging.getLogger('image_redraw')

def setup_logger(app, log_level=logging.INFO):
    """
    设置应用的日志配置
    
    Args:
        app: Flask应用实例
        log_level: 日志级别，默认为INFO
    """
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 设置日志文件路径
    log_file = os.path.join(log_dir, 'app.log')
    
    # 创建日志处理器
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    
    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # 设置日志级别
    file_handler.setLevel(log_level)
    
    # 添加处理器到应用
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
    
    # 设置Werkzeug日志
    logging.getLogger('werkzeug').addHandler(file_handler)
    
    # 设置默认logger
    global logger
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
    
    return app.logger

def setup_image_redraw_logger(app=None, log_level=logging.INFO):
    """
    设置图像重绘功能的专用日志配置
    
    Args:
        app: Flask应用实例（可选）
        log_level: 日志级别，默认为INFO
        
    Returns:
        logging.Logger: 图像重绘专用日志记录器
    """
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 设置图像重绘专用日志文件路径
    image_redraw_log_file = os.path.join(log_dir, 'image_redraw.log')
    
    # 创建日志处理器
    file_handler = RotatingFileHandler(
        image_redraw_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    
    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # 设置日志级别
    file_handler.setLevel(log_level)
    
    # 配置图像重绘日志记录器
    global image_redraw_logger
    
    # 移除现有处理器（如果有）
    for handler in image_redraw_logger.handlers[:]:
        image_redraw_logger.removeHandler(handler)
    
    # 添加处理器
    image_redraw_logger.addHandler(file_handler)
    image_redraw_logger.setLevel(log_level)
    
    # 如果提供了app，添加同样的处理器到app.logger
    if app:
        app.logger.info(f"已配置图像重绘专用日志，文件路径: {image_redraw_log_file}")
    
    return image_redraw_logger

def get_logger(name):
    """
    获取一个命名的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器实例
    """
    logger = logging.getLogger(name)
    
    # 如果已经有处理器，直接返回
    if logger.handlers:
        return logger
    
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 设置日志文件路径
    log_file = os.path.join(log_dir, f'{name}.log')
    
    # 创建处理器
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    
    # 设置格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    
    return logger

def get_image_redraw_logger():
    """
    获取图像重绘专用日志记录器
    
    Returns:
        logging.Logger: 图像重绘日志记录器实例
    """
    global image_redraw_logger
    
    # 如果已经有处理器，直接返回
    if image_redraw_logger.handlers:
        return image_redraw_logger
    
    # 否则，设置图像重绘日志记录器
    return setup_image_redraw_logger()
    