#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 设置工作目录
PROJECT_DIR="/Users/duanxiaofei/Desktop/ezijing_ai_apps_platform"
FRONTEND_DIR="$PROJECT_DIR/frontend"
BACKEND_DIR="$PROJECT_DIR/backend"
NODEJS_DIR="$PROJECT_DIR"
FRONTEND_PORT=8018
BACKEND_PORT=9000
NODEJS_PORT=3000

echo -e "${BLUE}====== 紫荆AI应用平台服务重启脚本 ======${NC}"
echo -e "${BLUE}开始时间: $(date)${NC}"
echo ""

# 释放前端端口函数
free_frontend_port() {
    echo -e "${YELLOW}检查前端端口 $FRONTEND_PORT 是否被占用...${NC}"
    VUE_PIDS=$(lsof -i :$FRONTEND_PORT -t)
    if [ -n "$VUE_PIDS" ]; then
        echo -e "发现占用前端端口的进程: $VUE_PIDS"
        for pid in $VUE_PIDS; do
            echo "终止进程 $pid"
            kill -9 $pid 2>/dev/null
        done
        echo -e "${GREEN}✓ 前端端口已释放${NC}"
    else
        echo -e "${GREEN}✓ 前端端口未被占用${NC}"
    fi
}

# 释放后端端口函数
free_backend_port() {
    echo -e "${YELLOW}检查后端端口 $BACKEND_PORT 是否被占用...${NC}"
    BACKEND_PORT_PIDS=$(lsof -i :$BACKEND_PORT -t)
    if [ -n "$BACKEND_PORT_PIDS" ]; then
        echo -e "发现占用后端端口的进程: $BACKEND_PORT_PIDS"
        for pid in $BACKEND_PORT_PIDS; do
            echo "终止进程 $pid"
            kill -9 $pid 2>/dev/null
        done
        echo -e "${GREEN}✓ 后端端口已释放${NC}"
    else
        echo -e "${GREEN}✓ 后端端口未被占用${NC}"
    fi
}

# 释放Node.js端口函数
free_nodejs_port() {
    echo -e "${YELLOW}检查Node.js端口 $NODEJS_PORT 是否被占用...${NC}"
    NODEJS_PORT_PIDS=$(lsof -i :$NODEJS_PORT -t)
    if [ -n "$NODEJS_PORT_PIDS" ]; then
        echo -e "发现占用Node.js端口的进程: $NODEJS_PORT_PIDS"
        for pid in $NODEJS_PORT_PIDS; do
            echo "终止进程 $pid"
            kill -9 $pid 2>/dev/null
        done
        echo -e "${GREEN}✓ Node.js端口已释放${NC}"
    else
        echo -e "${GREEN}✓ Node.js端口未被占用${NC}"
    fi
}

# 杀死前端Vue开发服务器
echo -e "${YELLOW}[1/6] 停止前端服务...${NC}"
free_frontend_port

# 查找并关闭现有的后端Python进程
echo -e "${YELLOW}[2/6] 停止后端服务...${NC}"
BACKEND_PIDS=$(ps -ef | grep "[p]ython.*app.py" | awk '{print $2}')
if [ -n "$BACKEND_PIDS" ]; then
    echo -e "发现正在运行的后端服务进程: $BACKEND_PIDS"
    for pid in $BACKEND_PIDS; do
        echo "终止进程 $pid"
        kill -9 $pid 2>/dev/null
    done
    echo -e "${GREEN}✓ 后端服务已停止${NC}"
else
    echo -e "${GREEN}✓ 未发现运行中的后端服务${NC}"
fi

# 释放后端端口
free_backend_port

# 查找并关闭现有的Node.js进程
echo -e "${YELLOW}[3/6] 停止Node.js服务...${NC}"
NODEJS_PIDS=$(ps -ef | grep "[n]ode.*src/app.js" | awk '{print $2}')
if [ -n "$NODEJS_PIDS" ]; then
    echo -e "发现正在运行的Node.js服务进程: $NODEJS_PIDS"
    for pid in $NODEJS_PIDS; do
        echo "终止进程 $pid"
        kill -9 $pid 2>/dev/null
    done
    echo -e "${GREEN}✓ Node.js服务已停止${NC}"
else
    echo -e "${GREEN}✓ 未发现运行中的Node.js服务${NC}"
fi

# 释放Node.js端口
free_nodejs_port

# 等待进程完全退出
sleep 1

# 启动后端服务
echo -e "${YELLOW}[4/6] 启动后端服务...${NC}"
cd "$BACKEND_DIR" || { echo -e "${RED}✗ 无法进入后端目录${NC}"; exit 1; }

# 再次确认后端端口是否可用
free_backend_port

# 检测Python命令
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ 找不到Python命令，无法启动后端服务${NC}"
    exit 1
fi

echo "使用 $PYTHON_CMD 命令启动后端服务..."
nohup $PYTHON_CMD app.py > backend.log 2>&1 &
BACKEND_PID=$!
sleep 2

# 检查后端服务是否成功启动
if ps -p $BACKEND_PID > /dev/null; then
    if lsof -i :$BACKEND_PORT -t | grep -q "$BACKEND_PID"; then
        echo -e "${GREEN}✓ 后端服务已启动，PID: $BACKEND_PID，端口: $BACKEND_PORT${NC}"
    else
        echo -e "${YELLOW}⚠ 后端服务进程存在，但未监听端口 $BACKEND_PORT${NC}"
        echo -e "${YELLOW}查看日志获取详细信息:${NC}"
        cat backend.log | tail -n 10
    fi
else
    echo -e "${RED}✗ 后端服务启动失败，请检查backend.log文件${NC}"
    cat backend.log | tail -n 20
fi

# 启动Node.js服务
echo -e "${YELLOW}[5/6] 启动Node.js服务...${NC}"
cd "$NODEJS_DIR" || { echo -e "${RED}✗ 无法进入Node.js目录${NC}"; exit 1; }

# 再次确认Node.js端口是否可用
free_nodejs_port

echo "启动Node.js服务，端口$NODEJS_PORT..."
nohup node src/app.js > nodejs.log 2>&1 &
NODEJS_PID=$!
sleep 2

# 检查Node.js服务是否成功启动
if ps -p $NODEJS_PID > /dev/null; then
    if lsof -i :$NODEJS_PORT -t | grep -q "$NODEJS_PID"; then
        echo -e "${GREEN}✓ Node.js服务已启动，PID: $NODEJS_PID，端口: $NODEJS_PORT${NC}"
    else
        echo -e "${YELLOW}⚠ Node.js服务进程存在，但未监听端口 $NODEJS_PORT${NC}"
        echo -e "${YELLOW}查看日志获取详细信息:${NC}"
        cat nodejs.log | tail -n 10
    fi
else
    echo -e "${RED}✗ Node.js服务启动失败，请检查nodejs.log文件${NC}"
    cat nodejs.log | tail -n 20
fi

# 启动前端服务
echo -e "${YELLOW}[6/6] 启动前端服务...${NC}"
cd "$FRONTEND_DIR" || { echo -e "${RED}✗ 无法进入前端目录${NC}"; exit 1; }

# 再次确认前端端口是否可用
free_frontend_port

echo "启动Vue开发服务器，端口$FRONTEND_PORT..."
nohup npm run serve > frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 5

# 检查前端服务是否正常启动
if lsof -i :$FRONTEND_PORT > /dev/null; then
    ACTUAL_PID=$(lsof -i :$FRONTEND_PORT -t)
    echo -e "${GREEN}✓ 前端服务已启动，运行在 http://localhost:$FRONTEND_PORT${NC}"
else
    echo -e "${RED}✗ 前端服务启动失败，请检查frontend.log文件${NC}"
    cat frontend.log | tail -n 20
fi

# 提示服务可访问性
echo -e "${YELLOW}[服务状态检查] 检查所有服务状态...${NC}"
echo "等待5秒检查服务状态..."
sleep 5

echo -e "${BLUE}======= 服务状态 =======${NC}"

# 检查前端服务
FRONTEND_PIDS=$(lsof -i :$FRONTEND_PORT -t)
if [ -n "$FRONTEND_PIDS" ]; then
    echo -e "前端服务: ${GREEN}http://localhost:$FRONTEND_PORT (PID: $FRONTEND_PIDS)${NC}"
else
    echo -e "前端服务: ${RED}未运行${NC}"
fi

# 检查后端服务
if ps -p $BACKEND_PID > /dev/null; then
    if lsof -i :$BACKEND_PORT -t | grep -q "$BACKEND_PID"; then
        echo -e "后端服务: ${GREEN}运行中 (PID: $BACKEND_PID, 端口: $BACKEND_PORT)${NC}"
    else
        echo -e "后端服务: ${YELLOW}进程运行中但可能未监听端口 (PID: $BACKEND_PID)${NC}"
    fi
else
    BACKEND_PORT_PIDS=$(lsof -i :$BACKEND_PORT -t)
    if [ -n "$BACKEND_PORT_PIDS" ]; then
        echo -e "后端服务: ${YELLOW}端口被其他进程占用 (PID: $BACKEND_PORT_PIDS)${NC}"
    else
        echo -e "后端服务: ${RED}未运行${NC}"
    fi
fi

# 检查Node.js服务
if ps -p $NODEJS_PID > /dev/null; then
    if lsof -i :$NODEJS_PORT -t | grep -q "$NODEJS_PID"; then
        echo -e "Node.js服务: ${GREEN}运行中 (PID: $NODEJS_PID, 端口: $NODEJS_PORT)${NC}"
    else
        echo -e "Node.js服务: ${YELLOW}进程运行中但可能未监听端口 (PID: $NODEJS_PID)${NC}"
    fi
else
    NODEJS_PORT_PIDS=$(lsof -i :$NODEJS_PORT -t)
    if [ -n "$NODEJS_PORT_PIDS" ]; then
        echo -e "Node.js服务: ${YELLOW}端口被其他进程占用 (PID: $NODEJS_PORT_PIDS)${NC}"
    else
        echo -e "Node.js服务: ${RED}未运行${NC}"
    fi
fi

echo -e "${BLUE}=========================${NC}"
echo -e "${GREEN}重启完成！${NC}"
echo -e "${YELLOW}如需停止所有服务，请运行: ./restart.sh stop${NC}"

# 如果有stop参数，只停止服务
if [ "$1" = "stop" ]; then
    echo -e "${RED}停止所有服务${NC}"
    
    # 杀死前端服务
    VUE_PIDS=$(lsof -i :$FRONTEND_PORT -t)
    if [ -n "$VUE_PIDS" ]; then
        echo "停止前端服务 ($VUE_PIDS)..."
        for pid in $VUE_PIDS; do
            kill -9 $pid 2>/dev/null
        done
    fi
    
    # 杀死后端服务
    BACKEND_PIDS=$(ps -ef | grep "[p]ython.*app.py" | awk '{print $2}')
    if [ -n "$BACKEND_PIDS" ]; then
        echo "停止后端服务 ($BACKEND_PIDS)..."
        for pid in $BACKEND_PIDS; do
            kill -9 $pid 2>/dev/null
        done
    fi
    
    # 杀死Node.js服务
    NODEJS_PIDS=$(ps -ef | grep "[n]ode.*src/app.js" | awk '{print $2}')
    if [ -n "$NODEJS_PIDS" ]; then
        echo "停止Node.js服务 ($NODEJS_PIDS)..."
        for pid in $NODEJS_PIDS; do
            kill -9 $pid 2>/dev/null
        done
    fi
    
    # 确保端口已释放
    BACKEND_PORT_PIDS=$(lsof -i :$BACKEND_PORT -t)
    if [ -n "$BACKEND_PORT_PIDS" ]; then
        echo "终止占用后端端口的其他进程 ($BACKEND_PORT_PIDS)..."
        for pid in $BACKEND_PORT_PIDS; do
            kill -9 $pid 2>/dev/null
        done
    fi
    
    # 确保Node.js端口已释放
    NODEJS_PORT_PIDS=$(lsof -i :$NODEJS_PORT -t)
    if [ -n "$NODEJS_PORT_PIDS" ]; then
        echo "终止占用Node.js端口的其他进程 ($NODEJS_PORT_PIDS)..."
        for pid in $NODEJS_PORT_PIDS; do
            kill -9 $pid 2>/dev/null
        done
    fi
    
    echo -e "${GREEN}所有服务已停止${NC}"
    exit 0
fi 