<template>
  <div class="deepseek-stream-demo">
    <div class="demo-header">
      <div class="model-selector">
        <label for="model-select">模型:</label>
        <select id="model-select" v-model="selectedModel">
          <option v-for="model in models" :key="model.id" :value="model.id">
            {{ model.name }}
          </option>
        </select>
      </div>
      <div class="controls">
        <div class="stream-toggle">
          <input type="checkbox" id="stream-toggle" v-model="streamMode">
          <label for="stream-toggle">流式输出</label>
        </div>
        <div class="reasoning-toggle">
          <input type="checkbox" id="reasoning-toggle" v-model="showReasoning">
          <label for="reasoning-toggle">显示思考过程</label>
        </div>
        <button class="control-button" @click="clearChat">清空对话</button>
      </div>
    </div>

    <div class="chat-container">
      <div class="messages-container" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
          <div class="message-header">
            <span class="role-badge">{{ message.role === 'user' ? '用户' : '助手' }}</span>
            <span v-if="message.role === 'assistant' && message.reasoning" 
                  class="reasoning-toggle-btn" 
                  @click="toggleReasoning(index)">
              {{ message.showReasoning ? '隐藏思考过程' : '显示思考过程' }}
            </span>
          </div>
          
          <!-- 思考过程区域 -->
          <div v-if="message.role === 'assistant' && message.reasoning && message.showReasoning" 
               class="reasoning-content">
            <div class="reasoning-header">思考过程:</div>
            <div v-html="formatContent(message.reasoning)"></div>
          </div>
          
          <div class="message-content" v-html="formatContent(message.content)"></div>
        </div>
        
        <!-- 流式响应区域 -->
        <div v-if="isStreaming" class="message assistant streaming">
          <div v-if="triggerUpdate >= 0" class="message-header">
            <span class="role-badge">助手</span>
            <span v-if="streamingReasoning && showReasoning" 
                  class="reasoning-toggle-btn" 
                  @click="showStreamingReasoning = !showStreamingReasoning">
              {{ showStreamingReasoning ? '隐藏思考过程' : '显示思考过程' }}
            </span>
            <small style="color: #888;">更新计数: {{triggerUpdate}}</small>
          </div>
          
          <!-- 流式思考过程区域 -->
          <div v-if="streamingReasoning && showReasoning && showStreamingReasoning" class="reasoning-content">
            <div class="reasoning-header">思考过程:</div>
            <div v-html="formatContent(streamingReasoning)" :key="'reasoning'+triggerUpdate"></div>
            <div v-if="isThinking" class="thinking-indicator">
              <span>思考中</span>
              <span class="dot">.</span>
              <span class="dot">.</span>
              <span class="dot">.</span>
            </div>
          </div>
          
          <div class="message-content" v-html="formatContent(streamingContent)" :key="'content'+triggerUpdate"></div>
        </div>
      </div>
      
      <div class="input-area">
        <textarea
          v-model="userInput"
          placeholder="请输入您的问题..."
          @keydown.enter.prevent="onEnterPress"
          :disabled="isStreaming"
          ref="inputTextarea"
          rows="1"
        ></textarea>
        <button 
          class="send-button" 
          @click="sendMessage" 
          :disabled="isStreaming || !userInput.trim()"
        >
          <span v-if="!isStreaming">发送</span>
          <span v-else>接收中...</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';

// 响应式状态
const userInput = ref('');
const messages = ref([]);
const isStreaming = ref(false);
const isThinking = ref(false);
const streamingContent = ref('');
const streamingReasoning = ref('');
const showStreamingReasoning = ref(true);
const messagesContainer = ref(null);
const inputTextarea = ref(null);
const streamMode = ref(true);
const showReasoning = ref(true);
const selectedModel = ref('deepseek-r1');
const triggerUpdate = ref(0); // 添加用于强制更新的触发器

// 可用模型列表
const models = ref([
  { id: 'deepseek-r1', name: 'DeepSeek R1-64K (火山引擎)' },
  { id: 'deepseek-v3', name: 'DeepSeek V3-64K (火山引擎)' }
]);

// 加载模型列表
onMounted(async () => {
  try {
    // 注释掉加载模型列表的代码，直接使用硬编码的模型
    // const response = await fetch('/api/v1/v1/deepseek_volcano/models');
    // const data = await response.json();
    // if (data.status === 'success') {
    //   models.value = data.data;
    //   if (models.value.length > 0) {
    //     selectedModel.value = models.value[0].id;
    //   }
    // }
    // 确保默认选择deepseek-r1
    selectedModel.value = 'deepseek-r1';
  } catch (error) {
    console.error('加载模型列表失败:', error);
  }
  
  // 自动调整输入框高度
  autoResizeTextarea();
  
  // 添加UI刷新定时器
  setInterval(() => {
    if (isStreaming.value) {
      triggerUpdate.value++;
      console.log("定时UI刷新:", triggerUpdate.value);
    }
  }, 500); // 每500毫秒刷新一次
});

// 监听输入框内容变化，自动调整高度
watch(userInput, () => {
  autoResizeTextarea();
});

// 自动滚动到底部
watch([messages, streamingContent, streamingReasoning], () => {
  scrollToBottom();
}, { deep: true });

// 自动调整文本框高度
function autoResizeTextarea() {
  nextTick(() => {
    if (inputTextarea.value) {
      inputTextarea.value.style.height = 'auto';
      inputTextarea.value.style.height = `${Math.min(inputTextarea.value.scrollHeight, 150)}px`;
    }
  });
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}

// 切换显示/隐藏思考过程
function toggleReasoning(index) {
  if (messages.value[index] && messages.value[index].reasoning) {
    messages.value[index].showReasoning = !messages.value[index].showReasoning;
  }
}

// 回车发送
function onEnterPress(event) {
  if (!event.shiftKey) {
    sendMessage();
  }
}

// 清空聊天
function clearChat() {
  messages.value = [];
  streamingContent.value = '';
  streamingReasoning.value = '';
  isStreaming.value = false;
  isThinking.value = false;
}

// 格式化消息内容，处理换行和代码块
function formatContent(content) {
  if (!content) return '';
  
  // 处理代码块
  let formattedContent = content.replace(/```([\s\S]*?)```/g, (match, code) => {
    return `<pre class="code-block"><code>${escapeHtml(code)}</code></pre>`;
  });
  
  // 处理单行代码
  formattedContent = formattedContent.replace(/`([^`]+)`/g, (match, code) => {
    return `<code class="inline-code">${escapeHtml(code)}</code>`;
  });
  
  // 处理换行
  formattedContent = formattedContent.replace(/\n/g, '<br>');
  
  return formattedContent;
}

// 转义HTML特殊字符
function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// 强制更新视图
function forceUpdate() {
  triggerUpdate.value += 1;
}

// 发送消息
async function sendMessage() {
  if (!userInput.value.trim() || isStreaming.value) return;
  
  // 添加用户消息
  const userMessage = { role: 'user', content: userInput.value.trim() };
  messages.value.push(userMessage);
  
  // 清空输入框
  userInput.value = '';
  autoResizeTextarea();
  
  // 准备请求数据
  const requestData = {
    model: selectedModel.value,
    messages: messages.value.map(msg => ({
      role: msg.role,
      content: msg.content
    })),
    stream: streamMode.value,
    return_reasoning: selectedModel.value === 'deepseek-r1' && showReasoning.value
  };
  
  // 设置流式响应状态
  isStreaming.value = true;
  isThinking.value = true;
  streamingContent.value = '';
  streamingReasoning.value = '';
  
  // 发送请求
  try {
    if (streamMode.value) {
      // 流式请求 - 完全重写这部分逻辑
      fetch('/api/v1/v1/deepseek_volcano/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify(requestData)
      }).then(response => {
        // 获取响应的文本流
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 处理数据函数
        function processChunk() {
          reader.read().then(({ value, done }) => {
            if (done) {
              console.log("流读取完成");
              isStreaming.value = false;
              isThinking.value = false;
              
              // 保存流式内容到消息列表
              if (streamingContent.value) {
                const assistantMessage = {
                  role: 'assistant',
                  content: streamingContent.value,
                  showReasoning: true
                };
                
                if (streamingReasoning.value) {
                  assistantMessage.reasoning = streamingReasoning.value;
                }
                
                messages.value.push(assistantMessage);
                streamingContent.value = '';
                streamingReasoning.value = '';
              }
              return;
            }
            
            // 解码并处理新数据
            buffer += decoder.decode(value, { stream: true });
            console.log("收到原始数据:", buffer);
            
            // 处理接收到的SSE数据
            const lines = buffer.split('\n\n');
            buffer = lines.pop() || '';
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const dataStr = line.slice(6);
                console.log("处理SSE数据行:", dataStr);
                
                // 处理结束标记
                if (dataStr === '[DONE]') {
                  console.log("收到结束标记");
                  isStreaming.value = false;
                  isThinking.value = false;
                  
                  // 保存流式内容到消息列表
                  if (streamingContent.value) {
                    const assistantMessage = {
                      role: 'assistant',
                      content: streamingContent.value,
                      showReasoning: true
                    };
                    
                    if (streamingReasoning.value) {
                      assistantMessage.reasoning = streamingReasoning.value;
                    }
                    
                    messages.value.push(assistantMessage);
                    streamingContent.value = '';
                    streamingReasoning.value = '';
                  }
                  return;
                }
                
                try {
                  const data = JSON.parse(dataStr);
                  
                  // 处理错误消息
                  if (data.error) {
                    streamingContent.value += `[错误] ${data.error.message}`;
                    isStreaming.value = false;
                    isThinking.value = false;
                    return;
                  }
                  
                  // 处理火山引擎返回的delta格式数据
                  if (data.choices && data.choices[0].delta) {
                    const delta = data.choices[0].delta;
                    
                    // 处理思考过程增量（火山引擎DeepSeek R1返回格式）
                    if (delta.reasoning_content) {
                      console.log("收到思考过程:", delta.reasoning_content);
                      isThinking.value = true;
                      streamingReasoning.value += delta.reasoning_content;
                      // 强制DOM更新
                      document.title = triggerUpdate.value.toString(); // 间接触发更新
                      triggerUpdate.value++;
                    }
                    
                    // 处理内容增量
                    if (delta.content) {
                      console.log("收到内容:", delta.content);
                      isThinking.value = false;
                      streamingContent.value += delta.content;
                      // 强制DOM更新
                      document.title = triggerUpdate.value.toString(); // 间接触发更新
                      triggerUpdate.value++;
                    }
                  }
                  // 处理标准格式的思考过程
                  else if (data.reasoning) {
                    console.log("收到标准思考过程:", data.reasoning);
                    isThinking.value = true;
                    streamingReasoning.value += data.reasoning;
                    // 强制DOM更新
                    document.title = triggerUpdate.value.toString(); // 间接触发更新
                    triggerUpdate.value++;
                  }
                  // 处理完整思考过程（在结束前发送）
                  else if (data.full_reasoning) {
                    console.log("收到完整思考过程");
                    isThinking.value = false;
                    streamingReasoning.value = data.full_reasoning;
                    // 强制DOM更新
                    document.title = triggerUpdate.value.toString(); // 间接触发更新
                    triggerUpdate.value++;
                  }
                } catch (e) {
                  console.error('解析SSE数据失败:', e, dataStr);
                }
              }
            }
            
            // 继续读取下一块数据
            processChunk();
            
            // 强制DOM刷新和滚动
            nextTick(() => {
              scrollToBottom();
            });
          }).catch(error => {
            console.error("流读取错误:", error);
            isStreaming.value = false;
            isThinking.value = false;
          });
        }
        
        // 开始处理数据流
        processChunk();
      }).catch(error => {
        console.error("请求错误:", error);
        messages.value.push({
          role: 'assistant',
          content: `[错误] 请求失败: ${error.message}`
        });
        isStreaming.value = false;
        isThinking.value = false;
      });
    } else {
      // 非流式请求
      const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });
      
      const data = await response.json();
      
      if (data.status === 'success' && data.data.choices && data.data.choices[0].message) {
        const assistantMessage = {
          role: 'assistant',
          content: data.data.choices[0].message.content,
          showReasoning: true
        };
        
        // 添加思考过程（如果有）
        if (data.reasoning) {
          assistantMessage.reasoning = data.reasoning;
        } else if (data.data.reasoning) {
          assistantMessage.reasoning = data.data.reasoning;
        }
        
        messages.value.push(assistantMessage);
      } else {
        messages.value.push({
          role: 'assistant',
          content: `[错误] ${data.message || '请求失败'}`
        });
      }
      
      isStreaming.value = false;
      isThinking.value = false;
    }
  } catch (error) {
    console.error('请求失败:', error);
    messages.value.push({
      role: 'assistant',
      content: `[错误] 请求失败: ${error.message}`
    });
    isStreaming.value = false;
    isThinking.value = false;
  }
}
</script>

<style scoped>
.deepseek-stream-demo {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 80px);
  min-height: 600px;
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0;
  gap: 20px;
}

.demo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px 10px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.controls {
  display: flex;
  gap: 20px;
  align-items: center;
}

.control-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #f44336;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.control-button:hover {
  background-color: #d32f2f;
}

.stream-toggle, .reasoning-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #f9f9f9;
}

.message {
  padding: 16px;
  border-radius: 8px;
  max-width: 90%;
  animation: fadeIn 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.message.user {
  align-self: flex-end;
  background-color: #e3f2fd;
  border: 1px solid #bbdefb;
}

.message.assistant {
  align-self: flex-start;
  background-color: white;
  border: 1px solid #e0e0e0;
}

.message.streaming {
  border-left: 3px solid #4caf50;
  border-right: 3px solid #4caf50;
  animation: pulseBorder 1.5s infinite;
  background-color: #f1f8e9;
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
}

.message-header {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.role-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: bold;
}

.message.user .role-badge {
  background-color: #2196f3;
  color: white;
}

.message.assistant .role-badge {
  background-color: #4caf50;
  color: white;
}

.message-content {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
  font-size: 15px;
}

.reasoning-toggle-btn {
  cursor: pointer;
  color: #1976d2;
  font-size: 13px;
  text-decoration: underline;
}

.reasoning-content {
  background-color: #f5f5f5;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 12px;
  font-size: 14px;
  border-left: 3px solid #ff9800;
  color: #555;
}

.reasoning-header {
  font-weight: bold;
  margin-bottom: 8px;
  color: #ff9800;
}

.model-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.model-selector select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
  min-width: 220px;
  font-size: 14px;
}

.input-area {
  display: flex;
  padding: 15px 20px;
  background-color: white;
  border-top: 1px solid #e0e0e0;
  gap: 10px;
}

.input-area textarea {
  flex: 1;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
  outline: none;
  font-family: inherit;
  min-height: 24px;
  max-height: 150px;
  font-size: 15px;
}

.send-button {
  padding: 0 25px;
  border: none;
  border-radius: 4px;
  background-color: #2196f3;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  min-width: 100px;
}

.send-button:hover:not(:disabled) {
  background-color: #1976d2;
}

.send-button:disabled {
  background-color: #b0bec5;
  cursor: not-allowed;
}

.code-block {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 10px;
  overflow-x: auto;
  margin: 10px 0;
  border: 1px solid #e0e0e0;
}

.inline-code {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
  border: 1px solid #eee;
}

.typing-indicator, .thinking-indicator {
  display: flex;
  padding: 6px;
  gap: 2px;
  justify-content: flex-start;
  align-items: center;
  margin-top: 10px;
}

/* 简化typing-indicator的样式 */
.typing-indicator {
  padding: 3px;
  margin-top: 5px;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.dot {
  display: inline-block;
  animation: bounce 1s infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulseBorder {
  0% { border-color: #4caf50; }
  50% { border-color: #81c784; }
  100% { border-color: #4caf50; }
}
</style> 