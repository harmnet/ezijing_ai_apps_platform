#!/bin/bash

# 停止并移除旧容器
echo "正在停止并移除旧容器..."
docker-compose -f docker-compose.ghcr.yml down

# 确保移除旧镜像
echo "移除旧镜像..."
docker rmi ghcr.io/harmnet/ezijing-frontend:latest || true
docker rmi ghcr.io/harmnet/ezijing-backend:latest || true
docker rmi ghcr.io/harmnet/ezijing-nodejs:latest || true

# 登录GitHub Container Registry
echo "登录GitHub Container Registry..."
echo "请输入您的GitHub用户名:"
read GITHUB_USERNAME
echo "请输入您的GitHub个人访问令牌(PAT):"
read -s GITHUB_PAT

echo "$GITHUB_PAT" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin

# 拉取最新镜像
echo "拉取最新镜像..."
docker-compose -f docker-compose.ghcr.yml pull

# 启动服务
echo "启动服务..."
docker-compose -f docker-compose.ghcr.yml up -d

# 查看运行状态
echo "服务状态:"
docker-compose -f docker-compose.ghcr.yml ps

echo "部署完成!" 