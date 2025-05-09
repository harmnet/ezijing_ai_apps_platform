#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库表创建脚本
用于手动创建缺失的数据库表
"""

from app import db, create_app
from app.models.academic_paper import AcademicPaper

def create_tables():
    """创建缺失的数据库表"""
    print("开始创建数据库表...")
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建完成")
        
        # 查询有哪些表已创建
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"当前数据库中的表: {tables}")
        
        # 检查academic_papers表是否存在
        if 'academic_papers' in tables:
            print("学术论文表(academic_papers)已存在")
            # 获取表的列
            columns = [col['name'] for col in inspector.get_columns('academic_papers')]
            print(f"学术论文表列: {columns}")
        else:
            print("警告: 学术论文表(academic_papers)不存在")

if __name__ == '__main__':
    create_tables()
    print("脚本执行完成") 