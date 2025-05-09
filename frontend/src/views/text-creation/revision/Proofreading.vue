<template>
  <div class="text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>文章校对</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showTips">
          <i class="ri-book-read-line"></i>
          知识学习
        </button>
      </div>
    </div>
    
    <!-- 主要内容区域 - 使用两列布局 -->
    <div class="main-container">
      <!-- 左侧：输入参数 -->
      <div class="input-section">
        <div class="section-header">
          <h3 class="section-title">
            <i class="ri-file-text-line"></i>
            文本输入
          </h3>
        </div>
        
        <!-- 移除诗歌类型、主题、风格倾向、背景情景和关键词部分 -->
        
        <!-- 文本输入支持直接输入和上传文件两种形式 -->
        <div class="form-group">
          <label for="text-input" class="required">直接文本输入</label>
          <textarea 
            id="text-input" 
            v-model="textInput" 
            placeholder="请输入需要校对的文本内容（最多1000个汉字）..."
            class="form-control"
            rows="10"
            maxlength="1000"
          ></textarea>
          <div class="text-counter">{{textInput.length}}/1000</div>
        </div>
        
        <div class="form-group">
          <label for="file-upload">上传文件</label>
          <div class="file-upload-container">
            <input 
              type="file" 
              id="file-upload" 
              ref="fileUpload" 
              class="file-input" 
              @change="handleFileUpload" 
              accept=".pdf,.doc,.docx,.txt,.csv,.md,.xls,.xlsx"
            />
            <button class="file-upload-btn" @click="triggerFileUpload">
              <i class="ri-upload-2-line"></i>
              选择文件
            </button>
            <span class="file-upload-hint" v-if="!selectedFile">
              支持PDF、Word、Excel和文本文件等格式
            </span>
            <span class="file-upload-selected" v-else>
              已选择: {{ selectedFile.name }}
              <button class="file-clear-btn" @click="clearSelectedFile">
                <i class="ri-close-line"></i>
              </button>
            </span>
          </div>
          <div class="file-upload-progress" v-if="isUploading">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <span class="progress-text">上传中... {{ uploadProgress }}%</span>
          </div>
        </div>
        
        <!-- 校对选项 -->
        <div class="form-group">
          <label>校对选项</label>
          <div class="checkbox-group">
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.grammar}">
              <input type="checkbox" v-model="checkOptions.grammar">
              <span class="checkbox-label">语法检查</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.spelling}">
              <input type="checkbox" v-model="checkOptions.spelling">
              <span class="checkbox-label">拼写检查</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.punctuation}">
              <input type="checkbox" v-model="checkOptions.punctuation">
              <span class="checkbox-label">标点符号</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.tone}">
              <input type="checkbox" v-model="checkOptions.tone">
              <span class="checkbox-label">语气一致性</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.readability}">
              <input type="checkbox" v-model="checkOptions.readability">
              <span class="checkbox-label">可读性分析</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.format}">
              <input type="checkbox" v-model="checkOptions.format">
              <span class="checkbox-label">格式规范</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.synonym}">
              <input type="checkbox" v-model="checkOptions.synonym">
              <span class="checkbox-label">同义词建议</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.clarity}">
              <input type="checkbox" v-model="checkOptions.clarity">
              <span class="checkbox-label">表达清晰度</span>
            </label>
          </div>
        </div>
        
        <!-- 模型选择 -->
        <div class="form-group">
          <label for="model">AI模型</label>
          <select id="model" v-model="selectedModel" class="form-control">
            <option v-for="model in modelList" :key="model.id" :value="model.id">
              {{ model.name }}
            </option>
          </select>
        </div>
        
        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="generateLongform" class="btn btn-primary" :disabled="isGenerating || (!textInput.trim() && !selectedFile)">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '校对中...' : '开始校对' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：结果 -->
      <div class="right-column">
        <!-- 校对结果 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              校对结果
            </h3>
            <div class="action-buttons">
              <button @click="generateLongform" class="primary-button" :disabled="isGenerating">
                <i class="ri-refresh-line" v-if="!isGenerating"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isGenerating ? '校对中...' : '再次校对' }}
              </button>
              <button @click="copyText" class="secondary-button" :disabled="isGenerating || !generatedNote">
                <i class="ri-file-copy-line"></i>
                复制文本
              </button>
              <button @click="showPrompt" class="prompt-button" :disabled="!lastUsedPrompt">
                <i class="ri-code-line"></i>
                查看提示词
              </button>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isGenerating" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedNote && !isGenerating" class="empty-result">
              <div class="empty-content">
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无校对内容，请点击"开始校对"按钮开始校对</p>
              </div>
            </div>
            
            <div v-else-if="generatedNote" class="note-result" :class="{'blur-content': isGenerating, 'streaming': isStreaming}">
              <textarea v-model="generatedNote" class="result-textarea" readonly></textarea>
              <div v-if="isStreaming" class="streaming-indicator">
                <span class="dot-typing"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 替换原有的弹窗为侧边抽屉 -->
    <el-drawer
      v-model="showTipsModal"
      title="文章校对知识学习"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in articleKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
      </div>
    </el-drawer>

    <!-- 提示词模态框 -->
    <div class="modal" v-if="showPromptModal">
      <div class="modal-content prompt-modal">
        <div class="modal-header">
          <h3><i class="ri-file-text-line"></i> 生成提示词</h3>
          <button class="close-btn" @click="showPromptModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="prompt-content">
            <div v-if="lastUsedPrompt && lastUsedPrompt.length">
              <div v-for="(msg, index) in lastUsedPrompt" :key="index" class="prompt-message">
                <div class="prompt-role">{{ msg.role === 'system' ? '系统提示词' : '用户提示词' }}</div>
                <div class="prompt-text">{{ msg.content }}</div>
              </div>
            </div>
            <div v-else>暂无提示词内容</div>
          </div>
          <div class="prompt-actions">
            <button class="secondary-button" @click="copyPrompt">
              <i class="ri-file-copy-line"></i> 复制提示词
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import '@/assets/css/text-creation-common.css'; // 引入统一CSS样式文件
import { proofreadingKnowledge } from '@/views/Knowledge_data.js';

export default {
  name: 'Proofreading',
  data() {
    return {
      // 文本输入
      textInput: '',
      
      // 文件上传相关
      selectedFile: null,
      isUploading: false,
      uploadProgress: 0,
      
      // 校对选项
      checkOptions: {
        grammar: true,
        spelling: true,
        punctuation: true,
        tone: false,
        readability: false,
        format: false,
        synonym: false,
        clarity: false
      },
      
      // 结果内容
      isGenerating: false,
      loadingText: '正在校对文章，请耐心等待...',
      generatedNote: '',
      lastUsedPrompt: null,
      isStreaming: false,
      
      // 模态框控制
      showTipsModal: false,
      showPromptModal: false,
      
      // 模型选择 - 默认使用火山引擎V3
      selectedModel: 'deepseek-v3',
      modelList: [],
      
      // 添加文章校对知识内容
      articleKnowledge: proofreadingKnowledge
    };
  },
  mounted() {
    this.fetchModelList();
  },
  methods: {
    // 设置默认模型列表
    setupDefaultModels() {
      console.log('使用默认模型列表');
      this.modelList = [
        { id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' },
        { id: 'deepseek-r1', name: 'DeepSeek R1（火山引擎）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎旧版）' },
        { id: 'douban', name: '豆包大模型' }
      ];
      this.selectedModel = 'deepseek-v3';
    },
    
    // 获取可用的大模型列表
    async fetchModelList() {
      try {
        console.log('开始获取模型列表...');
        // 获取模型列表
        const response = await axios.get('/api/v1/llm/models', { timeout: 10000 });
        console.log('获取模型列表响应:', response.data);
        
        if (response.data && response.data.status === 'success') {
          // 过滤模型，只保留火山引擎R1、V3和豆包模型
          let allModels = response.data.data || [];
          this.modelList = allModels.filter(model => 
            model.id === 'deepseek-v3' || 
            model.id === 'deepseek-r1' ||
            model.id === 'deepseek-r1-vol' || 
            model.id === 'douban'
          );
          
          // 确保所有需要的模型都在列表中，没有则添加
          const modelIds = this.modelList.map(model => model.id);
          if (!modelIds.includes('deepseek-v3')) {
            this.modelList.push({ id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' });
          }
          if (!modelIds.includes('deepseek-r1')) {
            this.modelList.push({ id: 'deepseek-r1', name: 'DeepSeek R1（火山引擎）' });
          }
          
          console.log('过滤后的可用模型列表:', this.modelList);
          
          // 如果过滤后没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.setupDefaultModels();
          }
          
          // 默认选择火山引擎V3
          const volcanoModel = this.modelList.find(model => model.id === 'deepseek-v3');
          if (volcanoModel) {
            this.selectedModel = volcanoModel.id;
          } else if (this.modelList.length > 0) {
            this.selectedModel = this.modelList[0].id;
          } else {
            this.selectedModel = 'deepseek-v3';
          }
          
          console.log('已选择模型:', this.selectedModel);
        } else {
          console.error('获取模型列表失败:', response.data?.message);
          this.setupDefaultModels();
        }
      } catch (error) {
        console.error('获取模型列表异常:', error.message);
        if (error.response) {
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
        }
        this.setupDefaultModels();
      }
    },
    
    // 触发文件上传控件点击
    triggerFileUpload() {
      this.$refs.fileUpload.click();
    },
    
    // 临时函数：检查API路径是否存在和可访问
    async checkApiPath() {
      try {
        console.log('测试API路径...');
        // 尝试获取模型列表以检查API是否可访问
        const testResponse = await axios.get('/api/v1/llm/models');
        console.log('API测试结果:', testResponse.data);
        
        // 显示可用模型列表
        if (testResponse.data && testResponse.data.status === 'success' && 
            testResponse.data.data && Array.isArray(testResponse.data.data.models)) {
          console.log('后端支持的模型列表:');
          const models = testResponse.data.data.models;
          models.forEach((model, index) => {
            console.log(`[${index}] ID: ${model.id}, 名称: ${model.name}, 提供商: ${model.provider}`);
          });
        }
        
        return true;
      } catch (error) {
        console.error('API路径测试失败:', error);
        return false;
      }
    },
    
    // 处理文件上传
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      // 检查文件大小（限制为10MB）
      if (file.size > 10 * 1024 * 1024) {
        this.$message ? 
          this.$message.error('文件大小不能超过10MB') : 
          alert('文件大小不能超过10MB');
        return;
      }
      
      // 文件类型检查
      const allowedTypes = [
        'application/pdf', 
        'application/msword', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'text/csv',
        'text/markdown',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      ];
      
      if (!allowedTypes.includes(file.type) && 
          !file.name.match(/\.(pdf|doc|docx|txt|csv|md|xls|xlsx)$/i)) {
        this.$message ? 
          this.$message.error('不支持的文件格式') : 
          alert('不支持的文件格式');
        return;
      }
      
      // 保存选中的文件
      this.selectedFile = file;
      console.log('选择文件:', file.name, '类型:', file.type, '大小:', file.size);
    },
    
    // 清除已选择的文件
    clearSelectedFile() {
      this.selectedFile = null;
      // 重置文件输入控件
      this.$refs.fileUpload.value = '';
    },
    
    // 上传文件并使用流式输出处理校对结果
    async uploadFileWithStreaming() {
      if (!this.selectedFile) return false;
      
      this.isUploading = true;
      this.uploadProgress = 0;
      
      try {
        console.log('========== 第1步：上传文档，读取文档内容 ==========');
        console.log('文件信息:', {
          名称: this.selectedFile.name,
          类型: this.selectedFile.type,
          大小: `${(this.selectedFile.size / 1024).toFixed(2)} KB`
        });
        
        // 创建FormData对象
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        
        // 模型ID映射表 - 从前端选择器ID到后端支持的ID
        const modelMap = {
          'deepseek-v3': 'deepseek-v3-vol', // 火山引擎 DeepSeek V3
          'deepseek-r1': 'deepseek-r1-vol', // 火山引擎 DeepSeek R1
          'deepseek-r1-vol': 'deepseek-r1-vol', // 已经是正确格式
          'douban': 'doubao-pro' // 豆包模型
        };
        
        // 重要：上传文件API需要使用转换后的模型ID
        const originalModelId = this.selectedModel; // 存储原始ID，供后续流式请求使用
        const uploadModelId = modelMap[originalModelId] || originalModelId;
        
        console.log('前端选择的模型ID:', originalModelId);
        console.log('文件上传使用的转换后模型ID:', uploadModelId);
        
        // 使用转换后的模型ID进行文件上传
        formData.append('model', uploadModelId);
        
        // 构建校对提示词
        let prompt = '请对以下文件内容进行校对，';
        
        // 添加校对选项
        prompt += '包括以下方面：';
        
        const options = [];
        if (this.checkOptions.grammar) options.push('语法检查');
        if (this.checkOptions.spelling) options.push('拼写检查');
        if (this.checkOptions.punctuation) options.push('标点符号');
        if (this.checkOptions.tone) options.push('语气一致性');
        if (this.checkOptions.readability) options.push('可读性分析');
        if (this.checkOptions.format) options.push('格式规范');
        if (this.checkOptions.synonym) options.push('同义词建议');
        if (this.checkOptions.clarity) options.push('表达清晰度');
        
        prompt += options.join('、');
        prompt += '。请列出发现的主要问题类型及数量，并按照文本顺序列出具体问题和修改建议。';
        
        formData.append('prompt', prompt);
        
        // 文件上传API路径
        const fileUploadApi = '/api/v1/llm/file_chat';
        
        console.log('文件上传参数:', {
          API路径: fileUploadApi,
          文件名: this.selectedFile.name,
          模型ID: uploadModelId,
          提示词长度: prompt.length
        });
        
        console.log('开始上传文件...');
        
        // 上传文件，获取文本内容
        const uploadResponse = await axios.post(fileUploadApi, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            this.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            console.log(`上传进度: ${this.uploadProgress}%`);
          }
        });
        
        console.log('文件上传完成，响应状态:', uploadResponse.status);
        console.log('文件上传响应数据结构:', Object.keys(uploadResponse.data));
        
        // 检查上传响应
        if (!uploadResponse.data || uploadResponse.data.status !== 'success') {
          console.error('文件上传失败:', uploadResponse.data);
          throw new Error(uploadResponse.data?.message || '文件处理失败');
        }
        
        console.log('文件上传成功，状态:', uploadResponse.data.status);
        
        // 检查响应数据结构
        console.log('响应data字段结构:', Object.keys(uploadResponse.data.data || {}));
        
        // 检查是否有提取的文本
        let extractedText = '';
        
        // 处理不同的响应格式
        if (uploadResponse.data.data && uploadResponse.data.data.extracted_text) {
          extractedText = uploadResponse.data.data.extracted_text;
          console.log('从extracted_text字段提取到文本');
        } else if (uploadResponse.data.data && uploadResponse.data.data.text) {
          extractedText = uploadResponse.data.data.text;
          console.log('从text字段提取到文本');
        } else if (uploadResponse.data.data && typeof uploadResponse.data.data === 'string') {
          extractedText = uploadResponse.data.data;
          console.log('从data字段直接提取到文本');
        } else if (uploadResponse.data.data && uploadResponse.data.data.choices && 
                  uploadResponse.data.data.choices.length > 0 && 
                  uploadResponse.data.data.choices[0].message) {
          
          // 如果已经有完整结果，直接使用
          console.log('发现上传响应中已包含完整的校对结果，直接使用');
          this.generatedNote = uploadResponse.data.data.choices[0].message.content || '';
          return true;
        } else {
          console.error('无法从响应中提取文本内容:', uploadResponse.data);
          throw new Error('无法从上传的文件中提取文本');
        }
        
        console.log('成功提取文本，长度:', extractedText.length);
        if (extractedText.length > 100) {
          console.log('文本前100字符:', extractedText.substring(0, 100) + '...');
        } else {
          console.log('提取的文本:', extractedText);
        }
        
        console.log('第1步完成：成功上传文档并读取内容');
        
        // 保存提取的文本、提示词和原始模型ID，供后续步骤使用
        this._extractedText = extractedText;
        this._prompt = prompt;
        this._originalModelId = originalModelId;
        
        // 继续执行第2步和第3步
        await this.processExtractedText(extractedText, prompt, originalModelId);
        
        return true;
      } catch (error) {
        console.error('文件上传失败:', error);
        
        // 记录所有可能的错误信息
        if (error.response) {
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          
          const errorMsg = error.response.data?.message || error.response.data?.error || '请求参数错误';
          this.$message ? 
            this.$message.error(`文档上传失败: ${errorMsg}`) : 
            alert(`文档上传失败: ${errorMsg}`);
        } else {
          this.$message ? 
            this.$message.error(`文档上传失败: ${error.message || '未知错误'}`) : 
            alert(`文档上传失败: ${error.message || '未知错误'}`);
        }
        
        return false;
      } finally {
        this.isUploading = false;
      }
    },
    
    // 处理第2步和第3步：处理提取的文本并调用流式API
    async processExtractedText(extractedText, prompt, originalModelId) {
      console.log('========== 第2步：整理提示词 ==========');
      // 构建完整提示词（包含文件内容）
      const fullPrompt = `${prompt}\n\n${extractedText}`;
      console.log('完整提示词长度:', fullPrompt.length);
      
      // 保存提示词供后续显示
      this.lastUsedPrompt = [
        { role: "user", content: prompt }
      ];
      
      console.log('第2步完成：成功整理完整提示词');
      
      // 第3步：调用流式API获取结果
      console.log('========== 第3步：调用流式API获取结果 ==========');
      this.generatedNote = '';
      this.isStreaming = true;
      
      // 流式API使用原始模型ID
      console.log('流式请求使用原始模型ID:', originalModelId);
      
      // 流式API路径
      const streamApiUrl = '/api/v1/v1/deepseek_volcano/chat';
      console.log('流式API路径:', streamApiUrl);
      
      try {
        // 构建API请求参数
        const requestParams = {
          model: originalModelId, // 使用原始模型ID
          messages: [{ role: 'user', content: fullPrompt }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        // 记录API请求详情
        console.log('流式请求参数:', {
          model: requestParams.model,
          stream: requestParams.stream,
          temperature: requestParams.temperature,
          max_tokens: requestParams.max_tokens,
          messages_length: requestParams.messages[0].content.length
        });
        
        // 发送流式请求
        const response = await fetch(streamApiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestParams)
        });
        
        console.log('流式响应状态:', response.status);
        
        if (!response.ok) {
          const errorText = await response.text();
          console.error('流式请求错误响应:', errorText);
          throw new Error(`流式请求失败: ${response.status}`);
        }
        
        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 读取流数据
        console.log('开始读取流数据...');
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
            console.log('流式响应完成');
            break;
          }
          
          // 解码二进制数据
          const decoded = decoder.decode(value, { stream: true });
          buffer += decoded;
          
          // 处理收到的数据
          const lines = buffer.split('\n\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (line.trim() === '') continue;
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                console.log('收到结束标志');
                continue;
              }
              
              try {
                const parsed = JSON.parse(data);
                
                // 处理错误消息
                if (parsed.error) {
                  console.error("API错误:", parsed.error);
                  throw new Error(parsed.error.message || '校对失败');
                }
                
                // 处理火山引擎返回的delta格式数据
                if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                  const delta = parsed.choices[0].delta;
                  
                  // 处理内容增量
                  if (delta.content) {
                    // 累加收到的内容
                    this.generatedNote += delta.content;
                  }
                }
              } catch (e) {
                console.error('解析流式数据失败:', e);
              }
            }
          }
        }
        
        console.log('第3步完成，生成校对结果，总字数:', this.generatedNote.length);
        this.$message ? this.$message.success('文章校对完成！') : alert('文章校对完成！');
      } catch (error) {
        console.error('流式请求处理失败:', error);
        this.$message ? 
          this.$message.error(`校对失败: ${error.message || '未知错误'}`) : 
          alert(`校对失败: ${error.message || '未知错误'}`);
      } finally {
        this.isStreaming = false;
      }
    },
    
    // 上传文件到服务器 (非流式方式，备用)
    async uploadFile() {
      if (!this.selectedFile) return null;
      
      this.isUploading = true;
      this.uploadProgress = 0;
      let apiUrl = '/api/v1/llm/file_chat';
      
      try {
        // 检查API是否可用 - 只在开发模式下检查
        if (process.env.NODE_ENV === 'development') {
          try {
            const apiCheck = await this.checkApiPath();
            console.log('API路径检查结果:', apiCheck);
          } catch (e) {
            console.warn('API路径检查失败，将继续尝试上传:', e);
          }
        }
        
        // 创建FormData对象
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        
        // 转换模型ID为后端支持的模型ID格式
        // 模型ID映射表 - 从前端选择器ID到后端支持的ID
        const modelMap = {
          'deepseek-v3': 'deepseek-v3-vol', // 火山引擎 DeepSeek V3
          'deepseek-r1': 'deepseek-r1-vol', // 火山引擎 DeepSeek R1
          'deepseek-r1-vol': 'deepseek-r1-vol', // 已经是正确格式
          'douban': 'doubao-pro' // 豆包模型
        };
        
        // 获取后端支持的模型ID，如果映射中没有则使用原始ID
        const backendModelId = modelMap[this.selectedModel] || this.selectedModel;
        console.log('前端选择的模型ID:', this.selectedModel);
        console.log('转换为后端模型ID:', backendModelId);
        
        formData.append('model', backendModelId);
        
        // 构建校对提示词
        let prompt = '请对以下文件内容进行校对，';
        
        // 添加校对选项
        prompt += '包括以下方面：';
        
        const options = [];
        if (this.checkOptions.grammar) options.push('语法检查');
        if (this.checkOptions.spelling) options.push('拼写检查');
        if (this.checkOptions.punctuation) options.push('标点符号');
        if (this.checkOptions.tone) options.push('语气一致性');
        if (this.checkOptions.readability) options.push('可读性分析');
        if (this.checkOptions.format) options.push('格式规范');
        if (this.checkOptions.synonym) options.push('同义词建议');
        if (this.checkOptions.clarity) options.push('表达清晰度');
        
        prompt += options.join('、');
        
        prompt += '。请列出发现的主要问题类型及数量，并按照文本顺序列出具体问题和修改建议。';
        
        formData.append('prompt', prompt);
        
        console.log('上传文件:', this.selectedFile.name);
        console.log('选择的模型:', this.selectedModel);
        console.log('实际使用的模型ID:', backendModelId);
        console.log('提示词:', prompt);
        console.log('使用API URL:', apiUrl);
        
        // 修正API请求路径，使用正确的路径
        let response;
        try {
          response = await axios.post(apiUrl, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              this.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            },
            // 添加更长的超时时间
            timeout: 90000 // 90秒超时
          });
        } catch (error) {
          console.error('第一次尝试上传失败:', error);
          
          if (error.response && error.response.status === 404) {
            console.log('尝试备用API路径...');
            
            // 尝试备用路径
            const backupUrl = '/api/v1/file_chat/upload';
            console.log('使用备用API URL:', backupUrl);
            
            response = await axios.post(backupUrl, formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              },
              onUploadProgress: (progressEvent) => {
                this.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              },
              timeout: 90000
            });
          } else {
            throw error; // 如果不是404错误，继续向上抛出
          }
        }
        
        console.log('文件上传响应:', response.data);
        
        // 保存提示词供后续显示
        this.lastUsedPrompt = [
          { role: "system", content: "你是一位专业的文章校对专家，能够提供准确、全面的文章校对和修改建议。" },
          { role: "user", content: prompt }
        ];
        
        return response.data;
      } catch (error) {
        console.error('文件上传失败:', error);
        if (error.response) {
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          
          // 根据状态码提供更具体的错误信息
          if (error.response.status === 400) {
            const errorMsg = error.response.data?.message || error.response.data?.error || '请求参数错误';
            this.$message ? 
              this.$message.error(`上传失败: ${errorMsg}`) : 
              alert(`上传失败: ${errorMsg}`);
          } else if (error.response.status === 413) {
            this.$message ? 
              this.$message.error('文件内容过长，超出模型上下文限制') : 
              alert('文件内容过长，超出模型上下文限制');
          } else if (error.response.status === 404) {
            this.$message ? 
              this.$message.error('API路径不存在，请联系系统管理员') : 
              alert('API路径不存在，请联系系统管理员');
          } else {
            this.$message ? 
              this.$message.error(`服务器错误 (${error.response.status})`) : 
              alert(`服务器错误 (${error.response.status})`);
          }
        } else if (error.code === 'ECONNABORTED') {
          this.$message ? 
            this.$message.error('请求超时，服务器处理时间过长') : 
            alert('请求超时，服务器处理时间过长');
        } else {
          this.$message ? 
            this.$message.error(`上传失败: ${error.message || '未知错误'}`) : 
            alert(`上传失败: ${error.message || '未知错误'}`);
        }
        
        // 在开发模式下使用测试数据
        if (process.env.NODE_ENV === 'development') {
          console.log('开发模式：返回模拟数据');
          return {
            status: 'success',
            data: {
              choices: [
                {
                  message: {
                    content: '【文件校对测试结果】\n\n由于API调用失败，这是一个测试响应。在实际环境中，系统会返回真实的校对结果。\n\n【测试问题摘要】\n- 语法问题：3处\n- 拼写错误：2处\n- 标点问题：4处\n\n【测试修改建议】\n1. 测试问题1：语法不通顺\n2. 测试问题2：标点使用错误\n3. 测试问题3：拼写错误'
                  }
                }
              ]
            }
          };
        }
        
        return null;
      } finally {
        this.isUploading = false;
      }
    },
    
    // 生成校对结果的方法
    async generateLongform() {
      // 验证必填字段
      if (!this.validateForm()) {
        return;
      }
      
      this.isGenerating = true;
      this.generatedNote = '';
      this.isStreaming = false;
      
      try {
        // 如果选择了文件，则使用流式方式处理
        if (this.selectedFile) {
          console.log('开始使用流式方式处理文件...');
          this.loadingText = '正在上传和处理文件，请耐心等待...';
          
          // 使用流式方法处理文件
          const streamSuccess = await this.uploadFileWithStreaming();
          
          if (streamSuccess) {
            // 流式处理成功
            this.$message ? this.$message.success('文章校对完成！') : alert('文章校对完成！');
            return;
          } else {
            console.log('流式处理失败，尝试使用非流式方式...');
            // 如果流式失败，尝试使用常规方式
            const uploadResult = await this.uploadFile();
            
            if (uploadResult && uploadResult.status === 'success') {
              console.log('文件处理成功:', uploadResult);
              
              // 根据响应格式处理结果
              if (uploadResult.data && uploadResult.data.choices && uploadResult.data.choices.length > 0) {
                const choice = uploadResult.data.choices[0];
                if (choice.message && choice.message.content) {
                  this.generatedNote = choice.message.content;
                } else {
                  this.generatedNote = '校对成功，但返回格式异常';
                  console.warn('校对结果格式异常:', choice);
                }
              } else {
                // 若返回格式不是期望的格式，尝试其他可能的数据结构
                if (typeof uploadResult.data === 'string') {
                  this.generatedNote = uploadResult.data;
                } else if (uploadResult.data && uploadResult.data.content) {
                  this.generatedNote = uploadResult.data.content;
                } else {
                  console.warn('无法识别的返回格式:', uploadResult);
                  this.generatedNote = '校对成功，但无法解析返回结果';
                }
              }
              
              // 添加成功提示
              this.$message ? this.$message.success('文章校对完成！') : alert('文章校对完成！');
              return;
            } else if (uploadResult && uploadResult.status === 'error') {
              throw new Error(uploadResult.message || uploadResult.error || '文件处理失败');
            } else if (!uploadResult) {
              throw new Error('文件上传失败，请检查网络连接');
            } else {
              throw new Error('未知错误，请稍后重试');
            }
          }
        }
        
        // 如果没有选择文件，使用原有的文本输入处理逻辑
        // 构建提示词
        const prompt = this.generatePrompt();
        
        // 构建API请求参数
        const systemMessage = "你是一位专业的文章校对专家，能够提供准确、全面的文章校对和修改建议。";
        const userMessage = prompt;
        
        const apiMessages = [
          { role: "system", content: systemMessage },
          { role: "user", content: userMessage }
        ];
        
        // 保存apiMessages供后续显示
        this.lastUsedPrompt = apiMessages;
        
        this.loadingText = '正在校对文章，请耐心等待...';
        
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        console.log('开始调用API，模型:', this.selectedModel);
        
        // 准备API参数
        const apiParams = {
          model: this.selectedModel,
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        // 记录API请求详情，方便调试
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        // 开始流式状态
        this.isStreaming = true;
        
        // 使用fetch API发送请求，以处理流式响应
        console.log('开始发送流式请求到:', '/api/v1/v1/deepseek_volcano/chat');
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(apiParams)
        });
        
        console.log('收到响应, 状态码:', response.status);
        console.log('响应头:', {
          'Content-Type': response.headers.get('Content-Type'),
          'Transfer-Encoding': response.headers.get('Transfer-Encoding')
        });
        
        if (!response.ok) {
          throw new Error(`服务器返回错误: ${response.status}`);
        }
        
        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 读取流数据
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
            console.log('流式响应完成');
            break;
          }
          
          // 解码二进制数据
          const decoded = decoder.decode(value, { stream: true });
          console.log('收到数据块:', decoded.length, '字节');
          buffer += decoded;
          
          // 处理收到的数据
          const lines = buffer.split('\n\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (line.trim() === '') continue;
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                console.log('收到结束标志');
                continue;
              }
              
              try {
                console.log('解析数据:', data.substring(0, 100) + '...');
                const parsed = JSON.parse(data);
                console.log('解析后的数据格式:', Object.keys(parsed));
                
                // 处理错误消息
                if (parsed.error) {
                  console.error("API错误:", parsed.error);
                  throw new Error(parsed.error.message || '校对失败');
                }
                
                // 处理火山引擎返回的delta格式数据
                if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                  const delta = parsed.choices[0].delta;
                  
                  // 处理内容增量
                  if (delta.content) {
                    console.log("收到内容增量:", delta.content);
                    // 累加收到的内容
                    this.generatedNote += delta.content;
                  }
                }
              } catch (e) {
                console.error('解析流式数据失败:', e, data);
              }
            }
          }
        }
        
        // 流式响应完成
        this.isStreaming = false;
        console.log('校对完成，总字数:', this.generatedNote.length);
        
        // 添加成功提示
        this.$message ? this.$message.success('文章校对完成！') : alert('文章校对完成！');
          
      } catch (error) {
        console.error('生成校对结果出错，详细错误:', error);
        
        // 更详细的错误日志
        if (error.response) {
          // 服务器响应了，但状态码不在2xx范围
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          this.$message ? 
            this.$message.error(`校对失败: 服务器错误 (${error.response.status})`) : 
            alert(`校对失败: 服务器错误 (${error.response.status})`);
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到服务器响应');
          this.$message ? 
            this.$message.error('校对失败: 服务器无响应，请检查网络连接') : 
            alert('校对失败: 服务器无响应，请检查网络连接');
        } else {
          // 设置请求时发生错误
          console.error('错误信息:', error.message);
          this.$message ? 
            this.$message.error(`校对失败: ${error.message}`) : 
            alert(`校对失败: ${error.message}`);
        }
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          console.log('开发模式：使用示例内容');
          this.generatedNote = `文章校对结果：\n\n【问题摘要】\n- 发现语法错误：3处\n- 发现拼写错误：2处\n- 标点符号问题：4处\n- 表达不清晰：2处\n\n【详细修改建议】\n1. 第一段第二句：语法错误，主语缺失\n   原文："经过多年发展，已成为行业领导者。"\n   建议："经过多年发展，公司已成为行业领导者。"\n\n2. 第二段第一句：标点使用不当\n   原文："然而，研究表明；消费者更关注..."\n   建议："然而，研究表明：消费者更关注..."\n\n3. 第三段：拼写错误\n   原文："这些数据充分表明了该趋是不可逆转的"\n   建议："这些数据充分表明了该趋势是不可逆转的"`;
        }
      } finally {
        this.isGenerating = false;
        this.isStreaming = false;
      }
    },
    
    // 验证表单
    validateForm() {
      // 检查是否至少有文本输入或者上传了文件
      if (!this.textInput.trim() && !this.selectedFile) {
        this.$message ? this.$message.error('请输入需要校对的文本内容或上传文件') : alert('请输入需要校对的文本内容或上传文件');
        return false;
      }
      
      // 检查是否至少选择了一个校对选项
      const hasSelectedOption = Object.values(this.checkOptions).some(value => value === true);
      if (!hasSelectedOption) {
        this.$message ? this.$message.error('请至少选择一个校对选项') : alert('请至少选择一个校对选项');
        return false;
      }
      
      return true;
    },
    
    // 生成提示词
    generatePrompt() {
      let prompt = '请对以下文本进行校对和修改：\n\n';
      
      // 添加文本内容
      prompt += `${this.textInput}\n\n`;
      
      // 添加校对选项
      prompt += '请根据以下选项进行校对：\n';
      
      if (this.checkOptions.grammar) {
        prompt += '- 语法检查：检查语法错误，包括主谓一致、时态、语态等问题\n';
      }
      
      if (this.checkOptions.spelling) {
        prompt += '- 拼写检查：查找并纠正拼写错误、错别字和用词不当\n';
      }
      
      if (this.checkOptions.punctuation) {
        prompt += '- 标点符号：检查标点符号的使用是否正确、缺失或多余\n';
      }
      
      if (this.checkOptions.tone) {
        prompt += '- 语气一致性：检查全文语气是否一致，包括人称和表达方式\n';
      }
      
      if (this.checkOptions.readability) {
        prompt += '- 可读性分析：分析文本的可读性，包括句子长度、复杂度等\n';
      }
      
      if (this.checkOptions.format) {
        prompt += '- 格式规范：检查文本格式是否规范，包括段落划分、缩进等\n';
      }
      
      if (this.checkOptions.synonym) {
        prompt += '- 同义词建议：提供更准确或更生动的同义词替换建议\n';
      }
      
      if (this.checkOptions.clarity) {
        prompt += '- 表达清晰度：检查表达是否清晰，提供改进模糊或冗余表达的建议\n';
      }
      
      // 输出要求
      prompt += '\n请提供以下内容：\n1. 问题摘要：列出发现的主要问题类型及数量\n2. 详细修改建议：按照文本顺序列出具体问题，并提供修改建议\n3. 对于重要问题，请同时提供原文和修改后的建议文本\n';
      
      return prompt;
    },
    
    // 重置表单
    resetForm() {
      this.textInput = '';
      // 清除已选择的文件
      this.selectedFile = null;
      if (this.$refs.fileUpload) {
        this.$refs.fileUpload.value = '';
      }
      
      // 重置校对选项为默认值
      this.checkOptions = {
        grammar: true,
        spelling: true,
        punctuation: true,
        tone: false,
        readability: false,
        format: false,
        synonym: false,
        clarity: false
      };
      this.generatedNote = '';
    },
    
    // 显示创作小贴士
    showTips() {
      this.showTipsModal = true;
    },
    
    // 复制生成的文本
    copyText() {
      if (!this.generatedNote) return;
      
      try {
        navigator.clipboard.writeText(this.generatedNote).then(() => {
          this.$message ? this.$message.success('内容已复制到剪贴板') : alert('内容已复制到剪贴板');
        });
      } catch (error) {
        console.error('复制失败:', error);
        this.$message ? this.$message.error('复制失败，请手动复制') : alert('复制失败，请手动复制');
      }
    },
    
    // 显示提示词模态框
    showPrompt() {
      this.showPromptModal = true;
    },
    
    // 复制提示词到剪贴板
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      
      try {
        let promptText = '';
        if (typeof this.lastUsedPrompt === 'string') {
          promptText = this.lastUsedPrompt;
        } else {
          // 遍历消息数组
          this.lastUsedPrompt.forEach(msg => {
            promptText += `【${msg.role === 'system' ? '系统' : '用户'}】\n${msg.content}\n\n`;
          });
        }
        
        navigator.clipboard.writeText(promptText).then(() => {
          this.$message ? this.$message.success('提示词已复制到剪贴板') : alert('提示词已复制到剪贴板');
        });
      } catch (error) {
        console.error('复制提示词失败:', error);
        this.$message ? this.$message.error('复制失败，请手动复制') : alert('复制失败，请手动复制');
      }
    },
    
    // 下载生成的文本
    downloadText() {
      if (!this.generatedNote) return;
      
      const element = document.createElement('a');
      const file = new Blob([this.generatedNote], {type: 'text/plain'});
      element.href = URL.createObjectURL(file);
      element.download = `校对结果_${new Date().toISOString().slice(0,10)}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    
    // 格式化Markdown文本
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗语法
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理换行
      text = text.replace(/\n\n/g, '</p><p>');
      
      // 处理列表项
      if (text.includes('- ')) {
        const lines = text.split('\n');
        let inList = false;
        let formattedText = '';
        
        for (let line of lines) {
          if (line.trim().startsWith('- ')) {
            if (!inList) {
              formattedText += '<ul>';
              inList = true;
            }
            formattedText += `<li>${line.substring(2).trim()}</li>`;
          } else {
            if (inList) {
              formattedText += '</ul>';
              inList = false;
            }
            formattedText += line + '\n';
          }
        }
        
        if (inList) {
          formattedText += '</ul>';
        }
        
        text = formattedText;
      }
      
      return `<p>${text}</p>`;
    }
  }
};
</script>

<style scoped>
/* 导入统一CSS样式文件 */
@import "@/assets/css/text-creation-common.css";

/* 页面特有样式 - 仅保留未在text-creation-common.css中定义的样式 */

/* 文本计数器 */
.text-counter {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* 文件上传容器 */
.file-upload-container {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.file-input {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.file-upload-btn {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.file-upload-btn:hover {
  background-color: #e9e9e9;
  border-color: #ccc;
}

.file-upload-hint {
  font-size: 13px;
  color: #999;
}

.file-upload-selected {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #333;
  background-color: #f0f0f0;
  padding: 4px 10px;
  border-radius: 4px;
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-clear-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.file-clear-btn:hover {
  background-color: #e0e0e0;
  color: #666;
}

.file-upload-progress {
  margin-top: 10px;
  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--primary-color, #ba003f);
  transition: width 0.3s ease;
}

.progress-text {
  display: block;
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  text-align: right;
}

/* 提示词模态框样式 */
.prompt-modal {
  width: 90%;
  max-width: 900px;
}

.prompt-content {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 20px;
  overflow-x: auto;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  white-space: normal;
  max-height: 60vh;
  overflow-y: auto;
}

.prompt-message {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.prompt-message:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.prompt-role {
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--primary-color, #ba003f);
  font-size: 16px;
}

.prompt-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

/* 特殊按钮样式 */
.prompt-button {
  background-color: white;
  color: var(--primary-color, #ba003f);
  border: 1px solid var(--primary-color, #ba003f);
  padding: 0 16px;
  height: 36px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.2s ease;
}

.prompt-button:hover {
  background-color: rgba(186, 0, 63, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(186, 0, 63, 0.1);
}

.prompt-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  color: #aaa;
  border-color: #e0e0e0;
  transform: none;
  box-shadow: none;
}

/* 添加流式输出相关样式 */
.streaming-indicator {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 5px 10px;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dot-typing {
  position: relative;
  left: -9999px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--primary-color, #ba003f);
  color: var(--primary-color, #ba003f);
  box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  animation: dot-typing 1.5s infinite linear;
}

@keyframes dot-typing {
  0% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  16.667% {
    box-shadow: 9984px -10px 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  33.333% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  50% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px -10px 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  66.667% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  83.333% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px -10px 0 0 var(--primary-color, #ba003f);
  }
  100% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
}

/* 结果区域相关样式 */
.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
}

.result-section {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 650px;
}

.result-content-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
  height: 100%;
  min-height: 590px;
}

.note-result {
  position: relative;
  flex: 1;
  display: flex;
  height: 100%;
  width: 100%;
  overflow: hidden;
  background-color: #fcfcfc;
  border-radius: 0 0 8px 8px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.result-textarea {
  flex: 1;
  width: 100%;
  height: 100%;
  padding: 20px;
  border: none;
  resize: none;
  outline: none;
  background-color: #fcfcfc;
  font-size: 15px;
  line-height: 1.7;
  color: #333;
  overflow-y: auto;
  border-radius: 0 0 8px 8px;
  box-shadow: none;
  font-family: 'PingFang SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  transition: background-color 0.3s;
}

.result-textarea:focus {
  background-color: #fff;
}

/* 增加文本高亮样式 */
.result-textarea::selection {
  background-color: rgba(186, 0, 63, 0.2);
  color: #333;
}

/* 美化滚动条 */
.result-textarea::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.result-textarea::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

.result-textarea::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

.result-textarea::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}
</style> 