<template>
  <div class="longform-article-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>文章总结</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" title="知识学习" @click="showTips">
          <i class="ri-book-open-line"></i>
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
            输入参数
          </h3>
        </div>
        
        <div class="input-section-content">
          <!-- 文本输入支持直接输入和上传文件两种形式 -->
          <div class="form-group">
            <label for="text-input" class="form-control-label required">直接文本输入</label>
            <textarea 
              id="text-input" 
              v-model="textInput" 
              placeholder="请输入需要总结的文本内容（最多1000个汉字）..."
              class="form-control"
              rows="10"
              maxlength="1000"
            ></textarea>
            <div class="text-counter">{{textInput.length}}/1000</div>
          </div>
          
          <!-- 注释掉文件上传区域 -->
          <!--
          <div class="form-group">
            <label for="file-upload" class="form-control-label">上传文件</label>
            <div class="file-upload-container">
              <button class="file-upload-btn" disabled>
                <i class="ri-upload-2-line"></i>
                选择文件
              </button>
              <span class="file-upload-hint">文件上传功能暂不可用</span>
            </div>
          </div>
          -->
          
          <!-- 总结长度 -->
          <div class="form-group">
            <label class="form-control-label">总结长度</label>
            <div class="radio-group">
              <div class="radio-item" :class="{'radio-active': summaryLength === 'short'}">
                <input type="radio" v-model="summaryLength" value="short" name="summaryLength" id="length-short">
                <label class="radio-label" for="length-short">简短</label>
              </div>
              <div class="radio-item" :class="{'radio-active': summaryLength === 'medium'}">
                <input type="radio" v-model="summaryLength" value="medium" name="summaryLength" id="length-medium">
                <label class="radio-label" for="length-medium">中等</label>
              </div>
              <div class="radio-item" :class="{'radio-active': summaryLength === 'detailed'}">
                <input type="radio" v-model="summaryLength" value="detailed" name="summaryLength" id="length-detailed">
                <label class="radio-label" for="length-detailed">详细</label>
              </div>
              <div class="radio-item" :class="{'radio-active': summaryLength === 'comprehensive'}">
                <input type="radio" v-model="summaryLength" value="comprehensive" name="summaryLength" id="length-comprehensive">
                <label class="radio-label" for="length-comprehensive">全面</label>
              </div>
            </div>
          </div>
          
          <!-- 总结选项 -->
          <div class="form-group">
            <label class="form-control-label">总结选项</label>
            <div class="checkbox-group">
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.keyPoints}">
                <input type="checkbox" v-model="summaryOptions.keyPoints" id="keyPoints">
                <label class="checkbox-label" for="keyPoints">提取关键观点</label>
              </div>
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.keywords}">
                <input type="checkbox" v-model="summaryOptions.keywords" id="keywords">
                <label class="checkbox-label" for="keywords">包含关键词</label>
              </div>
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.outline}">
                <input type="checkbox" v-model="summaryOptions.outline" id="outline">
                <label class="checkbox-label" for="outline">生成文档大纲</label>
              </div>
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.takeaways}">
                <input type="checkbox" v-model="summaryOptions.takeaways" id="takeaways">
                <label class="checkbox-label" for="takeaways">包含核心要点</label>
              </div>
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.simpleLang}">
                <input type="checkbox" v-model="summaryOptions.simpleLang" id="simpleLang">
                <label class="checkbox-label" for="simpleLang">使用简明语言</label>
              </div>
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.stats}">
                <input type="checkbox" v-model="summaryOptions.stats" id="stats">
                <label class="checkbox-label" for="stats">包含文档统计</label>
              </div>
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.quotes}">
                <input type="checkbox" v-model="summaryOptions.quotes" id="quotes">
                <label class="checkbox-label" for="quotes">包含关键引述</label>
              </div>
              <div class="checkbox-item" :class="{'checkbox-active': summaryOptions.academic}">
                <input type="checkbox" v-model="summaryOptions.academic" id="academic">
                <label class="checkbox-label" for="academic">学术风格</label>
              </div>
            </div>
          </div>
          
          <!-- 模型选择 -->
          <div class="form-group">
            <label for="model" class="form-control-label">AI模型</label>
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
              {{ isGenerating ? '总结中...' : '开始总结' }}
            </button>
            <button @click="resetForm" class="btn btn-secondary">
              <i class="ri-refresh-line"></i>
              重置
            </button>
          </div>
        </div>
      </div>
      
      <!-- 右侧：结果 -->
      <div class="right-column">
        <!-- 总结结果 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              AI生成内容
            </h3>
            <div class="action-buttons">
              <button @click="generateLongform" class="primary-button" :disabled="isGenerating">
                <i class="ri-refresh-line" v-if="!isGenerating"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isGenerating ? '总结中...' : '再次总结' }}
              </button>
              <button @click="copyText" class="secondary-button" :disabled="isGenerating || !generatedNote">
                <i class="ri-file-copy-line"></i>
                复制文本
              </button>
              <button @click="showPrompt" class="secondary-button" :disabled="!lastUsedPrompt">
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
                <p class="empty-message">暂无总结内容，请点击"开始总结"按钮开始总结</p>
              </div>
            </div>
            
            <div v-else-if="generatedNote" class="note-result" :class="{'blur-content': isGenerating}">
              <textarea v-model="generatedNote" class="result-textarea" readonly></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 知识学习侧边抽屉 -->
    <el-drawer
      v-model="showTipsModal"
      title="文章总结创作指南"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in summaryKnowledge" :key="index" class="knowledge-section">
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
          <h3><i class="ri-file-text-line"></i> 总结提示词</h3>
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
import { summaryKnowledge } from '@/views/Knowledge_data.js';
import '@/assets/css/text-creation-common.css'; // 引入统一CSS样式文件

export default {
  name: 'Summary',
  data() {
    return {
      // 文本输入
      textInput: '',
      
      // 总结长度
      summaryLength: 'medium',
      
      // 总结选项
      summaryOptions: {
        keyPoints: true,
        keywords: true,
        outline: false,
        takeaways: true,
        simpleLang: true,
        stats: false,
        quotes: false,
        academic: false
      },
      
      // 结果内容
      isGenerating: false,
      loadingText: '正在总结文章，请耐心等待...',
      generatedNote: '',
      lastUsedPrompt: null,
      
      // 模态框控制
      showTipsModal: false,
      showPromptModal: false,
      
      // 模型选择 - 默认使用火山引擎V3
      selectedModel: 'deepseek-v3',
      modelList: [],
      
      // 添加知识库内容
      summaryKnowledge: summaryKnowledge,
      
      // 添加流式输出状态标记
      isStreaming: false,
    };
  },
  mounted() {
    this.fetchModelList();
  },
  methods: {
    // 获取可用的大模型列表
    async fetchModelList() {
      try {
        console.log('开始获取模型列表...');
        // 获取模型列表
        const response = await axios.get('/api/v1/llm/models', { timeout: 10000 });
        console.log('获取模型列表响应:', response.data);
        
        if (response.data && response.data.status === 'success') {
          // 获取API返回的所有模型
          const allModels = response.data.data || [];
          console.log('API返回的模型列表:', allModels);
          
          // 只保留火山引擎的R1、V3和豆包大模型
          this.modelList = allModels.filter(model => 
            model.id === 'deepseek-v3' || 
            model.id === 'deepseek-r1' || 
            model.id === 'doubi-doupo'
          );
          
          console.log('过滤后的可用模型列表:', this.modelList);
          
          // 如果没有模型，添加默认模型
          if (this.modelList.length === 0) {
            console.log('未找到可用模型，使用默认模型');
            this.modelList.push({ id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' });
          }
          
          // 默认选择火山引擎V3
          const volcanoModel = this.modelList.find(model => model.id === 'deepseek-v3');
          this.selectedModel = volcanoModel ? volcanoModel.id : (this.modelList[0] ? this.modelList[0].id : 'deepseek-v3');
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
    
    // 设置默认模型列表
    setupDefaultModels() {
      console.log('使用默认模型列表');
      this.modelList = [
        { id: 'deepseek-v3', name: '火山引擎 DeepSeek V3' },
        { id: 'deepseek-r1', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'doubi-doupo', name: '豆包大模型' }
        // 以下模型已注释掉
        // { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        // { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        // { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      this.selectedModel = 'deepseek-v3';
    },
    
    // 生成总结结果的方法
    async generateLongform() {
      // 验证必填字段
      if (!this.validateForm()) {
        return;
      }
      
      this.isGenerating = true;
      this.generatedNote = '';
      
      try {
        // 构建提示词
        const prompt = this.generatePrompt();
        
        // 保存提示词供后续显示
        this.lastUsedPrompt = [
          { role: "system", content: "你是一位专业的文章总结专家，能够提供准确、精炼的文章摘要和关键内容提炼。" },
          { role: "user", content: prompt }
        ];
        
        this.loadingText = '正在总结文章，请耐心等待...';
        
        // 确保选择了模型
        if (!this.selectedModel) {
          this.selectedModel = 'deepseek-v3';
          console.log('未选择模型，已自动选择默认模型');
        }
        
        // 准备API请求参数
        const apiParams = {
          model: this.selectedModel,
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        console.log('API请求参数:', JSON.stringify(apiParams));
        
        try {
          // 开始流式状态
          this.isStreaming = true;
          
          // 发送API请求，使用fetch API来处理流式响应
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
                    throw new Error(parsed.error.message || '生成总结失败');
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
          
          // 处理完成，移除流式状态
          this.isStreaming = false;
          console.log('流式响应处理完成，生成的内容长度:', this.generatedNote.length);
          
          // 成功提示
          this.$message ? this.$message.success('文章总结完成！') : alert('文章总结完成！');
          
        } catch (error) {
          // 结束流式状态
          this.isStreaming = false;
          console.error('API调用异常:', error);
          throw error;
        }
      } catch (error) {
        console.error('生成总结结果出错，详细错误:', error);
        
        // 更详细的错误日志
        if (error.response) {
          // 服务器响应了，但状态码不在2xx范围
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
          this.$message ? 
            this.$message.error(`总结失败: 服务器错误 (${error.response.status})`) : 
            alert(`总结失败: 服务器错误 (${error.response.status})`);
        } else if (error.request) {
          // 请求已发送但没有收到响应
          console.error('未收到服务器响应');
          this.$message ? 
            this.$message.error('总结失败: 服务器无响应，请检查网络连接') : 
            alert('总结失败: 服务器无响应，请检查网络连接');
        } else {
          // 设置请求时发生错误
          console.error('错误信息:', error.message);
          this.$message ? 
            this.$message.error(`总结失败: ${error.message}`) : 
            alert(`总结失败: ${error.message}`);
        }
        
        // 开发模式下使用示例内容
        if (process.env.NODE_ENV === 'development') {
          console.log('开发模式：使用示例内容');
          this.generatedNote = `文章总结：\n\n【摘要】\n这篇文章主要讨论了人工智能在现代社会中的应用及其影响。作者深入分析了AI技术如何改变各行各业的工作方式，并探讨了这一技术革命带来的伦理和社会挑战。\n\n【关键观点】\n• AI技术正在各行各业快速普及，从医疗到金融领域都有突破性应用\n• 机器学习算法不断进步，使AI系统能够处理复杂的决策任务\n• 数据隐私和算法偏见是AI发展面临的主要伦理挑战\n• 需要建立完善的监管框架来引导AI的健康发展\n\n【核心要点】\n1. 技术现状：文章详细介绍了深度学习、自然语言处理和计算机视觉等AI技术的最新进展\n2. 行业应用：分析了AI在医疗诊断、金融风险评估和智能制造中的具体应用案例\n3. 社会影响：探讨了AI对就业市场的冲击，预测某些工作岗位将被自动化取代\n4. 未来展望：提出了"人机协作"模式可能是未来工作的主要形式\n\n【文档统计】\n• 原文字数：约5000字\n• 段落数：15段\n• 主要章节：4个\n• 引用来源：12处\n\n【总结】\n作者认为，虽然AI技术带来了巨大的社会变革和挑战，但通过合理的政策引导和伦理约束，人工智能有望成为推动人类社会进步的积极力量。关键在于如何平衡技术创新与伦理考量，确保AI发展方向符合人类共同利益。`;
        }
      } finally {
        this.isGenerating = false;
      }
    },
    
    // 验证表单
    validateForm() {
      if (!this.textInput.trim()) {
        this.$message ? this.$message.error('请输入需要总结的文本内容') : alert('请输入需要总结的文本内容');
        return false;
      }
      
      return true;
    },
    
    // 生成提示词
    generatePrompt() {
      let prompt = '请对以下文本进行总结：\n\n';
      
      // 添加文本内容
      prompt += `${this.textInput}\n\n`;
      
      // 添加总结长度
      prompt += '总结长度要求：\n';
      switch (this.summaryLength) {
        case 'short':
          prompt += '- 简短：请提供简短的总结，约原文的10%长度\n';
          break;
        case 'medium':
          prompt += '- 中等：请提供中等长度的总结，约原文的20%长度\n';
          break;
        case 'detailed':
          prompt += '- 详细：请提供详细的总结，约原文的30%长度\n';
          break;
        case 'comprehensive':
          prompt += '- 全面：请提供全面的总结，约原文的40%长度\n';
          break;
        default:
          prompt += '- 中等：请提供中等长度的总结，约原文的20%长度\n';
      }
      
      // 添加总结选项
      prompt += '\n请根据以下选项进行总结：\n';
      
      if (this.summaryOptions.keyPoints) {
        prompt += '- 提取关键观点：识别并列出文章中的主要观点和论点\n';
      }
      
      if (this.summaryOptions.keywords) {
        prompt += '- 包含关键词：提取并列出文章中的核心关键词\n';
      }
      
      if (this.summaryOptions.outline) {
        prompt += '- 生成文档大纲：创建一个简洁的文档结构大纲\n';
      }
      
      if (this.summaryOptions.takeaways) {
        prompt += '- 包含核心要点：总结文章中最重要的信息和要点\n';
      }
      
      if (this.summaryOptions.simpleLang) {
        prompt += '- 使用简明语言：使用清晰、简洁的语言表达\n';
      }
      
      if (this.summaryOptions.stats) {
        prompt += '- 包含文档统计：提供关于原文的统计信息（如字数、段落数等）\n';
      }
      
      if (this.summaryOptions.quotes) {
        prompt += '- 包含关键引述：引用原文中重要的句子或段落\n';
      }
      
      if (this.summaryOptions.academic) {
        prompt += '- 学术风格：使用正式的学术语言和格式\n';
      }
      
      // 输出要求
      prompt += '\n请提供结构化的总结，包括摘要部分和根据选择的选项组织的内容部分。确保总结准确反映原文的核心内容和论点。\n';
      
      return prompt;
    },
    
    // 重置表单
    resetForm() {
      this.textInput = '';
      // 重置总结选项为默认值
      this.summaryLength = 'medium';
      this.summaryOptions = {
        keyPoints: true,
        keywords: true,
        outline: false,
        takeaways: true,
        simpleLang: true,
        stats: false,
        quotes: false,
        academic: false
      };
      this.generatedNote = '';
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
      element.download = `总结结果_${new Date().toISOString().slice(0,10)}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    
    // 显示创作小贴士
    showTips() {
      this.showTipsModal = true;
    },
    
    // 格式化Markdown文本的方法
    formatMarkdown(text) {
      if (!text) return '';
      
      // 处理加粗文本
      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理列表项
      text = text.replace(/\n\n/g, '<br><br>');
      
      return text;
    }
  }
};
</script>

<style scoped>
/* 导入通用样式 */
@import '~@/assets/css/text-creation-common.css';

/* 优化左侧输入区域 */
.input-section {
  width: 45%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.input-section-content {
  padding: 16px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 18px;
}

.form-control-label {
  margin-bottom: 10px;
  font-size: 15px;
  font-weight: 500;
}

textarea.form-control {
  padding: 12px;
  font-size: 15px;
  line-height: 1.6;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  background-color: #fafafa;
  min-height: 180px;
  transition: all 0.3s;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

textarea.form-control:focus {
  border-color: var(--primary-color, #ba003f);
  background-color: #fff;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05), 0 0 0 3px rgba(186, 0, 63, 0.1);
}

.btn {
  padding: 10px 18px;
  font-size: 15px;
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  border: none;
  font-weight: 500;
}

.btn i {
  font-size: 18px;
}

.btn-primary {
  background-color: var(--primary-color, #ba003f);
  color: white;
  box-shadow: 0 2px 5px rgba(186, 0, 63, 0.2);
}

.btn-primary:hover {
  background-color: #cf0046;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.3);
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #555;
  border: 1px solid #e0e0e0;
}

.btn-secondary:hover {
  background-color: #e8e8e8;
  color: #333;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

/* 仅保留与通用CSS不重复的特殊样式 */
/* 文本计数器 */
.text-counter {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

/* 文件上传容器 */
.file-upload-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.file-upload-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  color: #666;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.file-upload-btn:hover:not(:disabled) {
  background-color: #eaeaea;
  color: var(--primary-color, #ba003f);
}

.file-upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.file-upload-hint {
  font-size: 13px;
  color: #999;
  font-style: italic;
}

/* 优化右侧布局结构 */
.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
}

/* 优化总结结果区域 */
.result-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  height: 100%;
}

.result-content-wrapper {
  flex-grow: 1;
  position: relative;
  padding: 0;
  display: flex;
  flex-direction: column;
  min-height: 500px;
}

.note-result {
  height: 100%;
  flex-grow: 1;
  display: flex;
  padding: 16px;
}

.result-textarea {
  width: 100%;
  height: 100%;
  min-height: 500px;
  padding: 16px;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  background-color: #fafafa;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  resize: none;
  overflow-y: auto;
  white-space: pre-wrap;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.result-textarea:focus {
  outline: none;
  border-color: var(--primary-color, #ba003f);
  background-color: #fff;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05), 0 0 0 3px rgba(186, 0, 63, 0.1);
}

.result-textarea::-webkit-scrollbar {
  width: 8px;
}

.result-textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.result-textarea::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}

.result-textarea::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}

.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  flex-grow: 1;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 6px;
  margin: 10px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 10;
  border-radius: 6px;
}

/* 提示词模态框样式 */
.prompt-modal {
  width: 90%;
  max-width: 800px;
}

.prompt-content {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  max-height: 60vh;
  overflow-y: auto;
  margin-bottom: 15px;
  border: 1px solid #eee;
}

.prompt-message {
  margin-bottom: 20px;
}

.prompt-role {
  font-weight: 600;
  margin-bottom: 5px;
  color: var(--primary-color, #ba003f);
}

.prompt-text {
  white-space: pre-wrap;
  font-family: monospace;
  background-color: white;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #eee;
  font-size: 14px;
  line-height: 1.5;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section, 
  .right-column {
    width: 100%;
  }
  
  .result-content-wrapper {
    min-height: 300px;
  }
  
  .result-textarea {
    min-height: 300px;
  }
}
</style> 