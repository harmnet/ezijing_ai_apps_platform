<template>
  <div class="digital-human-ppt-container">
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <h2><el-icon class="header-icon"><VideoCamera /></el-icon> AI数字人微课制作</h2>
        </div>
      </template>
      
      <el-form :model="formData" label-width="120px" :rules="rules" ref="formRef">
        <!-- PPT文件上传 -->
        <el-form-item label="PPT文件" prop="pptFile">
          <div class="ppt-upload-section">
            <el-upload
              v-if="!formData.pptFile"
              class="upload-box"
              drag
              action="#"
              :http-request="uploadFile"
              :show-file-list="false"
              :limit="1"
              :on-exceed="handleExceed"
              :on-change="handleFileChange"
              :auto-upload="false"
              accept=".ppt,.pptx,.pdf"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                拖拽文件到此处或 <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持PPT、PPTX、PDF文件，大小不超过10MB
                </div>
              </template>
            </el-upload>
            
            <!-- 文件已上传时显示文件信息 -->
            <div v-if="formData.pptFile" class="ppt-file-info">
              <div class="file-info-header">
                <el-icon class="file-icon"><Document /></el-icon>
                <div class="file-name-wrapper">
                  <div class="file-name" :title="formData.pptFile.name">{{ formData.pptFile.name }}</div>
                  <div class="file-size">{{ formatFileSize(formData.pptFile.size) }}</div>
                </div>
                <div class="file-actions">
                  <el-button type="danger" text @click="removePptFile">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
              
              <el-progress 
                v-if="uploadProgress > 0 && uploadProgress < 100" 
                :percentage="uploadProgress" 
                :format="percentageFormat"
                class="upload-progress"
                :stroke-width="8"
                color="#C10D0C"
              />
              
              <div class="file-type-badge" :class="getFileTypeBadgeClass(formData.pptFile.name)">
                {{ getFileTypeText(formData.pptFile.name) }}
              </div>
            </div>
          </div>
        </el-form-item>

        <!-- 讲解文本 -->
        <el-form-item label="讲解文本" prop="textScript">
          <el-input
            v-model="formData.textScript"
            type="textarea"
            :rows="6"
            placeholder="输入讲解文本，如不填写将使用PPT中的备注内容"
          />
        </el-form-item>

        <!-- 视频标题 -->
        <el-form-item label="视频标题" prop="title">
          <el-input 
            v-model="formData.title" 
            placeholder="请输入视频标题"
            prefix-icon="Document"
          />
        </el-form-item>

        <!-- 数字人形象 -->
        <el-form-item label="数字人形象" prop="virtualHumanId">
          <div class="radio-option-wrapper">
            <el-radio-group v-model="formData.virtualHumanId" @change="handleHumanChange" class="human-radio-group">
              <label 
                v-for="item in digitalHumans" 
                :key="item.virtualHumanId" 
                class="custom-radio-label"
                :class="{'is-checked': formData.virtualHumanId === item.virtualHumanId}"
              >
                <el-radio :label="item.virtualHumanId" class="hidden-radio">{{ item.name }}</el-radio>
                <div class="custom-radio-content">
                  {{ item.name }}
                </div>
              </label>
              
              <!-- 添加不可选择的数字人形象 -->
              <label class="custom-radio-label disabled-radio">
                <div class="custom-radio-content disabled-content">
                  馨馨/女
                  <el-tag size="small" type="info" effect="plain">即将上线</el-tag>
                </div>
              </label>
              
              <label class="custom-radio-label disabled-radio">
                <div class="custom-radio-content disabled-content">
                  范宇/女
                  <el-tag size="small" type="info" effect="plain">即将上线</el-tag>
                </div>
              </label>
              
              <label class="custom-radio-label disabled-radio">
                <div class="custom-radio-content disabled-content">
                  博涵/男
                  <el-tag size="small" type="info" effect="plain">即将上线</el-tag>
                </div>
              </label>
              
              <label class="custom-radio-label disabled-radio">
                <div class="custom-radio-content disabled-content">
                  江峰/男
                  <el-tag size="small" type="info" effect="plain">即将上线</el-tag>
                </div>
              </label>
              
              <label class="custom-radio-label disabled-radio">
                <div class="custom-radio-content disabled-content">
                  定制形象
                  <el-tag size="small" type="info" effect="plain">敬请期待</el-tag>
                </div>
              </label>
            </el-radio-group>
          </div>
        </el-form-item>

        <!-- 姿势选择 -->
        <el-form-item label="数字人姿势" prop="virtualHumanPostureId">
          <div class="radio-option-wrapper">
            <el-radio-group v-model="formData.virtualHumanPostureId" class="posture-radio-group">
              <label 
                v-for="item in postures" 
                :key="item.postureId" 
                class="custom-radio-label"
                :class="{'is-checked': formData.virtualHumanPostureId === item.postureId}"
              >
                <el-radio :label="item.postureId" class="hidden-radio">{{ item.name }}</el-radio>
                <div class="custom-radio-content">
                  {{ item.name }}
                </div>
              </label>
            </el-radio-group>
          </div>
        </el-form-item>

        <!-- 分辨率选择 -->
        <el-form-item label="视频分辨率" prop="resolution">
          <div class="radio-option-wrapper">
            <el-radio-group v-model="formData.resolution" class="resolution-radio-group">
              <label 
                v-for="item in resolutions" 
                :key="item" 
                class="custom-radio-label"
                :class="{'is-checked': formData.resolution === item}"
              >
                <el-radio :label="item" class="hidden-radio">{{ item }}</el-radio>
                <div class="custom-radio-content">
                  {{ item }}
                </div>
              </label>
            </el-radio-group>
          </div>
        </el-form-item>

        <!-- 字幕设置 -->
        <el-form-item label="显示字幕">
          <el-switch 
            v-model="formData.showCaption"
            active-color="#ba003f"
          />
        </el-form-item>

        <!-- 转换类型 -->
        <el-form-item label="PPT转换类型">
          <div class="radio-option-wrapper">
            <el-radio-group v-model="formData.convertType" class="convert-radio-group">
              <label 
                class="custom-radio-label"
                :class="{'is-checked': formData.convertType === 'IMG'}"
              >
                <el-radio label="IMG" class="hidden-radio">仅保留PPT内容</el-radio>
                <div class="custom-radio-content">
                  仅保留PPT内容
                </div>
              </label>
              <label 
                class="custom-radio-label"
                :class="{'is-checked': formData.convertType === 'VIDEO'}"
              >
                <el-radio label="VIDEO" class="hidden-radio">保留PPT动画效果</el-radio>
                <div class="custom-radio-content">
                  保留PPT动画效果
                </div>
              </label>
            </el-radio-group>
          </div>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item class="action-buttons">
          <el-button 
            type="danger" 
            @click="submitForm" 
            :loading="loading"
            class="submit-button"
            size="large"
          >
            <el-icon><VideoCamera /></el-icon> 生成讲解视频
          </el-button>
          <el-button 
            @click="resetForm"
            class="reset-button"
            size="large"
          >
            <el-icon><Refresh /></el-icon> 重置
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 生成结果展示 -->
      <div v-if="taskId" class="result-container">
        <el-divider>
          <el-icon><Check /></el-icon> 生成结果
        </el-divider>
        
        <div class="task-info">
          <p>任务ID: <span class="task-id">{{ taskId }}</span>
            <el-button type="danger" size="small" @click="queryTaskStatus" :loading="queryLoading" class="refresh-btn">
              <el-icon><Refresh /></el-icon> 刷新状态
            </el-button>
          </p>
        </div>
        
        <!-- 添加PPT文件和讲解文本信息 -->
        <div class="ppt-info" v-if="currentTaskDetails && currentTaskDetails.pptUrl">
          <div class="ppt-details-card">
            <div class="ppt-details-header">
              <el-icon class="ppt-icon"><Document /></el-icon>
              <div class="ppt-info-title">PPT文件信息</div>
            </div>
            
            <div class="ppt-details-content">
              <div class="info-item">
                <div class="info-label">文件名:</div>
                <div class="info-content">
                  <span class="file-name-full">{{ getFileNameFromUrl(currentTaskDetails.pptUrl) }}</span>
                  <el-tag size="small" class="file-type-tag" 
                    :type="getFileTypeTagType(getFileExtension(currentTaskDetails.pptUrl))">
                    {{ getFileTypeText(getFileNameFromUrl(currentTaskDetails.pptUrl)) }}
                  </el-tag>
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-label">文件地址:</div>
                <div class="info-content">
                  <el-button type="primary" link @click="window.open(currentTaskDetails.pptUrl, '_blank')">
                    <el-icon><Document /></el-icon> 查看PPT文件
                  </el-button>
                  <el-button type="success" link @click="downloadPptFile(currentTaskDetails.pptUrl)">
                    <el-icon><Download /></el-icon> 下载文件
                  </el-button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="text-script-card" v-if="currentTaskDetails.textScript">
            <div class="text-script-header">
              <el-icon class="text-icon"><ChatLineRound /></el-icon>
              <div class="text-info-title">讲解文本</div>
            </div>
            
            <div class="text-script-content">
              {{ currentTaskDetails.textScript }}
            </div>
          </div>
        </div>
        
        <el-alert
          v-if="taskStatus === 'failed'"
          title="视频生成失败"
          type="error"
          :description="errorMessage"
          show-icon
        />
        
        <el-alert
          v-if="taskStatus === 'completed'"
          title="视频生成成功"
          type="success"
          description="PPT讲解视频已生成完成，可以点击下方按钮查看或下载"
          show-icon
        />
        
        <el-alert
          v-if="['creating', 'pending', 'processing'].includes(taskStatus)"
          title="视频生成中"
          type="info"
          description="PPT讲解视频正在生成中，请耐心等待"
          show-icon
        />
        
        <el-progress 
          v-if="['creating', 'pending', 'processing'].includes(taskStatus)"
          :percentage="progressPercentage"
          :indeterminate="true"
          status="active"
          :stroke-width="15"
          color="#ba003f"
        />
        
        <div v-if="taskStatus === 'completed'" class="video-preview">
          <video v-if="videoUrl" controls :src="videoUrl" class="preview-video"></video>
          <div class="video-actions">
            <el-button type="danger" @click="previewVideo" :disabled="!videoUrl">
              <el-icon><video-play /></el-icon> 查看视频
            </el-button>
            <el-button type="success" @click="downloadVideo" :disabled="!videoUrl">
              <el-icon><download /></el-icon> 下载视频
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 查询历史任务 -->
      <div class="history-query-container">
        <el-divider>
          <el-icon><History /></el-icon> 最近任务
        </el-divider>
        
        <div class="recent-tasks" v-if="recentTasks.length > 0">
          <div class="section-header">
            <h3>
              <el-icon><History /></el-icon> 最近任务
            </h3>
          </div>
          
          <el-table :data="recentTasks" style="width: 100%" size="small" stripe border>
            <el-table-column label="任务ID" prop="taskId" width="280" show-overflow-tooltip />
            <el-table-column label="标题" prop="title" width="120" />
            <el-table-column label="状态" width="100">
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
            <el-table-column label="创建时间" prop="createdAt" width="180" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button 
                  size="small" 
                  @click="previewTaskVideo(scope.row)"
                  :disabled="scope.row.status !== 'completed' || !scope.row.videoUrl"
                >
                  查看视频
                </el-button>
                <el-button 
                  size="small" 
                  type="info" 
                  @click="refreshTaskStatus(scope.row.taskId)"
                  :loading="refreshingTaskIds.has(scope.row.taskId)"
                >
                  <el-icon><Refresh /></el-icon> 刷新状态
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  UploadFilled, Download, VideoPlay, Refresh, Search, 
  VideoCamera, Check, History, List, Picture, 
  Document, Key, UserFilled, Delete, InfoFilled, ChatLineRound 
} from '@element-plus/icons-vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

export default {
  name: 'DigitalHumanPPTVideo',
  components: {
    UploadFilled,
    Download,
    VideoPlay,
    Refresh,
    Search,
    VideoCamera,
    Check,
    History,
    List,
    Picture,
    Document,
    Key,
    UserFilled,
    Delete,
    InfoFilled,
    ChatLineRound
  },
  setup() {
    const route = useRoute()
    
    // 从URL参数获取数字人ID和名称
    const humanIdFromUrl = route.query.humanId
    const humanNameFromUrl = route.query.humanName
    const virtualHumanIdFromUrl = route.query.virtualHumanId
    
    // 表单数据
    const formData = reactive({
      pptFile: null,
      textScript: '',
      title: 'PPT讲解视频',
      virtualHumanId: virtualHumanIdFromUrl || '',
      virtualHumanPostureId: '',
      resolution: '480p',
      showCaption: true,
      convertType: 'IMG'
    })

    // 表单验证规则
    const rules = {
      title: [
        { required: true, message: '请输入视频标题', trigger: 'blur' }
      ],
      pptFile: [
        { required: true, message: '请上传PPT文件', trigger: 'change' }
      ],
      textScript: [
        { required: true, message: '请输入讲解文本', trigger: 'blur' }
      ]
    }

    // 数据列表
    const digitalHumans = ref([])
    const postures = ref([])
    const resolutions = ref([])
    const fileList = ref([])
    const formRef = ref(null)

    // 状态管理
    const loading = ref(false)
    const taskId = ref('')
    const taskStatus = ref('')
    const videoUrl = ref('')
    const thumbnailUrl = ref('')
    const errorMessage = ref('')
    const progressPercentage = ref(0)
    let pollInterval = null

    // 添加新的响应式变量
    const queryLoading = ref(false)
    const historyTaskId = ref('')
    const recentTasks = ref([])
    const currentTaskDetails = ref(null)

    // 添加响应式变量
    const uploadProgress = ref(0)
    // 跟踪刷新状态的任务ID
    const refreshingTaskIds = ref(new Set())

    // 获取数字人列表
    const getDigitalHumans = async () => {
      try {
        const response = await axios.get('/api/v1/digital_human/ppt/humans')
        if (response.data.code === 0 && response.data.data) {
          digitalHumans.value = response.data.data
          
          // 判断是否有URL传入的数字人ID
          if (virtualHumanIdFromUrl) {
            // 直接使用URL传入的virtualHumanId
            formData.virtualHumanId = virtualHumanIdFromUrl
            getPostures(formData.virtualHumanId)
            
            // 添加提示信息
            ElMessage.success(`已自动选择数字人${humanNameFromUrl ? ': ' + humanNameFromUrl : ''}`)
            return
          } else if (humanIdFromUrl) {
            // 查找匹配的数字人ID
            const targetHuman = digitalHumans.value.find(human => human.id === humanIdFromUrl)
            if (targetHuman) {
              formData.virtualHumanId = targetHuman.virtualHumanId
              getPostures(formData.virtualHumanId)
              
              // 添加提示信息
              ElMessage.success(`已自动选择数字人: ${humanNameFromUrl || targetHuman.name}`)
              return
            }
          }
          
          // 如果没有匹配的数字人或没有提供ID，设置默认选择第一个数字人
          if (digitalHumans.value.length > 0) {
            formData.virtualHumanId = digitalHumans.value[0].virtualHumanId
            getPostures(formData.virtualHumanId)
          }
        }
      } catch (error) {
        console.error('获取数字人列表失败:', error)
        ElMessage.error('获取数字人列表失败')
      }
    }

    // 获取姿势列表
    const getPostures = async (humanId) => {
      if (!humanId) return
      
      try {
        const response = await axios.get(`/api/v1/digital_human/ppt/postures/${humanId}`)
        if (response.data.code === 0 && response.data.data) {
          postures.value = response.data.data
          
          // 设置默认选择第一个姿势
          if (postures.value.length > 0) {
            formData.virtualHumanPostureId = postures.value[0].postureId
          }
        }
      } catch (error) {
        console.error('获取姿势列表失败:', error)
        ElMessage.error('获取姿势列表失败')
      }
    }

    // 获取支持的分辨率
    const getResolutions = async () => {
      try {
        const response = await axios.get('/api/v1/digital_human/ppt/resolutions')
        if (response.data.code === 0 && response.data.data) {
          // 调整分辨率顺序为480p、720p、1080p
          const sortedResolutions = ['480p', '720p', '1080p'].filter(res => 
            response.data.data.includes(res)
          );
          
          // 添加其他可能的分辨率
          response.data.data.forEach(res => {
            if (!sortedResolutions.includes(res)) {
              sortedResolutions.push(res);
            }
          });
          
          resolutions.value = sortedResolutions;
          
          // 设置默认选择480p
          formData.resolution = '480p';
        }
      } catch (error) {
        console.error('获取支持的分辨率失败:', error)
        ElMessage.error('获取支持的分辨率失败')
      }
    }

    // 监听数字人选择变化
    const handleHumanChange = (humanId) => {
      formData.virtualHumanPostureId = '' // 清空姿势选择
      getPostures(humanId)
    }

    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]
    }

    // 百分比格式化
    const percentageFormat = (percentage) => {
      return percentage === 100 ? '上传完成' : `${percentage}%`
    }

    // 获取文件类型
    const getFileTypeText = (filename) => {
      const ext = filename.split('.').pop().toLowerCase()
      if (ext === 'ppt') return 'PPT'
      if (ext === 'pptx') return 'PPTX'
      if (ext === 'pdf') return 'PDF'
      return 'FILE'
    }

    // 获取文件类型样式
    const getFileTypeBadgeClass = (filename) => {
      const ext = filename.split('.').pop().toLowerCase()
      if (ext === 'ppt' || ext === 'pptx') return 'ppt-badge'
      if (ext === 'pdf') return 'pdf-badge'
      return 'file-badge'
    }

    // 删除PPT文件
    const removePptFile = () => {
      formData.pptFile = null
      fileList.value = []
      uploadProgress.value = 0
      // 通知表单验证更新
      if (formRef.value) {
        formRef.value.validateField('pptFile')
      }
    }

    // 模拟上传进度
    const simulateUploadProgress = () => {
      uploadProgress.value = 0
      const interval = setInterval(() => {
        if (uploadProgress.value < 95) {
          uploadProgress.value += 5
        } else {
          clearInterval(interval)
          uploadProgress.value = 100
        }
      }, 200)
    }

    // 处理文件选择
    const handleFileChange = (file) => {
      if (file.status === 'ready') {
        formData.pptFile = file.raw
        // 模拟上传进度
        simulateUploadProgress()
      }
    }

    // 处理超出文件数量限制
    const handleExceed = () => {
      ElMessage.warning('最多只能上传1个文件')
    }

    // 上传文件方法（自定义上传）
    const uploadFile = async (options) => {
      // 在提交表单时统一处理上传，这里不需要实现
      return true
    }

    // 提交表单
    const submitForm = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (!valid) return
        
        // 检查文件是否已选择
        if (!formData.pptFile) {
          ElMessage.error('请选择PPT文件')
          return
        }
        
        loading.value = true
        
        try {
          // 创建FormData对象用于文件上传
          const formDataObj = new FormData()
          formDataObj.append('ppt_file', formData.pptFile)
          formDataObj.append('text_script', formData.textScript || '')
          formDataObj.append('title', formData.title)
          formDataObj.append('virtual_human_id', formData.virtualHumanId)
          formDataObj.append('virtual_human_posture_id', formData.virtualHumanPostureId)
          formDataObj.append('resolution', formData.resolution)
          formDataObj.append('show_caption', formData.showCaption)
          formDataObj.append('convert_type', formData.convertType)
          
          // 发送请求
          const response = await axios.post('/api/v1/digital_human/ppt/generate', formDataObj, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          
          if (response.data.code === 0 && response.data.data) {
            // 获取任务ID
            const responseData = response.data.data;
            console.log('任务创建响应:', responseData); // 添加日志，便于调试
            
            // 确保使用正确的属性名来获取taskId
            taskId.value = responseData.task_id || responseData.taskId;
            taskStatus.value = responseData.status;
            
            ElMessage.success('任务创建成功，正在生成视频...');
            
            // 开始定时查询任务状态
            startPollingTaskStatus();
            
            // 保存任务记录到本地存储
            saveTaskToLocal({
              taskId: taskId.value,
              title: formData.title,
              status: taskStatus.value,
              createdAt: new Date().toLocaleString(),
              videoUrl: null,
              textScript: formData.textScript
            });
            
            // 立即更新历史记录，这样可以看到最新创建的任务
            await loadTaskHistory();
            
            // 从历史记录中查找当前任务的详细信息
            currentTaskDetails.value = recentTasks.value.find(task => task.taskId === taskId.value);
          } else {
            ElMessage.error(response.data.message || '任务创建失败');
          }
        } catch (error) {
          console.error('提交表单失败:', error);
          ElMessage.error('提交表单失败: ' + (error.response?.data?.message || error.message || '未知错误'));
        } finally {
          loading.value = false;
        }
      });
    };

    // 重置表单
    const resetForm = () => {
      if (formRef.value) {
        formRef.value.resetFields()
      }
      
      fileList.value = []
      formData.pptFile = null
      taskId.value = ''
      taskStatus.value = ''
      videoUrl.value = ''
      thumbnailUrl.value = ''
      errorMessage.value = ''
      progressPercentage.value = 0
      
      // 停止轮询
      stopPollingTaskStatus()
    }

    // 开始轮询任务状态
    const startPollingTaskStatus = () => {
      // 先停止已有的轮询
      stopPollingTaskStatus()
      
      // 每5秒查询一次任务状态
      pollInterval = setInterval(async () => {
        if (!taskId.value) {
          stopPollingTaskStatus()
          return
        }
        
        try {
          const response = await axios.get(`/api/v1/digital_human/ppt/task/${taskId.value}`)
          
          if (response.data.code === 0 && response.data.data) {
            taskStatus.value = response.data.data.status
            
            // 如果任务完成或失败，停止轮询
            if (taskStatus.value === 'completed') {
              videoUrl.value = response.data.data.video_url
              thumbnailUrl.value = response.data.data.thumbnail_url
              progressPercentage.value = 100
              stopPollingTaskStatus()
              ElMessage.success('视频生成成功')
              
              // 更新本地存储中的任务状态
              saveTaskToLocal({
                taskId: taskId.value,
                title: formData.title,
                status: taskStatus.value,
                createdAt: new Date().toLocaleString(),
                videoUrl: videoUrl.value
              })
            } else if (taskStatus.value === 'failed') {
              errorMessage.value = response.data.data.error?.message || '生成失败，请重试'
              progressPercentage.value = 0
              stopPollingTaskStatus()
              ElMessage.error('视频生成失败: ' + errorMessage.value)
              
              // 更新本地存储中的任务状态
              saveTaskToLocal({
                taskId: taskId.value,
                title: formData.title,
                status: taskStatus.value,
                createdAt: new Date().toLocaleString(),
                videoUrl: null
              })
            } else if (taskStatus.value === 'processing') {
              progressPercentage.value = 60
              
              // 更新本地存储中的任务状态
              saveTaskToLocal({
                taskId: taskId.value,
                title: formData.title,
                status: taskStatus.value,
                createdAt: new Date().toLocaleString(),
                videoUrl: null
              })
            } else if (taskStatus.value === 'pending') {
              progressPercentage.value = 30
              
              // 更新本地存储中的任务状态
              saveTaskToLocal({
                taskId: taskId.value,
                title: formData.title,
                status: taskStatus.value,
                createdAt: new Date().toLocaleString(),
                videoUrl: null
              })
            } else {
              progressPercentage.value = 10
            }
          }
        } catch (error) {
          console.error('查询任务状态失败:', error)
        }
      }, 5000)
    }

    // 停止轮询任务状态
    const stopPollingTaskStatus = () => {
      if (pollInterval) {
        clearInterval(pollInterval)
        pollInterval = null
      }
    }

    // 预览视频
    const previewVideo = () => {
      if (!videoUrl.value) return
      
      // 在新窗口打开视频URL
      window.open(videoUrl.value, '_blank')
    }

    // 下载视频
    const downloadVideo = () => {
      if (!videoUrl.value) return
      
      // 创建下载链接
      const link = document.createElement('a')
      link.href = videoUrl.value
      link.download = `${formData.title || 'PPT讲解视频'}.mp4`
      link.target = '_blank'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }

    // 查询任务状态
    const queryTaskStatus = async () => {
      queryLoading.value = true
      
      try {
        const response = await axios.get(`/api/v1/digital_human/ppt/task/${taskId.value}`)
        
        if (response.data.code === 0 && response.data.data) {
          ElMessage.success('任务查询成功')
          const responseData = response.data.data;
          taskStatus.value = responseData.status;
          
          // 如果任务完成，更新视频URL
          if (taskStatus.value === 'completed') {
            videoUrl.value = responseData.video_url;
            thumbnailUrl.value = responseData.thumbnail_url;
            progressPercentage.value = 100;
            ElMessage.success('视频已生成完成');
          } else if (taskStatus.value === 'failed') {
            errorMessage.value = responseData.error?.message || '生成失败，请重试';
            progressPercentage.value = 0;
            ElMessage.error('视频生成失败: ' + errorMessage.value);
          } else {
            ElMessage.info(`任务状态: ${getStatusText(taskStatus.value)}`);
          }
        } else {
          ElMessage.error(response.data.message || '任务查询失败')
        }
      } catch (error) {
        console.error('任务查询失败:', error)
        ElMessage.error('任务查询失败: ' + (error.response?.data?.message || error.message || '未知错误'))
      } finally {
        queryLoading.value = false
      }
    }

    // 查询历史任务
    const queryHistoryTask = async () => {
      if (!historyTaskId.value.trim()) {
        ElMessage.warning('请输入任务ID')
        return
      }
      
      loadTaskById(historyTaskId.value.trim())
    }

    // 加载任务历史记录
    const loadTaskHistory = async () => {
      try {
        // 从API获取历史记录
        const response = await axios.get('/api/v1/digital_human/ppt/history?limit=10')
        
        if (response.data.code === 0 && response.data.data) {
          // 转换API返回的历史记录为组件需要的格式
          recentTasks.value = response.data.data.tasks.map(task => ({
            taskId: task.task_id,
            title: task.title,
            status: task.status,
            createdAt: new Date(task.created_at).toLocaleString(),
            videoUrl: task.video_url,
            thumbnailUrl: task.thumbnail_url,
            pptUrl: task.ppt_url,
            textScript: task.text_script
          }))
        } else {
          console.error('加载历史记录失败:', response.data.message)
        }
      } catch (error) {
        console.error('加载历史记录失败:', error)
      }
    }

    // 根据ID加载任务
    const loadTaskById = async (id) => {
      queryLoading.value = true
      try {
        const response = await axios.get(`/api/v1/digital_human/ppt/task/${id}`)
        
        if (response.data.code === 0 && response.data.data) {
          // 更新任务信息
          taskId.value = id
          taskStatus.value = response.data.data.status
          
          // 从历史记录中查找当前任务的详细信息
          currentTaskDetails.value = recentTasks.value.find(task => task.taskId === id)
          
          // 如果任务完成，更新视频URL
          if (response.data.data.status === 'completed') {
            videoUrl.value = response.data.data.video_url
            thumbnailUrl.value = response.data.data.thumbnail_url
            progressPercentage.value = 100
          } else if (response.data.data.status === 'failed') {
            errorMessage.value = response.data.data.error?.message || '生成失败'
            progressPercentage.value = 0
          } else if (response.data.data.status === 'processing') {
            progressPercentage.value = 60
            startPollingTaskStatus() // 如果任务还在处理中，开始轮询
          } else if (response.data.data.status === 'pending') {
            progressPercentage.value = 30
            startPollingTaskStatus() // 如果任务还在处理中，开始轮询
          } else {
            progressPercentage.value = 10
            startPollingTaskStatus() // 如果任务还在处理中，开始轮询
          }
          
          ElMessage.success('成功加载任务信息')
          
          // 滚动到结果区域
          setTimeout(() => {
            document.querySelector('.result-container')?.scrollIntoView({ behavior: 'smooth' })
          }, 100)
        }
      } catch (error) {
        console.error('加载任务失败:', error)
        ElMessage.error('加载任务失败: ' + (error.response?.data?.message || error.message || '未知错误'))
      } finally {
        queryLoading.value = false
      }
    }
    
    // 查看历史任务视频
    const previewTaskVideo = (task) => {
      if (!task.videoUrl) return
      
      // 在新窗口打开视频URL
      window.open(task.videoUrl, '_blank')
    }
    
    // 刷新单个任务状态
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
          const taskIndex = recentTasks.value.findIndex(task => task.taskId === taskId)
          
          if (taskIndex !== -1) {
            const oldStatus = recentTasks.value[taskIndex].status
            const newStatus = updatedTask.status
            
            // 创建更新后的任务对象
            const updatedTaskObj = {
              ...recentTasks.value[taskIndex],
              status: newStatus,
              videoUrl: updatedTask.video_url,
              thumbnailUrl: updatedTask.thumbnail_url,
              pptUrl: updatedTask.ppt_url
            }
            
            // 更新任务列表中的任务
            recentTasks.value[taskIndex] = updatedTaskObj
            
            // 保存到本地存储
            saveTasksToLocalStorage()
            
            // 显示状态变化的提示
            if (oldStatus !== newStatus) {
              ElMessage.success(`任务状态已从"${getStatusText(oldStatus)}"变为"${getStatusText(newStatus)}"`)
              
              // 如果当前正在查看此任务，也更新当前任务的状态
              if (taskId === taskId.value) {
                taskStatus.value = newStatus
                if (newStatus === 'completed') {
                  videoUrl.value = updatedTask.video_url
                  thumbnailUrl.value = updatedTask.thumbnail_url
                  progressPercentage.value = 100
                  // 停止轮询
                  stopPollingTaskStatus()
                  ElMessage.success('视频生成成功')
                } else if (newStatus === 'failed') {
                  errorMessage.value = updatedTask.error?.message || '生成失败，请重试'
                  progressPercentage.value = 0
                  // 停止轮询
                  stopPollingTaskStatus()
                  ElMessage.error('视频生成失败: ' + errorMessage.value)
                }
              }
            } else {
              ElMessage.info(`任务状态未变化，仍为"${getStatusText(newStatus)}"`)
            }
          }
        } else {
          ElMessage.error('获取任务状态失败: ' + (response.data.message || '未知错误'))
        }
      } catch (error) {
        console.error('刷新任务状态失败:', error)
        ElMessage.error('刷新任务状态失败: ' + (error.response?.data?.message || error.message || '未知错误'))
      } finally {
        // 移除刷新标记
        refreshingTaskIds.value.delete(taskId)
      }
    }
    
    // 获取任务状态的显示文本
    const getStatusText = (status) => {
      const statusMap = {
        'creating': '创建中',
        'pending': '等待处理',
        'processing': '处理中',
        'completed': '已完成',
        'failed': '失败'
      }
      return statusMap[status] || status
    }
    
    // 获取任务状态的标签类型
    const getStatusType = (status) => {
      // 所有状态都使用'danger'（紫荆红色）
      return 'danger';
    }
    
    // 保存任务到本地存储
    const saveTaskToLocal = (task) => {
      try {
        // 获取现有的任务列表
        let tasks = JSON.parse(localStorage.getItem('pptVideoTasks') || '[]')
        
        // 添加新任务到列表顶部（如果已存在则更新）
        const existingIndex = tasks.findIndex(t => t.taskId === task.taskId)
        if (existingIndex >= 0) {
          tasks[existingIndex] = task
        } else {
          tasks.unshift(task)
        }
        
        // 只保留最近10个任务
        tasks = tasks.slice(0, 10)
        
        // 保存到localStorage
        localStorage.setItem('pptVideoTasks', JSON.stringify(tasks))
        
        // 更新最近任务列表
        loadRecentTasks()
      } catch (error) {
        console.error('保存任务到本地存储失败:', error)
      }
    }
    
    // 从本地存储加载最近任务
    const loadRecentTasks = () => {
      try {
        const tasks = JSON.parse(localStorage.getItem('pptVideoTasks') || '[]')
        recentTasks.value = tasks
      } catch (error) {
        console.error('从本地存储加载任务失败:', error)
        recentTasks.value = []
      }
    }

    // 组件挂载时
    onMounted(() => {
      // 获取初始数据
      getDigitalHumans()
      getResolutions()
      loadRecentTasks() // 加载最近任务
      
      // 如果URL中有taskId参数，则加载该任务
      const urlTaskId = new URLSearchParams(window.location.search).get('taskId')
      if (urlTaskId) {
        historyTaskId.value = urlTaskId
        queryHistoryTask()
      }
      
      // 从API加载历史记录
      loadTaskHistory()
      
      // 开始自动刷新任务状态
      startAutoRefreshAllTasks()
    })

    // 在beforeUnmount中清除所有定时器
    onBeforeUnmount(() => {
      // 停止轮询
      stopPollingTaskStatus()
      
      // 停止任务列表刷新
      stopAutoRefreshAllTasks()
    })
    
    // 定时刷新所有任务的定时器
    let refreshAllTasksInterval = null
    
    // 开始定时刷新所有任务状态
    const startAutoRefreshAllTasks = () => {
      // 先停止已有的定时器
      stopAutoRefreshAllTasks()
      
      // 每30秒刷新一次所有任务状态
      refreshAllTasksInterval = setInterval(async () => {
        try {
          // 调用历史记录API获取最新状态
          const response = await axios.get('/api/v1/digital_human/ppt/history?limit=10')
          
          if (response.data.code === 0 && response.data.data) {
            // 更新本地任务列表
            recentTasks.value = response.data.data.tasks.map(task => ({
              taskId: task.task_id,
              title: task.title,
              status: task.status,
              createdAt: new Date(task.created_at).toLocaleString(),
              videoUrl: task.video_url,
              thumbnailUrl: task.thumbnail_url,
              pptUrl: task.ppt_url,
              textScript: task.text_script
            }))
            
            // 如果当前正在查看的任务也在列表中，更新它的状态
            if (taskId.value) {
              const currentTask = response.data.data.tasks.find(task => task.task_id === taskId.value)
              if (currentTask) {
                taskStatus.value = currentTask.status
                
                // 如果任务完成，更新视频URL
                if (currentTask.status === 'completed') {
                  videoUrl.value = currentTask.video_url
                  thumbnailUrl.value = currentTask.thumbnail_url
                  progressPercentage.value = 100
                  
                  // 停止查询当前任务的轮询
                  stopPollingTaskStatus()
                } else if (currentTask.status === 'failed') {
                  errorMessage.value = '生成失败，请重试'
                  progressPercentage.value = 0
                  
                  // 停止查询当前任务的轮询
                  stopPollingTaskStatus()
                } else if (currentTask.status === 'processing') {
                  progressPercentage.value = 60
                } else if (currentTask.status === 'pending') {
                  progressPercentage.value = 30
                }
              }
            }
          }
        } catch (error) {
          console.error('自动刷新任务状态失败:', error)
        }
      }, 30000) // 30秒刷新一次
    }
    
    // 停止定时刷新所有任务状态
    const stopAutoRefreshAllTasks = () => {
      if (refreshAllTasksInterval) {
        clearInterval(refreshAllTasksInterval)
        refreshAllTasksInterval = null
      }
    }
    
    // 保存所有任务到本地存储
    const saveTasksToLocalStorage = () => {
      try {
        localStorage.setItem('pptVideoTasks', JSON.stringify(recentTasks.value.slice(0, 10)))
      } catch (error) {
        console.error('保存任务到本地存储失败:', error)
      }
    }

    // 手动刷新所有任务
    const refreshAllTasksNow = async () => {
      if (recentTasks.value.length === 0) {
        ElMessage.info('没有需要刷新的任务')
        return
      }
      
      ElMessage.info('正在刷新所有任务状态...')
      
      // 重新加载历史记录来刷新任务状态
      await loadTaskHistory()
      
      ElMessage.success('任务状态已更新')
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

    // 获取文件扩展名
    const getFileExtension = (filename) => {
      if (!filename) return ''
      try {
        const name = getFileNameFromUrl(filename)
        const parts = name.split('.')
        if (parts.length > 1) {
          return parts[parts.length - 1].toLowerCase()
        }
        return ''
      } catch (e) {
        return ''
      }
    }

    // 获取文件类型对应的Tag类型
    const getFileTypeTagType = (extension) => {
      if (extension === 'ppt' || extension === 'pptx') return 'danger'
      if (extension === 'pdf') return 'warning'
      return 'info'
    }

    // 下载PPT文件
    const downloadPptFile = (url) => {
      if (!url) return
      const link = document.createElement('a')
      link.href = url
      link.download = getFileNameFromUrl(url)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }

    return {
      formData,
      rules,
      digitalHumans,
      postures,
      resolutions,
      fileList,
      formRef,
      loading,
      taskId,
      taskStatus,
      videoUrl,
      thumbnailUrl,
      errorMessage,
      progressPercentage,
      queryLoading,
      historyTaskId,
      recentTasks,
      currentTaskDetails,
      uploadProgress,
      refreshingTaskIds,
      handleHumanChange,
      handleFileChange,
      handleExceed,
      uploadFile,
      submitForm,
      resetForm,
      previewVideo,
      downloadVideo,
      queryTaskStatus,
      queryHistoryTask,
      getStatusText,
      getStatusType,
      previewTaskVideo,
      refreshTaskStatus,
      refreshAllTasksNow,
      formatFileSize,
      percentageFormat,
      getFileTypeText,
      getFileTypeBadgeClass,
      removePptFile,
      simulateUploadProgress,
      getFileNameFromUrl,
      getFileExtension,
      getFileTypeTagType,
      downloadPptFile
    }
  }
}
</script>

<style scoped>
.digital-human-ppt-container {
  padding: 20px;
  background-color: #f9f9f9;
}

.main-card {
  max-width: 900px;
  margin: 0 auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #ba003f;
  padding-bottom: 10px;
}

.card-header h2 {
  color: #ba003f;
  display: flex;
  align-items: center;
  margin: 0;
}

.header-icon {
  margin-right: 8px;
  font-size: 24px;
}

.upload-box {
  width: 100%;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  transition: all 0.3s;
  max-height: 180px;
  overflow: hidden;
}

.upload-box:hover {
  border-color: #ba003f;
}

.result-container {
  margin-top: 30px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.video-preview {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview-video {
  width: 100%;
  max-width: 640px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-actions {
  margin-top: 15px;
  display: flex;
  gap: 15px;
}

:deep(.el-progress-bar__inner) {
  transition: width 0.6s ease;
}

.task-info {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  background-color: #f8f9fa;
  padding: 10px 15px;
  border-radius: 4px;
  border-left: 3px solid #ba003f;
}

.task-id {
  font-weight: bold;
  color: #ba003f;
  margin-left: 5px;
}

.refresh-btn {
  margin-left: 10px;
}

.history-query-container {
  margin-top: 30px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.recent-tasks {
  margin-top: 20px;
}

.recent-tasks h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #303133;
  border-left: 3px solid #ba003f;
  padding-left: 10px;
  display: flex;
  align-items: center;
}

.recent-tasks h3 .el-icon {
  margin-right: 5px;
  color: #ba003f;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

:deep(.el-table__row) {
  cursor: pointer;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-divider__text) {
  background-color: #f8f9fa;
  color: #ba003f;
  font-weight: bold;
  display: flex;
  align-items: center;
}

:deep(.el-divider__text .el-icon) {
  margin-right: 5px;
}

.radio-option-wrapper {
  width: 100%;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.human-radio-group,
.posture-radio-group,
.resolution-radio-group,
.convert-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 8px;
}

.custom-radio-label {
  position: relative;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  min-width: unset;
  margin-right: 0;
}

.custom-radio-label input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.custom-radio-content {
  width: auto;
  padding: 8px 16px;
  background: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 20px;
  font-size: 14px;
  color: #C10D0C;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  white-space: nowrap;
}

.custom-radio-label:hover .custom-radio-content {
  border-color: #C10D0C;
  box-shadow: 0 2px 8px rgba(193, 13, 12, 0.2);
}

.custom-radio-label.is-checked .custom-radio-content {
  background: #C10D0C;
  border-color: #C10D0C;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(193, 13, 12, 0.3);
}

.hidden-radio {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  overflow: hidden;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  gap: 20px;
}

.submit-button {
  background-color: #C10D0C;
  border-color: #C10D0C;
  padding: 15px 40px;
  font-weight: bold;
  font-size: 18px;
  min-width: 400px;
  height: 60px;
}

.reset-button {
  height: 60px;
  padding: 15px 30px;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #d4185b;
  border-color: #d4185b;
}

:deep(.el-radio__input.is-checked .el-radio__inner) {
  border-color: #C10D0C;
  background: #C10D0C;
}

:deep(.el-radio__input.is-checked + .el-radio__label) {
  color: #C10D0C;
}

:deep(.el-input-group__prepend .el-icon),
:deep(.el-input__prefix-inner .el-icon) {
  color: #ba003f;
}

:deep(.el-textarea__inner) {
  min-height: 120px !important;
}

:deep(.el-switch.is-checked .el-switch__core) {
  border-color: #C10D0C !important;
  background-color: #C10D0C !important;
}

/* 修复进度条颜色 */
.el-progress :deep(.el-progress-bar__inner) {
  background-color: #C10D0C !important;
}

/* 强化单选框选中状态样式 */
.el-radio-group :deep(.el-radio.is-checked) .human-radio-item,
.el-radio-group :deep(.el-radio.is-checked) .posture-radio-item,
.el-radio-group :deep(.el-radio.is-checked) .resolution-radio-item,
.el-radio-group :deep(.el-radio.is-checked) .convert-radio-item,
.el-radio-group :deep(.el-radio.is-checked) .human-option,
.el-radio-group :deep(.el-radio.is-checked) .posture-option,
.el-radio-group :deep(.el-radio.is-checked) .resolution-option,
.el-radio-group :deep(.el-radio.is-checked) .convert-option {
  /* 这些样式已被替换，可以删除 */
}

/* 禁用的单选框样式 */
.disabled-radio {
  cursor: not-allowed;
  opacity: 0.8;
}

.disabled-content {
  background: #f0f0f0;
  border-color: #dcdcdc;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 8px;
}

.disabled-radio:hover .disabled-content {
  border-color: #dcdcdc;
  box-shadow: none;
}

.ppt-info {
  margin: 15px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #C10D0C;
}

.info-item {
  margin-bottom: 10px;
  display: flex;
}

.info-label {
  font-weight: bold;
  min-width: 100px;
  color: #606266;
}

.info-content {
  flex: 1;
}

.text-content {
  padding: 10px;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #e6e6e6;
  max-height: 150px;
  overflow-y: auto;
  white-space: pre-wrap;
}

.ppt-upload-section {
  width: 100%;
}

.ppt-file-info {
  width: 100%;
  border: 2px solid #e6e6e6;
  border-radius: 8px;
  padding: 15px;
  position: relative;
  background-color: #f9f9f9;
  transition: all 0.3s;
}

.ppt-file-info:hover {
  border-color: #C10D0C;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.file-info-header {
  display: flex;
  align-items: center;
}

.file-icon {
  font-size: 32px;
  color: #C10D0C;
  margin-right: 15px;
}

.file-name-wrapper {
  flex: 1;
  overflow: hidden;
}

.file-name {
  font-weight: bold;
  font-size: 16px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  color: #606266;
  font-size: 14px;
  margin-top: 5px;
}

.file-actions {
  margin-left: 10px;
}

.upload-progress {
  margin-top: 15px;
}

.file-type-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.ppt-badge {
  background-color: #C10D0C;
}

.pdf-badge {
  background-color: #e74c3c;
}

.file-badge {
  background-color: #3498db;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
  border-left: 3px solid #C10D0C;
  padding-left: 10px;
  display: flex;
  align-items: center;
}

.section-header .el-icon {
  margin-right: 5px;
  color: #C10D0C;
}

.table-file-info {
  display: flex;
  align-items: center;
  gap: 5px;
}

.file-name-short {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: inline-block;
}

.tooltip-file-info {
  padding: 5px;
  max-width: 300px;
}

.tooltip-file-buttons {
  margin-top: 8px;
  display: flex;
  gap: 10px;
}

.no-file {
  color: #909399;
  font-style: italic;
}

.ppt-details-card, .text-script-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  margin-bottom: 15px;
  overflow: hidden;
  border: 1px solid #ebeef5;
}

.ppt-details-header, .text-script-header {
  background-color: #f5f7fa;
  padding: 12px 15px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
}

.ppt-icon, .text-icon {
  font-size: 18px;
  margin-right: 8px;
  color: #C10D0C;
}

.ppt-info-title, .text-info-title {
  font-weight: bold;
  color: #303133;
  font-size: 16px;
}

.ppt-details-content {
  padding: 15px;
}

.text-script-content {
  padding: 15px;
  white-space: pre-wrap;
  line-height: 1.5;
  max-height: 200px;
  overflow-y: auto;
  color: #606266;
  background-color: #f9f9f9;
  border-radius: 0 0 8px 8px;
}

.file-name-full {
  margin-right: 10px;
  word-break: break-all;
}

.file-type-tag {
  vertical-align: middle;
}
</style>