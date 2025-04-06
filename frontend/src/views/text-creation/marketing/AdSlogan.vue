<template>
  <div class="ad-slogan-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>广告语生成</h2>
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
              <button @click="copyAllSlogans" class="secondary-button" :disabled="isLoading || slogans.length === 0">
                <i class="ri-file-copy-line"></i>
                复制全部
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
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无广告语，请点击"生成广告语"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="slogans.length > 0" class="slogan-results" :class="{'blur-content': isLoading}">
              <!-- 添加离线模式提示条 -->
              <div v-if="slogans.length > 0 && slogans[0].isOfflineGenerated" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板广告语。要获得AI生成的更优质广告语，请联系管理员启动后端服务。</span>
              </div>
              
              <div v-for="(slogan, index) in slogans" :key="index" class="slogan-item">
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
            <li>提供详细的产品信息，有助于AI生成更有针对性的广告语</li>
            <li>可以尝试不同的风格，看哪种更适合您的品牌调性</li>
            <li>好的广告语通常简短有力，容易记忆</li>
            <li>考虑目标受众的偏好和语言习惯</li>
            <li>可以多次生成，从中选择最适合的内容</li>
            <li>注意产品特点与广告语风格的匹配度</li>
            <li>简短有力的广告语往往比长篇大论更有效</li>
            <li>尝试使用押韵、对比或双关语等修辞手法增强记忆点</li>
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
      
      try {
        this.validationErrors = [];
        
        // 验证必填字段
        if (!this.productName.trim()) {
          this.validationErrors.push('请输入产品名称');
        }
        
        if (this.validationErrors.length > 0) {
          return;
        }
        
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
          this.$notify && this.$notify({
            title: '离线模式提示',
            message: '后端服务不可用，当前显示的是离线生成的广告语。要获得AI生成的更优质广告语，请联系管理员启动后端服务。',
            type: 'warning',
            duration: 10000,
            position: 'top-right'
          });
        }
      } catch (error) {
        console.error('生成广告语失败:', error);
        // 显示错误信息
        this.$message ? this.$message.error(error.message || '生成广告语失败') : 
          alert(error.message || '生成广告语失败');
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
          console.error('未选择模型');
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
        
        // 记录API请求详情，方便调试
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        try {
          // 发送API请求
          const response = await axios.post('/api/v1/llm/chat', apiParams, { timeout: 15000 });
          console.log('API响应:', response);
          
          if (response.data.status === 'success') {
            const content = response.data.data.choices[0].message.content;
            console.log('成功获取到结果:', content);
            
            // 解析返回的内容
            return this.parseResponse(content);
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
            const offlineResult = this.generateOfflineSlogans();
            return offlineResult;
          }
          
          // 其他API错误
          throw error;
        }
      } catch (error) {
        console.error('广告语生成失败:', error);
        
        // 根据错误类型提供更具体的错误信息
        let errorMessage = '生成广告语失败';
        
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
          return this.generateOfflineSlogans();
        } else {
          // 请求设置时出错
          errorMessage += `: ${error.message}`;
        }
        
        throw new Error(errorMessage);
      } finally {
        this.isLoading = false;
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
      try {
        console.log('正在解析API返回内容');
        
        // 尝试作为JSON解析
        try {
          const jsonData = JSON.parse(content);
          if (Array.isArray(jsonData)) {
            return {
              slogans: jsonData.map(item => ({
                text: typeof item === 'string' ? item : item.slogan || item.text,
                isSelected: false
              }))
            };
          } else if (jsonData.slogans && Array.isArray(jsonData.slogans)) {
            return {
              slogans: jsonData.slogans.map(item => ({
                text: typeof item === 'string' ? item : item.slogan || item.text,
                isSelected: false
              }))
            };
          }
        } catch (e) {
          console.log('内容不是有效JSON，尝试文本处理');
        }
        
        // 如果不是JSON，尝试按行分割
        const lines = content.split('\n').filter(line => line.trim());
        const slogans = lines.map(line => {
          // 尝试移除序号、破折号等前缀
          const cleanLine = line.replace(/^[\d\.\-\*\s]+/, '').trim();
          return {
            text: cleanLine,
            isSelected: false
          };
        }).filter(item => item.text.length > 0);
        
        return { slogans };
      } catch (error) {
        console.error('解析响应内容失败:', error);
        throw new Error('解析生成的广告语失败');
      }
    },
    
    copySlogan(text) {
      navigator.clipboard.writeText(text)
        .then(() => {
          this.$message ? this.$message.success('广告语已复制到剪贴板') : 
            alert('广告语已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          this.$message ? this.$message.error('复制失败') : 
            alert('复制失败');
        });
    },
    
    copyAllSlogans() {
      const allSlogans = this.slogans.map(item => item.text).join('\n\n');
      navigator.clipboard.writeText(allSlogans)
        .then(() => {
          this.$message ? this.$message.success('所有广告语已复制到剪贴板') : alert('所有广告语已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败：', err);
        });
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
        // 转换风格枚举为中文名称
        const styleMap = {
          'professional': '专业正式',
          'friendly': '亲切友好',
          'humorous': '幽默风趣',
          'dramatic': '戏剧性强', 
          'inspirational': '励志鼓舞'
        };
        
        let styleName = styleMap[this.sloganStyle] || this.sloganStyle;
        prompt += `广告语风格：${styleName}\n`;
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
  }
}
</script>

<style scoped>
.ad-slogan-page {
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
  flex: 0 0 200px; /* 减小固定宽度，显示更多案例 */
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
  display: none; /* 默认隐藏广告语 */
  overflow: hidden;
  text-overflow: ellipsis; /* 文本过长时显示省略号 */
}

.example-card:hover .example-slogan {
  display: block; /* 悬浮时显示广告语 */
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

.slogan-results {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
}

.slogan-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.slogan-item:hover {
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.slogan-content {
  font-size: 16px;
  color: #333;
  flex: 1;
}

.slogan-actions {
  display: flex;
  margin-left: 15px;
}

.action-button {
  background: none;
  border: none;
  color: #666;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.action-button:hover {
  color: var(--primary-color, #ba003f);
  background-color: #f0f0f0;
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
  z-index: 1000;
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

/* 历史记录样式 */
.history-records {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.history-record {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #eee;
  transition: transform 0.2s, box-shadow 0.2s;
}

.history-record:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.history-date {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
}

.history-product {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--primary-color, #ba003f);
}

.history-slogans {
  margin-top: 10px;
}

.history-slogan {
  padding: 8px 10px;
  background-color: white;
  border-radius: 4px;
  margin-bottom: 8px;
  font-size: 14px;
  border: 1px solid #eee;
}

.more-slogans {
  text-align: center;
  color: #888;
  font-size: 13px;
  margin-top: 5px;
}

.history-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.history-btn {
  padding: 6px 10px;
  font-size: 12px;
  background-color: var(--primary-color, #ba003f);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.history-btn:hover {
  background-color: #980034;
}

.empty-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
  color: #999;
}

.empty-history i {
  font-size: 40px;
  margin-bottom: 16px;
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

/* 响应式布局 */
@media (max-width: 992px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section, .right-column {
    width: 100%;
  }
  
  .history-records {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .history-records {
    grid-template-columns: 1fr;
  }
  
  .example-cards {
    justify-content: flex-start;
  }
  
  .example-card {
    flex: 0 0 130px;
  }
}

/* 添加样式 */
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


/* 结果展示部分标题也固定 */
.result-section .section-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #fff;
}

@media (max-width: 1400px) {
  .example-card {
    flex: 0 0 180px; /* 在较窄的屏幕上减小卡片宽度 */
  }
}

@media (max-width: 1200px) {
  .example-card {
    flex: 0 0 160px; /* 在更窄的屏幕上进一步减小卡片宽度 */
  }
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

.result-section {
  display: flex;
  flex-direction: column;
  padding: 0;
  position: relative; /* 为了绝对定位loading overlay */
  overflow: hidden; /* 保持内容在边界内 */
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
  margin: 12px;
  color: #856404;
  font-size: 14px;
}

.offline-mode-banner i {
  font-size: 18px;
}
</style> 