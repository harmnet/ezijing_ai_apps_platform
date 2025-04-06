#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库初始化脚本
用于创建所有必要的数据库表
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# 加载环境变量
load_dotenv()

from app import create_app, db
from app.models.digital_human import PPTVideoTask

def init_db():
    """初始化数据库，创建所有表"""
    app = create_app('migrations')
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建成功!")

if __name__ == "__main__":
    init_db() 