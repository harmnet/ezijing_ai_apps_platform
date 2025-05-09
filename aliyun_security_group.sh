#!/bin/bash

# 此脚本用于配置阿里云安全组规则
# 注意：执行前请先安装阿里云CLI并配置访问凭证

# 获取安全组ID
# 替换 REGION_ID 为您的区域ID，如 cn-beijing
REGION_ID="cn-beijing"

echo "1. 获取当前ECS实例的安全组ID..."
INSTANCE_ID=$(aliyun ecs DescribeInstances --RegionId ${REGION_ID} --PageSize 10 | grep -A 3 "123.57.71.66" | grep "InstanceId" | awk -F'"' '{print $4}')

if [ -z "$INSTANCE_ID" ]; then
    echo "未找到IP为123.57.71.66的实例，请检查区域设置"
    exit 1
fi

echo "找到实例ID: $INSTANCE_ID"

# 获取安全组ID
SECURITY_GROUP_ID=$(aliyun ecs DescribeInstanceAttribute --InstanceId ${INSTANCE_ID} --RegionId ${REGION_ID} | grep -A 3 "SecurityGroupIds" | grep "SecurityGroupId" | head -1 | awk -F'"' '{print $4}')

if [ -z "$SECURITY_GROUP_ID" ]; then
    echo "未找到安全组ID，请手动检查"
    exit 1
fi

echo "找到安全组ID: $SECURITY_GROUP_ID"

# 添加80端口入站规则
echo "2. 添加80端口(HTTP)入站规则..."
aliyun ecs AuthorizeSecurityGroup --RegionId ${REGION_ID} \
    --SecurityGroupId ${SECURITY_GROUP_ID} \
    --IpProtocol tcp \
    --PortRange 80/80 \
    --SourceCidrIp 0.0.0.0/0 \
    --Priority 1

# 添加443端口入站规则
echo "3. 添加443端口(HTTPS)入站规则..."
aliyun ecs AuthorizeSecurityGroup --RegionId ${REGION_ID} \
    --SecurityGroupId ${SECURITY_GROUP_ID} \
    --IpProtocol tcp \
    --PortRange 443/443 \
    --SourceCidrIp 0.0.0.0/0 \
    --Priority 1

echo "安全组规则添加完成"
echo "请等待几分钟后再测试连接" 