#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
清除数据库测试数据脚本
用于删除数据库中的测试记录
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

def clear_test_data():
    """清除数据库中的测试数据"""
    app = create_app('migrations')
    with app.app_context():
        # 删除所有PPTVideoTask记录
        count = PPTVideoTask.query.delete()
        db.session.commit()
        print(f"已成功删除 {count} 条测试数据!")

if __name__ == "__main__":
    clear_test_data() 