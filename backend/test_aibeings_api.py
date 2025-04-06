import requests
import json
import sqlite3
import os

# 数据库路径
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "dev.db")

def create_aibeings_table_if_not_exists():
    """创建数字人表（如果不存在）"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ai_beings'")
        if cursor.fetchone() is None:
            print("正在创建ai_beings表...")
            
            # 创建表
            cursor.execute('''
            CREATE TABLE ai_beings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                avatar VARCHAR(255),
                description TEXT,
                type VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'active',
                config JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # 插入测试数据
            test_data = [
                {
                    "name": "小冰助手",
                    "avatar": "https://ezijingai.oss-cn-beijing.aliyuncs.com/aibeings/avatar1.png",
                    "description": "智能问答助手，可以回答各种问题",
                    "type": "chat",
                    "status": "active",
                    "config": json.dumps({"model": "gpt-4", "temperature": 0.7})
                },
                {
                    "name": "数字人讲解员",
                    "avatar": "https://ezijingai.oss-cn-beijing.aliyuncs.com/aibeings/avatar2.png",
                    "description": "可以生成视频讲解内容",
                    "type": "video",
                    "status": "active",
                    "config": json.dumps({"model": "video-gen-1", "resolution": "720p"})
                },
                {
                    "name": "AI画师",
                    "avatar": "https://ezijingai.oss-cn-beijing.aliyuncs.com/aibeings/avatar3.png",
                    "description": "智能绘画，可以根据描述生成图片",
                    "type": "image",
                    "status": "inactive",
                    "config": json.dumps({"model": "stable-diffusion-3", "steps": 30})
                }
            ]
            
            for item in test_data:
                cursor.execute('''
                INSERT INTO ai_beings (name, avatar, description, type, status, config)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    item["name"],
                    item["avatar"],
                    item["description"],
                    item["type"],
                    item["status"],
                    item["config"]
                ))
            
            conn.commit()
            print("ai_beings表创建成功，并插入了测试数据")
        else:
            print("ai_beings表已存在")
            
        conn.close()
    except sqlite3.Error as e:
        print(f"数据库操作出错: {e}")

def test_get_aibeings():
    """测试获取数字人列表API"""
    try:
        response = requests.get("http://localhost:9000/api/v1/aibeings/aibeings")
        print(f"状态码: {response.status_code}")
        print("响应内容:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"请求出错: {e}")

def test_get_aibeing_by_id(aibeing_id=1):
    """测试获取单个数字人详情API"""
    try:
        response = requests.get(f"http://localhost:9000/api/v1/aibeings/aibeings/{aibeing_id}")
        print(f"状态码: {response.status_code}")
        print("响应内容:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"请求出错: {e}")

if __name__ == "__main__":
    print("===== 开始测试数字人API =====")
    
    # 创建数据库表和测试数据
    create_aibeings_table_if_not_exists()
    
    # 测试获取数字人列表
    print("\n===== 测试获取数字人列表 =====")
    test_get_aibeings()
    
    # 测试获取单个数字人详情
    print("\n===== 测试获取数字人详情 =====")
    test_get_aibeing_by_id(1)
    
    print("\n===== 测试完成 =====") 