<template>
  <div class="short-video-script-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>短视频脚本生成</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showTips">
          <i class="ri-book-open-line"></i>
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
            <div class="checkbox-item" :class="{'checkbox-active': includeSceneDesc}">
              <input type="checkbox" id="includeSceneDesc" v-model="includeSceneDesc">
              <label for="includeSceneDesc" class="checkbox-label">场景描述</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeDialogue}">
              <input type="checkbox" id="includeDialogue" v-model="includeDialogue">
              <label for="includeDialogue" class="checkbox-label">对白/解说</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeTextOverlay}">
              <input type="checkbox" id="includeTextOverlay" v-model="includeTextOverlay">
              <label for="includeTextOverlay" class="checkbox-label">屏显文字</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeShots}">
              <input type="checkbox" id="includeShots" v-model="includeShots">
              <label for="includeShots" class="checkbox-label">镜头建议</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeMusic}">
              <input type="checkbox" id="includeMusic" v-model="includeMusic">
              <label for="includeMusic" class="checkbox-label">音乐/音效</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeCTA}">
              <input type="checkbox" id="includeCTA" v-model="includeCTA">
              <label for="includeCTA" class="checkbox-label">互动引导</label>
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
            <div class="example-cards" ref="exampleCarousel" :style="{ transform: `translateX(${exampleTranslateX}px)` }">
              <div 
                class="example-card" 
                v-for="(example, index) in examples" 
                :key="index" 
                @click="loadExample(example.id)"
              >
                <div class="example-card-header">
                  <div class="video-example-icon">
                  <i :class="example.icon"></i>
                </div>
                  <div class="example-title">{{ example.title }}</div>
                  <div class="example-desc">{{ example.desc }}</div>
                </div>
                <div class="example-content">
                  <div class="example-topic">{{ example.topic }}</div>
                  <div class="example-details">
                    <div class="example-detail-item">
                      <i class="ri-video-line"></i>
                      <span>{{ example.platform === 'bilibili' ? 'B站' : 
                        example.platform === 'douyin' ? '抖音' : 
                        example.platform === 'kuaishou' ? '快手' : 
                        example.platform === 'xiaohongshu' ? '小红书' : 
                        example.platform === 'wechat' ? '视频号' : '微博' }}</span>
                    </div>
                    <div class="example-detail-item">
                      <i class="ri-time-line"></i>
                      <span>{{ example.duration }}</span>
                    </div>
                  </div>
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
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无脚本内容，请点击"生成短视频脚本"按钮开始创作</p>
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
                    <div class="status-icons">
                      <i class="ri-signal-wifi-fill"></i>
                      <i class="ri-signal-tower-fill"></i>
                      <span class="time">{{ currentTime }}</span>
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
    
    <!-- 知识学习侧边栏 -->
    <el-drawer
      v-model="showTipsModal"
      title="短视频脚本创作指南"
      direction="rtl"
      size="28%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in shortVideoScriptKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
      </div>
    </el-drawer>
    
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
            {{ lastUsedPrompt }}
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
import { shortVideoScriptExamples } from '@/views/example_data.js'
import { shortVideoScriptKnowledge } from '@/views/Knowledge_data.js'
import { ElDrawer } from 'element-plus'
import '@/assets/css/text-creation-common.css'

export default {
  name: 'ShortVideoScript',
  components: {
    ElDrawer
  },
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
      isStreaming: false,
      loadingText: '正在生成脚本内容，请耐心等待...',
      lastUsedPrompt: null,
      
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
      examples: shortVideoScriptExamples,
      
      // 添加知识学习数据
      shortVideoScriptKnowledge: shortVideoScriptKnowledge
    }
  },
  
  computed: {
    // 显示当前时间
    currentTime() {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`;
    },
    
    // 格式化脚本展示
    formattedScript() {
      if (!this.generatedScript) return '';
      
      let formatted = this.generatedScript;
      
      // 替换标题格式
      formatted = formatted.replace(/^#\s(.*?)$/gm, '<div class="video-title">$1</div>');
      formatted = formatted.replace(/^##\s(.*?)$/gm, '<div class="video-subtitle">$1</div>');
      formatted = formatted.replace(/^###\s(.*?)$/gm, '<div class="video-section-title">$1</div>');
      
      // 处理分节符号
      formatted = formatted.replace(/^----*$/gm, '<div class="section-divider"></div>');
      
      // 处理场景描述
      formatted = formatted.replace(/【场景】(.*?)(?=\n)/g, '<div class="scene-desc"><span class="tag scene-tag">场景</span><span class="content">$1</span></div>');
      formatted = formatted.replace(/【场景描述】(.*?)(?=\n)/g, '<div class="scene-desc"><span class="tag scene-tag">场景</span><span class="content">$1</span></div>');
      
      // 处理对白/解说
      formatted = formatted.replace(/【解说】(.*?)(?=\n)/g, '<div class="dialogue"><span class="tag dialogue-tag">解说</span><span class="content">$1</span></div>');
      formatted = formatted.replace(/【对白】(.*?)(?=\n)/g, '<div class="dialogue"><span class="tag dialogue-tag">对白</span><span class="content">$1</span></div>');
      
      // 处理屏显文字
      formatted = formatted.replace(/【文字】(.*?)(?=\n)/g, '<div class="text-overlay"><span class="tag text-tag">文字</span><span class="content">$1</span></div>');
      formatted = formatted.replace(/【屏显】(.*?)(?=\n)/g, '<div class="text-overlay"><span class="tag text-tag">文字</span><span class="content">$1</span></div>');
      
      // 处理镜头建议
      formatted = formatted.replace(/【镜头】(.*?)(?=\n)/g, '<div class="shot"><span class="tag shot-tag">镜头</span><span class="content">$1</span></div>');
      
      // 处理音乐/音效
      formatted = formatted.replace(/【音乐】(.*?)(?=\n)/g, '<div class="music"><span class="tag music-tag">音乐</span><span class="content">$1</span></div>');
      formatted = formatted.replace(/【音效】(.*?)(?=\n)/g, '<div class="music"><span class="tag music-tag">音效</span><span class="content">$1</span></div>');
      
      // 处理互动引导
      formatted = formatted.replace(/【互动】(.*?)(?=\n)/g, '<div class="cta"><span class="tag cta-tag">互动</span><span class="content">$1</span></div>');
      formatted = formatted.replace(/【CTA】(.*?)(?=\n)/g, '<div class="cta"><span class="tag cta-tag">互动</span><span class="content">$1</span></div>');
      
      // 处理换行符
      formatted = formatted.replace(/\n\n/g, '<div class="paragraph-break"></div>');
      formatted = formatted.replace(/\n/g, '<br>');
      
      return formatted;
    },
    
    // 判断是否已经到达最后一页
    isLastPage() {
      if (!this.$refs.exampleCarousel) return false;
      
      // 计算是否已经滚动到最后一页
      const cardWidth = 225; // 卡片宽度+间距
      const containerWidth = this.$refs.exampleCarousel?.parentElement?.clientWidth || 0;
      const totalWidth = this.examples.length * cardWidth;
      const maxScrollX = Math.max(0, totalWidth - containerWidth);
      
      // 当滚动到最大滚动距离的90%以上时，认为是最后一页
      return Math.abs(this.exampleTranslateX) >= maxScrollX * 0.9;
    },
    
    // 获取平台图标
    getPlatformIcon() {
      const platform = this.platforms.find(p => p.id === this.selectedPlatform);
      return platform ? platform.icon : 'ri-music-fill';
    },
    
    // 获取平台名称
    getPlatformName() {
      const platform = this.platforms.find(p => p.id === this.selectedPlatform);
      return platform ? platform.name : '抖音';
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
        
        if (response.data && response.data.status === 'success') {
          // 获取所有模型列表
          const allModels = response.data.data || [];
          
          // 直接使用默认的火山引擎模型列表
          this.setupDefaultModels();
          
          // 从API结果中找到我们需要的模型并更新名称等信息
          for (const model of allModels) {
            if (model.id === 'deepseek-v3' || 
                model.id === 'deepseek-r1-vol' || 
                model.id === 'doubao-pro') {
              // 更新已有模型的信息
              const index = this.modelList.findIndex(m => m.id === model.id);
              if (index !== -1) {
                this.modelList[index] = model;
              }
            }
          }
          
          // 确保默认选择V3模型
          this.selectedModel = 'deepseek-v3';
        } else {
          // 设置默认值
          this.setupDefaultModels();
        }
      } catch (error) {
        // 设置默认值
        this.setupDefaultModels();
      }
    },
    
    setupDefaultModels() {
      // 确保V3模型在第一位
      this.modelList = [
        { id: 'deepseek-v3', name: 'DeepSeek-V3（火山引擎）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'doubao-pro', name: '豆包-Pro（火山引擎）' }
      ];
      this.selectedModel = 'deepseek-v3';
      
      // 打印一下当前的模型列表，用于调试
      console.log('当前模型列表:', this.modelList);
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
      textarea.value = this.lastUsedPrompt;
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
      
      const cardWidth = 225; // 卡片宽度+间距
      this.exampleTranslateX = -this.currentExampleIndex * cardWidth;
      
      // 直接通过Vue的响应式系统更新样式，不需要直接操作DOM
      // 在模板中已经通过 :style 绑定了transform
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
      
      // 构建系统消息和用户消息的组合提示词
      let prompt = `作为专业的短视频脚本策划师，请根据以下信息，创建一个适合${platformName}平台的${categoryName}类短视频脚本：

目标平台：${platformName}
视频类别：${categoryName}
视频主题：${this.videoTopic || '(用户未提供具体主题)'}
目标受众：${this.targetAudience || '(用户未提供目标受众)'}
关键词/要点：${this.keywords || '(用户未提供关键词)'}
风格基调：${this.style}
视频时长：${this.duration}
`;

      // 添加脚本元素要求
      prompt += `\n需要包含的脚本元素：${selectedElements}`;
      
      // 添加附加说明
      if (this.additionalNotes) {
        prompt += `\n\n附加说明：${this.additionalNotes}`;
      }
      
      // 添加输出格式要求
      prompt += `\n\n请按照以下格式输出脚本：
1. 脚本标题（以"#"开头）
2. 视频概要（简短介绍视频内容和目的）
3. 分场景详细脚本，每个场景包含：`;
      
      // 根据选择的元素添加格式要求
      if (this.includeSceneDesc) prompt += "\n   - 【场景】描述拍摄场景和画面";
      if (this.includeDialogue) prompt += "\n   - 【解说】或【对白】内容";
      if (this.includeTextOverlay) prompt += "\n   - 【文字】屏幕上显示的文本内容";
      if (this.includeShots) prompt += "\n   - 【镜头】镜头角度和运动建议";
      if (this.includeMusic) prompt += "\n   - 【音乐】背景音乐或音效建议";
      if (this.includeCTA) prompt += "\n   - 【互动】引导观众评论、点赞或关注的话术";
      
      console.log('完整提示词:', prompt);
      
      // 保存提示词以便之后查看
      this.lastUsedPrompt = prompt;
      
      // 返回完整的提示词
      return prompt;
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
          this.selectedModel = 'deepseek-v3';
        }
        
        // 构建提示词
        const prompt = this.buildPrompt();
        
        // 添加更详细的日志输出
        console.log('提示词类型:', typeof prompt);
        console.log('提示词长度:', prompt.length);
        console.log('提示词前100字符:', prompt.substring(0, 100));
        
        // 清空之前的生成结果
        this.generatedScript = '';
        
        // 准备API请求参数 - 注意messages格式与CopywritingGenerator.vue一致
        const messages = [{ role: 'user', content: prompt }];
        
        const apiParams = {
          model: this.selectedModel,
          messages: messages,
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        // 记录更详细的参数
        console.log('API请求参数(完整):', JSON.stringify(apiParams));
        console.log('API请求参数中messages类型:', typeof apiParams.messages);
        console.log('API请求参数中messages长度:', apiParams.messages.length);
        
        // 开始流式状态
        this.isStreaming = true;
        
        // 发送API请求，使用fetch API处理流式响应
        console.log('开始发送流式请求到:', '/api/v1/v1/deepseek_volcano/chat');
        console.log('API请求参数:', JSON.stringify(apiParams));
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
                continue;
              }
              
              try {
                const parsed = JSON.parse(data);
                
                // 处理错误消息
                if (parsed.error) {
                  console.error("API错误:", parsed.error);
                  throw new Error(parsed.error.message || '生成脚本失败');
                }
                
                console.log('解析后的数据格式:', Object.keys(parsed));
                
                // 处理火山引擎返回的delta格式数据
                if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                  const delta = parsed.choices[0].delta;
                  console.log("收到delta数据类型:", Object.keys(delta));
                  
                  // 处理内容增量
                  if (delta.content) {
                    console.log("收到内容增量:", delta.content.substring(0, 20) + "...");
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
        
      } catch (error) {
        console.error('生成短视频脚本失败:', error);
        alert('生成内容异常: ' + (error.message || '请重试'));
        this.generatedScript = '抱歉，生成内容时出现错误，请重试。';
        // 确保结束流式状态
        this.isStreaming = false;
      } finally {
        this.isGenerating = false;
      }
    },
    
    // 格式化Markdown文本
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理粗体
      let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理斜体
      formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
      
      // 处理换行
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
/* 导入通用样式 */
@import "@/assets/css/text-creation-common.css";

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

/* 参考案例卡片样式（优化后） */
.example-carousel {
  overflow: hidden;
  position: relative;
  padding: 8px 0;
}

.example-cards {
  display: flex;
  gap: 15px;
  transition: transform 0.3s ease;
  padding: 5px;
}

.example-card {
  flex: 0 0 auto;
  width: 210px;
}

.example-card-header {
  padding: 12px 16px 10px;
  position: relative;
  padding-left: 70px;
  min-height: 70px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0;
}

.video-example-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  box-shadow: 0 3px 6px rgba(186, 0, 63, 0.1);
}

.video-example-icon i {
  font-size: 22px;
  color: #ba003f;
}

.example-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 0;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.example-desc {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: -1px;
}

.example-topic {
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  position: relative;
  padding-left: 18px;
}

.example-topic:before {
  content: '';
  position: absolute;
  left: 0;
  top: 5px;
  width: 10px;
  height: 10px;
  background-color: rgba(186, 0, 63, 0.15);
  border-radius: 50%;
}

.example-topic:after {
  content: '';
  position: absolute;
  left: 3px;
  top: 8px;
  width: 4px;
  height: 4px;
  background-color: #ba003f;
  border-radius: 50%;
}

.example-content {
  padding: 10px 16px 16px;
  background-color: #f9f9f9;
  border-top: 1px dashed #eee;
}

.example-details {
  display: flex;
  gap: 12px;
}

.example-detail-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #666;
}

.example-detail-item i {
  color: #ba003f;
  font-size: 14px;
}

/* 手机设备模拟样式 */
.mobile-device-container {
  display: flex;
  justify-content: center;
  padding: 60px 20px;
  perspective: 1500px;
  position: relative;
  background: linear-gradient(135deg, #f0f4f9 0%, #d8e2ef 100%);
  border-radius: 10px;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.8), inset 0 -1px 1px rgba(0, 0, 0, 0.05);
}

.mobile-device-container:before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(186, 0, 63, 0.1) 0%, rgba(186, 0, 63, 0) 70%);
  transform: translate(-50%, -50%);
  z-index: 0;
  border-radius: 50%;
  pointer-events: none;
}

.mobile-device {
  width: 340px;
  height: 680px;
  background-color: #fff;
  border-radius: 40px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3), 0 15px 30px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 12px solid #222;
  transform: rotateX(2deg) rotateY(-2deg);
  transition: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
  animation: float 6s ease-in-out infinite;
  z-index: 2;
}

.mobile-device:after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 28px;
  box-shadow: inset 0 0 8px rgba(255, 255, 255, 0.5);
  z-index: 3;
  pointer-events: none;
}

@keyframes float {
  0% { transform: rotateX(2deg) rotateY(-2deg) translateY(0px); }
  50% { transform: rotateX(1deg) rotateY(-1deg) translateY(-12px) scale(1.01); }
  100% { transform: rotateX(2deg) rotateY(-2deg) translateY(0px); }
}

.mobile-device:hover {
  transform: rotateX(0) rotateY(0) translateY(-8px) scale(1.02);
  box-shadow: 0 35px 80px rgba(0, 0, 0, 0.35), 0 15px 40px rgba(0, 0, 0, 0.2);
  animation-play-state: paused;
}

/* 手机设备其他样式 */
.mobile-device-frame {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  border-radius: 28px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.mobile-device-buttons {
  position: absolute;
  right: -14px;
  top: 100px;
  width: 3px;
  height: 30px;
  background-color: #111;
  border-radius: 0 3px 3px 0;
  z-index: 1;
}

.mobile-device-buttons:before {
  content: '';
  position: absolute;
  right: 0;
  top: 50px;
  width: 3px;
  height: 60px;
  background-color: #111;
  border-radius: 0 3px 3px 0;
}

.mobile-device-buttons:after {
  content: '';
  position: absolute;
  left: -12px;
  top: 50px;
  width: 3px;
  height: 40px;
  background-color: #111;
  border-radius: 3px 0 0 3px;
}

.mobile-device-notch {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 150px;
  height: 28px;
  background-color: #111;
  border-radius: 0 0 16px 16px;
  z-index: 4;
}

.mobile-status-bar {
  height: 40px;
  padding: 0 15px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  background-color: #fff;
  border-bottom: 1px solid #eee;
  position: relative;
  z-index: 1;
}

.status-icons {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #333;
}

.mobile-app-header {
  height: 50px;
  padding: 0 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  border-bottom: 1px solid #eee;
}

.platform-info {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
}

.platform-info i {
  font-size: 16px;
}

.app-actions {
  display: flex;
  gap: 12px;
  color: #555;
}

.mobile-content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.mobile-script-content {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background-color: #fff;
}

.mobile-app-footer {
  height: 50px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  border-top: 1px solid #eee;
  background-color: #fff;
}

.footer-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 12px;
  color: #666;
  gap: 4px;
}

.footer-icon i {
  font-size: 18px;
}

.footer-icon.active {
  color: #ba003f;
  position: relative;
}

.footer-icon.active:after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 10px;
  height: 3px;
  background-color: #ba003f;
  border-radius: 1.5px;
}

.mobile-device-shadow {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 20px;
  background: rgba(0, 0, 0, 0.15);
  filter: blur(12px);
  border-radius: 50%;
  z-index: 1;
}

.mobile-device-screen-reflection {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0) 50%);
  z-index: 3;
  pointer-events: none;
  border-radius: 28px;
}

/* 平台特定样式 */
[data-platform="douyin"] .mobile-app-header {
  background-color: #121212;
  color: #fff;
  border-bottom: none;
}

[data-platform="douyin"] .app-actions {
  color: #eee;
}

[data-platform="douyin"] .mobile-status-bar {
  background-color: #121212;
}

[data-platform="douyin"] .mobile-script-content {
  background-color: #121212;
  color: #fff;
}

[data-platform="douyin"] .mobile-app-footer {
  background-color: #000;
  color: #fff;
  border-top: 1px solid #333;
}

[data-platform="douyin"] .scene-desc,
[data-platform="douyin"] .dialogue,
[data-platform="douyin"] .text-overlay,
[data-platform="douyin"] .shot,
[data-platform="douyin"] .music,
[data-platform="douyin"] .cta {
  background-color: #222;
  border-color: #333;
}

[data-platform="douyin"] .content {
  color: #eee;
}

[data-platform="douyin"] .footer-icon {
  color: #888;
}

[data-platform="douyin"] .footer-icon.active {
  color: #fe2c55;
}

[data-platform="douyin"] .footer-icon.active:after {
  background-color: #fe2c55;
}

[data-platform="bilibili"] .mobile-app-header {
  background-color: #fb7299;
  color: #fff;
  border-bottom: none;
  box-shadow: 0 1px 6px rgba(251, 114, 153, 0.4);
}

[data-platform="bilibili"] .video-title {
  background: linear-gradient(to right, #fb7299, #ff9eb7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

[data-platform="bilibili"] .video-title:after {
  background: linear-gradient(to right, #fb7299, #ff9eb7);
}

[data-platform="bilibili"] .footer-icon.active {
  color: #23ade5;
}

[data-platform="bilibili"] .footer-icon.active:after {
  background-color: #23ade5;
}

[data-platform="xiaohongshu"] .mobile-app-header {
  background-color: #fff;
  color: #333;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

[data-platform="xiaohongshu"] .platform-info {
  font-weight: 700;
}

[data-platform="xiaohongshu"] .platform-info i {
  color: #fe2c55;
}

[data-platform="xiaohongshu"] .mobile-script-content {
  background-color: #fafafa;
  padding-top: 20px;
}

[data-platform="xiaohongshu"] .video-title {
  background: linear-gradient(to right, #fe2c55, #ff6c79);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

[data-platform="xiaohongshu"] .video-title:after {
  background: linear-gradient(to right, #fe2c55, #ff6c79);
}

[data-platform="xiaohongshu"] .footer-icon.active {
  color: #fe2c55;
}

[data-platform="xiaohongshu"] .footer-icon.active:after {
  background-color: #fe2c55;
}

[data-platform="kuaishou"] .mobile-app-header {
  background-color: #fff;
  border-bottom: 1px solid #eee;
}

[data-platform="kuaishou"] .platform-info i {
  color: #00c1de;
}

[data-platform="kuaishou"] .mobile-script-content {
  background-color: #f9f9f9;
}

[data-platform="kuaishou"] .footer-icon.active {
  color: #00c1de;
}

[data-platform="kuaishou"] .footer-icon.active:after {
  background-color: #00c1de;
}

[data-platform="wechat"] .mobile-app-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid #eee;
}

[data-platform="wechat"] .platform-info i {
  color: #07c160;
}

[data-platform="wechat"] .footer-icon.active {
  color: #07c160;
}

[data-platform="wechat"] .footer-icon.active:after {
  background-color: #07c160;
}

[data-platform="weibo"] .mobile-app-header {
  background-color: #fff;
  border-bottom: 1px solid #eee;
}

[data-platform="weibo"] .platform-info i {
  color: #e6162d;
}

[data-platform="weibo"] .footer-icon.active {
  color: #e6162d;
}

[data-platform="weibo"] .footer-icon.active:after {
  background-color: #e6162d;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .mobile-device {
    width: 300px;
    height: 600px;
    border-width: 8px;
  }
  
  .mobile-device-notch {
    width: 100px;
    height: 20px;
  }
}

/* 脚本结果样式 */
.script-result {
  padding: 0;
  transition: all 0.2s;
  background-color: #f5f7fa;
  border-radius: 10px;
  overflow: hidden;
}

.blur-content {
  pointer-events: none;
}

.script-content {
  line-height: 1.6;
  color: #333;
  font-size: 14px;
}

/* 输出内容结构样式 */
.scene-desc, .dialogue, .text-overlay, .shot, .music, .cta {
  margin-bottom: 10px;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #eee;
  background-color: #f9f9f9;
}

.scene-head, .dialogue-head, .overlay-head, .shot-head, .music-head, .cta-head {
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 14px;
  color: #555;
}

.content {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.scene-desc .content {
  font-style: italic;
  color: #666;
}

.text-overlay .content {
  font-weight: 500;
}

.video-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 18px;
  padding-bottom: 8px;
  position: relative;
  color: #333;
}

.video-title:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background-color: #ba003f;
  border-radius: 1.5px;
}

/* 模态框样式 */
.prompt-content {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 6px;
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 13px;
  overflow-x: auto;
  max-height: 60vh;
  color: #333;
}

.prompt-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.tips-list {
  padding-left: 20px;
  margin: 0;
}

.tips-list li {
  margin-bottom: 12px;
  color: #555;
}

/* 模型选择样式 */
.model-loading {
  margin-top: 8px;
  font-size: 13px;
  color: #888;
  display: flex;
  align-items: center;
  gap: 6px;
}

.model-loading i {
  animation: spin 1s linear infinite;
}

.knowledge-drawer :deep(.el-drawer__header) {
  padding: 16px 20px;
  margin-bottom: 0;
  font-size: 18px;
  border-bottom: 1px solid #e6e6e6;
}

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