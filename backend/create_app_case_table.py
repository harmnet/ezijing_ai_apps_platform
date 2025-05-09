#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI应用案例表创建脚本
用于创建app_cases表
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# 加载环境变量
load_dotenv()

from app import db, create_app
from app.models.app_case import AppCase

def create_app_case_table():
    """创建AI应用案例表"""
    print("开始创建AI应用案例表...")
    app = create_app()
    with app.app_context():
        # 检查表是否已存在
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'app_cases' in tables:
            print("AI应用案例表(app_cases)已存在")
            # 获取表的列
            columns = [col['name'] for col in inspector.get_columns('app_cases')]
            print(f"AI应用案例表列: {columns}")
        else:
            # 创建表
            AppCase.__table__.create(db.engine)
            print("已创建AI应用案例表(app_cases)")

if __name__ == '__main__':
    create_app_case_table()
    print("脚本执行完成") 