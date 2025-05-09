# 构建阶段
FROM node:16-alpine AS build-stage

# 设置工作目录
WORKDIR /app

# 设置Node环境
ENV NODE_ENV=production

# 复制package.json
COPY package.json ./
COPY package-lock.json ./

# 安装依赖，包括全局安装vue-cli-service
RUN npm install && npm install -g @vue/cli-service

# 复制所有源文件
COPY . .

# 使用vue-cli-service构建
RUN vue-cli-service build

# 生产阶段
FROM nginx:1.23-alpine

# 复制构建产物到Nginx服务目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制自定义Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"] 