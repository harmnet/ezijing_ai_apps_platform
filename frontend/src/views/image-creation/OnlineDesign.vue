<template>
  <div class="chuangkit-container">
    <div id="ckt-design-page"></div>
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>正在加载创可贴设计工具...</p>
      <div v-if="debugInfo" class="debug-info">
        <pre>{{ debugInfo }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import CktDesign from '@chuangkit/chuangkit-design'
import md5 from 'blueimp-md5'
import { useStore } from 'vuex'
import axios from 'axios'

const props = defineProps({ kindId: { type: Number, default: 447 }, modelValue: { type: String, default: "" } })
const modelValue = ref(props.modelValue)
const emit = defineEmits(["close", "save", "update:modelValue"])
// 监听props中的modelValue变化，更新本地的modelValue
watch(() => props.modelValue, (newVal) => {
  modelValue.value = newVal
})

// 监听本地的modelValue变化，通过emit更新父组件的值
watch(modelValue, (newVal) => {
  emit("update:modelValue", newVal)
})
const isLoading = ref(true)
const debugInfo = ref('')

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
  
  // 记录签名前的原始字符串
  console.log('签名前的字符串:', signPlaintext);
  
  // 进行MD5加密并转大写
  const finalSign = md5(signPlaintext).toUpperCase();
  console.log('最终生成的签名:', finalSign);
  
  return finalSign
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
  // 记录输入参数
  console.log('签名输入参数:', {
    appId,
    expireTime,
    userFlag,
    appSecret
  });
  
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
      modelValue.value = uploadedURL
    }
    emit('save', modelValue.value)
  }
  if ([1, 2, 3].includes(result.kind)) {
    emit('close')
  }
}

let cktInstance
function openDesignPage() {
  isLoading.value = true
  
  console.log('=========== 开始生成签名 ===========');
  const appId = '54d9adec77d0402794018d166110f3dd'
  const appSecret = '08097010E0EF4B85EE2B8CE438328249'
  // 从当前store获取用户信息，如果没有则使用默认值
  const userFlag = store.state.user?.id || 'default_user'
  const expireTime = Date.now()
  const sign = buildVersion2Sign(appId, expireTime, userFlag, appSecret)
  console.log('=========== 签名生成完成 ===========');
  console.log('生成的签名结果:', sign);
  
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
  
  // 输出完整参数到控制台和页面
  console.log('完整初始化参数:', JSON.stringify(params, null, 2))
  debugInfo.value = JSON.stringify(params, null, 2)
  
  // 检查容器元素是否存在
  const container = document.getElementById('ckt-design-page')
  console.log('容器元素:', {
    exists: !!container,
    id: container?.id,
    dimensions: container ? `${container.offsetWidth}x${container.offsetHeight}` : 'unknown'
  })
    
  // 检查CktDesign库是否正确加载
  console.log('CktDesign库状态:', {
    loaded: !!CktDesign,
    methods: Object.keys(CktDesign)
  })

  try {
    console.log('创建CktDesign实例...')
    cktInstance = new CktDesign(params)
    console.log('调用open方法打开编辑器...')
    cktInstance.open()
    console.log('创可贴实例创建成功:', cktInstance)
    debugInfo.value += '\n\n创建成功'
    isLoading.value = false
  } catch (error) {
    console.error('创可贴初始化失败:', error)
    debugInfo.value += '\n\n创建失败: ' + error.message
    // 保持加载状态以显示调试信息
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

// 检查 CktDesign 库是否存在
console.log('组件初始化阶段 CktDesign:', {
  exists: typeof CktDesign !== 'undefined',
  methods: typeof CktDesign !== 'undefined' ? Object.keys(CktDesign) : []
})

onMounted(() => {
  console.log('组件已挂载，准备打开创可贴设计页面')
  
  // 确保DOM渲染完成后初始化编辑器
  setTimeout(() => {
    openDesignPage()
  }, 300)
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

.debug-info {
  margin-top: 20px;
  max-width: 80%;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 5px;
  font-family: monospace;
  font-size: 12px;
  white-space: pre-wrap;
  word-break: break-all;
  text-align: left;
  max-height: 50vh;
  overflow-y: auto;
  border: 1px solid #ddd;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style> 
