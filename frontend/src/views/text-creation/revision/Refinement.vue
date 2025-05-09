<template>
  <div class="text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>文章润色</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showTips">
          <i class="ri-lightbulb-line"></i>
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
            placeholder="请输入需要润色的文本内容（最多1000个汉字）..."
            class="form-control"
            rows="10"
            maxlength="1000"
          ></textarea>
          <div class="text-counter">{{textInput.length}}/1000</div>
        </div>
        
        <!-- 注释掉上传文件功能
        <div class="form-group">
          <label for="file-upload">上传文件</label>
          <div class="file-upload-container">
            <button class="file-upload-btn" disabled>
              <i class="ri-upload-2-line"></i>
              选择文件
            </button>
            <span class="file-upload-hint">文件上传功能暂不可用</span>
          </div>
        </div>
        -->
        
        <!-- 润色风格 -->
        <div class="form-group">
          <label>润色风格</label>
          <div class="radio-group">
            <div class="radio-item" :class="{'radio-active': refinementStyle === 'general'}">
              <input type="radio" v-model="refinementStyle" value="general" name="style" id="style-general">
              <label class="radio-label" for="style-general">通用改进</label>
            </div>
            <div class="radio-item" :class="{'radio-active': refinementStyle === 'academic'}">
              <input type="radio" v-model="refinementStyle" value="academic" name="style" id="style-academic">
              <label class="radio-label" for="style-academic">学术论文</label>
            </div>
            <div class="radio-item" :class="{'radio-active': refinementStyle === 'business'}">
              <input type="radio" v-model="refinementStyle" value="business" name="style" id="style-business">
              <label class="radio-label" for="style-business">商务正式</label>
            </div>
            <div class="radio-item" :class="{'radio-active': refinementStyle === 'creative'}">
              <input type="radio" v-model="refinementStyle" value="creative" name="style" id="style-creative">
              <label class="radio-label" for="style-creative">创意文学</label>
            </div>
            <div class="radio-item" :class="{'radio-active': refinementStyle === 'news'}">
              <input type="radio" v-model="refinementStyle" value="news" name="style" id="style-news">
              <label class="radio-label" for="style-news">新闻报道</label>
            </div>
            <div class="radio-item" :class="{'radio-active': refinementStyle === 'technical'}">
              <input type="radio" v-model="refinementStyle" value="technical" name="style" id="style-technical">
              <label class="radio-label" for="style-technical">技术文档</label>
            </div>
          </div>
        </div>
        
        <!-- 润色选项 -->
        <div class="form-group">
          <label>润色选项</label>
          <div class="checkbox-group">
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.grammar}">
              <input type="checkbox" v-model="refineOptions.grammar" id="grammar">
              <label class="checkbox-label" for="grammar">改进语法</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.punctuation}">
              <input type="checkbox" v-model="refineOptions.punctuation" id="punctuation">
              <label class="checkbox-label" for="punctuation">标点优化</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.wording}">
              <input type="checkbox" v-model="refineOptions.wording" id="wording">
              <label class="checkbox-label" for="wording">用词优化</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.clarity}">
              <input type="checkbox" v-model="refineOptions.clarity" id="clarity">
              <label class="checkbox-label" for="clarity">增强清晰度</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.coherence}">
              <input type="checkbox" v-model="refineOptions.coherence" id="coherence">
              <label class="checkbox-label" for="coherence">增强连贯性</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.concise}">
              <input type="checkbox" v-model="refineOptions.concise" id="concise">
              <label class="checkbox-label" for="concise">精简表达</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.attractive}">
              <input type="checkbox" v-model="refineOptions.attractive" id="attractive">
              <label class="checkbox-label" for="attractive">提升吸引力</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': refineOptions.tone}">
              <input type="checkbox" v-model="refineOptions.tone" id="tone">
              <label class="checkbox-label" for="tone">调整语气</label>
            </div>
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
          <button @click="generateLongform" class="btn btn-primary" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '润色中...' : '开始润色' }}
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
              润色结果
            </h3>
            <div class="action-buttons">
              <button @click="generateLongform" class="primary-button" :disabled="isGenerating">
                <i class="ri-refresh-line" v-if="!isGenerating"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isGenerating ? '润色中...' : '再次润色' }}
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
            <div v-if="isGenerating && !isStreaming" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedNote && !isGenerating" class="empty-result">
              <div class="empty-content">
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无内容，请点击"开始润色"按钮开始润色</p>
              </div>
            </div>
            
            <div v-else-if="generatedNote || isStreaming" class="note-result" :class="{'blur-content': isGenerating && !isStreaming, 'streaming': isStreaming}">
              <textarea v-model="generatedNote" class="result-textarea" readonly></textarea>
              <div v-if="isStreaming" class="streaming-indicator">
                <span class="dot-typing"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态框 -->
    <el-drawer
      v-model="showTipsModal"
      title="文章润色知识学习"
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
          <h3><i class="ri-file-text-line"></i> 润色提示词</h3>
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
import { refinementKnowledge } from '@/views/Knowledge_data.js'; // 引入文章润色知识数据
import { ElDrawer } from 'element-plus'; // 引入Element Plus的Drawer组件

export default {
  name: 'Refinement',
  components: {
    ElDrawer
  },
  data() {
    return {
      // 文本输入
      textInput: '',
      
      // 润色选项
      refineOptions: {
        grammar: false,
        punctuation: true,
        wording: true,
        clarity: false,
        coherence: false,
        concise: false,
        attractive: false,
        tone: false
      },
      
      // 结果内容
      isGenerating: false,
      loadingText: 'AI正在拼命润色文章，请耐心等待...',
      generatedNote: '',
      lastUsedPrompt: null,
      
      // 模态框控制
      showTipsModal: false,
      showPromptModal: false,
      
      // 模型选择 - 默认使用火山引擎V3
      selectedModel: 'deepseek-v3',
      modelList: [],
      
      // 润色风格
      refinementStyle: 'general',
      
      // 添加文章润色知识数据
      articleKnowledge: refinementKnowledge,
      
      // 流式输出相关状态
      isStreaming: false
    };
  },
  mounted() {
    this.fetchModelList();
  },
  methods: {
    // 获取可用的大模型列表
    async fetchModelList() {
      try {
        console.log('开始获取模型列表...');
        // 获取模型列表
        const response = await axios.get('/api/v1/llm/models', { timeout: 10000 });
        console.log('获取模型列表响应:', response.data);
        
        if (response.data && response.data.status === 'success') {
          // 过滤模型列表，只保留火山引擎的R1和V3大模型以及豆包大模型
          const allModels = response.data.data || [];
          const allowedModelIds = ['deepseek-v3', 'deepseek-r1-vol', 'douban'];
          this.modelList = allModels.filter(model => allowedModelIds.includes(model.id));
          
          console.log('过滤后的模型列表:', this.modelList);
          
          // 如果过滤后没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.setupDefaultModels();
          }
          
          // 默认选择火山引擎V3
          if (!this.selectedModel) {
            const volcanoModel = this.modelList.find(model => model.id === 'deepseek-v3');
            this.selectedModel = volcanoModel ? volcanoModel.id : 'deepseek-v3';
            console.log('已选择模型:', this.selectedModel);
          }
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
    
    // 设置默认模型列表
    setupDefaultModels() {
      console.log('使用默认模型列表');
      this.modelList = [
        { id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'douban', name: '豆包大模型' }
        // 以下模型已注释掉
        // { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        // { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        // { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3';
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
        // 构建提示词
        const prompt = this.generatePrompt();
        
        // 构建API请求
        const systemMessage = "你是一位专业的文章校对专家，能够提供准确、全面的文章校对和修改建议。";
        const userMessage = prompt;
        
        const apiMessages = [
          { role: "system", content: systemMessage },
          { role: "user", content: userMessage }
        ];
        
        // 保存apiMessages供后续显示
        this.lastUsedPrompt = apiMessages;
        
        this.loadingText = 'AI正在拼命润色文章，请耐心等待...';
        
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        // 调用流式API获取结果
        await this.callStreamingApi(prompt);
        
        // 添加成功提示
        this.$message ? this.$message.success('文章润色完成！') : alert('文章润色完成！');
      } catch (error) {
        console.error('生成润色结果出错，详细错误:', error);
        
        // 更详细的错误日志
        if (error.response) {
          // 服务器响应了，但状态码不在2xx范围
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          this.$message ? 
            this.$message.error(`润色失败: 服务器错误 (${error.response.status})`) : 
            alert(`润色失败: 服务器错误 (${error.response.status})`);
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到服务器响应');
          this.$message ? 
            this.$message.error('润色失败: 服务器无响应，请检查网络连接') : 
            alert('润色失败: 服务器无响应，请检查网络连接');
        } else {
          // 设置请求时发生错误
          console.error('错误信息:', error.message);
          this.$message ? 
            this.$message.error(`润色失败: ${error.message}`) : 
            alert(`润色失败: ${error.message}`);
        }
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          console.log('开发模式：使用示例内容');
          this.generatedNote = `文章润色结果：\n\n【润色摘要】\n- 优化语法结构：3处\n- 改进用词选择：5处\n- 提升表达清晰度：4处\n- 增强文章连贯性：2处\n\n【详细润色建议】\n1. 第一段第二句：增强表达清晰度\n   原文："经过多年发展，已成为行业领导者。"\n   润色："经过多年的稳健发展，公司已跻身行业领军企业的行列，引领着行业发展方向。"\n\n2. 第二段第一句：改进用词和标点\n   原文："然而，研究表明；消费者更关注产品质量而非价格。"\n   润色："然而，近期研究清晰表明：消费者愈发重视产品质量，而价格因素的影响力正在减弱。"\n\n3. 第三段：提升表达吸引力\n   原文："这些数据充分表明了该趋势是不可逆转的。"\n   润色："这些令人信服的数据不仅验证了这一趋势的存在，更预示着这一转变将持续深入，不可逆转。"\n\n4. 整体建议：\n   - 适当增加过渡词，增强段落间的连贯性\n   - 引入更多具体数据或案例，增强论证力度\n   - 结尾部分可以增加对未来的展望，使文章更加完整`;
        }
      } finally {
        this.isGenerating = false;
        this.isStreaming = false;
      }
    },
    
    // 调用流式API
    async callStreamingApi(prompt) {
      console.log('===== 调用流式API开始 =====');
      console.log('当前isStreaming状态:', this.isStreaming);
      console.log('当前generatedNote长度:', this.generatedNote ? this.generatedNote.length : 0);
      
      try {
        // 检查是否有可用模型
        if (!this.selectedModel) {
          console.error('未选择模型');
          throw new Error('请选择AI模型');
        }
        
        // 构建API请求消息
        const messages = [{ role: 'user', content: prompt }];
        
        // 构建API请求参数
        const apiParams = {
          model: this.selectedModel,
          messages: messages,
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        console.log(`正在调用流式API，使用模型: ${this.selectedModel}，提示词长度: ${prompt.length}`);
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        // 开始流式输出状态
        this.isStreaming = true;
        
        // 发送API请求，使用fetch API来处理流式响应
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
                  throw new Error(parsed.error.message || '生成文案失败');
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
        
        // 处理完成，移除流式状态
        this.isStreaming = false;
        console.log('流式响应处理完成，生成的内容长度:', this.generatedNote.length);
        
      } catch (error) {
        console.error('流式API调用异常:', error);
        // 结束流式状态
        this.isStreaming = false;
        throw error;
      }
    },
    
    // 验证表单
    validateForm() {
      if (!this.textInput.trim()) {
        this.$message ? this.$message.error('请输入需要润色的文本内容') : alert('请输入需要润色的文本内容');
        return false;
      }
      
      // 检查是否至少选择了一个校对选项
      const hasSelectedOption = Object.values(this.refineOptions).some(value => value === true);
      if (!hasSelectedOption) {
        this.$message ? this.$message.error('请至少选择一个润色选项') : alert('请至少选择一个润色选项');
        return false;
      }
      
      return true;
    },
    
    // 生成提示词
    generatePrompt() {
      let prompt = '请对以下文本进行润色和修改：\n\n';
      
      // 添加文本内容
      prompt += `${this.textInput}\n\n`;
      
      // 添加润色选项
      prompt += '请根据以下选项进行润色：\n';
      
      if (this.refineOptions.grammar) {
        prompt += '- 语法检查：检查语法错误，包括主谓一致、时态、语态等问题\n';
      }
      
      if (this.refineOptions.punctuation) {
        prompt += '- 标点符号：检查标点符号的使用是否正确、缺失或多余\n';
      }
      
      if (this.refineOptions.wording) {
        prompt += '- 用词优化：优化文本中的用词，使其更加准确、生动或符合语境\n';
      }
      
      if (this.refineOptions.clarity) {
        prompt += '- 增强清晰度：增强文本的清晰度，提供改进模糊或冗余表达的建议\n';
      }
      
      if (this.refineOptions.coherence) {
        prompt += '- 增强连贯性：增强文本的连贯性，提供改进段落组织和句子连接的建议\n';
      }
      
      if (this.refineOptions.concise) {
        prompt += '- 精简表达：精简文本，去除冗余，提供更简洁明了的表达建议\n';
      }
      
      if (this.refineOptions.attractive) {
        prompt += '- 提升吸引力：提升文本的吸引力，提供增强情感表达和故事性的建议\n';
      }
      
      if (this.refineOptions.tone) {
        prompt += '- 调整语气：调整文本的语气，使其更加符合文章的风格和目的\n';
      }
      
      // 输出要求
      prompt += '\n请提供以下内容：\n1. 问题摘要：列出发现的主要问题类型及数量\n2. 详细修改建议：按照文本顺序列出具体问题，并提供修改建议\n3. 对于重要问题，请同时提供原文和修改后的建议文本\n4. 请给出润色之后的完整内容\n';
      
      return prompt;
    },
    
    // 重置表单
    resetForm() {
      this.textInput = '';
      // 重置润色选项为默认值
      this.refineOptions = {
        grammar: false,
        punctuation: true,
        wording: true,
        clarity: false,
        coherence: false,
        concise: false,
        attractive: false,
        tone: false
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
      element.download = `润色结果_${new Date().toISOString().slice(0,10)}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    
    // 添加格式化Markdown的方法
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理粗体文本
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理列表项
      text = text.replace(/\n\n/g, '<br><br>');
      
      return text;
    }
  }
};
</script>

<style scoped>
@import '@/assets/css/text-creation-common.css';

.longform-article-page {
  padding: 0;
  margin-top: -40px;
}

/* 表单元素自定义样式 */
.text-counter {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.file-upload-container {
  border: 1px dashed #ddd;
  border-radius: 6px;
  padding: 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #f9f9f9;
}

.file-upload-btn {
  background-color: #f0f0f0;
  color: #888;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: all 0.3s;
}

.file-upload-btn:not(:disabled):hover {
  background-color: #e0e0e0;
  color: #555;
}

.file-upload-hint {
  display: block;
  font-size: 13px;
  color: #999;
}

/* 结果区域 */
.note-result {
  flex: 1;
  padding: 15px;
  overflow: hidden;
  display: flex;
  height: 100%;
  position: relative;
}

.result-textarea {
  width: 100%;
  height: 100%;
  min-height: 350px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 6px;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  resize: none;
  background-color: #f9f9f9;
  outline: none;
  overflow-y: auto;
  transition: border-color 0.3s;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  white-space: pre-wrap;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.result-textarea:focus {
  border-color: var(--primary-color, #ba003f);
}

/* 流式输出相关样式 */
.streaming .result-textarea {
  border-color: var(--primary-color, #ba003f);
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.2);
}

.streaming-indicator {
  position: absolute;
  bottom: 25px;
  right: 30px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 5px 10px;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.dot-typing {
  position: relative;
  left: -9999px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--primary-color, #ba003f);
  color: var(--primary-color, #ba003f);
  box-shadow: 9984px 0 0 0 currentColor, 9999px 0 0 0 currentColor, 10014px 0 0 0 currentColor;
  animation: dot-typing 1.5s infinite linear;
  display: inline-block;
}

@keyframes dot-typing {
  0% {
    box-shadow: 9984px 0 0 0 currentColor, 9999px 0 0 0 currentColor, 10014px 0 0 0 currentColor;
  }
  16.667% {
    box-shadow: 9984px -6px 0 0 currentColor, 9999px 0 0 0 currentColor, 10014px 0 0 0 currentColor;
  }
  33.333% {
    box-shadow: 9984px 0 0 0 currentColor, 9999px 0 0 0 currentColor, 10014px 0 0 0 currentColor;
  }
  50% {
    box-shadow: 9984px 0 0 0 currentColor, 9999px -6px 0 0 currentColor, 10014px 0 0 0 currentColor;
  }
  66.667% {
    box-shadow: 9984px 0 0 0 currentColor, 9999px 0 0 0 currentColor, 10014px 0 0 0 currentColor;
  }
  83.333% {
    box-shadow: 9984px 0 0 0 currentColor, 9999px 0 0 0 currentColor, 10014px -6px 0 0 currentColor;
  }
  100% {
    box-shadow: 9984px 0 0 0 currentColor, 9999px 0 0 0 currentColor, 10014px 0 0 0 currentColor;
  }
}

/* 提示词相关样式 */
.prompt-modal {
  max-width: 800px;
}

.prompt-content {
  background-color: #f8f8f8;
  border-radius: 6px;
  padding: 15px;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
  font-family: monospace;
  white-space: pre-wrap;
  font-size: 14px;
  color: #333;
}

.prompt-message {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.prompt-message:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.prompt-role {
  font-weight: bold;
  margin-bottom: 5px;
  color: var(--primary-color, #ba003f);
  font-size: 13px;
}

.prompt-text {
  line-height: 1.6;
}

.tips-list {
  margin: 0;
  padding: 0 0 0 20px;
  list-style-type: none;
}

.tips-list li {
  margin-bottom: 14px;
  position: relative;
  line-height: 1.5;
}

.tips-list li:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
}

/* 知识学习抽屉相关样式 */
.knowledge-content {
  padding: 10px 15px;
  max-height: calc(100vh - 60px);
  overflow-y: auto;
}

.knowledge-section {
  margin-bottom: 25px;
}

.knowledge-subtitle {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-color, #ba003f);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.knowledge-icon {
  margin-right: 8px;
  font-size: 18px;
  color: var(--primary-color, #ba003f);
}

.knowledge-text {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

.knowledge-text strong {
  color: #222;
  font-weight: 600;
}
</style> 