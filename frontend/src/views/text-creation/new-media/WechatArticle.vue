<template>
  <div class="wechat-article-page">
    <div class="page-header no-border">
      <div class="page-nav">
        <h2>公众号文章生成</h2>
      </div>
      <div class="page-actions">
        <div class="learn-button" @click="showTipsModal = true">
          <i class="ri-lightbulb-flash-line"></i>
          <span>知识学习</span>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区域 - 使用两列布局 -->
    <div class="main-container">
      <!-- 左侧：输入参数 -->
      <div class="input-section">
        <div class="section-header">
          <h3 class="section-title">
            <i class="ri-settings-3-line"></i>
            输入参数
          </h3>
        </div>
        
        <!-- 文章类型选择 -->
        <div class="form-group">
          <label for="article-type">文章类型</label>
          <select id="article-type" v-model="articleType" class="form-control">
            <option value="knowledge">知识科普</option>
            <option value="story">故事感悟</option>
            <option value="opinion">观点评论</option>
            <option value="tutorial">教程指南</option>
            <option value="industry">行业分析</option>
            <option value="list">清单合集</option>
            <option value="interview">访谈问答</option>
            <option value="case">案例分析</option>
          </select>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="article-title" class="required">文章标题</label>
            <input 
              type="text" 
              id="article-title" 
              v-model="articleTitle" 
              placeholder="输入文章主标题，或描述您想要的标题主题"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="target-audience" class="required">目标读者群体</label>
            <input 
              type="text" 
              id="target-audience" 
              v-model="targetAudience" 
              placeholder="例如：大学生、职场人士、宝妈、科技爱好者等"
              class="form-control"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="article-keywords" class="required">文章关键词或内容要点</label>
          <textarea 
            id="article-keywords" 
            v-model="articleKeywords" 
            placeholder="输入文章需要包含的关键词、内容要点或核心观点，每点用逗号或分号分隔"
            class="form-control"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="writing-style">写作风格</label>
            <select id="writing-style" v-model="writingStyle" class="form-control">
              <option value="professional">专业严谨</option>
              <option value="conversational">轻松对话</option>
              <option value="humorous">幽默风趣</option>
              <option value="storytelling">故事叙述</option>
              <option value="inspirational">励志激励</option>
              <option value="analytical">分析思辨</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="article-length">文章长度</label>
            <select id="article-length" v-model="articleLength" class="form-control">
              <option value="short">短文 (800字左右)</option>
              <option value="medium">中篇 (1500字左右)</option>
              <option value="long">长文 (2500字左右)</option>
              <option value="very-long">深度长文 (3500字以上)</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label for="additional-requirements">其他特殊要求（可选）</label>
          <textarea 
            id="additional-requirements" 
            v-model="additionalRequirements" 
            placeholder="如需要特定的文章结构、引用来源、风格要求等，请在此说明"
            class="form-control"
            rows="3"
          ></textarea>
        </div>
        
        <!-- 自定义参数区域 -->
        <div class="form-group custom-params-section">
          <div class="custom-params-header">
            <label>自定义参数 <span class="custom-param-tip">(可根据需要添加更多参数)</span></label>
            <button type="button" class="add-param-btn" @click="addCustomParam">
              <i class="ri-add-line"></i> 添加参数
            </button>
          </div>
          
          <div v-if="customParams.length === 0" class="empty-params-tip">
            <i class="ri-information-line"></i> 
            您可以添加任意自定义参数，例如：行业背景、引用资料、参考案例等
          </div>
          
          <div v-for="(param, index) in customParams" :key="index" class="custom-param-item">
            <div class="param-input-group">
              <input 
                type="text" 
                v-model="param.key" 
                placeholder="参数名称" 
                class="param-key form-control"
              />
              <textarea 
                v-model="param.value" 
                placeholder="参数值" 
                class="param-value form-control"
                rows="2"
              ></textarea>
              <button type="button" class="remove-param-btn" @click="removeCustomParam(index)">
                <i class="ri-delete-bin-line"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 添加模型选择 -->
        <div class="form-group">
          <label class="form-label">AI模型选择:</label>
          <select id="model-select" v-model="selectedModel" class="form-control" :disabled="modelList.length === 0">
            <option v-for="model in modelList" :key="model.id" :value="model.id">
              {{ model.name }}
            </option>
            <option v-if="modelList.length === 0" value="" disabled>加载模型列表中...</option>
          </select>
          <div v-if="modelList.length === 0" class="model-loading">
            <i class="ri-loader-4-line"></i> 正在加载可用模型...
          </div>
        </div>
        
        <div class="action-buttons">
          <button class="btn btn-primary" @click="generateArticle" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '正在生成...' : '生成公众号文章' }}
          </button>
          <button class="btn btn-secondary" @click="resetForm">
            <i class="ri-refresh-line"></i> 重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：参考案例和结果 -->
      <div class="right-column">
        <!-- 参考案例部分 -->
        <div class="examples-section">
          <div class="examples-header">
            <h3 class="section-title">
              <i class="ri-lightbulb-flash-line"></i>
              参考案例
            </h3>
            <!-- 添加轮播控制按钮 -->
            <div class="carousel-controls">
              <button class="carousel-control prev" @click="prevExample" :class="{ 'disabled': currentExampleIndex <= 0 }">
                <i class="ri-arrow-left-s-line"></i>
              </button>
              <button class="carousel-control next" @click="nextExample" :class="{ 'disabled': isLastPage }">
                <i class="ri-arrow-right-s-line"></i>
              </button>
            </div>
          </div>
          
          <div class="example-carousel">
            <div class="example-cards" ref="exampleCarousel">
              <div class="example-card" v-for="(example, index) in examples" :key="index" @click="loadExample('example' + (index + 1))" :title="example.title + '：' + example.desc">
                <div class="example-card-header">
                  <div class="example-icon">
                    <i :class="example.icon"></i>
                  </div>
                  <div class="example-info">
                    <div class="example-title">{{ example.title }}</div>
                    <div class="example-desc">{{ example.type }}</div>
                  </div>
                </div>
                <div class="example-content" v-if="example.desc">
                  <div class="example-detail">{{ example.desc }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 结果展示部分 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              文章结果
            </h3>
            <div class="action-buttons">
              <button @click="generateArticle" class="primary-button" :disabled="isLoading">
                <i class="ri-refresh-line" v-if="!isLoading"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isLoading ? '生成中...' : '重新生成' }}
              </button>
              <button @click="copyResult" class="secondary-button" :disabled="isLoading || !generatedArticle">
                <i class="ri-file-copy-line"></i>
                复制文章
              </button>
              <button @click="showPrompt" class="prompt-button" :disabled="!lastUsedPrompt">
                <i class="ri-code-line"></i>
                查看提示词
              </button>
              <button @click="toggleDisplayMode" class="toggle-display-button" :disabled="!generatedArticle">
                <i :class="isPhoneMode ? 'ri-layout-line' : 'ri-smartphone-line'"></i>
                {{ isPhoneMode ? '普通视图' : '手机视图' }}
              </button>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isLoading && !isStreaming" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedArticle && !isLoading && !isStreaming" class="empty-result">
              <div class="empty-content">
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无文章内容，请点击"生成公众号文章"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedArticle || isStreaming" class="article-result" :class="{'blur-content': isLoading && !isStreaming, 'streaming': isStreaming}">
              <!-- 添加离线模式提示条 -->
              <div v-if="isOfflineGenerated" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板文章。要获得AI生成的更优质文章，请联系管理员启动后端服务。</span>
              </div>
              
              <!-- 流式生成指示器 -->
              <div v-if="isStreaming" class="streaming-indicator">
                <span class="dot-typing"></span>
              </div>
              
              <!-- 普通视图模式 -->
              <div v-if="!isPhoneMode" class="normal-article-view">
                <div class="article-content" v-html="formattedArticle"></div>
                
                <!-- 普通视图下的流式指示器 -->
                <div v-if="isStreaming" class="normal-streaming-indicator">
                  <div class="typing-animation">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                  </div>
                  <span class="typing-text">AI正在持续创作中...</span>
                </div>
              </div>
              
              <!-- 手机视图模式 -->
              <div v-else class="wechat-article-container">
                <div class="wechat-article">
                  <div class="wechat-article-header">
                    <div class="wechat-article-title">{{ this.articleTitle || '公众号文章标题' }}</div>
                    <div class="wechat-article-info">
                      <span class="wechat-article-account">易紫荆AI</span>
                      <span class="wechat-article-date">{{ new Date().toLocaleDateString() }}</span>
                    </div>
                  </div>
                  <div class="wechat-article-content" v-html="formattedArticle"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态框 - 修改为抽屉组件 -->
    <el-drawer
      v-model="showTipsModal"
      title="公众号文章创作指南"
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
    
    <!-- 提示词查看模态框 -->
    <div class="modal" v-if="showPromptModal">
      <div class="modal-content prompt-modal">
        <div class="modal-header">
          <h3><i class="ri-code-box-line"></i> 生成提示词</h3>
          <button class="close-btn" @click="showPromptModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="prompt-content">
            <pre>{{ lastUsedPrompt }}</pre>
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
import axios from 'axios'
import { wechatArticleExamples } from '@/views/example_data.js'
import { wechatArticleKnowledge } from '@/views/Knowledge_data.js'
import '@/assets/css/text-creation-common.css' // 引入统一CSS样式文件
import '@/assets/css/mobile-preview.css' // 引入手机预览样式文件

export default {
  name: 'WechatArticle',
  data() {
    return {
      articleType: 'knowledge',
      articleTitle: '',
      targetAudience: '',
      articleKeywords: '',
      writingStyle: 'conversational',
      articleLength: 'short',
      additionalRequirements: '',
      generatedArticle: '',
      isOfflineGenerated: false,
      showTipsModal: false,
      showPromptModal: false,
      lastUsedPrompt: '',
      modelList: [],
      selectedModel: 'deepseek-v3',
      isGenerating: false,
      isLoading: false,
      loadingText: '正在生成公众号文章...',
      validationErrors: [],
      isStreaming: false, // 添加流式输出状态标记
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      isPhoneMode: false, // 将默认视图改为普通视图
      imageLoading: true, // 图片加载状态
      examples: wechatArticleExamples,
      customParams: [],
      // 添加公众号文章知识内容
      articleKnowledge: wechatArticleKnowledge
    }
  },
  
  computed: {
    // 格式化文章展示
    formattedArticle() {
      if (!this.generatedArticle) return '';
      
      // 将换行符转换为HTML段落
      return this.generatedArticle
        .split('\n\n')
        .map(para => para.trim())
        .filter(para => para.length > 0)
        .map(para => {
          // 检查是否为标题 (# 或 ## 开头)
          if (para.startsWith('# ')) {
            return `<h1 class="article-h1">${para.substring(2)}</h1>`;
          } else if (para.startsWith('## ')) {
            return `<h2 class="article-h2">${para.substring(3)}</h2>`;
          } else if (para.startsWith('### ')) {
            return `<h3 class="article-h3">${para.substring(4)}</h3>`;
          } else if (para.startsWith('> ')) {
            // 引用样式
            return `<blockquote class="article-quote">${para.substring(2).replace(/\n/g, '<br>')}</blockquote>`;
          } else if (para.startsWith('* ') || para.startsWith('- ')) {
            // 无序列表
            const items = para.split('\n').map(item => {
              if (item.startsWith('* ') || item.startsWith('- ')) {
                return `<li>${item.substring(2)}</li>`;
              }
              return `<li>${item}</li>`;
            }).join('');
            return `<ul class="article-list">${items}</ul>`;
          } else if (/^\d+\.\s/.test(para)) {
            // 有序列表
            const items = para.split('\n').map(item => {
              if (/^\d+\.\s/.test(item)) {
                return `<li>${item.replace(/^\d+\.\s/, '')}</li>`;
              }
              return `<li>${item}</li>`;
            }).join('');
            return `<ol class="article-list">${items}</ol>`;
          } else if (para.startsWith('*') && para.endsWith('*')) {
            // 斜体段落
            return `<p class="article-italic">${para.substring(1, para.length - 1).replace(/\n/g, '<br>')}</p>`;
          } else {
            // 添加关键词高亮
            let content = para.replace(/\n/g, '<br>');
            const keywords = this.articleKeywords.split(/[,;，；]/);
            keywords.forEach(keyword => {
              if (keyword.trim().length > 1) {
                const regex = new RegExp(`(${keyword.trim()})`, 'gi');
                content = content.replace(regex, '<span class="keyword-highlight">$1</span>');
              }
            });
            
            // 添加随机强调样式（约10%的段落）
            if (Math.random() < 0.1) {
              return `<p class="article-emphasis">${content}</p>`;
            }
            
            return `<p class="article-p">${content}</p>`;
          }
        })
        .join('');
    },
    
    // 判断是否已经到达最后一页
    isLastPage() {
      // 计算是否已经滚动到最后一页
      const cardWidth = 215; // 卡片宽度+间距
      const containerWidth = this.$refs.exampleCarousel?.parentElement?.clientWidth || 0;
      const totalWidth = this.examples.length * cardWidth;
      const maxScrollX = totalWidth - containerWidth;
      
      // 当滚动到最大滚动距离的90%以上时，认为是最后一页
      return Math.abs(this.exampleTranslateX) >= maxScrollX * 0.9;
    }
  },
  
  mounted() {
    this.fetchModels();
  },
  
  methods: {
    // 获取可用的大模型列表
    async fetchModels() {
      try {
        const response = await axios.get('/api/v1/llm/models');
        
        if (response.data.status === 'success') {
          // 获取模型列表
          const models = response.data.data;
          
          // 按照指定顺序排序模型
          const orderedModelIds = [
            'deepseek-v3-vol',  // DeepSeek-V3（火山引擎）- 放在第一位
            'qwen-max',         // 通义千问-Max（阿里云）
            'deepseek-r1-vol',  // DeepSeek-R1（火山引擎）
            'deepseek-r1-sf',   // DeepSeek-R1（硅基流动）
            'deepseek-v3-sf',   // DeepSeek-V3（硅基流动）
            'qwq-32b',          // 通义千问-32B（硅基流动）
          ];
          
          // 按指定顺序排序
          this.modelList = orderedModelIds
            .map(id => models.find(model => model.id === id))
            .filter(model => model !== undefined);
          
          // 默认选择火山引擎的DeepSeek V3模型
          this.selectedModel = 'deepseek-v3';
          
          // 如果没有可用模型，创建一个默认列表作为备用
          if (this.modelList.length === 0) {
            this.setupDefaultModels();
          }
        } else {
          console.error('获取模型列表失败:', response.data.message);
          this.setupDefaultModels();
        }
      } catch (error) {
        console.error('获取模型列表异常:', error);
        this.setupDefaultModels();
      }
    },
    
    setupDefaultModels() {
      this.modelList = [
        { id: 'deepseek-v3', name: 'DeepSeek-V3（火山引擎）' },
        { id: 'qwen-max', name: '通义千问-Max（阿里云）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3';
    },
    
    // 显示创作小贴士
    showTips() {
      this.showTipsModal = true;
    },
    
    // 重置表单
    resetForm() {
      this.articleTitle = '';
      this.targetAudience = '';
      this.articleKeywords = '';
      this.articleType = 'knowledge';
      this.writingStyle = 'conversational';
      this.articleLength = 'short';
      this.additionalRequirements = '';
      this.generatedArticle = '';
      this.lastUsedPrompt = '';
      this.isOfflineGenerated = false;
      this.customParams = []; // 重置自定义参数
    },
    
    // 添加自定义参数
    addCustomParam() {
      this.customParams.push({
        key: '',
        value: ''
      });
    },
    
    // 移除自定义参数
    removeCustomParam(index) {
      this.customParams.splice(index, 1);
    },
    
    // 轮播控制 - 上一页
    prevExample() {
      if (this.currentExampleIndex > 0) {
        this.currentExampleIndex--;
        this.updateExampleCarousel();
      }
    },
    
    // 轮播控制 - 下一页
    nextExample() {
      const maxVisibleCards = Math.floor(document.querySelector('.example-carousel').clientWidth / 185);
      const maxIndex = this.examples.length - maxVisibleCards;
      
      if (this.currentExampleIndex < maxIndex) {
        this.currentExampleIndex++;
        this.updateExampleCarousel();
      }
    },
    
    // 更新轮播位置
    updateExampleCarousel() {
      const cardWidth = 185; // 卡片宽度(170px) + 间距(15px)
      this.exampleTranslateX = -this.currentExampleIndex * cardWidth;
      if (this.$refs.exampleCarousel) {
        this.$refs.exampleCarousel.style.transform = `translateX(${this.exampleTranslateX}px)`;
        this.$refs.exampleCarousel.style.transition = 'transform 0.3s ease';
      }
    },
    
    // 加载参考案例
    loadExample(example) {
      // 通过索引找到对应的参考案例
      const index = parseInt(example.replace('example', '')) - 1;
      const data = this.examples[index];
      
      if (!data) return;
      
      console.log('加载参考案例:', data);
      
      // 填充表单字段
      this.articleTitle = data.title || '';
      this.targetAudience = data.audience || '对' + data.desc + '感兴趣的读者';
      this.articleKeywords = data.desc || '';
      this.articleType = data.articleType || 'knowledge';
      this.writingStyle = data.writingStyle || 'conversational';
      this.articleLength = 'short';
    },
    
    // 验证表单
    validateForm() {
      // 重置验证错误
      this.validationErrors = [];
      
      // 验证必填字段
      if (!this.articleTitle.trim()) {
        this.validationErrors.push('文章标题不能为空');
      }
      
      if (!this.targetAudience.trim()) {
        this.validationErrors.push('目标读者群体不能为空');
      }
      
      if (!this.articleKeywords.trim()) {
        this.validationErrors.push('文章关键词/内容要点不能为空');
      }
      
      // 自定义参数验证
      if (this.customParams.length > 0) {
        for (let i = 0; i < this.customParams.length; i++) {
          const param = this.customParams[i];
          if ((param.key.trim() && !param.value.trim()) || (!param.key.trim() && param.value.trim())) {
            this.validationErrors.push(`自定义参数 #${i+1} 的键和值必须同时填写或同时为空`);
          }
        }
      }
      
      // 返回验证结果
      return this.validationErrors.length === 0;
    },
    
    // 生成公众号文章
    async generateArticle() {
      console.log('开始生成公众号文章');
      try {
        // 验证表单
        if (!this.validateForm()) {
          this.$message ? this.$message.error('请完善表单信息') : alert('请完善表单信息');
          return;
        }
        
        // 显示加载状态
        this.isLoading = true;
        this.isGenerating = true;
        this.loadingText = '正在生成公众号文章...';
        // 清空之前的生成结果
        this.generatedArticle = '';
        this.isOfflineGenerated = false;
        // 初始化流式输出状态
        this.isStreaming = false;
        
        // 构建提示词
        const prompt = this.buildPrompt();
        
        // 调用API并获取结果
        const result = await this.callLLMApi(prompt);
        
        // 不需要再次设置generatedArticle，因为在流式输出中已经设置了
        // 只需设置离线模式标志
        this.isOfflineGenerated = result.offlineMode || false;
        
        // 如果是离线模式，显示提示
        if (result.offlineMode) {
          this.$notify && this.$notify({
            title: '离线模式提示',
            message: '后端服务不可用，当前显示的是离线生成的文章。要获得AI生成的更优质文章，请联系管理员启动后端服务。',
            type: 'warning',
            duration: 10000,
            position: 'top-right'
          });
        }
      } catch (error) {
        console.error('生成公众号文章失败:', error);
        // 显示错误信息
        this.$message ? this.$message.error(error.message || '生成公众号文章失败') : 
          alert(error.message || '生成公众号文章失败');
      } finally {
        this.isLoading = false;
        this.isGenerating = false;
      }
    },
    
    // 构建提示词
    buildPrompt() {
      console.log('构建公众号文章生成提示词');
      
      // 获取文章类型的中文名称
      const getArticleTypeName = () => {
        const typeMap = {
          'knowledge': '知识科普',
          'story': '故事感悟',
          'opinion': '观点评论',
          'tutorial': '教程指南',
          'industry': '行业分析',
          'list': '清单合集',
          'interview': '访谈问答',
          'case': '案例分析'
        };
        return typeMap[this.articleType] || '知识科普';
      };
      
      // 获取风格的中文名称
      const getStyleName = () => {
        const styleMap = {
          'professional': '专业严谨',
          'conversational': '轻松对话',
          'humorous': '幽默风趣',
          'storytelling': '故事叙述',
          'inspirational': '励志激励',
          'analytical': '分析思辨'
        };
        return styleMap[this.writingStyle] || '专业严谨';
      };
      
      // 获取长度的中文描述
      const getLengthDescription = () => {
        const lengthMap = {
          'short': '短文 (800字左右)',
          'medium': '中篇 (1500字左右)',
          'long': '长文 (2500字左右)',
          'very-long': '深度长文 (3500字以上)'
        };
        return lengthMap[this.articleLength] || '中篇 (1500字左右)';
      };
      
      // 构建系统提示词
      const systemPrompt = `你是一位专业的公众号内容创作者，精通各类型公众号文章的创作，包括知识科普、故事感悟、观点评论等多种类型。请根据用户提供的信息，创作一篇符合要求的高质量公众号文章。`;
      
      // 构建用户提示词
      let prompt = `请为我创作一篇类型为【${getArticleTypeName()}】的公众号文章：\n\n`;
      prompt += `文章类型：${getArticleTypeName()}\n`;
      prompt += `文章标题/主题：${this.articleTitle}\n`;
      prompt += `目标读者群体：${this.targetAudience}\n`;
      prompt += `文章关键词/内容要点：${this.articleKeywords}\n`;
      prompt += `写作风格：${getStyleName()}\n`;
      prompt += `文章长度：${getLengthDescription()}\n`;
      
      if (this.additionalRequirements) {
        prompt += `其他特殊要求：${this.additionalRequirements}\n`;
      }
      
      // 添加自定义参数
      if (this.customParams.length > 0) {
        prompt += `\n自定义参数：\n`;
        this.customParams.forEach(param => {
          if (param.key && param.value) {
            prompt += `- ${param.key}：${param.value}\n`;
          }
        });
      }
      
      // 添加特定的要求和建议
      prompt += `\n请根据以上信息创作一篇符合公众号平台特点的优质文章，具体要求如下：`;
      
      // 根据不同的文章类型添加特定要求
      switch (this.articleType) {
        case 'knowledge':
          prompt += `
          1. 文章应该包含准确的专业知识，同时通过通俗易懂的表达方式让读者容易理解
          2. 建议采用"提问-解答"或"问题-分析-解决"的结构
          3. 适当使用例子、比喻和类比帮助读者理解复杂概念
          4. 在文章结尾提供延伸阅读建议或思考问题`;
          break;
        case 'story':
          prompt += `
          1. 文章应该围绕一个或多个生动的故事展开
          2. 故事应该有清晰的情节发展和人物塑造
          3. 每个故事应该包含明确的感悟或启示
          4. 结尾部分应该提炼出故事的核心价值观或人生哲理`;
          break;
        case 'opinion':
          prompt += `
          1. 文章应该围绕一个明确的观点或立场展开
          2. 提供充分的论据和事实支持你的观点
          3. 客观分析不同的声音和反对意见
          4. 结论部分应该强化你的核心观点并给读者留下思考空间`;
          break;
        case 'tutorial':
          prompt += `
          1. 文章应该提供清晰的步骤指导
          2. 每个步骤应该详细解释操作方法和注意事项
          3. 可以添加常见问题及解答部分
          4. 结尾提供进阶学习资源或后续实践建议`;
          break;
        case 'industry':
          prompt += `
          1. 文章应该基于行业数据和事实进行分析
          2. 分析当前行业趋势、挑战和机遇
          3. 提供专业的洞见和前瞻性预测
          4. 结论部分可以给出行业从业者的建议`;
          break;
        case 'list':
          prompt += `
          1. 文章应该以清单形式呈现内容要点
          2. 每个要点需要简明扼要的标题和详细解释
          3. 可以使用编号或分类组织内容
          4. 结尾总结清单的核心价值和应用场景`;
          break;
        case 'interview':
          prompt += `
          1. 文章应该以问答形式呈现内容
          2. 问题应该有逻辑性和连贯性
          3. 回答应该具有专业性和信息量
          4. 可以添加背景介绍和总结评论部分`;
          break;
        case 'case':
          prompt += `
          1. 文章应该围绕一个或多个具体案例展开
          2. 详细描述案例背景、过程和结果
          3. 提供深入分析和关键洞察
          4. 结论部分提炼出可借鉴的经验和教训`;
          break;
      }
      
      // 添加公众号文章的通用要求
      prompt += `
      
      公众号文章通用要求：
      1. 标题应该吸引人且包含关键词，可以使用数字、问号或情感词增强吸引力
      2. 开篇第一段应该简洁有力，直接切入主题并吸引读者继续阅读
      3. 正文应该使用清晰的段落结构，适当使用小标题、加粗、分隔符等元素增强可读性
      4. 语言应该符合目标读者的阅读习惯，避免过于专业的术语（除非必要）
      5. 结尾应该包含总结、号召性用语或设置互动话题，增加读者互动率
      6. 文章整体应该逻辑清晰，论点有力，内容有深度和价值
      
      请直接输出文章内容，不需要添加任何额外的解释或说明。文章应该是完整的，包括标题、正文和结尾。`;
      
      // 记录完整提示词用于调试
      console.log('完整提示词:', prompt);
      
      // 保存提示词以便之后查看
      this.lastUsedPrompt = prompt;
      
      return prompt;
    },
    
    // 调用大模型API
    async callLLMApi(prompt) {
      try {
        // 检查是否有可用模型
        if (!this.selectedModel) {
          console.error('未选择模型');
          throw new Error('请选择AI模型');
        }
        
        // 准备所有消息历史
        const messages = [{ role: 'user', content: prompt }];
        
        // 构建API请求参数
        const apiParams = {
          model: 'deepseek-v3',  // 使用与CopywritingGenerator.vue相同的模型名称
          messages: messages,
          stream: true,
          temperature: 0.7,
          max_tokens: 2000,
          return_reasoning: this.selectedModel.includes('r1') // 如果是R1模型，则启用思考过程
        };
        
        try {
          // 重置生成的内容已经在generateArticle方法中完成
          // 开始流式状态
          this.isStreaming = true;
          
          // 发送API请求，使用fetch API来处理流式响应
          const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'text/event-stream'
            },
            body: JSON.stringify(apiParams)
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
                    throw new Error(parsed.error.message || '生成文章失败');
                  }
                  
                  // 处理火山引擎返回的delta格式数据
                  if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                    const delta = parsed.choices[0].delta;
                    
                    // 处理思考过程（如果有）
                    if (delta.reasoning_content) {
                      console.log("收到思考过程:", delta.reasoning_content);
                      // 这里可以添加思考过程的处理逻辑，如果需要的话
                    }
                    
                    // 处理内容增量
                    if (delta.content) {
                      const contentDelta = delta.content;
                      console.log("收到内容增量:", contentDelta);
                      
                      // 累加收到的内容到数据模型
                      this.generatedArticle += contentDelta;
                      
                      // 创建高亮效果的内容元素
                      const latestContent = document.createElement('span');
                      latestContent.textContent = contentDelta;
                      latestContent.className = 'latest';
                      
                      // 根据当前模式选择正确的内容容器
                      let contentContainer = null;
                      if (this.isPhoneMode) {
                        // 手机模式下找到微信文章内容区域
                        contentContainer = document.querySelector('.wechat-article-content');
                      } else {
                        // 普通模式下找到文章内容区域
                        contentContainer = document.querySelector('.article-content');
                      }
                      
                      // 如果找到了容器并且当前正处于流式输出状态
                      if (contentContainer && this.isStreaming) {
                        // 清空当前内容并重新渲染带有高亮效果的内容
                        // 由于v-html绑定，我们需要特殊处理
                        
                        // 1. 暂时移除v-html的绑定
                        if (this.isPhoneMode) {
                          const phoneContainer = document.querySelector('.wechat-article-content');
                          if (phoneContainer) {
                            // 第一次收到增量内容时替换整个内容区域
                            if (phoneContainer.getAttribute('v-html')) {
                              phoneContainer.removeAttribute('v-html');
                              phoneContainer.innerHTML = this.generatedArticle.slice(0, -contentDelta.length);
                              phoneContainer.appendChild(latestContent);
                            } else {
                              // 后续内容直接添加
                              phoneContainer.appendChild(latestContent);
                            }
                          }
                        } else {
                          const normalContainer = document.querySelector('.article-content');
                          if (normalContainer) {
                            // 第一次收到增量内容时替换整个内容区域
                            if (normalContainer.getAttribute('v-html')) {
                              normalContainer.removeAttribute('v-html');
                              normalContainer.innerHTML = this.generatedArticle.slice(0, -contentDelta.length);
                              normalContainer.appendChild(latestContent);
                            } else {
                              // 后续内容直接添加
                              normalContainer.appendChild(latestContent);
                            }
                          }
                        }
                      }
                      
                      // 强制滚动到最新内容区域
                      this.$nextTick(() => {
                        const resultArea = this.isPhoneMode 
                          ? document.querySelector('.wechat-article-container') 
                          : document.querySelector('.article-result');
                        if (resultArea) {
                          resultArea.scrollTop = resultArea.scrollHeight;
                        }
                      });
                    }
                  }
                  // 处理标准格式的思考过程
                  else if (parsed.reasoning) {
                    console.log("收到标准思考过程:", parsed.reasoning);
                    // 这里可以添加思考过程的处理逻辑，如果需要的话
                  }
                  // 处理完整思考过程
                  else if (parsed.full_reasoning) {
                    console.log("收到完整思考过程");
                    // 这里可以添加完整思考过程的处理逻辑，如果需要的话
                  }
                  // 处理旧版格式增量数据（如果有）
                  else if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta && parsed.choices[0].delta.content) {
                    const contentDelta = parsed.choices[0].delta.content;
                    console.log("收到旧版内容增量:", contentDelta);
                    // 累加收到的内容
                    this.generatedArticle += contentDelta;
                    
                    // 可以添加与上面相同的显示效果代码
                  }
                } catch (e) {
                  console.error('解析流式数据失败:', e, data);
                }
              }
            }
          }
          
          // 处理完成，移除流式状态
          this.isStreaming = false;
          
          return {
            text: this.generatedArticle,
            offlineMode: false
          };
          
        } catch (error) {
          console.error('API调用异常:', error);
          // 结束流式状态
          this.isStreaming = false;
          
          // 判断是否是网络错误或服务器不可用
          if (error.code === 'ECONNABORTED' || !error.response || error.message.includes('Network Error')) {
            console.warn('后端服务不可用，切换到离线模式');
            // 离线模式
            return this.generateOfflineContent();
          }
          
          // 其他API错误
          throw error;
        }
      } catch (error) {
        console.error('文章生成失败:', error);
        // 确保结束流式状态
        this.isStreaming = false;
        
        // 根据错误类型提供更具体的错误信息
        let errorMessage = '生成公众号文章失败';
        
        if (error.response) {
          // 服务器响应了，但状态码不在2xx范围
          console.error('错误响应数据:', error.response.data);
          errorMessage += `: 服务器错误 (${error.response.status})`;
          if (error.response.data && error.response.data.message) {
            errorMessage += ` - ${error.response.data.message}`;
          }
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到响应');
          errorMessage += ': 服务器无响应，切换到离线模式';
          
          // 后端不可用时直接返回离线模式结果
          return this.generateOfflineContent();
        } else {
          // 请求设置时出错
          errorMessage += `: ${error.message}`;
        }
        
        throw new Error(errorMessage);
      }
    },
    
    // 离线模式下生成基本文章
    generateOfflineContent() {
      console.log('使用离线模式生成公众号文章');
      
      // 获取基本信息
      const title = this.articleTitle || '公众号文章标题';
      const type = this.articleType || 'knowledge';
      const keywords = this.articleKeywords || '';
      
      // 根据不同类型的模板生成不同的基础文章
      let content = '';
      const currentDate = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
      
      // 添加标题
      content = `# ${title}\n\n`;
      content += `*发布日期：${currentDate}*\n\n`;
      
      // 添加导语
      content += `> 导语：这是一篇关于${keywords}的${this.getArticleTypeName(type)}文章，希望能给${this.targetAudience}带来有价值的内容。\n\n`;
      
      // 根据文章类型添加不同的模板内容
      switch (type) {
        case 'knowledge':
          content += `## 什么是${keywords}？\n\n这部分将解释${keywords}的基本概念和背景知识。\n\n`;
          content += `## ${keywords}的主要特点\n\n1. 特点一：这里是详细解释\n2. 特点二：这里是详细解释\n3. 特点三：这里是详细解释\n\n`;
          content += `## ${keywords}的应用场景\n\n在实际生活中，${keywords}有着广泛的应用...\n\n`;
          content += `## 专家观点\n\n根据行业专家的看法，${keywords}未来的发展趋势...\n\n`;
          break;
          
        case 'story':
          content += `## 故事的开始\n\n一切要从那个平凡的日子说起，关于${keywords}的故事...\n\n`;
          content += `## 转折点\n\n然而，事情并没有想象中那么简单...\n\n`;
          content += `## 感悟与启示\n\n通过这个故事，我们可以得到以下启示：\n1. 启示一\n2. 启示二\n3. 启示三\n\n`;
          break;
          
        case 'opinion':
          content += `## 当前背景\n\n在讨论${keywords}之前，我们需要了解当前的情况...\n\n`;
          content += `## 我的观点\n\n对于${keywords}，我认为...\n\n`;
          content += `## 支持论据\n\n以下事实和数据支持我的观点：\n1. 论据一\n2. 论据二\n3. 论据三\n\n`;
          content += `## 反方观点及回应\n\n有人可能会提出不同意见，比如...\n对此，我的回应是...\n\n`;
          break;
          
        case 'tutorial':
          content += `## ${keywords}教程概述\n\n本教程将指导您如何...\n\n`;
          content += `## 准备工作\n\n在开始之前，您需要准备以下内容：\n1. 准备一\n2. 准备二\n3. 准备三\n\n`;
          content += `## 步骤一：开始入门\n\n详细步骤描述...\n\n`;
          content += `## 步骤二：进阶技巧\n\n详细步骤描述...\n\n`;
          content += `## 常见问题及解答\n\nQ1: 问题一？\nA1: 回答一\n\nQ2: 问题二？\nA2: 回答二\n\n`;
          break;
          
        case 'industry':
          content += `## ${keywords}行业现状\n\n当前，${keywords}行业正处于...\n\n`;
          content += `## 市场趋势分析\n\n根据最新数据，${keywords}市场呈现以下趋势：\n1. 趋势一\n2. 趋势二\n3. 趋势三\n\n`;
          content += `## 典型企业案例\n\n在${keywords}领域，以下企业表现突出：...\n\n`;
          content += `## 未来发展预测\n\n展望未来，${keywords}行业可能会...\n\n`;
          break;
          
        case 'list':
          content += `## ${keywords}必知要点\n\n以下是关于${keywords}的重要信息：\n\n`;
          content += `### 1. 第一要点\n\n详细描述...\n\n`;
          content += `### 2. 第二要点\n\n详细描述...\n\n`;
          content += `### 3. 第三要点\n\n详细描述...\n\n`;
          content += `### 4. 第四要点\n\n详细描述...\n\n`;
          content += `### 5. 第五要点\n\n详细描述...\n\n`;
          break;
          
        case 'interview':
          content += `## 嘉宾介绍\n\n今天我们有幸邀请到了${keywords}领域的专家...\n\n`;
          content += `## 访谈内容\n\n`;
          content += `Q1: 能否向读者介绍一下您眼中的${keywords}？\n\nA1: 详细回答...\n\n`;
          content += `Q2: 您认为${keywords}的发展前景如何？\n\nA2: 详细回答...\n\n`;
          content += `Q3: 对于想要进入${keywords}领域的新人，您有什么建议？\n\nA3: 详细回答...\n\n`;
          content += `## 访谈总结\n\n通过本次访谈，我们了解到...\n\n`;
          break;
          
        case 'case':
          content += `## 案例背景\n\n${keywords}的案例背景是...\n\n`;
          content += `## 问题与挑战\n\n在这个案例中，面临的主要挑战包括：\n1. 挑战一\n2. 挑战二\n3. 挑战三\n\n`;
          content += `## 解决方案\n\n针对上述挑战，采取了以下解决方案：...\n\n`;
          content += `## 结果与成效\n\n通过实施上述方案，取得了以下成效：...\n\n`;
          content += `## 经验与教训\n\n从此案例中，我们可以总结出以下经验和教训：...\n\n`;
          break;
          
        default:
          content += `## ${keywords}的主要内容\n\n这是关于${keywords}的主要内容...\n\n`;
          content += `## 为什么${keywords}很重要\n\n${keywords}之所以重要，是因为...\n\n`;
          content += `## 如何更好地理解${keywords}\n\n要更好地理解${keywords}，我们可以...\n\n`;
      }
      
      // 添加文章结尾
      content += `## 结语\n\n以上就是关于${keywords}的全部内容，希望对${this.targetAudience}有所帮助。如果您有任何问题或想法，欢迎在评论区留言，我们一起讨论。\n\n`;
      content += `*【本文为离线模式生成的示例文章，仅供参考】*`;
      
      return {
        text: content,
        offlineMode: true
      };
    },
    
    // 获取文章类型的中文名称
    getArticleTypeName(type) {
      const typeMap = {
        'knowledge': '知识科普',
        'story': '故事感悟',
        'opinion': '观点评论',
        'tutorial': '教程指南',
        'industry': '行业分析',
        'list': '清单合集',
        'interview': '访谈问答',
        'case': '案例分析'
      };
      return typeMap[type] || '知识科普';
    },
    
    // 复制生成的结果
    copyResult() {
      if (!this.generatedArticle) return;
      
      try {
        // 检查是否支持clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(this.generatedArticle)
            .then(() => {
              this.$message ? this.$message.success('文章已复制到剪贴板') : 
                alert('文章已复制到剪贴板');
            })
            .catch(err => {
              console.error('复制失败:', err);
              this.fallbackCopy(this.generatedArticle);
            });
        } else {
          // 浏览器不支持clipboard API，使用备选方法
          this.fallbackCopy(this.generatedArticle);
        }
      } catch (error) {
        console.error('复制操作异常:', error);
        this.fallbackCopy(this.generatedArticle);
      }
    },
    
    // 显示提示词模态框
    showPrompt() {
      if (this.lastUsedPrompt) {
        console.log('显示提示词模态框');
        this.showPromptModal = true;
      } else {
        this.$message ? this.$message.info('请先生成文章以查看提示词') : 
          alert('请先生成文章以查看提示词');
      }
    },
    
    // 复制提示词到剪贴板
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      
      try {
        // 检查是否支持clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(this.lastUsedPrompt)
            .then(() => {
              this.$message ? this.$message.success('提示词已复制到剪贴板') : 
                alert('提示词已复制到剪贴板');
            })
            .catch(err => {
              console.error('复制失败:', err);
              this.fallbackCopy(this.lastUsedPrompt);
            });
        } else {
          // 浏览器不支持clipboard API，使用备选方法
          this.fallbackCopy(this.lastUsedPrompt);
        }
      } catch (error) {
        console.error('复制操作异常:', error);
        this.fallbackCopy(this.lastUsedPrompt);
      }
    },
    
    // 备选的复制方法
    fallbackCopy(text) {
      try {
        // 创建临时textarea元素
        const textArea = document.createElement('textarea');
        textArea.value = text;
        
        // 设置样式使元素不可见
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        
        // 选择文本并执行复制命令
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        if (successful) {
          this.$message ? this.$message.success('内容已复制到剪贴板') : 
            alert('内容已复制到剪贴板');
        } else {
          this.$message ? this.$message.error('复制失败，请手动复制') : 
            alert('复制失败，请手动复制');
        }
        
        // 清理临时元素
        document.body.removeChild(textArea);
      } catch (err) {
        console.error('备选复制方法失败:', err);
        this.$message ? this.$message.error('复制失败，请手动复制文本') : 
          alert('复制失败，请手动复制文本');
      }
    },
    
    // 切换显示模式
    toggleDisplayMode() {
      this.isPhoneMode = !this.isPhoneMode;
    },
    
    // 添加Markdown格式化函数
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗文本
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理列表项
      text = text.replace(/\n\n/g, '<br><br>');
      
      return text;
    },
  }
}
</script>

<style scoped>
/* 引入统一样式文件 */
@import "@/assets/css/text-creation-common.css";

/* 只保留特定于WechatArticle的样式，其余使用统一样式 */
.wechat-article-page {
  padding: 10px;
}

/* 文章结果特有样式 */
.article-result {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  line-height: 1.6;
  font-size: 15px;
}

.article-content {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.article-content h1 {
  font-size: 24px;
  margin-top: 0;
  margin-bottom: 16px;
  color: #222;
  font-weight: 600;
}

.article-content h2 {
  font-size: 20px;
  margin-top: 24px;
  margin-bottom: 16px;
  color: #333;
  font-weight: 600;
}

.article-content h3 {
  font-size: 18px;
  margin-top: 20px;
  margin-bottom: 12px;
  color: #444;
  font-weight: 600;
}

.article-content p {
  margin-bottom: 16px;
  color: #333;
  line-height: 1.8;
}

.article-content ul, .article-content ol {
  margin-left: 20px;
  margin-bottom: 16px;
}

.article-content li {
  margin-bottom: 8px;
}

/* 流式输出相关样式 */
.streaming {
  position: relative;
}

.streaming-indicator {
  position: absolute;
  bottom: 30px;
  right: 30px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.dot-typing {
  position: relative;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--primary-color, #ba003f);
  box-shadow: 0 0 5px rgba(186, 0, 63, 0.5);
  animation: dot-typing 1.2s infinite linear;
}

.dot-typing::before,
.dot-typing::after {
  content: '';
  position: absolute;
  top: 0;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--primary-color, #ba003f);
  box-shadow: 0 0 5px rgba(186, 0, 63, 0.5);
  animation: dot-typing 1.2s infinite linear;
}

.dot-typing::before {
  left: -12px;
  animation-delay: 0s;
}

.dot-typing::after {
  left: 12px;
  animation-delay: 0.8s;
}

@keyframes dot-typing {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.5);
    opacity: 0.6;
  }
}

/* 添加打字机效果 */
.streaming .article-content {
  position: relative;
}

.streaming .article-content::after {
  content: '|';
  display: inline-block;
  color: var(--primary-color, #ba003f);
  font-weight: bold;
  font-size: 20px;
  animation: blink 0.5s infinite;
  position: relative;
  margin-left: 4px;
  vertical-align: middle;
}

/* 普通视图模式样式 */
.normal-article-view {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* 离线模式提示条 */
.offline-mode-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #fff9e6;
  border: 1px solid #ffeeba;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 15px;
  color: #856404;
  font-size: 14px;
}

.offline-mode-banner i {
  font-size: 18px;
}

/* 提示词按钮样式 */
.prompt-button {
  background-color: var(--primary-color, #ba003f);
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
}

.prompt-button:hover {
  background-color: #980034;
}

.toggle-display-button {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #495057;
}

.toggle-display-button:hover {
  background-color: #e5e5e5;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 手机视图模式样式 */
.phone-preview-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

/* 提示词模态框样式 */
.prompt-modal .modal-body {
  padding: 0;
}

.prompt-content {
  padding: 20px;
  background-color: #272822; /* Monokai背景色 */
  border-radius: 0 0 8px 8px;
  overflow-x: auto;
}

.prompt-content pre {
  margin: 0;
  color: #f8f8f2; /* Monokai文本色 */
  font-family: "Consolas", "Monaco", monospace;
  line-height: 1.6;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
}

.prompt-actions {
  padding: 15px;
  background-color: #f8f9fa;
  display: flex;
  justify-content: flex-end;
  border-radius: 0 0 8px 8px;
  border-top: 1px solid #eee;
}

/* 添加知识学习抽屉的样式 */
.knowledge-content {
  padding: 20px;
}

.knowledge-section {
  margin-bottom: 25px;
}

.knowledge-subtitle {
  color: var(--primary-color, #ba003f);
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid rgba(186, 0, 63, 0.2);
  padding-bottom: 8px;
  display: flex;
  align-items: center;
}

.knowledge-text {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
}

.knowledge-text p {
  margin-bottom: 12px;
}

.knowledge-text ul, .knowledge-text ol {
  padding-left: 20px;
  margin-bottom: 12px;
}

.knowledge-text li {
  margin-bottom: 8px;
}

.knowledge-text strong {
  color: var(--primary-color, #ba003f);
  font-weight: 600;
}

.knowledge-text a {
  color: var(--primary-color, #ba003f);
  text-decoration: none;
}

.knowledge-text a:hover {
  text-decoration: underline;
}

.knowledge-icon {
  margin-right: 8px;
  font-size: 20px;
}

/* 自定义参数样式 */
.custom-params-section {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  margin-top: 15px;
  background-color: #fafafa;
}

.custom-params-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.add-param-btn {
  background-color: #e9ecef;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #495057;
}

.add-param-btn:hover {
  background-color: #dee2e6;
}

.custom-param-tip {
  font-size: 12px;
  color: #6c757d;
  font-weight: normal;
}

.empty-params-tip {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  color: #6c757d;
  display: flex;
  align-items: center;
  gap: 8px;
}

.empty-params-tip i {
  font-size: 20px;
  color: #adb5bd;
}

.custom-param-item {
  margin-bottom: 10px;
}

.param-input-group {
  display: flex;
  gap: 10px;
}

.param-key {
  width: 30%;
  flex-shrink: 0;
}

.param-value {
  flex-grow: 1;
}

.remove-param-btn {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  padding: 0 5px;
  font-size: 18px;
  align-self: center;
}

.remove-param-btn:hover {
  color: #bd2130;
}

/* 服务不可用提示 */
.service-unavailable {
  padding: 12px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.service-unavailable i {
  font-size: 20px;
}

.model-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 5px;
  font-size: 14px;
  color: #6c757d;
}

.model-loading i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.mobile-preview {
  width: 375px;
  height: 667px;
  position: relative;
  overflow: hidden;
  margin: 0 auto;
}

/* 高亮关键词样式 */
.keyword-highlight {
  background-color: rgba(186, 0, 63, 0.1);
  color: var(--primary-color, #ba003f);
  padding: 0 2px;
  border-radius: 2px;
  font-weight: 500;
}

/* 文章强调段落样式 */
.article-emphasis {
  border-left: 3px solid var(--primary-color, #ba003f);
  padding-left: 15px;
  font-weight: 500;
}

/* 文章引用样式 */
.article-quote {
  background-color: #f3f4f6;
  border-left: 4px solid #ced4da;
  padding: 12px 15px;
  margin: 15px 0;
  font-style: italic;
  color: #495057;
}

/* 手机预览样式已经在mobile-preview.css中定义 */
</style> 