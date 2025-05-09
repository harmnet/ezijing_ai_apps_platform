#!/bin/bash

# 部署本地打包的Docker镜像到服务器
# 使用方法: ./deploy-local-images.sh [服务器IP] [用户名]

# 默认值
SERVER_IP=${1:-"123.57.71.66"}
SERVER_USER=${2:-"root"}

# 确认参数
echo "将要部署到服务器: $SERVER_USER@$SERVER_IP"
read -p "是否继续? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
  echo "部署已取消"
  exit 0
fi

# 检查本地Docker镜像tar包是否存在
for IMAGE in frontend.tar.gz backend.tar.gz nodejs.tar.gz; do
  if [ ! -f "$IMAGE" ]; then
    echo "错误: $IMAGE 不存在!"
    exit 1
  fi
done

# 创建部署目录
echo "在服务器上创建部署目录..."
ssh $SERVER_USER@$SERVER_IP "mkdir -p /opt/ezijing"

# 复制docker-compose配置和部署脚本
echo "复制docker-compose配置和部署脚本..."
scp docker-compose.ghcr.yml deploy-ghcr.sh $SERVER_USER@$SERVER_IP:/opt/ezijing/

# 复制Docker镜像tar包
echo "复制Docker镜像tar包到服务器..."
scp frontend.tar.gz backend.tar.gz nodejs.tar.gz $SERVER_USER@$SERVER_IP:/opt/ezijing/

# 在服务器上加载镜像并启动服务
echo "在服务器上加载镜像并启动服务..."
ssh $SERVER_USER@$SERVER_IP << EOF
cd /opt/ezijing
echo "加载前端镜像..."
docker load < frontend.tar.gz
echo "加载后端镜像..."
docker load < backend.tar.gz
echo "加载Node.js镜像..."
docker load < nodejs.tar.gz

# 修改docker-compose配置使用本地镜像
sed -i 's/ghcr.io\/harmnet//' docker-compose.ghcr.yml

# 启动服务
docker-compose -f docker-compose.ghcr.yml down
docker-compose -f docker-compose.ghcr.yml up -d

# 查看运行状态
docker-compose -f docker-compose.ghcr.yml ps
EOF

echo "部署完成!"
echo "前端访问: http://$SERVER_IP:8018"
echo "后端访问: http://$SERVER_IP:9000"
echo "Node.js访问: http://$SERVER_IP:3000" 