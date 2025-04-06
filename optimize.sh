#!/bin/bash

# 优化脚本 - 紫荆AI平台
# 用于清理临时文件、停止重复服务和重启应用

echo "=== 紫荆AI平台优化脚本 ==="

# 停止所有运行中的服务
echo "停止所有运行中的服务..."
lsof -ti :8080 :8081 :8082 :9000 | xargs kill -9 2>/dev/null || true

# 清理临时文件
echo "清理临时文件..."
mkdir -p /Users/duanxiaofei/Desktop/ezijing_ai_apps_platform/backend/app/temp
find /Users/duanxiaofei/Desktop/ezijing_ai_apps_platform/backend/app/temp -type f -mtime +1 -delete 2>/dev/null || true

# 检查依赖
echo "检查依赖..."
cd /Users/duanxiaofei/Desktop/ezijing_ai_apps_platform/backend
pip3 install -r requirements.txt

# 启动后端
echo "启动后端服务..."
cd /Users/duanxiaofei/Desktop/ezijing_ai_apps_platform/backend
nohup python3 app.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务已启动，PID: $BACKEND_PID"

# 等待后端启动
echo "等待后端启动..."
sleep 3

# 启动前端
echo "启动前端服务..."
cd /Users/duanxiaofei/Desktop/ezijing_ai_apps_platform/frontend
nohup npm run serve > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务已启动，PID: $FRONTEND_PID"

echo "=== 优化完成 ==="
echo "服务已启动，请访问: http://localhost:8080" 