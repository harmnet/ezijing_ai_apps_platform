# 图片风格转换服务

基于阿里云通义万相通用图像编辑API实现的图片风格转换服务，支持多种图像处理功能。

## 功能特点

- **图像风格化**：全局风格化、局部风格化
- **图像内容编辑**：局部重绘、去文字水印（中英文）
- **图像尺寸与分辨率优化**：扩图、图像超分（高清放大）
- **图像色彩处理**：图像上色（黑白或灰度图像转为彩色图像）
- **基于参考图像生成**：线稿生图、垫图

## 安装和运行

### 前提条件

- Node.js (v14+)
- 阿里云通义万相API Key

### 安装依赖

```bash
npm install
```

### 配置环境变量

创建 `.env` 文件，添加以下内容：

```
DASHSCOPE_API_KEY=your_api_key_here
PORT=3000
```

替换 `your_api_key_here` 为你的阿里云通义万相API Key。

### 启动服务

```bash
npm start
```

或者开发模式启动：

```bash
npm run dev
```

服务将在 http://localhost:3000 上运行。

## API 接口说明

### 1. 获取支持的功能列表

```
GET /api/images/functions
```

返回支持的所有图像处理功能。

### 2. 上传图片

```
POST /api/images/upload
```

上传一张图片，表单字段名为 `image`。

### 3. 创建风格转换任务

```
POST /api/images/style-transfer
```

请求体：

```json
{
  "imageUrl": "图片URL",
  "prompt": "提示词", 
  "functionType": "处理功能类型"
}
```

返回任务ID，用于查询任务状态。

### 4. 查询任务状态

```
GET /api/images/tasks/:taskId
```

查询指定任务ID的处理状态和结果。

## 前端界面

访问 http://localhost:3000 使用内置的前端界面，可进行图片上传、选择处理功能和查看处理结果。

## 技术栈

- Node.js
- Express
- 阿里云通义万相API

## 注意事项

- API Key 不要泄露
- 阿里云通义万相API有使用限制和计费规则，详见官方文档
- 处理结果图片的OSS链接仅在24小时内有效 