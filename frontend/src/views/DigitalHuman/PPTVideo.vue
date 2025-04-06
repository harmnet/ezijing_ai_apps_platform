<template>
  <div class="digital-human-ppt-container">
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <h2>数字人PPT讲解视频生成</h2>
        </div>
      </template>
      
      <el-form :model="formData" label-width="120px" :rules="rules" ref="formRef">
        <!-- PPT文件上传 -->
        <el-form-item label="PPT文件" prop="pptFile">
          <el-upload
            class="upload-box"
            drag
            action="#"
            :http-request="uploadFile"
            :show-file-list="true"
            :limit="1"
            :on-exceed="handleExceed"
            :on-change="handleFileChange"
            :auto-upload="false"
            :file-list="fileList"
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
        </el-form-item>

        <!-- 讲解文本 -->
        <el-form-item label="讲解文本" prop="textScript">
          <el-input
            v-model="formData.textScript"
            type="textarea"
            :rows="4"
            placeholder="输入讲解文本，如不填写将使用PPT中的备注内容"
          />
        </el-form-item>

        <!-- 视频标题 -->
        <el-form-item label="视频标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入视频标题" />
        </el-form-item>

        <!-- 数字人选择 -->
        <el-form-item label="数字人形象" prop="virtualHumanId">
          <el-select v-model="formData.virtualHumanId" placeholder="请选择数字人形象" @change="handleHumanChange">
            <el-option
              v-for="item in digitalHumans"
              :key="item.virtualHumanId"
              :label="item.name"
              :value="item.virtualHumanId"
            />
          </el-select>
        </el-form-item>

        <!-- 姿势选择 -->
        <el-form-item label="数字人姿势" prop="virtualHumanPostureId">
          <el-select v-model="formData.virtualHumanPostureId" placeholder="请选择数字人姿势">
            <el-option
              v-for="item in postures"
              :key="item.postureId"
              :label="item.name"
              :value="item.postureId"
            />
          </el-select>
        </el-form-item>

        <!-- 分辨率选择 -->
        <el-form-item label="视频分辨率" prop="resolution">
          <el-select v-model="formData.resolution" placeholder="请选择视频分辨率">
            <el-option
              v-for="item in resolutions"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>

        <!-- 字幕设置 -->
        <el-form-item label="显示字幕">
          <el-switch v-model="formData.showCaption" />
        </el-form-item>

        <!-- 转换类型 -->
        <el-form-item label="PPT转换类型">
          <el-radio-group v-model="formData.convertType">
            <el-radio label="VIDEO">保留PPT动画效果</el-radio>
            <el-radio label="IMG">仅保留PPT内容</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">生成讲解视频</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 生成结果展示 -->
      <div v-if="taskId" class="result-container">
        <el-divider>生成结果</el-divider>
        
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
        />
        
        <div v-if="taskStatus === 'completed'" class="video-preview">
          <video v-if="videoUrl" controls :src="videoUrl" class="preview-video"></video>
          <div class="video-actions">
            <el-button type="primary" @click="previewVideo" :disabled="!videoUrl">
              <el-icon><video-play /></el-icon> 查看视频
            </el-button>
            <el-button type="success" @click="downloadVideo" :disabled="!videoUrl">
              <el-icon><download /></el-icon> 下载视频
            </el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled, Download, VideoPlay } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'DigitalHumanPPTVideo',
  components: {
    UploadFilled,
    Download,
    VideoPlay
  },
  setup() {
    // 表单数据
    const formData = reactive({
      pptFile: null,
      textScript: '',
      title: 'PPT讲解视频',
      virtualHumanId: '',
      virtualHumanPostureId: '',
      resolution: '720p',
      showCaption: true,
      convertType: 'VIDEO'
    })

    // 表单验证规则
    const rules = {
      title: [
        { required: true, message: '请输入视频标题', trigger: 'blur' }
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

    // 获取数字人列表
    const getDigitalHumans = async () => {
      try {
        const response = await axios.get('/api/v1/digital_human/ppt/humans')
        if (response.data.code === 0 && response.data.data) {
          digitalHumans.value = response.data.data
          
          // 设置默认选择第一个数字人
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
          resolutions.value = response.data.data
          
          // 设置默认选择720p
          if (resolutions.value.includes('720p')) {
            formData.resolution = '720p'
          } else if (resolutions.value.length > 0) {
            formData.resolution = resolutions.value[0]
          }
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

    // 处理文件选择
    const handleFileChange = (file) => {
      if (file.status === 'ready') {
        formData.pptFile = file.raw
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
            taskId.value = response.data.data.taskId
            taskStatus.value = response.data.data.status
            
            ElMessage.success('任务创建成功，正在生成视频...')
            
            // 开始定时查询任务状态
            startPollingTaskStatus()
          } else {
            ElMessage.error(response.data.message || '任务创建失败')
          }
        } catch (error) {
          console.error('提交表单失败:', error)
          ElMessage.error('提交表单失败: ' + (error.response?.data?.message || error.message || '未知错误'))
        } finally {
          loading.value = false
        }
      })
    }

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
            } else if (taskStatus.value === 'failed') {
              errorMessage.value = response.data.data.error?.message || '生成失败，请重试'
              progressPercentage.value = 0
              stopPollingTaskStatus()
              ElMessage.error('视频生成失败: ' + errorMessage.value)
            } else if (taskStatus.value === 'processing') {
              progressPercentage.value = 60
            } else if (taskStatus.value === 'pending') {
              progressPercentage.value = 30
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

    // 组件挂载时
    onMounted(() => {
      // 获取初始数据
      getDigitalHumans()
      getResolutions()
    })

    // 组件销毁前
    onBeforeUnmount(() => {
      // 停止轮询
      stopPollingTaskStatus()
    })

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
      handleHumanChange,
      handleFileChange,
      handleExceed,
      uploadFile,
      submitForm,
      resetForm,
      previewVideo,
      downloadVideo
    }
  }
}
</script>

<style scoped>
.digital-human-ppt-container {
  padding: 20px;
}

.main-card {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-box {
  width: 100%;
}

.result-container {
  margin-top: 30px;
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
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.video-actions {
  margin-top: 15px;
  display: flex;
  gap: 15px;
}

:deep(.el-progress-bar__inner) {
  transition: width 0.6s ease;
}
</style>