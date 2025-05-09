<template>
  <div class="longform-article-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>长文章生成</h2>
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
                <div class="example-card-header">
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
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无长文内容，请点击"生成长文"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedNote" class="note-result" :class="{'blur-content': isGenerating}">
              <!-- 移除原始的textarea展示 -->
              <!-- <textarea v-model="generatedNote" class="result-textarea" readonly></textarea> -->
              
              <!-- 模拟Word文档界面 -->
              <div class="word-document">
                <div class="word-toolbar">
                  <div class="toolbar-group">
                    <button class="toolbar-btn" title="保存为PDF" @click="saveAsPdf">
                      <i class="ri-file-pdf-line"></i>
                    </button>
                    <button class="toolbar-btn" title="打印文档" @click="printDocument">
                      <i class="ri-printer-line"></i>
                    </button>
                  </div>
                  <div class="toolbar-group">
                    <button class="toolbar-btn" title="粗体" @click="applyFormat('bold')">
                      <i class="ri-bold"></i>
                    </button>
                    <button class="toolbar-btn" title="斜体" @click="applyFormat('italic')">
                      <i class="ri-italic"></i>
                    </button>
                    <button class="toolbar-btn" title="下划线" @click="applyFormat('underline')">
                      <i class="ri-underline"></i>
                    </button>
                  </div>
                  <div class="toolbar-group">
                    <button class="toolbar-btn" title="左对齐" @click="applyAlign('left')">
                      <i class="ri-align-left"></i>
                    </button>
                    <button class="toolbar-btn" title="居中对齐" @click="applyAlign('center')">
                      <i class="ri-align-center"></i>
                    </button>
                    <button class="toolbar-btn" title="右对齐" @click="applyAlign('right')">
                      <i class="ri-align-right"></i>
                    </button>
                  </div>
                </div>
                <div class="word-page">
                  <div class="word-content">
                    <div v-html="wordFormattedContent"></div>
                  </div>
                  <!-- 添加页脚和页码 -->
                  <div class="word-footer">
                    <div class="word-page-number">第 1 页</div>
                    <div class="word-document-title">{{ noteTitle || '长文章' }}</div>
                  </div>
                </div>
                <!-- 添加状态栏 -->
                <div class="word-statusbar">
                  <div class="word-statusbar-item">100%</div>
                  <div class="word-statusbar-item">编辑</div>
                  <div class="word-statusbar-item">
                    <i class="ri-check-line"></i> 已保存
                  </div>
                  <div class="word-statusbar-item">
                    {{ new Date().toLocaleDateString('zh-CN') }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 替换为知识学习抽屉组件 -->
    <el-drawer
      v-model="showTipsModal"
      title="AI长文档编写知识指南"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in aiLongformKnowledge" :key="index" class="knowledge-section">
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
import { longformExamples, longformExampleData } from '@/views/example_data.js';
import { documentStructureKnowledge, aiLongformKnowledge } from '@/views/Knowledge_data.js';
import '@/assets/css/text-creation-common.css'; // 引入统一CSS样式文件
import { ElDrawer } from 'element-plus';

export default {
  name: 'Longform',
  components: {
    ElDrawer
  },
  data() {
    return {
      // 输入参数
      noteType: 'product-review',
      noteTitle: '',
      targetAudience: '',
      description: '',
      writingStyle: 'professional',
      contentType: 'informative',
      articleLength: 'medium',
      citationStandard: 'none',
      keywords: '',
      includeAbstract: false,
      includeTableOfContents: false,
      includeIntroduction: true,
      includeMethodology: false,
      includeLiteratureReview: false,
      includeAnalysis: false,
      includeResults: false,
      includeConclusion: true,
      includeReferences: false,
      includeAppendix: false,
      specialRequirements: '',
      
      // 使用导入的案例数据替换自定义的对象
      exampleData: longformExampleData,
      
      // 模型选择
      selectedModel: 'deepseek-v3-vol',
      modelList: [
        { id: 'deepseek-v3-vol', name: 'DeepSeek-V3' },
        { id: 'llama3-8b', name: 'Llama3-8B' },
        { id: 'qwen-max', name: 'Qwen-Max' }
      ],
      
      // 生成结果
      generatedNote: '',
      isGenerating: false,
      loadingText: '正在生成长文，请稍候...',
      loadingTexts: [
        '正在构思文章结构...',
        '正在整理关键信息...',
        '正在润色语言表达...',
        '正在完善内容细节...',
        '正在进行最终检查...'
      ],
      loadingInterval: null,
      lastUsedPrompt: null,
      
      // 提示词模态框
      showPromptModal: false,
      
      // 知识学习模态框
      showTipsModal: false,
      aiLongformKnowledge: aiLongformKnowledge,
      
      // 案例轮播
      examples: longformExamples,
      currentExampleIndex: 0,
      exampleTranslateX: 0,
      carouselItemWidth: 0,
      isLastPage: false
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
    },
    // Word风格的格式化内容
    wordFormattedContent() {
      if (!this.generatedNote) return '';
      return this.parseMarkdown(this.generatedNote);
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
          // 过滤模型，只保留火山引擎和豆包模型
          const allModels = response.data.data || [];
          this.modelList = allModels.filter(model => 
            model.id.includes('vol') || // 火山引擎模型
            model.id === 'doubao'      // 豆包模型
          );
          
          console.log('过滤后的可用模型列表:', this.modelList);
          
          // 如果没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.setupDefaultModels();
          }
          
          // 默认选择火山引擎V3或第一个可用模型
          if (!this.selectedModel) {
            const volcanoV3Model = this.modelList.find(model => model.id === 'deepseek-v3-vol');
            this.selectedModel = volcanoV3Model ? volcanoV3Model.id : (this.modelList[0] ? this.modelList[0].id : 'deepseek-v3-vol');
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
        { id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' },
        { id: 'deepseek-r1-vol', name: '火山引擎 DeepSeek R1' },
        { id: 'doubao', name: '豆包' }
      ];
      this.selectedModel = 'deepseek-v3';
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
        console.log('完整提示词:', prompt);
        
        // 保存提示词以便之后查看
        this.lastUsedPrompt = [
          { role: "system", content: "你是一位专业的学术文章和长文创作专家，能够根据用户要求创作出结构清晰、内容专业的高质量长文。" },
          { role: "user", content: prompt }
        ];
        
        this.loadingText = '正在生成长文内容，请耐心等待...';
        
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        // 将模型 deepseek-v3-vol 转换为 deepseek-v3（适配新API）
        let apiModel = this.selectedModel;
        if (apiModel === 'deepseek-v3-vol') {
          apiModel = 'deepseek-v3';
        }
        
        console.log('使用API模型:', apiModel);
        
        // 准备API参数
        const messages = [{ role: 'user', content: prompt }];
        
        // 构建API请求参数
        const apiParams = {
          model: apiModel,
          messages: messages,
          stream: true,
          temperature: 0.7,
          max_tokens: 4000
        };
        
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        // 发送流式请求
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
                  throw new Error(parsed.error.message || '生成文案失败');
                }
                
                // 处理火山引擎返回的delta格式数据
                if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                  const delta = parsed.choices[0].delta;
                  
                  // 处理内容增量
                  if (delta.content) {
                    // 累加收到的内容
                    this.generatedNote += delta.content;
                    // 添加自动滚动到最新内容
                    this.$nextTick(() => {
                      this.scrollToLatestContent();
                    });
                  }
                }
              } catch (e) {
                console.error('解析流式数据失败:', e, data);
              }
            }
          }
        }
        
        console.log('成功获取长文内容');
        // 添加成功提示
        this.$message ? this.$message.success('长文生成成功！') : alert('长文生成成功！');
        
      } catch (error) {
        console.error(`API调用失败:`, error);
        
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
      
      this.includeAbstract = false;
      this.includeTableOfContents = false;
      this.includeIntroduction = false;
      this.includeMethodology = false;
      this.includeLiteratureReview = false;
      this.includeAnalysis = false;
      this.includeResults = false;
      this.includeConclusion = false;
      this.includeReferences = false;
      this.includeAppendix = false;
      
      this.generatedNote = '';
    },
    
    // 显示知识学习内容
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
      // 确保exampleData和对应的示例ID存在
      if (!this.exampleData || !this.exampleData[exampleId]) {
        console.error(`案例数据不存在: ${exampleId}`);
        this.$message ? this.$message.error(`案例数据不存在: ${exampleId}`) : alert(`案例数据不存在: ${exampleId}`);
        return;
      }
      
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
    },
    
    // 将markdown转换为Word样式的HTML内容
    parseMarkdown(markdown) {
      if (!markdown) return '';
      
      // 提取文档标题（如果存在）
      let documentTitle = this.noteTitle || '长文章';
      let contentWithoutTitle = markdown;
      
      // 检查第一行是否是一级标题
      const titleMatch = markdown.match(/^# (.+)$/m);
      if (titleMatch) {
        documentTitle = titleMatch[1];
        // 移除第一个标题，稍后会在封面添加
        contentWithoutTitle = markdown.replace(/^# .+$/m, '');
      }
      
      // 创建封面
      let html = `
        <div class="word-cover">
          <div class="word-cover-title">${documentTitle}</div>
          <div class="word-cover-subtitle">${this.getNoteTypeName()} - ${this.getContentTypeName()}</div>
          <div class="word-cover-date">${new Date().toLocaleDateString('zh-CN')}</div>
          <div class="word-cover-author">AI助手生成</div>
        </div>
        <div class="word-page-break"></div>
      `;
      
      // 处理正文内容
      html += contentWithoutTitle
        // 处理一级标题
        .replace(/^# (.*$)/gm, '<div class="word-heading word-heading-1">$1</div>')
        // 处理二级标题
        .replace(/^## (.*$)/gm, '<div class="word-heading word-heading-2">$1</div>')
        // 处理三级标题
        .replace(/^### (.*$)/gm, '<div class="word-heading word-heading-3">$1</div>')
        // 处理四级标题
        .replace(/^#### (.*$)/gm, '<div class="word-heading word-heading-4">$1</div>')
        // 处理无序列表
        .replace(/^[\*\-] (.*$)/gm, '<div class="word-list-item"><span class="word-bullet">•</span>$1</div>')
        // 处理带编号的列表
        .replace(/^(\d+)\. (.*$)/gm, '<div class="word-list-item"><span class="word-number">$1.</span>$2</div>')
        // 处理粗体
        .replace(/\*\*(.*?)\*\*/g, '<span class="word-bold">$1</span>')
        // 处理斜体
        .replace(/\*(.*?)\*/g, '<span class="word-italic">$1</span>')
        // 处理代码块
        .replace(/```([\s\S]*?)```/g, '<div class="word-code-block">$1</div>')
        // 处理行内代码
        .replace(/`(.*?)`/g, '<span class="word-inline-code">$1</span>')
        // 处理分隔线
        .replace(/^---$/gm, '<hr class="word-hr">')
        // 处理引用块
        .replace(/^> (.*$)/gm, '<div class="word-blockquote">$1</div>')
        // 处理普通段落：找到不是标题和列表项的内容行
        .replace(/^(?!#|[\*\-]|\d+\.|>)(.+)$/gm, '<div class="word-paragraph">$1</div>')
        // 处理空行
        .replace(/^\s*$/gm, '<div class="word-paragraph-spacing"></div>');

      return html;
    },
    
    // 获取长文类型的中文名称
    getNoteTypeName() {
      switch (this.noteType) {
        case 'product-review': return '产品测评';
        case 'lifestyle': return '生活方式';
        case 'travel': return '旅行游记';
        case 'food': return '美食分享';
        case 'fashion': return '穿搭分享';
        case 'beauty': return '美妆心得';
        default: return this.noteType;
      }
    },
    
    // 获取内容类型的中文名称
    getContentTypeName() {
      switch (this.contentType) {
        case 'informative': return '信息类';
        case 'educational': return '教育类';
        case 'persuasive': return '说服类';
        case 'narrative': return '叙事类';
        case 'descriptive': return '描述类';
        case 'argumentative': return '论证类';
        default: return this.contentType;
      }
    },
    
    // 打印文档
    printDocument() {
      // 创建一个新的打印窗口，只包含文档内容
      const printWindow = window.open('', '_blank');
      if (!printWindow) {
        this.$message ? this.$message.error('无法打开打印窗口，请检查浏览器的弹窗设置') : alert('无法打开打印窗口，请检查浏览器的弹窗设置');
        return;
      }

      // 添加样式和内容
      printWindow.document.write(`
        <html>
          <head>
            <title>${this.noteTitle || '长文章'}</title>
            <style>
              @media print {
                body {
                  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
                  margin: 0;
                  padding: 20mm;
                }
                
                /* 复制所有word-相关的样式... */
                .word-heading-1 {
                  font-size: 24px;
                  font-weight: bold;
                  margin-top: 24px;
                  color: #2b579a;
                  border-bottom: 1px solid #e0e0e0;
                  padding-bottom: 8px;
                }
                
                .word-heading-2 {
                  font-size: 20px;
                  font-weight: bold;
                  margin-top: 20px;
                  color: #2b579a;
                }
                
                .word-heading-3 {
                  font-size: 16px;
                  font-weight: bold;
                  margin-top: 16px;
                }
                
                .word-paragraph {
                  font-size: 14px;
                  line-height: 1.5;
                  margin-bottom: 8px;
                  text-align: justify;
                }
                
                .word-list-item {
                  font-size: 14px;
                  line-height: 1.5;
                  margin-bottom: 6px;
                  padding-left: 24px;
                  position: relative;
                }
                
                /* 其他样式... */
              }
            </style>
          </head>
          <body>
            ${this.wordFormattedContent}
          </body>
        </html>
      `);
      
      printWindow.document.close();
      
      // 等待样式加载完成后打印
      setTimeout(() => {
        printWindow.print();
        printWindow.close();
      }, 500);
    },
    
    // 保存为PDF
    saveAsPdf() {
      this.$message ? this.$message.info('准备将文档保存为PDF...') : alert('准备将文档保存为PDF...');
      
      // 实际产品中，可以使用html2pdf.js或jspdf等库进行PDF转换
      // 这里简化为使用打印功能的"另存为PDF"选项
      this.printDocument();
      
      this.$message ? this.$message.success('请通过浏览器的打印功能选择"另存为PDF"选项') : alert('请通过浏览器的打印功能选择"另存为PDF"选项');
    },
    
    // 格式应用函数（实际环境中这些按钮只是样式展示，并不会有实际功能）
    applyFormat(format) {
      // 在实际的Word中，这些按钮会修改选中的文本样式
      // 这里只是模拟界面，不需要实际功能
      console.log(`应用${format}格式`);
    },
    
    // 对齐应用函数
    applyAlign(align) {
      // 在实际的Word中，这些按钮会修改段落对齐方式
      // 这里只是模拟界面，不需要实际功能
      console.log(`应用${align}对齐`);
    },
    
    // 格式化Markdown文本
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗文本 **文本**
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理列表 - 项目
      text = text.replace(/^- (.*?)$/gm, '<li>$1</li>');
      text = text.replace(/<li>.*?<\/li>(\n|$)+/g, function(match) {
        return '<ul class="knowledge-list">' + match + '</ul>';
      });
      
      // 处理换行
      text = text.replace(/\n\n/g, '<br><br>');
      
      return text;
    },
    
    // 添加此方法以自动滚动到最新内容
    scrollToLatestContent() {
      const wordContent = document.querySelector('.word-content');
      if (wordContent) {
        const wordPage = document.querySelector('.word-page');
        if (wordPage) {
          // 确保滚动到可以看到最新内容的位置
          wordPage.scrollTop = wordPage.scrollHeight;
        }
      }
    },
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateCarouselPosition);
  }
};
</script>

<style>
@import '@/assets/css/text-creation-common.css';

/* 删除与text-creation-common.css重复的样式 */

/* 特定于Longform组件的样式 */
.longform-article-page {
  width: 100%;
}

/* 结果区域样式 */
.result-section {
  background-color: white;
  border-radius: 8px;
  padding-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

/* 长文章页面特定样式 */
.checkbox-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #f9f9f9;
  border: 1px solid #eee;
}

.checkbox-container:hover {
  background-color: #f5f5f5;
  border-color: #ddd;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.checkbox-container input {
  margin-right: 8px;
}

/* 删除重复的section-title样式 */

/* 保留Word文档模拟样式 */
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

/* 添加回action-buttons样式，但设置margin-top为0，保持与结果区域一致 */
.action-buttons {
  display: flex;
  gap: 8px;
  margin-top: 15px;
}

/* 添加旋转动画效果 */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinning {
  animation: spin 1.5s linear infinite;
  display: inline-block;
}

.blur-content {
  filter: blur(2px);
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

/* Word文档样式 */
.note-result {
  padding: 0;
  overflow-y: auto;
  max-height: 700px;
  background-color: white; /* 改为白色背景 */
  margin-bottom: 40px; /* 增加底部间距，与左侧表单对齐 */
  border-radius: 8px;
}

/* Word模拟样式 */
.word-document {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: white; /* 修改为白色背景 */
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; /* 增加底部间距 */
}

.word-toolbar {
  display: flex;
  background-color: #2b579a;
  padding: 8px 16px;
  gap: 20px;
}

.toolbar-group {
  display: flex;
  gap: 4px;
}

.toolbar-btn {
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.toolbar-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.word-page {
  background-color: white; /* 改为白色背景 */
  padding: 20px;
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.word-content {
  width: 100%;
  max-width: 800px;
  min-height: 1120px; /* A4尺寸高度模拟 */
  background-color: white;
  padding: 60px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 2px;
  position: relative;
  margin-bottom: 20px; /* 添加底部间距 */
}

/* 添加页脚和页码样式 */
.word-footer {
  position: absolute;
  bottom: 20px; /* 增加距底部距离 */
  width: 100%;
  max-width: 680px; /* 调整宽度与内容区匹配 */
  display: flex;
  justify-content: space-between;
  padding: 0;
  color: #777;
  font-size: 12px;
  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
}

.word-page-number {
  text-align: left;
}

.word-document-title {
  text-align: right;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

/* 添加Word状态栏样式 */
.word-statusbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  background-color: white; /* 改为白色背景 */
  border-top: 1px solid #e0e0e0;
  padding: 4px 16px;
  gap: 24px;
  font-size: 12px;
  color: #666;
  height: 24px;
}

.word-statusbar-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.word-statusbar-item i {
  font-size: 14px;
  color: #2b579a;
}

/* Word封面样式 */
.word-cover {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 800px;
  text-align: center;
  position: relative;
  background-color: white; /* 确保封面背景为白色 */
}

.word-cover-title {
  font-size: 32px;
  font-weight: bold;
  color: #2b579a;
  margin-bottom: 16px;
  max-width: 80%;
}

.word-cover-subtitle {
  font-size: 18px;
  color: #666;
  margin-bottom: 24px;
}

.word-cover-date {
  position: absolute;
  bottom: 100px;
  font-size: 14px;
  color: #777;
}

.word-cover-author {
  position: absolute;
  bottom: 70px;
  font-size: 14px;
  color: #777;
}

.word-page-break {
  page-break-after: always;
  margin: 30px 0;
  border-bottom: 1px dashed #eee;
  width: 100%;
}

/* Word内容样式 */
.word-heading {
  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
  color: #333;
  margin-bottom: 10px;
  page-break-after: avoid;
}

.word-heading-1 {
  font-size: 24px;
  font-weight: bold;
  margin-top: 24px;
  color: #2b579a;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 8px;
}

.word-heading-2 {
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
  color: #2b579a;
}

.word-heading-3 {
  font-size: 16px;
  font-weight: bold;
  margin-top: 16px;
}

.word-heading-4 {
  font-size: 14px;
  font-weight: bold;
  margin-top: 12px;
}

.word-paragraph {
  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 8px;
  text-align: justify;
}

.word-paragraph-spacing {
  height: 12px;
}

.word-list-item {
  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 6px;
  padding-left: 24px;
  position: relative;
}

.word-bullet, .word-number {
  position: absolute;
  left: 0;
}

.word-bold {
  font-weight: bold;
}

.word-italic {
  font-style: italic;
}

.word-code-block {
  font-family: 'Consolas', 'Courier New', monospace;
  background-color: #f8f8f8;
  padding: 12px;
  margin: 12px 0;
  border-radius: 4px;
  border-left: 3px solid #2b579a;
  white-space: pre-wrap;
  font-size: 13px;
  color: #333;
  line-height: 1.5;
}

.word-inline-code {
  font-family: 'Consolas', 'Courier New', monospace;
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 0.9em;
  color: #d63384;
}

.word-blockquote {
  border-left: 3px solid #2b579a;
  padding: 8px 16px;
  margin: 12px 0;
  background-color: #f9f9f9;
  color: #555;
  font-style: italic;
}

.word-hr {
  border: none;
  border-bottom: 1px solid #e0e0e0;
  margin: 16px 0;
}

@media print {
  .word-document {
    box-shadow: none;
  }
  
  .word-toolbar, .word-statusbar {
    display: none;
  }
  
  .word-page {
    padding: 0;
  }
  
  .word-content {
    box-shadow: none;
  }
}

/* 添加知识学习抽屉的样式 */
.knowledge-drawer {
  font-family: 'Microsoft YaHei', sans-serif;
}

:deep(.el-drawer__header) {
  margin-bottom: 20px;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  color: var(--primary-color, #ba003f);
  font-weight: bold;
}

:deep(.el-drawer__body) {
  padding: 0;
  overflow-y: auto;
}

.knowledge-content {
  padding: 0 20px 30px;
}

.knowledge-section {
  margin-bottom: 25px;
}

.knowledge-subtitle {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #eee;
  color: var(--primary-color, #ba003f);
  font-size: 16px;
  font-weight: 600;
}

.knowledge-icon {
  margin-right: 8px;
  font-size: 18px;
}

.knowledge-text {
  line-height: 1.6;
  color: #333;
  font-size: 14px;
}

.knowledge-text strong {
  color: var(--primary-color, #ba003f);
  font-weight: 600;
}

.knowledge-list {
  margin: 10px 0;
  padding-left: 20px;
}

.knowledge-list li {
  margin-bottom: 8px;
}

.result-content-wrapper {
  position: relative;
  height: 100%;
  border-radius: 8px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  min-height: 580px; /* 设置最小高度，确保有足够空间显示内容 */
  margin-bottom: 40px; /* 增加底部边距，与左侧表单底部对齐 */
}
</style> 