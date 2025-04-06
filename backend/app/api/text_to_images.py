#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台文生图API路由（MiniMax版本）
"""

from flask import Blueprint

# 创建蓝图
text_to_images = Blueprint('text_to_images', __name__) 