/**
 * 图片URL检查工具
 * 提供方法验证图片URL是否可以正常加载
 */
import { ref } from 'vue';

/**
 * 检查图片URL是否有效
 * @param {string} url - 要检查的图片URL
 * @param {number} timeout - 超时时间(毫秒)
 * @returns {Promise<boolean>} - 图片是否可以加载
 */
export const checkImageUrl = (url, timeout = 3000) => {
  return new Promise((resolve) => {
    if (!url) {
      console.warn('图片URL为空，无法验证');
      resolve(false);
      return;
    }

    // 如果是base64格式，认为总是有效
    if (url.startsWith('data:image/')) {
      console.log('Base64图片，跳过验证');
      resolve(true);
      return;
    }

    const img = new Image();
    
    // 成功加载
    img.onload = () => {
      console.log('图片URL有效:', url.substring(0, 30) + '...');
      resolve(true);
    };
    
    // 加载失败
    img.onerror = () => {
      console.warn('图片URL无效:', url.substring(0, 30) + '...');
      resolve(false);
    };
    
    // 设置超时
    const timer = setTimeout(() => {
      console.warn('图片加载超时:', url.substring(0, 30) + '...');
      resolve(false);
    }, timeout);
    
    // 清理超时计时器
    img.onload = () => {
      clearTimeout(timer);
      console.log('图片URL有效:', url.substring(0, 30) + '...');
      resolve(true);
    };
    
    img.onerror = () => {
      clearTimeout(timer);
      console.warn('图片URL无效:', url.substring(0, 30) + '...');
      resolve(false);
    };
    
    // 开始加载图片
    img.src = url;
  });
};

/**
 * 图片加载检查钩子
 * @returns {Object} - 图片加载检查工具函数
 */
export default function useImageLoadCheck() {
  // 本地保存的临时URL
  const localUrls = ref(new Map());
  
  /**
   * 保存本地预览URL
   * @param {string} key - 存储键名
   * @param {string} url - 本地预览URL
   */
  const saveLocalPreview = (key, url) => {
    localUrls.value.set(key, url);
  };
  
  /**
   * 获取本地预览URL
   * @param {string} key - 存储键名
   * @returns {string|null} - 对应的本地预览URL或null
   */
  const getLocalPreview = (key) => {
    return localUrls.value.get(key) || null;
  };
  
  /**
   * 检查URL并返回可用的URL
   * @param {string} key - 图片键名(用于本地缓存)
   * @param {string} serverUrl - 服务器返回的URL
   * @param {string} localUrl - 本地预览URL
   * @returns {Promise<string>} - 可用的图片URL
   */
  const validateAndGetUrl = async (key, serverUrl, localUrl = null) => {
    // 保存本地URL
    if (localUrl) {
      saveLocalPreview(key, localUrl);
    }

    // 检查服务器URL
    const isServerUrlValid = await checkImageUrl(serverUrl);
    
    if (isServerUrlValid) {
      return serverUrl;
    } else {
      // 服务器URL无效，回退到本地预览
      console.log('使用本地预览URL作为回退');
      return getLocalPreview(key) || serverUrl;
    }
  };
  
  return {
    checkImageUrl,
    saveLocalPreview,
    getLocalPreview,
    validateAndGetUrl
  };
}
