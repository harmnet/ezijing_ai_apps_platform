<template>
  <div class="contract-check-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>AI数据分析</h2>
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
            数据集上传
          </h3>
        </div>
        
        <!-- 文件上传区域 -->
        <div class="form-group">
          <label for="file-upload">上传数据集文件</label>
          <div class="file-upload-container">
            <input 
              type="file" 
              id="file-upload" 
              ref="fileInput" 
              class="file-input" 
              @change="handleFileUpload" 
              accept=".xlsx,.xls"
              style="display: none"
            />
            <button class="file-upload-btn" @click="triggerFileUpload">
              <i class="ri-upload-2-line"></i>
              选择文件
            </button>
            <span class="file-upload-hint" v-if="!selectedFile">
              支持xls、xlsx格式
            </span>
            <span class="file-upload-selected" v-else>
              已选择: {{ selectedFile.name }}
              <button class="file-clear-btn" @click="clearSelectedFile">
                <i class="ri-close-line"></i>
              </button>
            </span>
          </div>
          <div class="file-upload-progress" v-if="isUploading">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <span class="progress-text">上传中... {{ uploadProgress }}%</span>
          </div>
        </div>

        <!-- 检查选项 -->
        <div class="form-group">
          <label>检查重点</label>
          <div class="checkbox-group">
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="data_quality">
              <span>数据质量</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="missing_values">
              <span>缺失值</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="duplicate_values">
              <span>重复值</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="outliers">
              <span>异常值</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="regular_analysis">
              <span>常规数据分析</span>
            </label>
            <label class="checkbox-container">
              <input type="radio" v-model="analysisOption" value="user_profile">
              <span>用户画像</span>
            </label>
          </div>
        </div>
        
        <!-- 更多提示词要求 -->
        <div class="form-group">
          <label for="extra-prompt">更多提示词要求</label>
          <textarea 
            id="extra-prompt" 
            v-model="extraPrompt" 
            placeholder="请输入额外的分析要求或提示词..." 
            class="form-control" 
            rows="6"
          ></textarea>
        </div>
        
        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="checkContract" class="btn btn-primary" :disabled="isChecking || !selectedFile">
            <i class="ri-search-line" v-if="!isChecking"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isChecking ? '分析中...' : '开始分析' }}
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
              数据分析结果
            </h3>
            <div class="action-buttons">
              <button @click="checkContract" class="primary-button" :disabled="isChecking || !selectedFile">
                <i class="ri-refresh-line" v-if="!isChecking"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isChecking ? '分析中...' : '重新分析' }}
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
                <p class="empty-message">请上传数据集文件后进行分析</p>
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
          <h3><i class="ri-lightbulb-line"></i> AI数据分析使用说明</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>📄 <b>文件支持</b> - 支持上传xls、xlsx格式的Excel数据文件</li>
            <li>🔍 <b>分析选项</b> - 选择需要重点分析的数据方面</li>
            <li>📊 <b>数据质量</b> - 全面评估数据集的完整性、准确性和一致性</li>
            <li>❓ <b>缺失值</b> - 识别并分析数据集中的空值或缺失数据</li>
            <li>🔄 <b>重复值</b> - 检测数据集中的重复记录并提供处理建议</li>
            <li>⚠️ <b>异常值</b> - 发现数据集中的异常或离群值</li>
            <li>📈 <b>常规数据分析</b> - 提供基本的统计分析，包括平均值、中位数等</li>
          </ul>
          <div class="tips-note">
            <p><b>注意：</b>本工具提供的分析结果仅供参考，复杂数据分析问题可能需要专业的数据科学工具。</p>
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
  name: 'DataAnalysis',
  setup() {
    // 状态变量
    const selectedFile = ref(null)
    const isChecking = ref(false)
    const checkResult = ref('')
    const fileInput = ref(null)
    const showTipsModal = ref(false)
    const fileId = ref('')
    const loadingText = ref('正在生成分析报告...')
    const messages = ref([])
    const loadingInstance = ref(null)
    
    // 新增文件上传相关状态
    const isUploading = ref(false)
    const uploadProgress = ref(0)
    const isStreaming = ref(false)
    
    // 新增更多提示词要求
    const extraPrompt = ref('')

    // 检查选项
    const analysisOption = ref('data_quality')
    
    // 处理URL参数
    onMounted(() => {
      // 获取当前URL的查询参数
      const queryParams = new URLSearchParams(window.location.search)
      
      // 获取URL中的分析选项参数
      if (queryParams.has('analysisOption')) {
        analysisOption.value = queryParams.get('analysisOption')
      }
      
      // 获取URL中的额外提示词参数
      if (queryParams.has('extraPrompt')) {
        extraPrompt.value = queryParams.get('extraPrompt')
      }
      
      console.log('从URL参数获取的分析选项:', analysisOption.value)
      if (extraPrompt.value) {
        console.log('从URL参数获取的额外提示词:', extraPrompt.value.substring(0, 50) + '...')
      }
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

    // 清除已选择的文件
    const clearSelectedFile = () => {
      selectedFile.value = null
      fileId.value = ''
      // 重置文件输入控件
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    // 处理文件上传
    const handleFileUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      // 检查文件大小（限制为10MB）
      const maxSize = 10 * 1024 * 1024 // 10MB
      if (file.size > maxSize) {
        ElMessage.error('文件大小不能超过10MB')
        return
      }

      // 文件类型检查
      const allowedTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
        'application/vnd.ms-excel'
      ]
      
      if (!allowedTypes.includes(file.type) && 
          !file.name.endsWith('.xlsx') && 
          !file.name.endsWith('.xls')) {
        ElMessage.error('文件格式不支持，请上传xls或xlsx格式的文件')
        return
      }

      // 保存选中的文件
      selectedFile.value = file
      console.log('选择文件:', file.name, '类型:', file.type, '大小:', file.size)
    }

    // 上传文件到服务器 - 参考Proofreading.vue实现
    const uploadFile = async () => {
      if (!selectedFile.value) return false

      isUploading.value = true
      uploadProgress.value = 0

      try {
        console.log('========== 第1步：上传数据集文件 ==========')
        console.log('文件信息:', {
          名称: selectedFile.value.name,
          类型: selectedFile.value.type,
          大小: `${(selectedFile.value.size / 1024).toFixed(2)} KB`
        })
        
        // 创建FormData对象
        const formData = new FormData()
        formData.append('file', selectedFile.value)
        
        // 模型ID映射表 - 从前端选择器ID到后端支持的ID
        const modelMap = {
          'deepseek-v3': 'deepseek-v3-vol', // 火山引擎 DeepSeek V3
          'deepseek-r1': 'deepseek-r1-vol', // 火山引擎 DeepSeek R1
          'deepseek-r1-vol': 'deepseek-r1-vol', // 已经是正确格式
          'douban': 'doubao-pro' // 豆包模型
        }
        
        // 使用默认模型ID
        const modelId = 'deepseek-v3'
        const uploadModelId = modelMap[modelId] || modelId
        
        console.log('使用的模型ID:', modelId)
        console.log('文件上传使用的转换后模型ID:', uploadModelId)
        
        // 添加模型参数
        formData.append('model', uploadModelId)
        
        // 构建分析提示词
        let prompt = '请对以下数据集文件内容进行分析，';
        
        // 添加分析选项
        prompt += '重点关注：';
        
        if (analysisOption.value === 'data_quality') {
          prompt += '数据质量，全面评估数据集的完整性、准确性和一致性';
        } else if (analysisOption.value === 'missing_values') {
          prompt += '缺失值，识别并分析数据集中的空值或缺失数据';
        } else if (analysisOption.value === 'duplicate_values') {
          prompt += '重复值，检测数据集中的重复记录并提供处理建议';
        } else if (analysisOption.value === 'outliers') {
          prompt += '异常值，发现数据集中的异常或离群值';
        } else if (analysisOption.value === 'regular_analysis') {
          prompt += '常规数据分析，提供基本的统计分析，包括平均值、中位数等';
        } else if (analysisOption.value === 'user_profile') {
          prompt += '用户画像，分析数据集中的用户特征和行为模式';
        }
        
        // 添加额外提示词要求
        if (extraPrompt.value && extraPrompt.value.trim()) {
          prompt += `。\n\n此外，请特别注意以下要求：${extraPrompt.value.trim()}`;
        } else {
          prompt += '。请提供一份详细的分析报告，包括数据集基本信息、主要特征、问题分析和建议。';
        }
        
        formData.append('prompt', prompt)
        
        // 文件上传API路径
        const fileUploadApi = '/api/v1/llm/file_chat'
        
        console.log('文件上传参数:', {
          API路径: fileUploadApi,
          文件名: selectedFile.value.name,
          模型ID: uploadModelId,
          提示词长度: prompt.length
        })
        
        console.log('开始上传文件...')
        
        // 上传文件，获取文本内容
        const uploadResponse = await axios.post(fileUploadApi, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            console.log(`上传进度: ${uploadProgress.value}%`)
          }
        })
        
        console.log('文件上传完成，响应状态:', uploadResponse.status)
        console.log('文件上传响应数据结构:', Object.keys(uploadResponse.data))
        
        // 检查上传响应
        if (!uploadResponse.data || uploadResponse.data.status !== 'success') {
          console.error('文件上传失败:', uploadResponse.data)
          throw new Error(uploadResponse.data?.message || '文件处理失败')
        }
        
        console.log('文件上传成功，状态:', uploadResponse.data.status)
        
        // 检查响应数据结构
        console.log('响应data字段结构:', Object.keys(uploadResponse.data.data || {}))
        
        // 检查是否有提取的文本
        let extractedText = ''
        
        // 处理不同的响应格式
        if (uploadResponse.data.data && uploadResponse.data.data.extracted_text) {
          extractedText = uploadResponse.data.data.extracted_text
          console.log('从extracted_text字段提取到文本')
        } else if (uploadResponse.data.data && uploadResponse.data.data.text) {
          extractedText = uploadResponse.data.data.text
          console.log('从text字段提取到文本')
        } else if (uploadResponse.data.data && typeof uploadResponse.data.data === 'string') {
          extractedText = uploadResponse.data.data
          console.log('从data字段直接提取到文本')
        } else if (uploadResponse.data.data && uploadResponse.data.data.choices && 
                  uploadResponse.data.data.choices.length > 0 && 
                  uploadResponse.data.data.choices[0].message) {
          
          // 如果已经有完整结果，直接使用
          console.log('发现上传响应中已包含完整的分析结果，直接使用')
          checkResult.value = uploadResponse.data.data.choices[0].message.content || ''
          return true
        } else {
          console.error('无法从响应中提取文本内容:', uploadResponse.data)
          throw new Error('无法从上传的文件中提取文本')
        }
        
        console.log('成功提取文本，长度:', extractedText.length)
        if (extractedText.length > 100) {
          console.log('文本前100字符:', extractedText.substring(0, 100) + '...')
        } else {
          console.log('提取的文本:', extractedText)
        }
        
        console.log('第1步完成：成功上传数据集文件并读取内容')
        
        // 保存提取的文本、提示词和原始模型ID，供后续步骤使用
        this._extractedText = extractedText
        this._prompt = prompt
        this._originalModelId = modelId
        
        // 继续执行第2步和第3步
        await processExtractedText(extractedText, prompt, modelId)
        
        return true
      } catch (error) {
        console.error('文件上传失败:', error)
        
        // 记录所有可能的错误信息
        if (error.response) {
          console.error('错误响应状态:', error.response.status)
          console.error('错误响应数据:', error.response.data)
          
          const errorMsg = error.response.data?.message || error.response.data?.error || '请求参数错误'
          ElMessage.error(`数据集上传失败: ${errorMsg}`)
        } else {
          ElMessage.error(`数据集上传失败: ${error.message || '未知错误'}`)
        }
        
        return false
      } finally {
        isUploading.value = false
      }
    }
    
    // 处理提取的文本并调用流式API - 参考Proofreading.vue实现
    const processExtractedText = async (extractedText, prompt, modelId) => {
      console.log('========== 第2步：整理提示词 ==========')
      // 构建完整提示词（包含文件内容）
      const fullPrompt = `${prompt}\n\n${extractedText}`
      console.log('完整提示词长度:', fullPrompt.length)
      
      // 保存提示词供后续显示（可选）
      messages.value = [
        { role: "user", content: prompt }
      ]
      
      console.log('第2步完成：成功整理完整提示词')
      
      // 第3步：调用流式API获取结果
      console.log('========== 第3步：调用流式API获取结果 ==========')
      checkResult.value = ''
      isStreaming.value = true
      
      // 流式API使用原始模型ID
      console.log('流式请求使用原始模型ID:', modelId)
      
      // 流式API路径
      const streamApiUrl = '/api/v1/v1/deepseek_volcano/chat'
      console.log('流式API路径:', streamApiUrl)
      
      try {
        // 构建API请求参数
        const requestParams = {
          model: modelId, // 使用原始模型ID
          messages: [{ role: 'user', content: fullPrompt }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        }
        
        // 记录API请求详情
        console.log('流式请求参数:', {
          model: requestParams.model,
          stream: requestParams.stream,
          temperature: requestParams.temperature,
          max_tokens: requestParams.max_tokens,
          messages_length: requestParams.messages[0].content.length
        })
        
        // 发送流式请求
        const response = await fetch(streamApiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestParams)
        })
        
        console.log('流式响应状态:', response.status)
        
        if (!response.ok) {
          const errorText = await response.text()
          console.error('流式请求错误响应:', errorText)
          throw new Error(`流式请求失败: ${response.status}`)
        }
        
        // 处理流式响应
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''
        
        // 读取流数据
        console.log('开始读取流数据...')
        while (true) {
          const { done, value } = await reader.read()
          
          if (done) {
            console.log('流式响应完成')
            break
          }
          
          // 解码二进制数据
          const decoded = decoder.decode(value, { stream: true })
          buffer += decoded
          
          // 处理收到的数据
          const lines = buffer.split('\n\n')
          buffer = lines.pop() || ''
          
          for (const line of lines) {
            if (line.trim() === '') continue
            if (line.startsWith('data: ')) {
              const data = line.slice(6)
              if (data === '[DONE]') {
                console.log('收到结束标志')
                continue
              }
              
              try {
                const parsed = JSON.parse(data)
                
                // 处理错误消息
                if (parsed.error) {
                  console.error("API错误:", parsed.error)
                  throw new Error(parsed.error.message || '分析失败')
                }
                
                // 处理火山引擎返回的delta格式数据
                if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                  const delta = parsed.choices[0].delta
                  
                  // 处理内容增量
                  if (delta.content) {
                    // 累加收到的内容
                    checkResult.value += delta.content
                  }
                }
              } catch (e) {
                console.error('解析流式数据失败:', e)
              }
            }
          }
        }
        
        console.log('第3步完成，生成分析结果，总字数:', checkResult.value.length)
        ElMessage.success('数据分析完成！')
      } catch (error) {
        console.error('流式请求处理失败:', error)
        ElMessage.error(`分析失败: ${error.message || '未知错误'}`)
      } finally {
        isStreaming.value = false
      }
    }

    // 执行数据分析 - 更新为参考Proofreading.vue的实现
    const checkContract = async () => {
      // 验证是否有内容需要检查
      if (!selectedFile.value) {
        ElMessage.warning('请上传数据集文件')
        return
      }

      // 设置正在检查状态
      isChecking.value = true
      checkResult.value = ''

      // 显示加载指示器，直接使用"正在生成分析报告"作为文本
      loadingText.value = '正在生成分析报告...'
      loadingInstance.value = ElLoading.service({
        lock: true,
        text: '正在生成分析报告...',
        background: 'rgba(255, 255, 255, 0.8)'
      })

      try {
        // 使用Proofreading.vue的方式直接上传文件并处理
        await uploadFile()
      } catch (error) {
        console.error('数据分析错误:', error)
        let errorMessage = '数据分析失败，请稍后重试'
        
        if (error.response) {
          // 服务器返回了状态码
          console.error('错误状态:', error.response.status)
          console.error('错误数据:', error.response.data)
          errorMessage = `数据分析失败: ${error.response.status} - ${error.response.data?.message || '未知错误'}`
        } else if (error.request) {
          // 请求发出但没有收到响应
          console.error('没有收到响应:', error.request)
          console.error('请求URL:', error.config?.url)
          console.error('请求方法:', error.config?.method)
          errorMessage = '服务器没有响应，请检查网络连接或后端服务状态'
        } else {
          errorMessage = error.message || '数据分析过程中发生未知错误'
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
      
      const filename = `数据分析报告_${new Date().toLocaleDateString().replace(/\//g, '-')}.md`
      const blob = new Blob([checkResult.value], { type: 'text/markdown' })
      const link = document.createElement('a')
      
      link.href = URL.createObjectURL(blob)
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      ElMessage.success('报告下载成功')
    }

    // 显示提示
    const showTips = () => {
      showTipsModal.value = true
    }

    // 重置表单
    const resetForm = () => {
      selectedFile.value = null
      analysisOption.value = 'data_quality'
      checkResult.value = ''
      fileId.value = ''
      isUploading.value = false
      uploadProgress.value = 0
      isStreaming.value = false
      extraPrompt.value = ''
      
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
      isUploading,
      uploadProgress,
      isStreaming,
      clearSelectedFile,
      triggerFileUpload,
      handleFileUpload,
      checkContract,
      resetForm,
      copyText,
      downloadResult,
      showTips,
      extraPrompt,
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
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.file-upload-btn {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  color: #333;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.file-upload-btn:hover {
  background-color: #e0e0e0;
}

.file-upload-hint {
  color: #888;
  font-size: 13px;
}

.file-upload-selected {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  font-size: 14px;
}

.file-clear-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 2px;
  font-size: 16px;
  line-height: 1;
}

.file-clear-btn:hover {
  color: #666;
}

.file-upload-progress {
  margin-top: 8px;
  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #409eff;
  transition: width 0.2s;
}

.progress-text {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  display: block;
}

.streaming-indicator {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
}

.dot-typing {
  position: relative;
  display: inline-block;
  width: 4px;
  height: 4px;
  background-color: #666;
  border-radius: 50%;
  animation: dot-typing 1.5s infinite linear;
}

.dot-typing::before,
.dot-typing::after {
  content: '';
  position: absolute;
  top: 0;
  display: inline-block;
  width: 4px;
  height: 4px;
  background-color: #666;
  border-radius: 50%;
}

.dot-typing::before {
  left: -8px;
  animation: dot-typing 1.5s infinite linear;
  animation-delay: 0s;
}

.dot-typing::after {
  left: 8px;
  animation: dot-typing 1.5s infinite linear;
  animation-delay: 0.5s;
}

@keyframes dot-typing {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.5); opacity: 0.5; }
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