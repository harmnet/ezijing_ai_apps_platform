<template>
  <div class="quick-start-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>数字人快速入门示例</h2>
        </div>
      </template>
      
      <div class="digital-human-container">
        <el-card class="control-panel">
          <h3>控制面板</h3>
          <p>选择数字人角色并发送消息，查看数字人的响应</p>
          
          <el-form :model="form" label-width="100px">
            <el-form-item label="选择数字人">
              <el-select v-model="form.digitalHumanId" @change="handleDigitalHumanChange">
                <el-option 
                  v-for="item in digitalHumans" 
                  :key="item.id" 
                  :label="item.name" 
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item label="发送消息">
              <div class="input-group">
                <el-input v-model="form.message" placeholder="输入要发送给数字人的消息..."></el-input>
                <el-button type="primary" @click="sendMessage">发送</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>
        
        <div class="digital-human-display">
          <div class="video-container" ref="videoContainer">
            <video ref="digitalHumanVideo" autoplay loop muted>
              <source src="https://ezijingai.oss-cn-beijing.aliyuncs.com/digital-human/demo.mp4" type="video/mp4">
              您的浏览器不支持视频标签。
            </video>
            <div v-if="isLoading" class="loading-overlay">
              <el-icon class="loading-icon"><Loading /></el-icon>
              <span>加载数字人中...</span>
            </div>
          </div>
        </div>
        
        <el-card class="digital-human-info">
          <h3>接入说明</h3>
          <p>要在您的应用中接入数字人服务，请参考以下代码示例：</p>
          
          <div class="code-block">
            <pre><code><span class="comment">// 1. 引入数字人SDK</span>
&lt;script src="https://aibeings-vip.xiaoice.com/sdk/digital-human.js"&gt;&lt;/script&gt;

<span class="comment">// 2. 初始化数字人</span>
const digitalHuman = new DigitalHuman({
    container: 'digitalHumanContainer', // 容器ID
    token: 'YOUR_API_TOKEN',            // API令牌
    modelId: 'model_123456',            // 数字人模型ID
    options: {
        autoPlay: true,                 // 自动播放
        width: '100%',                  // 宽度
        height: '400px',                // 高度
        background: '#000000'           // 背景色
    }
});

<span class="comment">// 3. 发送消息给数字人</span>
function sendMessage(message) {
    digitalHuman.sendMessage({
        content: message,
        onStart: () => {
            console.log('数字人开始响应');
        },
        onFinish: () => {
            console.log('数字人响应结束');
        },
        onError: (error) => {
            console.error('发生错误:', error);
        }
    });
}

<span class="comment">// 4. 事件监听</span>
digitalHuman.on('ready', () => {
    console.log('数字人准备就绪');
});

digitalHuman.on('speaking', (data) => {
    console.log('数字人正在说话:', data.text);
});

<span class="comment">// 5. 销毁实例</span>
function destroyDigitalHuman() {
    digitalHuman.destroy();
}</code></pre>
          </div>
          
          <h3>接口文档</h3>
          <p>完整的接口文档请参考：<a href="https://aibeings-vip.xiaoice.com/developer-doc/show/91" target="_blank">数字人开发文档</a></p>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
import { ElMessage } from 'element-plus';
import { Loading } from '@element-plus/icons-vue';
import { aiBeingApi } from '@/utils/request';

export default {
  name: 'DigitalHumanQuickStart',
  components: {
    Loading
  },
  setup() {
    const digitalHumanVideo = ref(null);
    const videoContainer = ref(null);
    const isLoading = ref(false);
    const digitalHumans = ref([]);
    
    const form = reactive({
      digitalHumanId: '',
      message: ''
    });
    
    const fetchDigitalHumans = async () => {
      try {
        const response = await aiBeingApi.getAIBeings({
          status: 'active'
        });
        
        digitalHumans.value = response.data.items;
        
        if (digitalHumans.value.length > 0) {
          form.digitalHumanId = digitalHumans.value[0].id;
        }
      } catch (error) {
        console.error('获取数字人列表失败:', error);
        ElMessage.error('获取数字人列表失败，请稍后重试');
      }
    };
    
    const handleDigitalHumanChange = (id) => {
      isLoading.value = true;
      
      // 模拟加载数字人模型
      setTimeout(() => {
        console.log(`加载ID为${id}的数字人`);
        isLoading.value = false;
        ElMessage.success('数字人加载成功');
      }, 1500);
    };
    
    const sendMessage = () => {
      if (!form.message.trim()) {
        ElMessage.warning('请输入要发送的消息');
        return;
      }
      
      // 在实际应用中，这里会调用数字人SDK发送消息
      ElMessage.success(`消息"${form.message}"已发送给数字人`);
      form.message = '';
    };
    
    // 模拟初始化数字人SDK
    const initDigitalHuman = () => {
      console.log('初始化数字人SDK');
      // 在实际应用中，这里会初始化数字人SDK
    };
    
    // 模拟销毁数字人SDK
    const destroyDigitalHuman = () => {
      console.log('销毁数字人SDK');
      // 在实际应用中，这里会销毁数字人SDK实例
    };
    
    onMounted(() => {
      fetchDigitalHumans();
      initDigitalHuman();
    });
    
    onBeforeUnmount(() => {
      destroyDigitalHuman();
    });
    
    return {
      digitalHumanVideo,
      videoContainer,
      isLoading,
      digitalHumans,
      form,
      handleDigitalHumanChange,
      sendMessage
    };
  }
};
</script>

<style scoped>
.quick-start-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: #409eff;
}

.digital-human-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-panel {
  margin-bottom: 0;
}

.input-group {
  display: flex;
  gap: 10px;
}

.digital-human-display {
  position: relative;
  height: 400px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  background-color: #000;
}

.video-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.video-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
}

.loading-icon {
  font-size: 32px;
  margin-bottom: 10px;
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.code-block {
  background-color: #282c34;
  color: #abb2bf;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 15px 0;
}

.comment {
  color: #5c6370;
  font-style: italic;
}
</style> 