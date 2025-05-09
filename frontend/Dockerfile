# 构建阶段
FROM node:16-alpine AS build-stage

# 设置工作目录
WORKDIR /app

# 设置Node环境变量
ENV NODE_ENV=production
ENV PATH /app/node_modules/.bin:$PATH

# 先复制package.json和package-lock.json
COPY package.json ./
COPY package-lock.json ./

# 安装依赖
RUN npm install

# 复制所有源文件
COPY . .

# 列出文件确认
RUN ls -la

# 显示vue.config.js内容
RUN cat vue.config.js

# 使用npm run build构建
RUN npm run build

# 检查构建结果
RUN ls -la dist || echo "dist目录不存在"

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