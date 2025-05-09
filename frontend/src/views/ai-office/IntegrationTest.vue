<template>
  <div class="integration-test-container">
    <div id="aippt-container" class="aippt-container" ref="aipptContainer"></div>
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <div class="loading-text">正在加载AIPPT...</div>
    </div>
    <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>
  </div>
</template>

<script>
import CryptoJS from 'crypto-js'

export default {
  name: 'IntegrationTest',
  data() {
    return {
      loading: true,
      errorMsg: '',
      config: {
        appkey: '673e95c065226',
        secret: '7bVcH15FeB1zTy08PN5n3YtmRxsVXjEv',
        editorModel: true
      }
    }
  },
  async mounted() {
    // 设置容器高度
    this.adjustHeight();
    window.addEventListener('resize', this.adjustHeight);
    
    this.initAipptAsync();
  },
  methods: {
    adjustHeight() {
      // 获取视窗高度并减去头部高度
      const viewHeight = window.innerHeight;
      const headerHeight = 60; // 预估的头部高度
      const containerHeight = viewHeight - headerHeight;
      if (this.$refs.aipptContainer) {
        this.$refs.aipptContainer.style.height = `${containerHeight}px`;
      }
    },
    
    getSavedCodeData() {
      const savedData = localStorage.getItem('aippt_code_data')
      return savedData ? JSON.parse(savedData) : null
    },
    
    saveCodeData(codeData) {
      localStorage.setItem('aippt_code_data', JSON.stringify({
        code: codeData.code,
        expiresAt: Date.now() + (codeData.time_expire * 1000) // 转换为毫秒时间戳
      }))
    },
    
    isCodeValid(savedCodeData) {
      // 提前5分钟过期，避免边界问题
      return savedCodeData.expiresAt > (Date.now() + 5 * 60 * 1000)
    },
    
    loadAipptSDK() {
      if (window.AipptIframe) {
        console.log('AIPPT SDK已加载')
        return Promise.resolve()
      }

      return new Promise((resolve, reject) => {
        const script = document.createElement('script')
        script.src = 'https://api-static.aippt.cn/aippt-iframe-sdk.js'
        script.onload = () => {
          console.log('AIPPT SDK加载成功')
          resolve()
        }
        script.onerror = (error) => {
          console.error('AIPPT SDK加载失败', error)
          reject(new Error('SDK加载失败，请检查网络连接'))
        }
        document.head.appendChild(script)
      })
    },
    
    async getNewCode() {
      try {
        console.log('通过后端代理获取授权码')
        
        // 直接使用相对路径，不再通过环境变量判断
        const url = '/aippt-proxy/grant/code?uid=1&channel=ezijing'
        
        console.log('通过后端代理获取授权码，请求URL:', url)
        
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Accept': 'application/json'
          },
          credentials: 'same-origin'
        })
        
        if (!response.ok) {
          throw new Error(`通过后端代理获取授权码失败: ${response.status} ${response.statusText}`)
        }
        
        const data = await response.json()
        
        if (data.code === 0 && data.data && data.data.code) {
          // 保存授权码数据到localStorage
          this.saveCodeData(data.data)
          console.log('通过后端代理获取授权码成功')
          return data.data.code
        } else {
          throw new Error(data.msg || '通过后端代理获取授权码失败')
        }
      } catch (error) {
        console.error('获取授权码异常:', error)
        throw new Error(`获取授权码失败: ${error.message}`)
      }
    },
    
    async initAipptAsync() {
      try {
        // 1. 加载AIPPT SDK
        await this.loadAipptSDK()
        
        // 2. 检查是否有有效的授权码
        const savedCodeData = this.getSavedCodeData()
        
        let code = null
        if (savedCodeData && this.isCodeValid(savedCodeData)) {
          // 使用保存的有效授权码
          console.log('使用缓存的授权码:', savedCodeData.code)
          code = savedCodeData.code
        } else {
          // 获取新的授权码
          console.log('获取新的授权码')
          try {
            code = await this.getNewCode()
          } catch (error) {
            console.error('获取授权码失败:', error)
            // 检查后端服务是否正常运行
            this.errorMsg = `获取授权码失败: ${error.message}。请确保后端服务(端口9000)已正常启动。`
            return
          }
        }
        
        // 3. 初始化AIPPT
        if (code) {
          await this.initAippt(code)
        } else {
          throw new Error('无法获取授权码')
        }
      } catch (error) {
        console.error('AIPPT初始化失败:', error)
        this.errorMsg = `初始化失败: ${error.message || '未知错误'}`
      } finally {
        this.loading = false
      }
    },
    
    async initAippt(code) {
      try {
        if (!window.AipptIframe) {
          throw new Error('AIPPT SDK未加载')
        }
        
        await window.AipptIframe.show({
          options: { 
            fc_plate: [2003, 2011, 2014, 2024] 
          },
          appkey: this.config.appkey,
          channel: 'ezijing',
          code: code,
          container: document.getElementById('aippt-container'),
          editorModel: this.config.editorModel,
          onMessage: (eventType, data) => {
            console.log('AIPPT事件:', eventType, data)
          }
          
        })
        
        console.log('AIPPT初始化成功')
      } catch (e) {
        console.error('AIPPT初始化失败', e)
        throw new Error(e.msg || e.message || '未知错误')
      }
    }
  },
  beforeUnmount() {
    // 组件销毁前，清理iframe和事件监听器
    window.removeEventListener('resize', this.adjustHeight);
    
    if (window.AipptIframe) {
      try {
        window.AipptIframe.deleteIframe()
      } catch (e) {
        console.error('销毁AIPPT iframe失败', e)
      }
    }
  }
}
</script>

<style scoped>
.integration-test-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.aippt-container {
  width: 100%;
  height: calc(100vh - 65px);
  border: none;
  background-color: #fafafa;
}

.loading-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #ba003f;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 16px;
  color: #333;
}

.error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #ffeeee;
  color: #ba003f;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 90%;
  text-align: center;
  z-index: 10;
}
</style> 