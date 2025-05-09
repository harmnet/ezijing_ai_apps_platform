import axios from 'axios';
import { uploadImageToBos } from './bosDirectUpload';

const baseURL = '/api/v1';

/**
 * 百度数字人视频合成服务API
 */
const digitalHumanAPI = {
  /**
   * 提交百度数字人视频合成任务
   * @param {Object} params - 任务参数
   * @returns {Promise} - axios请求Promise
   */
  submitVideoTask(params) {
    return axios.post(`${baseURL}/digital_human/video/advanced/submit`, params);
  },
  
  /**
   * 提交基础数字人视频任务
   * @param {Object} params - 任务参数
   * @returns {Promise} - axios请求Promise
   */
  submitBasicVideoTask(params) {
    return axios.post(`${baseURL}/digital_human/video/submit`, params);
  },
  
  /**
   * 查询百度数字人视频合成任务状态
   * @param {string} taskId - 任务ID
   * @returns {Promise} - axios请求Promise
   */
  queryVideoTask(taskId) {
    return axios.get(`${baseURL}/digital_human/video/advanced/query`, {
      params: { taskId }
    });
  },
  
  /**
   * 查询基础数字人视频任务状态
   * @param {string} taskId - 任务ID
   * @returns {Promise} - axios请求Promise
   */
  queryBasicVideoTask(taskId) {
    return axios.get(`${baseURL}/digital_human/video/query`, {
      params: { taskId }
    });
  },
  
  /**
   * 上传图片到阿里云OSS
   * @param {File|string} imageData - 图片文件对象或Base64编码的图片数据
   * @param {string} type - 图片类型 (background|logo)
   * @param {Object} options - 上传选项
   * @param {Function} options.onProgress - 上传进度回调函数
   * @param {Number} options.retryCount - 失败重试次数，默认为2
   * @param {Number} options.retryDelay - 重试间隔(毫秒)，默认为1000
   * @returns {Promise} - axios请求Promise
   */
  uploadImageToAliyunOSS(imageData, type, options = {}) {
    const { 
      onProgress = null, 
      retryCount = 2, 
      retryDelay = 1000 
    } = options;
    
    let currentRetry = 0;
    
    const executeUpload = () => {
      // 使用FormData封装数据
      const formData = new FormData();
      
      if (imageData instanceof File) {
        formData.append('file', imageData);
      } else {
        // 如果是Base64，使用Blob转换
        try {
          // 提取Base64数据
          const base64Data = imageData.split(',')[1];
          const blob = this._base64ToBlob(base64Data, 'image/png');
          formData.append('file', blob, `image_${Date.now()}.png`);
        } catch (error) {
          console.error('Base64转换失败:', error);
          formData.append('image', imageData);
        }
      }
      
      formData.append('type', type);
      
      // 构建上传请求
      const uploadEndpoint = `${baseURL}/uploads/image`;
      
      return axios.post(uploadEndpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        // 添加上传进度回调
        onUploadProgress: onProgress ? (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted, progressEvent);
        } : undefined
      }).catch(error => {
        // 实现重试逻辑
        if (currentRetry < retryCount) {
          currentRetry++;
          console.log(`上传失败，第${currentRetry}次重试...`);
          
          // 延迟后重试
          return new Promise(resolve => {
            setTimeout(() => {
              resolve(executeUpload());
            }, retryDelay);
          });
        }
        
        // 所有重试都失败，抛出错误
        throw error;
      });
    };
    
    return executeUpload();
  },
  
  /**
   * 上传视频到阿里云OSS
   * @param {File} videoFile - 视频文件对象
   * @param {string} type - 视频类型 (opening-video|ending-video)
   * @param {Object} options - 上传选项
   * @param {Function} options.onProgress - 上传进度回调函数
   * @returns {Promise} - axios请求Promise
   */
  uploadVideoToAliyunOSS(videoFile, type, options = {}) {
    const { onProgress = null } = options;
    
    const formData = new FormData();
    formData.append('file', videoFile);
    formData.append('type', type);
    formData.append('is_video', 'true');
    
    const uploadEndpoint = `${baseURL}/uploads/video`;
    
    return axios.post(uploadEndpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: onProgress ? (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percentCompleted, progressEvent);
      } : undefined
    });
  },
  
  /**
   * 将Base64数据转换为Blob对象
   * @private
   * @param {string} base64Data - Base64编码的数据
   * @param {string} contentType - 内容类型
   * @returns {Blob} - Blob对象
   */
  _base64ToBlob(base64Data, contentType) {
    const byteCharacters = atob(base64Data);
    const byteArrays = [];
    
    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      const slice = byteCharacters.slice(offset, offset + 512);
      
      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      
      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }
    
    return new Blob(byteArrays, { type: contentType });
  },
  
  /**
   * 提交高级视频合成任务
   * @param {Object} data 请求参数
   * @returns {Promise} 请求结果
   */
  submitAdvancedVideoTask(data) {
    return axios.post(`${baseURL}/digital_human/video/advanced/submit`, data);
  },
  
  /**
   * 查询高级视频合成任务状态
   * @param {String} taskId 任务ID
   * @returns {Promise} 请求结果
   */
  queryAdvancedVideoTask(taskId) {
    return axios.get(`${baseURL}/digital_human/video/advanced/query?taskId=${taskId}`);
  },
  
  /**
   * 获取模板列表
   * @returns {Array} 模板列表
   */
  getTemplateList() {
    return [
      { id: 't-pf4kqasspwzwyexyte121', name: '模板1', ratio: '9:16', isVertical: true },
      { id: 't-af4keqsspfzwyexyte123', name: '模板2', ratio: '9:16', isVertical: true },
      { id: 't-ad4eeqsspfzwyqxyte125', name: '模板3', ratio: '9:16', isVertical: true },
      { id: 't-cd4eeqsspfzwyqxyte127', name: '模板4', ratio: '9:16', isVertical: true },
      { id: 't-hb4eeqsspfzwyqxyte129', name: '模板5', ratio: '16:9', isVertical: false },
      { id: 't-cd4eeqsspfzwyqxyteditu3', name: '模板6', ratio: '9:16', isVertical: true },
      { id: 't-cd4eeqsspfzwyqxyteditu4', name: '模板7', ratio: '9:16', isVertical: true },
      { id: 't-cd4eeqsspfzwyqxyteditu5', name: '无数字人模板', ratio: '9:16', isVertical: true, noDigitalHuman: true }
    ];
  },
  
  /**
   * 上传图片到存储服务 (兼容方法)
   * @param {File|string} imageData - 图片文件对象或Base64编码的图片数据
   * @param {string} type - 图片类型 (background|logo)
   * @param {boolean} useBaiduCloud - 是否使用百度云存储，默认false使用阿里云OSS
   * @returns {Promise} - axios请求Promise
   */
  uploadImageToOSS(imageData, type, useBaiduCloud = false) {
    // 统一使用阿里云OSS上传，忽略useBaiduCloud参数
    console.log('使用阿里云OSS上传图片');
    
    // 如果传入的是File对象，使用FormData
    if (imageData instanceof File) {
      return this.uploadImageToAliyunOSS(imageData, type, {});
    }
    
    // 否则按原来的方式处理
    const formData = new FormData();
    const blob = this._base64ToBlob(imageData.split(',')[1], 'image/png');
    formData.append('file', blob, `image_${Date.now()}.png`);
    formData.append('type', type);
    
    const uploadEndpoint = `${baseURL}/uploads/image`;
    return axios.post(uploadEndpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  
  /**
   * 上传视频到存储服务 (兼容方法)
   * @param {File} videoFile - 视频文件对象
   * @param {string} type - 视频类型 (opening-video|ending-video)
   * @param {boolean} useBaiduCloud - 是否使用百度云存储，默认false使用阿里云OSS
   * @returns {Promise} - axios请求Promise
   */
  uploadVideoToOSS(videoFile, type, useBaiduCloud = false) {
    // 统一使用阿里云OSS上传，忽略useBaiduCloud参数
    console.log('使用阿里云OSS上传视频');
    return this.uploadVideoToAliyunOSS(videoFile, type, {});
  },
  
  /**
   * 上传图片到百度云BOS
   * @param {File|string} imageData - 图片文件对象或Base64编码的图片数据
   * @param {string} type - 图片类型 (background|logo)
   * @param {Object} options - 上传选项
   * @returns {Promise} - 包含上传结果的Promise
   */
  uploadImageToBaiduBOS(imageData, type, options = {}) {
    console.log('使用百度云BOS PUT方式上传图片');
    
    // 处理Base64图片数据
    if (typeof imageData === 'string' && imageData.startsWith('data:')) {
      // 转换Base64到Blob对象
      const blob = this._base64ToBlob(imageData.split(',')[1], 'image/png');
      const file = new File([blob], `image_${Date.now()}.png`, { type: 'image/png' });
      
      // 使用直接上传到百度云BOS的方法，明确指定PUT方法
      return uploadImageToBos(file, {
        fileType: type,
        method: 'PUT' // 明确指定使用PUT上传
      }, options.onProgress).then(url => {
        console.log('百度云BOS上传成功，文件URL:', url);
        return {
          data: {
            success: true,
            data: { url }
          }
        };
      });
    }
    
    // 处理File对象，直接上传到百度云BOS
    if (imageData instanceof File) {
      return uploadImageToBos(imageData, {
        fileType: type,
        method: 'PUT' // 明确指定使用PUT上传
      }, options.onProgress).then(url => {
        console.log('百度云BOS上传成功，文件URL:', url);
        return {
          data: {
            success: true,
            data: { url }
          }
        };
      });
    }
    
    // 如果不是File或Base64，返回错误
    return Promise.reject(new Error('不支持的图片数据格式，请提供File对象或Base64编码的图片数据'));
  },
  
  /**
   * 上传视频到百度云BOS (兼容方法，实际使用阿里云OSS)
   * @param {File} videoFile - 视频文件对象
   * @param {string} type - 视频类型 (opening-video|ending-video)
   * @param {Object} options - 上传选项
   * @returns {Promise} - axios请求Promise
   */
  uploadVideoToBaiduBOS(videoFile, type, options = {}) {
    console.warn('uploadVideoToBaiduBOS已废弃，请使用uploadVideoToAliyunOSS');
    return this.uploadVideoToAliyunOSS(videoFile, type, options);
  }
};

export default digitalHumanAPI; 