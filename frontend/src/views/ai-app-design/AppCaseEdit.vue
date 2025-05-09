<template>
  <div class="text-creation-page app-case-edit">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <div class="page-nav">
        <h2>编辑AI应用案例</h2>
      </div>
      <div class="page-actions">
        <button class="btn btn-primary btn-compact" @click="saveCase">
          <i class="fa fa-check icon-left"></i>保存
        </button>
        <button class="btn btn-secondary btn-compact" @click="goBack">
          <i class="fa fa-arrow-left icon-left"></i>返回
        </button>
      </div>
    </div>

    <!-- 编辑表单 -->
    <div class="section-header">
      <div class="section-title">
        <i class="el-icon-edit"></i>基本信息
      </div>
    </div>
    
    <div class="section-content edit-form-container">
      <div class="form-row">
        <div class="form-group" style="width: 100%;">
          <label class="required">案例名称</label>
          <div style="display: flex; align-items: center; gap: 10px; width: 100%;">
            <input type="text" class="form-control" placeholder="请输入案例名称" v-model="caseForm.name" style="flex: 1;">
            <button 
              class="btn btn-primary" 
              @click="optimizeName" 
              :disabled="optimizationLoading"
              style="flex: 0 0 auto; display: inline-block; padding: 0 12px; max-width: none; width: auto; margin: 0; height: 40px; line-height: 40px;"
            >
              <i class="fa" :class="optimizationLoading ? 'fa-spinner fa-spin' : 'fa-magic'"></i>
              {{ optimizationLoading ? '处理中...' : '一键AI优化' }}
            </button>
          </div>
          <div class="error-message" v-if="formErrors.name">{{ formErrors.name }}</div>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label class="required">类型</label>
          <select class="form-control" v-model="caseForm.case_type">
            <option value="">请选择类型</option>
            <option value="experience">场景体验型</option>
            <option value="problem-solving">解决问题型</option>
          </select>
          <div class="error-message" v-if="formErrors.case_type">{{ formErrors.case_type }}</div>
        </div>

        <div class="form-group">
          <label class="required">所在行业</label>
          <select class="form-control" v-model="caseForm.industry">
            <option value="">请选择行业</option>
            <option value="education">教育</option>
            <option value="healthcare">医疗</option>
            <option value="finance">金融</option>
            <option value="technology">科技</option>
            <option value="manufacturing">制造业</option>
          </select>
          <div class="error-message" v-if="formErrors.industry">{{ formErrors.industry }}</div>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label class="required">学时</label>
          <input type="number" class="form-control" placeholder="请输入学时" v-model="caseForm.study_hours" min="0.5" step="0.5">
          <div class="error-message" v-if="formErrors.study_hours">{{ formErrors.study_hours }}</div>
        </div>
        
        <div class="form-group" style="width: 100%;">
          <label class="required">主要标签</label>
          <div style="display: flex; align-items: center; gap: 10px; width: 100%;">
            <input type="text" class="form-control" placeholder="请输入主要标签，多个标签用逗号分隔" v-model="caseForm.tags" style="flex: 1;">
            <button 
              class="btn btn-primary" 
              @click="optimizeTags" 
              :disabled="optimizationLoading"
              style="flex: 0 0 auto; display: inline-block; padding: 0 12px; max-width: none; width: auto; margin: 0; height: 40px; line-height: 40px;"
            >
              <i class="fa" :class="optimizationLoading ? 'fa-spinner fa-spin' : 'fa-magic'"></i>
              {{ optimizationLoading ? '处理中...' : '一键AI优化' }}
            </button>
          </div>
          <div class="error-message" v-if="formErrors.tags">{{ formErrors.tags }}</div>
        </div>
      </div>
      
      <!-- 标签预览 -->
      <div class="tags-preview" v-if="caseForm.tags">
        <span class="tag" v-for="tag in previewTags" :key="tag">{{ tag }}</span>
      </div>
      
      <!-- 案例封面上传 -->
      <div class="form-row">
        <div class="form-group">
          <label>案例封面</label>
          <div class="cover-upload-container">
            <div class="cover-preview" v-if="coverPreview">
              <img :src="coverPreview" alt="案例封面预览">
              <button class="cover-remove-btn" @click="removeCoverImage">
                <i class="fa fa-trash icon-left"></i>
              </button>
            </div>
            <div class="cover-upload" v-else>
              <input type="file" id="cover-upload" accept="image/*" @change="handleCoverUpload" class="file-input">
              <label for="cover-upload" class="cover-upload-button">
                <i class="fa fa-upload icon-left"></i>
                <span>上传封面图片</span>
              </label>
            </div>
          </div>
          <div class="upload-tip">建议上传16:9比例的图片，大小不超过2MB</div>
        </div>
      </div>
    </div>
    
    <!-- 辅助设定 -->
    <div class="section-header">
      <div class="section-title">
        <i class="el-icon-setting"></i>辅助设定
      </div>
    </div>
    
    <div class="section-content edit-form-container">
      <div class="form-row">
        <div class="form-group">
          <label>选择AI大模型</label>
          <select class="form-control" v-model="caseForm.aiModel">
            <option value="">请选择AI大模型</option>
            <option value="deepseek-v3-vol">DeepSeek-V3（火山引擎）</option>
            <option value="deepseek-r1-vol">DeepSeek-R1（火山引擎）</option>
            <option value="doupo">豆包大模型</option>
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>上传辅助文件</label>
          <div class="file-upload-container">
            <input type="file" id="file-upload" accept=".docx,.doc,.pdf" @change="handleFileUpload" class="file-input">
            <label for="file-upload" class="file-upload-button">
              <i class="fa fa-upload icon-left"></i>
              选择文件
            </label>
            <span class="file-name">{{ fileName || '未选择文件' }}</span>
          </div>
          <div class="upload-tip">支持Word和PDF文件</div>
        </div>
      </div>
      
      <!-- 已上传文件列表 -->
      <div class="uploaded-files" v-if="uploadedFiles.length > 0">
        <div class="uploaded-file" v-for="(file, index) in uploadedFiles" :key="index">
          <span class="file-icon">
            <i :class="file.type === 'pdf' ? 'fa fa-file-pdf' : 'fa fa-file-word'"></i>
          </span>
          <span class="file-info">{{ file.name }}</span>
          <button class="btn-compact-sm btn-danger" @click="removeFile(index)">
            <i class="fa fa-trash icon-left"></i>
          </button>
        </div>
      </div>
    </div>
    
    <!-- AI设计案例提示词工程 -->
    <div class="section-header">
      <div class="section-title">
        <i class="el-icon-chat-line-square"></i>AI设计案例提示词工程
      </div>
    </div>
    
    <div class="section-content edit-form-container">
      <!-- 案例背景 -->
      <div class="prompt-section">
        <div class="prompt-header">
          <h4>案例背景</h4>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" name="backgroundSource" value="file" v-model="promptSources.background">
              <span>来自于辅助文件</span>
            </label>
            <label class="radio-label">
              <input type="radio" name="backgroundSource" value="custom" v-model="promptSources.background">
              <span>自定义</span>
            </label>
          </div>
        </div>
        <div class="prompt-content" v-if="promptSources.background === 'custom'">
          <textarea 
            class="form-control" 
            rows="8" 
            placeholder="请输入案例背景信息..." 
            v-model="promptContents.background"
          ></textarea>
        </div>
        <div class="prompt-content file-content" v-else>
          <p class="file-placeholder" v-if="!uploadedFiles.length">请先在辅助设定中上传文件</p>
          <p class="file-info" v-else>系统将从上传的辅助文件中提取案例背景信息</p>
        </div>
      </div>
      
      <!-- 案例角色 -->
      <div class="prompt-section">
        <div class="prompt-header">
          <h4>案例角色</h4>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" name="rolesSource" value="file" v-model="promptSources.roles">
              <span>来自于辅助文件</span>
            </label>
            <label class="radio-label">
              <input type="radio" name="rolesSource" value="custom" v-model="promptSources.roles">
              <span>自定义</span>
            </label>
          </div>
        </div>
        <div class="prompt-content" v-if="promptSources.roles === 'custom'">
          <textarea 
            class="form-control" 
            rows="8" 
            placeholder="请输入案例角色信息..." 
            v-model="promptContents.roles"
          ></textarea>
        </div>
        <div class="prompt-content file-content" v-else>
          <p class="file-placeholder" v-if="!uploadedFiles.length">请先在辅助设定中上传文件</p>
          <p class="file-info" v-else>系统将从上传的辅助文件中提取案例角色信息</p>
        </div>
      </div>
      
      <!-- 案例目标 -->
      <div class="prompt-section">
        <div class="prompt-header">
          <h4>案例目标</h4>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" name="goalsSource" value="file" v-model="promptSources.goals">
              <span>来自于辅助文件</span>
            </label>
            <label class="radio-label">
              <input type="radio" name="goalsSource" value="custom" v-model="promptSources.goals">
              <span>自定义</span>
            </label>
          </div>
        </div>
        <div class="prompt-content" v-if="promptSources.goals === 'custom'">
          <textarea 
            class="form-control" 
            rows="8" 
            placeholder="请输入案例目标信息..." 
            v-model="promptContents.goals"
          ></textarea>
        </div>
        <div class="prompt-content file-content" v-else>
          <p class="file-placeholder" v-if="!uploadedFiles.length">请先在辅助设定中上传文件</p>
          <p class="file-info" v-else>系统将从上传的辅助文件中提取案例目标信息</p>
        </div>
      </div>
      
      <!-- 案例流程 -->
      <div class="prompt-section">
        <div class="prompt-header">
          <h4>案例流程</h4>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" name="processSource" value="file" v-model="promptSources.process">
              <span>来自于辅助文件</span>
            </label>
            <label class="radio-label">
              <input type="radio" name="processSource" value="custom" v-model="promptSources.process">
              <span>自定义</span>
            </label>
          </div>
        </div>
        <div class="prompt-content" v-if="promptSources.process === 'custom'">
          <textarea 
            class="form-control" 
            rows="8" 
            placeholder="请输入案例流程信息..." 
            v-model="promptContents.process"
          ></textarea>
        </div>
        <div class="prompt-content file-content" v-else>
          <p class="file-placeholder" v-if="!uploadedFiles.length">请先在辅助设定中上传文件</p>
          <p class="file-info" v-else>系统将从上传的辅助文件中提取案例流程信息</p>
        </div>
      </div>
      
      <!-- 生成提示词按钮 -->
      <div class="prompt-actions">
        <button class="btn btn-primary wide-btn" @click="generatePrompt">
          <i class="fa fa-magic icon-left"></i>生成提示词
        </button>
      </div>
      
      <!-- 提示词预览和编辑 -->
      <div class="generated-prompt" v-if="generatedPrompt">
        <div class="prompt-header">
          <h4>生成的提示词</h4>
          <div class="prompt-controls">
            <button class="btn btn-secondary btn-sm" @click="regeneratePrompt">
              <i class="fa fa-refresh icon-left"></i>重新生成
            </button>
            <button class="btn btn-primary btn-sm" @click="copyPromptToClipboard">
              <i class="fa fa-copy icon-left"></i>复制提示词
            </button>
          </div>
        </div>
        <div class="prompt-editor">
          <textarea 
            class="form-control" 
            rows="24" 
            v-model="generatedPrompt"
            placeholder="点击生成提示词按钮生成AI设计提示词..."
          ></textarea>
        </div>
        
        <!-- 一键创建案例按钮 -->
        <div class="create-case-action">
          <button class="btn btn-primary btn-lg wide-btn" @click="createCase" :disabled="isCreating">
            <i class="fa fa-magic icon-left"></i>一键创建案例
          </button>
        </div>
      </div>
      
      <!-- 案例创建进度 -->
      <div class="case-creation-progress" v-if="creationSteps.length > 0">
        <div class="progress-header">
          <h4>案例创建进度</h4>
          <div class="progress-bar-container">
            <div class="progress-bar" :style="{ width: creationProgress + '%' }"></div>
          </div>
          <div class="progress-percentage">{{ creationProgress }}%</div>
        </div>
        
        <div class="creation-steps">
          <div 
            v-for="(step, index) in creationSteps" 
            :key="index" 
            class="creation-step"
            :class="{
              'step-current': index === currentStepIndex,
              'step-completed': index < currentStepIndex
            }"
          >
            <div class="step-indicator">
              <i class="fa fa-spinner fa-spin" v-if="index === currentStepIndex"></i>
              <i class="fa fa-check" v-else-if="index < currentStepIndex"></i>
              <span class="step-number" v-else>{{ index + 1 }}</span>
            </div>
            <div class="step-content">
              <div class="step-name">{{ step.name }}</div>
              <div class="step-description">{{ step.description }}</div>
            </div>
          </div>
        </div>
        
        <!-- 创建完成后的操作按钮 -->
        <div class="creation-complete-actions" v-if="creationComplete">
          <button class="btn btn-lg btn-primary action-btn" @click="viewCreatedCase">
            <i class="fas fa-eye"></i>查看创建的案例
          </button>
          <button class="btn btn-lg btn-primary action-btn" @click="resetCreation">
            <i class="fas fa-sync-alt"></i>重新创建
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'AppCaseEdit',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 编辑表单
    const caseForm = reactive({
      id: '',
      name: '',
      case_type: '',
      industry: '',
      study_hours: '',
      tags: '',
      aiModel: '',
      cover_url: '',
      updated_by: '当前用户' // 实际应用中应获取当前登录用户
    })
    
    // 表单错误信息
    const formErrors = reactive({
      name: '',
      case_type: '',
      industry: '',
      study_hours: '',
      tags: '',
      cover_url: ''
    })
    
    // 加载状态
    const loading = ref(false)
    const saveLoading = ref(false)
    
    // 是否是编辑模式
    const isEditMode = computed(() => !!route.params.id)
    
    // 表单标题
    const formTitle = computed(() => isEditMode.value ? '编辑AI应用案例' : '新建AI应用案例')
    
    // 案例创建相关
    const isCreating = ref(false)
    const creationComplete = ref(false)
    const currentStepIndex = ref(-1)
    const creationProgress = ref(0)
    
    // 创建步骤定义
    const creationSteps = ref([])
    
    // 初始化创建步骤
    const initCreationSteps = () => {
      creationSteps.value = [
        {
          name: '更新案例基本信息',
          description: '正在更新案例名称、类型、所在行业等基本信息...'
        },
        {
          name: '更新案例背景信息',
          description: '根据提示词生成并更新案例背景信息...'
        },
        {
          name: '更新案例角色信息',
          description: '根据提示词生成并更新案例中的角色信息...'
        },
        {
          name: '更新案例目标信息',
          description: '根据提示词生成并更新案例的学习目标...'
        },
        {
          name: '更新案例流程信息',
          description: '根据提示词生成并更新案例的执行流程...'
        },
        {
          name: '创建案例背景的试题',
          description: '根据案例背景生成相关的背景知识测试题...'
        },
        {
          name: '创建流程理论知识',
          description: '根据案例流程创建每一个流程的理论知识...'
        },
        {
          name: '创建流程AI实操',
          description: '根据案例流程创建每一个流程的AI实操指导...'
        },
        {
          name: '创建流程测试题',
          description: '根据案例流程创建每一个流程的测试题...'
        }
      ]
    }
    
    // 一键创建案例
    const createCase = () => {
      if (!generatedPrompt.value) {
        alert('请先生成提示词')
        return
      }
      
      // 初始化创建步骤
      initCreationSteps()
      isCreating.value = true
      creationComplete.value = false
      currentStepIndex.value = 0
      creationProgress.value = 0
      
      // 模拟创建过程
      simulateCreation()
    }
    
    // 模拟创建过程
    const simulateCreation = () => {
      const totalSteps = creationSteps.value.length
      let currentStep = 0
      
      const processStep = () => {
        if (currentStep >= totalSteps) {
          // 创建完成
          isCreating.value = false
          creationComplete.value = true
          creationProgress.value = 100
          return
        }
        
        // 更新当前步骤
        currentStepIndex.value = currentStep
        
        // 更新进度
        creationProgress.value = Math.round(((currentStep + 1) / totalSteps) * 100)
        
        // 模拟步骤处理时间（随机1-3秒）
        const processingTime = Math.floor(Math.random() * 2000) + 1000
        
        setTimeout(() => {
          // 进入下一步
          currentStep++
          processStep()
        }, processingTime)
      }
      
      // 开始处理
      processStep()
    }
    
    // 文件上传相关
    const fileName = ref('')
    const uploadedFiles = ref([])
    
    // 案例封面相关
    const coverPreview = ref('')
    
    // 处理封面上传
    const handleCoverUpload = async (event) => {
      const file = event.target.files[0]
      if (file) {
        // 检查文件类型
        if (!file.type.match('image.*')) {
          alert('请上传图片文件')
          return
        }
        
        // 检查文件大小 (2MB限制)
        if (file.size > 2 * 1024 * 1024) {
          alert('图片大小不能超过2MB')
          return
        }
        
        // 创建本地预览
        const reader = new FileReader()
        reader.onload = (e) => {
          coverPreview.value = e.target.result
        }
        reader.readAsDataURL(file)
        
        // 上传到服务器
        const saveLoading = ref(true)
        try {
          const formData = new FormData()
          formData.append('file', file)
          
          const response = await axios.post('/api/v1/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          
          if (response.data && response.data.url) {
            // 设置OSS URL到表单
            caseForm.cover_url = response.data.url
            console.log('图片上传成功：', response.data.url)
          } else {
            alert('图片上传失败，请重试')
          }
        } catch (error) {
          console.error('图片上传错误：', error)
          alert('图片上传出错，请重试')
        } finally {
          saveLoading.value = false
        }
      }
    }
    
    // 移除封面图片
    const removeCoverImage = () => {
      caseForm.cover_url = ''
      coverPreview.value = ''
    }
    
    // AI优化功能
    const optimizationLoading = ref(false)
    
    // AI设计案例提示词工程
    const promptSources = reactive({
      background: 'file',
      roles: 'file',
      goals: 'file',
      process: 'file'
    })
    
    const promptContents = reactive({
      background: '',
      roles: '',
      goals: '',
      process: ''
    })
    
    const generatedPrompt = ref('')
    
    // 处理文件上传
    const handleFileUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        fileName.value = file.name
        const fileType = file.name.split('.').pop().toLowerCase()
        
        // 添加到已上传文件列表
        uploadedFiles.value.push({
          name: file.name,
          type: fileType === 'pdf' ? 'pdf' : 'word',
          size: (file.size / 1024 / 1024).toFixed(2) + 'MB', // 转换为MB
          file: file
        })
        
        // 重置文件输入，允许重复上传同一文件
        event.target.value = ''
      }
    }
    
    // 移除文件
    const removeFile = (index) => {
      uploadedFiles.value.splice(index, 1)
      if (uploadedFiles.value.length === 0) {
        fileName.value = ''
      }
    }
    
    // 优化案例名称
    const optimizeName = async () => {
      // 检查必要的行业和类型信息
      if (!caseForm.industry || !caseForm.case_type) {
        alert('请先选择行业和类型')
        return
      }
      
      // 保存原来的名称用于恢复和参考
      const originalName = caseForm.name
      
      // 不再清空名称，而是保留用于AI参考
      
      optimizationLoading.value = true
      
      try {
        // 获取行业和类型信息，用于构建提示词
        const industry = caseForm.industry ? getIndustryName(caseForm.industry) : '通用'
        const type = caseForm.case_type ? getTypeName(caseForm.case_type) : '应用'
        
        // 构建提示词
        const prompt = `请基于现有的名称"${originalName || '（无）'}"，帮我优化生成一个${industry}行业的${type}类型AI应用案例的名称。

要求：
1. 名称应当体现案例所在的行业特点：${industry}
2. 名称应当体现案例类型特点：${type}
3. 名称可以包含"应用案例"或者"行业综合案例"等体现出案例的字样
4. 名称应当简洁明了，突出重点
5. 名称前可添加行业和应用类型前缀

请直接返回生成的名称，不要添加任何解释或额外内容。`
        
        // 用户消息
        const userMessage = { role: 'user', content: prompt }
        
        // 请求参数
        const requestData = {
          model: 'deepseek-v3', // 使用火山引擎V3模型
          messages: [userMessage],
          stream: false,
          temperature: 0.7,
          max_tokens: 200
        }
        
        // 发送请求到DeepSeek Volcano API
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData)
        })
        
        if (!response.ok) {
          throw new Error(`请求失败: ${response.status}`)
        }
        
        // 解析响应
        const data = await response.json()
        
        // 处理API返回的结果
        if (data.status === 'success' && data.data) {
          // 提取AI生成的内容
          const optimizedName = data.data.choices && data.data.choices[0] && data.data.choices[0].message
            ? data.data.choices[0].message.content.trim()
            : '';
          
          if (optimizedName) {
            // 更新表单中的案例名称
            caseForm.name = optimizedName;
          } else {
            throw new Error('API返回数据中未找到生成的内容');
          }
        } else {
          throw new Error('API返回数据格式不正确');
        }
      } catch (error) {
        console.error('名称优化出错:', error)
        alert(`名称优化失败: ${error.message || '未知错误'}`)
      } finally {
        optimizationLoading.value = false
      }
    }
    
    // 优化标签
    const optimizeTags = async () => {
      // 检查必要的信息
      if (!caseForm.name || !caseForm.industry || !caseForm.case_type) {
        alert('请先填写案例名称、行业和类型')
        return
      }
      
      // 保存原来的标签用于参考
      const originalTags = caseForm.tags
      
      // 不再清空标签，保留用于AI参考
      // caseForm.tags = ''
      
      optimizationLoading.value = true
      
      try {
        const industry = caseForm.industry ? getIndustryName(caseForm.industry) : '通用'
        const type = caseForm.case_type ? getTypeName(caseForm.case_type) : '应用'
        
        // 构建提示词
        const prompt = `请基于现有的标签"${originalTags || '（无）'}"，为以下AI应用案例优化生成5-8个标签：
- 案例名称：${caseForm.name}
- 所在行业：${industry}
- 案例类型：${type}

要求：
1. 生成5-8个有代表性的标签
2. 确保包含行业相关标签（${industry}）
3. 确保包含与AI技术相关的标签
4. 确保包含与案例类型相关的标签（${type}）
5. 标签应当简洁，通常为2-4个字
6. 标签之间用半角逗号分隔

请直接返回标签列表，不要添加任何解释或额外内容，格式如"标签1, 标签2, 标签3"。`
        
        // 用户消息
        const userMessage = { role: 'user', content: prompt }
        
        // 请求参数
        const requestData = {
          model: 'deepseek-v3', // 使用火山引擎V3模型
          messages: [userMessage],
          stream: false,
          temperature: 0.7,
          max_tokens: 200
        }
        
        // 发送请求到DeepSeek Volcano API
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData)
        })
        
        if (!response.ok) {
          throw new Error(`请求失败: ${response.status}`)
        }
        
        // 解析响应
        const data = await response.json()
        
        // 处理API返回的结果
        if (data.status === 'success' && data.data) {
          // 提取AI生成的内容
          const optimizedTags = data.data.choices && data.data.choices[0] && data.data.choices[0].message
            ? data.data.choices[0].message.content.trim()
            : '';
          
          if (optimizedTags) {
            // 更新表单中的标签
            caseForm.tags = optimizedTags;
          } else {
            throw new Error('API返回数据中未找到生成的内容');
          }
        } else {
          throw new Error('API返回数据格式不正确');
        }
      } catch (error) {
        console.error('标签优化出错:', error)
        alert(`标签优化失败: ${error.message || '未知错误'}`)
      } finally {
        optimizationLoading.value = false
      }
    }
    
    // 预览标签
    const previewTags = computed(() => {
      if (!caseForm.tags) return []
      return caseForm.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
    })
    
    // 行业映射
    const industryMap = {
      'education': '教育',
      'healthcare': '医疗',
      'finance': '金融',
      'technology': '科技',
      'manufacturing': '制造业'
    }

    // 类型映射
    const typeMap = {
      'experience': '场景体验型',
      'problem-solving': '解决问题型'
    }

    // 获取类型名称
    const getTypeName = (code) => {
      return typeMap[code] || code
    }

    // 获取行业名称
    const getIndustryName = (code) => {
      return industryMap[code] || code
    }
    
    // 生成提示词
    const generatePrompt = () => {
      // 检查所需的基本信息是否填写
      if (!caseForm.name || !caseForm.case_type || !caseForm.industry) {
        alert('请先填写基本信息中的案例名称、类型和所在行业')
        return
      }
      
      // 获取行业和类型的中文名称
      const industryName = getIndustryName(caseForm.industry)
      const typeName = getTypeName(caseForm.case_type)
      
      // 获取提示词内容
      const backgroundContent = promptSources.background === 'file' 
        ? '(来自辅助文件的案例背景)' 
        : promptContents.background.trim()
      
      const rolesContent = promptSources.roles === 'file'
        ? '(来自辅助文件的案例角色)' 
        : promptContents.roles.trim()
      
      const goalsContent = promptSources.goals === 'file'
        ? '(来自辅助文件的案例目标)' 
        : promptContents.goals.trim()
      
      const processContent = promptSources.process === 'file'
        ? '(来自辅助文件的案例流程)' 
        : promptContents.process.trim()
      
      // 生成案例提示词
      const prompt = `请你帮我设计一个AI应用案例，具体信息如下：

案例名称：${caseForm.name}
案例类型：${typeName}
所在行业：${industryName}
学时：${caseForm.study_hours || '未指定'}
主要标签：${previewTags.value.join('、') || '未指定'}

案例背景：
${backgroundContent || '请根据案例名称和行业特点设计合理的背景信息。'}

案例角色：
${rolesContent || '请设计合适的角色，包括使用AI应用的主要角色和辅助角色。'}

案例目标：
${goalsContent || '请根据案例类型和行业特点，设计明确的学习或应用目标。'}

案例流程：
${processContent || '请设计案例的主要流程步骤，使其合理、有序、符合实际应用场景。'}

要求：
1. 案例内容应当真实可信，符合${industryName}行业的实际情况
2. 案例应当充分体现${typeName}的特点
3. 设计的AI应用案例应包含明确的应用场景、用户交互流程和预期效果
4. 案例设计应考虑学时为${caseForm.study_hours || '未指定'}学时的学习量
5. 结合提供的信息，设计出完整、具体、有教育意义的AI应用案例

请提供完整的案例设计方案，包括详细的背景、角色、目标、流程和预期效果。`

      // 设置生成的提示词
      generatedPrompt.value = prompt
      
      // 重置创建相关状态
      resetCreation()
    }
    
    // 重新生成提示词
    const regeneratePrompt = () => {
      generatePrompt()
    }
    
    // 复制提示词到剪贴板
    const copyPromptToClipboard = () => {
      if (!generatedPrompt.value) {
        alert('请先生成提示词')
        return
      }
      
      // 使用 Clipboard API 复制文本
      navigator.clipboard.writeText(generatedPrompt.value)
        .then(() => {
          alert('提示词已复制到剪贴板')
        })
        .catch(err => {
          console.error('复制失败:', err)
          alert('复制失败，请手动复制')
        })
    }
    
    // 表单验证
    const validateForm = () => {
      let isValid = true
      
      // 重置所有错误信息
      Object.keys(formErrors).forEach(key => {
        formErrors[key] = ''
      })
      
      // 验证案例名称
      if (!caseForm.name.trim()) {
        formErrors.name = '请输入案例名称'
        isValid = false
      }
      
      // 验证类型
      if (!caseForm.case_type) {
        formErrors.case_type = '请选择类型'
        isValid = false
      }
      
      // 验证所在行业
      if (!caseForm.industry) {
        formErrors.industry = '请选择行业'
        isValid = false
      }
      
      // 验证学时
      if (!caseForm.study_hours) {
        formErrors.study_hours = '请输入学时'
        isValid = false
      } else if (parseFloat(caseForm.study_hours) < 0.5) {
        formErrors.study_hours = '学时必须不小于0.5'
        isValid = false
      }
      
      // 验证主要标签
      if (!caseForm.tags.trim()) {
        formErrors.tags = '请输入主要标签'
        isValid = false
      }
      
      return isValid
    }
    
    // 加载案例数据
    const loadCaseData = async () => {
      const caseId = route.params.id
      if (!caseId) return // 新建模式，不需要加载数据
      
      loading.value = true
      try {
        // 调用API获取案例详情
        const response = await axios.get(`/api/v1/app-cases/${caseId}`)
        
        if (response.data.status === 'success') {
          // 获取案例数据
          const caseData = response.data.data
          
          // 填充表单数据
          caseForm.id = caseData.id
          caseForm.name = caseData.name
          caseForm.case_type = caseData.case_type
          caseForm.industry = caseData.industry
          caseForm.study_hours = caseData.study_hours
          caseForm.tags = caseData.tags || ''
          caseForm.cover_url = caseData.cover_url || ''
          caseForm.updated_by = '当前用户' // 实际应用中应获取当前登录用户
          
          // 设置封面预览
          if (caseData.cover_url) {
            coverPreview.value = caseData.cover_url
          }
        } else {
          console.error('获取案例详情失败:', response.data.message)
          alert(`获取案例详情失败: ${response.data.message}`)
        }
      } catch (error) {
        console.error('加载案例数据出错:', error)
        alert('加载案例数据失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
    
    // 保存案例
    const saveCase = async () => {
      if (!validateForm()) return
      
      saveLoading.value = true
      try {
        // 准备请求数据
        const caseData = {
          name: caseForm.name,
          case_type: caseForm.case_type,
          industry: caseForm.industry,
          study_hours: parseFloat(caseForm.study_hours),
          tags: caseForm.tags,
          cover_url: caseForm.cover_url,
          updated_by: caseForm.updated_by
        }
        
        let response
        if (isEditMode.value) {
          // 更新案例
          response = await axios.put(`/api/v1/app-cases/${caseForm.id}`, caseData)
        } else {
          // 创建新案例
          response = await axios.post('/api/v1/app-cases', caseData)
        }
        
        if (response.data.status === 'success') {
          // 保存成功
          alert(`${isEditMode.value ? '更新' : '创建'}案例成功`)
          
          // 返回列表页
          goBack()
        } else {
          // 保存失败
          alert(`${isEditMode.value ? '更新' : '创建'}案例失败: ${response.data.message}`)
        }
      } catch (error) {
        console.error(`${isEditMode.value ? '更新' : '创建'}案例出错:`, error)
        alert(`${isEditMode.value ? '更新' : '创建'}案例失败，请稍后重试`)
      } finally {
        saveLoading.value = false
      }
    }
    
    // 查看创建的案例
    const viewCreatedCase = () => {
      router.push('/ai-app-design/list')
    }
    
    // 重新创建
    const resetCreation = () => {
      creationSteps.value = []
      creationComplete.value = false
      currentStepIndex.value = -1
      creationProgress.value = 0
    }
    
    // 返回列表页
    const goBack = () => {
      router.push('/ai-app-design/list')
    }
    
    // 页面加载时获取案例数据
    onMounted(() => {
      loadCaseData()
    })
    
    return {
      caseForm,
      formErrors,
      loading,
      saveLoading,
      isEditMode,
      formTitle,
      optimizationLoading,
      previewTags,
      fileName,
      uploadedFiles,
      coverPreview,
      handleFileUpload,
      handleCoverUpload,
      removeCoverImage,
      removeFile,
      optimizeName,
      optimizeTags,
      getTypeName,
      getIndustryName,
      promptSources,
      promptContents,
      generatedPrompt,
      generatePrompt,
      regeneratePrompt,
      copyPromptToClipboard,
      isCreating,
      creationComplete,
      creationSteps,
      currentStepIndex,
      creationProgress,
      createCase,
      viewCreatedCase,
      resetCreation,
      saveCase,
      goBack
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/text-creation-common.css';
</style> 