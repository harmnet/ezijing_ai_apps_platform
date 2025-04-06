<template>
  <div class="xiaohongshu-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>小红书笔记生成</h2>
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
        
        <!-- 笔记类型选择 -->
        <div class="form-group">
          <label for="note-type">笔记类型</label>
          <select id="note-type" v-model="noteType" class="form-control">
            <option value="product-review">产品测评</option>
            <option value="lifestyle">生活方式</option>
            <option value="travel">旅行游记</option>
            <option value="food">美食分享</option>
            <option value="fashion">穿搭分享</option>
            <option value="beauty">美妆心得</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="note-title" class="required">笔记标题</label>
          <input 
            type="text" 
            id="note-title" 
            v-model="noteTitle" 
            placeholder="输入吸引人的标题"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="product-name">产品名称 (如适用)</label>
          <input 
            type="text" 
            id="product-name" 
            v-model="productName" 
            placeholder="输入产品名称"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="description" class="required">内容描述</label>
          <textarea 
            id="description" 
            v-model="description" 
            placeholder="描述你希望分享的内容要点..."
            class="form-control"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="writing-style">写作风格</label>
            <select id="writing-style" v-model="writingStyle" class="form-control">
              <option value="friendly">亲切友好</option>
              <option value="professional">专业分析</option>
              <option value="casual">轻松随意</option>
              <option value="enthusiastic">热情洋溢</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label for="keywords">关键词 (可选)</label>
          <input 
            type="text" 
            id="keywords" 
            v-model="keywords" 
            placeholder="逗号分隔的关键词"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label>内容元素</label>
          <div class="checkbox-group">
            <label class="checkbox-container">
              <input type="checkbox" v-model="includeEmoji">
              <span>表情符号</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="includeRating">
              <span>评分</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="includeProsCons">
              <span>优缺点</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="includeTips">
              <span>小贴士</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="includeHashtags">
              <span>话题标签</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="includeImageDesc">
              <span>图片建议</span>
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label for="additional-requirements">其他特殊要求 (可选)</label>
          <textarea 
            id="additional-requirements" 
            v-model="additionalRequirements" 
            placeholder="如需要特定的笔记结构、风格要求等，请在此说明"
            class="form-control"
            rows="3"
          ></textarea>
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
          <button @click="generateNote" class="btn btn-primary" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '生成中...' : '生成笔记' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
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
              <button class="carousel-control prev" @click="prevExample" :disabled="currentExampleIndex <= 0" :class="{ 'disabled': currentExampleIndex <= 0 }">
                <i class="ri-arrow-left-s-line"></i>
              </button>
              <button class="carousel-control next" @click="nextExample" :disabled="!$refs.exampleCarousel || isLastPage" :class="{ 'disabled': !$refs.exampleCarousel || isLastPage }">
                <i class="ri-arrow-right-s-line"></i>
              </button>
            </div>
          </div>
          
          <div class="example-carousel">
            <div class="example-cards" ref="exampleCarousel" :style="{transform: `translateX(${exampleTranslateX}px)`}">
              <div class="example-card" v-for="(example, index) in examples" :key="index" @click="loadExample(example.id)">
                <div class="example-icon">
                  <!-- 使用固定的紫荆红色SVG图标，确保一定能显示 -->
                  <svg v-if="example.id === 'skincare1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M7 21h10V9a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v12z"></path>
                    <path d="M12 16a3 3 0 0 0 0-6"></path>
                    <path d="M8 5.5v-1C8 3.12 8.9 2 10 2h4c1.1 0 2 1.12 2 2.5v1"></path>
                  </svg>
                  <svg v-else-if="example.id === 'food1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 10h2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2h-2"></path>
                    <path d="M11 18a3 3 0 0 1-3 3H4l1-7h5l1 4"></path>
                    <path d="M7 14l7-7"></path>
                    <path d="M16 3l1.5 1.5"></path>
                    <path d="M19 6l-1.5-1.5"></path>
                    <path d="M12 8l-2-2"></path>
                  </svg>
                  <svg v-else-if="example.id === 'travel1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="4" y="8" width="16" height="12" rx="2"></rect>
                    <path d="M8 8V5c0-1.1.9-2 2-2h4a2 2 0 0 1 2 2v3"></path>
                    <line x1="12" y1="16" x2="12" y2="16"></line>
                  </svg>
                  <svg v-else-if="example.id === 'lifestyle1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 12l-8-8-8 8"></path>
                    <path d="M20 12l-8 8-8-8"></path>
                    <path d="M4 12h16"></path>
                  </svg>
                  <svg v-else-if="example.id === 'fashion1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 7l9 4-9 4"></path>
                    <path d="M21 7l-9 4 9 4"></path>
                  </svg>
                  <svg v-else-if="example.id === 'workout1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="7" r="3"></circle>
                    <line x1="8" y1="21" x2="10" y2="17"></line>
                    <line x1="16" y1="21" x2="14" y2="17"></line>
                    <path d="M8 13V7"></path>
                    <path d="M16 13V7"></path>
                    <path d="M12 21v-8"></path>
                  </svg>
                  <svg v-else-if="example.id === 'makeup1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 3l18 18"></path>
                    <path d="M9 5a5 5 0 0 0 8 6m2.007-9.003A5 5 0 0 0 12 5"></path>
                    <path d="M7 19a2 2 0 1 0 0-4"></path>
                    <path d="M12 19c1.657 0 3-1.325 3-2.959 0-1.47-1.156-2.633-2.79-2.746"></path>
                  </svg>
                  <svg v-else-if="example.id === 'book1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                  </svg>
                  <svg v-else-if="example.id === 'tech1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect>
                    <line x1="12" y1="18" x2="12.01" y2="18"></line>
                  </svg>
                  <svg v-else-if="example.id === 'diy1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                  </svg>
                </div>
                <div class="example-info">
                  <span class="example-title">{{example.title}}</span>
                  <span class="example-desc">{{example.type}}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 生成结果 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              笔记结果
            </h3>
            <div class="action-buttons">
              <button @click="generateNote" class="primary-button" :disabled="isGenerating">
                <i class="ri-refresh-line" v-if="!isGenerating"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isGenerating ? '生成中...' : '重新生成' }}
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
                <p class="empty-message">暂无笔记内容，请点击"生成笔记"按钮开始创作</p>
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
          <h3><i class="ri-lightbulb-line"></i> 创作小贴士</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>📱 吸引注意的标题 - 标题要简洁、吸引人，使用数字、emoji和问句效果更好</li>
            <li>📷 高质量图片 - 准备6-9张高质量图片，第一张最重要，要有吸引力</li>
            <li>🔍 内容结构 - 开头直接切入主题，中间详细描述体验，结尾总结或发问引导互动</li>
            <li>🏷️ 合适的话题 - 使用3-5个相关话题标签，提高内容曝光率</li>
            <li>👩‍💼 个人观点 - 分享真实的个人体验和观点，增加内容可信度</li>
            <li>❤️ 互动引导 - 结尾提出问题或邀请留言，增加互动性</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 提示词模态框 -->
    <div class="modal" v-if="showPromptModal">
      <div class="modal-content prompt-modal">
        <div class="modal-header">
          <h3><i class="ri-file-text-line"></i> 生成提示词</h3>
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
  name: 'XiaohongshuArticle',
  data() {
    return {
      // 表单数据
      noteType: 'product-review',
      noteTitle: '',
      productName: '',
      description: '',
      writingStyle: 'friendly',
      keywords: '',
      additionalRequirements: '',
      
      // 内容元素选项
      includeEmoji: true,
      includeRating: true,
      includeProsCons: true,
      includeTips: false,
      includeHashtags: true,
      includeImageDesc: true,
      
      // 结果内容
      isGenerating: false,
      loadingText: '正在生成笔记内容，请耐心等待...',
      generatedNote: '',
      lastUsedPrompt: null,
      
      // 模态框控制
      showTipsModal: false,
      showPromptModal: false,
      
      // 模型选择 - 默认使用火山引擎V3
      selectedModel: 'deepseek-v3-vol',
      modelList: [],
      
      // 轮播控制
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      
      // 示例数据
      examples: [
        { id: 'skincare1', title: '这款面霜真的绝了', type: '护肤测评', icon: 'ri-lotion-line' },
        { id: 'food1', title: '隐藏在巷子里的神级小吃', type: '美食探店', icon: 'ri-restaurant-line' },
        { id: 'travel1', title: '三亚度假攻略', type: '旅游攻略', icon: 'ri-suitcase-line' },
        { id: 'lifestyle1', title: '提升生活品质的10个小物件', type: '好物分享', icon: 'ri-gift-line' },
        { id: 'fashion1', title: '春季穿搭指南', type: '穿搭分享', icon: 'ri-t-shirt-line' },
        { id: 'workout1', title: '15分钟居家燃脂运动', type: '健身分享', icon: 'ri-run-line' },
        { id: 'makeup1', title: '日常妆容分享', type: '美妆教程', icon: 'ri-paint-brush-line' },
        { id: 'book1', title: '这本书改变了我的思考方式', type: '读书笔记', icon: 'ri-book-open-line' },
        { id: 'tech1', title: '最新数码产品测评', type: '数码科技', icon: 'ri-smartphone-line' },
        { id: 'diy1', title: '超简单的家居DIY改造', type: 'DIY手工', icon: 'ri-tools-line' }
      ],
      
      // 示例数据模板
      exampleData: {
        'skincare1': {
          noteType: 'product-review',
          noteTitle: '这款面霜真的绝了！敏感肌救星✨',
          productName: 'XXX舒缓修复面霜',
          description: '适合敏感肌和干燥肌肤的保湿面霜，质地轻薄但很滋润，使用后皮肤屏障有明显改善',
          writingStyle: 'enthusiastic',
          includeEmoji: true,
          includeRating: true,
          includeProsCons: true
        },
        'food1': {
          noteType: 'food',
          noteTitle: '隐藏在巷子里的神级小吃！排队两小时值得吗？',
          description: '探访藏在老城区小巷里的网红美食店，特色小吃和招牌菜品的味道体验',
          writingStyle: 'humorous',
          includeEmoji: true,
          includeRating: true,
          includeHashtags: true,
          includeImageDesc: true
        },
        'travel1': {
          noteType: 'travel',
          noteTitle: '三亚度假攻略｜看这一篇就够了',
          description: '三亚三天两晚深度游攻略，包含景点、酒店、美食推荐和实用小贴士',
          writingStyle: 'informative',
          includeEmoji: true,
          includeProsCons: false,
          includeHashtags: true,
          includeTips: true,
          includeImageDesc: true
        },
        'lifestyle1': {
          noteType: 'lifestyle',
          noteTitle: '提升生活品质的10个小物件',
          description: '分享近期入手的提升生活品质和幸福感的小物件，包括厨房用品和居家好物',
          writingStyle: 'friendly',
          includeEmoji: true,
          includeHashtags: true,
          includeImageDesc: true
        },
        'fashion1': {
          noteType: 'fashion',
          noteTitle: '春季穿搭指南｜5套百搭Look',
          description: '适合春季的5套日常穿搭分享，包含单品推荐和搭配技巧',
          writingStyle: 'enthusiastic',
          includeEmoji: true,
          includeHashtags: true,
          includeImageDesc: true
        },
        'workout1': {
          noteType: 'lifestyle',
          noteTitle: '15分钟居家燃脂运动｜无需器械',
          description: '适合没有健身器材的居家运动方案，每天15分钟高效燃脂',
          writingStyle: 'professional',
          includeEmoji: true,
          includeTips: true,
          includeHashtags: true
        },
        'makeup1': {
          noteType: 'lifestyle',
          noteTitle: '上班族日常妆容分享｜5分钟搞定',
          description: '适合职场女性的快速日常妆容教程，突出重点部位，提升精神面貌',
          writingStyle: 'friendly',
          includeEmoji: true,
          includeHashtags: true,
          includeImageDesc: true
        },
        'book1': {
          noteType: 'lifestyle',
          noteTitle: '这本书改变了我的思考方式｜读书笔记',
          description: '分享一本关于心理学的书籍读后感，以及对日常生活的启发和应用',
          writingStyle: 'informative',
          includeEmoji: true,
          includeHashtags: true,
          includeProsCons: false
        },
        'tech1': {
          noteType: 'product-review',
          noteTitle: '最新旗舰手机深度测评｜值不值得买？',
          productName: 'XX旗舰手机',
          description: '全面测试新款旗舰手机的性能、拍照、续航等关键特性，帮助你决定是否值得购买',
          writingStyle: 'professional',
          includeEmoji: true,
          includeRating: true,
          includeProsCons: true,
          includeHashtags: true
        },
        'diy1': {
          noteType: 'lifestyle',
          noteTitle: '超简单的家居DIY改造｜旧物改造新生',
          description: '用简单的材料和工具，将家中的旧物改造成实用又美观的装饰品',
          writingStyle: 'friendly',
          includeEmoji: true,
          includeHashtags: true,
          includeImageDesc: true,
          includeTips: true
        }
      }
    };
  },
  mounted() {
    // 获取模型列表
    this.fetchModels();
    
    // 确保默认选择火山引擎的DeepSeek V3模型
    if (!this.selectedModel || this.selectedModel === '') {
      this.selectedModel = 'deepseek-v3-vol';
    }
    
    console.log('默认选择模型:', this.selectedModel);
  },
  computed: {
    isLastPage() {
      if (!this.$refs.exampleCarousel) return true;
      const cardWidth = 215; // 卡片宽度+间距
      const containerWidth = this.$refs.exampleCarousel.parentElement.clientWidth;
      const totalWidth = this.examples.length * cardWidth;
      const maxScrollX = totalWidth - containerWidth;
      
      // 当滚动到最大滚动距离的90%以上时，认为是最后一页
      return Math.abs(this.exampleTranslateX) >= maxScrollX * 0.9;
    }
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
          
          // 如果未设置模型或列表中有火山引擎V3模型，则默认选择它
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
          this.selectedModel = 'deepseek-v3-vol';
        }
      } catch (error) {
        console.error('获取模型列表异常:', error);
        // 设置默认值
        this.selectedModel = 'deepseek-v3-vol';
      }
    },
    
    // 生成笔记
    async generateNote() {
      if (this.isGenerating) return;
      
      this.isGenerating = true;
      this.loadingText = '正在生成笔记内容，请耐心等待...';
      
      try {
        // 确保选择了火山引擎V3模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3-vol';
          console.log('未选择模型，已自动选择火山引擎V3模型');
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
            this.generatedNote = content;
          } else {
            console.error('无法从响应中提取内容:', response.data);
            this.generatedNote = '抱歉，生成内容时出现错误，请重试。';
            
            // 开发模式下使用示例内容
            if (process.env.NODE_ENV === 'development') {
              this.generatedNote = this.getDemoContent();
              console.log('开发模式：使用示例内容');
            }
          }
        } else {
          console.error('生成内容失败:', response.data?.message || '未知错误');
          alert('生成内容失败: ' + (response.data?.message || '请重试'));
          
          // 开发模式下使用示例内容
          if (process.env.NODE_ENV === 'development') {
            this.generatedNote = this.getDemoContent();
            console.log('开发模式：使用示例内容');
          } else {
            this.generatedNote = '抱歉，生成内容时出现错误，请重试。';
          }
        }
      } catch (error) {
        console.error('生成笔记异常:', error);
        alert('生成内容异常: ' + (error.message || '请重试'));
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          this.generatedNote = this.getDemoContent();
          console.log('开发模式：使用示例内容');
        } else {
          this.generatedNote = '抱歉，生成内容时出现错误，请重试。';
        }
      } finally {
        this.isGenerating = false;
      }
    },
    
    // 构建提示词
    buildPrompt() {
      console.log('构建小红书笔记生成提示词');
      
      // 获取笔记类型的中文名称
      const getNoteTypeName = () => {
        const typeMap = {
          'product-review': '产品测评',
          'lifestyle': '生活方式',
          'travel': '旅行游记',
          'food': '美食探店',
          'fashion': '穿搭分享'
        };
        return typeMap[this.noteType] || '产品测评';
      };
      
      // 获取风格的中文名称
      const getStyleName = () => {
        const styleMap = {
          'friendly': '亲切友好',
          'professional': '专业严谨',
          'enthusiastic': '热情洋溢',
          'humorous': '幽默风趣',
          'informative': '信息丰富'
        };
        return styleMap[this.writingStyle] || '亲切友好';
      };
      
      // 获取选中的内容元素
      const getSelectedElements = () => {
        const elements = [];
        if (this.includeEmoji) elements.push('表情符号');
        if (this.includeRating) elements.push('评分');
        if (this.includeProsCons) elements.push('优缺点');
        if (this.includeTips) elements.push('小贴士');
        if (this.includeHashtags) elements.push('话题标签');
        if (this.includeImageDesc) elements.push('图片建议');
        return elements.join('、');
      };
      
      // 构建系统提示词
      const systemPrompt = `你是一位专业的小红书内容创作者，精通各种类型小红书笔记的创作，包括产品测评、美食探店、旅行分享等。请根据用户提供的信息，创作一篇吸引人的小红书笔记。`;
      
      // 构建用户提示词
      let prompt = `请帮我创作一篇类型为【${getNoteTypeName()}】的小红书笔记：\n\n`;
      prompt += `笔记类型：${getNoteTypeName()}\n`;
      prompt += `笔记标题/主题：${this.noteTitle}\n`;
      if (this.noteType === 'product-review' && this.productName) {
        prompt += `产品名称：${this.productName}\n`;
      }
      prompt += `内容描述：${this.description}\n`;
      prompt += `写作风格：${getStyleName()}\n`;
      if (this.keywords) {
        prompt += `关键词：${this.keywords}\n`;
      }
      prompt += `包含元素：${getSelectedElements()}\n`;
      if (this.additionalRequirements) {
        prompt += `额外要求：${this.additionalRequirements}\n`;
      }
      
      // 构建完整消息
      const messages = [
        { role: "system", content: systemPrompt },
        { role: "user", content: prompt }
      ];
      
      console.log('生成提示词:', messages);
      return messages;
    },
    
    // 获取示例内容（仅开发模式使用）
    getDemoContent() {
      return `# ${this.noteTitle || '这款面霜真的绝了！'}

${this.productName || '熬夜星人'}的福音来啦！😍 这款补水面霜简直是我的救星！

⭐⭐⭐⭐⭐ 满分推荐！

👍 优点：
- 质地轻薄，吸收超快
- 保湿效果持久，不油腻
- 温和不刺激，敏感肌也能用

👎 缺点：
- 价格稍贵（但绝对值得！）
- 限量版包装容易断货

💡 使用小贴士：
睡前厚涂一层，第二天起床皮肤水嫩得像剥了壳的鸡蛋🥚

实测连续用了一周，皮肤状态明显改善，连闺蜜都问我最近用了什么护肤品～

#熬夜必备 #敏感肌友好 #面霜推荐 #护肤好物分享 #平价好物`;
    },
    
    // 重置表单
    resetForm() {
      this.noteType = 'product-review';
      this.noteTitle = '';
      this.productName = '';
      this.description = '';
      this.writingStyle = 'friendly';
      this.keywords = '';
      this.additionalRequirements = '';
      
      this.includeEmoji = true;
      this.includeRating = true;
      this.includeProsCons = true;
      this.includeTips = false;
      this.includeHashtags = true;
      this.includeImageDesc = true;
      
      this.generatedNote = '';
    },
    
    // 显示创作小贴士
    showTips() {
      this.showTipsModal = true;
    },
    
    // 复制生成的文本
    copyText() {
      const textToCopy = this.generatedNote;
      if (!textToCopy) return;
      
      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          alert('内容已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          alert('复制失败，请手动选择并复制');
        });
    },
    
    // 显示提示词模态框
    showPrompt() {
      if (this.lastUsedPrompt) {
        console.log('显示提示词模态框');
        this.showPromptModal = true;
      } else {
        alert('请先生成笔记以查看提示词');
      }
    },
    
    // 复制提示词到剪贴板
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      
      const promptText = this.lastUsedPrompt
        .map(msg => `【${msg.role === 'system' ? '系统提示词' : '用户提示词'}】\n${msg.content}`)
        .join('\n\n');
        
      navigator.clipboard.writeText(promptText)
        .then(() => {
          alert('提示词已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
        });
    },
    
    // 下载生成的文本
    downloadText() {
      if (!this.generatedNote) return;
      
      const element = document.createElement('a');
      const file = new Blob([this.generatedNote], {type: 'text/plain'});
      element.href = URL.createObjectURL(file);
      element.download = `小红书笔记_${this.noteTitle || '未命名'}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    
    // 前一个示例
    prevExample() {
      if (this.currentExampleIndex <= 0) return;
      
      const cardWidth = 215; // 卡片宽度+间距
      const visibleCards = Math.floor(this.$refs.exampleCarousel.parentElement.clientWidth / cardWidth);
      
      this.currentExampleIndex -= visibleCards;
      if (this.currentExampleIndex < 0) this.currentExampleIndex = 0;
      
      this.exampleTranslateX = -(this.currentExampleIndex * cardWidth);
      console.log('前一个示例', this.currentExampleIndex, this.exampleTranslateX);
    },
    
    // 后一个示例
    nextExample() {
      if (!this.$refs.exampleCarousel) return;
      
      const cardWidth = 215; // 卡片宽度+间距
      const containerWidth = this.$refs.exampleCarousel.parentElement.clientWidth;
      const visibleCards = Math.floor(containerWidth / cardWidth);
      const maxIndex = this.examples.length - visibleCards;
      
      if (this.currentExampleIndex >= maxIndex) return;
      
      this.currentExampleIndex += visibleCards;
      if (this.currentExampleIndex > maxIndex) this.currentExampleIndex = maxIndex;
      
      this.exampleTranslateX = -(this.currentExampleIndex * cardWidth);
      console.log('后一个示例', this.currentExampleIndex, this.exampleTranslateX);
    },
    
    // 加载示例数据
    loadExample(exampleId) {
      const example = this.exampleData[exampleId];
      if (!example) {
        console.warn(`未找到示例ID: ${exampleId} 的数据`);
        return;
      }
      
      console.log(`加载示例: ${exampleId}`, example);
      
      // 清空现有数据
      this.resetForm();
      
      // 填充表单数据
      Object.keys(example).forEach(key => {
        if (this[key] !== undefined) {
          this[key] = example[key];
        }
      });
      
      // 特别处理产品名称，确保正确设置
      if (example.noteType === 'product-review' && example.productName) {
        this.productName = example.productName;
        console.log('设置产品名称:', this.productName);
      }
      
      // 滚动到表单顶部
      const formElement = document.querySelector('.input-section');
      if (formElement) {
        formElement.scrollTop = 0;
      }
    }
  }
};
</script>

<style scoped>
.xiaohongshu-article-page {
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
  gap: 12px;
  margin-top: 10px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  padding: 8px 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
  position: relative;
}

.checkbox-container:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.06);
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
  border: 1px solid #ddd;
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
  top: 3px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
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
  min-height: 300px;
  padding: 15px;
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
</style> 