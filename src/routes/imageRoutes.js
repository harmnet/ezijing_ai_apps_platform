const express = require('express');
const imageController = require('../controllers/imageController');
const uploadController = require('../controllers/uploadController');

const router = express.Router();

// 获取支持的功能列表
router.get('/functions', imageController.getSupportedFunctions);

// 上传图片
router.post('/upload', uploadController.uploadImage);

// 创建风格转换任务
router.post('/style-transfer', imageController.createStyleTransfer);

// 查询任务状态
router.get('/tasks/:taskId', imageController.checkTaskStatus);

module.exports = router; 