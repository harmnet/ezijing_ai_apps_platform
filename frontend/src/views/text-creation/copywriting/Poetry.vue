<template>
  <div class="longform-article-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>诗歌创作</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showKnowledge">
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
        
        <!-- 诗歌类型选择 -->
        <div class="form-group">
          <label for="note-type">诗歌类型</label>
          <select id="note-type" v-model="noteType" class="form-control">
            <option value="modern-poem">现代诗</option>
            <option value="classical-poem">古典诗</option>
            <option value="free-verse">自由诗</option>
            <option value="song-ci">宋词</option>
            <option value="tang-poem">唐诗</option>
            <option value="haiku">俳句</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="note-title" class="required">诗歌主题</label>
          <input 
            type="text" 
            id="note-title" 
            v-model="noteTitle" 
            placeholder="输入诗歌主题"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="target-audience">风格倾向</label>
          <select id="target-audience" v-model="targetAudience" class="form-control">
            <option value="romantic">浪漫抒情</option>
            <option value="philosophical">哲理思考</option>
            <option value="narrative">叙事描写</option>
            <option value="landscape">山水田园</option>
            <option value="emotional">情感表达</option>
            <option value="historical">历史怀古</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="description">背景/情景</label>
          <textarea 
            id="description" 
            v-model="description" 
            placeholder="描述诗歌的创作背景或情景..."
            class="form-control"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="keywords">关键词</label>
          <input 
            type="text" 
            id="keywords" 
            v-model="keywords" 
            placeholder="逗号分隔的关键词"
            class="form-control"
          />
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
          <button @click="generateLongform" class="primary-button" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '生成中...' : '创作诗歌' }}
          </button>
          <button @click="resetForm" class="secondary-button">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：参考案例和结果 -->
      <div class="right-column">
        <!-- 参考案例部分 -->
        <div class="examples-section">
          <div class="section-header">
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
                <div class="example-card-header">
                  <div class="example-icon">
                    <!-- 使用固定的紫荆红色SVG图标，确保一定能显示 -->
                    <svg v-if="example.id === 'modern1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 现代诗图标 -->
                      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                    <svg v-else-if="example.id === 'classical1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 古典诗图标 -->
                      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
                    </svg>
                    <svg v-else-if="example.id === 'free1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 自由诗图标 -->
                      <path d="M10.5 21.5V.5"></path>
                      <path d="M5.5 13.5c7-2 10-6 10-13"></path>
                      <path d="M5.5 18.5c6.3-1.7 9-5.5 9.5-9.5"></path>
                    </svg>
                    <svg v-else-if="example.id === 'song1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 宋词图标 -->
                      <path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3H6a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3h12a3 3 0 0 0 3-3 3 3 0 0 0-3-3z"></path>
                    </svg>
                    <svg v-else-if="example.id === 'tang1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 唐诗图标 -->
                      <path d="M12 8L7 13M12 8L17 13M12 8V20M4 19V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14"></path>
                      <path d="M3 19h18"></path>
                    </svg>
                    <svg v-else-if="example.id === 'haiku1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 俳句图标 -->
                      <path d="M6 20h0a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h0"></path>
                      <path d="M8 2v4"></path>
                      <path d="M16 2v4"></path>
                      <path d="M8 10h8"></path>
                      <path d="M8 14h4"></path>
                    </svg>
                    <svg v-else-if="example.id === 'landscape1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 山水图标 -->
                      <path d="m8 3 4 8 5-5 5 15H2L8 3z"></path>
                    </svg>
                    <svg v-else-if="example.id === 'love1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 爱情图标 -->
                      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
                    </svg>
                    <svg v-else-if="example.id === 'philosophical1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 哲理图标 -->
                      <path d="M2 12h5M9 12h5M16 12h5"></path>
                      <path d="M12 2v20"></path>
                      <path d="M8 17a5 5 0 1 0 8 0"></path>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <!-- 默认诗歌图标 -->
                      <path d="M12 2L22 8.5V15.5L12 22L2 15.5V8.5L12 2Z"></path>
                      <path d="M12 22V15.5"></path>
                      <path d="M22 8.5L12 15.5L2 8.5"></path>
                      <path d="M12 2V8.5"></path>
                      <path d="M12 15.5L17 18.5"></path>
                      <path d="M7 11.5L12 8.5"></path>
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
        </div>
        
        <!-- 生成结果 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              生成结果
            </h3>
            <div class="action-buttons">
              <button @click="generateLongform" class="primary-button" :disabled="isGenerating">
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
          
          <!-- 加载动画 -->
          <div v-if="isGenerating" class="loading-overlay">
            <div class="loading-spinner"></div>
            <div class="loading-text">{{ loadingText }}</div>
          </div>
          
          <!-- 无内容状态 -->
          <div v-if="!generatedNote && !isGenerating" class="empty-result">
            <div class="empty-content">
              <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
              <p class="empty-message">暂无诗歌内容，请点击"创作诗歌"按钮开始创作</p>
            </div>
          </div>
          
          <!-- 有内容状态 - 直接显示诗歌，移除多余嵌套 -->
          <div v-else-if="generatedNote" :class="{'blur-content': isGenerating}" class="poem-container">
            <div class="poem-wrapper" :class="noteType">
              <div class="poem-title">{{ extractPoemTitle() }}</div>
              <div class="poem-content" v-html="formattedPoemContent()"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 知识学习侧边栏 -->
    <el-drawer
      v-model="showKnowledgeModal"
      title="诗词创作知识"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in poetryKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
      </div>
    </el-drawer>

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
import { poetryKnowledge } from '@/views/Knowledge_data.js';  // 导入诗词创作知识数据
import { ElDrawer } from 'element-plus';  // 导入Element Plus的Drawer组件

export default {
  name: 'Poetry',
  components: {
    ElDrawer  // 注册组件
  },
  data() {
    return {
      // 表单数据
      noteType: 'modern-poem',
      noteTitle: '',
      targetAudience: 'romantic',
      description: '',
      keywords: '',
      
      // 结果内容
      isGenerating: false,
      loadingText: '正在创作诗歌，请耐心等待...',
      generatedNote: '',
      lastUsedPrompt: null,
      
      // 模态框控制
      showKnowledgeModal: false,
      showPromptModal: false,
      
      // 模型选择 - 默认使用火山引擎V3
      selectedModel: 'deepseek-v3-vol',
      modelList: [],
      
      // 轮播控制
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      isLastPage: false,
      
      // 示例数据
      examples: [
        { id: 'modern1', title: '城市夜景', type: '现代诗', icon: 'ri-book-open-line' },
        { id: 'classical1', title: '月下思乡', type: '古典诗', icon: 'ri-book-read-line' },
        { id: 'free1', title: '生命的意义', type: '自由诗', icon: 'ri-quill-pen-line' },
        { id: 'song1', title: '雨巷情思', type: '宋词', icon: 'ri-ink-bottle-line' },
        { id: 'tang1', title: '秋日山水', type: '唐诗', icon: 'ri-mountains-line' },
        { id: 'haiku1', title: '夏日蝉鸣', type: '俳句', icon: 'ri-leaf-line' },
        { id: 'landscape1', title: '田园黄昏', type: '山水诗', icon: 'ri-sun-foggy-line' },
        { id: 'love1', title: '思念情人', type: '爱情诗', icon: 'ri-heart-line' },
        { id: 'philosophical1', title: '生死沉思', type: '哲理诗', icon: 'ri-mind-map-line' },
        { id: 'seasonal1', title: '春天的脚步', type: '季节诗', icon: 'ri-seedling-line' }
      ],
      
      // 诗词创作知识内容
      poetryKnowledge: poetryKnowledge,
      
      // 示例数据模板
      exampleData: {
        'modern1': {
          noteType: 'modern-poem',
          noteTitle: '城市夜景',
          targetAudience: 'emotional',
          description: '描述现代城市的夜晚景象，霓虹灯与孤独人影的交织',
          keywords: '霓虹灯,高楼,寂寞,城市,夜晚'
        },
        'classical1': {
          noteType: 'classical-poem',
          noteTitle: '月下思乡',
          targetAudience: 'emotional',
          description: '游子在异乡赏月，触景生情，思念故乡和亲人',
          keywords: '明月,思乡,游子,离愁,夜色'
        },
        'free1': {
          noteType: 'free-verse',
          noteTitle: '生命的意义',
          targetAudience: 'philosophical',
          description: '探讨人生存在的价值和意义，表达对生命本质的思考',
          keywords: '生命,存在,哲思,意义,时间'
        },
        'song1': {
          noteType: 'song-ci',
          noteTitle: '雨巷情思',
          targetAudience: 'romantic',
          description: '雨中漫步的情人，打着油纸伞，在青石板路上留下足迹与思念',
          keywords: '油纸伞,雨巷,青石,思念,丁香'
        },
        'tang1': {
          noteType: 'tang-poem',
          noteTitle: '秋日山水',
          targetAudience: 'landscape',
          description: '秋天山间的景色，红叶、流水与远山的和谐画面',
          keywords: '秋山,红叶,流水,远眺,晚霞'
        },
        'haiku1': {
          noteType: 'haiku',
          noteTitle: '夏日蝉鸣',
          targetAudience: 'landscape',
          description: '夏日午后，蝉在树上鸣叫，表达夏天的炎热与生机',
          keywords: '蝉鸣,夏日,树荫,炎热,静谧'
        },
        'landscape1': {
          noteType: 'classical-poem',
          noteTitle: '田园黄昏',
          targetAudience: 'landscape',
          description: '黄昏时分的农村景象，炊烟袅袅，牧童归家',
          keywords: '炊烟,黄昏,田园,牧童,归家'
        },
        'love1': {
          noteType: 'modern-poem',
          noteTitle: '思念爱人',
          targetAudience: 'romantic',
          description: '描述对远方恋人的思念之情，以及相思带来的甜蜜与痛苦',
          keywords: '思念,距离,情书,等待,相思'
        },
        'philosophical1': {
          noteType: 'free-verse',
          noteTitle: '生死沉思',
          targetAudience: 'philosophical',
          description: '对生死问题的哲学思考，探讨存在的本质与意义',
          keywords: '生死,哲思,时间,永恒,灵魂'
        },
        'seasonal1': {
          noteType: 'modern-poem',
          noteTitle: '春天的脚步',
          targetAudience: 'landscape',
          description: '描述春天来临时大地复苏的景象与生机',
          keywords: '春天,新芽,花开,生机,鸟鸣'
        }
      }
    };
  },
  mounted() {
    this.fetchModelList();
    this.$nextTick(() => {
      this.updateCarouselPosition();
      window.addEventListener('resize', this.updateCarouselPosition);
    });
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
    async fetchModelList() {
      try {
        console.log('开始获取模型列表...');
        // 获取模型列表
        const response = await axios.get('/api/v1/llm/models', { timeout: 10000 });
        console.log('获取模型列表响应:', response.data);
        
        if (response.data && response.data.status === 'success') {
          // 获取所有模型但进行过滤，只保留火山引擎R1和V3模型
          const allModels = response.data.data || [];
          // 过滤模型，只保留火山引擎R1和V3模型
          this.modelList = allModels.filter(model => {
            return model.id === 'deepseek-v3-vol' || 
                   model.id === 'deepseek-r1-vol';
          });
          
          console.log('过滤后的可用模型列表:', this.modelList);
          
          // 如果过滤后没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.setupDefaultModels();
          }
          
          // 默认选择火山引擎V3
          const volcanoModel = this.modelList.find(model => model.id === 'deepseek-v3-vol');
          this.selectedModel = volcanoModel ? volcanoModel.id : (this.modelList[0] ? this.modelList[0].id : 'deepseek-v3-vol');
          console.log('已选择模型:', this.selectedModel);
        } else {
          console.error('获取模型列表失败:', response.data?.message);
          this.setupDefaultModels();
        }
      } catch (error) {
        console.error('获取模型列表异常:', error.message);
        if (error.response) {
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
        }
        this.setupDefaultModels();
      }
    },
    
    // 设置默认模型列表
    setupDefaultModels() {
      console.log('使用默认模型列表');
      this.modelList = [
        { id: 'deepseek-v3-vol', name: '火山引擎 DeepSeek V3' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' }
      ];
    },
    
    // 格式化Markdown文本
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗文本 **text**
      let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理换行符
      formattedText = formattedText.replace(/\n\n/g, '<br><br>');
      formattedText = formattedText.replace(/\n/g, '<br>');
      
      // 处理无序列表
      formattedText = formattedText.replace(/- (.*?)(<br>|$)/g, '<li>$1</li>');
      
      return formattedText;
    },
    
    // 生成诗歌的方法
    async generateLongform() {
      // 验证必填字段
      if (!this.validateForm()) {
        return;
      }
      
      this.isGenerating = true;
      this.generatedNote = '';
      
      try {
        // 构建提示词
        const prompt = this.generatePrompt();
        
        // 构建API请求
        const systemMessage = "你是一位富有创意和感染力的诗歌创作大师，能够根据用户要求创作出优美、有深度的诗歌作品。";
        const userMessage = prompt;
        
        const apiMessages = [
          { role: "system", content: systemMessage },
          { role: "user", content: userMessage }
        ];
        
        // 保存apiMessages供后续显示
        this.lastUsedPrompt = apiMessages;
        
        this.loadingText = '正在创作诗歌，请耐心等待...';
        
        // 确保选择了模型
        let modelId = this.selectedModel;
        if (!modelId) {
          modelId = 'deepseek-v3';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        // 将 deepseek-v3-vol 更改为 deepseek-v3
        if (modelId === 'deepseek-v3-vol') {
          modelId = 'deepseek-v3';
        }
        
        console.log('开始调用流式API，模型:', modelId);
        
        // 构建请求参数
        const requestData = {
          model: modelId,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.8,
          top_p: 0.95,
          stream: true,
          max_tokens: 2000
        };
        
        // 使用fetch API进行流式请求
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
          throw new Error(`服务器返回错误: ${response.status}`);
        }
        
        // 获取响应的reader用于流式处理
        const reader = response.body.getReader();
        
        // 清空之前的生成内容
        this.generatedNote = '';
        
        // 处理流式数据
        const processStream = async () => {
          let decoder = new TextDecoder('utf-8');
          
          while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
              console.log('流式响应完成');
              break;
            }
            
            // 解码接收到的数据
            const chunk = decoder.decode(value, { stream: true });
            console.log('收到流式数据块:', chunk);
            
            // 处理接收到的数据，通常格式为 "data: {...}\n\n"
            const lines = chunk.split('\n');
            
            for (const line of lines) {
              if (line.startsWith('data: ') && line.length > 6) {
                try {
                  const dataStr = line.substring(6); // 去掉 "data: " 前缀
                  
                  // 处理特殊的 [DONE] 结束标记
                  if (dataStr.trim() === '[DONE]') {
                    console.log('收到结束标记 [DONE]');
                    continue;
                  }
                  
                  const data = JSON.parse(dataStr);
                  
                  // 从响应中提取内容
                  let content = '';
                  
                  if (data.choices && data.choices.length > 0 && data.choices[0].delta) {
                    content = data.choices[0].delta.content || '';
                  } else if (data.content) {
                    content = data.content;
                  }
                  
                  if (content) {
                    // 累加内容到结果中
                    this.generatedNote += content;
                  }
                } catch (e) {
                  console.error('解析流式数据出错:', e, line);
                }
              }
            }
          }
        };
        
        // 开始处理流
        await processStream();
        
        if (this.generatedNote) {
          console.log('成功获取诗歌内容');
          // 添加成功提示
          this.$message ? this.$message.success('诗歌创作成功！') : alert('诗歌创作成功！');
        } else {
          console.error('API返回成功，但无内容');
          throw new Error('无法从API响应中获取内容');
        }
      } catch (error) {
        console.error('生成诗歌出错，详细错误:', error);
        
        // 更详细的错误日志
        if (error.response) {
          // 服务器响应了，但状态码不在2xx范围
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          this.$message ? 
            this.$message.error(`生成失败: 服务器错误 (${error.response.status})`) : 
            alert(`生成诗歌失败: 服务器错误 (${error.response.status})`);
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到服务器响应');
          this.$message ? 
            this.$message.error('生成失败: 服务器无响应，请检查网络连接') : 
            alert('生成诗歌失败: 服务器无响应，请检查网络连接');
        } else {
          // 设置请求时发生错误
          console.error('错误信息:', error.message);
          this.$message ? 
            this.$message.error(`生成失败: ${error.message}`) : 
            alert(`生成诗歌失败: ${error.message}`);
        }
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          console.log('开发模式：使用示例内容');
          this.generatedNote = `《${this.noteTitle}》\n\n静谧的夜晚\n星光点点\n思绪如潮\n\n谁的脚步声\n敲打着心弦\n像远方的呼唤\n\n生命如诗\n跌宕起伏\n在时光的长河中\n寻找永恒的回响`;
        }
      } finally {
        this.isGenerating = false;
      }
    },
    
    // 验证表单
    validateForm() {
      if (!this.noteTitle) {
        this.$message ? this.$message.error('请输入诗歌主题') : alert('请输入诗歌主题');
        return false;
      }
      
      return true;
    },
    
    // 生成提示词
    generatePrompt() {
      let prompt = '请根据以下要求创作一首诗歌：\n\n';
      
      // 获取诗歌类型的中文名称
      const getNoteTypeName = () => {
        switch (this.noteType) {
          case 'modern-poem': return '现代诗';
          case 'classical-poem': return '古典诗';
          case 'free-verse': return '自由诗';
          case 'song-ci': return '宋词';
          case 'tang-poem': return '唐诗';
          case 'haiku': return '俳句';
          default: return this.noteType;
        }
      };
      
      prompt += `诗歌类型：${getNoteTypeName()}\n`;
      prompt += `诗歌主题：${this.noteTitle}\n`;
      
      if (this.targetAudience) {
        // 获取风格倾向的中文名称
        const getStyleName = () => {
          switch (this.targetAudience) {
            case 'romantic': return '浪漫抒情';
            case 'philosophical': return '哲理思考';
            case 'narrative': return '叙事描写';
            case 'landscape': return '山水田园';
            case 'emotional': return '情感表达';
            case 'historical': return '历史怀古';
            default: return this.targetAudience;
          }
        };
        
        prompt += `风格倾向：${getStyleName()}\n`;
      }
      
      if (this.description) {
        prompt += `背景/情景：${this.description}\n`;
      }
      
      // 关键词
      if (this.keywords) {
        prompt += `关键词：${this.keywords}\n`;
      }
      
      // 特别要求
      if (this.noteType === 'classical-poem' || this.noteType === 'tang-poem') {
        prompt += '\n请注意遵循古典诗词的格律要求，注意平仄和韵律。\n';
      } else if (this.noteType === 'song-ci') {
        prompt += '\n请根据宋词的词牌格式创作，注意平仄和韵律。\n';
      } else if (this.noteType === 'haiku') {
        prompt += '\n请遵循俳句5-7-5音节的格式，简洁凝练，意境优美。\n';
      }
      
      // 额外要求
      prompt += '\n请创作一首有深度、富有情感且语言优美的诗歌，避免使用陈词滥调。诗歌应当有意境，能引发读者的共鸣。\n';
      
      return prompt;
    },
    
    // 重置表单
    resetForm() {
      this.noteType = 'modern-poem';
      this.noteTitle = '';
      this.targetAudience = 'romantic';
      this.description = '';
      this.keywords = '';
      this.generatedNote = '';
    },
    
    // 显示创作小贴士
    showKnowledge() {
      this.showKnowledgeModal = true;
    },
    
    // 复制生成的文本
    copyText() {
      if (!this.generatedNote) return;
      
      try {
        navigator.clipboard.writeText(this.generatedNote).then(() => {
          this.$message ? this.$message.success('诗歌已复制到剪贴板') : alert('诗歌已复制到剪贴板');
        });
      } catch (error) {
        console.error('复制失败:', error);
        this.$message ? this.$message.error('复制失败，请手动复制') : alert('复制失败，请手动复制');
      }
    },
    
    // 显示提示词模态框
    showPrompt() {
      this.showPromptModal = true;
    },
    
    // 复制提示词到剪贴板
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      
      try {
        // The code is unchanged as it already works
        let promptText = '';
        if (typeof this.lastUsedPrompt === 'string') {
          promptText = this.lastUsedPrompt;
        } else {
          // 遍历消息数组
          this.lastUsedPrompt.forEach(msg => {
            promptText += `【${msg.role === 'system' ? '系统' : '用户'}】\n${msg.content}\n\n`;
          });
        }
        
        navigator.clipboard.writeText(promptText).then(() => {
          this.$message ? this.$message.success('提示词已复制到剪贴板') : alert('提示词已复制到剪贴板');
        });
      } catch (error) {
        console.error('复制提示词失败:', error);
        this.$message ? this.$message.error('复制失败，请手动复制') : alert('复制失败，请手动复制');
      }
    },
    
    // 下载生成的文本
    downloadText() {
      if (!this.generatedNote) return;
      
      const element = document.createElement('a');
      const file = new Blob([this.generatedNote], {type: 'text/plain'});
      element.href = URL.createObjectURL(file);
      element.download = `诗歌_${this.noteTitle || '未命名'}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    
    // 前一个示例
    prevExample() {
      if (this.currentExampleIndex <= 0) return;
      this.currentExampleIndex--;
      this.updateCarouselPosition();
    },
    
    // 后一个示例
    nextExample() {
      if (this.isLastPage) return;
      this.currentExampleIndex++;
      this.updateCarouselPosition();
    },
    
    updateCarouselPosition() {
      const carousel = this.$refs.exampleCarousel;
      if (!carousel) return;
      
      const cardWidth = 180; // 每个卡片的宽度 + 边距
      const containerWidth = carousel.parentElement.offsetWidth;
      const cardsPerPage = Math.floor(containerWidth / cardWidth);
      const maxIndex = Math.max(0, this.examples.length - cardsPerPage);
      
      // 限制索引范围
      this.currentExampleIndex = Math.min(this.currentExampleIndex, maxIndex);
      
      // 计算平移距离
      this.exampleTranslateX = -this.currentExampleIndex * cardWidth;
      
      // 更新是否为最后一页
      this.isLastPage = this.currentExampleIndex >= maxIndex;
    },
    
    // 加载示例数据
    loadExample(exampleId) {
      const example = this.exampleData[exampleId];
      if (example) {
        this.noteType = example.noteType;
        this.noteTitle = example.noteTitle;
        this.targetAudience = example.targetAudience;
        this.description = example.description;
        this.keywords = example.keywords || '';
      }
    },
    
    // 提取诗歌标题
    extractPoemTitle() {
      if (!this.generatedNote) return this.noteTitle || '无题';
      
      // 检查是否有《》包围的标题
      const titleMatch = this.generatedNote.match(/《([^》]+)》/);
      if (titleMatch && titleMatch[1]) {
        return titleMatch[1];
      }
      
      // 检查是否有"标题："格式
      const titlePrefixMatch = this.generatedNote.match(/标题[:：]\s*(.+)[\n\r]/);
      if (titlePrefixMatch && titlePrefixMatch[1]) {
        return titlePrefixMatch[1];
      }
      
      // 使用用户输入的主题作为标题
      return this.noteTitle || '无题';
    },
    
    // 格式化诗歌内容
    formattedPoemContent() {
      if (!this.generatedNote) return '';
      
      let content = this.generatedNote;
      
      // 移除可能的标题行
      content = content.replace(/《([^》]+)》\s*[\n\r]?/, '');
      content = content.replace(/标题[:：]\s*.+[\n\r]/, '');
      
      // 根据诗歌类型应用不同的格式
      if (this.noteType === 'haiku') {
        // 俳句格式：将每行加上特殊的样式
        content = content.split('\n').map(line => {
          if (line.trim()) {
            return `<div class="haiku-line">${line}</div>`;
          }
          return '<div class="poem-separator"></div>';
        }).join('');
      } else if (this.noteType === 'classical-poem' || this.noteType === 'tang-poem') {
        // 古典诗词格式：注意平仄和对仗
        content = content.split('\n').map(line => {
          if (line.trim()) {
            return `<div class="classical-line">${line}</div>`;
          }
          return '<div class="poem-separator"></div>';
        }).join('');
      } else if (this.noteType === 'song-ci') {
        // 宋词格式：段落之间的区分更明显
        content = content.split('\n').map(line => {
          if (line.trim()) {
            return `<div class="classical-line">${line}</div>`;
          }
          return '<div class="poem-separator"></div>';
        }).join('');
      } else if (this.noteType === 'free-verse') {
        // 自由诗：行与行之间的位置可以更自由
        content = content.split('\n').map((line, index) => {
          if (line.trim()) {
            // 让每行的缩进不同，营造参差错落的效果
            const indent = index % 3 === 0 ? 'style="margin-left: 10px;"' : 
                           index % 3 === 1 ? 'style="margin-left: 30px;"' : 
                           'style="margin-left: 50px;"';
            return `<div class="poem-line" ${indent}>${line}</div>`;
          }
          return '<div class="poem-separator"></div>';
        }).join('');
      } else {
        // 现代诗格式
        content = content.split('\n').map(line => {
          if (line.trim()) {
            return `<div class="poem-line">${line}</div>`;
          }
          return '<div class="poem-separator"></div>';
        }).join('');
      }
      
      return content;
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateCarouselPosition);
  }
};
</script>

<style scoped>
@import "../../../assets/css/text-creation-common.css";

/* 重置所有可能的滚动设置 - 确保只有最外层有滚动条 */
.note-result, 
.poem-wrapper, 
.result-content-wrapper,
.empty-result,
.loading-overlay {
  overflow: visible !important;
  max-height: none !important;
  height: auto !important;
}

/* 页面布局和大小调整 */
.longform-article-page {
  padding: 20px;
  height: calc(100vh - 60px);
  overflow-y: auto; /* 只在顶层保留滚动 */
  background-color: #f5f7fa;
}

.main-container {
  display: flex;
  gap: 20px;
  position: relative;
  padding-bottom: 30px; /* 增加底部内边距确保内容完全包含 */
}

/* 左侧输入区域 */
.input-section {
  flex: 0 0 300px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  padding-bottom: 50px; /* 增加底部内边距确保内容都被包含 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 20px;
  display: flex;
  flex-direction: column;
  margin-bottom: 30px; /* 增加底部外边距 */
}

/* 确保表单组和按钮区域正确显示 */
.form-group {
  margin-bottom: 18px;
  width: 100%;
}

.form-group:last-of-type {
  margin-bottom: 25px; /* 最后一个表单元素与按钮区域的间距 */
}

/* 左侧输入区域的按钮样式 */
.input-section .action-buttons {
  margin-top: 25px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 15px;
}

/* 右侧内容区域 */
.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0; /* 防止内容溢出 */
}

/* 示例部分 */
.examples-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 结果部分 */
.result-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: auto; /* 自动适应内容高度 */
  min-height: 650px; /* 设置更大的最小高度，确保容器足够大 */
  display: flex;
  flex-direction: column;
}

/* 确保空间充足 */
.section-header {
  margin-bottom: 15px; /* 增加头部与内容区的间距 */
}

.result-content-wrapper {
  position: relative;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* 按钮样式确保不超出容器 */
.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.action-buttons button {
  padding: 0 15px;
  height: 36px;
  white-space: nowrap;
}

/* 诗歌容器样式 */
.poem-container {
  overflow-y: auto !important;
  max-height: 600px !important; /* 使用最大高度而非固定高度 */
  padding: 15px;
  flex: 1; /* 让容器自适应填充剩余空间 */
  display: flex;
  flex-direction: column;
  align-items: center; /* 居中显示诗歌 */
  background-color: #f9f9f9; /* 使用微妙的背景色增加视觉区分 */
  border-radius: 0 0 8px 8px; /* 底部边角圆角 */
  margin-bottom: 10px; /* 底部增加间距 */
}

/* 诗歌内容展示的特殊样式 */
.poem-wrapper {
  max-width: 600px;
  width: 100%; /* 确保宽度撑开 */
  margin: 0 auto;
  padding: 30px;
  background-color: #fffbf0;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  min-height: 300px;
  height: auto; /* 自动适应内容高度 */
  overflow: visible !important;
}

.poem-wrapper.classical-poem,
.poem-wrapper.tang-poem,
.poem-wrapper.song-ci {
  font-family: "KaiTi", "STKaiti", "FangSong", "SimSun", serif;
  font-size: 18px;
  line-height: 1.8;
}

.poem-wrapper.modern-poem,
.poem-wrapper.free-verse {
  font-family: "PingFang SC", "Helvetica Neue", Helvetica, "Microsoft YaHei", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
}

.poem-wrapper.haiku {
  font-family: "PingFang SC", "Helvetica Neue", Helvetica, "Microsoft YaHei", Arial, sans-serif;
  font-size: 18px;
  line-height: 2;
}

.poem-title {
  font-size: 24px;
  text-align: center;
  margin-bottom: 25px;
  color: #5d4037;
  font-weight: bold;
}

.poem-content {
  padding: 0 20px;
  white-space: pre-wrap;
}

.poem-wrapper.classical-poem .poem-content,
.poem-wrapper.tang-poem .poem-content,
.poem-wrapper.song-ci .poem-content {
  text-align: center;
}

/* 结果内容区样式 */
.note-result {
  padding: 15px;
}

/* 空白状态 */
.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  flex: 1; /* 让空白状态容器也填充剩余空间 */
}

.empty-content {
  text-align: center;
  padding: 20px;
}

.empty-image {
  width: 120px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.empty-message {
  color: #999;
  font-size: 15px;
}

/* 加载状态 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  min-height: 300px;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  border-radius: 8px; /* 圆角与父容器匹配 */
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid var(--primary-color, #ba003f);
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 15px;
  color: var(--primary-color, #ba003f);
  font-weight: 500;
}

/* 全面禁用所有内部滚动条样式（保留功能但美化外观） */
.poem-container::-webkit-scrollbar {
  width: 8px !important;
  height: 8px !important;
  display: block !important;
}

.poem-container::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

.poem-container::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

.poem-container::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}

/* 其他元素仍然禁用滚动条 */
.note-result::-webkit-scrollbar,
.poem-wrapper::-webkit-scrollbar,
.result-content-wrapper::-webkit-scrollbar,
.empty-result::-webkit-scrollbar,
.loading-overlay::-webkit-scrollbar,
.prompt-content::-webkit-scrollbar,
.prompt-modal::-webkit-scrollbar {
  display: none !important;
  width: 0px !important;
  height: 0px !important;
}

/* 响应式样式 */
@media (max-width: 1200px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section {
    flex: none;
    width: 100%;
    position: static;
  }
  
  .right-column {
    width: 100%;
  }
  
  .poem-wrapper {
    max-width: 100%;
    overflow: visible !important; /* 强制避免移动端上的滚动 */
  }
}

@media (max-width: 768px) {
  /* 移动端也确保没有内部滚动 */
  .note-result, 
  .poem-wrapper, 
  .result-content-wrapper,
  .empty-result,
  .loading-overlay {
    overflow: visible !important;
    max-height: none !important;
    height: auto !important;
  }
  
  .poem-wrapper {
    padding: 15px;
    min-height: 300px;
  }
  
  .empty-result, .loading-overlay {
    min-height: 300px; /* 与poem-wrapper保持一致 */
  }
  
  .poem-title {
    font-size: 20px;
    margin-bottom: 15px;
  }
  
  .poem-content {
    padding: 0 10px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .section-header .action-buttons {
    margin-top: 10px;
    width: 100%;
    justify-content: space-between;
  }
  
  .input-section {
    padding-bottom: 30px;
  }
  
  .note-result {
    overflow: visible !important; /* 强制避免移动端上的滚动 */
  }
  
  .result-content-wrapper {
    overflow: visible !important; /* 强制避免移动端上的滚动 */
  }
  
  .poem-container {
    max-height: 500px !important; /* 移动端稍微减小高度 */
  }
  
  /* 确保移动端下内容也能完整显示 */
  .result-section {
    display: flex;
    flex-direction: column;
    min-height: 500px; /* 移动端也保持较大高度 */
  }
}

/* 提示词模态框样式 */
.prompt-modal {
  width: 90%;
  max-width: 800px;
}

.prompt-content {
  background-color: #fafafa;
  padding: 15px;
  border-radius: 6px;
  max-height: none; /* 移除高度限制 */
  overflow-y: visible; /* 不再使用auto */
}

.prompt-message {
  margin-bottom: 15px;
  border-left: 3px solid var(--primary-color, #ba003f);
  padding-left: 12px;
}

.prompt-role {
  font-weight: bold;
  margin-bottom: 5px;
  color: var(--primary-color, #ba003f);
}

.prompt-text {
  white-space: pre-wrap;
  line-height: 1.5;
  font-family: monospace;
  font-size: 14px;
}

.prompt-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

/* 加载动画样式 - 特定于此页面的额外样式 */
.loading-text {
  margin-top: 15px;
  color: var(--primary-color, #ba003f);
}

/* 结果内容区样式 */
.note-result {
  padding: 15px;
}

/* 修复内容被截断的问题 */
.blur-content {
  filter: blur(3px);
  pointer-events: none;
  opacity: 0.7;
}
</style> 