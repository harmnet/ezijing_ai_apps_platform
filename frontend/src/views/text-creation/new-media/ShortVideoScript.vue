<template>
  <div class="short-video-script-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>短视频脚本生成</h2>
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
        
        <!-- 目标平台选择 -->
        <div class="form-group">
          <label>目标平台</label>
          <div class="platform-category-container">
            <div 
              v-for="platform in platforms" 
              :key="platform.id"
              class="platform-category-card" 
              :class="{ 'selected': selectedPlatform === platform.id }"
              @click="selectedPlatform = platform.id"
            >
              <div class="platform-category-icon">
                <i :class="platform.icon"></i>
              </div>
              <div class="platform-category-name">{{ platform.name }}</div>
            </div>
          </div>
        </div>
        
        <!-- 视频类别选择 -->
        <div class="form-group">
          <label>视频类别</label>
          <div class="platform-category-container">
            <div 
              v-for="category in categories" 
              :key="category.id"
              class="platform-category-card" 
              :class="{ 'selected': selectedCategory === category.id }"
              @click="selectedCategory = category.id"
            >
              <div class="platform-category-icon">
                <i :class="category.icon"></i>
              </div>
              <div class="platform-category-name">{{ category.name }}</div>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="video-topic" class="required">视频主题/内容</label>
          <textarea 
            id="video-topic" 
            v-model="videoTopic" 
            class="form-control" 
            rows="3" 
            placeholder="描述您想表达的主题或内容要点"
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="target-audience" class="required">目标受众</label>
            <input 
              type="text" 
              id="target-audience" 
              v-model="targetAudience" 
              class="form-control" 
              placeholder="描述您的目标观众群体"
            />
          </div>
          <div class="form-group">
            <label for="keywords" class="required">关键词/要点</label>
            <input 
              type="text" 
              id="keywords" 
              v-model="keywords" 
              class="form-control" 
              placeholder="用逗号分隔多个关键词"
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="style">风格基调</label>
            <select id="style" v-model="style" class="form-control">
              <option value="教学型">教学型 - 清晰专业的讲解</option>
              <option value="幽默型">幽默型 - 轻松有趣的表达</option>
              <option value="故事型">故事型 - 娓娓道来的叙述</option>
              <option value="干货型">干货型 - 直接有效的知识点</option>
              <option value="情感型">情感型 - 富有共鸣的分享</option>
            </select>
          </div>
          <div class="form-group">
            <label for="duration">视频时长</label>
            <select id="duration" v-model="duration" class="form-control">
              <option value="15-30秒">15-30秒 - 超短视频</option>
              <option value="30-60秒">30-60秒 - 标准短视频</option>
              <option value="1-2分钟">1-2分钟 - 中等长度</option>
              <option value="2-5分钟">2-5分钟 - 较长视频</option>
              <option value="5-10分钟">5-10分钟 - 长视频</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label>脚本元素</label>
          <div class="checkbox-group">
            <div class="checkbox-item">
              <input type="checkbox" id="includeSceneDesc" v-model="includeSceneDesc">
              <label for="includeSceneDesc">场景描述</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="includeDialogue" v-model="includeDialogue">
              <label for="includeDialogue">对白/解说</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="includeTextOverlay" v-model="includeTextOverlay">
              <label for="includeTextOverlay">屏显文字</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="includeShots" v-model="includeShots">
              <label for="includeShots">镜头建议</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="includeMusic" v-model="includeMusic">
              <label for="includeMusic">音乐/音效</label>
            </div>
            <div class="checkbox-item">
              <input type="checkbox" id="includeCTA" v-model="includeCTA">
              <label for="includeCTA">互动引导</label>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="additional-notes">附加说明 (可选)</label>
          <textarea 
            id="additional-notes" 
            v-model="additionalNotes" 
            class="form-control" 
            rows="2" 
            placeholder="添加其他特殊要求或说明"
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
          <button class="btn btn-primary" @click="generateScript" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '正在生成...' : '生成短视频脚本' }}
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
              <div 
                class="example-card" 
                v-for="(example, index) in examples" 
                :key="index" 
                @click="loadExample(example.id)"
              >
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
              脚本结果
            </h3>
            <div class="action-buttons">
              <button @click="generateScript" class="primary-button" :disabled="isGenerating">
                <i class="ri-refresh-line" v-if="!isGenerating"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isGenerating ? '生成中...' : '重新生成' }}
              </button>
              <button @click="copyResult" class="secondary-button" :disabled="isGenerating || !generatedScript">
                <i class="ri-file-copy-line"></i>
                复制脚本
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
            
            <div v-if="!generatedScript && !isGenerating" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无脚本内容，请点击"生成短视频脚本"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedScript" class="script-result" :class="{'blur-content': isGenerating}">
              <div class="script-content" v-html="formattedScript"></div>
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
            <li>视频主题应明确具体，避免过于宽泛的表述</li>
            <li>针对不同平台调整内容长度和节奏，如抖音侧重简短吸引，B站可更加详细</li>
            <li>开场3-5秒极为关键，应直接点明主题或设置悬念吸引观众</li>
            <li>考虑目标受众的兴趣点和痛点，内容应该解决特定问题</li>
            <li>保持内容结构清晰，通常采用"开场-主体内容-结尾互动"的三段式</li>
            <li>适当添加转场和视觉效果建议，增强观看体验</li>
            <li>引导观众互动的CTA很重要，可提高视频完播率和互动率</li>
          </ul>
        </div>
      </div>
    </div>
    
    <!-- 提示词查看模态框 -->
    <div class="modal prompt-modal" v-if="showPromptModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="ri-code-box-line"></i> 生成提示词</h3>
          <button class="close-btn" @click="showPromptModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="prompt-content">
            {{ lastUsedPrompt[1].content }}
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
  name: 'ShortVideoScript',
  data() {
    return {
      // 平台和类别
      platforms: [
        { id: 'douyin', name: '抖音', icon: 'ri-music-fill' },
        { id: 'kuaishou', name: '快手', icon: 'ri-camera-fill' },
        { id: 'bilibili', name: 'B站', icon: 'ri-bilibili-fill' },
        { id: 'xiaohongshu', name: '小红书', icon: 'ri-book-2-fill' },
        { id: 'weibo', name: '微博', icon: 'ri-weibo-fill' },
        { id: 'wechat', name: '视频号', icon: 'ri-wechat-fill' }
      ],
      categories: [
        { id: 'tutorial', name: '教程指南', icon: 'ri-book-open-line' },
        { id: 'vlog', name: '日常记录', icon: 'ri-movie-line' },
        { id: 'review', name: '产品测评', icon: 'ri-shopping-bag-line' },
        { id: 'comedy', name: '搞笑娱乐', icon: 'ri-emotion-laugh-line' },
        { id: 'knowledge', name: '知识科普', icon: 'ri-lightbulb-line' },
        { id: 'story', name: '故事讲述', icon: 'ri-chat-heart-line' }
      ],
      selectedPlatform: 'douyin',
      selectedCategory: 'tutorial',
      
      // 表单数据
      videoTopic: '',
      targetAudience: '',
      keywords: '',
      style: '教学型',
      duration: '30-60秒',
      
      // 脚本元素
      includeSceneDesc: true,
      includeDialogue: true,
      includeTextOverlay: true,
      includeShots: false,
      includeMusic: false,
      includeCTA: true,
      
      additionalNotes: '',
      
      // 结果内容
      generatedScript: '',
      isGenerating: false,
      loadingText: '正在生成脚本内容，请耐心等待...',
      lastUsedPrompt: null,
      
      // 模态框控制
      showTipsModal: false,
      showPromptModal: false,
      
      // 模型选择
      selectedModel: 'deepseek-v3-vol',
      modelList: [],
      
      // 轮播设置
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      
      // 参考案例数据
      examples: [
        {
          id: 'douyin-tutorial',
          title: '手机摄影技巧',
          desc: '抖音风格教程',
          platform: 'douyin',
          category: 'tutorial',
          icon: 'ri-camera-line',
          topic: '如何用手机拍出专业级照片',
          audience: '摄影爱好者，18-35岁年轻人',
          keywords: '手机摄影,构图技巧,光线利用,后期处理',
          style: '教学型',
          duration: '30-60秒'
        },
        {
          id: 'bilibili-knowledge',
          title: '历史冷知识',
          desc: 'B站科普视频',
          platform: 'bilibili',
          category: 'knowledge',
          icon: 'ri-time-line',
          topic: '鲜为人知的历史趣闻：古代人如何计时？',
          audience: '历史爱好者，学生，知识分子',
          keywords: '历史知识,日晷,水钟,计时工具,古代科技',
          style: '干货型',
          duration: '2-5分钟'
        },
        {
          id: 'xiaohongshu-review',
          title: '美妆新品评测',
          desc: '小红书测评视频',
          platform: 'xiaohongshu',
          category: 'review',
          icon: 'ri-palette-line',
          topic: '平价替代大牌？这5款国货粉底实测对比',
          audience: '美妆爱好者，女性，18-30岁',
          keywords: '美妆测评,国货粉底,性价比,使用感受,持久度',
          style: '教学型',
          duration: '1-2分钟'
        },
        {
          id: 'kuaishou-comedy',
          title: '烦恼日常',
          desc: '搞笑吐槽视频',
          platform: 'kuaishou',
          category: 'comedy',
          icon: 'ri-emotion-laugh-line',
          topic: '当代年轻人的居家烦恼',
          audience: '年轻上班族，20-35岁',
          keywords: '生活吐槽,搞笑,日常烦恼,居家生活,反差感',
          style: '幽默型',
          duration: '15-30秒'
        },
        {
          id: 'weibo-vlog',
          title: '美食Vlog',
          desc: '美食日常记录',
          platform: 'weibo',
          category: 'vlog',
          icon: 'ri-restaurant-line',
          topic: '跟我一起做简单美味的家常菜',
          audience: '家庭煮夫煮妇，美食爱好者',
          keywords: '美食vlog,家常菜,简单料理,烹饪技巧,食材搭配',
          style: '故事型',
          duration: '1-2分钟'
        },
        {
          id: 'wechat-story',
          title: '职场成长故事',
          desc: '视频号成长分享',
          platform: 'wechat',
          category: 'story',
          icon: 'ri-briefcase-line',
          topic: '从菜鸟到主管：我的5年职场蜕变之路',
          audience: '职场新人，求职者，职场人士',
          keywords: '职场成长,经验分享,职业发展,工作技巧,自我提升',
          style: '情感型',
          duration: '2-5分钟'
        }
      ]
    }
  },
  
  computed: {
    // 格式化脚本展示
    formattedScript() {
      if (!this.generatedScript) return '';
      
      let formatted = this.generatedScript;
      
      // 替换标题格式
      formatted = formatted.replace(/^#\s(.*?)$/gm, '<h1>$1</h1>');
      formatted = formatted.replace(/^##\s(.*?)$/gm, '<h2>$1</h2>');
      formatted = formatted.replace(/^###\s(.*?)$/gm, '<h3>$1</h3>');
      
      // 处理分节符号
      formatted = formatted.replace(/^----*$/gm, '<hr>');
      
      // 处理场景描述
      formatted = formatted.replace(/【场景】(.*?)(?=\n)/g, '<div class="scene-desc"><strong>【场景】</strong>$1</div>');
      formatted = formatted.replace(/【场景描述】(.*?)(?=\n)/g, '<div class="scene-desc"><strong>【场景描述】</strong>$1</div>');
      
      // 处理对白/解说
      formatted = formatted.replace(/【解说】(.*?)(?=\n)/g, '<div class="dialogue"><strong>【解说】</strong>$1</div>');
      formatted = formatted.replace(/【对白】(.*?)(?=\n)/g, '<div class="dialogue"><strong>【对白】</strong>$1</div>');
      
      // 处理屏显文字
      formatted = formatted.replace(/【文字】(.*?)(?=\n)/g, '<div class="text-overlay"><strong>【文字】</strong>$1</div>');
      formatted = formatted.replace(/【屏显】(.*?)(?=\n)/g, '<div class="text-overlay"><strong>【屏显】</strong>$1</div>');
      
      // 处理镜头建议
      formatted = formatted.replace(/【镜头】(.*?)(?=\n)/g, '<div class="shot"><strong>【镜头】</strong>$1</div>');
      
      // 处理音乐/音效
      formatted = formatted.replace(/【音乐】(.*?)(?=\n)/g, '<div class="music"><strong>【音乐】</strong>$1</div>');
      formatted = formatted.replace(/【音效】(.*?)(?=\n)/g, '<div class="music"><strong>【音效】</strong>$1</div>');
      
      // 处理互动引导
      formatted = formatted.replace(/【互动】(.*?)(?=\n)/g, '<div class="cta"><strong>【互动】</strong>$1</div>');
      formatted = formatted.replace(/【CTA】(.*?)(?=\n)/g, '<div class="cta"><strong>【CTA】</strong>$1</div>');
      
      // 处理换行符
      formatted = formatted.replace(/\n\n/g, '<br><br>');
      formatted = formatted.replace(/\n/g, '<br>');
      
      return formatted;
    },
    
    // 判断是否已经到达最后一页
    isLastPage() {
      if (!this.$refs.exampleCarousel) return false;
      
      // 计算是否已经滚动到最后一页
      const cardWidth = 210; // 卡片宽度+间距
      const containerWidth = this.$refs.exampleCarousel?.parentElement?.clientWidth || 0;
      const totalWidth = this.examples.length * cardWidth;
      const maxScrollX = Math.max(0, totalWidth - containerWidth);
      
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
        
        if (response.data && response.data.status === 'success') {
          // 获取模型列表
          this.modelList = response.data.data || [];
          
          // 默认选择火山引擎V3模型
          const volcanoV3 = this.modelList.find(model => model.id === 'deepseek-v3-vol');
          if (volcanoV3) {
            this.selectedModel = 'deepseek-v3-vol';
          } else if (this.modelList.length > 0) {
            // 如果没有火山引擎V3模型但有其他模型，则选择第一个
            this.selectedModel = this.modelList[0].id;
          }
          
          console.log('已设置默认模型:', this.selectedModel);
        } else {
          console.error('获取模型列表失败:', response.data?.message);
          // 设置默认值
          this.setupDefaultModels();
        }
      } catch (error) {
        console.error('获取模型列表异常:', error);
        // 设置默认值
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
    
    // 显示创作小贴士
    showTips() {
      this.showTipsModal = true;
    },
    
    // 显示提示词
    showPrompt() {
      if (this.lastUsedPrompt) {
        this.showPromptModal = true;
      }
    },
    
    // 复制结果
    copyResult() {
      if (!this.generatedScript) return;
      
      // 创建一个不可见的textarea元素
      const textarea = document.createElement('textarea');
      textarea.value = this.generatedScript;
      document.body.appendChild(textarea);
      textarea.select();
      
      try {
        // 执行复制命令
        document.execCommand('copy');
        alert('已复制到剪贴板');
      } catch (err) {
        console.error('复制失败:', err);
        alert('复制失败，请手动复制');
      } finally {
        document.body.removeChild(textarea);
      }
    },
    
    // 复制提示词
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      
      // 创建一个不可见的textarea元素
      const textarea = document.createElement('textarea');
      textarea.value = this.lastUsedPrompt[1].content;
      document.body.appendChild(textarea);
      textarea.select();
      
      try {
        // 执行复制命令
        document.execCommand('copy');
        alert('已复制提示词到剪贴板');
      } catch (err) {
        console.error('复制失败:', err);
        alert('复制失败，请手动复制');
      } finally {
        document.body.removeChild(textarea);
      }
    },
    
    // 重置表单
    resetForm() {
      this.videoTopic = '';
      this.targetAudience = '';
      this.keywords = '';
      this.style = '教学型';
      this.duration = '30-60秒';
      this.includeSceneDesc = true;
      this.includeDialogue = true;
      this.includeTextOverlay = true;
      this.includeShots = false;
      this.includeMusic = false;
      this.includeCTA = true;
      this.additionalNotes = '';
      this.generatedScript = '';
      this.lastUsedPrompt = null;
    },
    
    // 加载示例
    loadExample(exampleId) {
      const example = this.examples.find(e => e.id === exampleId);
      if (!example) return;
      
      this.selectedPlatform = example.platform;
      this.selectedCategory = example.category;
      this.videoTopic = example.topic;
      this.targetAudience = example.audience;
      this.keywords = example.keywords;
      this.style = example.style;
      this.duration = example.duration;
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
      if (!this.isLastPage && this.$refs.exampleCarousel) {
        this.currentExampleIndex++;
        this.updateExampleCarousel();
      }
    },
    
    // 更新轮播位置
    updateExampleCarousel() {
      if (!this.$refs.exampleCarousel) return;
      
      const cardWidth = 210; // 卡片宽度+间距
      this.exampleTranslateX = -this.currentExampleIndex * cardWidth;
      this.$refs.exampleCarousel.style.transform = `translateX(${this.exampleTranslateX}px)`;
    },
    
    // 获取选中的元素
    getSelectedElements() {
      const elements = [];
      if (this.includeSceneDesc) elements.push('场景描述');
      if (this.includeDialogue) elements.push('对白/解说');
      if (this.includeTextOverlay) elements.push('屏显文字');
      if (this.includeShots) elements.push('镜头建议');
      if (this.includeMusic) elements.push('音乐/音效');
      if (this.includeCTA) elements.push('互动引导');
      return elements.join('、');
    },
    
    // 构建提示词
    buildPrompt() {
      const platformName = this.platforms.find(p => p.id === this.selectedPlatform)?.name || '抖音';
      const categoryName = this.categories.find(c => c.id === this.selectedCategory)?.name || '教程指南';
      
      // 获取已选择的元素
      const selectedElements = this.getSelectedElements();
      
      // 构建系统消息
      const systemMessage = {
        role: 'system',
        content: `你是一位专业的短视频脚本策划师，熟悉各大平台的内容特点和受众喜好。请根据用户提供的信息，创建一个适合${platformName}平台的${categoryName}类短视频脚本。脚本应该符合平台特色、视频类型要求，并且能够有效吸引目标受众。`
      };
      
      // 构建用户消息
      let userMessage = `请为我创建一个短视频脚本，具体要求如下：

目标平台：${platformName}
视频类别：${categoryName}
视频主题：${this.videoTopic || '(用户未提供具体主题)'}
目标受众：${this.targetAudience || '(用户未提供目标受众)'}
关键词/要点：${this.keywords || '(用户未提供关键词)'}
风格基调：${this.style}
视频时长：${this.duration}
`;

      // 添加脚本元素要求
      userMessage += `\n需要包含的脚本元素：${selectedElements}`;
      
      // 添加附加说明
      if (this.additionalNotes) {
        userMessage += `\n\n附加说明：${this.additionalNotes}`;
      }
      
      // 添加输出格式要求
      userMessage += `\n\n请按照以下格式输出脚本：
1. 脚本标题（以"#"开头）
2. 视频概要（简短介绍视频内容和目的）
3. 分场景详细脚本，每个场景包含：`;
      
      // 根据选择的元素添加格式要求
      if (this.includeSceneDesc) userMessage += "\n   - 【场景】描述拍摄场景和画面";
      if (this.includeDialogue) userMessage += "\n   - 【解说】或【对白】内容";
      if (this.includeTextOverlay) userMessage += "\n   - 【文字】屏幕上显示的文本内容";
      if (this.includeShots) userMessage += "\n   - 【镜头】镜头角度和运动建议";
      if (this.includeMusic) userMessage += "\n   - 【音乐】背景音乐或音效建议";
      if (this.includeCTA) userMessage += "\n   - 【互动】引导观众评论、点赞或关注的话术";
      
      // 返回完整的提示词
      return [
        systemMessage,
        { role: 'user', content: userMessage }
      ];
    },
    
    // 生成脚本
    async generateScript() {
      if (this.isGenerating) return;
      
      // 基础验证
      if (!this.videoTopic || !this.targetAudience || !this.keywords) {
        alert('请填写必填字段：视频主题、目标受众和关键词');
        return;
      }
      
      // 开始生成
      this.isGenerating = true;
      this.loadingText = '正在生成脚本内容，请耐心等待...';
      
      try {
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3-vol';
        }
        
        // 构建提示词
        const prompt = this.buildPrompt();
        this.lastUsedPrompt = prompt;
        
        console.log('使用模型:', this.selectedModel);
        console.log('发送请求...');
        
        // 调用API生成内容
        const response = await axios.post('/api/v1/llm/chat', {
          model: this.selectedModel,
          messages: prompt,
          temperature: 0.7,
          top_p: 0.95,
          max_tokens: 2000
        });
        
        console.log('API响应:', response);
        
        // 处理响应结果
        if (response.data && response.data.status === 'success') {
          // 从响应中提取生成的内容
          let content = '';
          
          if (response.data.data && response.data.data.choices && response.data.data.choices.length > 0) {
            // 火山引擎格式
            const message = response.data.data.choices[0].message;
            content = message.content || '';
          } else if (response.data.data && response.data.data.response) {
            // 硅基流动格式
            content = response.data.data.response || '';
          } else if (response.data.data && typeof response.data.data === 'string') {
            // 直接返回字符串
            content = response.data.data;
          } else if (response.data.content) {
            // 直接包含在内容字段
            content = response.data.content;
          }
          
          if (content) {
            this.generatedScript = content;
          } else {
            console.error('无法从响应中提取内容:', response.data);
            this.generatedScript = '抱歉，生成内容时出现错误，请重试。';
            
            // 开发模式下使用示例内容
            if (process.env.NODE_ENV === 'development') {
              this.generatedScript = this.getDemoScript();
              console.log('开发模式：使用示例内容');
            }
          }
        } else {
          console.error('生成内容失败:', response.data?.message || '未知错误');
          alert('生成内容失败: ' + (response.data?.message || '请重试'));
          
          // 开发模式下使用示例内容
          if (process.env.NODE_ENV === 'development') {
            this.generatedScript = this.getDemoScript();
            console.log('开发模式：使用示例内容');
          } else {
            this.generatedScript = '抱歉，生成内容时出现错误，请重试。';
          }
        }
      } catch (error) {
        console.error('生成脚本异常:', error);
        alert('生成内容异常: ' + (error.message || '请重试'));
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          this.generatedScript = this.getDemoScript();
          console.log('开发模式：使用示例内容');
        } else {
          this.generatedScript = '抱歉，生成内容时出现错误，请重试。';
        }
      } finally {
        this.isGenerating = false;
      }
    },
    
    // 获取示例脚本（仅开发模式使用）
    getDemoScript() {
      return `# ${this.videoTopic || '如何用手机拍出专业级照片'} - ${this.platforms.find(p => p.id === this.selectedPlatform)?.name || '抖音'}脚本

这是一个${this.duration}长度的${this.style}短视频，针对${this.targetAudience || '摄影爱好者'}，讲解${this.videoTopic || '手机摄影技巧'}。

### 开场部分

【场景】博主手持最新款手机，站在明亮的室内环境，镜头特写手机和博主面部

【解说】嘿，各位！不需要昂贵的相机，只用这个小东西，也能拍出让朋友惊叹的大片！

【文字】手机也能拍大片？

【音乐】轻快现代的背景音乐，节奏感强

### 主体部分1：构图技巧

【场景】博主展示手机拍摄界面，演示不同构图方式

【解说】第一个技巧：构图！三分法构图超简单，把主体放在这些交叉点上，立刻提升照片质感！

【文字】技巧一：三分法构图

【镜头】特写手机屏幕，展示构图网格和实际拍摄效果对比

### 主体部分2：光线运用

【场景】博主在窗边演示不同光线角度的效果

【解说】第二个必杀技：善用自然光！侧光最显立体感，顺光拍人更好看，逆光...呃，等等，看我的小技巧！

【文字】技巧二：巧用光线

【镜头】展示同一场景在不同光线角度下的效果对比

### 主体部分3：简单后期

【场景】博主演示手机上的简单后期调整

【解说】最后，简单调整一下就能大大提升照片质感！对比度+15，饱和度轻微提高，加点暖色调...瞬间高级感拉满！

【文字】技巧三：一分钟后期

### 结尾部分

【场景】展示几张使用这些技巧拍摄的成片

【解说】掌握这三点，你也可以随手拍大片！评论区告诉我你最喜欢哪个技巧，下期想学什么继续说！

【文字】你也可以拍出这样的照片！

【互动】评论区留言你最想学的拍摄技巧，点赞关注不迷路！`;
    }
  }
}
</script>

<style scoped>
/* 页面整体样式 */
.short-video-script-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f8f9fa;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", sans-serif;
  padding: 0;
  margin-top: -40px; /* 与公众号文章页面一致 */
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 0;
  background: transparent;
  box-shadow: none;
  border-bottom: none;
  z-index: 10;
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
  width: auto;
  height: auto;
}

.action-btn:hover {
  background-color: #f5f5f5;
  color: #ba003f;
  transform: scale(1.1);
  box-shadow: 0 2px 6px rgba(186, 0, 63, 0.2);
}

/* 主容器布局 */
.main-container {
  display: flex;
  gap: 20px;
  padding: 20px 20px 0 20px;
  flex: 1;
  overflow: hidden;
}

/* 左侧输入区域 */
.input-section {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.08);
  padding: 20px;
  overflow-y: auto;
  max-width: 500px;
  min-width: 360px;
}

/* 右侧展示区域 */
.right-column {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
}

/* 公共区块样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
}

.section-title i {
  color: #ba003f;
  font-size: 18px;
}

/* 表单样式 */
.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
}

.form-group label.required::after {
  content: "*";
  color: #ba003f;
  margin-left: 4px;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s;
  background-color: #fff;
}

.form-control:focus {
  border-color: #ba003f;
  outline: none;
  box-shadow: 0 0 0 3px rgba(186, 0, 63, 0.1);
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 18px;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

/* 平台和类别卡片样式 */
.platform-category-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 12px;
  margin-top: 10px;
}

.platform-category-card {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 12px 10px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.platform-category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
  border-color: #ddd;
}

.platform-category-card.selected {
  border-color: #ba003f;
  background-color: rgba(186, 0, 63, 0.05);
}

.platform-category-icon {
  width: 36px;
  height: 36px;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 8px;
}

.platform-category-icon i {
  font-size: 18px;
  color: #ba003f;
}

.platform-category-name {
  font-size: 12px;
  font-weight: 500;
  color: #333;
}

/* 复选框组样式 */
.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  margin-top: 10px;
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 12px;
  border: 1px solid #eee;
}

.checkbox-item {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-item input[type="checkbox"] {
  margin-right: 8px;
  cursor: pointer;
}

.checkbox-item label {
  margin-bottom: 0;
  cursor: pointer;
}

/* 按钮样式 */
.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn {
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s;
  height: 40px;
}

.btn-primary {
  background-color: #ba003f;
  color: white;
  flex: 2;
}

.btn-primary:hover {
  background-color: #d4185b;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  flex: 1;
  border: 1px solid #e0e0e0;
}

.btn-secondary:hover {
  background-color: #e5e5e5;
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-button, 
.secondary-button, 
.prompt-button {
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
  height: 32px;
}

.primary-button {
  background-color: #ba003f;
  color: white;
}

.primary-button:hover {
  background-color: #d4185b;
}

.secondary-button {
  background-color: #f5f5f5;
  color: #555;
  border: 1px solid #e0e0e0;
}

.secondary-button:hover {
  background-color: #e5e5e5;
}

.prompt-button {
  background-color: transparent;
  color: #ba003f;
  border: 1px solid #ba003f;
}

.prompt-button:hover {
  background-color: rgba(186, 0, 63, 0.05);
}

.primary-button:disabled,
.secondary-button:disabled,
.prompt-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 参考案例区域 */
.examples-section {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.08);
  padding: 20px;
  position: relative;
}

.examples-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.carousel-controls {
  display: flex;
  gap: 8px;
}

.carousel-control {
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #555;
}

.carousel-control:hover:not(.disabled) {
  border-color: #ba003f;
  color: #ba003f;
  transform: scale(1.05);
}

.carousel-control.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.example-carousel {
  overflow: hidden;
  position: relative;
}

.example-cards {
  display: flex;
  gap: 15px;
  transition: transform 0.3s ease;
}

.example-card {
  flex: 0 0 auto;
  min-width: 180px;
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.2s;
}

.example-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.08);
  border-color: #ba003f;
}

.example-icon {
  width: 48px;
  height: 48px;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
}

.example-icon i {
  font-size: 22px;
  color: #ba003f;
}

.example-info {
  text-align: center;
  width: 100%;
}

.example-title {
  display: block;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.example-desc {
  display: block;
  font-size: 12px;
  color: #666;
}

/* 结果区域 */
.result-section {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.08);
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.result-content-wrapper {
  flex: 1;
  position: relative;
  overflow: auto;
  border: 1px solid #eee;
  border-radius: 6px;
  background-color: #fcfcfc;
}

.script-result {
  padding: 20px;
  transition: all 0.2s;
}

.blur-content {
  filter: blur(2px);
  pointer-events: none;
}

.script-content {
  line-height: 1.6;
  color: #333;
  font-size: 14px;
}

.script-content h1 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.script-content h2 {
  font-size: 18px;
  color: #444;
  margin: 20px 0 10px;
}

.script-content h3 {
  font-size: 16px;
  color: #ba003f;
  margin: 16px 0 10px;
  padding-left: 10px;
  border-left: 3px solid #ba003f;
}

.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 30px;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-image {
  width: 110px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-message {
  color: #999;
  font-size: 14px;
}

/* 加载动画 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 5;
}

.loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(186, 0, 63, 0.2);
  border-radius: 50%;
  border-top-color: #ba003f;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

.loading-text {
  color: #666;
  font-size: 14px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinning {
  animation: spin 1s linear infinite;
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
  width: 90%;
  max-width: 600px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  max-height: 80vh;
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
  color: #ba003f;
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

.prompt-modal .modal-body {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.prompt-content {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  overflow: auto;
  max-height: 50vh;
  border: 1px solid #eee;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  white-space: pre-line;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
}

/* 脚本内容样式 */
.scene-desc, .dialogue, .text-overlay, .shot, .music, .cta {
  margin-bottom: 10px;
  padding: 10px 12px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}

.scene-desc {
  background-color: #f5f5f5;
  border-left: 3px solid #999;
}

.dialogue {
  background-color: #e8f4ff;
  border-left: 3px solid #4a90e2;
}

.text-overlay {
  background-color: #fff0e8;
  border-left: 3px solid #f5a623;
}

.shot {
  background-color: #f0f8e8;
  border-left: 3px solid #7ed321;
}

.music {
  background-color: #f5e8ff;
  border-left: 3px solid #9013fe;
}

.cta {
  background-color: #ffe8e8;
  border-left: 3px solid #ba003f;
}

/* 响应式样式 */
@media screen and (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section, 
  .right-column {
    max-width: none;
    width: 100%;
  }
}
</style>