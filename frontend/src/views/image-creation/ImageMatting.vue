<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import CktDesign from "@chuangkit/chuangkit-design"
import CryptoJS from "crypto-js";
import store from "@/store";
import { useRouter } from "vue-router";

/**
 * 构建签名
 * @param obj 参数对象，对象中的所有属性全部参与签名的生成
 * @returns {string} 签名
 */
const buildSign = obj => {
  let signParameterArray = [];
  for (let key in obj) {
    signParameterArray.push(`${key}=${obj[key]}`)
  }

  let signPlaintext = signParameterArray.sort().join("&");
  return CryptoJS.MD5(signPlaintext)
      .toString()
      .toUpperCase();
}

/**
 * 构建ai功能签名
 * @param appId 第三方企业id
 * @param appSecret 企业密钥
 * @param timestamp 时间戳，取当前时间即可
 * @param unionId 用户标识
 * @returns {string} 签名
 */
const buildAIProgramSign = (appId, appSecret, timestamp, unionId) => {
  let signParameterObj = {
    app_id: appId,
    timestamp: timestamp,
    union_id: unionId,
    app_secret: appSecret
  }

  return buildSign(signParameterObj);
}

// 状态控制
const isLoading = ref(false);
const errorMessage = ref('');
const showUploadCard = ref(true);
const fileInput = ref(null);

// 记录组件状态
const isMounted = ref(false);
const router = useRouter(); // 获取router实例

// 触发文件选择
const triggerFileSelect = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

// 处理文件选择
const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    // 检查文件大小 (最大10MB)
    if (file.size > 10 * 1024 * 1024) {
      errorMessage.value = "文件大小超过10MB限制，请选择更小的文件。";
      return;
    }
    
    // 检查文件类型
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
      errorMessage.value = "请选择JPG或PNG格式的图片文件。";
      return;
    }
    
    openMattingEditorWithFile(file);
  }
};

// 使用选中的文件打开抠图工具
const openMattingEditorWithFile = (file) => {
  try {
    // 更新UI状态
    isLoading.value = true;
    showUploadCard.value = false;
    errorMessage.value = '';
    
    // 准备参数
    const appId = "54d9adec77d0402794018d166110f3dd";
    const appSecret = "08097010E0EF4B85EE2B8CE438328249";
    const unionId = store.state.user?.id || 'default_user';
    const timestamp = Date.now();
    const sign = buildAIProgramSign(appId, appSecret, timestamp, unionId);

    let params = {
      appId: appId,
      unionId: unionId,
      timestamp: timestamp,
      sign: sign,
      file: file, // 传入文件对象
      finishBtn: "完成抠图", // 自定义完成按钮文案
      hideLogo: true, // 是否隐藏创客贴logo
      closeType: 0 // 完成后关闭弹窗
    }

    console.log("初始化智能抠图实例参数:", {
      ...params,
      file: "File对象" // 不打印文件对象本身，避免日志过大
    });
    
    // 最简单的方式创建并打开实例
    try {
      // 仅创建实例并打开，不注册事件处理器
      const instance = CktDesign.createMattingDesign(params);
      
      // 打开实例，不尝试任何其他操作
      instance.open()
        .then(() => {
          console.log("智能抠图工具打开成功");
          if (isMounted.value) {
            isLoading.value = false;
          }
        })
        .catch(err => {
          console.error("打开智能抠图工具失败:", err);
          if (isMounted.value) {
            errorMessage.value = `抠图工具初始化失败: ${err.message || '未知错误'}`;
            isLoading.value = false;
            showUploadCard.value = true;
          }
        });
    } catch (e) {
      console.error("创建或打开抠图工具失败:", e);
      errorMessage.value = `创建抠图工具失败: ${e.message || '未知错误'}`;
      isLoading.value = false;
      showUploadCard.value = true;
    }
  } catch (error) {
    console.error("智能抠图初始化过程错误:", error);
    errorMessage.value = `初始化错误: ${error.message || '未知错误'}`;
    isLoading.value = false;
    showUploadCard.value = true;
  }
};

// 生命周期钩子
onMounted(() => {
  // 组件挂载后，记录挂载状态
  isMounted.value = true;
  
  // 注册全局事件监听器
  window.addEventListener('message', (event) => {
    // 尝试捕获第三方抠图工具可能发出的消息
    // 如果是关闭事件
    if (event.data && typeof event.data === 'object' && event.data.type === 'close') {
      console.log('接收到抠图工具关闭消息');
      if (isMounted.value) {
        showUploadCard.value = true;
        isLoading.value = false;
      }
    }
  });
});

onUnmounted(() => {
  // 标记组件已卸载，避免异步操作更新已卸载组件的状态
  isMounted.value = false;
});

// 添加一个我们自己的退出处理方法
const handleCustomExit = () => {
  // 关闭第三方页面或返回到我们的主页面
  router.push('/image-creation'); // 返回上级页面，根据实际路由结构调整
};
</script>

<template>
  <div class="image-matting-container">
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>正在加载智能抠图工具，请稍候...</p>
    </div>
    
    <div v-else-if="showUploadCard" class="upload-container">
      <div class="upload-card">
        <i class="ri-scissors-cut-line"></i>
        <h3>智能抠图</h3>
        <p>选择一张图片开始抠图，支持10MB以下的PNG、JPG格式</p>
        
        <div class="error-message" v-if="errorMessage">
          <i class="ri-error-warning-line"></i>
          <span>{{ errorMessage }}</span>
        </div>
        
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileSelect" 
          accept=".jpg,.jpeg,.png" 
          style="display: none;"
        />
        
        <div class="button-group">
          <button class="primary-button full-width" @click="triggerFileSelect">
            <i class="ri-upload-2-line"></i> 选择图片
          </button>
        </div>
        
        <div class="features">
          <div class="feature">
            <i class="ri-magic-line"></i>
            <p>一键移除背景</p>
          </div>
          <div class="feature">
            <i class="ri-crop-line"></i>
            <p>精细抠图编辑</p>
          </div>
          <div class="feature">
            <i class="ri-download-line"></i>
            <p>高质量下载</p>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else id="ai-matting-container"></div>
    
    <div class="custom-exit-button" @click="handleCustomExit">返回</div>
  </div>
</template>

<style scoped>
.image-matting-container {
  width: 100%;
  height: 85vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

#ai-matting-container {
  width: 100%;
  height: 100%;
}

.loading-container, .upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(186, 0, 63, 0.2);
  border-radius: 50%;
  border-top-color: #ba003f;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.upload-card {
  background-color: white;
  border-radius: 16px;
  padding: 40px;
  max-width: 500px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
}

.upload-card i.ri-scissors-cut-line {
  font-size: 60px;
  color: #ba003f;
  background: rgba(186, 0, 63, 0.08);
  border-radius: 50%;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}

.upload-card h3 {
  font-size: 24px;
  margin: 0 0 16px;
  color: #333;
}

.upload-card p {
  color: #666;
  margin: 0 0 24px;
  line-height: 1.5;
}

.error-message {
  background-color: #fff2f2;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 24px;
  color: #ba003f;
  display: flex;
  align-items: center;
  text-align: left;
}

.error-message i {
  margin-right: 8px;
  font-size: 18px;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
  width: 100%;
}

.primary-button {
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  transition: all 0.2s ease;
  background-color: #ba003f;
  color: white;
}

.primary-button:hover {
  background-color: #d4185b;
}

.full-width {
  width: 100%;
  max-width: 250px;
}

.features {
  display: flex;
  justify-content: space-around;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.feature i {
  font-size: 24px;
  color: #ba003f;
}

.feature p {
  font-size: 14px;
  margin: 0;
}

.custom-exit-button {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  background: #fff;
  padding: 8px 15px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  cursor: pointer;
}
</style> 