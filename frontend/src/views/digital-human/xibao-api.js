// 小冰API调用封装

import axios from 'axios';

// 小冰API官方域名
const baseURL = 'https://openapi.xiaoice.com';
// 小冰API路径前缀
const API_PATH_PREFIX = '/vh';

// 数字人接口密钥
const SUB_KEY = '282cd94b697e48e6aca6d20bbdaf0d0f';

// 尝试不同格式的认证头
const AUTH_HEADER = {
  'subscription-key': SUB_KEY,  // 尝试使用小写格式认证头
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};

// 认证密钥仅在URL参数中使用
const AUTH_PARAMS = {
  'subscription-key': SUB_KEY
};

// 创建axios实例，使用请求头传递subscription-key
const apiClient = axios.create({
  baseURL,
  timeout: 60000, // 60秒超时
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'subscription-key': SUB_KEY  // 在请求头中添加subscription-key
  }
});

// 添加请求拦截器
apiClient.interceptors.request.use(config => {
  console.log('发送请求:', config.url, config.data);
  return config;
}, error => {
  console.error('请求错误:', error);
  return Promise.reject(error);
});

// 添加响应拦截器
apiClient.interceptors.response.use(response => {
  console.log('收到响应:', response.data);
  return response;
}, error => {
  if (error.response) {
    // 服务器返回了错误状态码
    console.error('响应错误:', error.response.status, error.response.data);
  } else if (error.request) {
    // 请求已发送但未收到响应
    console.error('请求未收到响应:', error.request);
  } else {
    // 请求设置时出错
    console.error('请求设置错误:', error.message);
  }
  return Promise.reject(error);
});

/**
 * 创建PPT讲解视频生成任务
 * @param {Object} data - 请求参数
 * @returns {Promise} - 返回创建任务的响应
 */
export const createPptVideoTask = async (data) => {
  try {
    console.log('创建PPT讲解视频任务, 请求参数:', data);
    console.log('请求头信息:', AUTH_HEADER);
    console.log('完整请求URL:', `${baseURL}${API_PATH_PREFIX}/video/task/v2/ppt/submit`);
    
    // 直接用axios发送请求，确保带有正确的认证头
    const response = await axios({
      method: 'post',
      url: `${baseURL}${API_PATH_PREFIX}/video/task/v2/ppt/submit`,
      headers: AUTH_HEADER,
      data: data,
      timeout: 60000
    });
    
    console.log('创建任务响应状态:', response.status);
    console.log('创建任务响应数据:', response.data);
    
    return response.data;
  } catch (error) {
    console.error('创建PPT讲解视频任务失败:', error);
    throw error;
  }
};

/**
 * 查询任务状态
 * @param {String} taskId - 任务ID
 * @returns {Promise} - 返回任务状态的响应
 */
export const getTaskStatus = async (taskId) => {
  try {
    console.log('查询任务状态, 任务ID:', taskId);
    console.log('请求头信息:', AUTH_HEADER);
    console.log('完整请求URL:', `${baseURL}${API_PATH_PREFIX}/video/task/status`);
    
    // 直接用axios发送请求
    const response = await axios({
      method: 'get',
      url: `${baseURL}${API_PATH_PREFIX}/video/task/status`,
      headers: AUTH_HEADER,
      params: { taskId }
    });
    
    console.log('查询任务状态响应:', response.data);
    
    return response.data;
  } catch (error) {
    console.error('查询任务状态失败:', error);
    throw error;
  }
};

/**
 * 测试API连接
 * @returns {Promise} - 返回测试结果
 */
export const testApiConnection = async () => {
  try {
    console.log('====== 测试小冰API连接(多种方法尝试) ======');
    
    // 方法1: 使用原生fetch API
    try {
      console.log('方法1: 使用原生fetch API');
      console.log('请求头信息:', AUTH_HEADER);
      console.log('完整请求URL:', `${baseURL}${API_PATH_PREFIX}/video/task/status`);
      const fetchResponse = await fetch(`${baseURL}${API_PATH_PREFIX}/video/task/status`, {
        method: 'GET',
        headers: AUTH_HEADER
      });
      const jsonResponse = await fetchResponse.json();
      console.log('方法1响应:', jsonResponse);
    } catch (error) {
      console.error('方法1错误:', error);
    }
    
    // 方法2: 使用axios实例
    try {
      console.log('方法2: 使用axios实例');
      console.log('请求头信息:', apiClient.defaults.headers);
      console.log('完整请求URL:', `${baseURL}${API_PATH_PREFIX}/video/task/status`);
      const axiosResponse = await apiClient.get(`${API_PATH_PREFIX}/video/task/status`);
      console.log('方法2响应:', axiosResponse.data);
    } catch (error) {
      console.error('方法2错误:', error);
    }
    
    // 方法3: 使用axios全局配置
    try {
      console.log('方法3: 使用axios全局配置');
      console.log('请求头信息:', AUTH_HEADER);
      console.log('完整请求URL:', `${baseURL}${API_PATH_PREFIX}/video/task/status`);
      const axiosResponse = await axios.get(`${baseURL}${API_PATH_PREFIX}/video/task/status`, {
        headers: AUTH_HEADER
      });
      console.log('方法3响应:', axiosResponse.data);
    } catch (error) {
      console.error('方法3错误:', error);
    }
  } catch (error) {
    console.error('测试小冰API连接失败:', error);
    throw error;
  }
};

// 添加以下导出语句
// 导出常量
export { baseURL, API_PATH_PREFIX, SUB_KEY, AUTH_HEADER };

// 导出所有方法
export default {
  baseURL,
  API_PATH_PREFIX,
  SUB_KEY,
  AUTH_HEADER,
  createPptVideoTask,
  getTaskStatus,
  testApiConnection
};