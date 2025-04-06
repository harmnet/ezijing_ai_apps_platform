// 从环境变量读取API密钥，如果未设置则使用硬编码的值（仅开发环境）
const apiKey = process.env.DASHSCOPE_API_KEY || 'sk-1f4bdb8a73ee47809ee148a977c39737';

// 输出配置信息以便调试
console.log('阿里云配置信息:');
console.log('- API密钥设置状态:', apiKey ? '已设置' : '未设置');
console.log('- API密钥来源:', process.env.DASHSCOPE_API_KEY ? '环境变量' : '默认值');

module.exports = {
  API_KEY: apiKey,
  API_ENDPOINT: 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis',
  TASK_API_ENDPOINT: 'https://dashscope.aliyuncs.com/api/v1/tasks',
  MODEL: 'wanx2.1-imageedit'
}; 