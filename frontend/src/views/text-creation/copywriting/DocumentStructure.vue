<template>
  <div class="document-structure-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>文档结构撰写</h2>
      </div>
      <div class="page-actions">
        <button class="action-btn" title="创作小贴士" @click="showTips">
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
            <i class="ri-settings-3-line"></i>
            输入参数
          </h3>
        </div>
        
        <!-- 文档类型选择 -->
        <div class="form-group">
          <label for="document-type">文档类型</label>
          <select id="document-type" v-model="selectedType" class="form-control">
            <option v-for="type in documentTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
          </select>
        </div>
        
        <!-- 文档用途选择 -->
        <div class="form-group">
          <label for="document-purpose">文档用途</label>
          <select id="document-purpose" v-model="selectedPurpose" class="form-control">
            <option v-for="purpose in documentPurposes" :key="purpose.id" :value="purpose.id">{{ purpose.name }}</option>
          </select>
        </div>
        
        <!-- 目标受众 -->
        <div class="form-group">
          <label for="target-audience">目标受众</label>
          <select id="target-audience" v-model="selectedAudience" class="form-control">
            <option v-for="audience in audienceOptions" :key="audience.id" :value="audience.id">{{ audience.name }}</option>
          </select>
        </div>
        
        <!-- 文档标题 -->
        <div class="form-group">
          <label for="document-title" class="required">文档标题</label>
          <input 
            type="text" 
            id="document-title" 
            v-model="topic" 
            placeholder="请输入文档标题"
            class="form-control"
          />
        </div>
        
        <!-- 文档目的 -->
        <div class="form-group">
          <label for="document-purpose" class="required">文档目的</label>
          <textarea 
            id="document-purpose" 
            v-model="keyPoints" 
            placeholder="描述文档的关键要点"
            class="form-control"
            rows="5"
          ></textarea>
        </div>
        
        <div class="form-row">
          <!-- 删除三个原始选项（包括研究方法、包括背景信息、包括未来计划） -->
        </div>
        
        <!-- 文档包含元素 (移动到AI模型上面) -->
        <div class="panel-section document-elements">
          <h3>文档包含元素</h3>
          <div class="elements-container">
            <label class="element-checkbox">
              <input type="checkbox" id="include-summary" v-model="includeSummary">
              <span>摘要/总结</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-toc" v-model="includeTableOfContents">
              <span>目录</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-intro" v-model="includeIntroduction">
              <span>引言</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-background" v-model="includeBackground">
              <span>背景信息</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-methods" v-model="includeMethods">
              <span>研究方法</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-charts" v-model="includeCharts">
              <span>图表数据</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-case-studies" v-model="includeCaseStudies">
              <span>案例研究</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-findings" v-model="includeFindings">
              <span>关键发现</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-implementation" v-model="includeImplementation">
              <span>实施计划</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-resources" v-model="includeResources">
              <span>资源分配</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-conclusion" v-model="includeConclusion">
              <span>结论</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-future" v-model="includeFuturePlans">
              <span>未来计划</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-references" v-model="includeReferences">
              <span>参考文献</span>
            </label>
            <label class="element-checkbox">
              <input type="checkbox" id="include-appendix" v-model="includeAppendix">
              <span>附录</span>
            </label>
          </div>
        </div>
        
        <!-- 添加模型选择 -->
        <div class="panel-section">
          <h3>AI模型</h3>
          <div class="form-group">
            <label class="form-label">AI模型选择:</label>
            <select id="model-select" v-model="selectedModel" class="form-control" :disabled="modelList.length === 0">
              <option v-for="model in modelList" :key="model.id" :value="model.id">
                {{ model.name }}
              </option>
              <option v-if="modelList.length === 0" value="" disabled>加载模型列表中...</option>
            </select>
            <div v-if="modelList.length === 0" class="model-loading">
              <i class="ri-loader-4-line"></i> 正在加载可用模型...
            </div>
          </div>
        </div>
        
        <!-- 删除这里原来的文档包含元素部分，已移至上方 -->
        
        <div class="action-buttons">
          <button class="btn btn-primary" @click="generateContent" :disabled="isGenerating">
            <i class="ri-magic-line" v-if="!isGenerating"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isGenerating ? '正在生成...' : '生成文档结构' }}
          </button>
          <button class="btn btn-secondary" @click="resetForm">
            <i class="ri-refresh-line"></i> 重置
          </button>
        </div>
      </div>
      
      <!-- 右侧：参考案例和结果 -->
      <div class="right-column">
        <!-- 参考案例部分 -->
        <div class="examples-section">
          <div class="examples-header">
            <h3 class="section-title">
              <i class="ri-lightbulb-flash-line"></i>
              参考案例
            </h3>
            <!-- 添加轮播控制按钮 -->
            <div class="carousel-controls">
              <button class="carousel-control prev" @click="prevExample" :class="{ 'disabled': currentExampleIndex <= 0 }">
                <i class="ri-arrow-left-s-line"></i>
              </button>
              <button class="carousel-control next" @click="nextExample" :class="{ 'disabled': isLastPage }">
                <i class="ri-arrow-right-s-line"></i>
              </button>
            </div>
          </div>
          
          <div class="example-carousel">
            <div class="example-cards" ref="exampleCarousel">
              <div class="example-card" v-for="(example, index) in examples" :key="index" @click="loadExample(index)">
                <div class="example-icon">
                  <i :class="example.icon"></i>
                </div>
                <div class="example-info">
                  <span class="example-title">{{ example.title }}</span>
                  <span class="example-desc">{{ example.desc }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 结果展示部分 -->
        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-article-line"></i>
              文档结构
            </h3>
            <div class="action-buttons">
              <button @click="generateContent" class="primary-button" :disabled="isLoading">
                <i class="ri-refresh-line" v-if="!isLoading"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isLoading ? '生成中...' : '重新生成' }}
              </button>
              <button @click="copyContent" class="secondary-button" :disabled="isLoading || !generatedStructure">
                <i class="ri-file-copy-line"></i>
                复制结构
              </button>
              <button @click="showPrompt" class="prompt-button" :disabled="!lastUsedPrompt">
                <i class="ri-code-line"></i>
                查看提示词
              </button>
            </div>
          </div>
          
          <div class="result-content-wrapper">
            <!-- 加载动画 -->
            <div v-if="isLoading" class="loading-overlay">
              <div class="loading-steps">
                <div v-for="(step, index) in steps" :key="step.id" 
                     class="step-item" 
                     :class="{ 
                       'active': currentStep >= step.id, 
                       'current': currentStep === step.id,
                       'completed': currentStep > step.id 
                     }">
                  <div class="step-icon">
                    <i :class="step.icon"></i>
                  </div>
                  <div class="step-info">
                    <div class="step-name">{{ step.name }}</div>
                    <div class="step-status" v-if="currentStep === step.id">
                      <div class="loading-dots">
                        <span></span><span></span><span></span>
                      </div>
                    </div>
                    <div class="step-status" v-else-if="currentStep > step.id">
                      <i class="ri-check-line"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="loading-text">{{ loadingText }}</div>
            </div>
            
            <div v-if="!generatedStructure" class="empty-result">
              <div class="empty-content">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbC1vcGFjaXR5PSIuMDgiIGZpbGw9IiNEOEQ4RDgiIGN4PSI2NCIgY3k9IjY0IiByPSI2NCIvPjxwYXRoIGQ9Ik00MS41OTkgNDkuODhjMS4xIDAgMiAuOSAyIDJ2MzIuMjRjMCAxLjEtLjkgMi0yIDJoLTguOTdhLjk3Ljk3IDAgMDEtLjk1LS45NSAwIDAgMCAwLS4wNCAwIDAgMCAwLS4wM3YtMjkuNTFjMC0xLjk5IDEuNjItMy42MiAzLjYyLTMuNjJsMCAwUTQxLjU5OCA0OS44OTggNDEuNTk5IDQ5Ljg4ek04Ni4wNyA0OS44OGMxLjEgMCAyIC45IDIgMnYzMi4yNGMwIDEuMS0uOSAyLTIgMmgtOC45N3MtLjk2LS43OS0uOTYtLjk2VjUyLjgyYzAtMS42MiAxLjMyLTIuOTUgMi45NS0yLjk1bDAgMGg2Ljk4ek02NC4wNyA0Ni44M2MxLjMxIDAgMi4zNyAxLjA2IDIuMzcgMi4zN3YzNC44OGMwIDEuMzEtMS4wNiAyLjM3LTIuMzcgMi4zN2gtOS43YTIuMzcgMi4zNyAwIDAxLTIuMzctMi4zN1Y0OS4yYzAtMS4zMSAxLjA2LTIuMzcgMi4zNy0yLjM3bDAgMGg5LjciIGZpbGw9IiNFMUUxRTEiLz48cGF0aCBkPSJNMzIuNjMgNjkuNzVjMCAyLjYgMi4xMSA0LjcxIDQuNzEgNC43MXMyLjYtMi4xMSA0LjctNC43MS0yLjExLTQuNzEtNC43LTQuNzEtNC43MSAyLjExLTQuNzEgNC43MXpNODcuMDMgNjkuNzVjMCAyLjYtMi4xMSA0LjcxLTQuNzEgNC43MXMtNC43MS0yLjExLTQuNzEtNC43MSAyLjExLTQuNzEgNC43MS00LjcxIDQuNzEgMi4xMSA0LjcxIDQuNzF6TTY0LjQgNjcuMzhjMCAzLjczLTMuMDIgNi43NS02Ljc1IDYuNzVzLTYuNzYtMy4wMi02Ljc2LTYuNzUgMy4wMy02Ljc2IDYuNzYtNi43NiA2Ljc1IDMuMDMgNi43NSA2Ljc2eiIgZmlsbD0iI0JBMDA0MCIgZmlsbC1vcGFjaXR5PSIuNSIvPjwvZz48L3N2Zz4=" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无文档结构内容，请点击"生成文档结构"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedStructure" class="article-result" :class="{'blur-content': isLoading}">
              <!-- 添加离线模式提示条 -->
              <div v-if="isOfflineGenerated" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板结构。要获得AI生成的更优质结构，请联系管理员启动后端服务。</span>
              </div>
              
              <!-- 添加调试显示 -->
              <div class="debug-content" style="margin-bottom: 20px; padding: 10px; border: 1px solid #f0f0f0; background-color: #f9f9f9;">
                <h4 style="color: #666;">原始内容（调试模式）:</h4>
                <pre style="white-space: pre-wrap; word-break: break-all;">{{ generatedStructure }}</pre>
              </div>
              
              <div class="article-content" v-html="formattedContent"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态窗口 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line"></i> 创作小贴士</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <ul class="tips-list">
            <li>使用标题和小标题来组织文章结构，使内容层次分明</li>
            <li>保持段落简短，每段聚焦一个主题或观点</li>
            <li>使用列表和编号来展示步骤或关键点</li>
            <li>适当使用粗体和斜体来强调重要内容</li>
            <li>增加实例和数据来支持你的观点</li>
          </ul>
        </div>
      </div>
    </div>
    
    <!-- 提示词模态窗口 -->
    <div class="modal" v-if="showPromptModal">
      <div class="modal-content prompt-modal">
        <div class="modal-header">
          <h3><i class="ri-code-box-line"></i> 生成提示词</h3>
          <button class="close-btn" @click="showPromptModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="prompt-content">
            <pre>{{ lastUsedPrompt }}</pre>
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
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { ElMessage } from 'element-plus';
// 导入简化版API测试函数
import { testApiConnection } from '../../../utils/apiTest';

export default {
  name: 'DocumentStructure',
  setup() {
    const router = useRouter();
    const toast = useToast();
    
    // 模型列表
    const modelList = ref([]);
    const selectedModel = ref('');
    
    // 文档类型选项
    const documentTypes = ref([
      { id: 'report', name: '报告' },
      { id: 'presentation', name: '演示文稿' },
      { id: 'proposal', name: '提案' },
      { id: 'article', name: '文章' },
      { id: 'manual', name: '手册' },
      { id: 'whitepaper', name: '白皮书' },
      { id: 'marketing', name: '营销方案' }
    ]);
    
    // 文档用途选项
    const documentPurposes = ref([
      { id: 'informative', name: '信息传递' },
      { id: 'persuasive', name: '说服/建议' },
      { id: 'instructional', name: '教学/指导' },
      { id: 'analysis', name: '分析/研究' },
      { id: 'marketing', name: '营销/推广' }
    ]);
    
    // 文档受众选项
    const audienceOptions = ref([
      { id: 'technical', name: '技术人员' },
      { id: 'business', name: '商业决策者' },
      { id: 'general', name: '普通大众' },
      { id: 'academic', name: '学术/研究人员' },
      { id: 'students', name: '学生' }
    ]);
    
    // 旧的表单数据变量
    const documentType = ref('business');
    const documentTitle = ref('');
    const documentPurpose = ref('');
    const targetAudience = ref('');
    const documentLength = ref('medium');
    const keyPoints = ref('');
    const additionalNotes = ref('');
    
    // 新的表单数据（用于替换旧的表单数据）
    const selectedType = ref('report');  // 设置默认值为'report'
    const topic = ref('');
    const selectedPurpose = ref('analysis');  // 设置默认值为'analysis'
    const selectedAudience = ref('business');  // 设置默认值为'business'
    
    // 文档包含元素选项
    const includeSummary = ref(false);      // 摘要/总结
    const includeTableOfContents = ref(false); // 目录
    const includeIntroduction = ref(false); // 引言
    const includeMethods = ref(false);      // 研究方法
    const includeBackground = ref(false);   // 背景信息
    const includeCharts = ref(false);       // 图表数据
    const includeCaseStudies = ref(false);  // 案例研究
    const includeFindings = ref(false);     // 关键发现
    const includeImplementation = ref(false); // 实施计划
    const includeResources = ref(false);    // 资源分配
    const includeConclusion = ref(false);   // 结论
    const includeReferences = ref(false);   // 参考文献
    const includeAppendix = ref(false);     // 附录
    const includeFuturePlans = ref(false);  // 未来计划
    
    // 结果状态
    const isGenerating = ref(false);
    const isLoading = ref(false);
    const isOfflineGenerated = ref(false);
    const generatedStructure = ref('');  // 使用ref来定义初始值为空字符串
    const loadingText = ref('正在生成文档结构...');
    const lastUsedPrompt = ref('');
    
    // 步骤状态
    const currentStep = ref(0);
    const steps = [
      { id: 1, name: '生成提示词', icon: 'ri-file-text-line', status: 'pending' },
      { id: 2, name: '测试AI大模型连通性', icon: 'ri-wifi-line', status: 'pending' },
      { id: 3, name: '传递提示词', icon: 'ri-send-plane-line', status: 'pending' },
      { id: 4, name: 'AI创作中', icon: 'ri-brain-line', status: 'pending' },
      { id: 5, name: '获取结果', icon: 'ri-inbox-archive-line', status: 'pending' },
      { id: 6, name: '完成', icon: 'ri-check-double-line', status: 'pending' }
    ];
    
    // 模态窗口
    const showPromptModal = ref(false);
    const showTipsModal = ref(false);
    
    // 参考案例
    const examples = ref([
      {
        title: '商业计划书',
        desc: '适合创业融资',
        icon: 'ri-briefcase-line',
        data: {
          documentType: 'business',
          documentTitle: '零碳科技创业商业计划书',
          documentPurpose: '为零碳科技公司的创业项目寻求投资融资，展示公司的商业模式、市场机会和盈利潜力',
          targetAudience: '潜在投资者、风险投资公司',
          documentLength: 'medium',
          keyPoints: '- 环保科技创新解决方案\n- 目标市场规模和增长趋势\n- 产品技术优势和专利保护\n- 营销策略和销售渠道\n- 财务预测和投资回报分析\n- 管理团队背景',
          additionalNotes: '需要包含详细的财务模型和市场分析数据'
        }
      },
      {
        title: '研究报告',
        desc: '适合学术研究',
        icon: 'ri-book-open-line',
        data: {
          documentType: 'research',
          documentTitle: '5G技术对远程医疗发展的影响研究',
          documentPurpose: '分析5G技术为远程医疗带来的机遇与挑战，并提出应用建议',
          targetAudience: '医疗信息化管理人员、医院管理者、政策制定者',
          documentLength: 'long',
          keyPoints: '- 当前远程医疗技术现状\n- 5G技术关键特性分析\n- 5G对医疗图像传输的改进\n- 实时远程手术可能性\n- 患者监控设备创新\n- 案例研究与实践经验\n- 实施挑战与建议',
          additionalNotes: '需要包含国内外多个成功案例分析'
        }
      },
      {
        title: '白皮书',
        desc: '适合技术产品',
        icon: 'ri-file-paper-2-line',
        data: {
          documentType: 'whitepaper',
          documentTitle: '企业级区块链解决方案白皮书',
          documentPurpose: '介绍我司区块链技术在企业应用中的创新方案，解释技术原理和应用场景',
          targetAudience: '企业CTO、IT决策者、技术采购负责人',
          documentLength: 'comprehensive',
          keyPoints: '- 区块链技术概述和发展趋势\n- 传统系统面临的挑战\n- 我司区块链方案架构\n- 安全性和隐私保护设计\n- 性能优化与扩展性\n- 应用场景示例\n- 实施路径与ROI分析',
          additionalNotes: '强调我们的方案与竞争对手的差异化优势'
        }
      },
      {
        title: '操作手册',
        desc: '适合技术指导',
        icon: 'ri-book-read-line',
        data: {
          documentType: 'handbook',
          documentTitle: '企业数据安全管理操作手册',
          documentPurpose: '为企业IT管理人员提供数据安全管理的标准操作流程和最佳实践指南',
          targetAudience: 'IT管理员、系统管理员、信息安全专员',
          documentLength: 'medium',
          keyPoints: '- 数据分类与敏感度标记\n- 访问控制策略制定\n- 数据加密标准与实施\n- 备份与恢复流程\n- 安全事件响应流程\n- 员工安全意识培训\n- 合规审计检查要点',
          additionalNotes: '需要包含详细的操作截图和步骤说明'
        }
      },
      {
        title: '项目提案',
        desc: '适合项目申请',
        icon: 'ri-projector-line',
        data: {
          documentType: 'proposal',
          documentTitle: '智慧城市交通系统改造项目提案',
          documentPurpose: '向市政部门申请智慧交通系统改造项目，展示技术方案和实施计划',
          targetAudience: '城市规划者、交通管理部门负责人、政府决策者',
          documentLength: 'medium',
          keyPoints: '- 当前交通系统痛点分析\n- 智慧交通系统架构设计\n- 人工智能交通预测模型\n- 实时数据监控与分析\n- 分阶段实施计划\n- 投资回报与社会效益\n- 案例城市成功经验',
          additionalNotes: '需要强调方案的可扩展性和与现有系统的兼容性'
        }
      },
      {
        title: '市场调研',
        desc: '适合市场分析',
        icon: 'ri-line-chart-line',
        data: {
          documentType: 'research',
          documentTitle: '2023年中国电动汽车市场调研报告',
          documentPurpose: '分析中国电动汽车市场现状、消费者偏好和未来趋势，为产品策略提供依据',
          targetAudience: '汽车制造企业高管、产品经理、投资分析师',
          documentLength: 'long',
          keyPoints: '- 中国电动汽车市场规模与增长\n- 消费者购买决策因素分析\n- 充电基础设施现状评估\n- 主要竞争对手产品对比\n- 政策支持与监管趋势\n- 技术发展路线图\n- 未来五年市场预测',
          additionalNotes: '需要包含大量图表和数据可视化'
        }
      },
      {
        title: '培训课程',
        desc: '适合教育培训',
        icon: 'ri-mental-health-line',
        data: {
          documentType: 'handbook',
          documentTitle: '数据分析师入门到精通培训课程',
          documentPurpose: '设计一套完整的数据分析培训课程，涵盖基础知识到高级应用',
          targetAudience: '职场新人、转行人士、在职提升者',
          documentLength: 'comprehensive',
          keyPoints: '- 数据分析基础概念\n- Excel高级数据处理\n- SQL数据库查询\n- Python数据分析库应用\n- 数据可视化技巧\n- 统计学原理与应用\n- 商业智能工具实战\n- 真实项目案例实践',
          additionalNotes: '每个模块需要包含练习和测验'
        }
      },
      {
        title: '产品规划',
        desc: '适合产品开发',
        icon: 'ri-rocket-line',
        data: {
          documentType: 'proposal',
          documentTitle: '智能家居中央控制系统产品规划',
          documentPurpose: '制定智能家居中央控制系统的产品路线图和开发计划',
          targetAudience: '产品开发团队、工程师、公司高管',
          documentLength: 'medium',
          keyPoints: '- 市场需求与机会分析\n- 核心功能定义\n- 技术架构设计\n- 用户体验设计原则\n- 开发里程碑规划\n- 上市策略\n- 后续迭代方向',
          additionalNotes: '需要关注与其他智能家居产品的互操作性'
        }
      },
      {
        title: '营销策略',
        desc: '适合品牌推广',
        icon: 'ri-advertisement-line',
        data: {
          documentType: 'marketing',
          documentTitle: '新品牌市场营销全渠道策略',
          documentPurpose: '为新上市的消费品牌制定全面的市场营销策略和执行计划',
          targetAudience: '营销团队、品牌经理、社交媒体专员',
          documentLength: 'medium',
          keyPoints: '- 目标受众画像分析\n- 品牌定位与核心信息\n- 社交媒体营销策略\n- 内容营销计划\n- KOL合作方案\n- 线下活动规划\n- 营销效果评估框架',
          additionalNotes: '需包含竞品分析和差异化战略'
        }
      },
      {
        title: '战略规划',
        desc: '适合企业发展',
        icon: 'ri-pie-chart-line',
        data: {
          documentType: 'business',
          documentTitle: '五年企业战略发展规划',
          documentPurpose: '制定公司未来五年的战略目标、业务发展方向和实施路径',
          targetAudience: '公司董事会、高管团队、投资人',
          documentLength: 'long',
          keyPoints: '- 行业趋势与市场机会\n- 企业核心竞争力分析\n- 战略目标与关键绩效指标\n- 业务扩展规划\n- 人才发展战略\n- 风险管理框架\n- 资源配置与财务规划',
          additionalNotes: '需要包含多种情景分析和应对策略'
        }
      }
    ]);
    
    // 轮播控制
    const currentExampleIndex = ref(0);
    const exampleCarousel = ref(null);
    
    const isLastPage = computed(() => {
      if (!exampleCarousel.value) return true;
      const totalWidth = examples.value.length * 168; // 160px宽度 + 8px间距
      const visibleWidth = exampleCarousel.value.offsetWidth;
      const maxScroll = totalWidth - visibleWidth;
      return currentExampleIndex.value * 168 >= maxScroll;
    });
    
    // 格式化结果
    const formattedContent = computed(() => {
      if (!generatedStructure.value) return '';
      
      // 基本格式化处理，包括换行符转换为HTML标签、标题加粗等
      let formatted = generatedStructure.value
        .replace(/\n/g, '<br>')
        .replace(/#{1,6}\s+(.*?)$/gm, '<h3>$1</h3>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
      
      return formatted;
    });
    
    // 获取模型列表
    const fetchModels = async () => {
      try {
        console.log('正在获取可用模型列表...');
        // 使用完整URL
        const response = await axios.get('http://localhost:9000/api/v1/llm/models', { timeout: 5000 });
        console.log('获取模型响应:', response);
        
        if (response.data && response.data.status === 'success') {
          modelList.value = response.data.data || [];
          
          console.log('可用模型:', modelList.value);
          
          // 默认选择火山引擎的DeepSeek V3模型
          selectedModel.value = 'deepseek-v3-vol';
          
          // 如果没有可用模型，创建一个默认列表作为备用
          if (modelList.value.length === 0) {
            setupDefaultModels();
          }
        } else {
          console.error('获取模型列表失败:', response.data ? response.data.message : '未知错误');
          setupDefaultModels();
        }
      } catch (error) {
        console.error('获取模型列表异常:', error);
        console.error('错误详情:', error.message);
        if (error.response) {
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
        }
        setupDefaultModels();
      }
    };
    
    // 设置默认模型列表
    const setupDefaultModels = () => {
      modelList.value = [
        { id: 'deepseek-v3-vol', name: 'DeepSeek-V3（火山引擎）' },
        { id: 'deepseek-r1-vol', name: 'DeepSeek-R1（火山引擎）' },
        { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      selectedModel.value = 'deepseek-v3-vol';
    };
    
    // 轮播控制函数
    const prevExample = () => {
      if (currentExampleIndex.value > 0) {
        currentExampleIndex.value--;
        scrollCarousel();
      }
    };
    
    const nextExample = () => {
      if (!isLastPage.value) {
        currentExampleIndex.value++;
        scrollCarousel();
      }
    };
    
    const scrollCarousel = () => {
      if (exampleCarousel.value) {
        const scrollAmount = currentExampleIndex.value * 168; // 160px宽度 + 8px间距
        exampleCarousel.value.style.transform = `translateX(-${scrollAmount}px)`;
      }
    };
    
    // 加载示例
    const loadExample = (index) => {
      if (!examples.value[index]) return;
      
      const example = examples.value[index];
      console.log('加载案例:', example); // 调试日志
      
      try {
        // 文档类型映射 - 确保映射关系正确
        const typeMapping = {
          'business': 'report',
          'academic': 'article',
          'technical': 'manual',
          'proposal': 'proposal',
          'research': 'report',
          'whitepaper': 'whitepaper',
          'marketing': 'marketing',
          'handbook': 'manual'
        };
        
        // 文档用途映射 - 确保映射关系正确
        const purposeMapping = {
          'business': 'analysis',
          'academic': 'informative',
          'technical': 'instructional',
          'proposal': 'persuasive',
          'research': 'analysis',
          'whitepaper': 'informative',
          'marketing': 'marketing',
          'handbook': 'instructional'
        };
        
        // 受众映射 - 将描述性文本映射到ID
        const audienceMapping = {
          '潜在投资者、风险投资公司': 'business',
          '医疗信息化管理人员、医院管理者、政策制定者': 'technical',
          '企业CTO、IT决策者、技术采购负责人': 'technical',
          'IT管理员、系统管理员、信息安全专员': 'technical',
          '城市规划者、交通管理部门负责人、政府决策者': 'business',
          '汽车制造企业高管、产品经理、投资分析师': 'business',
          '职场新人、转行人士、在职提升者': 'general',
          '产品开发团队、工程师、公司高管': 'technical',
          '营销团队、品牌经理、社交媒体专员': 'business',
          '公司董事会、高管团队、投资人': 'business'
        };
        
        // 设置表单数据
        selectedType.value = typeMapping[example.data.documentType] || 'report';
        topic.value = example.data.documentTitle || '';
        selectedPurpose.value = purposeMapping[example.data.documentType] || 'informative';
        selectedAudience.value = audienceMapping[example.data.targetAudience] || 'business';
        keyPoints.value = example.data.keyPoints || '';
        
        // 设置额外选项
        includeSummary.value = ['research', 'whitepaper', 'business'].includes(example.data.documentType);
        includeTableOfContents.value = ['research', 'whitepaper', 'technical'].includes(example.data.documentType);
        includeIntroduction.value = true; // 大多数文档都需要引言
        includeMethods.value = ['research', 'academic'].includes(example.data.documentType);
        includeBackground.value = ['business', 'whitepaper'].includes(example.data.documentType);
        includeCharts.value = ['business', 'research', 'whitepaper'].includes(example.data.documentType);
        includeCaseStudies.value = ['business', 'marketing'].includes(example.data.documentType);
        includeFindings.value = ['research', 'academic'].includes(example.data.documentType);
        includeImplementation.value = ['proposal', 'business'].includes(example.data.documentType);
        includeResources.value = ['proposal', 'business'].includes(example.data.documentType);
        includeConclusion.value = true; // 大多数文档都需要结论
        includeReferences.value = ['research', 'academic', 'whitepaper'].includes(example.data.documentType);
        includeAppendix.value = ['research', 'technical', 'whitepaper'].includes(example.data.documentType);
        includeFuturePlans.value = ['business', 'proposal'].includes(example.data.documentType);
        
        console.log('已设置表单值:', {
          selectedType: selectedType.value,
          selectedPurpose: selectedPurpose.value,
          selectedAudience: selectedAudience.value,
          topic: topic.value
        });
      } catch (error) {
        console.error('设置表单值出错:', error);
      }
    };
    
    // 测试API连通性
    const testApiConnection = async () => {
      try {
        console.log('\n=== 开始测试API连接 ===');
        const testData = {
          messages: [
            {
              role: 'user',
              content: '测试连接'
            }
          ],
          model: 'deepseek-v3-vol'
        };
        
        console.log('发送测试请求数据:', JSON.stringify(testData, null, 2));
        
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', testData, {
          timeout: 30000
        });
        
        console.log('测试响应状态码:', response.status);
        console.log('测试响应数据:', response.data);
        
        if (response.data && response.data.choices && response.data.choices.length > 0) {
          console.log('API连接测试成功');
          return true;
        } else if (response.data && response.data.content) {
          console.log('API连接测试成功');
          return true;
        } else {
          console.log('API连接测试失败：响应格式不正确');
          return false;
        }
      } catch (error) {
        console.error('API连接测试失败:', error);
        return false;
      }
    };
    
    // 更新步骤状态
    const updateStep = (stepId, status = 'processing') => {
      currentStep.value = stepId;
      // 更新步骤状态
      steps.forEach(step => {
        if (step.id < stepId) {
          step.status = 'completed';
        } else if (step.id === stepId) {
          step.status = status;
        } else {
          step.status = 'pending';
        }
      });
      
      // 更新加载文本
      switch(stepId) {
        case 1:
          loadingText.value = '正在生成提示词...';
          break;
        case 2:
          loadingText.value = '正在测试AI大模型连通性...';
          break;
        case 3:
          loadingText.value = '正在传递提示词...';
          break;
        case 4:
          loadingText.value = 'AI正在创作中，请稍候...';
          break;
        case 5:
          loadingText.value = '正在获取生成结果...';
          break;
        case 6:
          loadingText.value = '生成完成！';
          break;
        default:
          loadingText.value = '正在处理...';
      }
    };
    
    // 生成文档结构
    const generateContent = async () => {
      try {
        console.log('\n=== 开始生成文档结构 ===');
        console.log('当前表单数据:', {
          selectedType: selectedType.value,
          topic: topic.value,
          selectedPurpose: selectedPurpose.value,
          selectedAudience: selectedAudience.value,
          keyPoints: keyPoints.value
        });
        
        if (!topic.value || !keyPoints.value) {
          console.log('错误：标题或内容为空');
          ElMessage.error('请填写标题和内容');
          return;
        }

        // 设置加载状态
        isLoading.value = true;
        isGenerating.value = true;
        currentStep.value = 1;
        
        console.log('\n=== 准备API请求 ===');
        const prompt = buildPrompt();
        lastUsedPrompt.value = prompt;
        
        console.log('生成的提示词:', prompt);
        
        const requestData = {
          messages: [
            {
              role: 'user',
              content: prompt
            }
          ],
          model: 'deepseek-v3-vol'
        };
        
        console.log('发送的请求数据:', JSON.stringify(requestData, null, 2));
        
        // 更新步骤状态
        currentStep.value = 2;
        console.log('\n=== 发送API请求 ===');
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', requestData, {
          timeout: 60000 // 设置60秒超时
        });
        
        console.log('\n=== 收到API响应 ===');
        console.log('响应状态码:', response.status);
        console.log('响应头:', response.headers);
        console.log('完整响应数据:', JSON.stringify(response.data, null, 2));
        
        // 详细日志输出，记录每个层级的数据结构
        console.log('\n=== 详细API响应结构分析 ===');
        if (response.data) {
          console.log('1. response.data存在，类型:', typeof response.data);
          console.log('2. response.data包含的字段:', Object.keys(response.data));
          
          if (response.data.status) {
            console.log('3. status字段值:', response.data.status);
          }
          
          if (response.data.data) {
            console.log('4. data嵌套字段存在，类型:', typeof response.data.data);
            console.log('5. data嵌套字段包含:', Object.keys(response.data.data));
            
            if (response.data.data.choices) {
              console.log('6. choices数组长度:', response.data.data.choices.length);
              console.log('7. 第一个choice内容:', JSON.stringify(response.data.data.choices[0], null, 2));
              
              if (response.data.data.choices[0].message) {
                console.log('8. 消息内容:', response.data.data.choices[0].message.content);
              }
            }
          }
        }
        
        // 关键修改：处理backend返回的标准格式
        if (response.data && response.data.status === 'success' && response.data.data) {
          console.log('标准后端响应格式检测成功');
          // 保存原始data对象的引用
          const apiResponseData = response.data.data;
          
          console.log('API响应data字段:', JSON.stringify(apiResponseData, null, 2));
          
          // 检查API响应中是否有choices
          if (apiResponseData.choices && apiResponseData.choices.length > 0) {
            const content = apiResponseData.choices[0].message.content;
            console.log('\n=== 提取的内容(choices) ===');
            console.log('原始内容:', content);
            
            generatedStructure.value = content;
            console.log('已设置generatedStructure:', generatedStructure.value);
            
            // 更新步骤状态
            currentStep.value = 6;
            ElMessage.success('文档结构生成成功');
            return; // 提前返回
          }
        }
        
        // 如果没有找到标准格式，继续尝试其他格式
        if (response.data && response.data.choices && response.data.choices.length > 0) {
          const content = response.data.choices[0].message.content;
          console.log('\n=== 提取的内容 ===');
          console.log('原始内容:', content);
          
          generatedStructure.value = content;
          console.log('已设置generatedStructure:', generatedStructure.value);
          
          // 更新步骤状态
          currentStep.value = 6;
          ElMessage.success('文档结构生成成功');
        } else if (response.data && response.data.content) {
          // 处理直接返回content的情况
          const content = response.data.content;
          console.log('\n=== 提取的内容 ===');
          console.log('原始内容:', content);
          
          generatedStructure.value = content;
          console.log('已设置generatedStructure:', generatedStructure.value);
          
          // 更新步骤状态
          currentStep.value = 6;
          ElMessage.success('文档结构生成成功');
        } else if (response.data && response.data.data && response.data.data.choices && response.data.data.choices.length > 0) {
          // 处理火山引擎API的响应格式
          const content = response.data.data.choices[0].message.content;
          console.log('\n=== 提取的内容 ===');
          console.log('原始内容:', content);
          
          generatedStructure.value = content;
          console.log('已设置generatedStructure:', generatedStructure.value);
          
          // 更新步骤状态
          currentStep.value = 6;
          ElMessage.success('文档结构生成成功');
        } else {
          console.log('错误：响应数据格式不正确');
          console.log('响应数据:', response.data);
          ElMessage.error('生成失败：响应数据格式不正确');
        }
      } catch (error) {
        console.error('\n=== 发生错误 ===');
        console.error('错误类型:', error.name);
        console.error('错误信息:', error.message);
        if (error.response) {
          console.error('错误响应状态码:', error.response.status);
          console.error('错误响应数据:', error.response.data);
        }
        console.error('错误堆栈:', error.stack);
        
        ElMessage.error(`生成失败：${error.message}`);
      } finally {
        // 重置加载状态
        isLoading.value = false;
        isGenerating.value = false;
      }
    };
    
    // 构建提示词
    const buildPrompt = () => {
      // 根据选定的类型获取类型名称
      const getTypeName = () => {
        const typeMap = {
          'report': '报告',
          'presentation': '演示文稿',
          'proposal': '提案',
          'article': '文章',
          'manual': '手册',
          'whitepaper': '白皮书',
          'marketing': '营销方案'
        };
        return typeMap[selectedType.value] || '报告';
      };
      
      // 根据选定的目的获取目的名称
      const getPurposeName = () => {
        const purposeMap = {
          'informative': '信息传递',
          'persuasive': '说服/建议',
          'instructional': '教学/指导',
          'analysis': '分析/研究',
          'marketing': '营销/推广'
        };
        return purposeMap[selectedPurpose.value] || '信息传递';
      };
      
      // 根据选定的受众获取受众名称
      const getAudienceName = () => {
        const audienceMap = {
          'technical': '技术人员',
          'business': '商业决策者',
          'general': '普通大众',
          'academic': '学术/研究人员',
          'students': '学生'
        };
        return audienceMap[selectedAudience.value] || '普通大众';
      };
      
      // 构建提示词文本
      let prompt = `请为我创建一个${getTypeName()}的详细结构大纲。\n\n`;
      prompt += `文档标题：${topic.value}\n`;
      prompt += `文档类型：${getTypeName()}\n`;
      prompt += `文档用途：${getPurposeName()}\n`;
      prompt += `目标受众：${getAudienceName()}\n`;
      prompt += `关键内容：${keyPoints.value}\n\n`;
      
      // 添加文档应包含的元素
      prompt += "文档应包含以下元素：\n";
      if (includeSummary.value) prompt += "- 摘要/总结\n";
      if (includeTableOfContents.value) prompt += "- 目录\n";
      if (includeIntroduction.value) prompt += "- 引言\n";
      if (includeMethods.value) prompt += "- 研究方法\n";
      if (includeBackground.value) prompt += "- 背景信息\n";
      if (includeCharts.value) prompt += "- 图表数据\n";
      if (includeCaseStudies.value) prompt += "- 案例研究\n";
      if (includeFindings.value) prompt += "- 关键发现\n";
      if (includeImplementation.value) prompt += "- 实施计划\n";
      if (includeResources.value) prompt += "- 资源分配\n";
      if (includeConclusion.value) prompt += "- 结论\n";
      if (includeReferences.value) prompt += "- 参考文献\n";
      if (includeAppendix.value) prompt += "- 附录\n";
      if (includeFuturePlans.value) prompt += "- 未来计划\n";
      
      prompt += "\n请提供一个详细且组织良好的结构大纲，包括主要章节和子章节，以帮助我创建一个高质量、专业的文档。";
      
      return prompt;
    };
    
    // 离线模式下生成基础模板
    const generateOfflineTemplate = () => {
      const types = {
        business: {
          title: '商业报告',
          sections: [
            { title: '执行摘要', desc: '概述报告的主要发现、结论和建议' },
            { title: '背景介绍', desc: '介绍报告的上下文、目的和范围' },
            { title: '市场分析', desc: '详细分析目标市场规模、趋势和竞争情况' },
            { title: '产品/服务描述', desc: '详细描述产品或服务及其特点和价值主张' },
            { title: '营销策略', desc: '说明如何推广和销售产品或服务' },
            { title: '运营计划', desc: '详细说明业务运营的方式和资源需求' },
            { title: '财务计划', desc: '提供详细的财务预测和分析' },
            { title: '结论与建议', desc: '总结主要发现并提出具体建议' },
            { title: '附录', desc: '包含支持性文件和详细数据' }
          ]
        },
        research: {
          title: '研究报告',
          sections: [
            { title: '摘要', desc: '概述研究的主要发现和结论' },
            { title: '引言', desc: '介绍研究背景、目的和范围' },
            { title: '文献综述', desc: '回顾和评估相关研究文献' },
            { title: '研究方法', desc: '详细说明研究设计、方法和分析技术' },
            { title: '研究结果', desc: '呈现研究发现和数据分析结果' },
            { title: '讨论', desc: '解释研究结果并与现有文献进行比较' },
            { title: '结论', desc: '总结主要发现并提出建议' },
            { title: '参考文献', desc: '列出引用的所有资料来源' },
            { title: '附录', desc: '包含补充材料和详细数据' }
          ]
        }
      };
      
      // 选择适当的模板，如果没有特定类型的模板，则使用商业报告模板
      const template = types[selectedType.value] || types.business;
      
      let result = `# ${topic.value || template.title}\n\n`;
      
      template.sections.forEach((section, index) => {
        result += `## ${index + 1}. ${section.title}\n${section.desc}\n\n`;
      });
      
      return result;
    };
    
    // 复制结果
    const copyResult = () => {
      if (!generatedStructure.value) return;
      
      // 创建一个纯文本版本的结构内容
      const textContent = generatedStructure.value;
      
      navigator.clipboard.writeText(textContent)
        .then(() => {
          toast.success('文档结构已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          toast.error('复制失败，请手动选择并复制');
        });
    };
    
    // 显示提示词
    const showPrompt = () => {
      if (lastUsedPrompt.value) {
        console.log('显示提示词模态框');
        showPromptModal.value = true;
      } else {
        toast.info('请先生成文档结构以查看提示词');
      }
    };
    
    // 复制提示词到剪贴板
    const copyPrompt = () => {
      if (!lastUsedPrompt.value) return;
      
      try {
        // 检查是否支持clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(lastUsedPrompt.value)
            .then(() => {
              toast.success('提示词已复制到剪贴板');
            })
            .catch(err => {
              console.error('复制失败:', err);
              fallbackCopy(lastUsedPrompt.value);
            });
        } else {
          // 浏览器不支持clipboard API，使用备选方法
          fallbackCopy(lastUsedPrompt.value);
        }
      } catch (error) {
        console.error('复制操作异常:', error);
        fallbackCopy(lastUsedPrompt.value);
      }
    };
    
    // 备选的复制方法
    const fallbackCopy = (text) => {
      try {
        // 创建临时textarea元素
        const textArea = document.createElement('textarea');
        textArea.value = text;
        
        // 设置样式使元素不可见
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        
        // 选择文本并执行复制命令
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        if (successful) {
          toast.success('内容已复制到剪贴板');
        } else {
          toast.error('复制失败，请手动复制');
        }
        
        // 清理临时元素
        document.body.removeChild(textArea);
      } catch (err) {
        console.error('备选复制方法失败:', err);
        toast.error('复制失败，请手动复制文本');
      }
    };
    
    // 重置表单
    const resetForm = () => {
      selectedType.value = 'report';
      topic.value = '';
      selectedPurpose.value = 'analysis';
      selectedAudience.value = 'business';
      includeSummary.value = false;
      includeTableOfContents.value = false;
      includeIntroduction.value = false;
      includeMethods.value = false;
      includeBackground.value = false;
      includeCharts.value = false;
      includeCaseStudies.value = false;
      includeFindings.value = false;
      includeImplementation.value = false;
      includeResources.value = false;
      includeConclusion.value = false;
      includeReferences.value = false;
      includeAppendix.value = false;
      includeFuturePlans.value = false;
      
      toast.info('表单已重置');
    };
    
    // 显示创作小贴士
    const showTips = () => {
      showTipsModal.value = true;
    };
    
    // 生命周期钩子
    onMounted(() => {
      fetchModels();
    });
    
    // 计算属性
    const renderedMarkdown = computed(() => {
      console.log('渲染Markdown，内容:', generatedStructure.value);
      if (!generatedStructure.value) return '';
      
      try {
        // 使用marked库将markdown转为html (如果项目中已有)
        // return marked(generatedStructure.value);
        
        // 简单格式化处理，将markdown转为HTML
        // 如果没有使用marked库，可以实现简单的转换
        let html = generatedStructure.value
          // 处理标题
          .replace(/^# (.*$)/gm, '<h1>$1</h1>')
          .replace(/^## (.*$)/gm, '<h2>$1</h2>')
          .replace(/^### (.*$)/gm, '<h3>$1</h3>')
          // 处理列表
          .replace(/^\* (.*$)/gm, '<li>$1</li>')
          .replace(/^- (.*$)/gm, '<li>$1</li>')
          // 处理分隔线
          .replace(/^---$/gm, '<hr>')
          // 处理段落
          .replace(/\n\n/g, '</p><p>')
          // 添加换行符
          .replace(/\n/g, '<br>');
        
        // 包装在段落中
        html = '<p>' + html + '</p>';
        
        // 列表项包装在ul中
        html = html.replace(/<li>.*?<\/li>/g, function(match) {
          return '<ul>' + match + '</ul>';
        });
        
        console.log('渲染后的HTML:', html);
        return html;
      } catch (error) {
        console.error('Markdown渲染错误:', error);
        return '<p>渲染错误: ' + error.message + '</p><pre>' + generatedStructure.value + '</pre>';
      }
    });
    
    return {
      // 状态和数据
      modelList,
      selectedModel,
      
      // 旧的表单数据
      documentType,
      documentTitle,
      documentPurpose,
      targetAudience,
      documentLength,
      keyPoints,
      additionalNotes,
      
      // 新的表单数据
      selectedType,
      topic,
      selectedPurpose,
      selectedAudience,
      includeSummary,
      includeTableOfContents,
      includeIntroduction,
      includeMethods,
      includeBackground,
      includeCharts,
      includeCaseStudies,
      includeFindings,
      includeImplementation,
      includeResources,
      includeConclusion,
      includeReferences,
      includeAppendix,
      includeFuturePlans,
      
      isGenerating,
      isLoading,
      isOfflineGenerated,
      generatedStructure,
      loadingText,
      lastUsedPrompt,
      showPromptModal,
      showTipsModal,
      examples,
      currentExampleIndex,
      exampleCarousel,
      isLastPage,
      formattedContent,
      
      // 步骤状态
      steps,
      currentStep,
      
      // 方法
      prevExample,
      nextExample,
      loadExample,
      generateContent,
      copyResult,
      copyPrompt,
      fallbackCopy,
      resetForm,
      showPrompt,
      showTips,
      
      // 新增属性
      documentTypes,
      documentPurposes,
      audienceOptions,
    };
  }
};
</script>

<style scoped>
/* 全局样式 */
.document-structure-page {
  padding: 0 20px 15px 20px; /* 将顶部内边距设为0 */
  margin-top: -30px; /* 增加负上边距到-30px */
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px; /* 进一步减少底部边距 */
  margin-top: 0; /* 确保顶部没有边距 */
}

.page-nav h2 {
  font-size: 1.3rem; /* 略微减小标题 */
  font-weight: 600;
  color: #333;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 15px;
}

.action-btn {
  background: none;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: #eaeaea;
  color: #BA003F;
}

.main-container {
  display: flex;
  gap: 15px;
  margin-top: -8px; /* 增加负边距 */
}

.input-section {
  width: 45%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #444;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.section-title i {
  color: #BA003F;
  font-size: 1.1rem;
}

.form-group {
  margin-bottom: 16px;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
}

.form-row .form-group {
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  padding: 8px 12px;
  border-radius: 4px;
  gap: 8px;
  min-width: 140px;
}

.form-row .form-group label {
  margin-bottom: 0;
  font-size: 13px;
  white-space: nowrap;
}

.form-row .form-group input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 6px;
  color: #555;
}

.form-group label.required::after {
  content: '*';
  color: #BA003F;
  margin-left: 4px;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #BA003F;
  outline: none;
  box-shadow: 0 0 0 3px rgba(186, 0, 63, 0.1);
}

textarea.form-control {
  min-height: 100px;
  resize: vertical;
}

select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23555' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
}

.form-note {
  font-size: 12px;
  color: #777;
  margin-top: 4px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.btn {
  border: none;
  border-radius: 6px;
  padding: 10px 15px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
}

.btn i {
  font-size: 16px;
}

.btn-primary {
  background-color: #BA003F;
  color: white;
  flex: 2;
}

.btn-primary:hover {
  background-color: #9D0036;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #444;
}

.btn-secondary:hover {
  background-color: #e5e5e5;
}

.model-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.spinning {
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 参考案例部分 */
.examples-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 15px;
}

.examples-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.carousel-controls {
  display: flex;
  gap: 8px;
}

.carousel-control {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #f5f5f5;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.carousel-control:hover {
  background-color: #eaeaea;
}

.carousel-control.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.example-carousel {
  overflow: hidden;
}

.example-cards {
  display: flex;
  gap: 8px; /* 减少间距 */
  transition: transform 0.3s ease;
}

.example-card {
  min-width: 160px; /* 进一步减小宽度 */
  flex: 0 0 auto;
  background-color: #fff;
  border-radius: 8px;
  padding: 10px; /* 减少内边距 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #eee;
}

.example-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  border-color: #BA003F;
}

.example-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(186, 0, 63, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 8px;
}

.example-icon i {
  font-size: 20px;
  color: #BA003F;
}

.example-info {
  display: flex;
  flex-direction: column;
  text-align: center;
}

.example-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #333;
}

.example-desc {
  font-size: 12px;
  color: #666;
}

/* 结果部分 */
.result-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 15px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.result-content-wrapper {
  position: relative;
  flex-grow: 1;
  overflow: hidden;
  margin-top: -5px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  padding: 20px;
}

.loading-steps {
  display: flex;
  flex-direction: column;
  width: 80%;
  max-width: 450px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 20px;
}

.step-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.step-item:last-child {
  border-bottom: none;
}

.step-item.active {
  opacity: 1;
}

.step-item.current {
  background-color: rgba(186, 0, 63, 0.05);
  border-radius: 8px;
  padding: 12px 8px;
}

.step-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  transition: all 0.3s ease;
}

.step-item.active .step-icon {
  background-color: rgba(186, 0, 63, 0.1);
  color: #BA003F;
}

.step-item.completed .step-icon {
  background-color: #BA003F;
  color: white;
}

.step-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.step-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.step-status {
  font-size: 14px;
  display: flex;
  align-items: center;
}

.step-item.completed .step-status {
  color: #52c41a;
}

.loading-dots {
  display: flex;
  align-items: center;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  margin: 0 2px;
  background-color: #BA003F;
  border-radius: 50%;
  display: inline-block;
  animation: dot-flashing 1s infinite linear alternate;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dot-flashing {
  0% { opacity: 0.2; }
  100% { opacity: 1; }
}

.loading-text {
  font-size: 15px;
  color: #555;
  font-weight: 500;
  text-align: center;
}

.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 250px;
}

.empty-content {
  text-align: center;
  padding: 20px;
}

.empty-image {
  width: 70px;
  height: 70px;
  margin-bottom: 12px;
}

.empty-message {
  font-size: 14px;
  color: #666;
  max-width: 300px;
  margin: 0 auto;
}

.article-result {
  padding: 8px;
  overflow-y: auto;
  max-height: 600px;
}

.blur-content {
  filter: blur(2px);
}

.article-content {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

.article-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #BA003F;
  margin: 16px 0 8px 0;
}

.offline-mode-banner {
  background-color: #FFF8E1;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #856404;
}

.primary-button, .secondary-button, .prompt-button {
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background-color 0.2s;
}

.primary-button {
  background-color: #BA003F;
  color: white;
}

.primary-button:hover {
  background-color: #9D0036;
}

.secondary-button {
  background-color: #f5f5f5;
  color: #444;
}

.secondary-button:hover {
  background-color: #e5e5e5;
}

.prompt-button {
  background-color: var(--primary-color, #ba003f);
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
}

.prompt-button:hover {
  background-color: #980034;
}

.prompt-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #ccc;
  color: #666;
}

/* 模态窗口样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
  animation: modal-pop 0.3s ease-out;
}

@keyframes modal-pop {
  0% { transform: scale(0.9); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-header h3 i {
  color: var(--primary-color, #ba003f);
}

.close-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 20px;
  cursor: pointer;
  line-height: 1;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}

.prompt-content {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  border-left: 3px solid #BA003F;
  margin: 0;
}

.tips-list {
  padding-left: 20px;
  margin: 10px 0;
}

.tips-list li {
  margin-bottom: 10px;
  color: #555;
  line-height: 1.5;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  padding: 15px 0 0;
}

.prompt-modal {
  max-width: 700px;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .main-container {
    flex-direction: column;
  }
  
  .input-section, .right-column {
    flex: none;
    width: 100%;
  }
}

/* AI模型选择下拉框样式 */
.model-select-wrapper {
  position: relative;
  width: 100%;
}

.model-select {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  background-color: #fff;
  transition: all 0.3s;
  color: #333;
  font-size: 14px;
}

.model-select:hover {
  border-color: #c0c4cc;
}

.model-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-width: 450px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  z-index: 10;
  margin-top: 8px;
  overflow: hidden;
  animation: dropdown-fade 0.2s ease;
}

@keyframes dropdown-fade {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.model-dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  font-weight: 500;
  color: #333;
}

.close-dropdown {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #909399;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-dropdown:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.model-list {
  max-height: 350px;
  overflow-y: auto;
  padding: 5px 0;
}

.model-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.model-item:hover {
  background-color: #f5f7fa;
}

.model-item.active {
  background-color: #ecf5ff;
}

.model-info {
  flex: 1;
  padding-right: 10px;
}

.model-name {
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
  font-size: 14px;
}

.model-desc {
  font-size: 12px;
  color: #909399;
  white-space: normal;
  line-height: 1.4;
}

.model-check {
  color: #409EFF;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.model-loading {
  display: flex;
  align-items: center;
  padding: 10px;
  color: #909399;
  font-size: 13px;
}

.model-loading i {
  margin-right: 6px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 文档目的输入框样式 */
textarea#document-purpose {
  min-height: 120px;
  padding: 12px;
  font-size: 14px;
  line-height: 1.5;
  resize: vertical;
}

/* 添加紧凑布局的样式 */
.form-row {
  margin-bottom: 5px;
}
.form-group label {
  font-size: 0.9em;
  margin-left: 2px;
}

/* 文档包含元素的新样式 */
.document-elements {
  margin-bottom: 15px;
}
.elements-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}
.element-checkbox {
  display: flex;
  align-items: center;
  width: calc(25% - 8px);
  font-size: 0.9em;
  background-color: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.element-checkbox:hover {
  background-color: #e9ecef;
}
.element-checkbox input {
  margin-right: 4px;
}

.prompt-content {
  background-color: #f5f5f5;
  border-radius: 6px;
  padding: 15px;
  overflow-x: auto;
  font-family: Consolas, Monaco, 'Andale Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  white-space: pre-wrap;
  max-height: 50vh;
  overflow-y: auto;
}

.prompt-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}
</style> 