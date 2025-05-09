<template>
  <div class="wenxin-search-page">
    <h2>学术搜索</h2>
    
    <div class="search-container">
      <div class="search-input-wrapper">
        <el-input 
          v-model="searchQuery" 
          placeholder="请输入研究主题、论文关键词或学术问题..." 
          @keyup.enter="handleSearch"
          :disabled="isSearching"
          class="enhanced-search-input"
        >
          <template #prefix>
            <i class="el-icon-search search-icon"></i>
          </template>
          <template #append>
            <el-button 
              class="search-button"
              :loading="isSearching" 
              @click="handleSearch"
            >
              {{ isSearching ? '搜索中...' : '搜索' }}
            </el-button>
          </template>
        </el-input>
      </div>
    </div>

    <div v-if="isSearching || searchResults.length > 0" class="search-results">
      <el-card shadow="hover" class="results-card">
        <template #header>
          <div class="card-header">
            <span>搜索结果</span>
            <div class="search-status">
              <div v-if="isSearching" class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <el-tag v-else-if="searchResults.length > 0" type="success" class="custom-success-tag">搜索完成</el-tag>
            </div>
          </div>
        </template>
        
        <!-- 搜索结果内容展示 -->
        <div class="content-area" v-loading="isSearching && !hasPartialResults">
          <transition name="fade">
            <div class="search-result-content markdown-body" v-html="formattedContent"></div>
          </transition>
        </div>
        
        <!-- 引用来源展示 -->
        <div v-if="references.length > 0" class="reference-area">
          <h3>参考来源</h3>
          <transition-group name="list" tag="div">
            <div v-for="(ref, index) in references" :key="index" class="reference-item">
              <h4>
                <a :href="ref.orgUrl" target="_blank" rel="noopener noreferrer">
                  {{ ref.title }}
                </a>
              </h4>
              <p>{{ ref.abstract }}</p>
            </div>
          </transition-group>
        </div>
      </el-card>
    </div>
    
    <div v-if="errorMessage" class="error-message">
      <el-alert
        :title="errorMessage"
        type="error"
        show-icon
        :closable="false"
      />
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import mermaid from 'mermaid';

// 安全地初始化mermaid
let mermaidInitialized = false;
function initMermaid() {
  if (!mermaidInitialized) {
    try {
      mermaid.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'
      });
      mermaidInitialized = true;
    } catch (e) {
      console.error('Failed to initialize mermaid:', e);
    }
  }
}

export default {
  name: 'WenxinSearch',
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      isSearching: false,
      hasPartialResults: false,
      errorMessage: '',
      contentText: '',
      references: [],
      mermaidCharts: [],
      isMermaidRendering: false,
      renderAttempts: 0
    }
  },
  mounted() {
    // 延迟初始化mermaid
    this.$nextTick(() => {
      initMermaid();
    });
  },
  computed: {
    formattedContent() {
      // 处理内容并渲染Markdown
      if (!this.contentText) return '';
      
      // 设置marked选项
      marked.setOptions({
        highlight: (code, lang) => {
          // 对于mermaid图表，不使用highlight.js处理
          if (lang === 'mermaid') {
            return code;
          }
          
          if (lang && hljs.getLanguage(lang)) {
            try {
              return hljs.highlight(code, { language: lang }).value;
            } catch (e) {
              console.error('Highlight error:', e);
            }
          }
          return hljs.highlightAuto(code).value;
        },
        breaks: true
      });
      
      // 解析markdown
      const htmlContent = marked(this.contentText);
      
      // 安全处理
      const cleanHtml = DOMPurify.sanitize(htmlContent);
      
      return cleanHtml;
    }
  },
  updated() {
    this.renderMermaidDiagrams();
  },
  methods: {
    async handleSearch() {
      if (!this.searchQuery.trim() || this.isSearching) return;
      
      this.isSearching = true;
      this.searchResults = [];
      this.contentText = '';
      this.references = [];
      this.errorMessage = '';
      this.hasPartialResults = false;
      
      try {
        // 创建请求
        const response = await fetch('/api/v1/wenxin/ai-search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            userQuery: this.searchQuery
          })
        });
        
        if (!response.ok) {
          throw new Error(`搜索请求失败: ${response.status}`);
        }
        
        // 处理SSE流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        const processChunk = ({ done, value }) => {
          if (done) {
            console.log('Stream complete');
            this.isSearching = false;
            return;
          }
          
          // 解码接收到的数据并添加到缓冲区
          buffer += decoder.decode(value, { stream: true });
          
          // 处理SSE事件
          const lines = buffer.split('\n');
          buffer = lines.pop(); // 最后一行可能不完整，保留到下次处理
          
          for (const line of lines) {
            if (line.trim() === '') continue;
            
            // 解析SSE事件
            if (line.startsWith('event:')) {
              const eventType = line.slice(6).trim();
              if (eventType === 'lastMessage') {
                this.isSearching = false;
              }
            } else if (line.startsWith('data:')) {
              try {
                const jsonData = JSON.parse(line.slice(5).trim());
                this.handleEventData(jsonData);
                
                // 标记我们已经收到部分结果
                if (!this.hasPartialResults) {
                  this.hasPartialResults = true;
                }
              } catch (error) {
                console.error('Error parsing JSON:', error, line);
              }
            }
          }
          
          // 继续读取下一个块
          return reader.read().then(processChunk);
        };
        
        // 开始读取流
        reader.read().then(processChunk);
        
      } catch (error) {
        console.error('Search error:', error);
        this.errorMessage = `搜索出错: ${error.message}`;
        this.isSearching = false;
      }
    },
    
    handleEventData(data) {
      // 处理事件数据
      if (data.errCode !== 0) {
        this.errorMessage = `API错误: ${data.errMsg || '未知错误'}`;
        return;
      }
      
      if (data.raw) {
        // 处理内容
        if (data.raw.content !== undefined) {
          const previousContent = this.contentText;
          this.contentText += data.raw.content;
          
          // 如果内容变化较大，延迟触发mermaid渲染
          if (this.contentText.length - previousContent.length > 100) {
            this.$nextTick(() => {
              this.renderMermaidDiagrams();
            });
          }
        }
        
        // 处理搜索引用列表
        if (data.raw.searchReferList && Array.isArray(data.raw.searchReferList)) {
          // 合并去重引用列表
          const newRefs = data.raw.searchReferList.filter(ref => 
            !this.references.some(existingRef => existingRef.orgUrl === ref.orgUrl)
          );
          this.references.push(...newRefs);
        }
        
        this.searchResults.push(data);
      }
    },
    
    // 检查内容中是否包含mermaid图表
    hasMermaidDiagrams(content) {
      return /```mermaid/.test(content);
    },
    
    renderMermaidDiagrams() {
      if (this.isMermaidRendering) return;
      
      // 最多尝试渲染5次
      if (this.renderAttempts >= 5) {
        console.warn('Max mermaid render attempts reached');
        return;
      }
      this.renderAttempts++;
      
      this.isMermaidRendering = true;
      
      // 确保mermaid已初始化
      if (!mermaidInitialized) {
        initMermaid();
      }
      
      setTimeout(() => {
        try {
          // 检查DOM是否准备好
          if (!document || !document.querySelectorAll) {
            throw new Error('DOM not ready');
          }
          
          // 寻找所有mermaid代码块并渲染
          const elements = document.querySelectorAll('.language-mermaid');
          
          if (elements && elements.length > 0) {
            console.log(`Found ${elements.length} mermaid diagrams to render`);
            
            elements.forEach((element, index) => {
              if (element && !element.getAttribute('data-processed') && element.textContent.trim()) {
                try {
                  const id = `mermaid-diagram-${Date.now()}-${index}`;
                  const content = element.textContent.trim();
                  
                  // 检查mermaid语法是否有效 - 使用try/catch包裹
                  try {
                    // 简单验证语法而不实际渲染
                    if (content.includes('graph') || content.includes('sequenceDiagram') || 
                        content.includes('classDiagram') || content.includes('gantt')) {
                      
                      // 标记为处理中
                      element.setAttribute('data-processing', 'true');
                      
                      // 避免在原始元素上渲染
                      const container = document.createElement('div');
                      container.className = 'mermaid-container';
                      container.style.margin = '10px 0';
                      element.parentNode.insertBefore(container, element.nextSibling);
                      
                      try {
                        // 在新容器中渲染
                        mermaid.render(id, content, (svgCode) => {
                          if (container && container.parentNode) {
                            container.innerHTML = svgCode;
                            element.setAttribute('data-processed', 'true');
                            element.removeAttribute('data-processing');
                          }
                        });
                      } catch (renderError) {
                        console.error('Failed during mermaid render:', renderError);
                        this.handleMermaidRenderError(element, container);
                      }
                    } else {
                      // 内容不是有效的mermaid图表
                      element.setAttribute('data-processed', 'invalid');
                    }
                  } catch (parseError) {
                    console.warn('Failed to parse mermaid diagram:', parseError);
                    this.handleMermaidRenderError(element);
                  }
                } catch (innerError) {
                  console.warn('Element handling error:', innerError);
                  // 标记为已处理以避免重复尝试渲染
                  if (element) {
                    element.setAttribute('data-processed', 'failed');
                  }
                }
              }
            });
          }
        } catch (error) {
          console.error('Mermaid rendering error:', error);
        } finally {
          this.isMermaidRendering = false;
        }
      }, 1000); // 增加延迟，确保DOM已完全加载
    },
    
    handleMermaidRenderError(element, container = null) {
      // 标记为已处理失败
      if (element) {
        element.setAttribute('data-processed', 'failed');
        element.removeAttribute('data-processing');
      }
      
      // 如果创建了容器但渲染失败，显示错误信息
      if (container && container.parentNode) {
        container.innerHTML = '<div style="color:red;padding:5px;border:1px solid #ffcccc;background:#fff5f5;border-radius:4px;margin:5px 0;font-size:12px;">图表渲染失败</div>';
      }
    }
  }
}
</script>

<style scoped>
.wenxin-search-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: transparent;
}

.search-container {
  margin: 20px 0 30px;
  display: flex;
  justify-content: center;
  background-color: transparent;
  box-shadow: none;
  border: none;
}

.search-input-wrapper {
  width: 100%;
  max-width: 800px;
  background-color: transparent;
}

.enhanced-search-input :deep(.el-input__inner) {
  height: 50px;
  font-size: 16px;
  padding-left: 15px;
  border-radius: 8px 0 0 8px;
  transition: all 0.3s;
  border: 1px solid #dcdfe6;
  background-color: white;
}

.enhanced-search-input:hover :deep(.el-input__inner) {
  border-color: #c0c4cc;
  box-shadow: 0 0 0 1px rgba(192, 196, 204, 0.1);
}

.enhanced-search-input :deep(.el-input__inner):focus {
  border-color: #C1232B;
  box-shadow: 0 0 0 2px rgba(193, 35, 43, 0.2);
}

/* 强制覆盖Element UI的样式 */
.search-button {
  height: 50px !important;
  padding: 0 20px !important;
  font-size: 16px !important;
  border-radius: 0 8px 8px 0 !important;
  border: none !important;
  background-color: #C1232B !important;
  color: white !important;
}

.search-button:hover, 
.search-button:focus, 
.search-button:active {
  background-color: #d63742 !important;
  color: white !important;
}

/* 覆盖成功标签颜色 */
:deep(.custom-success-tag) {
  background-color: #C1232B !important;
  border-color: #C1232B !important;
}

.search-icon {
  color: #909399;
  font-size: 18px;
  margin-right: 5px;
}

.search-results {
  margin-top: 30px;
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.results-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.results-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ebeef5;
}

.search-status {
  display: flex;
  align-items: center;
}

.typing-indicator {
  display: flex;
  align-items: center;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #C1232B;
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px;
  opacity: 0.7;
  animation: typing 1.2s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
  100% { transform: translateY(0); }
}

.content-area {
  min-height: 200px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  position: relative;
}

.search-result-content {
  text-align: left;
  line-height: 1.6;
}

.reference-area {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding: 20px;
}

.reference-area h3 {
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.reference-item {
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 6px;
  background-color: #f9f9f9;
  border-left: 3px solid #C1232B;
  transition: all 0.3s;
}

.reference-item:hover {
  background-color: #fff5f5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.reference-item h4 {
  margin-bottom: 8px;
  font-weight: 600;
}

.reference-item a {
  color: #C1232B;
  text-decoration: none;
  transition: color 0.2s;
}

.reference-item a:hover {
  color: #e14b53;
  text-decoration: underline;
}

.reference-item p {
  color: #606266;
  margin: 5px 0 0 0;
  font-size: 14px;
  line-height: 1.5;
}

.error-message {
  margin-top: 20px;
}

/* 添加动画过渡效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.list-enter-active, .list-leave-active {
  transition: all 0.5s;
}
.list-enter-from, .list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 添加markdown样式 */
:deep(.markdown-body) {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6;
}

:deep(.markdown-body h1),
:deep(.markdown-body h2),
:deep(.markdown-body h3),
:deep(.markdown-body h4) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

:deep(.markdown-body code) {
  padding: 0.2em 0.4em;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
}

:deep(.markdown-body pre) {
  padding: 16px;
  overflow: auto;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 3px;
}

:deep(.markdown-body pre code) {
  padding: 0;
  background-color: transparent;
}

:deep(.markdown-body img) {
  max-width: 100%;
  box-sizing: border-box;
}

:deep(.markdown-body table) {
  border-spacing: 0;
  border-collapse: collapse;
  width: 100%;
  overflow: auto;
}

:deep(.markdown-body table th),
:deep(.markdown-body table td) {
  padding: 6px 13px;
  border: 1px solid #dfe2e5;
}

:deep(.markdown-body table tr) {
  background-color: #fff;
  border-top: 1px solid #c6cbd1;
}

:deep(.markdown-body table tr:nth-child(2n)) {
  background-color: #f6f8fa;
}

:deep(.markdown-body blockquote) {
  padding: 0 1em;
  color: #6a737d;
  border-left: 0.25em solid #dfe2e5;
}
</style>