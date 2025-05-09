<template>
  <div class="weibo-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>微博文章生成</h2>
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
        
        <!-- 内容元素 - 优化复选框布局和视觉效果 -->
        <div class="form-group">
          <label>内容元素</label>
          <div class="checkbox-group">
            <div class="checkbox-item" :class="{'checkbox-active': includeEmoji}">
              <input type="checkbox" id="include-emoji" v-model="includeEmoji">
              <label for="include-emoji" class="checkbox-label">表情符号</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeHashtags}">
              <input type="checkbox" id="include-hashtags" v-model="includeHashtags">
              <label for="include-hashtags" class="checkbox-label">话题标签</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeMention}">
              <input type="checkbox" id="include-mention" v-model="includeMention">
              <label for="include-mention" class="checkbox-label">@提及</label>
            </div>
            <div class="checkbox-item" :class="{'checkbox-active': includeQuestion}">
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
            <div class="example-cards" ref="exampleCarouselRef">
              <div class="example-card" v-for="(example, index) in examples" :key="index" @click="loadExample('example' + (index + 1))">
                <div class="example-card-header">
                  <div class="example-icon">
                    <i :class="example.icon"></i>
                  </div>
                  <div class="example-info">
                    <div class="example-title">{{ example.title }}</div>
                    <div class="example-desc">{{ example.type }}</div>
                  </div>
                </div>
                <div class="example-content" v-if="example.desc">
                  <div class="example-detail">{{ example.desc }}</div>
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
              <button @click="showPrompt" class="primary-button" :disabled="!lastUsedPrompt">
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
              <div class="weibo-phone-mockup">
                <div class="weibo-status-bar">
                  <div class="status-icons">
                    <i class="ri-wifi-line"></i>
                    <i class="ri-signal-wifi-line"></i>
                    <i class="ri-battery-charge-line"></i>
                  </div>
                  <div class="status-time">10:30</div>
                </div>
                <div class="weibo-app-header">
                  <div class="app-back">
                    <i class="ri-arrow-left-s-line"></i>
                  </div>
                  <div class="app-title">微博热门</div>
                  <div class="app-more">
                    <i class="ri-more-line"></i>
                  </div>
                </div>
                <div class="weibo-article-container">
                  <div class="weibo-post">
                    <div class="weibo-header">
                      <div class="weibo-avatar">
                        <i class="ri-user-line"></i>
                      </div>
                      <div class="weibo-user-info">
                        <h4 class="weibo-username">AI助手</h4>
                        <div class="weibo-timestamp">刚刚</div>
                      </div>
                      <div class="weibo-follow-btn">关注</div>
                    </div>
                    <div class="weibo-body" v-html="formatWeiboContent(generatedWeibo)"></div>
                    
                    <!-- 添加模拟图片区域 -->
                    <div v-if="includeEmoji && hasImageContent()" class="weibo-image-container">
                      <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQwIiBoZWlnaHQ9IjI0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbD0iI0YyRjJGMiIgY3g9IjEyMCIgY3k9IjEyMCIgcj0iMTIwIi8+PHBhdGggZD0iTTg2LjQgMTM5LjVjMCAyNi4zIDI3IDQ3LjYgNjAuMyA0Ny42czYwLjMtMjEuMyA2MC4zLTQ3LjZIODYuNHoiIGZpbGw9IiNFMkU1RTciLz48cGF0aCBkPSJNODYuNCAxMjBjMC0zMi4zIDI3LTU4LjUgNjAuMy01OC41czYwLjMgMjYuMiA2MC4zIDU4LjUiIHN0cm9rZT0iI0UyRTVFNyIgc3Ryb2tlLXdpZHRoPSIxOCIvPjxjaXJjbGUgZmlsbD0iIzFEMUQxQiIgY3g9IjExNyIgY3k9IjEyMCIgcj0iOSIvPjxjaXJjbGUgZmlsbD0iIzFEMUQxQiIgY3g9IjE3NiIgY3k9IjEyMCIgcj0iOSIvPjwvZz48L3N2Zz4=" class="weibo-image" alt="示例图片">
                    </div>
                    
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
                      <div class="weibo-stat">
                        <i class="ri-star-line"></i>
                        <span>收藏</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="weibo-interaction-bar">
                  <div class="interaction-item">
                    <i class="ri-home-line"></i>
                    <span>首页</span>
                  </div>
                  <div class="interaction-item">
                    <i class="ri-video-line"></i>
                    <span>视频</span>
                  </div>
                  <div class="interaction-item">
                    <i class="ri-add-circle-line"></i>
                  </div>
                  <div class="interaction-item">
                    <i class="ri-message-3-line"></i>
                    <span>消息</span>
                  </div>
                  <div class="interaction-item">
                    <i class="ri-user-line"></i>
                    <span>我</span>
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
          <h3 class="modal-title">
            <i class="ri-code-line"></i>
            AI提示词
          </h3>
          <div class="modal-actions">
          <button class="primary-button" @click="copyPrompt">
            <i class="ri-file-copy-line"></i>
            复制提示词
          </button>
            <button class="close-btn" @click="showPromptModal = false">&times;</button>
          </div>
        </div>
        <div class="modal-body">
          <pre class="prompt-content">{{ lastUsedPrompt }}</pre>
        </div>
      </div>
    </div>
    
    <!-- 知识学习侧边栏 -->
    <el-drawer
      v-model="showTipsModal"
      title="微博文章创作指南"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in weiboArticleKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import axios from 'axios';
import '@/assets/css/text-creation-common.css'; // 引入统一CSS样式文件
import '@/assets/css/mobile-preview.css'; // 引入手机预览样式文件
import { weiboArticleExamples } from '@/views/example_data.js'; // 导入参考案例数据
import { weiboArticleKnowledge } from '@/views/Knowledge_data.js'; // 导入知识学习数据
import { ref, reactive, toRefs, computed, onMounted } from 'vue';
import { ElDrawer } from 'element-plus'; // 引入Element Plus的Drawer组件

// 检查导入是否成功，如果不成功则提供默认数据
const defaultWeiboKnowledge = [{
  title: '微博创作知识学习',
  tips: [
    '微博内容简洁有力，直入主题效果更好',
    '使用表情符号和话题标签可以增加互动性',
    '提出问题或邀请互动可以提高转发和评论率',
    '图文结合的内容更容易获得关注',
    '紧跟热点话题可以提高微博曝光度',
    '真实生活中的分享往往比抽象观点更有共鸣',
    '保持自己独特的风格和态度，更容易塑造个人品牌'
  ]
}];

export default {
  name: 'WeiboArticle',
  components: {
    ElDrawer
  },
  setup() {
    // 创建DOM引用 - 修复refs问题
    const exampleCarouselRef = ref(null);
    
    // 检查导入的知识数据，如果不可用则使用默认数据
    const knowledgeData = typeof weiboArticleKnowledge !== 'undefined' ? weiboArticleKnowledge : defaultWeiboKnowledge;

    const state = reactive({
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
      selectedModel: 'deepseek-v3', // 设置默认值
      modelList: [],
      
      // 参考案例设置
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      examples: weiboArticleExamples, // 使用导入的参考案例数据
      
      // 添加微博知识学习内容
      weiboArticleKnowledge: weiboArticleKnowledge
    });

    const isLastPage = computed(() => {
      // 计算是否已经滚动到最后一页
      const cardWidth = 185; // 卡片宽度+间距
      const containerWidth = exampleCarouselRef.value?.parentElement?.clientWidth || 0;
      const totalWidth = state.examples.length * cardWidth;
      const maxScrollX = totalWidth - containerWidth;
      
      // 当滚动到最大滚动距离的90%以上时，认为是最后一页
      return Math.abs(state.exampleTranslateX) >= maxScrollX * 0.9;
    });

    const setupDefaultModels = () => {
      state.modelList = [
        { id: 'deepseek-v3', name: 'DeepSeek-V3（火山引擎）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      state.selectedModel = 'deepseek-v3';
    };

    const generateWeibo = async () => {
      if (!validateForm()) return;
      
      state.isGenerating = true;
      state.isLoading = true;
      state.loadingText = 'AI正在创作中，请稍候...';
      state.generatedWeibo = ''; // 清空之前的内容
      
      try {
        // 构建提示词
        const prompt = buildPrompt();
        state.lastUsedPrompt = prompt;
        
        try {
          // 检查是否有可用模型
          if (!state.selectedModel) {
            console.error('未选择模型');
            throw new Error('请选择AI模型');
          }
          
          console.log(`正在调用API，使用模型: ${state.selectedModel}，提示词长度: ${prompt.length}`);
          
          // 构建API请求参数
          const apiParams = {
            model: state.selectedModel,
            messages: [{ role: 'user', content: prompt }],
            temperature: 0.7,
            max_tokens: getMaxTokensByLength(state.weiboLength),
            stream: true // 启用流式输出
          };
          
          // 记录API请求详情，方便调试
          console.log('API请求参数:', JSON.stringify(apiParams));
          
          // 使用fetch API处理流式响应
          const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'text/event-stream'
            },
            body: JSON.stringify(apiParams)
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          console.log('开始接收流式响应...');
          
          // 获取响应的reader
          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let buffer = ''; // 用于存储不完整的数据块
          
          while (true) {
            const { value, done } = await reader.read();
            if (done) {
              console.log('Reader 已完成');
              break;
            }
            
            const chunk = decoder.decode(value, { stream: true });
            console.log('收到数据块:', chunk);
            
            // 将新块添加到缓冲区
            buffer += chunk;
            
            // 尝试处理完整的SSE消息
            let processedBuffer = processSSEMessages(buffer);
            
            // 更新缓冲区为未处理的部分
            buffer = processedBuffer;
          }
          
          console.log('流式响应完成');
          
          // 如果到此时还没有内容，则尝试离线生成
          if (!state.generatedWeibo || state.generatedWeibo.trim() === '') {
            console.warn('未能从API获取内容，切换到离线模式');
            state.generatedWeibo = getOfflineGeneratedWeibo();
            state.$message && state.$message.warning('未能从服务器获取内容，使用离线模式生成');
          } else {
            state.$message && state.$message.success('已成功调用后端大模型生成内容');
          }
          
        } catch (error) {
          console.error('API调用异常:', error);
          
          // 判断是否是网络错误或服务器不可用
          if (error.name === 'AbortError' || !error.response || error.message.includes('Network Error')) {
            console.warn('后端服务不可用，切换到离线模式');
            // 离线模式
            state.generatedWeibo = getOfflineGeneratedWeibo();
            state.$message && state.$message.warning('后端服务不可用，使用离线模式生成内容');
          } else {
            // 其他API错误
            throw error;
          }
        }
      } catch (error) {
        console.error('生成微博出错:', error);
        state.generatedWeibo = '抱歉，服务器暂时无法响应，请稍后再试';
        
        // 开发环境下提供测试数据
        if (process.env.NODE_ENV === 'development') {
          setTimeout(() => {
            state.generatedWeibo = getOfflineGeneratedWeibo();
          }, 1000);
        }
      } finally {
        state.isGenerating = false;
        state.isLoading = false;
      }
    };

    const buildPrompt = () => {
      let prompt = `请你扮演一位专业的社交媒体内容创作者，为我创作一条原创微博。\n\n`;
      
      // 添加微博类型
      const typeMap = {
        trending: '热点话题',
        lifestyle: '生活日常',
        review: '产品测评',
        humor: '幽默段子',
        question: '提问互动'
      };
      prompt += `微博类型：${typeMap[state.weiboType]}\n`;
      
      // 添加主题和目标受众
      prompt += `微博主题：${state.weiboTitle}\n`;
      prompt += `目标受众：${state.targetAudience}\n`;
      
      // 添加关键词
      prompt += `内容要点：${state.weiboKeywords}\n`;
      
      // 添加风格和长度
      const styleMap = {
        casual: '轻松日常',
        humorous: '幽默诙谐',
        professional: '专业正式',
        emotional: '情感充沛',
        sarcastic: '讽刺调侃'
      };
      prompt += `语言风格：${styleMap[state.writingStyle]}\n`;
      
      const lengthMap = {
        short: '简短 (50字以内)',
        medium: '中等 (50-100字)',
        long: '较长 (100-200字)',
        'super-long': '超长 (200-500字)'
      };
      prompt += `微博长度：${lengthMap[state.weiboLength]}\n`;
      
      // 添加内容元素需求
      prompt += `内容元素要求：\n`;
      if (state.includeEmoji) prompt += `- 请在适当的地方添加表情符号\n`;
      if (state.includeHashtags) prompt += `- 请添加1-3个相关话题标签，格式为 #话题#\n`;
      if (state.includeMention) prompt += `- 可以适当添加@某人的元素\n`;
      if (state.includeQuestion) prompt += `- 请在微博末尾添加互动性提问\n`;
      
      // 添加其他要求
      if (state.additionalRequirements) {
        prompt += `其他特殊要求：${state.additionalRequirements}\n`;
      }
      
      // 最后的格式说明
      prompt += `\n请直接输出微博内容，不需要添加任何额外解释。确保内容原创、有吸引力，符合微博平台的表达习惯。`;
      
      return prompt;
    };

    const getMaxTokensByLength = (length) => {
      const tokenMap = {
        short: 100,
        medium: 200,
        long: 300,
        'super-long': 500
      };
      return tokenMap[length] || 200;
    };

    const validateForm = () => {
      if (!state.weiboTitle) {
        alert('请输入微博主题');
        return false;
      }
      if (!state.targetAudience) {
        alert('请输入目标读者群体');
        return false;
      }
      if (!state.weiboKeywords) {
        alert('请输入微博关键词或内容要点');
        return false;
      }
      return true;
    };

    const resetForm = () => {
      state.weiboTitle = '';
      state.targetAudience = '';
      state.weiboKeywords = '';
      state.writingStyle = 'casual';
      state.weiboLength = 'medium';
      state.additionalRequirements = '';
      state.includeEmoji = true;
      state.includeHashtags = true;
      state.includeMention = false;
      state.includeQuestion = true;
    };

    const copyResult = () => {
      if (!state.generatedWeibo) return;
      
      navigator.clipboard.writeText(state.generatedWeibo)
        .then(() => {
          alert('微博内容已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          alert('复制失败，请手动复制');
        });
    };

    const copyPrompt = () => {
      if (!state.lastUsedPrompt) return;
      
      try {
        // 检查是否支持clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(state.lastUsedPrompt)
            .then(() => {
              alert('提示词已复制到剪贴板');
            })
        .catch(err => {
          console.error('复制失败:', err);
              fallbackCopy(state.lastUsedPrompt);
            });
        } else {
          // 浏览器不支持clipboard API，使用备选方法
          fallbackCopy(state.lastUsedPrompt);
        }
      } catch (error) {
        console.error('复制操作异常:', error);
        fallbackCopy(state.lastUsedPrompt);
      }
    };

    // 备选的复制方法
    const fallbackCopy = (text) => {
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
          alert('提示词已复制到剪贴板');
        } else {
          alert('复制失败，请手动复制');
        }
        
        // 清理临时元素
        document.body.removeChild(textArea);
      } catch (err) {
        console.error('备选复制方法失败:', err);
        alert('复制失败，请手动复制文本');
      }
    };

    const showPrompt = () => {
      if (!state.lastUsedPrompt) return;
      state.showPromptModal = true;
    };

    const showTips = () => {
      state.showTipsModal = true;
    };

    const prevExample = () => {
      if (state.currentExampleIndex > 0) {
        state.currentExampleIndex--;
        updateExampleCarousel();
      }
    };

    const nextExample = () => {
      const carouselEl = document.querySelector('.example-carousel');
      const cardWidth = 220; // 调整为与CSS中定义的卡片宽度一致
      const maxVisibleCards = carouselEl ? Math.floor(carouselEl.clientWidth / cardWidth) : 1;
      const maxIndex = state.examples.length - maxVisibleCards;
      
      if (state.currentExampleIndex < maxIndex) {
        state.currentExampleIndex++;
        updateExampleCarousel();
      }
    };

    const updateExampleCarousel = () => {
      const cardWidth = 220; // 调整为与CSS中定义的卡片宽度一致
      state.exampleTranslateX = -state.currentExampleIndex * cardWidth;
      if (exampleCarouselRef.value) {
        exampleCarouselRef.value.style.transform = `translateX(${state.exampleTranslateX}px)`;
        exampleCarouselRef.value.style.transition = 'transform 0.3s ease';
      }
    };

    const loadExample = (exampleId) => {
      // 解析示例编号
      const index = parseInt(exampleId.replace('example', '')) - 1;
      if (index < 0 || index >= state.examples.length) return;
      
      // 获取示例内容
      const example = state.examples[index];
      if (!example) return;
      
      console.log('加载示例:', index, example);
      
      // 设置微博参数
      state.weiboType = example.weiboType || 'trending';
      state.weiboTitle = example.title;
      state.targetAudience = example.desc.includes('爱好者') ? 
                             example.desc.split('爱好者')[0] + '爱好者' : 
                             example.desc.split('的')[0] + '关注者';
      state.weiboKeywords = example.desc;
      state.writingStyle = example.writingStyle || 'casual';
      state.weiboLength = 'medium';
      
      // 根据微博类型设置合适的内容元素
      if (state.weiboType === 'question') {
        state.includeQuestion = true;
      } else if (state.weiboType === 'humor') {
        state.includeEmoji = true;
        state.writingStyle = 'humorous';
      } else if (state.weiboType === 'review') {
        state.includeRating = true;
        state.includeProsCons = true;
      }
      
      console.log('已设置参数:', {
        type: state.weiboType,
        title: state.weiboTitle,
        audience: state.targetAudience,
        keywords: state.weiboKeywords,
        style: state.writingStyle
      });
    };

    // 添加formatMarkdown方法
    const formatMarkdown = (text) => {
      if (!text) return '';
      
      // 处理加粗文本
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理列表项
      text = text.replace(/\n\n/g, '<br><br>');
      
      return text;
    };

    const getOfflineGeneratedWeibo = () => {
      // 简化模拟数据，每种类型只保留一个示例
      const samples = {
        'review': `刚入手的新款蓝牙耳机体验分享！🎧 降噪效果真的惊艳到我，地铁上嘈杂声瞬间消失，仿佛拥有了专属小宇宙！续航给我惊到，重度使用三天都不用充电！透明模式下交流完全不受影响，音质也相当不错👍 #数码好物推荐# #蓝牙耳机推荐# 你们用过这款吗？感觉如何？`,
        
        'trending': `《流浪地球2》今天二刷回来…真的被国产科幻片的进步震撼到了！特效已经完全不输好莱坞，剧情更是紧凑到让人窒息😱。最震撼的还是那种面对毁灭时的东方式浪漫与坚韧，看完莫名感到心安。中国科幻电影的未来，好像一下子就有了更多可能性✨。#流浪地球2# #国产科幻电影# 你们看了吗？最喜欢哪个片段？`,
        
        'lifestyle': `#2023职场感悟# 这周终于啃下了那个困扰团队半个月的技术难题！熬夜加班的疲惫一扫而空，成就感真的是工作中最好的续航能量了✨。感谢团队每个人的付出，单打独斗永远不如众人拾柴。职场中最重要的，与其说是个人能力，不如说是解决问题的决心和团队协作的默契。你们职场中遇到过最有成就感的时刻是什么？一起分享吧！👇`,
        
        'humor': `今天在公司茶水间听到两位同事聊天：\n"你知道AI为什么这么火吗？"\n"为什么？"\n"因为它不用996，不用交五险一金，不用年终述职，不吃不喝不休假还不辞职！"\n"那我们岂不是要失业了？😱"\n"放心，我们还有一个无可替代的优势..."\n"什么优势？"\n"我们会喝奶茶啊！" 🧋\n#职场段子# #AI时代# 你们觉得AI会取代哪些工作？`,
        
        'question': `世界杯1/4决赛也太刺激了吧！😱 梅西那脚助攻简直神来之笔，看得我从沙发上跳起来！C罗那个表情，心都要碎了。足球就是这样，一瞬间可以改变一切。突然意识到这可能是这两位球王同台的最后一届世界杯了…有点舍不得😢 #卡塔尔世界杯# #梅西C罗# 大家支持哪个队夺冠啊？评论区告诉我！⚽`
      };
      
      return samples[state.weiboType] || `今天的阳光也太好了吧！☀️ 午休时在公司楼下晒了会太阳，整个人都元气满满！这种初春的温暖真的很治愈，感觉冬天的阴霾一扫而空～生活中这种小确幸真的很重要。#春日分享# #生活碎片# 你们今天的小确幸是什么呢？`;
    };

    const formatWeiboContent = (content) => {
      if (!content) return '';
      
      // 高亮话题标签 #xxx#
      let formatted = content.replace(/#([^#]+)#/g, '<span class="weibo-hashtag">#$1#</span>');
      
      // 高亮@提及
      formatted = formatted.replace(/@([a-zA-Z0-9_\u4e00-\u9fa5]+)/g, '<span class="weibo-mention">@$1</span>');
      
      // 保留换行符
      formatted = formatted.replace(/\n/g, '<br>');
      
      return formatted;
    };

    const hasImageContent = () => {
      // 这里可以根据内容类型或关键词判断是否需要显示图片
      // 示例：如果是产品测评类型，或内容包含"图片"关键词，则显示图片
      return state.weiboType === 'review' || state.generatedWeibo?.includes('图片') || 
             (state.weiboType === 'lifestyle' && Math.random() > 0.5);
    };

    // 添加处理SSE消息的函数
    const processSSEMessages = (buffer) => {
      // 寻找完整的SSE消息（以\n\n分隔）
      const messages = buffer.split('\n\n');
      
      // 如果最后一块不是完整的（没有以\n\n结尾），保留它
      const incompleteChunk = buffer.endsWith('\n\n') ? '' : messages.pop();
      
      for (const message of messages) {
        if (!message.trim()) continue; // 跳过空消息
        
        // 记录原始消息用于调试
        console.log('处理SSE消息:', message);
        
        // 处理data:前缀的行
        if (message.startsWith('data:')) {
          const content = message.substring(5).trim();
          
          // 检查是否为结束标记
          if (content === '[DONE]') {
            console.log('流式响应已完成');
            continue;
          }
          
          try {
            const data = JSON.parse(content);
            console.log('解析的JSON数据:', data);
            
            // 尝试多种可能的数据格式
            let textContent = '';
            
            // 格式1: OpenAI格式 - choices[0].delta.content
            if (data.status === 'success' && data.data?.choices?.[0]?.delta?.content) {
              textContent = data.data.choices[0].delta.content;
            } 
            // 格式2: 简化格式 - content直接在顶层
            else if (data.content) {
              textContent = data.content;
            }
            // 格式3: data.choices[0].delta.content (没有status包装)
            else if (data.choices?.[0]?.delta?.content) {
              textContent = data.choices[0].delta.content;
            }
            // 格式4: data.choices[0].text 格式
            else if (data.choices?.[0]?.text) {
              textContent = data.choices[0].text;
            }
            // 格式5: data.text 格式
            else if (data.text) {
              textContent = data.text;
            }
            
            if (textContent) {
              console.log('提取到内容:', textContent);
              state.generatedWeibo += textContent;
            }
          } catch (e) {
            console.warn('解析JSON失败:', e, '原始内容:', content);
            
            // 如果不是JSON，可能是直接返回的文本
            if (content && content !== '[DONE]' && !content.includes('{') && !content.includes('[')) {
              console.log('直接使用非JSON内容:', content);
              state.generatedWeibo += content;
            }
          }
        }
      }
      
      return incompleteChunk;
    };

    // 在组件挂载后加载模型列表
    onMounted(() => {
      // 设置默认模型列表，防止等待API返回时界面显示"加载中"
      setupDefaultModels();
      // 然后尝试从API加载
      // loadModels(); // 如果有API加载函数，可以取消注释
    });

    return {
      ...toRefs(state),
      isLastPage,
      setupDefaultModels,
      generateWeibo,
      buildPrompt,
      getMaxTokensByLength,
      validateForm,
      resetForm,
      copyResult,
      copyPrompt,
      showPrompt,
      showTips,
      prevExample,
      nextExample,
      updateExampleCarousel,
      loadExample,
      getOfflineGeneratedWeibo,
      formatWeiboContent,
      hasImageContent,
      exampleCarouselRef,
      formatMarkdown
    };
  }
};
</script>

<style scoped>
/* 引入统一样式文件 */
@import "@/assets/css/text-creation-common.css";

/* 只保留特定于WeiboArticle的样式，其余使用统一样式 */

/* 参考案例部分优化 */
.example-carousel {
  overflow: hidden;
}

.example-cards {
  display: flex;
  gap: 20px;
  padding: 10px 0;
}

/* 确保每个卡片有适当的边距和宽度 */
.example-card {
  min-width: 200px;
  margin-right: 0; /* 移除右边距，使用gap代替 */
}

/* 微博特有样式 */
.weibo-result {
  padding: 20px;
  display: flex;
  justify-content: center;
}

/* 微博内容元素样式 */
.weibo-hashtag {
  color: #eb7350;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.weibo-hashtag:hover {
  color: #ba003f;
  text-decoration: underline;
}

.weibo-mention {
  color: #1da1f2;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.weibo-mention:hover {
  color: #0c85d0;
  text-decoration: underline;
}

/* 微博图片容器样式 */
.weibo-image-container {
  margin: 10px 0 12px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f2f2f2;
}

.weibo-image {
  width: 100%;
  display: block;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.weibo-image:hover {
  transform: scale(1.02);
}

/* 改进微博内容样式 */
.weibo-body {
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 12px;
  white-space: pre-wrap;
  word-break: break-word;
  letter-spacing: 0.3px;
  padding: 0 12px; /* 添加左右内边距 */
}

/* 增加微博文章容器内边距 */
.weibo-post {
  padding: 0 10px; /* 添加左右内边距 */
}

.weibo-article-container {
  padding: 0 5px; /* 添加容器内边距 */
}

/* 手机预览样式已在mobile-preview.css中定义 */

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

/* 模态框头部样式 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-title {
  margin: 0;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.prompt-content {
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.5;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
}
</style> 
