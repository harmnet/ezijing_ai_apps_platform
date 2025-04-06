<template>
  <div class="weibo-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>微博文章生成</h2>
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
        
        <!-- 微博类型选择 -->
        <div class="form-group">
          <label for="weibo-type">微博类型</label>
          <select id="weibo-type" v-model="weiboType" class="form-control">
            <option value="trending">热点话题</option>
            <option value="lifestyle">生活日常</option>
            <option value="review">产品测评</option>
            <option value="humor">幽默段子</option>
            <option value="question">提问互动</option>
          </select>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="weibo-title" class="required">微博主题</label>
            <input 
              type="text" 
              id="weibo-title" 
              v-model="weiboTitle" 
              placeholder="输入微博主题或中心内容"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="target-audience" class="required">目标读者群体</label>
            <input 
              type="text" 
              id="target-audience" 
              v-model="targetAudience" 
              placeholder="例如：90后、职场人士、学生党、美妆爱好者等"
              class="form-control"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="weibo-keywords" class="required">微博关键词或内容要点</label>
          <textarea 
            id="weibo-keywords" 
            v-model="weiboKeywords" 
            placeholder="输入微博需要包含的关键词、观点或要点，每点用逗号或分号分隔"
            class="form-control"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="writing-style">语言风格</label>
            <select id="writing-style" v-model="writingStyle" class="form-control">
              <option value="casual">轻松日常</option>
              <option value="humorous">幽默诙谐</option>
              <option value="professional">专业正式</option>
              <option value="emotional">情感充沛</option>
              <option value="sarcastic">讽刺调侃</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="weibo-length">微博长度</label>
            <select id="weibo-length" v-model="weiboLength" class="form-control">
              <option value="short">简短 (50字以内)</option>
              <option value="medium">中等 (50-100字)</option>
              <option value="long">较长 (100-200字)</option>
              <option value="super-long">超长 (200-500字)</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label>内容元素</label>
          <div class="checkbox-group">
            <div class="checkbox-item">
              <input type="checkbox" id="include-emoji" v-model="includeEmoji">
              <label for="include-emoji" class="checkbox-label">表情符号</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="include-hashtags" v-model="includeHashtags">
              <label for="include-hashtags" class="checkbox-label">话题标签</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="include-mention" v-model="includeMention">
              <label for="include-mention" class="checkbox-label">@提及</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="include-question" v-model="includeQuestion">
              <label for="include-question" class="checkbox-label">互动提问</label>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="additional-requirements">其他要求（可选）</label>
          <textarea 
            id="additional-requirements" 
            v-model="additionalRequirements" 
            placeholder="输入任何其他特殊要求或说明"
            class="form-control"
            rows="3"
          ></textarea>
        </div>
        
        <!-- 添加模型选择 -->
        <div class="form-group">
          <label class="form-label">AI模型选择:</label>
          <select id="model-select" v-model="selectedModel" class="form-control">
            <option v-for="model in modelList" :key="model.id" :value="model.id">
              {{ model.name }}
            </option>
          </select>
        </div>
        
        <div class="action-buttons">
          <button class="btn btn-primary" @click="generateWeibo" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '正在生成...' : '生成微博' }}
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
              <i class="ri-file-text-line"></i>
              微博结果
            </h3>
            <div class="action-buttons">
              <button @click="generateWeibo" class="primary-button" :disabled="isLoading">
                <i class="ri-refresh-line" v-if="!isLoading"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isLoading ? '生成中...' : '重新生成' }}
              </button>
              <button @click="copyResult" class="secondary-button" :disabled="isLoading || !generatedWeibo">
                <i class="ri-file-copy-line"></i>
                复制内容
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
            
            <div v-if="!generatedWeibo && !isLoading" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无微博内容，请点击"生成微博"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedWeibo" class="weibo-result" :class="{'blur-content': isLoading}">
              <div class="weibo-post">
                <div class="weibo-header">
                  <div class="weibo-avatar">
                    <i class="ri-user-line"></i>
                  </div>
                  <div class="weibo-user-info">
                    <h4 class="weibo-username">AI助手</h4>
                    <div class="weibo-timestamp">刚刚</div>
                  </div>
                </div>
                <div class="weibo-body">{{ generatedWeibo }}</div>
                <div class="weibo-stats">
                  <div class="weibo-stat">
                    <i class="ri-thumb-up-line"></i>
                    <span>赞</span>
                  </div>
                  <div class="weibo-stat">
                    <i class="ri-chat-1-line"></i>
                    <span>评论</span>
                  </div>
                  <div class="weibo-stat">
                    <i class="ri-share-forward-line"></i>
                    <span>转发</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 提示词模态框 -->
    <div class="modal" v-if="showPromptModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">AI提示词</h3>
          <button class="modal-close" @click="showPromptModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <pre class="prompt-content">{{ lastUsedPrompt }}</pre>
        </div>
        <div class="modal-footer">
          <button class="secondary-button" @click="showPromptModal = false">关闭</button>
          <button class="primary-button" @click="copyPrompt">
            <i class="ri-file-copy-line"></i>
            复制提示词
          </button>
        </div>
      </div>
    </div>
    
    <!-- 小贴士模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">微博创作小贴士</h3>
          <button class="modal-close" @click="showTipsModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>微博内容简洁有力，直入主题效果更好</li>
            <li>使用表情符号和话题标签可以增加互动性</li>
            <li>提出问题或邀请互动可以提高转发和评论率</li>
            <li>图文结合的内容更容易获得关注</li>
            <li>紧跟热点话题可以提高微博曝光度</li>
            <li>真实生活中的分享往往比抽象观点更有共鸣</li>
            <li>保持自己独特的风格和态度，更容易塑造个人品牌</li>
          </ul>
        </div>
        <div class="modal-footer">
          <button class="primary-button" @click="showTipsModal = false">明白了</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'WeiboArticle',
  data() {
    return {
      // 微博参数
      weiboType: 'trending',
      weiboTitle: '',
      targetAudience: '',
      weiboKeywords: '',
      writingStyle: 'casual',
      weiboLength: 'medium',
      additionalRequirements: '',
      
      // 内容元素
      includeEmoji: true,
      includeHashtags: true,
      includeMention: false,
      includeQuestion: true,
      
      // 生成结果
      generatedWeibo: '',
      lastUsedPrompt: '',
      
      // 状态
      isGenerating: false,
      isLoading: false,
      loadingText: 'AI正在创作中，请稍候...',
      showPromptModal: false,
      showTipsModal: false,
      
      // 模型选择
      selectedModel: 'deepseek-v3-vol', // 设置默认值
      modelList: [],
      
      // 参考案例
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      examples: [
        { icon: 'ri-briefcase-line', title: '职场感悟', desc: '分享工作中的感悟和经验' },
        { icon: 'ri-shopping-bag-line', title: '好物推荐', desc: '推荐最近使用的好产品' },
        { icon: 'ri-film-line', title: '影视评论', desc: '分享观影感受和推荐' },
        { icon: 'ri-football-line', title: '体育热点', desc: '体育赛事相关评论' },
        { icon: 'ri-book-open-line', title: '读书心得', desc: '分享阅读体验和推荐' },
        { icon: 'ri-seedling-line', title: '农业科技', desc: '农业技术与发展趋势' },
        { icon: 'ri-snowy-line', title: '冰雪产业', desc: '冬奥会后的冰雪经济' },
        { icon: 'ri-traffic-light-line', title: '智能交通', desc: '智能交通的应用与前景' },
        { icon: 'ri-charging-pile-line', title: '新能源汽车', desc: '电动汽车的现状与前景' },
        { icon: 'ri-bank-line', title: '金融科技', desc: '金融科技的创新与发展' }
      ]
    };
  },
  computed: {
    // 判断是否已经到达最后一页
    isLastPage() {
      // 计算是否已经滚动到最后一页
      const cardWidth = 185; // 卡片宽度+间距
      const containerWidth = this.$refs.exampleCarousel?.parentElement?.clientWidth || 0;
      const totalWidth = this.examples.length * cardWidth;
      const maxScrollX = totalWidth - containerWidth;
      
      // 当滚动到最大滚动距离的90%以上时，认为是最后一页
      return Math.abs(this.exampleTranslateX) >= maxScrollX * 0.9;
    }
  },
  mounted() {
    // 设置默认模型列表，防止等待API返回时界面显示"加载中"
    this.setupDefaultModels();
    // 然后尝试从API加载
    this.loadModels();
  },
  methods: {
    // 加载模型列表
    async loadModels() {
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
    
    // 生成微博
    async generateWeibo() {
      if (!this.validateForm()) return;
      
      this.isGenerating = true;
      this.isLoading = true;
      this.loadingText = 'AI正在创作中，请稍候...';
      
      try {
        // 构建提示词
        const prompt = this.buildPrompt();
        this.lastUsedPrompt = prompt;
        
        // 调用API并获取结果
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
            max_tokens: this.getMaxTokensByLength(this.weiboLength)
          };
          
          // 记录API请求详情，方便调试
          console.log('API请求参数:', JSON.stringify(apiParams));
          
          // 发送API请求 - 使用正确的API路径
          const response = await axios.post('/api/v1/llm/chat', apiParams, { timeout: 60000 });
          console.log('API响应:', response);
          
          if (response.data.status === 'success') {
            const content = response.data.data.choices[0].message.content;
            console.log('成功获取到结果:', content);
            this.generatedWeibo = content;
            // 添加提示消息到结果中，表明是调用API生成的
            this.$message && this.$message.success('已成功调用后端大模型生成内容');
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
            this.generatedWeibo = this.getOfflineGeneratedWeibo();
            this.$message && this.$message.warning('后端服务不可用，使用离线模式生成内容');
          } else {
            // 其他API错误
            throw error;
          }
        }
      } catch (error) {
        console.error('生成微博出错:', error);
        this.generatedWeibo = '抱歉，服务器暂时无法响应，请稍后再试';
        
        // 开发环境下提供测试数据
        if (process.env.NODE_ENV === 'development') {
          setTimeout(() => {
            this.generatedWeibo = this.getOfflineGeneratedWeibo();
          }, 1000);
        }
      } finally {
        this.isGenerating = false;
        this.isLoading = false;
      }
    },
    
    // 构建提示词
    buildPrompt() {
      let prompt = `请你扮演一位专业的社交媒体内容创作者，为我创作一条原创微博。\n\n`;
      
      // 添加微博类型
      const typeMap = {
        trending: '热点话题',
        lifestyle: '生活日常',
        review: '产品测评',
        humor: '幽默段子',
        question: '提问互动'
      };
      prompt += `微博类型：${typeMap[this.weiboType]}\n`;
      
      // 添加主题和目标受众
      prompt += `微博主题：${this.weiboTitle}\n`;
      prompt += `目标受众：${this.targetAudience}\n`;
      
      // 添加关键词
      prompt += `内容要点：${this.weiboKeywords}\n`;
      
      // 添加风格和长度
      const styleMap = {
        casual: '轻松日常',
        humorous: '幽默诙谐',
        professional: '专业正式',
        emotional: '情感充沛',
        sarcastic: '讽刺调侃'
      };
      prompt += `语言风格：${styleMap[this.writingStyle]}\n`;
      
      const lengthMap = {
        short: '简短 (50字以内)',
        medium: '中等 (50-100字)',
        long: '较长 (100-200字)',
        'super-long': '超长 (200-500字)'
      };
      prompt += `微博长度：${lengthMap[this.weiboLength]}\n`;
      
      // 添加内容元素需求
      prompt += `内容元素要求：\n`;
      if (this.includeEmoji) prompt += `- 请在适当的地方添加表情符号\n`;
      if (this.includeHashtags) prompt += `- 请添加1-3个相关话题标签，格式为 #话题#\n`;
      if (this.includeMention) prompt += `- 可以适当添加@某人的元素\n`;
      if (this.includeQuestion) prompt += `- 请在微博末尾添加互动性提问\n`;
      
      // 添加其他要求
      if (this.additionalRequirements) {
        prompt += `其他特殊要求：${this.additionalRequirements}\n`;
      }
      
      // 最后的格式说明
      prompt += `\n请直接输出微博内容，不需要添加任何额外解释。确保内容原创、有吸引力，符合微博平台的表达习惯。`;
      
      return prompt;
    },
    
    // 根据长度设置获取最大token数
    getMaxTokensByLength(length) {
      const tokenMap = {
        short: 100,
        medium: 200,
        long: 300,
        'super-long': 500
      };
      return tokenMap[length] || 200;
    },
    
    // 表单验证
    validateForm() {
      if (!this.weiboTitle) {
        alert('请输入微博主题');
        return false;
      }
      if (!this.targetAudience) {
        alert('请输入目标读者群体');
        return false;
      }
      if (!this.weiboKeywords) {
        alert('请输入微博关键词或内容要点');
        return false;
      }
      return true;
    },
    
    // 重置表单
    resetForm() {
      this.weiboTitle = '';
      this.targetAudience = '';
      this.weiboKeywords = '';
      this.writingStyle = 'casual';
      this.weiboLength = 'medium';
      this.additionalRequirements = '';
      this.includeEmoji = true;
      this.includeHashtags = true;
      this.includeMention = false;
      this.includeQuestion = true;
    },
    
    // 复制结果
    copyResult() {
      if (!this.generatedWeibo) return;
      
      navigator.clipboard.writeText(this.generatedWeibo)
        .then(() => {
          alert('微博内容已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          alert('复制失败，请手动复制');
        });
    },
    
    // 复制提示词
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      
      navigator.clipboard.writeText(this.lastUsedPrompt)
        .then(() => {
          alert('提示词已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          alert('复制失败，请手动复制');
        });
    },
    
    // 显示提示词
    showPrompt() {
      if (!this.lastUsedPrompt) return;
      this.showPromptModal = true;
    },
    
    // 显示小贴士
    showTips() {
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
    
    // 加载参考案例
    loadExample(exampleId) {
      // 解析示例编号
      const index = parseInt(exampleId.replace('example', '')) - 1;
      if (index < 0 || index >= this.examples.length) return;
      
      // 获取示例内容
      const example = this.examples[index];
      if (!example) return;
      
      console.log('加载示例:', index, example);
      
      // 根据示例设置不同的类型
      const typeMap = {
        '职场感悟': 'lifestyle',
        '好物推荐': 'review',
        '影视评论': 'trending',
        '体育热点': 'question',
        '读书心得': 'lifestyle',
        '农业科技': 'trending',
        '冰雪产业': 'trending',
        '智能交通': 'review',
        '新能源汽车': 'review',
        '金融科技': 'trending'
      };
      
      const styleMap = {
        '职场感悟': 'emotional',
        '好物推荐': 'casual',
        '影视评论': 'emotional',
        '体育热点': 'humorous',
        '读书心得': 'professional',
        '农业科技': 'professional',
        '冰雪产业': 'professional',
        '智能交通': 'casual',
        '新能源汽车': 'casual',
        '金融科技': 'professional'
      };
      
      // 设置微博参数
      this.weiboType = typeMap[example.title] || 'trending';
      this.weiboTitle = example.title;
      this.targetAudience = example.desc.includes('爱好者') ? example.desc.split('爱好者')[0] + '爱好者' : example.desc.split('的')[0] + '关注者';
      this.weiboKeywords = example.desc;
      this.writingStyle = styleMap[example.title] || 'casual';
      this.weiboLength = 'medium';
      
      // 设置合适的内容元素
      if (this.weiboType === 'question') {
        this.includeQuestion = true;
      }
      
      console.log('已设置参数:', {
        type: this.weiboType,
        title: this.weiboTitle,
        audience: this.targetAudience,
        keywords: this.weiboKeywords,
        style: this.writingStyle
      });
    },
    
    // 离线生成的示例微博（开发环境使用）
    getOfflineGeneratedWeibo() {
      // 根据不同的微博类型生成对应的示例内容
      let samples = [];
      
      switch(this.weiboType) {
        case 'review':
          samples = [
            `刚入手的新款蓝牙耳机体验分享！🎧 降噪效果真的惊艳到我，地铁上嘈杂声瞬间消失，仿佛拥有了专属小宇宙！续航给我惊到，重度使用三天都不用充电！透明模式下交流完全不受影响，音质也相当不错👍 #数码好物推荐# #蓝牙耳机推荐# 你们用过这款吗？感觉如何？`,
            `最近买的智能家居套装也太香了！💯 一句话控制全屋设备，回家自动开灯调温度，安防系统也很给力。特别是那个智能窗帘，早上跟着日出自动打开，起床体验不要太舒服～ #好物分享# #智能家居套装# 大家有没有智能家居踩坑经历？求分享经验～`,
            `新款电动牙刷入手两周报告📝 震动精准到位，清洁力比普通牙刷强太多！App监测刷牙死角很实用，充一次电能用20天。最爱的是旅行便携盒设计，出差带着超方便，再也不会忘记充电了😁 #测评分享# #口腔护理好物# 你们现在还在用普通牙刷吗？`
          ];
          break;
          
        case 'trending':
          samples = [
            `《流浪地球2》今天二刷回来…真的被国产科幻片的进步震撼到了！特效已经完全不输好莱坞，剧情更是紧凑到让人窒息😱。最震撼的还是那种面对毁灭时的东方式浪漫与坚韧，看完莫名感到心安。中国科幻电影的未来，好像一下子就有了更多可能性✨。#流浪地球2# #国产科幻电影# 你们看了吗？最喜欢哪个片段？`,
            `最近数字人民币普及也太快了吧！今天商场购物全程数字钱包支付，比传统支付还便捷，完全不需要掏手机了。据说还能离线支付，网络崩了也能用，这波操作很有未来感啊！#数字人民币# #支付新方式# 有多少朋友已经开始使用数字人民币了？体验如何？`,
            `AIGC技术发展真的太快了！今天试了最新的AI绘画工具，只需输入几个关键词就能生成超写实图像，完全颠覆了我对创作的理解！这是一场彻底的创意革命，以后设计师工作会被取代吗？🤔 #AI绘画# #AIGC趋势# 大家怎么看待AI创作的未来？`
          ];
          break;
          
        case 'lifestyle':
          samples = [
            `#2023职场感悟# 这周终于啃下了那个困扰团队半个月的技术难题！熬夜加班的疲惫一扫而空，成就感真的是工作中最好的续航能量了✨。感谢团队每个人的付出，单打独斗永远不如众人拾柴。职场中最重要的，与其说是个人能力，不如说是解决问题的决心和团队协作的默契。你们职场中遇到过最有成就感的时刻是什么？一起分享吧！👇`,
            `今日份早餐打卡：自制全麦三明治+鲜榨果汁🥪 早起半小时，给自己做顿营养早餐，整个上午都元气满满！把时间花在仪式感上，生活品质真的会不一样～ #健康生活方式# #早餐日记# 你们平时早餐都吃什么？有推荐的快手早餐吗？`,
            `连续21天健身打卡成功！💪 刚开始真的每天都要靠意志力爬起来，现在已经养成习惯，不运动反而难受。体重下降5斤，精神状态也好了很多，朋友都说我气色变好了！健身真的是最值得坚持的事情之一。#健身打卡# #生活习惯养成# 有多少人因为懒放弃了健身？😂`
          ];
          break;
          
        case 'humor':
          samples = [
            `今天在公司茶水间听到两位同事聊天：\n"你知道AI为什么这么火吗？"\n"为什么？"\n"因为它不用996，不用交五险一金，不用年终述职，不吃不喝不休假还不辞职！"\n"那我们岂不是要失业了？😱"\n"放心，我们还有一个无可替代的优势..."\n"什么优势？"\n"我们会喝奶茶啊！" 🧋\n#职场段子# #AI时代# 你们觉得AI会取代哪些工作？`,
            `深夜打开冰箱，发现昨天的外卖在跟我热情招手👋\n我：你还能吃吗？\n外卖：那要看你的勇气了！\n我：……\n鼓起勇气吃了后，我成功…………\n躺在了卫生间地板上🥲\n#生活段子# #深夜卫生间爆笑史# 有多少人跟我一样勇敢（傻）？`,
            `刚才看到一个段子笑死我了：\n女朋友："亲爱的，如果我和你妈同时掉水里，你先救谁？"\n男友思考片刻："我先救我妈，然后再救你。"\n女友大怒："为什么！？"\n男友诚恳道："因为我妈不会游泳，你不是说你当年校运会游泳拿过冠军吗？" 😂\n#爆笑情侣日常# #恋爱脑回路# 你们遇到过类似的灵魂拷问吗？`
          ];
          break;
          
        case 'question':
          samples = [
            `世界杯1/4决赛也太刺激了吧！😱 梅西那脚助攻简直神来之笔，看得我从沙发上跳起来！C罗那个表情，心都要碎了。足球就是这样，一瞬间可以改变一切。突然意识到这可能是这两位球王同台的最后一届世界杯了…有点舍不得😢 #卡塔尔世界杯# #梅西C罗# 大家支持哪个队夺冠啊？评论区告诉我！⚽`,
            `大家有没有发现，很多时候我们舍不得为自己花钱，但给家人朋友买礼物却毫不犹豫？🎁 今天给妈妈买了一个很贵的护肤品，自己却一直舍不得买，看到她笑得那么开心，突然觉得很值得！#生活感悟# #亲情# 你们最近为爱的人花的最值得的一笔钱是什么？`,
            `现在各APP的广告是不是越来越离谱了？😡 刚才看视频，正看到关键时刻，突然蹦出30秒广告！我真的会谢！有时候就想为了避开广告开个会员，但又觉得这是掉进了商家的陷阱...#吐槽大会# #APP广告# 你们会为了避开广告而开会员吗？怎么看待这种营销策略？`
          ];
          break;
          
        default:
          samples = [
            `今天的阳光也太好了吧！☀️ 午休时在公司楼下晒了会太阳，整个人都元气满满！这种初春的温暖真的很治愈，感觉冬天的阴霾一扫而空～生活中这种小确幸真的很重要。#春日分享# #生活碎片# 你们今天的小确幸是什么呢？`,
            `刚刚看完《流浪地球2》，被震撼到了！中国科幻电影真的成长了😭 特效不输好莱坞，情感戏更是催泪，那种东方式的浪漫与牺牲精神太感人了。看完走出影院时感觉整个人都被掏空了，但又充满希望。#流浪地球2# #国产科幻# 有一起看的吗？感觉如何？`,
            `新入手的降噪耳机体验分享！🎧 地铁上嘈杂声瞬间消失90%，仿佛有了专属小世界！续航能力超乎想象，重度使用三天才需充电一次。最爱的是透明模式，不用摘下就能正常交流，太智能了！#好物分享# #数码推荐# 你们用过哪款降噪耳机体验最好？`
          ];
      }
      
      const index = Math.floor(Math.random() * samples.length);
      return samples[index];
    }
  }
};
</script>

<style scoped>
.weibo-article-page {
  padding: 0;
  margin-top: -40px; /* 与公众号文章位置一致 */
  background-color: #f7f7f7;
  min-height: calc(100vh - 60px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-nav h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.page-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border: 1px solid #eee;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background-color: #f0f0f0;
}

.action-btn i {
  font-size: 18px;
  color: #666;
}

/* 两列布局 */
.main-container {
  display: flex;
  gap: 20px;
}

.input-section {
  width: 45%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 标题样式 */
.section-header {
  padding: 10px 0;
  margin-bottom: 10px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 18px;
  color: #333;
}

.section-title i {
  color: var(--primary-color, #ba003f);
}

/* 表单样式 */
.form-group {
  flex: 1;
  margin-bottom: 16px;
  position: relative;
  transition: all 0.3s ease;
}

.form-group:hover label {
  color: var(--primary-color, #ba003f);
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #444;
  font-weight: 500;
  transition: color 0.3s ease;
}

.form-group label.required::after {
  content: '*';
  color: var(--primary-color, #ba003f);
  margin-left: 4px;
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

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 16px;
}

/* 复选框样式 - 优化外观 */
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 8px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f9f9f9;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #eee;
  transition: all 0.2s;
}

.checkbox-item:hover {
  background: #f2f2f2;
  border-color: #ddd;
}

.checkbox-label {
  margin: 0;
  font-weight: normal;
  cursor: pointer;
  color: #555;
}

input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--primary-color, #ba003f);
}

/* 按钮样式 */
.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn {
  padding: 10px 15px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
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
  flex: 2;
}

.btn-primary:hover {
  background-color: #d4185b;
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.2);
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #444;
  flex: 1;
}

.btn-secondary:hover {
  background-color: #e5e5e5;
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.15);
  transform: translateY(-2px);
}

.primary-button, .secondary-button, .prompt-button {
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  border: none;
  transition: all 0.2s;
}

.primary-button {
  background-color: var(--primary-color, #ba003f);
  color: white;
}

.primary-button:hover {
  background-color: #d4185b;
}

.secondary-button {
  background-color: #f5f5f5;
  color: #444;
  border: 1px solid #eee;
}

.secondary-button:hover {
  background-color: #e5e5e5;
}

.prompt-button {
  background-color: transparent;
  color: var(--primary-color, #ba003f);
  border: 1px solid var(--primary-color, #ba003f);
}

.prompt-button:hover {
  background-color: rgba(186, 0, 63, 0.05);
}

/* 加载状态 */
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

.spinning {
  animation: spin 1.5s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 参考案例样式 */
.examples-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 15px;
}

.examples-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.example-carousel {
  overflow: hidden;
}

.example-cards {
  display: flex;
  gap: 15px;
  transition: transform 0.3s ease;
}

.example-card {
  flex: 0 0 170px; /* 减小固定宽度，显示更多案例 */
  background-color: #fff;
  border-radius: 8px;
  padding: 12px 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #eee;
  display: flex;
  flex-direction: row;
  gap: 12px;
  overflow: hidden; /* 防止内容溢出 */
}

.example-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  border-color: var(--primary-color, #ba003f);
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
  margin-bottom: 5px;
  color: #333;
  font-size: 16px;
}

.example-desc {
  color: #666;
  font-size: 14px;
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

/* 结果展示样式 */
.result-section {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.section-header .action-buttons {
  margin: 0;
  display: flex;
  gap: 8px;
}

.result-content-wrapper {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 400px;
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
  border-radius: 0 0 8px 8px;
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

.blur-content {
  filter: blur(1px);
  opacity: 0.6;
  pointer-events: none;
}

/* 微博特有样式 */
.weibo-result {
  padding: 20px;
}

.weibo-post {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
}

.weibo-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.weibo-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-color, #ba003f);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.weibo-avatar i {
  font-size: 20px;
  color: white;
}

.weibo-username {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 2px 0;
}

.weibo-timestamp {
  font-size: 12px;
  color: #999;
}

.weibo-body {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 15px;
  white-space: pre-wrap;
  word-break: break-word;
}

.weibo-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 10px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.weibo-stat {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  cursor: pointer;
  transition: color 0.2s;
}

.weibo-stat:hover {
  color: var(--primary-color, #ba003f);
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

.modal-close {
  background: none;
  border: none;
  color: #666;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.modal-close:hover {
  background-color: #f0f0f0;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: calc(80vh - 130px);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #eee;
}

.prompt-content {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  border-left: 3px solid var(--primary-color, #ba003f);
  margin: 0;
  overflow-x: auto;
}

.tips-list {
  padding-left: 20px;
  margin: 0;
}

.tips-list li {
  margin-bottom: 12px;
  color: #555;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section, .right-column {
    width: 100%;
  }
  
  .examples-section {
    margin-bottom: 20px;
  }
}
</style> 