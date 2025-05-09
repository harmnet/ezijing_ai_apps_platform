<template>
  <div class="paper-outline-page">
    <h2 class="page-title">智能论文生成</h2>
    
    <div class="input-section">
      <!-- 主题输入区域 -->
      <div class="form-group">
        <label class="section-label">研究主题：</label>
        <el-input 
          v-model="topic" 
          placeholder="请输入研究主题..."
          clearable
          class="topic-input"
        ></el-input>
        <div class="outline-tips">
          <p class="tips-text">请输入您的研究主题，系统将自动为您生成论文大纲，然后根据大纲生成完整论文。</p>
          <p class="tips-text">例如：人工智能在医疗领域的应用、可持续发展与绿色能源、中国传统文化在现代教育中的应用等。</p>
        </div>
      </div>
      
      <!-- 操作按钮区域 -->
      <div class="action-buttons">
        <el-button 
          type="primary" 
          :loading="isGeneratingOutline"
          :disabled="!canGenerateOutline"
          @click="generateOutline"
        >
          <i class="ri-file-list-line"></i> 生成大纲
        </el-button>
        
        <el-button 
          type="default"
          @click="generateSampleTopic"
          :disabled="isGeneratingOutline || isGeneratingPaper"
        >
          <i class="ri-magic-line"></i> 生成示例主题
        </el-button>
        
        <el-button 
          type="default"
          @click="clearAll"
          :disabled="(isGeneratingOutline || isGeneratingPaper) || !topic.trim()"
        >
          <i class="ri-delete-bin-line"></i> 清空
        </el-button>
        
        <button 
          class="btn btn-history" 
          @click="openHistoryDialog" 
          title="查看历史记录"
        >
          <i class="ri-history-line"></i> 历史记录
        </button>
      </div>
      
      <!-- 生成状态显示区域 -->
      <div class="generation-status" v-if="isGeneratingOutline || isGeneratingPaper">
        <el-progress 
          :percentage="100" 
          :indeterminate="true" 
          :duration="3"
          status="active"
          style="margin-bottom: 10px;"
        ></el-progress>
        <div class="status-text">
          <i class="ri-loader-line rotating"></i> 
          <span v-if="isGeneratingOutline">
            正在生成论文大纲，已用时 {{ elapsedTime }} 秒，请耐心等待...
          </span>
          <span v-else-if="isGeneratingPaper">
            正在生成论文内容，已用时 {{ elapsedTime }} 秒，请耐心等待...
          </span>
        </div>
        <p class="status-tip">
          <i class="ri-information-line"></i>
          <span v-if="isGeneratingOutline">生成大纲通常需要30秒至1分钟，请耐心等待</span>
          <span v-else-if="isGeneratingPaper">生成完整论文通常需要1-5分钟，取决于大纲的复杂程度，请耐心等待</span>
        </p>
        <p class="status-tip" v-if="elapsedTime > 180 && isGeneratingPaper">
          <i class="ri-alert-line"></i>
          处理时间较长，如果超过5分钟将自动中断，您可以尝试使用更简单的研究主题
        </p>
      </div>
      
      <!-- 生成的大纲展示区域 -->
      <div class="outline-content" v-if="generatedOutline">
        <h3 class="section-title">生成的论文大纲</h3>
        <div class="generation-info" v-if="outlineGenerationTime > 0">
          <i class="ri-time-line"></i> 大纲生成耗时: {{ outlineGenerationTime }} 秒
        </div>
        
        <!-- 添加编辑/查看切换 -->
        <div class="edit-switch">
          <el-switch
            v-model="isEditingOutline"
            active-text="编辑模式"
            inactive-text="预览模式"
            @change="handleEditModeChange"
            :disabled="paperContent"
          ></el-switch>
          <span class="edit-tip" v-if="isEditingOutline && !paperContent">
            <i class="ri-information-line"></i> 您可以直接编辑大纲内容，完成后点击"根据大纲生成论文"
          </span>
          <span class="edit-tip" v-if="paperContent">
            <i class="ri-information-line"></i> 论文已生成，无法修改大纲
          </span>
        </div>
        
        <!-- 编辑模式：文本框 -->
        <div v-if="isEditingOutline && !paperContent" class="outline-editor">
          <el-input
            v-model="generatedOutline"
            type="textarea"
            :rows="20"
            resize="vertical"
            placeholder="编辑大纲内容..."
          ></el-input>
        </div>
        
        <!-- 预览模式：渲染的Markdown -->
        <div v-else class="content-wrapper markdown-body" v-html="renderedOutline"></div>
        
        <div class="action-buttons" v-if="!paperContent">
          <el-button 
            type="primary" 
            :loading="isGeneratingPaper"
            @click="generatePaperFromOutline"
          >
            <i class="ri-file-text-line"></i> 根据大纲生成论文
          </el-button>
          
          <el-button 
            type="default"
            @click="regenerateOutline"
            :disabled="isGeneratingPaper"
          >
            <i class="ri-refresh-line"></i> 重新生成大纲
          </el-button>
        </div>
      </div>
      
      <!-- 生成的论文内容展示区域 -->
      <div class="paper-content" v-if="paperContent">
        <h3 class="section-title">生成的论文内容</h3>
        <div class="generation-info" v-if="totalGenerationTime > 0">
          <i class="ri-time-line"></i> 论文生成耗时: {{ totalGenerationTime }} 秒
        </div>
        <div class="content-wrapper markdown-body" v-html="renderedContent"></div>
        <div class="export-buttons">
          <el-tooltip
            v-if="documentStatus === 'generating'"
            content="文档正在生成中，请等待完成后再下载"
            placement="top"
          >
            <div class="button-wrapper">
              <el-button type="primary" disabled>
                <i class="ri-loader-line rotating"></i> 文档生成中...
              </el-button>
            </div>
          </el-tooltip>
          
          <el-button 
            v-else 
            type="primary" 
            @click="downloadPaperFile"
            :disabled="documentStatus !== 'completed'"
          >
            <i class="ri-download-line"></i> 下载论文文件
          </el-button>
          
          <div v-if="statusMessage" class="status-message">
            {{ statusMessage }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加历史记录弹窗 -->
    <el-dialog
      title=""
      v-model="historyDialogVisible"
      width="70%"
      :close-on-click-modal="false"
    >
      <div class="history-container">
        <el-table
          v-loading="historyLoading"
          :data="historyPapers"
          style="width: 100%"
          border
        >
          <el-table-column prop="query" label="论文主题" min-width="180">
          </el-table-column>
          <el-table-column label="创建时间" min-width="150">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="生成状态" min-width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.document_status)">
                {{ getStatusText(scope.row.document_status) }}
              </el-tag>
              <!-- 添加失败状态的提示图标 -->
              <el-tooltip
                v-if="scope.row.document_status === 'failed'"
                :content="scope.row.status_message || '未知错误'"
                placement="top"
              >
                <i class="ri-information-line" style="margin-left: 5px; color: #F56C6C; cursor: pointer;"></i>
              </el-tooltip>
              <!-- 添加生成中状态的提示图标 -->
              <el-tooltip
                v-if="scope.row.document_status === 'generating'"
                :content="scope.row.doc_id ? `文档ID: ${scope.row.doc_id}` : '无文档ID'"
                placement="top"
              >
                <i class="ri-information-line" style="margin-left: 5px; color: #E6A23C; cursor: pointer;"></i>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="220">
            <template #default="scope">
              <el-button 
                size="small" 
                type="primary" 
                plain
                @click="loadHistoryOutline(scope.row)"
              >
                查看大纲
              </el-button>
              <el-button 
                v-if="scope.row.download_url" 
                size="small" 
                type="primary" 
                plain
                @click="downloadPaper(scope.row)"
              >
                下载论文
              </el-button>
              <el-button 
                v-if="scope.row.document_status !== 'completed' && scope.row.doc_id" 
                size="small" 
                type="primary" 
                plain
                :loading="scope.row.refreshing"
                @click="refreshPaperStatus(scope.row)"
              >
                刷新
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                plain
                @click="confirmDeletePaper(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-container" v-if="historyTotal > 0">
          <el-pagination
            @current-change="handleCurrentChange"
            :current-page="historyCurrentPage"
            :page-size="historyPageSize"
            layout="total, prev, pager, next"
            :total="historyTotal"
          >
          </el-pagination>
        </div>
        
        <div class="empty-text" v-if="historyPapers.length === 0 && !historyLoading">
          暂无历史记录
        </div>
      </div>
    </el-dialog>
    
    <!-- 论文详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="论文详情"
      width="80%"
      :before-close="closeDetailDialog"
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
            <button class="btn btn-outline" @click="refreshPaperStatus(selectedPaper)">
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
          <button class="btn btn-outline" @click="closeDetailDialog">关闭</button>
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
    
    <!-- 历史大纲预览弹窗 -->
    <el-dialog
      title="历史大纲预览"
      v-model="outlinePreviewVisible"
      width="60%"
      :close-on-click-modal="false"
    >
      <div v-html="outlinePreviewHtml" class="outline-preview"></div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElLoading, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { saveAs } from 'file-saver'
import { Document, Packer, Paragraph, TextRun } from 'docx'
import * as marked from 'marked'
import DOMPurify from 'dompurify'
import { useRouter } from 'vue-router'

export default {
  name: 'PaperOutline',
  setup() {
    const topic = ref('') // 用户输入的研究主题
    const generatedOutline = ref('') // AI生成的大纲
    const paperContent = ref('') // 最终生成的论文内容
    const isGeneratingOutline = ref(false) // 是否正在生成大纲
    const isGeneratingPaper = ref(false) // 是否正在生成论文
    const docId = ref('') // 存储生成的文档ID，用于后续获取
    const startTime = ref(Date.now()) // 开始时间戳
    const elapsedTime = ref(0) // 记录经过的时间
    const outlineGenerationTime = ref(0) // 大纲生成耗时
    const totalGenerationTime = ref(0) // 总生成耗时
    const isEditingOutline = ref(false) // 是否处于大纲编辑模式
    const documentStatus = ref('none') // 文档状态：none-未生成, generating-生成中, completed-已完成, failed-失败
    const statusMessage = ref('') // 状态消息
    const router = useRouter()
    
    // 修改goToHistory方法，改为打开弹窗而非跳转
    const historyDialogVisible = ref(false)
    const historyLoading = ref(false)
    const historyError = ref(null)
    const historyPapers = ref([])
    const historyCurrentPage = ref(1)
    const historyPerPage = ref(10)
    const historyTotal = ref(0)
    const historyTotalPages = ref(1)
    const detailDialogVisible = ref(false)
    const selectedPaper = ref(null)
    const outlinePreviewVisible = ref(false)
    const outlinePreviewHtml = ref('')
    
    // 检查是否可以生成大纲
    const canGenerateOutline = computed(() => {
      return topic.value.trim().length > 0
    })

    // 将Markdown转换为HTML并清理
    const renderedOutline = computed(() => {
      if (!generatedOutline.value) return ''
      try {
        const rawHtml = marked.parse(generatedOutline.value)
        return DOMPurify.sanitize(rawHtml)
      } catch (error) {
        console.error('渲染大纲出错:', error)
        return `<div class="error">渲染错误: ${error.message}</div>`
      }
    })

    const renderedContent = computed(() => {
      if (!paperContent.value) return ''
      try {
        // 确保paperContent.value是字符串
        const contentToRender = typeof paperContent.value === 'string' 
          ? paperContent.value 
          : JSON.stringify(paperContent.value, null, 2)
          
        const rawHtml = marked.parse(contentToRender)
        return DOMPurify.sanitize(rawHtml)
      } catch (error) {
        console.error('渲染论文内容出错:', error)
        return `<div class="error">渲染错误: ${error.message}</div>`
      }
    })

    // 开始整个生成流程 - 一键生成论文
    const startGeneration = async () => {
      if (!canGenerateOutline.value) {
        ElMessage.warning('请输入研究主题')
        return
      }

      // 清空之前的内容
      generatedOutline.value = ''
      paperContent.value = ''
      docId.value = ''
      
      // 只生成大纲
      const outlineSuccess = await generateOutline()
      
      if (!outlineSuccess) {
        ElMessage.warning('大纲生成失败，请重试')
      }
    }

    // 生成大纲
    const generateOutline = async () => {
      isGeneratingOutline.value = true
      startTime.value = Date.now() // 重置开始时间
      elapsedTime.value = 0 // 重置已用时间
      let timer = null
      let success = false
      
      // 启动计时器
      timer = setInterval(() => {
        elapsedTime.value = Math.floor((Date.now() - startTime.value) / 1000)
      }, 1000)
      
      try {
        ElMessage.info('正在根据主题生成论文大纲，请稍候...')
        
        const loading = ElLoading.service({
          lock: true,
          text: '正在生成大纲，请耐心等待...',
          background: 'rgba(0, 0, 0, 0.7)'
        })
        
        // 先验证API服务是否正常
        await checkApiHealth()
        
        // 调用生成大纲的API - 修正为正确的API路径
        const response = await axios.post('/api/v1/academic/paper_outline', {
          query: topic.value.trim()
        }, {
          timeout: 120000 // 延长超时时间到2分钟
        })
        
        // 关闭加载提示
        loading.close()
        
        console.log('API响应:', response.data)
        
        if (response.data.status === 'success') {
          // 停止计时器
          clearInterval(timer)
          // 计算耗时
          outlineGenerationTime.value = Math.floor((Date.now() - startTime.value) / 1000)
          
          // 设置生成的大纲
          generatedOutline.value = response.data.data
          
          ElMessage.success(`大纲生成成功！耗时：${outlineGenerationTime.value}秒`)
          ElMessage.info('请检查大纲内容，如有需要可编辑修改后，点击"根据大纲生成论文"按钮继续')
          success = true
        } else {
          clearInterval(timer)
          // 显示具体错误信息
          const errorMsg = response.data.message || '大纲生成失败，请稍后重试'
          ElMessage.error(errorMsg)
          
          // 即使出错，也可能返回一些内容，如错误提示大纲
          if (response.data.data) {
            generatedOutline.value = response.data.data
            success = true // 允许用户查看错误信息大纲
          }
        }
      } catch (error) {
        clearInterval(timer)
        console.error('生成大纲出错:', error)
        
        // 获取更详细的错误信息
        let errorMessage = '大纲生成失败'
        
        if (error.response) {
          // 服务器响应了错误状态码
          console.error('错误响应状态:', error.response.status)
          console.error('错误响应数据:', error.response.data)
          
          if (error.response.data && error.response.data.message) {
            errorMessage = `${errorMessage}: ${error.response.data.message}`
          } else {
            errorMessage = `${errorMessage}: 服务器错误 (${error.response.status})`
          }
          
          // 如果是500错误，尝试测试API健康状态
          if (error.response.status === 500) {
            tryDiagnoseApiIssue()
          }
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到响应:', error.request)
          errorMessage = `${errorMessage}: 服务器未响应，请检查网络连接`
          
          // 尝试测试API连接
          tryDiagnoseApiIssue()
        } else {
          // 请求设置时出错
          console.error('请求错误:', error.message)
          errorMessage = `${errorMessage}: ${error.message}`
        }
        
        if (error.code === 'ECONNABORTED') {
          errorMessage = '请求超时，请尝试使用更简单的研究主题'
        }
        
        ElMessage.error(errorMessage)
        
        // 添加重试按钮
        ElMessageBox.confirm(
          '生成大纲失败，是否重试？',
          '操作失败',
          {
            confirmButtonText: '重试',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(() => {
          // 用户点击重试
          setTimeout(() => {
            generateOutline()
          }, 1000)
        }).catch(() => {
          // 用户取消重试
          ElMessage.info('您可以稍后再试或更换研究主题')
        })
      } finally {
        clearInterval(timer)
        isGeneratingOutline.value = false
      }
      
      return success // 返回是否成功
    }
    
    // 添加API健康检查功能
    const checkApiHealth = async () => {
      try {
        // 发送一个简单的OPTIONS请求检查API是否在线
        await axios.options('/api/v1/academic/paper_outline')
        return true
      } catch (error) {
        console.error('API健康检查失败:', error)
        ElMessage.error('无法连接到AI服务，请检查服务是否正常运行')
        throw new Error('API服务不可用')
      }
    }
    
    // 尝试诊断API问题
    const tryDiagnoseApiIssue = async () => {
      try {
        console.log('正在诊断API问题...')
        
        // 测试基本连接
        try {
          await axios.get('/api/v1/ping', { timeout: 5000 })
          console.log('基本API连接正常')
        } catch (error) {
          console.error('基本API连接异常:', error)
          ElMessage.error('后端服务连接异常，请联系管理员检查服务状态')
          return
        }
        
        // 尝试获取API版本信息
        try {
          await axios.get('/api/v1/version', { timeout: 5000 })
          console.log('API版本信息请求正常')
        } catch (error) {
          console.error('无法获取API版本信息:', error)
        }
        
        // 提示用户
        ElMessage.warning('API服务连接正常，但处理请求时出错，请稍后再试')
      } catch (error) {
        console.error('诊断过程中出错:', error)
      }
    }
    
    // 重新生成大纲
    const regenerateOutline = async () => {
      if (isGeneratingPaper.value) return
      
      // 清空论文内容
      paperContent.value = ''
      
      // 重新生成大纲
      await generateOutline()
    }

    // 根据大纲生成论文
    const generatePaperFromOutline = async () => {
      if (!generatedOutline.value) {
        ElMessage.warning('请先生成论文大纲')
        return
      }

      isGeneratingPaper.value = true
      startTime.value = Date.now() // 重置开始时间
      elapsedTime.value = 0 // 重置已用时间
      let timer = null
      
      // 重置文档状态
      documentStatus.value = 'none'
      statusMessage.value = ''
      
      // 启动计时器
      timer = setInterval(() => {
        elapsedTime.value = Math.floor((Date.now() - startTime.value) / 1000)
      }, 1000)
      
      try {
        ElMessage.info('正在根据大纲生成完整论文，请耐心等待...')
        
        // 调用根据大纲生成论文的API
        const response = await axios.post('/api/v1/academic/paper_from_outline', {
          user_query: topic.value.trim(),
          outline: generatedOutline.value
        }, {
          timeout: 300000 // 5分钟超时
        })
        
        if (response.data.status === 'success') {
          // 停止计时器
          clearInterval(timer)
          // 计算总耗时
          totalGenerationTime.value = Math.floor((Date.now() - startTime.value) / 1000)
          
          // 设置生成的论文内容
          if (typeof response.data.data === 'string') {
            // 直接内容模式
            paperContent.value = response.data.data
            
            // 更新文档状态为已完成
            documentStatus.value = 'completed'
            statusMessage.value = '文档已生成完成，可以下载'
            
            ElMessage.success(`论文生成成功！耗时：${totalGenerationTime.value}秒`)
          } else if (typeof response.data.data === 'object' && response.data.data.doc_id) {
            // 文档ID模式
            const docIdValue = response.data.data.doc_id
            docId.value = docIdValue
            
            // 将对象转换为字符串，以便显示
            paperContent.value = `文档正在生成中，请稍后查看。\n\n文档ID: ${docIdValue}`
            
            // 更新文档状态为正在生成
            documentStatus.value = 'generating'
            statusMessage.value = '文档正在生成中，请稍后再试'
            
            ElMessage.success(`论文生成任务已提交！文档ID: ${docId.value}`)
            ElMessage.info('完整论文正在后台生成中，这可能需要3-5分钟...')
          } else {
            // 未知格式，尝试转换为字符串
            try {
              paperContent.value = JSON.stringify(response.data.data) || '获取论文内容失败'
              console.warn('API返回了未知格式的数据:', response.data.data)
              
              // 更新文档状态为已完成（非理想情况）
              documentStatus.value = 'completed'
              statusMessage.value = '文档格式异常，但可以查看'
              
              ElMessage.warning('论文生成格式异常，但内容已展示')
            } catch (e) {
              console.error('无法处理API返回的数据格式:', e)
              paperContent.value = '无法解析论文内容，请联系管理员'
              
              // 更新文档状态为失败
              documentStatus.value = 'failed'
              statusMessage.value = '无法解析论文内容'
              
              ElMessage.error('无法解析论文内容，请联系管理员')
            }
          }
        } else {
          clearInterval(timer)
          
          // 更新文档状态为失败
          documentStatus.value = 'failed'
          statusMessage.value = response.data.message || '论文生成失败'
          
          ElMessage.error(response.data.message || '论文生成失败')
        }
      } catch (error) {
        clearInterval(timer)
        console.error('生成论文出错:', error)
        
        // 更新文档状态为失败
        documentStatus.value = 'failed'
        statusMessage.value = error.message
        
        if (error.code === 'ECONNABORTED') {
          ElMessage.error('请求超时(5分钟)，请尝试使用更简单的研究主题')
        } else {
          ElMessage.error(`论文生成失败: ${error.response?.data?.message || error.message}`)
        }
      } finally {
        clearInterval(timer)
        isGeneratingPaper.value = false
      }
    }

    // 导出为Word文档
    const exportToWord = async () => {
      try {
        const title = topic.value.trim() || '学术论文'
        
        const doc = new Document({
          sections: [{
            properties: {},
            children: paperContent.value.split('\n').map(line => 
              new Paragraph({
                children: [new TextRun(line)]
              })
            )
          }]
        })

        const blob = await Packer.toBlob(doc)
        saveAs(blob, `${title}.docx`)
        ElMessage.success('导出成功')
      } catch (error) {
        console.error('导出文档失败:', error)
        ElMessage.error('导出失败，请重试')
      }
    }

    // 复制内容到剪贴板
    const copyContent = async () => {
      try {
        await navigator.clipboard.writeText(paperContent.value)
        ElMessage.success('内容已复制到剪贴板（Markdown格式）')
      } catch (error) {
        console.error('复制失败:', error)
        ElMessage.error('复制失败，请手动复制')
      }
    }

    // 生成示例主题
    const generateSampleTopic = () => {
      const sampleTopics = [
        '人工智能在医疗领域的应用及挑战',
        '可持续发展与绿色能源技术的未来趋势',
        '中国传统文化在现代教育中的应用',
        '区块链技术对金融行业的影响',
        '全球气候变化的应对策略研究',
        '数字化转型对企业管理的影响',
        '大数据分析在城市规划中的应用',
        '远程工作对职场文化的影响'
      ]
      
      // 随机选择一个示例
      const randomSample = sampleTopics[Math.floor(Math.random() * sampleTopics.length)]
      topic.value = randomSample
      
      ElMessage.success(`已生成示例主题: ${randomSample}`)
    }
    
    // 清空所有内容
    const clearAll = () => {
      topic.value = ''
      generatedOutline.value = ''
      paperContent.value = ''
      docId.value = ''
      elapsedTime.value = 0
      outlineGenerationTime.value = 0
      totalGenerationTime.value = 0
    }

    // 调用接口检查当前论文状态
    const checkPaperStatus = async (paper) => {
      try {
        if (!paper || !paper.doc_id) {
          console.error('检查状态错误: 缺少必要参数')
          ElMessage.error('无法检查状态: 缺少必要参数')
          throw new Error('缺少必要参数')
        }
        
        console.log(`调用检查状态接口，paper_id=${paper.id}, doc_id=${paper.doc_id}`)
        
        const response = await axios.post('/api/v1/academic/check_paper_status', {
          doc_id: paper.doc_id,
          paper_id: paper.id // 确保传递paper_id参数
        })
        
        console.log('状态检查响应:', response.data)
        
        if (response.data.status === 'success') {
          const statusData = response.data.data
          
          // 检查数据库是否成功更新
          const dbUpdated = statusData.db_updated === true
          console.log(`数据库更新状态: ${dbUpdated ? '成功' : '失败'}`)
          
          // 更新前端显示的状态
          paper.document_status = statusData.document_status
          paper.status_message = statusData.message
          
          if (statusData.document_status === 'generating') {
            ElMessage.info('论文仍在生成中，请稍后再试')
          } else if (statusData.document_status === 'completed') {
            ElMessage.success('论文生成完成，可以下载')
          } else if (statusData.document_status === 'failed') {
            ElMessage.error(`论文生成失败: ${statusData.message}`)
          }
        }
        
        return response.data
      } catch (error) {
        console.error('检查状态出错:', error)
        ElMessage.error(`检查状态失败: ${error.message || '未知错误'}`)
        throw error
      }
    }

    // 修改下载论文文件函数，添加轮询机制
    const downloadPaperFile = async () => {
      if (!docId.value) {
        ElMessage.warning('没有可下载的论文文件，请先生成论文')
        return
      }
      
      try {
        console.log('开始下载论文，文档ID:', docId.value)
        
        // 如果已知文档已完成，直接获取下载链接
        if (documentStatus.value === 'completed') {
          getAndOpenDownloadLink()
          return
        }
        
        ElMessage.info('正在检查文档状态，请稍候...')
        
        // 检查文档状态
        const statusResult = await checkPaperStatus({ doc_id: docId.value })
        
        // 如果文档已生成完成，直接获取下载链接
        if (statusResult.document_status === 'completed') {
          // 更新状态
          documentStatus.value = 'completed'
          statusMessage.value = '文档已生成完成，可以下载'
          
          getAndOpenDownloadLink()
        } 
        // 如果文档仍在生成中，开始轮询
        else if (statusResult.document_status === 'generating') {
          // 更新状态
          documentStatus.value = 'generating'
          statusMessage.value = '文档正在生成中，请稍后再试'
          
          ElMessage.info('文档正在生成中，将自动等待并下载...')
          startStatusPolling()
        } 
        // 如果文档生成失败，显示错误信息
        else {
          // 更新状态
          documentStatus.value = 'failed'
          statusMessage.value = statusResult.message
          
          ElMessage.error(`无法下载文档: ${statusResult.message}`)
        }
      } catch (error) {
        console.error('下载论文文件出错:', error)
        ElMessage.error(`下载论文失败: ${error.message}`)
      }
    }

    // 添加获取并打开下载链接的函数
    const getAndOpenDownloadLink = async () => {
      try {
        ElMessage.info('正在获取论文下载链接，请稍候...')
        
        // 调用后端API获取下载链接
        const response = await axios.post('/api/v1/academic/download_paper', {
          doc_id: docId.value
        })
        
        console.log('下载API响应:', response)
        
        if (response.data.status === 'success') {
          const downloadLink = response.data.data
          console.log('获取到下载链接:', downloadLink)
          
          // 检查是否是有效的下载链接
          if (downloadLink.startsWith('http')) {
            // 更新状态
            documentStatus.value = 'completed'
            statusMessage.value = '文档已生成完成，可以下载'
            
            // 使用window.open在新标签页打开下载链接
            window.open(downloadLink, '_blank')
            ElMessage.success('下载链接已打开，请在新标签页中完成下载')
          } else {
            // 如果返回的不是链接，可能文档还在生成中
            if (downloadLink.includes('错误码 200009') || downloadLink.includes('File is generating')) {
              // 更新状态
              documentStatus.value = 'generating'
              statusMessage.value = '文档正在生成中，请稍后再试'
              
              ElMessage.info('文档仍在生成中，请稍后再试')
            } else {
              // 其他错误
              console.error('非有效下载链接:', downloadLink)
              
              // 更新状态
              documentStatus.value = 'failed'
              statusMessage.value = downloadLink
              
              ElMessage.error(`获取下载链接失败: ${downloadLink}`)
            }
          }
        } else {
          console.error('下载API返回错误:', response.data)
          
          // 更新状态
          documentStatus.value = 'failed'
          statusMessage.value = response.data.message || '获取下载链接失败'
          
          ElMessage.error(response.data.message || '获取下载链接失败')
        }
      } catch (error) {
        console.error('获取下载链接失败:', error)
        
        // 更新状态
        documentStatus.value = 'failed'
        statusMessage.value = error.message
        
        ElMessage.error(`获取下载链接失败: ${error.message}`)
      }
    }

    // 添加轮询文档状态的函数
    const startStatusPolling = () => {
      let pollCount = 0
      const maxPolls = 10 // 最多轮询10次，总时长10分钟
      const pollInterval = 60000 // 60秒轮询一次
      let isPolling = true
      let pollTimer = null
      
      // 更新文档状态
      documentStatus.value = 'generating'
      statusMessage.value = '文档正在生成中，请耐心等待...'
      
      // 创建加载指示器
      const loadingInstance = ElLoading.service({
        lock: true,
        text: '等待文档生成完成(0%)...',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      
      // 定义轮询函数
      const pollStatus = async () => {
        try {
          pollCount++
          
          // 更新加载提示
          const progress = Math.min(Math.floor((pollCount / maxPolls) * 100), 99)
          loadingInstance.setText(`等待文档生成完成(${progress}%)...`)
          
          console.log(`轮询文档状态 [${pollCount}/${maxPolls}]，间隔：${pollInterval/1000}秒`)
          
          // 检查文档状态
          const statusResult = await checkPaperStatus({ doc_id: docId.value })
          
          // 如果文档已生成完成
          if (statusResult.document_status === 'completed') {
            console.log('文档已生成完成，停止轮询')
            clearInterval(pollTimer)
            isPolling = false
            loadingInstance.close()
            
            // 更新状态
            documentStatus.value = 'completed'
            statusMessage.value = '文档已生成完成，可以下载'
            
            ElMessage.success('文档已生成完成，可以下载')
            return
          }
          
          // 如果文档生成失败
          if (statusResult.document_status === 'failed') {
            console.error('文档生成失败，停止轮询:', statusResult.message)
            clearInterval(pollTimer)
            isPolling = false
            loadingInstance.close()
            
            // 更新状态
            documentStatus.value = 'failed'
            statusMessage.value = statusResult.message
            
            ElMessage.error(`文档生成失败: ${statusResult.message}`)
            return
          }
          
          // 如果达到最大轮询次数
          if (pollCount >= maxPolls) {
            console.warn('达到最大轮询次数，停止轮询')
            clearInterval(pollTimer)
            isPolling = false
            loadingInstance.close()
            
            // 更新状态
            documentStatus.value = 'generating'
            statusMessage.value = '等待超时，请稍后手动检查状态'
            
            ElMessage.warning('等待文档生成超时，请稍后再试')
          }
        } catch (error) {
          console.error('轮询过程中出错:', error)
          // 错误时不停止轮询，继续等待下一次
        }
      }
      
      // 开始轮询
      pollTimer = setInterval(pollStatus, pollInterval)
      
      // 立即执行一次
      pollStatus()
    }

    // 处理编辑模式切换
    const handleEditModeChange = (val) => {
      isEditingOutline.value = val
      if (val) {
        ElMessage.info('已切换到编辑模式，您可以直接修改大纲内容')
      } else {
        ElMessage.info('已切换到预览模式，可查看大纲渲染效果')
      }
    }

    // 修改打开历史记录的方法
    const showHistory = async () => {
      // 设置loading状态
      historyLoading.value = true
      ElMessage.info('正在获取最新历史记录...')
      
      // 重置历史记录数据
      historyPapers.value = []
      historyCurrentPage.value = 1
      
      // 不再在这里设置对话框为可见，因为此函数可能由watch触发
      // historyDialogVisible.value = true
      
      try {
        // 使用force=true参数强制从数据库获取最新数据
        const response = await axios.get('/api/v1/academic/history', {
          params: {
            page: 1,
            per_page: historyPerPage.value,
            force: true,
            _t: new Date().getTime() // 添加时间戳防止缓存
          }
        })
        
        if (response.data.status === 'success') {
          historyPapers.value = response.data.data.items
          historyTotal.value = response.data.data.total
          historyTotalPages.value = response.data.data.pages
          
          console.log('历史记录获取成功，记录数:', historyPapers.value.length)
        } else {
          throw new Error(response.data.message || '获取历史记录失败')
        }
      } catch (err) {
        console.error('获取历史记录失败:', err)
        historyError.value = err.message || '获取历史记录失败，请稍后重试'
        ElMessage.error(`获取历史记录失败: ${historyError.value}`)
      } finally {
        historyLoading.value = false
      }
    }
    
    // 关闭历史记录弹窗
    const closeHistoryDialog = () => {
      historyDialogVisible.value = false
      
      // 清空状态，确保下次打开时重新获取数据
      historyPapers.value = []
      historyError.value = null
    }
    
    // 关闭详情弹窗
    const closeDetailDialog = () => {
      detailDialogVisible.value = false
      selectedPaper.value = null
    }
    
    // 获取历史记录
    const fetchHistory = async (page = 1) => {
      historyLoading.value = true
      try {
        const response = await axios.get('/api/v1/academic/history', {
          params: {
            page: page,
            per_page: historyPerPage.value
          }
        })
        if (response.data.status === 'success') {
          historyPapers.value = response.data.data.items
          historyTotal.value = response.data.data.total
          historyTotalPages.value = response.data.data.pages
          historyCurrentPage.value = page
          
          // 不再自动检查生成中的记录状态
          // await checkGeneratingPapers()
        } else {
          throw new Error(response.data.message || '获取历史记录失败')
        }
      } catch (err) {
        console.error('获取历史记录失败:', err)
        historyError.value = err.message || '获取历史记录失败，请稍后重试'
        ElMessage.error(`获取历史记录失败: ${historyError.value}`)
      } finally {
        historyLoading.value = false
      }
    }
    
    // 刷新单个论文的状态
    const refreshPaperStatus = async (paper) => {
      if (!paper || !paper.id || !paper.doc_id) {
        ElMessage.error('缺少必要参数，无法刷新状态')
        return
      }
      
      // 设置刷新状态
      paper.refreshing = true
      
      // 同时更新历史记录和选中的论文
      if (selectedPaper.value && selectedPaper.value.id === paper.id) {
        selectedPaper.value.refreshing = true
      }
      
      try {
        console.log(`刷新论文状态: paper_id=${paper.id}, doc_id=${paper.doc_id}`)
        
        // 先尝试下载论文，如果可以下载则状态已完成
        const downloadResponse = await axios.post('/api/v1/academic/download_paper', {
          doc_id: paper.doc_id,
          paper_id: paper.id
        })
        
        console.log('下载API响应:', downloadResponse)
        
        if (downloadResponse.data.status === 'success' && downloadResponse.data.data) {
          const downloadUrl = downloadResponse.data.data
          
          if (typeof downloadUrl === 'string' && downloadUrl.startsWith('http')) {
            // 下载链接有效，更新状态
            paper.document_status = 'completed'
            paper.status_message = '论文生成完成，可以下载'
            paper.download_url = downloadUrl
            
            // 同步更新选中的论文
            if (selectedPaper.value && selectedPaper.value.id === paper.id) {
              selectedPaper.value.document_status = 'completed'
              selectedPaper.value.status_message = '论文生成完成，可以下载'
              selectedPaper.value.download_url = downloadUrl
            }
            
            ElMessage.success('论文状态已更新：已完成')
          } else {
            // 下载链接无效，检查状态
            console.log('下载链接无效，检查状态')
            await checkPaperStatus(paper)
          }
        } else {
          // 下载失败，检查状态
          console.log('下载API调用失败，检查状态')
          await checkPaperStatus(paper)
        }
      } catch (error) {
        console.error('刷新论文状态出错:', error)
        // 出错时检查状态
        try {
          await checkPaperStatus(paper)
        } catch (e) {
          console.error('检查状态也失败:', e)
          ElMessage.error(`刷新状态失败: ${error.message || '未知错误'}`)
        }
      } finally {
        // 清除刷新状态
        paper.refreshing = false
        
        // 同步更新选中的论文
        if (selectedPaper.value && selectedPaper.value.id === paper.id) {
          selectedPaper.value.refreshing = false
        }
        
        // 刷新完成后，从数据库获取最新数据
        try {
          console.log(`从数据库获取最新数据: paper_id=${paper.id}`)
          const latestDataResponse = await axios.get(`/api/v1/academic/history/${paper.id}?force=true`)
          
          if (latestDataResponse.data.status === 'success' && latestDataResponse.data.data) {
            const latestPaper = latestDataResponse.data.data
            
            console.log('数据库最新数据:', latestPaper)
            console.log('当前前端数据:', paper)
            
            // 用后端数据更新前端显示
            Object.assign(paper, {
              document_status: latestPaper.document_status,
              status_message: latestPaper.status_message,
              download_url: latestPaper.download_url,
              updated_at: latestPaper.updated_at
            })
            
            // 同步更新选中的论文
            if (selectedPaper.value && selectedPaper.value.id === paper.id) {
              Object.assign(selectedPaper.value, {
                document_status: latestPaper.document_status,
                status_message: latestPaper.status_message,
                download_url: latestPaper.download_url,
                updated_at: latestPaper.updated_at
              })
            }
            
            console.log('更新后的记录:', paper)
            
            if (latestPaper.document_status === 'completed' && latestPaper.download_url) {
              ElMessage.success(`论文已完成，可以下载 (${latestPaper.updated_at || '最新'})`)
            } else if (latestPaper.document_status === 'generating') {
              ElMessage.info(`论文仍在生成中，请稍后再试 (${latestPaper.updated_at || '最新'})`)
            } else if (latestPaper.document_status === 'failed') {
              ElMessage.error(`论文生成失败: ${latestPaper.status_message || '未知错误'}`)
            }
          }
        } catch (e) {
          console.error('获取最新数据失败:', e)
        }
      }
    }
    
    // 监视历史记录对话框的显示状态
    watch(historyDialogVisible, (newVal) => {
      if (newVal) {
        // 当对话框变为可见状态时，重新获取历史记录
        console.log('历史记录对话框打开，重新获取数据')
        showHistory()
      }
    })
    
    // 打开历史记录对话框的函数
    const openHistoryDialog = () => {
      // 只负责打开对话框，showHistory会通过watch自动调用
      historyDialogVisible.value = true
    }
    
    // 切换页码
    const handleCurrentChange = (page) => {
      if (page < 1 || page > historyTotalPages.value) return
      fetchHistory(page)
    }
    
    // 查看详情
    const viewDetails = async (paper) => {
      if (!paper) return
      
      try {
        // 获取最新的论文详情
        const response = await axios.get(`/api/v1/academic/history/${paper.id}`)
        
        if (response.data.status === 'success') {
          selectedPaper.value = response.data.data
          detailDialogVisible.value = true
        } else {
          throw new Error(response.data.message || '获取论文详情失败')
        }
      } catch (err) {
        console.error('获取论文详情失败:', err)
        ElMessage.error(`获取论文详情失败: ${err.message}`)
      }
    }
    
    // 下载论文
    const downloadPaper = (paper) => {
      // 判断参数是对象还是字符串URL
      let downloadUrl
      
      if (typeof paper === 'string') {
        // 直接传入URL
        downloadUrl = paper
      } else if (paper && paper.download_url) {
        // 传入paper对象
        downloadUrl = paper.download_url
      } else {
        ElMessage.warning('没有可用的下载链接')
        return
      }
      
      // 在新标签页打开下载链接
      window.open(downloadUrl, '_blank')
      ElMessage.success('已打开下载链接，请在新标签页完成下载')
    }
    
    // 格式化日期函数
    const formatDate = (dateString) => {
      if (!dateString) return '';  // 返回空字符串而不是"未知时间"
      
      try {
        // 直接处理数据库返回的字符串格式
        // 例如: "2025-04-18 12:52:31.152885"
        if (typeof dateString === 'string') {
          // 将2025年的日期修正为当前年份
          const currentYear = new Date().getFullYear()
          const correctedDateString = dateString.replace(/^2025-/, `${currentYear}-`)
          
          // 创建日期对象
          const date = new Date(correctedDateString)
          
          // 检查日期是否有效
          if (!isNaN(date.getTime())) {
            // 格式化为友好的本地显示格式
            return date.toLocaleString('zh-CN', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit'
            })
          }
        }
        
        // 如果上面的处理失败，使用原始字符串
        return dateString.toString().replace(/^2025-/, `${new Date().getFullYear()}-`)
      } catch (error) {
        console.error('日期格式化错误:', error, dateString)
        return '';  // 出错时返回空字符串
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      if (!status) return '';  // 为空值返回空字符串
      switch (status) {
        case 'none': return '仅大纲'
        case 'generating': return '生成中'
        case 'completed': return '已完成'
        case 'failed': return '失败'
        default: return ''  // 默认也返回空字符串而非"未知"
      }
    }
    
    // 获取状态CSS类
    const getStatusClass = (status) => {
      if (!status) return '';  // 为空值返回空字符串
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
      try {
        if (typeof markdown !== 'string') {
          console.error('formatMarkdown: 非字符串输入:', markdown)
          return ''
        }
        const rawHtml = marked.parse(markdown)
        return DOMPurify.sanitize(rawHtml)
      } catch (error) {
        console.error('格式化Markdown出错:', error)
        return ''
      }
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      if (!status) return '';  // 为空值返回空字符串
      switch (status) {
        case 'completed':
          return 'success'
        case 'generating':
          return 'warning'
        case 'failed':
          return 'danger'
        default:
          return 'info'
      }
    }
    
    // 加载历史大纲
    const loadHistoryOutline = (record) => {
      if (record.outline) {
        outlinePreviewHtml.value = DOMPurify.sanitize(marked.parse(record.outline))
        outlinePreviewVisible.value = true
      } else {
        ElMessage.warning('该记录没有大纲内容')
      }
    }
    
    // 确认删除论文记录
    const confirmDeletePaper = (paper) => {
      if (!paper || !paper.id) return
      
      ElMessageBox.confirm(
        '确定要删除这条记录吗？此操作不可恢复。',
        '删除确认',
        {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
        .then(() => {
          deletePaper(paper.id)
        })
        .catch(() => {
          // 用户取消删除，不做任何操作
        })
    }
    
    // 删除论文记录
    const deletePaper = async (paperId) => {
      try {
        const response = await axios.delete(`/api/v1/academic/history/${paperId}`)
        
        if (response.data.status === 'success') {
          ElMessage.success('记录已成功删除')
          // 刷新列表
          await fetchHistory(historyCurrentPage.value)
        } else {
          throw new Error(response.data.message || '删除失败')
        }
      } catch (err) {
        console.error('删除记录失败:', err)
        ElMessage.error(`删除失败: ${err.message}`)
      }
    }
    
    return {
      topic,
      generatedOutline,
      paperContent,
      isGeneratingOutline,
      isGeneratingPaper,
      isEditingOutline,
      documentStatus,
      statusMessage,
      canGenerateOutline,
      renderedOutline,
      renderedContent,
      startGeneration,
      generateOutline,
      regenerateOutline,
      generatePaperFromOutline,
      handleEditModeChange,
      exportToWord,
      copyContent,
      generateSampleTopic,
      clearAll,
      downloadPaperFile,
      elapsedTime,
      outlineGenerationTime,
      totalGenerationTime,
      showHistory,
      historyDialogVisible,
      historyLoading,
      historyError,
      historyPapers,
      historyCurrentPage,
      historyPerPage,
      historyTotal,
      historyTotalPages,
      detailDialogVisible,
      selectedPaper,
      fetchHistory,
      handleCurrentChange,
      viewDetails,
      refreshPaperStatus,
      downloadPaper,
      closeHistoryDialog,
      closeDetailDialog,
      formatDate,
      getStatusText,
      getStatusClass,
      formatMarkdown,
      getStatusType,
      loadHistoryOutline,
      outlinePreviewVisible,
      outlinePreviewHtml,
      confirmDeletePaper,
      deletePaper,
      openHistoryDialog,
    }
  }
}
</script>

<style>
/* 引入GitHub Markdown样式 */
@import 'github-markdown-css/github-markdown.css';
</style>

<style scoped>
.paper-outline-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  color: #c62828; /* 紫荆红色 */
  font-size: 28px;
  margin-bottom: 20px;
  text-align: center;
  border-bottom: 2px solid #c62828;
  padding-bottom: 10px;
}

.section-label, .section-title {
  color: #c62828; /* 紫荆红色 */
  font-weight: bold;
}

.input-section {
  margin-top: 20px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  font-size: 16px;
}

.outline-tips {
  margin-top: 8px;
  padding: 8px;
  background: #f9f9f9;
  border: 1px solid #eaeaea;
  border-radius: 4px;
  font-size: 13px;
  color: #888;
}

.tips-text {
  margin-bottom: 5px;
  font-size: 13px;
  color: #888;
  line-height: 1.4;
}

.topic-input {
  margin-top: 10px;
}

.topic-input :deep(.el-input__inner) {
  font-size: 16px;
  padding: 12px;
  height: 50px;
  border-color: #ba003f;
  border-width: 2px;
  box-shadow: 0 2px 6px rgba(186, 0, 63, 0.1);
}

.format-example {
  background: #fff;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  margin: 10px 0;
}

.action-buttons {
  margin: 20px 0;
  display: flex;
  gap: 10px;
  justify-content: center;
}

/* 设置主题颜色为紫荆红 */
.action-buttons :deep(.el-button--primary) {
  background-color: #ba003f;
  border-color: #ba003f;
}

.action-buttons :deep(.el-button--primary:hover),
.action-buttons :deep(.el-button--primary:focus) {
  background-color: #d40046;
  border-color: #d40046;
}

.paper-content {
  margin-top: 30px;
  padding: 20px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.content-wrapper {
  margin: 20px 0;
  max-height: 600px;
  overflow-y: auto;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

/* 自定义Markdown样式 */
.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  word-wrap: break-word;
  color: #000; /* 确保文本颜色为黑色 */
}

.markdown-body p {
  color: #000; /* 确保段落文本为黑色 */
  margin-bottom: 16px;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body h1 { 
  font-size: 2em; 
  color: #ba003f; /* 紫荆红色标题 */
}

.markdown-body h2 { 
  font-size: 1.5em; 
  color: #c62828; /* 紫荆红色标题 */
}

.markdown-body h3 { 
  font-size: 1.25em; 
  color: #d32f2f; /* 紫荆红色标题（稍浅） */
}

.export-buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* 同样应用紫荆红主题 */
.export-buttons :deep(.el-button--primary) {
  background-color: #ba003f;
  border-color: #ba003f;
}

.export-buttons :deep(.el-button--primary:hover),
.export-buttons :deep(.el-button--primary:focus) {
  background-color: #d40046;
  border-color: #d40046;
}

/* 生成状态显示区域样式 */
.generation-status {
  margin: 20px 0;
  padding: 15px;
  border-radius: 6px;
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.status-text {
  margin: 10px 0;
  font-size: 16px;
  color: #333;
  display: flex;
  align-items: center;
}

.status-text .rotating {
  margin-right: 8px;
  font-size: 18px;
  color: #ba003f;
  animation: rotate 1.5s linear infinite;
}

.status-tip {
  margin: 5px 0 0;
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
}

.status-tip i {
  margin-right: 5px;
  color: #ba003f;
}

.generation-info {
  margin-bottom: 15px;
  padding: 8px 12px;
  background-color: #f0f8ff;
  border-left: 3px solid #ba003f;
  border-radius: 3px;
  font-size: 15px;
  color: #555;
  display: flex;
  align-items: center;
}

.generation-info i {
  margin-right: 8px;
  color: #ba003f;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .paper-outline-page {
    padding: 10px;
  }
  
  .action-buttons,
  .export-buttons {
    flex-direction: column;
  }
  
  .action-buttons .el-button,
  .export-buttons .el-button {
    width: 100%;
    margin-bottom: 10px;
  }
}

/* 添加编辑相关的CSS样式 */
.edit-switch {
  margin: 10px 0;
  display: flex;
  align-items: center;
}

.edit-tip {
  margin-left: 10px;
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
}

.edit-tip i {
  margin-right: 5px;
  color: #ba003f;
}

.outline-editor {
  margin: 20px 0;
}

/* 编辑框样式调整 */
.outline-editor :deep(.el-textarea__inner) {
  font-family: monospace;
  padding: 15px;
  line-height: 1.6;
  min-height: 300px;
}

/* 添加状态消息样式到style段中 */
.status-message {
  margin-top: 10px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
  text-align: center;
  background-color: #f0f8ff;
  border-left: 3px solid #ba003f;
  color: #666;
}

.button-wrapper {
  display: inline-block;
}

/* 历史记录按钮样式 */
.btn-history {
  background-color: #ba003f; /* 紫荆红色 */
  color: white;
  border: none;
  padding: 9px 15px; /* 调整为与el-button一致的内边距 */
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 32px; /* 确保高度与el-button一致 */
  line-height: 1;
}

.btn-history:hover {
  background-color: #d40046; /* 紫荆红色hover状态 */
}

.btn-history i {
  margin-right: 5px;
}

/* 历史记录样式 */
.history-container {
  padding: 10px;
}

.pagination-container {
  margin-top: 20px;
  text-align: center;
}

.empty-text {
  text-align: center;
  padding: 30px 0;
  color: #909399;
  font-size: 14px;
}

.outline-preview {
  max-height: 60vh;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #f5f7fa;
}

/* 确保弹窗内的内容样式正常 */
:deep(.outline-preview h1) {
  font-size: 1.8em;
  margin-bottom: 16px;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

:deep(.outline-preview h2) {
  font-size: 1.5em;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
}

:deep(.outline-preview h3) {
  font-size: 1.25em;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
}

:deep(.outline-preview p) {
  margin-top: 0;
  margin-bottom: 16px;
  line-height: 1.6;
}

:deep(.outline-preview ul, .outline-preview ol) {
  padding-left: 2em;
  margin-top: 0;
  margin-bottom: 16px;
}

:deep(.outline-preview li) {
  margin-bottom: 0.5em;
}
</style>