<template>
  <div class="digital-human-video-params">
    <div class="params-header">
      <h3 class="params-title">视频参数</h3>
    </div>
    
    <div class="params-form">
      <div class="form-item">
        <label>视频格式</label>
        <el-select v-model="formattedParams.format" placeholder="请选择视频格式">
          <el-option v-for="item in formatOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </div>
      
      <div class="form-item">
        <label>视频分辨率</label>
        <el-select v-model="formattedParams.resolution" placeholder="请选择视频分辨率">
          <el-option v-for="item in resolutionOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </div>
      
      <div class="form-item">
        <label>背景颜色</label>
        <el-color-picker v-model="formattedParams.backgroundColor" show-alpha />
      </div>
      
      <div class="form-item">
        <label>背景图片</label>
        <el-upload
          class="background-uploader"
          action="#"
          :http-request="uploadBackgroundImage"
          :show-file-list="false"
          :before-upload="beforeBackgroundUpload"
        >
          <img v-if="backgroundImageUrl" :src="backgroundImageUrl" class="background-preview" />
          <el-icon v-else class="uploader-icon"><Plus /></el-icon>
        </el-upload>
        <el-button v-if="backgroundImageUrl" size="small" type="danger" @click="removeBackgroundImage">移除图片</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  videoParams: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:videoParams'])

// 本地状态
const backgroundImageUrl = ref('')

// 格式化后的参数，便于表单处理
const formattedParams = reactive({
  format: 'mp4',
  resolution: '1920x1080',
  backgroundColor: 'rgba(0, 0, 0, 0)',
  backgroundImage: null
})

// 从父组件接收的参数初始化本地状态
watch(() => props.videoParams, (newParams) => {
  if (newParams) {
    formattedParams.format = newParams.format || 'mp4'
    formattedParams.resolution = newParams.resolution || '1920x1080'
    formattedParams.backgroundColor = newParams.backgroundColor || 'rgba(0, 0, 0, 0)'
    
    if (newParams.backgroundImage) {
      formattedParams.backgroundImage = newParams.backgroundImage
      backgroundImageUrl.value = newParams.backgroundImage.url || ''
    }
  }
}, { immediate: true, deep: true })

// 监听本地状态变化，更新父组件
watch(formattedParams, (newParams) => {
  emit('update:videoParams', {
    format: newParams.format,
    resolution: newParams.resolution,
    backgroundColor: newParams.backgroundColor,
    backgroundImage: newParams.backgroundImage
  })
}, { deep: true })

// 选项数据
const formatOptions = [
  { value: 'mp4', label: 'MP4' },
  { value: 'webm', label: 'WebM' },
  { value: 'mov', label: 'MOV' }
]

const resolutionOptions = [
  { value: '1920x1080', label: '1920x1080 (全高清)' },
  { value: '1280x720', label: '1280x720 (高清)' },
  { value: '854x480', label: '854x480 (标清)' }
]

// 上传背景图片前的校验
const beforeBackgroundUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!')
    return false
  }
  return true
}

// 上传背景图片
const uploadBackgroundImage = (options) => {
  const file = options.file
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = () => {
    backgroundImageUrl.value = reader.result
    formattedParams.backgroundImage = {
      file: file,
      url: reader.result,
      name: file.name
    }
  }
}

// 移除背景图片
const removeBackgroundImage = () => {
  backgroundImageUrl.value = ''
  formattedParams.backgroundImage = null
}
</script>

<style scoped>
.digital-human-video-params {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 20px;
}

.params-header {
  margin-bottom: 20px;
}

.params-title {
  font-size: 18px;
  color: #333;
  margin: 0;
}

.params-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-item {
  display: flex;
  flex-direction: column;
}

.form-item label {
  margin-bottom: 8px;
  font-weight: 500;
}

.background-uploader {
  width: 200px;
  height: 120px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.background-uploader:hover {
  border-color: #409EFF;
}

.uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 28px;
  height: 28px;
}

.background-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style> 