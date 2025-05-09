<template>
  <div class="prompt-engineering-container">
    <div class="page-header">
      <h1 class="page-title">提示词工程助手</h1>
      <p class="page-desc">选择下方提示语结构类型，按步骤填写信息，获得高质量AI回复</p>
    </div>

    <div class="method-selector">
      <div 
        class="method-option" 
        :class="{'active-method': activeTab === 'basic'}"
        @click="activeTab = 'basic'"
      >
        <div class="method-icon"><i class="ri-text-spacing"></i></div>
        <div class="method-info">
          <div class="method-name">基础提示语结构</div>
          <div class="method-desc">简单实用，适合新手</div>
        </div>
      </div>
      
      <div 
        class="method-option" 
        :class="{'active-method': activeTab === 'rtgo'}"
        @click="activeTab = 'rtgo'"
      >
        <div class="method-icon"><i class="ri-stack-line"></i></div>
        <div class="method-info">
          <div class="method-name">RTGO提示语结构</div>
          <div class="method-desc">专业输出，适合工作场景</div>
        </div>
      </div>
      
      <div 
        class="method-option" 
        :class="{'active-method': activeTab === 'costar'}"
        @click="activeTab = 'costar'"
      >
        <div class="method-icon"><i class="ri-film-line"></i></div>
        <div class="method-info">
          <div class="method-name">CO-STAR提示语结构</div>
          <div class="method-desc">创意写作，精确风格控制</div>
        </div>
      </div>
    </div>

    <!-- 添加指示器 -->
    <div class="tab-indicator-container">
      <div class="tab-indicator">
        <div class="indicator-item" :class="{'active': activeTab === 'basic'}"></div>
        <div class="indicator-item" :class="{'active': activeTab === 'rtgo'}"></div>
        <div class="indicator-item" :class="{'active': activeTab === 'costar'}"></div>
      </div>
    </div>

    <el-tabs v-model="activeTab" type="border-card" class="prompt-tabs">
      <el-tab-pane name="basic">
        <template #label>
          <div class="custom-tab-label basic-tab">
            <i class="ri-text-spacing"></i>
            <span>基础提示语结构</span>
          </div>
        </template>
        <div class="tab-description">
          <strong>基础提示语结构</strong> 是最简单实用的提示词框架，适合新手用户。通过"任务+背景+目标+负面"四要素构建，帮助您快速获得满意的AI回复。
        </div>
        <div class="knowledge-button-container">
          <el-button class="knowledge-button" type="primary" plain size="small" @click="showKnowledgeDrawer('basic')">
            <i class="ri-book-2-line"></i> 知识学习
          </el-button>
        </div>
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
            <el-button type="primary" @click="getAIFeedback" :disabled="!isFormComplete" :loading="isLoading"><i class="ri-robot-line btn-icon"></i> 获取AI建议</el-button>
            <el-button type="primary" @click="executePrompt" :disabled="!isFormComplete" :loading="isExecuting"><i class="ri-rocket-line btn-icon"></i> 执行提示词</el-button>
            <el-button @click="clearForm"><i class="ri-delete-bin-line btn-icon"></i> 清空</el-button>
          </div>
        </div>
        
        <div v-if="aiFeedback || isStreaming" class="feedback-container">
          <h3 class="section-title">AI建议</h3>
          <el-card class="ai-feedback" shadow="hover">
            <!-- 调试信息 -->
            <div v-if="isDebugMode" class="debug-info">
              <p>流式状态: {{isStreaming}}</p>
              <p>文本长度: {{isStreaming ? streamText.length : aiFeedback.length}}字节</p>
            </div>
            <!-- 使用纯文本显示框，不使用v-html -->
            <div class="feedback-text-box">{{isStreaming ? streamText : aiFeedback}}</div>
            <!-- 加载指示器 -->
            <div v-if="isStreaming" class="streaming-indicator">
              <span class="streaming-dot"></span>
              <span class="streaming-dot"></span>
              <span class="streaming-dot"></span>
            </div>
          </el-card>
        </div>

        <div v-if="executionResult || isExecutionStreaming" class="execution-container">
          <h3 class="section-title">执行结果</h3>
          <el-card class="execution-result" shadow="hover">
            <!-- 使用纯文本显示框，不使用v-html -->
            <div class="feedback-text-box">{{isExecutionStreaming ? executionStreamText : executionResult}}</div>
            <!-- 加载指示器 -->
            <div v-if="isExecutionStreaming" class="streaming-indicator">
              <span class="streaming-dot"></span>
              <span class="streaming-dot"></span>
              <span class="streaming-dot"></span>
            </div>
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
        <div class="tab-description">
          <strong>RTGO提示语结构</strong> 是一种专门设计用于优化与AI模型交互的提示工程框架，其核心目标是通过结构化指令提升生成内容的准确性、相关性和执行效率。该框架主要应用于技术文档编写、数据分析等需要高效率响应的场景。
        </div>
        <div class="knowledge-button-container">
          <el-button class="knowledge-button" type="primary" plain size="small" @click="showKnowledgeDrawer('rtgo')">
            <i class="ri-book-2-line"></i> 知识学习
          </el-button>
        </div>
        <div class="prompt-container">
          <div class="prompt-formula-card">
            <div class="prompt-formula-title">提示词公式：角色（Role） + 任务（Task） + 目标（Goal） + 操作要求（Objective）</div>
            <div class="prompt-formula-description">
              <p><span class="icon-wrapper"><i class="ri-user-star-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>角色（Role）：</strong>指定AI应该扮演的角色或身份，如专家类型、经验水平、职业背景等。</p>
              <p><span class="icon-wrapper"><i class="ri-task-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>任务（Task）：</strong>明确告诉AI需要完成的具体任务，包括内容类型、主题范围、处理对象等。</p>
              <p><span class="icon-wrapper"><i class="ri-flag-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>目标（Goal）：</strong>明确指定AI需要完成的具体任务和预期的结果，使其能够精确理解要求。</p>
              <p><span class="icon-wrapper"><i class="ri-settings-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>操作要求（Objective）：</strong>提供具体的操作指南，如格式要求、长度限制、语气风格、结构安排等。</p>
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
              <el-button type="primary" @click="getRtgoAIFeedback" :disabled="!isRtgoFormComplete" :loading="isRtgoLoading"><i class="ri-robot-line btn-icon"></i> 获取AI建议</el-button>
              <el-button type="primary" @click="executeRtgoPrompt" :disabled="!isRtgoFormComplete" :loading="isRtgoExecuting"><i class="ri-rocket-line btn-icon"></i> 执行提示词</el-button>
              <el-button @click="clearRtgoForm"><i class="ri-delete-bin-line btn-icon"></i> 清空</el-button>
            </div>
          </div>

          <div v-if="rtgoAIFeedback || isRtgoStreaming" class="feedback-container">
            <h3 class="section-title">AI建议</h3>
            <el-card class="ai-feedback" shadow="hover">
              <!-- 使用纯文本显示框，不使用v-html -->
              <div class="feedback-text-box">{{isRtgoStreaming ? rtgoStreamText : rtgoAIFeedback}}</div>
              <!-- 加载指示器 -->
              <div v-if="isRtgoStreaming" class="streaming-indicator">
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
              </div>
            </el-card>
          </div>

          <div v-if="rtgoExecutionResult || isRtgoExecutionStreaming" class="execution-container">
            <h3 class="section-title">执行结果</h3>
            <el-card class="execution-result" shadow="hover">
              <!-- 使用纯文本显示框，不使用v-html -->
              <div class="feedback-text-box">{{isRtgoExecutionStreaming ? rtgoExecutionStreamText : rtgoExecutionResult}}</div>
              <!-- 加载指示器 -->
              <div v-if="isRtgoExecutionStreaming" class="streaming-indicator">
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
              </div>
            </el-card>
          </div>
        </div>
      </el-tab-pane>
      
      <el-tab-pane name="costar">
        <template #label>
          <div class="custom-tab-label costar-tab">
            <i class="ri-film-line"></i>
            <span>CO-STAR提示语结构</span>
          </div>
        </template>
        <div class="tab-description">
          <strong>CO-STAR提示语结构</strong> 是一个系统化的提示词设计框架，旨在通过六个关键要素帮助用户构建清晰、精准的AI指令，从而优化生成内容的针对性和效果。该框架由新加坡政府科技局（GovTech）在提示工程大赛中推广，现广泛应用于社交媒体、商业报告等场景。其结构化设计能显著提升大型语言模型（LLM）的响应质量，并支持后续自动化优化。
        </div>
        <div class="knowledge-button-container">
          <el-button class="knowledge-button" type="primary" plain size="small" @click="showKnowledgeDrawer('costar')">
            <i class="ri-book-2-line"></i> 知识学习
          </el-button>
        </div>
        <div class="prompt-container">
          <div class="prompt-formula-card">
            <div class="prompt-formula-title">提示词公式：上下文（Context） + 目标（Objective） + 风格（Style） + 语调（Tone） + 受众（Audience） + 回应（Response）</div>
            <div class="prompt-formula-description">
              <p><span class="icon-wrapper"><i class="ri-file-info-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>上下文（Context）：</strong>提供相关背景和环境信息，包括项目需求、资源限制或其他任务相关的关键信息。</p>
              <p><span class="icon-wrapper"><i class="ri-flag-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>目标（Objective）：</strong>明确指定AI需要完成的具体任务和预期的结果，使其能够精确理解要求。</p>
              <p><span class="icon-wrapper"><i class="ri-brush-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>风格（Style）：</strong>定义内容的表达风格，如专业学术型、通俗易懂型、创意实验型或说明指导型等。</p>
              <p><span class="icon-wrapper"><i class="ri-volume-up-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>语调（Tone）：</strong>设定内容的情感基调，如正式严谨、友好亲切、幽默轻松或权威专业等。</p>
              <p><span class="icon-wrapper"><i class="ri-user-3-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>受众（Audience）：</strong>明确目标用户群体的特征，如专业水平、年龄段、行业背景或特定兴趣群体等。</p>
              <p><span class="icon-wrapper"><i class="ri-mail-send-line formula-icon" style="display: inline-block; background-color: rgba(186, 0, 63, 0.15); width: 32px; height: 32px; border-radius: 50%; color: #ba003f; text-align: center; line-height: 32px;"></i></span> <strong>回应（Response）：</strong>规定输出的形式和格式要求，如结构布局、字数限制、文档格式或视觉元素等。</p>
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
              <el-button type="primary" @click="getCostarAIFeedback" :disabled="!isCostarFormComplete" :loading="isCostarLoading"><i class="ri-robot-line btn-icon"></i> 获取AI建议</el-button>
              <el-button type="primary" @click="executeCostarPrompt" :disabled="!isCostarFormComplete" :loading="isCostarExecuting"><i class="ri-rocket-line btn-icon"></i> 执行提示词</el-button>
              <el-button @click="clearCostarForm"><i class="ri-delete-bin-line btn-icon"></i> 清空</el-button>
            </div>
          </div>

          <div v-if="costarAIFeedback || isCostarStreaming" class="feedback-container">
            <h3 class="section-title">AI建议</h3>
            <el-card class="ai-feedback" shadow="hover">
              <!-- 使用纯文本显示框，不使用v-html -->
              <div class="feedback-text-box">{{isCostarStreaming ? costarStreamText : costarAIFeedback}}</div>
              <!-- 加载指示器 -->
              <div v-if="isCostarStreaming" class="streaming-indicator">
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
              </div>
            </el-card>
          </div>

          <div v-if="costarExecutionResult || isCostarExecutionStreaming" class="execution-container">
            <h3 class="section-title">执行结果</h3>
            <el-card class="execution-result" shadow="hover">
              <!-- 使用纯文本显示框，不使用v-html -->
              <div class="feedback-text-box">{{isCostarExecutionStreaming ? costarExecutionStreamText : costarExecutionResult}}</div>
              <!-- 加载指示器 -->
              <div v-if="isCostarExecutionStreaming" class="streaming-indicator">
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
                <span class="streaming-dot"></span>
              </div>
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
            <div class="example-card" @click="applyExample(example)">
              <div class="example-card-header">
                <div class="example-icon"><i :class="example.icon"></i></div>
                <div class="example-title">{{ example.title }}</div>
              </div>
              <div class="example-desc">{{ example.description }}</div>
              <div class="example-detail">
                <div class="detail-item"><span class="detail-label">任务：</span>{{ example.task }}</div>
                <div class="detail-item"><span class="detail-label">受众：</span>{{ example.audience }}</div>
                <div class="detail-item"><span class="detail-label">目标：</span>{{ example.goal }}</div>
                <div class="detail-item"><span class="detail-label">顾虑：</span>{{ example.concern }}</div>
              </div>
              <div class="example-action">
                <span class="apply-btn">应用此案例</span>
              </div>
            </div>
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
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" v-for="(example, index) in rtgoPromptExamples" :key="index">
            <div class="example-card" @click="applyRtgoExample(example)">
              <div class="example-card-header">
                <div class="example-icon"><i :class="example.icon"></i></div>
                <div class="example-title">{{ example.title }}</div>
          </div>
              <div class="example-desc">{{ example.description }}</div>
              <div class="example-detail">
                <div class="detail-item"><span class="detail-label">角色：</span>{{ example.role.slice(0, 30) }}{{ example.role.length > 30 ? '...' : '' }}</div>
                <div class="detail-item"><span class="detail-label">任务：</span>{{ example.task.slice(0, 30) }}{{ example.task.length > 30 ? '...' : '' }}</div>
                <div class="detail-item"><span class="detail-label">目标：</span>{{ example.goal.slice(0, 30) }}{{ example.goal.length > 30 ? '...' : '' }}</div>
        </div>
              <div class="example-action">
                <span class="apply-btn">应用此案例</span>
              </div>
            </div>
          </el-col>
        </el-row>
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
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" v-for="(example, index) in costarPromptExamples" :key="index">
            <div class="example-card" @click="applyCostarExample(example)">
              <div class="example-card-header">
                <div class="example-icon"><i :class="example.icon"></i></div>
                <div class="example-title">{{ example.title }}</div>
          </div>
              <div class="example-desc">{{ example.description }}</div>
              <div class="example-detail">
                <div class="detail-item"><span class="detail-label">上下文：</span>{{ example.context.slice(0, 30) }}{{ example.context.length > 30 ? '...' : '' }}</div>
                <div class="detail-item"><span class="detail-label">目标：</span>{{ example.objective.slice(0, 30) }}{{ example.objective.length > 30 ? '...' : '' }}</div>
                <div class="detail-item"><span class="detail-label">受众：</span>{{ example.audience.slice(0, 30) }}{{ example.audience.length > 30 ? '...' : '' }}</div>
        </div>
              <div class="example-action">
                <span class="apply-btn">应用此案例</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-dialog>

    <!-- 显示结果对话框 -->
    <el-dialog
      title="提示词结果"
      v-model="showResultDialog"
      width="50%"
      destroy-on-close
      class="prompt-result-dialog"
    >
      <div class="result-container">
        <p>{{ generatedPrompt }}</p>
      </div>
      <div class="action-buttons">
        <el-button type="primary" @click="closeResultDialog">关闭</el-button>
        <el-button type="primary" @click="copyPrompt">复制提示词</el-button>
      </div>
    </el-dialog>

    <!-- 添加知识学习右侧抽屉组件 -->
    <el-drawer
      v-model="knowledgeDrawerVisible"
      :title="currentKnowledge.title"
      direction="rtl"
      size="30%"
      :destroy-on-close="false"
      class="knowledge-drawer"
    >
      <div class="knowledge-content">
        <div v-for="(item, index) in currentKnowledge.content" :key="index" class="knowledge-section">
          <h3 class="knowledge-subtitle">
            <i :class="getKnowledgeIcon()" class="knowledge-icon"></i>
            {{ item.subtitle }}
          </h3>
          <div class="knowledge-text" v-html="formatMarkdown(item.text)"></div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import 'remixicon/fonts/remixicon.css';

// 响应式状态
const activeTab = ref('basic');
const promptForm = reactive({
        task: '',
        audience: '',
        goal: '',
        concern: ''
});

// 新增流式输出相关状态
const isStreaming = ref(false);
const streamText = ref("");
// 添加执行提示词相关的流式输出状态
const isExecutionStreaming = ref(false);
const executionStreamText = ref("");
// 添加RTGO相关的流式输出状态
const isRtgoStreaming = ref(false);
const rtgoStreamText = ref("");
const isRtgoExecutionStreaming = ref(false);
const rtgoExecutionStreamText = ref("");
// 添加CO-STAR相关的流式输出状态
const isCostarStreaming = ref(false);
const costarStreamText = ref("");
const isCostarExecutionStreaming = ref(false);
const costarExecutionStreamText = ref("");
// 添加调试模式控制
const isDebugMode = ref(false);  // 设为false隐藏调试信息

      // RTGO表单数据
const rtgoForm = reactive({
        role: '',
        task: '',
        goal: '',
        objective: ''
});

      // CO-STAR表单数据
const costarForm = reactive({
        context: '',
        objective: '',
        style: '',
        tone: '',
        audience: '',
        response: ''
});

const aiFeedback = ref('');
const executionResult = ref('');
const rtgoAIFeedback = ref('');
const rtgoExecutionResult = ref('');
const costarAIFeedback = ref('');
const costarExecutionResult = ref('');
const isLoading = ref(false);
const isExecuting = ref(false);
const isRtgoLoading = ref(false);
const isRtgoExecuting = ref(false);
const isCostarLoading = ref(false);
const isCostarExecuting = ref(false);
const currentStep = ref(1);
const currentRtgoStep = ref(1);
const currentCostarStep = ref(1);
const modelOptions = [
        { label: 'DeepSeek R1-64K (硅基流动)', value: 'deepseek-r1-sf' },
        { label: 'DeepSeek V3-64K (硅基流动)', value: 'deepseek-v3-sf' },
        { label: 'DeepSeek R1-64K (火山引擎)', value: 'deepseek-r1-vol' },
        { label: 'DeepSeek V3-64K (火山引擎)', value: 'deepseek-v3-vol' },
        { label: '通义千问-32B (硅基流动)', value: 'qwq-32b' },
        { label: '豆包-Pro (火山引擎)', value: 'doubao-pro' },
        { label: '通义千问-Max (阿里云)', value: 'qwen-max' }
];
const selectedModel = ref('deepseek-v3-vol');
const dialogVisible = ref(false);
const rtgoDialogVisible = ref(false);
const costarDialogVisible = ref(false);
const showResultDialog = ref(false);

// 知识学习抽屉相关状态
const knowledgeDrawerVisible = ref(false);
const currentKnowledgeType = ref('basic');
const currentKnowledge = computed(() => {
  return promptKnowledge[currentKnowledgeType.value] || promptKnowledge.basic;
});

// 导入示例数据
import { promptExamples, rtgoPromptExamples, costarPromptExamples } from './example-data.js';
import { promptKnowledge } from './knowledge-data.js';

// 计算属性
const isFormComplete = computed(() => {
  return promptForm.task && promptForm.audience && promptForm.goal && promptForm.concern;
});

const generatedPrompt = computed(() => {
  if (!isFormComplete.value) return '填写完所有字段后将在此显示完整提示语...';
  return `我要${promptForm.task}，要给${promptForm.audience}用，我希望达到${promptForm.goal}效果，但是担心${promptForm.concern}问题。`;
});

const progressWidth = computed(() => {
  let count = 0;
  if (promptForm.task) count++;
  if (promptForm.audience) count++;
  if (promptForm.goal) count++;
  if (promptForm.concern) count++;
  return `${count * 25}%`;
});

const progressText = computed(() => {
  let count = 0;
  if (promptForm.task) count++;
  if (promptForm.audience) count++;
  if (promptForm.goal) count++;
  if (promptForm.concern) count++;
  return `${count}/4`;
});

const formattedFeedback = computed(() => {
  // 使用流式文本或普通反馈文本
  const text = isStreaming.value ? streamText.value : aiFeedback.value;
  console.log("格式化反馈:", text ? text.length : 0, "字节");
  
  // 调试信息
  let debugInfo = '';
  if (isStreaming.value) {
    debugInfo = `<div style="color: green; margin-bottom: 10px;">
      [调试] 流式状态: ${isStreaming.value}, 文本长度: ${text.length}字节
    </div>`;
  }
  
  // 转义换行为<br>标签
  const formatted = text.replace(/\n/g, '<br>');
  
  // 返回带调试信息的HTML
  return debugInfo + formatted;
});

const formattedExecutionResult = computed(() => {
  return executionResult.value.replace(/\n/g, '<br>');
});

// RTGO相关计算属性
const isRtgoFormComplete = computed(() => {
  return rtgoForm.role && rtgoForm.task && rtgoForm.goal && rtgoForm.objective;
});

const generatedRtgoPrompt = computed(() => {
  if (!isRtgoFormComplete.value) return '填写完所有字段后将在此显示完整提示语...';
  return `角色：${rtgoForm.role}\n\n任务：${rtgoForm.task}\n\n目标：${rtgoForm.goal}\n\n操作要求：${rtgoForm.objective}`;
});

const rtgoProgressWidth = computed(() => {
  let count = 0;
  if (rtgoForm.role) count++;
  if (rtgoForm.task) count++;
  if (rtgoForm.goal) count++;
  if (rtgoForm.objective) count++;
  return `${count * 25}%`;
});

const rtgoProgressText = computed(() => {
  let count = 0;
  if (rtgoForm.role) count++;
  if (rtgoForm.task) count++;
  if (rtgoForm.goal) count++;
  if (rtgoForm.objective) count++;
  return `${count}/4`;
});

const formattedRtgoFeedback = computed(() => {
  return rtgoAIFeedback.value.replace(/\n/g, '<br>');
});

const formattedRtgoExecutionResult = computed(() => {
  return rtgoExecutionResult.value.replace(/\n/g, '<br>');
});

// CO-STAR相关计算属性
const isCostarFormComplete = computed(() => {
  return costarForm.context && costarForm.objective && costarForm.style && 
         costarForm.tone && costarForm.audience && costarForm.response;
});

const generatedCostarPrompt = computed(() => {
  if (!isCostarFormComplete.value) return '填写完所有字段后将在此显示完整提示语...';
  return `上下文：${costarForm.context}\n\n目标：${costarForm.objective}\n\n风格：${costarForm.style}\n\n语气：${costarForm.tone}\n\n受众：${costarForm.audience}\n\n回复格式：${costarForm.response}`;
});

const costarProgressWidth = computed(() => {
  let count = 0;
  if (costarForm.context) count++;
  if (costarForm.objective) count++;
  if (costarForm.style) count++;
  if (costarForm.tone) count++;
  if (costarForm.audience) count++;
  if (costarForm.response) count++;
  return `${(count / 6) * 100}%`;
});

const costarProgressText = computed(() => {
  let count = 0;
  if (costarForm.context) count++;
  if (costarForm.objective) count++;
  if (costarForm.style) count++;
  if (costarForm.tone) count++;
  if (costarForm.audience) count++;
  if (costarForm.response) count++;
  return `${count}/6`;
});

const formattedCostarFeedback = computed(() => {
  return costarAIFeedback.value.replace(/\n/g, '<br>');
});

const formattedCostarExecutionResult = computed(() => {
  return costarExecutionResult.value.replace(/\n/g, '<br>');
});

// 基础提示语方法
function isCurrentStep(step) {
  return currentStep.value === step;
}

function updateProgress() {
  // 使用nextTick确保DOM已更新
  nextTick(() => {
    // 根据填写情况自动更新当前步骤
    if (!promptForm.task) {
      currentStep.value = 1;
    } else if (!promptForm.audience) {
      currentStep.value = 2;
    } else if (!promptForm.goal) {
      currentStep.value = 3;
    } else if (!promptForm.concern) {
      currentStep.value = 4;
    }
  });
}

function showExamplesDialog() {
  // 预先设置对话框状态为true，但不立即显示
  dialogVisible.value = true;
  
  // 使用setTimeout确保DOM更新后再显示对话框
  setTimeout(() => {
    // 强制重新渲染对话框
    dialogVisible.value = false;
    nextTick(() => {
      dialogVisible.value = true;
    });
  }, 50);
}

function applyExample(example) {
  promptForm.task = example.task;
  promptForm.audience = example.audience;
  promptForm.goal = example.goal;
  promptForm.concern = example.concern;
  
  nextTick(() => {
    dialogVisible.value = false;
    currentStep.value = 4; // 设置为最后一步，显示完整提示词
      ElMessage({
        message: '已应用参考案例',
        type: 'success'
      });
  });
}

async function getAIFeedback() {
  if (!isFormComplete.value) return;
  
  isLoading.value = true;
  isStreaming.value = true;
  aiFeedback.value = "";
  streamText.value = "";
  
  try {
    // 准备发送给API的提示词
    const prompt = generatedPrompt.value;
    console.log("开始执行getAIFeedback请求", prompt);
    
    // 构造请求数据
    const requestData = {
      model: 'deepseek-v3', // 使用火山引擎V3模型
      messages: [
        { role: 'system', content: '你是一个专业的提示词工程师，擅长给出专业的提示词建议。' },
        { role: 'user', content: `请针对以下提示词给出改进建议，尤其是如何让这个提示词更加清晰、有效。提示词：${prompt}` }
      ],
      stream: true,
      temperature: 0.7,
      max_tokens: 2000
    };
    
    console.log("请求数据:", JSON.stringify(requestData));
    
    // 使用原生fetch进行请求
    const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    
    // 检查返回的内容类型
    console.log("响应Content-Type:", response.headers.get('Content-Type'));
    
    // 使用原生响应体处理流式数据
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    
    // 使用循环处理流数据
    let buffer = '';
    let accumulatedText = '';
    
    // 处理流数据
    while (true) {
      // 读取一块数据
      const { value, done } = await reader.read();
      
      // 如果读取完毕，退出循环
      if (done) {
        console.log("数据流已结束");
        break;
      }
      
      // 解码二进制数据为文本
      const chunk = decoder.decode(value, { stream: true });
      console.log("收到数据块:", chunk.length, "字节");
      buffer += chunk;
      
      // 按SSE格式解析 (data: xxx\n\n)
      const messages = buffer.split('\n\n');
      buffer = messages.pop() || ''; // 保留最后一部分，可能是不完整的消息
      
      // 处理每条完整消息
      for (const message of messages) {
        // 跳过空消息
        if (!message.trim()) continue;
        
        // 提取data部分
        if (message.startsWith('data: ')) {
          const data = message.substring(6);
          console.log("处理消息:", data.substring(0, 50) + (data.length > 50 ? '...' : ''));
          
          // 处理结束标记
          if (data === '[DONE]') {
            console.log("收到结束标记");
            isStreaming.value = false;
            isLoading.value = false;
            // 确保最终内容被保存
            aiFeedback.value = accumulatedText;
            return;
          }
          
          try {
            // 解析JSON数据
            const jsonData = JSON.parse(data);
            
            // 处理错误
            if (jsonData.error) {
              console.error("API错误:", jsonData.error);
              ElMessage.error(jsonData.error.message || '请求出错');
              isStreaming.value = false;
              isLoading.value = false;
              return;
            }
            
            // 处理内容增量
            if (jsonData.choices && 
                jsonData.choices[0].delta && 
                jsonData.choices[0].delta.content) {
              const content = jsonData.choices[0].delta.content;
              console.log("收到内容:", content);
              
              // 累积内容
              accumulatedText += content;
              
              // 使用直接赋值方式完全替换字符串，确保Vue检测到变化
              streamText.value = accumulatedText;
              
              // 强制更新视图（Vue 3中使用nextTick）
              await nextTick();
            }
          } catch (e) {
            console.error("解析JSON失败:", e, data);
          }
        }
      }
    }
    
    // 处理可能的剩余buffer
    if (buffer.trim() && buffer.startsWith('data: ')) {
      const data = buffer.substring(6);
      try {
        const jsonData = JSON.parse(data);
        if (jsonData.choices && 
            jsonData.choices[0].delta && 
            jsonData.choices[0].delta.content) {
          accumulatedText += jsonData.choices[0].delta.content;
          streamText.value = accumulatedText;
          await nextTick();
        }
      } catch (e) {
        console.error("解析剩余JSON失败:", e);
      }
    }
    
    // 结束时更新
    console.log("流处理完成");
    isStreaming.value = false;
    isLoading.value = false;
    aiFeedback.value = accumulatedText;
    
  } catch (error) {
    console.error('获取AI建议错误:', error);
    ElMessage.error('获取AI建议出错: ' + error.message);
    isStreaming.value = false;
    isLoading.value = false;
  }
}

async function executePrompt() {
  if (!isFormComplete.value) return;
  
  isExecuting.value = true;
  isExecutionStreaming.value = true;
  executionResult.value = "";
  executionStreamText.value = "";
  
  try {
    // 准备发送给API的提示词
    const prompt = generatedPrompt.value;
    console.log("开始执行executePrompt请求", prompt);
    
    // 构造请求数据
    const requestData = {
      model: 'deepseek-v3', // 使用火山引擎V3模型
      messages: [
        { role: 'system', content: '你是一个专业的AI助手，请直接回答用户的问题或执行用户的请求。' },
        { role: 'user', content: prompt }
      ],
      stream: true,
      temperature: 0.7,
      max_tokens: 2000
    };
    
    console.log("请求数据:", JSON.stringify(requestData));
    
    // 使用原生fetch进行请求
    const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    
    // 检查返回的内容类型
    console.log("响应Content-Type:", response.headers.get('Content-Type'));
    
    // 使用原生响应体处理流式数据
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    
    // 使用循环处理流数据
    let buffer = '';
    let accumulatedText = '';
    
    // 处理流数据
    while (true) {
      // 读取一块数据
      const { value, done } = await reader.read();
      
      // 如果读取完毕，退出循环
      if (done) {
        console.log("数据流已结束");
        break;
      }
      
      // 解码二进制数据为文本
      const chunk = decoder.decode(value, { stream: true });
      console.log("收到数据块:", chunk.length, "字节");
      buffer += chunk;
      
      // 按SSE格式解析 (data: xxx\n\n)
      const messages = buffer.split('\n\n');
      buffer = messages.pop() || ''; // 保留最后一部分，可能是不完整的消息
      
      // 处理每条完整消息
      for (const message of messages) {
        // 跳过空消息
        if (!message.trim()) continue;
        
        // 提取data部分
        if (message.startsWith('data: ')) {
          const data = message.substring(6);
          console.log("处理消息:", data.substring(0, 50) + (data.length > 50 ? '...' : ''));
          
          // 处理结束标记
          if (data === '[DONE]') {
            console.log("收到结束标记");
            isExecutionStreaming.value = false;
            isExecuting.value = false;
            // 确保最终内容被保存
            executionResult.value = accumulatedText;
            return;
          }
          
          try {
            // 解析JSON数据
            const jsonData = JSON.parse(data);
            
            // 处理错误
            if (jsonData.error) {
              console.error("API错误:", jsonData.error);
              ElMessage.error(jsonData.error.message || '请求出错');
              isExecutionStreaming.value = false;
              isExecuting.value = false;
              return;
            }
            
            // 处理内容增量
            if (jsonData.choices && 
                jsonData.choices[0].delta && 
                jsonData.choices[0].delta.content) {
              const content = jsonData.choices[0].delta.content;
              console.log("收到内容:", content);
              
              // 累积内容
              accumulatedText += content;
              
              // 使用直接赋值方式完全替换字符串，确保Vue检测到变化
              executionStreamText.value = accumulatedText;
              
              // 强制更新视图（Vue 3中使用nextTick）
              await nextTick();
            }
          } catch (e) {
            console.error("解析JSON失败:", e, data);
          }
        }
      }
    }
    
    // 处理可能的剩余buffer
    if (buffer.trim() && buffer.startsWith('data: ')) {
      const data = buffer.substring(6);
      try {
        const jsonData = JSON.parse(data);
        if (jsonData.choices && 
            jsonData.choices[0].delta && 
            jsonData.choices[0].delta.content) {
          accumulatedText += jsonData.choices[0].delta.content;
          executionStreamText.value = accumulatedText;
          await nextTick();
        }
      } catch (e) {
        console.error("解析剩余JSON失败:", e);
      }
    }
    
    // 结束时更新
    console.log("流处理完成");
    isExecutionStreaming.value = false;
    isExecuting.value = false;
    executionResult.value = accumulatedText;
    
  } catch (error) {
    console.error('执行提示词出错:', error);
    ElMessage.error('执行提示词出错: ' + error.message);
    isExecutionStreaming.value = false;
    isExecuting.value = false;
  }
}

function clearForm() {
  promptForm.task = '';
  promptForm.audience = '';
  promptForm.goal = '';
  promptForm.concern = '';
  
  nextTick(() => {
    aiFeedback.value = '';
    executionResult.value = '';
    currentStep.value = 1;
  });
}

// RTGO提示词相关方法
function isCurrentRtgoStep(step) {
  return currentRtgoStep.value === step;
}

function updateRtgoProgress() {
  // 使用nextTick确保DOM已更新
  nextTick(() => {
    // 根据填写情况自动更新当前步骤
    if (!rtgoForm.role) {
      currentRtgoStep.value = 1;
    } else if (!rtgoForm.task) {
      currentRtgoStep.value = 2;
    } else if (!rtgoForm.goal) {
      currentRtgoStep.value = 3;
    } else if (!rtgoForm.objective) {
      currentRtgoStep.value = 4;
    }
  });
}

function showRtgoExamplesDialog() {
  // 预先设置对话框状态为true，但不立即显示
  rtgoDialogVisible.value = true;
  
  // 使用setTimeout确保DOM更新后再显示对话框
  setTimeout(() => {
    // 强制重新渲染对话框
    rtgoDialogVisible.value = false;
    nextTick(() => {
      rtgoDialogVisible.value = true;
    });
  }, 50);
}

function applyRtgoExample(example) {
  rtgoForm.role = example.role;
  rtgoForm.task = example.task;
  rtgoForm.goal = example.goal;
  rtgoForm.objective = example.objective;
  
  nextTick(() => {
    rtgoDialogVisible.value = false;
    currentRtgoStep.value = 4; // 设置为最后一步，显示完整提示词
      ElMessage({
        message: '已应用参考案例',
        type: 'success'
      });
  });
}

async function getRtgoAIFeedback() {
  if (!isRtgoFormComplete.value) return;
  
  isRtgoLoading.value = true;
  isRtgoStreaming.value = true;
  rtgoAIFeedback.value = "";
  rtgoStreamText.value = "";
  
  try {
    // 准备发送给API的提示词
    const prompt = generatedRtgoPrompt.value;
    console.log("开始执行getRtgoAIFeedback请求", prompt);
    
    // 构造请求数据
    const requestData = {
      model: 'deepseek-v3', // 使用火山引擎V3模型
      messages: [
        { role: 'system', content: '你是一个专业的提示词工程师，擅长给出专业的提示词建议。' },
        { role: 'user', content: `请针对以下RTGO结构提示词给出改进建议，尤其是如何让这个提示词更加清晰、有效。提示词：${prompt}` }
      ],
      stream: true,
      temperature: 0.7,
      max_tokens: 2000
    };
    
    console.log("请求数据:", JSON.stringify(requestData));
    
    // 使用原生fetch进行请求
    const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    
    // 检查返回的内容类型
    console.log("响应Content-Type:", response.headers.get('Content-Type'));
    
    // 使用原生响应体处理流式数据
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    
    // 使用循环处理流数据
    let buffer = '';
    let accumulatedText = '';
    
    // 处理流数据
    while (true) {
      // 读取一块数据
      const { value, done } = await reader.read();
      
      // 如果读取完毕，退出循环
      if (done) {
        console.log("数据流已结束");
        break;
      }
      
      // 解码二进制数据为文本
      const chunk = decoder.decode(value, { stream: true });
      console.log("收到数据块:", chunk.length, "字节");
      buffer += chunk;
      
      // 按SSE格式解析 (data: xxx\n\n)
      const messages = buffer.split('\n\n');
      buffer = messages.pop() || ''; // 保留最后一部分，可能是不完整的消息
      
      // 处理每条完整消息
      for (const message of messages) {
        // 跳过空消息
        if (!message.trim()) continue;
        
        // 提取data部分
        if (message.startsWith('data: ')) {
          const data = message.substring(6);
          console.log("处理消息:", data.substring(0, 50) + (data.length > 50 ? '...' : ''));
          
          // 处理结束标记
          if (data === '[DONE]') {
            console.log("收到结束标记");
            isRtgoStreaming.value = false;
            isRtgoLoading.value = false;
            // 确保最终内容被保存
            rtgoAIFeedback.value = accumulatedText;
            return;
          }
          
          try {
            // 解析JSON数据
            const jsonData = JSON.parse(data);
            
            // 处理错误
            if (jsonData.error) {
              console.error("API错误:", jsonData.error);
              ElMessage.error(jsonData.error.message || '请求出错');
              isRtgoStreaming.value = false;
              isRtgoLoading.value = false;
              return;
            }
            
            // 处理内容增量
            if (jsonData.choices && 
                jsonData.choices[0].delta && 
                jsonData.choices[0].delta.content) {
              const content = jsonData.choices[0].delta.content;
              console.log("收到内容:", content);
              
              // 累积内容
              accumulatedText += content;
              
              // 使用直接赋值方式完全替换字符串，确保Vue检测到变化
              rtgoStreamText.value = accumulatedText;
              
              // 强制更新视图（Vue 3中使用nextTick）
              await nextTick();
            }
          } catch (e) {
            console.error("解析JSON失败:", e, data);
          }
        }
      }
    }
    
    // 处理可能的剩余buffer
    if (buffer.trim() && buffer.startsWith('data: ')) {
      const data = buffer.substring(6);
      try {
        const jsonData = JSON.parse(data);
        if (jsonData.choices && 
            jsonData.choices[0].delta && 
            jsonData.choices[0].delta.content) {
          accumulatedText += jsonData.choices[0].delta.content;
          rtgoStreamText.value = accumulatedText;
          await nextTick();
        }
      } catch (e) {
        console.error("解析剩余JSON失败:", e);
      }
    }
    
    // 结束时更新
    console.log("流处理完成");
    isRtgoStreaming.value = false;
    isRtgoLoading.value = false;
    rtgoAIFeedback.value = accumulatedText;
    
  } catch (error) {
    console.error('获取RTGO AI建议错误:', error);
    ElMessage.error('获取AI建议出错: ' + error.message);
    isRtgoStreaming.value = false;
    isRtgoLoading.value = false;
  }
}

async function executeRtgoPrompt() {
  if (!isRtgoFormComplete.value) return;
  
  isRtgoExecuting.value = true;
  isRtgoExecutionStreaming.value = true;
  rtgoExecutionResult.value = "";
  rtgoExecutionStreamText.value = "";
  
  try {
    // 准备发送给API的提示词
    const prompt = generatedRtgoPrompt.value;
    console.log("开始执行executeRtgoPrompt请求", prompt);
    
    // 构造请求数据
    const requestData = {
      model: 'deepseek-v3', // 使用火山引擎V3模型
      messages: [
        { role: 'system', content: '你是一个专业的AI助手，请直接回答用户的问题或执行用户的请求。' },
        { role: 'user', content: prompt }
      ],
      stream: true,
      temperature: 0.7,
      max_tokens: 2000
    };
    
    console.log("请求数据:", JSON.stringify(requestData));
    
    // 使用原生fetch进行请求
    const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    
    // 检查返回的内容类型
    console.log("响应Content-Type:", response.headers.get('Content-Type'));
    
    // 使用原生响应体处理流式数据
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    
    // 使用循环处理流数据
    let buffer = '';
    let accumulatedText = '';
    
    // 处理流数据
    while (true) {
      // 读取一块数据
      const { value, done } = await reader.read();
      
      // 如果读取完毕，退出循环
      if (done) {
        console.log("数据流已结束");
        break;
      }
      
      // 解码二进制数据为文本
      const chunk = decoder.decode(value, { stream: true });
      console.log("收到数据块:", chunk.length, "字节");
      buffer += chunk;
      
      // 按SSE格式解析 (data: xxx\n\n)
      const messages = buffer.split('\n\n');
      buffer = messages.pop() || ''; // 保留最后一部分，可能是不完整的消息
      
      // 处理每条完整消息
      for (const message of messages) {
        // 跳过空消息
        if (!message.trim()) continue;
        
        // 提取data部分
        if (message.startsWith('data: ')) {
          const data = message.substring(6);
          console.log("处理消息:", data.substring(0, 50) + (data.length > 50 ? '...' : ''));
          
          // 处理结束标记
          if (data === '[DONE]') {
            console.log("收到结束标记");
            isRtgoExecutionStreaming.value = false;
            isRtgoExecuting.value = false;
            // 确保最终内容被保存
            rtgoExecutionResult.value = accumulatedText;
            return;
          }
          
          try {
            // 解析JSON数据
            const jsonData = JSON.parse(data);
            
            // 处理错误
            if (jsonData.error) {
              console.error("API错误:", jsonData.error);
              ElMessage.error(jsonData.error.message || '请求出错');
              isRtgoExecutionStreaming.value = false;
              isRtgoExecuting.value = false;
              return;
            }
            
            // 处理内容增量
            if (jsonData.choices && 
                jsonData.choices[0].delta && 
                jsonData.choices[0].delta.content) {
              const content = jsonData.choices[0].delta.content;
              console.log("收到内容:", content);
              
              // 累积内容
              accumulatedText += content;
              
              // 使用直接赋值方式完全替换字符串，确保Vue检测到变化
              rtgoExecutionStreamText.value = accumulatedText;
              
              // 强制更新视图（Vue 3中使用nextTick）
              await nextTick();
            }
          } catch (e) {
            console.error("解析JSON失败:", e, data);
          }
        }
      }
    }
    
    // 处理可能的剩余buffer
    if (buffer.trim() && buffer.startsWith('data: ')) {
      const data = buffer.substring(6);
      try {
        const jsonData = JSON.parse(data);
        if (jsonData.choices && 
            jsonData.choices[0].delta && 
            jsonData.choices[0].delta.content) {
          accumulatedText += jsonData.choices[0].delta.content;
          rtgoExecutionStreamText.value = accumulatedText;
          await nextTick();
        }
      } catch (e) {
        console.error("解析剩余JSON失败:", e);
      }
    }
    
    // 结束时更新
    console.log("流处理完成");
    isRtgoExecutionStreaming.value = false;
    isRtgoExecuting.value = false;
    rtgoExecutionResult.value = accumulatedText;
    
      } catch (error) {
    console.error('执行RTGO提示词出错:', error);
    ElMessage.error('执行提示词出错: ' + error.message);
    isRtgoExecutionStreaming.value = false;
    isRtgoExecuting.value = false;
  }
}

function clearRtgoForm() {
  rtgoForm.role = '';
  rtgoForm.task = '';
  rtgoForm.goal = '';
  rtgoForm.objective = '';
  
  nextTick(() => {
    rtgoAIFeedback.value = '';
    rtgoExecutionResult.value = '';
    currentRtgoStep.value = 1;
  });
}

// CO-STAR提示词相关方法
function isCurrentCostarStep(step) {
  return currentCostarStep.value === step;
}

function updateCostarProgress() {
  // 使用nextTick确保DOM已更新
  nextTick(() => {
    // 根据填写情况自动更新当前步骤
    if (!costarForm.context) {
      currentCostarStep.value = 1;
    } else if (!costarForm.objective) {
      currentCostarStep.value = 2;
    } else if (!costarForm.style) {
      currentCostarStep.value = 3;
    } else if (!costarForm.tone) {
      currentCostarStep.value = 4;
    } else if (!costarForm.audience) {
      currentCostarStep.value = 5;
    } else if (!costarForm.response) {
      currentCostarStep.value = 6;
    }
  });
}

function showCostarExamplesDialog() {
  // 预先设置对话框状态为true，但不立即显示
  costarDialogVisible.value = true;
  
  // 使用setTimeout确保DOM更新后再显示对话框
  setTimeout(() => {
    // 强制重新渲染对话框
    costarDialogVisible.value = false;
    nextTick(() => {
      costarDialogVisible.value = true;
    });
  }, 50);
}

function applyCostarExample(example) {
  costarForm.context = example.context;
  costarForm.objective = example.objective;
  costarForm.style = example.style;
  costarForm.tone = example.tone;
  costarForm.audience = example.audience;
  costarForm.response = example.response;
  
  nextTick(() => {
    costarDialogVisible.value = false;
    currentCostarStep.value = 6; // 设置为最后一步，显示完整提示词
    ElMessage({
      message: '已应用参考案例',
      type: 'success'
    });
  });
}

async function getCostarAIFeedback() {
  if (!isCostarFormComplete.value) return;
  
  isCostarLoading.value = true;
  isCostarStreaming.value = true;
  costarAIFeedback.value = "";
  costarStreamText.value = "";
  
  try {
    // 准备发送给API的提示词
    const prompt = generatedCostarPrompt.value;
    console.log("开始执行getCostarAIFeedback请求", prompt);
    
    // 构造请求数据
    const requestData = {
      model: 'deepseek-v3', // 使用火山引擎V3模型
      messages: [
        { role: 'system', content: '你是一个专业的提示词工程师，擅长给出专业的提示词建议。' },
        { role: 'user', content: `请针对以下CO-STAR结构提示词给出改进建议，尤其是如何让这个提示词更加清晰、有效。提示词：${prompt}` }
      ],
      stream: true,
      temperature: 0.7,
      max_tokens: 2000
    };
    
    console.log("请求数据:", JSON.stringify(requestData));
    
    // 使用原生fetch进行请求
    const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    
    // 检查返回的内容类型
    console.log("响应Content-Type:", response.headers.get('Content-Type'));
    
    // 使用原生响应体处理流式数据
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    
    // 使用循环处理流数据
    let buffer = '';
    let accumulatedText = '';
    
    // 处理流数据
    while (true) {
      // 读取一块数据
      const { value, done } = await reader.read();
      
      // 如果读取完毕，退出循环
      if (done) {
        console.log("数据流已结束");
        break;
      }
      
      // 解码二进制数据为文本
      const chunk = decoder.decode(value, { stream: true });
      console.log("收到数据块:", chunk.length, "字节");
      buffer += chunk;
      
      // 按SSE格式解析 (data: xxx\n\n)
      const messages = buffer.split('\n\n');
      buffer = messages.pop() || ''; // 保留最后一部分，可能是不完整的消息
      
      // 处理每条完整消息
      for (const message of messages) {
        // 跳过空消息
        if (!message.trim()) continue;
        
        // 提取data部分
        if (message.startsWith('data: ')) {
          const data = message.substring(6);
          console.log("处理消息:", data.substring(0, 50) + (data.length > 50 ? '...' : ''));
          
          // 处理结束标记
          if (data === '[DONE]') {
            console.log("收到结束标记");
            isCostarStreaming.value = false;
            isCostarLoading.value = false;
            // 确保最终内容被保存
            costarAIFeedback.value = accumulatedText;
            return;
          }
          
          try {
            // 解析JSON数据
            const jsonData = JSON.parse(data);
            
            // 处理错误
            if (jsonData.error) {
              console.error("API错误:", jsonData.error);
              ElMessage.error(jsonData.error.message || '请求出错');
              isCostarStreaming.value = false;
              isCostarLoading.value = false;
              return;
            }
            
            // 处理内容增量
            if (jsonData.choices && 
                jsonData.choices[0].delta && 
                jsonData.choices[0].delta.content) {
              const content = jsonData.choices[0].delta.content;
              console.log("收到内容:", content);
              
              // 累积内容
              accumulatedText += content;
              
              // 使用直接赋值方式完全替换字符串，确保Vue检测到变化
              costarStreamText.value = accumulatedText;
              
              // 强制更新视图（Vue 3中使用nextTick）
              await nextTick();
            }
          } catch (e) {
            console.error("解析JSON失败:", e, data);
          }
        }
      }
    }
    
    // 处理可能的剩余buffer
    if (buffer.trim() && buffer.startsWith('data: ')) {
      const data = buffer.substring(6);
      try {
        const jsonData = JSON.parse(data);
        if (jsonData.choices && 
            jsonData.choices[0].delta && 
            jsonData.choices[0].delta.content) {
          accumulatedText += jsonData.choices[0].delta.content;
          costarStreamText.value = accumulatedText;
          await nextTick();
        }
      } catch (e) {
        console.error("解析剩余JSON失败:", e);
      }
    }
    
    // 结束时更新
    console.log("流处理完成");
    isCostarStreaming.value = false;
    isCostarLoading.value = false;
    costarAIFeedback.value = accumulatedText;
    
  } catch (error) {
    console.error('获取CO-STAR AI建议错误:', error);
    ElMessage.error('获取AI建议出错: ' + error.message);
    isCostarStreaming.value = false;
    isCostarLoading.value = false;
  }
}

async function executeCostarPrompt() {
  if (!isCostarFormComplete.value) return;
  
  isCostarExecuting.value = true;
  isCostarExecutionStreaming.value = true;
  costarExecutionResult.value = "";
  costarExecutionStreamText.value = "";
  
  try {
    // 准备发送给API的提示词
    const prompt = generatedCostarPrompt.value;
    console.log("开始执行executeCostarPrompt请求", prompt);
    
    // 构造请求数据
    const requestData = {
      model: 'deepseek-v3', // 使用火山引擎V3模型
      messages: [
        { role: 'system', content: '你是一个专业的AI助手，请直接回答用户的问题或执行用户的请求。' },
        { role: 'user', content: prompt }
      ],
      stream: true,
      temperature: 0.7,
      max_tokens: 2000
    };
    
    console.log("请求数据:", JSON.stringify(requestData));
    
    // 使用原生fetch进行请求
    const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    
    // 检查返回的内容类型
    console.log("响应Content-Type:", response.headers.get('Content-Type'));
    
    // 使用原生响应体处理流式数据
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    
    // 使用循环处理流数据
    let buffer = '';
    let accumulatedText = '';
    
    // 处理流数据
    while (true) {
      // 读取一块数据
      const { value, done } = await reader.read();
      
      // 如果读取完毕，退出循环
      if (done) {
        console.log("数据流已结束");
        break;
      }
      
      // 解码二进制数据为文本
      const chunk = decoder.decode(value, { stream: true });
      console.log("收到数据块:", chunk.length, "字节");
      buffer += chunk;
      
      // 按SSE格式解析 (data: xxx\n\n)
      const messages = buffer.split('\n\n');
      buffer = messages.pop() || ''; // 保留最后一部分，可能是不完整的消息
      
      // 处理每条完整消息
      for (const message of messages) {
        // 跳过空消息
        if (!message.trim()) continue;
        
        // 提取data部分
        if (message.startsWith('data: ')) {
          const data = message.substring(6);
          console.log("处理消息:", data.substring(0, 50) + (data.length > 50 ? '...' : ''));
          
          // 处理结束标记
          if (data === '[DONE]') {
            console.log("收到结束标记");
            isCostarExecutionStreaming.value = false;
            isCostarExecuting.value = false;
            // 确保最终内容被保存
            costarExecutionResult.value = accumulatedText;
            return;
          }
          
          try {
            // 解析JSON数据
            const jsonData = JSON.parse(data);
            
            // 处理错误
            if (jsonData.error) {
              console.error("API错误:", jsonData.error);
              ElMessage.error(jsonData.error.message || '请求出错');
              isCostarExecutionStreaming.value = false;
              isCostarExecuting.value = false;
              return;
            }
            
            // 处理内容增量
            if (jsonData.choices && 
                jsonData.choices[0].delta && 
                jsonData.choices[0].delta.content) {
              const content = jsonData.choices[0].delta.content;
              console.log("收到内容:", content);
              
              // 累积内容
              accumulatedText += content;
              
              // 使用直接赋值方式完全替换字符串，确保Vue检测到变化
              costarExecutionStreamText.value = accumulatedText;
              
              // 强制更新视图（Vue 3中使用nextTick）
              await nextTick();
            }
          } catch (e) {
            console.error("解析JSON失败:", e, data);
          }
        }
      }
    }
    
    // 处理可能的剩余buffer
    if (buffer.trim() && buffer.startsWith('data: ')) {
      const data = buffer.substring(6);
      try {
        const jsonData = JSON.parse(data);
        if (jsonData.choices && 
            jsonData.choices[0].delta && 
            jsonData.choices[0].delta.content) {
          accumulatedText += jsonData.choices[0].delta.content;
          costarExecutionStreamText.value = accumulatedText;
          await nextTick();
        }
      } catch (e) {
        console.error("解析剩余JSON失败:", e);
      }
    }
    
    // 结束时更新
    console.log("流处理完成");
    isCostarExecutionStreaming.value = false;
    isCostarExecuting.value = false;
    costarExecutionResult.value = accumulatedText;
    
  } catch (error) {
    console.error('执行CO-STAR提示词出错:', error);
    ElMessage.error('执行提示词出错: ' + error.message);
    isCostarExecutionStreaming.value = false;
    isCostarExecuting.value = false;
  }
}

function clearCostarForm() {
  costarForm.context = '';
  costarForm.objective = '';
  costarForm.style = '';
  costarForm.tone = '';
  costarForm.audience = '';
  costarForm.response = '';
  
  nextTick(() => {
    costarAIFeedback.value = '';
    costarExecutionResult.value = '';
    currentCostarStep.value = 1;
  });
}

// 对话框相关函数
function closeResultDialog() {
  nextTick(() => {
    showResultDialog.value = false;
    generatedPrompt.value = '';
  });
}

function showPromptResult(prompt) {
  nextTick(() => {
    generatedPrompt.value = prompt;
    showResultDialog.value = true;
  });
}

function generateSimplePrompt() {
  if (!promptForm.role || !promptForm.action || !promptForm.context) {
    ElMessage.warning('请填写所有必填项');
    return;
  }

  const prompt = `作为${promptForm.role}，${promptForm.action}。${promptForm.context ? '上下文：' + promptForm.context : ''}`;
  nextTick(() => {
    showPromptResult(prompt);
  });
}

function generateRtgoPrompt() {
  if (!rtgoForm.role || !rtgoForm.task || !rtgoForm.goal || !rtgoForm.objective) {
    ElMessage.warning('请填写所有必填项');
    return;
  }

  const prompt = `# 角色(Role)\n${rtgoForm.role}\n\n# 任务(Task)\n${rtgoForm.task}\n\n# 目标(Goal)\n${rtgoForm.goal}\n\n# 输出(Output)\n${rtgoForm.objective}`;
  nextTick(() => {
    showPromptResult(prompt);
  });
}

function generateCostarPrompt() {
  if (!costarForm.context || !costarForm.objective || !costarForm.style || !costarForm.tone || !costarForm.audience || !costarForm.response) {
    ElMessage.warning('请填写所有必填项');
    return;
  }

  const prompt = `# 背景(Context)\n${costarForm.context}\n\n# 目标(Objective)\n${costarForm.objective}\n\n# 风格(Style)\n${costarForm.style}\n\n# 语调(Tone)\n${costarForm.tone}\n\n# 受众(Audience)\n${costarForm.audience}\n\n# 回复格式(Response)\n${costarForm.response}`;
  nextTick(() => {
    showPromptResult(prompt);
  });
}

function copyPrompt() {
  nextTick(() => {
    const promptText = generatedPrompt.value;
    if (promptText) {
      navigator.clipboard.writeText(promptText)
        .then(() => {
          ElMessage.success('提示词已复制到剪贴板');
        })
        .catch(err => {
          console.error('复制失败:', err);
          ElMessage.error('复制失败');
        });
    }
  });
}

// 知识学习相关函数
function showKnowledgeDrawer(type) {
  currentKnowledgeType.value = type;
  knowledgeDrawerVisible.value = true;
}

// 根据知识类型获取对应图标
function getKnowledgeIcon() {
  const iconMap = {
    basic: 'ri-information-line',
    rtgo: 'ri-user-settings-line',
    costar: 'ri-film-line'
  };
  return iconMap[currentKnowledgeType.value] || 'ri-information-line';
}

// Markdown格式化函数
function formatMarkdown(text) {
  if (!text) return '';
  
  // 处理加粗
  let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // 处理斜体
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  // 处理换行
  formatted = formatted.replace(/\n\n/g, '<br><br>');
  
  // 处理列表
  formatted = formatted.replace(/- (.*?)(?:\n|$)/g, '<li>$1</li>');
  formatted = formatted.replace(/<li>/g, '<ul><li>').replace(/<\/li>(?!<li>)/g, '</li></ul>');
  formatted = formatted.replace(/<\/ul><ul>/g, '');
  
  // 处理数字列表
  formatted = formatted.replace(/(\d+)\. (.*?)(?:\n|$)/g, '<li>$1. $2</li>');
  
  return formatted;
}

// 预加载对话框和示例相关资源
onMounted(() => {
  console.log('预加载对话框资源...');
  // 预先初始化对话框状态
  setTimeout(() => {
    // 短暂显示各对话框以触发样式加载，然后立即隐藏
    dialogVisible.value = true;
    rtgoDialogVisible.value = true;
    costarDialogVisible.value = true;
    
    // 立即隐藏
    setTimeout(() => {
      dialogVisible.value = false;
      rtgoDialogVisible.value = false;
      costarDialogVisible.value = false;
    }, 10);
  }, 500);
});
</script>

<style scoped>
/* 样式已迁移到common-components.css */

/* 处理深度选择器问题 */
:deep(.prompt-tabs .el-tabs__header) {
  display: none !important;
}

:deep(.prompt-tabs .el-tabs__content) {
  background-color: white;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 0;
}

:deep(.prompt-tabs .el-tab-pane) {
  padding: 20px;
}

:deep(.el-button--primary) {
  background-color: #ba003f !important;
  border-color: #ba003f !important;
}

:deep(.el-button--primary:hover),
:deep(.el-button--primary:focus) {
  background-color: #cf0046 !important;
  border-color: #cf0046 !important;
}

:deep(.el-button--primary.is-plain) {
  color: #fff !important;
  background-color: rgba(186, 0, 63, 0.9) !important;
  border-color: #ba003f !important;
}

:deep(.el-button--primary.is-plain:hover),
:deep(.el-button--primary.is-plain:focus) {
  background-color: #ba003f !important;
  border-color: #ba003f !important;
}

:deep(.header-with-button .el-button) {
  height: 42px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.prompt-examples-dialog .el-dialog__header) {
  background-color: #ffffff;
  padding: 15px 20px;
  margin-right: 0;
  border-bottom: 1px solid #eaeaea;
}

:deep(.prompt-examples-dialog .el-dialog__title) {
  color: #ba003f;
  font-weight: bold;
  font-size: 18px;
}

:deep(.prompt-examples-dialog .el-dialog__headerbtn) {
  width: 30px;
  height: 30px;
  top: 15px;
  right: 15px;
  background-color: rgba(186, 0, 63, 0.08);
  border-radius: 50%;
  border: 1px solid rgba(186, 0, 63, 0.2);
  transition: all 0.3s;
}

:deep(.prompt-examples-dialog .el-dialog__headerbtn .el-dialog__close) {
  color: #ba003f;
  font-size: 18px;
  font-weight: bold;
}

:deep(.prompt-examples-dialog .el-dialog__headerbtn:hover) {
  background-color: rgba(186, 0, 63, 0.15);
  transform: rotate(90deg);
}

:deep(.prompt-examples-dialog .el-dialog__headerbtn:hover .el-dialog__close) {
  color: #ba003f;
}

:deep(.prompt-examples-dialog .el-dialog__body) {
  padding: 20px;
}

:deep(.el-tabs__content [aria-labelledby*="pane-basic"]) .tab-description {
  background-color: rgba(245, 245, 245, 0.7);
  border-left-color: transparent;
  color: #ba003f;
}

:deep(.el-tabs__content [aria-labelledby*="pane-rtgo"]) .tab-description {
  border-left-color: transparent;
  color: #ba003f;
}

:deep(.el-tabs__content [aria-labelledby*="pane-costar"]) .tab-description {
  border-left-color: transparent;
  color: #ba003f;
}

:deep(.el-tabs__content [aria-labelledby*="pane-basic"]) .section-title::before {
  background-color: #ba003f;
}

:deep(.el-tabs__content [aria-labelledby*="pane-rtgo"]) .section-title::before {
  background-color: #ba003f;
}

:deep(.el-tabs__content [aria-labelledby*="pane-costar"]) .section-title::before {
  background-color: #ba003f;
}

/* 知识按钮样式已移至common-components.css */

/* 添加流式输出样式 */
.streaming-indicator {
  margin-top: 10px;
  display: flex;
  gap: 4px;
  justify-content: center;
}

.streaming-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ba003f;
  animation: dotPulse 1.5s infinite;
}

.streaming-dot:nth-child(2) {
  animation-delay: 0.3s;
}

.streaming-dot:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes dotPulse {
  0%, 100% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
}

/* 添加调试信息和反馈文本样式 */
.debug-info {
  font-family: monospace;
  background-color: #f0f9ff;
  color: #0077cc;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.5;
}

.feedback-text {
  white-space: pre-wrap;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  font-size: 16px;
}

/* 修改反馈文本样式 */
.feedback-text-box {
  white-space: pre-wrap;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 10px;
  font-size: 16px;
  min-height: 100px;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  background-color: #fafafa;
}

.debug-info {
  font-family: monospace;
  background-color: #f0f9ff;
  color: #0077cc;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  font-size: 14px;
  line-height: 1.5;
}

.debug-info p {
  margin: 5px 0;
}

/* 提前加载对话框相关样式，解决首次打开样式问题 */
.prompt-examples-dialog {
  visibility: hidden;
  position: absolute;
  opacity: 0;
  z-index: -1;
}

.prompt-examples-dialog.el-dialog--center {
  visibility: visible;
  position: relative;
  opacity: 1;
  z-index: auto;
}

/* 确保对话框内容在显示时正确加载 */
.example-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.example-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* 添加调试信息和反馈文本样式 */
.debug-info {
  font-family: monospace;
  background-color: #f0f9ff;
  color: #0077cc;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.5;
}

/* 优化对话框样式，确保首次加载正确渲染 */
:deep(.prompt-examples-dialog) {
  display: flex !important;
}

:deep(.prompt-examples-dialog .el-dialog) {
  margin: 0 auto !important;
  max-width: 90% !important;
  max-height: 90vh !important;
  display: flex !important;
  flex-direction: column !important;
}

:deep(.prompt-examples-dialog .el-dialog__body) {
  overflow-y: auto !important;
  padding: 20px !important;
}

/* 修复示例卡片样式 */
:deep(.example-card) {
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  transition: all 0.3s ease !important;
}

:deep(.example-card-header) {
  display: flex !important;
  align-items: center !important;
  margin-bottom: 10px !important;
}

:deep(.example-icon) {
  width: 40px !important;
  height: 40px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 50% !important;
  background-color: rgba(186, 0, 63, 0.1) !important;
  margin-right: 10px !important;
}

:deep(.example-icon i) {
  font-size: 20px !important;
  color: #ba003f !important;
}

:deep(.examples-container) {
  padding: 10px !important;
}
</style>