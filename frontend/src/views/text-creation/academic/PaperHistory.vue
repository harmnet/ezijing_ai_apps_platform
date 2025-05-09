<template>
  <div class="paper-history-page">
    <h1 class="page-title">论文生成历史记录</h1>
    
    <!-- 表格加载和错误状态 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>正在加载历史记录...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <i class="ri-error-warning-line"></i>
      <p>{{ error }}</p>
      <button class="btn btn-primary" @click="fetchHistory">重试</button>
    </div>
    
    <!-- 历史记录表格 -->
    <div v-else class="table-container">
      <!-- 无数据时显示提示 -->
      <div v-if="!papers.length" class="empty-state">
        <i class="ri-file-list-3-line"></i>
        <p>暂无历史记录</p>
      </div>
      
      <!-- 有数据时显示表格 -->
      <table v-else class="history-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>论文标题</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="paper in papers" :key="paper.id" :class="{'generating': paper.document_status === 'generating'}">
            <td>{{ paper.id }}</td>
            <td :title="paper.title">{{ paper.title }}</td>
            <td>
              <span :class="getStatusClass(paper.document_status)">
                {{ getStatusText(paper.document_status) }}
              </span>
            </td>
            <td>{{ formatDate(paper.created_at) }}</td>
            <td class="action-column">
              <div class="action-buttons">
                <button class="btn btn-small btn-outline" @click="viewDetails(paper)" title="查看详情">
                  <i class="ri-eye-line"></i>
                </button>
                <button 
                  class="btn btn-small btn-outline" 
                  v-if="paper.document_status === 'completed' && paper.download_url"
                  @click="downloadPaper(paper)"
                  title="下载论文"
                >
                  <i class="ri-download-line"></i>
                </button>
                <button 
                  class="btn btn-small btn-outline" 
                  v-if="paper.document_status === 'generating'"
                  @click="refreshStatus(paper)"
                  title="刷新状态"
                >
                  <i class="ri-refresh-line" :class="{'spinning': paper.refreshing}"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- 分页控件 -->
      <div class="pagination-container" v-if="total > 0">
        <div class="pagination-info">
          共 {{ total }} 条记录，每页 {{ perPage }} 条
        </div>
        <div class="pagination-controls">
          <button 
            class="btn btn-small" 
            :disabled="currentPage <= 1"
            @click="changePage(currentPage - 1)"
          >
            <i class="ri-arrow-left-s-line"></i> 上一页
          </button>
          <span class="page-number">{{ currentPage }} / {{ totalPages }}</span>
          <button 
            class="btn btn-small" 
            :disabled="currentPage >= totalPages"
            @click="changePage(currentPage + 1)"
          >
            下一页 <i class="ri-arrow-right-s-line"></i>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 论文详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="论文详情"
      width="80%"
      :before-close="closeDialog"
    >
      <div v-if="selectedPaper" class="paper-detail">
        <div class="detail-header">
          <h2>{{ selectedPaper.title }}</h2>
          <div class="meta-info">
            <span>ID: {{ selectedPaper.id }}</span>
            <span>状态: 
              <span :class="getStatusClass(selectedPaper.document_status)">
                {{ getStatusText(selectedPaper.document_status) }}
              </span>
            </span>
            <span>创建时间: {{ formatDate(selectedPaper.created_at) }}</span>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="section">
            <h3>研究主题</h3>
            <p>{{ selectedPaper.query }}</p>
          </div>
          
          <div class="section">
            <h3>论文大纲</h3>
            <div class="markdown-content" v-html="formatMarkdown(selectedPaper.outline)"></div>
          </div>
          
          <div class="section" v-if="selectedPaper.document_status === 'generating'">
            <h3>状态信息</h3>
            <p>{{ selectedPaper.status_message || '论文正在生成中，请稍后查看' }}</p>
            <button class="btn btn-outline" @click="refreshStatus(selectedPaper)">
              <i class="ri-refresh-line" :class="{'spinning': selectedPaper.refreshing}"></i> 
              刷新状态
            </button>
          </div>
          
          <div class="section" v-if="selectedPaper.document_status === 'completed'">
            <h3>下载论文</h3>
            <button 
              class="btn btn-outline" 
              v-if="selectedPaper.download_url"
              @click="downloadPaper(selectedPaper)"
            >
              <i class="ri-download-line"></i> 下载论文文档
            </button>
            <p v-else class="error-text">下载链接不可用，请刷新状态</p>
          </div>
          
          <div class="section" v-if="selectedPaper.document_status === 'failed'">
            <h3>错误信息</h3>
            <p class="error-text">{{ selectedPaper.status_message || '论文生成失败' }}</p>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <button class="btn btn-outline" @click="closeDialog">关闭</button>
          <button 
            class="btn btn-outline" 
            v-if="selectedPaper && selectedPaper.document_status === 'completed' && selectedPaper.download_url"
            @click="downloadPaper(selectedPaper)"
          >
            下载论文
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

export default {
  name: 'PaperHistory',
  setup() {
    // 状态变量
    const papers = ref([])
    const loading = ref(true)
    const error = ref(null)
    
    // 分页相关
    const currentPage = ref(1)
    const perPage = ref(10)
    const total = ref(0)
    const totalPages = ref(1)
    
    // 详情对话框
    const dialogVisible = ref(false)
    const selectedPaper = ref(null)
    
    // 获取历史记录
    const fetchHistory = async (page = 1) => {
      loading.value = true
      error.value = null
      
      try {
        const response = await axios.get(`/api/v1/academic/history`, {
          params: {
            page,
            per_page: perPage.value
          }
        })
        
        if (response.data.status === 'success') {
          papers.value = response.data.data.items
          total.value = response.data.data.total
          totalPages.value = response.data.data.pages
          currentPage.value = page
        } else {
          throw new Error(response.data.message || '获取历史记录失败')
        }
      } catch (err) {
        console.error('获取历史记录失败:', err)
        error.value = err.message || '获取历史记录失败，请稍后重试'
        ElMessage.error(`获取历史记录失败: ${error.value}`)
      } finally {
        loading.value = false
      }
    }
    
    // 刷新论文状态
    const refreshStatus = async (paper) => {
      if (!paper || !paper.doc_id) {
        console.error('刷新状态失败: 缺少必要参数', paper)
        ElMessage.error('刷新状态失败: 缺少必要参数')
        return
      }
      
      console.log('开始刷新论文状态:', paper.id, paper.title)
      console.log('请求参数:', { doc_id: paper.doc_id, paper_id: paper.id })
      
      // 设置刷新中状态
      const index = papers.value.findIndex(p => p.id === paper.id)
      if (index >= 0) {
        papers.value[index].refreshing = true
      }
      
      if (selectedPaper.value && selectedPaper.value.id === paper.id) {
        selectedPaper.value.refreshing = true
      }
      
      try {
        // 添加调试信息到请求中
        const response = await axios.post('/api/v1/academic/check_paper_status', {
          doc_id: paper.doc_id,
          paper_id: paper.id,
          debug_info: {
            client_time: new Date().toISOString(),
            browser: navigator.userAgent
          }
        })
        
        console.log('状态刷新响应:', response.data)
        
        if (response.data.status === 'success') {
          const statusResult = response.data.data
          console.log('状态刷新结果:', statusResult)
          
          // 更新列表中的状态
          if (index >= 0) {
            const oldStatus = papers.value[index].document_status
            papers.value[index].document_status = statusResult.document_status
            papers.value[index].status_message = statusResult.message
            
            console.log('状态更新:', oldStatus, '->', statusResult.document_status)
            
            // 如果API返回了下载链接，直接更新
            if (statusResult.download_url) {
              const oldUrl = papers.value[index].download_url
              papers.value[index].download_url = statusResult.download_url
              console.log('更新下载链接:', 
                oldUrl ? '已有链接被替换' : '新增链接', 
                statusResult.download_url.substring(0, 50) + '...'
              )
            } else {
              console.log('未收到下载链接')
            }
          } else {
            console.error('未找到索引位置:', paper.id)
          }
          
          // 更新选中论文的状态
          if (selectedPaper.value && selectedPaper.value.id === paper.id) {
            selectedPaper.value.document_status = statusResult.document_status
            selectedPaper.value.status_message = statusResult.message
            
            // 如果API返回了下载链接，直接更新
            if (statusResult.download_url) {
              selectedPaper.value.download_url = statusResult.download_url
              console.log('更新详情视图的下载链接')
            }
          }
          
          // 如果状态为completed但未获取到下载链接，再次尝试获取
          if (statusResult.document_status === 'completed' && !statusResult.download_url) {
            console.log('状态为已完成但未收到下载链接，尝试单独获取')
            await getDownloadLink(paper)
          }
          
          ElMessage.success('状态已更新')
          
          // 如果状态变为completed，提示用户
          if (statusResult.document_status === 'completed') {
            console.log('论文生成已完成', '下载链接存在:', !!statusResult.download_url)
            ElMessage.success('论文已生成完成，可以下载')
            
            // 尝试获取最新的论文详情
            try {
              console.log('获取论文最新详情')
              const detailResponse = await axios.get(`/api/v1/academic/history/${paper.id}`)
              if (detailResponse.data.status === 'success') {
                const freshPaper = detailResponse.data.data
                console.log('获取到最新论文详情:', freshPaper.document_status, '下载链接存在:', !!freshPaper.download_url)
                
                // 更新列表中的记录
                if (index >= 0) {
                  console.log('使用最新详情更新列表项')
                  papers.value[index] = freshPaper
                }
                
                // 更新详情视图
                if (selectedPaper.value && selectedPaper.value.id === paper.id) {
                  console.log('使用最新详情更新详情视图')
                  selectedPaper.value = freshPaper
                }
              }
            } catch (detailErr) {
              console.error('获取最新论文详情失败:', detailErr)
            }
            
            // 强制刷新列表以获取最新状态
            await fetchHistory(currentPage.value)
          }
          
          // 返回数据库更新标志
          if (statusResult.db_updated === true) {
            console.log('后端确认数据库已更新')
          } else {
            console.warn('后端未确认数据库更新状态:', statusResult.db_updated)
          }
        } else {
          console.error('状态刷新失败:', response.data.message)
          throw new Error(response.data.message || '刷新状态失败')
        }
      } catch (err) {
        console.error('刷新状态异常:', err)
        ElMessage.error(`刷新状态失败: ${err.message}`)
      } finally {
        // 清除刷新中状态
        if (index >= 0) {
          papers.value[index].refreshing = false
        }
        
        if (selectedPaper.value && selectedPaper.value.id === paper.id) {
          selectedPaper.value.refreshing = false
        }
        
        console.log('刷新状态操作完成')
      }
    }
    
    // 获取下载链接
    const getDownloadLink = async (paper) => {
      if (!paper || !paper.doc_id) return
      
      try {
        const response = await axios.post('/api/v1/academic/download_paper', {
          doc_id: paper.doc_id,
          paper_id: paper.id
        })
        
        if (response.data.status === 'success') {
          const downloadUrl = response.data.data
          
          // 更新列表中的下载链接
          const index = papers.value.findIndex(p => p.id === paper.id)
          if (index >= 0) {
            papers.value[index].download_url = downloadUrl
          }
          
          // 更新选中论文的下载链接
          if (selectedPaper.value && selectedPaper.value.id === paper.id) {
            selectedPaper.value.download_url = downloadUrl
          }
          
          return downloadUrl
        }
      } catch (err) {
        console.error('获取下载链接失败:', err)
        return null
      }
    }
    
    // 下载论文
    const downloadPaper = (paper) => {
      if (!paper || !paper.download_url) return
      
      // 在新标签页打开下载链接
      window.open(paper.download_url, '_blank')
      ElMessage.success('已打开下载链接，请在新标签页完成下载')
    }
    
    // 查看详情
    const viewDetails = async (paper) => {
      if (!paper) return
      
      try {
        // 获取最新的论文详情
        const response = await axios.get(`/api/v1/academic/history/${paper.id}`)
        
        if (response.data.status === 'success') {
          selectedPaper.value = response.data.data
          dialogVisible.value = true
        } else {
          throw new Error(response.data.message || '获取论文详情失败')
        }
      } catch (err) {
        console.error('获取论文详情失败:', err)
        ElMessage.error(`获取论文详情失败: ${err.message}`)
      }
    }
    
    // 关闭对话框
    const closeDialog = () => {
      dialogVisible.value = false
      selectedPaper.value = null
    }
    
    // 切换页码
    const changePage = (page) => {
      if (page < 1 || page > totalPages.value) return
      fetchHistory(page)
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'none': return '仅大纲'
        case 'generating': return '生成中'
        case 'completed': return '已完成'
        case 'failed': return '失败'
        default: return '未知'
      }
    }
    
    // 获取状态CSS类
    const getStatusClass = (status) => {
      switch (status) {
        case 'none': return 'status-none'
        case 'generating': return 'status-generating'
        case 'completed': return 'status-completed'
        case 'failed': return 'status-failed'
        default: return ''
      }
    }
    
    // 格式化Markdown为HTML
    const formatMarkdown = (markdown) => {
      if (!markdown) return ''
      // 确保markdown是字符串类型
      if (typeof markdown !== 'string') {
        console.error('formatMarkdown接收到非字符串类型:', typeof markdown, markdown)
        markdown = String(markdown) // 尝试转换为字符串
      }
      const rawHtml = marked(markdown)
      return DOMPurify.sanitize(rawHtml)
    }
    
    // 组件加载时获取数据
    onMounted(() => {
      fetchHistory()
    })
    
    return {
      papers,
      loading,
      error,
      currentPage,
      perPage,
      total,
      totalPages,
      dialogVisible,
      selectedPaper,
      fetchHistory,
      refreshStatus,
      downloadPaper,
      viewDetails,
      closeDialog,
      changePage,
      formatDate,
      getStatusText,
      getStatusClass,
      formatMarkdown
    }
  }
}
</script>

<style scoped>
.paper-history-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
  font-weight: 600;
}

.loading-container, .error-container, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #cb2b83; /* 紫荆红 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container i, .empty-state i {
  font-size: 48px;
  color: #cb2b83;
  margin-bottom: 20px;
}

.error-container p, .empty-state p {
  margin-bottom: 20px;
  color: #666;
}

.table-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  overflow: hidden;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th, .history-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.history-table th {
  background-color: #f8f8f8;
  font-weight: 600;
  color: #333;
}

.history-table tr:hover {
  background-color: #f5f5f5;
}

.history-table tr.generating {
  background-color: #f0f9ff;
}

.action-column {
  width: 120px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  border: none;
  transition: all 0.2s;
}

.btn-small {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-primary {
  background-color: #cb2b83; /* 紫荆红 */
  color: white;
}

.btn-primary:hover {
  background-color: #b82575;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background-color: #e5e5e5;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid #ddd;
  color: #666;
}

.btn-outline:hover {
  background-color: #f5f5f5;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-top: 1px solid #eee;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-number {
  margin: 0 10px;
}

.status-none {
  color: #909399;
}

.status-generating {
  color: #409eff;
}

.status-completed {
  color: #67c23a;
}

.status-failed {
  color: #f56c6c;
}

.paper-detail {
  padding: 20px;
}

.detail-header {
  margin-bottom: 24px;
  border-bottom: 1px solid #eee;
  padding-bottom: 16px;
}

.detail-header h2 {
  margin-bottom: 10px;
  color: #333;
}

.meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  color: #666;
  font-size: 14px;
}

.section {
  margin-bottom: 24px;
}

.section h3 {
  margin-bottom: 12px;
  color: #333;
  font-size: 18px;
}

.markdown-content {
  background-color: #f9f9f9;
  padding: 16px;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
}

.error-text {
  color: #f56c6c;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.spinning {
  animation: spin 1s linear infinite;
  display: inline-block;
}

/* 让表格列宽合理 */
.history-table th:nth-child(1), 
.history-table td:nth-child(1) {
  width: 60px;
}

.history-table th:nth-child(3), 
.history-table td:nth-child(3) {
  width: 100px;
}

.history-table th:nth-child(4), 
.history-table td:nth-child(4) {
  width: 180px;
}
</style> 