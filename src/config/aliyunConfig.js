// 从环境变量读取API密钥
const apiKey = process.env.DASHSCOPE_API_KEY || '';

// 输出配置信息以便调试
console.log('阿里云配置信息:');
console.log('- API密钥设置状态:', apiKey ? '已设置' : '未设置');
console.log('- API密钥来源:', process.env.DASHSCOPE_API_KEY ? '环境变量' : '未设置');

// 检查API密钥是否已设置
if (!apiKey) {
  console.error('警告: DASHSCOPE_API_KEY未设置，阿里云API将无法正常工作');
  console.error('请在.env文件中设置DASHSCOPE_API_KEY环境变量');
}

module.exports = {
  API_KEY: apiKey,
  API_ENDPOINT: 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis',
  TASK_API_ENDPOINT: 'https://dashscope.aliyuncs.com/api/v1/tasks',
  MODEL: 'wanx2.1-imageedit'
}; 