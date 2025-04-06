<template>
  <div class="longform-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>文章润色</h2>
      </div>
      <div class="page-actions">
        <button class="action-btn" title="创作小贴士" @click="showTips">
          <i class="ri-lightbulb-line"></i>
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
        
        <!-- 润色风格 -->
        <div class="form-group">
          <label>润色风格</label>
          <div class="radio-group">
            <label class="radio-container">
              <input type="radio" v-model="refinementStyle" value="general" name="style">
              <span>通用改进</span>
            </label>
            <label class="radio-container">
              <input type="radio" v-model="refinementStyle" value="academic" name="style">
              <span>学术论文</span>
            </label>
            <label class="radio-container">
              <input type="radio" v-model="refinementStyle" value="business" name="style">
              <span>商务正式</span>
            </label>
            <label class="radio-container">
              <input type="radio" v-model="refinementStyle" value="creative" name="style">
              <span>创意文学</span>
            </label>
            <label class="radio-container">
              <input type="radio" v-model="refinementStyle" value="news" name="style">
              <span>新闻报道</span>
            </label>
            <label class="radio-container">
              <input type="radio" v-model="refinementStyle" value="technical" name="style">
              <span>技术文档</span>
            </label>
          </div>
        </div>
        
        <!-- 润色选项 -->
        <div class="form-group">
          <label>润色选项</label>
          <div class="checkbox-group">
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.grammar">
              <span>改进语法</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.punctuation">
              <span>标点优化</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.wording">
              <span>用词优化</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.clarity">
              <span>增强清晰度</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.coherence">
              <span>增强连贯性</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.concise">
              <span>精简表达</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.attractive">
              <span>提升吸引力</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="refineOptions.tone">
              <span>调整语气</span>
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
            <div v-if="isGenerating" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedNote && !isGenerating" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无内容，请点击"开始润色"按钮开始润色</p>
              </div>
            </div>
            
            <div v-else-if="generatedNote" class="note-result" :class="{'blur-content': isGenerating}">
              <textarea v-model="generatedNote" class="result-textarea" readonly></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line"></i> 润色小贴士</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>🎯 目标明确 - 确定润色的具体目标，如提高专业性、增强可读性或改变语气风格</li>
            <li>🧩 选择风格 - 根据文章用途选择合适的润色风格，如学术论文、商务正式或创意文学</li>
            <li>🌟 核心保留 - 在润色过程中保留原文的核心信息和主要观点</li>
            <li>📏 语法优先 - 首先确保文章的语法和标点符号使用正确</li>
            <li>💎 用词精准 - 用更精准、生动的词汇替换模糊或重复的表达</li>
            <li>🔗 增强连贯 - 注重段落之间和句子之间的逻辑连接，使文章更流畅</li>
            <li>✂️ 精简冗余 - 删除多余的词句，保持表达简洁有力</li>
            <li>🌈 增添魅力 - 适当增加修辞和生动描述，提升文章的吸引力</li>
          </ul>
        </div>
      </div>
    </div>

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

export default {
  name: 'Refinement',
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
      selectedModel: 'deepseek-v3-vol',
      modelList: [],
      
      // 润色风格
      refinementStyle: 'general'
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
          // 不做过滤，获取所有可用模型
          this.modelList = response.data.data || [];
          console.log('可用模型列表:', this.modelList);
          
          // 如果没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.modelList.push({ id: 'deepseek-v3-vol', name: '火山引擎 DeepSeek V3' });
          }
          
          // 默认选择火山引擎V3或第一个可用模型
          if (!this.selectedModel) {
            const volcanoModel = this.modelList.find(model => model.id === 'deepseek-v3-vol');
            this.selectedModel = volcanoModel ? volcanoModel.id : (this.modelList[0] ? this.modelList[0].id : 'deepseek-v3-vol');
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
        { id: 'deepseek-v3-vol', name: '火山引擎 DeepSeek V3' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3-vol';
    },
    
    // 生成校对结果的方法
    async generateLongform() {
      // 验证必填字段
      if (!this.validateForm()) {
        return;
      }
      
      this.isGenerating = true;
      this.generatedNote = '';
      
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
          this.selectedModel = 'deepseek-v3-vol';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        // 调用API (增加timeout和重试逻辑)
        console.log('开始调用API，模型:', this.selectedModel);
        
        let maxRetries = 2;
        let retryCount = 0;
        let response;
        
        while (retryCount <= maxRetries) {
          try {
            if (retryCount > 0) {
              this.loadingText = `正在重试润色 (${retryCount}/${maxRetries})...`;
              console.log(`尝试第${retryCount}次重试...`);
            }
            
            response = await axios.post('/api/v1/llm/chat', {
              model: this.selectedModel,
              messages: apiMessages,
              temperature: 0.7,
              top_p: 0.95,
              max_tokens: 2000
            }, { 
              timeout: 60000 // 设置60秒超时
            });
            
            // 如果成功获取响应，跳出重试循环
            console.log('API调用成功，响应状态:', response.status);
            console.log('API调用成功，返回数据类型:', typeof response.data);
            
            // 检查响应是否包含预期的字段
            if (response.data) {
              const hasStatus = 'status' in response.data;
              const hasData = 'data' in response.data;
              const hasContent = 'content' in response.data;
              console.log(`响应字段检查: status=${hasStatus}, data=${hasData}, content=${hasContent}`);
              
              if (hasData && response.data.data) {
                const dataType = typeof response.data.data;
                console.log(`data字段类型: ${dataType}`);
                
                if (dataType === 'object') {
                  console.log('data对象字段:', Object.keys(response.data.data).join(', '));
                  
                  // 检查choices字段
                  if (response.data.data.choices) {
                    console.log('choices数量:', response.data.data.choices.length);
                    if (response.data.data.choices.length > 0) {
                      const choice = response.data.data.choices[0];
                      console.log('第一个choice字段:', Object.keys(choice).join(', '));
                      if (choice.message) {
                        console.log('消息角色:', choice.message.role);
                        console.log('消息内容 (前200字符):', choice.message.content.substring(0, 200));
                      }
                    }
                  }
                }
              }
            }
            
            break;
          } catch (error) {
            console.error(`API调用失败 (尝试 ${retryCount+1}/${maxRetries+1}):`, error.message);
            
            if (retryCount === maxRetries) {
              // 所有重试都失败了，抛出最后一个错误
              throw error;
            }
            
            // 增加重试次数并继续
            retryCount++;
            // 等待一段时间再重试 (1秒)
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
        
        // 日志记录API响应状态
        console.log('API响应状态:', response.status);
        console.log('API响应数据:', response.data);
        
        if (response.data && response.data.status === 'success') {
          // 从响应中提取生成的内容
          let content = '';
          
          if (response.data.data && response.data.data.choices && response.data.data.choices.length > 0) {
            // 火山引擎格式
            const message = response.data.data.choices[0].message;
            content = message.content || '';
            console.log('使用火山引擎响应格式，内容长度:', content.length);
          } else if (response.data.data && response.data.data.response) {
            // 硅基流动格式
            content = response.data.data.response || '';
            console.log('使用硅基流动响应格式，内容长度:', content.length);
          } else if (response.data.data && typeof response.data.data === 'string') {
            // 直接返回字符串
            content = response.data.data;
            console.log('使用字符串响应格式，内容长度:', content.length);
          } else if (response.data.content) {
            // 直接包含在内容字段
            content = response.data.content;
            console.log('使用content字段响应格式，内容长度:', content.length);
          } else if (response.data.data) {
            // 尝试直接获取data对象
            const dataObj = response.data.data;
            if (typeof dataObj === 'object' && dataObj.message && dataObj.message.content) {
              content = dataObj.message.content;
              console.log('从data.message.content获取内容，长度:', content.length);
            } else if (typeof dataObj === 'object' && dataObj.content) {
              content = dataObj.content;
              console.log('从data.content获取内容，长度:', content.length);
            } else {
              // 尝试将整个data对象转换为字符串
              content = JSON.stringify(dataObj);
              console.log('将整个data对象转换为字符串，长度:', content.length);
            }
          }
          
          // 添加调试日志
          console.log('API响应数据结构:', JSON.stringify(response.data, null, 2));
          
          if (content) {
            this.generatedNote = content;
            console.log('成功获取润色结果');
            // 添加成功提示
            this.$message ? this.$message.success('文章润色完成！') : alert('文章润色完成！');
          } else {
            console.error('API返回成功，但无法提取内容:', response.data);
            // 尝试备用方法提取内容
            try {
              const rawData = JSON.stringify(response.data);
              if (rawData.includes('"content":')) {
                const contentMatch = rawData.match(/"content":"(.*?)"/);
                if (contentMatch && contentMatch[1]) {
                  this.generatedNote = contentMatch[1].replace(/\\n/g, '\n');
                  console.log('使用备用方法提取内容成功');
                  this.$message ? this.$message.success('文章润色完成！') : alert('文章润色完成！');
                  return;
                }
              }
            } catch (e) {
              console.error('备用提取方法失败:', e);
            }
            throw new Error('无法从API响应中提取内容');
          }
        } else {
          // 处理API响应不成功的情况
          console.error('API返回不成功状态:', response.data);
          throw new Error(response.data?.message || '服务器返回错误');
        }
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
      prompt += '\n请提供以下内容：\n1. 问题摘要：列出发现的主要问题类型及数量\n2. 详细修改建议：按照文本顺序列出具体问题，并提供修改建议\n3. 对于重要问题，请同时提供原文和修改后的建议文本\n';
      
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
    }
  }
};
</script>

<style scoped>
.longform-article-page {
  padding: 0;
  margin-top: -40px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 0;
}

.page-nav h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 18px;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.action-btn:hover {
  background-color: #f5f5f5;
  color: var(--primary-color, #ba003f);
  transform: scale(1.1);
  box-shadow: 0 2px 6px rgba(186, 0, 63, 0.2);
}

/* 主要内容区域 - 使用两列布局 */
.main-container {
  display: flex;
  gap: 20px;
  min-height: calc(100vh - 120px);
}

/* 左侧：输入参数 */
.input-section {
  width: 45%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 18px;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title i {
  color: var(--primary-color, #ba003f);
}

.form-row {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.form-group {
  flex: 1;
  margin-bottom: 16px;
  position: relative;
  transition: all 0.3s ease;
}

.form-group:hover label {
  color: var(--primary-color, #ba003f);
}

/* 标签动画效果 */
.form-group label {
  transition: color 0.3s ease;
  font-weight: 500;
  display: block;
  margin-bottom: 6px;
}

/* 焦点状态下整个表单组的效果 */
.form-group:focus-within {
  transform: translateY(-2px);
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 14px;
}

.required:after {
  content: " *";
  color: var(--primary-color, #ba003f);
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: var(--primary-color, #ba003f);
  outline: none;
  box-shadow: 0 0 0 3px rgba(186, 0, 63, 0.1);
}

/* 下拉菜单的自定义样式 */
select.form-control {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%23666' viewBox='0 0 16 16'><path d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/></svg>");
  background-repeat: no-repeat;
  background-position: calc(100% - 12px) center;
  background-size: 12px;
  padding-right: 32px;
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

select.form-control:hover {
  border-color: #bbb;
  background-color: #f9f9f9;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}

select.form-control:focus {
  border-color: var(--primary-color, #ba003f);
  box-shadow: 0 0 0 3px rgba(186, 0, 63, 0.1);
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%23ba003f' viewBox='0 0 16 16'><path d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/></svg>");
}

/* 优化下拉选项样式 */
select.form-control option {
  padding: 10px;
  font-size: 14px;
}

/* 禁用状态样式 */
select.form-control:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #f5f5f5;
}

/* 文本区域样式优化 */
textarea.form-control {
  min-height: 100px;
  line-height: 1.5;
  resize: vertical;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

textarea.form-control:focus {
  background-color: #fff;
  box-shadow: 0 0 0 3px rgba(186, 0, 63, 0.1);
}

/* 复选框样式 */
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 5px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  background-color: #fcf2f5;
  padding: 8px 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f9e0e7;
  position: relative;
}

.checkbox-container:hover {
  background-color: #f9e0e7;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(186, 0, 63, 0.1);
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkbox-container span {
  padding-left: 24px;
  position: relative;
  font-weight: 500;
  color: #555;
}

.checkbox-container span:before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  border-radius: 4px;
  border: 1px solid #e6aebe;
  background-color: #fff;
  transition: all 0.2s ease;
}

.checkbox-container input:checked + span:before {
  background-color: var(--primary-color, #ba003f);
  border-color: var(--primary-color, #ba003f);
}

.checkbox-container input:checked + span:after {
  content: '';
  position: absolute;
  left: 6px;
  top: 50%;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: translateY(-75%) rotate(45deg);
}

.checkbox-container input:focus + span:before {
  box-shadow: 0 0 0 3px rgba(186, 0, 63, 0.1);
}

.checkbox-container:active {
  transform: scale(0.98);
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 8px;
  margin-top: 15px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  height: 44px;
  padding: 0 16px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: none;
}

.btn:active {
  transform: scale(0.96);
}

.btn i {
  font-size: 16px;
}

.btn-primary {
  background-color: var(--primary-color, #ba003f);
  color: white;
  flex: 1;
}

.btn-primary:hover {
  background-color: #d4004c;
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.3);
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background-color: #e0e0e0;
  color: #999;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #666;
}

.btn-secondary:hover {
  background-color: #eaeaea;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* 右侧：输出内容 */
.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 示例区域 */
.examples-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 12px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  margin-bottom: 0;
  transition: all 0.3s;
}

.examples-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.carousel-controls {
  display: flex;
  gap: 10px;
}

.carousel-control {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid #ddd;
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #666;
}

.carousel-control:hover:not(.disabled):not(:disabled) {
  background-color: var(--primary-color, #ba003f);
  color: white;
  border-color: var(--primary-color, #ba003f);
  transform: scale(1.05);
}

.carousel-control.disabled,
.carousel-control:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.carousel-control i {
  font-size: 18px;
}

.example-carousel {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding-bottom: 5px;
}

.example-cards {
  display: flex;
  transition: transform 0.3s ease;
  padding: 8px 0;
  gap: 0;
}

.example-card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 12px;
  margin-right: 15px;
  width: 200px;
  min-width: 200px;
  max-width: 200px;
  height: 150px;
  min-height: 150px;
  max-height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  overflow: hidden;
  box-sizing: border-box;
}

.example-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.15);
  border-color: var(--primary-color, #ba003f);
}

.example-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(186, 0, 63, 0.1);
  margin-bottom: 12px;
}

.example-icon svg {
  width: 32px;
  height: 32px;
  color: #BA003F;
}

.example-info {
  display: flex;
  flex-direction: column;
  text-align: center;
  overflow: hidden;
  width: 100%;
}

.example-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.example-desc {
  font-size: 12px;
  color: #888;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

/* 结果区域 */
.result-section {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  background-color: #fff;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  flex-wrap: wrap;
  gap: 8px;
}

.section-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.section-title {
  display: flex;
  align-items: center;
  color: #333;
  font-size: 16px;
  margin: 0;
  font-weight: 600;
}

.section-title i {
  margin-right: 8px;
  font-size: 20px;
  color: var(--primary-color, #ba003f);
}

.result-content-wrapper {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 300px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color, #ba003f);
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

.loading-text {
  font-size: 14px;
  color: #666;
}

.empty-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-image {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
}

.empty-message {
  margin: 0 0 20px;
  font-size: 16px;
  color: #666;
}

.note-result {
  flex: 1;
  padding: 15px;
  overflow: hidden;
  display: flex;
  height: 100%;
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

.blur-content {
  filter: blur(1px);
  opacity: 0.6;
  pointer-events: none;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 模态框 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 20px;
}

.tips-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  margin-bottom: 12px;
  padding-left: 20px;
  position: relative;
  line-height: 1.5;
}

.tips-list li:before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--primary-color, #ba003f);
  font-weight: bold;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section, .right-column {
    width: 100%;
  }
}

/* 新增公众号风格按钮样式 */
.primary-button {
  background-color: var(--primary-color, #ba003f);
  color: white;
  border: none;
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

.primary-button:hover {
  background-color: #d4004c;
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(186, 0, 63, 0.2);
}

.primary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #ccc;
  color: #666;
  transform: none;
  box-shadow: none;
}

.secondary-button {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #e0e0e0;
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

.secondary-button:hover {
  background-color: #eaeaea;
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #f5f5f5;
  color: #aaa;
  transform: none;
  box-shadow: none;
}

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

.action-buttons {
  display: flex;
  gap: 8px;
  margin-top: 0;
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
}

.file-upload-btn {
  background-color: #f5f5f5;
  color: #999;
  border: 1px solid #ddd;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: not-allowed;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
}

.file-upload-hint {
  font-size: 13px;
  color: #999;
  font-style: italic;
}

/* 单选框样式 */
.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 5px;
}

.radio-container {
  display: flex;
  align-items: center;
  background-color: #f8f5f6;
  padding: 10px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f0e6e8;
  position: relative;
}

.radio-container:hover {
  background-color: #f9e0e7;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(186, 0, 63, 0.1);
}

.radio-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.radio-container span {
  padding-left: 28px;
  position: relative;
  font-weight: 500;
  color: #444;
  display: flex;
  align-items: center;
  gap: 5px;
}

.radio-container span:before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1px solid #e6aebe;
  background-color: #fff;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.radio-container input:checked + span:before {
  border: 6px solid var(--primary-color, #ba003f);
}

.radio-container input:focus + span:before {
  box-shadow: 0 0 0 3px rgba(186, 0, 63, 0.1);
}

.radio-container:active {
  transform: scale(0.98);
}

.radio-container input:checked ~ span {
  color: var(--primary-color, #ba003f);
}

.radio-container span i {
  font-size: 16px;
  color: var(--primary-color, #ba003f);
}
</style> 