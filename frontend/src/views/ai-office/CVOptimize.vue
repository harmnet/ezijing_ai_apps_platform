<template>
  <div class="contract-check-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>AI简历优化</h2>
      </div>
      <div class="page-actions">
        <button class="action-btn" title="使用说明" @click="showTips">
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
            <i class="ri-file-text-line"></i>
            简历上传
          </h3>
        </div>
        
        <!-- 文件上传区域 -->
        <div class="form-group">
          <label for="contract-upload">上传简历文件</label>
          <div class="file-upload-container">
            <button class="file-upload-btn" @click="triggerFileUpload">
              <i class="ri-upload-2-line"></i>
              选择文件
            </button>
            <input
              type="file"
              id="file-upload"
              ref="fileInput"
              @change="handleFileUpload"
              accept=".pdf,.docx,.doc"
              style="display: none"
            />
            <span class="file-name" v-if="selectedFile">{{ selectedFile.name }}</span>
            <span class="file-upload-hint" v-else>支持pdf、docx、doc格式</span>
          </div>
        </div>

        <!-- 检查选项 -->
        <div class="form-group">
          <label>优化重点</label>
          <div class="checkbox-group">
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="structure">
              <span>结构优化</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="content">
              <span>内容增强</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="highlight">
              <span>亮点提炼</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="keywords">
              <span>关键词优化</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="comprehensive">
              <span>全面优化</span>
            </label>
          </div>
        </div>
        
        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="checkContract" class="btn btn-primary" :disabled="isChecking || !selectedFile">
            <i class="ri-search-line" v-if="!isChecking"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isChecking ? '优化中...' : '开始优化' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：结果 -->
      <div class="right-column">
        <!-- 检查结果 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-file-search-line"></i>
              简历优化结果
            </h3>
            <div class="action-buttons">
              <button @click="checkContract" class="primary-button" :disabled="isChecking || !selectedFile">
                <i class="ri-refresh-line" v-if="!isChecking"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isChecking ? '优化中...' : '重新优化' }}
              </button>
              <button @click="copyText" class="secondary-button" :disabled="isChecking || !checkResult">
                <i class="ri-file-copy-line"></i>
                复制文本
              </button>
              <button @click="downloadResult" class="secondary-button" :disabled="isChecking || !checkResult">
                <i class="ri-download-line"></i>
                下载简历
              </button>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isChecking" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <!-- 空状态 -->
            <div v-if="!checkResult && !isChecking" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">请上传简历文件后进行优化</p>
              </div>
            </div>
            
            <!-- 检查结果展示 -->
            <div v-else-if="checkResult" class="contract-result" :class="{'blur-content': isChecking}">
              <div class="result-content">
                <div v-html="formattedResult"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 使用说明模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line"></i> AI简历优化使用说明</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>📄 <b>文件支持</b> - 支持上传pdf、docx、doc格式的简历文件</li>
            <li>🔍 <b>优化选项</b> - 选择需要重点优化的简历方面</li>
            <li>📊 <b>结构优化</b> - 调整简历结构更加清晰易读，突出重点</li>
            <li>❓ <b>内容增强</b> - 增强简历内容表述，使成就和经历更有说服力</li>
            <li>🔄 <b>亮点提炼</b> - 突出个人亮点和核心竞争力</li>
            <li>⚠️ <b>关键词优化</b> - 增加行业关键词，提高简历的ATS通过率</li>
            <li>📈 <b>全面优化</b> - 从结构、内容、关键词等多方面全面提升简历质量</li>
          </ul>
          <div class="tips-note">
            <p><b>注意：</b>本工具提供的优化结果仅供参考，细节可能需要根据个人情况进行调整。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElLoading } from 'element-plus'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

export default {
  name: 'CVOptimize',
  setup() {
    // 状态变量
    const selectedFile = ref(null)
    const isChecking = ref(false)
    const checkResult = ref('')
    const fileInput = ref(null)
    const showTipsModal = ref(false)
    const fileId = ref('')
    const loadingText = ref('正在处理简历内容...')
    const messages = ref([])
    const loadingInstance = ref(null)

    // 检查选项
    const analysisOption = ref('structure')

    // 格式化结果
    const formattedResult = computed(() => {
      if (!checkResult.value) return ''
      // 使用marked将markdown格式转换为HTML
      const html = marked(checkResult.value)
      // 使用DOMPurify来防止XSS攻击
      return DOMPurify.sanitize(html)
    })

    // 触发文件上传
    const triggerFileUpload = () => {
      fileInput.value.click()
    }

    // 处理文件上传
    const handleFileUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-word']
      const maxSize = 10 * 1024 * 1024 // 10MB

      if (!allowedTypes.includes(file.type) && 
          !file.name.endsWith('.pdf') && 
          !file.name.endsWith('.docx') && 
          !file.name.endsWith('.doc')) {
        ElMessage.error('文件格式不支持，请上传pdf、docx或doc格式的文件')
        return
      }

      if (file.size > maxSize) {
        ElMessage.error('文件大小不能超过10MB')
        return
      }

      selectedFile.value = file

      // 上传文件到服务器
      try {
        console.log('开始上传文件:', file.name)
        const formData = new FormData()
        formData.append('file', file)

        // 使用完整URL路径进行上传
        const uploadUrl = `${axios.defaults.baseURL}/api/v1/file_chat/upload`
        console.log('上传API URL:', uploadUrl)
        
        const response = await axios.post(uploadUrl, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          timeout: 60000 // 60秒超时
        })
        
        console.log('文件上传响应:', response.data)
        if (response.data.success) {
          fileId.value = response.data.file_id
          ElMessage.success('文件上传成功')
        } else {
          ElMessage.error(response.data.message || '文件上传失败')
        }
      } catch (error) {
        console.error('文件上传错误:', error)
        let errorMessage = '文件上传失败，请稍后重试'
        
        if (error.response) {
          // 服务器返回了状态码
          console.error('错误状态:', error.response.status)
          console.error('错误数据:', error.response.data)
        } else if (error.request) {
          // 请求发出但没有收到响应
          console.error('没有收到响应:', error.request)
          console.error('请求URL:', error.config?.url)
          console.error('请求方法:', error.config?.method)
        }
        
        ElMessage.error(errorMessage)
      }
    }

    // 执行数据分析
    const checkContract = async () => {
      // 验证是否有内容需要检查
      if (!selectedFile.value) {
        ElMessage.warning('请上传简历文件')
        return
      }

      // 设置正在检查状态
      isChecking.value = true
      checkResult.value = ''

      // 显示加载指示器
      loadingInstance.value = ElLoading.service({
        lock: true,
        text: '正在处理简历内容...',
        background: 'rgba(255, 255, 255, 0.8)'
      })

      // 更新loading文本
      setTimeout(() => {
        loadingText.value = '正在优化简历内容...'
      }, 3000)
      
      // 设置延时以显示多个loading文本
      setTimeout(() => {
        loadingText.value = '正在生成优化建议...'
      }, 6000)

      try {
        // 构建系统消息和用户消息
        const systemMessage = {
          role: "system",
          content: `你是一位专业的HR和简历优化专家，请对上传的简历文件进行分析和优化。重点关注以下方面：
            ${analysisOption.value === 'structure' ? '- 结构优化：调整简历结构更加清晰易读，突出重点内容，优化排版布局，帮助招聘者快速找到关键信息。' : ''}
            ${analysisOption.value === 'content' ? '- 内容增强：改进简历中的表述方式，使成就和工作经历更加量化和有说服力，增加行动导向的语言和成果展示。' : ''}
            ${analysisOption.value === 'highlight' ? '- 亮点提炼：突出个人核心优势和独特卖点，强调与目标职位相关的关键能力和成就，帮助申请者在竞争中脱颖而出。' : ''}
            ${analysisOption.value === 'keywords' ? '- 关键词优化：增加行业和职位关键词，提高简历的ATS系统通过率，确保简历能够匹配招聘软件的筛选条件。' : ''}
            ${analysisOption.value === 'comprehensive' ? '- 全面优化：从结构、内容、关键词、视觉呈现等多方面全面提升简历质量，提高求职成功率。' : ''}
            
            请提供一份详细的简历优化报告，包括以下部分：
            1. 简历整体评估
            2. 优势分析（当前简历的亮点和优势）
            3. 问题分析（以表格形式展示：问题部分|问题描述|优化建议）
            4. 优化后的简历内容建议
            5. 求职建议和下一步行动计划
            
            请使用markdown格式输出，确保分析专业、实用，建议具体可行。`
        }

        const userMessage = {
          role: "user",
          content: `请帮我优化我的简历，让它更有竞争力，能够吸引招聘者的注意，提高面试邀请率。请根据行业最佳实践提供详细的优化建议。`
        }

        // 将消息添加到数组
        messages.value = [systemMessage, userMessage]

        // 准备请求参数
        const requestData = {
          file_id: fileId.value,
          messages: messages.value,
          temperature: 0.7,
          max_tokens: 2000
        }

        console.log('发送请求数据:', JSON.stringify(requestData))
        console.log('文件ID检查:', fileId.value)

        // 使用完整URL路径，不依赖axios默认设置
        const chatUrl = `${axios.defaults.baseURL}/api/v1/file_chat/chat`
        console.log('聊天API URL:', chatUrl)

        // 发送请求到服务器
        const chatResponse = await axios.post(chatUrl, requestData, {
          timeout: 120000, // 增加超时时间到120秒
          headers: {
            'Content-Type': 'application/json'
          }
        })

        // 处理响应
        if (chatResponse.data.success) {
          console.log("API返回成功，内容长度:", chatResponse.data.content.length);
          console.log("API返回内容预览:", chatResponse.data.content.substring(0, 100));
          checkResult.value = chatResponse.data.content;
        } else {
          const errorMsg = chatResponse.data?.message || '未知错误'
          console.error('API返回错误:', errorMsg)
          ElMessage.error(`简历优化失败: ${errorMsg}`)
        }
      } catch (error) {
        console.error('简历优化错误:', error)
        let errorMessage = '简历优化失败，请稍后重试'
        
        if (error.response) {
          // 服务器返回了状态码
          console.error('错误状态:', error.response.status)
          console.error('错误数据:', error.response.data)
          errorMessage = `简历优化失败: ${error.response.status} - ${error.response.data?.message || '未知错误'}`
        } else if (error.request) {
          // 请求发出但没有收到响应
          console.error('没有收到响应:', error.request)
          // 尝试输出请求详情以便调试
          console.error('请求URL:', error.config?.url)
          console.error('请求方法:', error.config?.method)
          console.error('请求数据:', JSON.stringify(error.config?.data))
          errorMessage = '服务器没有响应，请检查网络连接或后端服务状态'
        }
        
        ElMessage.error(errorMessage)
      } finally {
        // 关闭加载指示器
        if (loadingInstance.value) {
          loadingInstance.value.close()
        }
        // 重置状态
        isChecking.value = false
      }
    }

    // 复制文本
    const copyText = () => {
      if (!checkResult.value) return
      
      navigator.clipboard.writeText(checkResult.value)
        .then(() => {
          ElMessage.success('已复制到剪贴板')
        })
        .catch(err => {
          console.error('复制失败:', err)
          ElMessage.error('复制失败')
        })
    }

    // 下载结果
    const downloadResult = () => {
      if (!checkResult.value) return
      
      const filename = `简历优化建议_${new Date().toLocaleDateString().replace(/\//g, '-')}.md`
      const blob = new Blob([checkResult.value], { type: 'text/markdown' })
      const link = document.createElement('a')
      
      link.href = URL.createObjectURL(blob)
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      ElMessage.success('简历优化建议下载成功')
    }

    // 显示提示
    const showTips = () => {
      showTipsModal.value = true
    }

    // 重置表单
    const resetForm = () => {
      selectedFile.value = null
      analysisOption.value = 'structure'
      checkResult.value = ''
      fileId.value = ''
      
      // 清空文件输入
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    return {
      selectedFile,
      isChecking,
      checkResult,
      fileInput,
      showTipsModal,
      analysisOption,
      loadingText,
      formattedResult,
      triggerFileUpload,
      handleFileUpload,
      checkContract,
      resetForm,
      copyText,
      downloadResult,
      showTips,
    }
  }
}
</script>

<style scoped>
.contract-check-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f7f7f7;
}

.page-header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.page-nav h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: #555;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: #f0f0f0;
  color: #BA0040;
}

.main-container {
  flex: 1;
  padding: 16px;
  display: flex;
  gap: 16px;
  overflow: hidden;
}

/* 左侧输入部分 */
.input-section {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title i {
  color: #BA0040;
}

.form-group {
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.form-control:focus {
  border-color: #BA0040;
}

.file-upload-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-upload-btn {
  background-color: #f0f0f0;
  color: #555;
  border: 1px dashed #ccc;
  padding: 10px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.file-upload-btn:hover {
  background-color: #e8e8e8;
  border-color: #BA0040;
  color: #BA0040;
}

.file-name {
  font-size: 14px;
  color: #333;
  padding: 4px 8px;
  background-color: #f7f7f7;
  border-radius: 4px;
  word-break: break-all;
}

.file-upload-hint {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.checkbox-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
}

.action-buttons {
  display: flex;
  gap: 8px;
  margin-top: auto;
  margin-bottom: 8px;
}

.btn {
  padding: 10px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #BA0040;
  color: #fff;
  flex: 1;
}

.btn-primary:hover {
  background-color: #A10038;
}

.btn-primary:disabled {
  background-color: #E6A0B8;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #555;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

/* 右侧结果区域 */
.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
}

.result-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.result-content-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.result-content {
  padding: 16px 24px;
  height: 100%;
  overflow-y: auto;
}

.empty-result {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.empty-content {
  text-align: center;
  padding: 24px;
}

.empty-image {
  width: 128px;
  height: 128px;
  margin-bottom: 16px;
}

.empty-message {
  color: #999;
  font-size: 14px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(186, 0, 64, 0.2);
  border-top-color: #BA0040;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 16px;
  font-size: 14px;
  color: #BA0040;
}

/* 结果内容 */
.contract-result {
  height: 100%;
}

.blur-content {
  filter: blur(4px);
  pointer-events: none;
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
  background-color: #fff;
  border-radius: 8px;
  width: 600px;
  max-width: 90vw;
  max-height: 80vh;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 16px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  color: #BA0040;
}

.close-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 20px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background-color: #f0f0f0;
  color: #333;
}

.modal-body {
  padding: 16px;
  overflow-y: auto;
}

.tips-list {
  list-style-type: none;
  padding: 0;
  margin: 0 0 16px;
}

.tips-list li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.tips-note {
  background-color: #f7f7f7;
  padding: 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #555;
}

.tips-note p {
  margin: 0;
}

/* 动画 */
.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.primary-button {
  padding: 6px 12px;
  border-radius: 4px;
  background-color: #BA0040;
  color: white;
  border: none;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.primary-button:hover {
  background-color: #A10038;
}

.primary-button:disabled {
  background-color: #E6A0B8;
  cursor: not-allowed;
}

.secondary-button {
  padding: 6px 12px;
  border-radius: 4px;
  background-color: #f0f0f0;
  color: #555;
  border: none;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.secondary-button:hover {
  background-color: #e0e0e0;
}

.secondary-button:disabled {
  background-color: #f0f0f0;
  color: #bbb;
  cursor: not-allowed;
}
</style> 