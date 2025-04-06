import axios from 'axios';
import { ElMessage } from 'element-plus';

// 创建axios实例
const service = axios.create({
  // API的base_url
  baseURL: process.env.VUE_APP_BASE_API || '/api',
  // 请求超时时间
  timeout: 15000
});

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    // 例如添加token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    // 处理请求错误
    console.error('请求发送失败:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data;
    
    // 如果响应码不是0，则认为请求有错误
    if (res.code !== 0) {
      ElMessage({
        message: res.message || '请求失败，请稍后重试',
        type: 'error',
        duration: 5 * 1000
      });
      
      // 根据特定响应码处理特殊情况
      if (res.code === 401) {
        // 未授权，可能需要重新登录
        ElMessage({
          message: '登录状态已失效，请重新登录',
          type: 'error',
          duration: 5 * 1000
        });
        
        // 可以在这里处理登出逻辑
        // store.dispatch('user/logout');
      }
      
      return Promise.reject(new Error(res.message || '未知错误'));
    } else {
      return res;
    }
  },
  error => {
    console.error('请求响应错误:', error);
    let message = '';
    
    if (error.response) {
      // 服务器返回了错误状态码
      switch (error.response.status) {
        case 400:
          message = '请求参数错误';
          break;
        case 401:
          message = '未授权，请重新登录';
          // 可以在这里处理登出逻辑
          // store.dispatch('user/logout');
          break;
        case 403:
          message = '拒绝访问';
          break;
        case 404:
          message = '请求的资源不存在';
          break;
        case 500:
          message = '服务器内部错误';
          break;
        default:
          message = `未知错误: ${error.response.status}`;
      }
    } else if (error.request) {
      // 请求已发出，但未收到响应
      message = '服务器无响应';
    } else {
      // 在设置请求时发生错误
      message = '请求配置错误';
    }
    
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    });
    
    return Promise.reject(error);
  }
);

// 数字人API相关请求方法
export const aiBeingApi = {
  // 获取数字人列表
  getAIBeings(params) {
    return service({
      url: '/v1/aibeings/aibeings',
      method: 'get',
      params
    });
  },
  
  // 获取数字人详情
  getAIBeingById(id) {
    return service({
      url: `/v1/aibeings/aibeings/${id}`,
      method: 'get'
    });
  },
  
  // 创建数字人
  createAIBeing(data) {
    return service({
      url: '/v1/aibeings/aibeings',
      method: 'post',
      data
    });
  },
  
  // 更新数字人
  updateAIBeing(id, data) {
    return service({
      url: `/v1/aibeings/aibeings/${id}`,
      method: 'put',
      data
    });
  },
  
  // 删除数字人
  deleteAIBeing(id) {
    return service({
      url: `/v1/aibeings/aibeings/${id}`,
      method: 'delete'
    });
  }
};

export default service; 