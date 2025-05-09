<template>
  <div class="ai-chat-page">
    <div class="chat-interface">
      <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
          <div v-if="messages.length === 0" class="welcome-section">
            <div class="welcome-header">
              <h1>欢迎使用人工智能应用与高效办公实践教学平台</h1>
            </div>
            
            <div class="feature-section">
              <div class="feature-card">
                <i class="ri-robot-line"></i>
                <h3>智能问答</h3>
                <p>回答各类问题，提供精准信息</p>
              </div>
              <div class="feature-card">
                <i class="ri-file-text-line"></i>
                <h3>文案创作</h3>
                <p>生成高质量文章、脚本和营销文案</p>
              </div>
              <div class="feature-card">
                <i class="ri-code-line"></i>
                <h3>代码编写</h3>
                <p>辅助编程，解决技术难题</p>
              </div>
              <div class="feature-card">
                <i class="ri-lightbulb-line"></i>
                <h3>创意激发</h3>
                <p>提供创意灵感，拓展思维边界</p>
              </div>
            </div>
            
            <div class="suggestion-section">
              <h3>你可以这样问我</h3>
              <div class="suggestion-cards">
                <div class="suggestion-card" @click="usePrompt('列出3个提高专注力的方法')">
                  <p>列出3个提高专注力的方法</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('设计一个15分钟的小组破冰活动')">
                  <p>设计一个15分钟的小组破冰活动</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('推荐2本Python入门书籍及理由')">
                  <p>推荐2本Python入门书籍及理由</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('学术演讲的3个开场技巧')">
                  <p>学术演讲的3个开场技巧</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('用200字描述毕业季的心情')">
                  <p>用200字描述毕业季的心情</p>
                </div>
                <div class="suggestion-card" @click="usePrompt('高数考试3天复习计划要点')">
                  <p>高数考试3天复习计划要点</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 消息列表 -->
          <div class="message-list" ref="messageListRef">
            <div v-for="message in messages" :key="message.id" :class="['message', message.role, {'streaming': message.isStreaming, 'error': message.isError}]">
              <div class="avatar">
                <img v-if="message.role !== 'assistant'" src="@/assets/user-avatar.svg" alt="User">
                <i v-else class="ri-brain-fill"></i>
              </div>
              <div class="content">
                <div v-if="message.role === 'assistant'" class="model-name">
                  {{ currentModelName }}
                  <!-- 添加复制按钮，仅在助手消息有内容且不在流式状态时显示 -->
                  <button v-if="message.content && !message.isStreaming" class="copy-btn" @click.stop="copyMessageContent(message.content)" title="复制内容">
                    <i class="ri-file-copy-line"></i>
                  </button>
                </div>
                
                <!-- 思考过程内容 - 集成到助手消息中，显示在消息内容前面 -->
                <div v-if="message.role === 'assistant' && message.thinkingProcess && message.thinkingProcess.length > 0" class="thinking-inline">
                  <div class="thinking-title">思考过程：</div>
                  <div class="thinking-steps" v-html="formatThinking(message.thinkingProcess)"></div>
                </div>
                
                <!-- 消息内容 -->
                <div class="message-content" v-html="formatMessage(message.content)"></div>
                
                <div v-if="message.attachments && message.attachments.length > 0" class="attachments">
                  <div v-for="(file, index) in message.attachments" :key="index" class="attachment-item">
                    <i class="ri-file-line"></i> {{ file.name }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-input-wrapper">
          <!-- 选择模型和按钮组放在上方 -->
          <div class="chat-input-actions-row">
            <div class="model-selector">
              <label for="model-select">模型:</label>
              <select id="model-select" class="model-select" v-model="selectedModel">
                <option v-for="model in availableModels" :key="model.id" :value="model.id">{{ model.name }}</option>
              </select>
            </div>
            <div class="chat-actions">
              <button class="toolbar-btn" @click="clearChat" title="清空对话">
                <span>清空</span>
              </button>
            </div>
          </div>
          
          <!-- 对话输入框放在下方 -->
          <div class="chat-input-container">
            <textarea 
              id="chat-input" 
              v-model="userInput" 
              placeholder="请输入您的问题..." 
              rows="1"
              @input="autoResize"
              @keydown.enter.exact.prevent="sendMessage"
            ></textarea>
            <div class="chat-input-actions">
              <button class="send-btn" @click="sendMessage" :disabled="!userInput.trim() || isLoading">
                <i class="ri-send-plane-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/utils/api';

// 添加路由对象
const route = useRoute();

// 响应式状态
const messages = ref([]);
const userInput = ref('');
const selectedModel = ref('deepseek-v3');
const isLoading = ref(false);
const errorMessage = ref('');
const thinkingProcess = ref([]);
const messageListRef = ref(null);

// 可用模型列表
const availableModels = [
  { id: 'deepseek-r1', name: 'DeepSeek-R1（火山引擎）' },
  { id: 'deepseek-v3', name: 'DeepSeek-V3（火山引擎）' }
];

// 计算属性
const currentModelName = computed(() => {
  const model = availableModels.find(m => m.id === selectedModel.value);
  return model ? model.name : selectedModel.value;
});

const isR1Model = computed(() => {
  return selectedModel.value.includes('deepseek-r1');
});

// 使用建议提示
function usePrompt(text) {
  userInput.value = text;
  sendMessage();
}

// 发送消息
async function sendMessage() {
  if (!userInput.value.trim() || isLoading.value) return;
  
  // 创建用户消息
  const userMsgId = Date.now();
  const newMessage = {
    id: userMsgId,
    role: 'user',
    content: userInput.value.trim()
  };
  
  console.log('第1步：添加用户消息');
  // 添加用户消息
  messages.value.push(newMessage);
  userInput.value = '';
  isLoading.value = true;
  errorMessage.value = '';
  thinkingProcess.value = []; // 清空思考过程
  
  // 创建助手消息（空的）
  const assistantMsgId = Date.now() + 1;
  console.log('第2步：创建空的助手消息，ID:', assistantMsgId);
  messages.value.push({
    id: assistantMsgId,
    role: 'assistant',
    content: '',  // 空内容，会在收到第一个响应时更新
    thinkingProcess: [],
    isStreaming: true // 添加标记为流式输出中
  });
  
  // 滚动到底部
  scrollToBottom();
  
  // 准备发送给API的所有历史消息
  const userMessages = messages.value
    .filter(msg => msg.role === 'user')
    .map(msg => ({ role: msg.role, content: msg.content }));
    
  console.log('第3步：发送用户消息给API，消息数:', userMessages.length);
  
  try {
    // 使用DeepSeek Volcano API进行流式对话
    const requestData = {
      model: selectedModel.value,
      messages: userMessages,
      stream: true,
      temperature: 0.7,
      max_tokens: 2000,
      return_reasoning: selectedModel.value === 'deepseek-r1'
    };

    // 发送请求到DeepSeek Volcano API
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
            
            // 更新消息，移除流式状态
            const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
            if (assistantMsgIndex !== -1) {
              const updatedMessages = [...messages.value];
              updatedMessages[assistantMsgIndex] = {
                ...updatedMessages[assistantMsgIndex],
                isStreaming: false
              };
              messages.value = updatedMessages;
            }
            
            isLoading.value = false;
            return;
          }
          
          // 解码并处理新数据
          buffer += decoder.decode(value, { stream: true });
          console.log("收到原始数据:", buffer.length, "字节");
          
          // 处理接收到的SSE数据
          const lines = buffer.split('\n\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.slice(6);
              console.log("处理SSE数据行:", dataStr.substring(0, 50) + "...");
              
              // 处理结束标记
              if (dataStr === '[DONE]') {
                console.log("收到结束标记");
                isLoading.value = false;
                
                // 更新消息，移除流式状态
                const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
                if (assistantMsgIndex !== -1) {
                  const updatedMessages = [...messages.value];
                  updatedMessages[assistantMsgIndex] = {
                    ...updatedMessages[assistantMsgIndex],
                    isStreaming: false
                  };
                  messages.value = updatedMessages;
                }
                return;
              }
              
              try {
                const data = JSON.parse(dataStr);
                
                // 处理错误消息
                if (data.error) {
                  console.error("API错误:", data.error);
                  errorMessage.value = data.error.message || '请求出错';
                  
                  // 更新消息，标记错误
                  const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
                  if (assistantMsgIndex !== -1) {
                    const updatedMessages = [...messages.value];
                    updatedMessages[assistantMsgIndex] = {
                      ...updatedMessages[assistantMsgIndex],
                      isError: true,
                      isStreaming: false,
                      content: '生成回复时出错: ' + (data.error.message || '未知错误')
                    };
                    messages.value = updatedMessages;
                  }
                  
                  isLoading.value = false;
                  return;
                }
                
                // 处理火山引擎返回的delta格式数据
                if (data.choices && data.choices[0].delta) {
                  const delta = data.choices[0].delta;
                  
                  // 处理思考过程增量（火山引擎DeepSeek R1返回格式）
                  if (delta.reasoning_content) {
                    console.log("收到思考过程:", delta.reasoning_content);
                    thinkingProcess.value.push(delta.reasoning_content);
                    
                    // 更新思考过程
                    const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
                    if (assistantMsgIndex !== -1) {
                      const updatedMessages = [...messages.value];
                      updatedMessages[assistantMsgIndex] = {
                        ...updatedMessages[assistantMsgIndex],
                        thinkingProcess: [...thinkingProcess.value]
                      };
                      messages.value = updatedMessages;
                    }
                  }
                  
                  // 处理内容增量
                  if (delta.content) {
                    console.log("收到内容增量:", delta.content);
                    
                    // 更新消息内容
                    const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
                    if (assistantMsgIndex !== -1) {
                      const currentContent = messages.value[assistantMsgIndex].content;
                      const updatedMessages = [...messages.value];
                      updatedMessages[assistantMsgIndex] = {
                        ...updatedMessages[assistantMsgIndex],
                        content: currentContent + delta.content
                      };
                      messages.value = updatedMessages;
                      
                      // 滚动到底部
                      nextTick(() => {
                        scrollToBottom();
                      });
                    }
                  }
                }
                // 处理标准格式的思考过程
                else if (data.reasoning) {
                  console.log("收到标准思考过程");
                  thinkingProcess.value.push(data.reasoning);
                  
                  // 更新思考过程
                  const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
                  if (assistantMsgIndex !== -1) {
                    const updatedMessages = [...messages.value];
                    updatedMessages[assistantMsgIndex] = {
                      ...updatedMessages[assistantMsgIndex],
                      thinkingProcess: [...thinkingProcess.value]
                    };
                    messages.value = updatedMessages;
                  }
                }
                // 处理完整思考过程（在结束前发送）
                else if (data.full_reasoning) {
                  console.log("收到完整思考过程");
                  
                  // 更新思考过程
                  const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
                  if (assistantMsgIndex !== -1) {
                    const updatedMessages = [...messages.value];
                    updatedMessages[assistantMsgIndex] = {
                      ...updatedMessages[assistantMsgIndex],
                      thinkingProcess: [data.full_reasoning]
                    };
                    messages.value = updatedMessages;
                  }
                }
              } catch (e) {
                console.error('解析SSE数据失败:', e, dataStr);
              }
            }
          }
          
          // 继续读取下一块数据
          processChunk();
          
          // 滚动到底部
          nextTick(() => {
            scrollToBottom();
          });
        }).catch(error => {
          console.error("流读取错误:", error);
          isLoading.value = false;
          
          // 标记错误
          const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
          if (assistantMsgIndex !== -1) {
            const updatedMessages = [...messages.value];
            updatedMessages[assistantMsgIndex] = {
              ...updatedMessages[assistantMsgIndex],
              isError: true,
              isStreaming: false,
              content: '接收响应时出错: ' + error.message
            };
            messages.value = updatedMessages;
          }
        });
      }
      
      // 开始处理数据流
      processChunk();
    }).catch(error => {
      console.error("请求错误:", error);
      errorMessage.value = error.message || '请求出错';
      isLoading.value = false;
      
      // 标记错误
      const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
      if (assistantMsgIndex !== -1) {
        const updatedMessages = [...messages.value];
        updatedMessages[assistantMsgIndex] = {
          ...updatedMessages[assistantMsgIndex],
          isError: true,
          isStreaming: false,
          content: '请求失败: ' + error.message
        };
        messages.value = updatedMessages;
      }
    });
    
  } catch (error) {
    console.error('发送消息失败:', error);
    errorMessage.value = error.message || '请求出错，请稍后重试';
    isLoading.value = false;
    
    // 尝试找到助手消息的索引
    const assistantMsgIndex = messages.value.findIndex(msg => msg.id === assistantMsgId);
    if (assistantMsgIndex !== -1) {
      // 标记错误
      const updatedMessages = [...messages.value];
      updatedMessages[assistantMsgIndex] = {
        ...updatedMessages[assistantMsgIndex],
        isError: true,
        isStreaming: false,
        content: '生成回复时出错: ' + (error.message || '未知错误')
      };
      messages.value = updatedMessages;
    }
  }
}

// 清空对话
function clearChat() {
  messages.value = [];
  errorMessage.value = '';
  thinkingProcess.value = [];
}

// 自动调整输入框高度
function autoResize(event) {
  const textarea = event.target;
  textarea.style.height = 'auto';
  textarea.style.height = (textarea.scrollHeight < 300 ? textarea.scrollHeight : 300) + 'px';
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
      const scrollHeight = messagesContainer.scrollHeight;
      messagesContainer.scrollTop = scrollHeight;
    }
  });
}

// 格式化消息内容
function formatMessage(content) {
  if (!content) return '';
  
  // 确保content是字符串
  const contentStr = String(content);
  
  // 使用标记换行符并转换为HTML
  let formattedContent = contentStr
    .replace(/\n/g, '<br>') // 换行符转为HTML的<br>
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **粗体**
    .replace(/\*(.*?)\*/g, '<em>$1</em>'); // *斜体*
    
  // 高亮代码块
  formattedContent = formattedContent.replace(
    /```([\s\S]*?)```/g, 
    '<pre><code>$1</code></pre>'
  );
  
  // 高亮行内代码
  formattedContent = formattedContent.replace(
    /`([^`]+)`/g, 
    '<code>$1</code>'
  );
  
  return formattedContent;
}

// 格式化思考过程
function formatThinking(text) {
  if (!text) return '';
  if (Array.isArray(text)) {
    text = text.join('');
  }
  return text.replace(/\n{2,}/g, '\n').replace(/\n/g, '<br>');
}

// 复制消息内容
function copyMessageContent(content) {
  if (!content) return;
  
  // 使用剪贴板API复制文本
  navigator.clipboard.writeText(content)
    .then(() => {
      // 显示复制成功的提示
      showCopySuccess();
      console.log('内容已复制到剪贴板');
    })
    .catch(err => {
      console.error('复制失败:', err);
    });
}

// 显示复制成功提示
function showCopySuccess() {
  // 创建一个临时的提示元素
  const toast = document.createElement('div');
  toast.className = 'copy-toast';
  toast.innerText = '已复制';
  document.body.appendChild(toast);
  
  // 动画显示后删除
  setTimeout(() => {
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        document.body.removeChild(toast);
      }, 300);
    }, 1500);
  }, 10);
}

// 显示错误提示
function showErrorToast(message) {
  const toast = document.createElement('div');
  toast.className = 'copy-toast error-toast';
  toast.innerText = message;
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        document.body.removeChild(toast);
      }, 300);
    }, 3000);
  }, 10);
}

// 判断是否为R1模型
function isFromR1Model(message) {
  return message && message.modelType && message.modelType.includes('r1-vol');
}

// 生命周期钩子
onMounted(() => {
  // 检查URL中是否有prompt参数
  if (route.query.prompt) {
    try {
      const promptFromUrl = decodeURIComponent(route.query.prompt);
      console.log('从URL接收到prompt参数:', promptFromUrl);
      
      // 设置到输入框并发送
      userInput.value = promptFromUrl;
      // 使用nextTick确保DOM更新后再发送
      nextTick(() => {
        sendMessage();
      });
    } catch (error) {
      console.error('解析URL prompt参数失败:', error);
    }
  }

  // 仅在开发环境添加测试辅助函数
  if (process.env.NODE_ENV !== 'production') {
    window.testAIChat = {
      updateMsg: (text) => {
        if (messages.value.length > 0) {
          // 获取最后一条消息的索引
          const lastIndex = messages.value.length - 1;
          // 创建新的消息数组
          const updatedMessages = [...messages.value];
          // 更新最后一条消息
          updatedMessages[lastIndex] = {
            ...updatedMessages[lastIndex],
            content: updatedMessages[lastIndex].content + text
          };
          // 替换整个数组
          messages.value = updatedMessages;
        }
      },
      addThinking: (text) => {
        if (messages.value.length > 0) {
          const lastIndex = messages.value.length - 1;
          const updatedMessages = [...messages.value];
          
          // 获取最后一条消息
          const lastMessage = updatedMessages[lastIndex];
          
          // 如果最后一条消息是助手消息，则更新其思考过程
          if (lastMessage.role === 'assistant') {
            updatedMessages[lastIndex] = {
              ...lastMessage,
              thinkingProcess: Array.isArray(lastMessage.thinkingProcess) 
                ? [...lastMessage.thinkingProcess, text]
                : [text]
            };
            messages.value = updatedMessages;
          }
        }
      },
      getState: () => {
        return {
          messages: messages.value,
          isR1Model: isR1Model.value,
          selectedModel: selectedModel.value
        };
      }
    };
  }
});
</script>

<style scoped>
@import '../assets/styles/chat-common.css';
</style> 