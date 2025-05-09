<template>
  <div class="xiaohongshu-article-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>小红书笔记生成</h2>
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
            <div class="checkbox-item" :class="{'checkbox-active': includeEmoji}">
              <input type="checkbox" v-model="includeEmoji" id="emoji-checkbox">
              <label for="emoji-checkbox" class="checkbox-label">表情符号</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeRating}">
              <input type="checkbox" v-model="includeRating" id="rating-checkbox">
              <label for="rating-checkbox" class="checkbox-label">评分</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeProsCons}">
              <input type="checkbox" v-model="includeProsCons" id="proscons-checkbox">
              <label for="proscons-checkbox" class="checkbox-label">优缺点</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeTips}">
              <input type="checkbox" v-model="includeTips" id="tips-checkbox">
              <label for="tips-checkbox" class="checkbox-label">小贴士</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeHashtags}">
              <input type="checkbox" v-model="includeHashtags" id="hashtags-checkbox">
              <label for="hashtags-checkbox" class="checkbox-label">话题标签</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeImageDesc}">
              <input type="checkbox" v-model="includeImageDesc" id="imagedesc-checkbox">
              <label for="imagedesc-checkbox" class="checkbox-label">图片建议</label>
            </div>
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
            <div class="section-title">
              <i class="ri-file-list-3-line"></i>
              参考案例
            </div>
            <div class="carousel-controls" v-if="examples.length > 0">
              <button class="carousel-control" @click="prevExample" :class="{ disabled: exampleIndex === 0 }">
                <i class="ri-arrow-left-s-line"></i>
              </button>
              <button class="carousel-control" @click="nextExample" :class="{ disabled: isLastPage }">
                <i class="ri-arrow-right-s-line"></i>
              </button>
            </div>
          </div>
          <div class="example-carousel">
            <div class="example-cards" ref="exampleCards" :style="exampleCardsStyle">
              <div v-for="(example, index) in examples" :key="index" class="example-card" @click="selectExample(example)">
                <div class="example-card-header">
                  <div class="xiaohongshu-example-icon" :class="{'has-svg': example.title === '这款面霜真的绝了'}">
                    <!-- 为面霜案例添加特殊处理 -->
                    <svg v-if="example.title === '这款面霜真的绝了'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" class="cream-icon">
                      <path fill="none" d="M0 0h24v24H0z"/>
                      <path d="M15.5 2a3.5 3.5 0 0 1 3.437 4.163l-.015.066a6.5 6.5 0 0 1 .943 9.337l-.177.221a6.5 6.5 0 0 1-7.602 1.645l-.313-.158-2.697 2.697-1.414-1.414 2.697-2.697-.158-.313a6.5 6.5 0 0 1 1.645-7.602l.221-.177a6.5 6.5 0 0 1 9.403.043A3.5 3.5 0 0 1 15.5 2zm0 2a1.5 1.5 0 0 0-1.493 1.65l.008.1.017.047a6.5 6.5 0 0 1-1.14 9.539l-.31.223a6.5 6.5 0 0 1-1.241.794c-.439.22-.87.377-1.285.466l-.385.071.144.182a4.5 4.5 0 0 0 5.975.141l.174-.156a4.5 4.5 0 0 0 .16-6.175l-.156-.174a6.5 6.5 0 0 1-1.217-2.592l-.037-.283a1.5 1.5 0 0 0 .768-1.266L17 6.5A1.5 1.5 0 0 0 15.5 4zM10 8a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9zm0 2a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5z" fill="#ba003f"/>
                    </svg>
                    
                    <!-- 其他案例的图标 -->
                    <i v-else-if="example.icon" :class="example.icon"></i>
                    <i v-else class="ri-file-text-line"></i>
                    
                    <!-- 备选方案 -->
                    <span v-if="!example.icon && example.title !== '这款面霜真的绝了'" class="fallback-icon">
                      {{ example.title ? example.title.charAt(0) : '例' }}
                    </span>
                  </div>
                  <div class="example-title" :title="example.title">{{ example.title }}</div>
                </div>
                <div class="example-content">
                  <div class="example-desc" :title="example.desc">{{ example.desc }}</div>
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
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无笔记内容，请点击"生成笔记"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedNote" class="note-result" :class="{'blur-content': isGenerating}">
              <div class="iphone-mockup">
                <div class="iphone-notch"></div>
                <div class="iphone-header">
                  <div class="status-bar">
                    <div class="time">10:30</div>
                    <div class="status-icons">
                      <i class="ri-battery-fill"></i>
                      <i class="ri-wifi-fill"></i>
                      <i class="ri-signal-wifi-3-fill"></i>
                    </div>
                  </div>
                  <div class="app-header">
                    <div class="app-title">
                      <i class="ri-arrow-left-s-line"></i>
                      <span>小红书</span>
                    </div>
                    <div class="app-actions">
                      <i class="ri-more-2-fill"></i>
                    </div>
                  </div>
                </div>
                <div class="phone-content">
                  <div class="redbook-post">
                    <div class="post-header">
                      <div class="user-avatar">
                        <i class="ri-user-3-fill"></i>
                      </div>
                      <div class="user-info">
                        <div class="username">AI助手</div>
                        <div class="publish-info">刚刚 · 小红书 iPhone</div>
                      </div>
                      <div class="follow-btn">关注</div>
                    </div>
                    <div class="post-title">{{ noteTitle || "今日份分享" }}</div>
                    <div class="post-content" v-if="generatedNote">
                      <div v-html="formatContent(generatedNote)"></div>
                    </div>
                    <div class="post-content-placeholder" v-else>
                      <p>点击"生成笔记"按钮开始创作精彩内容...</p>
                    </div>
                    <div class="post-tags">
                      <span class="tag" v-for="(tag, idx) in generateRandomTags()" :key="idx">
                        {{ tag }}
                      </span>
                    </div>
                    <div class="post-stats">
                      <div class="stat-item">
                        <i class="ri-heart-line"></i>
                        <span>赞</span>
                      </div>
                      <div class="stat-item">
                        <i class="ri-chat-1-line"></i>
                        <span>评论</span>
                      </div>
                      <div class="stat-item">
                        <i class="ri-star-line"></i>
                        <span>收藏</span>
                      </div>
                      <div class="stat-item">
                        <i class="ri-share-forward-line"></i>
                        <span>分享</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="home-indicator"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态框 - 修改为抽屉组件 -->
    <el-drawer
      v-model="showTipsModal"
      title="小红书内容创作指南"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in articleKnowledge" :key="index" class="knowledge-section">
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
import { xiaohongshuArticleExamples } from '@/views/example_data.js';
import { xiaohongshuArticleKnowledge } from '@/views/Knowledge_data.js';

export default {
  name: 'XiaohongshuArticle_v2',
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
      exampleIndex: 0,
      
      // 示例案例
      examples: xiaohongshuArticleExamples,
      currentExampleIndex: 0,
      
      // 添加知识内容
      articleKnowledge: xiaohongshuArticleKnowledge
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
    console.log('参考案例数据:', this.examples);
    
    // 使用更安全的方式初始化
    this.exampleIndex = 0;
    
    // 通过延迟执行确保组件已完全挂载
    setTimeout(() => {
      this.updateExamplesTranslation();
    }, 100);
  },
  computed: {
    isLastPage() {
      if (!this.$refs.exampleCards) return true;
      const cardWidth = 220; // 卡片宽度+间距，调整为220px
      const containerWidth = this.$refs.exampleCards.parentElement.clientWidth;
      const totalWidth = this.examples.length * cardWidth;
      const maxScrollX = totalWidth - containerWidth;
      
      // 当滚动到最大滚动距离的90%以上时，认为是最后一页
      return Math.abs(this.exampleIndex * cardWidth) >= maxScrollX * 0.9;
    },
    exampleCardsStyle() {
      // 避免在渲染时访问DOM元素
      return { transform: `translateX(-${Math.max(0, this.exampleIndex * 220)}px)` };
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
      
      // 首先尝试使用navigator.clipboard API
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(textToCopy)
          .then(() => {
            alert('内容已复制到剪贴板');
          })
          .catch(err => {
            console.error('使用clipboard API复制失败:', err);
            // 如果clipboard API失败，使用后备方法
            this.fallbackCopyText(textToCopy);
          });
      } else {
        // 直接使用后备方法
        this.fallbackCopyText(textToCopy);
      }
    },
    
    // 后备复制方法
    fallbackCopyText(text) {
      try {
        // 创建临时文本区域
        const textArea = document.createElement('textarea');
        textArea.value = text;
        
        // 设置样式使元素不可见
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        textArea.style.top = '0';
        textArea.style.left = '0';
        
        // 添加到DOM
        document.body.appendChild(textArea);
        
        // 选择文本并执行复制
        textArea.select();
        const successful = document.execCommand('copy');
        
        // 移除临时元素
        document.body.removeChild(textArea);
        
        if (successful) {
          alert('内容已复制到剪贴板');
        } else {
          alert('复制失败，请手动选择并复制');
        }
      } catch (err) {
        console.error('后备复制方法失败:', err);
        alert('复制失败，请手动选择并复制');
      }
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
        
      // 首先尝试使用navigator.clipboard API
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(promptText)
          .then(() => {
            alert('提示词已复制到剪贴板');
          })
          .catch(err => {
            console.error('使用clipboard API复制失败:', err);
            // 如果clipboard API失败，使用后备方法
            this.fallbackCopyText(promptText);
          });
      } else {
        // 直接使用后备方法
        this.fallbackCopyText(promptText);
      }
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
    
    // 下一个示例
    nextExample() {
      if (this.examples.length === 0) return;
      
      // 安全检查
      if (!this.$refs.exampleCards) {
        console.warn('示例卡片容器未加载');
        return;
      }
      
      this.exampleIndex = (this.exampleIndex + 1) % this.examples.length;
      this.$nextTick(() => {
        this.updateExamplesTranslation();
      });
    },
    
    // 上一个示例
    prevExample() {
      if (this.examples.length === 0) return;
      
      // 安全检查
      if (!this.$refs.exampleCards) {
        console.warn('示例卡片容器未加载');
        return;
      }
      
      this.exampleIndex = (this.exampleIndex - 1 + this.examples.length) % this.examples.length;
      this.$nextTick(() => {
        this.updateExamplesTranslation();
      });
    },
    
    // 选择示例
    selectExample(example) {
      this.loadExample(example);
    },
    
    // 处理选择示例
    loadExample(example) {
      // 直接使用example对象的属性
      this.noteType = example.noteType || 'product-review';
      this.noteTitle = example.noteTitle || '';
      this.productName = example.productName || '';
      this.description = example.desc || '';
      this.writingStyle = example.writingStyle || 'friendly';
      
      // 设置内容元素选项
      this.includeEmoji = example.includeEmoji !== undefined ? example.includeEmoji : true;
      this.includeRating = example.includeRating !== undefined ? example.includeRating : true;
      this.includeProsCons = example.includeProsCons !== undefined ? example.includeProsCons : true;
      this.includeTips = example.includeTips !== undefined ? example.includeTips : false;
      this.includeHashtags = example.includeHashtags !== undefined ? example.includeHashtags : true;
      this.includeImageDesc = example.includeImageDesc !== undefined ? example.includeImageDesc : true;
      
      // 生成随机标签
      this.keywords = this.generateRandomTags();
    },
    
    // 生成随机标签
    generateRandomTags() {
      // 根据笔记类型生成对应的标签
      const tagsByType = {
        'product-review': ['种草笔记', '好物推荐', '测评', '实用好物', '拔草指南'],
        'lifestyle': ['生活方式', '日常', '生活记录', '理想生活', '生活向上'],
        'travel': ['旅行', '旅游攻略', '周末去哪儿', '探店', '旅行记录'],
        'food': ['美食推荐', '吃货', '美食记录', '探店', '美食分享'],
        'fashion': ['穿搭', '时尚', '搭配', '穿搭分享', '时尚博主'],
        'beauty': ['美妆', '护肤', '化妆教程', '美妆分享', '护肤心得']
      };
      
      // 获取当前笔记类型的标签
      const typeTags = tagsByType[this.noteType] || ['小红书', '生活记录', '分享'];
      
      // 生成3个随机标签
      const tags = [];
      
      // 先添加一个当前笔记类型的标签
      tags.push(typeTags[Math.floor(Math.random() * typeTags.length)]);
      
      // 添加通用标签
      const commonTags = ['生活记录', '分享心得', '小红书', '好物推荐', '干货分享', '经验分享'];
      
      // 再添加2个通用随机标签，确保不重复
      while (tags.length < 3) {
        const randomTag = commonTags[Math.floor(Math.random() * commonTags.length)];
        if (!tags.includes(randomTag)) {
          tags.push(randomTag);
        }
      }
      
      return tags.join(', ');
    },
    formatContent(content) {
      if (!content) return '';
      
      // 处理换行符
      let formatted = content.replace(/\n/g, '<br>');
      
      // 处理Markdown风格的标题
      formatted = formatted.replace(/^#\s+(.+)$/gm, '<strong style="font-size:18px;">$1</strong>');
      formatted = formatted.replace(/^##\s+(.+)$/gm, '<strong style="font-size:16px;">$1</strong>');
      
      // 处理Markdown风格的粗体
      formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      
      // 处理Markdown风格的斜体
      formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');
      
      // 处理列表
      formatted = formatted.replace(/^-\s+(.+)$/gm, '• $1<br>');
      
      // 处理表情符号 (保持原样)
      
      return formatted;
    },
    // 获取示例描述信息
    getExampleDescription(example) {
      return example.desc || '';
    },
    
    // 更新示例卡片的位移
    updateExamplesTranslation() {
      // 不直接操作DOM，改为通过更新exampleIndex间接触发更新
      if (this.examples.length > 0) {
        // 确保exampleIndex不超出边界
        this.exampleIndex = Math.min(this.exampleIndex, this.examples.length - 1);
      }
    },
    // 添加Markdown格式化函数
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗文本
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理列表项
      text = text.replace(/\n\n/g, '<br><br>');
      
      return text;
    },
  }
};
</script>

<style scoped>
@import "@/assets/css/text-creation-common.css";

/* 以下是特定于小红书的样式，未在公共样式中定义的部分 */

/* 修改后的示例卡片样式 */
.example-card-header {
  display: flex;
  align-items: flex-start;
  position: relative;
  padding-left: 80px; /* 为图标预留空间 */
  min-height: 85px;
}

.example-title {
  flex: 1;
}

/* 自定义图标样式，避免与全局样式冲突 */
.xiaohongshu-example-icon {
  position: absolute;
  left: 16px;
  top: 15px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  box-shadow: 0 3px 6px rgba(186, 0, 63, 0.1);
}

.xiaohongshu-example-icon i {
  font-size: 26px;
  color: #ba003f;
}

/* 手机模拟器样式 */
.note-result {
  flex: 1;
  padding: 15px;
  overflow: hidden;
  display: flex;
  height: 100%;
  justify-content: center;
}

.iphone-mockup {
  position: relative;
  width: 360px;
  height: 680px;
  background-color: #fff;
  border-radius: 40px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2),
              inset 0 0 0 2px rgba(0, 0, 0, 0.05),
              inset 0 0 0 6px #f2f2f2,
              inset 0 0 0 10px #fff;
  border: 12px solid #333;
}

.iphone-notch {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 30px;
  background-color: #000;
  border-radius: 0 0 20px 20px;
  z-index: 10;
}

.iphone-header {
  background: linear-gradient(to right, #FF2C55, #FF4F5E);
  padding: 30px 15px 10px;
  position: relative;
  z-index: 5;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 5px 15px;
}

.time {
  font-size: 14px;
  color: #fff;
  font-weight: 600;
}

.status-icons {
  display: flex;
  gap: 7px;
}

.status-icons i {
  font-size: 14px;
  color: #fff;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 5px 10px;
}

.app-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.app-title i {
  font-size: 22px;
  color: #fff;
}

.app-title span {
  font-size: 18px;
  color: #fff;
  font-weight: 600;
}

.app-actions {
  display: flex;
  gap: 15px;
}

.app-actions i {
  font-size: 20px;
  color: #fff;
}

.phone-content {
  position: absolute;
  top: 110px;
  left: 0;
  right: 0;
  bottom: 20px;
  padding: 10px;
  overflow-y: auto;
  background-color: #f7f7f7;
  max-height: 540px;
}

.redbook-post {
  background-color: #fff;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: #f3f3f3;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.user-avatar i {
  font-size: 22px;
  color: #999;
}

.user-info {
  flex: 1;
}

.username {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
}

.publish-info {
  font-size: 12px;
  color: #999;
}

.follow-btn {
  background-color: #fe496c;
  color: #fff;
  border: none;
  border-radius: 15px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 500;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
  line-height: 1.4;
}

.post-content {
  font-size: 14px;
  color: #333;
  line-height: 1.6;
  margin-bottom: 15px;
}

.post-content-placeholder {
  font-size: 14px;
  color: #999;
  line-height: 1.6;
  margin-bottom: 15px;
  text-align: center;
  padding: 20px 0;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.tag {
  background-color: #f6f6f6;
  color: #666;
  border-radius: 15px;
  padding: 4px 12px;
  font-size: 12px;
}

.post-stats {
  display: flex;
  border-top: 1px solid #f3f3f3;
  padding-top: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  color: #666;
  font-size: 12px;
}

.stat-item i {
  font-size: 18px;
  margin-bottom: 5px;
}

.home-indicator {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 5px;
  background-color: #ccc;
  border-radius: 3px;
}

/* 提示词模态框样式 */
.prompt-modal {
  max-width: 700px;
  width: 90%;
}

.prompt-content {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 10px;
}

.prompt-message {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.prompt-message:last-child {
  border-bottom: none;
}

.prompt-role {
  font-weight: 600;
  margin-bottom: 5px;
  color: var(--primary-color, #ba003f);
}

.prompt-text {
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.5;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
}

.tips-list {
  padding-left: 20px;
  margin: 0;
}

.tips-list li {
  margin-bottom: 10px;
  line-height: 1.5;
}

.fallback-icon {
  font-size: 26px;
  font-weight: bold;
  color: #ba003f;
}

.xiaohongshu-example-icon.has-svg {
  display: flex;
  align-items: center;
  justify-content: center;
}

.cream-icon {
  width: 30px;
  height: 30px;
}

/* 添加知识学习抽屉的样式 */
.knowledge-content {
  padding: 20px;
}

.knowledge-section {
  margin-bottom: 25px;
}

.knowledge-subtitle {
  color: var(--primary-color, #ff2442);
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 36, 66, 0.2);
  padding-bottom: 8px;
  display: flex;
  align-items: center;
}

.knowledge-text {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
}

.knowledge-text p {
  margin-bottom: 12px;
}

.knowledge-text ul, .knowledge-text ol {
  padding-left: 20px;
  margin-bottom: 12px;
}

.knowledge-text li {
  margin-bottom: 8px;
}

.knowledge-text strong {
  color: var(--primary-color, #ff2442);
  font-weight: 600;
}

.knowledge-text a {
  color: var(--primary-color, #ff2442);
  text-decoration: none;
}

.knowledge-text a:hover {
  text-decoration: underline;
}

.knowledge-icon {
  margin-right: 8px;
  font-size: 20px;
}

/* 确保抽屉样式正确 */
:deep(.knowledge-drawer .el-drawer__header) {
  margin-bottom: 0;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  color: var(--primary-color, #ff2442);
  font-weight: 600;
}

:deep(.knowledge-drawer .el-drawer__body) {
  padding: 0;
  overflow-y: auto;
}
</style> 