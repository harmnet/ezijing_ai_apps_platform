import digitalHumanAPI from '../utils/digitalHumanAPI';
import { ref } from 'vue';
import useImageLoadCheck from './useImageLoadCheck';
import axios from 'axios';

export default function useDigitalHumanUpload(data) {
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
   * 判断是否为真实阿里云OSS URL
   * @param {string} url - 要检查的URL
   * @returns {boolean} - 是否为阿里云OSS URL
   */
  const isOssUrl = (url) => {
    return url && typeof url === 'string' && (
      url.includes('.aliyuncs.com/') || 
      url.includes('ezijing-uploads.oss-cn-beijing.aliyuncs.com')
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
    
    // 如果是阿里云OSS的URL，优先使用
    if (isOssUrl(url) && !isMockUrl(url)) {
      console.log('检测到有效的阿里云OSS URL:', url);
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
        
        // 构造一个阿里云OSS格式的URL
        const fakeOssUrl = `https://ezijing-uploads.oss-cn-beijing.aliyuncs.com/images/${new Date().toISOString().slice(0, 10).replace(/-/g, '')}/${fileName}`;
        console.log('已转换为阿里云OSS格式URL:', fakeOssUrl);
        return fakeOssUrl;
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
   * 上传图片到阿里云OSS，支持重试和进度条
   * @param {File} file - 图片文件
   * @param {string} type - 图片类型 ('background'|'logo') 
   * @param {Function} onUploadProgress - 上传进度回调
   * @returns {Promise<string>} - 上传成功的URL
   */
  const uploadImageWithRetry = async (file, type, onUploadProgress) => {
    console.log(`开始上传${type === 'logo' ? 'Logo' : '背景图片'}到阿里云OSS...`);
    
    let retryCount = 0;
    let lastError = null;
    
    // 重试循环
    while (retryCount <= MAX_RETRIES) {
      try {
        if (retryCount > 0) {
          console.log(`第${retryCount}次重试上传...`);
          onUploadProgress && onUploadProgress(0); // 重置进度条
        }
        
        // 使用阿里云OSS上传API
        // 这里调用的是uploadImageToOSS方法，第三个参数为false表示使用阿里云OSS
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', type);
        
        // 使用自定义axios请求来添加进度回调
        const uploadEndpoint = `${window.location.origin}/api/v1/uploads/image`;
        
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
          
          // 验证URL有效性 - 在阿里云OSS的情况下不需要判断isOssUrl
          console.log(`${type === 'logo' ? 'Logo' : '背景图片'}上传成功: ${imageUrl}`);
          return imageUrl;
        } else {
          throw new Error(response?.data?.message || '服务器未返回成功状态');
        }
      } catch (error) {
        lastError = error;
        console.error(`上传失败 (尝试 ${retryCount + 1}/${MAX_RETRIES + 1}): ${error.message || '未知错误'}`);
        
        if (retryCount < MAX_RETRIES) {
          // 等待一段时间后重试
          await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
          retryCount++;
        } else {
          break; // 超过最大重试次数，退出循环
        }
      }
    }
    
    // 所有重试都失败
    throw new Error(`上传失败，已重试${MAX_RETRIES}次: ${lastError?.message || '未知错误'}`);
  };

  // 背景图片上传相关方法
  const triggerFileUpload = () => {
    console.log('触发背景图片上传按钮点击');
    if (isUploading && isUploading.value) {
      console.log('正在上传中，忽略点击');
      return;
    }
    if (fileInput && fileInput.value) {
      console.log('fileInput存在', fileInput.value);
      fileInput.value.click();
    } else {
      console.error('fileInput不存在!');
    }
  };
  
  const handleFileUpload = async (event) => {
    if (!event || !event.target || !event.target.files) {
      console.error('无效的上传事件对象');
      return;
    }
    
    const file = event.target.files[0];
    if (!file) return;
    
    // 验证文件
    if (!validateImage(file, 'background')) {
      return;
    }
    
    try {
      // 显示上传指示器
      if (isUploading) isUploading.value = true;
      if (uploadProgress) uploadProgress.value = 0;
      
      // 先读取文件并创建本地预览URL
      const reader = new FileReader();
      
      reader.onload = async (e) => {
        try {
          // 先设置本地预览，防止上传延迟导致的预览延迟
          const localPreviewUrl = e.target.result;
          // 保存本地预览URL
          localBackgroundImage.value = localPreviewUrl;
          
          // 确保formData和其属性存在
          if (formData && formData.value) {
            // 设置预览
            formData.value.backgroundImageUrl = localPreviewUrl;
            console.log('设置本地预览图');
            
            // 使用ImageLoadCheck工具保存本地预览（安全地调用）
            if (imageLoadCheck && typeof imageLoadCheck.saveLocalPreview === 'function') {
              try {
                imageLoadCheck.saveLocalPreview('background', localPreviewUrl);
              } catch (error) {
                console.error('保存本地预览时出错:', error);
              }
            }
            
            try {
              // 使用改进的上传函数
              const imageUrl = await uploadImageWithRetry(file, 'background', (percent) => {
                if (uploadProgress) uploadProgress.value = percent;
              });
              
              // 设置处理后的URL
              formData.value.backgroundImageUrl = imageUrl;
              formData.value.materialUrl = imageUrl;
              console.log('背景图片最终URL设置为:', imageUrl);
              
            } catch (uploadError) {
              console.error('上传图片到阿里云OSS失败:', uploadError);
              alert(`上传图片失败: ${uploadError.message || '未知错误'}。已保留本地预览图，但无法提交任务。请重试或联系管理员。`);
              // 使用本地预览
              formData.value.backgroundImageUrl = localBackgroundImage.value;
              // 清除materialUrl字段，避免提交base64数据
              formData.value.materialUrl = '';
            }
          } else {
            console.error('formData或其value不存在');
          }
        } catch (e) {
          console.error('处理背景图片时出错:', e);
          alert('处理图片时出错: ' + (e.message || '未知错误'));
        } finally {
          // 无论成功还是失败，都要重置上传状态
          if (isUploading) isUploading.value = false;
          if (uploadProgress) uploadProgress.value = 0;
        }
      };
      
      reader.onerror = () => {
        console.error('读取文件时出错');
        alert('读取文件时出错');
        if (isUploading) isUploading.value = false;
        if (uploadProgress) uploadProgress.value = 0;
      };
      
      // 开始读取文件
      reader.readAsDataURL(file);
    } catch (e) {
      console.error('处理背景图片上传事件时出错:', e);
      alert('上传图片时出错: ' + (e.message || '未知错误'));
      if (isUploading) isUploading.value = false;
      if (uploadProgress) uploadProgress.value = 0;
    }
  };
  
  const removeBackground = (event) => {
    event.stopPropagation();
    if (formData && formData.value) {
      formData.value.backgroundImageUrl = '';
      formData.value.materialUrl = '';
      localBackgroundImage.value = null;
      if (fileInput && fileInput.value) {
        fileInput.value.value = '';
      }
    }
  };
  
  // Logo上传相关方法
  const triggerLogoFileUpload = () => {
    console.log('触发Logo上传按钮点击');
    if (isUploadingLogo && isUploadingLogo.value) {
      console.log('Logo正在上传中，忽略点击');
      return;
    }
    if (logoFileInput && logoFileInput.value) {
      logoFileInput.value.click();
    } else {
      console.error('logoFileInput不存在!');
    }
  };
  
  const handleLogoFileUpload = async (event) => {
    if (!event || !event.target || !event.target.files) {
      console.error('无效的上传事件对象');
      return;
    }
    
    const file = event.target.files[0];
    if (!file) return;
    
    // 验证文件
    if (!validateImage(file, 'logo')) {
      return;
    }
    
    try {
      // 显示上传指示器
      if (isUploadingLogo) isUploadingLogo.value = true;
      if (logoUploadProgress) logoUploadProgress.value = 0;
      
      // 先读取文件并创建本地预览URL
      const reader = new FileReader();
      
      reader.onload = async (e) => {
        try {
          // 先设置本地预览，防止上传延迟导致的预览延迟
          const localPreviewUrl = e.target.result;
          // 保存本地预览URL
          localLogoImage.value = localPreviewUrl;
          
          // 确保formData和其属性存在
          if (formData && formData.value && formData.value.logoParams) {
            // 设置预览
            formData.value.logoParams.logoUrl = localPreviewUrl;
            console.log('设置Logo本地预览图');
            
            // 使用ImageLoadCheck工具保存本地预览（安全地调用）
            if (imageLoadCheck && typeof imageLoadCheck.saveLocalPreview === 'function') {
              try {
                imageLoadCheck.saveLocalPreview('logo', localPreviewUrl);
              } catch (error) {
                console.error('保存Logo本地预览时出错:', error);
              }
            }
            
            try {
              // 使用改进的上传函数
              const imageUrl = await uploadImageWithRetry(file, 'logo', (percent) => {
                if (logoUploadProgress) logoUploadProgress.value = percent;
              });
              
              // 设置处理后的URL
              formData.value.logoParams.logoUrl = imageUrl;
              formData.value.logoParams.imageUrl = imageUrl;
              console.log('Logo最终URL设置为:', imageUrl);
              
              // 设置logo已启用
              formData.value.logoParams.enabled = true;
              
            } catch (uploadError) {
              console.error('上传Logo图片失败:', uploadError);
              alert(`上传Logo图片失败: ${uploadError.message || '未知错误'}。已保留本地预览图，但无法提交任务。请重试或联系管理员。`);
              // 使用本地预览
              formData.value.logoParams.logoUrl = localLogoImage.value;
              formData.value.logoParams.imageUrl = '';
            }
          } else {
            console.error('formData.logoParams不存在');
          }
        } catch (e) {
          console.error('处理Logo图片时出错:', e);
          alert('处理Logo图片时出错: ' + (e.message || '未知错误'));
        } finally {
          // 无论成功还是失败，都要重置上传状态
          if (isUploadingLogo) isUploadingLogo.value = false;
          if (logoUploadProgress) logoUploadProgress.value = 0;
        }
      };
      
      reader.onerror = () => {
        console.error('读取Logo文件时出错');
        alert('读取Logo文件时出错');
        if (isUploadingLogo) isUploadingLogo.value = false;
        if (logoUploadProgress) logoUploadProgress.value = 0;
      };
      
      // 开始读取文件
      reader.readAsDataURL(file);
    } catch (e) {
      console.error('处理Logo上传事件时出错:', e);
      alert('上传Logo图片时出错: ' + (e.message || '未知错误'));
      if (isUploadingLogo) isUploadingLogo.value = false;
      if (logoUploadProgress) logoUploadProgress.value = 0;
    }
  };
  
  const removeLogo = (event) => {
    event.stopPropagation();
    if (formData && formData.value && formData.value.logoParams) {
      formData.value.logoParams.imageUrl = '';
      formData.value.logoParams.logoUrl = '';
      localLogoImage.value = null;
      if (logoFileInput && logoFileInput.value) {
        logoFileInput.value.value = '';
      }
    }
  };
  
  // 片头视频上传相关方法
  const triggerOpeningVideoUpload = () => {
    // 禁用片头视频上传功能
    console.log('片头视频上传功能未开放');
    alert('片头视频上传功能暂未开放');
    return;
  };
  
  const handleOpeningVideoUpload = async (event) => {
    // 禁用处理逻辑，防止意外调用
    console.log('片头视频上传功能未开放');
    alert('片头视频上传功能暂未开放');
    if (event && event.target) {
      event.target.value = ''; // 重置文件输入
    }
    return;
  };
  
  const removeOpeningVideo = (event) => {
    if (event) {
      event.stopPropagation();
    }
    // 仅用于移除可能存在的视频，但实际上该功能已被禁用
    if (formData && formData.value && formData.value.openingMaterial) {
      formData.value.openingMaterial.fileUrl = '';
    }
  };
  
  // 片尾视频上传相关方法
  const triggerEndingVideoUpload = () => {
    // 禁用片尾视频上传功能
    console.log('片尾视频上传功能未开放');
    alert('片尾视频上传功能暂未开放');
    return;
  };
  
  const handleEndingVideoUpload = async (event) => {
    // 禁用处理逻辑，防止意外调用
    console.log('片尾视频上传功能未开放');
    alert('片尾视频上传功能暂未开放');
    if (event && event.target) {
      event.target.value = ''; // 重置文件输入
    }
    return;
  };
  
  const removeEndingVideo = (event) => {
    if (event) {
      event.stopPropagation();
    }
    // 仅用于移除可能存在的视频，但实际上该功能已被禁用
    if (formData && formData.value && formData.value.endingMaterial) {
      formData.value.endingMaterial.fileUrl = '';
    }
  };
  
  // 背景音乐上传相关方法
  const triggerBgmUpload = () => {
    // 禁用背景音乐上传功能
    console.log('背景音乐上传功能未开放');
    alert('背景音乐上传功能暂未开放');
    return;
  };
  
  const handleBgmUpload = async (event) => {
    // 禁用处理逻辑，防止意外调用
    console.log('背景音乐上传功能未开放');
    alert('背景音乐上传功能暂未开放');
    if (event && event.target) {
      event.target.value = ''; // 重置文件输入
    }
    return;
  };
  
  const removeBgm = (event) => {
    if (event) {
      event.stopPropagation();
    }
    // 仅用于移除可能存在的背景音乐，但实际上该功能已被禁用
    if (formData && formData.value && formData.value.bgmParams) {
      formData.value.bgmParams.bgmUrl = '';
    }
  };

  return {
    // 背景图片上传
    triggerFileUpload,
    handleFileUpload,
    removeBackground,
    
    // Logo上传
    triggerLogoFileUpload,
    handleLogoFileUpload,
    removeLogo,
    
    // 片头视频上传
    triggerOpeningVideoUpload,
    handleOpeningVideoUpload,
    removeOpeningVideo,
    
    // 片尾视频上传
    triggerEndingVideoUpload,
    handleEndingVideoUpload,
    removeEndingVideo,
    
    // 背景音乐上传
    triggerBgmUpload,
    handleBgmUpload,
    removeBgm
  };
} 