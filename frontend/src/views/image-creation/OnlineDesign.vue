<template>
  <div class="chuangkit-container">
    <div id="ckt-design-page"></div>
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>正在加载创可贴设计工具...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import CktDesign from '@chuangkit/chuangkit-design'
import md5 from 'blueimp-md5'
import { useStore } from 'vuex'
import axios from 'axios'

const props = defineProps({ kindId: { type: Number, default: 447 } })
const model = defineModel()
const emit = defineEmits(['close', 'save'])
const isLoading = ref(true)

const store = useStore()

/**
 * 简易实现的文件上传函数
 * @param {string} url 文件URL
 * @returns {Promise<string>} 上传后的URL
 */
const uploadFileByUrl = async (url) => {
  try {
    console.log('正在上传文件:', url)
    // 这里简化处理，直接返回原URL
    // 实际项目中，应该发送请求到服务器进行处理
    return url
  } catch (error) {
    console.error('文件上传失败:', error)
    return url
  }
}

/**
 * 构建签名
 * @param obj 参数对象，对象中的所有属性全部参与签名的生成
 * @returns {string} 签名
 */
const buildSign = (obj) => {
  const signParameterArray = []
  for (const key in obj) {
    signParameterArray.push(`${key}=${obj[key]}`)
  }

  const signPlaintext = signParameterArray.sort().join('&')
  return md5(signPlaintext).toUpperCase()
}

/**
 * 构建2.0版本签名
 * @param appId 第三方企业id
 * @param expireTime 时间戳，取当前时间即可
 * @param userFlag 用户标记
 * @param appSecret 企业密钥
 * @returns {string} 签名
 */
const buildVersion2Sign = (appId, expireTime, userFlag, appSecret) => {
  const signParameterObj = {
    app_id: appId,
    expire_time: expireTime,
    user_flag: userFlag,
    app_secret: appSecret,
  }

  return buildSign(signParameterObj)
}

window.chuangkitComplete = async (result) => {
  console.log(result)
  if (!result.cktMessage) {
    return
  }
  if (result.kind == 2) {
    for (const url of result['source-urls']) {
      const uploadedURL = await uploadFileByUrl(url)
      model.value = uploadedURL
    }
    emit('save', model.value)
  }
  if ([1, 2, 3].includes(result.kind)) {
    emit('close')
  }
}

let cktInstance
function openDesignPage() {
  isLoading.value = true
  const appId = '54d9adec77d0402794018d166110f3dd'
  const appSecret = '08097010E0EF4B85EE2B8CE438328249'
  // 从当前store获取用户信息，如果没有则使用默认值
  const userFlag = store.state.user?.id || 'default_user'
  const expireTime = Date.now()
  const sign = buildVersion2Sign(appId, expireTime, userFlag, appSecret)
  const params = {
    app_id: appId,
    expire_time: expireTime,
    user_flag: userFlag,
    device_type: 1,
    kind_id: props.kindId,
    version: '2.0',
    sign: sign,
    enable_authorize: '1',
    taxpayer_name: 'chuangkit',
    taxpayer_phone: '13820659475',
    taxpayer_number: '91120116636067462H',
  }

  try {
    cktInstance = new CktDesign(params)
    cktInstance.open()
    console.log('创可贴实例创建成功:', cktInstance)
    isLoading.value = false
  } catch (error) {
    console.error('创可贴初始化失败:', error)
    isLoading.value = false
  }
}

function closeDesignPage() {
  if (cktInstance) {
    try {
      cktInstance.close()
      console.log('创可贴设计页面已关闭')
    } catch (error) {
      console.error('关闭创可贴设计页面失败:', error)
    }
  }
}

onMounted(() => {
  console.log('组件已挂载，准备打开创可贴设计页面')
  openDesignPage()
})

onUnmounted(() => {
  console.log('组件将卸载，关闭创可贴设计页面')
  closeDesignPage()
})
</script>

<style scoped>
.chuangkit-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

#ckt-design-page {
  width: 100%;
  height: 100%;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  border-top-color: #ba003f;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style> 