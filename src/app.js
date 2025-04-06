const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');
const imageRoutes = require('./routes/imageRoutes');

// 加载环境变量并调试输出
dotenv.config();
console.log('环境变量检查:');
console.log('- DASHSCOPE_API_KEY存在:', process.env.DASHSCOPE_API_KEY ? '是' : '否');
console.log('- API密钥前6位:', process.env.DASHSCOPE_API_KEY ? process.env.DASHSCOPE_API_KEY.substring(0, 6) + '...' : '未设置');
console.log('- PORT:', process.env.PORT || '未设置');

const app = express();
const PORT = process.env.PORT || 3000;

// 创建上传目录
const uploadDir = path.join(__dirname, '../uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件服务
app.use('/uploads', express.static(uploadDir));
app.use(express.static(path.join(__dirname, '../public')));

// 路由
app.use('/api/images', imageRoutes);

// 基础路由
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error('服务器错误:', err);
  res.status(500).json({
    success: false,
    error: '服务器内部错误'
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器运行在端口: ${PORT}`);
  console.log(`访问 http://localhost:${PORT} 使用图片风格转换服务`);
});

module.exports = app; 