<template>
  <div class="ai-chat-page">
    <!-- Toast提示 -->
    <div v-if="showToastMessage" class="toast-message">
      {{ toastMessage }}
    </div>
    
    <div class="chat-interface">
      <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
          <div v-if="messages.length === 0" class="welcome-section">
            <div class="welcome-header">
              <h1>欢迎使用人工智能应用与高效办公实践教学平台</h1>
            </div>
            
            <div class="feature-section">
              <div class="feature-card">
                <i class="ri-robot-line"></i>
                <h3>智能问答</h3>
                <p>回答各类问题，提供精准信息</p>
              </div>
              <div class="feature-card">
                <i class="ri-file-text-line"></i>
                <h3>文案创作</h3>
                <p>生成高质量文章、脚本和营销文案</p>
              </div>
              <div class="feature-card">
                <i class="ri-code-line"></i>
                <h3>代码编写</h3>
                <p>辅助编程，解决技术难题</p>
              </div>
              <div class="feature-card">
                <i class="ri-lightbulb-line"></i>
                <h3>创意激发</h3>
                <p>提供创意灵感，拓展思维边界</p>
              </div>
            </div>
            
            <div class="suggestion-section">
              <h3>你可以这样问我</h3>
              <div class="suggestion-cards">
                <div class="suggestion-card" @click="usePrompt('我想学习新的编程语言，可以给我一些建议吗？')">
                  <p>我想学习新的编程语言，可以给我一些建议吗？</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('帮我写一份产品发布会的演讲稿')">
                  <p>帮我写一份产品发布会的演讲稿</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('解释一下量子计算的基本原理')">
                  <p>解释一下量子计算的基本原理</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('分析当前人工智能发展的主要趋势')">
                  <p>分析当前人工智能发展的主要趋势</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 对话内容 -->
          <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
            <div class="message-avatar">
              <i v-if="message.role === 'user'" class="ri-user-line"></i>
              <i v-else class="ri-robot-line"></i>
            </div>
            <div class="message-content">
              <!-- 如果包含附件信息，则分离显示 -->
              <template v-if="message.attachments && message.attachments.length > 0">
                <div class="message-attachments">
                  <div v-for="(attachment, idx) in message.attachments" :key="idx" class="message-attachment">
                    <i :class="getFileIcon(attachment.type)"></i>
                    <span>{{ attachment.name }}</span>
                  </div>
                </div>
              </template>
              <div class="message-text" v-html="message.content"></div>
            </div>
          </div>
          
          <!-- 思考过程展示 -->
          <div v-if="loading && showThinking" class="message assistant thinking-message">
            <div class="message-avatar">
              <i class="ri-robot-line"></i>
            </div>
            <div class="message-content thinking-content">
              <div class="model-name">{{ currentModelName }} 思考过程:</div>
              <div class="thinking-steps">
                <div v-for="(step, index) in thinkingProcess" :key="index" class="thinking-step">
                  <span class="step-number">{{ index + 1 }}.</span>
                  <span class="step-content">{{ step }}</span>
                  <span v-if="index === thinkingProcess.length - 1" class="thinking-cursor"></span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 加载动画 -->
          <div v-if="loading && !showThinking" class="message assistant loading-message">
            <div class="message-avatar">
              <i class="ri-robot-line"></i>
            </div>
            <div class="message-content loading-content">
              <div class="thinking-text">{{ loadingText }}</div>
              <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-input-wrapper">
          <!-- 选择模型和按钮组放在上方 -->
          <div class="chat-input-actions-row">
            <div class="model-selector">
              <label for="model-select">模型:</label>
              <select id="model-select" class="model-select" v-model="selectedModel">
                <option v-for="model in availableModels" :key="model.id" :value="model.id">{{ model.name }}</option>
              </select>
            </div>
            <div class="chat-actions">
              <button class="toolbar-btn" @click="clearChat" title="清空对话">
                <i class="ri-delete-bin-line"></i>
                <span>清空</span>
              </button>
            </div>
          </div>
          
          <!-- 对话输入框放在下方 -->
          <div class="chat-input-container">
            <textarea 
              id="chat-input" 
              v-model="userInput" 
              placeholder="请输入您的问题..." 
              rows="1"
              @input="autoResize"
              @keydown.enter.exact.prevent="sendMessage"
            ></textarea>
            <!-- 在输入框内部右侧显示附件信息 -->
            <div v-if="uploadedFile" class="inline-file-info">
              <i :class="getFileIcon(uploadedFile.type)"></i>
              <span class="file-name">{{ uploadedFile.name.length > 15 ? uploadedFile.name.substring(0, 15) + '...' : uploadedFile.name }}</span>
              <span class="file-size">{{ formatFileSize(uploadedFile.size) }}</span>
              <button class="inline-remove-btn" @click="removeUploadedFile" title="移除文件">
                <i class="ri-close-line"></i>
              </button>
            </div>
            <div class="chat-input-actions">
              <input 
                type="file" 
                id="file-upload" 
                ref="fileUpload" 
                @change="handleFileUpload" 
                style="display: none"
                accept=".pdf,.doc,.docx,.xls,.xlsx,.txt,.csv"
              />
              <button 
                class="input-action-btn" 
                :class="{'disabled-btn': uploadedFile}" 
                :title="uploadedFile ? '已上传文件，发送或删除后可再次上传' : '上传文件'" 
                @click="triggerFileUpload"
              >
                <i class="ri-attachment-2"></i>
              </button>
              <button class="send-btn" @click="sendMessage" :disabled="!userInput.trim() && !uploadedFile">
                <i class="ri-send-plane-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AIChat',
  data() {
    return {
      messages: [],
      userInput: '',
      selectedModel: 'deepseek-v3-vol',
      loading: false,
      availableModels: [],
      loadingText: 'AI正在思考...',
      loadingTexts: [
        'AI正在思考...',
        '正在查询相关知识...',
        '正在整理思路...',
        '正在组织语言...',
        '请稍等片刻...',
        '即将为您解答...',
        '正在分析您的问题...',
        '思考中...',
      ],
      thinkingProcess: [], // 存储思考过程
      showThinking: false, // 是否显示思考过程
      loadingTextInterval: null,
      uploadedFile: null,
      toastMessage: '',
      showToastMessage: false,
      toastTimeout: null
    }
  },
  created() {
    this.fetchAvailableModels();
  },
  computed: {
    // 判断当前选择的模型是否支持思考过程显示
    // 只有R1模型和千问32B模型支持显示思考过程
    isThinkingModel() {
      return ['deepseek-r1-sf', 'deepseek-r1-vol', 'qwq-32b'].includes(this.selectedModel);
    },
    // 获取当前模型的名称
    currentModelName() {
      const model = this.availableModels.find(m => m.id === this.selectedModel);
      return model ? model.name : this.selectedModel;
    }
  },
  methods: {
    async fetchAvailableModels() {
      try {
        const response = await axios.get('/api/v1/llm/models');
        console.log('获取模型响应:', response); // 添加日志，帮助调试
        
        if (response.data.status === 'success') {
          // 获取模型列表
          const models = response.data.data;
          
          // 按照指定顺序排序模型
          const orderedModelIds = [
            'deepseek-r1-sf',   // DeepSeek-R1（硅基流动）
            'deepseek-v3-sf',   // DeepSeek-V3（硅基流动）
            'deepseek-r1-vol',  // DeepSeek-R1（火山引擎）
            'deepseek-v3-vol',  // DeepSeek-V3（火山引擎）
            'qwq-32b',          // 通义千问-32B（硅基流动）
            'qwen-max',         // 通义千问-Max（阿里云）
            'doubao-pro'        // 豆包-Pro（火山引擎）
          ];
          
          // 按指定顺序排序
          this.availableModels = orderedModelIds
            .map(id => models.find(model => model.id === id))
            .filter(model => model !== undefined);
          
          console.log('可用模型:', this.availableModels); // 添加日志，检查模型列表
          
          // 如果没有找到默认选择的模型，设置为第一个可用模型
          if (!this.availableModels.find(model => model.id === this.selectedModel) && this.availableModels.length > 0) {
            this.selectedModel = this.availableModels[0].id;
          }
          
          // 如果没有可用模型，创建一个默认列表作为备用
          if (this.availableModels.length === 0) {
            this.availableModels = [
              { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
              { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
              { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
              { id: 'deepseek-v3-vol', name: 'DeepSeek-V3（火山引擎）' },
              { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
            ];
            this.selectedModel = 'deepseek-v3-vol';
          }
        } else {
          console.error('获取模型列表失败:', response.data.message);
          // 创建默认模型列表作为备用
          this.createFallbackModels();
        }
      } catch (error) {
        console.error('获取模型列表异常:', error);
        // 创建默认模型列表作为备用
        this.createFallbackModels();
      }
    },
    
    // 创建备用模型列表
    createFallbackModels() {
      this.availableModels = [
        { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-v3-vol', name: 'DeepSeek-V3（火山引擎）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
    },
    usePrompt(text) {
      this.userInput = text;
      this.sendMessage();
    },
    async sendMessage() {
      // 如果既没有输入文本也没有上传文件，则不发送请求
      if ((!this.userInput.trim() && !this.uploadedFile) || this.loading) return;
      
      // 准备用户消息对象
      const userMessageObj = {
        role: 'user',
        content: this.userInput.trim(),
        attachments: []
      };
      
      // 如果上传了文件，添加附件信息
      if (this.uploadedFile) {
        userMessageObj.attachments.push({
          name: this.uploadedFile.name,
          type: this.uploadedFile.type,
          size: this.uploadedFile.size
        });
      }
      
      // 添加用户消息到对话列表
      this.messages.push(userMessageObj);
      
      const userMessage = this.userInput;
      this.userInput = '';
      
      // 滚动到底部
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      
      // 设置加载状态
      this.loading = true;
      
      // 清空思考过程
      this.thinkingProcess = [];
      
      // 如果是支持思考过程的模型，显示思考UI
      if (this.isThinkingModel) {
        this.showThinking = true;
        this.startRandomLoadingText(); // 在思考过程加载期间显示加载动画
      } else {
        this.showThinking = false;
        this.startRandomLoadingText();
      }
      
      // 准备要发送的数据
      const formData = new FormData();
      
      // 如果上传了文件，将文件添加到请求中
      const fileInput = this.$refs.fileUpload;
      let fileData = null;
      
      if (this.uploadedFile && fileInput.files.length > 0) {
        fileData = fileInput.files[0];
        formData.append('file', fileData);
      }
      
      // 添加其他参数
      formData.append('model', this.selectedModel);
      formData.append('prompt', userMessage);
      
      if (this.isThinkingModel) {
        formData.append('return_thinking', 'true');
      }
      
      try {
        // 如果有文件，使用文件上传API
        let response;
        
        if (fileData) {
          // 调用文件上传API
          response = await axios.post('/api/v1/llm/file_chat', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        } else {
          // 没有文件，使用常规API
          // 构建发送到API的消息数组（移除attachments字段）
          const apiMessages = this.messages.map(msg => ({
            role: msg.role,
            content: msg.content
          })).filter(m => m.role !== 'system');
          
          const apiParams = {
            model: this.selectedModel,
            messages: apiMessages,
            temperature: 0.7,
            max_tokens: 2000
          };
          
          if (this.isThinkingModel) {
            apiParams.return_thinking = true;
          }
          
          response = await axios.post('/api/v1/llm/chat', apiParams);
        }
        
        if (response.data.status === 'success') {
          // 如果是支持思考过程的模型且返回了思考过程，则显示
          if (this.isThinkingModel && response.data.data.thinking) {
            const thinkingData = response.data.data.thinking;
            // 处理思考过程数据，确保是数组形式
            if (Array.isArray(thinkingData)) {
              this.thinkingProcess = thinkingData;
            } else if (typeof thinkingData === 'string') {
              // 如果返回的是字符串，尝试将其分割为步骤
              this.thinkingProcess = thinkingData.split('\n').filter(step => step.trim());
            } else {
              // 如果是对象或其他格式，将其转为字符串
              this.thinkingProcess = [JSON.stringify(thinkingData)];
            }
            
            // 短暂延迟以确保用户能看到思考过程
            setTimeout(() => {
              this.showThinking = true;
            }, 500);
          }
          
          // 添加AI回复
          const aiResponse = response.data.data.choices[0].message.content;
          this.messages.push({
            role: 'assistant',
            content: aiResponse,
            attachments: []
          });
        } else {
          // 处理错误
          this.messages.push({
            role: 'assistant',
            content: `<p class="error-message">抱歉，处理请求时出错: ${response.data.message}</p>`,
            attachments: []
          });
        }
      } catch (error) {
        console.error('API调用失败:', error);
        
        // 显示错误消息
        this.messages.push({
          role: 'assistant',
          content: `<p class="error-message">抱歉，无法连接到服务器。请稍后再试。</p>`,
          attachments: []
        });
      } finally {
        // 无论成功或失败，都结束加载状态
        this.loading = false;
        this.stopRandomLoadingText();
        
        // 重置文件上传状态
        this.uploadedFile = null;
        this.$refs.fileUpload.value = '';
        
        // 思考过程在显示一段时间后隐藏
        if (this.showThinking) {
          setTimeout(() => {
            this.showThinking = false;
          }, 5000); // 显示5秒后隐藏
        }
        
        // 滚动到底部
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    clearChat() {
      this.messages = [];
    },
    autoResize(event) {
      const textarea = event.target;
      textarea.style.height = 'auto';
      textarea.style.height = (textarea.scrollHeight < 150 ? textarea.scrollHeight : 150) + 'px';
    },
    scrollToBottom() {
      const chatMessages = document.getElementById('chat-messages');
      chatMessages.scrollTop = chatMessages.scrollHeight;
    },
    startRandomLoadingText() {
      // 清除可能存在的旧定时器
      this.stopRandomLoadingText();
      
      // 立即设置一个随机文本
      this.loadingText = this.loadingTexts[Math.floor(Math.random() * this.loadingTexts.length)];
      
      // 每2.5秒随机更换加载文本
      this.loadingTextInterval = setInterval(() => {
        this.loadingText = this.loadingTexts[Math.floor(Math.random() * this.loadingTexts.length)];
      }, 2500);
    },
    stopRandomLoadingText() {
      if (this.loadingTextInterval) {
        clearInterval(this.loadingTextInterval);
        this.loadingTextInterval = null;
      }
    },
    getSuggestions() {
      return [
        '解释一下量子计算的基本原理',
        '帮我写一首关于春天的诗',
        '如何提高英语口语水平？',
        '详细介绍下中国的传统节日',
        '人工智能会对就业市场产生什么影响？',
        '如何学习编程？推荐一些入门资源'
      ];
    },
    getFeatures() {
      return [
        { icon: 'ri-brain-line', title: '智能对话', desc: '与先进AI模型自然交流' },
        { icon: 'ri-customer-service-2-line', title: '多模型支持', desc: '支持多种先进大语言模型' },
        { icon: 'ri-history-line', title: '对话历史', desc: '保存和恢复之前的对话' },
        { icon: 'ri-lock-line', title: '安全可靠', desc: '确保用户数据安全与隐私' }
      ];
    },
    selectSuggestion(suggestion) {
      this.userInput = suggestion;
      this.sendMessage();
    },
    handleFileUpload(event) {
      // 如果没有选择文件，直接返回
      if (!event.target.files || event.target.files.length === 0) {
        return;
      }

      // 如果已经上传了文件，显示提示并返回
      if (this.uploadedFile) {
        // 清空文件输入框，防止重复触发
        this.$refs.fileUpload.value = '';
        
        // 由于已经设置了按钮为禁用状态，这种情况通常不会触发
        // 但为了防止用户通过其他方式（如拖放）尝试上传第二个文件
        this.$nextTick(() => {
          // 显示toast提示
          this.showToast('一次只能上传一个文件，请先发送或删除当前文件');
        });
        return;
      }

      const file = event.target.files[0];
      if (file) {
        // 检查文件大小，限制为10MB
        if (file.size > 10 * 1024 * 1024) {
          this.$refs.fileUpload.value = '';
          this.showToast('文件大小不能超过10MB');
          return;
        }
        
        this.uploadedFile = {
          name: file.name,
          size: file.size,
          type: file.type
        };
        
        // 自动聚焦输入框，方便用户输入提示文字
        this.$nextTick(() => {
          document.getElementById('chat-input').focus();
        });
      }
    },
    triggerFileUpload() {
      // 如果已经上传了文件，不执行任何操作
      if (this.uploadedFile) {
        this.showToast('一次只能上传一个文件，请先发送或删除当前文件');
        return;
      }
      this.$refs.fileUpload.click();
    },
    removeUploadedFile() {
      this.uploadedFile = null;
    },
    getFileIcon(type) {
      // 根据文件类型返回相应的图标类名
      switch (type) {
        case 'application/pdf':
          return 'ri-file-pdf-line';
        case 'application/msword':
        case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
          return 'ri-file-word-line';
        case 'application/vnd.ms-excel':
        case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
          return 'ri-file-excel-line';
        case 'text/csv':
          return 'ri-file-csv-line';
        case 'text/plain':
          return 'ri-file-text-line';
        default:
          return 'ri-file-line';
      }
    },
    formatFileSize(size) {
      if (size < 1024) {
        return size + ' B';
      } else if (size < 1024 * 1024) {
        return (size / 1024).toFixed(2) + ' KB';
      } else if (size < 1024 * 1024 * 1024) {
        return (size / (1024 * 1024)).toFixed(2) + ' MB';
      } else {
        return (size / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
      }
    },
    // 显示简单的toast提示
    showToast(message) {
      if (this.toastTimeout) {
        clearTimeout(this.toastTimeout);
      }
      
      this.toastMessage = message;
      this.showToastMessage = true;
      
      this.toastTimeout = setTimeout(() => {
        this.showToastMessage = false;
      }, 3000);
    }
  },
  beforeUnmount() {
    this.stopRandomLoadingText();
  },
}
</script>

<style scoped>
/* 主容器样式 */
.ai-chat-page {
  padding: 0;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f9f9f9;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 聊天消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

/* 欢迎区域样式 */
.welcome-section {
  padding: 20px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

.welcome-header {
  text-align: center;
  margin-bottom: 30px;
}

.welcome-header h1 {
  font-size: 26px;
  font-weight: 600;
  color: #ba003f;
  margin-bottom: 10px;
}

.feature-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.feature-card i {
  font-size: 36px;
  color: #ba003f;
  margin-bottom: 10px;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

.feature-card p {
  font-size: 14px;
  color: #666;
}

.suggestion-section {
  padding: 20px;
  border-top: 1px solid #eee;
  margin-top: 20px;
}

.suggestion-section h3 {
  text-align: center;
  margin-bottom: 20px;
}

.suggestion-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.suggestion-card {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.suggestion-card:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

.suggestion-card p {
  margin: 0;
  font-size: 14px;
  color: #444;
}

/* 消息样式 */
.message {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
  flex-shrink: 0;
}

.message.assistant .message-avatar {
  background-color: #ba003f;
  color: white;
}

.message-avatar i {
  font-size: 20px;
}

.message-content {
  max-width: 80%;
  background-color: #f0f0f0;
  border-radius: 12px;
  padding: 12px 16px;
  position: relative;
}

.message.user .message-content {
  background-color: #fae7ec; /* 紫荆红的浅色背景 */
  border-top-right-radius: 0;
  border: 1px solid rgba(186, 0, 63, 0.15); /* 淡边框 */
  box-shadow: 0 1px 2px rgba(186, 0, 63, 0.1); /* 轻微阴影 */
}

.message.assistant .message-content {
  background-color: #f9f9f9;
  border-top-left-radius: 0;
}

.message-text {
  font-size: 15px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-text p {
  margin-bottom: 10px;
}

.message-text p:last-child {
  margin-bottom: 0;
}

.message-text ol, .message-text ul {
  margin: 10px 0;
  padding-left: 20px;
}

.message-text li {
  margin-bottom: 5px;
}

/* 用户头像背景色也改为紫荆红 */
.message.user .message-avatar {
  background-color: #ba003f;
  color: white;
}

/* 增强用户消息内容的文字样式 */
.message.user .message-text {
  color: #454545;
  font-weight: 500;
}

/* 用户消息的前置小三角 */
.message.user .message-content::before {
  content: '';
  display: block;
  width: 40px;
  height: 40px;
  position: absolute;
  top: 0;
  right: -30px;
  background-color: transparent;
  border-left: 10px solid #fae7ec; /* 与背景色相同 */
  border-top-left-radius: 50%;
  transform: rotate(-45deg);
  z-index: -1;
}

/* 输入区域样式 */
.chat-input-wrapper {
  padding: 15px;
  border-top: 1px solid #eee;
  background-color: #fff;
}

.chat-input-actions-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff; /* 改为白色背景 */
  border-radius: 5px;
  padding: 5px 10px;
  font-size: 14px;
  margin-bottom: 10px;
  border: 1px solid #eee;
}

.model-selector {
  display: flex;
  align-items: center;
}

.model-select {
  background: none;
  border: none;
  font-size: 14px;
  color: #333;
  padding: 2px 5px;
  cursor: pointer;
  outline: none;
  min-width: 180px; /* 确保下拉框有足够宽度 */
  appearance: auto; /* 确保下拉箭头显示 */
}

.chat-actions {
  display: flex;
  align-items: center;
  gap: 5px;
}

.toolbar-btn {
  background: none;
  border: none;
  color: #666;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.toolbar-btn:hover {
  background-color: #f0f0f0;
  color: #ba003f;
}

.chat-input-container {
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 10px 15px;
  transition: box-shadow 0.3s;
  margin-top: 10px;
  border: 1px solid #eee;
  position: relative;
}

.chat-input-container:focus-within {
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.2);
  border-color: #ba003f;
}

textarea {
  flex: 1;
  border: none;
  background: none;
  resize: none;
  outline: none;
  font-size: 15px;
  line-height: 1.5;
  max-height: 150px;
  overflow-y: auto;
  padding: 0;
  color: #333;
}

.chat-input-actions {
  display: flex;
  align-items: center;
  gap: 5px;
}

.input-action-btn {
  background: none;
  border: none;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.2s;
}

.input-action-btn:hover {
  background-color: #f0f0f0;
}

.send-btn {
  background-color: #ba003f;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-btn:hover {
  background-color: #d4154f;
}

.send-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .feature-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .suggestion-cards {
    grid-template-columns: 1fr;
  }
  
  .message-content {
    max-width: 90%;
  }
}

.error-message {
  color: #e74c3c;
  font-weight: 500;
}

.message.assistant .message-content {
  background-color: #f9f9f9;
  border-top-left-radius: 0;
  position: relative;
}

.message.assistant .message-content::before {
  content: '';
  display: block;
  width: 40px;
  height: 40px;
  position: absolute;
  top: 0;
  left: -30px;
  background-color: transparent;
  border-right: 10px solid #f9f9f9;
  border-top-right-radius: 50%;
  transform: rotate(45deg);
  z-index: -1;
}

.loading {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.loading::after {
  content: "AI正在思考...";
  display: inline-block;
  animation: dots 1.5s infinite;
  color: #666;
}

@keyframes dots {
  0%, 20% { content: "AI正在思考"; }
  40% { content: "AI正在思考."; }
  60% { content: "AI正在思考.."; }
  80%, 100% { content: "AI正在思考..."; }
}

/* 加载动画样式 */
.loading-message {
  animation: fadeIn 0.3s ease-in-out;
}

.loading-content {
  padding: 15px;
  min-width: 120px;
}

.thinking-text {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  text-align: center;
  animation: fadeInOut 2s infinite;
}

@keyframes fadeInOut {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.loading-dots {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-dots span {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ba003f;
  margin: 0 3px;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% { 
    transform: scale(0);
  } 40% { 
    transform: scale(1.0);
  }
}

/* 思考过程样式 */
.thinking-message {
  animation: fadeIn 0.3s ease-in-out;
}

.thinking-content {
  padding: 15px;
  width: 90%;
}

.model-name {
  font-weight: 600;
  color: #444;
  margin-bottom: 10px;
  font-size: 14px;
}

.thinking-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.thinking-step {
  display: flex;
  align-items: flex-start;
  font-size: 14px;
  color: #555;
  line-height: 1.5;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #f9f9f9;
  animation: stepFadeIn 0.5s ease-in-out;
}

.step-number {
  font-weight: 600;
  margin-right: 6px;
  color: #ba003f;
  min-width: 20px;
}

.thinking-cursor {
  display: inline-block;
  width: 8px;
  height: 16px;
  background-color: #ba003f;
  margin-left: 8px;
  animation: blink 1s infinite;
}

@keyframes stepFadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes blink {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

/* 添加附件样式 */
.attached-file {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #f2f2f2;
  border-radius: 8px;
  padding: 8px 12px;
  margin-top: 8px;
  font-size: 14px;
  color: #666;
  width: fit-content;
}

.file-upload-info {
  margin: 10px 0 15px;
  padding: 10px 12px;
  background-color: rgba(186, 0, 63, 0.05);
  border-radius: 8px;
  border: 1px dashed rgba(186, 0, 63, 0.2);
  transition: all 0.3s;
}

.file-upload-info:hover {
  background-color: rgba(186, 0, 63, 0.08);
}

.file-info {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #444;
}

.file-info i {
  font-size: 20px;
}

.file-size {
  color: #666;
  font-size: 12px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 8px;
  border-radius: 10px;
}

.remove-file-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 2px 5px;
  margin-left: auto;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-file-btn:hover {
  background-color: rgba(186, 0, 63, 0.1);
  color: #ba003f;
}

/* 附件显示样式 */
.message-attachments {
  margin-bottom: 10px;
  background-color: rgba(249, 249, 249, 0.7);
  border-radius: 8px;
  padding: 8px;
  border: 1px solid #eee;
}

.message.user .message-attachments {
  background-color: rgba(250, 231, 236, 0.7);
  border: 1px solid rgba(186, 0, 63, 0.1);
}

.message-attachment {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px;
  font-size: 14px;
  color: #555;
  border-radius: 4px;
}

.message-attachment i {
  font-size: 18px;
  color: #ba003f;
}

.message.user .message-attachment i {
  color: #ba003f;
}

.message.assistant .message-attachment i {
  color: #1976d2;
}

/* 为不同文件类型添加颜色 */
.ri-file-pdf-line {
  color: #f44336 !important;
}

.ri-file-word-line {
  color: #2196f3 !important;
}

.ri-file-excel-line {
  color: #4caf50 !important;
}

.ri-file-text-line {
  color: #607d8b !important;
}

.ri-file-csv-line {
  color: #ff9800 !important;
}

/* 优化输入框内附件信息的样式 */
.inline-file-info {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: rgba(186, 0, 63, 0.05);
  border: 1px solid rgba(186, 0, 63, 0.1);
  right: 90px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  max-width: 240px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  z-index: 10;
}

.inline-file-info i {
  font-size: 14px;
}

.file-name {
  color: #555;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  color: #777;
  font-size: 11px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 1px 5px;
  border-radius: 10px;
}

.inline-remove-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 2px;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.inline-remove-btn:hover {
  background-color: rgba(186, 0, 63, 0.1);
  color: #ba003f;
}

/* 禁用状态的按钮样式 */
.disabled-btn {
  opacity: 0.5;
  cursor: not-allowed !important;
}

.disabled-btn:hover {
  background-color: transparent !important;
}

/* Toast提示样式 */
.toast-message {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  z-index: 1000;
  animation: fadeInOut 0.3s ease-in-out;
}
</style> 