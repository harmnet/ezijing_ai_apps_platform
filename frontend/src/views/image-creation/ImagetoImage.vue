<template>
  <div class="content">
    <div class="page-header">
      <div class="page-nav">
        <h2>图片风格调整</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showTips">
          <i class="ri-book-read-line"></i>
          知识学习
        </button>
      </div>
    </div>

    <div class="function-container">
      <!-- 左侧表单区域 -->
      <div class="form-container">
        <div class="section-header">
          <h3 class="section-title">
            <i class="ri-settings-3-line"></i>
            输入参数
          </h3>
        </div>
        
        <div class="form-group">
          <label class="required">上传参考图片</label>
          <div class="upload-area" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileChange" 
              accept="image/*" 
              style="display: none"
            >
            <div v-if="!previewImage" class="upload-placeholder">
              <i class="ri-upload-cloud-line"></i>
              <p>点击或拖拽图片到此处上传</p>
              <small>支持jpg、png格式，建议尺寸不小于512x512</small>
            </div>
            <img v-else :src="previewImage" class="preview-image" alt="预览图">
          </div>
        </div>

        <div class="form-group">
          <label class="required">全局风格化</label>
          <div class="style-radio-group">
            <div class="style-radio-item" v-for="(style, index) in styleOptions" :key="index" :class="{'disabled': style.disabled}">
              <input
                type="radio"
                :id="`style-${index}`"
                :value="style.value"
                v-model="formData.styleType"
                :name="'styleType'"
                :disabled="style.disabled"
              >
              <label :for="`style-${index}`">{{ style.label }}</label>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="prompt" class="required">提示词</label>
          <textarea 
            id="prompt" 
            v-model="formData.prompt"
            placeholder="描述您希望的转换效果，例如：转换成油画风格，添加梦幻效果..."
            class="form-control"
            rows="5"
          ></textarea>
          <small>详细的描述可以帮助AI更好地理解您的需求，不同风格需要不同的提示词策略</small>
        </div>

        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="generateImage" class="btn btn-primary" :disabled="isLoading || !previewImage || (!formData.prompt.trim() && formData.styleType === 'none')">
            <i class="ri-magic-line" v-if="!isLoading"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isLoading ? '处理中...' : '开始转换' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>

      <!-- 右侧显示区域 -->
      <div class="right-column">
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-image-line"></i>
              处理结果
            </h3>
          </div>

          <div class="result-content-wrapper">
            <!-- 加载中显示 -->
            <div class="loading-overlay" v-if="isLoading">
              <div class="loading-spinner"></div>
              <div class="loading-text">正在处理图片，请稍候...</div>
              <div class="loading-status" v-if="taskStatus">{{ taskStatus }}</div>
            </div>
            
            <!-- 空状态显示 -->
            <div class="empty-result" v-else-if="!resultImage">
              <div class="empty-content">
                <i class="ri-image-add-line" style="font-size: 64px; color: #e9ecef;"></i>
                <div class="empty-message">请上传图片并填写提示词后点击"开始转换"按钮</div>
              </div>
            </div>
            
            <!-- 处理结果显示 -->
            <div class="result-comparison" v-else>
              <div class="image-container original">
                <h4>原始图片</h4>
                <div class="image-wrapper">
                  <img :src="previewImage" alt="原始图片">
                </div>
              </div>
              <div class="image-arrow">
                <i class="ri-arrow-right-line"></i>
              </div>
              <div class="image-container result">
                <h4>转换结果</h4>
                <div class="image-wrapper">
                  <img :src="resultImage" alt="转换后的图片">
                  <div class="image-overlay">
                    <button @click="downloadImage(resultImage)" class="overlay-button">
                      <i class="ri-download-line"></i>
                      下载图片
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 错误信息 -->
            <div class="error-message" v-if="error">
              <i class="ri-error-warning-line"></i>
              {{ error }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 知识学习侧边栏 -->
    <el-drawer
      v-model="knowledgeDrawerVisible"
      title="AI图片风格调整知识学习"
      direction="rtl"
      size="35%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in knowledgeData" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <span class="knowledge-icon"><i :class="item.icon"></i></span>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatText(item.text)"></div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
// 引入统一CSS文件
import '@/assets/css/text-creation-common.css';
import { imageToImageKnowledge } from '@/views/Knowledge_data.js';
import { ElDrawer } from 'element-plus';

export default {
  name: 'ImagetoImage',
  components: {
    ElDrawer
  },
  
  data() {
    return {
      formData: {
        prompt: '',
        styleType: 'none',
        imageUrl: ''
      },
      isLoading: false,
      error: null,
      previewImage: null,
      resultImage: null,
      taskId: null,
      taskStatus: '',
      showTipsModal: false,
      knowledgeDrawerVisible: false,
      knowledgeData: imageToImageKnowledge,
      // 全局风格化选项
      styleOptions: [
        { value: 'none', label: '无风格' },
        { value: 'oil', label: '油画风格' },
        { value: 'watercolor', label: '水彩画风格' },
        { value: 'sketch', label: '素描风格' },
        { value: 'comic', label: '卡通漫画风格' },
        { value: 'chinese', label: '中国水墨风格', disabled: true },
        { value: 'japan', label: '日式浮世绘风格', disabled: true },
        { value: 'impressionism', label: '印象派风格', disabled: true },
        { value: 'cyberpunk', label: '赛博朋克风格', disabled: true },
        { value: 'vintage', label: '复古风格', disabled: true },
        { value: 'fantasy', label: '梦幻风格', disabled: true }
      ],
      pollingInterval: null
    }
  },

  computed: {
    selectedStyle() {
      return this.styleOptions.find(s => s.value === this.formData.styleType) || null;
    }
  },

  watch: {
    // 监听styleType变化，自动生成提示词
    'formData.styleType': function(newStyleType) {
      // 检查选中的风格是否为禁用状态
      const selectedStyle = this.styleOptions.find(s => s.value === newStyleType);
      
      if (selectedStyle && selectedStyle.disabled) {
        // 如果选中了禁用的风格，重置为无风格
        this.formData.styleType = 'none';
        return;
      }
      
      if (newStyleType !== 'none') {
        const style = this.styleOptions.find(s => s.value === newStyleType);
        if (style) {
          this.formData.prompt = `转换成${style.label}`;
          console.log('自动生成提示词:', this.formData.prompt);
        }
      } else {
        // 选择"无风格"时，清空提示词
        this.formData.prompt = '';
      }
    }
  },

  methods: {
    showTips() {
      this.knowledgeDrawerVisible = true;
    },
    
    formatText(text) {
      if (!text) return '';
      // 将Markdown风格的加粗文本转换为HTML加粗标签
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // 将换行符转换为HTML段落
      text = text.replace(/\n\n/g, '</p><p>');
      return `<p>${text}</p>`;
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleFileChange(event) {
      const file = event.target.files[0];
      this.handleImage(file);
    },

    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.handleImage(file);
    },

    handleImage(file) {
      if (!file || !file.type.startsWith('image/')) {
        this.error = '请上传有效的图片文件';
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewImage = e.target.result;
        this.error = null;
        
        // 实际环境下上传图片到服务器
        this.uploadImage(file);
      };
      reader.readAsDataURL(file);
    },

    resetForm() {
      this.formData = {
        prompt: '',
        styleType: 'none',
        imageUrl: ''
      };
      this.previewImage = null;
      this.resultImage = null;
      this.error = null;
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
        this.pollingInterval = null;
      }
    },

    async uploadImage(file) {
      try {
        this.isLoading = true;
        this.error = null;
        this.taskStatus = '正在上传图片...';
        
        // 调试：本地先设置URL备用
        // 上传失败时也可以使用本地预览图
        this.formData.imageUrl = this.previewImage;
        console.log('已设置临时本地图片URL:', this.previewImage.substring(0, 50) + '...');
        
        const formData = new FormData();
        formData.append('image', file);
        
        console.log('开始上传图片到服务器...');
        
        // 增加超时和重试逻辑
        let response;
        let retryCount = 0;
        const maxRetries = 2;
        
        while (retryCount <= maxRetries) {
          try {
            response = await Promise.race([
              fetch(`${window.APP_CONFIG.API_BASE_URL}/api/images/upload`, {
                method: 'POST',
                body: formData
              }),
              new Promise((_, reject) => 
                setTimeout(() => reject(new Error('请求超时')), 10000)
              )
            ]);
            break; // 成功获取响应，跳出循环
          } catch (fetchError) {
            console.error(`上传尝试 ${retryCount + 1}/${maxRetries + 1} 失败:`, fetchError);
            retryCount++;
            
            if (retryCount <= maxRetries) {
              this.taskStatus = `上传失败，正在尝试第 ${retryCount + 1} 次重试...`;
              await new Promise(resolve => setTimeout(resolve, 1000)); // 等待1秒后重试
            } else {
              throw fetchError; // 达到最大重试次数，抛出错误
            }
          }
        }
        
        console.log('服务器响应状态:', response.status);
        
        // 调试：检查响应类型
        const contentType = response.headers.get("content-type");
        console.log('响应Content-Type:', contentType);
        
        if (contentType && contentType.includes("application/json")) {
          const result = await response.json();
          console.log('上传结果:', result);
          
          if (result.success) {
            this.formData.imageUrl = result.file.url;
            console.log('图片上传成功，URL已设置:', this.formData.imageUrl);
            this.taskStatus = '图片上传成功';
          } else {
            console.error('服务器返回上传失败:', result.error);
            // 不抛出错误，继续使用本地URL
            this.taskStatus = '服务器上传失败，将使用本地图片（功能可能受限）';
          }
        } else {
          // 如果不是JSON响应，尝试读取文本内容
          const textContent = await response.text();
          console.error('服务器返回非JSON数据:', textContent.substring(0, 150) + '...');
          this.error = '服务器响应格式错误，请检查接口';
          this.taskStatus = '上传失败：服务器响应格式错误';
        }
      } catch (error) {
        console.error('上传图片过程中出错:', error);
        
        // 更明确的错误信息
        if (error.message === 'Failed to fetch') {
          this.error = '上传失败：无法连接到服务器，请检查服务器是否运行';
          this.taskStatus = '上传失败：无法连接到服务器';
        } else if (error.message === '请求超时') {
          this.error = '上传失败：请求超时，服务器响应时间过长';
          this.taskStatus = '上传失败：请求超时';
        } else {
          this.error = `上传失败：${error.message || '未知错误'}`;
          this.taskStatus = '上传失败：' + (error.message || '未知错误');
        }
        
        // 仍然使用本地URL
        console.log('上传失败，将使用本地图片URL');
      } finally {
        this.isLoading = false;
        // 确保imageUrl已设置，否则使用预览URL
        if (!this.formData.imageUrl) {
          this.formData.imageUrl = this.previewImage;
          console.log('使用本地预览图URL作为备用');
        }
        
        // 验证最终设置的imageUrl
        console.log('最终图片URL:', this.formData.imageUrl ? '已设置' : '未设置');
      }
    },

    async generateImage() {
      // 在生成前确认URL存在
      if (!this.formData.imageUrl && this.previewImage) {
        console.log('imageUrl未设置但有预览图，使用预览图作为URL');
        this.formData.imageUrl = this.previewImage;
      }
      
      if (!this.formData.imageUrl) {
        this.error = '请先上传图片';
        return;
      }
      
      console.log('开始处理图片，使用URL:', this.formData.imageUrl.substring(0, 50) + '...');
      
      // 检查提示词是否为空
      if (!this.formData.prompt.trim()) {
        this.error = '请输入提示词或选择风格';
        return;
      }

      this.isLoading = true;
      this.error = null;
      this.resultImage = null;
      this.taskStatus = '正在创建风格转换任务...';

      try {
        // 使用阿里云图片风格调整API创建任务
        let createResponse;
        try {
          console.log('调用阿里云图片风格调整API创建任务...');
          
          // 对于本地预览图或Base64编码，给出错误提示
          if (this.formData.imageUrl.startsWith('data:image')) {
            throw new Error('阿里云API不支持直接使用Base64图片数据，请确保图片已上传到服务器');
          }
          
          // 确保只发送图片URL
          const imageUrl = this.formData.imageUrl;
          
          createResponse = await Promise.race([
            fetch(`${window.APP_CONFIG.API_BASE_URL}/api/v1/image_style/create`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                prompt: this.formData.prompt,
                image_url: imageUrl, // 只发送URL
                n: 1,
                watermark: false
              })
            }),
            new Promise((_, reject) => 
              setTimeout(() => reject(new Error('请求超时')), 15000)
            )
          ]);
        } catch (fetchError) {
          console.error('创建任务请求失败:', fetchError);
          if (fetchError.message === 'Failed to fetch') {
            throw new Error('无法连接到服务器，请检查服务器是否运行');
          } else {
            throw fetchError;
          }
        }
        
        const createResult = await createResponse.json();
        console.log('创建任务响应:', createResult);
        
        if (!createResult.success) {
          throw new Error(createResult.error?.message || '创建任务失败');
        }
        
        this.taskId = createResult.data.task_id;
        console.log('任务创建成功，ID:', this.taskId);
        this.taskStatus = '任务已创建，正在处理中...';
        
        // 开始轮询查询任务状态
        this.startPollingTaskStatus();
      } catch (error) {
        this.isLoading = false;
        
        // 更明确的错误信息
        if (error.message === 'Failed to fetch') {
          this.error = '处理失败：无法连接到服务器，请检查服务器是否运行';
        } else if (error.message === '请求超时') {
          this.error = '处理失败：请求超时，服务器响应时间过长';
        } else {
          this.error = `处理失败：${error.message || '未知错误'}`;
        }
        
        console.error('图片处理失败:', error);
      }
    },

    startPollingTaskStatus() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
      }
      
      let failedAttempts = 0;
      const maxFailedAttempts = 5;
      let pollingCount = 0;
      const maxPollingCount = 60; // 最多轮询60次，约2分钟
      
      this.pollingInterval = setInterval(async () => {
        try {
          pollingCount++;
          console.log(`开始第${pollingCount}次轮询，任务ID: ${this.taskId}`);
          
          // 检查是否超过最大轮询次数
          if (pollingCount > maxPollingCount) {
            console.log(`已达到最大轮询次数(${maxPollingCount})，停止轮询`);
            clearInterval(this.pollingInterval);
            this.isLoading = false;
            this.error = '任务处理时间过长，请稍后在历史记录中查看结果';
            return;
          }
          
          let statusResponse;
          try {
            // 使用阿里云图片风格调整API查询任务
            statusResponse = await Promise.race([
              fetch(`${window.APP_CONFIG.API_BASE_URL}/api/v1/image_style/query/${this.taskId}`, {
                headers: {
                  'Content-Type': 'application/json'
                }
              }),
              new Promise((_, reject) => 
                setTimeout(() => reject(new Error('请求超时')), 5000)
              )
            ]);
          } catch (fetchError) {
            failedAttempts++;
            console.error(`轮询失败 (${failedAttempts}/${maxFailedAttempts}):`, fetchError);
            
            if (failedAttempts >= maxFailedAttempts) {
              throw new Error('多次轮询失败，请检查网络连接');
            }
            
            // 不中断轮询，等待下一次尝试
            this.taskStatus = `查询任务状态失败，将在2秒后重试 (${failedAttempts}/${maxFailedAttempts})`;
            return;
          }
          
          // 重置失败计数
          failedAttempts = 0;
          
          const statusResult = await statusResponse.json();
          console.log('任务状态查询结果:', statusResult);
          
          if (!statusResult.success) {
            throw new Error(statusResult.error || '查询任务状态失败');
          }
          
          // 从阿里云API响应中获取状态信息
          const taskData = statusResult.data;
          const status = taskData.task_status;
          
          // 更新任务状态
          if (status === 'SUCCEEDED' && taskData.image_urls && taskData.image_urls.length > 0) {
            // 任务成功完成，获取第一个图片URL
            clearInterval(this.pollingInterval);
            this.isLoading = false;
            this.taskStatus = '处理完成';
            this.resultImage = taskData.image_urls[0];
            
            // 如果有完成时间，显示
            if (taskData.submit_time && taskData.end_time) {
              this.taskStatus = `处理完成，提交于 ${taskData.submit_time}，完成于 ${taskData.end_time}`;
            }
            
            console.log(`任务完成，结果URL: ${this.resultImage}`);
          } else if (status === 'FAILED' || status === 'ERROR') {
            // 任务失败
            clearInterval(this.pollingInterval);
            this.isLoading = false;
            throw new Error('任务处理失败');
          } else if (status === 'RUNNING' || status === 'PENDING') {
            // 任务处理中
            this.taskStatus = `任务正在${status === 'RUNNING' ? '处理中' : '等待处理'}，请耐心等待...`;
          } else {
            // 其他状态
            this.taskStatus = `任务状态：${status}`;
          }
        } catch (error) {
          clearInterval(this.pollingInterval);
          this.isLoading = false;
          this.error = `处理失败：${error.message || '未知错误'}`;
          console.error('处理任务状态时出错:', error);
        }
      }, 2000); // 每2秒查询一次
    },

    downloadImage(url) {
      const fileName = `风格转换_${new Date().toISOString().slice(0,10)}.jpg`;
      
      // 如果是远程URL，需要先获取图片
      if (url.startsWith('http')) {
        fetch(url)
          .then(response => response.blob())
          .then(blob => {
            const blobUrl = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
          })
          .catch(error => {
            console.error('下载图片失败:', error);
            this.error = '下载图片失败';
          });
      } else {
        // 本地Base64图片直接下载
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    },

    // 添加辅助方法：将DataURL转换为Blob
    dataURLtoBlob(dataURL) {
      return new Promise((resolve) => {
        const arr = dataURL.split(',');
        const mime = arr[0].match(/:(.*?);/)[1];
        const bstr = atob(arr[1]);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n);
        }
        resolve(new Blob([u8arr], { type: mime }));
      });
    }
  },

  beforeUnmount() {
    // 清除轮询定时器
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }
  }
}
</script>

<style>
.content {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-nav h2 {
  font-size: 24px;
  color: #212529;
  margin: 0;
}

.function-container {
  display: flex;
  gap: 24px;
}

.form-container {
  width: 320px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  color: #212529;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title i {
  color: #ba003f;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #212529;
}

.form-group label.required::after {
  content: '*';
  color: #ba003f;
  margin-left: 4px;
}

.upload-area {
  border: 2px dashed #e9ecef;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #f8f9fa;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: #ba003f;
}

.upload-placeholder {
  color: #6c757d;
}

.upload-placeholder i {
  font-size: 48px;
  margin-bottom: 10px;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 4px;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #ba003f;
  outline: none;
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.1);
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.form-group small {
  display: block;
  margin-top: 4px;
  color: #6c757d;
  font-size: 12px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-primary {
  background: #ba003f;
  color: white;
  border: none;
  flex: 2;
}

.btn-primary:hover:not(:disabled) {
  background: #d4004d;
}

.btn-secondary {
  background: white;
  color: #212529;
  border: 1px solid #e9ecef;
  flex: 1;
}

.btn-secondary:hover {
  background: #e9ecef;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.reference-section, .result-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.function-info {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.function-info h4 {
  color: #ba003f;
  margin-top: 0;
  margin-bottom: 10px;
}

.function-tips {
  margin-top: 15px;
}

.function-tips h5 {
  color: #212529;
  margin-bottom: 8px;
}

.function-tips ul {
  padding-left: 20px;
}

.function-tips li {
  margin-bottom: 5px;
  color: #495057;
}

.result-content-wrapper {
  position: relative;
  min-height: 400px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e9ecef;
  border-top-color: #ba003f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 16px;
  color: #212529;
  font-weight: 500;
}

.loading-status {
  margin-top: 8px;
  color: #6c757d;
  font-size: 14px;
}

.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.empty-content {
  text-align: center;
}

.empty-message {
  margin-top: 16px;
  color: #6c757d;
}

.result-comparison {
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-wrap: wrap;
  padding: 20px;
}

.image-container {
  text-align: center;
  flex: 1;
  min-width: 300px;
  margin-bottom: 20px;
}

.image-container h4 {
  margin-bottom: 12px;
  color: #212529;
}

.image-arrow {
  font-size: 32px;
  color: #6c757d;
  margin: 0 20px;
}

.image-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-wrapper:hover .image-overlay {
  opacity: 1;
}

.overlay-button {
  background: #ba003f;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
  font-weight: 500;
}

.overlay-button:hover {
  background: #d4004d;
}

.image-container img {
  display: block;
  width: 100%;
  max-height: 400px;
  object-fit: contain;
}

.error-message {
  margin-top: 16px;
  padding: 12px;
  background: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinning {
  animation: spin 1s linear infinite;
}

@media (max-width: 768px) {
  .function-container {
    flex-direction: column;
  }
  
  .form-container {
    width: 100%;
  }
  
  .image-arrow {
    transform: rotate(90deg);
    margin: 20px 0;
  }
}

.style-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.style-radio-item {
  position: relative;
}

.style-radio-item input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.style-radio-item label {
  display: inline-block;
  padding: 8px 12px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #f8f9fa;
  color: #495057;
}

.style-radio-item input[type="radio"]:checked + label {
  background-color: #ba003f;
  color: white;
  border-color: #ba003f;
}

.style-radio-item input[type="radio"]:focus + label {
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.2);
}

.style-radio-item label:hover {
  background-color: #e9ecef;
  border-color: #ced4da;
}

.style-radio-item input[type="radio"]:checked + label:hover {
  background-color: #d4004d;
  border-color: #d4004d;
}

.style-radio-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.style-radio-item.disabled label {
  cursor: not-allowed;
  color: #6c757d;
  background-color: #e9ecef;
}

.style-radio-item.disabled label:hover {
  background-color: #e9ecef;
  border-color: #e9ecef;
}
</style> 