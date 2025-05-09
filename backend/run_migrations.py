#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库迁移脚本
用于应用新创建的迁移文件
"""

import os
import sys
from flask_migrate import upgrade

# 添加项目根目录到sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# 从当前应用中导入必要的组件
from app import create_app, db

def run_migrations():
    """运行数据库迁移"""
    app = create_app('migrations')
    with app.app_context():
        # 应用所有待处理的迁移
        upgrade()
        print("数据库迁移成功应用!")

if __name__ == "__main__":
    run_migrations() 