<template>
  <div class="prompt-engineering-container">
    <el-tabs v-model="activeTab" type="border-card" class="prompt-tabs">
      <el-tab-pane name="basic">
        <template #label>
          <div class="custom-tab-label basic-tab">
            <i class="ri-text-spacing"></i>
            <span>基础提示语结构</span>
          </div>
        </template>
        <div class="formula-container">
          <h3 class="section-title">提示词公式：任务+背景+目标+负面</h3>
          <p class="formula">
            我要（做）<span class="highlight">***</span>，要给<span class="highlight">***</span>用，
            我希望达到<span class="highlight">***</span>效果，但是担心<span class="highlight">***</span>问题。
          </p>
          
          <div class="example-box">
            <h4>示例</h4>
            <p>我要做一个从北京到日本的旅游攻略，要给爸妈用，希望让他们在日本开心的玩20天，但我担心他们玩的累，腿和腰不太好。</p>
          </div>
        </div>
        
        <div class="workflow-container">
          <div class="header-with-button">
            <h3 class="section-title">编写你的提示词</h3>
            <el-button type="primary" plain size="small" @click="showExamplesDialog">
              <i class="ri-file-list-3-line"></i> 参考案例
            </el-button>
          </div>
          
          <div class="workflow-progress">
            <div class="progress-bar">
              <div class="progress-indicator" :style="{width: progressWidth}"></div>
            </div>
            <div class="progress-text">{{progressText}}</div>
          </div>
          
          <div class="workflow-steps">
            <div class="step-item" :class="{'active-step': isCurrentStep(1)}">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4 class="step-title">任务：我要（做）什么？</h4>
                <el-input 
                  v-model="promptForm.task" 
                  placeholder="例如：做一个从北京到日本的旅游攻略"
                  @input="updateProgress"
                  @focus="currentStep = 1"
                ></el-input>
                <div class="step-hint">描述你想完成的任务或创建的内容</div>
              </div>
            </div>
            
            <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>
            
            <div class="step-item" :class="{'active-step': isCurrentStep(2)}">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4 class="step-title">背景：要给谁用/背景描述</h4>
                <el-input 
                  v-model="promptForm.audience" 
                  placeholder="例如：爸妈"
                  @input="updateProgress"
                  @focus="currentStep = 2"
                ></el-input>
                <div class="step-hint">明确目标受众或使用者</div>
              </div>
            </div>
            
            <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>
            
            <div class="step-item" :class="{'active-step': isCurrentStep(3)}">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4 class="step-title">目标：希望达到什么效果？</h4>
                <el-input 
                  v-model="promptForm.goal" 
                  placeholder="例如：让他们在日本开心的玩20天"
                  @input="updateProgress"
                  @focus="currentStep = 3"
                ></el-input>
                <div class="step-hint">描述你期望的结果或成效</div>
              </div>
            </div>
            
            <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>
            
            <div class="step-item" :class="{'active-step': isCurrentStep(4)}">
              <div class="step-number">4</div>
              <div class="step-content">
                <h4 class="step-title">负面：担心什么问题？</h4>
                <el-input 
                  v-model="promptForm.concern" 
                  placeholder="例如：他们玩的累，腿和腰不太好"
                  @input="updateProgress"
                  @focus="currentStep = 4"
                ></el-input>
                <div class="step-hint">说明可能的限制条件或需要避免的情况</div>
              </div>
            </div>
            
            <div class="step-arrow final-arrow"><i class="ri-arrow-down-s-line"></i></div>
            
            <div class="result-step">
              <div class="result-header">
                <div class="result-icon"><i class="ri-check-line"></i></div>
                <h4 class="result-title">完整提示词</h4>
              </div>
              <el-card class="prompt-result" shadow="hover">
                <p>{{ generatedPrompt }}</p>
              </el-card>
            </div>
          </div>
        </div>
        
        <div class="action-container">
          <div class="action-buttons">
            <el-button type="primary" @click="getAIFeedback" :disabled="!isFormComplete" :loading="isLoading">获取AI建议</el-button>
            <el-button type="primary" @click="executePrompt" :disabled="!isFormComplete" :loading="isExecuting">执行提示词</el-button>
            <el-button @click="clearForm">清空</el-button>
          </div>
        </div>
        
        <div v-if="aiFeedback" class="feedback-container">
          <h3 class="section-title">AI建议</h3>
          <el-card class="ai-feedback" shadow="hover">
            <p v-html="formattedFeedback"></p>
          </el-card>
        </div>

        <div v-if="executionResult" class="execution-container">
          <h3 class="section-title">执行结果</h3>
          <el-card class="execution-result" shadow="hover">
            <p v-html="formattedExecutionResult"></p>
          </el-card>
        </div>
      </el-tab-pane>
      
      <el-tab-pane name="rtgo">
        <template #label>
          <div class="custom-tab-label rtgo-tab">
            <i class="ri-stack-line"></i>
            <span>RTGO提示语结构</span>
          </div>
        </template>
        <div class="prompt-container">
          <div class="prompt-formula-card">
            <div class="prompt-formula-title">提示词公式：角色（Role） + 任务（Task） + 目标（Goal） + 操作要求（Objective）</div>
            <div class="prompt-formula-description">
              <p><i class="ri-user-star-line formula-icon"></i> <strong>角色（Role）：</strong>指定AI应该扮演的角色或身份，如专家类型、经验水平、职业背景等。</p>
              <p><i class="ri-task-line formula-icon"></i> <strong>任务（Task）：</strong>明确告诉AI需要完成的具体任务，包括内容类型、主题范围、处理对象等。</p>
              <p><i class="ri-flag-line formula-icon"></i> <strong>目标（Goal）：</strong>指明完成任务后想要达到的效果或结果，如目标受众、预期影响、量化指标等。</p>
              <p><i class="ri-settings-line formula-icon"></i> <strong>操作要求（Objective）：</strong>提供具体的操作指南，如格式要求、长度限制、语气风格、结构安排等。</p>
            </div>
          </div>

          <div class="workflow-container">
            <div class="header-with-button">
              <h3 class="section-title">编写你的提示词</h3>
              <el-button type="primary" plain size="small" @click="showRtgoExamplesDialog">
                <i class="ri-file-list-3-line"></i> 参考案例
              </el-button>
            </div>
            
            <div class="workflow-progress">
              <div class="progress-bar">
                <div class="progress-indicator" :style="{width: rtgoProgressWidth}"></div>
              </div>
              <div class="progress-text">{{rtgoProgressText}}</div>
            </div>

            <div class="workflow-steps">
              <div class="step-item" :class="{'active-step': isCurrentRtgoStep(1)}">
                <div class="step-number">1</div>
                <div class="step-content">
                  <h4 class="step-title">角色（Role）</h4>
                  <el-input
                    v-model="rtgoForm.role"
                    type="textarea"
                    :rows="3"
                    placeholder="指定AI应扮演的角色或身份，如资深营销策略专家、拥有10年经验的UX设计师等"
                    @input="updateRtgoProgress"
                    @focus="currentRtgoStep = 1"
                  ></el-input>
                  <div class="step-hint">定义AI应当扮演的专业角色或身份</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentRtgoStep(2)}">
                <div class="step-number">2</div>
                <div class="step-content">
                  <h4 class="step-title">任务（Task）</h4>
                  <el-input
                    v-model="rtgoForm.task"
                    type="textarea"
                    :rows="3"
                    placeholder="描述需要完成的具体任务，如为新上市的智能手表写一篇博客文章、分析近6个月的用户数据并提供增长策略等"
                    @input="updateRtgoProgress"
                    @focus="currentRtgoStep = 2"
                  ></el-input>
                  <div class="step-hint">明确具体需要完成的任务内容</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentRtgoStep(3)}">
                <div class="step-number">3</div>
                <div class="step-content">
                  <h4 class="step-title">目标（Goal）</h4>
                  <el-input
                    v-model="rtgoForm.goal"
                    type="textarea"
                    :rows="3"
                    placeholder="明确希望达成的结果，如'提高目标用户的购买意愿'、'为管理层提供可执行的业务决策依据'等"
                    @input="updateRtgoProgress"
                    @focus="currentRtgoStep = 3"
                  ></el-input>
                  <div class="step-hint">说明期望通过任务达成的目标</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentRtgoStep(4)}">
                <div class="step-number">4</div>
                <div class="step-content">
                  <h4 class="step-title">操作要求（Objective）</h4>
                  <el-input
                    v-model="rtgoForm.objective"
                    type="textarea"
                    :rows="3"
                    placeholder="提供具体的格式或内容要求，如使用简洁明了的语言，不超过800字，包含3个实用建议，使用友好的语气等"
                    @input="updateRtgoProgress"
                    @focus="currentRtgoStep = 4"
                  ></el-input>
                  <div class="step-hint">明确格式、风格、字数等具体要求</div>
                </div>
              </div>
              
              <div class="step-arrow final-arrow"><i class="ri-arrow-down-s-line"></i></div>
              
              <div class="result-step">
                <div class="result-header">
                  <div class="result-icon"><i class="ri-check-line"></i></div>
                  <h4 class="result-title">完整提示词</h4>
                </div>
                <el-card class="prompt-result" shadow="hover">
                  <p>{{ generatedRtgoPrompt }}</p>
                </el-card>
              </div>
            </div>
          </div>
          
          <div class="action-container">
            <div class="action-buttons">
              <el-button type="primary" @click="getRtgoAIFeedback" :disabled="!isRtgoFormComplete" :loading="isRtgoLoading">获取AI建议</el-button>
              <el-button type="primary" @click="executeRtgoPrompt" :disabled="!isRtgoFormComplete" :loading="isRtgoExecuting">执行提示词</el-button>
              <el-button @click="clearRtgoForm">清空</el-button>
            </div>
          </div>

          <div v-if="rtgoAIFeedback" class="feedback-container">
            <h3 class="section-title">AI建议</h3>
            <el-card class="ai-feedback" shadow="hover">
              <p v-html="formattedRtgoFeedback"></p>
            </el-card>
          </div>

          <div v-if="rtgoExecutionResult" class="execution-container">
            <h3 class="section-title">执行结果</h3>
            <el-card class="execution-result" shadow="hover">
              <p v-html="formattedRtgoExecutionResult"></p>
            </el-card>
          </div>
        </div>
      </el-tab-pane>
      
      <el-tab-pane name="costar">
        <template #label>
          <div class="custom-tab-label costar-tab">
            <i class="ri-star-line"></i>
            <span>CO-STAR提示语框架</span>
          </div>
        </template>
        <div class="prompt-container">
          <div class="prompt-formula-card">
            <div class="prompt-formula-title">提示词公式：上下文（Context） + 目标（Objective） + 风格（Style） + 语调（Tone） + 受众（Audience） + 回应（Response）</div>
            <div class="prompt-formula-description">
              <p><i class="ri-file-info-line formula-icon"></i> <strong>上下文（Context）：</strong>相关的背景信息，比如你自己或是你希望它完成的任务信息。</p>
              <p><i class="ri-target-line formula-icon"></i> <strong>目标（Objective）：</strong>明确的指示告诉AI你希望它做什么。</p>
              <p><i class="ri-brush-line formula-icon"></i> <strong>风格（Style）：</strong>想要的写作风格，如严肃的、有趣的、创新性表达、学术性等。</p>
              <p><i class="ri-volume-up-line formula-icon"></i> <strong>语调（Tone）：</strong>幽默的？情绪化的？有威胁性的？</p>
              <p><i class="ri-user-3-line formula-icon"></i> <strong>受众（Audience）：</strong>小白用户？专业人群？未成年人群？女性人群？老年人群？</p>
              <p><i class="ri-mail-send-line formula-icon"></i> <strong>回应（Response）：</strong>一份详细的研究报告？一个表格？Markdown格式？</p>
            </div>
          </div>

          <div class="workflow-container">
            <div class="header-with-button">
              <h3 class="section-title">编写你的提示词</h3>
              <el-button type="primary" plain size="small" @click="showCostarExamplesDialog">
                <i class="ri-file-list-3-line"></i> 参考案例
              </el-button>
            </div>
            
            <div class="workflow-progress">
              <div class="progress-bar">
                <div class="progress-indicator" :style="{width: costarProgressWidth}"></div>
              </div>
              <div class="progress-text">{{costarProgressText}}</div>
            </div>

            <div class="workflow-steps">
              <div class="step-item" :class="{'active-step': isCurrentCostarStep(1)}">
                <div class="step-number">1</div>
                <div class="step-content">
                  <h4 class="step-title">上下文（Context）</h4>
                  <el-input
                    v-model="costarForm.context"
                    type="textarea"
                    :rows="3"
                    placeholder="提供相关的背景信息，如任务的来源、目的、限制条件等"
                    @input="updateCostarProgress"
                    @focus="currentCostarStep = 1"
                  ></el-input>
                  <div class="step-hint">提供AI需要了解的背景信息</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentCostarStep(2)}">
                <div class="step-number">2</div>
                <div class="step-content">
                  <h4 class="step-title">目标（Objective）</h4>
                  <el-input
                    v-model="costarForm.objective"
                    type="textarea"
                    :rows="3"
                    placeholder="明确告诉AI你希望它做什么，例如'编写一篇博客文章'、'分析这些销售数据'"
                    @input="updateCostarProgress"
                    @focus="currentCostarStep = 2"
                  ></el-input>
                  <div class="step-hint">指明具体的任务目标</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentCostarStep(3)}">
                <div class="step-number">3</div>
                <div class="step-content">
                  <h4 class="step-title">风格（Style）</h4>
                  <el-input
                    v-model="costarForm.style"
                    type="textarea"
                    :rows="3"
                    placeholder="指定写作风格，如'正式学术风格'、'通俗易懂的科普风格'、'创新性的表达方式'"
                    @input="updateCostarProgress"
                    @focus="currentCostarStep = 3"
                  ></el-input>
                  <div class="step-hint">指定内容的风格特点</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentCostarStep(4)}">
                <div class="step-number">4</div>
                <div class="step-content">
                  <h4 class="step-title">语调（Tone）</h4>
                  <el-input
                    v-model="costarForm.tone"
                    type="textarea"
                    :rows="3"
                    placeholder="指定表达的语气，如'幽默轻松的'、'严肃专业的'、'温暖鼓励的'"
                    @input="updateCostarProgress"
                    @focus="currentCostarStep = 4"
                  ></el-input>
                  <div class="step-hint">设定内容的情感语调</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentCostarStep(5)}">
                <div class="step-number">5</div>
                <div class="step-content">
                  <h4 class="step-title">受众（Audience）</h4>
                  <el-input
                    v-model="costarForm.audience"
                    type="textarea"
                    :rows="3"
                    placeholder="明确目标受众群体，如'技术小白用户'、'高级管理人员'、'18-25岁的年轻女性'"
                    @input="updateCostarProgress"
                    @focus="currentCostarStep = 5"
                  ></el-input>
                  <div class="step-hint">确定内容面向的人群</div>
                </div>
              </div>
              
              <div class="step-arrow"><i class="ri-arrow-down-s-line"></i></div>

              <div class="step-item" :class="{'active-step': isCurrentCostarStep(6)}">
                <div class="step-number">6</div>
                <div class="step-content">
                  <h4 class="step-title">回应（Response）</h4>
                  <el-input
                    v-model="costarForm.response"
                    type="textarea"
                    :rows="3"
                    placeholder="指定回答的格式，如'Markdown格式的报告'、'包含5个要点的列表'、'不超过500字的简洁总结'"
                    @input="updateCostarProgress"
                    @focus="currentCostarStep = 6"
                  ></el-input>
                  <div class="step-hint">规定输出的形式和格式</div>
                </div>
              </div>
              
              <div class="step-arrow final-arrow"><i class="ri-arrow-down-s-line"></i></div>
              
              <div class="result-step">
                <div class="result-header">
                  <div class="result-icon"><i class="ri-check-line"></i></div>
                  <h4 class="result-title">完整提示词</h4>
                </div>
                <el-card class="prompt-result" shadow="hover">
                  <p>{{ generatedCostarPrompt }}</p>
                </el-card>
              </div>
            </div>
          </div>
          
          <div class="action-container">
            <div class="action-buttons">
              <el-button type="primary" @click="getCostarAIFeedback" :disabled="!isCostarFormComplete" :loading="isCostarLoading">获取AI建议</el-button>
              <el-button type="primary" @click="executeCostarPrompt" :disabled="!isCostarFormComplete" :loading="isCostarExecuting">执行提示词</el-button>
              <el-button @click="clearCostarForm">清空</el-button>
            </div>
          </div>

          <div v-if="costarAIFeedback" class="feedback-container">
            <h3 class="section-title">AI建议</h3>
            <el-card class="ai-feedback" shadow="hover">
              <p v-html="formattedCostarFeedback"></p>
            </el-card>
          </div>

          <div v-if="costarExecutionResult" class="execution-container">
            <h3 class="section-title">执行结果</h3>
            <el-card class="execution-result" shadow="hover">
              <p v-html="formattedCostarExecutionResult"></p>
            </el-card>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 参考案例弹窗 -->
    <el-dialog
      title="参考案例"
      v-model="dialogVisible"
      width="70%"
      destroy-on-close
      class="prompt-examples-dialog"
    >
      <div class="examples-container">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" v-for="(example, index) in promptExamples" :key="index">
            <el-card class="example-card" @click="applyExample(example)">
              <div class="example-header">
                <i :class="example.icon"></i>
                <div class="example-title">{{ example.title }}</div>
              </div>
              <div class="example-desc">{{ example.description }}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-dialog>

    <!-- 添加RTGO参考案例对话框 -->
    <el-dialog
      v-model="rtgoDialogVisible"
      title="RTGO提示语参考案例"
      width="80%"
      class="prompt-examples-dialog"
    >
      <div class="examples-container">
        <div
          v-for="(example, index) in rtgoPromptExamples"
          :key="index"
          class="example-card"
          @click="applyRtgoExample(example)"
        >
          <div class="example-header">
            <i :class="example.icon"></i>
            <span class="example-title">{{ example.title }}</span>
          </div>
          <div class="example-description">{{ example.description }}</div>
        </div>
      </div>
    </el-dialog>

    <!-- 添加CO-STAR参考案例对话框 -->
    <el-dialog
      v-model="costarDialogVisible"
      title="CO-STAR提示语参考案例"
      width="80%"
      class="prompt-examples-dialog"
    >
      <div class="examples-container">
        <div
          v-for="(example, index) in costarPromptExamples"
          :key="index"
          class="example-card"
          @click="applyCostarExample(example)"
        >
          <div class="example-header">
            <i :class="example.icon"></i>
            <span class="example-title">{{ example.title }}</span>
          </div>
          <div class="example-description">{{ example.description }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import 'remixicon/fonts/remixicon.css';

export default {
  name: 'PromptEngineering',
  data() {
    return {
      activeTab: 'basic',
      promptForm: {
        task: '',
        audience: '',
        goal: '',
        concern: ''
      },
      // RTGO表单数据
      rtgoForm: {
        role: '',
        task: '',
        goal: '',
        objective: ''
      },
      // CO-STAR表单数据
      costarForm: {
        context: '',
        objective: '',
        style: '',
        tone: '',
        audience: '',
        response: ''
      },
      aiFeedback: '',
      executionResult: '',
      rtgoAIFeedback: '',
      rtgoExecutionResult: '',
      costarAIFeedback: '',
      costarExecutionResult: '',
      isLoading: false,
      isExecuting: false,
      isRtgoLoading: false,
      isRtgoExecuting: false,
      isCostarLoading: false,
      isCostarExecuting: false,
      currentStep: 1,
      currentRtgoStep: 1,
      currentCostarStep: 1,
      modelOptions: [
        { label: 'DeepSeek R1-64K (硅基流动)', value: 'deepseek-r1-sf' },
        { label: 'DeepSeek V3-64K (硅基流动)', value: 'deepseek-v3-sf' },
        { label: 'DeepSeek R1-64K (火山引擎)', value: 'deepseek-r1-vol' },
        { label: 'DeepSeek V3-64K (火山引擎)', value: 'deepseek-v3-vol' },
        { label: '通义千问-32B (硅基流动)', value: 'qwq-32b' },
        { label: '豆包-Pro (火山引擎)', value: 'doubao-pro' },
        { label: '通义千问-Max (阿里云)', value: 'qwen-max' }
      ],
      selectedModel: 'deepseek-v3-vol',
      dialogVisible: false,
      rtgoDialogVisible: false,
      costarDialogVisible: false,
      promptExamples: [
        {
          title: "旅游攻略",
          description: "制作适合老年人的日本旅游攻略",
          task: "做一个从北京到日本的旅游攻略",
          audience: "爸妈",
          goal: "让他们在日本开心的玩20天",
          concern: "他们玩的累，腿和腰不太好",
          icon: "ri-map-pin-line"
        },
        {
          title: "学习计划",
          description: "为小学生制定高效学习计划",
          task: "制定一个小学五年级数学学习计划",
          audience: "注意力不集中的小学生",
          goal: "在三个月内提高数学成绩",
          concern: "孩子容易对枯燥的内容失去兴趣",
          icon: "ri-book-open-line"
        },
        {
          title: "健身计划",
          description: "为办公室工作者定制健身计划",
          task: "设计一套居家健身计划",
          audience: "长期久坐的上班族",
          goal: "改善体态，增强体质",
          concern: "没有健身器材，时间有限",
          icon: "ri-heart-pulse-line"
        },
        {
          title: "演讲稿",
          description: "撰写技术产品发布会演讲稿",
          task: "写一份新产品发布会的演讲稿",
          audience: "技术行业的投资者和媒体",
          goal: "展示产品创新点并吸引投资",
          concern: "听众对技术细节的理解有限",
          icon: "ri-mic-line"
        },
        {
          title: "食谱规划",
          description: "为糖尿病患者设计食谱",
          task: "设计一周的健康饮食食谱",
          audience: "糖尿病患者",
          goal: "控制血糖同时保证营养均衡",
          concern: "食材选择有限，口味不能太单调",
          icon: "ri-restaurant-line"
        },
        {
          title: "商业计划书",
          description: "编写创业项目商业计划书",
          task: "撰写一份人工智能创业项目的商业计划书",
          audience: "风险投资人",
          goal: "获得种子轮融资",
          concern: "市场竞争激烈，差异化不够明显",
          icon: "ri-briefcase-line"
        },
        {
          title: "育儿建议",
          description: "为新手父母提供育儿建议",
          task: "整理0-1岁婴儿科学喂养指南",
          audience: "第一次当父母的年轻夫妇",
          goal: "帮助他们科学喂养宝宝",
          concern: "他们工作忙，时间精力有限",
          icon: "ri-parent-line"
        },
        {
          title: "网站内容",
          description: "创建企业网站的核心内容",
          task: "为一家科技公司设计网站首页内容",
          audience: "潜在客户和合作伙伴",
          goal: "展示公司实力并促成合作",
          concern: "内容过于技术化会降低用户体验",
          icon: "ri-global-line"
        },
        {
          title: "教学课件",
          description: "设计高中物理教学课件",
          task: "制作高中物理力学单元的教学课件",
          audience: "对物理不感兴趣的高中生",
          goal: "通过生动的例子让学生理解物理概念",
          concern: "学生基础参差不齐，注意力容易分散",
          icon: "ri-presentation-line"
        },
        {
          title: "社交媒体策略",
          description: "规划品牌社交媒体营销策略",
          task: "设计化妆品品牌的社交媒体营销策略",
          audience: "18-25岁年轻女性",
          goal: "提高品牌知名度和产品销量",
          concern: "预算有限，市场竞争激烈",
          icon: "ri-share-line"
        }
      ],
      // RTGO参考案例
      rtgoPromptExamples: [
        {
          title: "小红书营销文案",
          description: "撰写吸引年轻消费群体的小红书营销文案",
          role: "一位拥有5年小红书内容运营经验的资深营销专家",
          task: "为一款新上市的保湿补水面膜写一篇小红书推广文案",
          goal: "吸引25-35岁的年轻女性消费者，提高产品试用率",
          objective: "800字以内，包含3-5张示意图位置标注，使用轻松有趣的语气，包含产品使用体验和效果对比",
          icon: "ri-shopping-bag-line"
        },
        {
          title: "数据分析报告",
          description: "分析电商平台销售数据并提供优化建议",
          role: "具有10年电商行业经验的高级数据分析师",
          task: "分析过去6个月电商平台的销售数据并提供增长策略",
          goal: "找出销售瓶颈并提出可行的提升销量30%的方案",
          objective: "包含数据可视化图表说明，分析至少5个关键指标，提供3-5个具体可执行的优化建议",
          icon: "ri-line-chart-line"
        },
        {
          title: "产品培训教程",
          description: "为新员工创建产品功能培训内容",
          role: "拥有丰富培训经验的产品经理",
          task: "创建新版CRM系统的功能培训教程",
          goal: "帮助新员工在1周内掌握系统基本操作",
          objective: "分步骤讲解，包含截图示例，使用简单易懂的语言，添加常见问题解答环节",
          icon: "ri-questionnaire-line"
        },
        {
          title: "创业商业计划",
          description: "撰写AI创业项目商业计划书",
          role: "连续创业者和风投顾问",
          task: "为AI驱动的健康管理App撰写商业计划书",
          goal: "吸引种子轮投资者，获得至少100万美元融资",
          objective: "包括市场分析、竞争优势、商业模式、营收预测和团队介绍，必须有数据支持，长度控制在15页以内",
          icon: "ri-funds-line"
        },
        {
          title: "SEO文章撰写",
          description: "创建针对特定关键词优化的SEO内容",
          role: "拥有8年经验的SEO内容策略专家",
          task: "撰写一篇关于'智能家居与能源节约'的SEO优化文章",
          goal: "提高网站在相关搜索词的排名，增加有机流量",
          objective: "至少1500字，H1/H2/H3标题结构清晰，关键词密度3-5%，包含2-3个外部权威引用链接",
          icon: "ri-search-line"
        },
        {
          title: "视频脚本创作",
          description: "为教育类YouTube频道创作视频脚本",
          role: "经验丰富的教育内容创作者",
          task: "创作一个关于'人工智能基础知识'的10分钟视频脚本",
          goal: "以通俗易懂的方式向初学者解释AI概念",
          objective: "包含开场白、正文和结尾，标注视觉效果提示，使用对话式语言，添加3-4个互动问题环节",
          icon: "ri-video-line"
        },
        {
          title: "社交媒体运营计划",
          description: "制定品牌社交媒体月度运营计划",
          role: "社交媒体运营总监",
          task: "为一家科技创新公司制定下个月的社交媒体内容计划",
          goal: "提高品牌知名度，增加粉丝互动率和关注量",
          objective: "包含每周主题，每日内容类型，最佳发布时间，互动话题建议，以表格形式呈现，附带3个创意活动方案",
          icon: "ri-facebook-circle-line"
        },
        {
          title: "产品说明文档",
          description: "编写技术产品的用户说明文档",
          role: "技术文档专家",
          task: "为智能家居控制系统编写用户说明文档",
          goal: "帮助非技术背景用户轻松上手使用产品",
          objective: "使用简单直观的语言，包含详细的步骤说明和故障排除指南，添加图示标记，分章节组织内容",
          icon: "ri-file-list-3-line"
        },
        {
          title: "活动策划方案",
          description: "策划公司年度客户答谢活动",
          role: "拥有10年经验的高级活动策划师",
          task: "设计科技公司的年度VIP客户答谢活动方案",
          goal: "增强客户黏性，促进合作伙伴关系升级",
          objective: "包含活动主题、流程安排、预算分配、场地布置和宣传方案，注重创新体验和品牌展示",
          icon: "ri-calendar-event-line"
        },
        {
          title: "市场调研报告",
          description: "分析特定行业市场趋势和机会",
          role: "资深市场研究分析师",
          task: "分析中国智能家居市场的现状和未来5年发展趋势",
          goal: "为企业提供市场进入或扩张的决策依据",
          objective: "包含市场规模、主要竞争者分析、消费者需求分析、技术发展趋势和投资机会评估，需要有数据支持和图表展示",
          icon: "ri-bar-chart-box-line"
        }
      ],
      // CO-STAR参考案例
      costarPromptExamples: [
        {
          title: "社交媒体营销",
          description: "为产品创建吸引年轻用户的社交媒体营销方案",
          context: "我们是一家推出新款智能手表的科技公司，产品具有健康监测和运动追踪功能",
          objective: "创建一套为期一个月的社交媒体营销方案，包括内容主题和发布时间表",
          style: "创新且具有视觉吸引力的内容，强调产品的科技感和生活方式属性",
          tone: "充满活力、鼓舞人心，偶尔使用幽默元素",
          audience: "18-35岁注重健康和科技的年轻专业人士",
          response: "一份分周的营销计划，包含具体的内容创意、发布平台和最佳发布时间",
          icon: "ri-instagram-line"
        },
        {
          title: "技术博客",
          description: "撰写关于新兴技术的深度技术博客",
          context: "我是一家技术公司的内容营销经理，需要为公司博客增加高质量的技术内容",
          objective: "撰写一篇关于人工智能在客户服务中应用的深度技术博客文章",
          style: "专业且信息丰富，包含实际案例和数据支持",
          tone: "权威和教育性，保持客观中立",
          audience: "技术决策者和企业IT部门的专业人士",
          response: "一篇2000字的博客文章，包含小标题、图表位置标注和参考资料列表",
          icon: "ri-article-line"
        },
        {
          title: "产品说明书",
          description: "为智能家居设备创建用户友好的产品说明书",
          context: "我们刚发布了一款智能家居中枢，可以控制家中的照明、温度和安全系统",
          objective: "创建一份详细但易于理解的产品用户手册",
          style: "简洁、直观，避免过多的技术术语",
          tone: "友好和支持性，像在帮助朋友设置设备一样",
          audience: "非技术背景的普通家庭用户，包括老年人",
          response: "分章节的用户手册，包含图解步骤、常见问题解答和故障排除指南",
          icon: "ri-file-list-3-line"
        },
        {
          title: "市场分析报告",
          description: "分析电子商务行业的最新趋势和机会",
          context: "我是一家创业投资公司的分析师，负责评估电子商务领域的投资机会",
          objective: "分析中国电子商务市场的当前状况和未来3年的发展趋势",
          style: "数据驱动且分析性强，重视洞察而非仅仅描述现象",
          tone: "专业、冷静，保持客观分析",
          audience: "投资决策者和高级商业分析师",
          response: "一份结构化的市场分析报告，包含执行摘要、数据图表、主要发现和投资建议",
          icon: "ri-line-chart-line"
        },
        {
          title: "教育课程",
          description: "设计中学生科学实验教案",
          context: "我是一名中学科学教师，需要为9年级学生准备有趣且有教育意义的实验课",
          objective: "设计一套关于可再生能源的动手实验课程，展示太阳能、风能和水能的原理",
          style: "互动性强，结合理论和实践",
          tone: "充满热情和好奇心，鼓励探索",
          audience: "14-15岁的中学生，有不同学习能力和兴趣水平",
          response: "一个包含5个实验的教案，每个实验包括目标、材料清单、步骤说明和讨论问题",
          icon: "ri-flask-line"
        },
        {
          title: "招聘广告",
          description: "创建吸引顶尖人才的职位描述",
          context: "我们是一家快速发展的金融科技公司，需要招聘高级数据科学家",
          objective: "撰写一则吸引顶尖数据科学人才的职位描述和招聘广告",
          style: "专业但不乏味，强调公司创新文化和成长机会",
          tone: "热情但不夸张，表达对卓越的追求",
          audience: "有3-5年经验的数据科学专业人士，对金融科技领域有兴趣",
          response: "一份完整的职位描述，包含职责、要求、公司福利和应聘流程",
          icon: "ri-user-search-line"
        },
        {
          title: "产品评测",
          description: "撰写公正客观的电子产品评测",
          context: "我是一个科技评测网站的内容创作者，刚收到最新旗舰智能手机样机",
          objective: "创作一篇详细评测文章，涵盖产品性能、设计、相机质量和电池续航",
          style: "详尽且基于事实，包含实际测试数据和对比分析",
          tone: "客观公正，既指出优点也不回避缺点",
          audience: "对科技产品有兴趣的普通消费者和科技爱好者",
          response: "一篇分章节的评测文章，带有评分系统、优缺点总结和适用人群建议",
          icon: "ri-smartphone-line"
        },
        {
          title: "健康饮食计划",
          description: "为特定健康需求创建营养饮食计划",
          context: "我是一名营养顾问，客户是一位想要减轻体重同时维持能量的上班族",
          objective: "设计一个为期两周的健康饮食计划，侧重于平衡营养和体重管理",
          style: "实用且易于遵循，避免过于复杂的饮食要求",
          tone: "支持和鼓励，不带评判色彩",
          audience: "30-40岁的忙碌职场人士，烹饪技能有限，时间紧张",
          response: "每日三餐加零食的详细饮食计划，包含食谱、购物清单和简单的准备指南",
          icon: "ri-restaurant-line"
        },
        {
          title: "旅游攻略",
          description: "为家庭旅行者创建城市旅游攻略",
          context: "我计划带着父母和两个孩子（8岁和12岁）去北京旅游一周",
          objective: "创建一份适合全家的北京七天旅游攻略，覆盖景点、住宿和餐饮推荐",
          style: "实用信息与趣味知识相结合，注重家庭友好型体验",
          tone: "轻松愉快，充满期待和冒险精神",
          audience: "带着不同年龄段家人出行的旅行者，关注安全、便利和趣味性",
          response: "一份按天排列的行程计划，包含每日景点建议、交通信息、餐厅推荐和实用贴士",
          icon: "ri-map-pin-line"
        },
        {
          title: "销售培训材料",
          description: "设计销售团队提升转化率的培训计划",
          context: "我是销售主管，团队销售数据良好但转化率低于行业平均水平",
          objective: "创建一个销售培训计划，重点提高团队的成交技巧和异议处理能力",
          style: "实用性强，包含具体场景和解决方案",
          tone: "积极向上，有挑战性但不施加压力",
          audience: "经验各异的销售团队成员，年龄在22-45岁之间",
          response: "一份包含3天培训安排的完整计划，包括教学内容、互动练习和评估方法",
          icon: "ri-presentation-line"
        }
      ]
    };
  },
  computed: {
    generatedPrompt() {
      if (!this.promptForm.task && !this.promptForm.audience && !this.promptForm.goal && !this.promptForm.concern) {
        return '完整提示词将在这里显示...';
      }
      
      return `我要做${this.promptForm.task || '___'}，要给${this.promptForm.audience || '___'}用，`
        + `我希望达到${this.promptForm.goal || '___'}效果，但是担心${this.promptForm.concern || '___'}问题。`;
    },
    isFormComplete() {
      return this.promptForm.task && this.promptForm.audience && this.promptForm.goal && this.promptForm.concern;
    },
    formattedFeedback() {
      if (!this.aiFeedback) return '';
      
      // 将文本中的换行符转换为HTML的<br>标签
      return this.aiFeedback.replace(/\n/g, '<br>');
    },
    formattedExecutionResult() {
      if (!this.executionResult) return '';
      
      // 将文本中的换行符转换为HTML的<br>标签
      return this.executionResult.replace(/\n/g, '<br>');
    },
    progressWidth() {
      const filledFields = [
        this.promptForm.task,
        this.promptForm.audience,
        this.promptForm.goal,
        this.promptForm.concern
      ].filter(Boolean).length;
      
      return `${filledFields * 25}%`;
    },
    progressText() {
      const filledFields = [
        this.promptForm.task,
        this.promptForm.audience,
        this.promptForm.goal,
        this.promptForm.concern
      ].filter(Boolean).length;
      
      if (filledFields === 0) return '开始填写';
      if (filledFields === 4) return '完成！';
      return `已完成 ${filledFields}/4`;
    },
    // RTGO提示词相关计算属性
    generatedRtgoPrompt() {
      if (!this.rtgoForm.role && !this.rtgoForm.task && !this.rtgoForm.goal && !this.rtgoForm.objective) {
        return '完整提示词将在这里显示...';
      }
      
      return '角色（Role）：' + (this.rtgoForm.role || '___') + '\n\n'
        + '任务（Task）：' + (this.rtgoForm.task || '___') + '\n\n'
        + '目标（Goal）：' + (this.rtgoForm.goal || '___') + '\n\n'
        + '操作要求（Objective）：' + (this.rtgoForm.objective || '___');
    },
    isRtgoFormComplete() {
      return this.rtgoForm.role && this.rtgoForm.task && this.rtgoForm.goal && this.rtgoForm.objective;
    },
    formattedRtgoFeedback() {
      if (!this.rtgoAIFeedback) return '';
      
      // 将文本中的换行符转换为HTML的<br>标签
      return this.rtgoAIFeedback.replace(/\n/g, '<br>');
    },
    formattedRtgoExecutionResult() {
      if (!this.rtgoExecutionResult) return '';
      
      // 将文本中的换行符转换为HTML的<br>标签
      return this.rtgoExecutionResult.replace(/\n/g, '<br>');
    },
    rtgoProgressWidth() {
      const filledFields = [
        this.rtgoForm.role,
        this.rtgoForm.task,
        this.rtgoForm.goal,
        this.rtgoForm.objective
      ].filter(Boolean).length;
      
      return `${filledFields * 25}%`;
    },
    rtgoProgressText() {
      const filledFields = [
        this.rtgoForm.role,
        this.rtgoForm.task,
        this.rtgoForm.goal,
        this.rtgoForm.objective
      ].filter(Boolean).length;
      
      if (filledFields === 0) return '开始填写';
      if (filledFields === 4) return '完成！';
      return `已完成 ${filledFields}/4`;
    },
    // CO-STAR提示词相关计算属性
    generatedCostarPrompt() {
      if (!this.costarForm.context && !this.costarForm.objective && !this.costarForm.style && 
          !this.costarForm.tone && !this.costarForm.audience && !this.costarForm.response) {
        return '完整提示词将在这里显示...';
      }
      
      return '上下文（Context）：' + (this.costarForm.context || '___') + '\n\n'
        + '目标（Objective）：' + (this.costarForm.objective || '___') + '\n\n'
        + '风格（Style）：' + (this.costarForm.style || '___') + '\n\n'
        + '语调（Tone）：' + (this.costarForm.tone || '___') + '\n\n'
        + '受众（Audience）：' + (this.costarForm.audience || '___') + '\n\n'
        + '回应（Response）：' + (this.costarForm.response || '___');
    },
    isCostarFormComplete() {
      return this.costarForm.context && this.costarForm.objective && this.costarForm.style && 
             this.costarForm.tone && this.costarForm.audience && this.costarForm.response;
    },
    formattedCostarFeedback() {
      if (!this.costarAIFeedback) return '';
      
      // 将文本中的换行符转换为HTML的<br>标签
      return this.costarAIFeedback.replace(/\n/g, '<br>');
    },
    formattedCostarExecutionResult() {
      if (!this.costarExecutionResult) return '';
      
      // 将文本中的换行符转换为HTML的<br>标签
      return this.costarExecutionResult.replace(/\n/g, '<br>');
    },
    costarProgressWidth() {
      const filledFields = [
        this.costarForm.context,
        this.costarForm.objective,
        this.costarForm.style,
        this.costarForm.tone,
        this.costarForm.audience,
        this.costarForm.response
      ].filter(Boolean).length;
      
      return `${filledFields * 100 / 6}%`;
    },
    costarProgressText() {
      const filledFields = [
        this.costarForm.context,
        this.costarForm.objective,
        this.costarForm.style,
        this.costarForm.tone,
        this.costarForm.audience,
        this.costarForm.response
      ].filter(Boolean).length;
      
      if (filledFields === 0) return '开始填写';
      if (filledFields === 6) return '完成！';
      return `已完成 ${filledFields}/6`;
    }
  },
  methods: {
    isCurrentStep(step) {
      return this.currentStep === step;
    },
    updateProgress() {
      // 根据填写情况自动更新当前步骤
      if (!this.promptForm.task) {
        this.currentStep = 1;
      } else if (!this.promptForm.audience) {
        this.currentStep = 2;
      } else if (!this.promptForm.goal) {
        this.currentStep = 3;
      } else if (!this.promptForm.concern) {
        this.currentStep = 4;
      }
    },
    showExamplesDialog() {
      this.dialogVisible = true;
    },
    applyExample(example) {
      this.promptForm.task = example.task;
      this.promptForm.audience = example.audience;
      this.promptForm.goal = example.goal;
      this.promptForm.concern = example.concern;
      this.dialogVisible = false;
      this.currentStep = 4; // 设置为最后一步，显示完整提示词
      ElMessage({
        message: '已应用参考案例',
        type: 'success'
      });
    },
    async getAIFeedback() {
      if (!this.isFormComplete) return;
      
      this.isLoading = true;
      
      try {
        // 构建向大模型发送的消息
        const userPrompt = this.generatedPrompt;
        
        // 系统提示词，指导大模型如何优化用户的提示词
        const systemPrompt = `你是一位专业的提示词工程师，你需要帮助用户优化他们的提示词，使其能够获得更好的AI回复效果。
请分析用户的提示词，然后提供具体的优化建议，包括：
1. 提示词的优点：分析现有提示词的哪些部分是清晰有效的
2. 可以改进的地方：指出模糊或缺少关键信息的部分
3. 优化后的提示词：给出一个更加完善、结构化的提示词版本
4. 建议：额外的提示词工程技巧或建议

请确保你的回复清晰、有条理，并且以优化后的提示词为重点。回复格式如下：

## 原始提示词分析
[分析用户原始提示词的优点和不足]

## 优化建议
[列出2-4点具体优化建议]

## 优化后的提示词
[提供优化后的完整提示词]

## 提示词工程小技巧
[1-2条相关的提示词工程技巧]`;

        console.log("发送请求到后端API...", this.selectedModel);
        // 不使用任何默认baseURL，直接发送到完整URL
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', {
          model: this.selectedModel,
          messages: [
            {
              role: 'system',
              content: systemPrompt
            },
            {
              role: 'user',
              content: userPrompt
            }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        
        console.log("收到API响应:", response.data);
        
        if (response.data.status === 'success' && response.data.data && 
            response.data.data.choices && response.data.data.choices.length > 0) {
          // 从API响应中提取AI的回复内容
          this.aiFeedback = response.data.data.choices[0].message.content;
          console.log("AI回复成功解析");
        } else {
          // 如果响应格式不符合预期，记录详细信息并抛出错误
          console.error("API响应格式不正确:", JSON.stringify(response.data));
          throw new Error('API响应格式不正确: ' + JSON.stringify(response.data, null, 2));
        }
      } catch (error) {
        console.error('获取AI建议错误:', error);
        ElMessage.error(`获取AI建议出错: ${error.message || '未知错误'}`);
        
        // 出错后显示错误提示
        this.aiFeedback = `## 抱歉，无法获取AI反馈
        
连接后端服务出现问题。错误信息：${error.message || '未知错误'}

请稍后再试，或联系系统管理员。`;
      } finally {
        this.isLoading = false;
      }
    },
    async executePrompt() {
      if (!this.isFormComplete) return;
      
      this.isExecuting = true;
      
      try {
        // 直接使用用户的提示词作为输入
        const userPrompt = this.generatedPrompt;
        
        console.log("执行提示词，发送请求到后端API...", this.selectedModel);
        
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', {
          model: this.selectedModel,
          messages: [
            {
              role: 'user',
              content: userPrompt
            }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        
        console.log("收到执行结果:", response.data);
        
        if (response.data.status === 'success' && response.data.data && 
            response.data.data.choices && response.data.data.choices.length > 0) {
          // 从API响应中提取AI的回复内容
          this.executionResult = response.data.data.choices[0].message.content;
          console.log("执行结果成功解析");
        } else {
          // 如果响应格式不符合预期，记录详细信息并抛出错误
          console.error("API响应格式不正确:", JSON.stringify(response.data));
          throw new Error('API响应格式不正确: ' + JSON.stringify(response.data, null, 2));
        }
      } catch (error) {
        console.error('执行提示词出错:', error);
        ElMessage.error(`执行提示词出错: ${error.message || '未知错误'}`);
        
        // 显示错误信息
        this.executionResult = `## 抱歉，执行提示词失败
        
连接后端服务出现问题。错误信息：${error.message || '未知错误'}

请稍后再试，或联系系统管理员。`;
      } finally {
        this.isExecuting = false;
      }
    },
    clearForm() {
      this.promptForm = {
        task: '',
        audience: '',
        goal: '',
        concern: ''
      };
      this.aiFeedback = '';
      this.executionResult = '';
      this.currentStep = 1;
    },
    // RTGO提示词相关方法
    isCurrentRtgoStep(step) {
      return this.currentRtgoStep === step;
    },
    updateRtgoProgress() {
      // 根据填写情况自动更新当前步骤
      if (!this.rtgoForm.role) {
        this.currentRtgoStep = 1;
      } else if (!this.rtgoForm.task) {
        this.currentRtgoStep = 2;
      } else if (!this.rtgoForm.goal) {
        this.currentRtgoStep = 3;
      } else if (!this.rtgoForm.objective) {
        this.currentRtgoStep = 4;
      }
    },
    showRtgoExamplesDialog() {
      this.rtgoDialogVisible = true;
    },
    applyRtgoExample(example) {
      this.rtgoForm.role = example.role;
      this.rtgoForm.task = example.task;
      this.rtgoForm.goal = example.goal;
      this.rtgoForm.objective = example.objective;
      this.rtgoDialogVisible = false;
      this.currentRtgoStep = 4; // 设置为最后一步，显示完整提示词
      ElMessage({
        message: '已应用参考案例',
        type: 'success'
      });
    },
    async getRtgoAIFeedback() {
      if (!this.isRtgoFormComplete) return;
      
      this.isRtgoLoading = true;
      
      try {
        // 构建向大模型发送的消息
        const userPrompt = this.generatedRtgoPrompt;
        
        // 系统提示词，指导大模型如何优化用户的提示词
        const systemPrompt = `你是一位专业的提示词工程师，你需要帮助用户优化他们的RTGO结构提示词，使其能够获得更好的AI回复效果。
请分析用户的提示词，然后提供具体的优化建议，包括：
1. 提示词的优点：分析现有提示词的哪些部分是清晰有效的
2. 可以改进的地方：指出模糊或缺少关键信息的部分
3. 优化后的提示词：给出一个更加完善、结构化的提示词版本
4. 建议：额外的提示词工程技巧或建议

请确保你的回复清晰、有条理，并且以优化后的提示词为重点。回复格式如下：

## 原始提示词分析
[分析用户原始提示词的优点和不足]

## 优化建议
[列出2-4点具体优化建议]

## 优化后的提示词
[提供优化后的完整提示词]

## 提示词工程小技巧
[1-2条相关的提示词工程技巧]`;

        console.log("发送RTGO请求到后端API...", this.selectedModel);
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', {
          model: this.selectedModel,
          messages: [
            {
              role: 'system',
              content: systemPrompt
            },
            {
              role: 'user',
              content: userPrompt
            }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        
        console.log("收到RTGO API响应:", response.data);
        
        if (response.data.status === 'success' && response.data.data && 
            response.data.data.choices && response.data.data.choices.length > 0) {
          // 从API响应中提取AI的回复内容
          this.rtgoAIFeedback = response.data.data.choices[0].message.content;
          console.log("RTGO AI回复成功解析");
        } else {
          // 如果响应格式不符合预期，记录详细信息并抛出错误
          console.error("API响应格式不正确:", JSON.stringify(response.data));
          throw new Error('API响应格式不正确: ' + JSON.stringify(response.data, null, 2));
        }
      } catch (error) {
        console.error('获取RTGO AI建议错误:', error);
        ElMessage.error(`获取AI建议出错: ${error.message || '未知错误'}`);
        
        // 出错后显示错误提示
        this.rtgoAIFeedback = `## 抱歉，无法获取AI反馈
        
连接后端服务出现问题。错误信息：${error.message || '未知错误'}

请稍后再试，或联系系统管理员。`;
      } finally {
        this.isRtgoLoading = false;
      }
    },
    async executeRtgoPrompt() {
      if (!this.isRtgoFormComplete) return;
      
      this.isRtgoExecuting = true;
      
      try {
        // 直接使用用户的提示词作为输入
        const userPrompt = this.generatedRtgoPrompt;
        
        console.log("执行RTGO提示词，发送请求到后端API...", this.selectedModel);
        
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', {
          model: this.selectedModel,
          messages: [
            {
              role: 'user',
              content: userPrompt
            }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        
        console.log("收到RTGO执行结果:", response.data);
        
        if (response.data.status === 'success' && response.data.data && 
            response.data.data.choices && response.data.data.choices.length > 0) {
          // 从API响应中提取AI的回复内容
          this.rtgoExecutionResult = response.data.data.choices[0].message.content;
          console.log("RTGO执行结果成功解析");
        } else {
          // 如果响应格式不符合预期，记录详细信息并抛出错误
          console.error("API响应格式不正确:", JSON.stringify(response.data));
          throw new Error('API响应格式不正确: ' + JSON.stringify(response.data, null, 2));
        }
      } catch (error) {
        console.error('执行RTGO提示词出错:', error);
        ElMessage.error(`执行提示词出错: ${error.message || '未知错误'}`);
        
        // 显示错误信息
        this.rtgoExecutionResult = `## 抱歉，执行提示词失败
        
连接后端服务出现问题。错误信息：${error.message || '未知错误'}

请稍后再试，或联系系统管理员。`;
      } finally {
        this.isRtgoExecuting = false;
      }
    },
    clearRtgoForm() {
      this.rtgoForm = {
        role: '',
        task: '',
        goal: '',
        objective: ''
      };
      this.rtgoAIFeedback = '';
      this.rtgoExecutionResult = '';
      this.currentRtgoStep = 1;
    },
    // CO-STAR提示词相关方法
    isCurrentCostarStep(step) {
      return this.currentCostarStep === step;
    },
    updateCostarProgress() {
      // 根据填写情况自动更新当前步骤
      if (!this.costarForm.context) {
        this.currentCostarStep = 1;
      } else if (!this.costarForm.objective) {
        this.currentCostarStep = 2;
      } else if (!this.costarForm.style) {
        this.currentCostarStep = 3;
      } else if (!this.costarForm.tone) {
        this.currentCostarStep = 4;
      } else if (!this.costarForm.audience) {
        this.currentCostarStep = 5;
      } else if (!this.costarForm.response) {
        this.currentCostarStep = 6;
      }
    },
    showCostarExamplesDialog() {
      this.costarDialogVisible = true;
    },
    applyCostarExample(example) {
      this.costarForm.context = example.context;
      this.costarForm.objective = example.objective;
      this.costarForm.style = example.style;
      this.costarForm.tone = example.tone;
      this.costarForm.audience = example.audience;
      this.costarForm.response = example.response;
      this.costarDialogVisible = false;
      this.currentCostarStep = 6; // 设置为最后一步，显示完整提示词
      ElMessage({
        message: '已应用参考案例',
        type: 'success'
      });
    },
    async getCostarAIFeedback() {
      if (!this.isCostarFormComplete) return;
      
      this.isCostarLoading = true;
      
      try {
        // 构建向大模型发送的消息
        const userPrompt = this.generatedCostarPrompt;
        
        // 系统提示词，指导大模型如何优化用户的提示词
        const systemPrompt = `你是一位专业的提示词工程师，你需要帮助用户优化他们的CO-STAR结构提示词，使其能够获得更好的AI回复效果。
请分析用户的提示词，然后提供具体的优化建议，包括：
1. 提示词的优点：分析现有提示词的哪些部分是清晰有效的
2. 可以改进的地方：指出模糊或缺少关键信息的部分
3. 优化后的提示词：给出一个更加完善、结构化的提示词版本
4. 建议：额外的提示词工程技巧或建议

请确保你的回复清晰、有条理，并且以优化后的提示词为重点。回复格式如下：

## 原始提示词分析
[分析用户原始提示词的优点和不足]

## 优化建议
[列出2-4点具体优化建议]

## 优化后的提示词
[提供优化后的完整提示词]

## 提示词工程小技巧
[1-2条相关的提示词工程技巧]`;

        console.log("发送CO-STAR请求到后端API...", this.selectedModel);
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', {
          model: this.selectedModel,
          messages: [
            {
              role: 'system',
              content: systemPrompt
            },
            {
              role: 'user',
              content: userPrompt
            }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        
        console.log("收到CO-STAR API响应:", response.data);
        
        if (response.data.status === 'success' && response.data.data && 
            response.data.data.choices && response.data.data.choices.length > 0) {
          // 从API响应中提取AI的回复内容
          this.costarAIFeedback = response.data.data.choices[0].message.content;
          console.log("CO-STAR AI回复成功解析");
        } else {
          // 如果响应格式不符合预期，记录详细信息并抛出错误
          console.error("API响应格式不正确:", JSON.stringify(response.data));
          throw new Error('API响应格式不正确: ' + JSON.stringify(response.data, null, 2));
        }
      } catch (error) {
        console.error('获取CO-STAR AI建议错误:', error);
        ElMessage.error(`获取AI建议出错: ${error.message || '未知错误'}`);
        
        // 出错后显示错误提示
        this.costarAIFeedback = `## 抱歉，无法获取AI反馈
        
连接后端服务出现问题。错误信息：${error.message || '未知错误'}

请稍后再试，或联系系统管理员。`;
      } finally {
        this.isCostarLoading = false;
      }
    },
    async executeCostarPrompt() {
      if (!this.isCostarFormComplete) return;
      
      this.isCostarExecuting = true;
      
      try {
        // 直接使用用户的提示词作为输入
        const userPrompt = this.generatedCostarPrompt;
        
        console.log("执行CO-STAR提示词，发送请求到后端API...", this.selectedModel);
        
        const response = await axios.post('http://localhost:9000/api/v1/llm/chat', {
          model: this.selectedModel,
          messages: [
            {
              role: 'user',
              content: userPrompt
            }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        
        console.log("收到CO-STAR执行结果:", response.data);
        
        if (response.data.status === 'success' && response.data.data && 
            response.data.data.choices && response.data.data.choices.length > 0) {
          // 从API响应中提取AI的回复内容
          this.costarExecutionResult = response.data.data.choices[0].message.content;
          console.log("CO-STAR执行结果成功解析");
        } else {
          // 如果响应格式不符合预期，记录详细信息并抛出错误
          console.error("API响应格式不正确:", JSON.stringify(response.data));
          throw new Error('API响应格式不正确: ' + JSON.stringify(response.data, null, 2));
        }
      } catch (error) {
        console.error('执行CO-STAR提示词出错:', error);
        ElMessage.error(`执行提示词出错: ${error.message || '未知错误'}`);
        
        // 显示错误信息
        this.costarExecutionResult = `## 抱歉，执行提示词失败
        
连接后端服务出现问题。错误信息：${error.message || '未知错误'}

请稍后再试，或联系系统管理员。`;
      } finally {
        this.isCostarExecuting = false;
      }
    },
    clearCostarForm() {
      this.costarForm = {
        context: '',
        objective: '',
        style: '',
        tone: '',
        audience: '',
        response: ''
      };
      this.costarAIFeedback = '';
      this.costarExecutionResult = '';
      this.currentCostarStep = 1;
    }
  }
}
</script>

<style scoped>
.prompt-engineering-container {
  padding: 20px;
  background-color: #f8f9fa;
}

.prompt-tabs {
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 自定义标签样式 */
.custom-tab-label {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s;
  border-radius: 6px;
  min-width: 180px;
  justify-content: center;
}

.custom-tab-label i {
  font-size: 20px;
  margin-right: 10px;
}

.custom-tab-label span {
  white-space: nowrap;
}

/* 各个标签的统一样式 */
.basic-tab,
.rtgo-tab,
.costar-tab {
  color: #909399;
}

/* 激活状态样式增强 */
:deep(.el-tabs__item.is-active .basic-tab),
:deep(.el-tabs__item.is-active .rtgo-tab),
:deep(.el-tabs__item.is-active .costar-tab) {
  color: #ba003f;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.2);
  background-color: transparent;
}

/* 悬停效果 */
:deep(.el-tabs__item:not(.is-active):hover .custom-tab-label) {
  transform: translateY(-1px);
  color: #606266;
}

:deep(.el-tabs__item) {
  padding: 0 20px;
}

:deep(.el-tabs__nav) {
  height: 56px;
}

:deep(.el-tabs__active-bar) {
  background-color: #ba003f;
  height: 3px;
}

:deep(.el-tabs__nav-wrap) {
  display: flex;
  justify-content: center;
}

:deep(.el-tabs__nav-scroll) {
  display: flex;
  justify-content: center;
}

.section-title {
  color: #333;
  border-bottom: 2px solid #ddd;
  padding-bottom: 5px;
  display: inline-block;
  margin-bottom: 15px;
}

.formula-container, 
.workflow-container,
.action-container,
.feedback-container,
.execution-container {
  margin-bottom: 30px;
  margin-top: 15px;
}

/* 标题与按钮并排样式 */
.header-with-button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.header-with-button .section-title {
  margin-bottom: 0;
}

.formula {
  font-size: 18px;
  line-height: 1.6;
  border-left: 4px solid #ba003f;
  padding: 10px 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.highlight {
  font-size: 20px;
  color: #ba003f;
  font-weight: bold;
  font-style: italic;
}

.example-box {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
  border-left: 3px solid #ddd;
}

.example-box h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #555;
}

.example-box p {
  margin: 0;
  color: #303133;
}

/* 进度条 */
.workflow-progress {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #f0f2f5;
  border-radius: 4px;
  overflow: hidden;
}

.progress-indicator {
  height: 100%;
  background-color: #ba003f;
  transition: width 0.3s ease;
}

.progress-text {
  margin-left: 10px;
  color: #666;
  min-width: 80px;
  text-align: right;
}

/* 流程步骤样式 */
.workflow-steps {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 5px 0;
}

.step-item {
  display: flex;
  align-items: flex-start;
  background-color: #f0f2f5;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s ease;
  margin-bottom: 5px;
  border: 1px solid #eee;
}

.step-item.active-step {
  background-color: #f8e8ec;
  border-color: #f0d0da;
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.1);
  transform: translateY(-2px) scale(1.01);
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #ba003f;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
  margin-top: 5px;
}

.step-content {
  flex: 1;
}

.step-title {
  margin-top: 0;
  margin-bottom: 12px;
  color: #333;
  font-weight: 500;
}

.step-hint {
  color: #999;
  font-size: 12px;
  margin-top: 8px;
}

.step-arrow {
  display: flex;
  justify-content: center;
  color: #ba003f;
  font-size: 24px;
  height: 25px;
  margin: 0;
}

.final-arrow {
  margin-bottom: 10px;
}

.result-step {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #eee;
}

.result-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.result-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #52c41a;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.result-title {
  margin: 0;
  color: #333;
  font-weight: 500;
}

.prompt-result {
  font-size: 16px;
  line-height: 1.6;
  background-color: white;
  border: 1px solid #eee;
}

.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin: 20px 0;
}

/* 使用Vue 3的深度选择器语法 */
:deep(.el-button--primary) {
  background-color: #ba003f;
  border-color: #ba003f;
}

:deep(.el-button--primary:hover),
:deep(.el-button--primary:focus) {
  background-color: #cf0046;
  border-color: #cf0046;
}

.ai-feedback {
  background-color: #f9f9f9;
  line-height: 1.6;
  border: 1px solid #eee;
}

.ai-feedback p {
  white-space: pre-line;
}

.execution-container {
  margin-bottom: 30px;
  margin-top: 15px;
}

.execution-result {
  background-color: #f0f9eb;
  line-height: 1.6;
  border: 1px solid #e1f3d8;
}

.execution-result p {
  white-space: pre-line;
}

/* 使用Vue 3的深度选择器语法 */
:deep(.el-button--primary.is-plain) {
  color: #fff;
  background-color: rgba(186, 0, 63, 0.9);
  border-color: #ba003f;
}

:deep(.el-button--primary.is-plain:hover),
:deep(.el-button--primary.is-plain:focus) {
  background-color: #ba003f;
  border-color: #ba003f;
}

/* 案例弹窗样式 */
:deep(.prompt-examples-dialog .el-dialog__header) {
  background-color: #ba003f;
  padding: 15px 20px;
  margin-right: 0;
  border-bottom: 1px solid #f0d0da;
}

:deep(.prompt-examples-dialog .el-dialog__title) {
  color: white;
  font-weight: bold;
  font-size: 18px;
}

:deep(.prompt-examples-dialog .el-dialog__headerbtn .el-dialog__close) {
  color: white;
}

:deep(.prompt-examples-dialog .el-dialog__headerbtn:hover .el-dialog__close) {
  color: #f0d0da;
}

:deep(.prompt-examples-dialog .el-dialog__body) {
  padding: 20px;
}

.examples-container {
  max-height: 70vh;
  overflow-y: auto;
  padding: 10px 0;
}

.example-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  overflow: hidden;
}

.example-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(186, 0, 63, 0.15);
  border-color: #ba003f;
}

.example-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 12px 15px 5px;
  border-bottom: 1px dashed rgba(186, 0, 63, 0.1);
}

.example-header i {
  font-size: 22px;
  color: #ba003f;
  margin-right: 10px;
  background-color: rgba(186, 0, 63, 0.1);
  padding: 8px;
  border-radius: 50%;
  height: 22px;
  width: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.example-title {
  font-weight: bold;
  font-size: 16px;
  color: #ba003f;
}

.example-desc {
  color: #666;
  font-size: 14px;
  padding: 0 15px 15px;
  line-height: 1.5;
}

/* RTGO标签页样式 */
.prompt-container {
  padding: 20px;
}

.prompt-formula-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  border-left: 4px solid #ba003f;
}

.prompt-formula-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.prompt-formula-description p {
  margin-bottom: 10px;
  line-height: 1.6;
}

.prompt-progress-container {
  margin: 30px 0;
}

.progress-bar-container {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.progress-bar-bg {
  flex: 1;
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #ba003f;
  transition: width 0.3s ease;
}

.progress-text {
  margin-left: 10px;
  min-width: 80px;
  font-size: 14px;
  color: #666;
}

.prompt-steps-container {
  margin-bottom: 30px;
}

.step-container {
  display: flex;
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
}

.step-container.active {
  border-color: #ba003f;
  box-shadow: 0 2px 12px rgba(186, 0, 63, 0.1);
}

.step-number {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #eee;
  color: #333;
  border-radius: 50%;
  margin-right: 15px;
  font-weight: bold;
}

.step-container.active .step-number {
  background-color: #ba003f;
  color: white;
}

.step-content {
  flex: 1;
}

.step-title {
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.step-container.active .step-title {
  color: #ba003f;
}

.prompt-buttons-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.generated-prompt-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #ba003f;
}

.generated-prompt-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.generated-prompt {
  padding: 15px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #e8e8e8;
}

.generated-prompt pre {
  white-space: pre-wrap;
  font-family: 'Courier New', monospace;
  color: #333;
  line-height: 1.6;
}

.prompt-action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  gap: 10px;
}

.feedback-container,
.execution-result-container {
  margin-top: 30px;
}

.feedback-title,
.execution-result-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.feedback-card {
  border-left: 4px solid #ba003f;
}

.execution-result-card {
  border-left: 4px solid #67c23a;
}

.feedback-content,
.execution-result-content {
  line-height: 1.6;
}

/* 添加formula-icon的样式 */
.formula-icon {
  color: #ba003f;
  font-size: 20px;
  margin-right: 8px;
  vertical-align: middle;
  background-color: rgba(186, 0, 63, 0.1);
  padding: 6px;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>