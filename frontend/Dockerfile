# 构建阶段
FROM node:16-alpine as build-stage

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有源文件
COPY . .

# 构建应用
RUN npm run build

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