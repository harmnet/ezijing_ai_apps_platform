<template>
  <div class="longform-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>长文章生成</h2>
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
        
        <!-- 长文类型选择 -->
        <div class="form-group">
          <label for="note-type">长文类型</label>
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
          <label for="note-title" class="required">文章标题</label>
          <input 
            type="text" 
            id="note-title" 
            v-model="noteTitle" 
            placeholder="输入吸引人的标题"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="target-audience">目标读者群体</label>
          <input 
            type="text" 
            id="target-audience" 
            v-model="targetAudience" 
            placeholder="输入目标读者群体"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="description" class="required">主要内容/关键要点</label>
          <textarea 
            id="description" 
            v-model="description" 
            placeholder="描述长文的主要内容和关键要点..."
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

        <div class="form-row">
          <div class="form-group">
            <label for="content-type">内容类型</label>
            <select id="content-type" v-model="contentType" class="form-control">
              <option value="informative">信息类</option>
              <option value="educational">教育类</option>
              <option value="persuasive">说服类</option>
              <option value="narrative">叙事类</option>
              <option value="descriptive">描述类</option>
              <option value="argumentative">论证类</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="article-length">文章长度</label>
            <select id="article-length" v-model="articleLength" class="form-control">
              <option value="short">短文 (500-1000字)</option>
              <option value="medium">中等 (1000-3000字)</option>
              <option value="long">长文 (3000-5000字)</option>
              <option value="very-long">特长文 (5000字以上)</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="citation-standard">引用标准</label>
            <select id="citation-standard" v-model="citationStandard" class="form-control">
              <option value="none">不需要引用</option>
              <option value="apa">APA</option>
              <option value="mla">MLA</option>
              <option value="chicago">Chicago</option>
              <option value="harvard">Harvard</option>
              <option value="gb">GB/T 7714</option>
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
          <label>文档结构元素</label>
          <div class="checkbox-group">
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeAbstract">
              <span>摘要</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeTableOfContents">
              <span>目录</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeIntroduction">
              <span>引言</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeMethodology">
              <span>研究方法</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeLiteratureReview">
              <span>文献综述</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeAnalysis">
              <span>分析与结论</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeResults">
              <span>研究结果</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeConclusion">
              <span>结论</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeReferences">
              <span>参考文献</span>
            </label>
            <label class="checkbox-container" style="color: #BA003F;">
              <input type="checkbox" v-model="includeAppendix">
              <span>附录</span>
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label for="special-requirements">其他特殊要求 (可选)</label>
          <textarea 
            id="special-requirements" 
            v-model="specialRequirements" 
            placeholder="如需要特定的文章结构、风格要求等，请在此说明"
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
          <button @click="generateLongform" class="btn btn-primary" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '生成中...' : '生成长文' }}
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
                  <svg v-if="example.id === 'academic1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 学术论文/教育图标 -->
                    <path d="M12 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"></path>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                    <path d="M3 6h18"></path>
                    <path d="M8 14h8"></path>
                    <path d="M8 18h5"></path>
                  </svg>
                  <svg v-else-if="example.id === 'report1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 经济/报告图标 -->
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                    <path d="M8 7l3 3 3-3 3 3"></path>
                    <path d="M8 11l3 3 3-3 3 3"></path>
                  </svg>
                  <svg v-else-if="example.id === 'review1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 文学评论图标 -->
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                  </svg>
                  <svg v-else-if="example.id === 'research1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 生物多样性/环保研究图标 -->
                    <path d="M5 3v4M19 3v4"></path>
                    <path d="M9 3v4M15 3v4"></path>
                    <path d="M12 12c.5 5 4 6 4 6-1.5.5-2 1.5-2 1.5.5 1.5 2 1.5 2 1.5-1 1-3.5.5-3.5.5s-2 2-5.5 1.5c0 0 1-1 .5-2 0 0-1 .5-2.5-1 0 0 2.5 0 4-2 1.5-2 3-2 3-6"></path>
                    <path d="M10.5 8.5c0 1-1 2-2 2-.75 0-1.5-.25-1.5-1S8 8 9 8"></path>
                    <path d="M13.5 8.5c0 1 1 2 2 2 .75 0 1.5-.25 1.5-1S16 8 15 8"></path>
                  </svg>
                  <svg v-else-if="example.id === 'tech1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 区块链/技术图标 -->
                    <path d="M1 8h7M14 8h1.5M8 8h6M1 16h1.5M7 16h2.5M12 16h7"></path>
                    <path d="M7 8a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-6a2 2 0 0 1-2-2v-8z"></path>
                  </svg>
                  <svg v-else-if="example.id === 'medical1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 医疗/卫生图标 -->
                    <path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"></path>
                    <path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"></path>
                    <path d="M22 10 A2 2 0 0 1 20 12 A2 2 0 0 1 18 10 A2 2 0 0 1 22 10 z"></path>
                    <path d="M14 13.5V12"></path>
                    <path d="M10 13.5V13"></path>
                    <path d="M14 17.5V17"></path>
                    <path d="M10 17.5V17"></path>
                  </svg>
                  <svg v-else-if="example.id === 'history1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 历史/文化图标 -->
                    <path d="M12 8L7 13M12 8L17 13M12 8V20M4 19V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14"></path>
                    <path d="M3 19h18"></path>
                  </svg>
                  <svg v-else-if="example.id === 'philosophy1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 哲学/思想图标 -->
                    <path d="M2 12h5M9 12h5M16 12h5"></path>
                    <path d="M12 2v20"></path>
                    <path d="M8 17a5 5 0 1 0 8 0"></path>
                  </svg>
                  <svg v-else-if="example.id === 'marketing1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 营销/社交媒体图标 -->
                    <path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3H6a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3h12a3 3 0 0 0 3-3 3 3 0 0 0-3-3z"></path>
                  </svg>
                  <svg v-else-if="example.id === 'psychology1'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 心理学/心理健康图标 -->
                    <path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"></path>
                    <path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-1"></path>
                    <path d="M18 8a6 6 0 0 0-6-6 6 6 0 0 0-6 6"></path>
                    <path d="M12 9v6"></path>
                    <path d="M9 12h6"></path>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#BA003F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <!-- 默认文档图标 -->
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
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isGenerating" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedNote && !isGenerating" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无长文内容，请点击"生成长文"按钮开始创作</p>
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
            <li>📄 标题要明确 - 使用具体、明确的标题，能够准确传达文章的主题和焦点</li>
            <li>📚 合理结构 - 良好的文章结构包括引言、主体和结论，有助于读者理解文章内容</li>
            <li>🔍 深入研究 - 进行充分的研究和资料收集，确保论点有可靠的支持</li>
            <li>📑 清晰论点 - 确保每个段落都有明确的中心思想，并与整体论点相关</li>
            <li>🧩 逻辑连贯 - 使用适当的过渡词和连接词，确保段落之间和观点之间的逻辑连贯</li>
            <li>📊 数据支持 - 使用相关数据、统计资料和引用来支持你的论点</li>
            <li>✍️ 语言精准 - 使用准确、专业的术语和表达方式，避免模糊不清的描述</li>
            <li>🔄 修改完善 - 写完初稿后进行多次修改，关注语法、拼写、逻辑和结构</li>
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
  name: 'Longform',
  data() {
    return {
      // 表单数据
      noteType: 'product-review',
      noteTitle: '',
      targetAudience: '',
      description: '',
      writingStyle: 'friendly',
      contentType: 'informative',
      articleLength: 'medium',
      citationStandard: 'none',
      keywords: '',
      specialRequirements: '',
      
      // 内容元素选项
      includeAbstract: true,
      includeTableOfContents: true,
      includeIntroduction: true,
      includeMethodology: false,
      includeLiteratureReview: false,
      includeAnalysis: true,
      includeResults: true,
      includeConclusion: true,
      includeReferences: false,
      includeAppendix: false,
      
      // 结果内容
      isGenerating: false,
      loadingText: '正在生成长文内容，请耐心等待...',
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
      isLastPage: false,
      
      // 示例数据
      examples: [
        { id: 'academic1', title: '人工智能在教育领域的应用前景', type: '学术论文', icon: 'ri-article-line' },
        { id: 'report1', title: '2023年全球经济发展趋势报告', type: '商业报告', icon: 'ri-bar-chart-line' },
        { id: 'review1', title: '文学作品分析：《百年孤独》的叙事结构', type: '文学评论', icon: 'ri-book-open-line' },
        { id: 'research1', title: '气候变化对生物多样性的影响研究', type: '研究论文', icon: 'ri-leaf-line' },
        { id: 'tech1', title: '区块链技术在供应链管理中的应用', type: '技术分析', icon: 'ri-link-m-line' },
        { id: 'medical1', title: '新冠疫情后的全球公共卫生体系建设', type: '医学论文', icon: 'ri-heart-pulse-line' },
        { id: 'history1', title: '丝绸之路与东西方文化交流', type: '历史研究', icon: 'ri-road-map-line' },
        { id: 'philosophy1', title: '东西方哲学思想比较研究', type: '哲学论文', icon: 'ri-mind-map-line' },
        { id: 'marketing1', title: '社交媒体时代的品牌营销策略', type: '营销分析', icon: 'ri-advertisement-line' },
        { id: 'psychology1', title: '童年创伤对成人心理健康的长期影响', type: '心理学研究', icon: 'ri-psychotherapy-line' }
      ],
      
      // 示例数据模板
      exampleData: {
        'academic1': {
          noteType: 'product-review',
          noteTitle: '人工智能在教育领域的应用前景',
          targetAudience: '教育工作者、教育技术研究人员、政策制定者',
          description: '探讨人工智能技术在教育领域的当前应用状况、潜在发展方向及可能带来的教育变革',
          writingStyle: 'professional',
          contentType: 'informative',
          articleLength: 'long',
          citationStandard: 'apa',
          includeAbstract: true,
          includeTableOfContents: true,
          includeIntroduction: true,
          includeMethodology: true,
          includeLiteratureReview: true,
          includeAnalysis: true,
          includeReferences: true
        },
        'report1': {
          noteType: 'lifestyle',
          noteTitle: '2023年全球经济发展趋势报告',
          targetAudience: '企业决策者、投资者、经济学研究人员',
          description: '分析2023年全球经济形势、主要经济体表现、新兴市场变化及未来发展预测',
          writingStyle: 'professional',
          contentType: 'informative',
          articleLength: 'long',
          citationStandard: 'mla',
          includeAbstract: true,
          includeTableOfContents: true,
          includeIntroduction: true,
          includeAnalysis: true,
          includeConclusion: true
        },
        'review1': {
          noteType: 'travel',
          noteTitle: '文学作品分析：《百年孤独》的叙事结构',
          targetAudience: '文学爱好者、文学研究者、大学生',
          description: '分析加西亚·马尔克斯《百年孤独》中的叙事手法、时间结构及魔幻现实主义表现',
          writingStyle: 'professional',
          contentType: 'argumentative',
          articleLength: 'medium',
          citationStandard: 'mla',
          includeAbstract: false,
          includeIntroduction: true,
          includeLiteratureReview: true,
          includeAnalysis: true,
          includeConclusion: true,
          includeReferences: true
        },
        'research1': {
          noteType: 'lifestyle',
          noteTitle: '气候变化对生物多样性的影响研究',
          targetAudience: '环保工作者、生物学研究人员、政策制定者',
          description: '研究全球气候变化对不同生态系统中生物多样性的影响、应对策略及未来挑战',
          writingStyle: 'professional',
          contentType: 'informative',
          articleLength: 'long',
          citationStandard: 'apa',
          includeAbstract: true,
          includeTableOfContents: true,
          includeIntroduction: true,
          includeMethodology: true,
          includeResults: true,
          includeAnalysis: true,
          includeConclusion: true,
          includeReferences: true
        },
        'tech1': {
          noteType: 'fashion',
          noteTitle: '区块链技术在供应链管理中的应用',
          targetAudience: '企业技术主管、供应链管理人员、IT从业者',
          description: '探讨区块链技术如何改善供应链透明度、追溯性和效率，分析实施案例和未来发展',
          writingStyle: 'professional',
          contentType: 'informative',
          articleLength: 'medium',
          citationStandard: 'harvard',
          includeAbstract: true,
          includeIntroduction: true,
          includeAnalysis: true,
          includeConclusion: true
        },
        'medical1': {
          noteType: 'beauty',
          noteTitle: '新冠疫情后的全球公共卫生体系建设',
          targetAudience: '公共卫生专业人士、政策制定者、医疗工作者',
          description: '分析新冠疫情暴露的全球公共卫生体系问题、各国应对措施及未来体系建设方向',
          writingStyle: 'professional',
          contentType: 'argumentative',
          articleLength: 'long',
          citationStandard: 'apa',
          includeAbstract: true,
          includeTableOfContents: true,
          includeIntroduction: true,
          includeLiteratureReview: true,
          includeAnalysis: true,
          includeConclusion: true,
          includeReferences: true
        },
        'history1': {
          noteType: 'travel',
          noteTitle: '丝绸之路与东西方文化交流',
          targetAudience: '历史爱好者、文化研究学者、大学生',
          description: '考察丝绸之路的历史发展、贸易路线及其对东西方文化、艺术、宗教等方面的影响',
          writingStyle: 'professional',
          contentType: 'narrative',
          articleLength: 'long',
          citationStandard: 'chicago',
          includeAbstract: true,
          includeIntroduction: true,
          includeAnalysis: true,
          includeConclusion: true,
          includeReferences: true
        },
        'philosophy1': {
          noteType: 'lifestyle',
          noteTitle: '东西方哲学思想比较研究',
          targetAudience: '哲学研究者、文化爱好者、大学生',
          description: '比较分析东西方主要哲学流派的核心思想、价值观念和世界观差异及其文化根源',
          writingStyle: 'professional',
          contentType: 'argumentative',
          articleLength: 'long',
          citationStandard: 'mla',
          includeAbstract: true,
          includeTableOfContents: true,
          includeIntroduction: true,
          includeLiteratureReview: true,
          includeAnalysis: true,
          includeConclusion: true,
          includeReferences: true
        },
        'marketing1': {
          noteType: 'product-review',
          noteTitle: '社交媒体时代的品牌营销策略',
          targetAudience: '市场营销人员、品牌管理者、企业决策者',
          description: '分析社交媒体环境下品牌营销的新特点、成功案例及有效策略',
          writingStyle: 'professional',
          contentType: 'informative',
          articleLength: 'medium',
          citationStandard: 'apa',
          includeAbstract: true,
          includeIntroduction: true,
          includeAnalysis: true,
          includeConclusion: true
        },
        'psychology1': {
          noteType: 'lifestyle',
          noteTitle: '童年创伤对成人心理健康的长期影响',
          targetAudience: '心理健康工作者、社会工作者、心理学研究人员',
          description: '研究童年期创伤经历对成人心理健康状况的影响机制、表现形式及干预策略',
          writingStyle: 'professional',
          contentType: 'informative',
          articleLength: 'long',
          citationStandard: 'apa',
          includeAbstract: true,
          includeTableOfContents: true,
          includeIntroduction: true,
          includeMethodology: true,
          includeResults: true,
          includeAnalysis: true,
          includeConclusion: true,
          includeReferences: true
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
          // 不做过滤，获取所有可用模型
          this.modelList = response.data.data || [];
          console.log('可用模型列表:', this.modelList);
          
          // 如果没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.modelList.push({ id: 'deepseek-v3-vol', name: '火山引擎 DeepSeek V3' });
          }
          
          // 默认选择火山引擎V3或第一个可用模型
          if (!this.selectedModel) {
            const volcanoModel = this.modelList.find(model => model.id === 'deepseek-v3-vol');
            this.selectedModel = volcanoModel ? volcanoModel.id : (this.modelList[0] ? this.modelList[0].id : 'deepseek-v3-vol');
            console.log('已选择模型:', this.selectedModel);
          }
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
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3-vol';
    },
    
    // 生成长文的方法
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
        const systemMessage = "你是一位专业的学术文章和长文创作专家，能够根据用户要求创作出结构清晰、内容专业的高质量长文。";
        const userMessage = prompt;
        
        const apiMessages = [
          { role: "system", content: systemMessage },
          { role: "user", content: userMessage }
        ];
        
        // 保存apiMessages供后续显示
        this.lastUsedPrompt = apiMessages;
        
        this.loadingText = '正在生成长文内容，请耐心等待...';
        
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3-vol';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        // 调用API (增加timeout和重试逻辑)
        console.log('开始调用API，模型:', this.selectedModel);
        
        let maxRetries = 2;
        let retryCount = 0;
        let response;
        
        while (retryCount <= maxRetries) {
          try {
            if (retryCount > 0) {
              this.loadingText = `正在重试生成 (${retryCount}/${maxRetries})...`;
              console.log(`尝试第${retryCount}次重试...`);
            }
            
            response = await axios.post('/api/v1/llm/chat', {
              model: this.selectedModel,
              messages: apiMessages,
              temperature: 0.7,
              top_p: 0.95,
              max_tokens: 4000
            }, { 
              timeout: 60000 // 设置60秒超时
            });
            
            // 如果成功获取响应，跳出重试循环
            break;
          } catch (error) {
            console.error(`API调用失败 (尝试 ${retryCount+1}/${maxRetries+1}):`, error.message);
            
            if (retryCount === maxRetries) {
              // 所有重试都失败了，抛出最后一个错误
              throw error;
            }
            
            // 增加重试次数并继续
            retryCount++;
            // 等待一段时间再重试 (1秒)
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
        
        // 日志记录API响应状态
        console.log('API响应状态:', response.status);
        console.log('API响应数据:', response.data);
        
        if (response.data && response.data.status === 'success') {
          // 从响应中提取生成的内容
          let content = '';
          
          if (response.data.data && response.data.data.choices && response.data.data.choices.length > 0) {
            // 火山引擎格式
            const message = response.data.data.choices[0].message;
            content = message.content || '';
            console.log('使用火山引擎响应格式');
          } else if (response.data.data && response.data.data.response) {
            // 硅基流动格式
            content = response.data.data.response || '';
            console.log('使用硅基流动响应格式');
          } else if (response.data.data && typeof response.data.data === 'string') {
            // 直接返回字符串
            content = response.data.data;
            console.log('使用字符串响应格式');
          } else if (response.data.content) {
            // 直接包含在内容字段
            content = response.data.content;
            console.log('使用content字段响应格式');
          }
          
          if (content) {
            this.generatedNote = content;
            console.log('成功获取长文内容');
            // 添加成功提示
            this.$message ? this.$message.success('长文生成成功！') : alert('长文生成成功！');
          } else {
            console.error('API返回成功，但无法提取内容:', response.data);
            throw new Error('无法从API响应中提取内容');
          }
        } else {
          // 处理API响应不成功的情况
          console.error('API返回不成功状态:', response.data);
          throw new Error(response.data?.message || '服务器返回错误');
        }
      } catch (error) {
        console.error('生成长文出错，详细错误:', error);
        
        // 更详细的错误日志
        if (error.response) {
          // 服务器响应了，但状态码不在2xx范围
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          this.$message ? 
            this.$message.error(`生成失败: 服务器错误 (${error.response.status})`) : 
            alert(`生成长文失败: 服务器错误 (${error.response.status})`);
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到服务器响应');
          this.$message ? 
            this.$message.error('生成失败: 服务器无响应，请检查网络连接') : 
            alert('生成长文失败: 服务器无响应，请检查网络连接');
        } else {
          // 设置请求时发生错误
          console.error('错误信息:', error.message);
          this.$message ? 
            this.$message.error(`生成失败: ${error.message}`) : 
            alert(`生成长文失败: ${error.message}`);
        }
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          console.log('开发模式：使用示例内容');
          this.generatedNote = `# ${this.noteTitle}\n\n## 摘要\n\n这是基于您的要求生成的示例长文内容。在实际环境中，这里将显示API返回的真实生成内容。\n\n## 引言\n\n在这个部分，将介绍文章的背景、目的和重要性。本文将探讨${this.description}相关的内容。\n\n## 主要内容\n\n这里将根据您的要求和设置，生成符合指定结构的详细内容。`;
        }
      } finally {
        this.isGenerating = false;
      }
    },
    
    // 验证表单
    validateForm() {
      if (!this.noteTitle) {
        this.$message ? this.$message.error('请输入文章标题') : alert('请输入文章标题');
        return false;
      }
      
      if (!this.description) {
        this.$message ? this.$message.error('请输入主要内容/关键要点') : alert('请输入主要内容/关键要点');
        return false;
      }
      
      return true;
    },
    
    // 生成提示词
    generatePrompt() {
      let prompt = '请根据以下要求创作一篇长文：\n\n';
      
      // 获取长文类型的中文名称
      const getNoteTypeName = () => {
        switch (this.noteType) {
          case 'product-review': return '产品测评';
          case 'lifestyle': return '生活方式';
          case 'travel': return '旅行游记';
          case 'food': return '美食分享';
          case 'fashion': return '穿搭分享';
          case 'beauty': return '美妆心得';
          default: return this.noteType;
        }
      };
      
      prompt += `长文类型：${getNoteTypeName()}\n`;
      prompt += `文章标题：${this.noteTitle}\n`;
      
      if (this.targetAudience) {
        prompt += `目标读者群体：${this.targetAudience}\n`;
      }
      
      prompt += `主要内容/关键要点：${this.description}\n`;
      
      // 内容类型
      const getContentTypeName = () => {
        switch (this.contentType) {
          case 'informative': return '信息类';
          case 'educational': return '教育类';
          case 'persuasive': return '说服类';
          case 'narrative': return '叙事类';
          case 'descriptive': return '描述类';
          case 'argumentative': return '论证类';
          default: return this.contentType;
        }
      };
      
      prompt += `内容类型：${getContentTypeName()}\n`;
      
      // 文章长度
      const getArticleLengthName = () => {
        switch (this.articleLength) {
          case 'short': return '短文 (500-1000字)';
          case 'medium': return '中等 (1000-3000字)';
          case 'long': return '长文 (3000-5000字)';
          case 'very-long': return '特长文 (5000字以上)';
          default: return this.articleLength;
        }
      };
      
      prompt += `文章长度：${getArticleLengthName()}\n`;
      
      // 引用标准
      if (this.citationStandard && this.citationStandard !== 'none') {
        const getCitationStandardName = () => {
          switch (this.citationStandard) {
            case 'apa': return 'APA格式';
            case 'mla': return 'MLA格式';
            case 'chicago': return 'Chicago格式';
            case 'harvard': return 'Harvard格式';
            case 'gb': return 'GB/T 7714格式';
            default: return this.citationStandard;
          }
        };
        
        prompt += `引用标准：${getCitationStandardName()}\n`;
      }
      
      // 写作风格
      const getStyleName = () => {
        switch (this.writingStyle) {
          case 'friendly': return '亲切友好';
          case 'professional': return '专业分析';
          case 'casual': return '轻松随意';
          case 'enthusiastic': return '热情洋溢';
          default: return this.writingStyle;
        }
      };
      
      prompt += `写作风格：${getStyleName()}\n`;
      
      // 关键词
      if (this.keywords) {
        prompt += `关键词：${this.keywords}\n`;
      }
      
      // 文档结构元素
      let docElements = [];
      if (this.includeAbstract) docElements.push('摘要');
      if (this.includeTableOfContents) docElements.push('目录');
      if (this.includeIntroduction) docElements.push('引言');
      if (this.includeMethodology) docElements.push('研究方法');
      if (this.includeLiteratureReview) docElements.push('文献综述');
      if (this.includeAnalysis) docElements.push('分析与结论');
      if (this.includeResults) docElements.push('研究结果');
      if (this.includeConclusion) docElements.push('结论');
      if (this.includeReferences) docElements.push('参考文献');
      if (this.includeAppendix) docElements.push('附录');
      
      if (docElements.length) {
        prompt += `文档结构元素：${docElements.join('、')}\n`;
      }
      
      // 特殊要求
      if (this.specialRequirements) {
        prompt += `其他特殊要求：${this.specialRequirements}\n`;
      }
      
      return prompt;
    },
    
    // 重置表单
    resetForm() {
      this.noteType = 'product-review';
      this.noteTitle = '';
      this.targetAudience = '';
      this.description = '';
      this.writingStyle = 'friendly';
      this.contentType = 'informative';
      this.articleLength = 'medium';
      this.citationStandard = 'none';
      this.keywords = '';
      this.specialRequirements = '';
      
      this.includeAbstract = true;
      this.includeTableOfContents = true;
      this.includeIntroduction = true;
      this.includeMethodology = false;
      this.includeLiteratureReview = false;
      this.includeAnalysis = true;
      this.includeResults = true;
      this.includeConclusion = true;
      this.includeReferences = false;
      this.includeAppendix = false;
      
      this.generatedNote = '';
    },
    
    // 显示创作小贴士
    showTips() {
      this.showTipsModal = true;
    },
    
    // 复制生成的文本
    copyText() {
      if (!this.generatedNote) return;
      
      try {
        navigator.clipboard.writeText(this.generatedNote).then(() => {
          this.$message ? this.$message.success('内容已复制到剪贴板') : alert('内容已复制到剪贴板');
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
        // 把提示词转换为字符串
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
      element.download = `长文_${this.noteTitle || '未命名'}.txt`;
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
        this.writingStyle = example.writingStyle;
        this.contentType = example.contentType || 'informative';
        this.articleLength = example.articleLength || 'medium';
        this.citationStandard = example.citationStandard || 'none';
        
        // 设置文档结构元素
        this.includeAbstract = example.includeAbstract || false;
        this.includeTableOfContents = example.includeTableOfContents || false;
        this.includeIntroduction = example.includeIntroduction || false;
        this.includeMethodology = example.includeMethodology || false;
        this.includeLiteratureReview = example.includeLiteratureReview || false;
        this.includeAnalysis = example.includeAnalysis || false;
        this.includeResults = example.includeResults || false;
        this.includeConclusion = example.includeConclusion || false;
        this.includeReferences = example.includeReferences || false;
        this.includeAppendix = example.includeAppendix || false;
      }
    }
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateCarouselPosition);
  }
};
</script>

<style scoped>
.longform-article-page {
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