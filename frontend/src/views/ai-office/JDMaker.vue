<template>
  <div class="contract-check-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>AI招聘JD生成</h2>
      </div>
      <div class="page-actions">
        <button class="action-btn" title="使用说明" @click="showTips">
          <i class="ri-lightbulb-line"></i>
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
            职位信息
          </h3>
        </div>
        
        <!-- 职位基本信息 -->
        <div class="form-group">
          <label for="job-title">职位名称</label>
          <input
            type="text"
            id="job-title"
            v-model="jobInfo.title"
            class="form-control"
            placeholder="例如：高级前端工程师"
          />
        </div>
        
        <div class="form-group">
          <label for="job-department">所属部门</label>
          <input
            type="text"
            id="job-department"
            v-model="jobInfo.department"
            class="form-control"
            placeholder="例如：研发部/技术中心"
          />
        </div>
        
        <div class="form-group">
          <label for="job-location">工作地点</label>
          <input
            type="text"
            id="job-location"
            v-model="jobInfo.location"
            class="form-control"
            placeholder="例如：北京/上海/广州"
          />
        </div>
        
        <div class="form-group">
          <label for="job-experience">工作经验要求</label>
          <select id="job-experience" v-model="jobInfo.experience" class="form-control">
            <option value="应届毕业生">应届毕业生</option>
            <option value="1-3年">1-3年</option>
            <option value="3-5年">3-5年</option>
            <option value="5-10年">5-10年</option>
            <option value="10年以上">10年以上</option>
          </select>
        </div>

        <div class="form-group">
          <label for="job-education">学历要求</label>
          <select id="job-education" v-model="jobInfo.education" class="form-control">
            <option value="不限">不限</option>
            <option value="大专">大专</option>
            <option value="本科">本科</option>
            <option value="硕士">硕士</option>
            <option value="博士">博士</option>
          </select>
        </div>
        
        <!-- JD生成重点 -->
        <div class="form-group">
          <label>JD重点</label>
          <div class="checkbox-group">
            <label class="checkbox-container">
              <input type="checkbox" v-model="jdFocus.responsibilities">
              <span>岗位职责</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="jdFocus.requirements">
              <span>任职要求</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="jdFocus.skills">
              <span>技能要求</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="jdFocus.benefits">
              <span>福利待遇</span>
            </label>
            <label class="checkbox-container">
              <input type="checkbox" v-model="jdFocus.company">
              <span>公司介绍</span>
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label for="job-keywords">关键技能/要求(用逗号分隔)</label>
          <textarea
            id="job-keywords"
            v-model="jobInfo.keywords"
            class="form-control"
            rows="3"
            placeholder="例如：Vue.js, React, 微前端, TypeScript"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="job-description">补充说明(选填)</label>
          <textarea
            id="job-description"
            v-model="jobInfo.description"
            class="form-control"
            rows="4"
            placeholder="可以添加其他需要说明的内容，如项目经历、行业背景等"
          ></textarea>
        </div>
        
        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="generateJD" class="btn btn-primary" :disabled="isGenerating || !jobInfo.title">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '生成中...' : 'AI生成JD' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：结果 -->
      <div class="right-column">
        <!-- 生成结果 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-file-list-3-line"></i>
              生成的招聘JD
            </h3>
            <div class="action-buttons">
              <button @click="generateJD" class="primary-button" :disabled="isGenerating || !jobInfo.title">
                <i class="ri-refresh-line" v-if="!isGenerating"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isGenerating ? '生成中...' : '重新生成' }}
              </button>
              <button @click="copyText" class="secondary-button" :disabled="isGenerating || !jdResult">
                <i class="ri-file-copy-line"></i>
                复制JD
              </button>
              <button @click="downloadResult" class="secondary-button" :disabled="isGenerating || !jdResult">
                <i class="ri-download-line"></i>
                下载JD
              </button>
            </div>
          </div>
          
          <!-- 参考案例区域 -->
          <div class="reference-section" v-if="!jdResult && !isGenerating">
            <h4 class="reference-title">参考案例</h4>
            <p class="reference-tip">点击案例可自动填充到左侧表单</p>
            <div class="reference-list">
              <div 
                v-for="(example, index) in referenceExamples" 
                :key="index" 
                class="reference-item"
                @click="applyExample(example)"
              >
                <div class="example-header">
                  <span class="example-title">{{ example.title }}</span>
                  <span class="example-tag">{{ example.department }}</span>
                </div>
                <div class="example-info">
                  <span><i class="ri-map-pin-line"></i> {{ example.location }}</span>
                  <span><i class="ri-time-line"></i> {{ example.experience }}</span>
                  <span><i class="ri-book-open-line"></i> {{ example.education }}</span>
                </div>
                <div class="example-skills">
                  <span v-for="(skill, skillIndex) in example.keywords.split(',')" :key="skillIndex" class="skill-tag">
                    {{ skill.trim() }}
                  </span>
                </div>
                <button class="apply-btn">
                  <i class="ri-arrow-left-line"></i> 应用此案例
                </button>
              </div>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isGenerating" class="loading-overlay">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <!-- 空状态 -->
            <div v-if="!jdResult && !isGenerating" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">请填写职位信息后生成JD</p>
              </div>
            </div>
            
            <!-- 生成结果展示 -->
            <div v-else-if="jdResult" class="contract-result" :class="{'blur-content': isGenerating}">
              <div class="result-content">
                <div v-html="formattedResult"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 使用说明模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line"></i> AI招聘JD生成使用说明</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>📝 <b>基本信息填写</b> - 填写职位名称、部门、工作地点等基本信息</li>
            <li>🔍 <b>JD重点选择</b> - 勾选需要在JD中重点突出的内容板块</li>
            <li>💼 <b>岗位职责</b> - 生成详细的岗位职责描述</li>
            <li>📋 <b>任职要求</b> - 根据选择的工作经验和学历自动生成符合要求的任职条件</li>
            <li>🔧 <b>技能要求</b> - 根据输入的关键技能生成技术技能要求</li>
            <li>🎁 <b>福利待遇</b> - 生成有吸引力的公司福利待遇描述</li>
            <li>🏢 <b>公司介绍</b> - 生成专业的公司简介</li>
          </ul>
          <div class="tips-note">
            <p><b>注意：</b>生成的JD仅供参考，请根据实际需求进行适当调整后使用。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElLoading } from 'element-plus'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

export default {
  name: 'JDMaker',
  setup() {
    // 状态变量
    const isGenerating = ref(false)
    const jdResult = ref('')
    const fileInput = ref(null)
    const showTipsModal = ref(false)
    const loadingText = ref('正在分析职位信息...')
    const messages = ref([])
    const loadingInstance = ref(null)

    // 职位信息
    const jobInfo = ref({
      title: '',
      department: '',
      location: '',
      experience: '3-5年',
      education: '本科',
      keywords: '',
      description: ''
    })

    // JD生成重点
    const jdFocus = ref({
      responsibilities: true,
      requirements: true,
      skills: true,
      benefits: true,
      company: false
    })

    // 参考案例数据
    const referenceExamples = [
      {
        title: '高级前端工程师',
        department: '技术研发中心',
        location: '北京',
        experience: '3-5年',
        education: '本科',
        keywords: 'Vue.js, React, TypeScript, 微前端, 性能优化',
        description: '负责公司核心产品的前端架构设计和开发，参与技术选型和重大技术决策。',
        focus: {
          responsibilities: true,
          requirements: true,
          skills: true,
          benefits: true,
          company: true
        }
      },
      {
        title: '产品经理',
        department: '产品部',
        location: '上海',
        experience: '5-10年',
        education: '本科',
        keywords: '用户研究, 需求分析, 产品规划, 数据分析, 项目管理',
        description: '负责企业级SaaS产品的全生命周期管理，主导产品从0到1的过程。',
        focus: {
          responsibilities: true,
          requirements: true,
          skills: true,
          benefits: true,
          company: false
        }
      },
      {
        title: '人工智能算法工程师',
        department: 'AI研究院',
        location: '深圳',
        experience: '3-5年',
        education: '硕士',
        keywords: '机器学习, 深度学习, Python, TensorFlow, PyTorch, NLP',
        description: '负责研发和优化大语言模型，解决实际业务场景中的AI应用问题。',
        focus: {
          responsibilities: true,
          requirements: true,
          skills: true,
          benefits: false,
          company: true
        }
      },
      {
        title: '销售经理',
        department: '销售部',
        location: '广州',
        experience: '5-10年',
        education: '本科',
        keywords: '客户开发, 销售管理, 谈判技巧, 团队管理, KPI制定',
        description: '负责企业级客户的开发和维护，制定销售策略，带领团队达成销售目标。',
        focus: {
          responsibilities: true,
          requirements: true,
          skills: false,
          benefits: true,
          company: false
        }
      }
    ]

    // 格式化结果
    const formattedResult = computed(() => {
      if (!jdResult.value) return ''
      // 使用marked将markdown格式转换为HTML
      const html = marked(jdResult.value)
      // 使用DOMPurify来防止XSS攻击
      return DOMPurify.sanitize(html)
    })

    // 执行JD生成
    const generateJD = async () => {
      // 验证是否有内容需要生成
      if (!jobInfo.value.title) {
        ElMessage.warning('请填写职位名称')
        return
      }

      // 设置正在生成状态
      isGenerating.value = true
      jdResult.value = ''

      // 显示加载指示器
      loadingInstance.value = ElLoading.service({
        lock: true,
        text: '正在分析职位信息...',
        background: 'rgba(255, 255, 255, 0.8)'
      })

      // 更新loading文本
      setTimeout(() => {
        loadingText.value = '正在撰写JD...'
      }, 3000)
      
      // 设置延时以显示多个loading文本
      setTimeout(() => {
        loadingText.value = '正在优化JD内容...'
      }, 6000)

      try {
        // 构建系统消息和用户消息
        const systemMessage = {
          role: "system",
          content: `你是一位专业的HR招聘专家，请根据提供的职位信息生成一份专业的招聘JD。请包含以下部分：
            ${jdFocus.value.company ? '- 公司介绍：简要描述公司情况' : ''}
            ${jdFocus.value.responsibilities ? '- 岗位职责：详细列出该职位的工作内容和职责' : ''}
            ${jdFocus.value.requirements ? '- 任职要求：包括必要的工作经验、学历要求' : ''}
            ${jdFocus.value.skills ? '- 技能要求：包括必备的专业技能和能力' : ''}
            ${jdFocus.value.benefits ? '- 福利待遇：列出公司提供的福利和薪资范围' : ''}
            请使用markdown格式输出，并确保专业、吸引力和针对性。`
        }

        const userMessage = {
          role: "user",
          content: `请为我生成一份职位JD，职位信息如下：
          - 职位名称：${jobInfo.value.title}
          - 所属部门：${jobInfo.value.department}
          - 工作地点：${jobInfo.value.location}
          - 工作经验：${jobInfo.value.experience}
          - 学历要求：${jobInfo.value.education}
          - 关键技能/要求：${jobInfo.value.keywords}
          ${jobInfo.value.description ? `- 补充说明：${jobInfo.value.description}` : ''}
          请根据以上信息生成一份专业、吸引力强的招聘JD。`
        }

        // 将消息添加到数组
        messages.value = [systemMessage, userMessage]

        // 准备请求参数
        const requestData = {
          messages: messages.value,
          model: "deepseek-v3-vol",
          temperature: 0.7
        }

        console.log('发送请求数据:', JSON.stringify(requestData))

        // 使用完整URL路径，不依赖axios默认设置
        const chatUrl = `${axios.defaults.baseURL}/api/v1/llm/chat`
        console.log('聊天API URL:', chatUrl)

        // 发送请求到服务器
        const chatResponse = await axios.post(chatUrl, requestData, {
          timeout: 120000, // 增加超时时间到120秒
          headers: {
            'Content-Type': 'application/json'
          }
        })

        // 处理响应
        console.log("完整API响应:", JSON.stringify(chatResponse.data));
        if (chatResponse.data && chatResponse.data.status === 'success' && chatResponse.data.data && chatResponse.data.data.choices && chatResponse.data.data.choices.length > 0) {
          console.log("API返回成功");
          const content = chatResponse.data.data.choices[0].message.content;
          console.log("API返回内容预览:", content.substring(0, 100));
          jdResult.value = content;
        } else if (chatResponse.data && chatResponse.data.choices && chatResponse.data.choices.length > 0) {
          console.log("API返回成功(无data包装层)");
          const content = chatResponse.data.choices[0].message.content;
          console.log("API返回内容预览:", content.substring(0, 100));
          jdResult.value = content;
        } else {
          const errorMsg = chatResponse.data?.error || chatResponse.data?.data?.error || '未知错误'
          console.error('API返回错误:', errorMsg)
          ElMessage.error(`JD生成失败: ${errorMsg}`)
        }
      } catch (error) {
        console.error('JD生成错误:', error)
        let errorMessage = 'JD生成失败，请稍后重试'
        
        if (error.response) {
          // 服务器返回了状态码
          console.error('错误状态:', error.response.status)
          console.error('错误数据:', error.response.data)
          errorMessage = `JD生成失败: ${error.response.status} - ${error.response.data?.error || '未知错误'}`
        } else if (error.request) {
          // 请求发出但没有收到响应
          console.error('没有收到响应:', error.request)
          // 尝试输出请求详情以便调试
          console.error('请求URL:', error.config?.url)
          console.error('请求方法:', error.config?.method)
          console.error('请求数据:', JSON.stringify(error.config?.data))
          errorMessage = '服务器没有响应，请检查网络连接或后端服务状态'
        }
        
        ElMessage.error(errorMessage)
      } finally {
        // 关闭加载指示器
        if (loadingInstance.value) {
          loadingInstance.value.close()
        }
        // 重置状态
        isGenerating.value = false
      }
    }

    // 应用参考案例
    const applyExample = (example) => {
      jobInfo.value = {
        title: example.title,
        department: example.department,
        location: example.location,
        experience: example.experience,
        education: example.education,
        keywords: example.keywords,
        description: example.description
      }
      
      jdFocus.value = example.focus
      
      ElMessage.success(`已应用"${example.title}"案例`)
      
      // 滚动到左侧表单顶部
      setTimeout(() => {
        const inputSection = document.querySelector('.input-section')
        if (inputSection) {
          inputSection.scrollTop = 0
        }
      }, 100)
    }

    // 复制文本
    const copyText = () => {
      if (!jdResult.value) return
      
      navigator.clipboard.writeText(jdResult.value)
        .then(() => {
          ElMessage.success('已复制到剪贴板')
        })
        .catch(err => {
          console.error('复制失败:', err)
          ElMessage.error('复制失败')
        })
    }

    // 下载结果
    const downloadResult = () => {
      if (!jdResult.value) return
      
      const filename = `${jobInfo.value.title}_招聘JD_${new Date().toLocaleDateString().replace(/\//g, '-')}.md`
      const blob = new Blob([jdResult.value], { type: 'text/markdown' })
      const link = document.createElement('a')
      
      link.href = URL.createObjectURL(blob)
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      ElMessage.success('JD下载成功')
    }

    // 显示提示
    const showTips = () => {
      showTipsModal.value = true
    }

    // 重置表单
    const resetForm = () => {
      jobInfo.value = {
        title: '',
        department: '',
        location: '',
        experience: '3-5年',
        education: '本科',
        keywords: '',
        description: ''
      }
      jdFocus.value = {
        responsibilities: true,
        requirements: true,
        skills: true,
        benefits: true,
        company: false
      }
      jdResult.value = ''
    }

    return {
      jobInfo,
      jdFocus,
      isGenerating,
      jdResult,
      showTipsModal,
      loadingText,
      formattedResult,
      referenceExamples,
      generateJD,
      resetForm,
      copyText,
      downloadResult,
      showTips,
      applyExample,
    }
  }
}
</script>

<style scoped>
.contract-check-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f7f7f7;
}

.page-header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.page-nav {
  display: flex;
  align-items: center;
}

.page-nav h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.page-actions {
  display: flex;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: rgba(186, 0, 63, 0.1);
  color: #ba003f;
}

.main-container {
  display: flex;
  flex: 1;
  min-height: 0;
  padding: 16px;
  gap: 16px;
}

.input-section {
  width: 400px;
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  overflow-y: auto;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 8px;
  color: #ba003f;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-control:focus {
  border-color: #ba003f;
  outline: none;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-container input {
  margin-right: 6px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.btn {
  padding: 10px 16px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  border: none;
}

.btn i {
  margin-right: 6px;
}

.btn-primary {
  background-color: #ba003f;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #d4185b;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #666;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e6e6e6;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.primary-button,
.secondary-button {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  border: none;
}

.primary-button {
  background-color: #ba003f;
  color: white;
}

.primary-button:hover:not(:disabled) {
  background-color: #d4185b;
}

.secondary-button {
  background-color: rgba(186, 0, 63, 0.1);
  color: #ba003f;
}

.secondary-button:hover:not(:disabled) {
  background-color: rgba(186, 0, 63, 0.15);
}

.primary-button:disabled,
.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-button i,
.secondary-button i {
  margin-right: 6px;
  font-size: 14px;
}

.result-content-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(186, 0, 63, 0.3);
  border-top: 3px solid #ba003f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 14px;
  color: #333;
}

.empty-result {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
  border-radius: 8px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px;
}

.empty-image {
  width: 80px;
  margin-bottom: 16px;
}

.empty-message {
  color: #666;
  text-align: center;
}

.contract-result {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
}

.result-content {
  background: #fff;
  border-radius: 4px;
  padding: 0 8px;
}

.blur-content {
  filter: blur(2px);
}

.spinning {
  animation: spin 1s linear infinite;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
}

.modal-header h3 i {
  margin-right: 8px;
  color: #ba003f;
}

.close-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #666;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background-color: #f0f0f0;
  color: #333;
}

.modal-body {
  padding: 24px;
}

.tips-list {
  list-style-type: none;
  padding: 0;
  margin: 0 0 16px 0;
}

.tips-list li {
  margin-bottom: 12px;
  font-size: 14px;
  color: #333;
}

.tips-note {
  background-color: #f8f8f8;
  border-left: 3px solid #ba003f;
  padding: 12px 16px;
  font-size: 14px;
  color: #555;
  border-radius: 0 4px 4px 0;
}

.reference-section {
  margin-bottom: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  padding: 16px;
}

.reference-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.reference-tip {
  font-size: 13px;
  color: #666;
  margin: 0 0 16px 0;
}

.reference-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.reference-item {
  background-color: white;
  border: 1px solid #eaeaea;
  border-radius: 6px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  position: relative;
}

.reference-item:hover {
  border-color: #ba003f;
  box-shadow: 0 2px 8px rgba(186, 0, 63, 0.1);
  transform: translateY(-2px);
}

.example-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.example-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.example-tag {
  font-size: 12px;
  color: #ba003f;
  background-color: rgba(186, 0, 63, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
}

.example-info {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #555;
}

.example-info span {
  display: flex;
  align-items: center;
}

.example-info i {
  margin-right: 4px;
  font-size: 14px;
}

.example-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.skill-tag {
  font-size: 12px;
  color: #555;
  background-color: #f0f0f0;
  padding: 2px 8px;
  border-radius: 4px;
}

.apply-btn {
  background-color: transparent;
  border: 1px dashed #ba003f;
  color: #ba003f;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: auto;
  transition: all 0.2s;
}

.apply-btn:hover {
  background-color: rgba(186, 0, 63, 0.05);
}

.apply-btn i {
  margin-right: 4px;
}

@media (max-width: 1024px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section {
    width: 100%;
  }

  .reference-list {
    grid-template-columns: 1fr;
  }
}
</style> 