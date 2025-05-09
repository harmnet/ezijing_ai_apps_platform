<template>
  <div class="ad-slogan-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>广告语生成</h2>
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
        <div class="form-row">
          <div class="form-group">
            <label for="product-name" class="required">产品/服务名称</label>
            <input 
              type="text" 
              id="product-name" 
              v-model="productName" 
              placeholder="请输入产品或服务名称"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="target-audience" class="required">目标受众</label>
            <input 
              type="text" 
              id="target-audience" 
              v-model="targetAudience" 
              placeholder="例如：18-35岁的年轻白领、户外运动爱好者等"
              class="form-control"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="product-description" class="required">产品/服务描述</label>
          <textarea 
            id="product-description" 
            v-model="productDescription" 
            placeholder="请描述产品/服务的特点、优势等"
            class="form-control"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="slogan-style">语调风格</label>
            <select id="slogan-style" v-model="sloganStyle" class="form-control">
              <option value="professional">专业正式</option>
              <option value="friendly">亲切友好</option>
              <option value="humorous">幽默风趣</option>
              <option value="dramatic">戏剧性强</option>
              <option value="inspirational">鼓舞人心</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="slogan-count">生成数量</label>
            <select id="slogan-count" v-model="sloganCount" class="form-control">
              <option value="3">3个</option>
              <option value="5">5个</option>
              <option value="10">10个</option>
            </select>
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
          <button class="btn btn-primary" @click="generateSlogans" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '正在生成...' : '生成广告语' }}
          </button>
          <button class="btn btn-secondary" @click="resetForm">
            <i class="ri-refresh-line"></i> 重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：参考案例和结果 -->
      <div class="right-column">
        <!-- 参考案例部分 - 改为轮播形式 -->
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
                  <span class="example-brand">{{ example.title }}</span>
                  <span class="example-slogan">{{ example.desc }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 结果展示部分 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-markup-line"></i>
              广告语结果
            </h3>
            <div class="action-buttons">
              <button @click="generateSlogans" class="primary-button" :disabled="isLoading">
                <i class="ri-refresh-line" v-if="!isLoading"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isLoading ? '生成中...' : '重新生成' }}
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
            
            <div v-if="slogans.length === 0 && !isLoading" class="empty-result">
              <div class="empty-content">
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无广告语，请点击"生成广告语"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="slogans.length > 0" class="slogan-results" :class="{'blur-content': isLoading}">
              <!-- 添加离线模式提示条 -->
              <div v-if="showOfflineBanner" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板广告语。要获得AI生成的更优质广告语，请联系管理员启动后端服务。</span>
              </div>
              
              <div v-for="(slogan, index) in slogans" :key="index" class="slogan-item">
                <div class="slogan-number">
                  <span>{{ index + 1 }}</span>
                </div>
                <div class="slogan-content">{{ slogan.text }}</div>
                <div class="slogan-actions">
                  <button @click="copySlogan(slogan.text)" class="action-button">
                    <i class="ri-file-copy-line"></i>
                    复制
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士侧边栏 -->
    <el-drawer
      v-model="showTipsModal"
      title="广告语创作指南"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in adSloganKnowledge" :key="index" class="knowledge-section">
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
import '@/assets/css/text-creation-common.css'

// 创建axios实例，配置baseURL
const apiClient = axios.create({
  baseURL: 'http://localhost:9000', // 后端服务地址
  timeout: 30000 // 请求超时时间
});

export default {
  name: 'AdSlogan',
  data() {
    return {
      productName: '',
      productDescription: '',
      targetAudience: '',
      sloganStyle: 'professional',
      sloganCount: 5,
      slogans: [],
      showTipsModal: false,
      showPromptModal: false,
      lastUsedPrompt: '',
      modelList: [],
      selectedModel: 'deepseek-v3-vol',
      isGenerating: false,
      errorMessage: '',
      isLoading: false,
      loadingText: '',
      validationErrors: [],
      // 添加广告语概念知识数据
      adSloganKnowledge: [
        {
          subtitle: '广告语的定义与作用',
          icon: 'ri-question-line',
          text: '广告语（Slogan）是广告创意的核心表达，是品牌识别系统中的关键听觉元素。在市场营销学中，广告语作为品牌传播的重要载体，具有提高品牌识别度、传递品牌核心价值、增强用户记忆和促进购买决策的功能。现代广告语不仅是产品信息的传递者，更是品牌文化和情感连接的建立者。'
        },
        {
          subtitle: '广告语的理论基础',
          icon: 'ri-book-line',
          text: '**AIDA模型**：优秀广告语遵循注意(Attention)、兴趣(Interest)、欲望(Desire)和行动(Action)的心理路径。\n\n**USP理论**：独特销售主张(Unique Selling Proposition)强调广告语应凸显产品独特优势。\n\n**品牌定位理论**：广告语是品牌定位的直接表达，应符合品牌在用户心智中的预期位置。\n\n**消费者行为学**：广告语设计应基于目标受众的认知特点、价值观和行为习惯。\n\n**修辞学原理**：运用比喻、拟人、对比等修辞手法增强表现力和记忆点。'
        },
        {
          subtitle: '广告语的类型与结构',
          icon: 'ri-folder-line',
          text: '**从表达方式看**：\n- 陈述型：直接阐述产品特性，如"农夫山泉，有点甜"\n- 诉求型：明确表达品牌主张，如"Just Do It"\n- 情感型：唤起情感共鸣，如"家是温暖的港湾"\n- 问题型：引发思考，如"你的电脑需要Intel Inside吗?"\n\n**从结构形式看**：\n- 单句式：简短有力，如"I\'m lovin\' it"\n- 对偶式：平行结构，如"好吃不上火，健康中国人"\n- 递进式：层层深入，如"想GET，就Go"\n- 反问式：设问引思，如"我的未来不是梦?"\n\n**从沟通目标看**：\n- 功能型：强调产品功能，如"给我一面墙，还您万丈光"\n- 形象型：塑造品牌形象，如"永远的经典"\n- 行动型：促使立即行动，如"就是要你买"'
        },
        {
          subtitle: '人工智能在广告语创作中的应用',
          icon: 'ri-robot-line',
          text: '**AI辅助创作原理**：现代大语言模型(如GPT、DeepSeek)通过分析海量文本数据，学习语言模式、修辞技巧和品牌表达，能够生成符合品牌调性的广告语候选。\n\n**AI创作优势**：\n- 创意多样性：短时间内生成多种表达方案\n- 语境适应性：根据不同产品特性快速调整创作方向\n- 数据驱动：基于历史成功案例的分析优化创作效果\n\n**人机协作最佳实践**：\n- 明确输入：提供详细的产品信息、目标受众和品牌调性\n- 创意筛选：AI生成多个方案后由人工进行筛选和优化\n- 迭代优化：根据反馈调整提示词(Prompt)获得更精准的结果\n\n**AI广告语评估标准**：\n- 相关性：与产品/服务的匹配程度\n- 独特性：区别于竞品的差异化表达\n- 记忆度：易于传播和记忆的程度\n- 情感共鸣：引发目标受众情感反应的能力'
        },
        {
          subtitle: '广告语创作的专业流程',
          icon: 'ri-flow-chart',
          text: '**市场调研**：分析目标受众、竞品广告语和市场定位。\n\n**品牌分析**：明确品牌核心价值、个性特征和传播目标。\n\n**创意发散**：头脑风暴多种表达方式，结合AI辅助生成多样化选项。\n\n**评估筛选**：根据CRITIC标准(创造性、相关性、影响力、信任度、独特性、清晰度)评估。\n\n**测试验证**：通过小规模用户测试评估记忆度和接受度。\n\n**落地应用**：将广告语融入整体营销传播体系，保持一致性。\n\n**效果追踪**：监测广告语在品牌识别、销售转化等方面的实际效果。'
        },
        {
          subtitle: '跨文化广告语创作与本地化',
          icon: 'ri-global-line',
          text: '**跨文化适应**：广告语在国际化过程中需要考虑语言、文化差异和地域禁忌。\n\n**本地化策略**：\n- 直译法：保持原意直接翻译，适用于简单明了的广告语\n- 意译法：保留核心概念，调整表达方式适应本地文化\n- 重创法：根据本地市场重新创作，保持品牌调性\n\n**经典案例**：\n- 可口可乐："Taste the Feeling"全球统一\n- 肯德基："Finger Lickin\' Good"在中国本地化为"吮指原味鸡"\n- 耐克："Just Do It"保持全球一致，强化品牌核心价值\n\n**AI辅助本地化**：利用多语言理解能力，AI可以协助评估广告语在不同文化背景下的含义和接受度，提供本地化建议。'
        }
      ],
      examples: [
        { title: 'Nike', desc: 'Just Do It', icon: 'ri-run-line', style: 'inspirational', productDesc: '专业运动鞋品牌，提供高品质运动装备，帮助运动员和健身爱好者追求卓越表现。', targetAudience: '运动爱好者、健身人士、专业运动员' },
        { title: 'Apple', desc: 'Think Different', icon: 'ri-apple-fill', style: 'professional', productDesc: '创新科技公司，提供易用、美观且功能强大的电子设备和服务，改变人们的生活方式。', targetAudience: '科技爱好者、创意工作者、商务人士' },
        { title: '小米', desc: '为发烧而生', icon: 'ri-smartphone-line', style: 'friendly', productDesc: '科技公司，提供高性价比的智能手机、智能家居和生活电子产品，注重用户体验。', targetAudience: '年轻人、科技爱好者、性价比追求者' },
        { title: '麦当劳', desc: '我就喜欢', icon: 'ri-restaurant-line', style: 'humorous', productDesc: '全球知名快餐连锁品牌，提供汉堡、薯条等快餐食品，以及舒适的用餐环境。', targetAudience: '家庭、青少年、上班族' },
        { title: '支付宝', desc: '信任，让简单更简单', icon: 'ri-bank-card-line', style: 'friendly', productDesc: '数字支付平台，提供安全、便捷的支付服务和多种生活服务功能。', targetAudience: '智能手机用户、网络购物人群' },
        { title: '特斯拉', desc: '驱动美好未来', icon: 'ri-flashlight-line', style: 'professional', productDesc: '电动汽车及清洁能源公司，生产创新电动汽车和可再生能源解决方案。', targetAudience: '环保意识强的消费者、科技爱好者、高端车主' },
        { title: '雪域滑雪场', desc: '纯净雪域，畅享极限', icon: 'ri-snowy-line', style: 'inspirational', productDesc: '位于天然雪山的高端滑雪度假胜地，提供专业滑雪道和舒适住宿体验。', targetAudience: '滑雪爱好者、冬季运动爱好者、家庭游客' },
        { title: '丰收农业', desc: '科技种植，健康收获', icon: 'ri-plant-line', style: 'friendly', productDesc: '现代化农业企业，使用智能科技种植有机农产品，注重环保和品质。', targetAudience: '健康生活追求者、有机食品消费者、农产品经销商' },
        { title: '安心保险', desc: '守护生活，安心未来', icon: 'ri-bank-line', style: 'dramatic', productDesc: '综合性保险公司，提供人寿、健康、财产等全方位保险服务，注重客户体验。', targetAudience: '家庭客户、企业客户、理财人士' },
        { title: '绿源能源', desc: '清洁能源，绿色生活', icon: 'ri-recycle-line', style: 'inspirational', productDesc: '专注于太阳能、风能等可再生能源开发的企业，提供家用和商用清洁能源解决方案。', targetAudience: '环保意识强的家庭、企业客户、政府机构' }
      ],
      currentExampleIndex: 0,
      visibleExamples: 4, // 一次显示的示例数量
      exampleTranslateX: 0 // 轮播位移值
    }
  },

  computed: {
    // 根据当前索引计算显示的示例
    displayedExamples() {
      return this.examples;
    },
    
    // 判断是否已经到达最后一页
    isLastPage() {
      if (!this.$el) return false;
      const carousel = this.$el.querySelector('.example-carousel');
      if (!carousel) return false;
      
      const maxVisibleCards = Math.floor(carousel.clientWidth / 295);
      return this.currentExampleIndex >= this.examples.length - maxVisibleCards;
    },
    
    // 获取当前选择的风格的中文名称
    currentStyleName() {
      const styleMap = {
        'professional': '专业正式',
        'friendly': '亲切友好',
        'humorous': '幽默风趣',
        'dramatic': '戏剧性强', 
        'inspirational': '励志鼓舞'
      };
      
      return styleMap[this.sloganStyle] || this.sloganStyle;
    },
    
    // 判断表单是否有效
    isFormValid() {
      return this.productName.trim() !== '';
    },
    
    // 判断是否显示离线模式提示
    showOfflineBanner() {
      return this.slogans.length > 0 && this.slogans[0].isOfflineGenerated;
    }
  },

  mounted() {
    this.getAvailableModels();
  },
  methods: {
    // 获取可用的大模型列表
    async getAvailableModels() {
      try {
        const response = await axios.get('/api/v1/llm/models');
        console.log('获取模型响应:', response);
        
        if (response.data.status === 'success') {
          // 获取模型列表
          const models = response.data.data;
          
          // 按照指定顺序排序模型
          const orderedModelIds = [
            'deepseek-v3-vol',  // DeepSeek-V3（火山引擎）- 放在第一位
            'deepseek-r1-vol',  // DeepSeek-R1（火山引擎）
            'deepseek-r1-sf',   // DeepSeek-R1（硅基流动）
            'deepseek-v3-sf',   // DeepSeek-V3（硅基流动）
            'qwq-32b',          // 通义千问-32B（硅基流动）
            'qwen-max',         // 通义千问-Max（阿里云）
            'doubao-pro'        // 豆包-Pro（火山引擎）
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
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3-vol';
    },
    
    async generateSlogans() {
      if (this.isLoading) return;
      
      // 使用计算属性验证表单
      if (!this.isFormValid) {
        this.$message ? this.$message.error('请输入产品名称') : 
          alert('请输入产品名称');
        return;
      }
      
      try {
        // 显示加载状态
        this.isLoading = true;
        this.loadingText = '正在生成广告语...';
        
        // 构建提示词
        const prompt = this.buildPrompt();
        
        // 调用API并获取结果
        const result = await this.callLLMApi(prompt);
        
        // 更新广告语列表
        this.slogans = result.slogans || [];
        
        // 如果是离线模式，显示提示
        if (result.offlineMode) {
          this.showNotification('离线模式提示', '后端服务不可用，当前显示的是离线生成的广告语。要获得AI生成的更优质广告语，请联系管理员启动后端服务。', 'warning');
        }
      } catch (error) {
        console.error('生成广告语失败:', error);
        // 显示错误信息
        this.showNotification('生成失败', error.message || '生成广告语失败', 'error');
      } finally {
        this.isLoading = false;
      }
    },
    
    buildPrompt() {
      console.log('构建广告语生成提示词');
      
      // 构建系统提示词
      const systemPrompt = `你是一位专业的广告语创作专家，可以为不同行业的产品和服务创作吸引人的广告语。请根据用户的需求，创作简短、有力且符合品牌调性的广告语。`;
      
      // 构建用户提示词
      let prompt = this.getPromptTemplate();
      
      // 记录完整提示词用于调试
      console.log('完整提示词:', prompt);
      
      // 保存提示词以便之后查看
      this.lastUsedPrompt = prompt;
      
      return prompt;
    },
    
    // 调用大模型API
    async callLLMApi(prompt) {
      try {
        this.isLoading = true;
        this.loadingText = '正在生成广告语...';
        
        // 检查是否有可用模型
        if (!this.selectedModel) {
          throw new Error('请选择AI模型');
        }
        
        console.log(`正在调用API，使用模型: ${this.selectedModel}，提示词长度: ${prompt.length}`);
        
        // 构建API请求参数
        const apiParams = {
          model: this.selectedModel,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 2000
        };
        
        try {
          // 发送API请求
          const response = await axios.post('/api/v1/llm/chat', apiParams, { timeout: 15000 });
          
          if (response.data.status === 'success') {
            const content = response.data.data.choices[0].message.content;
            return this.parseResponse(content);
          } else {
            throw new Error(`服务器返回错误: ${response.data.message || '未知错误'}`);
          }
        } catch (error) {
          // 判断是否是网络错误或服务器不可用
          if (this.isNetworkOrServerError(error)) {
            return this.generateOfflineSlogans();
          }
          
          // 其他API错误
          throw error;
        }
      } catch (error) {
        console.error('广告语生成失败:', error);
        
        // 如果是服务器无响应，则使用离线模式
        if (error.request && !error.response) {
          return this.generateOfflineSlogans();
        }
        
        // 构建错误信息
        let errorMessage = this.formatErrorMessage(error);
        throw new Error(errorMessage);
      } finally {
        this.isLoading = false;
      }
    },
    
    // 检查是否是网络或服务器错误
    isNetworkOrServerError(error) {
      return (
        error.code === 'ECONNABORTED' || 
        !error.response || 
        error.message.includes('Network Error') ||
        (error.response && error.response.status >= 500)
      );
    },
    
    // 格式化错误信息
    formatErrorMessage(error) {
      if (error.response) {
        // 服务器响应了，但状态码不在2xx范围
        let message = `服务器错误 (${error.response.status})`;
        if (error.response.data && error.response.data.message) {
          message += ` - ${error.response.data.message}`;
        }
        return message;
      } else if (error.request) {
        // 请求已发送但没有收到响应
        return '服务器无响应，切换到离线模式';
      } else {
        // 请求设置时出错
        return error.message || '未知错误';
      }
    },
    
    // 离线模式下生成基本广告语
    generateOfflineSlogans() {
      console.log('使用离线模式生成广告语');
      
      // 解析产品名称和行业特点以提供一些基本广告语
      const productName = this.productName || '产品';
      const productDesc = this.productDescription || '';
      const audience = this.targetAudience || '';
      const style = this.sloganStyle || 'professional';
      
      // 根据不同风格提供不同的模板
      const styleTemplates = {
        'professional': [
          `${productName}，专业品质的选择`,
          `${productName}，专注卓越，追求品质`,
          `${productName}，科技引领未来`,
          `${productName}，品质保障，值得信赖`,
          `选择${productName}，选择专业服务`
        ],
        'friendly': [
          `${productName}，像家人一样懂你`,
          `${productName}，温暖每一天`,
          `${productName}，为你的生活增添色彩`,
          `${productName}，贴心服务，用心呵护`,
          `${productName}，让生活更简单`
        ],
        'humorous': [
          `${productName}，让快乐触手可及`,
          `没有${productName}怎么行？`,
          `${productName}，笑着买，乐着用`,
          `生活需要${productName}的妙趣`,
          `${productName}，给枯燥生活加点料`
        ],
        'dramatic': [
          `${productName}，非凡体验从此开始`,
          `${productName}，突破想象，超越极限`,
          `${productName}，改变，就现在`,
          `震撼登场，${productName}引领潮流`,
          `${productName}，创造无限可能`
        ],
        'inspirational': [
          `${productName}，点燃梦想的力量`,
          `因为有${productName}，所以更精彩`,
          `${productName}，成就非凡人生`,
          `${productName}，让不可能变成可能`,
          `${productName}，勇往直前，无所畏惧`
        ]
      };
      
      // 根据选择的风格获取模板，如果没有则使用专业风格
      const templates = styleTemplates[style] || styleTemplates['professional'];
      
      // 基于输入和模板生成广告语
      const slogans = templates.map(text => ({
        text,
        isSelected: false,
        isOfflineGenerated: true  // 标记为离线生成
      }));
      
      return {
        slogans,
        offlineMode: true  // 标记为离线模式生成
      };
    },
    
    // 解析API返回的内容
    parseResponse(content) {
      if (!content || typeof content !== 'string') {
        return { slogans: [] };
      }
      
      try {
        // 1. 尝试作为JSON解析
        try {
          const jsonData = JSON.parse(content);
          // 处理数组格式
          if (Array.isArray(jsonData)) {
            return {
              slogans: jsonData.map(item => ({
                text: typeof item === 'string' ? item : (item.slogan || item.text || ''),
                isSelected: false
              })).filter(item => item.text.trim() !== '')
            };
          } 
          // 处理包含slogans字段的对象
          else if (jsonData.slogans && Array.isArray(jsonData.slogans)) {
            return {
              slogans: jsonData.slogans.map(item => ({
                text: typeof item === 'string' ? item : (item.slogan || item.text || ''),
                isSelected: false
              })).filter(item => item.text.trim() !== '')
            };
          }
          // 处理其他有效的JSON但不符合预期格式
          else {
            console.log('JSON格式不符合预期，尝试文本处理', jsonData);
          }
        } catch (e) {
          // JSON解析失败，继续下一步
        }
        
        // 2. 按行分割文本处理
        const lines = content.split('\n').filter(line => line.trim());
        const slogans = lines.map(line => {
          // 移除常见的序号、破折号等前缀
          const cleanLine = line.replace(/^[\d\.\-\*\s]+/, '').trim();
          return {
            text: cleanLine,
            isSelected: false
          };
        }).filter(item => item.text.length > 0);
        
        return { slogans };
      } catch (error) {
        console.error('解析响应内容失败:', error);
        return { 
          slogans: [],
          error: '解析返回内容失败'
        };
      }
    },
    
    copySlogan(text) {
      this.copyTextToClipboard(text, '广告语已复制到剪贴板');
    },
    
    resetForm() {
      this.productName = '';
      this.productDescription = '';
      this.targetAudience = '';
      this.sloganStyle = 'professional';
      this.sloganCount = 5;
      this.slogans = [];
    },
    
    loadExample(example) {
      const index = parseInt(example.match(/\d+/)[0]) - 1;
      if (index >= 0 && index < this.examples.length) {
        const data = this.examples[index];
        this.productName = data.title;
        this.productDescription = data.productDesc;
        this.targetAudience = data.targetAudience;
        this.sloganStyle = data.style;
        this.sloganCount = 5;
      }
    },
    
    showTips() {
      this.showTipsModal = true;
    },
    
    // 显示提示词模态框
    showPrompt() {
      if (this.lastUsedPrompt) {
        console.log('显示提示词模态框');
        this.showPromptModal = true;
      } else {
        this.$message ? this.$message.info('请先生成广告语以查看提示词') : 
          alert('请先生成广告语以查看提示词');
      }
    },
    
    // 复制提示词到剪贴板
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      this.copyTextToClipboard(this.lastUsedPrompt, '提示词已复制到剪贴板');
    },
    
    // 通用的通知方法
    showNotification(title, message, type = 'info') {
      if (this.$notify) {
        this.$notify({
          title: title,
          message: message,
          type: type,
          duration: 5000,
          position: 'top-right'
        });
      } else if (this.$message) {
        this.$message[type] ? this.$message[type](message) : this.$message(message);
      } else {
        alert(message);
      }
    },
    
    // 通用的复制文本方法
    copyTextToClipboard(text, successMessage = '复制成功') {
      if (!text) return;
      
      try {
        // 检查是否支持clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text)
            .then(() => {
              this.showNotification('成功', successMessage, 'success');
            })
            .catch(err => {
              console.error('复制失败:', err);
              this.fallbackCopy(text, successMessage);
            });
        } else {
          // 浏览器不支持clipboard API，使用备选方法
          this.fallbackCopy(text, successMessage);
        }
      } catch (error) {
        console.error('复制操作异常:', error);
        this.fallbackCopy(text, successMessage);
      }
    },
    
    // 备选的复制方法
    fallbackCopy(text, successMessage) {
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
          this.showNotification('成功', successMessage, 'success');
        } else {
          this.showNotification('失败', '复制失败，请手动复制', 'error');
        }
        
        // 清理临时元素
        document.body.removeChild(textArea);
      } catch (err) {
        console.error('备选复制方法失败:', err);
        this.showNotification('失败', '复制失败，请手动复制文本', 'error');
      }
    },
    
    // 获取提示词模板
    getPromptTemplate() {
      let prompt = `请为以下产品创作${this.sloganCount}条吸引人的广告语：\n\n`;
      prompt += `产品名称：${this.productName}\n`;
      
      if (this.productDescription) {
        prompt += `产品描述：${this.productDescription}\n`;
      }
      
      if (this.targetAudience) {
        prompt += `目标受众：${this.targetAudience}\n`;
      }
      
      if (this.sloganStyle) {
        // 使用计算属性获取风格名称
        prompt += `广告语风格：${this.currentStyleName}\n`;
      }
      
      prompt += `\n请按照以下要求：
1. 创作${this.sloganCount}条不同的广告语
2. 每条广告语简洁有力，长度控制在20个字以内
3. 突出产品特点和卖点
4. 符合指定的风格和目标受众
5. 直接返回广告语列表，每行一条广告语
6. 不要添加编号或解释`;
      
      return prompt;
    },
    
    prevExample() {
      if (this.currentExampleIndex > 0) {
        this.currentExampleIndex--;
        this.updateExampleCarousel();
      }
    },
    
    nextExample() {
      const maxVisibleCards = Math.floor(document.querySelector('.example-carousel').clientWidth / 295);
      const maxIndex = this.examples.length - maxVisibleCards;
      
      if (this.currentExampleIndex < maxIndex) {
        this.currentExampleIndex++;
        this.updateExampleCarousel();
      }
    },
    
    // 更新轮播位置
    updateExampleCarousel() {
      const cardWidth = 295; // 卡片宽度 + 间距，调整为更合适的值
      this.exampleTranslateX = -this.currentExampleIndex * cardWidth;
      if (this.$refs.exampleCarousel) {
        this.$refs.exampleCarousel.style.transform = `translateX(${this.exampleTranslateX}px)`;
        this.$refs.exampleCarousel.style.transition = 'transform 0.3s ease';
      }
    },
    
    // 格式化Markdown文本
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗
      let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理斜体
      formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
      
      // 处理换行
      formatted = formatted.replace(/\n\n/g, '<br><br>');
      
      // 处理列表
      formatted = formatted.replace(/- (.*?)(?:\n|$)/g, '<li>$1</li>');
      formatted = formatted.replace(/<li>/g, '<ul><li>').replace(/<\/li>(?!<li>)/g, '</li></ul>');
      formatted = formatted.replace(/<\/ul><ul>/g, '');
      
      // 处理数字列表
      formatted = formatted.replace(/(\d+)\. (.*?)(?:\n|$)/g, '<li>$1. $2</li>');
      
      return formatted;
    }
  }
}
</script>

<style scoped>
/* 使用通用CSS类，移除margin-top */
/* 仅保留特定于广告语生成的样式 */
.ad-slogan-page {
  padding: 0;
  border: none;
  border-top: none !important;
  border-bottom: none !important;
  box-shadow: none !important;
}

/* 参考案例部分 - 轮播形式样式 */
.examples-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 12px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  margin-bottom: 0;
}

.examples-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.example-carousel {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding-bottom: 5px;
}

.example-cards {
  display: flex;
  gap: 15px;
  transition: transform 0.3s ease;
  will-change: transform;
  padding: 5px 0;
  width: max-content;
}

.example-card {
  flex: 0 0 200px;
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
  overflow: hidden;
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
  overflow: hidden;
}

.example-brand {
  font-weight: 600;
  margin-bottom: 0;
  font-size: 15px;
}

.example-slogan {
  font-size: 14px;
  color: #666;
  display: none;
  overflow: hidden;
  text-overflow: ellipsis;
}

.example-card:hover .example-slogan {
  display: block;
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

.carousel-control.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.carousel-control.disabled:hover {
  background-color: #fff;
  color: inherit;
  border-color: #ddd;
}

/* 广告语展示项特定样式 */
.slogan-results {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.slogan-item {
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  border-left: 3px solid var(--primary-color, #8B0A50);
  border-top: none;
  border-bottom: none;
  border-right: none;
}

.slogan-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  background-color: #fcfcfc;
}

.slogan-number {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 30px;
  height: 30px;
  margin-right: 12px;
  border-radius: 50%;
  background-color: var(--primary-color, #ba003f);
  color: white;
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(186, 0, 63, 0.3);
}

.slogan-content {
  font-size: 16px;
  color: #333;
  flex: 1;
  line-height: 1.5;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.slogan-actions {
  display: flex;
  margin-left: 15px;
}

/* 离线模式提示条样式 */
.offline-mode-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #fff9e6;
  border: 1px solid #ffeeba;
  border-radius: 4px;
  padding: 12px;
  margin: 12px;
  color: #856404;
  font-size: 14px;
}

.offline-mode-banner i {
  font-size: 18px;
}

.model-loading {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #666;
  margin-top: 5px;
}

.model-loading i {
  font-size: 14px;
  margin-right: 6px;
  animation: spin 1.5s linear infinite;
}

/* 提示词模态框特定样式 */
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

/* 响应式特定调整 */
@media (max-width: 1400px) {
  .example-card {
    flex: 0 0 180px;
  }
}

@media (max-width: 1200px) {
  .example-card {
    flex: 0 0 160px;
  }
}

@media (max-width: 768px) {
  .example-cards {
    justify-content: flex-start;
  }
  
  .example-card {
    flex: 0 0 130px;
  }
}
</style> 