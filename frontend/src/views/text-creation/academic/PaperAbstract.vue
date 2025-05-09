<template>
  <div class="paper-outline-page">
    <!-- 主要内容区域 - 使用两列布局 -->
    <div class="main-container">
      <!-- 左侧：输入参数和示例主题 -->
      <div class="left-column">
        <!-- 输入参数部分 -->
        <div class="input-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-settings-3-line"></i>
              输入参数
            </h3>
          </div>
          
          <div class="form-group">
            <label for="paper-topic" class="required">论文主题</label>
            <el-input
              id="paper-topic"
              v-model="formData.query"
              type="textarea"
              :rows="5"
              placeholder="请输入论文主题或要求，例如：'人工智能在医疗领域的应用'"
              :disabled="isGenerating"
              class="form-control"
            ></el-input>
            <div class="form-tip">提示：明确具体的研究领域和研究问题，有助于生成更加详细和有针对性的论文大纲</div>
          </div>
          
          <div class="action-buttons">
            <button class="btn btn-primary" @click="generateOutline" :disabled="isGenerating || !formData.query.trim()">
              <i class="ri-magic-line" v-if="!isGenerating"></i>
              <i class="ri-loader-4-line spinning" v-else></i>
              {{ isGenerating ? '正在生成...' : '生成论文大纲' }}
            </button>
            <button class="btn btn-secondary" @click="resetForm" :disabled="isGenerating">
              <i class="ri-refresh-line"></i> 重置
            </button>
          </div>
        </div>
        
        <!-- 示例论文主题部分 -->
        <div class="examples-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-lightbulb-line"></i>
              示例主题
            </h3>
          </div>
          
          <div class="examples-list">
            <div v-for="(example, index) in examples" :key="index" class="example-item" @click="useExample(example)">
              <h4>{{ example.title }}</h4>
              <p>{{ example.description }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧：生成结果展示 -->
      <div class="right-column">
        <!-- 大纲生成结果 -->
        <div class="result-section" v-if="outlineContent || isGenerating">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-draft-line"></i>
              论文大纲
              <small v-if="outlineContent">{{ formData.query }}</small>
            </h3>
            <div class="result-actions" v-if="outlineContent">
              <button class="action-button" @click="generateFullPaper" :disabled="isGeneratingPaper">
                <i class="ri-file-text-line"></i>
                {{ isGeneratingPaper ? '生成中...' : '生成完整论文' }}
              </button>
              <button class="action-button" @click="copyOutline">
                <i class="ri-file-copy-line"></i>
                复制
              </button>
              <button class="action-button" @click="downloadOutline">
                <i class="ri-download-line"></i>
                下载
              </button>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isGenerating" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">正在生成论文大纲，请稍候...</div>
            </div>
            
            <!-- 大纲内容 -->
            <div v-if="outlineContent && !isGenerating" class="outline-content markdown-body">
              <div v-html="formattedOutlineContent"></div>
              <pre class="markdown-source" style="display: none;">{{ outlineContent }}</pre>
            </div>
          </div>
        </div>
        
        <!-- 完整论文内容显示区域 -->
        <div class="result-section" v-if="paperContent && !isGeneratingPaper" style="margin-top: 20px;">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              完整论文
              <small v-if="paperContent">{{ formData.query }}</small>
            </h3>
            <div class="result-actions" v-if="paperContent">
              <button class="action-button" @click="copyPaper">
                <i class="ri-file-copy-line"></i>
                复制
              </button>
              <button class="action-button" @click="downloadPaper">
                <i class="ri-download-line"></i>
                下载
              </button>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isGeneratingPaper" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">正在生成完整论文，请稍候...</div>
            </div>
            
            <!-- 论文内容 -->
            <div v-if="paperContent && !isGeneratingPaper" class="paper-content markdown-body">
              <div v-html="formattedPaperContent"></div>
              <pre class="markdown-source" style="display: none;">{{ paperContent }}</pre>
            </div>
          </div>
        </div>
        
        <!-- 未生成大纲时的提示 -->
        <div class="empty-result" v-if="!outlineContent && !isGenerating">
          <div class="empty-content">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
            <p class="empty-message">请输入论文主题并点击"生成论文大纲"按钮开始创作</p>
            <p class="empty-tip">或从左侧示例主题中选择一个</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士弹窗 -->
    <el-dialog
      title="论文大纲编写小贴士"
      v-model:visible="showTipsDialog"
      width="550px"
      custom-class="tips-dialog"
    >
      <div class="tips-content">
        <h4><i class="ri-checkbox-circle-line"></i> 什么是好的论文大纲？</h4>
        <p>一个好的论文大纲应该层次分明、逻辑清晰，能够涵盖论文的主要内容，包括引言、文献综述、研究方法、结果分析和结论等部分。</p>
        
        <h4><i class="ri-checkbox-circle-line"></i> 如何使用本工具？</h4>
        <p>输入您的论文主题或研究问题，系统将自动为您生成一个完整的论文框架，包括各章节和小节的标题及简要内容提示。</p>
        
        <h4><i class="ri-checkbox-circle-line"></i> 优化输入提示</h4>
        <ul>
          <li>明确具体的研究领域和问题</li>
          <li>可以加入研究方法或研究视角</li>
          <li>指明目标受众（例如：学术界、行业专家）</li>
          <li>如有需要，可指定论文类型（如综述、实证研究等）</li>
        </ul>
        
        <h4><i class="ri-checkbox-circle-line"></i> 后续步骤</h4>
        <p>生成的大纲仅供参考，您可能需要根据实际研究情况进行调整。建议在大纲的基础上，先撰写引言和结论，再填充具体内容。</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="showTipsDialog = false">我知道了</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import 'github-markdown-css/github-markdown.css'

export default {
  name: 'PaperOutline',
  data() {
    return {
      formData: {
        query: ''
      },
      rules: {
        query: [
          { required: true, message: '请输入论文主题或要求', trigger: 'blur' }
        ]
      },
      outlineContent: '',
      paperContent: '',
      isGenerating: false,
      isGeneratingPaper: false,
      showTipsDialog: false,
      examples: [
        { 
          title: '人工智能在医疗领域的应用及挑战', 
          description: '探讨AI技术如何改变医疗诊断、药物研发、精准医疗等领域，以及所面临的数据隐私、伦理和技术限制问题。'
        },
        { 
          title: '可持续发展与绿色能源技术的未来趋势', 
          description: '分析可再生能源技术的最新进展，包括太阳能、风能、氢能等在应对气候变化和实现碳中和目标中的作用。'
        },
        { 
          title: '数字经济时代的隐私保护与数据安全', 
          description: '研究大数据环境下个人隐私保护的理论框架、技术手段和法律法规，以及企业数据治理的最佳实践。'
        },
        { 
          title: '全球气候变化对生物多样性的影响研究', 
          description: '分析气候变暖、极端天气等因素如何影响生态系统平衡和物种多样性，以及相应的保护策略和国际合作。'
        }
      ]
    }
  },
  computed: {
    // 将大纲内容转换为HTML
    formattedOutlineContent() {
      if (!this.outlineContent) return ''
      // 确保outlineContent是字符串类型
      let content = this.outlineContent
      if (typeof content !== 'string') {
        console.error('formattedOutlineContent: outlineContent非字符串类型:', typeof content, content)
        content = String(content) // 尝试转换为字符串
      }
      const rawHtml = marked(content)
      return DOMPurify.sanitize(rawHtml)
    },
    // 将论文内容转换为HTML
    formattedPaperContent() {
      if (!this.paperContent) return ''
      // 确保paperContent是字符串类型
      let content = this.paperContent
      if (typeof content !== 'string') {
        console.error('formattedPaperContent: paperContent非字符串类型:', typeof content, content)
        content = String(content) // 尝试转换为字符串
      }
      const rawHtml = marked(content)
      return DOMPurify.sanitize(rawHtml)
    }
  },
  methods: {
    async generateOutline() {
      if (!this.formData.query.trim()) {
        this.$message.warning('请输入论文主题或要求')
        return
      }

      this.isGenerating = true
      this.outlineContent = ''

      console.log('开始请求论文大纲API, 主题:', this.formData.query)

      try {
        const response = await axios.post('/api/academic/paper_outline', {
          query: this.formData.query
        })

        console.log('API响应状态:', response.status)
        console.log('API响应数据:', response.data)

        if (response.data.status === 'success') {
          this.outlineContent = response.data.data || ''
          this.$message.success('大纲生成成功')
        } else {
          console.error('API返回错误状态:', response.data.message)
          this.$message.error(response.data.message || '生成论文大纲失败')
        }
      } catch (error) {
        console.error('API请求错误:', error)
        this.$message.error(`请求失败: ${error.message}`)
      } finally {
        this.isGenerating = false
      }
    },
    
    resetForm() {
      this.formData.query = ''
      this.outlineContent = ''
    },
    
    useExample(example) {
      this.formData.query = example.title
    },
    
    copyOutline() {
      try {
        // 直接复制原始的Markdown内容
        navigator.clipboard.writeText(this.outlineContent)
        this.$message.success('已复制Markdown格式的大纲内容')
      } catch (error) {
        console.error('复制到剪贴板失败:', error)
        this.$message.error('复制失败，请手动复制')
      }
    },
    
    downloadOutline() {
      try {
        const element = document.createElement('a')
        const file = new Blob([this.outlineContent], { type: 'text/plain' })
        element.href = URL.createObjectURL(file)
        element.download = `论文大纲_${this.formData.query.substring(0, 20)}.md`
        document.body.appendChild(element)
        element.click()
        document.body.removeChild(element)
      } catch (error) {
        console.error('下载文件失败:', error)
        this.$message.error('下载失败，请稍后重试')
      }
    },
    
    showTips() {
      this.showTipsDialog = true
    },
    
    // 从大纲生成完整论文
    async generateFullPaper() {
      if (!this.outlineContent) {
        this.$message.warning('请先生成论文大纲')
        return
      }

      this.isGeneratingPaper = true
      this.paperContent = ''

      console.log('开始请求生成完整论文API, 主题:', this.formData.query)

      try {
        const response = await axios.post('/api/academic/paper_from_outline', {
          query: this.formData.query,
          outline: this.outlineContent
        })

        console.log('API响应状态:', response.status)
        console.log('API响应数据:', response.data)

        if (response.data.status === 'success') {
          this.paperContent = response.data.data || ''
          this.$message.success('论文生成成功')
        } else {
          console.error('API返回错误状态:', response.data.message)
          this.$message.error(response.data.message || '生成完整论文失败')
        }
      } catch (error) {
        console.error('API请求错误:', error)
        this.$message.error(`请求失败: ${error.message}`)
      } finally {
        this.isGeneratingPaper = false
      }
    },
    
    // 复制生成的论文内容
    copyPaper() {
      try {
        navigator.clipboard.writeText(this.paperContent)
        this.$message.success('已复制Markdown格式的论文内容')
      } catch (error) {
        console.error('复制到剪贴板失败:', error)
        this.$message.error('复制失败，请手动复制')
      }
    },
    
    // 下载生成的论文
    downloadPaper() {
      try {
        const element = document.createElement('a')
        const file = new Blob([this.paperContent], { type: 'text/plain' })
        element.href = URL.createObjectURL(file)
        element.download = `论文_${this.formData.query.substring(0, 20)}.md`
        document.body.appendChild(element)
        element.click()
        document.body.removeChild(element)
      } catch (error) {
        console.error('下载文件失败:', error)
        this.$message.error('下载失败，请稍后重试')
      }
    }
  }
}
</script>

<style scoped>
.paper-outline-page {
  padding: 10px 20px 20px 20px;
  margin-top: -10px; /* 向上移动整个内容 */
}

/* 页面头部样式 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-nav h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.main-title {
  color: #ba003f;
  font-weight: 600;
  font-size: 26px;
}

.page-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #e0e0e0;
}

.action-btn i {
  font-size: 18px;
  color: #666;
}

/* 主容器两列布局 */
.main-container {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 20px;
  margin-top: 0; /* 减少顶部间距 */
}

/* 左侧栏样式 */
.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 左侧输入部分 */
.input-section, .examples-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px 20px; /* 减少上下内边距 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.section-header {
  margin-bottom: 12px; /* 减少标题与内容间距 */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 18px;
  color: #c62828; /* 紫荆红色 */
  margin: 0;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 8px;
  color: var(--primary-color, #ba003f);
}

.section-title small {
  font-size: 14px;
  color: #666;
  font-weight: normal;
  margin-left: 10px;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.form-group {
  margin-bottom: 16px;
}

.form-label, label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
}

.required:after {
  content: '*';
  color: #f56c6c;
  margin-left: 4px;
}

.form-control {
  width: 100%;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

/* 行动按钮样式 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 4px;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn i {
  margin-right: 6px;
  font-size: 16px;
}

.btn-primary {
  background-color: var(--primary-color, #ba003f);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #d40046;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 右侧示例和结果部分 */
.right-column {
  min-height: 500px;
}

.result-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: 100%;
}

/* 示例论文主题部分 */
.examples-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px 20px; /* 减少上下内边距 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.section-header {
  margin-bottom: 12px; /* 减少标题与内容间距 */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 18px;
  color: #c62828; /* 紫荆红色 */
  margin: 0;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 8px;
  color: var(--primary-color, #ba003f);
}

/* 修改为网格布局的选择项 */
.examples-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 15px;
}

.example-item {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #e0e0e0;
}

.example-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f0f0f0;
}

.example-item h4 {
  color: #ba003f;
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 16px;
}

.example-item p {
  color: #666;
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
}

/* 结果部分样式 */
.result-actions {
  display: flex;
  gap: 8px;
}

.action-button {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #f5f5f5;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:hover {
  background: #e0e0e0;
}

.action-button i {
  margin-right: 4px;
  font-size: 14px;
}

.result-content-wrapper {
  position: relative;
  min-height: 200px;
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
  border-radius: 8px;
  z-index: 10;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--primary-color, #ba003f);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-text {
  color: #666;
  font-size: 14px;
}

.outline-content {
  max-height: 500px;
  overflow-y: auto;
  padding: 16px;
  border-radius: 4px;
  border: 1px solid #eee;
  background-color: #fafafa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
}

.outline-content pre {
  background-color: #f6f8fa;
  border-radius: 3px;
  padding: 16px;
  overflow: auto;
}

.outline-content code {
  font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
  font-size: 85%;
  padding: 0.2em 0.4em;
  margin: 0;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
}

/* 隐藏原始Markdown源码，但保留用于复制 */
.markdown-source {
  display: none;
}

/* 调整Markdown渲染后的样式 */
:deep(.markdown-body) {
  font-size: 14px;
  line-height: 1.6;
}

:deep(.markdown-body h1) {
  font-size: 24px;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eaecef;
}

:deep(.markdown-body h2) {
  font-size: 20px;
  margin-top: 24px;
  margin-bottom: 16px;
  padding-bottom: 6px;
  border-bottom: 1px solid #eaecef;
}

:deep(.markdown-body h3) {
  font-size: 16px;
  margin-top: 20px;
  margin-bottom: 12px;
}

:deep(.markdown-body p) {
  margin-bottom: 12px;
}

:deep(.markdown-body ul, .markdown-body ol) {
  padding-left: 20px;
  margin-bottom: 12px;
}

:deep(.markdown-body li) {
  margin-bottom: 4px;
}

/* 空状态样式 */
.empty-result {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-content {
  text-align: center;
  padding: 30px;
}

.empty-image {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.empty-message {
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
}

.empty-tip {
  font-size: 14px;
  color: #999;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinning {
  animation: spin 1s linear infinite;
}

/* 小贴士对话框样式 */
:deep(.tips-dialog) {
  border-radius: 8px;
}

:deep(.tips-dialog .el-dialog__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

:deep(.tips-dialog .el-dialog__body) {
  padding: 20px;
}

.tips-content h4 {
  color: var(--primary-color, #ba003f);
  margin: 16px 0 8px;
  display: flex;
  align-items: center;
}

.tips-content h4:first-child {
  margin-top: 0;
}

.tips-content h4 i {
  margin-right: 6px;
}

.tips-content p {
  margin: 8px 0;
  line-height: 1.5;
}

.tips-content ul {
  margin: 8px 0;
  padding-left: 20px;
}

.tips-content li {
  margin-bottom: 6px;
}

/* 全局样式，应用于生成的Markdown内容 */
:deep(.markdown-body) {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
}

:deep(.markdown-body h1) {
  color: var(--primary-color, #ba003f);
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
}

:deep(.markdown-body h2) {
  padding-bottom: 0.3em;
  border-bottom: 1px solid #eee;
}

:deep(.markdown-body blockquote) {
  padding: 0 1em;
  color: #666;
  border-left: 0.25em solid #dfe2e5;
}

/* 在深色模式下调整样式 */
@media (prefers-color-scheme: dark) {
  .page-nav h2, .section-title {
    color: #e0e0e0;
  }
  
  .main-title {
    color: #ff4081; /* 深色模式下标题使用更亮的红色 */
  }
  
  .action-btn, .btn-secondary {
    background: #333;
  }
  
  .action-btn:hover, .btn-secondary:hover:not(:disabled) {
    background: #444;
  }
  
  .action-btn i, .btn-secondary {
    color: #ccc;
  }
  
  .input-section, .examples-section, .result-section, .empty-result {
    background-color: #262a37;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
  }
  
  .form-label, label, .example-info h4 {
    color: #e0e0e0;
  }
  
  .example-card {
    background-color: #2d313e;
    border-color: #414858;
  }
  
  .example-card:hover {
    background-color: #33394a;
  }
  
  .example-info p, .section-title small, .form-tip, .empty-message, .empty-tip {
    color: #a0a0a0;
  }
  
  .action-button {
    background: #333;
    border-color: #555;
    color: #ccc;
  }
  
  .action-button:hover {
    background: #444;
  }
  
  .outline-content {
    border-color: #3a3f4d;
    background-color: #2d313e;
  }
  
  .loading-overlay {
    background-color: rgba(38, 42, 55, 0.8);
  }
  
  .loading-text {
    color: #a0a0a0;
  }
  
  :deep(.markdown-body) {
    color: #e0e0e0;
    background-color: transparent;
  }
  
  :deep(.markdown-body h2) {
    border-bottom-color: #3a3f4d;
  }
  
  :deep(.markdown-body blockquote) {
    color: #a0a0a0;
    border-left-color: #4c5464;
  }
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .main-container {
    grid-template-columns: 1fr;
  }
  
  .example-cards {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}
</style>