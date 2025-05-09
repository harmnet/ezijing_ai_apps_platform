<template>
  <div class="text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>文章校对</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showTips">
          <i class="ri-book-read-line"></i>
          知识学习
        </button>
      </div>
    </div>
    
    <!-- 主要内容区域 - 使用两列布局 -->
    <div class="main-container">
      <!-- 左侧：输入参数 -->
      <div class="input-section">
        <div class="section-header">
          <h3 class="section-title">
            <i class="ri-file-text-line"></i>
            文本输入
          </h3>
        </div>
        
        <!-- 移除诗歌类型、主题、风格倾向、背景情景和关键词部分 -->
        
        <!-- 文本输入支持直接输入和上传文件两种形式 -->
        <div class="form-group">
          <label for="text-input" class="required">直接文本输入</label>
          <textarea 
            id="text-input" 
            v-model="textInput" 
            placeholder="请输入需要校对的文本内容（最多1000个汉字）..."
            class="form-control"
            rows="10"
            maxlength="1000"
          ></textarea>
          <div class="text-counter">{{textInput.length}}/1000</div>
        </div>
        
        <div class="form-group">
          <label for="file-upload">上传文件</label>
          <div class="file-upload-container">
            <button class="file-upload-btn" disabled>
              <i class="ri-upload-2-line"></i>
              选择文件
            </button>
            <span class="file-upload-hint">文件上传功能暂不可用</span>
          </div>
        </div>
        
        <!-- 校对选项 -->
        <div class="form-group">
          <label>校对选项</label>
          <div class="checkbox-group">
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.grammar}">
              <input type="checkbox" v-model="checkOptions.grammar">
              <span class="checkbox-label">语法检查</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.spelling}">
              <input type="checkbox" v-model="checkOptions.spelling">
              <span class="checkbox-label">拼写检查</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.punctuation}">
              <input type="checkbox" v-model="checkOptions.punctuation">
              <span class="checkbox-label">标点符号</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.tone}">
              <input type="checkbox" v-model="checkOptions.tone">
              <span class="checkbox-label">语气一致性</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.readability}">
              <input type="checkbox" v-model="checkOptions.readability">
              <span class="checkbox-label">可读性分析</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.format}">
              <input type="checkbox" v-model="checkOptions.format">
              <span class="checkbox-label">格式规范</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.synonym}">
              <input type="checkbox" v-model="checkOptions.synonym">
              <span class="checkbox-label">同义词建议</span>
            </label>
            <label class="checkbox-item" :class="{'checkbox-active': checkOptions.clarity}">
              <input type="checkbox" v-model="checkOptions.clarity">
              <span class="checkbox-label">表达清晰度</span>
            </label>
          </div>
        </div>
        
        <!-- 模型选择 -->
        <div class="form-group">
          <label for="model">AI模型</label>
          <select id="model" v-model="selectedModel" class="form-control">
            <option v-for="model in modelList" :key="model.id" :value="model.id">
              {{ model.name }}
            </option>
          </select>
        </div>
        
        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="generateLongform" class="btn btn-primary" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '校对中...' : '开始校对' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：结果 -->
      <div class="right-column">
        <!-- 校对结果 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              校对结果
            </h3>
            <div class="action-buttons">
              <button @click="generateLongform" class="primary-button" :disabled="isGenerating">
                <i class="ri-refresh-line" v-if="!isGenerating"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isGenerating ? '校对中...' : '再次校对' }}
              </button>
              <button @click="copyText" class="secondary-button" :disabled="isGenerating || !generatedNote">
                <i class="ri-file-copy-line"></i>
                复制文本
              </button>
              <button @click="showPrompt" class="prompt-button" :disabled="!lastUsedPrompt">
                <i class="ri-code-line"></i>
                查看提示词
              </button>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isGenerating" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedNote && !isGenerating" class="empty-result">
              <div class="empty-content">
                <img src="@/assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无校对内容，请点击"开始校对"按钮开始校对</p>
              </div>
            </div>
            
            <div v-else-if="generatedNote" class="note-result" :class="{'blur-content': isGenerating, 'streaming': isStreaming}">
              <textarea v-model="generatedNote" class="result-textarea" readonly></textarea>
              <div v-if="isStreaming" class="streaming-indicator">
                <span class="dot-typing"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 替换原有的弹窗为侧边抽屉 -->
    <el-drawer
      v-model="showTipsModal"
      title="文章校对知识学习"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in articleKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
      </div>
    </el-drawer>

    <!-- 提示词模态框 -->
    <div class="modal" v-if="showPromptModal">
      <div class="modal-content prompt-modal">
        <div class="modal-header">
          <h3><i class="ri-file-text-line"></i> 生成提示词</h3>
          <button class="close-btn" @click="showPromptModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="prompt-content">
            <div v-if="lastUsedPrompt && lastUsedPrompt.length">
              <div v-for="(msg, index) in lastUsedPrompt" :key="index" class="prompt-message">
                <div class="prompt-role">{{ msg.role === 'system' ? '系统提示词' : '用户提示词' }}</div>
                <div class="prompt-text">{{ msg.content }}</div>
              </div>
            </div>
            <div v-else>暂无提示词内容</div>
          </div>
          <div class="prompt-actions">
            <button class="secondary-button" @click="copyPrompt">
              <i class="ri-file-copy-line"></i> 复制提示词
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import '@/assets/css/text-creation-common.css'; // 引入统一CSS样式文件
import { proofreadingKnowledge } from '@/views/Knowledge_data.js';

export default {
  name: 'Proofreading',
  data() {
    return {
      // 文本输入
      textInput: '',
      
      // 校对选项
      checkOptions: {
        grammar: true,
        spelling: true,
        punctuation: true,
        tone: false,
        readability: false,
        format: false,
        synonym: false,
        clarity: false
      },
      
      // 结果内容
      isGenerating: false,
      loadingText: '正在校对文章，请耐心等待...',
      generatedNote: '',
      lastUsedPrompt: null,
      isStreaming: false,
      
      // 模态框控制
      showTipsModal: false,
      showPromptModal: false,
      
      // 模型选择 - 默认使用火山引擎V3
      selectedModel: 'deepseek-v3',
      modelList: [],
      
      // 添加文章校对知识内容
      articleKnowledge: proofreadingKnowledge
    };
  },
  mounted() {
    this.fetchModelList();
  },
  methods: {
    // 设置默认模型列表
    setupDefaultModels() {
      console.log('使用默认模型列表');
      this.modelList = [
        { id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' },
        { id: 'deepseek-r1', name: 'DeepSeek R1（火山引擎）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎旧版）' },
        { id: 'douban', name: '豆包大模型' }
      ];
      this.selectedModel = 'deepseek-v3';
    },
    
    // 获取可用的大模型列表
    async fetchModelList() {
      try {
        console.log('开始获取模型列表...');
        // 获取模型列表
        const response = await axios.get('/api/v1/llm/models', { timeout: 10000 });
        console.log('获取模型列表响应:', response.data);
        
        if (response.data && response.data.status === 'success') {
          // 过滤模型，只保留火山引擎R1、V3和豆包模型
          let allModels = response.data.data || [];
          this.modelList = allModels.filter(model => 
            model.id === 'deepseek-v3' || 
            model.id === 'deepseek-r1' ||
            model.id === 'deepseek-r1-vol' || 
            model.id === 'douban'
          );
          
          // 确保所有需要的模型都在列表中，没有则添加
          const modelIds = this.modelList.map(model => model.id);
          if (!modelIds.includes('deepseek-v3')) {
            this.modelList.push({ id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' });
          }
          if (!modelIds.includes('deepseek-r1')) {
            this.modelList.push({ id: 'deepseek-r1', name: 'DeepSeek R1（火山引擎）' });
          }
          
          console.log('过滤后的可用模型列表:', this.modelList);
          
          // 如果过滤后没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.setupDefaultModels();
          }
          
          // 默认选择火山引擎V3
          const volcanoModel = this.modelList.find(model => model.id === 'deepseek-v3');
          if (volcanoModel) {
            this.selectedModel = volcanoModel.id;
          } else if (this.modelList.length > 0) {
            this.selectedModel = this.modelList[0].id;
          } else {
            this.selectedModel = 'deepseek-v3';
          }
          
          console.log('已选择模型:', this.selectedModel);
        } else {
          console.error('获取模型列表失败:', response.data?.message);
          this.setupDefaultModels();
        }
      } catch (error) {
        console.error('获取模型列表异常:', error.message);
        if (error.response) {
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
        }
        this.setupDefaultModels();
      }
    },
    
    // 生成校对结果的方法
    async generateLongform() {
      // 验证必填字段
      if (!this.validateForm()) {
        return;
      }
      
      this.isGenerating = true;
      this.generatedNote = '';
      this.isStreaming = false;
      
      try {
        // 构建提示词
        const prompt = this.generatePrompt();
        
        // 构建API请求参数
        const systemMessage = "你是一位专业的文章校对专家，能够提供准确、全面的文章校对和修改建议。";
        const userMessage = prompt;
        
        const apiMessages = [
          { role: "system", content: systemMessage },
          { role: "user", content: userMessage }
        ];
        
        // 保存apiMessages供后续显示
        this.lastUsedPrompt = apiMessages;
        
        this.loadingText = '正在校对文章，请耐心等待...';
        
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        console.log('开始调用API，模型:', this.selectedModel);
        
        // 准备API参数
        const apiParams = {
          model: this.selectedModel,
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        // 记录API请求详情，方便调试
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        // 开始流式状态
        this.isStreaming = true;
        
        // 使用fetch API发送请求，以处理流式响应
        console.log('开始发送流式请求到:', '/api/v1/v1/deepseek_volcano/chat');
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(apiParams)
        });
        
        console.log('收到响应, 状态码:', response.status);
        console.log('响应头:', {
          'Content-Type': response.headers.get('Content-Type'),
          'Transfer-Encoding': response.headers.get('Transfer-Encoding')
        });
        
        if (!response.ok) {
          throw new Error(`服务器返回错误: ${response.status}`);
        }
        
        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 读取流数据
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
            console.log('流式响应完成');
            break;
          }
          
          // 解码二进制数据
          const decoded = decoder.decode(value, { stream: true });
          console.log('收到数据块:', decoded.length, '字节');
          buffer += decoded;
          
          // 处理收到的数据
          const lines = buffer.split('\n\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (line.trim() === '') continue;
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                console.log('收到结束标志');
                continue;
              }
              
              try {
                console.log('解析数据:', data.substring(0, 100) + '...');
                const parsed = JSON.parse(data);
                console.log('解析后的数据格式:', Object.keys(parsed));
                
                // 处理错误消息
                if (parsed.error) {
                  console.error("API错误:", parsed.error);
                  throw new Error(parsed.error.message || '校对失败');
                }
                
                // 处理火山引擎返回的delta格式数据
                if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                  const delta = parsed.choices[0].delta;
                  
                  // 处理内容增量
                  if (delta.content) {
                    console.log("收到内容增量:", delta.content);
                    // 累加收到的内容
                    this.generatedNote += delta.content;
                  }
                }
              } catch (e) {
                console.error('解析流式数据失败:', e, data);
              }
            }
          }
        }
        
        // 流式响应完成
        this.isStreaming = false;
        console.log('校对完成，总字数:', this.generatedNote.length);
        
        // 添加成功提示
        this.$message ? this.$message.success('文章校对完成！') : alert('文章校对完成！');
          
      } catch (error) {
        console.error('生成校对结果出错，详细错误:', error);
        
        // 更详细的错误日志
        if (error.response) {
          // 服务器响应了，但状态码不在2xx范围
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          this.$message ? 
            this.$message.error(`校对失败: 服务器错误 (${error.response.status})`) : 
            alert(`校对失败: 服务器错误 (${error.response.status})`);
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到服务器响应');
          this.$message ? 
            this.$message.error('校对失败: 服务器无响应，请检查网络连接') : 
            alert('校对失败: 服务器无响应，请检查网络连接');
        } else {
          // 设置请求时发生错误
          console.error('错误信息:', error.message);
          this.$message ? 
            this.$message.error(`校对失败: ${error.message}`) : 
            alert(`校对失败: ${error.message}`);
        }
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          console.log('开发模式：使用示例内容');
          this.generatedNote = `文章校对结果：\n\n【问题摘要】\n- 发现语法错误：3处\n- 发现拼写错误：2处\n- 标点符号问题：4处\n- 表达不清晰：2处\n\n【详细修改建议】\n1. 第一段第二句：语法错误，主语缺失\n   原文："经过多年发展，已成为行业领导者。"\n   建议："经过多年发展，公司已成为行业领导者。"\n\n2. 第二段第一句：标点使用不当\n   原文："然而，研究表明；消费者更关注..."\n   建议："然而，研究表明：消费者更关注..."\n\n3. 第三段：拼写错误\n   原文："这些数据充分表明了该趋是不可逆转的"\n   建议："这些数据充分表明了该趋势是不可逆转的"`;
        }
      } finally {
        this.isGenerating = false;
        this.isStreaming = false;
      }
    },
    
    // 验证表单
    validateForm() {
      if (!this.textInput.trim()) {
        this.$message ? this.$message.error('请输入需要校对的文本内容') : alert('请输入需要校对的文本内容');
        return false;
      }
      
      // 检查是否至少选择了一个校对选项
      const hasSelectedOption = Object.values(this.checkOptions).some(value => value === true);
      if (!hasSelectedOption) {
        this.$message ? this.$message.error('请至少选择一个校对选项') : alert('请至少选择一个校对选项');
        return false;
      }
      
      return true;
    },
    
    // 生成提示词
    generatePrompt() {
      let prompt = '请对以下文本进行校对和修改：\n\n';
      
      // 添加文本内容
      prompt += `${this.textInput}\n\n`;
      
      // 添加校对选项
      prompt += '请根据以下选项进行校对：\n';
      
      if (this.checkOptions.grammar) {
        prompt += '- 语法检查：检查语法错误，包括主谓一致、时态、语态等问题\n';
      }
      
      if (this.checkOptions.spelling) {
        prompt += '- 拼写检查：查找并纠正拼写错误、错别字和用词不当\n';
      }
      
      if (this.checkOptions.punctuation) {
        prompt += '- 标点符号：检查标点符号的使用是否正确、缺失或多余\n';
      }
      
      if (this.checkOptions.tone) {
        prompt += '- 语气一致性：检查全文语气是否一致，包括人称和表达方式\n';
      }
      
      if (this.checkOptions.readability) {
        prompt += '- 可读性分析：分析文本的可读性，包括句子长度、复杂度等\n';
      }
      
      if (this.checkOptions.format) {
        prompt += '- 格式规范：检查文本格式是否规范，包括段落划分、缩进等\n';
      }
      
      if (this.checkOptions.synonym) {
        prompt += '- 同义词建议：提供更准确或更生动的同义词替换建议\n';
      }
      
      if (this.checkOptions.clarity) {
        prompt += '- 表达清晰度：检查表达是否清晰，提供改进模糊或冗余表达的建议\n';
      }
      
      // 输出要求
      prompt += '\n请提供以下内容：\n1. 问题摘要：列出发现的主要问题类型及数量\n2. 详细修改建议：按照文本顺序列出具体问题，并提供修改建议\n3. 对于重要问题，请同时提供原文和修改后的建议文本\n';
      
      return prompt;
    },
    
    // 重置表单
    resetForm() {
      this.textInput = '';
      // 重置校对选项为默认值
      this.checkOptions = {
        grammar: true,
        spelling: true,
        punctuation: true,
        tone: false,
        readability: false,
        format: false,
        synonym: false,
        clarity: false
      };
      this.generatedNote = '';
    },
    
    // 显示创作小贴士
    showTips() {
      this.showTipsModal = true;
    },
    
    // 复制生成的文本
    copyText() {
      if (!this.generatedNote) return;
      
      try {
        navigator.clipboard.writeText(this.generatedNote).then(() => {
          this.$message ? this.$message.success('内容已复制到剪贴板') : alert('内容已复制到剪贴板');
        });
      } catch (error) {
        console.error('复制失败:', error);
        this.$message ? this.$message.error('复制失败，请手动复制') : alert('复制失败，请手动复制');
      }
    },
    
    // 显示提示词模态框
    showPrompt() {
      this.showPromptModal = true;
    },
    
    // 复制提示词到剪贴板
    copyPrompt() {
      if (!this.lastUsedPrompt) return;
      
      try {
        let promptText = '';
        if (typeof this.lastUsedPrompt === 'string') {
          promptText = this.lastUsedPrompt;
        } else {
          // 遍历消息数组
          this.lastUsedPrompt.forEach(msg => {
            promptText += `【${msg.role === 'system' ? '系统' : '用户'}】\n${msg.content}\n\n`;
          });
        }
        
        navigator.clipboard.writeText(promptText).then(() => {
          this.$message ? this.$message.success('提示词已复制到剪贴板') : alert('提示词已复制到剪贴板');
        });
      } catch (error) {
        console.error('复制提示词失败:', error);
        this.$message ? this.$message.error('复制失败，请手动复制') : alert('复制失败，请手动复制');
      }
    },
    
    // 下载生成的文本
    downloadText() {
      if (!this.generatedNote) return;
      
      const element = document.createElement('a');
      const file = new Blob([this.generatedNote], {type: 'text/plain'});
      element.href = URL.createObjectURL(file);
      element.download = `校对结果_${new Date().toISOString().slice(0,10)}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    
    // 格式化Markdown文本
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗语法
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理换行
      text = text.replace(/\n\n/g, '</p><p>');
      
      // 处理列表项
      if (text.includes('- ')) {
        const lines = text.split('\n');
        let inList = false;
        let formattedText = '';
        
        for (let line of lines) {
          if (line.trim().startsWith('- ')) {
            if (!inList) {
              formattedText += '<ul>';
              inList = true;
            }
            formattedText += `<li>${line.substring(2).trim()}</li>`;
          } else {
            if (inList) {
              formattedText += '</ul>';
              inList = false;
            }
            formattedText += line + '\n';
          }
        }
        
        if (inList) {
          formattedText += '</ul>';
        }
        
        text = formattedText;
      }
      
      return `<p>${text}</p>`;
    }
  }
};
</script>

<style scoped>
/* 导入统一CSS样式文件 */
@import "@/assets/css/text-creation-common.css";

/* 页面特有样式 - 仅保留未在text-creation-common.css中定义的样式 */

/* 文本计数器 */
.text-counter {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* 文件上传容器 */
.file-upload-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.file-upload-btn {
  background-color: #f5f5f5;
  color: #999;
  border: 1px solid #ddd;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: not-allowed;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
}

.file-upload-hint {
  font-size: 13px;
  color: #999;
  font-style: italic;
}

/* 提示词模态框样式 */
.prompt-modal {
  width: 90%;
  max-width: 900px;
}

.prompt-content {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 20px;
  overflow-x: auto;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  white-space: normal;
  max-height: 60vh;
  overflow-y: auto;
}

.prompt-message {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.prompt-message:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.prompt-role {
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--primary-color, #ba003f);
  font-size: 16px;
}

.prompt-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

/* 特殊按钮样式 */
.prompt-button {
  background-color: white;
  color: var(--primary-color, #ba003f);
  border: 1px solid var(--primary-color, #ba003f);
  padding: 0 16px;
  height: 36px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.2s ease;
}

.prompt-button:hover {
  background-color: rgba(186, 0, 63, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(186, 0, 63, 0.1);
}

.prompt-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  color: #aaa;
  border-color: #e0e0e0;
  transform: none;
  box-shadow: none;
}

/* 添加流式输出相关样式 */
.streaming-indicator {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 5px 10px;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dot-typing {
  position: relative;
  left: -9999px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--primary-color, #ba003f);
  color: var(--primary-color, #ba003f);
  box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  animation: dot-typing 1.5s infinite linear;
}

@keyframes dot-typing {
  0% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  16.667% {
    box-shadow: 9984px -10px 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  33.333% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  50% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px -10px 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  66.667% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
  83.333% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px -10px 0 0 var(--primary-color, #ba003f);
  }
  100% {
    box-shadow: 9984px 0 0 0 var(--primary-color, #ba003f), 9999px 0 0 0 var(--primary-color, #ba003f), 10014px 0 0 0 var(--primary-color, #ba003f);
  }
}

/* 结果区域相关样式 */
.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
}

.result-section {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 650px;
}

.result-content-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
  height: 100%;
  min-height: 590px;
}

.note-result {
  position: relative;
  flex: 1;
  display: flex;
  height: 100%;
  width: 100%;
  overflow: hidden;
  background-color: #fcfcfc;
  border-radius: 0 0 8px 8px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.result-textarea {
  flex: 1;
  width: 100%;
  height: 100%;
  padding: 20px;
  border: none;
  resize: none;
  outline: none;
  background-color: #fcfcfc;
  font-size: 15px;
  line-height: 1.7;
  color: #333;
  overflow-y: auto;
  border-radius: 0 0 8px 8px;
  box-shadow: none;
  font-family: 'PingFang SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  transition: background-color 0.3s;
}

.result-textarea:focus {
  background-color: #fff;
}

/* 增加文本高亮样式 */
.result-textarea::selection {
  background-color: rgba(186, 0, 63, 0.2);
  color: #333;
}

/* 美化滚动条 */
.result-textarea::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.result-textarea::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

.result-textarea::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

.result-textarea::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}
</style> 