<template>
  <div class="marketing-copy-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>营销文案生成</h2>
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
            <label for="brand-name">品牌名称</label>
            <input 
              type="text" 
              id="brand-name" 
              v-model="brandName" 
              placeholder="请输入品牌名称（可选）"
              class="form-control"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="product-description" class="required">产品/服务描述</label>
          <textarea 
            id="product-description" 
            v-model="productDescription" 
            placeholder="请详细描述产品/服务的特点、功能、优势等"
            class="form-control"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="target-audience" class="required">目标受众</label>
            <input 
              type="text" 
              id="target-audience" 
              v-model="targetAudience" 
              placeholder="如：18-35岁的年轻白领、户外运动爱好者等"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="industry">所属行业</label>
            <input 
              type="text" 
              id="industry" 
              v-model="industry" 
              placeholder="如：科技、教育、健康等"
              class="form-control"
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="copy-style">文案风格</label>
            <select id="copy-style" v-model="copyStyle" class="form-control">
              <option value="professional">专业正式</option>
              <option value="friendly">亲切友好</option>
              <option value="humorous">幽默风趣</option>
              <option value="dramatic">戏剧性强</option>
              <option value="storytelling">故事叙事</option>
              <option value="persuasive">说服力强</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="copy-length">文案长度</label>
            <select id="copy-length" v-model="copyLength" class="form-control">
              <option value="short">简短(100字以内)</option>
              <option value="medium">中等(300字左右)</option>
              <option value="long">较长(500字以上)</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label for="key-points">关键卖点或信息</label>
          <textarea 
            id="key-points" 
            v-model="keyPoints" 
            placeholder="请列出希望在文案中强调的关键卖点或重要信息（每行一个要点）"
            class="form-control"
            rows="3"
          ></textarea>
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
          <button class="btn btn-primary" @click="generateCopy" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '正在生成...' : '生成文案' }}
          </button>
          <button class="btn btn-secondary" @click="resetForm">
            <i class="ri-refresh-line"></i> 重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：参考案例和结果 -->
      <div class="right-column">
        <!-- 参考案例部分 - 轮播形式 -->
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
              文案结果
            </h3>
            <div class="action-buttons">
              <button @click="generateCopy" class="primary-button" :disabled="isLoading">
                <i class="ri-refresh-line" v-if="!isLoading"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isLoading ? '生成中...' : '重新生成' }}
              </button>
              <button @click="copyResult" class="secondary-button" :disabled="isLoading || !generatedCopy">
                <i class="ri-file-copy-line"></i>
                复制文案
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
            
            <div v-if="!generatedCopy && !isLoading" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无文案，请点击"生成文案"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedCopy" class="copy-result" :class="{'blur-content': isLoading}">
              <!-- 添加离线模式提示条 -->
              <div v-if="isOfflineGenerated" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板文案。要获得AI生成的更优质文案，请联系管理员启动后端服务。</span>
              </div>
              
              <div class="copy-content" v-html="formattedCopy"></div>
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
            <li>根据目标受众选择适合的文案风格和语调</li>
            <li>突出产品/服务的独特卖点和解决的问题</li>
            <li>根据不同的平台调整文案长度和格式</li>
            <li>使用行业数据和统计数字增加文案的说服力</li>
            <li>加入情感元素，与目标受众建立情感连接</li>
            <li>确保文案有明确的行动号召(CTA)</li>
            <li>使用客户见证和社会认同原则增强信任度</li>
            <li>注意文案的节奏和可读性，使用短句和段落</li>
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

// 创建axios实例，配置baseURL
const apiClient = axios.create({
  baseURL: 'http://localhost:9000', // 后端服务地址
  timeout: 30000 // 请求超时时间
});

export default {
  name: 'CopywritingGenerator',
  data() {
    return {
      selectedTemplate: 'product-intro',
      productName: '',
      brandName: '',
      productDescription: '',
      targetAudience: '',
      industry: '',
      copyStyle: 'professional',
      copyLength: 'medium',
      keyPoints: '',
      generatedCopy: '',
      isOfflineGenerated: false,
      showTipsModal: false,
      showPromptModal: false,
      lastUsedPrompt: '',
      modelList: [],
      selectedModel: 'deepseek-v3-vol',
      isGenerating: false,
      isLoading: false,
      loadingText: '正在生成文案...',
      validationErrors: [],
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      examples: [
        { title: '科技', desc: '产品介绍', icon: 'ri-smartphone-line', style: 'professional', template: 'product-intro', 
          productDesc: '新一代智能手机搭载最新处理器，提供超长电池续航和专业级摄像系统，支持5G网络和AI智能助手功能。', 
          targetAudience: '科技爱好者、商务人士、数字化生活追求者', brand: '科技品牌', industry: '电子科技' },
        { title: '运动', desc: '社交媒体', icon: 'ri-run-line', style: 'inspirational', template: 'social-media', 
          productDesc: '专业运动装备采用轻量化材料和人体工学设计，提供卓越的舒适度和运动表现，适合各类户外活动。', 
          targetAudience: '运动爱好者、健身达人、户外探险者', brand: '运动品牌', industry: '体育用品' },
        { title: '教育', desc: '产品描述', icon: 'ri-book-open-line', style: 'friendly', template: 'product-description', 
          productDesc: '在线教育平台提供丰富的课程内容，专业讲师授课，随时随地学习，支持个性化学习计划和进度跟踪。', 
          targetAudience: '学生、在职人士、终身学习者', brand: '教育机构', industry: '在线教育' },
        { title: '餐饮', desc: '促销活动', icon: 'ri-restaurant-line', style: 'friendly', template: 'promotion', 
          productDesc: '季节限定美食系列，采用当季新鲜食材，传统工艺与创新口味相结合，带来独特的味觉体验。', 
          targetAudience: '美食爱好者、年轻消费群体、城市白领', brand: '餐饮品牌', industry: '餐饮服务' },
        { title: '金融', desc: '电子邮件', icon: 'ri-bank-line', style: 'professional', template: 'email', 
          productDesc: '个人理财服务提供多元化投资方案，智能资产配置，低费率高效益，全方位保障客户资金安全。', 
          targetAudience: '投资者、上班族、理财新手', brand: '金融机构', industry: '金融服务' },
        { title: '旅游', desc: '品牌故事', icon: 'ri-suitcase-line', style: 'storytelling', template: 'brand-story', 
          productDesc: '专注于提供深度文化体验的旅行服务，带领旅行者探索世界各地的独特文化和自然风光。', 
          targetAudience: '旅行爱好者、摄影师、文化探索者', brand: '旅游品牌', industry: '旅游服务' },
        { title: '医疗', desc: 'SEO文案', icon: 'ri-heart-pulse-line', style: 'professional', template: 'seo', 
          productDesc: '健康管理平台提供个性化健康解决方案，包括健康评估、营养指导、运动计划和远程医疗咨询。', 
          targetAudience: '健康关注者、亚健康人群、慢性病患者', brand: '医疗品牌', industry: '健康医疗' },
        { title: '房地产', desc: '落地页', icon: 'ri-home-line', style: 'friendly', template: 'landing-page', 
          productDesc: '现代化高品质住宅项目，地理位置优越，智能家居系统，社区配套齐全，打造理想生活空间。', 
          targetAudience: '年轻家庭、专业人士、品质生活追求者', brand: '地产开发商', industry: '房地产' },
        { title: '汽车', desc: '新闻稿', icon: 'ri-car-line', style: 'professional', template: 'press-release', 
          productDesc: '新能源汽车采用尖端电池技术，提供超长续航里程，智能驾驶辅助系统，豪华内饰设计。', 
          targetAudience: '车辆购买者、环保人士、科技爱好者', brand: '汽车制造商', industry: '汽车制造' },
        { title: '娱乐', desc: '视频脚本', icon: 'ri-film-line', style: 'humorous', template: 'video-script', 
          productDesc: '流媒体平台提供丰富的影视内容，原创精品节目，多设备同步，支持离线观看和个性化推荐。', 
          targetAudience: '影视爱好者、年轻群体、数字内容消费者', brand: '娱乐平台', industry: '数字娱乐' }
      ]
    }
  },
  
  computed: {
    // 格式化文案展示
    formattedCopy() {
      if (!this.generatedCopy) return '';
      
      // 将换行符转换为HTML段落
      return this.generatedCopy
        .split('\n\n')
        .map(para => para.trim())
        .filter(para => para.length > 0)
        .map(para => `<p>${para.replace(/\n/g, '<br>')}</p>`)
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
    
    // 生成营销文案
    async generateCopy() {
      if (this.isLoading) return;
      
      try {
        this.validationErrors = [];
        
        // 验证必填字段
        if (!this.productName.trim()) {
          this.validationErrors.push('请输入产品/服务名称');
        }
        if (!this.productDescription.trim()) {
          this.validationErrors.push('请输入产品/服务描述');
        }
        if (!this.targetAudience.trim()) {
          this.validationErrors.push('请输入目标受众');
        }
        
        if (this.validationErrors.length > 0) {
          const errorMsg = this.validationErrors.join('，');
          this.$message ? this.$message.error(errorMsg) : alert(errorMsg);
          return;
        }
        
        // 显示加载状态
        this.isLoading = true;
        this.isGenerating = true;
        this.loadingText = '正在生成营销文案...';
        
        // 构建提示词
        const prompt = this.buildPrompt();
        
        // 调用API并获取结果
        const result = await this.callLLMApi(prompt);
        
        // 更新营销文案内容
        this.generatedCopy = result.text || '';
        this.isOfflineGenerated = result.offlineMode || false;
        
        // 如果是离线模式，显示提示
        if (result.offlineMode) {
          this.$notify && this.$notify({
            title: '离线模式提示',
            message: '后端服务不可用，当前显示的是离线生成的文案。要获得AI生成的更优质文案，请联系管理员启动后端服务。',
            type: 'warning',
            duration: 10000,
            position: 'top-right'
          });
        }
      } catch (error) {
        console.error('生成营销文案失败:', error);
        // 显示错误信息
        this.$message ? this.$message.error(error.message || '生成营销文案失败') : 
          alert(error.message || '生成营销文案失败');
      } finally {
        this.isLoading = false;
        this.isGenerating = false;
      }
    },
    
    // 构建提示词
    buildPrompt() {
      console.log('构建营销文案生成提示词');
      
      // 获取文案模板类型的中文名称
      const getTemplateTypeName = () => {
        const templateMap = {
          'product-intro': '产品介绍文案',
          'social-media': '社交媒体文案',
          'landing-page': '落地页文案',
          'email': '邮件营销文案',
          'seo': 'SEO优化文案',
          'promotion': '促销活动文案',
          'brand-story': '品牌故事文案',
          'product-description': '产品描述文案',
          'press-release': '新闻稿文案',
          'video-script': '短视频脚本'
        };
        return templateMap[this.selectedTemplate] || '营销文案';
      };
      
      // 获取风格的中文名称
      const getStyleName = () => {
        const styleMap = {
          'professional': '专业正式',
          'friendly': '亲切友好',
          'humorous': '幽默风趣',
          'dramatic': '戏剧性强',
          'storytelling': '故事叙事',
          'persuasive': '说服力强'
        };
        return styleMap[this.copyStyle] || '专业';
      };
      
      // 获取长度的中文描述
      const getLengthDescription = () => {
        const lengthMap = {
          'short': '简短(100字以内)',
          'medium': '中等(300字左右)',
          'long': '较长(500字以上)'
        };
        return lengthMap[this.copyLength] || '中等(300字左右)';
      };
      
      // 构建系统提示词
      const systemPrompt = `你是一位专业的营销文案撰写专家，精通各类营销文案的创作，包括产品介绍、社交媒体、落地页等不同类型的文案。请根据用户提供的信息，创作一份符合要求的高质量营销文案。`;
      
      // 构建用户提示词
      let prompt = `请为以下产品/服务创作一份${getTemplateTypeName()}：\n\n`;
      prompt += `文案类型：${getTemplateTypeName()}\n`;
      prompt += `产品/服务名称：${this.productName}\n`;
      
      if (this.brandName) {
        prompt += `品牌名称：${this.brandName}\n`;
      }
      
      prompt += `产品/服务描述：${this.productDescription}\n`;
      prompt += `目标受众：${this.targetAudience}\n`;
      
      if (this.industry) {
        prompt += `所属行业：${this.industry}\n`;
      }
      
      prompt += `文案风格：${getStyleName()}\n`;
      prompt += `文案长度：${getLengthDescription()}\n`;
      
      if (this.keyPoints) {
        prompt += `关键卖点或信息：\n${this.keyPoints}\n`;
      }
      
      // 根据不同的文案类型添加特定要求
      switch (this.selectedTemplate) {
        case 'product-intro':
          prompt += `\n请重点突出产品的核心特点和优势，以及如何解决用户的痛点问题。`;
          break;
        case 'social-media':
          prompt += `\n请创作简短有力的社交媒体文案，适合在微信、微博等平台发布，能够引发用户互动和分享。`;
          break;
        case 'landing-page':
          prompt += `\n请创作能够提高转化率的落地页文案，包括标题、主要内容和行动号召(CTA)部分。`;
          break;
        case 'email':
          prompt += `\n请创作一份吸引人的邮件营销文案，包括引人注目的主题行和能够促使用户采取行动的正文内容。`;
          break;
        case 'seo':
          prompt += `\n请创作针对搜索引擎优化的内容，合理插入关键词，同时保持文案的流畅性和可读性。`;
          break;
        case 'promotion':
          prompt += `\n请创作一份强调促销活动价值和紧迫感的文案，突出优惠力度，促使用户快速转化。`;
          break;
        case 'brand-story':
          prompt += `\n请创作一份能够讲述品牌故事、建立情感连接的文案，增强品牌认同感。`;
          break;
        case 'product-description':
          prompt += `\n请创作适合电商平台的产品详情描述，全面介绍产品特点、规格和使用场景。`;
          break;
        case 'press-release':
          prompt += `\n请创作一份正式的新闻稿，包括标题、导语、主体内容和关于公司的简介。`;
          break;
        case 'video-script':
          prompt += `\n请创作一份适合短视频平台的脚本，包括引人入胜的开场、主要内容和结尾号召。`;
          break;
      }
      
      prompt += `\n\n请直接给出文案内容，无需额外解释或说明。请确保文案符合指定的风格和长度要求，同时突出产品/服务的核心卖点。`;
      
      // 添加要求AI在文案末尾提供字数统计
      prompt += `\n\n在文案最后，请添加一行字数统计信息，格式为"【字数统计：xxx字】"。`;
      
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
          const response = await axios.post('/api/v1/llm/chat', apiParams, { timeout: 30000 });
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
        console.error('营销文案生成失败:', error);
        
        // 根据错误类型提供更具体的错误信息
        let errorMessage = '生成营销文案失败';
        
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
    
    // 离线模式下生成基本文案
    generateOfflineContent() {
      console.log('使用离线模式生成营销文案');
      
      // 获取基本信息
      const productName = this.productName || '产品';
      const brandName = this.brandName || '品牌';
      const description = this.productDescription || '';
      const audience = this.targetAudience || '';
      const templateType = this.selectedTemplate || 'product-intro';
      
      // 根据不同类型的模板生成不同的基础文案
      let content = '';
      
      switch (templateType) {
        case 'product-intro':
          content = `# ${productName}产品介绍\n\n${brandName}全新推出的${productName}是市场上极具创新性的产品。\n\n它不仅具有${description.slice(0, 50)}等卓越特点，还特别适合${audience}的需求。\n\n无论您是需要提高效率，还是追求卓越体验，${productName}都能满足您的各种期望。\n\n立即体验${productName}，开启全新可能！`;
          break;
          
        case 'social-media':
          content = `【${brandName}新品】\n\n想要${description.slice(0, 30)}？${productName}闪亮登场！\n\n专为${audience}打造，解决您的痛点问题。\n\n限时体验，不容错过！ #${productName} #${brandName}新品`;
          break;
          
        case 'landing-page':
          content = `# 探索${productName}的非凡价值\n\n## 为${audience}量身打造\n\n${description.slice(0, 100)}\n\n## 核心优势\n\n- 创新性：领先行业的技术\n- 实用性：解决实际问题\n- 可靠性：品质保证\n\n## 立即行动\n\n现在购买${productName}，享受限时优惠！`;
          break;
          
        case 'email':
          content = `亲爱的客户：\n\n我们很高兴向您介绍${brandName}最新推出的${productName}。\n\n作为${audience}，您一定会欣赏它的这些特点：${description.slice(0, 100)}\n\n现在购买，还可享受独家优惠。\n\n期待您的体验！\n\n${brandName}团队`;
          break;
          
        case 'seo':
          content = `# ${productName}：满足${audience}需求的最佳选择\n\n在当今竞争激烈的市场中，选择一款能够真正满足需求的产品至关重要。${brandName}推出的${productName}以其${description.slice(0, 80)}的特点，成为众多${audience}的首选。\n\n## 为什么选择${productName}？\n\n专业设计，优质体验，解决实际问题。无论您是专业用户还是普通消费者，${productName}都能满足您的期望。\n\n立即了解更多信息，开启全新体验！`;
          break;
          
        default:
          content = `# ${productName}\n\n${brandName}推出的${productName}是一款卓越的产品。\n\n${description}\n\n特别适合${audience}使用。\n\n了解更多信息，请联系我们。`;
      }
      
      return {
        text: content,
        offlineMode: true
      };
    },
    
    // 复制生成的结果
    copyResult() {
      if (!this.generatedCopy) return;
      
      navigator.clipboard.writeText(this.generatedCopy)
        .then(() => {
          this.$message ? this.$message.success('文案已复制到剪贴板') : 
            alert('文案已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          this.$message ? this.$message.error('复制失败') : 
            alert('复制失败');
        });
    },
    
    // 重置表单
    resetForm() {
      this.productName = '';
      this.brandName = '';
      this.productDescription = '';
      this.targetAudience = '';
      this.industry = '';
      this.copyStyle = 'professional';
      this.copyLength = 'medium';
      this.keyPoints = '';
      this.generatedCopy = '';
    },
    
    // 加载参考案例
    loadExample(example) {
      // 通过索引找到对应的参考案例
      const index = parseInt(example.replace('example', '')) - 1;
      const data = this.examples[index];
      
      if (!data) return;
      
      console.log('加载参考案例:', data);
      
      // 根据行业提供更真实的品牌名称
      const getBrandNameByIndustry = (industry, title) => {
        const brandMap = {
          '电子科技': ['华为智选', '小米科技', '苹果中国', '三星电子', '联想科技'],
          '体育用品': ['安踏体育', '李宁运动', '耐克中国', '阿迪达斯', '迪卡侬'],
          '在线教育': ['好未来', '网易云课堂', '腾讯课堂', '跟谁学', '作业帮'],
          '餐饮服务': ['海底捞', '星巴克中国', '西贝莜面村', '奈雪的茶', '麦当劳中国'],
          '金融服务': ['招商银行', '蚂蚁财富', '平安财富', '京东金融', '微众银行'],
          '旅游服务': ['携程旅行', '马蜂窝', '途牛旅游', '飞猪旅行', '同程旅游'],
          '健康医疗': ['平安健康', '好大夫在线', '丁香医生', '微医', '春雨医生'],
          '房地产': ['万科地产', '碧桂园', '恒大地产', '龙湖地产', '保利发展'],
          '汽车制造': ['比亚迪', '理想汽车', '小鹏汽车', '蔚来汽车', '特斯拉中国'],
          '数字娱乐': ['腾讯视频', '爱奇艺', '哔哩哔哩', '网易云音乐', '抖音'],
        };
        
        // 获取该行业的品牌名称列表
        const brands = brandMap[industry] || brandMap['电子科技'];
        
        // 根据标题选择一个品牌，或随机选择
        if (title && title.length > 0) {
          // 使用标题的第一个字符的Unicode码作为索引
          const charCode = title.charCodeAt(0);
          return brands[charCode % brands.length];
        } else {
          // 随机选择一个品牌
          return brands[Math.floor(Math.random() * brands.length)];
        }
      };
      
      // 填充表单字段
      this.productName = data.title || '';
      this.brandName = getBrandNameByIndustry(data.industry, data.title);
      this.productDescription = data.productDesc || '';
      this.targetAudience = data.targetAudience || '';
      this.industry = data.industry || '';
      this.copyStyle = data.style || 'professional';
      this.copyLength = 'medium';
      
      console.log('设置文案风格为:', this.copyStyle);
      console.log('设置品牌名称为:', this.brandName);
    },
    
    // 显示创作小贴士
    showTips() {
      console.log('显示创作小贴士模态框');
      this.showTipsModal = true;
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
    
    // 显示提示词模态框
    showPrompt() {
      if (this.lastUsedPrompt) {
        console.log('显示提示词模态框');
        this.showPromptModal = true;
      } else {
        this.$message ? this.$message.info('请先生成文案以查看提示词') : 
          alert('请先生成文案以查看提示词');
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
              this.fallbackCopy();
            });
        } else {
          // 浏览器不支持clipboard API，使用备选方法
          this.fallbackCopy();
        }
      } catch (error) {
        console.error('复制操作异常:', error);
        this.fallbackCopy();
      }
    },
    
    // 备选的复制方法
    fallbackCopy() {
      try {
        // 创建临时textarea元素
        const textArea = document.createElement('textarea');
        textArea.value = this.lastUsedPrompt;
        
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
          this.$message ? this.$message.success('提示词已复制到剪贴板') : 
            alert('提示词已复制到剪贴板');
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
.marketing-copy-page {
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
  margin-bottom: 12px;
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
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: var(--primary-color, #ba003f);
  outline: none;
}

textarea.form-control {
  min-height: 100px;
  resize: vertical;
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
  transition: all 0.2s;
  border: none;
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
}

/* 右侧：参考案例和结果 */
.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 添加参考案例和结果之间的间距 */
}

/* 参考案例部分 - 改为轮播形式 */
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

.example-brand {
  font-weight: 600;
  margin-bottom: 0;
  font-size: 15px;
}

.example-slogan {
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

/* 营销文案结果特有样式 */
.copy-result {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  line-height: 1.6;
  font-size: 15px;
}

.copy-content {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.copy-content p {
  margin-bottom: 16px;
  color: #333;
}

.copy-content h1, .copy-content h2, .copy-content h3 {
  color: #222;
  margin-top: 24px;
  margin-bottom: 16px;
}

.copy-content h1 {
  font-size: 24px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.copy-content h2 {
  font-size: 20px;
}

.copy-content h3 {
  font-size: 18px;
}

.copy-content ul, .copy-content ol {
  margin-left: 20px;
  margin-bottom: 16px;
}

.copy-content li {
  margin-bottom: 8px;
}

.copy-content strong {
  font-weight: 600;
}

.copy-content em {
  font-style: italic;
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

.section-header {
  position: sticky;
  top: 0;
  background-color: #fff;
  z-index: 100;
  padding: 15px 15px 20px; /* 增加底部内边距从10px到20px */
  margin: -15px -15px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
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

/* 表单控件容器样式优化 */
.form-group {
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

/* 按钮动画效果 */
.btn {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.btn:active {
  transform: scale(0.96);
}

.btn-primary:hover {
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.2);
  transform: translateY(-2px);
}

.btn-secondary:hover {
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.15);
  transform: translateY(-2px);
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
</style> 