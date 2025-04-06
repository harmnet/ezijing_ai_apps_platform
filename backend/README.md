## 紫荆AI平台后端服务

### 服务启动与停止

**重要说明：使用restart.sh脚本启动或停止服务**

- 启动所有服务: `./restart.sh`
- 停止所有服务: `./restart.sh stop`

脚本会自动:
1. 停止所有已运行的服务
2. 释放被占用的端口
3. 启动后端服务、Node.js服务和前端服务
4. 检查服务状态

### API接口列表

#### 阿里云图片风格调整API

1. 创建风格调整任务
   - 请求: `POST /api/v1/image_style/create`
   - 参数:
     ```json
     {
       "prompt": "转换成法国绘本风格",
       "image_url": "http://example.com/image.jpg",
       "n": 1,
       "seed": 12345,  // 可选
       "watermark": false  // 可选
     }
     ```
   - 返回:
     ```json
     {
       "success": true,
       "data": {
         "task_id": "52e066c7-7541-4004-a390-dfbce0ce7820",
         "task_status": "PENDING",
         "request_id": "0e7ea759-2078-962b-afa9-6def3e7df113"
       }
     }
     ```

2. 查询任务状态
   - 请求: `GET /api/v1/image_style/query/{task_id}`
   - 返回(执行中):
     ```json
     {
       "success": true,
       "data": {
         "task_id": "52e066c7-7541-4004-a390-dfbce0ce7820",
         "task_status": "RUNNING",
         "request_id": "3c4873f3-8f62-9a06-be08-2593972601c7"
       }
     }
     ```
   - 返回(完成):
     ```json
     {
       "success": true,
       "data": {
         "task_id": "52e066c7-7541-4004-a390-dfbce0ce7820",
         "task_status": "SUCCEEDED",
         "request_id": "136676ad-c49d-9820-90b9-9364b1d1f0f2",
         "image_urls": ["https://example.com/result.png"],
         "submit_time": "2025-04-03 22:00:19.554",
         "end_time": "2025-04-03 22:00:53.004"
       }
     }
     ```

3. 获取API信息
   - 请求: `GET /api/v1/image_style/info`
   - 返回:
     ```json
     {
       "success": true,
       "data": {
         "name": "阿里云图片风格调整API",
         "description": "使用阿里云百炼DashScope API进行图片风格化调整",
         "model_version": "wanx2.1-imageedit",
         "features": [
           "支持全局风格化调整",
           "支持多种风格提示词",
           "支持多张结果生成",
           "支持异步任务处理"
         ]
       }
     }
     ``` 