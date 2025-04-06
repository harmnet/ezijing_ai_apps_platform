<template>
  <div class="meeting-minutes-container">
    <h1 class="page-title">AI会议纪要</h1>
    
    <el-steps :active="currentStep" finish-status="success" class="steps" process-status="process">
      <el-step title="上传音频" description="上传会议录音文件"></el-step>
      <el-step title="音频转文本" description="将录音转换为文字内容"></el-step>
      <el-step title="生成会议纪要" description="AI智能生成纪要内容"></el-step>
    </el-steps>
    
    <!-- 步骤1: 上传音频 -->
    <div v-if="currentStep === 0" class="step-content">
      <el-card class="upload-card">
        <div class="upload-area">
          <el-upload
            class="audio-uploader"
            drag
            :auto-upload="false"
            :show-file-list="true"
            :limit="1"
            :on-change="handleFileChange"
            :on-exceed="handleExceed"
            :on-remove="handleRemove"
            accept=".mp3,.wav,.ogg,.flac,.m4a"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">拖拽文件到此处或 <em>点击上传</em></div>
            <template #tip>
              <div class="el-upload__tip">
                支持 MP3、WAV、OGG、FLAC、M4A 格式音频文件
              </div>
            </template>
          </el-upload>
        </div>
        
        <div class="file-info" v-if="audioFile">
          <h3>已选择文件</h3>
          <p><strong>文件名：</strong>{{ audioFile.name }}</p>
          <p><strong>文件大小：</strong>{{ formatFileSize(audioFile.size) }}</p>
          <p><strong>文件类型：</strong>{{ audioFile.type || '未知' }}</p>
          <p class="tips">* 大文件处理需要更长时间，请耐心等待</p>
        </div>
        
        <div class="action-buttons">
          <el-button 
            type="primary" 
            :disabled="!audioFile || isProcessing" 
            @click="startTranscription" 
            class="primary-btn"
            :loading="isProcessing"
          >
            {{ isProcessing ? '转录中...' : '开始转录' }}
          </el-button>
        </div>
      </el-card>
    </div>
    
    <!-- 步骤2: 音频转文本 -->
    <div v-if="currentStep === 1" class="step-content">
      <el-card class="transcription-card">
        <div class="progress-area" v-if="isProcessing">
          <div class="progress-spinner">
            <el-progress 
              type="circle" 
              :percentage="processingProgress" 
              :stroke-width="6"
              :status="processingProgress === 100 ? 'success' : ''"
              color="#ba003f"
            />
          </div>
          <p class="progress-text">{{ processingMessage }}</p>
          <div class="estimate-time" v-if="processingProgress < 100">
            <p>预计剩余时间: {{ estimatedTimeRemaining }}</p>
            <div class="processing-tips">
              <p>音频转换可能需要一些时间，您可以：</p>
              <ul>
                <li>如有较长音频，可以先准备好会议大纲</li>
                <li>长音频处理时请勿关闭或刷新页面</li>
                <li>转换速度取决于音频长度和质量</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="text-output" v-if="transcript">
          <h3>转录结果</h3>
          <div class="transcript-container">
            <p v-if="streamingText" class="streaming-text">{{ streamingText }}</p>
            <p v-else class="full-text">{{ transcript }}</p>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button @click="currentStep--" :disabled="isProcessing">上一步</el-button>
          <el-button 
            type="primary" 
            :disabled="!transcript || isGenerating" 
            @click="generateMinutes" 
            class="primary-btn"
            :loading="isGenerating"
          >
            {{ isGenerating ? '生成中...' : '生成会议纪要' }}
          </el-button>
        </div>
      </el-card>
    </div>
    
    <!-- 步骤3: 生成会议纪要 -->
    <div v-if="currentStep === 2" class="step-content">
      <el-card class="minutes-card">
        <div class="progress-area" v-if="isGenerating">
          <div class="progress-spinner">
            <el-progress 
              type="circle" 
              :percentage="generatingProgress" 
              :stroke-width="6"
              :status="generatingProgress === 100 ? 'success' : ''"
              color="#ba003f"
            />
          </div>
          <p class="progress-text">{{ generatingMessage }}</p>
          <div class="estimate-time" v-if="generatingProgress < 100">
            <p>预计剩余时间: {{ estimatedTimeRemainingGeneration }}</p>
            <div class="pulse-animation">AI 正在思考中...</div>
            <div class="generating-stages" v-if="generatingStage">
              <div class="stage-indicator">{{ generatingStage }}</div>
            </div>
          </div>
        </div>
        
        <div class="minutes-result" v-if="minutes">
          <div class="minutes-header">
            <h3>会议纪要</h3>
            <div class="minutes-actions">
              <el-button type="primary" size="small" @click="copyMinutes" class="action-btn">
                <el-icon><document-copy /></el-icon> 复制
              </el-button>
              <el-button type="success" size="small" @click="downloadMinutes" class="action-btn">
                <el-icon><download /></el-icon> 下载
              </el-button>
            </div>
          </div>
          
          <div class="minutes-content" v-html="formattedMinutes"></div>
        </div>
        
        <div class="action-buttons">
          <el-button @click="currentStep--" :disabled="isGenerating">上一步</el-button>
          <el-button 
            type="primary" 
            @click="startOver" 
            class="primary-btn"
            :disabled="isGenerating"
          >完成</el-button>
        </div>
      </el-card>
    </div>
    
    <!-- 全局错误提示 -->
    <el-dialog
      v-model="errorDialogVisible"
      title="处理出错"
      width="30%"
      :show-close="true"
      :close-on-click-modal="true"
      class="error-dialog"
    >
      <div class="error-content">
        <el-icon class="error-icon" color="#F56C6C" :size="64"><circle-close /></el-icon>
        <p class="error-message">{{ errorMessage }}</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="errorDialogVisible = false" :disabled="isRetrying">关闭</el-button>
          <el-button 
            type="primary" 
            @click="handleErrorRetry" 
            class="primary-btn" 
            :loading="isRetrying"
          >重试</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onBeforeUnmount } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import { 
  UploadFilled, 
  DocumentCopy, 
  Download, 
  CircleClose 
} from '@element-plus/icons-vue';

export default {
  name: 'MeetingMinutes',
  components: {
    UploadFilled,
    DocumentCopy,
    Download,
    CircleClose
  },
  setup() {
    const toast = useToast();
    
    // 状态变量
    const currentStep = ref(0);
    const audioFile = ref(null);
    const transcript = ref('');
    const streamingText = ref('');
    const minutes = ref('');
    const isProcessing = ref(false);
    const isGenerating = ref(false);
    const processingProgress = ref(0);
    const generatingProgress = ref(0);
    const processingMessage = ref('正在处理音频...');
    const generatingMessage = ref('正在分析会议内容...');
    const errorDialogVisible = ref(false);
    const errorMessage = ref('');
    const errorRetryFunction = ref(null);
    const estimatedTimeRemaining = ref('计算中...');
    const estimatedTimeRemainingGeneration = ref('计算中...');
    const generatingStage = ref('');
    const isRetrying = ref(false);
    
    // 生成阶段提示
    const generatingStages = [
      '分析会议内容结构...',
      '提取关键讨论点...',
      '识别参会人员...',
      '整理议题和决议...',
      '形成会议结论...',
      '生成任务和行动计划...',
      '格式化最终纪要...'
    ];
    
    // 用于管理事件源连接
    let eventSource = null;
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // 格式化会议纪要 (去除markdown代码块标记并改进格式化逻辑)
    const formattedMinutes = computed(() => {
      if (!minutes.value) return '';
      
      // 首先移除markdown代码块标记
      let content = minutes.value
        .replace(/```markdown/g, '')
        .replace(/```/g, '');
      
      // 预处理：移除多余空行（连续两个以上的空行替换为一个）
      content = content.replace(/\n\s*\n\s*\n+/g, '\n\n');
      
      // 替换标题
      let formatted = content
        .replace(/^#\s+(.*?)$/gm, '<h2>$1</h2>')
        .replace(/^##\s+(.*?)$/gm, '<h3>$1</h3>')
        .replace(/^###\s+(.*?)$/gm, '<h4>$1</h4>');
      
      // 替换列表
      formatted = formatted
        .replace(/^\*\s+(.*?)$/gm, '<li>$1</li>')
        .replace(/^\d+\.\s+(.*?)$/gm, '<li>$1</li>');
      
      // 将连续的li元素包装在ul中
      let lines = formatted.split('\n');
      let inList = false;
      let result = [];
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        // 跳过空行
        if (line === '') continue;
        
        if (line.startsWith('<li>')) {
          if (!inList) {
            result.push('<ul>');
            inList = true;
          }
          result.push(line);
        } else {
          if (inList) {
            result.push('</ul>');
            inList = false;
          }
          result.push(line);
        }
      }
      
      if (inList) {
        result.push('</ul>');
      }
      
      formatted = result.join('\n');
      
      // 添加段落标签
      formatted = formatted
        .replace(/^(?!<h|<li|<ul|<\/ul)(.*?)$/gm, '<p>$1</p>');
      
      // 清理空段落
      formatted = formatted.replace(/<p>\s*<\/p>/g, '');
      
      return formatted;
    });
    
    // 处理文件选择变更
    const handleFileChange = (file) => {
      audioFile.value = file.raw;
    };
    
    // 处理超出文件数量限制
    const handleExceed = () => {
      toast.error('只能上传一个音频文件');
    };
    
    // 处理移除文件
    const handleRemove = () => {
      audioFile.value = null;
    };
    
    // 更新估计剩余时间
    const updateEstimatedTime = (startTime, progressRef, estimatedTimeRef, totalTime) => {
      const elapsed = Date.now() - startTime;
      const progress = progressRef.value / 100;
      
      if (progress <= 0.05) {
        estimatedTimeRef.value = '计算中...';
        return;
      }
      
      const remaining = progress < 1 ? (elapsed / progress) * (1 - progress) : 0;
      
      if (remaining <= 0) {
        estimatedTimeRef.value = '即将完成';
        return;
      }
      
      // 格式化时间
      const minutes = Math.floor(remaining / 60000);
      const seconds = Math.floor((remaining % 60000) / 1000);
      
      if (minutes > 0) {
        estimatedTimeRef.value = `约 ${minutes} 分 ${seconds} 秒`;
      } else {
        estimatedTimeRef.value = `约 ${seconds} 秒`;
      }
    };
    
    // 更新生成阶段提示
    const updateGeneratingStage = (progress) => {
      const stageIndex = Math.min(
        Math.floor((progress / 100) * generatingStages.length),
        generatingStages.length - 1
      );
      generatingStage.value = generatingStages[stageIndex];
    };
    
    // 开始音频转文字流程
    const startTranscription = async () => {
      if (!audioFile.value) {
        toast.error('请先上传音频文件');
        return;
      }
      
      isProcessing.value = true;
      processingProgress.value = 0;
      processingMessage.value = '正在处理音频...';
      streamingText.value = '';
      transcript.value = '';
      estimatedTimeRemaining.value = '计算中...';
      
      try {
        // 准备FormData
        const formData = new FormData();
        formData.append('audio_file', audioFile.value);
        formData.append('streaming', 'true');
        
        // 初始化时间和进度
        const startTime = Date.now();
        const estimatedTotalTime = audioFile.value.size > 10 * 1024 * 1024 ? 60000 : 30000; // 大文件预估60秒，小文件30秒
        
        // 初始化进度更新器
        let progressInterval = startProgressAnimation(
          processingProgress, 
          95, 
          estimatedTotalTime,
          () => updateEstimatedTime(startTime, processingProgress, estimatedTimeRemaining, estimatedTotalTime)
        );
        
        // 使用EventSource处理流式响应
        const url = '/api/v1/api/audio-to-text';
        const response = await fetch(url, {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) {
          throw new Error(`服务器响应错误: ${response.status}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 读取流
        const readStream = async () => {
          const { done, value } = await reader.read();
          
          if (done) {
            clearInterval(progressInterval);
            processingProgress.value = 100;
            processingMessage.value = '转录完成';
            estimatedTimeRemaining.value = '0秒';
            
            // 确保我们有最终结果
            if (!transcript.value && streamingText.value) {
              transcript.value = streamingText.value;
            }
            
            setTimeout(() => {
              currentStep.value++;
              isProcessing.value = false;
            }, 1000);
            
            return;
          }
          
          // 解码数据
          const text = decoder.decode(value, { stream: true });
          buffer += text;
          
          // 处理收到的数据行
          const lines = buffer.split('\n');
          buffer = lines.pop(); // 保留可能不完整的最后一行
          
          for (const line of lines) {
            if (line.trim() === '') continue;
            
            try {
              if (line.startsWith('data: ')) {
                const jsonData = JSON.parse(line.substring(6));
                
                if (jsonData.code === 200 && jsonData.data && jsonData.data.text) {
                  streamingText.value = jsonData.data.text;
                  
                  // 当接收到最终消息时，保存完整文本
                  if (jsonData.message === '转换完成') {
                    transcript.value = jsonData.data.text;
                  }
                } else if (jsonData.code !== 200) {
                  throw new Error(jsonData.message || '转换失败');
                }
              }
            } catch (e) {
              console.error('解析数据失败:', e, line);
            }
          }
          
          // 继续读取
          return readStream();
        };
        
        await readStream();
        
      } catch (error) {
        showError(`音频转换失败: ${error.message}`, startTranscription);
        isProcessing.value = false;
      }
    };
    
    // 生成会议纪要
    const generateMinutes = async () => {
      if (!transcript.value) {
        toast.error('没有转录文本，无法生成会议纪要');
        return;
      }
      
      isGenerating.value = true;
      generatingProgress.value = 0;
      generatingMessage.value = '正在分析会议内容...';
      minutes.value = '';
      estimatedTimeRemainingGeneration.value = '计算中...';
      
      try {
        // 使用Toast显示分步骤进度
        const progressToast = toast.info(
          `阶段 1/3: 分析会议内容...`, 
          { timeout: false, closeButton: false }
        );
        
        // 初始化总体时间和进度
        const startTime = Date.now();
        const totalEstimatedTime = Math.min(transcript.value.length * 20, 30000);
        const stepsTime = [
          totalEstimatedTime * 0.3, // 分析阶段占30%
          totalEstimatedTime * 0.6, // 生成阶段占60%
          totalEstimatedTime * 0.1  // 格式化阶段占10%
        ];
        
        // 阶段1: 分析会议内容
        generatingStage.value = generatingStages[0];
        
        let progressInterval = startProgressAnimation(
          generatingProgress,
          30, // 第一阶段到30%
          stepsTime[0],
          () => {
            updateEstimatedTime(startTime, generatingProgress, estimatedTimeRemainingGeneration, totalEstimatedTime);
            updateGeneratingStage(generatingProgress.value);
          }
        );
        
        // 在阶段1完成时更新Toast通知
        await new Promise(resolve => setTimeout(resolve, stepsTime[0]));
        clearInterval(progressInterval);
        toast.dismiss(progressToast);
        
        // 阶段2: 提取关键信息并生成纪要
        const stage2Toast = toast.info(
          `阶段 2/3: 生成会议纪要...`, 
          { timeout: false, closeButton: false }
        );
        generatingMessage.value = '正在生成会议纪要...';
        generatingStage.value = generatingStages[2]; // 提取关键讨论点
        
        progressInterval = startProgressAnimation(
          generatingProgress,
          80, // 第二阶段到80%
          stepsTime[1],
          () => {
            updateEstimatedTime(
              startTime + stepsTime[0], 
              { value: generatingProgress.value - 30 }, 
              estimatedTimeRemainingGeneration, 
              stepsTime[1]
            );
            // 随着进度更新不同的生成阶段
            const stageIndex = Math.floor(((generatingProgress.value - 30) / 50) * 4) + 2;
            generatingStage.value = generatingStages[Math.min(stageIndex, 5)];
            
            // 更新Toast内容以显示当前子阶段
            toast.update(stage2Toast, {
              content: `阶段 2/3: ${generatingStage.value}`
            });
          }
        );
        
        // 构建提示词
        const prompt = `
          请根据以下会议转录内容，生成一份结构清晰、要点明确的会议纪要。
          纪要应包含以下部分：
          1. 会议主题和基本信息
          2. 参会人员（从对话中推断）
          3. 会议讨论的主要议题（按重要性排序）
          4. 每个议题的关键讨论要点
          5. 达成的决议或结论
          6. 分配的任务和负责人（如有）
          7. 下一步行动计划（如有）

          转录内容：
          ${transcript.value}
          
          请以Markdown格式输出，使用适当的标题层级、列表和强调。保持专业、简明的风格，过滤掉无关内容，只保留对理解会议实质内容有帮助的信息。
          注意：
          1. 不要在输出中包含markdown代码块标记如 \`\`\`markdown 或 \`\`\`，直接输出纯markdown内容
          2. 避免使用过多空行，段落之间最多保留一个空行
          3. 保持简洁清晰的格式，减少不必要的换行
        `;
        
        // 打印请求信息便于调试
        console.log("发送LLM请求:", {
          model: 'deepseek-v3-vol',
          temperature: 0.3,
          max_tokens: 2000,
          messageLength: prompt.length
        });
        
        // 调用后端LLM服务
        try {
          const response = await axios.post('/api/v1/llm/chat', {
            model: 'deepseek-v3-vol', // 使用DeepSeek-V3火山引擎模型
            messages: [
              { role: "user", content: prompt }
            ],
            temperature: 0.3, // 较低的温度，使输出更确定性
            max_tokens: 2000
          });
          
          console.log("LLM响应:", response.data);
          clearInterval(progressInterval);
          toast.dismiss(stage2Toast);
          
          if (response.data && response.data.data && response.data.data.choices && response.data.data.choices.length > 0) {
            // 阶段3: 格式化最终内容
            const stage3Toast = toast.info(
              `阶段 3/3: 格式化会议纪要...`, 
              { timeout: false, closeButton: false }
            );
            generatingMessage.value = '正在整理会议纪要格式...';
            generatingStage.value = generatingStages[6]; // 格式化最终纪要
            
            // 获取原始会议纪要内容
            let rawMinutes = response.data.data.choices[0].message.content;
            
            // 预处理：移除多余空行
            rawMinutes = rawMinutes.replace(/\n\s*\n\s*\n+/g, '\n\n');
            
            progressInterval = startProgressAnimation(
              generatingProgress,
              100, // 最后阶段到100%
              stepsTime[2],
              () => {
                updateEstimatedTime(
                  startTime + stepsTime[0] + stepsTime[1],
                  { value: (generatingProgress.value - 80) * 5 }, // 缩放到0-100
                  estimatedTimeRemainingGeneration,
                  stepsTime[2]
                );
              }
            );
            
            await new Promise(resolve => setTimeout(resolve, stepsTime[2] * 0.8));
            
            // 设置会议纪要内容
            minutes.value = rawMinutes;
            clearInterval(progressInterval);
            toast.dismiss(stage3Toast);
            
            generatingProgress.value = 100;
            generatingMessage.value = '会议纪要生成完成';
            estimatedTimeRemainingGeneration.value = '0秒';
            
            toast.success('会议纪要生成完成！', { timeout: 3000 });
            
            setTimeout(() => {
              currentStep.value++;
              isGenerating.value = false;
            }, 1000);
          } else {
            throw new Error('获取会议纪要失败，服务器返回格式不正确: ' + JSON.stringify(response.data));
          }
        } catch (apiError) {
          console.error("API调用错误:", apiError);
          
          // 尝试检查错误响应的详细信息
          let errorMessage = "API调用失败";
          if (apiError.response) {
            // 服务器返回了响应
            console.error("错误响应状态:", apiError.response.status);
            console.error("错误响应数据:", apiError.response.data);
            errorMessage = `服务器错误 (${apiError.response.status}): ${JSON.stringify(apiError.response.data || {})}`;
          } else if (apiError.request) {
            // 请求已发送但未收到响应
            console.error("未收到响应:", apiError.request);
            errorMessage = "未收到服务器响应，请检查网络连接";
          } else {
            // 设置请求时出错
            console.error("请求错误:", apiError.message);
            errorMessage = `请求错误: ${apiError.message}`;
          }
          
          throw new Error(errorMessage);
        }
        
      } catch (error) {
        console.error("生成会议纪要异常:", error);
        if (progressInterval) clearInterval(progressInterval);
        showError(`生成会议纪要失败: ${error.message}`, generateMinutes);
        isGenerating.value = false;
        toast.error('会议纪要生成失败', { timeout: 3000 });
      }
    };
    
    // 复制会议纪要
    const copyMinutes = () => {
      if (!minutes.value) return;
      
      navigator.clipboard.writeText(minutes.value)
        .then(() => {
          toast.success('会议纪要已复制到剪贴板');
        })
        .catch(err => {
          toast.error('复制失败: ' + err.message);
        });
    };
    
    // 下载会议纪要
    const downloadMinutes = () => {
      if (!minutes.value) return;
      
      const fileName = `会议纪要_${new Date().toISOString().substring(0, 10)}.md`;
      const blob = new Blob([minutes.value], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      toast.success(`会议纪要已下载: ${fileName}`);
    };
    
    // 显示错误对话框
    const showError = (message, retryFunction = null) => {
      errorMessage.value = message;
      errorRetryFunction.value = retryFunction;
      errorDialogVisible.value = true;
    };
    
    // 处理错误重试
    const handleErrorRetry = async () => {
      if (isRetrying.value) return;
      
      isRetrying.value = true;
      errorDialogVisible.value = false;
      
      try {
        if (typeof errorRetryFunction.value === 'function') {
          await errorRetryFunction.value();
        }
      } finally {
        isRetrying.value = false;
      }
    };
    
    // 重新开始流程
    const startOver = () => {
      audioFile.value = null;
      transcript.value = '';
      streamingText.value = '';
      minutes.value = '';
      currentStep.value = 0;
    };
    
    // 启动进度条动画
    const startProgressAnimation = (progressRef, targetValue, duration, callback = null) => {
      const startTime = Date.now();
      const startValue = progressRef.value;
      
      return setInterval(() => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(1, elapsed / duration);
        progressRef.value = Math.round(startValue + (targetValue - startValue) * progress);
        
        if (progress >= 1) {
          progressRef.value = targetValue;
        }
        
        if (callback && typeof callback === 'function') {
          callback();
        }
      }, 100);
    };
    
    // 组件销毁前清理事件源
    onBeforeUnmount(() => {
      if (eventSource) {
        eventSource.close();
      }
    });
    
    return {
      currentStep,
      audioFile,
      transcript,
      streamingText,
      minutes,
      formattedMinutes,
      isProcessing,
      isGenerating,
      processingProgress,
      generatingProgress,
      processingMessage,
      generatingMessage,
      errorDialogVisible,
      errorMessage,
      formatFileSize,
      handleFileChange,
      handleExceed,
      handleRemove,
      startTranscription,
      generateMinutes,
      copyMinutes,
      downloadMinutes,
      handleErrorRetry,
      startOver,
      estimatedTimeRemaining,
      estimatedTimeRemainingGeneration,
      generatingStage,
      isRetrying
    };
  }
};
</script>

<style>
:root {
  --primary-color: #ba003f;
  --primary-hover: #d4124d;
  --primary-active: #9a0035;
  --primary-light: #f3c1d1;
  --primary-lighter: #f9e0e8;
  --primary-bg: #fdf2f5;
  --white: #ffffff;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --gray-300: #dee2e6;
  --gray-400: #ced4da;
  --gray-500: #adb5bd;
  --gray-600: #6c757d;
  --gray-700: #495057;
  --gray-800: #343a40;
  --gray-900: #212529;
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.1);
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
}

/* 修改Element Plus主题色 */
.el-button--primary {
  --el-button-bg-color: var(--primary-color) !important;
  --el-button-border-color: var(--primary-color) !important;
  --el-button-hover-bg-color: var(--primary-hover) !important;
  --el-button-hover-border-color: var(--primary-hover) !important;
  --el-button-active-bg-color: var(--primary-active) !important;
  --el-button-active-border-color: var(--primary-active) !important;
}

.el-button--default {
  color: var(--gray-700) !important;
  border-color: var(--gray-400) !important;
}

.el-button--default:hover {
  color: var(--primary-color) !important;
  border-color: var(--primary-light) !important;
  background-color: var(--primary-bg) !important;
}

.el-step__head.is-process {
  color: var(--primary-color) !important;
  border-color: var(--primary-color) !important;
}

.el-step__title.is-process {
  color: var(--primary-color) !important;
  font-weight: 600 !important;
}

.el-step__description.is-process {
  color: var(--primary-color) !important;
}

.el-step__head.is-wait {
  color: var(--gray-400) !important;
}

.el-step__title.is-wait {
  color: var(--gray-500) !important;
}

.el-progress-circle__path {
  stroke: var(--primary-color) !important;
}

.el-upload-dragger {
  background-color: var(--white) !important;
}

.el-card {
  border: none !important;
  background-color: var(--white) !important;
  box-shadow: var(--shadow-md) !important;
  transition: box-shadow 0.3s ease !important;
}

.el-card:hover {
  box-shadow: var(--shadow-lg) !important;
}
</style>

<style scoped>
.meeting-minutes-container {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: var(--gray-100);
  min-height: calc(100vh - 100px);
  border-radius: var(--border-radius-lg);
}

.page-title {
  text-align: center;
  margin-bottom: 40px;
  color: var(--primary-color);
  font-weight: bold;
  font-size: 32px;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  position: relative;
  padding-bottom: 15px;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 3px;
}

.steps {
  margin-bottom: 50px;
  padding: 10px 20px 30px;
  background-color: var(--white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
}

.step-content {
  margin-bottom: 40px;
  animation: fadeIn 0.5s ease;
}

.upload-card,
.transcription-card,
.minutes-card {
  margin-bottom: 20px;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  overflow: hidden;
  border-top: 4px solid var(--primary-color);
}

.upload-card:hover,
.transcription-card:hover,
.minutes-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background-color: var(--primary-bg);
  border-radius: var(--border-radius-md);
}

.audio-uploader {
  width: 100%;
}

.audio-uploader :deep(.el-upload-dragger) {
  border: 2px dashed var(--primary-light);
  background-color: var(--white);
  border-radius: var(--border-radius-md);
  transition: all 0.3s ease;
}

.audio-uploader :deep(.el-upload-dragger:hover) {
  border-color: var(--primary-color);
  background-color: var(--primary-bg);
  transform: scale(1.01);
}

.audio-uploader :deep(.el-upload__text) {
  color: var(--gray-700);
}

.audio-uploader :deep(.el-upload__text em) {
  color: var(--primary-color);
  font-style: normal;
  font-weight: bold;
}

.audio-uploader :deep(.el-icon--upload) {
  color: var(--primary-color);
  font-size: 64px;
  margin-bottom: 10px;
}

.file-info {
  background-color: var(--white);
  padding: 20px;
  border-radius: var(--border-radius-md);
  margin-bottom: 20px;
  border-left: 4px solid var(--primary-color);
  box-shadow: var(--shadow-sm);
}

.file-info h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: var(--primary-color);
  font-weight: 600;
  font-size: 18px;
}

.file-info p {
  margin: 8px 0;
  color: var(--gray-700);
}

.file-info p strong {
  color: var(--gray-800);
  margin-right: 6px;
}

.tips {
  font-style: italic;
  color: var(--gray-600);
  font-size: 0.9em;
  margin-top: 15px;
  padding: 8px 12px;
  background-color: var(--primary-lighter);
  border-radius: var(--border-radius-sm);
  border-left: 3px solid var(--primary-light);
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
}

.primary-btn {
  font-weight: 500;
  padding: 10px 24px;
  border-radius: var(--border-radius-md);
  font-size: 16px;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.2);
}

.primary-btn:active {
  transform: translateY(0);
}

.action-btn {
  border-radius: var(--border-radius-sm);
  padding: 8px 16px;
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-1px);
}

.progress-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40px 0;
  padding: 30px;
  background-color: var(--primary-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm) inset;
}

.progress-spinner {
  margin-bottom: 25px;
}

.progress-text {
  font-size: 20px;
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 20px;
  text-align: center;
}

.estimate-time {
  text-align: center;
  margin-top: 25px;
  color: var(--gray-700);
  font-size: 14px;
  background-color: var(--white);
  padding: 15px 20px;
  border-radius: var(--border-radius-md);
  max-width: 500px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--primary-light);
}

.processing-tips {
  margin-top: 20px;
  text-align: left;
  background-color: var(--white);
  padding: 15px 20px;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
  border-top: 3px solid var(--primary-light);
}

.processing-tips p {
  margin-bottom: 10px;
  font-weight: 500;
  color: var(--gray-800);
}

.processing-tips ul {
  padding-left: 20px;
}

.processing-tips li {
  margin: 6px 0;
  line-height: 1.5;
  color: var(--gray-700);
}

.pulse-animation {
  margin: 20px 0;
  padding: 12px 24px;
  background-color: var(--primary-light);
  color: var(--primary-color);
  border-radius: 50px;
  font-weight: 600;
  animation: pulse 2s infinite;
  box-shadow: 0 0 0 rgba(186, 0, 63, 0.4);
  display: inline-block;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(186, 0, 63, 0.4);
    opacity: 0.8;
  }
  70% {
    box-shadow: 0 0 0 15px rgba(186, 0, 63, 0);
    opacity: 1;
  }
  100% {
    box-shadow: 0 0 0 0 rgba(186, 0, 63, 0);
    opacity: 0.8;
  }
}

.generating-stages {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.stage-indicator {
  background-color: var(--primary-color);
  color: var(--white);
  padding: 10px 20px;
  border-radius: 50px;
  font-weight: 500;
  display: inline-block;
  animation: fadeIn 0.5s ease;
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.text-output,
.minutes-result {
  margin-top: 30px;
  animation: fadeIn 0.6s ease;
}

.text-output h3,
.minutes-result h3 {
  color: var(--primary-color);
  font-weight: 600;
  font-size: 20px;
  margin-bottom: 15px;
  position: relative;
  padding-left: 15px;
}

.text-output h3::before,
.minutes-result h3::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 20px;
  background-color: var(--primary-color);
  border-radius: 2px;
}

.transcript-container {
  background-color: var(--white);
  padding: 25px;
  border-radius: var(--border-radius-md);
  max-height: 400px;
  overflow-y: auto;
  margin-top: 15px;
  white-space: normal;
  line-height: 1.6;
  border-left: 4px solid var(--primary-color);
  box-shadow: var(--shadow-sm);
  color: var(--gray-800);
}

.streaming-text {
  color: var(--gray-700);
}

.minutes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--gray-300);
}

.minutes-actions {
  display: flex;
  gap: 10px;
}

.minutes-content {
  margin-top: 20px;
  background-color: var(--white);
  padding: 25px;
  border-radius: var(--border-radius-md);
  max-height: 450px;
  overflow-y: auto;
  white-space: normal;
  line-height: 1.6;
  border-left: 4px solid var(--primary-color);
  box-shadow: var(--shadow-sm);
  color: var(--gray-800);
}

.minutes-content h2 {
  color: var(--primary-color);
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.5em;
  border-bottom: 1px solid var(--primary-light);
  padding-bottom: 8px;
}

.minutes-content h3 {
  color: var(--gray-800);
  margin-top: 16px;
  margin-bottom: 10px;
  font-size: 1.3em;
}

.minutes-content h4 {
  color: var(--gray-700);
  margin-top: 12px;
  margin-bottom: 8px;
  font-size: 1.1em;
}

.minutes-content p {
  margin: 4px 0;
  line-height: 1.5;
  color: var(--gray-700);
}

.minutes-content ul {
  margin: 8px 0;
  padding-left: 20px;
}

.minutes-content li {
  margin: 3px 0;
  line-height: 1.5;
  color: var(--gray-700);
}

.minutes-content br {
  display: block;
  margin: 2px 0;
}

.error-dialog :deep(.el-dialog__header) {
  background-color: #fef0f0;
  padding: 15px 20px;
  border-bottom: 1px solid #fde2e2;
}

.error-dialog :deep(.el-dialog__title) {
  color: #f56c6c;
  font-weight: 600;
}

.error-dialog :deep(.el-dialog__body) {
  padding: 30px 20px;
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 10px 0;
}

.error-icon {
  font-size: 64px;
  color: #F56C6C;
}

.error-message {
  text-align: center;
  color: var(--gray-700);
  max-width: 90%;
  word-break: break-word;
  line-height: 1.5;
  background-color: #fef0f0;
  padding: 15px;
  border-radius: var(--border-radius-md);
  border-left: 3px solid #f56c6c;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  padding-top: 10px;
}

/* 调整toast样式使提示更明显 */
:deep(.Vue-Toastification__toast--info) {
  background-color: var(--primary-color) !important;
  font-weight: 500;
  border-radius: var(--border-radius-md) !important;
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.3) !important;
}

:deep(.Vue-Toastification__toast--success) {
  border-radius: var(--border-radius-md) !important;
  box-shadow: 0 4px 12px rgba(38, 160, 88, 0.3) !important;
}

:deep(.Vue-Toastification__toast--error) {
  border-radius: var(--border-radius-md) !important;
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.3) !important;
}

/* 适配较小屏幕 */
@media (max-width: 768px) {
  .meeting-minutes-container {
    padding: 20px 15px;
  }
  
  .page-title {
    font-size: 26px;
    margin-bottom: 30px;
  }
  
  .steps {
    margin-bottom: 30px;
    padding: 5px 10px 20px;
  }
  
  .file-info,
  .transcript-container,
  .minutes-content {
    padding: 15px;
  }
  
  .minutes-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .minutes-actions {
    margin-top: 10px;
    width: 100%;
    justify-content: space-between;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .progress-area {
    padding: 20px 15px;
  }
  
  .progress-text {
    font-size: 18px;
  }
  
  .estimate-time {
    width: 100%;
    padding: 12px 15px;
  }
  
  .stage-indicator {
    padding: 8px 16px;
    font-size: 14px;
  }
}
</style> 