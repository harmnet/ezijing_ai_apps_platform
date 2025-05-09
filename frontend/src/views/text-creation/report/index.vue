<template>
  <div class="research-report-container">
    <div class="input-section">
      <div class="input-header">
        <h2>{{ isOutlineToReport ? '大纲生成研报' : '智能研报大纲' }}</h2>
        <p class="input-description">
          {{ 
            isOutlineToReport 
              ? '跟随下面的步骤，让AI为您生成完整的专业研究报告' 
              : '输入行业、主题或关键词，AI将为您生成结构化研报大纲'
          }}
        </p>
      </div>
      
      <!-- 步骤指示器 - 仅在大纲生成研报模式下显示 -->
      <div v-if="isOutlineToReport" class="step-indicator">
        <el-steps 
          :active="currentStep-1" 
          class="custom-steps zijin-steps"
          style="--el-color-success: #c62828 !important; --el-color-primary: #c62828 !important;"
          finish-status="success"
        >
          <el-step title="填写标题" description="输入研报标题"></el-step>
          <el-step title="生成大纲" description="生成研报大纲"></el-step>
          <el-step title="调整大纲" description="修改完善大纲"></el-step>
          <el-step title="生成研报" description="根据大纲生成研报"></el-step>
          <el-step title="查看状态" description="查询研报生成状态"></el-step>
          <el-step title="下载研报" description="下载生成的研报文档"></el-step>
        </el-steps>
      </div>
      
      <!-- 添加示例主题，仅在智能研报大纲模式下显示 -->
      <div class="example-topics" v-if="!isOutlineToReport">
        <div class="example-title">示例主题：</div>
        <div class="topic-grid">
          <div class="topic-item" @click="selectTopic('新能源汽车行业研究报告')">新能源汽车行业研究报告</div>
          <div class="topic-item" @click="selectTopic('人工智能在金融领域的应用分析')">人工智能在金融领域的应用分析</div>
          <div class="topic-item" @click="selectTopic('医疗健康产业发展趋势预测')">医疗健康产业发展趋势预测</div>
          <div class="topic-item" @click="selectTopic('5G技术商业化应用前景展望')">5G技术商业化应用前景展望</div>
          <div class="topic-item" @click="selectTopic('智慧农业发展现状与未来机遇')">智慧农业发展现状与未来机遇</div>
          <div class="topic-item" @click="selectTopic('太阳能光伏产业链分析报告')">太阳能光伏产业链分析报告</div>
          <div class="topic-item" @click="selectTopic('区块链技术在金融行业的应用与挑战')">区块链技术在金融行业的应用与挑战</div>
          <div class="topic-item" @click="selectTopic('农业科技创新与粮食安全研究')">农业科技创新与粮食安全研究</div>
          <div class="topic-item" @click="selectTopic('储能技术发展趋势与投资机会')">储能技术发展趋势与投资机会</div>
          <div class="topic-item" @click="selectTopic('绿色金融发展现状与前景分析')">绿色金融发展现状与前景分析</div>
        </div>
      </div>
      
      <!-- 研报标题输入 - 大纲生成研报步骤1 -->
      <div v-if="isOutlineToReport && currentStep === 1" class="step-content">
        <h3 class="step-title">步骤1: 填写研报标题</h3>
        <el-form :model="formData" label-position="top">
          <el-form-item label="研报标题">
            <div class="input-with-button">
              <el-input 
                v-model="formData.reportTitle" 
                placeholder="请输入研报标题，如：新能源汽车行业趋势分析研究报告"
                maxlength="100"
                show-word-limit
              />
              <el-button 
                type="default" 
                @click="generateExampleTitle" 
                class="example-title-btn"
              >
                生成示例研报标题
              </el-button>
            </div>
          </el-form-item>
          
          <el-form-item>
            <div class="action-buttons center-buttons">
              <el-button 
                type="primary" 
                @click="goToStep(2)" 
                :disabled="!formData.reportTitle.trim()"
                class="generate-btn"
              >
                下一步
              </el-button>
              <el-button @click="resetProcess" class="reset-btn">重置</el-button>
              <el-button type="info" @click="openHistoryDialog">历史记录</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 生成大纲 - 大纲生成研报步骤2 -->
      <div v-if="isOutlineToReport && currentStep === 2" class="step-content">
        <h3 class="step-title">步骤2: 生成研报大纲</h3>
        <el-form :model="formData" label-position="top">
          <el-form-item label="研报标题">
            <el-input 
              v-model="formData.topic" 
              placeholder="输入研报标题..."
              maxlength="100"
              show-word-limit
              type="text"
            />
          </el-form-item>
          
          <el-form-item>
            <div v-if="generating" class="timer-container">
              <span class="timer-label">生成中</span>
              <span class="timer-value">{{ formatTime(elapsedTime) }}</span>
            </div>
            <div class="action-buttons center-buttons">
              <el-button 
                type="primary" 
                @click="generateOutlineForReport" 
                :loading="generating"
                :disabled="!formData.topic.trim()"
                class="generate-btn"
              >
                生成大纲
              </el-button>
              <el-button @click="goToStep(1)" class="reset-btn">上一步</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 调整大纲 - 大纲生成研报步骤3 -->
      <div v-if="isOutlineToReport && currentStep === 3" class="step-content">
        <h3 class="step-title">步骤3: 修改调整大纲</h3>
        <p class="step-description">您可以直接编辑下方的大纲内容，完成后点击"下一步"继续</p>
        
        <div class="edit-options">
          <el-switch
            v-model="isEditingOutline"
            active-text="编辑模式"
            inactive-text="预览模式"
          ></el-switch>
        </div>
        
        <!-- 编辑模式 -->
        <div v-if="isEditingOutline" class="outline-editor">
          <el-input
            v-model="generatedOutline"
            type="textarea"
            :rows="15"
            resize="vertical"
            placeholder="编辑大纲内容..."
          ></el-input>
        </div>
        
        <!-- 预览模式 -->
        <div v-else class="outline-preview markdown-body" v-html="formattedOutline"></div>
        
        <div class="action-buttons center-buttons">
          <el-button @click="goToStep(2)" class="reset-btn">上一步</el-button>
          <el-button 
            type="primary" 
            @click="goToStep(4)" 
            :disabled="!generatedOutline.trim()"
            class="generate-btn"
          >
            下一步
          </el-button>
        </div>
      </div>
      
      <!-- 生成研报 - 大纲生成研报步骤4 -->
      <div v-if="isOutlineToReport && currentStep === 4" class="step-content">
        <h3 class="step-title">步骤4: 生成完整研报</h3>
        <p class="step-description">确认以下信息无误后，点击"生成研报"按钮开始生成完整研究报告</p>
        
        <div class="confirm-info">
          <div class="info-item">
            <span class="info-label">研报标题:</span>
            <span class="info-value">{{ formData.reportTitle }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">大纲字数:</span>
            <span class="info-value">{{ generatedOutline.length }} 字符</span>
          </div>
        </div>
        
        <div class="outline-preview-compact markdown-body" v-html="formattedOutline"></div>
        
        <div class="action-buttons center-buttons">
          <el-button @click="goToStep(3)" class="reset-btn">上一步</el-button>
          <el-button 
            type="primary" 
            @click="submitGenerateReport" 
            :loading="generatingReport"
            class="generate-btn"
          >
            生成研报
          </el-button>
        </div>
      </div>
      
      <!-- 查询状态 - 大纲生成研报步骤5 -->
      <div v-if="isOutlineToReport && currentStep === 5" class="step-content">
        <h3 class="step-title">步骤5: 查询研报生成状态</h3>
        <p class="step-description">研报正在生成中，这可能需要几分钟时间...您可以查看生成进度或查询历史记录</p>
        
        <div class="status-card">
          <div class="status-info">
            <i class="el-icon-loading status-icon"></i>
            <div class="status-details">
              <div class="status-title">研报生成中</div>
              <div class="status-desc">AI正在根据您提供的大纲内容生成完整研究报告</div>
              <div class="status-doc-id">文档ID: {{ reportDocId || '暂无文档ID，请点击刷新状态按钮更新' }}</div>
              <div class="status-doc-id">论文ID: {{ currentPaperId || '暂无论文ID' }}</div>
              <div class="status-time">提交时间: {{ formatDate(reportSubmitTime) }}</div>
            </div>
          </div>
          
          <div class="status-actions center-buttons">
            <el-button type="primary" @click="checkReportStatus" :loading="checkingStatus">
              刷新状态
            </el-button>
            <el-button type="info" @click="openHistoryDialog">
              查看历史记录
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 下载研报 - 大纲生成研报步骤6 -->
      <div v-if="isOutlineToReport && currentStep === 6" class="step-content">
        <h3 class="step-title">步骤6: 下载研报文档</h3>
        <p class="step-description">研报已生成完成，您可以下载文档或查看历史记录</p>
        
        <div class="success-card">
          <div class="success-info">
            <i class="el-icon-success success-icon"></i>
            <div class="success-details">
              <div class="success-title">研报生成成功</div>
              <div class="success-desc">您的研报已经准备就绪，可以立即下载</div>
              <div class="success-time">完成时间: {{ formatDate(reportCompleteTime) }}</div>
            </div>
          </div>
          
          <div class="success-actions center-buttons">
            <el-button type="primary" @click="downloadCurrentReport" class="download-btn">
              下载研报
            </el-button>
            <el-button type="success" @click="resetProcess">
              创建新研报
            </el-button>
            <el-button type="info" @click="openHistoryDialog">
              查看历史记录
            </el-button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="generatedOutline && !isOutlineToReport" class="result-section">
      <div class="result-header">
        <h3>{{ isOutlineToReport ? '' : '研报大纲' }}</h3>
        <div class="action-buttons center-buttons">
          <el-button type="primary" @click="copyOutline" size="small" class="copy-btn">
            复制内容
          </el-button>
          <el-button 
            v-if="!isOutlineToReport && currentPaperId && queryID" 
            type="success" 
            size="small" 
            @click="generateReportFromOutline"
            :loading="generatingReport"
            class="copy-btn"
          >
            生成研报
          </el-button>
        </div>
      </div>
      
      <div class="outline-content" ref="outlineContent">
        <div v-html="formattedOutline"></div>
      </div>
    </div>
    
    <!-- 历史记录对话框 -->
    <el-dialog v-model="historyDialogVisible" width="80%" title="" class="history-dialog">
      <div class="history-container">
        <el-table :data="historyRecords" style="width: 100%" border stripe>
          <el-table-column prop="query" label="研报主题" min-width="120">
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="document_status" label="状态" width="120">
            <template #default="scope">
              <span>{{ formatStatus(scope.row.document_status) }}</span>
              <el-tooltip 
                v-if="scope.row.document_status === 'failed'" 
                effect="dark" 
                :content="scope.row.error_message || '生成失败'" 
                placement="top"
              >
                <i class="el-icon-info info-icon"></i>
              </el-tooltip>
              <el-tooltip 
                v-if="scope.row.document_status === 'generating'" 
                effect="dark" 
                :content="'文档ID: ' + (scope.row.doc_id || '未知')" 
                placement="top"
              >
                <i class="el-icon-info info-icon"></i>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="300">
            <template #default="scope">
              <el-button 
                type="primary" 
                size="small" 
                @click="viewOutline(scope.row)"
              >
                查看
              </el-button>
              <el-button 
                v-if="scope.row.document_status === 'completed'" 
                type="success" 
                size="small" 
                @click="downloadReport(scope.row)"
              >
                下载
              </el-button>
              <el-button 
                v-if="scope.row.document_status === 'none' && scope.row.query_id" 
                type="warning" 
                size="small" 
                @click="generateReportFromHistory(scope.row)"
              >
                生成研报
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="confirmDeletePaper(scope.row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { marked } from 'marked'
import axios from 'axios'

export default {
  name: 'ReportOutline',
  
  setup() {
    const route = useRoute()
    const formData = ref({
      topic: '',
      reportTitle: '' // 为大纲生成研报模式添加的标题字段
    })
    
    // 示例研报标题库
    const exampleTitles = [
      "2023年中国新能源汽车产业发展趋势研究报告",
      "人工智能技术在医疗健康领域的应用前景分析",
      "数字经济时代金融科技发展与监管研究",
      "中国半导体产业自主创新与发展策略分析",
      "绿色低碳转型背景下能源结构调整研究报告",
      "元宇宙产业生态构建与商业模式研究",
      "中国智能制造产业链发展现状与未来展望",
      "区块链技术在供应链金融中的应用研究",
      "中国农业科技创新与乡村振兴战略研究",
      "5G技术赋能智慧城市建设的实践与展望",
      "大数据时代个人隐私保护与数据安全研究",
      "碳中和背景下中国能源转型路径分析",
      "生物医药产业创新发展与投资机会研究",
      "云计算与边缘计算融合发展趋势分析",
      "中国集成电路产业自主可控战略研究"
    ]
    
    // 检测当前路由来确定是哪个功能
    const isOutlineToReport = computed(() => {
      return route.path.includes('outline-to-report')
    })
    
    // 为大纲生成研报添加流程控制
    const currentStep = ref(1) // 当前处于的步骤，从1开始
    const isEditingOutline = ref(true) // 是否处于编辑大纲模式
    const reportSubmitTime = ref(null) // 研报提交时间
    const reportCompleteTime = ref(null) // 研报完成时间
    const reportDocId = ref('') // 研报文档ID
    const checkingStatus = ref(false) // 是否正在检查状态
    const currentReportRecord = ref(null) // 当前研报记录
    
    const generating = ref(false)
    const generatingReport = ref(false)
    const generatedOutline = ref('')
    const currentPaperId = ref(null)
    const queryID = ref('') // 存储大纲生成时返回的queryID
    const historyDialogVisible = ref(false)
    const historyRecords = ref([])
    const outlineContent = ref(null)
    const elapsedTime = ref(0) // 用于计时器
    const timerInterval = ref(null) // 计时器间隔
    
    // 格式化大纲
    const formattedOutline = computed(() => {
      return generatedOutline.value ? marked(generatedOutline.value) : ''
    })
    
    // 监听步骤变化，当进入步骤2时，自动填充研报标题
    watch(() => currentStep.value, (newStep) => {
      if (newStep === 2) {
        // 将步骤1的研报标题复制到步骤2
        formData.value.topic = formData.value.reportTitle;
      }
    })
    
    // 监听路由变化，如果是大纲生成研报路由，则设置为第一步
    watch(() => route.path, (newPath) => {
      if (newPath.includes('outline-to-report')) {
        currentStep.value = 1
        resetForm()
      }
    })
    
    // 进入特定步骤
    const goToStep = (step) => {
      // 确保步骤合法
      if (step < 1 || step > 6) return
      
      // 确保必要条件已满足
      if (step > 1 && !formData.value.reportTitle.trim()) {
        ElMessage.warning('请先填写研报标题')
        currentStep.value = 1
        return
      }
      
      if (step > 2 && !generatedOutline.value) {
        ElMessage.warning('请先生成研报大纲')
        currentStep.value = 2
        return
      }
      
      if (step === 5 && !reportSubmitTime.value) {
        ElMessage.warning('请先提交研报生成任务')
        currentStep.value = 4
        return
      }
      
      if (step === 6 && !currentReportRecord.value?.download_url) {
        ElMessage.warning('研报尚未生成完成，无法进入下载步骤')
        currentStep.value = 5
        return
      }
      
      // 保存当前步骤状态或执行必要的操作
      if (step === 2 && currentStep.value === 1) {
        // 从步骤1到步骤2时，将研报标题传递给主题字段
        formData.value.topic = formData.value.reportTitle;
      }
      
      currentStep.value = step
    }
    
    // 重置整个流程
    const resetProcess = () => {
      currentStep.value = 1
      formData.value.reportTitle = ''
      formData.value.topic = ''
      generatedOutline.value = ''
      currentPaperId.value = null
      queryID.value = ''
      reportSubmitTime.value = null
      reportCompleteTime.value = null
      reportDocId.value = ''
      currentReportRecord.value = null
    }
    
    // 格式化时间为分:秒格式
    const formatTime = (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    };
    
    // 专门为大纲生成研报流程设置的生成大纲函数
    const generateOutlineForReport = async () => {
      if (!formData.value.topic.trim()) {
        ElMessage.warning('请输入研报主题')
        return
      }
      
      generating.value = true
      elapsedTime.value = 0
      
      // 启动计时器
      timerInterval.value = setInterval(() => {
        elapsedTime.value += 1;
      }, 1000);
      
      try {
        const response = await axios.post('/api/v1/academic/report_outline', {
          content: formData.value.topic,
          rebuild_times: 0
        })
        
        if (response.data.status === 'success') {
          generatedOutline.value = response.data.data
          currentPaperId.value = response.data.paper_id
          queryID.value = response.data.queryID || '' // 保存queryID
          
          ElMessage.success('研报大纲生成成功')
          
          // 进入下一步
          goToStep(3)
        } else {
          ElMessage.error(response.data.message || '生成失败')
        }
      } catch (error) {
        console.error('生成大纲错误:', error)
        ElMessage.error('生成大纲时出错: ' + (error.response?.data?.message || error.message || '未知错误'))
      } finally {
        // 停止计时器
        clearInterval(timerInterval.value);
        generating.value = false
      }
    }
    
    // 提交生成研报的请求
    const submitGenerateReport = async () => {
      console.log('==================== 开始生成研报 ====================');
      console.log('当前大纲内容:', generatedOutline.value);
      console.log('当前queryID:', queryID.value);
      console.log('当前paperID:', currentPaperId.value);
      
      if (!generatedOutline.value) {
        ElMessage.warning('缺少必要的大纲内容');
        return;
      }
      
      if (!currentPaperId.value) {
        ElMessage.warning('缺少论文ID，请重新生成大纲');
        return;
      }
      
      generatingReport.value = true;
      
      try {
        // 准备请求参数，即使没有queryID也能提交
        const requestData = {
          outline: generatedOutline.value,
          title: formData.value.reportTitle,
          paper_id: currentPaperId.value,
          timestamp: new Date().getTime() // 添加时间戳避免缓存问题
        };
        
        // 如果有queryID，添加到请求中
        if (queryID.value) {
          requestData.queryID = queryID.value;
        }
        
        console.log('提交生成研报的请求参数:', JSON.stringify(requestData).substring(0, 500) + '...');
        console.log('准备发送POST请求到:', '/api/v1/academic/report_from_outline');
        console.log('请求参数大小:', JSON.stringify(requestData).length, '字节');
        
        const startTime = new Date().getTime();
        console.log('发送API请求，开始时间:', new Date().toLocaleTimeString());
        
        ElMessage.info('开始生成研报请求，可能需要20-30秒...');
        
        // 使用 fetch API 测试，确保请求发送成功
        const fetchResponse = await fetch('/api/v1/academic/report_from_outline', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        });
        
        // 获取响应内容
        const responseText = await fetchResponse.text();
        let responseData;
        try {
          responseData = JSON.parse(responseText);
        } catch (e) {
          responseData = { status: 'error', message: '解析响应失败', raw: responseText };
        }
        
        const endTime = new Date().getTime();
        const elapsed = (endTime - startTime) / 1000;
        
        console.log(`生成研报API调用完成，耗时: ${elapsed}秒`);
        console.log('生成研报API响应状态:', fetchResponse.status);
        console.log('生成研报API响应Headers:', JSON.stringify(Object.fromEntries([...fetchResponse.headers])));
        console.log('生成研报API响应内容:', responseData);
        
        if (responseData.status === 'success') {
          ElMessage.success('研报生成请求已提交');
          
          // 记录提交时间和文档ID
          reportSubmitTime.value = new Date();
          
          // 确保doc_id被正确设置
          if (responseData.data && responseData.data.doc_id) {
            reportDocId.value = responseData.data.doc_id;
            console.log('获取到文档ID:', reportDocId.value);
          } else {
            console.warn('警告: 服务器响应中未包含doc_id或为空，需要后续刷新获取:', JSON.stringify(responseData));
            reportDocId.value = ''; // 设置为空字符串而不是undefined
          }
          
          // 更新当前研报记录
          await fetchCurrentReportStatus();
          console.log('获取当前研报记录:', currentReportRecord.value);
          
          // 如果fetchCurrentReportStatus获取到了文档ID，则使用它
          if (currentReportRecord.value && currentReportRecord.value.doc_id) {
            reportDocId.value = currentReportRecord.value.doc_id;
            console.log('从当前记录中获取到文档ID:', reportDocId.value);
          }
          
          // 进入下一步
          goToStep(5);
        } else {
          ElMessage.error(response.data.message || '提交失败');
          console.error('生成研报API调用返回错误:', response.data);
        }
      } catch (error) {
        console.error('生成研报API调用异常:', error);
        console.error('错误详情:', error.response ? JSON.stringify(error.response.data) : error.message);
        ElMessage.error('生成研报时出错: ' + (error.response?.data?.message || error.message || '未知错误'));
      } finally {
        generatingReport.value = false;
        console.log('==================== 生成研报流程结束 ====================');
      }
    };
    
    // 检查当前研报状态
    const checkReportStatus = async () => {
      if (!currentPaperId.value) {
        ElMessage.warning('无法检查状态：缺少论文ID');
        return;
      }
      
      checkingStatus.value = true;
      
      try {
        // 首先尝试查询当前研报记录以获取最新状态
        await fetchCurrentReportStatus();
        console.log('刷新状态：当前研报记录', currentReportRecord.value);
        
        // 从记录中获取文档ID
        if (currentReportRecord.value && currentReportRecord.value.doc_id) {
          reportDocId.value = currentReportRecord.value.doc_id;
          console.log('刷新状态：从当前记录中获取到文档ID:', reportDocId.value);
        }
        
        // 如果仍然没有文档ID，给出提示但继续尝试检查状态
        if (!reportDocId.value) {
          console.warn('刷新状态：仍然没有文档ID，将尝试使用论文ID继续检查');
        }
        
        // 构建检查状态的请求参数
        const requestParams = {
          paper_id: currentPaperId.value
        };
        
        // 如果有文档ID，则添加到请求中
        if (reportDocId.value) {
          requestParams.doc_id = reportDocId.value;
        }
        
        console.log('刷新状态：请求参数', requestParams);
        
        const response = await axios.post('/api/v1/academic/check_paper_status', requestParams);
        console.log('刷新状态：响应结果', response.data);
        
        if (response.data.status === 'success') {
          const statusData = response.data.data;
          
          // 如果响应中包含文档ID，更新到本地
          if (statusData.doc_id) {
            reportDocId.value = statusData.doc_id;
            console.log('刷新状态：从响应中更新文档ID:', reportDocId.value);
          }
          
          // 再次获取最新记录
          await fetchCurrentReportStatus();
          
          // 检查是否已完成
          if (currentReportRecord.value?.document_status === 'completed') {
            reportCompleteTime.value = new Date();
            ElMessage.success('研报已生成完成！');
            goToStep(6);
          } else if (currentReportRecord.value?.document_status === 'failed') {
            ElMessage.error('研报生成失败: ' + (currentReportRecord.value.error_message || '未知错误'));
          } else {
            const timeElapsed = new Date() - reportSubmitTime.value;
            const minutesElapsed = Math.floor(timeElapsed / (1000 * 60));
            ElMessage.info(`研报仍在生成中(已经过${minutesElapsed}分钟)，请稍后再查询`);
          }
        } else {
          ElMessage.error(response.data.message || '查询状态失败');
        }
      } catch (error) {
        console.error('检查状态错误:', error);
        ElMessage.error('检查状态时出错: ' + (error.response?.data?.message || error.message || '未知错误'));
      } finally {
        checkingStatus.value = false;
      }
    };
    
    // 获取当前研报的最新记录
    const fetchCurrentReportStatus = async () => {
      if (!currentPaperId.value) {
        console.warn('获取当前研报状态：缺少论文ID，无法获取最新记录');
        return;
      }
      
      try {
        console.log('获取当前研报状态：正在获取论文ID为', currentPaperId.value, '的记录');
        // 直接获取特定ID的论文详情，避免获取所有历史记录
        const response = await axios.get(`/api/v1/academic/history/${currentPaperId.value}`);
        
        if (response.data.status === 'success') {
          currentReportRecord.value = response.data.data;
          console.log('获取当前研报状态：成功', currentReportRecord.value);
        } else {
          console.error('获取当前研报状态：失败', response.data.message);
        }
      } catch (error) {
        console.error('获取当前研报状态错误:', error);
      }
    }
    
    // 下载当前生成的研报
    const downloadCurrentReport = () => {
      if (!currentReportRecord.value?.download_url) {
        ElMessage.warning('没有可下载的研报链接')
        return
      }
      
      try {
        window.open(currentReportRecord.value.download_url, '_blank')
      } catch (error) {
        console.error('下载研报错误:', error)
        ElMessage.error('下载研报时出错: ' + (error.message || '未知错误'))
      }
    }
    
    // 格式化状态
    const formatStatus = (status) => {
      const statusMap = {
        'none': '未生成',
        'generating': '生成中',
        'completed': '已完成',
        'failed': '失败'
      }
      return statusMap[status] || status
    }
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      
      try {
        const date = new Date(dateStr)
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        const hours = String(date.getHours()).padStart(2, '0')
        const minutes = String(date.getMinutes()).padStart(2, '0')
        
        return `${year}/${month}/${day} ${hours}:${minutes}`
      } catch (e) {
        console.error('日期格式化错误:', e)
        return dateStr
      }
    }
    
    // 重置表单
    const resetForm = () => {
      formData.value.topic = ''
      generatedOutline.value = ''
      currentPaperId.value = null
      queryID.value = ''
    }
    
    // 复制大纲内容 - 确保复制的是markdown格式
    const copyOutline = () => {
      if (!generatedOutline.value) return
      
      // 直接复制原始markdown内容，而不是HTML格式
      navigator.clipboard.writeText(generatedOutline.value)
        .then(() => {
          ElMessage.success('大纲内容已复制到剪贴板(Markdown格式)')
        })
        .catch(err => {
          console.error('复制失败:', err)
          ElMessage.error('复制失败，请手动选择内容复制')
        })
    }
    
    // 获取历史记录
    const fetchHistoryRecords = async () => {
      try {
        const response = await axios.get('/api/v1/academic/history')
        
        if (response.data.status === 'success') {
          historyRecords.value = response.data.data || []
          
          // 检查正在生成中的研报状态
          checkGeneratingReports()
        } else {
          console.error('获取历史记录失败:', response.data.message)
        }
      } catch (error) {
        console.error('获取历史记录错误:', error)
      }
    }
    
    // 检查正在生成中的研报状态
    const checkGeneratingReports = () => {
      const generatingReports = historyRecords.value.filter(
        report => report.document_status === 'generating' && report.doc_id
      )
      
      generatingReports.forEach(report => {
        updateReportStatus(report.id, report.doc_id)
      })
    }
    
    // 更新研报状态
    const updateReportStatus = async (paperId, docId) => {
      if (!paperId || !docId) return
      
      try {
        const response = await axios.post('/api/v1/academic/check_paper_status', {
          doc_id: docId,
          paper_id: paperId
        })
        
        if (response.data.status === 'success') {
          console.log(`研报(ID:${paperId})状态更新:`, response.data.data)
          
          // 如果状态有变化，刷新列表
          if (response.data.data.document_status !== 'generating') {
            fetchHistoryRecords()
          }
        }
      } catch (error) {
        console.error(`更新研报(ID:${paperId})状态出错:`, error)
      }
    }
    
    // 打开历史记录对话框
    const openHistoryDialog = async () => {
      historyDialogVisible.value = true
      await fetchHistoryRecords()
    }
    
    // 查看历史大纲
    const viewOutline = (paper) => {
      if (paper.outline) {
        currentPaperId.value = paper.id
        queryID.value = paper.query_id || ''  // 设置queryID
        generatedOutline.value = paper.outline
        historyDialogVisible.value = false
      } else {
        ElMessage.warning('该记录没有大纲内容')
      }
    }
    
    // 下载研报
    const downloadReport = async (paper) => {
      if (!paper.doc_id || !paper.download_url) {
        ElMessage.warning('该记录没有可下载的研报')
        return
      }
      
      try {
        // 直接打开下载链接
        window.open(paper.download_url, '_blank')
      } catch (error) {
        console.error('下载研报错误:', error)
        ElMessage.error('下载研报时出错: ' + (error.message || '未知错误'))
      }
    }
    
    // 从历史记录中生成研报
    const generateReportFromHistory = async (paper) => {
      if (!paper.outline) {
        ElMessage.warning('该记录没有大纲内容，无法生成研报')
        return
      }
      
      try {
        // 准备请求参数
        const requestData = {
          outline: paper.outline,
          title: paper.title || paper.query,
          paper_id: paper.id
        };
        
        // 如果有queryID，添加到请求中
        if (paper.query_id) {
          requestData.queryID = paper.query_id;
        }
        
        const response = await axios.post('/api/v1/academic/report_from_outline', requestData)
        
        if (response.data.status === 'success') {
          ElMessage.success('研报生成请求已提交，请稍后在历史记录中查看结果')
          fetchHistoryRecords()
        } else {
          ElMessage.error(response.data.message || '提交失败')
        }
      } catch (error) {
        console.error('生成研报错误:', error)
        ElMessage.error('生成研报时出错: ' + (error.response?.data?.message || error.message || '未知错误'))
      }
    }
    
    // 确认删除论文记录
    const confirmDeletePaper = (paperId) => {
      ElMessageBox.confirm('确定要删除这条记录吗？', '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePaper(paperId)
      }).catch(() => {
        // 用户取消操作
      })
    }
    
    // 删除论文记录
    const deletePaper = async (paperId) => {
      try {
        const response = await axios.delete(`/api/v1/academic/history/${paperId}`)
        
        if (response.data.status === 'success') {
          ElMessage.success('删除成功')
          // 刷新历史记录
          fetchHistoryRecords()
          
          // 如果当前正在查看的是被删除的记录，则清空显示
          if (currentPaperId.value === paperId) {
            generatedOutline.value = ''
            currentPaperId.value = null
            queryID.value = ''
          }
        } else {
          ElMessage.error(response.data.message || '删除失败')
        }
      } catch (error) {
        console.error('删除记录错误:', error)
        ElMessage.error('删除记录时出错: ' + (error.response?.data?.message || error.message || '未知错误'))
      }
    }
    
    // 添加选择主题的方法
    const selectTopic = (topic) => {
      formData.value.topic = topic
    }
    
    // 生成示例研报标题
    const generateExampleTitle = () => {
      // 随机从标题库中选择一个标题
      const randomIndex = Math.floor(Math.random() * exampleTitles.length)
      formData.value.reportTitle = exampleTitles[randomIndex]
      ElMessage.success('已生成示例研报标题')
    }
    
    // 页面加载时获取历史记录
    onMounted(() => {
      fetchHistoryRecords()
    })
    
    return {
      formData,
      generating,
      generatingReport,
      generatedOutline,
      formattedOutline,
      currentPaperId,
      queryID,
      historyDialogVisible,
      historyRecords,
      outlineContent,
      isOutlineToReport,
      // 添加大纲生成研报流程所需属性
      currentStep,
      isEditingOutline,
      reportSubmitTime,
      reportCompleteTime,
      reportDocId,
      checkingStatus,
      currentReportRecord,
      elapsedTime, // 添加计时器时间
      // 添加流程控制方法
      goToStep,
      resetProcess,
      generateOutlineForReport,
      submitGenerateReport,
      checkReportStatus,
      downloadCurrentReport,
      formatTime, // 添加时间格式化函数
      // 添加生成示例标题方法
      generateExampleTitle,
      // 原有方法
      formatStatus,
      formatDate,
      resetForm,
      copyOutline,
      openHistoryDialog,
      viewOutline,
      downloadReport,
      generateReportFromHistory,
      confirmDeletePaper,
      deletePaper,
      selectTopic
    }
  }
}
</script>

<style>
/* 全局样式，不使用scoped，确保能覆盖Element Plus样式 */
.research-report-container .custom-steps .el-step__head.is-finish {
  color: #c62828 !important;
  border-color: #c62828 !important;
}

.research-report-container .custom-steps .el-step__title.is-finish {
  color: #c62828 !important;
}

.research-report-container .custom-steps .el-step__description.is-finish {
  color: #c62828 !important;
}

.research-report-container .custom-steps .el-step__icon.is-finish {
  background-color: #c62828 !important;
  color: white !important;
}

.research-report-container .custom-steps .el-step__head.is-finish .el-step__icon,
.research-report-container .custom-steps .el-step__head.is-finish .el-step__icon-inner {
  background-color: #c62828 !important;
  color: white !important;
}

.research-report-container .custom-steps .el-step__head.is-finish .el-step__line {
  background-color: #c62828 !important;
}

.research-report-container .custom-steps .el-step__head.is-success {
  color: #c62828 !important;
  border-color: #c62828 !important;
}

/* 添加自定义finish样式 */
.research-report-container .zijin-steps .el-step__head.is-finish,
.research-report-container .zijin-steps .el-step__head.is-success,
.research-report-container .zijin-steps .el-step__head.is-custom-finish {
  color: #c62828 !important;
  border-color: #c62828 !important;
}

.research-report-container .zijin-steps .el-step__title.is-finish,
.research-report-container .zijin-steps .el-step__title.is-success,
.research-report-container .zijin-steps .el-step__title.is-custom-finish {
  color: #c62828 !important;
}

.research-report-container .zijin-steps .el-step__description.is-finish,
.research-report-container .zijin-steps .el-step__description.is-success,
.research-report-container .zijin-steps .el-step__description.is-custom-finish {
  color: #c62828 !important;
}

.research-report-container .zijin-steps .el-step__icon.is-finish,
.research-report-container .zijin-steps .el-step__icon.is-success,
.research-report-container .zijin-steps .el-step__icon.is-custom-finish {
  background-color: #c62828 !important;
  color: white !important;
}

.research-report-container .zijin-steps .el-step__head.is-finish .el-step__line,
.research-report-container .zijin-steps .el-step__head.is-success .el-step__line,
.research-report-container .zijin-steps .el-step__head.is-custom-finish .el-step__line {
  background-color: #c62828 !important;
}

/* 添加内联样式覆盖 */
.zijin-steps :deep(.el-step__title) {
  color: #c62828 !important;
}

.zijin-steps :deep(.el-step__title.is-finish),
.zijin-steps :deep(.el-step__description.is-finish) {
  color: #c62828 !important;
}

/* 覆盖Element Plus使用的CSS变量 */
:root {
  --el-color-success: #c62828 !important;
}

/* 覆盖icon用的图标颜色 */
.zijin-steps :deep(.el-step__head.is-finish) .el-step__icon.is-text,
.zijin-steps :deep(.el-step__head.is-finish) .el-step__icon-inner {
  background-color: #c62828 !important;
  color: white !important;
}

/* 强行覆盖!important规则 */
html body .research-report-container .custom-steps .el-step__title.is-finish,
html body .research-report-container .custom-steps .el-step__description.is-finish,
html body .research-report-container .custom-steps .el-step__head.is-finish {
  color: #c62828 !important;
}

html body .research-report-container .custom-steps .el-step__head.is-finish .el-step__icon,
html body .research-report-container .custom-steps .el-step__head.is-finish .el-step__icon.el-step__icon--success {
  background-color: #c62828 !important;
}
</style>

<style scoped>
.research-report-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f5f5f5;
}

.input-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.input-header {
  margin-bottom: 20px;
}

.input-header h2 {
  color: #c62828; /* 紫荆红 */
  font-weight: bold;
}

.input-description {
  color: #666;
  margin-top: 8px;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.generate-btn {
  background-color: #c62828; /* 紫荆红 */
  border-color: #c62828;
}

.generate-btn:hover, .generate-btn:focus {
  background-color: #b71c1c;
  border-color: #b71c1c;
}

.reset-btn {
  color: #666;
  border-color: #ddd;
}

.copy-btn {
  background-color: #c62828; /* 紫荆红 */
  border-color: #c62828;
}

.copy-btn:hover, .copy-btn:focus {
  background-color: #b71c1c;
  border-color: #b71c1c;
}

.result-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.result-header h3 {
  color: #c62828; /* 紫荆红 */
  font-weight: bold;
}

.outline-content {
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  min-height: 300px;
  max-height: 600px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
}

.history-container {
  padding: 10px 0;
}

.info-icon {
  margin-left: 5px;
  color: #c62828; /* 紫荆红 */
  cursor: pointer;
}

/* 示例主题区域样式 */
.example-topics {
  margin-bottom: 20px;
}

.example-title {
  font-weight: bold;
  margin-bottom: 10px;
  color: #666;
}

.topic-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.topic-item {
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  padding: 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
  color: #333;
}

.topic-item:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
  box-shadow: 0 3px 5px rgba(0,0,0,0.1);
  border-color: #c62828; /* 紫荆红 */
  color: #c62828;
}

/* 针对生成的Markdown内容的样式 */
:deep(h1) {
  font-size: 1.8em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
  color: #c62828; /* 紫荆红 */
}

:deep(h2) {
  font-size: 1.5em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #eaecef;
  color: #c62828; /* 紫荆红 */
}

:deep(h3) {
  font-size: 1.25em;
  color: #333;
}

:deep(ul), :deep(ol) {
  padding-left: 2em;
}

:deep(li + li) {
  margin-top: 0.25em;
}

:deep(a) {
  color: #c62828; /* 紫荆红 */
  text-decoration: none;
}

:deep(a:hover) {
  text-decoration: underline;
}

:deep(pre) {
  padding: 16px;
  overflow: auto;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 3px;
}

:deep(code) {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27,31,35,0.05);
  border-radius: 3px;
}

:deep(blockquote) {
  margin: 0;
  padding: 0 1em;
  color: #6a737d;
  border-left: 0.25em solid #c62828; /* 紫荆红 */
}

:deep(table) {
  border-spacing: 0;
  border-collapse: collapse;
  width: 100%;
}

:deep(table th) {
  font-weight: 600;
  padding: 6px 13px;
  border: 1px solid #dfe2e5;
  background-color: #f5f5f5;
}

:deep(table td) {
  padding: 6px 13px;
  border: 1px solid #dfe2e5;
}

:deep(table tr) {
  background-color: #fff;
  border-top: 1px solid #c6cbd1;
}

:deep(table tr:nth-child(2n)) {
  background-color: #f6f8fa;
}

/* 步骤指示器样式 */
.step-indicator {
  margin-bottom: 30px;
}

.step-content {
  margin-top: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.step-title {
  color: #c62828;
  margin-bottom: 15px;
  font-weight: bold;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.step-description {
  color: #666;
  margin-bottom: 20px;
  font-size: 14px;
}

.edit-options {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-end;
}

.outline-editor {
  margin-bottom: 20px;
}

.outline-preview {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  min-height: 300px;
  max-height: 500px;
  overflow-y: auto;
}

.outline-preview-compact {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  max-height: 300px;
  overflow-y: auto;
}

.outline-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.confirm-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.info-item {
  margin-bottom: 10px;
}

.info-label {
  font-weight: bold;
  color: #333;
  margin-right: 10px;
}

.info-value {
  color: #666;
}

.status-card, .success-card {
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  margin-top: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.status-info, .success-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.status-icon {
  font-size: 48px;
  color: #ba003f; /* 修改为紫荆红色 */
  margin-right: 20px;
}

.success-icon {
  font-size: 48px;
  color: #ba003f; /* 修改为紫荆红色 */
  margin-right: 20px;
}

.status-details, .success-details {
  flex: 1;
}

.status-title, .success-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #ba003f; /* 修改为紫荆红色 */
}

.success-title {
  color: #ba003f; /* 修改为紫荆红色 */
}

.status-desc, .success-desc {
  color: #666;
  margin-bottom: 10px;
}

.status-time, .success-time, .status-doc-id {
  font-size: 13px;
  color: #999;
  margin-top: 5px;
}

.status-actions, .success-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.download-btn {
  background-color: #67c23a;
  border-color: #67c23a;
}

.download-btn:hover {
  background-color: #529b2e;
  border-color: #529b2e;
}

/* 自定义按钮的紫荆红色主题 */
.action-buttons {
  :deep(.el-button--primary) {
    background-color: #ba003f;
    border-color: #ba003f;
  }
  
  :deep(.el-button--primary:hover),
  :deep(.el-button--primary:focus) {
    background-color: #d40046;
    border-color: #d40046;
  }
  
  :deep(.el-button--primary.is-disabled),
  :deep(.el-button--primary.is-disabled:hover),
  :deep(.el-button--primary.is-disabled:focus) {
    background-color: #f9d1db;
    border-color: #f9d1db;
  }
  
  :deep(.el-button--success) {
    background-color: #ba003f;
    border-color: #ba003f;
  }
  
  :deep(.el-button--success:hover),
  :deep(.el-button--success:focus) {
    background-color: #d40046;
    border-color: #d40046;
  }
}

/* 自定义进度条的紫荆红色主题 */
:deep(.el-progress-bar__inner) {
  background-color: #ba003f !important;
}

:deep(.el-progress__text) {
  color: #ba003f !important;
}

/* 添加新样式 */
.input-with-button {
  display: flex;
  gap: 10px;
  width: 100%;
}

.input-with-button :deep(.el-input) {
  width: 75% !important;
}

.example-title-btn {
  white-space: nowrap;
  width: 25%;
}

/* 添加计时器样式 */
.timer-container {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  border-left: 4px solid #ba003f;
}

.timer-label {
  font-weight: bold;
  margin-right: 10px;
  color: #ba003f;
}

.timer-value {
  font-family: monospace;
  font-size: 16px;
  color: #333;
}

/* 添加居中按钮样式 */
.center-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}
</style> 