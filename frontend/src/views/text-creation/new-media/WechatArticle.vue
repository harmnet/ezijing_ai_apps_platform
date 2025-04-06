<template>
  <div class="wechat-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>公众号文章生成</h2>
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
              <div class="example-card" v-for="(example, index) in examples" :key="index" @click="loadExample('example' + (index + 1))">
                <div class="example-icon">
                  <i :class="example.icon"></i>
                </div>
                <div class="example-info">
                  <span class="example-title">{{ example.title }}</span>
                  <span class="example-desc">{{ example.desc }}</span>
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
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isLoading" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedArticle && !isLoading" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无文章内容，请点击"生成公众号文章"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedArticle" class="article-result" :class="{'blur-content': isLoading}">
              <!-- 添加离线模式提示条 -->
              <div v-if="isOfflineGenerated" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板文章。要获得AI生成的更优质文章，请联系管理员启动后端服务。</span>
              </div>
              
              <div class="article-content" v-html="formattedArticle"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line"></i> 创作小贴士</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>公众号文章标题要有吸引力，可以使用"数字+疑问+情感"结构</li>
            <li>开篇第一段至关重要，要能迅速吸引读者注意力</li>
            <li>适当使用小标题分段，让文章结构更清晰</li>
            <li>图文结合的内容更易引起读者共鸣和互动</li>
            <li>结尾部分可设置互动话题，增加粉丝互动率</li>
            <li>尝试多种写作风格，找到最适合您目标受众的表达方式</li>
            <li>定期分析阅读数据，了解读者喜好，针对性优化内容</li>
          </ul>
        </div>
      </div>
    </div>
    
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
      selectedModel: 'deepseek-v3-vol',
      isGenerating: false,
      isLoading: false,
      loadingText: '正在生成公众号文章...',
      validationErrors: [],
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      examples: [
        { title: '农业科技', desc: '智慧农业新趋势', icon: 'ri-seedling-line', 
          articleType: 'industry', writingStyle: 'professional' },
        { title: '冰雪产业', desc: '冬奥带动冰雪经济', icon: 'ri-snowy-line', 
          articleType: 'industry', writingStyle: 'analytical' },
        { title: '交通出行', desc: '智能交通新时代', icon: 'ri-train-line', 
          articleType: 'knowledge', writingStyle: 'professional' },
        { title: '新能源车', desc: '电动未来已来临', icon: 'ri-battery-charge-line', 
          articleType: 'opinion', writingStyle: 'analytical' },
        { title: '金融科技', desc: '数字金融新变革', icon: 'ri-bank-line', 
          articleType: 'industry', writingStyle: 'professional' },
        { title: '云计算', desc: '云端科技新体验', icon: 'ri-cloud-line', 
          articleType: 'knowledge', writingStyle: 'professional' },
        { title: '健康医疗', desc: '智慧医疗新未来', icon: 'ri-heart-pulse-line', 
          articleType: 'tutorial', writingStyle: 'conversational' },
        { title: '游戏产业', desc: '元宇宙与游戏融合', icon: 'ri-gamepad-line', 
          articleType: 'opinion', writingStyle: 'humorous' },
        { title: '房地产', desc: '智慧地产新模式', icon: 'ri-building-line', 
          articleType: 'case', writingStyle: 'analytical' },
        { title: '在线教育', desc: '数字化学习革命', icon: 'ri-book-line', 
          articleType: 'knowledge', writingStyle: 'inspirational' }
      ],
      customParams: []
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
            return `<h1>${para.substring(2)}</h1>`;
          } else if (para.startsWith('## ')) {
            return `<h2>${para.substring(3)}</h2>`;
          } else if (para.startsWith('### ')) {
            return `<h3>${para.substring(4)}</h3>`;
          } else {
            return `<p>${para.replace(/\n/g, '<br>')}</p>`;
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
        console.log('获取模型响应:', response);
        
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
          
          console.log('可用模型:', this.modelList);
          
          // 默认选择火山引擎的DeepSeek V3模型
          this.selectedModel = 'deepseek-v3-vol';
          
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
        { id: 'deepseek-v3-vol', name: 'DeepSeek-V3（火山引擎）' },
        { id: 'qwen-max', name: '通义千问-Max（阿里云）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3-vol';
    },
    
    // 显示创作小贴士
    showTips() {
      console.log('显示创作小贴士模态框');
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
    
    // 生成公众号文章
    async generateArticle() {
      if (this.isLoading) return;
      
      try {
        this.validationErrors = [];
        
        // 验证必填字段
        if (!this.articleTitle.trim()) {
          this.validationErrors.push('请输入文章标题');
        }
        if (!this.targetAudience.trim()) {
          this.validationErrors.push('请输入目标读者群体');
        }
        if (!this.articleKeywords.trim()) {
          this.validationErrors.push('请输入文章关键词或内容要点');
        }
        
        if (this.validationErrors.length > 0) {
          const errorMsg = this.validationErrors.join('，');
          this.$message ? this.$message.error(errorMsg) : alert(errorMsg);
          return;
        }
        
        // 显示加载状态
        this.isLoading = true;
        this.isGenerating = true;
        this.loadingText = '正在生成公众号文章...';
        
        // 构建提示词
        const prompt = this.buildPrompt();
        
        // 调用API并获取结果
        const result = await this.callLLMApi(prompt);
        
        // 更新文章内容
        this.generatedArticle = result.text || '';
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
        
        console.log(`正在调用API，使用模型: ${this.selectedModel}，提示词长度: ${prompt.length}`);
        
        // 构建API请求参数
        const apiParams = {
          model: this.selectedModel,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 3000
        };
        
        // 记录API请求详情，方便调试
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        try {
          // 发送API请求
          const response = await axios.post('/api/v1/llm/chat', apiParams, { timeout: 60000 });
          console.log('API响应:', response);
          
          if (response.data.status === 'success') {
            const content = response.data.data.choices[0].message.content;
            console.log('成功获取到结果:', content);
            
            return {
              text: content,
              offlineMode: false
            };
          } else {
            console.error('API返回错误:', response.data.message);
            throw new Error(`服务器返回错误: ${response.data.message || '未知错误'}`);
          }
        } catch (error) {
          console.error('API调用异常:', error);
          
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
    }
  }
}
</script>

<style scoped>
.wechat-article-page {
  padding: 0;
  margin-top: -40px; /* 只保留这个负边距使整体上移，数值调大 */
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
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
}

/* 左侧：输入参数 */
.input-section {
  width: 45%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 15px;
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
  height: 54px; /* 原来36px的1.5倍 */
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
  background-color: #980034;
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.2);
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #eee;
}

.btn-secondary:hover {
  background-color: #e5e5e5;
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.15);
  transform: translateY(-2px);
}

/* 右侧：参考案例和结果 */
.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 添加参考案例和结果之间的间距 */
}

/* 参考案例部分 - 轮播形式 */
.examples-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 12px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  margin-bottom: 0; /* 移除底部边距 */
}

.examples-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.section-title {
  display: flex;
  align-items: center;
  color: #333;
  font-size: 16px;
  margin: 0 0 10px 0;
  font-weight: 600;
}

.section-title i {
  margin-right: 8px;
  font-size: 20px;
  color: var(--primary-color, #ba003f);
}

.example-carousel {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding-bottom: 5px; /* 添加底部间距避免阴影被裁剪 */
}

.example-cards {
  display: flex;
  gap: 15px;
  transition: transform 0.3s ease;
  will-change: transform;
  padding: 5px 0;
  width: max-content; /* 确保足够宽以容纳所有内容 */
}

.example-card {
  flex: 0 0 170px; /* 减小固定宽度，显示更多案例 */
  display: flex;
  align-items: center;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 12px 15px;
  cursor: pointer;
  transition: all 0.3s;
  flex-direction: row;
  gap: 12px;
  overflow: hidden; /* 防止内容溢出 */
}

.example-card:hover {
  border-color: var(--primary-color, #ba003f);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.example-icon {
  width: 45px;
  height: 45px;
  min-width: 45px;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0;
}

.example-icon i {
  font-size: 24px;
  color: var(--primary-color, #ba003f);
}

.example-info {
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 14px;
  overflow: hidden; /* 防止溢出 */
}

.example-title {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 15px;
}

.example-desc {
  font-size: 14px;
  color: #666;
  display: block; /* 始终显示描述 */
  overflow: hidden;
  text-overflow: ellipsis; /* 文本过长时显示省略号 */
  white-space: nowrap; /* 确保单行显示 */
}

/* 轮播控制按钮样式 */
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
}

.carousel-control:hover {
  background-color: var(--primary-color, #ba003f);
  color: white;
  border-color: var(--primary-color, #ba003f);
}

.carousel-control i {
  font-size: 18px;
}

/* 结果展示部分 */
.result-section {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 0; /* 移除内边距 */
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
}

.section-header h2 {
  margin: 0;
  font-size: 18px; /* 减小标题大小 */
}

.result-content-wrapper {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 300px; /* 确保有足够的高度显示加载动画 */
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

.primary-button {
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

.primary-button:hover {
  background-color: #980034;
}

.secondary-button {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #eee;
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
}

.secondary-button:hover {
  background-color: #e5e5e5;
}

.section-header-fixed {
  position: relative;
  top: 0;
  background-color: #fff;
  z-index: 100;
  padding: 15px 15px 20px; /* 增加底部内边距从10px到20px */
  margin: -15px -15px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-header-placeholder {
  display: none;
}

/* 模态框样式 */
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
  z-index: 9999;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
  animation: modal-pop 0.3s ease-out;
}

@keyframes modal-pop {
  0% { transform: scale(0.9); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
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
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-header h3 i {
  color: var(--primary-color, #ba003f);
}

.close-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 20px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: calc(80vh - 60px);
}

/* 小贴士样式 */
.tips-list {
  padding-left: 20px;
  margin: 0;
}

.tips-list li {
  margin-bottom: 12px;
  color: #555;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 5;
  border-radius: 0 0 8px 8px; /* 圆角与结果区域一致 */
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color, #ba003f);
  animation: spin 1s ease-in-out infinite;
  margin: 0 auto 20px;
}

.loading-text {
  font-size: 16px;
  color: var(--primary-color, #ba003f);
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 350px;
  background-color: #fff;
  border-radius: 8px;
  color: #666;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
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

/* 禁用状态的轮播按钮 */
.carousel-control.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.carousel-control.disabled:hover {
  background-color: #fff;
  color: inherit;
  border-color: #ddd;
}

.blur-content {
  filter: blur(1px);
  opacity: 0.6;
  pointer-events: none; /* 防止与模糊内容交互 */
}

/* 为按钮添加禁用状态样式 */
.primary-button:disabled,
.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #ccc;
  color: #666;
  border-color: #ccc;
}

.primary-button:disabled:hover {
  background-color: #ccc;
  transform: none;
  box-shadow: none;
}

.secondary-button:disabled:hover {
  background-color: #f5f5f5;
  transform: none;
}

/* 添加旋转动画样式 */
.spinning {
  animation: spin 1.5s linear infinite;
  display: inline-block;
}

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

.prompt-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #ccc;
  color: #666;
}

/* 提示词模态框样式 */
.prompt-modal {
  width: 90%;
  max-width: 1000px;
}

.prompt-content {
  background-color: #f5f5f5;
  border-radius: 6px;
  padding: 15px;
  overflow-x: auto;
  font-family: Consolas, Monaco, 'Andale Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  white-space: pre-wrap;
  max-height: 50vh;
  overflow-y: auto;
}

.prompt-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

/* 响应式布局 */
@media (max-width: 1400px) {
  .example-card {
    flex: 0 0 160px; /* 在较窄的屏幕上减小卡片宽度 */
  }
}

@media (max-width: 1200px) {
  .example-card {
    flex: 0 0 140px; /* 在更窄的屏幕上进一步减小卡片宽度 */
  }
}

@media (max-width: 992px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section, .right-column {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .example-cards {
    justify-content: flex-start;
  }
  
  .example-card {
    flex: 0 0 130px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
}

/* 自定义参数样式 */
.custom-params-section {
  margin-top: 15px;
  border: 1px dashed #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #fafafa;
}

.custom-params-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.custom-param-tip {
  font-weight: normal;
  font-size: 13px;
  color: #666;
}

.add-param-btn {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}

.add-param-btn:hover {
  background-color: #e0e0e0;
  color: var(--primary-color, #ba003f);
}

.empty-params-tip {
  color: #666;
  font-size: 14px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.custom-param-item {
  margin-bottom: 10px;
  animation: fade-in 0.3s ease-out;
}

.param-input-group {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.param-key {
  flex: 0 0 150px;
}

.param-value {
  flex: 1;
}

.remove-param-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 18px;
  padding: 6px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-param-btn:hover {
  color: #d9534f;
  background-color: rgba(217, 83, 79, 0.1);
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 模型选择下拉菜单特殊样式 */
#model-select {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  font-weight: 500;
  position: relative;
}

#model-select:focus {
  background-color: #fff;
  border-color: var(--primary-color, #ba003f);
}

/* 下拉菜单选项样式 */
select.form-control option {
  font-weight: normal;
  background-color: white;
  color: #333;
  padding: 8px;
}

/* 加载状态指示器样式 */
.model-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #777;
  margin-top: 6px;
}

.model-loading i {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(186, 0, 63, 0.3);
  border-radius: 50%;
  border-top-color: var(--primary-color, #ba003f);
  animation: modelSpin 1s linear infinite;
}

@keyframes modelSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 生成结果容器样式 */
.generated-content {
  transition: all 0.5s ease;
}

.generated-content:hover {
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}
</style> 