<template>
  <div class="wenxin-search-page">
    <h2 class="page-title">学术搜索</h2>
    
    <div class="search-container">
      <div class="search-input-group">
        <el-input 
          v-model="searchQuery" 
          placeholder="请输入学术研究内容，获取专业搜索结果" 
          @keyup.enter="handleSearch"
          :disabled="isSearching"
          class="search-input"
        >
          <template #append>
            <el-button 
              :loading="isSearching" 
              @click="handleSearch"
              type="primary"
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
            <el-tag v-if="isSearching" type="info">加载中...</el-tag>
            <el-tag v-else-if="searchResults.length > 0" type="success">搜索完成</el-tag>
          </div>
        </template>
        
        <!-- 搜索结果内容展示 -->
        <div class="content-area" v-loading="isSearching && !hasPartialResults">
          <div class="search-result-content markdown-body" v-html="formattedContent"></div>
        </div>
        
        <!-- 引用来源展示 -->
        <div v-if="references.length > 0" class="reference-area">
          <h3 class="reference-title">参考来源</h3>
          <div v-for="(ref, index) in references" :key="index" class="reference-item">
            <h4>
              <a :href="ref.orgUrl" target="_blank" rel="noopener noreferrer">
                {{ ref.title }}
              </a>
            </h4>
            <p>{{ ref.abstract }}</p>
          </div>
        </div>
      </el-card>
    </div>
    
    <div v-if="!isSearching && searchResults.length === 0 && !errorMessage" class="empty-state">
      <div class="empty-state-icon">
        <i class="el-icon-search"></i>
      </div>
      <div class="empty-state-text">
        输入您的学术问题或研究主题，获取专业的搜索结果和引用
      </div>
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
      isMermaidRendering: false
    }
  },
  computed: {
    formattedContent() {
      // 处理内容并渲染Markdown
      if (!this.contentText) return '';
      
      // 设置marked选项
      marked.setOptions({
        highlight: (code, lang) => {
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
    this.$nextTick(() => {
      this.renderMermaidDiagrams();
    });
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
          this.contentText += data.raw.content;
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
    
    renderMermaidDiagrams() {
      if (this.isMermaidRendering) return;
      
      this.isMermaidRendering = true;
      
      // 检查是否在浏览器环境中
      if (typeof window === 'undefined' || typeof document === 'undefined') {
        console.warn('Mermaid rendering skipped - not in browser environment');
        this.isMermaidRendering = false;
        return;
      }
      
      // 配置Mermaid
      try {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'default',
          securityLevel: 'loose',
          deterministicIds: true, // 使用确定性ID以避免重复渲染
          fontFamily: 'monospace',
          flowchart: {
            htmlLabels: true
          }
        });
        
        // 使用requestAnimationFrame确保DOM已经完全渲染
        window.requestAnimationFrame(() => {
          try {
            // 使用一个独立的容器进行渲染
            const elements = document.querySelectorAll('.language-mermaid');
            
            if (elements.length === 0) {
              console.log('No mermaid diagrams found to render');
              this.isMermaidRendering = false;
              return;
            }
            
            elements.forEach((element, index) => {
              if (!element || element.getAttribute('data-processed') === 'true') {
                return; // 跳过已处理的元素
              }
              
              const id = `mermaid-diagram-${Date.now()}-${index}`;
              const content = element.textContent || '';
              
              if (!content.trim()) {
                console.warn('Empty mermaid content, skipping render');
                return;
              }
              
              try {
                // 先验证Mermaid语法
                mermaid.parse(content);
                
                  // 创建一个新的渲染容器替换原始元素
                  const renderDiv = document.createElement('div');
                  renderDiv.className = 'mermaid-rendered';
                renderDiv.id = id;
                
                // 将渲染容器插入DOM
                if (element.parentNode) {
                  element.parentNode.insertBefore(renderDiv, element);
                  
                  // 使用异步渲染，避免阻塞UI
                  setTimeout(() => {
                    try {
                      mermaid.render(id, content)
                        .then(result => {
                          renderDiv.innerHTML = result.svg;
                      element.setAttribute('data-processed', 'true');
                      element.style.display = 'none';
                        })
                        .catch(err => {
                          console.error('Mermaid render promise error:', err);
                          renderDiv.innerHTML = '<div class="mermaid-error">图表渲染失败</div>';
                          element.style.display = 'block'; // 显示原始代码
                        });
                    } catch (asyncError) {
                      console.error('Async mermaid render error:', asyncError);
                      renderDiv.innerHTML = '<div class="mermaid-error">图表渲染失败</div>';
                      element.style.display = 'block';
                    }
                  }, 0);
                }
              } catch (parseError) {
                console.error('Mermaid parsing error:', parseError);
                // 显示解析错误
                  element.style.display = 'block';
                const errorDiv = document.createElement('div');
                errorDiv.className = 'mermaid-error';
                errorDiv.textContent = '图表语法错误，无法渲染';
                if (element.parentNode) {
                  element.parentNode.insertBefore(errorDiv, element);
                }
              }
            });
          } catch (error) {
            console.error('Mermaid rendering error:', error);
          } finally {
            this.isMermaidRendering = false;
          }
        });
      } catch (initError) {
        console.error('Mermaid initialization error:', initError);
        this.isMermaidRendering = false;
      }
    }
  }
}
</script>

<style scoped>
.wenxin-search-page {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.page-title {
  color: #333;
  font-size: 28px;
  margin-bottom: 30px;
  text-align: center;
  position: relative;
  font-weight: 600;
}

.page-title::after {
  content: "";
  display: block;
  width: 60px;
  height: 4px;
  background: #ba003f;
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 2px;
}

.search-container {
  margin: 30px 0;
  display: flex;
  justify-content: center;
}

.search-input-group {
  width: 100%;
  max-width: 800px;
}

.search-input :deep(.el-input__wrapper) {
  box-shadow: none !important;
  background-color: transparent;
}

.search-input :deep(.el-input__inner) {
  height: 50px;
  font-size: 16px;
  border-radius: 25px 0 0 25px;
  border: 2px solid #dcdfe6;
  border-right: none;
  transition: all 0.3s;
  background-color: white;
  box-shadow: none;
}

.search-input :deep(.el-input__inner:focus) {
  border-color: #ba003f;
}

.search-input :deep(.el-input-group__append) {
  border-radius: 0 25px 25px 0;
  background-color: #ba003f;
  border: 2px solid #ba003f;
  color: white;
}

.search-input :deep(.el-input-group__append .el-button) {
  background-color: transparent;
  border: none;
  color: white;
  font-size: 16px;
  font-weight: 500;
  padding: 12px 20px;
}

.search-results {
  margin-top: 30px;
  transition: all 0.3s ease;
}

.results-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.results-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  padding: 15px 20px;
  font-size: 18px;
  font-weight: 600;
}

.content-area {
  min-height: 200px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: white;
  border-radius: 4px;
}

.search-result-content {
  text-align: left;
  line-height: 1.7;
  font-size: 16px;
}

.reference-area {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.reference-title {
  color: #333;
  font-size: 20px;
  margin-bottom: 20px;
  position: relative;
  padding-left: 15px;
  font-weight: 600;
}

.reference-title::before {
  content: "";
  position: absolute;
  left: 0;
  top: 2px;
  bottom: 2px;
  width: 4px;
  background: #ba003f;
  border-radius: 2px;
}

.reference-item {
  margin-bottom: 20px;
  padding: 16px;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
  text-align: left;
  border-left: 3px solid #ba003f;
}

.reference-item:hover {
  background-color: #f3f5f9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.reference-item h4 {
  margin-bottom: 8px;
  color: #333;
  font-size: 17px;
}

.reference-item a {
  color: #ba003f;
  text-decoration: none;
  transition: all 0.2s ease;
  word-break: break-word;
}

.reference-item a:hover {
  color: #d4185b;
  text-decoration: underline;
}

.reference-item p {
  color: #606266;
  margin: 8px 0 0 0;
  font-size: 14px;
  line-height: 1.6;
}

.error-message {
  margin-top: 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 60px auto;
  padding: 40px;
  text-align: center;
  background-color: #f9fafc;
  border-radius: 8px;
  max-width: 800px;
}

.empty-state-icon {
  font-size: 48px;
  color: #ba003f;
  margin-bottom: 20px;
  opacity: 0.8;
}

.empty-state-text {
  color: #606266;
  font-size: 18px;
  line-height: 1.6;
  max-width: 400px;
}

/* 添加markdown样式 */
:deep(.markdown-body) {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.8;
  color: #24292e;
  font-size: 16px;
}

:deep(.markdown-body h1),
:deep(.markdown-body h2) {
  padding-bottom: 0.3em;
  border-bottom: 1px solid #eaecef;
  margin-top: 32px;
  margin-bottom: 20px;
  font-weight: 600;
  line-height: 1.25;
}

:deep(.markdown-body h1) {
  font-size: 2em;
  color: #ba003f;
}

:deep(.markdown-body h2) {
  font-size: 1.5em;
  color: #333;
}

:deep(.markdown-body h3) {
  font-size: 1.25em;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: #24292e;
}

:deep(.markdown-body h4) {
  font-size: 1em;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

:deep(.markdown-body code) {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
  font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
}

:deep(.markdown-body pre) {
  padding: 16px;
  overflow: auto;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 6px;
  margin-top: 0;
  margin-bottom: 16px;
  word-wrap: normal;
}

:deep(.markdown-body pre code) {
  padding: 0;
  margin: 0;
  font-size: 100%;
  word-break: normal;
  white-space: pre;
  background: transparent;
  border: 0;
  display: inline;
  overflow: visible;
}

:deep(.markdown-body img) {
  max-width: 100%;
  box-sizing: border-box;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

:deep(.markdown-body table) {
  border-spacing: 0;
  border-collapse: collapse;
  width: 100%;
  overflow: auto;
  margin-top: 16px;
  margin-bottom: 16px;
}

:deep(.markdown-body table th) {
  font-weight: 600;
  background-color: #f6f8fa;
}

:deep(.markdown-body table th),
:deep(.markdown-body table td) {
  padding: 8px 16px;
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
  border-left: 0.25em solid #ba003f;
  margin: 16px 0;
}

:deep(.markdown-body blockquote > :last-child) {
  margin-bottom: 0;
}

:deep(.markdown-body blockquote > :first-child) {
  margin-top: 0;
}

:deep(.markdown-body p) {
  margin-top: 0;
  margin-bottom: 16px;
}

:deep(.markdown-body a) {
  color: #ba003f;
  text-decoration: none;
}

:deep(.markdown-body a:hover) {
  text-decoration: underline;
}

:deep(.mermaid-rendered) {
  text-align: center;
  margin: 20px 0;
  overflow-x: auto;
}

:deep(.mermaid-rendered svg) {
  max-width: 100%;
  height: auto !important;
}

:deep(.mermaid-error) {
  color: #e74c3c;
  padding: 15px;
  background-color: #fdf2f0;
  border-left: 4px solid #e74c3c;
  margin: 10px 0;
  font-family: monospace;
  font-size: 14px;
  text-align: left;
}

@media (max-width: 768px) {
  .wenxin-search-page {
    padding: 20px 15px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .search-input :deep(.el-input__inner) {
    height: 45px;
    font-size: 15px;
  }
  
  .search-input :deep(.el-input-group__append .el-button) {
    font-size: 15px;
    padding: 10px 15px;
  }
  
  .content-area {
    padding: 15px;
  }
  
  .reference-item {
    padding: 12px;
  }
  
  .reference-item h4 {
    font-size: 16px;
  }
}
</style>