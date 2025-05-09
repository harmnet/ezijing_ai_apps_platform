<template>
  <div class="knowledge-qa-container">
    <div class="qa-content">
      <!-- 功能简介部分 -->
      <div class="description-section">
        <h2>智能企业知识库问答系统</h2>
        <p>通过AI技术，快速从文档中获取专业领域的精准解答，提升工作效率和决策质量。</p>
        <div class="features">
          <div class="feature-item">
            <el-icon><ChatDotSquare /></el-icon>
            <span>智能问答互动</span>
          </div>
          <div class="feature-item">
            <el-icon><DataAnalysis /></el-icon>
            <span>专业领域解答</span>
          </div>
          <div class="feature-item">
            <el-icon><DocumentCopy /></el-icon>
            <span>支持文档引用</span>
          </div>
          <div class="feature-item">
            <el-icon><Connection /></el-icon>
            <span>知识关联推荐</span>
          </div>
        </div>
      </div>
      
      <!-- 文档上传区域 -->
      <div class="document-section" v-if="!documentUploaded">
        <h3>上传知识文档</h3>
        <p class="section-desc">上传一份文档，AI将基于文档内容回答您的问题</p>
        
        <el-upload
          class="document-uploader"
          drag
          :auto-upload="false"
          :show-file-list="true"
          :limit="1"
          :on-change="handleFileChange"
          :on-exceed="handleExceed"
          :on-remove="handleRemove"
          :before-upload="beforeUpload"
          accept=".pdf"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">拖拽文件到此处或 <em>点击上传</em></div>
          <template #tip>
            <div class="el-upload__tip">
              仅支持PDF格式文档，文件大小不超过2MB
            </div>
          </template>
        </el-upload>
        
        <div class="file-info" v-if="selectedFile">
          <h4>已选择文件</h4>
          <p><strong>文件名：</strong>{{ selectedFile.name }}</p>
          <p><strong>文件大小：</strong>{{ formatFileSize(selectedFile.size) }}</p>
          <p><strong>文件类型：</strong>{{ selectedFile.type || getFileTypeByExtension(selectedFile.name) }}</p>
          <div class="action-buttons">
            <el-button 
              type="primary" 
              :disabled="!selectedFile || isUploading" 
              @click="uploadDocument" 
              :loading="isUploading"
            >
              {{ isUploading ? '处理中...' : '开始分析文档' }}
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 聊天问答区域 -->
      <div class="chat-section" v-if="documentUploaded">
        <div class="document-info">
          <div class="info-header">
            <h3>已分析文档</h3>
            <el-button type="text" @click="resetDocument">更换文档</el-button>
          </div>
          <div class="info-content">
            <el-icon><Document /></el-icon>
            <div class="info-text">
              <p class="file-name">{{ selectedFile.name }}</p>
              <p class="file-details">{{ formatFileSize(selectedFile.size) }} · {{ getFileTypeByExtension(selectedFile.name) }}</p>
            </div>
          </div>
        </div>
        
        <div class="chat-container" ref="chatContainer">
          <div class="chat-messages" ref="chatMessages">
            <div class="message system">
              <div class="message-content">
                <p>您好，我是AI助手。我已经阅读了您上传的文档《{{ selectedFile.name }}》，请问有什么问题需要咨询？</p>
              </div>
            </div>
            
            <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
              <div class="message-content">
                <p v-if="message.role === 'user'">{{ message.content }}</p>
                <p v-else v-html="formatAIMessage(message.content)"></p>
              </div>
            </div>
            
            <div class="message assistant" v-if="isStreaming">
              <div class="message-content">
                <p v-html="formatAIMessage(streamingContent)"></p>
                <div class="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="chat-input">
            <el-input
              v-model="userQuestion"
              type="textarea"
              :rows="2"
              :disabled="isStreaming"
              placeholder="请输入您的问题..."
              @keyup.enter.native="sendQuestion"
            />
            <el-button 
              type="primary" 
              :disabled="!userQuestion || isStreaming" 
              @click="sendQuestion"
              :loading="isStreaming"
            >
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 错误提示对话框 -->
    <el-dialog
      v-model="errorDialogVisible"
      title="操作失败"
      width="30%"
    >
      <span>{{ errorMessage }}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="errorDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { ChatDotSquare, DataAnalysis, DocumentCopy, Connection, UploadFilled, Document } from '@element-plus/icons-vue';
import axios from 'axios';

export default {
  name: 'KnowledgeQA',
  components: {
    ChatDotSquare,
    DataAnalysis,
    DocumentCopy,
    Connection,
    UploadFilled,
    Document
  },
  setup() {
    const selectedFile = ref(null);
    const isUploading = ref(false);
    const documentUploaded = ref(false);
    const documentId = ref('');
    const chatContainer = ref(null);
    const chatMessages = ref(null);
    const userQuestion = ref('');
    const messages = ref([]);
    const isStreaming = ref(false);
    const streamingContent = ref('');
    const errorDialogVisible = ref(false);
    const errorMessage = ref('');
    
    // 文件上传相关方法
    const handleFileChange = (file) => {
      selectedFile.value = file.raw;
    };
    
    const handleExceed = () => {
      ElMessage.warning('只能上传1个文件');
    };
    
    const handleRemove = () => {
      selectedFile.value = null;
    };
    
    const beforeUpload = (file) => {
      const isValidType = file.type === 'application/pdf' || 
                         file.type === 'application/msword' || 
                         file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
      
      // 检查扩展名作为备用
      const fileName = file.name.toLowerCase();
      const validExtension = fileName.endsWith('.pdf') || 
                            fileName.endsWith('.doc') || 
                            fileName.endsWith('.docx');
      
      const isLessThan2M = file.size / 1024 / 1024 < 2;

      if (!isValidType && !validExtension) {
        ElMessage.error('只支持PDF和Word文档');
        return false;
      }
      
      if (!isLessThan2M) {
        ElMessage.error('文件大小不能超过2MB');
        return false;
      }
      
      return true;
    };
    
    const formatFileSize = (size) => {
      if (size < 1024) {
        return size + ' B';
      } else if (size < 1024 * 1024) {
        return (size / 1024).toFixed(2) + ' KB';
      } else {
        return (size / 1024 / 1024).toFixed(2) + ' MB';
      }
    };
    
    const getFileTypeByExtension = (filename) => {
      if (filename.toLowerCase().endsWith('.pdf')) {
        return 'PDF文档';
      } else if (filename.toLowerCase().endsWith('.doc') || filename.toLowerCase().endsWith('.docx')) {
        return 'Word文档';
      }
      return '未知类型';
    };
    
    const uploadDocument = async () => {
      if (!selectedFile.value) {
        ElMessage.warning('请先选择文件');
        return;
      }
      
      isUploading.value = true;
      
      try {
        // 创建FormData对象
        const formData = new FormData();
        formData.append('file', selectedFile.value);
        
        // 调用上传文档API - 使用完整的服务器地址
        const apiUrl = 'http://123.57.71.66:8018/api/knowledge/upload';
        const response = await axios.post(apiUrl, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          // 添加超时设置
          timeout: 30000,
          // 确保发送凭证
          withCredentials: true
        });
        
        if (response.data.success) {
          ElMessage.success('文档上传成功');
          documentId.value = response.data.documentId;
          documentUploaded.value = true;
          
          // 等待DOM更新后滚动到底部
          await nextTick();
          scrollToBottom();
        } else {
          throw new Error(response.data.message || '文档上传失败');
        }
      } catch (error) {
        console.error('上传文档失败:', error);
        // 更详细的错误信息
        let errorMsg = '文档上传失败，请稍后重试';
        if (error.response) {
          // 服务器响应错误
          errorMsg = `服务器错误(${error.response.status}): ${error.response.data?.message || '未知错误'}`;
          console.error('响应数据:', error.response.data);
        } else if (error.request) {
          // 请求发送但没有收到响应
          errorMsg = '无法连接到服务器，请检查网络连接';
        } else {
          // 请求设置错误
          errorMsg = `请求错误: ${error.message}`;
        }
        errorMessage.value = errorMsg;
        errorDialogVisible.value = true;
      } finally {
        isUploading.value = false;
      }
    };
    
    const resetDocument = () => {
      documentUploaded.value = false;
      documentId.value = '';
      selectedFile.value = null;
      messages.value = [];
      streamingContent.value = '';
    };
    
    // 聊天相关方法
    const sendQuestion = async () => {
      if (!userQuestion.value.trim() || isStreaming.value) {
        return;
      }
      
      // 添加用户问题到消息列表
      const question = userQuestion.value.trim();
      messages.value.push({
        role: 'user',
        content: question
      });
      
      // 清空输入框
      userQuestion.value = '';
      
      // 滚动到底部
      await nextTick();
      scrollToBottom();
      
      // 开始流式响应
      isStreaming.value = true;
      streamingContent.value = '';
      
      try {
        // 发送请求到后端 - 使用完整服务器地址
        const eventSource = new EventSource(`http://123.57.71.66:8018/api/knowledge/chat?documentId=${documentId.value}&question=${encodeURIComponent(question)}`);
        
        eventSource.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.content) {
            streamingContent.value += data.content;
            nextTick(() => {
              scrollToBottom();
            });
          }
        };
        
        eventSource.onerror = (error) => {
          console.error('流式响应错误:', error);
          eventSource.close();
          isStreaming.value = false;
          
          // 如果有部分回答，添加到消息列表
          if (streamingContent.value) {
            messages.value.push({
              role: 'assistant',
              content: streamingContent.value
            });
            streamingContent.value = '';
          } else {
            // 显示错误消息
            messages.value.push({
              role: 'assistant',
              content: '抱歉，处理您的问题时发生错误，请重试。'
            });
          }
        };
        
        eventSource.addEventListener('end', () => {
          eventSource.close();
          isStreaming.value = false;
          
          // 添加完整回答到消息列表
          messages.value.push({
            role: 'assistant',
            content: streamingContent.value
          });
          streamingContent.value = '';
        });
      } catch (error) {
        console.error('发送问题失败:', error);
        isStreaming.value = false;
        
        // 显示错误消息
        messages.value.push({
          role: 'assistant',
          content: '抱歉，处理您的问题时发生错误，请重试。'
        });
      }
    };
    
    const scrollToBottom = () => {
      if (chatMessages.value) {
        chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
      }
    };
    
    const formatAIMessage = (text) => {
      // 简单格式化：替换换行符为<br>标签
      return text.replace(/\n/g, '<br>');
    };
    
    onMounted(() => {
      // 初始化时的操作
    });
    
    return {
      selectedFile,
      isUploading,
      documentUploaded,
      documentId,
      chatContainer,
      chatMessages,
      userQuestion,
      messages,
      isStreaming,
      streamingContent,
      errorDialogVisible,
      errorMessage,
      handleFileChange,
      handleExceed,
      handleRemove,
      beforeUpload,
      formatFileSize,
      getFileTypeByExtension,
      uploadDocument,
      resetDocument,
      sendQuestion,
      formatAIMessage
    };
  }
};
</script>

<style scoped>
.knowledge-qa-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 160px);
}

.qa-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.description-section {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.description-section h2 {
  font-size: 24px;
  margin-bottom: 16px;
  color: #c74b50;
}

.description-section p {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 20px;
}

.features {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.feature-item .el-icon {
  color: #c74b50;
  font-size: 20px;
}

.feature-item span {
  font-size: 15px;
  font-weight: 500;
}

.document-section {
  background: #fff;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.document-section h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 8px;
}

.section-desc {
  color: #666;
  margin-bottom: 20px;
}

.document-uploader {
  margin: 20px 0;
}

.file-info {
  margin-top: 20px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.file-info h4 {
  font-size: 16px;
  margin-bottom: 12px;
  color: #333;
}

.file-info p {
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.chat-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.document-info {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.info-header h3 {
  font-size: 18px;
  color: #333;
  margin: 0;
}

.info-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

.info-content .el-icon {
  font-size: 24px;
  color: #c74b50;
}

.info-text {
  flex: 1;
}

.file-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.file-details {
  font-size: 12px;
  color: #666;
}

.chat-container {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 600px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 8px;
  word-break: break-word;
}

.message.system .message-content {
  background-color: #f0f0f0;
  color: #666;
}

.message.user .message-content {
  background-color: #c74b50;
  color: white;
}

.message.assistant .message-content {
  background-color: #f5f5f5;
  color: #333;
}

.message-content p {
  margin: 0;
  line-height: 1.5;
}

.typing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 8px;
}

.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: #aaa;
  border-radius: 50%;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-8px);
  }
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 12px;
}

.chat-input .el-input {
  flex: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .knowledge-qa-container {
    padding: 16px;
  }
  
  .description-section {
    padding: 20px;
  }
  
  .chat-container {
    height: 500px;
  }
  
  .features {
    flex-direction: column;
    gap: 10px;
  }
  
  .message-content {
    max-width: 90%;
  }
}
</style> 