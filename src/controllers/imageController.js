const { createStyleTransferTask, getTaskStatus: queryTaskStatus } = require('../services/aliyunService');

// 安全的substring函数
function safeSubstring(str, start, end) {
  if (!str || typeof str !== 'string') return '未提供';
  return str.substring(0, Math.min(str.length, end)) + '...';
}

/**
 * 创建风格转换任务
 * @param {Object} req - 请求对象
 * @param {Object} res - 响应对象
 */
async function createStyleTransfer(req, res) {
  try {
    const { imageUrl, prompt, functionType } = req.body;
    console.log('收到风格转换请求:', {
      imageUrl: imageUrl ? safeSubstring(imageUrl, 0, 30) : '未提供',
      prompt: prompt || '未提供',
      functionType: functionType || 'stylization_all'
    });

    // 验证必要参数
    if (!imageUrl) {
      return res.status(400).json({ 
        success: false,
        error: '缺少图片URL参数' 
      });
    }
    if (!prompt) {
      return res.status(400).json({ 
        success: false,
        error: '缺少提示词参数' 
      });
    }

    // 使用try-catch包装API调用，避免未处理的异常
    try {
      console.log('准备调用阿里云API...');
      // 调用阿里云服务创建任务
      const taskResult = await createStyleTransferTask(imageUrl, prompt, functionType || 'stylization_all');
      console.log('API调用成功，返回数据:', JSON.stringify(taskResult));
      
      // 输出完整的响应内容用于调试
      console.log('完整响应内容:', JSON.stringify(taskResult));
      
      if (!taskResult) {
        console.error('API返回为空');
        return res.status(500).json({
          success: false,
          error: 'API返回为空'
        });
      }
      
      // 检查是否是我们处理过的特殊错误
      if (taskResult.error_handled) {
        console.log('接收到已处理的错误响应，继续处理任务ID');
      }
      
      // 检查API响应格式，支持不同的返回格式
      // 1. 顶层的task_id或taskId
      // 2. 嵌套在output内部的task_id或task_status
      let taskId = null;
      
      // 输出全部字段名，帮助调试
      console.log('任务结果字段:', Object.keys(taskResult));
      if (taskResult.output) {
        console.log('output字段内容:', taskResult.output);
        console.log('output字段内的键:', Object.keys(taskResult.output));
      }
      
      if (taskResult.task_id) {
        taskId = taskResult.task_id;
        console.log('从顶层task_id字段获取任务ID:', taskId);
      } else if (taskResult.taskId) {
        taskId = taskResult.taskId;
        console.log('从顶层taskId字段获取任务ID:', taskId);
      } else if (taskResult.output && taskResult.output.task_id) {
        taskId = taskResult.output.task_id;
        console.log('从output.task_id字段获取任务ID:', taskId);
      } else if (taskResult.output && taskResult.output.taskId) {
        taskId = taskResult.output.taskId;
        console.log('从output.taskId字段获取任务ID:', taskId);
      } else if (taskResult.request_id) {
        // 某些API可能使用request_id作为任务跟踪ID
        taskId = taskResult.request_id;
        console.log('使用request_id作为任务ID:', taskId);
      }
      
      if (!taskId) {
        console.error('API返回异常结果，无法提取任务ID:', JSON.stringify(taskResult));
        
        // 尝试从整个返回体中搜索任务ID的模式
        const jsonStr = JSON.stringify(taskResult);
        const taskIdMatch = jsonStr.match(/"task_id":"([^"]+)"/);
        
        if (taskIdMatch && taskIdMatch[1]) {
          taskId = taskIdMatch[1];
          console.log('通过正则表达式从JSON字符串中提取任务ID:', taskId);
        } else {
          return res.status(500).json({
            success: false,
            error: 'API返回异常结果，缺少任务ID'
          });
        }
      }
      
      console.log('风格转换任务创建成功, 任务ID:', taskId);
      res.json({
        success: true,
        taskId: taskId,
        message: '风格转换任务已创建，请使用任务ID查询结果'
      });
    } catch (apiError) {
      console.error('阿里云API调用失败:', apiError);
      
      // 检查是否有request_id可用作任务ID
      if (apiError.response && apiError.response.data && apiError.response.data.request_id) {
        const taskId = apiError.response.data.request_id;
        console.log('从错误响应中提取request_id作为任务ID:', taskId);
        
        // 即使出错，也返回任务ID给前端，允许进行任务状态查询
        return res.json({
          success: true,
          taskId: taskId,
          warning: '任务创建可能有问题，但已返回临时任务ID',
          message: '风格转换任务已创建，请使用任务ID查询结果'
        });
      }
      
      return res.status(500).json({
        success: false,
        error: `阿里云API调用失败: ${apiError.message || '未知错误'}`
      });
    }
  } catch (error) {
    console.error('风格转换任务创建失败:', error);
    res.status(500).json({
      success: false,
      error: error.message || '风格转换任务创建失败'
    });
  }
}

/**
 * 查询任务结果
 * @param {Object} req - 请求对象
 * @param {Object} res - 响应对象
 */
async function checkTaskStatus(req, res) {
  try {
    const { taskId } = req.params;
    if (!taskId) {
      return res.status(400).json({
        success: false,
        error: '缺少任务ID参数'
      });
    }

    console.log('准备查询任务状态:', taskId);
    // 调用阿里云API查询任务状态
    const taskResult = await queryTaskStatus(taskId);
    
    // 输出完整的响应内容用于调试
    console.log('任务状态查询结果:', JSON.stringify(taskResult));
    console.log('任务结果对象的字段:', Object.keys(taskResult));
    
    if (taskResult.output) {
      console.log('output字段内容:', JSON.stringify(taskResult.output));
    }

    // 检查是否是我们处理过的错误
    if (taskResult.error_handled) {
      console.log('接收到已处理的错误响应');
      
      // 如果是NOT_FOUND错误，返回特定的状态
      if (taskResult.output && taskResult.output.task_status === 'NOT_FOUND') {
        return res.status(404).json({
          success: false,
          taskId,
          status: 'NOT_FOUND',
          error: '任务ID不存在或已过期',
          isCompleted: false
        });
      }
      
      // 如果是ACCESS_DENIED错误，返回特定的状态
      if (taskResult.output && taskResult.output.task_status === 'ACCESS_DENIED') {
        return res.status(403).json({
          success: false,
          taskId,
          status: 'ACCESS_DENIED',
          error: '无权访问该任务',
          isCompleted: false
        });
      }
    }

    // 检查任务状态
    let status = 'UNKNOWN'; // 默认状态
    let resultUrl = '';
    let isCompleted = false;
    let errorMessage = '';
    let errorCode = '';

    // 支持多种返回格式
    if (taskResult.output) {
      // 安全地提取状态，提供默认值
      status = taskResult.output.task_status || taskResult.output.status || 'UNKNOWN';
      
      console.log('检测到的任务状态:', status);
      
      // 处理UNKNOWN状态
      if (status === 'UNKNOWN') {
        console.log('任务状态为UNKNOWN，可能任务还未启动或状态未知');
        errorMessage = '任务状态未知，请稍后再试';
      }
      
      // 处理FAILED状态
      if (status === 'FAILED' || status === 'ERROR') {
        errorCode = taskResult.output.code || '';
        errorMessage = taskResult.output.message || taskResult.output.error || '任务处理失败';
        console.log(`任务失败，错误码: ${errorCode}, 错误信息: ${errorMessage}`);
      }
      
      // 首先检查标准的results数组格式
      if (taskResult.output.results && taskResult.output.results.length > 0) {
        // 遍历results数组，找到包含url的对象
        for (const result of taskResult.output.results) {
          if (result.url) {
            resultUrl = result.url;
            isCompleted = status === 'SUCCEEDED';
            console.log('从output.results[i].url获取结果URL:', resultUrl);
            break;
          }
        }
      }
      // 检查是否有图像结果
      else if (taskResult.output.images && taskResult.output.images.length > 0) {
        resultUrl = taskResult.output.images[0];
        isCompleted = status === 'SUCCEEDED';
        console.log('从output.images获取结果URL:', resultUrl);
      }
      // 有些API返回格式可能不同
      else if (taskResult.output.url) {
        resultUrl = taskResult.output.url;
        isCompleted = status === 'SUCCEEDED';
        console.log('从output.url获取结果URL:', resultUrl);
      }
    } else if (taskResult.task_status) {
      // 直接在顶层包含状态
      status = taskResult.task_status;
      console.log('从顶层task_status获取状态:', status);
      
      if (taskResult.images && taskResult.images.length > 0) {
        resultUrl = taskResult.images[0];
        isCompleted = status === 'SUCCEEDED';
        console.log('从顶层images获取结果URL:', resultUrl);
      }
      
      if (!resultUrl && taskResult.url) {
        resultUrl = taskResult.url;
        isCompleted = status === 'SUCCEEDED';
        console.log('从顶层url获取结果URL:', resultUrl);
      }
    } else if (taskResult.status) {
      // 另一种可能的格式
      status = taskResult.status;
      console.log('从顶层status获取状态:', status);
      
      if (taskResult.result && taskResult.result.url) {
        resultUrl = taskResult.result.url;
        isCompleted = status === 'SUCCEEDED' || status === 'DONE';
        console.log('从result.url获取结果URL:', resultUrl);
      }
    }
    
    // 如果状态表明成功但没有URL，可能需要进一步处理
    if ((status === 'SUCCEEDED' || status === 'DONE') && !resultUrl) {
      console.log('任务显示成功但没有找到结果URL，尝试从其他字段获取');
      // 尝试从整个对象中搜索可能的URL
      const jsonStr = JSON.stringify(taskResult);
      const urlMatch = jsonStr.match(/"url":"(https?:\/\/[^"]+\.(jpg|jpeg|png|gif))"/i);
      if (urlMatch) {
        resultUrl = urlMatch[1];
        isCompleted = true;
        console.log('从JSON字符串中提取URL:', resultUrl);
      }
    }
    
    // 任务指标和进度信息
    let taskMetrics = null;
    if (taskResult.output && taskResult.output.task_metrics) {
      taskMetrics = taskResult.output.task_metrics;
      console.log('任务指标:', JSON.stringify(taskMetrics));
    }
    
    // 模拟进度信息，提供更好的用户体验
    let progress = 0;
    
    // 基于任务指标计算进度
    if (taskMetrics) {
      const total = taskMetrics.TOTAL || 1;
      const succeeded = taskMetrics.SUCCEEDED || 0;
      const failed = taskMetrics.FAILED || 0;
      
      // 计算已处理的任务百分比
      const processed = succeeded + failed;
      progress = Math.floor((processed / total) * 100);
      console.log(`根据任务指标计算进度: ${progress}%`);
    }
    // 否则使用状态模拟进度
    else if (status === 'PENDING' || status === 'UNKNOWN') {
      // 随机生成10%-30%的进度
      progress = Math.floor(Math.random() * 20) + 10;
    } else if (status === 'RUNNING') {
      // 随机生成60%-90%的进度
      progress = Math.floor(Math.random() * 30) + 60;
    } else if (status === 'SUCCEEDED' || status === 'DONE') {
      progress = 100;
    }

    // 提取时间信息
    const submitTime = taskResult.output ? taskResult.output.submit_time : null;
    const scheduledTime = taskResult.output ? taskResult.output.scheduled_time : null;
    const endTime = taskResult.output ? taskResult.output.end_time : null;
    
    // 检查任务是否已经超时
    let isTimeout = false;
    if (submitTime) {
      const submitDate = new Date(submitTime);
      const currentDate = new Date();
      const diffMinutes = (currentDate - submitDate) / (1000 * 60);
      
      // 如果任务提交时间超过5分钟且状态仍是UNKNOWN或PENDING
      if (diffMinutes > 5 && (status === 'UNKNOWN' || status === 'PENDING')) {
        isTimeout = true;
        console.log(`任务已等待${diffMinutes.toFixed(2)}分钟，视为超时`);
        status = 'TIMEOUT';
        errorMessage = '任务处理超时，请重试';
      }
    }

    // 返回任务状态
    res.json({
      success: true,
      taskId,
      status,
      resultUrl,
      isCompleted,
      progress,
      errorMessage,
      errorCode,
      submitTime,
      scheduledTime,
      endTime,
      isTimeout,
      taskMetrics,
      rawResponse: taskResult // 返回原始响应以便前端调试
    });
  } catch (error) {
    console.error('检查任务状态失败:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}

/**
 * 获取支持的风格转换功能列表
 * @param {Object} req - 请求对象
 * @param {Object} res - 响应对象
 */
function getSupportedFunctions(req, res) {
  const functions = [
    { 
      id: 'stylization_all', 
      name: '全局风格化',
      description: '将整个图像转换为特定风格'
    },
    { 
      id: 'stylization_local', 
      name: '局部风格化',
      description: '将图像的特定部分转换为特定风格'
    },
    { 
      id: 'description_edit_with_mask', 
      name: '局部重绘',
      description: '在指定区域增加/删除/修改图片内容'
    },
    { 
      id: 'description_edit', 
      name: '去文字水印',
      description: '去除图像中的文字水印（中英文）'
    },
    { 
      id: 'outpainting', 
      name: '扩图',
      description: '按比例扩大图像'
    },
    { 
      id: 'super_resolution', 
      name: '图像超分',
      description: '提高图像分辨率和清晰度'
    },
    { 
      id: 'colorization', 
      name: '图像上色',
      description: '将黑白或灰度图像转为彩色图像'
    },
    { 
      id: 'sketchguided', 
      name: '线稿生图',
      description: '先提取输入图像的线稿，再参考线稿生成图像'
    },
    { 
      id: 'inpainting', 
      name: '垫图',
      description: '参考卡通形象生成图像'
    }
  ];

  res.json({
    success: true,
    functions
  });
}

module.exports = {
  createStyleTransfer,
  checkTaskStatus,
  getSupportedFunctions
}; 