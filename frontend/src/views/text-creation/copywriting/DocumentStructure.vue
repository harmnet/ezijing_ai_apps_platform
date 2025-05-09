<template>
  <div class="document-structure-page text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>文档结构撰写</h2>
      </div>
      <div class="page-actions">
        <button class="learn-button" @click="showTips">
          <i class="ri-lightbulb-line"></i>
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
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-lightbulb-flash-line"></i>
              参考案例
            </h3>
            <!-- 添加轮播控制按钮 -->
            <div class="carousel-controls">
              <button type="button" class="carousel-control prev" @click="prevExample($event)" :class="{ 'disabled': currentExampleIndex <= 0 }">
                <i class="ri-arrow-left-s-line"></i>
              </button>
              <button type="button" class="carousel-control next" @click="nextExample($event)" :class="{ 'disabled': isLastPage }">
                <i class="ri-arrow-right-s-line"></i>
              </button>
            </div>
          </div>
          
          <div class="example-carousel">
            <div class="example-cards" ref="exampleCarousel">
              <div class="example-card" v-for="(example, index) in examples" :key="index" @click="loadExample(index)">
                <div class="example-card-header">
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
            <div v-if="isLoading && !isStreaming" class="loading-overlay">
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
                <img src="../../../assets/images/no_data.png" class="empty-image" alt="暂无数据" />
                <p class="empty-message">暂无文档结构内容，请点击"生成文档结构"按钮开始创作</p>
              </div>
            </div>
            
            <div v-else-if="generatedStructure" class="article-result" :class="{'blur-content': isLoading, 'streaming': isStreaming}">
              <!-- 添加离线模式提示条 -->
              <div v-if="isOfflineGenerated" class="offline-mode-banner">
                <i class="ri-information-line"></i>
                <span>您当前正在使用离线模式，生成的是基础模板结构。要获得AI生成的更优质结构，请联系管理员启动后端服务。</span>
              </div>
              
              <!-- 添加流式输出指示器 -->
              <div v-if="isStreaming" class="streaming-indicator">
                <i class="ri-loader-4-line spinning"></i>
                <span>AI正在生成内容...</span>
              </div>
              
              <!-- 注释：原始内容显示区域已被隐藏 -->
              
              <!-- 模拟Word文档界面 -->
              <div class="word-document">
                <div class="word-toolbar">
                  <div class="toolbar-group">
                    <button class="toolbar-btn" title="保存为PDF" @click="saveAsPdf">
                      <i class="ri-file-pdf-line"></i>
                    </button>
                    <button class="toolbar-btn" title="打印文档" @click="printDocument">
                      <i class="ri-printer-line"></i>
                    </button>
                  </div>
                  <div class="toolbar-group">
                    <button class="toolbar-btn" title="粗体" @click="applyFormat('bold')">
                      <i class="ri-bold"></i>
                    </button>
                    <button class="toolbar-btn" title="斜体" @click="applyFormat('italic')">
                      <i class="ri-italic"></i>
                    </button>
                    <button class="toolbar-btn" title="下划线" @click="applyFormat('underline')">
                      <i class="ri-underline"></i>
                    </button>
                  </div>
                  <div class="toolbar-group">
                    <button class="toolbar-btn" title="左对齐" @click="applyAlign('left')">
                      <i class="ri-align-left"></i>
                    </button>
                    <button class="toolbar-btn" title="居中对齐" @click="applyAlign('center')">
                      <i class="ri-align-center"></i>
                    </button>
                    <button class="toolbar-btn" title="右对齐" @click="applyAlign('right')">
                      <i class="ri-align-right"></i>
                    </button>
                  </div>
                </div>
                <div class="word-page">
                  <!-- 修复v-html错误 -->
                  <div class="word-content">
                    <div v-html="wordFormattedContent"></div>
                  </div>
                  <!-- 添加页脚和页码 -->
                  <div class="word-footer">
                    <div class="word-page-number">第 1 页</div>
                    <div class="word-document-title">{{ topic || '文档结构' }}</div>
                  </div>
                </div>
                <!-- 添加状态栏 -->
                <div class="word-statusbar">
                  <div class="word-statusbar-item">100%</div>
                  <div class="word-statusbar-item">编辑</div>
                  <div class="word-statusbar-item">
                    <i class="ri-check-line"></i> 已保存
                  </div>
                  <div class="word-statusbar-item">
                    {{ new Date().toLocaleDateString('zh-CN') }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创作小贴士模态窗口 - 替换为el-drawer抽屉组件 -->
    <el-drawer
      v-model="showTipsModal"
      title="文档结构创作指南"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in documentStructureKnowledge" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="item.icon" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
      </div>
    </el-drawer>
    
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
import { ref, onMounted, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { ElMessage } from 'element-plus';
// 导入简化版API测试函数
import { testApiConnection } from '../../../utils/apiTest';
// 导入文档结构知识数据
import { documentStructureKnowledge } from '@/views/Knowledge_data.js';

export default {
  name: 'DocumentStructure',
  setup() {
    const router = useRouter();
    const toast = useToast();
    
    // 添加Markdown格式化函数
    const formatMarkdown = (text) => {
      if (!text) return '';
      
      // 处理粗体 **text**
      let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理列表项 - item (改进列表项处理逻辑)
      formatted = formatted.replace(/- (.*?)(?=\n|$)/g, '<li>$1</li>');
      
      // 将连续的列表项包装在ul标签中
      const listPattern = /<li>.*?<\/li>(?:\s*<li>.*?<\/li>)*/gs;
      formatted = formatted.replace(listPattern, '<ul>$&</ul>');
      
      // 处理换行符
      formatted = formatted.replace(/\n\n/g, '<br><br>');
      formatted = formatted.replace(/\n/g, '<br>');
      
      return formatted;
    };
    
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
    const isStreaming = ref(false); // 添加流式输出状态标记
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
      
      try {
        const totalWidth = examples.value.length * 168; // 160px宽度 + 8px间距
        const visibleWidth = exampleCarousel.value.parentElement?.offsetWidth || 0;
        const maxScroll = Math.max(0, totalWidth - visibleWidth);
        const currentScroll = currentExampleIndex.value * 168;
        
        console.log('轮播状态:', {
          totalWidth,
          visibleWidth,
          maxScroll,
          currentScroll,
          isLast: currentScroll >= maxScroll
        });
        
        return currentScroll >= maxScroll;
      } catch (error) {
        console.error('计算isLastPage时出错:', error);
        return true;
      }
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
    
    // Word风格的格式化内容
    const wordFormattedContent = computed(() => {
      if (!generatedStructure.value) return '';
      
      try {
        // 提取文档标题（如果存在）
        let documentTitle = topic.value || '文档结构';
        let contentWithoutTitle = generatedStructure.value;
        
        // 检查第一行是否是一级标题
        const titleMatch = generatedStructure.value.match(/^# (.+)$/m);
        if (titleMatch) {
          documentTitle = titleMatch[1];
          // 移除第一个标题，稍后会在封面添加
          contentWithoutTitle = generatedStructure.value.replace(/^# .+$/m, '');
        }
        
        // 创建封面
        let html = `
          <div class="word-cover">
            <div class="word-cover-title">${documentTitle}</div>
            <div class="word-cover-subtitle">${getTypeName()} - ${getPurposeName()}</div>
            <div class="word-cover-date">${new Date().toLocaleDateString('zh-CN')}</div>
            <div class="word-cover-author">AI助手生成</div>
          </div>
          <div class="word-page-break"></div>
        `;
        
        // 处理正文内容
        html += contentWithoutTitle
          // 处理一级标题
          .replace(/^# (.*$)/gm, '<div class="word-heading word-heading-1">$1</div>')
          // 处理二级标题
          .replace(/^## (.*$)/gm, '<div class="word-heading word-heading-2">$1</div>')
          // 处理三级标题
          .replace(/^### (.*$)/gm, '<div class="word-heading word-heading-3">$1</div>')
          // 处理四级标题
          .replace(/^#### (.*$)/gm, '<div class="word-heading word-heading-4">$1</div>')
          // 处理无序列表
          .replace(/^[\*\-] (.*$)/gm, '<div class="word-list-item"><span class="word-bullet">•</span>$1</div>')
          // 处理带编号的列表
          .replace(/^(\d+)\. (.*$)/gm, '<div class="word-list-item"><span class="word-number">$1.</span>$2</div>')
          // 处理粗体
          .replace(/\*\*(.*?)\*\*/g, '<span class="word-bold">$1</span>')
          // 处理斜体
          .replace(/\*(.*?)\*/g, '<span class="word-italic">$1</span>')
          // 处理代码块
          .replace(/```([\s\S]*?)```/g, '<div class="word-code-block">$1</div>')
          // 处理行内代码
          .replace(/`(.*?)`/g, '<span class="word-inline-code">$1</span>')
          // 处理分隔线
          .replace(/^---$/gm, '<hr class="word-hr">')
          // 处理引用块
          .replace(/^> (.*$)/gm, '<div class="word-blockquote">$1</div>')
          // 处理普通段落：找到不是标题和列表项的内容行
          .replace(/^(?!#|[\*\-]|\d+\.|>)(.+)$/gm, '<div class="word-paragraph">$1</div>')
          // 处理空行
          .replace(/^\s*$/gm, '<div class="word-paragraph-spacing"></div>');

        return html;
      } catch (error) {
        console.error('Word格式化错误:', error);
        return '<div class="word-paragraph">格式化错误: ' + error.message + '</div>';
      }
    });
    
    // 辅助函数：根据选定的类型获取类型名称
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
    
    // 辅助函数：根据选定的目的获取目的名称
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
    
    // 获取模型列表
    const fetchModels = async () => {
      try {
        console.log('正在获取可用模型列表...');
        // 使用完整URL
        const response = await axios.get(`${window.APP_CONFIG.API_BASE_URL}/api/v1/llm/models`, { timeout: 5000 });
        console.log('获取模型响应:', response);
        
        if (response.data && response.data.status === 'success') {
          // 过滤只保留火山引擎的R1和V3大模型以及豆包大模型
          const allModels = response.data.data || [];
          modelList.value = allModels.filter(model => 
            model.id === 'deepseek-v3-vol' || 
            model.id === 'deepseek-r1-vol' || 
            model.id === 'doupo'
          );
          
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
        { id: 'doupo', name: '豆包大模型' }
        // 以下模型已被注释掉
        // { id: 'deepseek-r1-sf', name: 'DeepSeek-R1（硅基流动）' },
        // { id: 'deepseek-v3-sf', name: 'DeepSeek-V3（硅基流动）' },
        // { id: 'qwq-32b', name: '通义千问-32B（硅基流动）' }
      ];
      // 确保默认选择火山引擎的V3模型
      selectedModel.value = 'deepseek-v3-vol';
    };
    
    // 轮播控制函数
    const prevExample = (event) => {
      // 阻止事件冒泡
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      
      if (currentExampleIndex.value > 0) {
        currentExampleIndex.value--;
        scrollCarousel();
        console.log('向前翻页:', currentExampleIndex.value);
      }
    };
    
    const nextExample = (event) => {
      // 阻止事件冒泡
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      
      if (!isLastPage.value) {
        currentExampleIndex.value++;
        scrollCarousel();
        console.log('向后翻页:', currentExampleIndex.value);
      }
    };
    
    const scrollCarousel = () => {
      if (exampleCarousel.value) {
        const scrollAmount = currentExampleIndex.value * 168; // 160px宽度 + 8px间距
        console.log('设置轮播滚动位置:', scrollAmount);
        exampleCarousel.value.style.transform = `translateX(-${scrollAmount}px)`;
      } else {
        console.error('轮播容器未找到');
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
        
        const response = await axios.post(`${window.APP_CONFIG.API_BASE_URL}/api/v1/llm/chat`, testData, {
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
        
        // 当不是流式输出时才更新步骤
        if (!isStreaming.value) {
          currentStep.value = 1;
        }
        
        console.log('\n=== 准备API请求 ===');
        const prompt = buildPrompt();
        lastUsedPrompt.value = prompt;
        
        console.log('生成的提示词:', prompt);
        
        // 创建API请求参数
        const apiParams = {
          messages: [
            {
              role: 'user',
              content: prompt
            }
          ],
          model: 'deepseek-v3', // 修改为deepseek-v3
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };
        
        console.log('发送的请求数据:', JSON.stringify(apiParams, null, 2));
        
        try {
          // 开始流式状态
          isStreaming.value = true;
          
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
          
          // 清空当前生成内容
          generatedStructure.value = '';
          
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
                    throw new Error(parsed.error.message || '生成文档结构失败');
                  }
                  
                  // 处理火山引擎返回的delta格式数据
                  if (parsed.choices && parsed.choices.length > 0 && parsed.choices[0].delta) {
                    const delta = parsed.choices[0].delta;
                    
                    // 处理内容增量
                    if (delta.content) {
                      console.log("收到内容增量:", delta.content);
                      // 累加收到的内容
                      generatedStructure.value += delta.content;
                    }
                  }
                } catch (e) {
                  console.error('解析流式数据失败:', e, data);
                }
              }
            }
          }
          
          // 处理完成，移除流式状态
          isStreaming.value = false;
          
          ElMessage.success('文档结构生成成功');
          isOfflineGenerated.value = false;
          
        } catch (error) {
          console.error('API调用异常:', error);
          
          // 结束流式状态
          isStreaming.value = false;
          
          // 判断是否是网络错误或服务器不可用
          if (!error.response || error.message.includes('Network Error') || error.message.includes('Failed to fetch')) {
            console.warn('后端服务不可用，切换到离线模式');
            // 离线模式
            generatedStructure.value = generateOfflineTemplate();
            isOfflineGenerated.value = true;
            ElMessage.warning('使用离线模式生成基础结构模板');
          } else {
            // 其他API错误
            ElMessage.error(`生成失败：${error.message}`);
          }
        }
        
      } catch (error) {
        console.error('\n=== 发生错误 ===');
        console.error('错误类型:', error.name);
        console.error('错误信息:', error.message);
        
        ElMessage.error(`生成失败：${error.message}`);
        
        // 确保结束流式状态
        isStreaming.value = false;
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
      
      // 从URL参数中获取并填充表单
      const params = new URLSearchParams(window.location.search);
      
      // 记录接收到的所有参数到控制台
      console.log('获取到URL参数:', Object.fromEntries(params.entries()));
      
      // 解析文档类型
      if (params.has('documentType')) {
        const docType = params.get('documentType');
        console.log('解析文档类型:', docType);
        // 查找匹配的文档类型选项
        const foundType = documentTypes.value.find(type => type.name === docType);
        if (foundType) {
          console.log('找到匹配的文档类型:', foundType.id);
          selectedType.value = foundType.id;
        }
      }
      
      // 解析文档用途
      if (params.has('documentUsage')) {
        const usage = params.get('documentUsage');
        console.log('解析文档用途:', usage);
        // 查找匹配的用途选项
        const foundPurpose = documentPurposes.value.find(purpose => purpose.name === usage);
        if (foundPurpose) {
          console.log('找到匹配的文档用途:', foundPurpose.id);
          selectedPurpose.value = foundPurpose.id;
        }
      }
      
      // 解析目标受众
      if (params.has('targetAudience')) {
        const audience = params.get('targetAudience');
        console.log('解析目标受众:', audience);
        // 查找匹配的受众选项
        const foundAudience = audienceOptions.value.find(option => option.name === audience);
        if (foundAudience) {
          console.log('找到匹配的目标受众:', foundAudience.id);
          selectedAudience.value = foundAudience.id;
        }
      }
      
      // 解析文档标题
      if (params.has('documentTitle')) {
        const title = params.get('documentTitle');
        console.log('解析文档标题:', title);
        topic.value = title;
      }
      
      // 解析文档目的
      if (params.has('documentPurpose')) {
        const purpose = params.get('documentPurpose');
        console.log('解析文档目的:', purpose);
        keyPoints.value = purpose;
      }
      
      // 解析文档包含元素
      if (params.has('includeElements')) {
        const elements = params.get('includeElements');
        console.log('解析文档包含元素:', elements);
        
        // 如果是none，所有元素设为false
        if (elements === 'none') {
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
        } else if (elements) {
          // 如果是逗号分隔的元素列表，分别设置
          const elementsList = elements.split(',');
          includeSummary.value = elementsList.includes('summary');
          includeTableOfContents.value = elementsList.includes('toc');
          includeIntroduction.value = elementsList.includes('intro');
          includeMethods.value = elementsList.includes('methods');
          includeBackground.value = elementsList.includes('background');
          includeCharts.value = elementsList.includes('charts');
          includeCaseStudies.value = elementsList.includes('cases');
          includeFindings.value = elementsList.includes('findings');
          includeImplementation.value = elementsList.includes('implementation');
          includeResources.value = elementsList.includes('resources');
          includeConclusion.value = elementsList.includes('conclusion');
          includeReferences.value = elementsList.includes('references');
          includeAppendix.value = elementsList.includes('appendix');
          includeFuturePlans.value = elementsList.includes('futurePlans');
        }
      }
      
      // 确保轮播引用已初始化
      nextTick(() => {
        if (exampleCarousel.value) {
          console.log('轮播容器已初始化:', exampleCarousel.value);
          // 重置轮播位置
          currentExampleIndex.value = 0;
          scrollCarousel();
        }
      });
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
    
    // 打印文档
    const printDocument = () => {
      // 创建一个新的打印窗口，只包含文档内容
      const printWindow = window.open('', '_blank');
      if (!printWindow) {
        toast.error('无法打开打印窗口，请检查浏览器的弹窗设置');
        return;
      }

      // 添加样式和内容
      printWindow.document.write(`
        <html>
          <head>
            <title>${topic.value || '文档结构'}</title>
            <style>
              @media print {
                body {
                  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
                  margin: 0;
                  padding: 20mm;
                }
                
                /* 复制所有word-相关的样式... */
                .word-heading-1 {
                  font-size: 24px;
                  font-weight: bold;
                  margin-top: 24px;
                  color: #2b579a;
                  border-bottom: 1px solid #e0e0e0;
                  padding-bottom: 8px;
                }
                
                .word-heading-2 {
                  font-size: 20px;
                  font-weight: bold;
                  margin-top: 20px;
                  color: #2b579a;
                }
                
                .word-heading-3 {
                  font-size: 16px;
                  font-weight: bold;
                  margin-top: 16px;
                }
                
                .word-paragraph {
                  font-size: 14px;
                  line-height: 1.5;
                  margin-bottom: 8px;
                  text-align: justify;
                }
                
                .word-list-item {
                  font-size: 14px;
                  line-height: 1.5;
                  margin-bottom: 6px;
                  padding-left: 24px;
                  position: relative;
                }
                
                /* 其他样式... */
              }
            </style>
          </head>
          <body>
            ${wordFormattedContent.value}
          </body>
        </html>
      `);
      
      printWindow.document.close();
      
      // 等待样式加载完成后打印
      setTimeout(() => {
        printWindow.print();
        printWindow.close();
      }, 500);
    };

    // 保存为PDF
    const saveAsPdf = () => {
      toast.info('准备将文档保存为PDF...');
      
      // 实际产品中，可以使用html2pdf.js或jspdf等库进行PDF转换
      // 这里简化为使用打印功能的"另存为PDF"选项
      printDocument();
      
      toast.success('请通过浏览器的打印功能选择"另存为PDF"选项');
    };

    // 格式应用函数（实际环境中这些按钮只是样式展示，并不会有实际功能）
    const applyFormat = (format) => {
      // 在实际的Word中，这些按钮会修改选中的文本样式
      // 这里只是模拟界面，不需要实际功能
      console.log(`应用${format}格式`);
    };

    // 对齐应用函数
    const applyAlign = (align) => {
      // 在实际的Word中，这些按钮会修改段落对齐方式
      // 这里只是模拟界面，不需要实际功能
      console.log(`应用${align}对齐`);
    };
    
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
      isStreaming,
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
      wordFormattedContent,
      
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
      
      // 打印和保存功能
      printDocument,
      saveAsPdf,
      applyFormat,
      applyAlign,
      
      // 添加文档结构知识内容
      documentStructureKnowledge,
      formatMarkdown,
    };
  }
};
</script>

<style>
/* 导入通用样式 */
@import '../../../assets/css/text-creation-common.css';

/* 特定于文档结构的样式 */
.document-structure-page {
  padding: 20px;
}

/* 文档包含元素 */
.document-elements {
  margin-bottom: 15px;
}

.document-elements h3 {
  font-size: 16px;
  color: #444;
  margin-bottom: 10px;
}

.elements-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
}

.element-checkbox {
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #eee;
}

.element-checkbox:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.element-checkbox input[type="checkbox"] {
  margin-right: 8px;
}

.element-checkbox span {
  font-size: 14px;
  color: #444;
}

.element-checkbox input[type="checkbox"]:checked + span {
  color: var(--primary-color, #ba003f);
  font-weight: 500;
}

/* 面板样式 */
.panel-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #f0f0f0;
}

.panel-section h3 {
  font-size: 16px;
  color: #444;
  margin-top: 0;
  margin-bottom: 15px;
}

/* 离线模式提示条 */
.offline-mode-banner {
  background-color: #fff8e1;
  color: #856404;
  padding: 10px 15px;
  margin-bottom: 15px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.offline-mode-banner i {
  font-size: 18px;
}

.article-result {
  padding: 15px;
  transition: all 0.3s ease;
}

.prompt-button {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #eee;
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
}

.prompt-button:hover {
  background-color: #e5e5e5;
}

.prompt-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

/* Word模拟样式 */
.word-document {
  background: #f5f5f5;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-width: 800px; /* 控制最大宽度 */
  margin: 0 auto; /* 居中显示 */
}

.word-toolbar {
  background-color: #2b579a; /* 恢复Word顶部的蓝色区域 */
  border-bottom: 1px solid #1e3f73;
  display: flex;
  padding: 8px;
  gap: 10px;
}

.toolbar-group {
  display: flex;
  gap: 4px;
  border-right: 1px solid rgba(255, 255, 255, 0.2); /* 调整分割线颜色 */
  padding-right: 10px;
  margin-right: 10px;
}

.toolbar-group:last-child {
  border-right: none;
}

.toolbar-btn {
  background: none;
  border: none;
  border-radius: 3px;
  color: white; /* 恢复白色按钮 */
  cursor: pointer;
  font-size: 16px;
  padding: 4px 6px;
}

.toolbar-btn:hover {
  background-color: rgba(255, 255, 255, 0.2); /* 恢复悬停效果 */
}

.word-page {
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin: 15px;
  min-height: auto; /* 由固定高度改为auto，适应内容高度 */
  padding: 40px 40px 60px; /* 修改下内边距为60px，为页脚留出空间 */
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  width: calc(100% - 30px); /* 考虑margin */
}

.word-content {
  overflow-y: auto; /* 保留垂直滚动 */
  flex: 1;
  margin-bottom: 30px; /* 为页脚预留空间，减少冗余高度 */
}

.word-footer {
  border-top: 1px solid #eee;
  color: #777;
  display: flex;
  font-size: 11px;
  justify-content: space-between;
  padding-top: 10px;
  position: relative; /* 改为相对定位，更好地跟随内容 */
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%; /* 确保宽度占满 */
}

.word-statusbar {
  background-color: #f0f0f0;
  border-top: 1px solid #ddd;
  color: #666;
  display: flex;
  font-size: 12px;
  padding: 4px 15px;
}

.word-statusbar-item {
  margin-right: 15px;
  display: flex;
  align-items: center;
}

.word-statusbar-item i {
  margin-right: 4px;
}

/* 修改流式输出样式 */
.streaming .streaming-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(186, 0, 63, 1); /* 移除透明度，使其完全不透明 */
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  color: white;
  font-size: 16px;
  font-weight: 500;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 12px 24px;
  z-index: 100;
}

.streaming .streaming-indicator i {
  margin-right: 10px;
  font-size: 20px;
}

/* 增强旋转动画效果 */
.spinning {
  animation: spin 1.2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 添加页脚和页码样式 */
.word-footer {
  position: absolute;
  bottom: 10px;
  width: 100%;
  max-width: 800px;
  display: flex;
  justify-content: space-between;
  padding: 0 60px;
  color: #777;
  font-size: 12px;
  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
}

.word-page-number {
  text-align: left;
}

.word-document-title {
  text-align: right;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

/* 添加Word状态栏样式 */
.word-statusbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  background-color: #f3f3f3;
  border-top: 1px solid #e0e0e0;
  padding: 4px 16px;
  gap: 24px;
  font-size: 12px;
  color: #666;
  height: 24px;
}

.word-statusbar-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.word-statusbar-item i {
  font-size: 14px;
  color: #2b579a;
}

/* 加载中的点动画 */
.loading-dots span {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #666;
  border-radius: 50%;
  margin: 0 2px;
  animation: dotPulse 1.4s infinite ease-in-out;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotPulse {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
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

/* 创作小贴士模态窗口 - 替换为el-drawer抽屉组件 */
.knowledge-drawer {
  width: 30%;
}

.knowledge-content {
  padding: 20px;
}

.knowledge-section {
  margin-bottom: 20px;
}

.knowledge-subtitle {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.knowledge-icon {
  margin-right: 10px;
}

.knowledge-text {
  font-size: 14px;
  line-height: 1.5;
}

/* 流式输出样式 */
.streaming .streaming-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(186, 0, 63, 1); /* 移除透明度，使其完全不透明 */
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  color: white;
  font-size: 16px;
  font-weight: 500;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 12px 24px;
  z-index: 100;
}

.streaming .streaming-indicator i {
  margin-right: 10px;
  font-size: 20px;
}

/* 增强旋转动画效果 */
.spinning {
  animation: spin 1.2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.streaming .word-content {
  position: relative;
}

.streaming .word-content::after {
  content: '|';
  display: inline-block;
  animation: blink 1s step-end infinite;
  color: var(--primary-color, #ba003f);
  font-weight: bold;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 确保轮播控制按钮可点击 */
.carousel-controls {
  display: flex;
  gap: 8px;
  position: relative;
  z-index: 10; /* 提高z-index确保控件在最上层 */
}

.carousel-control {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: white;
  border: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  z-index: 15; /* 确保按钮在最上层 */
  pointer-events: auto !important; /* 强制启用点击事件 */
}

.carousel-control i {
  font-size: 20px;
  color: #666;
  display: inline-block; /* 确保图标可见 */
  line-height: 1; /* 修正行高 */
  pointer-events: none; /* 防止图标干扰点击 */
}

.carousel-control:hover {
  background-color: rgba(186, 0, 63, 0.05);
  border-color: var(--primary-color, #ba003f);
}

.carousel-control:hover i {
  color: var(--primary-color, #ba003f);
}

.carousel-control.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none; /* 禁用点击 */
}
</style> 