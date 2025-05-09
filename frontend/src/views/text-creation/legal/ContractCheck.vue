<template>
  <div class="contract-check-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>合同检查</h2>
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
            <i class="ri-file-text-line"></i>
            合同上传
          </h3>
        </div>
        
        <!-- 文件上传区域 -->
        <div class="form-group">
          <label for="contract-type">合同类型</label>
          <select id="contract-type" v-model="contractType" class="form-control">
            <option value="labor">劳动合同</option>
            <option value="purchase">采购合同</option>
            <option value="lease">租赁合同</option>
            <option value="service">服务合同</option>
            <option value="confidentiality">保密协议</option>
            <option value="other">其他合同</option>
          </select>
        </div>

        <div class="form-group">
          <label for="contract-upload">上传合同文件</label>
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
              accept=".txt,.doc,.docx,.pdf"
              style="display: none"
            />
            <span class="file-name" v-if="selectedFile">{{ selectedFile.name }}</span>
            <span class="file-upload-hint" v-else>支持txt、doc、docx、pdf格式</span>
          </div>
        </div>

        <!-- 检查选项 -->
        <div class="form-group">
          <label>检查重点</label>
          <div class="checkbox-group">
            <label class="checkbox-container">
              <input type="checkbox" v-model="checkOptions.rights">
              <span>权利义务</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="checkOptions.risks">
              <span>风险条款</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="checkOptions.terms">
              <span>关键条款</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="checkOptions.penalties">
              <span>违约责任</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="checkOptions.compliance">
              <span>合规性</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="checkOptions.language">
              <span>语言表述</span>
            </label>
          </div>
        </div>
        
        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="checkContract" class="btn btn-primary" :disabled="isChecking || !selectedFile">
            <i class="ri-search-line" v-if="!isChecking"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isChecking ? '检查中...' : '开始检查' }}
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
              合同分析结果
            </h3>
            <div class="action-buttons">
              <button @click="checkContract" class="primary-button" :disabled="isChecking || !selectedFile">
                <i class="ri-refresh-line" v-if="!isChecking"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isChecking ? '检查中...' : '重新检查' }}
              </button>
              <button @click="copyText" class="secondary-button" :disabled="isChecking || !checkResult">
                <i class="ri-file-copy-line"></i>
                复制文本
              </button>
              <button @click="downloadResult" class="secondary-button" :disabled="isChecking || !checkResult">
                <i class="ri-download-line"></i>
                下载报告
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
                <p class="empty-message">请上传合同文件后进行检查</p>
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
    
    <!-- 知识学习侧边抽屉 -->
    <el-drawer
      v-model="showTipsModal"
      title="文章总结知识学习"
      direction="rtl"
      size="30%"
      class="knowledge-drawer"
      :with-header="true"
      :destroy-on-close="false"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in summaryKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatKnowledgeText(item.text)"></div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElLoading } from 'element-plus'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { summaryKnowledge } from '../../Knowledge_data.js'

export default {
  name: 'ContractCheck',
  setup() {
    // 状态变量
    const selectedFile = ref(null)
    const contractType = ref('other')
    const isChecking = ref(false)
    const checkResult = ref('')
    const fileInput = ref(null)
    const showTipsModal = ref(false)
    const fileId = ref('')
    const loadingText = ref('正在分析合同内容...')
    const messages = ref([])
    const loadingInstance = ref(null)

    // 检查选项
    const checkOptions = ref({
      rights: true,
      risks: true,
      terms: true,
      penalties: true,
      compliance: true,
      language: false
    })

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

      const allowedTypes = ['text/plain', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
      const maxSize = 10 * 1024 * 1024 // 10MB

      if (!allowedTypes.includes(file.type) && 
          !file.name.endsWith('.txt') && 
          !file.name.endsWith('.pdf') && 
          !file.name.endsWith('.doc') && 
          !file.name.endsWith('.docx')) {
        ElMessage.error('文件格式不支持，请上传txt、doc、docx或pdf格式的文件')
        return
      }

      if (file.size > maxSize) {
        ElMessage.error('文件大小不能超过10MB')
        return
      }

      selectedFile.value = file

      // 上传文件到服务器
      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await axios.post('/api/v1/file_chat/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        if (response.data.success) {
          ElMessage.success('文件上传成功')
          fileId.value = response.data.file_id
        } else {
          ElMessage.error(`文件上传失败: ${response.data.message}`)
        }
      } catch (error) {
        console.error('文件上传错误:', error)
        ElMessage.error('文件上传失败，请稍后重试')
      }
    }

    // 检查合同
    const checkContract = async () => {
      // 验证是否有内容需要检查
      if (!selectedFile.value) {
        ElMessage.warning('请上传合同文件')
        return
      }

      // 准备检查
      isChecking.value = true
      checkResult.value = ''
      
      // 显示loading
      loadingInstance.value = ElLoading.service({
        lock: true,
        text: '正在分析合同内容...',
        background: 'rgba(255, 255, 255, 0.8)'
      })

      // 更新loading文本
      setTimeout(() => {
        loadingText.value = '正在检查合同条款...'
      }, 3000)
      
      setTimeout(() => {
        loadingText.value = '正在撰写分析结果...'
      }, 6000)

      try {
        // 准备系统消息和用户消息
        const systemMessage = {
          role: "system",
          content: `你是一位专业的合同审查专家，请详细检查合同内容并提供专业分析。重点关注以下方面：
            ${checkOptions.value.rights ? '- 权利义务：分析合同中双方权利义务是否对等' : ''}
            ${checkOptions.value.risks ? '- 风险条款：识别可能存在风险的条款并提出建议' : ''}
            ${checkOptions.value.terms ? '- 关键条款：突出显示合同中的关键条款' : ''}
            ${checkOptions.value.penalties ? '- 违约责任：检查违约责任条款是否明确且合理' : ''}
            ${checkOptions.value.compliance ? '- 合规性：基于常见法律法规检查合同合规性' : ''}
            ${checkOptions.value.language ? '- 语言表述：提供语言表述方面的改进建议' : ''}
            分析后，请提供一份合同审查报告，包括以下部分：
            1. 合同基本信息分析
            2. 主要条款概述
            3. 问题条款分析（以表格形式展示：条款|问题描述|修改建议）
            4. 整体评估和建议
            请使用markdown格式输出，并确保专业、客观。`
        }

        const userMessage = {
          role: "user",
          content: `我需要你帮我审查一份${contractType.value === 'other' ? '合同' : contractType.value}合同，请分析其中可能存在的问题并给出修改建议。`
        }

        // 准备请求参数
        const requestData = {
          file_id: fileId.value,
          messages: [systemMessage, userMessage],
          temperature: 0.5,
          max_tokens: 4000
        }

        console.log('发送请求数据:', JSON.stringify(requestData))
        console.log('文件ID检查:', fileId.value)

        // 使用完整URL路径，不依赖axios默认设置
        const chatUrl = `${axios.defaults.baseURL}/api/v1/file_chat/chat`
        console.log('聊天API URL:', chatUrl)
        
        // 发送请求
        const chatResponse = await axios.post(chatUrl, requestData, {
          timeout: 120000, // 增加超时时间到120秒
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        console.log('API响应:', chatResponse.data)

        if (chatResponse.data && chatResponse.data.success) {
          // 将后端返回格式直接存储，我们的后端API返回格式为:
          // { success: true, content: "...", role: "assistant" }
          checkResult.value = chatResponse.data.content
          messages.value = [systemMessage, userMessage, {
            role: "assistant",
            content: chatResponse.data.content
          }]
        } else {
          const errorMsg = chatResponse.data?.message || '未知错误'
          console.error('API返回错误:', errorMsg)
          ElMessage.error(`合同检查失败: ${errorMsg}`)
        }
      } catch (error) {
        console.error('合同检查错误:', error)
        let errorMessage = '合同检查失败，请稍后重试'
        
        if (error.response) {
          // 服务器返回了状态码
          console.error('错误状态:', error.response.status)
          console.error('错误数据:', error.response.data)
          errorMessage = `合同检查失败: ${error.response.status} - ${error.response.data?.message || '未知错误'}`
        } else if (error.request) {
          // 请求发出但没有收到响应
          console.error('无响应:', error.request)
          errorMessage = '服务器无响应，请检查后端服务是否正常运行于端口9000'
        } else {
          // 请求设置时出错
          console.error('请求错误:', error.message)
          errorMessage = `请求错误: ${error.message}`
        }
        
        ElMessage.error(errorMessage)
      } finally {
        isChecking.value = false
        if (loadingInstance.value) {
          loadingInstance.value.close()
        }
      }
    }

    // 复制文本
    const copyText = () => {
      if (!checkResult.value) return
      
      // 创建一个纯文本版本
      const plainText = checkResult.value
      
      navigator.clipboard.writeText(plainText)
        .then(() => {
          ElMessage.success('已复制到剪贴板')
        })
        .catch(() => {
          ElMessage.error('复制失败')
        })
    }

    // 下载报告
    const downloadResult = () => {
      if (!checkResult.value) return
      
      const filename = `合同检查报告_${new Date().toLocaleDateString().replace(/\//g, '-')}.md`
      const blob = new Blob([checkResult.value], { type: 'text/markdown' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }

    // 重置表单
    const resetForm = () => {
      selectedFile.value = null
      contractType.value = 'other'
      checkResult.value = ''
      fileId.value = ''
      
      // 重置文件输入
      if (fileInput.value) {
        fileInput.value.value = ''
      }
      
      // 默认选项
      checkOptions.value = {
        rights: true,
        risks: true,
        terms: true,
        penalties: true,
        compliance: true,
        language: false
      }
    }

    // 显示使用说明
    const showTips = () => {
      showTipsModal.value = true
    }

    // 格式化知识文本（将Markdown转换为HTML）
    const formatKnowledgeText = (text) => {
      return marked(text)
    }

    // 组件挂载
    onMounted(() => {
      // 初始化
    })

    return {
      selectedFile,
      contractType,
      isChecking,
      checkResult,
      fileInput,
      showTipsModal,
      checkOptions,
      loadingText,
      formattedResult,
      summaryKnowledge,
      formatKnowledgeText,
      triggerFileUpload,
      handleFileUpload,
      checkContract,
      copyText,
      downloadResult,
      resetForm,
      showTips
    }
  }
}
</script>

<style scoped>
@import "@/assets/css/text-creation-common.css";

.contract-check-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f7f7f7;
}

/* 文件上传相关样式 */
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
  border-color: var(--primary-color, #ba003f);
  color: var(--primary-color, #ba003f);
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

/* 复选框容器样式 */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
}

/* 结果内容 */
.contract-result {
  height: 100%;
}

/* 小贴士列表样式 */
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

/* 知识学习相关样式 */
:deep(.el-drawer__header) {
  margin-bottom: 0;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-drawer__title) {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-color, #ba003f);
}
</style> 