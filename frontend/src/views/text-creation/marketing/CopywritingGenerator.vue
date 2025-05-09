<template>
  <div class="marketing-copy-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>营销文案生成</h2>
      </div>
      <div class="page-actions">
        <div class="learn-button" @click="showTipsModal = true">
          <i class="ri-lightbulb-flash-line"></i>
          <span>知识学习</span>
        </div>
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
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无文案，请点击"生成文案"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedCopy" class="copy-result" :class="{'blur-content': isLoading, 'streaming': isStreaming}">
              <!-- 添加离线模式提示条 -->
              <div v-if="isOfflineGenerated" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板文案。要获得AI生成的更优质文案，请联系管理员启动后端服务。</span>
              </div>
              
              <!-- 简单内容展示区 -->
              <div class="content-display-container">
                <div class="pad-status-icons">
                  <div class="pad-status-icon wifi"></div>
                  <div class="pad-status-icon"></div>
                  <div class="pad-status-icon battery"></div>
                </div>
                <div class="pad-screen-glare"></div>
                <div class="content-display" v-html="formattedCopy"></div>
                <div v-if="isStreaming" class="streaming-indicator">
                  <span class="dot-typing"></span>
                </div>
                <div class="pad-home-button"></div>
              </div>
              
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态框 -->
    <el-drawer
      v-model="showTipsModal"
      title="营销文案创作指南"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in copywritingKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
        </div>
    </el-drawer>
    
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
import '@/assets/css/text-creation-common.css'

// 创建axios实例，配置baseURL
const apiClient = axios.create({
  baseURL: window.APP_CONFIG.API_BASE_URL, // 后端服务地址
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
      selectedModel: 'deepseek-v3',
      isGenerating: false,
      isLoading: false,
      loadingText: '正在生成文案...',
      validationErrors: [],
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      isStreaming: false, // 添加流式输出状态标记
      // 添加营销文案知识内容
      copywritingKnowledge: [
        {
          subtitle: '营销文案的定义与重要性',
          icon: 'ri-question-line',
          text: '营销文案是指为推广产品、服务或品牌而创作的文字内容。它是营销传播的核心组成部分，直接影响消费者对产品的认知和购买决策。优秀的营销文案能够准确传达产品价值，引发目标受众共鸣，并促使其采取行动。在当今信息爆炸的时代，有效的营销文案是品牌脱颖而出的关键。'
        },
        {
          subtitle: '营销文案的理论基础',
          icon: 'ri-book-line',
          text: '**AIDA模型**：引起注意(Attention)→激发兴趣(Interest)→激发欲望(Desire)→促成行动(Action)，是经典的营销文案结构模型。\n\n**FAB原则**：特点(Feature)→优势(Advantage)→效益(Benefit)，强调从产品特点到用户实际获益的转化逻辑。\n\n**USP理论**：独特销售主张(Unique Selling Proposition)，强调产品独特的竞争优势。\n\n**情感诉求理论**：通过触发情感共鸣建立品牌与消费者的情感连接。\n\n**社会认同原则**：利用消费者从众心理，通过他人的认可增强说服力。'
        },
        {
          subtitle: '营销文案的类型与结构',
          icon: 'ri-folder-line',
          text: '**产品介绍文案**：详细描述产品特点、功能和优势，帮助用户全面了解产品。\n\n**品牌故事文案**：讲述品牌起源、理念和价值观，增强品牌情感连接。\n\n**社交媒体文案**：简短、有趣、易传播的内容，适合在社交平台分享。\n\n**电子邮件营销文案**：包含引人注目的主题行和促使用户点击的内容。\n\n**落地页文案**：引导用户完成转化的页面文案，包含清晰的行动号召。\n\n**SEO文案**：优化搜索引擎排名的内容，合理包含关键词。\n\n**促销活动文案**：强调优惠力度和紧迫感，促使用户快速行动。'
        },
        {
          subtitle: '营销文案的基本要素',
          icon: 'ri-layout-line',
          text: '**标题**：抓住注意力的第一关，应具有吸引力和独特性。\n\n**开场**：快速建立联系，明确价值主张。\n\n**正文**：详细阐述产品优势，解决用户痛点。\n\n**证明**：提供数据、案例和用户见证增强可信度。\n\n**承诺**：明确产品将为用户带来的价值和保证。\n\n**行动号召(CTA)**：明确指导用户下一步行动，如"立即购买"、"免费试用"等。\n\n**紧迫感**：创造限时、限量的稀缺感，促使用户迅速行动。'
        },
        {
          subtitle: '文案写作的专业技巧',
          icon: 'ri-pen-nib-line',
          text: '**目标受众分析**：深入了解目标用户的需求、痛点和语言习惯。\n\n**独特价值提炼**：明确产品与竞品的差异化优势。\n\n**情感触发**：选择适合的情感元素，如希望、恐惧、成就感等。\n\n**故事化表达**：通过故事情节增强代入感和记忆点。\n\n**简洁明了**：使用清晰、简洁的语言，避免行业术语和冗长表达。\n\n**突出主要卖点**：集中强调最核心的2-3个产品优势。\n\n**数据支持**：适当引用具体数据增强说服力。\n\n**消除顾虑**：预先解答潜在疑问，降低购买障碍。'
        },
        {
          subtitle: '数字化时代的营销文案趋势',
          icon: 'ri-global-line',
          text: '**个性化文案**：基于用户数据和行为，提供定制化的营销信息。\n\n**对话式文案**：模拟真实对话，增强亲和力和互动性。\n\n**沉浸式体验**：结合视频、图像等多媒体元素，创造全方位感官体验。\n\n**价值导向**：从单纯推销产品转向提供有价值的内容和解决方案。\n\n**社会责任**：融入环保、可持续发展等社会议题，与消费者建立价值共鸣。\n\n**AI辅助创作**：利用人工智能技术提高文案创作效率和针对性。\n\n**数据驱动优化**：通过A/B测试和数据分析持续优化文案效果。'
        },
        {
          subtitle: '不同行业的文案特点',
          icon: 'ri-briefcase-line',
          text: '**科技行业**：强调创新性、技术优势和用户体验，注重专业术语与通俗表达的平衡。\n\n**教育行业**：突出学习成果和未来发展，激发成长动力和自我提升愿望。\n\n**健康医疗**：注重专业权威性和解决实际健康问题，同时满足监管要求。\n\n**金融服务**：强调安全性、稳定性和收益潜力，清晰解释复杂金融概念。\n\n**时尚美妆**：营造品牌调性和生活方式，重视视觉元素与文案的协调。\n\n**餐饮食品**：通过感官描述激发食欲，突出食材品质和独特口味。\n\n**旅游服务**：描绘目的地体验和情感价值，激发探索欲和度假需求。'
        }
      ],
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
      
      // 将文本分成不同部分（标题、正文等）
      const lines = this.generatedCopy.split('\n').map(line => line.trim()).filter(line => line);
      let result = '';
      
      // 检查第一行是否是标题（以"#"开头或者没有标点的短句）
      let hasTitle = false;
      if (lines.length > 0) {
        const firstLine = lines[0];
        if (firstLine.startsWith('#') || (firstLine.length < 30 && !firstLine.match(/[.,:;?!。，：；？！]/))) {
          // 是标题，特殊处理
          // 当标题中包含产品名称时自动加粗
          let titleText = firstLine.replace(/^#+\s*/, '');
          if (this.productName && titleText.includes(this.productName)) {
            titleText = titleText.replace(
              this.productName,
              `<strong class="product-highlight">${this.productName}</strong>`
            );
          }
          result += `<div class="poster-title">${titleText}</div>`;
          hasTitle = true;
          lines.shift(); // 移除已处理的标题行
        }
      }
      
      // 检查副标题（如果有标题且下一行较短）
      let hasSubtitle = false;
      if (hasTitle && lines.length > 0 && lines[0].length < 50 && !lines[0].startsWith('#')) {
        result += `<div class="poster-subtitle">${lines[0]}</div>`;
        hasSubtitle = true;
        lines.shift(); // 移除已处理的副标题行
      }
      
      // 添加海报装饰元素和背景
      result = `<div class="poster-container">
        <div class="poster-corner poster-corner-tl"></div>
        <div class="poster-corner poster-corner-tr"></div>
        <div class="poster-corner poster-corner-bl"></div>
        <div class="poster-corner poster-corner-br"></div>
        <div class="poster-background-overlay"></div>
        ${result}
        <div class="poster-accent-line"></div>
        <div class="poster-ribbon"></div>
        <div class="poster-content">
      `;
      
      // 处理剩余的段落
      const paragraphs = [];
      let currentParagraph = '';
      
      for (const line of lines) {
        // 如果是标题，创建新的标题元素
        if (line.startsWith('#')) {
          if (currentParagraph) {
            paragraphs.push(`<p>${currentParagraph}</p>`);
            currentParagraph = '';
          }
          
          const level = (line.match(/^#+/) || ['#'])[0].length;
          let titleText = line.replace(/^#+\s*/, '');
          
          // 为标题中的产品名称和品牌名称添加强调
          if (this.productName && titleText.includes(this.productName)) {
            titleText = titleText.replace(
              this.productName,
              `<strong class="product-highlight">${this.productName}</strong>`
            );
          }
          
          if (level === 1) {
            paragraphs.push(`<h2 class="poster-section-title">${titleText}</h2>`);
          } else {
            paragraphs.push(`<h3 class="poster-section-subtitle">${titleText}</h3>`);
          }
        } 
        // 检查是否是列表项
        else if (line.match(/^[-*•]\s+/)) {
          if (currentParagraph) {
            paragraphs.push(`<p>${currentParagraph}</p>`);
            currentParagraph = '';
          }
          
          // 提取列表项文本并添加到结果中
          let listItemText = line.replace(/^[-*•]\s+/, '');
          
          // 为列表项中的产品名称和品牌名称添加强调
          if (this.productName && listItemText.includes(this.productName)) {
            listItemText = listItemText.replace(
              this.productName,
              `<strong class="product-highlight">${this.productName}</strong>`
            );
          }
          
          paragraphs.push(`<div class="poster-list-item"><span class="poster-bullet">•</span>${listItemText}</div>`);
        }
        // 强调文本（引号包围）
        else if (line.match(/^["'"「].*[""'」]$/)) {
          if (currentParagraph) {
            paragraphs.push(`<p>${currentParagraph}</p>`);
            currentParagraph = '';
          }
          paragraphs.push(`<div class="poster-quote">${line}</div>`);
        }
        // 普通段落
        else {
          if (line.endsWith('.') || line.endsWith('。') || line.endsWith('!') || line.endsWith('！') || 
              line.endsWith('?') || line.endsWith('？') || line.length > 50) {
            // 完整句子，添加为新段落
            if (currentParagraph) {
              currentParagraph += ' ' + line;
              
              // 添加简单文本强调：为产品名称添加强调
              let processedText = currentParagraph;
              if (this.productName && processedText.includes(this.productName)) {
                processedText = processedText.replace(
                  new RegExp(this.productName, 'g'),
                  `<strong class="product-highlight">${this.productName}</strong>`
                );
              }
              
              paragraphs.push(`<p>${processedText}</p>`);
              currentParagraph = '';
            } else {
              // 对单行文本也应用相同的强调处理
              let processedText = line;
              if (this.productName && processedText.includes(this.productName)) {
                processedText = processedText.replace(
                  new RegExp(this.productName, 'g'),
                  `<strong class="product-highlight">${this.productName}</strong>`
                );
              }
              
              paragraphs.push(`<p>${processedText}</p>`);
            }
          } else {
            // 短句，可能是段落的一部分
            if (currentParagraph) {
              currentParagraph += ' ' + line;
            } else {
              currentParagraph = line;
            }
          }
        }
      }
      
      // 添加最后剩余的段落
      if (currentParagraph) {
        // 对最后的段落也应用强调处理
        let processedText = currentParagraph;
        if (this.productName && processedText.includes(this.productName)) {
          processedText = processedText.replace(
            new RegExp(this.productName, 'g'),
            `<strong class="product-highlight">${this.productName}</strong>`
          );
        }
        
        paragraphs.push(`<p>${processedText}</p>`);
      }
      
      // 将所有段落添加到结果中
      result += paragraphs.join('');
      
      // 添加品牌签名和装饰元素
      if (this.brandName) {
        result += `<div class="poster-brand">
          <span class="poster-brand-prefix">by</span> 
          <span class="brand-name">${this.brandName}</span>
        </div>`;
      }
      
      // 添加行业标签（如果有）
      if (this.industry) {
        result += `<div class="poster-tag">${this.industry}</div>`;
      }
      
      // 检测文案底部的字数统计信息
      const lastParagraph = paragraphs[paragraphs.length - 1];
      if (lastParagraph && lastParagraph.match(/【字数统计：\d+字】/)) {
        result = result.replace(/【字数统计：\d+字】/, '');
        result += `<div class="poster-word-count">字数统计：${this.generatedCopy.match(/【字数统计：(\d+)字】/)?.[1] || ''}字</div>`;
      }
      
      // 添加底部装饰和海报效果
      result += `<div class="poster-shadow-inner"></div>
                <div class="poster-footer-decoration"></div>
              </div>
              <div class="poster-decoration"></div>
              <div class="poster-shine-effect"></div>
            </div>`;
      
      return result;
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
            'deepseek-r1',  // DeepSeek-R1（火山引擎）- 放在第一位
            'deepseek-v3',  // DeepSeek-V3（火山引擎）
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
          this.selectedModel = 'deepseek-v3';
          
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
        { id: 'deepseek-r1', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-v3', name: 'DeepSeek-V3（火山引擎）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3';
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
        // 清空之前的生成结果
        this.generatedCopy = '';
        this.isOfflineGenerated = false;
        
        // 构建提示词
        const prompt = this.buildPrompt();
        
        // 调用API并获取结果
        const result = await this.callLLMApi(prompt);
        
        // 不需要再次设置generatedCopy，因为在流式输出中已经设置了
        // 只需设置离线模式标志
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
      console.log('===== 调用LLM API开始 =====');
      console.log('当前isStreaming状态:', this.isStreaming);
      console.log('当前generatedCopy长度:', this.generatedCopy ? this.generatedCopy.length : 0);
      
      try {
        // 检查是否有可用模型
        if (!this.selectedModel) {
          console.error('未选择模型');
          throw new Error('请选择AI模型');
        }
        
        console.log(`正在调用API，使用模型: ${this.selectedModel}，提示词长度: ${prompt.length}`);
        
        // 准备所有消息历史
        const messages = [{ role: 'user', content: prompt }];
        
        // 构建API请求参数
        const apiParams = {
          model: this.selectedModel,
          messages: messages,
          stream: true,
          temperature: 0.7,
          max_tokens: 2000,
          return_reasoning: this.selectedModel.includes('r1') // 如果是R1模型，则启用思考过程
        };
        
        // 记录API请求详情，方便调试
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        try {
          // 重置生成的内容已经在generateCopy方法中完成
          // 开始流式状态
          this.isStreaming = true;
          
          // 发送API请求，使用fetch API来处理流式响应
          console.log('开始发送流式请求到:', '/api/v1/v1/deepseek_volcano/chat');
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
              console.log('流式响应完成');
              break;
            }
            
            // 解码二进制数据
            const decoded = decoder.decode(value, { stream: true });
            console.log('收到数据块:', decoded.length, '字节');
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
                  console.log('解析数据:', data.substring(0, 100) + '...');
                  const parsed = JSON.parse(data);
                  console.log('解析后的数据格式:', Object.keys(parsed));
                  
                  // 处理错误消息
                  if (parsed.error) {
                    console.error("API错误:", parsed.error);
                    throw new Error(parsed.error.message || '生成文案失败');
                  }
                  
                  // 处理火山引擎返回的delta格式数据
                  if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                    const delta = parsed.choices[0].delta;
                    
                    // 处理思考过程（如果有）
                    if (delta.reasoning_content) {
                      console.log("收到思考过程:", delta.reasoning_content);
                      // 这里可以添加思考过程的处理逻辑，如果需要的话
                    }
                    
                    // 处理内容增量
                    if (delta.content) {
                      console.log("收到内容增量:", delta.content);
                      // 累加收到的内容
                      this.generatedCopy += delta.content;
                    }
                  }
                  // 处理标准格式的思考过程
                  else if (parsed.reasoning) {
                    console.log("收到标准思考过程:", parsed.reasoning);
                    // 这里可以添加思考过程的处理逻辑，如果需要的话
                  }
                  // 处理完整思考过程
                  else if (parsed.full_reasoning) {
                    console.log("收到完整思考过程");
                    // 这里可以添加完整思考过程的处理逻辑，如果需要的话
                  }
                  // 如果是包含使用情况统计的最后一个数据块，不需要特殊处理
                } catch (e) {
                  console.error('解析流式数据失败:', e, data);
                }
              }
            }
          }
          
          // 处理完成，移除流式状态
          this.isStreaming = false;
          
          return {
            text: this.generatedCopy,
            offlineMode: false
          };
          
        } catch (error) {
          console.error('API调用异常:', error);
          // 结束流式状态
          this.isStreaming = false;
          
          // 判断是否是网络错误或服务器不可用
          if (error.code === 'ECONNABORTED' || !error.response || error.message.includes('Network Error')) {
            console.warn('后端服务不可用，切换到离线模式');
            // 离线模式
            const offlineContent = await this.generateOfflineContent();
            this.generatedCopy = offlineContent.text; // 设置离线生成的内容
            return offlineContent;
          }
          
          // 其他API错误
          throw error;
        }
      } catch (error) {
        console.error('营销文案生成失败:', error);
        // 确保结束流式状态
        this.isStreaming = false;
        
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
    },
    
    // 格式化Markdown文本
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗
      let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理斜体
      formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
      
      // 处理换行
      formatted = formatted.replace(/\n\n/g, '<br><br>');
      
      // 处理列表
      formatted = formatted.replace(/- (.*?)(?:\n|$)/g, '<li>$1</li>');
      formatted = formatted.replace(/<li>/g, '<ul><li>').replace(/<\/li>(?!<li>)/g, '</li></ul>');
      formatted = formatted.replace(/<\/ul><ul>/g, '');
      
      // 处理数字列表
      formatted = formatted.replace(/(\d+)\. (.*?)(?:\n|$)/g, '<li>$1. $2</li>');
      
      return formatted;
    },
    
    // 获取提示词模板
    getPromptTemplate() {
      // 这里应该返回提示词模板的内容
      return '';
    },
    
    // 检查内容是否可滚动
    checkScrollable() {
      this.$nextTick(() => {
        const contentEl = document.querySelector('.content-display');
        if (contentEl) {
          if (contentEl.scrollHeight > contentEl.clientHeight) {
            contentEl.classList.add('scrollable');
          } else {
            contentEl.classList.remove('scrollable');
          }
        }
      });
    }
  },
  
  // 在内容更新后检查是否可滚动
  updated() {
    this.checkScrollable();
  },
  
  // 监听生成的文案变化
  watch: {
    generatedCopy() {
      this.checkScrollable();
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
  /* 删除顶部的灰色虚线 */
  border-top: none;
  border-bottom: none;
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
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 15px 0;
  color: #ba003f; /* 紫荆红色 */
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.section-title i {
  margin-right: 8px;
  font-size: 20px;
  color: #ba003f; /* 紫荆红色 */
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
  padding: 15px 20px; /* 增加左右内边距 */
  border-bottom: 1px solid #eee;
  background-color: #f9f9f9;
  border-radius: 8px 8px 0 0;
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
  background-color: white;
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
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
  margin-bottom: 15px;
  padding: 0 15px;
  /* 移除sticky定位 */
  position: relative;
  top: auto;
  z-index: auto;
  background: transparent;
  border-bottom: none;
  box-shadow: none;
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
  opacity: 0.8;
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

/* 恢复和增强海报样式 */
/* 海报容器 */
.poster-container {
  position: relative;
  background: linear-gradient(135deg, #ffffff, #f5f5f5);
  border-radius: 12px;
  overflow: hidden;
  color: #333;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  margin: 10px 0;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  background-image: 
    radial-gradient(circle at 90% 10%, rgba(186, 0, 63, 0.03) 10%, transparent 10.5%),
    radial-gradient(circle at 10% 90%, rgba(186, 0, 63, 0.03) 10%, transparent 10.5%),
    linear-gradient(135deg, #ffffff, #f9f9f9);
  padding-bottom: 30px; /* 添加底部间距 */
}

.poster-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 15% 15%, rgba(186, 0, 63, 0.01) 5%, transparent 5.5%),
    radial-gradient(circle at 85% 85%, rgba(186, 0, 63, 0.01) 5%, transparent 5.5%);
  pointer-events: none;
}

/* 首字放大效果 */
.poster-content p:first-of-type::first-letter {
  font-size: 200%;
  color: var(--primary-color, #ba003f);
  font-weight: bold;
  float: left;
  margin-right: 6px;
  line-height: 1;
}

/* 段落强调线 */
.poster-section-title::after {
  content: "";
  display: block;
  width: 40px;
  height: 3px;
  background-color: var(--primary-color, #ba003f);
  margin-top: 8px;
  border-radius: 2px;
  opacity: 0.7;
}

/* 增强引用样式 */
.poster-quote {
  position: relative;
  padding: 20px 30px;
  margin: 25px 15px;
  background-color: rgba(186, 0, 63, 0.05);
  border-radius: 8px;
  font-style: italic;
  text-align: center;
  box-shadow: 0 3px 10px rgba(186, 0, 63, 0.1);
}

.poster-quote::before,
.poster-quote::after {
  content: '"';
  position: absolute;
  font-size: 60px;
  color: rgba(186, 0, 63, 0.15);
  font-family: Georgia, serif;
}

.poster-quote::before {
  top: -20px;
  left: 10px;
}

.poster-quote::after {
  bottom: -50px;
  right: 10px;
}

/* 强化列表项 */
.poster-list-item {
  position: relative;
  padding: 8px 0 8px 30px;
  margin: 8px 0;
}

.poster-bullet {
  position: absolute;
  left: 0;
  top: 5px;
  width: 20px;
  height: 20px;
  background-color: var(--primary-color, #ba003f);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}

.poster-container:hover {
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
}

/* 角标装饰 */
.poster-corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border-color: var(--primary-color, #ba003f);
  border-style: solid;
  opacity: 0.7;
  z-index: 2;
}

.poster-corner-tl {
  top: 12px;
  left: 12px;
  border-width: 2px 0 0 2px;
  border-radius: 4px 0 0 0;
}

.poster-corner-tr {
  top: 12px;
  right: 12px;
  border-width: 2px 2px 0 0;
  border-radius: 0 4px 0 0;
}

.poster-corner-bl {
  bottom: 12px;
  left: 12px;
  border-width: 0 0 2px 2px;
  border-radius: 0 0 0 4px;
}

.poster-corner-br {
  bottom: 12px;
  right: 12px;
  border-width: 0 2px 2px 0;
  border-radius: 0 0 4px 0;
}

/* 强调线条 */
.poster-accent-line {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 5px;
  background-color: var(--primary-color, #ba003f);
  border-radius: 0 0 3px 3px;
  opacity: 0.8;
  z-index: 3;
}

/* 主标题样式 */
.poster-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color, #ba003f);
  text-align: center;
  padding: 40px 30px 5px;
  margin: 0;
  position: relative;
  z-index: 2;
  text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.8);
  line-height: 1.3;
}

/* 副标题样式 */
.poster-subtitle {
  font-size: 18px;
  color: #555;
  text-align: center;
  padding: 0 30px 25px;
  font-weight: 500;
  position: relative;
  z-index: 2;
  font-style: italic;
}

/* 主内容区域 */
.poster-content {
  position: relative;
  z-index: 2;
  padding: 20px 30px 40px;
}

/* 内容区段标题 */
.poster-section-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--primary-color, #ba003f);
  margin: 25px 0 15px;
  position: relative;
  padding-bottom: 8px;
}

.poster-section-title:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: var(--primary-color, #ba003f);
  opacity: 0.6;
}

/* 内容区小标题 */
.poster-section-subtitle {
  font-size: 18px;
  font-weight: 600;
  color: #444;
  margin: 20px 0 12px;
}

/* 正文段落 */
.poster-content p {
  margin-bottom: 16px;
  color: #555;
  line-height: 1.7;
  font-size: 16px;
}

/* 列表项样式 */
.poster-list-item {
  margin: 10px 0;
  padding-left: 25px;
  position: relative;
  line-height: 1.6;
  color: #555;
}

.poster-bullet {
  position: absolute;
  left: 0;
  top: 2px;
  color: var(--primary-color, #ba003f);
  font-size: 18px;
  font-weight: bold;
}

/* 引用样式 */
.poster-quote {
  font-size: 18px;
  font-style: italic;
  color: var(--primary-color, #ba003f);
  padding: 15px 25px;
  position: relative;
  margin: 20px 0;
  line-height: 1.6;
  background-color: rgba(186, 0, 63, 0.05);
  border-radius: 6px;
  text-align: center;
}

.poster-quote::before {
  content: '"';
  font-size: 40px;
  color: rgba(186, 0, 63, 0.15);
  position: absolute;
  top: -10px;
  left: 8px;
}

.poster-quote::after {
  content: '"';
  font-size: 40px;
  color: rgba(186, 0, 63, 0.15);
  position: absolute;
  bottom: -30px;
  right: 8px;
}

/* 品牌签名 */
.poster-brand {
  text-align: right;
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color, #ba003f);
  margin-top: 30px;
  padding-top: 15px;
  border-top: 1px dashed rgba(186, 0, 63, 0.3);
  font-style: italic;
  position: relative;
}

.poster-brand-prefix {
  font-size: 14px;
  font-weight: normal;
  color: #888;
  font-style: normal;
  margin-right: 5px;
}

/* 行业标签 */
.poster-tag {
  position: absolute;
  bottom: 15px;
  left: 15px;
  background-color: var(--primary-color, #ba003f);
  color: white;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 4px;
  opacity: 0.8;
  box-shadow: 0 2px 4px rgba(186, 0, 63, 0.2);
}

/* 海报背景装饰 */
.poster-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, rgba(186, 0, 63, 0.1), rgba(186, 0, 63, 0.02));
  border-radius: 0 0 0 100%;
  z-index: 1;
}

/* 自动高亮文本的关键部分 */
.poster-content p strong,
.poster-content p b,
.poster-section-title strong,
.poster-section-subtitle strong {
  color: var(--primary-color, #ba003f);
  font-weight: 700;
}

/* 首段特殊样式 */
.poster-content p:first-of-type {
  font-size: 17px;
  font-weight: 500;
}

/* 在小屏幕上调整样式 */
@media (max-width: 768px) {
  .poster-title {
    font-size: 26px;
    padding: 30px 20px 5px;
  }
  
  .poster-subtitle {
    font-size: 16px;
    padding: 0 20px 20px;
  }
  
  .poster-content {
    padding: 15px 20px 30px;
  }
  
  .poster-section-title {
    font-size: 20px;
  }
  
  .poster-section-subtitle {
    font-size: 17px;
  }
  
  .poster-quote {
    font-size: 16px;
    padding: 12px 20px;
  }
  
  .poster-corner {
    width: 16px;
    height: 16px;
  }
  
  .poster-accent-line {
    width: 60px;
    height: 4px;
  }
}

/* 修改整体内容容器样式 */
.copy-content {
  background-color: white;
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 添加额外的海报样式 */
.brand-name {
  font-weight: 700;
  color: var(--primary-color, #ba003f);
}

.poster-footer-decoration {
  width: 100%;
  height: 3px;
  margin-top: 20px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(186, 0, 63, 0.3) 20%, 
    rgba(186, 0, 63, 0.5) 50%, 
    rgba(186, 0, 63, 0.3) 80%, 
    transparent 100%);
}

/* 重新设计营销海报样式 */
.marketing-poster-wrapper {
  position: relative;
  max-width: 700px;
  margin: 20px auto;
  padding: 20px;
  perspective: 1000px;
  transform-style: preserve-3d;
}

.marketing-poster {
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
  transform-style: preserve-3d;
}

.marketing-poster:hover {
  transform: translateY(-5px) rotateX(2deg);
}

/* 增强海报容器样式 */
.poster-container {
  position: relative;
  background-color: #fff;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition: all 0.4s ease;
  transform-style: preserve-3d;
  margin-bottom: 30px;
}

.poster-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 15% 15%, rgba(186, 0, 63, 0.03) 5%, transparent 10%),
    radial-gradient(circle at 85% 85%, rgba(186, 0, 63, 0.03) 5%, transparent 10%);
  pointer-events: none;
  z-index: 1;
}

/* 新增背景叠加层 */
.poster-background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    rgba(255,255,255,0.4) 0%, 
    rgba(255,255,255,0.1) 100%);
  z-index: 1;
  pointer-events: none;
}

/* 首字放大效果增强 */
.poster-content p:first-of-type::first-letter {
  font-size: 300%;
  color: var(--primary-color, #ba003f);
  font-weight: bold;
  float: left;
  margin-right: 8px;
  line-height: 0.85;
  text-shadow: 1px 1px 2px rgba(186, 0, 63, 0.2);
}

/* 增强段落强调线 */
.poster-section-title::after {
  content: "";
  display: block;
  width: 50px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color, #ba003f), rgba(186, 0, 63, 0.3));
  margin-top: 10px;
  border-radius: 3px;
}

/* 产品名高亮样式 */
.product-highlight {
  color: var(--primary-color, #ba003f);
  font-weight: 700;
  position: relative;
  display: inline-block;
  padding: 0 2px;
}

.product-highlight::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 5px;
  z-index: -1;
}

/* 增强海报引用样式 */
.poster-quote {
  position: relative;
  padding: 25px 35px;
  margin: 30px 15px;
  background-color: rgba(186, 0, 63, 0.05);
  border-radius: 10px;
  font-style: italic;
  text-align: center;
  box-shadow: 0 5px 15px rgba(186, 0, 63, 0.07);
  border-left: 4px solid var(--primary-color, #ba003f);
}

.poster-quote::before,
.poster-quote::after {
  content: '"';
  position: absolute;
  font-size: 70px;
  color: rgba(186, 0, 63, 0.15);
  font-family: Georgia, serif;
  line-height: 0.5;
}

.poster-quote::before {
  top: 15px;
  left: 15px;
}

.poster-quote::after {
  bottom: 0;
  right: 15px;
}

/* 强化列表项 */
.poster-list-item {
  position: relative;
  padding: 10px 0 10px 34px;
  margin: 12px 0;
  transition: transform 0.2s ease;
}

.poster-list-item:hover {
  transform: translateX(5px);
}

.poster-bullet {
  position: absolute;
  left: 0;
  top: 9px;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, var(--primary-color, #ba003f), #e83e6c);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 3px 6px rgba(186, 0, 63, 0.2);
}

/* 增加海报光泽效果 */
.poster-shine-effect {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: shine 6s infinite linear;
  pointer-events: none;
  z-index: 10;
}

@keyframes shine {
  0% { transform: translateX(-100%) rotate(30deg); }
  100% { transform: translateX(100%) rotate(30deg); }
}

/* 角标装饰增强 */
.poster-corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border-color: var(--primary-color, #ba003f);
  border-style: solid;
  opacity: 0.7;
  z-index: 3;
}

.poster-corner-tl {
  top: 12px;
  left: 12px;
  border-width: 3px 0 0 3px;
  border-radius: 5px 0 0 0;
}

.poster-corner-tr {
  top: 12px;
  right: 12px;
  border-width: 3px 3px 0 0;
  border-radius: 0 5px 0 0;
}

.poster-corner-bl {
  bottom: 12px;
  left: 12px;
  border-width: 0 0 3px 3px;
  border-radius: 0 0 0 5px;
}

.poster-corner-br {
  bottom: 12px;
  right: 12px;
  border-width: 0 3px 3px 0;
  border-radius: 0 0 5px 0;
}

/* 强调线条加强 */
.poster-accent-line {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 6px;
  background: linear-gradient(to right, rgba(186, 0, 63, 0.3), var(--primary-color, #ba003f), rgba(186, 0, 63, 0.3));
  border-radius: 0 0 3px 3px;
  z-index: 5;
}

/* 新增彩带效果 */
.poster-ribbon {
  position: absolute;
  top: 0;
  right: 40px;
  width: 30px;
  height: 100px;
  background-color: var(--primary-color, #ba003f);
  z-index: 2;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.poster-ribbon::before {
  content: '';
  position: absolute;
  bottom: -20px;
  left: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 15px 20px 15px;
  border-color: transparent transparent var(--primary-color, #ba003f) transparent;
  transform: rotate(180deg);
}

/* 主标题样式增强 */
.poster-title {
  font-size: 36px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary-color, #ba003f), #e83e6c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-align: center;
  padding: 45px 30px 20px;
  margin: 0;
  position: relative;
  z-index: 3;
  text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.8);
  line-height: 1.3;
  letter-spacing: -0.5px;
}

.poster-title::after {
  content: '';
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 3px;
  background: linear-gradient(to right, rgba(186, 0, 63, 0.1), var(--primary-color, #ba003f), rgba(186, 0, 63, 0.1));
  border-radius: 3px;
}

/* 副标题样式增强 */
.poster-subtitle {
  font-size: 20px;
  color: #555;
  text-align: center;
  padding: 5px 30px 25px;
  margin: 0;
  font-weight: 500;
  font-style: italic;
  position: relative;
  z-index: 3;
  text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.8);
}

/* 内容区样式增强 */
.poster-content {
  padding: 25px 35px;
  background-color: rgba(255, 255, 255, 0.7);
  position: relative;
  z-index: 3;
  border-radius: 8px;
}

.poster-content p {
  margin-bottom: 18px;
  line-height: 1.8;
  font-size: 16px;
  color: #444;
  position: relative;
  z-index: 5;
}

.poster-content p:first-of-type {
  font-size: 18px;
  font-weight: 500;
  color: #222;
}

/* 内部阴影效果 */
.poster-shadow-inner {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  pointer-events: none;
  z-index: 4;
}

/* 段落标题增强 */
.poster-section-title {
  font-size: 26px;
  font-weight: 700;
  color: var(--primary-color, #ba003f);
  margin: 35px 0 20px;
  position: relative;
  padding-left: 15px;
  border-left: 5px solid var(--primary-color, #ba003f);
  letter-spacing: -0.5px;
}

.poster-section-subtitle {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin: 30px 0 15px;
  position: relative;
  letter-spacing: -0.3px;
}

/* 品牌签名增强 */
.poster-brand {
  text-align: right;
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary-color, #ba003f), #e83e6c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-top: 40px;
  padding: 20px 20px 10px;
  position: relative;
  border-top: 2px dashed rgba(186, 0, 63, 0.2);
  text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.8);
}

.poster-brand-prefix {
  font-size: 14px;
  font-weight: normal;
  color: #999;
  font-style: normal;
  margin-right: 6px;
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
  color: #999;
}

.brand-name {
  position: relative;
  display: inline-block;
}

.brand-name::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(to right, rgba(186, 0, 63, 0.3), var(--primary-color, #ba003f), rgba(186, 0, 63, 0.3));
  border-radius: 3px;
}

/* 行业标签增强 */
.poster-tag {
  position: absolute;
  top: 30px;
  right: -35px;
  background: linear-gradient(135deg, var(--primary-color, #ba003f), #e83e6c);
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 6px 35px;
  transform: rotate(45deg);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  z-index: 10;
  letter-spacing: 1px;
}

/* 字数统计样式 */
.poster-word-count {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 15px;
  font-style: italic;
  opacity: 0.7;
}

/* 底部装饰增强 */
.poster-footer-decoration {
  width: 100%;
  height: 6px;
  margin-top: 30px;
  background: linear-gradient(90deg, 
    rgba(186, 0, 63, 0.3) 0%, 
    var(--primary-color, #ba003f) 50%, 
    rgba(186, 0, 63, 0.3) 100%);
  border-radius: 5px;
}

/* 纸质效果叠加 */
.poster-texture-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.05;
  background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAUVBMVEWFhYWDg4N3d3dtbW17e3t1dXWBgYGHh4d5eXlzc3OLi4ubm5uVlZWPj4+NjY19fX2JiYl/f39ra2uRkZGZmZlpaWmXl5dvb29xcXGTk5NnZ2c8TV1mAAAAG3RSTlNAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAvEOwtAAAFVklEQVR4XpWWB67c2BUFb3g557T/hRo9/WUMZHlgr4Bg8Z4qQgQJlHI4A8SzFVrapvmTF9O7dmYRFZ60YiBhJRCgh1FYhiLAmdvX0CzTOpNE77ME0Zty/nWWzchDtiqrmQDeuv3powQ5ta2eN0FY0InkqDD73lT9c9lEzwUNqgFHs9VQce3TVClFCQrSTfOiYkVJQBmpbq2L6iZavPnAPcoU0dSw0SUTqz/GtrGuXfbyyBniKykOWQWGqwwMA7QiYAxi+IlPdqo+hYHnUt5ZPfnsHJyNiDtnpJyayNBkF6cWoYGAMY92U2hXHF/C1M8uP/ZtYdiuj26UdAdQQSXQErwSOMzt/XWRWAz5GuSBIkwG1H3FabJ2OsUOUhGC6tK4EMtJO0ttC6IBD3kM0ve0tJwMdSfjZo+EEISaeTr9P3wYrGjXqyC1krcKdhMpxEnt5JetoulscpyzhXN5FRpuPHvbeQaKxFAEB6EN+cYN6xD7RYGpXpNndMmZgM5Dcs3YSNFDHUo2LGfZuukSWyUYirJAdYbF3MfqEKmjM+I2EfhA94iG3L7uKrR+GdWD73ydlIB+6hgref1QTlmgmbM3/LeX5GI1Ux1RWpgxpLuZ2+I+IjzZ8wqE4nilvQdkUdfhzI5QDWy+kw5Wgg2pGpeEVeCCA7b85BO3F9DzxB3cdqvBzWcmzbyMiqhzuYqtHRVG2y4x+KOlnyqla8AoWWpuBoYRxzXrfKuILl6SfiWCbjxoZJUaCBj1CjH7GIaDbc9kqBY3W/Rgjda1iqQcOJu2WW+76pZC9QG7M00dffe9hNnseupFL53r8F7YHSwJWUKP2q+k7RdsxyOB11n0xtOvnW4irMMFNV4H0uqwS5ExsmP9AxbDTc9JwgneAT5vTiUSm1E7BSflSt3bfa1tv8Di3R8n3Af7MNWzs49hmauE2wP+ttrq+AsWpFG2awvsuOqbipWHgtuvuaAE+A1Z/7gC9hesnr+7wqCwG8c5yAg3AL1fm8T9AZtp/bbJGwl1pNrE7RuOX7PeMRUERVaPpEs+yqeoSmuOlokqw49pgomjLeh7icHNlG19yjs6XXOMedYm5xH2YxpV2tc0Ro2jJfxC50ApuxGob7lMsxfTbeUv07TyYxpeLucEH1gNd4IKH2LAg5TdVhlCafZvpskfncCfx8pOhJzd76bJWeYFnFciwcYfubRc12Ip/ppIhA1/mSZ/RxjFDrJC5xifFjJpY2Xl5zXdguFqYyTR1zSp1Y9p+tktDYYSNflcxI0iyO4TPBdlRcpeqjK/piF5bklq77VSEaA+z8qmJTFzIWiitbnzR794USKBUaT0NTEsVjZqLaFVqJoPN9ODG70IPbfBHKK+/q/AWR0tJzYHRULOa4MP+W/HfGadZUbfw177G7j/OGbIs8TahLyynl4X4RinF793Oz+BU0saXtUHrVBFT/DnA3ctNPoGbs4hRIjTok8i+algT1lTHi4SxFvONKNrgQFAq2/gFnWMXgwffgYMJpiKYkmW3tTg3ZQ9Jq+f8XN+A5eeUKHWvJWJ2sgJ1Sop+wwhqFVijqWaJhwtD8MNlSBeWNNWTa5Z5kPZw5+LbVT99wqTdx29lMUH4OIG/D86ruKEauBjvH5xy6um/Sfj7ei6UUVk4AIl3MyD4MSSTOFgSwsH/QJWaQ5as7ZcmgBZkzjjU1UrQ74ci1gWBCSGHtuV1H2mhSnO3Wp/3fEV5a+4wz//6qy8JxjZsmxxy5+4w9CDNJY09T072iKG0EnOS0arEYgXqYnXcYHwjTtUNAcMelOd4xpkoqiTYICWFq0JSiPfPDQdnt+4/wuqcXY47QILbgAAAABJRU5ErkJggg==');
  pointer-events: none;
  z-index: 2;
  mix-blend-mode: overlay;
}

.poster-fold-line {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.03);
  z-index: 2;
  pointer-events: none;
}

.poster-fold-horizontal {
  height: 1px;
  width: 100%;
  top: 50%;
  left: 0;
}

.poster-fold-vertical {
  width: 1px;
  height: 100%;
  left: 50%;
  top: 0;
}

.poster-shadow {
  position: absolute;
  bottom: -10px;
  left: 10%;
  width: 80%;
  height: 20px;
  background: rgba(0, 0, 0, 0.1);
  filter: blur(10px);
  border-radius: 50%;
  z-index: 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .poster-title {
    font-size: 30px;
    padding: 35px 15px 15px;
  }
  
  .poster-subtitle {
    font-size: 18px;
    padding: 0 15px 20px;
  }
  
  .poster-content {
    padding: 20px 25px;
  }
  
  .poster-content p:first-of-type::first-letter {
    font-size: 250%;
  }
  
  .poster-section-title {
    font-size: 22px;
  }
  
  .poster-section-subtitle {
    font-size: 18px;
  }
  
  .poster-quote {
    padding: 20px 30px;
    margin: 20px 10px;
  }
  
  .poster-corner {
    width: 20px;
    height: 20px;
  }
}

/* 营销文案海报风格 */
.marketing-poster-wrapper {
  position: relative;
  overflow: hidden; /* 保持内容不溢出 */
  min-height: 300px; /* 保证最小高度 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.marketing-poster {
  font-family: 'SimSun', 'Songti SC', serif; /* 使用更适合中文排版的字体 */
  color: #333; /* 默认文字颜色 */
  line-height: 1.8;
  white-space: pre-wrap; /* 保留换行和空格 */
  word-wrap: break-word; /* 允许长单词换行 */
  text-align: left; /* 文本左对齐 */
  width: 100%;
  max-width: 90%; /* 限制内容最大宽度 */
  padding: 20px; /* 内部内容边距 */
  background-color: #fff; /* 文案内容的背景色 */
  box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* 轻微阴影 */
  border-radius: 4px; /* 轻微圆角 */
}

/* 简单内容展示区 */
.content-display-container {
  position: relative;
  background-color: white;
  overflow: hidden;
  margin: 30px auto;
  max-width: 700px;
  height: 438px; /* 调整高度为16:10比例 (700÷16×10=437.5) */
  /* 平板外观样式 */
  border: 16px solid #333;
  border-radius: 24px;
  box-shadow: 
    0 0 0 2px #666,
    0 15px 40px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  padding: 0; /* 移除padding以便更好地控制内部布局 */
}

/* 平板顶部状态栏 */
.content-display-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 24px; /* 减小状态栏高度 */
  background-color: #333;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  z-index: 4; /* 调整z-index */
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
}

/* 平板摄像头 */
.content-display-container::after {
  content: '';
  position: absolute;
  top: 8px; /* 调整位置 */
  left: 50%;
  transform: translateX(-50%);
  width: 6px; /* 减小尺寸 */
  height: 6px; /* 减小尺寸 */
  background-color: #555;
  border-radius: 50%;
  border: 2px solid #444;
  z-index: 5; /* 调整z-index */
}

/* 平板底部Home按钮 */
.pad-home-button {
  position: absolute;
  bottom: 8px; /* 调整到平板内部底部 */
  left: 50%;
  transform: translateX(-50%);
  width: 32px; /* 减小尺寸 */
  height: 32px; /* 减小尺寸 */
  border-radius: 50%;
  border: 1px solid #444;
  background-color: #333;
  z-index: 5; /* 增大z-index确保在内容之上 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.pad-home-button::before {
  content: '';
  width: 16px; /* 减小尺寸 */
  height: 16px; /* 减小尺寸 */
  border: 2px solid #666;
  border-radius: 4px;
}

/* 添加状态栏图标 */
.pad-status-icons {
  position: absolute;
  top: 6px; /* 调整位置 */
  right: 15px;
  z-index: 5; /* 调整z-index */
  display: flex;
  gap: 10px;
}

.pad-status-icon {
  width: 10px; /* 减小尺寸 */
  height: 10px; /* 减小尺寸 */
  border-radius: 50%;
  background-color: #666;
}

.pad-status-icon.wifi {
  background-color: #80c080;
  clip-path: polygon(0% 100%, 50% 30%, 100% 100%);
}

.pad-status-icon.battery {
  width: 16px; /* 调整宽度 */
  height: 8px; /* 调整高度 */
  border-radius: 2px;
  background-color: #80b0ff;
  position: relative;
}

.pad-status-icon.battery::after {
  content: '';
  position: absolute;
  top: 2px;
  right: -3px; /* 调整位置 */
  width: 3px; /* 调整宽度 */
  height: 4px; /* 调整高度 */
  background-color: #80b0ff;
  border-radius: 0 2px 2px 0;
}

/* 屏幕光泽效果 */
.pad-screen-glare {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, 
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0) 40%,
    rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
  z-index: 3;
}

.content-display {
  font-size: 16px;
  line-height: 1.7; /* 减小行高 */
  color: #333;
  padding: 15px 20px 50px 20px; /* 减小内边距 */
  height: calc(100% - 24px); /* 调整为新的状态栏高度 */
  overflow-y: auto; /* 添加垂直滚动 */
  position: relative;
  background-color: #f8f8f8; /* 轻微的背景色 */
  margin-top: 24px; /* 调整为新的状态栏高度 */
  box-sizing: border-box; /* 确保padding包含在高度内 */
}

.content-display > *:last-child::after {
  content: '↓ 向下滚动查看更多 ↓';
  display: none; /* 默认隐藏 */
  text-align: center;
  font-size: 12px;
  color: #888;
  margin: 20px 0 30px; /* 底部留出足够空间不被Home按钮遮挡 */
}

/* 只有在内容可滚动时显示提示 */
.content-display.scrollable > *:last-child::after {
  display: block;
}

/* 自定义滚动条样式 */
.content-display::-webkit-scrollbar {
  width: 8px;
}

.content-display::-webkit-scrollbar-track {
  background: #eee;
  border-radius: 4px;
}

.content-display::-webkit-scrollbar-thumb {
  background-color: #999;
  border-radius: 4px;
  border: 2px solid #eee;
}

.streaming .streaming-indicator {
  display: flex;
  margin-top: 8px;
  justify-content: center;
}

.dot-typing {
  position: relative;
  left: -9999px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background-color: var(--primary-color, #ba003f);
  color: var(--primary-color, #ba003f);
  box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9998px 0 0 0 var(--primary-color, #ba003f), 10012px 0 0 0 var(--primary-color, #ba003f);
  animation: dotTyping 1.5s infinite linear;
}

@keyframes dotTyping {
  0% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9998px 0 0 0 var(--primary-color, #ba003f), 10012px 0 0 0 var(--primary-color, #ba003f);
  }
  16.667% {
    box-shadow: 9984px -6px 0 0 var(--primary-color, #ba003f), 9998px 0 0 0 var(--primary-color, #ba003f), 10012px 0 0 0 var(--primary-color, #ba003f);
  }
  33.333% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9998px 0 0 0 var(--primary-color, #ba003f), 10012px 0 0 0 var(--primary-color, #ba003f);
  }
  50% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9998px -6px 0 0 var(--primary-color, #ba003f), 10012px 0 0 0 var(--primary-color, #ba003f);
  }
  66.667% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9998px 0 0 0 var(--primary-color, #ba003f), 10012px 0 0 0 var(--primary-color, #ba003f);
  }
  83.333% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9998px 0 0 0 var(--primary-color, #ba003f), 10012px -6px 0 0 var(--primary-color, #ba003f);
  }
  100% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9998px 0 0 0 var(--primary-color, #ba003f), 10012px 0 0 0 var(--primary-color, #ba003f);
  }
}

.streaming .content-display {
  position: relative;
}

.streaming .content-display::after {
  content: '|';
  display: inline-block;
  color: var(--primary-color, #ba003f);
  font-weight: bold;
  font-size: 20px;
  animation: blink 0.5s infinite;
  position: relative;
  margin-left: 4px;
  vertical-align: middle;
}

/* 调整内容在流式输出时的样式 */
.streaming .content-display {
  position: relative;
  color: #000000;
  font-weight: 500;
}

/* 最新输出的文字有颜色变化效果 */
.streaming .content-display span.latest {
  color: var(--primary-color, #ba003f);
  font-weight: bold;
  animation: fadeToNormal 2s forwards;
}

@keyframes fadeToNormal {
  from { color: var(--primary-color, #ba003f); font-weight: bold; }
  to { color: #000000; font-weight: normal; }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style> 