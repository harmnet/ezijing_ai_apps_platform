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
          
          <!-- 消息列表 -->
          <div class="message-list" ref="messageList">
            <div v-for="message in messages" :key="message.id" :class="['message', message.role, { 'loading': message.isGenerating && !message.streaming, 'streaming': message.streaming }]">
              <div class="avatar">
                <img v-if="message.role === 'assistant'" src="@/assets/bot-avatar.svg" alt="AI">
                <img v-else src="@/assets/user-avatar.svg" alt="User">
              </div>
              <div class="content">
                <div v-if="message.role === 'assistant'" class="model-name">
                  {{ currentModelName }}
                  <span v-if="message.streaming" class="streaming-indicator">生成中...</span>
                </div>
                <div class="message-content" v-html="formatMessage(message.content)"></div>
                <div v-if="message.isGenerating && !message.streaming" class="thinking-cursor"></div>
                <div v-if="message.attachments && message.attachments.length > 0" class="attachments">
                  <div v-for="(file, index) in message.attachments" :key="index" class="attachment-item">
                    <i class="ri-file-line"></i> {{ file.name }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 思考过程展示 - 修改条件，不再依赖loading状态 -->
            <div v-if="thinkingProcess.length > 0 && isThinkingModel" class="message assistant thinking-message">
              <div class="avatar">
                <img src="@/assets/bot-avatar.svg" alt="AI">
              </div>
              <div class="content thinking-content">
                <div class="model-name">思考过程</div>
                <div class="thinking-steps">
                  <div v-for="(step, index) in thinkingProcess" :key="index" class="thinking-step">
                    <span class="step-number">{{ step.step }}.</span>
                    <span class="step-content">{{ step.content }}</span>
                    <span v-if="index === thinkingProcess.length - 1" class="thinking-cursor"></span>
                  </div>
                </div>
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
      loadingTextIndex: 0,
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
    
    // 为Vue 3添加$set方法的兼容性
    this.$set = (obj, key, value) => {
      if (Array.isArray(obj)) {
        obj.splice(key, 1, value);
      } else {
        obj[key] = value;
      }
    };
    
    // 调试用函数：手动触发思考过程显示
    window.testThinking = () => {
      console.log('开始测试思考过程显示');
      this.showThinking = true;
      this.thinkingProcess = [
        {step: 1, content: '这是测试思考步骤1'},
        {step: 2, content: '这是测试思考步骤2'}
      ];
      console.log('思考过程设置完成:', this.showThinking, this.thinkingProcess);
      this.$forceUpdate();
      console.log('isThinkingModel:', this.isThinkingModel);
      console.log('思考元素是否存在:', !!document.querySelector('.thinking-message'));
    };
  },
  computed: {
    // 判断当前选择的模型是否支持思考过程显示
    // 只有volcanic engine的R1模型支持思考过程
    isThinkingModel() {
      return this.selectedModel && this.selectedModel.includes('deepseek-r1');
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
        // 调整输入框高度
        const textarea = document.getElementById('chat-input');
        if (textarea) {
          textarea.style.height = 'auto';
        }
      });
      
      // 设置加载状态
      this.loading = true;
      
      // 清空思考过程
      this.thinkingProcess = [];
      
      // 初始不显示思考过程UI
      this.showThinking = false;
      
      // 开始加载动画
      this.startRandomLoadingText();
      
      // 立即添加一个临时的AI响应消息，以显示加载状态
      const tempMessageId = Date.now();
      const tempMessage = {
        id: tempMessageId,
        role: 'assistant',
        content: '正在思考您的问题...',
        attachments: [],
        isGenerating: true,
        streaming: true
      };
      
      this.messages.push(tempMessage);
      
      // 滚动到底部显示加载状态
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      
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
        formData.append('return_reasoning', 'true');
      }
      
      // 检查是否是DeepSeek Volcano R1模型
      const isDeepSeekVolcano = this.selectedModel && this.selectedModel.includes('deepseek-r1-vol');
      
      try {
        // 如果有文件，使用文件上传API
        if (fileData) {
          // 调用文件上传API（文件上传暂不支持流式输出）
          const response = await axios.post('/api/v1/llm/file_chat', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          
          this.handleNonStreamResponse(response);
        } 
        // 如果是DeepSeek Volcano R1模型，使用专用的流式接口
        else if (isDeepSeekVolcano) {
          console.log("使用DeepSeek Volcano流式接口...");
          // 对于DeepSeek Volcano的特殊处理，停止轮换加载文本，避免干扰流式输出
          this.stopRandomLoadingText();
          await this.handleDeepSeekVolcanoStream();
        }
        else {
          // 构建发送到API的消息数组（移除attachments字段）
          const apiMessages = this.messages.map(msg => ({
            role: msg.role,
            content: msg.content
          })).filter(m => m.role !== 'system');
          
          // 使用流式输出专用接口
          await this.handleStreamResponse(apiMessages);
        }
        
        // 确保在API调用完成后清除loading状态，无论成功或失败
        this.loading = false;
        this.stopRandomLoadingText();
        
        // 重置文件上传状态
        this.uploadedFile = null;
        if (this.$refs.fileUpload) {
          this.$refs.fileUpload.value = '';
        }
      } catch (error) {
        console.error('API调用失败:', error);
        
        // 显示错误消息
        this.messages.push({
          role: 'assistant',
          content: `<p class="error-message">抱歉，无法连接到服务器。错误信息: ${error.message || '未知错误'}</p>`,
          attachments: []
        });
        
        // 结束加载状态
        this.loading = false;
        this.showThinking = false;
        this.stopRandomLoadingText();
        
        // 重置文件上传状态
        this.uploadedFile = null;
        if (this.$refs.fileUpload) {
          this.$refs.fileUpload.value = '';
        }
        
        // 滚动到底部
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    
    // 处理DeepSeek Volcano流式响应
    async handleDeepSeekVolcanoStream() {
      console.log("处理DeepSeek Volcano流式响应");
      
      try {
        // 查找现有的"正在生成"消息
        const existingGeneratingIndex = this.messages.findIndex(m => m.isGenerating);
        let tempMessageId;
        
        if (existingGeneratingIndex !== -1) {
          // 如果存在，获取其ID并保留原来的消息
          tempMessageId = this.messages[existingGeneratingIndex].id;
          // 将内容清空，准备接收新内容
          this.messages[existingGeneratingIndex].content = '';
          
          // 立即停止加载文本循环，避免干扰流式输出
          this.stopRandomLoadingText();
        } else {
          // 如果不存在，创建一个新的临时消息
          tempMessageId = Date.now();
          const tempMessage = {
            id: tempMessageId,
            role: 'assistant',
            content: '',  // 内容初始为空，不显示默认加载文本
            attachments: [],
            isGenerating: true,
            streaming: true
          };
          
          this.messages.push(tempMessage);
          
          // 立即停止加载文本循环
          this.stopRandomLoadingText();
        }
        
        // 清空思考过程
        this.thinkingProcess = [];
        // 初始不显示思考过程
        this.showThinking = false;
        
        // 构建发送到API的消息数组
        const apiMessages = this.messages.map(msg => ({
          role: msg.role,
          content: msg.content
        })).filter(m => m.role !== 'system');
        
        // 准备请求参数
        const requestBody = {
          messages: apiMessages,
          model: this.selectedModel.replace('-vol', ''), // 将deepseek-r1-vol转换为deepseek-r1
          stream: true,
          return_reasoning: this.isThinkingModel
        };
        
        console.log("发送Volcano流式请求参数:", JSON.stringify(requestBody));
        
        // 使用fetch发起请求
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
          throw new Error(`HTTP错误 ${response.status}: ${response.statusText}`);
        }
        
        console.log("成功建立DeepSeek Volcano SSE连接");
        
        // 获取response body stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 使用while循环手动读取流数据
        while (true) {
          // 读取数据块
          const { done, value } = await reader.read();
          if (done) {
            console.log("DeepSeek Volcano流结束");
            break;
          }
          
          // 解码数据
          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;
          
          // 按行分割数据 - 修正分隔符处理
          const lines = buffer.split('\n\n');
          // 保留最后一个可能不完整的行
          buffer = lines.pop() || '';
          
          // 解析和处理每一行
          for (const line of lines) {
            if (!line.trim() || !line.startsWith('data: ')) continue;
            
            const jsonString = line.substring(6).trim();
            if (jsonString === '[DONE]') {
              console.log('DeepSeek Volcano流结束标记');
              continue;
            }
            
            try {
              const data = JSON.parse(jsonString);
              console.log("收到DeepSeek Volcano数据:", Object.keys(data).join(','));
              
              // 处理数据
              if (data.choices && data.choices.length > 0) {
                const choice = data.choices[0];
                
                // 处理增量内容的delta格式
                if (choice.delta) {
                  // 处理思考过程
                  if (choice.delta.reasoning_content) {
                    console.log(`收到思考内容: '${choice.delta.reasoning_content}'`);
                    
                    // 直接处理思考内容，不再依赖showThinking标志
                    this.processReasoningDelta(choice.delta.reasoning_content);
                    
                    // 确保不再显示加载文本
                    this.stopRandomLoadingText();
                    
                    // 强制立即更新DOM
                    this.$forceUpdate();
                  }
                  
                  // 处理内容增量
                  if (choice.delta.content) {
                    console.log(`收到内容增量: '${choice.delta.content}'`);
                    const msgIndex = this.messages.findIndex(m => m.id === tempMessageId);
                    if (msgIndex !== -1) {
                      // 确保不再显示加载文本
                      this.stopRandomLoadingText();
                      
                      // 直接追加内容，不做条件判断
                      this.messages[msgIndex].content += choice.delta.content;
                      this.$forceUpdate();
                    }
                  }
                }
                // 处理完整消息的message格式
                else if (choice.message) {
                  // 处理思考过程
                  if (choice.message.reasoning_content) {
                    console.log("收到完整思考过程:", choice.message.reasoning_content);
                    this.processFullReasoningContent(choice.message.reasoning_content);
                    this.showThinking = true;
                    this.$forceUpdate();
                  }
                  
                  // 处理完整内容
                  if (choice.message.content) {
                    console.log("收到完整内容:", choice.message.content);
                    const msgIndex = this.messages.findIndex(m => m.id === tempMessageId);
                    if (msgIndex !== -1) {
                      this.messages[msgIndex].content = choice.message.content;
                      this.$forceUpdate();
                    }
                  }
                }
              }
            } catch (error) {
              console.error("解析JSON失败:", error, jsonString);
            }
          }
          
          // 确保滚动到最新消息
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }
        
        // 流结束时更新消息状态
        console.log("更新最终消息状态");
        const finalIndex = this.messages.findIndex(m => m.id === tempMessageId);
        if (finalIndex !== -1) {
          this.messages[finalIndex].isGenerating = false;
          this.messages[finalIndex].streaming = false;
          
          // 如果内容为空，添加默认消息
          if (!this.messages[finalIndex].content.trim()) {
            this.messages[finalIndex].content = "无法获取响应。请重试或联系管理员。";
          }
          
          this.$forceUpdate();
        }
        
      } catch (error) {
        console.error("DeepSeek Volcano流式处理出错:", error);
        throw error;  // 向上层函数传递错误，让它进行统一的错误处理
      }
    },
    
    // 处理非流式响应
    handleNonStreamResponse(response) {
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
        
        // 检查是否有reasoning_content
        const messageObj = response.data.data.choices[0].message;
        let aiResponse = messageObj.content || '';
        const reasoningContent = messageObj.reasoning_content;
        
        // 如果有reasoning_content，添加到思考过程
        if (reasoningContent && this.isThinkingModel) {
          this.thinkingProcess = reasoningContent.split('\n').filter(step => step.trim());
          this.showThinking = true;
        }
        
        // 添加AI回复
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
      
      // 结束加载状态
      this.loading = false;
      this.stopRandomLoadingText();
      
      // 滚动到底部
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    
    // 使用标准的EventSource API处理流式响应
    async handleStreamResponse(apiMessages) {
      console.log("使用EventSource原生方式处理流式响应");
      
      try {
        // 查找现有的"正在生成"消息
        const existingGeneratingIndex = this.messages.findIndex(m => m.isGenerating);
        let tempMessageId;
        
        if (existingGeneratingIndex !== -1) {
          // 如果存在，获取其ID并保留原来的消息
          tempMessageId = this.messages[existingGeneratingIndex].id;
          // 将内容清空，准备接收新内容
          this.messages[existingGeneratingIndex].content = '';
        } else {
          // 如果不存在，创建一个新的临时消息
          tempMessageId = Date.now();
          const tempMessage = {
            id: tempMessageId,
            role: 'assistant',
            content: this.isThinkingModel ? '' : '正在生成中...',
            attachments: [],
            isGenerating: true,
            streaming: true
          };
          
          this.messages.push(tempMessage);
        }
        
        // 清空思考过程
        this.thinkingProcess = [];
        // 初始不显示思考过程
        this.showThinking = false;
        
        // 准备请求参数
        const apiParams = {
          model: this.selectedModel,
          messages: apiMessages,
          temperature: 0.7, 
          max_tokens: 2000,
          stream: true,
          stream_options: {
            include_usage: true
          }
        };
        
        // 对R1模型启用思考过程返回
        if (this.isThinkingModel) {
          console.log("启用思考过程返回");
          apiParams.return_reasoning = true;
        }
        
        console.log("发送请求参数:", JSON.stringify(apiParams));
        
        // 使用fetch进行POST请求初始化SSE连接
        let endpoint = '/api/v1/llm/chat/stream';
        
        // 对于非R1模型，可能需要使用不同的端点
        if (!this.isThinkingModel) {
          // 如果后端提供了统一的流式端点，使用同一个端点并设置合适的参数
          apiParams.stream = true;
        }
        
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(apiParams)
        });
        
        if (!response.ok) {
          throw new Error(`HTTP错误 ${response.status}`);
        }
        
        console.log("成功建立SSE连接");
        
        // 获取response body stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 使用while循环手动读取流数据
        while (true) {
          // 读取数据块
          const { done, value } = await reader.read();
          if (done) {
            console.log("SSE流结束");
            break;
          }
          
          // 解码数据
          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;
          
          console.log(`收到数据块: ${buffer.length}字节`);
          
          // 按行分割数据
          const lines = buffer.split('\n');
          // 保留最后一个可能不完整的行
          buffer = lines.pop() || '';
          
          // 解析和处理每一行
          for (const line of lines) {
            if (!line.trim() || !line.startsWith('data:')) continue;
            
            const jsonString = line.substring(5).trim();
            if (jsonString === '[DONE]') {
              console.log('流结束标记');
              continue;
            }
            
            try {
              const data = JSON.parse(jsonString);
              console.log("收到数据:", Object.keys(data).join(','), data);
              
              // 处理不同的数据格式
              if (data.choices && data.choices.length > 0) {
                const choice = data.choices[0];
                
                // 处理增量内容的delta格式
                if (choice.delta) {
                  // 处理思考过程
                  if (choice.delta.reasoning_content) {
                    console.log(`收到思考内容: '${choice.delta.reasoning_content}'`);
                    
                    // 直接处理思考内容，不再依赖showThinking标志
                    this.processReasoningDelta(choice.delta.reasoning_content);
                    
                    // 确保不再显示加载文本
                    this.stopRandomLoadingText();
                    
                    // 强制立即更新DOM
                    this.$forceUpdate();
                  }
                  
                  // 处理内容增量
                  if (choice.delta.content) {
                    console.log(`收到内容增量: '${choice.delta.content}'`);
                    const msgIndex = this.messages.findIndex(m => m.id === tempMessageId);
                    if (msgIndex !== -1) {
                      // 如果是第一次收到内容，停止循环显示加载文本
                      if (this.messages[msgIndex].content === '正在思考您的问题...' ||
                          this.loadingTexts.includes(this.messages[msgIndex].content)) {
                        this.messages[msgIndex].content = choice.delta.content;
                        // 停止加载文本循环
                        this.stopRandomLoadingText();
                      } else {
                        this.messages[msgIndex].content += choice.delta.content;
                      }
                      this.$forceUpdate();
                    }
                  }
                }
                // 处理完整消息的message格式
                else if (choice.message) {
                  // 处理思考过程
                  if (choice.message.reasoning_content) {
                    console.log("收到完整思考过程:", choice.message.reasoning_content);
                    this.processFullReasoningContent(choice.message.reasoning_content);
                    this.showThinking = true;
                    this.$forceUpdate();
                  }
                  
                  // 处理完整内容
                  if (choice.message.content) {
                    console.log("收到完整内容:", choice.message.content);
                    const msgIndex = this.messages.findIndex(m => m.id === tempMessageId);
                    if (msgIndex !== -1) {
                      this.messages[msgIndex].content = choice.message.content;
                      this.$forceUpdate();
                    }
                  }
                }
              }
              // 处理包含usage信息但没有choices的结束帧
              else if (data.usage && !data.choices) {
                console.log("收到usage信息:", data.usage);
              }
              
            } catch (error) {
              console.error("解析JSON失败:", error, jsonString);
            }
          }
          
          // 确保滚动到最新消息
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }
        
        // 流结束时更新消息状态
        console.log("更新最终消息状态");
        const finalIndex = this.messages.findIndex(m => m.id === tempMessageId);
        if (finalIndex !== -1) {
          this.messages[finalIndex].isGenerating = false;
          this.messages[finalIndex].streaming = false;
        }
        
        // 重置加载状态
        this.loading = false;
        
        // 最后滚动到底部
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error("流式处理异常:", error);
        
        // 显示错误消息
        this.messages.push({
          role: 'assistant',
          content: `流式输出错误: ${error.message || '未知错误'}`,
          attachments: []
        });
        
        // 结束加载状态
        this.loading = false;
        this.showThinking = false;
      }
    },
    clearChat() {
      this.messages = [];
    },
    autoResize(event) {
      const textarea = event.target;
      textarea.style.height = 'auto';
      textarea.style.height = (textarea.scrollHeight < 300 ? textarea.scrollHeight : 300) + 'px';
    },
    scrollToBottom() {
      const chatMessages = document.getElementById('chat-messages');
      chatMessages.scrollTop = chatMessages.scrollHeight;
    },
    startRandomLoadingText() {
      // 清除可能存在的旧定时器
      this.stopRandomLoadingText();
      
      // 随机选择加载文本并定时更改
      this.loadingTextIndex = 0;
      this.loadingTextInterval = setInterval(() => {
        // 循环显示不同的加载文本
        const loadingMessage = this.messages.find(m => m.isGenerating && m.streaming);
        if (loadingMessage) {
          this.loadingTextIndex = (this.loadingTextIndex + 1) % this.loadingTexts.length;
          loadingMessage.content = this.loadingTexts[this.loadingTextIndex];
          this.$forceUpdate();
        } else {
          // 如果没有正在加载的消息，清除定时器
          this.stopRandomLoadingText();
        }
      }, 3000); // 每3秒切换一次提示文本
      
      // 需要跟踪加载状态
      this.loading = true;
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
    },
    // 修改思考过程处理方法
    processFullReasoningContent(content) {
      if (!content) return;
      
      console.log("处理完整思考过程:", content);
      
      // 如果思考过程为空但接收到了内容，确保显示
      if (content.trim()) {
        this.showThinking = true;
      }
      
      // 按段落或行分割
      const steps = content.split(/\n+/).filter(step => step.trim());
      
      if (steps.length === 0) {
        // 如果没有明显的分段，将整个内容作为一步
        if (content.trim()) {
          this.thinkingProcess = [{
            step: 1,
            content: content.trim()
          }];
          console.log("将整个内容作为单个思考步骤");
        } else {
          console.log("未找到有效的思考步骤");
          return;
        }
      } else {
        // 重置思考过程
        this.thinkingProcess = [];
        
        // 添加每个步骤
        steps.forEach((step, index) => {
          this.thinkingProcess.push({
            step: index + 1,
            content: step.trim()
          });
        });
      }
      
      // 确保思考过程显示
      if (this.isThinkingModel && this.thinkingProcess.length > 0) {
        console.log("显示思考过程, 共", this.thinkingProcess.length, "步骤");
        this.showThinking = true;
        
        // 强制视图更新
        this.$forceUpdate();
        
        // 滚动到思考过程区域
        this.$nextTick(() => {
          const thinkingElement = document.querySelector('.thinking-message');
          if (thinkingElement) {
            thinkingElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
          }
        });
      }
    },
    // 修改格式化消息的方法，添加对技术内容的高亮支持
    formatMessage(content) {
      if (!content) return '';
      
      console.log("格式化消息内容，长度:", content.length);
      
      // 确保content是字符串
      const contentStr = String(content);
      
      // 使用标记换行符并转换为HTML
      let formattedContent = contentStr
        .replace(/\n/g, '<br>') // 换行符转为HTML的<br>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **粗体**
        .replace(/\*(.*?)\*/g, '<em>$1</em>'); // *斜体*
        
      // 高亮代码块
      formattedContent = formattedContent.replace(
        /```([\s\S]*?)```/g, 
        '<pre><code>$1</code></pre>'
      );
      
      // 高亮行内代码
      formattedContent = formattedContent.replace(
        /`([^`]+)`/g, 
        '<code>$1</code>'
      );
      
      return formattedContent;
    },
    // 处理增量思考内容 - 简化为直接添加到数组
    processReasoningDelta(reasoningDelta) {
      console.log('处理增量思考内容:', reasoningDelta);
      
      // 第一次收到思考内容
      if (this.thinkingProcess.length === 0) {
        // 创建第一个步骤
        this.thinkingProcess.push({
          step: 1,
          content: reasoningDelta
        });
        console.log('创建第一个思考步骤');
      } else {
        // 附加到现有步骤
        const lastIndex = this.thinkingProcess.length - 1;
        this.thinkingProcess[lastIndex].content += reasoningDelta;
        console.log('附加到现有步骤');
      }
      
      // 强制视图更新
      this.$forceUpdate();
      console.log('思考过程步骤数量:', this.thinkingProcess.length);
      
      // 确保滚动到思考过程区域
      this.$nextTick(() => {
        const thinkingElement = document.querySelector('.thinking-message');
        if (thinkingElement) {
          thinkingElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
      });
    },
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

.avatar {
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

.message.assistant .avatar {
  background-color: #ba003f;
  color: white;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.content {
  max-width: 80%;
  background-color: #f0f0f0;
  border-radius: 12px;
  padding: 12px 16px;
  position: relative;
}

.message.user .content {
  background-color: #fae7ec; /* 紫荆红的浅色背景 */
  border-top-right-radius: 0;
  border: 1px solid rgba(186, 0, 63, 0.15); /* 淡边框 */
  box-shadow: 0 1px 2px rgba(186, 0, 63, 0.1); /* 轻微阴影 */
}

.message.assistant .content {
  background-color: #f9f9f9;
  border-top-left-radius: 0;
}

.model-name {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.streaming-indicator {
  display: inline-block;
  font-size: 11px;
  color: #ba003f;
  padding: 1px 6px;
  border-radius: 10px;
  background-color: rgba(186, 0, 63, 0.1);
  margin-left: 5px;
  animation: fadeInOut 1.5s infinite;
}

.message-content {
  font-size: 15px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-content p {
  margin-bottom: 10px;
}

.message-content p:last-child {
  margin-bottom: 0;
}

.message-content ol, .message-content ul {
  margin: 10px 0;
  padding-left: 20px;
}

.message-content li {
  margin-bottom: 5px;
}

/* 用户头像背景色也改为紫荆红 */
.message.user .avatar {
  background-color: #ba003f;
  color: white;
}

/* 增强用户消息内容的文字样式 */
.message.user .message-content {
  color: #454545;
  font-weight: 500;
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
  max-height: 300px;
  min-height: 60px;
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
  .feature-section {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .suggestion-cards {
    grid-template-columns: 1fr;
  }
  
  .content {
    max-width: 90%;
  }
}

.error-message {
  color: #e74c3c;
  font-weight: 500;
}

/* 思考过程样式 */
.thinking-message {
  opacity: 1;
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 12px;
  background-color: #fffcfd;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.thinking-steps {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.thinking-step {
  display: flex;
  align-items: flex-start;
  line-height: 1.5;
  padding: 8px 12px;
  background-color: rgba(186, 0, 63, 0.05);
  border-radius: 8px;
  border-left: 3px solid #ba003f !important;
}

/* 恢复缺失的.step-number样式 */
.step-number {
  font-weight: 600;
  margin-right: 8px;
  color: #ba003f;
  min-width: 20px;
}

.step-content {
  flex: 1;
  white-space: pre-wrap;
  word-break: break-word;
}

.thinking-cursor {
  display: inline-block;
  width: 2px;
  height: 16px;
  background-color: #ba003f;
  margin-left: 4px;
  vertical-align: middle;
  animation: blink 0.8s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
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

/* 文件上传相关样式 */
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

/* 生成中动画 */
.generating-indicator {
  margin-top: 5px;
  display: flex;
  align-items: center;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #666;
  margin: 0 3px;
  animation: pulse 1.5s infinite ease-in-out;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.4;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 消息布局固定样式 */
.message-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background-color: #e0e0e0;
  font-size: 1.5rem;
  margin: 0 10px;
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

/* 添加消息流式样式 */
.message.assistant.streaming .message-content {
  border-left: 3px solid #ba003f !important;
  position: relative;
  padding-left: 10px;
}

/* 增加加载指示器 */
.message.assistant.streaming:after {
  content: "";
  position: absolute;
  right: 15px;
  bottom: 15px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #ba003f;
  animation: pulseDot 1s infinite;
}

@keyframes pulseDot {
  0%, 100% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.3);
  }
}

/* 流式加载时添加打字光标效果 */
.message.assistant.streaming .message-content:after {
  content: "";
  display: inline-block;
  width: 2px;
  height: 14px;
  background-color: #ba003f;
  margin-left: 3px;
  vertical-align: middle;
  animation: blink 0.8s infinite;
}
</style> 