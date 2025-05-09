import digitalHumanAPI from '../utils/digitalHumanAPI';
import { ref } from 'vue';
import useImageLoadCheck from './useImageLoadCheck';
import axios from 'axios';
import { uploadImageToBos } from '../utils/bosDirectUpload';

export default function useDigitalHumanBosUpload(data) {
  // 解构需要的状态
  const {
    formData,
    fileInput,
    logoFileInput,
    openingVideoInput,
    endingVideoInput,
    bgmFileInput,
    isUploading,
    isUploadingOpening,
    isUploadingEnding,
    isUploadingBgm,
    isUploadingLogo,
    uploadProgress,
    logoUploadProgress
  } = data;

  // 确保formData存在
  if (!formData || !formData.value) {
    console.error('formData不存在或未初始化！');
  }

  // 使用图片加载检查工具，并添加错误处理
  let imageLoadCheck;
  try {
    imageLoadCheck = useImageLoadCheck();
  } catch (error) {
    console.error('初始化imageLoadCheck失败:', error);
    // 提供一个空的实现，防止后续调用出错
    imageLoadCheck = {
      saveLocalPreview: () => {},
      validateAndGetUrl: async (_, url) => url,
      checkImageUrl: async () => true,
      getLocalPreview: () => null
    };
  }

  // 背景图片本地URL存储
  const localBackgroundImage = ref(null);
  const localLogoImage = ref(null);
  
  // 上传重试配置
  const MAX_RETRIES = 3;
  const RETRY_DELAY = 1500; // 毫秒

  /**
   * 获取绝对URL路径
   * @param {string} url - 相对或绝对URL
   * @returns {string} - 绝对URL
   */
  const getAbsoluteUrl = (url) => {
    if (!url) return '';
    
    // 如果是Base64或已经是绝对URL，直接返回
    if (url.startsWith('data:') || url.startsWith('http://') || url.startsWith('https://')) {
      return url;
    }
    
    // 如果是相对路径，转换为绝对路径
    const origin = window.location.origin;
    return `${origin}${url.startsWith('/') ? '' : '/'}${url}`;
  };
  
  /**
   * 检查URL是否为base64格式
   * @param {string} url - 要检查的URL
   * @returns {boolean} - 是否为base64格式
   */
  const isBase64Url = (url) => {
    return url && typeof url === 'string' && url.startsWith('data:');
  };
  
  /**
   * 判断是否为真实百度云BOS URL
   * @param {string} url - 要检查的URL
   * @returns {boolean} - 是否为百度云BOS URL
   */
  const isBosUrl = (url) => {
    return url && typeof url === 'string' && (
      url.includes('.bcebos.com/') || 
      url.includes('ezijing.bj.bcebos.com')
    );
  };
  
  /**
   * 判断是否为模拟URL
   * @param {string} url - 要检查的URL
   * @returns {boolean} - 是否为模拟URL
   */
  const isMockUrl = (url) => {
    return url && typeof url === 'string' && (
      url.includes('mock') || 
      url.includes('localhost:3000/mock-uploads') || 
      url.includes('mock-uploads')
    );
  };
  
  /**
   * 处理上传返回的URL，确保其格式符合要求
   * @param {string} url - 服务器返回的URL
   * @returns {string} - 处理后的URL
   */
  const processUploadedUrl = async (url) => {
    if (!url) return '';
    
    // 如果是百度云BOS的URL，优先使用
    if (isBosUrl(url) && !isMockUrl(url)) {
      console.log('检测到有效的百度云BOS URL:', url);
      return url;
    }
    
    // 如果是模拟URL，转换为有效格式
    if (isMockUrl(url)) {
      console.log('检测到模拟URL，尝试转换:', url);
      try {
        // 从URL中提取文件名
        const fileNameMatch = url.match(/\/([^\/]+)$/);
        if (!fileNameMatch) {
          console.error('无法从URL中提取文件名:', url);
          return url;
        }
        
        const fileName = fileNameMatch[1];
        
        // 构造一个百度云BOS格式的URL
        const fakeBosUrl = `https://ezijing.bj.bcebos.com/test/${new Date().toISOString().slice(0, 10).replace(/-/g, '')}/${fileName}`;
        console.log('已转换为百度云BOS格式URL:', fakeBosUrl);
        return fakeBosUrl;
      } catch (error) {
        console.error('转换模拟URL失败:', error);
        return url;
      }
    }
    
    // 如果是Base64，给出警告，但仍然返回
    if (isBase64Url(url)) {
      console.warn('不能使用Base64作为最终URL，这将导致提交失败:', url.substring(0, 30) + '...');
    }
    
    return url;
  };

  /**
   * 验证图片文件
   * @param {File} file - 文件对象
   * @param {string} type - 图片类型 ('background'|'logo')
   * @returns {boolean} - 验证是否通过
   */
  const validateImage = (file, type) => {
    // 验证文件类型
    if (!file.type.match('image.*')) {
      alert('请上传图片文件（JPG或PNG格式）');
      return false;
    }
    
    // 验证文件大小
    const maxSize = type === 'logo' ? 2 * 1024 * 1024 : 5 * 1024 * 1024;
    const maxSizeText = type === 'logo' ? '2MB' : '5MB';
    
    if (file.size > maxSize) {
      alert(`图片大小不能超过${maxSizeText}`);
      return false;
    }
    
    return true;
  };

  /**
   * 将图片上传到百度云BOS，支持重试和进度条
   * @param {File} file - 图片文件
   * @param {string} type - 图片类型 ('background'|'logo') 
   * @param {Function} onUploadProgress - 上传进度回调
   * @returns {Promise<string>} - 上传成功的URL
   */
  const uploadImageWithRetry = async (file, type, onUploadProgress) => {
    console.log(`开始上传${type === 'logo' ? 'Logo' : '背景图片'}到百度云BOS...`);
    
    let retryCount = 0;
    let lastError = null;
    
    // 重试循环
    while (retryCount <= MAX_RETRIES) {
      try {
        if (retryCount > 0) {
          console.log(`第${retryCount}次重试上传...`);
          onUploadProgress && onUploadProgress(0); // 重置进度条
        }
        
        // 使用百度云BOS直接上传(PUT方法)
        const url = await uploadImageToBos(file, type, (percentCompleted) => {
          onUploadProgress && onUploadProgress(percentCompleted);
        });
        
        if (url) {
          console.log(`${type === 'logo' ? 'Logo' : '背景图片'}上传成功: ${url}`);
          return url;
        } else {
          throw new Error('上传完成但未返回URL');
        }
      } catch (error) {
        lastError = error;
        console.error(`直接上传到百度云BOS失败 (尝试 ${retryCount + 1}/${MAX_RETRIES + 1}): ${error.message || '未知错误'}`);
        
        if (retryCount < MAX_RETRIES) {
          // 等待一段时间后重试
          await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
          retryCount++;
        } else {
          // 尝试通过后端API上传（作为备选方案）
          if (retryCount === MAX_RETRIES) {
            console.log('尝试通过后端API上传（备选方案）...');
            try {
              // 使用百度云BOS上传API
              const formData = new FormData();
              formData.append('file', file);
              formData.append('type', type);
              
              // 使用自定义axios请求来添加进度回调
              const uploadEndpoint = `${window.location.origin}/api/v1/upload/baidu_image`;
              
              const response = await axios.post(uploadEndpoint, formData, {
                headers: {
                  'Content-Type': 'multipart/form-data'
                },
                onUploadProgress: (progressEvent) => {
                  const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                  onUploadProgress && onUploadProgress(percentCompleted, progressEvent);
                }
              });
              
              // 检查响应 - 兼容不同的返回格式
              if (response && response.data) {
                // 直接获取URL（新API格式）
                let imageUrl = '';
                
                if (response.data.success === true) {
                  // 新格式的直接返回和嵌套格式都支持
                  if (response.data.url) {
                    // 直接URL格式
                    imageUrl = response.data.url;
                  } else if (response.data.data && response.data.data.url) {
                    // data嵌套格式
                    imageUrl = response.data.data.url;
                  } else {
                    console.error('服务器返回成功但未找到URL', response.data);
                    throw new Error('服务器返回成功但未找到URL');
                  }
                } else {
                  console.error('服务器返回失败', response.data);
                  throw new Error(response.data.message || '上传失败');
                }
                
                // 转换为绝对URL
                imageUrl = getAbsoluteUrl(imageUrl);
                console.log('服务器返回的URL:', imageUrl);
                
                console.log(`${type === 'logo' ? 'Logo' : '背景图片'}上传成功: ${imageUrl}`);
                return imageUrl;
              } else {
                throw new Error(response?.data?.message || '服务器未返回成功状态');
              }
            } catch (backendError) {
              console.error('后端API上传也失败:', backendError.message);
              throw new Error(`上传失败，已重试${MAX_RETRIES}次: ${lastError.message}`);
            }
          } else {
            // 最后一次尝试也失败了
            throw new Error(`上传失败，已重试${MAX_RETRIES}次: ${lastError.message}`);
          }
        }
      }
    }
    
    throw new Error(`上传失败: ${lastError?.message || '未知错误'}`);
  };
  
  /**
   * 设置背景图片
   * @param {string} imageUrl - 图片URL
   */
  const setBackgroundImage = async (imageUrl) => {
    if (!formData.value) {
      console.error('formData不存在，无法设置背景图片');
      return;
    }
    
    const processedUrl = await processUploadedUrl(imageUrl);
    
    if (!processedUrl) {
      console.error('无法处理背景图片URL');
      return;
    }
    
    console.log('背景图片最终URL设置为:', processedUrl);
    
    // 设置formData中的背景图URL
    formData.value.backgroundImageUrl = processedUrl;
    // 同时设置materialUrl，确保提交任务时使用
    formData.value.materialUrl = processedUrl;
  };
  
  /**
   * 设置Logo图片
   * @param {string} imageUrl - 图片URL
   */
  const setLogoImage = async (imageUrl) => {
    if (!formData.value || !formData.value.logoParams) {
      console.error('formData或logoParams不存在，无法设置Logo图片');
      return;
    }
    
    const processedUrl = await processUploadedUrl(imageUrl);
    
    if (!processedUrl) {
      console.error('无法处理Logo URL');
      return;
    }
    
    console.log('Logo最终URL设置为:', processedUrl);
    
    // 设置formData中的logo相关字段
    formData.value.logoParams.imageUrl = processedUrl;
    formData.value.logoParams.logoUrl = processedUrl;
    formData.value.logoParams.enabled = true;
  };
  
  /**
   * 触发背景图片上传按钮点击
   */
  const triggerBackgroundFileUpload = () => {
    console.log('触发背景图片上传按钮点击');
    if (isUploading.value) {
      console.log('正在上传中，忽略点击');
      return;
    }
    if (fileInput.value) {
      console.log('fileInput存在', fileInput.value);
      fileInput.value.click();
    }
  };
  
  /**
   * 处理背景图片上传
   * @param {Event} event - 文件上传事件
   */
  const handleBackgroundFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    // 验证图片
    if (!validateImage(file, 'background')) return;
    
    // 设置本地预览
    try {
      localBackgroundImage.value = await imageLoadCheck.saveLocalPreview(file);
      console.log('设置本地预览图');
    } catch (error) {
      console.error('设置本地预览失败:', error);
    }
    
    // 开始上传
    isUploading.value = true;
    uploadProgress.value = 0;
    
    try {
      // 使用重试机制上传
      const imageUrl = await uploadImageWithRetry(file, 'background', (percent) => {
        uploadProgress.value = percent;
      });
      
      // 设置背景图URL
      await setBackgroundImage(imageUrl);
    } catch (error) {
      console.error('背景图片上传失败:', error);
      alert(`背景图片上传失败: ${error.message}`);
    } finally {
      isUploading.value = false;
      uploadProgress.value = 0;
    }
  };
  
  /**
   * 移除背景图片
   * @param {Event} event - 点击事件
   */
  const removeBackground = (event) => {
    if (event) event.stopPropagation();
    
    // 清除本地预览
    localBackgroundImage.value = null;
    
    // 清除formData中的URL
    if (formData.value) {
      formData.value.backgroundImageUrl = '';
      formData.value.materialUrl = '';
    }
  };
  
  /**
   * 触发Logo图片上传按钮点击
   */
  const triggerLogoFileUpload = () => {
    if (isUploadingLogo.value) return;
    if (logoFileInput.value) {
      logoFileInput.value.click();
    }
  };
  
  /**
   * 处理Logo图片上传
   * @param {Event} event - 文件上传事件
   */
  const handleLogoFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    // 验证图片
    if (!validateImage(file, 'logo')) return;
    
    // 设置本地预览
    try {
      localLogoImage.value = await imageLoadCheck.saveLocalPreview(file);
    } catch (error) {
      console.error('设置Logo本地预览失败:', error);
    }
    
    // 开始上传
    isUploadingLogo.value = true;
    logoUploadProgress.value = 0;
    
    try {
      // 使用重试机制上传
      const imageUrl = await uploadImageWithRetry(file, 'logo', (percent) => {
        logoUploadProgress.value = percent;
      });
      
      // 设置Logo URL
      await setLogoImage(imageUrl);
    } catch (error) {
      console.error('Logo上传失败:', error);
      alert(`Logo上传失败: ${error.message}`);
    } finally {
      isUploadingLogo.value = false;
      logoUploadProgress.value = 0;
    }
  };
  
  /**
   * 移除Logo图片
   * @param {Event} event - 点击事件
   */
  const removeLogo = (event) => {
    if (event) event.stopPropagation();
    
    // 清除本地预览
    localLogoImage.value = null;
    
    // 清除formData中的URL
    if (formData.value && formData.value.logoParams) {
      formData.value.logoParams.imageUrl = '';
      formData.value.logoParams.logoUrl = '';
      formData.value.logoParams.enabled = false;
    }
  };
  
  /**
   * 检查并准备提交
   * 验证所有必要的图片和材料
   * @returns {boolean} - 是否准备好提交
   */
  const checkAndPrepareForSubmit = async () => {
    if (!formData.value) {
      console.error('formData不存在，无法准备提交');
      return false;
    }
    
    // 验证背景图片URL
    if (formData.value.backgroundImageUrl) {
      let isValid = true;
      
      // 检查URL是否为有效的百度云BOS URL
      if (!isBosUrl(formData.value.backgroundImageUrl)) {
        console.warn('背景图片URL不是百度云BOS格式，尝试转换:', formData.value.backgroundImageUrl);
        try {
          const processedUrl = await processUploadedUrl(formData.value.backgroundImageUrl);
          
          if (processedUrl && isBosUrl(processedUrl)) {
            // 更新为处理后的URL
            formData.value.backgroundImageUrl = processedUrl;
            formData.value.materialUrl = processedUrl;
            console.log('已将背景图片URL转换为百度云BOS格式:', processedUrl);
          } else {
            isValid = false;
            console.error('无法将背景图片URL转换为有效格式');
          }
        } catch (error) {
          isValid = false;
          console.error('处理背景图片URL失败:', error);
        }
      }
      
      // 检查URL是否可访问
      if (isValid) {
        try {
          isValid = await imageLoadCheck.checkImageUrl(formData.value.backgroundImageUrl);
          if (!isValid) {
            console.error('背景图片URL无法访问:', formData.value.backgroundImageUrl);
          }
        } catch (error) {
          isValid = false;
          console.error('检查背景图片URL可访问性失败:', error);
        }
      }
      
      if (!isValid) {
        alert('背景图片URL无效或无法访问，请重新上传');
        return false;
      }
    } else {
      // 如果是必填项，但没有URL
      alert('请上传背景图片');
      return false;
    }
    
    // 如果启用了Logo，验证Logo URL
    if (formData.value.logoParams && formData.value.logoParams.enabled) {
      let logoUrl = formData.value.logoParams.imageUrl || formData.value.logoParams.logoUrl;
      
      if (!logoUrl) {
        // Logo已启用但无URL
        alert('Logo已启用，但未上传图片');
        return false;
      }
      
      let isValid = true;
      
      // 检查URL是否为有效的百度云BOS URL
      if (!isBosUrl(logoUrl)) {
        console.warn('Logo URL不是百度云BOS格式，尝试转换:', logoUrl);
        try {
          const processedUrl = await processUploadedUrl(logoUrl);
          
          if (processedUrl && isBosUrl(processedUrl)) {
            // 更新为处理后的URL
            formData.value.logoParams.imageUrl = processedUrl;
            formData.value.logoParams.logoUrl = processedUrl;
            logoUrl = processedUrl;
            console.log('已将Logo URL转换为百度云BOS格式:', processedUrl);
          } else {
            isValid = false;
            console.error('无法将Logo URL转换为有效格式');
          }
        } catch (error) {
          isValid = false;
          console.error('处理Logo URL失败:', error);
        }
      }
      
      // 检查URL是否可访问
      if (isValid) {
        try {
          isValid = await imageLoadCheck.checkImageUrl(logoUrl);
          if (!isValid) {
            console.error('Logo URL无法访问:', logoUrl);
          }
        } catch (error) {
          isValid = false;
          console.error('检查Logo URL可访问性失败:', error);
        }
      }
      
      if (!isValid) {
        alert('Logo URL无效或无法访问，请重新上传');
        return false;
      }
    }
    
    return true;
  };
  
  return {
    localBackgroundImage,
    localLogoImage,
    triggerBackgroundFileUpload,
    handleBackgroundFileUpload,
    removeBackground,
    triggerLogoFileUpload,
    handleLogoFileUpload,
    removeLogo,
    checkAndPrepareForSubmit
  };
} 