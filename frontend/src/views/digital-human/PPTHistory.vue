<template>
  <div class="ppt-history-container">
    <el-card class="history-card">
      <template #header>
        <div class="card-header">
          <h2><el-icon><List /></el-icon> PPT视频历史记录</h2>
          <el-button type="primary" @click="refreshTaskHistory" :loading="loading">
            <el-icon><Refresh /></el-icon> 刷新
          </el-button>
        </div>
      </template>

      <div class="history-content">
        <el-table 
          v-loading="loading" 
          :data="historyTasks" 
          style="width: 100%" 
          border 
          stripe
          :empty-text="emptyTableText"
        >
          <el-table-column label="标题" prop="title" min-width="120" show-overflow-tooltip />
          <el-table-column label="创建时间" prop="createdAt" width="180" />
          <el-table-column label="状态" width="120">
            <template #default="scope">
              <el-tag 
                :type="getStatusType(scope.row.status)"
                size="small"
                effect="dark"
              >
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="进度" width="150">
            <template #default="scope">
              <el-progress 
                :percentage="scope.row.progress || 0" 
                :status="getProgressStatus(scope.row.status)"
                :format="percentageFormat"
                :stroke-width="12"
                :show-text="true"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="280">
            <template #default="scope">
              <el-button-group class="action-buttons">
                <el-button 
                  v-if="scope.row.status === 'completed'" 
                  type="primary" 
                  size="small" 
                  @click="previewVideo(scope.row)"
                >
                  <el-icon><VideoPlay /></el-icon> 预览
                </el-button>
                <el-button 
                  v-if="scope.row.pptUrl" 
                  type="info" 
                  size="small" 
                  @click="viewPpt(scope.row.pptUrl)"
                >
                  <el-icon><Document /></el-icon> 查看PPT
                </el-button>
                <el-button 
                  type="success" 
                  size="small" 
                  @click="viewTaskDetails(scope.row)"
                >
                  <el-icon><InfoFilled /></el-icon> 详情
                </el-button>
                <el-button 
                  v-if="['inprogress', 'pending'].includes(scope.row.status)" 
                  type="warning" 
                  size="small" 
                  @click="refreshTaskStatus(scope.row.taskId)"
                  :loading="refreshingTaskIds.has(scope.row.taskId)"
                >
                  <el-icon><Refresh /></el-icon> 更新
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalTasks"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :disabled="loading"
          />
        </div>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailsDialogVisible"
      title="任务详情"
      width="700px"
      destroy-on-close
    >
      <div v-if="selectedTask" class="task-details">
        <div class="details-item">
          <div class="details-label">任务ID:</div>
          <div class="details-value">
            {{ selectedTask.taskId }}
            <el-button size="small" type="primary" link @click="copyToClipboard(selectedTask.taskId)">
              <el-icon><CopyDocument /></el-icon> 复制
            </el-button>
          </div>
        </div>

        <div class="details-item">
          <div class="details-label">标题:</div>
          <div class="details-value">{{ selectedTask.title }}</div>
        </div>

        <div class="details-item">
          <div class="details-label">状态:</div>
          <div class="details-value">
            <el-tag :type="getStatusType(selectedTask.status)">
              {{ getStatusText(selectedTask.status) }}
            </el-tag>
          </div>
        </div>

        <div class="details-item">
          <div class="details-label">创建时间:</div>
          <div class="details-value">{{ selectedTask.createdAt }}</div>
        </div>

        <div class="details-item">
          <div class="details-label">PPT文件:</div>
          <div class="details-value">
            <div v-if="selectedTask.pptUrl">
              <span>{{ getFileNameFromUrl(selectedTask.pptUrl) }}</span>
              <el-button type="primary" link @click="viewPpt(selectedTask.pptUrl)">
                <el-icon><Document /></el-icon> 查看
              </el-button>
              <el-button type="success" link @click="downloadFile(selectedTask.pptUrl)">
                <el-icon><Download /></el-icon> 下载
              </el-button>
            </div>
            <span v-else>-</span>
          </div>
        </div>

        <div class="details-item">
          <div class="details-label">讲解文本:</div>
          <div class="details-value text-content">
            <el-scrollbar height="100px">
              {{ selectedTask.textScript || '无讲解文本' }}
            </el-scrollbar>
          </div>
        </div>

        <div v-if="selectedTask.videoUrl" class="details-item">
          <div class="details-label">视频预览:</div>
          <div class="details-value">
            <el-button type="primary" @click="previewVideo(selectedTask)">
              <el-icon><VideoPlay /></el-icon> 打开视频
            </el-button>
          </div>
        </div>

        <div v-if="selectedTask.thumbnailUrl" class="details-item">
          <div class="details-label">视频缩略图:</div>
          <div class="details-value">
            <img 
              :src="selectedTask.thumbnailUrl" 
              alt="视频缩略图" 
              class="thumbnail-preview" 
              @click="previewVideo(selectedTask)"
            />
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { 
  List, 
  Refresh, 
  VideoPlay, 
  Document, 
  InfoFilled, 
  Download,
  CopyDocument
} from '@element-plus/icons-vue'

export default {
  name: 'PPTHistory',
  components: {
    List,
    Refresh,
    VideoPlay,
    Document,
    InfoFilled,
    Download,
    CopyDocument
  },
  setup() {
    // 分页数据
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalTasks = ref(0)
    
    // 任务列表
    const historyTasks = ref([])
    const loading = ref(false)
    const refreshingTaskIds = ref(new Set())
    const emptyTableText = ref('暂无历史任务记录')
    
    // 详情对话框
    const detailsDialogVisible = ref(false)
    const selectedTask = ref(null)
    
    // 自动刷新计时器
    let autoRefreshTimer = null
    
    // 加载历史任务
    const loadTaskHistory = async () => {
      loading.value = true
      emptyTableText.value = '正在加载...'
      
      try {
        const response = await axios.get('/api/v1/digital_human/ppt/history', {
          params: {
            page: currentPage.value,
            per_page: pageSize.value
          }
        })
        
        if (response.data.code === 0 && response.data.data) {
          // 转换API返回的历史记录为组件需要的格式
          historyTasks.value = response.data.data.items.map(task => ({
            taskId: task.task_id,
            title: task.title,
            status: task.status,
            createdAt: new Date(task.created_at).toLocaleString(),
            videoUrl: task.result_url,
            thumbnailUrl: task.thumbnail_url,
            pptUrl: task.ppt_url,
            textScript: task.text_script,
            progress: task.status === 'completed' ? 100 : (task.status === 'failed' ? 0 : (task.progress || 0))
          }))
          
          // 更新总数
          totalTasks.value = response.data.data.total || historyTasks.value.length
        } else {
          console.error('加载历史记录失败:', response.data.message)
          ElMessage.error(response.data.message || '加载历史记录失败')
          emptyTableText.value = '加载失败，请重试'
        }
      } catch (error) {
        console.error('加载历史记录失败:', error)
        ElMessage.error('加载历史记录失败: ' + (error.response?.data?.message || error.message || '未知错误'))
        emptyTableText.value = '加载失败，请重试'
      } finally {
        loading.value = false
      }
    }
    
    // 刷新任务状态
    const refreshTaskStatus = async (taskId) => {
      // 如果已经在刷新中，则不重复处理
      if (refreshingTaskIds.value.has(taskId)) {
        return
      }
      
      try {
        // 标记该任务正在刷新
        refreshingTaskIds.value.add(taskId)
        
        // 调用API查询任务状态
        const response = await axios.get(`/api/v1/digital_human/ppt/task/${taskId}`)
        
        if (response.data.code === 0 && response.data.data) {
          // 更新本地任务状态
          const updatedTask = response.data.data
          
          // 查找要更新的任务索引
          const taskIndex = historyTasks.value.findIndex(task => task.taskId === taskId)
          
          if (taskIndex !== -1) {
            // 更新任务状态
            historyTasks.value[taskIndex].status = updatedTask.status
            historyTasks.value[taskIndex].progress = updatedTask.status === 'completed' ? 100 : 
                                                 (updatedTask.status === 'failed' ? 0 : 
                                                 (updatedTask.progress || historyTasks.value[taskIndex].progress || 0))
            
            // 如果任务完成，更新视频URL和缩略图
            if (updatedTask.status === 'completed') {
              historyTasks.value[taskIndex].videoUrl = updatedTask.result_url
              historyTasks.value[taskIndex].thumbnailUrl = updatedTask.thumbnail_url
              ElMessage.success('任务已完成')
            } else if (updatedTask.status === 'failed') {
              ElMessage.error('任务失败: ' + (updatedTask.error?.message || '未知错误'))
            } else {
              ElMessage.info(`任务状态: ${getStatusText(updatedTask.status)}`)
            }
            
            // 如果当前显示的是该任务的详情，也更新详情信息
            if (selectedTask.value && selectedTask.value.taskId === taskId) {
              selectedTask.value = {...historyTasks.value[taskIndex]}
            }
          }
        } else {
          ElMessage.error(response.data.message || '任务状态更新失败')
        }
      } catch (error) {
        console.error('任务状态更新失败:', error)
        ElMessage.error('任务状态更新失败: ' + (error.response?.data?.message || error.message || '未知错误'))
      } finally {
        // 移除刷新标记
        refreshingTaskIds.value.delete(taskId)
      }
    }
    
    // 刷新所有任务
    const refreshTaskHistory = () => {
      loadTaskHistory()
    }
    
    // 预览视频
    const previewVideo = (task) => {
      if (!task.videoUrl) {
        ElMessage.warning('视频尚未生成或生成失败')
        return
      }
      
      window.open(task.videoUrl, '_blank')
    }
    
    // 查看PPT
    const viewPpt = (url) => {
      if (!url) return
      window.open(url, '_blank')
    }
    
    // 查看任务详情
    const viewTaskDetails = (task) => {
      selectedTask.value = {...task}
      detailsDialogVisible.value = true
    }
    
    // 下载文件
    const downloadFile = (url) => {
      if (!url) return
      
      const link = document.createElement('a')
      link.href = url
      link.target = '_blank'
      link.download = getFileNameFromUrl(url)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
    
    // 复制到剪贴板
    const copyToClipboard = (text) => {
      navigator.clipboard.writeText(text).then(() => {
        ElMessage.success('已复制到剪贴板')
      }).catch(() => {
        ElMessage.error('复制失败')
      })
    }
    
    // 分页处理
    const handleSizeChange = (val) => {
      pageSize.value = val
      loadTaskHistory()
    }
    
    const handleCurrentChange = (val) => {
      currentPage.value = val
      loadTaskHistory()
    }
    
    // 格式化百分比
    const percentageFormat = (percentage) => {
      return percentage === 100 ? '完成' : `${percentage}%`
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 'completed': return 'success'
        case 'failed': return 'danger'
        case 'inprogress': return 'warning'
        case 'pending': return 'info'
        default: return 'info'
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'completed': return '已完成'
        case 'failed': return '失败'
        case 'inprogress': return '处理中'
        case 'pending': return '等待中'
        default: return status
      }
    }
    
    // 获取进度状态
    const getProgressStatus = (status) => {
      switch (status) {
        case 'completed': return 'success'
        case 'failed': return 'exception'
        case 'inprogress': return ''
        default: return ''
      }
    }
    
    // 从URL中获取文件名
    const getFileNameFromUrl = (url) => {
      if (!url) return '未知文件'
      try {
        // 尝试解码URL
        const decodedUrl = decodeURIComponent(url)
        // 获取最后一个斜杠后面的内容作为文件名
        const fileName = decodedUrl.split('/').pop()
        // 如果文件名中包含下划线或特定标记，尝试提取原始文件名
        if (fileName.includes('_')) {
          // 提取最后一个下划线后的内容，这通常是原始文件名
          const parts = fileName.split('_')
          return parts[parts.length - 1]
        }
        return fileName
      } catch (e) {
        console.error('解析URL文件名失败:', e)
        return '未知文件'
      }
    }
    
    // 开始自动刷新
    const startAutoRefresh = () => {
      // 停止已有的定时器
      stopAutoRefresh()
      
      // 每30秒自动刷新一次
      autoRefreshTimer = setInterval(() => {
        // 只有在页面处于活动状态时才刷新
        if (document.visibilityState === 'visible') {
          // 自动刷新进行中的任务
          historyTasks.value.forEach(task => {
            if (['pending', 'inprogress'].includes(task.status)) {
              refreshTaskStatus(task.taskId)
            }
          })
        }
      }, 30000)
    }
    
    // 停止自动刷新
    const stopAutoRefresh = () => {
      if (autoRefreshTimer) {
        clearInterval(autoRefreshTimer)
        autoRefreshTimer = null
      }
    }
    
    // 生命周期钩子
    onMounted(() => {
      // 加载任务历史
      loadTaskHistory()
      
      // 开始自动刷新
      startAutoRefresh()
      
      // 监听页面可见性变化
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
          // 页面变为可见时刷新数据
          refreshTaskHistory()
        }
      })
    })
    
    onBeforeUnmount(() => {
      // 清除定时器
      stopAutoRefresh()
      
      // 移除事件监听
      document.removeEventListener('visibilitychange', () => {})
    })
    
    return {
      currentPage,
      pageSize,
      totalTasks,
      historyTasks,
      loading,
      refreshingTaskIds,
      emptyTableText,
      detailsDialogVisible,
      selectedTask,
      loadTaskHistory,
      refreshTaskStatus,
      refreshTaskHistory,
      previewVideo,
      viewPpt,
      viewTaskDetails,
      downloadFile,
      copyToClipboard,
      handleSizeChange,
      handleCurrentChange,
      percentageFormat,
      getStatusType,
      getStatusText,
      getProgressStatus,
      getFileNameFromUrl
    }
  }
}
</script>

<style scoped>
.ppt-history-container {
  padding: 20px;
  height: 100%;
}

.history-card {
  height: calc(100vh - 140px);
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  display: flex;
  align-items: center;
}

.card-header h2 .el-icon {
  margin-right: 8px;
}

.history-content {
  flex: 1;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 详情弹窗样式 */
.task-details {
  padding: 10px;
}

.details-item {
  margin-bottom: 15px;
  display: flex;
}

.details-label {
  width: 100px;
  font-weight: bold;
  color: #606266;
}

.details-value {
  flex: 1;
  word-break: break-word;
}

.text-content {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 10px;
}

.thumbnail-preview {
  max-width: 200px;
  max-height: 120px;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s;
}

.thumbnail-preview:hover {
  transform: scale(1.05);
}
</style> 