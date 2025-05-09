<template>
  <div class="livestream-script-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>直播脚本生成</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showTips">
          <i class="ri-book-open-line"></i>
          <span>知识学习</span>
        </button>
      </div>
    </div>
    
    <!-- 主要内容区域 - 使用两列布局 -->
    <div class="main-container">
      <!-- 左侧：输入参数 -->
      <div class="input-section content-card">
        <div class="section-header">
          <h3 class="section-title content-section-title">
            <i class="section-icon ri-settings-3-line"></i>
            <span>输入参数</span>
          </h3>
        </div>
        
        <!-- 目标平台选择 -->
        <div class="form-group">
          <label>直播平台</label>
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
        
        <!-- 直播类型选择 -->
        <div class="form-group">
          <label>直播类型</label>
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
          <label for="video-topic" class="required">直播主题/内容</label>
          <textarea 
            id="video-topic" 
            v-model="videoTopic" 
            class="form-control" 
            rows="3" 
            placeholder="描述您的直播主题或内容要点"
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
            <label for="keywords" class="required">内容要点/关键词</label>
            <input 
              type="text" 
              id="keywords" 
              v-model="keywords" 
              class="form-control" 
              placeholder="用逗号分隔多个关键词或内容要点"
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="style">主播风格</label>
            <select id="style" v-model="style" class="form-control">
              <option value="热情活力">热情活力 - 充满激情的表达</option>
              <option value="专业知识型">专业知识型 - 权威且详细</option>
              <option value="轻松对话型">轻松对话型 - 亲切自然</option>
              <option value="幽默风趣">幽默风趣 - 诙谐有趣</option>
              <option value="魅力型">魅力型 - 有感染力的表现</option>
            </select>
          </div>
          <div class="form-group">
            <label for="duration">直播时长</label>
            <select id="duration" v-model="duration" class="form-control">
              <option value="30分钟内">30分钟内 - 短时段</option>
              <option value="30-90分钟">30-90分钟 - 中等时长</option>
              <option value="1.5-3小时">1.5-3小时 - 长时段</option>
              <option value="3小时以上">3小时以上 - 超长直播</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label>脚本元素</label>
          <div class="checkbox-group">
            <div class="checkbox-item" :class="{'checkbox-active': includeOpening}">
              <input type="checkbox" id="includeOpening" v-model="includeOpening">
              <label for="includeOpening" class="checkbox-label">开场白</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeIntro}">
              <input type="checkbox" id="includeIntro" v-model="includeIntro">
              <label for="includeIntro" class="checkbox-label">自我介绍</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeSegmentTransitions}">
              <input type="checkbox" id="includeSegmentTransitions" v-model="includeSegmentTransitions">
              <label for="includeSegmentTransitions" class="checkbox-label">环节过渡</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeAudienceInteraction}">
              <input type="checkbox" id="includeAudienceInteraction" v-model="includeAudienceInteraction">
              <label for="includeAudienceInteraction" class="checkbox-label">观众互动话术</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeQaResponses}">
              <input type="checkbox" id="includeQaResponses" v-model="includeQaResponses">
              <label for="includeQaResponses" class="checkbox-label">常见问题回应</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includePromotions}">
              <input type="checkbox" id="includePromotions" v-model="includePromotions">
              <label for="includePromotions" class="checkbox-label">促销/购买引导</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeClosing}">
              <input type="checkbox" id="includeClosing" v-model="includeClosing">
              <label for="includeClosing" class="checkbox-label">结束语</label>
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
            {{ isGenerating ? '正在生成...' : '生成直播脚本' }}
          </button>
          <button class="btn btn-secondary" @click="resetForm">
            <i class="ri-refresh-line"></i> 重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：参考案例和结果 -->
      <div class="right-column">
        <!-- 参考案例部分 -->
        <div class="examples-section content-card">
          <div class="section-header">
            <h3 class="section-title content-section-title">
              <i class="section-icon ri-lightbulb-flash-line"></i>
              <span>参考案例</span>
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
        <div class="result-section content-card">
          <div class="section-header">
            <h3 class="section-title content-section-title">
              <i class="section-icon ri-file-text-line"></i>
              <span>直播脚本</span>
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
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无脚本内容，请点击"生成直播脚本"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedScript" class="script-result" :class="{'blur-content': isGenerating}">
              <div class="mobile-device-container">
                <div class="mobile-device" :data-platform="selectedPlatform">
                  <div class="mobile-device-frame"></div>
                  <div class="mobile-device-buttons"></div>
                  <div class="mobile-device-notch"></div>
                  <div class="mobile-device-screen-reflection"></div>
                  <div class="mobile-status-bar">
                    <div class="status-time">{{ currentTime }}</div>
                    <div class="status-icons">
                      <i class="ri-signal-wifi-fill"></i>
                      <i class="ri-signal-tower-fill"></i>
                      <i class="ri-battery-fill"></i>
                    </div>
                  </div>
                  <div class="mobile-content-area">
                    <div class="mobile-app-header">
                      <div class="platform-info">
                        <i :class="getPlatformIcon"></i>
                        <span>{{ getPlatformName }}</span>
                      </div>
                      <div class="app-actions">
                        <i class="ri-search-line"></i>
                        <i class="ri-more-2-fill"></i>
                      </div>
                    </div>
                    <div class="mobile-script-content" v-html="formattedScript"></div>
                    <div class="mobile-app-footer">
                      <div class="footer-icon">
                        <i class="ri-home-5-line"></i>
                        <span>首页</span>
                      </div>
                      <div class="footer-icon active">
                        <i class="ri-compass-3-line"></i>
                        <span>发现</span>
                      </div>
                      <div class="footer-icon">
                        <i class="ri-add-box-line"></i>
                        <span>创作</span>
                      </div>
                      <div class="footer-icon">
                        <i class="ri-message-2-line"></i>
                        <span>消息</span>
                      </div>
                      <div class="footer-icon">
                        <i class="ri-user-3-line"></i>
                        <span>我</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="mobile-device-shadow"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content knowledge-modal-content">
        <div class="modal-header">
          <h3><i class="ri-book-open-line"></i> 知识学习</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body knowledge-body">
          <div class="knowledge-sidebar">
            <div 
              v-for="(item, index) in articleKnowledge" 
              :key="index"
              class="knowledge-sidebar-item"
              :class="{ 'active': activeKnowledgeIndex === index }"
              @click="activeKnowledgeIndex = index"
            >
              <i :class="item.icon"></i>
              <span>{{ item.subtitle }}</span>
            </div>
          </div>
          <div class="knowledge-content">
            <div v-if="articleKnowledge.length > 0" class="article-knowledge-item">
              <h3 class="knowledge-title">
                <i :class="articleKnowledge[activeKnowledgeIndex].icon"></i>
                {{ articleKnowledge[activeKnowledgeIndex].subtitle }}
              </h3>
              <div class="knowledge-text" v-html="formatKnowledgeText(articleKnowledge[activeKnowledgeIndex].text)"></div>
            </div>
          </div>
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
import '@/assets/css/text-creation-common.css'
import { livestreamScriptExamples } from '@/views/example_data.js'
import { livestreamScriptKnowledge } from '@/views/Knowledge_data.js'

export default {
  name: 'LivestreamScript',
  data() {
    return {
      // 平台和类别
      platforms: [
        { id: 'douyin', name: '抖音', icon: 'ri-live-line' },
        { id: 'kuaishou', name: '快手', icon: 'ri-vidicon-line' },
        { id: 'taobao', name: '淘宝直播', icon: 'ri-shopping-basket-2-line' },
        { id: 'jd', name: '京东直播', icon: 'ri-store-2-line' },
        { id: 'bilibili', name: 'B站直播', icon: 'ri-bilibili-fill' },
        { id: 'xiaohongshu', name: '小红书直播', icon: 'ri-book-2-fill' }
      ],
      categories: [
        { id: 'shopping', name: '电商带货', icon: 'ri-shopping-cart-line' },
        { id: 'gaming', name: '游戏娱乐', icon: 'ri-gamepad-line' },
        { id: 'makeup', name: '美妆教程', icon: 'ri-palette-line' },
        { id: 'cooking', name: '美食烹饪', icon: 'ri-restaurant-line' },
        { id: 'fitness', name: '健身运动', icon: 'ri-run-line' },
        { id: 'knowledge', name: '知识分享', icon: 'ri-lightbulb-line' }
      ],
      selectedPlatform: 'douyin',
      selectedCategory: 'shopping',
      
      // 表单数据
      videoTopic: '',
      targetAudience: '',
      keywords: '',
      style: '热情活力',
      duration: '30-90分钟',
      
      // 脚本元素
      includeOpening: true,
      includeIntro: true,
      includeSegmentTransitions: true,
      includeAudienceInteraction: true, 
      includeQaResponses: false,
      includePromotions: true,
      includeClosing: true,
      
      additionalNotes: '',
      
      // 结果内容
      generatedScript: '',
      isGenerating: false,
      loadingText: '正在生成脚本内容，请耐心等待...',
      lastUsedPrompt: null,
      
      // 流式输出相关状态
      isStreaming: false,
      isLoading: false,
      isOfflineGenerated: false,
      
      // 模态框控制
      showTipsModal: false,
      showPromptModal: false,
      
      // 模型选择
      selectedModel: 'deepseek-v3',
      modelList: [],
      
      // 轮播设置
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      
      // 参考案例数据 - 从example_data.js导入
      examples: livestreamScriptExamples,
      
      // 知识学习内容 - 从Knowledge_data.js导入
      articleKnowledge: livestreamScriptKnowledge,
      
      // 知识学习模态框控制
      activeKnowledgeIndex: 0
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
      
      // 处理开场白
      formatted = formatted.replace(/【开场】(.*?)(?=\n)/g, '<div class="scene-desc"><strong>【开场】</strong>$1</div>');
      
      // 处理介绍
      formatted = formatted.replace(/【介绍】(.*?)(?=\n)/g, '<div class="dialogue"><strong>【介绍】</strong>$1</div>');
      
      // 处理过渡
      formatted = formatted.replace(/【过渡】(.*?)(?=\n)/g, '<div class="text-overlay"><strong>【过渡】</strong>$1</div>');
      
      // 处理互动
      formatted = formatted.replace(/【互动】(.*?)(?=\n)/g, '<div class="shot"><strong>【互动】</strong>$1</div>');
      
      // 处理问答
      formatted = formatted.replace(/【问答】(.*?)(?=\n)/g, '<div class="music"><strong>【问答】</strong>$1</div>');
      
      // 处理促销
      formatted = formatted.replace(/【促销】(.*?)(?=\n)/g, '<div class="cta"><strong>【促销】</strong>$1</div>');
      
      // 处理结束语
      formatted = formatted.replace(/【结束】(.*?)(?=\n)/g, '<div class="scene-desc"><strong>【结束】</strong>$1</div>');
      
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
    },
    
    // 获取平台图标
    getPlatformIcon() {
      const platform = this.platforms.find(p => p.id === this.selectedPlatform);
      return platform ? platform.icon : 'ri-live-line';
    },
    
    // 获取平台名称
    getPlatformName() {
      const platform = this.platforms.find(p => p.id === this.selectedPlatform);
      return platform ? platform.name : '抖音';
    },
    
    // 获取当前时间
    currentTime() {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`;
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
          // 获取模型列表并筛选只保留火山引擎的R1和V3大模型，以及豆包大模型
          const allModels = response.data.data || [];
          this.modelList = allModels.filter(model => 
            model.id === 'deepseek-v3-vol' || 
            model.id === 'deepseek-r1-vol' || 
            model.id === 'dongbao'
          );
          
          // 默认选择火山引擎V3模型
          const volcanoV3 = this.modelList.find(model => model.id === 'deepseek-v3-vol');
          if (volcanoV3) {
            this.selectedModel = 'deepseek-v3-vol';
          } else if (this.modelList.length > 0) {
            // 如果没有火山引擎V3模型但有其他模型，则选择第一个
            this.selectedModel = this.modelList[0].id;
          }
          
          console.log('已设置默认模型:', this.selectedModel);
          
          // 如果筛选后没有可用模型，设置默认值
          if (this.modelList.length === 0) {
            this.setupDefaultModels();
          }
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
        { id: 'dongbao', name: '豆包大模型' }
        // 注释掉其他模型选项
        // { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        // { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        // { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
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
      this.style = '热情活力';
      this.duration = '30-90分钟';
      this.includeOpening = true;
      this.includeIntro = true;
      this.includeSegmentTransitions = true;
      this.includeAudienceInteraction = true;
      this.includeQaResponses = false;
      this.includePromotions = true;
      this.includeClosing = true;
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
      if (this.includeOpening) elements.push('开场白');
      if (this.includeIntro) elements.push('自我介绍');
      if (this.includeSegmentTransitions) elements.push('环节过渡');
      if (this.includeAudienceInteraction) elements.push('观众互动话术');
      if (this.includeQaResponses) elements.push('常见问题回应');
      if (this.includePromotions) elements.push('促销/购买引导');
      if (this.includeClosing) elements.push('结束语');
      return elements.join('、');
    },
    
    // 构建提示词
    buildPrompt() {
      const platformName = this.platforms.find(p => p.id === this.selectedPlatform)?.name || '抖音';
      const categoryName = this.categories.find(c => c.id === this.selectedCategory)?.name || '电商带货';
      
      // 获取已选择的元素
      const selectedElements = this.getSelectedElements();
      
      // 构建系统消息内容
      const systemContent = `你是一位专业的直播脚本策划师，熟悉各大直播平台的内容特点和受众喜好。请根据用户提供的信息，创建一个适合${platformName}平台的${categoryName}类直播脚本。脚本应该符合平台特色、直播类型要求，并且能够有效吸引目标受众。`;
      
      // 构建用户消息内容
      let userPrompt = `请为我创建一个直播脚本，具体要求如下：

直播平台：${platformName}
直播类型：${categoryName}
直播主题：${this.videoTopic || '(用户未提供具体主题)'}
目标受众：${this.targetAudience || '(用户未提供目标受众)'}
内容要点/关键词：${this.keywords || '(用户未提供关键词)'}
主播风格：${this.style}
直播时长：${this.duration}
`;

      // 添加脚本元素要求
      userPrompt += `\n需要包含的脚本元素：${selectedElements}`;
      
      // 添加附加说明
      if (this.additionalNotes) {
        userPrompt += `\n\n附加说明：${this.additionalNotes}`;
      }
      
      // 添加输出格式要求
      userPrompt += `\n\n请按照以下格式输出脚本：
1. 脚本标题（以"#"开头）
2. 直播概要（简短介绍直播内容和目的）
3. 分环节详细脚本，每个环节包含：`;
      
      // 根据选择的元素添加格式要求
      if (this.includeOpening) userPrompt += "\n   - 【开场】开场白内容";
      if (this.includeIntro) userPrompt += "\n   - 【介绍】自我介绍或主题介绍";
      if (this.includeSegmentTransitions) userPrompt += "\n   - 【过渡】环节转换的话术";
      if (this.includeAudienceInteraction) userPrompt += "\n   - 【互动】与观众互动的话术";
      if (this.includeQaResponses) userPrompt += "\n   - 【问答】常见问题的回应";
      if (this.includePromotions) userPrompt += "\n   - 【促销】产品介绍或购买引导";
      if (this.includeClosing) userPrompt += "\n   - 【结束】直播结束语";
      
      // 合并系统提示和用户提示
      const fullPrompt = `${systemContent}\n\n${userPrompt}`;
      
      console.log('完整提示词:', fullPrompt);
      
      // 返回单个字符串类型的提示词
      return fullPrompt;
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
      this.isLoading = true;
      this.loadingText = '正在生成脚本内容，请耐心等待...';
      // 清空之前的生成结果
      this.generatedScript = '';
      this.isOfflineGenerated = false;
      
      try {
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3';
        }
        
        // 将模型ID从'deepseek-v3-vol'转换为'deepseek-v3'
        let modelId = this.selectedModel;
        if (modelId === 'deepseek-v3-vol') {
          modelId = 'deepseek-v3';
        }
        
        // 构建提示词
        const prompt = this.buildPrompt();
        // 记录提示词以供查看
        this.lastUsedPrompt = [
          { role: 'system', content: '系统提示词' },
          { role: 'user', content: prompt }
        ];
        
        console.log('使用模型:', modelId);
        console.log('发送流式请求...');
        
        // 构建API请求参数
        const apiParams = {
          model: modelId,
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        // 标记为流式输出状态
        this.isStreaming = true;
        
        // 使用fetch API发送流式请求
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(apiParams)
        });
        
        console.log('收到响应, 状态码:', response.status);
        
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
                  throw new Error(parsed.error.message || '生成脚本失败');
                }
                
                // 处理火山引擎返回的delta格式数据
                if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                  const delta = parsed.choices[0].delta;
                  
                  // 处理内容增量
                  if (delta.content) {
                    // 累加收到的内容
                    this.generatedScript += delta.content;
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
        
        if (!this.generatedScript) {
          console.error('未能生成有效内容');
          this.generatedScript = '抱歉，生成内容时出现错误，请重试。';
          
          // 开发模式下使用示例内容
          if (process.env.NODE_ENV === 'development') {
            this.generatedScript = this.getDemoScript();
            console.log('开发模式：使用示例内容');
          }
        }
      } catch (error) {
        console.error('生成脚本异常:', error);
        alert('生成内容异常: ' + (error.message || '请重试'));
        
        // 结束流式状态
        this.isStreaming = false;
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          this.generatedScript = this.getDemoScript();
          console.log('开发模式：使用示例内容');
        } else {
          this.generatedScript = '抱歉，生成内容时出现错误，请重试。';
        }
      } finally {
        this.isGenerating = false;
        this.isLoading = false;
      }
    },
    
    // 获取示例脚本（仅开发模式使用）
    getDemoScript() {
      return `# ${this.videoTopic || '春季必备护肤品推荐'} - ${this.platforms.find(p => p.id === this.selectedPlatform)?.name || '抖音'}直播脚本

这是一个${this.duration}的${this.style}类型直播，针对${this.targetAudience || '美妆爱好者'}，讲解${this.videoTopic || '春季必备护肤品推荐'}。

### 直播准备

【开场】大家好！欢迎来到今天的直播间！稍等一下，我们马上就要开始今天的春季护肤品推荐啦，先到的小伙伴可以打个1，让我看看有多少人来啦~

【介绍】我是你们的美妆达人小美，每周为大家带来最新最实用的美妆护肤知识。今天我们要聊的是春季必备的几款平价好用的护肤单品，对抗换季肌肤问题！

### 主题内容部分

【过渡】感谢大家的热情参与！现在我们正式开始今天的直播内容。首先，春季护肤有三个核心要点：补水保湿、温和修护、防晒隔离。

【互动】大家现在用的是什么护肤品啊？在评论区告诉我，有没有遇到换季肌肤问题？看到留言我会一一回复！

【问答】很多小伙伴问"混合肌适合用什么保湿产品"，这个问题很好，混合肌可以选择质地轻薄的凝胶状保湿产品，我今天第二款要推荐的就非常适合。

### 产品展示环节

【促销】现在让我们来看第一款产品：XX牌清爽保湿精华。这款精华最大的特点是...（详细介绍）今天直播间价格只需要¥99，比平时优惠30元，而且买二送一，性价比超高！

【互动】想要抢购这款产品的小伙伴，可以直接点击下方链接，或者打666，我让助理给你们发优惠券！

### 结束部分

【过渡】今天我们介绍了5款春季必备护肤品，每一款都是我亲测有效的，希望能帮助大家解决换季肌肤问题。

【互动】如果你们还有任何护肤问题，可以在评论区留言，或者私信我，我都会一一回复！

【结束】感谢大家今天的观看和支持，我们下周同一时间再见，到时候我会带来夏季防晒产品大测评，千万不要错过！拜拜~`;
    },
    
    // 格式化知识文本，将markdown转为HTML
    formatKnowledgeText(text) {
      if (!text) return '';
      
      // 处理加粗文本
      let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理换行符
      formatted = formatted.replace(/\n\n/g, '</p><p>');
      formatted = formatted.replace(/\n/g, '<br>');
      
      // 包装在段落标签中
      formatted = '<p>' + formatted + '</p>';
      
      return formatted;
    }
  }
}
</script>

<style scoped>
/* 页面特有样式 - 仅保留未在text-creation-common.css中定义的样式 */
.livestream-script-page {
  margin-top: -40px; /* 与公众号文章页面一致 */
}

/* 主容器布局 - 特有样式 */
.main-container {
  padding: 20px 20px 0 20px;
}

/* 左侧输入区域 - 特有样式 */
.input-section {
  max-width: 500px;
  min-width: 360px;
}

/* 右侧展示区域 - 特有样式 */
.right-column {
  flex: 1.5;
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

/* 模型加载 */
.model-loading {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  font-size: 12px;
  margin-top: 5px;
}

/* 模型加载图标使用通用旋转动画 */
.model-loading i {
  animation: spin 1s linear infinite;
}

/* 参考案例特有样式 */
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

/* 结果展示部分的特有样式 */
.result-content-wrapper {
  border: 1px solid #eee;
  border-radius: 6px;
  background-color: #fcfcfc;
}

.script-result {
  transition: all 0.2s;
}

/* 移动设备模拟样式 - 特有 */
.mobile-device-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 360px;
  margin: 0 auto;
}

.mobile-device {
  width: 320px;
  height: 650px;
  background: white;
  border-radius: 30px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border: 12px solid #333;
  display: flex;
  flex-direction: column;
}

.mobile-device-frame {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  pointer-events: none;
  z-index: 10;
}

.mobile-device-buttons {
  position: absolute;
  top: 100px;
  right: -26px;
  width: 4px;
  height: 30px;
  background-color: #222;
  border-radius: 4px 0 0 4px;
  z-index: 10;
}

.mobile-device-buttons::before {
  content: '';
  position: absolute;
  top: -60px;
  right: 0;
  width: 4px;
  height: 50px;
  background-color: #222;
  border-radius: 4px 0 0 4px;
}

.mobile-device-buttons::after {
  content: '';
  position: absolute;
  top: 40px;
  right: 0;
  width: 4px;
  height: 50px;
  background-color: #222;
  border-radius: 4px 0 0 4px;
}

.mobile-device-notch {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 150px;
  height: 30px;
  background-color: #222;
  border-radius: 0 0 15px 15px;
  z-index: 10;
}

.mobile-device-shadow {
  position: absolute;
  bottom: -5px;
  width: 90%;
  height: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  filter: blur(10px);
  z-index: 1;
}

.mobile-device-screen-reflection {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.15), transparent 30%);
  z-index: 9;
  pointer-events: none;
}

.mobile-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  height: 30px;
  padding: 0 15px;
  font-size: 12px;
  color: #333;
  border-bottom: 1px solid #eee;
}

.status-time {
  font-weight: 600;
}

.status-icons {
  display: flex;
  gap: 5px;
}

.mobile-content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.mobile-app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
  background-color: #fff;
}

.platform-info {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
  font-size: 14px;
}

.app-actions {
  display: flex;
  gap: 10px;
  color: #555;
  font-size: 16px;
}

.mobile-script-content {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.6;
  background-color: #fafafa;
}

.mobile-script-content h1, 
.mobile-script-content h2, 
.mobile-script-content h3 {
  margin-top: 0;
  margin-bottom: 12px;
  color: #333;
}

.mobile-script-content h1 {
  font-size: 18px;
}

.mobile-script-content h2 {
  font-size: 16px;
}

.mobile-script-content h3 {
  font-size: 15px;
}

.mobile-script-content hr {
  margin: 15px 0;
  border: 0;
  border-top: 1px dashed #ddd;
}

.scene-desc, .dialogue, .text-overlay, .shot, .music, .cta {
  margin-bottom: 15px;
  padding: 8px 12px;
  border-radius: 8px;
  position: relative;
}

.scene-desc {
  background-color: #f0f0f0;
  border-left: 3px solid #999;
}

.dialogue {
  background-color: #e8f4f8;
  border-left: 3px solid #0088cc;
}

.text-overlay {
  background-color: #fff4e5;
  border-left: 3px solid #ff9500;
}

.shot {
  background-color: #f0f8e8;
  border-left: 3px solid #7ed321;
}

.music {
  background-color: #f8e8f8;
  border-left: 3px solid #cc00cc;
}

.cta {
  background-color: #ffe8e8;
  border-left: 3px solid #ff3b30;
}

.mobile-app-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-top: 1px solid #eee;
  background-color: #fff;
}

.footer-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  flex: 1;
  font-size: 12px;
  color: #666;
}

.footer-icon i {
  font-size: 18px;
}

.footer-icon.active {
  color: #ba003f;
}

/* 提示词模态框特有样式 */
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

/* 响应式调整 - 特有 */
@media (max-width: 1200px) {
  .input-section {
    max-width: 400px;
  }
}

/* 知识学习模态框样式 */
.knowledge-modal-content {
  max-width: 900px;
  width: 90%;
  max-height: 80vh;
}

.knowledge-body {
  display: flex;
  height: 70vh;
  overflow: hidden;
}

.knowledge-sidebar {
  width: 220px;
  background-color: #f8f8f8;
  border-right: 1px solid #eee;
  overflow-y: auto;
  flex-shrink: 0;
}

.knowledge-sidebar-item {
  padding: 12px 15px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.knowledge-sidebar-item i {
  color: #ba003f;
  font-size: 18px;
}

.knowledge-sidebar-item span {
  font-size: 14px;
  color: #333;
}

.knowledge-sidebar-item:hover {
  background-color: #f0f0f0;
}

.knowledge-sidebar-item.active {
  background-color: #fff;
  border-left: 3px solid #ba003f;
  color: #ba003f;
}

.knowledge-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.article-knowledge-item {
  margin-bottom: 20px;
}

.knowledge-title {
  margin-top: 0;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.knowledge-title i {
  color: #ba003f;
  font-size: 22px;
}

.knowledge-text {
  font-size: 15px;
  line-height: 1.6;
  color: #444;
}

.knowledge-text p {
  margin-bottom: 15px;
}

.knowledge-text strong {
  color: #ba003f;
  font-weight: 600;
}

/* 响应式调整 - 知识学习模态框 */
@media (max-width: 768px) {
  .knowledge-body {
    flex-direction: column;
    height: auto;
    max-height: 70vh;
  }
  
  .knowledge-sidebar {
    width: 100%;
    max-height: 30vh;
    border-right: none;
    border-bottom: 1px solid #eee;
  }
  
  .knowledge-content {
    max-height: 40vh;
  }
}
</style>