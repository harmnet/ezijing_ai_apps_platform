<template>
  <div class="prompt-case-container">
    <div class="header">
      <h1 class="main-title">基础对话篇：掌握与AI的高效沟通技巧</h1>
      <p class="sub-title">找到AI时代的人机对话"关键钥匙"，掌握AI黄金对话技巧，养成超出一般人群的基础技能</p>
    </div>

    <div class="content-section">
      <!-- 学习路径导航 -->
      <div class="learning-path-nav">
        <div class="path-nav-item" :class="{ 'active': activePath === 1 }" @click="scrollToSection('self-assessment')">
          <div class="path-number">01</div>
          <div class="path-name">课前思考</div>
        </div>
        <div class="path-nav-item" :class="{ 'active': activePath === 2 }" @click="scrollToSection('basics-section')">
          <div class="path-number">02</div>
          <div class="path-name">提示词基础知识</div>
        </div>
        <div class="path-nav-item" :class="{ 'active': activePath === 3 }" @click="scrollToSection('step-by-step-section')">
          <div class="path-number">03</div>
          <div class="path-name">手把手提示词优化</div>
        </div>
        <div class="path-nav-item" :class="{ 'active': activePath === 4 }" @click="scrollToSection('more-examples-section')">
          <div class="path-number">04</div>
          <div class="path-name">更多对照示例</div>
        </div>
        <div class="path-nav-item" :class="{ 'active': activePath === 5 }" @click="scrollToSection('practice-section')">
          <div class="path-number">05</div>
          <div class="path-name">动手练习</div>
        </div>
        <div class="path-nav-item" :class="{ 'active': activePath === 6 }" @click="scrollToSection('more-knowledge-section')">
          <div class="path-number">06</div>
          <div class="path-name">更多提示词工程知识</div>
        </div>
      </div>
    
      <div class="learning-path-content">
        <!-- 垂直学习路径线 -->
        <div class="learning-path-line"></div>
        
        <!-- 01 课前思考 -->
        <div id="self-assessment" class="self-assessment learning-section" ref="selfAssessment">
          <h2 class="section-title"><span class="section-number">01</span> 课前思考</h2>
          <div class="question-card">
            <div class="question-header">
              <i class="ri-question-line"></i>
              <h3>你平时是怎么与DeepSeek、豆包等大模型对话的？</h3>
            </div>
            <p class="question-desc">在开始学习之前，花一分钟想一想：当你需要让AI完成一项任务时，你是如何描述你的需求的？你的提问方式有什么特点？</p>
            <div class="thought-experiment">
              <div class="prompt-example-header">
                <p>假设你需要让AI<span v-html="promptExamples[currentPromptIndex].text"></span>你会怎么向AI描述这个需求？</p>
                <button @click="changePromptExample" class="change-example-btn">
                  <i class="ri-refresh-line"></i> 换一个
                </button>
              </div>
              <div class="textarea-container">
                <textarea v-model="userPrompt" placeholder="在这里输入你会对AI说的话..." rows="5"></textarea>
                <div class="button-container">
                  <button class="test-ai-btn" @click="testAIResponse" :disabled="isLoading || !userPrompt.trim()">
                    <i class="ri-robot-line"></i> 测试AI返回结果
                  </button>
                </div>
              </div>
              
              <!-- AI响应区域 -->
              <div v-if="showAIResponse" class="ai-response-container">
                <div class="response-header">
                  <div class="model-tag">大模型生成结果</div>
                  <button v-if="aiResponse && !isLoading" class="copy-btn" @click="copyResponseContent" title="复制内容">
                    <i class="ri-file-copy-line"></i>
                  </button>
                </div>
                <div class="response-content" :class="{'streaming': isLoading}" v-html="formattedResponse"></div>
                <div v-if="!isLoading && aiResponse" class="debug-info">
                  <small>状态: {{ showAnalysis ? '已分析' : '未分析' }}</small>
                </div>
                <!-- 分析按钮 -->
                <div v-if="!isLoading && aiResponse && !showAnalysis" class="button-container">
                  <button @click="analyzePrompt" class="test-ai-btn">
                    <i class="ri-file-search-line"></i> 分析提示词
                  </button>
                </div>
              </div>

              <!-- 提示词分析部分 -->
              <div v-if="aiResponse && showAnalysis" class="prompt-analysis">
                <div class="analysis-header">
                  <i class="ri-error-warning-line"></i>
                  <h4>大模型输出内容及提示词分析报告</h4>
                </div>
                <div class="analysis-content">
                  <!-- 分析加载中 -->
                  <div v-if="isAnalyzing && !analysisResponse" class="analysis-loading">
                    <div class="loading-spinner"></div>
                    <p>分析中，请稍候...</p>
                  </div>
                  
                  <!-- 动态分析结果 -->
                  <div v-if="analysisResponse" class="response-content" :class="{'streaming': isAnalyzing}" v-html="formattedAnalysis"></div>

                  <!-- 课前思考结论 -->
                  <div v-if="!isAnalyzing && analysisResponse" class="conclusion-highlight">
                    <div class="conclusion-title">
                      <i class="ri-lightbulb-flash-fill"></i> 课前思考总结
                    </div>
                    <div class="conclusion-content">
                      <div class="expanded-conclusion">
                        <p>
                          <strong>提示词工程</strong>是AI时代的核心技能，正如计算机操作曾是信息时代的基础能力。熟练掌握高效的人机对话技巧，能够大幅提升工作效率，让AI真正成为您的"超级助手"，释放创造力与生产力。
                        </p>
                        <p>
                          在当今AI迅速融入各行各业的背景下，提示词工程不再是技术专家的专利，而是<strong>每个知识工作者的必备素养</strong>。精心设计的提示词就像与AI沟通的"密码"，能够将模糊的需求转化为精准的指令，获取高质量的输出结果。
                        </p>
                        <p>
                          从简单的文案创作到复杂的数据分析，从个人学习辅助到企业级应用开发，掌握提示词技巧的人将在效率和质量上遥遥领先。这不仅是技术工具的使用，更是一种<strong>思维方式的转变</strong>——学会如何清晰、结构化地表达需求，让人机协作达到新的高度。
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 02 提示词基础知识 -->
        <div id="basics-section" class="basics-section learning-section" ref="basicsSection">
          <h2 class="section-title"><span class="section-number">02</span> 提示词基础知识</h2>
          <div class="basics-card">
            <div class="basics-content">
              <h3>什么是提示词工程？</h3>
              <p>提示词工程（Prompt Engineering）是指设计、优化与精炼与AI系统交互时使用的文本指令的过程，旨在获得更准确、更有用的AI回应。</p>
              
              <div class="basics-points">
                <div class="basics-point">
                  <div class="point-icon"><i class="ri-compass-3-line"></i></div>
                  <div class="point-content">
                    <h4>指令与意图</h4>
                    <p>提示词是人类意图的载体，良好的提示词能够清晰传达你的需求和预期，减少AI理解偏差。</p>
                  </div>
                </div>
                
                <div class="basics-point">
                  <div class="point-icon"><i class="ri-tools-fill"></i></div>
                  <div class="point-content">
                    <h4>结构与组成</h4>
                    <p>有效的提示词通常包含明确的任务描述、必要的上下文信息、输出格式要求以及其他约束条件。</p>
                  </div>
                </div>
                
                <div class="basics-point">
                  <div class="point-icon"><i class="ri-magic-line"></i></div>
                  <div class="point-content">
                    <h4>迭代与优化</h4>
                    <p>提示词工程是一个反复优化的过程，通过调整指令、增加细节和改变表达方式来获得更好的结果。</p>
                  </div>
                </div>
              </div>
              
              <div class="learn-more-container">
                <button class="learn-more-btn" @click="showKnowledgeDrawer = true">
                  <i class="ri-book-open-line"></i> 学习提示词工程
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 03 手把手提示词设计优化 -->
        <div id="step-by-step-section" class="step-by-step-section learning-section" ref="stepByStepSection">
          <h2 class="section-title"><span class="section-number">03</span> 手把手提示词设计优化</h2>
          <div class="step-intro">
            <p>让我们一起将你在"课前思考"中的初始提示词逐步优化，通过添加四个关键元素，打造一个结构完整、高效的提示词。</p>
          </div>

          <!-- 步骤导航 -->
          <div class="step-nav">
            <div class="step-nav-item" :class="{ active: currentStep === 1 }" @click="setStep(1)">
              <div class="step-number">1</div>
              <div class="step-name">添加背景</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-nav-item" :class="{ active: currentStep === 2 }" @click="setStep(2)">
              <div class="step-number">2</div>
              <div class="step-name">明确目标</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-nav-item" :class="{ active: currentStep === 3 }" @click="setStep(3)">
              <div class="step-number">3</div>
              <div class="step-name">定义任务</div>
            </div>
            <div class="step-connector"></div>
            <div class="step-nav-item" :class="{ active: currentStep === 4 }" @click="setStep(4)">
              <div class="step-number">4</div>
              <div class="step-name">添加注意事项</div>
            </div>
          </div>

          <!-- 步骤内容区域 -->
          <div class="step-content-container">
            <!-- 步骤1: 添加背景 -->
            <div v-show="currentStep === 1" class="step-content">
              <div class="step-header">
                <h3><i class="ri-information-line"></i> 第一步：添加背景信息</h3>
              </div>
              <div class="step-description">
                <p><strong>为什么需要背景信息？</strong> 大模型需要理解你的处境和上下文，才能生成符合特定情境的内容。背景信息让AI了解你的具体情况，从而提供更贴合实际的回答。</p>
                <div class="example-block">
                  <div class="example-title">示例背景信息</div>
                  <ul>
                    <li>发货延迟的原因（如供应链问题、天气因素）</li>
                    <li>延迟的具体时间（如延迟了几天）</li>
                    <li>客户的重要程度（如是否是VIP客户、合作年限）</li>
                    <li>之前是否已有沟通</li>
                  </ul>
                </div>
              </div>
              
              <div class="prompt-building">
                <div class="current-prompt">
                  <div class="prompt-label">初始提示词</div>
                  <div class="prompt-box" v-if="userPrompt">{{ userPrompt }}</div>
                  <div class="prompt-box empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词
                  </div>
                </div>
                
                <div class="prompt-improvement">
                  <div class="prompt-label-row">
                    <div class="prompt-label">添加背景信息</div>
                    <div class="example-actions">
                      <button @click="useBackgroundExample" class="use-example-btn" title="使用示例背景">
                        <i class="ri-file-copy-line"></i> 使用示例
                      </button>
                      <button @click="clearBackground" class="clear-btn" title="清空内容" v-if="stepPrompts.background">
                        <i class="ri-delete-bin-line"></i> 清空
                      </button>
                    </div>
                  </div>
                  <textarea 
                    v-model="stepPrompts.background" 
                    placeholder="在这里添加背景信息..." 
                    rows="4"
                  ></textarea>
                  <div class="example-hint" v-if="!stepPrompts.background">
                    <i class="ri-lightbulb-flash-line"></i> 
                    <span>点击"使用示例"按钮可以查看和使用示例背景信息</span>
                  </div>
                </div>
              
                <div class="optimized-prompt">
                  <div class="prompt-label">优化后的提示词</div>
                  <div class="prompt-box optimized" v-if="userPrompt">
                    {{ userPrompt }} {{ stepPrompts.background ? stepPrompts.background : "" }}
                  </div>
                  <div class="prompt-box optimized empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词，再进行优化
                  </div>
                </div>
              
                <div class="step-actions">
                  <button @click="setStep(2)" class="next-step-btn" :disabled="!stepPrompts.background">
                    下一步：明确目标 <i class="ri-arrow-right-line"></i>
                  </button>
                </div>
              </div>
              
            </div>
            
            <!-- 步骤2: 明确目标 -->
            <div v-show="currentStep === 2" class="step-content">
              <div class="step-header">
                <h3><i class="ri-target-line"></i> 第二步：明确目标</h3>
              </div>
              <div class="step-description">
                <p><strong>为什么要明确目标？</strong> 告诉AI你想通过这封信达成什么效果，帮助模型理解你的意图和期望结果，使生成的内容更具目的性。</p>
                <div class="example-block">
                  <div class="example-title">目标可能包括</div>
                  <ul>
                    <li>表达诚挚的歉意并维持客户关系</li>
                    <li>希望客户理解并接受延迟</li>
                    <li>挽回客户信任</li>
                    <li>减少客户损失或不满</li>
                  </ul>
                </div>
              </div>
              
              <div class="prompt-building">
                <div class="current-prompt">
                  <div class="prompt-label">当前提示词</div>
                  <div class="prompt-box" v-if="userPrompt">
                    {{ userPrompt }} {{ stepPrompts.background }}
                  </div>
                  <div class="prompt-box empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词
                  </div>
                </div>
                
                <div class="prompt-improvement">
                  <div class="prompt-label-row">
                    <div class="prompt-label">添加目标说明</div>
                    <div class="example-actions">
                      <button @click="useGoalExample" class="use-example-btn" title="使用示例目标">
                        <i class="ri-file-copy-line"></i> 使用示例
                      </button>
                      <button @click="clearGoal" class="clear-btn" title="清空内容" v-if="stepPrompts.goal">
                        <i class="ri-delete-bin-line"></i> 清空
                      </button>
                    </div>
                  </div>
                  <textarea 
                    v-model="stepPrompts.goal" 
                    placeholder="在这里明确你的目标..." 
                    rows="3"
                  ></textarea>
                  <div class="example-hint" v-if="!stepPrompts.goal">
                    <i class="ri-lightbulb-flash-line"></i> 
                    <span>点击"使用示例"按钮可以查看和使用示例目标说明</span>
                  </div>
                </div>
              
                <div class="optimized-prompt">
                  <div class="prompt-label">优化后的提示词</div>
                  <div class="prompt-box optimized" v-if="userPrompt">
                    {{ userPrompt }} {{ stepPrompts.background }} {{ stepPrompts.goal ? stepPrompts.goal : "" }}
                  </div>
                  <div class="prompt-box optimized empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词，再进行优化
                  </div>
                </div>
              
                <div class="step-actions">
                  <button @click="setStep(1)" class="prev-step-btn">
                    <i class="ri-arrow-left-line"></i> 上一步
                  </button>
                  <button @click="setStep(3)" class="next-step-btn" :disabled="!stepPrompts.goal">
                    下一步：定义任务 <i class="ri-arrow-right-line"></i>
                  </button>
                </div>
              </div>
              
            </div>
            
            <!-- 步骤3: 定义任务 -->
            <div v-show="currentStep === 3" class="step-content">
              <div class="step-header">
                <h3><i class="ri-task-line"></i> 第三步：定义具体任务</h3>
              </div>
              <div class="step-description">
                <p><strong>为什么要定义任务？</strong> 具体说明你需要AI完成什么，包括内容类型、格式、风格和长度等要素，确保结果符合你的实际需求。</p>
                <div class="example-block">
                  <div class="example-title">任务定义要素</div>
                  <ul>
                    <li>信件类型和格式（如正式商务信、电子邮件）</li>
                    <li>语气风格（如诚恳、专业、友好）</li>
                    <li>内容部分（如道歉、解释、补偿、下一步行动）</li>
                    <li>字数限制或长度要求</li>
                  </ul>
                </div>
              </div>
              
              <div class="prompt-building">
                <div class="current-prompt">
                  <div class="prompt-label">当前提示词</div>
                  <div class="prompt-box" v-if="userPrompt">
                    {{ userPrompt }} {{ stepPrompts.background }} {{ stepPrompts.goal }}
                  </div>
                  <div class="prompt-box empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词
                  </div>
                </div>
                
                <div class="prompt-improvement">
                  <div class="prompt-label-row">
                    <div class="prompt-label">添加任务定义</div>
                    <div class="example-actions">
                      <button @click="useTaskExample" class="use-example-btn" title="使用示例任务">
                        <i class="ri-file-copy-line"></i> 使用示例
                      </button>
                      <button @click="clearTask" class="clear-btn" title="清空内容" v-if="stepPrompts.task">
                        <i class="ri-delete-bin-line"></i> 清空
                      </button>
                    </div>
                  </div>
                  <textarea 
                    v-model="stepPrompts.task" 
                    placeholder="在这里定义具体任务..." 
                    rows="4"
                  ></textarea>
                  <div class="example-hint" v-if="!stepPrompts.task">
                    <i class="ri-lightbulb-flash-line"></i> 
                    <span>点击"使用示例"按钮可以查看和使用示例任务定义</span>
                  </div>
                </div>
              
                <div class="optimized-prompt">
                  <div class="prompt-label">优化后的提示词</div>
                  <div class="prompt-box optimized" v-if="userPrompt">
                    {{ userPrompt }} {{ stepPrompts.background }} {{ stepPrompts.goal }} {{ stepPrompts.task ? stepPrompts.task : "" }}
                  </div>
                  <div class="prompt-box optimized empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词，再进行优化
                  </div>
                </div>
              
                <div class="step-actions">
                  <button @click="setStep(2)" class="prev-step-btn">
                    <i class="ri-arrow-left-line"></i> 上一步
                  </button>
                  <button @click="setStep(4)" class="next-step-btn" :disabled="!stepPrompts.task">
                    下一步：添加注意事项 <i class="ri-arrow-right-line"></i>
                  </button>
                </div>
              </div>
              
            </div>
            
            <!-- 步骤4: 添加注意事项 -->
            <div v-show="currentStep === 4" class="step-content">
              <div class="step-header">
                <h3><i class="ri-error-warning-line"></i> 第四步：添加注意事项</h3>
              </div>
              <div class="step-description">
                <p><strong>为什么要添加注意事项？</strong> 告诉AI应该避免什么、特别注意什么，帮助模型避开潜在问题，生成更符合预期的内容。</p>
                <div class="example-block">
                  <div class="example-title">常见注意事项</div>
                  <ul>
                    <li>避免过度道歉或显得过于消极</li>
                    <li>不要使用过于技术性的语言解释问题</li>
                    <li>避免承诺无法实现的事情</li>
                    <li>保持简洁，避免冗长</li>
                    <li>确保语气一致</li>
                  </ul>
                </div>
              </div>
              
              <div class="prompt-building">
                <div class="current-prompt">
                  <div class="prompt-label">当前提示词</div>
                  <div class="prompt-box" v-if="userPrompt">
                    {{ userPrompt }} {{ stepPrompts.background }} {{ stepPrompts.goal }} {{ stepPrompts.task }}
                  </div>
                  <div class="prompt-box empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词
                  </div>
                </div>
                
                <div class="prompt-improvement">
                  <div class="prompt-label-row">
                    <div class="prompt-label">添加注意事项</div>
                    <div class="example-actions">
                      <button @click="useCautionsExample" class="use-example-btn" title="使用示例注意事项">
                        <i class="ri-file-copy-line"></i> 使用示例
                      </button>
                      <button @click="clearCautions" class="clear-btn" title="清空内容" v-if="stepPrompts.cautions">
                        <i class="ri-delete-bin-line"></i> 清空
                      </button>
                    </div>
                  </div>
                  <textarea 
                    v-model="stepPrompts.cautions" 
                    placeholder="在这里添加注意事项..." 
                    rows="3"
                  ></textarea>
                  <div class="example-hint" v-if="!stepPrompts.cautions">
                    <i class="ri-lightbulb-flash-line"></i> 
                    <span>点击"使用示例"按钮可以查看和使用示例注意事项</span>
                  </div>
                </div>
              
                <div class="optimized-prompt">
                  <div class="prompt-label">最终优化的完整提示词</div>
                  <div class="prompt-box optimized final" v-if="userPrompt">
                    {{ userPrompt }} {{ stepPrompts.background }} {{ stepPrompts.goal }} {{ stepPrompts.task }} {{ stepPrompts.cautions ? stepPrompts.cautions : "" }}
                  </div>
                  <div class="prompt-box optimized final empty-prompt" v-else>
                    <i class="ri-information-line"></i> 请先在"01 课前思考"部分输入提示词，再进行优化
                  </div>
                  <div class="final-actions">
                    <button class="copy-final-btn" @click="copyFinalPrompt">
                      <i class="ri-file-copy-line"></i> 复制完整提示词
                    </button>
                    <button class="test-final-btn" @click="testFinalPrompt">
                      <i class="ri-robot-line"></i> 测试优化后的提示词
                    </button>
                  </div>
                </div>
              
                <!-- 添加优化提示词响应区域 -->
                <div v-if="showOptimizedResponse" class="ai-response-container optimized-response-container">
                  <div class="response-header">
                    <div class="model-tag">优化提示词的AI生成结果</div>
                    <button v-if="optimizedResponse && !isLoadingOptimized" class="copy-btn" @click="copyOptimizedResponseContent" title="复制内容">
                      <i class="ri-file-copy-line"></i>
                    </button>
                  </div>
                  <div class="response-content" :class="{'streaming': isLoadingOptimized}" v-html="formattedOptimizedResponse"></div>
                </div>
                
                <!-- 添加结果对比视图 -->
                <div v-if="showComparison && aiResponse && optimizedResponse && !isLoadingOptimized && !isLoading" class="comparison-view">
                  <h4 class="comparison-title"><i class="ri-contrast-2-line"></i> 提示词优化效果对比</h4>
                  
                  <div class="comparison-container">
                    <div class="comparison-column">
                      <div class="comparison-header">
                        <h5>原始提示词</h5>
                        <div class="comparison-prompt-text">{{ userPrompt }}</div>
                      </div>
                      <div class="comparison-content" v-html="formattedResponse"></div>
                    </div>
                    
                    <div class="comparison-divider"></div>
                    
                    <div class="comparison-column">
                      <div class="comparison-header">
                        <h5>优化后提示词</h5>
                        <div class="comparison-prompt-text">{{ optimizedPrompt }}</div>
                      </div>
                      <div class="comparison-content" v-html="formattedOptimizedResponse"></div>
                    </div>
                  </div>
                  
                  <div class="comparison-conclusion">
                    <p><strong>对比结论：</strong> 优化后的提示词提供了更清晰的背景信息、明确的目标、具体的任务定义和注意事项，使AI能够生成更符合需求的回复。</p>
                  </div>
                </div>
                
                <div class="step-actions">
                  <button @click="setStep(3)" class="prev-step-btn">
                    <i class="ri-arrow-left-line"></i> 上一步
                  </button>
                  <button @click="resetSteps" class="reset-btn">
                    <i class="ri-restart-line"></i> 重新开始
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 04 更多对照示例 -->
        <div id="more-examples-section" class="more-examples-section learning-section" ref="moreExamplesSection">
          <h2 class="section-title"><span class="section-number">04</span> 更多对照示例</h2>
          <p class="section-desc">以下是不同行业和场景下的提示词对比示例，展示了如何通过添加背景、目标、任务和注意事项，将简单提示词优化为高效提示词。</p>
          
          <!-- 示例滑块控制 -->
          <div class="examples-navigation">
            <button 
              v-for="(example, index) in moreExamples" 
              :key="index"
              @click="setCurrentExample(index)"
              :class="['example-nav-btn', {'active': currentExampleIndex === index}]"
            >
              示例{{ index + 1 }}：{{ example.title }}
            </button>
          </div>
          
          <!-- 示例展示区域 -->
          <div class="example-showcase">
            <div class="example-columns">
              <!-- 弱提示词列 -->
              <div class="example-column weak-column">
                <div class="example-header">
                  <i class="ri-error-warning-line"></i>
                  <h3>弱提示词</h3>
                </div>
                <div class="example-content">
                  <p>{{ moreExamples[currentExampleIndex].weak }}</p>
                </div>
                <div class="example-analysis">
                  <h4>问题分析</h4>
                  <ul>
                    <li v-for="(issue, i) in moreExamples[currentExampleIndex].issues" :key="i">
                      {{ issue }}
                    </li>
                  </ul>
                </div>
              </div>
              
              <!-- 更好提示词列 -->
              <div class="example-column better-column">
                <div class="example-header">
                  <i class="ri-flashlight-line"></i>
                  <h3>更好的提示词</h3>
                </div>
                <div class="example-content">
                  <div class="better-prompt-structure">
                    <!-- 背景部分 -->
                    <div class="prompt-structure-item">
                      <div class="structure-label">背景信息：</div>
                      <div class="structure-content">{{ moreExamples[currentExampleIndex].better.background }}</div>
                    </div>
                    
                    <!-- 目标部分 -->
                    <div class="prompt-structure-item">
                      <div class="structure-label">目标：</div>
                      <div class="structure-content">{{ moreExamples[currentExampleIndex].better.goal }}</div>
                    </div>
                    
                    <!-- 任务部分 -->
                    <div class="prompt-structure-item">
                      <div class="structure-label">任务：</div>
                      <div class="structure-content">{{ moreExamples[currentExampleIndex].better.task }}</div>
                    </div>
                    
                    <!-- 注意事项部分 -->
                    <div class="prompt-structure-item">
                      <div class="structure-label">注意事项：</div>
                      <div class="structure-content">{{ moreExamples[currentExampleIndex].better.cautions }}</div>
                    </div>
                  </div>
                </div>
                <div class="example-benefits">
                  <h4>优势分析</h4>
                  <ul>
                    <li v-for="(benefit, i) in moreExamples[currentExampleIndex].benefits" :key="i">
                      {{ benefit }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            
            <!-- 示例行业场景说明 -->
            <div class="example-context">
              <p><strong>行业场景：</strong> {{ moreExamples[currentExampleIndex].context }}</p>
            </div>
          </div>
        </div>

        <!-- 05 现在轮到你来练习 -->
        <div id="practice-section" class="practice-section learning-section" ref="practiceSection">
          <h2 class="section-title"><span class="section-number">05</span> 现在轮到你来练习</h2>
          <p>尝试下面这个任务，看看你能否写出有效的提示词：</p>
          
          <div class="challenge-card">
            <h3>挑战任务：工作周报撰写</h3>
            <p>假设你需要AI帮你撰写一份本周工作总结，包含项目进展、遇到的挑战和下周计划等内容。</p>
            
            <div class="textarea-container">
              <textarea v-model="practicePrompt" placeholder="编写你的提示词..." rows="6"></textarea>
              <div class="button-container">
                <button class="execute-prompt-btn" @click="executePracticePrompt" :disabled="isLoadingPractice || !practicePrompt.trim()">
                  <i class="ri-robot-line"></i> 执行提示词
                </button>
              </div>
            </div>
            
            <!-- 练习响应区域 -->
            <div class="practice-response-area" v-if="showPracticeResponse || isLoadingPractice">
              <div class="response-header">
                <h4>AI 响应结果</h4>
                <div class="loading-indicator" v-if="isLoadingPractice">
                  <div class="dot-flashing"></div>
                </div>
              </div>
              <div class="response-content" v-html="formattedPracticeResponse"></div>
            </div>
          </div>
        </div>
        
        <!-- 06 更多提示词工程知识 -->
        <div id="more-knowledge-section" class="more-knowledge-section learning-section" ref="moreKnowledgeSection">
          <h2 class="section-title"><span class="section-number">06</span> 更多提示词工程知识</h2>
          <p class="section-desc">想要深入学习提示词工程？我们为您准备了更多专业知识和实用技巧。</p>
          
          <div class="knowledge-action">
            <a href="/prompt-engineering" target="_blank" class="more-knowledge-btn">
              <i class="ri-book-open-line"></i> 点击学习更多提示词工程知识
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- 知识抽屉弹窗 -->
  <el-drawer
    v-model="showKnowledgeDrawer"
    title="提示词工程知识"
    direction="rtl"
    size="30%"
  >
    <div class="knowledge-drawer-content">
      <h3>什么是提示词工程？</h3>
      <p>提示词工程（Prompt Engineering）是设计、优化与精炼与AI系统交互时使用的文本指令的过程，旨在获得更准确、更有用的AI回应。掌握提示词工程，就像学会了与AI沟通的"母语"，能够大幅提升人机协作效率。</p>
      
      <h3>基础知识要点</h3>
      <div class="knowledge-points">
        <div class="knowledge-point">
          <div class="point-icon"><i class="ri-number-1"></i></div>
          <div class="point-content">
            <h4>清晰性与精确性</h4>
            <p>提示词应该清晰、明确，避免模糊或歧义的表达，让AI准确理解你的需求。例如，不要说"写一些关于气候的内容"，而应该说"写一篇800字的关于气候变化对农业影响的科普文章"。</p>
          </div>
        </div>
        
        <div class="knowledge-point">
          <div class="point-icon"><i class="ri-number-2"></i></div>
          <div class="point-content">
            <h4>提供足够上下文</h4>
            <p>包含必要的背景信息和约束条件，帮助AI生成符合特定情境的回答。比如说明目标受众、使用场景、已有的相关信息等，这些都能大幅提高AI输出的相关性。</p>
          </div>
        </div>
        
        <div class="knowledge-point">
          <div class="point-icon"><i class="ri-number-3"></i></div>
          <div class="point-content">
            <h4>迭代式改进</h4>
            <p>提示词工程通常需要多次尝试和微调，根据AI的回应不断优化提示词。将第一次回答的内容作为反馈，再次指导AI进行修改、扩展或改进，能够获得更高质量的结果。</p>
          </div>
        </div>
        
        <div class="knowledge-point">
          <div class="point-icon"><i class="ri-number-4"></i></div>
          <div class="point-content">
            <h4>结构化与模板化</h4>
            <p>使用结构化的模板（如本课程中的四步法）可以大幅提高提示词的有效性。通过统一、有条理的格式组织你的需求，帮助AI更系统化地处理和响应。</p>
          </div>
        </div>
      </div>
      
      <h3>进阶技巧</h3>
      <div class="advanced-tips">
        <div class="tip-item">
          <i class="ri-lightbulb-flash-line"></i>
          <p><strong>角色引导：</strong>让AI扮演特定角色（如"作为一名经验丰富的营销专家"）可增强回答质量。这种方法能让AI从特定专业视角出发，提供更有针对性的建议。</p>
        </div>
        
        <div class="tip-item">
          <i class="ri-lightbulb-flash-line"></i>
          <p><strong>示例演示：</strong>在提示词中提供示例，展示你期望的输出格式和风格。例如："请生成三个产品描述，格式如下：[产品名称] - [一句话亮点] - [详细说明]"。</p>
        </div>
        
        <div class="tip-item">
          <i class="ri-lightbulb-flash-line"></i>
          <p><strong>思维链：</strong>要求AI"一步步思考"，可获得更有逻辑性的解答。例如："请一步步分析这个数学问题，先列出已知条件，然后说明解题思路，最后得出结论。"</p>
        </div>
        
        <div class="tip-item">
          <i class="ri-lightbulb-flash-line"></i>
          <p><strong>负面指导：</strong>明确告诉AI不要做什么，避免不必要的解释或偏离主题。例如："请直接给出步骤，不需要解释为什么这样做。"或"回答中不要包含背景历史介绍。"</p>
        </div>
      </div>
      
      <h3>常用提示词模板</h3>
      <div class="template-section">
        <div class="template-item">
          <h4>专家角色模板</h4>
          <div class="template-content">
            你是[专家身份]，拥有[相关经验/背景]。请针对[具体问题/任务]提供专业意见。回答需要包含[具体要求]，并考虑到[限制条件]。
          </div>
        </div>
        
        <div class="template-item">
          <h4>内容创作模板</h4>
          <div class="template-content">
            请以[风格/语气]的方式，创作一篇关于[主题]的[内容类型]。目标受众是[受众描述]，长度约[字数]字。需要强调[关键点]，并包含[特定元素]。避免[不需要的内容]。
          </div>
        </div>
        
        <div class="template-item">
          <h4>问题解析模板</h4>
          <div class="template-content">
            请帮我分析以下[问题类型]：[具体问题描述]。请从[角度1]、[角度2]和[角度3]三个方面进行分析，并在每个分析后提供可行的解决方案。最后总结最优选择。
          </div>
        </div>
      </div>
      
      <h3>提示词优化对比示例</h3>
      <div class="example-comparison">
        <div class="weak-example">
          <h4>弱提示词</h4>
          <p>写一篇关于人工智能的文章</p>
        </div>
        <div class="better-example">
          <h4>优化后的提示词</h4>
          <p>请以科技记者的身份，撰写一篇面向普通大众的关于人工智能在医疗领域应用的科普文章。文章应约1000字，使用通俗易懂的语言解释AI如何帮助诊断疾病、开发新药和提高医疗效率。请包含2-3个真实案例，并在结尾讨论伦理考量。避免使用过多技术术语，重点放在实际影响和未来前景上。</p>
        </div>
      </div>
      
    </div>
  </el-drawer>
</template>

<script>
export default {
  name: 'PromptCase',
  metaInfo: {
    title: '提示词工程学习'
  },
  data() {
    return {
      showTips: false,
      userPrompt: '',
      aiResponse: '',
      analysisResponse: '',
      isLoading: false,
      showAIResponse: false,
      errorMessage: '',
      showAnalysis: false,
      optimizedPrompt: '',      // 存储优化后的完整提示词
      optimizedResponse: '',    // 存储优化后提示词的AI回复
      isLoadingOptimized: false, // 优化提示词的加载状态
      showOptimizedResponse: false, // 是否显示优化后的响应
      showComparison: false,    // 是否显示对比视图
      
      promptAnalysis: {
        isSimple: false,
        tooShort: false,
        noContext: false,
        noStyle: false,
        noStructure: false,
        noSpecifics: false
      },
      isAnalyzing: false,
      analysisResult: null,
      currentPromptIndex: 0,
      promptExamples: [
        {
          text: '帮你写一份<strong>给客户的道歉信</strong>，说明产品发货延迟的原因。'
        },
        {
          text: '帮你写一篇<strong>产品发布会的演讲稿</strong>，介绍一款新型智能手表。'
        },
        {
          text: '帮你制作<strong>一份社交媒体营销计划</strong>，针对小型咖啡馆的线上推广。'
        },
        {
          text: '帮你写一封<strong>求职申请邮件</strong>，应聘软件开发工程师职位。'
        },
        {
          text: '帮你起草<strong>一份商业合作提案</strong>，寻求潜在投资者的支持。'
        },
        {
          text: '帮你写一份<strong>周报总结</strong>，突出项目进展和遇到的挑战。'
        },
        {
          text: '帮你制作<strong>一份市场调研问卷</strong>，收集用户对新产品的反馈。'
        },
        {
          text: '帮你写一份<strong>租房协议</strong>，明确房东与租客的权利和义务。'
        },
        {
          text: '帮你创建<strong>一个健康饮食计划</strong>，适合忙碌的上班族每周参考。'
        },
        {
          text: '帮你编写<strong>一份活动策划书</strong>，为公司年会设计主题和流程。'
        }
      ],
      currentStep: 1,
      stepPrompts: {
        background: '',
        goal: '',
        task: '',
        cautions: ''
      },
      // 添加背景信息示例
      backgroundExample: '我们是一家电子产品公司，由于供应链中断问题，我们的一批高端耳机产品发货延迟了5天。这批订单是给一位已合作3年的VIP客户，年采购额超过10万元。',
      // 添加其他步骤的示例文本
      goalExample: '我希望通过这封信表达诚挚的歉意，挽回客户的信任，并确保他们继续与我们保持长期合作关系。',
      taskExample: '请以公司客户服务部门的名义，写一封正式的道歉信。语气要诚恳但专业，不超过300字。包含道歉、解释原因、提供补偿方案（10%的折扣）和新的发货日期（下周二），以及未来如何改进的承诺。',
      cautionsExample: '请避免过度道歉或表现得太过消极，保持专业和积极的态度。不要使用太多技术术语解释延迟原因。信中要强调我们重视与客户的长期关系，而不只是这一次订单。',
      finalPrompt: '',
      copySuccess: false,
      
      // 添加更多对照示例数据
      currentExampleIndex: 0,
      moreExamples: [
        {
          title: "市场研究报告",
          weak: "分析电动汽车市场",
          issues: [
            "太过笼统，没有明确研究范围",
            "未指定报告格式和深度",
            "缺少相关数据或信息来源要求",
            "没有指明分析维度和关注点",
            "未说明研究目的和受众"
          ],
          better: {
            background: "我是一家投资公司的分析师，需要为考虑投资电动汽车行业的客户提供参考。当前电动汽车市场正经历快速变化，特斯拉、比亚迪等主要竞争者不断推出新车型，各国政府也在调整补贴政策。",
            goal: "目标是提供一份全面但精炼的市场分析，帮助客户了解电动汽车行业的投资机会与风险，作为投资决策的参考依据。",
            task: "请创建一份2000字左右的电动汽车市场分析报告，包括：1)市场规模与增长预测(2023-2025年)；2)主要厂商市场份额对比；3)消费者购买趋势分析；4)政策环境影响；5)投资机会与风险评估。请使用专业但易于理解的语言，包含数据支持的图表描述，并在结论部分提供投资建议。",
            cautions: "避免过度技术细节；保持客观中立的分析态度；不要只关注特斯拉等知名企业；考虑不同地区市场的差异性；明确标注数据来源可能需要更新的部分。"
          },
          benefits: [
            "明确了分析背景与目的，使AI了解报告意图",
            "指定了具体分析维度和报告结构",
            "设定了合理的内容长度和专业度要求",
            "提供了清晰的受众信息，帮助调整内容风格",
            "注意事项确保了分析的全面性和实用性"
          ],
          context: "投资分析和市场研究领域，针对需要了解新兴市场机会的投资者或企业决策者。"
        },
        {
          title: "技术文档编写",
          weak: "写一个React组件的文档",
          issues: [
            "未指明具体是什么组件",
            "没有提供任何组件的属性和功能信息",
            "未说明文档的受众和技术水平",
            "没有规定文档的结构和格式",
            "缺少对预期使用场景的描述"
          ],
          better: {
            background: "我们团队开发了一个名为DateRangePicker的React组件，用于在管理系统中选择日期范围。该组件支持多种日期格式、自定义节假日显示、预设范围选择等功能，主要面向中级以上的React开发者。",
            goal: "创建一份清晰、全面的技术文档，使其他开发者能够快速理解并正确实现这个组件，减少集成问题和支持请求。",
            task: "请编写一份DateRangePicker组件的技术文档，包含以下部分：1)组件概述和使用场景；2)安装和基本用法示例；3)完整的属性(props)API表格，包含类型、默认值和说明；4)高级用法示例（如自定义格式、禁用特定日期等）；5)事件处理；6)与表单库集成方法；7)常见问题解答。使用Markdown格式，并包含可复制的代码示例。",
            cautions: "代码示例必须是有效且完整的；避免过于简化而忽略错误处理；不要假设读者熟悉我们的其他组件；使用一致的命名和格式；包含性能注意事项；避免使用过时的React模式。"
          },
          benefits: [
            "提供了组件的具体信息和技术背景",
            "明确了文档的目标受众和技术水平",
            "详细规定了文档结构和必要内容",
            "指定了文档格式（Markdown）和内容要求",
            "通过注意事项确保了文档的实用性和完整性"
          ],
          context: "软件开发领域，为开源或企业内部的技术组件创建开发者文档。"
        },
        {
          title: "医疗健康建议",
          weak: "写一篇关于糖尿病管理的文章",
          issues: [
            "未指明针对的糖尿病类型",
            "没有明确文章的受众群体",
            "缺乏内容的专业程度要求",
            "未说明文章目的和长度",
            "没有提及需要包含的关键信息"
          ],
          better: {
            background: "我是一名社区健康教育工作者，负责为新确诊的2型糖尿病患者（多为50岁以上的非医学背景人士）提供健康管理指导。许多患者对疾病认识有限，不了解日常管理对控制病情的重要性。",
            goal: "创建一份易于理解且实用的指南，帮助患者建立日常糖尿病管理的正确认识，鼓励他们采取积极的自我管理措施，提高生活质量并减少并发症风险。",
            task: "请撰写一篇1500字左右的《2型糖尿病日常管理指南》，使用平易近人但准确的语言，避免过多专业术语。内容应包括：1)2型糖尿病基础知识简介；2)血糖监测方法和频率指导；3)饮食管理原则和实例；4)适合2型糖尿病患者的运动建议；5)药物管理注意事项；6)如何识别和处理低血糖状况；7)定期医疗随访的重要性。",
            cautions: "不要使用过多医学术语；避免过于笼统的建议，提供具体可行的步骤；不要引起不必要的恐慌；明确标注哪些情况需要立即就医；避免推荐特定品牌的药物或设备；提醒内容仅供参考，不能替代医生的个性化建议。"
          },
          benefits: [
            "明确了目标受众（新确诊2型糖尿病的非医学背景人士）",
            "提供了患者群体的具体背景和需求",
            "详细规定了内容框架和表达方式要求",
            "强调了实用性和可操作性的重要性",
            "通过注意事项确保了内容的医学安全性"
          ],
          context: "医疗健康教育领域，为特定患者群体提供疾病管理的科普和指导。"
        },
        {
          title: "教育课程设计",
          weak: "设计一个编程入门课程",
          issues: [
            "未指明针对的学习者年龄和背景",
            "没有明确编程语言和工具",
            "缺乏课程目标和学习成果说明",
            "未提及课程时长和结构安排",
            "没有说明教学方法和评估要求"
          ],
          better: {
            background: "我在一所高中教授选修课程，学生是16-18岁对编程感兴趣但没有任何编程经验的高中生。学校计算机实验室配有Windows电脑，我们有10周时间（每周两节45分钟的课）来完成这门入门课程。学生表达了对游戏开发和网站制作的兴趣。",
            goal: "设计一个引人入胜的Python编程入门课程，在激发学生学习兴趣的同时，帮助他们建立编程思维，掌握基础编程技能，并能够独立完成简单的项目，为将来的进阶学习打下基础。",
            task: "请创建一个10周的高中Python编程入门课程大纲，包括：1)每周的主题、学习目标和课程内容概述；2)课堂练习和作业设计；3)一个贯穿课程的项目式学习活动（如简单游戏或网站）；4)需要使用的工具和资源（偏好免费开源工具）；5)课程评估方法（如小测验、项目展示等）；6)每单元教学建议，包括可能的难点和解决方案。",
            cautions: "避免过于理论化的内容；确保每次课都有动手实践环节；不要假设学生有任何编程基础；考虑到学生的注意力持续时间设计活动；课程进度要循序渐进；包含团队协作的机会；注意项目难度的设置，确保在课程时间内可完成。"
          },
          benefits: [
            "明确了学习者的年龄、背景和兴趣",
            "提供了具体的教学环境和时间限制信息",
            "指定了编程语言(Python)和教学方向",
            "详细说明了课程结构和评估需求",
            "通过注意事项确保了课程的可行性和有效性"
          ],
          context: "教育培训领域，为特定学习者群体设计编程或其他技能的教学课程。"
        }
      ],
      practicePrompt: '',
      practiceResponse: '',
      isLoadingPractice: false,
      showPracticeResponse: false,
      showKnowledgeDrawer: false, // 添加抽屉弹窗状态变量
      activePath: 1,
    }
  },
  computed: {
    formattedResponse() {
      if (!this.aiResponse) return '';
      
      // 格式化AI响应内容
      const contentStr = String(this.aiResponse);
      
      // 处理markdown格式
      let formattedContent = contentStr
        .replace(/\n/g, '<br>') // 换行符转为HTML的<br>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **粗体**
        .replace(/\*(.*?)\*/g, '<em>$1</em>'); // *斜体*
        
      // 高亮代码块
      formattedContent = formattedContent.replace(
        /```([\s\S]*?)```/g, 
        '<pre><code>$1</code></pre>'
      );
      
      // 高亮行内代码
      formattedContent = formattedContent.replace(
        /`([^`]+)`/g, 
        '<code>$1</code>'
      );
      
      return formattedContent;
    },
    formattedAnalysis() {
      if (!this.analysisResponse) return '';
      
      // 格式化分析响应内容
      let contentStr = String(this.analysisResponse);
      
      // 移除markdown标记或提示
      contentStr = contentStr.replace(/```markdown/gi, '');
      contentStr = contentStr.replace(/```/g, '');
      contentStr = contentStr.replace(/markdown格式[:：]?/gi, '');
      
      // 处理markdown格式
      let formattedContent = contentStr
        .replace(/\n/g, '<br>') // 换行符转为HTML的<br>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **粗体**
        .replace(/\*(.*?)\*/g, '<em>$1</em>'); // *斜体*
        
      // 高亮行内代码
      formattedContent = formattedContent.replace(
        /`([^`]+)`/g, 
        '<code>$1</code>'
      );
      
      return formattedContent;
    },
    formattedOptimizedResponse() {
      if (!this.optimizedResponse) return '';
      
      // 格式化优化后的AI响应内容
      const contentStr = String(this.optimizedResponse);
      
      // 处理markdown格式
      let formattedContent = contentStr
        .replace(/\n/g, '<br>') // 换行符转为HTML的<br>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **粗体**
        .replace(/\*(.*?)\*/g, '<em>$1</em>'); // *斜体*
        
      // 高亮代码块
      formattedContent = formattedContent.replace(
        /```([\s\S]*?)```/g, 
        '<pre><code>$1</code></pre>'
      );
      
      // 高亮行内代码
      formattedContent = formattedContent.replace(
        /`([^`]+)`/g, 
        '<code>$1</code>'
      );
      
      return formattedContent;
    },
    formattedPracticeResponse() {
      if (!this.practiceResponse) return '';
      
      // 格式化练习响应内容
      const contentStr = String(this.practiceResponse);
      
      // 处理markdown格式
      let formattedContent = contentStr
        .replace(/\n/g, '<br>') // 换行符转为HTML的<br>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **粗体**
        .replace(/\*(.*?)\*/g, '<em>$1</em>'); // *斜体*
        
      // 高亮代码块
      formattedContent = formattedContent.replace(
        /```([\s\S]*?)```/g, 
        '<pre><code>$1</code></pre>'
      );
      
      return formattedContent;
    },
  },
  methods: {
    // 切换提示词示例
    changePromptExample() {
      this.currentPromptIndex = (this.currentPromptIndex + 1) % this.promptExamples.length;
    },
    
    // 设置当前步骤
    setStep(step) {
      this.currentStep = step;
    },
    
    // 重置所有步骤
    resetSteps() {
      this.currentStep = 1;
      this.stepPrompts = {
        background: '',
        goal: '',
        task: '',
        cautions: ''
      };
    },
    
    // 复制最终优化的提示词
    copyFinalPrompt() {
      if (!this.userPrompt) {
        alert('请先在"01 课前思考"部分输入提示词');
        return;
      }
      const finalPrompt = `${this.userPrompt} ${this.stepPrompts.background} ${this.stepPrompts.goal} ${this.stepPrompts.task} ${this.stepPrompts.cautions}`.trim();
      // 更安全的判断方式
      if (
        typeof navigator !== 'undefined' &&
        navigator.clipboard &&
        typeof navigator.clipboard.writeText === 'function'
      ) {
        navigator.clipboard.writeText(finalPrompt)
          .then(() => {
            this.copySuccess = true;
            setTimeout(() => {
              this.copySuccess = false;
            }, 2000);
          })
          .catch(err => {
            console.error('复制失败:', err);
            this.fallbackCopy(finalPrompt);
          });
      } else {
        this.fallbackCopy(finalPrompt);
      }
    },
    // 降级处理方法
    fallbackCopy(text) {
      try {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        const successful = document.execCommand('copy');
        document.body.removeChild(textarea);
        if (successful) {
          this.copySuccess = true;
          setTimeout(() => {
            this.copySuccess = false;
          }, 2000);
        } else {
          alert('复制失败，请手动复制');
        }
      } catch (err) {
        alert('复制失败，请手动复制');
      }
    },
    
    // 测试最终优化的提示词
    testFinalPrompt() {
      if (!this.userPrompt) {
        alert('请先在"01 课前思考"部分输入提示词');
        return;
      }
      
      const finalPrompt = `${this.userPrompt} ${this.stepPrompts.background} ${this.stepPrompts.goal} ${this.stepPrompts.task} ${this.stepPrompts.cautions}`.trim();
      this.optimizedPrompt = finalPrompt; // 保存优化后的提示词
      
      // 执行API请求获取优化提示词的结果
      this.getOptimizedAIResponse(finalPrompt);
    },
    
    // 添加新方法来获取优化提示词的AI响应
    async getOptimizedAIResponse(prompt) {
      if (!prompt.trim() || this.isLoadingOptimized) return;
      
      this.isLoadingOptimized = true;
      this.showOptimizedResponse = true;
      this.optimizedResponse = ''; // 清空之前的响应
      this.errorMessage = '';
      
      // 如果同时存在初始响应和优化响应，则显示对比视图
      if (this.aiResponse && this.showAIResponse) {
        this.showComparison = true;
      }
      
      try {
        // 准备API请求参数
        const requestData = {
          model: 'deepseek-v3', // 默认使用DeepSeek-V3模型
          messages: [{ role: 'user', content: prompt.trim() }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };

        // 发送请求到后端API
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
          throw new Error(`HTTP错误 ${response.status}`);
        }

        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 读取数据流
        const readStream = async () => {
          try {
            while (true) {
              const { value, done } = await reader.read();
              
              if (done) {
                console.log("优化提示词流读取完成");
                this.isLoadingOptimized = false;
                break;
              }
              
              // 解码并处理新数据
              buffer += decoder.decode(value, { stream: true });
              
              // 处理SSE数据
              const lines = buffer.split('\n\n');
              buffer = lines.pop() || '';
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const dataStr = line.slice(6);
                  
                  // 处理结束标记
                  if (dataStr === '[DONE]') {
                    this.isLoadingOptimized = false;
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理错误消息
                    if (data.error) {
                      this.errorMessage = data.error.message || '请求出错';
                      this.isLoadingOptimized = false;
                      return;
                    }
                    
                    // 处理内容增量
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      this.optimizedResponse += deltaContent;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.errorMessage = '读取响应出错';
            this.isLoadingOptimized = false;
          }
        };
        
        // 开始读取流
        readStream();
        
      } catch (error) {
        console.error("请求出错:", error);
        this.errorMessage = error.message || '请求出错';
        this.isLoadingOptimized = false;
      }
    },
    
    // 添加复制优化响应内容的方法
    copyOptimizedResponseContent() {
      if (!this.optimizedResponse) return;
      
      // 使用剪贴板API复制文本
      navigator.clipboard.writeText(this.optimizedResponse)
        .then(() => {
          this.showCopySuccess();
        })
        .catch(err => {
          console.error('复制失败:', err);
        });
    },
    
    toggleTips() {
      this.showTips = !this.showTips
    },
    
    // 测试AI响应
    async testAIResponse() {
      if (!this.userPrompt.trim() || this.isLoading) return;
      
      this.isLoading = true;
      this.showAIResponse = true;
      this.aiResponse = ''; // 清空之前的响应
      this.errorMessage = '';
      this.showAnalysis = false; // 重置分析状态
      
      try {
        // 准备API请求参数
        const requestData = {
          model: 'deepseek-v3', // 默认使用DeepSeek-V3模型
          messages: [{ role: 'user', content: this.userPrompt.trim() }],
          stream: true,
          temperature: 0.7,
          max_tokens: 2000
        };

        // 发送请求到后端API
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
          throw new Error(`HTTP错误 ${response.status}`);
        }

        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 读取数据流
        const readStream = async () => {
          try {
            while (true) {
              const { value, done } = await reader.read();
              
              if (done) {
                console.log("流读取完成");
                this.isLoading = false;
                break;
              }
              
              // 解码并处理新数据
              buffer += decoder.decode(value, { stream: true });
              
              // 处理SSE数据
              const lines = buffer.split('\n\n');
              buffer = lines.pop() || '';
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const dataStr = line.slice(6);
                  
                  // 处理结束标记
                  if (dataStr === '[DONE]') {
                    this.isLoading = false;
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理错误消息
                    if (data.error) {
                      this.errorMessage = data.error.message || '请求出错';
                      this.isLoading = false;
                      return;
                    }
                    
                    // 处理内容增量
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      this.aiResponse += deltaContent;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.errorMessage = '读取响应出错';
            this.isLoading = false;
          }
        };
        
        // 开始读取流
        readStream();
        
      } catch (error) {
        console.error("请求出错:", error);
        this.errorMessage = error.message || '请求出错';
        this.isLoading = false;
      }
    },
    
    // 复制响应内容
    copyResponseContent() {
      if (!this.aiResponse) return;
      
      // 如果navigator.clipboard可用（安全上下文如HTTPS或localhost）
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(this.aiResponse)
          .then(() => {
            this.showCopySuccess();
          })
          .catch(err => {
            console.error('使用clipboard API复制失败，尝试后备方法:', err);
            this.fallbackCopy(this.aiResponse);
          });
      } else {
        // 后备复制方法
        this.fallbackCopy(this.aiResponse);
      }
    },
    
    // 后备复制方法（使用传统的DOM选择和execCommand方法）
    fallbackCopy(text) {
      try {
        // 创建临时textarea元素
        const textarea = document.createElement('textarea');
        textarea.value = text;
        
        // 设置样式使其不可见
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        textarea.style.pointerEvents = 'none';
        
        // 添加到DOM并选中内容
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        
        // 执行复制命令
        const successful = document.execCommand('copy');
        
        // 移除临时元素
        document.body.removeChild(textarea);
        
        if (successful) {
          this.showCopySuccess();
        } else {
          console.error('后备复制方法失败');
        }
      } catch (err) {
        console.error('复制失败:', err);
      }
    },
    
    // 显示复制成功提示
    showCopySuccess() {
      // 创建一个临时的提示元素
      const toast = document.createElement('div');
      toast.className = 'copy-toast';
      toast.innerText = '已复制';
      document.body.appendChild(toast);
      
      // 动画显示后删除
      setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
          toast.classList.remove('show');
          setTimeout(() => {
            document.body.removeChild(toast);
          }, 300);
        }, 1500);
      }, 10);
    },

    // 添加提示词分析方法
    analyzePrompt() {
      if (this.isAnalyzing || !this.userPrompt.trim() || !this.aiResponse) return;
      
      this.isAnalyzing = true;
      this.showAnalysis = true;
      this.analysisResponse = ''; // 清空之前的分析结果
      
      try {
        // 构造分析提示词，让大模型分析用户提示词和AI回复
        const analysisPrompt = `你是一位专业的提示词工程与AI输出分析专家。请对以下用户提示词和AI回复进行严格评估和分析。

用户的原始提示词:
"""
${this.userPrompt.trim()}
"""

AI的回复内容:
"""
${this.aiResponse}
"""

请提供详细分析，包括两个主要部分：

1. AI输出内容分析：
   - 总体评价：说明AI输出是不准确的半成品，需要用户进一步打磨和修改
   - 列出5个具体问题：内容针对性不足、格式结构不规范、语气表达不恰当、关键信息不完整或不准确、需要大量人工修改等

2. 提示词分析：
   - 总体评价：说明提示词不够精确，缺乏明确指导和关键信息
   - 列出5个具体问题：任务描述不清晰、缺少必要背景信息、没有指定风格要求、缺少具体细节、没有提供结构化指导等

最后，总结提示词质量与AI输出质量的关系，强调简单提示词往往得到需要大量修改的半成品。

请使用markdown格式进行回复，加粗重要结论。不要提供具体的改进建议，只需指出问题。`;

        // 准备API请求参数，与testAIResponse()方法类似
        const requestData = {
          model: 'deepseek-v3', // 使用与testAIResponse相同的模型
          messages: [{ role: 'user', content: analysisPrompt }],
          stream: true, // 使用流式响应
          temperature: 0.2, // 使用较低的temperature以获得更确定的回答
          max_tokens: 2000
        };

        // 发送请求到同样的后端API
        fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        }).then(async response => {
          if (!response.ok) {
            throw new Error(`HTTP错误 ${response.status}`);
          }
          
          // 处理流式响应
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let buffer = '';
          
          // 读取数据流
          const readStream = async () => {
            try {
              while (true) {
                const { value, done } = await reader.read();
                
                if (done) {
                  console.log("分析流读取完成");
                  this.isAnalyzing = false;
                  break;
                }
                
                // 解码并处理新数据
                buffer += decoder.decode(value, { stream: true });
                
                // 处理SSE数据
                const lines = buffer.split('\n\n');
                buffer = lines.pop() || '';
                
                for (const line of lines) {
                  if (line.startsWith('data: ')) {
                    const dataStr = line.slice(6);
                    
                    // 处理结束标记
                    if (dataStr === '[DONE]') {
                      this.isAnalyzing = false;
                      return;
                    }
                    
                    try {
                      const data = JSON.parse(dataStr);
                      
                      // 处理错误消息
                      if (data.error) {
                        this.errorMessage = data.error.message || '请求出错';
                        this.isAnalyzing = false;
                        return;
                      }
                      
                      // 处理内容增量
                      if (data.choices && data.choices[0]?.delta?.content) {
                        const deltaContent = data.choices[0].delta.content;
                        this.analysisResponse += deltaContent;
                      }
                    } catch (error) {
                      console.error("解析数据出错:", error);
                    }
                  }
                }
              }
            } catch (error) {
              console.error("读取流出错:", error);
              this.errorMessage = '读取响应出错';
              this.isAnalyzing = false;
            }
          };
          
          // 开始读取流
          readStream();
        }).catch(error => {
          console.error("分析请求出错:", error);
          this.isAnalyzing = false;
          this.analysisResponse = "**分析失败**\n\n发生错误，无法完成分析。";
        });
      } catch (error) {
        console.error("执行分析时出错:", error);
        this.isAnalyzing = false;
        this.analysisResponse = "**分析失败**\n\n发生错误，无法完成分析。";
      }
    },
    // 使用背景信息示例
    useBackgroundExample() {
      this.stepPrompts.background = this.backgroundExample;
    },
    
    // 清空背景信息
    clearBackground() {
      this.stepPrompts.background = '';
    },
    
    // 使用目标示例
    useGoalExample() {
      this.stepPrompts.goal = this.goalExample;
    },
    
    // 清空目标
    clearGoal() {
      this.stepPrompts.goal = '';
    },
    
    // 使用任务示例
    useTaskExample() {
      this.stepPrompts.task = this.taskExample;
    },
    
    // 清空任务
    clearTask() {
      this.stepPrompts.task = '';
    },
    
    // 使用注意事项示例
    useCautionsExample() {
      this.stepPrompts.cautions = this.cautionsExample;
    },
    
    // 清空注意事项
    clearCautions() {
      this.stepPrompts.cautions = '';
    },
    
    // 设置当前示例
    setCurrentExample(index) {
      this.currentExampleIndex = index;
    },
    async executePracticePrompt() {
      if (!this.practicePrompt.trim()) return;
      
      this.isLoadingPractice = true;
      this.practiceResponse = '';
      this.showPracticeResponse = true;
      this.errorMessage = '';
      
      try {
        const requestData = {
          model: 'deepseek-v3',
          messages: [
            {
              role: "user",
              content: this.practicePrompt
            }
          ],
          stream: true,
          temperature: 0.7,
          max_tokens: 2048
        };
        
        // 发起流式请求 - 使用与testAIResponse相同的API端点
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        });

        if (!response.ok) {
          throw new Error(`API请求失败: ${response.status}`);
        }

        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        const processChunk = async () => {
          const { done, value } = await reader.read();
          
          if (done) {
            this.isLoadingPractice = false;
            return;
          }
          
          buffer += decoder.decode(value, { stream: true });
          
          // 解析SSE数据
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                this.isLoadingPractice = false;
                break;
              }
              
              try {
                const json = JSON.parse(data);
                const content = json.choices?.[0]?.delta?.content || '';
                if (content) {
                  this.practiceResponse += content;
                }
              } catch (e) {
                console.error('解析SSE数据失败:', e);
              }
            }
          }
          
          await processChunk();
        };
        
        await processChunk();
      } catch (error) {
        console.error("请求出错:", error);
        this.errorMessage = error.message || '请求出错';
        this.isLoadingPractice = false;
      }
    },
    scrollToSection(sectionId) {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // 更新活动部分
        switch(sectionId) {
          case 'self-assessment':
            this.activePath = 1;
            break;
          case 'basics-section':
            this.activePath = 2;
            break;
          case 'step-by-step-section':
            this.activePath = 3;
            break;
          case 'more-examples-section':
            this.activePath = 4;
            break;
          case 'practice-section':
            this.activePath = 5;
            break;
          case 'more-knowledge-section':
            this.activePath = 6;
            break;
        }
      }
    },
    handleScroll() {
      // 获取所有学习部分的位置
      const sections = [
        this.$refs.selfAssessment,
        this.$refs.basicsSection, 
        this.$refs.stepByStepSection,
        this.$refs.moreExamplesSection,
        this.$refs.practiceSection,
        this.$refs.moreKnowledgeSection
      ];
      
      // 计算当前滚动位置
      const scrollPosition = window.scrollY + 100; // 添加一些偏移
      
      // 找到当前可见的部分
      for(let i = sections.length - 1; i >= 0; i--) {
        if (sections[i] && sections[i].offsetTop <= scrollPosition) {
          this.activePath = i + 1;
          break;
        }
      }
    },
  },
  mounted() {
    // 为提示技巧的下拉菜单添加点击事件
    const tipsHeader = document.querySelector('.tips-header')
    const tipsContent = document.querySelector('.tips-content')
    
    if (tipsHeader && tipsContent) {
      tipsHeader.addEventListener('click', () => {
        tipsContent.style.display = tipsContent.style.display === 'block' ? 'none' : 'block'
        tipsHeader.classList.toggle('active')
      })
    }
    // 添加滚动监听来更新活动路径
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    // 移除滚动监听
    window.removeEventListener('scroll', this.handleScroll);
  }
}
</script>

<style scoped>
.prompt-case-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 80px;
  color: #333;
}

.header {
  text-align: center;
  margin-bottom: 50px;
}

.main-title {
  font-size: 36px;
  font-weight: 700;
  color: #C74B50;
  margin-bottom: 16px;
}

.sub-title {
  font-size: 18px;
  color: #666;
  max-width: 700px;
  margin: 0 auto;
}

.content-section {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  padding: 40px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 40px 0 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

/* 自我评估部分 */
.self-assessment {
  margin-bottom: 48px;
}

.question-card {
  background-color: #f8f5ff;
  border-radius: 12px;
  padding: 30px;
  border-left: 4px solid #ba003f;
}

.question-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.question-header i {
  font-size: 28px;
  color: #ba003f;
  margin-right: 12px;
}

.question-header h3 {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.question-desc {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 24px;
}

.thought-experiment {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #eee;
}

.thought-experiment p {
  margin-bottom: 16px;
}

.textarea-container {
  margin-top: 16px;
}

.textarea-container textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
  font-size: 15px;
  resize: vertical;
}

.textarea-container textarea:focus {
  outline: none;
  border-color: #ba003f;
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.1);
}

/* 介绍部分 */
.intro-section {
  margin-bottom: 48px;
}

.intro-text {
  font-size: 16px;
  line-height: 1.8;
  color: #555;
  margin-bottom: 16px;
}

/* 阶段式学习容器 */
.levels-container {
  margin-bottom: 48px;
}

.level-block {
  margin-bottom: 36px;
  border: 1px solid #eee;
  border-radius: 12px;
  overflow: hidden;
}

.level-header {
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
}

.level-badge {
  background-color: #ba003f;
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 16px;
  margin-right: 12px;
}

.level-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.level-content {
  padding: 24px;
}

.level-content > p {
  font-size: 16px;
  color: #555;
  margin-bottom: 20px;
}

/* 比较框 */
.comparison-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.comparison-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
}

.comparison-item.weak {
  border-left: 4px solid #e74c3c;
}

.comparison-item.better {
  border-left: 4px solid #2ecc71;
}

.comparison-item h4 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.weak h4 {
  color: #e74c3c;
}

.better h4 {
  color: #2ecc71;
}

.prompt-example {
  background-color: white;
  border-radius: 6px;
  padding: 16px;
  border: 1px solid #eee;
  margin-bottom: 12px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
}

.result-preview {
  font-size: 14px;
  line-height: 1.6;
}

/* 关键提示 */
.key-tips {
  background-color: #f0f7ff;
  border-radius: 8px;
  padding: 20px;
  border-left: 4px solid #3498db;
}

.key-tips h4 {
  font-size: 16px;
  font-weight: 600;
  color: #3498db;
  margin: 0 0 12px 0;
}

.key-tips ul {
  padding-left: 20px;
  margin: 0;
}

.key-tips li {
  margin-bottom: 8px;
  font-size: 15px;
  color: #555;
}

/* 提示词展示 */
.prompt-showcase {
  margin-bottom: 24px;
}

.prompt-showcase h4 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.prompt-code {
  background-color: #f8f8f8;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  overflow-x: auto;
}

.prompt-code pre {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  margin: 0;
}

/* 结果表格 */
.advanced-results {
  margin-top: 24px;
}

.result-table {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.result-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  background-color: #f5f5f5;
  font-weight: 600;
  font-size: 15px;
}

.result-header div {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
}

.result-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.result-row div {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

.result-row:last-child div {
  border-bottom: none;
}

/* 迭代展示 */
.iteration-showcase {
  margin-bottom: 24px;
}

.iteration-step {
  display: flex;
  margin-bottom: 20px;
}

.step-number {
  background-color: #ba003f;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  margin-right: 16px;
  flex-shrink: 0;
  margin-top: 3px;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.dialogue-box {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.user-message, .ai-message {
  padding: 16px;
  font-size: 14px;
}

.user-message {
  background-color: #f0f7ff;
  border-bottom: 1px solid #eee;
}

.ai-message {
  background-color: white;
}

.ai-message p:last-child {
  margin-bottom: 0;
}

/* 专业提示 */
.pro-tips {
  background-color: #fdf2e9;
  border-radius: 8px;
  padding: 20px;
  border-left: 4px solid #e67e22;
}

.pro-tips h4 {
  font-size: 16px;
  font-weight: 600;
  color: #e67e22;
  margin: 0 0 12px 0;
}

.pro-tips ul {
  padding-left: 20px;
  margin: 0;
}

.pro-tips li {
  margin-bottom: 8px;
  font-size: 15px;
  color: #555;
}

/* 挑战卡片 */
.challenge-card {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 36px;
}

.challenge-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.challenge-card p {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
}

.tips-dropdown {
  margin-top: 20px;
}

.tips-header {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 12px 16px;
  background-color: #f0f0f0;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.tips-header:hover {
  background-color: #e8e8e8;
}

.tips-header.active {
  background-color: #e0e0e0;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.tips-header i {
  color: #ba003f;
  margin-right: 8px;
}

.tips-header i:last-child {
  margin-left: auto;
  margin-right: 0;
}

.tips-content {
  display: none;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-top: none;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  padding: 16px;
}

.tips-content ul {
  padding-left: 20px;
  margin: 0;
}

.tips-content li {
  margin-bottom: 8px;
  font-size: 15px;
  color: #555;
}

/* 资源卡片 */
.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.resource-card {
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-align: center;
}

.resource-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.resource-card i {
  font-size: 32px;
  color: #ba003f;
  margin-bottom: 16px;
}

.resource-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.resource-card p {
  font-size: 15px;
  color: #666;
  margin-bottom: 16px;
}

.resource-link {
  display: inline-flex;
  align-items: center;
  color: #ba003f;
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
}

.resource-link i {
  font-size: 16px;
  margin-left: 4px;
  margin-bottom: 0;
  transition: transform 0.2s;
}

.resource-link:hover i {
  transform: translateX(4px);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .content-section {
    padding: 24px;
  }
  
  .comparison-box {
    grid-template-columns: 1fr;
  }
  
  .result-table {
    font-size: 14px;
  }
  
  .resources-grid {
    grid-template-columns: 1fr;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* AI测试按钮样式 */
.test-ai-btn {
  margin-top: 16px;
  background-color: #ba003f;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s, transform 0.2s;
}

.test-ai-btn:hover {
  background-color: #9e0035;
  transform: translateY(-2px);
}

.test-ai-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
}

.test-ai-btn i {
  margin-right: 8px;
  font-size: 16px;
}

/* 按钮容器样式 */
.button-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

/* AI响应区域样式 */
.ai-response-container {
  margin-top: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9;
}

.response-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #e0e0e0;
}

.model-tag {
  font-size: 14px;
  font-weight: 600;
  color: #555;
}

.copy-btn {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
  transition: color 0.2s;
}

.copy-btn:hover {
  color: #ba003f;
}

.response-content {
  padding: 16px;
  min-height: 100px;
  max-height: 400px;
  overflow-y: auto;
  line-height: 1.6;
  font-size: 15px;
  color: #333;
  background-color: white;
}

.response-content.streaming::after {
  content: '|';
  display: inline-block;
  animation: blink 1s step-end infinite;
  margin-left: 2px;
  font-weight: normal;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 代码块样式 */
.response-content pre {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  border-left: 3px solid #ba003f;
  overflow-x: auto;
  margin: 12px 0;
}

.response-content code {
  font-family: 'Courier New', monospace;
  font-size: 14px;
}

.response-content p code {
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 14px;
}

/* 复制提示样式 */
.copy-toast {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  opacity: 0;
  transition: all 0.3s ease;
  z-index: 1000;
}

.copy-toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* 提示词分析部分样式 */
.prompt-analysis {
  margin-top: 24px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  overflow: hidden;
}

.analysis-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #e0e0e0;
}

.analysis-header i {
  color: #e67e22;
  font-size: 20px;
  margin-right: 8px;
}

.analysis-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.analysis-content {
  padding: 16px;
}

.output-analysis, .prompt-analysis-section {
  margin-bottom: 24px;
  padding: 16px;
  background-color: white;
  border-radius: 8px;
  border: 1px solid #eee;
}

.output-analysis h5, .prompt-analysis-section h5 {
  font-size: 17px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
}

.output-analysis h5 i, .prompt-analysis-section h5 i {
  margin-right: 8px;
  color: #666;
}

.analysis-warning {
  padding: 12px 16px;
  background-color: rgba(230, 126, 34, 0.1);
  border-left: 3px solid #e67e22;
  border-radius: 4px;
  color: #333;
  font-size: 15px;
  margin-bottom: 16px;
}

.analysis-details {
  margin-bottom: 16px;
}

.analysis-details p {
  font-weight: 600;
  margin-bottom: 8px;
}

.analysis-details ul {
  margin: 0;
  padding-left: 24px;
}

.analysis-details li {
  margin-bottom: 6px;
  color: #555;
}

.analysis-conclusion {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: #f5f5f5;
  border-radius: 6px;
  font-size: 15px;
}

.analysis-conclusion p {
  margin: 0;
  line-height: 1.6;
}

/* 添加调试样式 */
.debug-info {
  font-size: 10px;
  color: #999;
  text-align: right;
  padding: 4px;
  margin-top: 4px;
}

/* 添加分析加载中样式 */
.analysis-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 添加高亮结论样式 */
.conclusion-highlight {
  margin-top: 32px;
  background: linear-gradient(to right, #fcf2e8, #fff9f2);
  border-radius: 10px;
  border-left: 4px solid #e67e22;
  overflow: hidden;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.8s ease-out;
}

.conclusion-title {
  padding: 12px 16px;
  background-color: rgba(230, 126, 34, 0.1);
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(230, 126, 34, 0.2);
}

.conclusion-title i {
  color: #e67e22;
  font-size: 20px;
  margin-right: 8px;
}

.conclusion-content {
  padding: 16px 20px;
}

.conclusion-content p {
  margin: 0;
  font-size: 16px;
  line-height: 1.7;
  color: #333;
}

.conclusion-content strong {
  color: #ba003f;
}

/* 添加示例切换按钮样式 */
.prompt-example-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.prompt-example-header p {
  margin: 0;
  flex: 1;
}

.change-example-btn {
  background-color: transparent;
  color: #ba003f;
  border: 1px solid #ba003f;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  margin-left: 12px;
}

.change-example-btn:hover {
  background-color: rgba(186, 0, 63, 0.1);
}

.change-example-btn i {
  margin-right: 4px;
  font-size: 16px;
}

/* 扩展的结论样式 */
.expanded-conclusion p {
  margin-bottom: 14px;
}

.expanded-conclusion p:last-child {
  margin-bottom: 0;
}

/* 提示词基础知识部分样式 */
.basics-section {
  margin-bottom: 48px;
}

.basics-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.basics-content {
  padding: 32px;
}

.basics-content h3 {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.basics-content > p {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 28px;
}

.basics-points {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

@media (min-width: 768px) {
  .basics-points {
    grid-template-columns: repeat(3, 1fr);
  }
}

.basics-point {
  display: flex;
  align-items: flex-start;
}

.point-icon {
  width: 40px;
  height: 40px;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.point-icon i {
  font-size: 20px;
  color: #ba003f;
}

.point-content h4 {
  font-size: 17px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.point-content p {
  font-size: 15px;
  line-height: 1.5;
  color: #666;
  margin: 0;
}

.learn-more-container {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.learn-more-btn {
  background-color: #ba003f;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 8px rgba(186, 0, 63, 0.2);
}

.learn-more-btn:hover {
  background-color: #9e0035;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.3);
}

.learn-more-btn i {
  margin-right: 8px;
  font-size: 18px;
}

/* 添加手把手提示词设计优化样式 */
.step-by-step-section {
  margin-bottom: 48px;
}

.step-intro {
  margin-bottom: 24px;
}

.step-intro p {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
}

/* 步骤导航 */
.step-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.step-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  padding: 8px;
}

.step-nav-item:hover .step-number {
  background-color: rgba(186, 0, 63, 0.8);
}

.step-nav-item.active .step-number {
  background-color: #ba003f;
  transform: scale(1.1);
}

.step-nav-item.active .step-name {
  color: #ba003f;
  font-weight: 600;
}

.step-number {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: rgba(186, 0, 63, 0.5);
  color: white;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  transition: all 0.2s;
}

.step-name {
  font-size: 14px;
  color: #666;
  text-align: center;
}

.step-connector {
  height: 2px;
  background-color: #e0e0e0;
  flex-grow: 1;
  margin: 0 8px;
  margin-bottom: 20px;
}

/* 步骤内容 */
.step-content-container {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.step-content {
  padding: 24px;
}

.step-header {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.step-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
}

.step-header h3 i {
  color: #ba003f;
  margin-right: 10px;
  font-size: 22px;
}

.step-description {
  margin-bottom: 24px;
}

.step-description p {
  margin-bottom: 16px;
  line-height: 1.6;
}

.example-block {
  background-color: #f8f8f8;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.example-title {
  font-weight: 600;
  margin-bottom: 8px;
  color: #555;
}

.example-block ul {
  margin: 0;
  padding-left: 20px;
}

.example-block li {
  margin-bottom: 6px;
  color: #666;
}

/* 提示词构建区域 */
.prompt-building {
  margin-bottom: 24px;
}

.prompt-label {
  font-weight: 600;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.prompt-box {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 16px;
  color: #555;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
  white-space: pre-wrap;
  word-break: break-word;
}

.prompt-box.optimized {
  background-color: #f0f7ff;
  border-left: 3px solid #3498db;
}

.prompt-box.final {
  background-color: #f0f7ff;
  border-left: 3px solid #3498db;
}

.prompt-improvement textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
}

.prompt-improvement textarea:focus {
  outline: none;
  border-color: #ba003f;
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.1);
}

/* 步骤操作按钮 */
.step-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
}

.next-step-btn, .prev-step-btn, .reset-btn {
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.2s;
  border: none;
}

.next-step-btn {
  background-color: #ba003f;
  color: white;
  margin-left: auto;
}

.next-step-btn:hover {
  background-color: #9e0035;
  transform: translateY(-2px);
}

.next-step-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
}

.prev-step-btn {
  background-color: #f0f0f0;
  color: #666;
}

.prev-step-btn:hover {
  background-color: #e0e0e0;
}

.reset-btn {
  background-color: #f8d7da;
  color: #721c24;
}

.reset-btn:hover {
  background-color: #f5c6cb;
}

.next-step-btn i, .prev-step-btn i, .reset-btn i {
  font-size: 16px;
}

.next-step-btn i {
  margin-left: 6px;
}

.prev-step-btn i, .reset-btn i {
  margin-right: 6px;
}

/* 最终提示词操作 */
.final-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.copy-final-btn, .test-final-btn {
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  transition: all 0.2s;
}

.copy-final-btn {
  background-color: #f0f0f0;
  color: #555;
  flex: 1;
}

.copy-final-btn:hover {
  background-color: #e0e0e0;
}

.test-final-btn {
  background-color: #ba003f;
  color: white;
  flex: 1;
}

.test-final-btn:hover {
  background-color: #9e0035;
  transform: translateY(-2px);
}

.copy-final-btn i, .test-final-btn i {
  margin-right: 6px;
  font-size: 16px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .step-nav {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .step-nav-item {
    flex-direction: row;
    width: 100%;
    margin-bottom: 10px;
  }
  
  .step-number {
    margin-bottom: 0;
    margin-right: 10px;
  }
  
  .step-connector {
    width: 2px;
    height: 20px;
    margin: 0 0 0 18px;
  }
  
  .final-actions {
    flex-direction: column;
  }
}

/* 空提示词样式 */
.empty-prompt {
  color: #888;
  font-style: italic;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60px;
  background-color: #f8f8f8;
  border-style: dashed;
  border-color: #ddd;
}

.empty-prompt i {
  margin-right: 8px;
  font-size: 18px;
  color: #888;
}

/* 示例操作按钮样式 */
.example-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-bottom: 8px;
}

.use-example-btn, .clear-btn {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

.use-example-btn {
  color: #3498db;
}

.use-example-btn:hover {
  background-color: #eaf6ff;
  border-color: #3498db;
}

.clear-btn {
  color: #e74c3c;
}

.clear-btn:hover {
  background-color: #fdeeee;
  border-color: #e74c3c;
}

.use-example-btn i, .clear-btn i {
  margin-right: 4px;
  font-size: 14px;
}

.example-hint {
  display: flex;
  align-items: center;
  justify-content: flex-end; /* 添加右对齐 */
  font-size: 12px;
  color: #888;
  margin-top: 8px;
  text-align: right; /* 文本右对齐 */
}

.example-hint i {
  margin-right: 6px;
  color: #e67e22;
  font-size: 14px;
}

/* 添加标题行样式 */
.prompt-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

/* 修改已存在的样式 */
.prompt-label {
  font-weight: 600;
  font-size: 14px;
  color: #666;
}

.example-actions {
  display: flex;
  gap: 8px;
}

.use-example-btn, .clear-btn {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

/* 优化提示词响应区域样式 */
.optimized-response-container {
  margin-top: 24px;
}

/* 对比视图样式 */
.comparison-view {
  margin-top: 32px;
  padding: 24px;
  background-color: #f9f9f9;
  border-radius: 12px;
  border: 1px solid #eee;
}

.comparison-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
}

.comparison-title i {
  margin-right: 8px;
  color: #3498db;
  font-size: 20px;
}

.comparison-container {
  display: flex;
  gap: 20px;
}

.comparison-column {
  flex: 1;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.comparison-header {
  padding: 16px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #eee;
}

.comparison-header h5 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.comparison-prompt-text {
  font-size: 13px;
  color: #666;
  max-height: 100px;
  overflow-y: auto;
  padding: 8px;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
}

.comparison-content {
  padding: 16px;
  height: 350px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.6;
}

.comparison-divider {
  width: 1px;
  background-color: #eee;
}

.comparison-conclusion {
  margin-top: 20px;
  padding: 16px;
  background-color: #f0f7ff;
  border-radius: 8px;
  border-left: 3px solid #3498db;
}

.comparison-conclusion p {
  margin: 0;
  color: #333;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .comparison-container {
    flex-direction: column;
  }
  
  .comparison-divider {
    height: 1px;
    width: 100%;
    margin: 8px 0;
  }
}

/* 更多对照示例部分样式 */
.more-examples-section {
  margin-bottom: 48px;
}

.section-desc {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 24px;
}

.examples-navigation {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}

.example-nav-btn {
  padding: 10px 16px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}

.example-nav-btn:hover {
  background-color: #e0e0e0;
  transform: translateY(-2px);
}

.example-nav-btn.active {
  background-color: #ba003f;
  color: white;
  box-shadow: 0 2px 8px rgba(186, 0, 63, 0.2);
}

.example-showcase {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  background-color: white;
}

.example-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
}

.example-column {
  padding: 24px;
}

.weak-column {
  background-color: #f0f7ff;
  border-top: 4px solid #3498db;
}

.better-column {
  background-color: #fdf2f5;
  border-top: 4px solid #ba003f;
}

.example-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.example-header i {
  font-size: 24px;
  margin-right: 12px;
}

.weak-column .example-header i {
  color: #3498db;
}

.better-column .example-header i {
  color: #ba003f;
}

.example-header h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.weak-column .example-header h3 {
  color: #3498db;
}

.better-column .example-header h3 {
  color: #ba003f;
}

.example-content {
  background-color: white;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 15px;
  line-height: 1.6;
  min-height: 150px;
}

.weak-column .example-content {
  border-left: 3px solid #3498db;
}

.better-column .example-content {
  border-left: 3px solid #ba003f;
}

.better-prompt-structure {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.prompt-structure-item {
  display: flex;
  flex-direction: column;
}

.structure-label {
  font-weight: 600;
  margin-bottom: 4px;
  color: #ba003f;
}

.structure-content {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.example-analysis, .example-benefits {
  padding: 16px;
  border-radius: 8px;
  font-size: 14px;
}

.example-analysis {
  background-color: rgba(52, 152, 219, 0.1);
}

.example-benefits {
  background-color: rgba(186, 0, 63, 0.1);
}

.example-analysis h4, .example-benefits h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.example-analysis h4 {
  color: #3498db;
}

.example-benefits h4 {
  color: #ba003f;
}

.example-analysis ul, .example-benefits ul {
  margin: 0;
  padding-left: 20px;
}

.example-analysis li, .example-benefits li {
  margin-bottom: 6px;
}

.example-context {
  padding: 16px 24px;
  background-color: #f9f9f9;
  border-top: 1px solid #eee;
}

.example-context p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .example-columns {
    grid-template-columns: 1fr;
  }
  
  .example-nav-btn {
    font-size: 13px;
    padding: 8px 12px;
  }
}

/* 练习部分按钮样式 */
.execute-prompt-btn {
  background-color: #ba003f;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 12px;
}

.execute-prompt-btn:hover:not(:disabled) {
  background-color: #d10046;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.2);
}

.execute-prompt-btn:disabled {
  background-color: #999;
  cursor: not-allowed;
}

.execute-prompt-btn i {
  font-size: 18px;
}

.practice-response-area {
  margin-top: 24px;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.practice-response-area .response-header {
  background-color: #f0f0f0;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.practice-response-area .response-header h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.practice-response-area .response-content {
  padding: 16px;
  line-height: 1.6;
  max-height: 400px;
  overflow-y: auto;
  white-space: pre-wrap;
}

/* 加载动画 */
.loading-indicator {
  display: flex;
  align-items: center;
}

.dot-flashing {
  position: relative;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: #ba003f;
  color: #ba003f;
  animation: dot-flashing 1s infinite linear alternate;
  animation-delay: 0.5s;
}

.dot-flashing::before, .dot-flashing::after {
  content: '';
  display: inline-block;
  position: absolute;
  top: 0;
}

.dot-flashing::before {
  left: -15px;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: #ba003f;
  color: #ba003f;
  animation: dot-flashing 1s infinite alternate;
  animation-delay: 0s;
}

.dot-flashing::after {
  left: 15px;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: #ba003f;
  color: #ba003f;
  animation: dot-flashing 1s infinite alternate;
  animation-delay: 1s;
}

@keyframes dot-flashing {
  0% {
    background-color: #ba003f;
  }
  50%, 100% {
    background-color: rgba(186, 0, 63, 0.2);
  }
}

/* 06 更多提示词工程知识 */
.more-knowledge-section {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 30px;
  margin-top: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.more-knowledge-section .section-desc {
  margin-bottom: 30px;
  color: #555;
  font-size: 16px;
  line-height: 1.6;
}

.knowledge-action {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.more-knowledge-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: #ba003f;
  color: white;
  font-size: 16px;
  font-weight: 500;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  gap: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.2);
}

.more-knowledge-btn:hover {
  background-color: #d10046;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(186, 0, 63, 0.3);
}

.more-knowledge-btn i {
  font-size: 20px;
}

/* 知识抽屉样式 */
.knowledge-drawer-content {
  padding: 20px;
  overflow-y: auto;
  max-height: 100%;
}

.knowledge-drawer-content h3 {
  color: #333;
  font-size: 18px;
  margin-top: 24px;
  margin-bottom: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.knowledge-drawer-content h3:first-child {
  margin-top: 0;
}

.knowledge-drawer-content p {
  color: #555;
  line-height: 1.6;
  margin-bottom: 16px;
}

.knowledge-points {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.knowledge-point {
  display: flex;
  gap: 12px;
}

.point-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  background-color: rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ba003f;
}

.point-content h4 {
  margin: 0 0 6px 0;
  font-size: 16px;
  color: #333;
}

.point-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.advanced-tips {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.tip-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.tip-item i {
  color: #ba003f;
  font-size: 18px;
  margin-top: 3px;
}

.tip-item p {
  margin: 0;
  font-size: 14px;
}

/* 添加模板部分样式 */
.template-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.template-item h4 {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.template-content {
  background-color: #f5f5f5;
  border-left: 3px solid #ba003f;
  padding: 12px;
  font-size: 13px;
  color: #555;
  border-radius: 0 4px 4px 0;
  font-style: italic;
}

/* 添加对比示例样式 */
.example-comparison {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.weak-example, .better-example {
  padding: 12px;
  border-radius: 4px;
}

.weak-example {
  background-color: rgba(52, 152, 219, 0.1);
  border-left: 3px solid #3498db;
}

.better-example {
  background-color: rgba(186, 0, 63, 0.1);
  border-left: 3px solid #ba003f;
}

.weak-example h4, .better-example h4 {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.weak-example h4 {
  color: #3498db;
}

.better-example h4 {
  color: #ba003f;
}

.weak-example p, .better-example p {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
}

.learn-more-link {
  margin-top: 30px;
  text-align: center;
}

.learn-more-link a {
  color: #ba003f;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  transition: all 0.2s;
}

.learn-more-link a:hover {
  color: #d10046;
  text-decoration: underline;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .more-knowledge-btn {
    width: 100%;
    font-size: 15px;
  }
  
  .knowledge-drawer-content {
    padding: 15px;
  }
}

/* 学习路径导航栏 */
.learning-path-nav {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 20px 14px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  position: fixed;
  top: 100px;
  right: 20px;
  z-index: 100;
  width: 160px;
}

.path-nav-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  padding: 10px 8px;
  border-radius: 8px;
  margin-bottom: 6px;
}

.path-nav-item:last-child {
  margin-bottom: 0;
}

.path-nav-item:hover {
  background-color: rgba(186, 0, 63, 0.05);
}

.path-nav-item.active {
  background-color: rgba(186, 0, 63, 0.1);
}

.path-nav-item.active::after {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background-color: #ba003f;
  border-radius: 3px;
}

.path-number {
  font-size: 16px;
  font-weight: 700;
  color: #ba003f;
  margin-right: 8px;
  width: 26px;
  text-align: center;
}

.path-name {
  font-size: 13px;
  color: #666;
}

.path-nav-item.active .path-name {
  color: #ba003f;
  font-weight: 600;
}

/* 学习内容容器 */
.learning-path-content {
  position: relative;
  padding-left: 40px; /* 为左侧时间线留出空间 */
  padding-right: 180px; /* 为右侧导航栏留出空间 */
}

/* 响应式调整 */
@media (max-width: 1100px) {
  .learning-path-nav {
    position: sticky;
    top: 20px;
    right: unset;
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 40px;
    padding: 16px 24px;
  }
  
  .path-nav-item {
    flex-direction: column;
    margin-bottom: 0;
  }
  
  .path-nav-item.active::after {
    left: 50%;
    top: unset;
    bottom: 0;
    transform: translateX(-50%);
    width: 60%;
    height: 3px;
  }
  
  .path-number {
    margin-right: 0;
    margin-bottom: 4px;
    width: auto;
  }
  
  .learning-path-content {
    padding-right: 0;
  }
}

@media (max-width: 768px) {
  .learning-path-nav {
    overflow-x: auto;
    justify-content: flex-start;
    padding: 12px 16px;
  }
  
  .path-nav-item {
    flex: 0 0 auto;
    margin-right: 16px;
    padding: 8px 12px;
  }
  
  .path-number {
    font-size: 16px;
  }
  
  .path-name {
    font-size: 12px;
  }
  
  .learning-path-content {
    padding-left: 30px;
  }
  
  .learning-section::before {
    left: -30px;
    width: 20px;
    height: 20px;
  }
  
  .section-number {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}

/* 学习路径垂直线 */
.learning-path-line {
  position: absolute;
  left: 10px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(to bottom, #ba003f 0%, #3498db 100%);
  z-index: 1;
}

/* 学习部分通用样式 */
.learning-section {
  position: relative;
  padding-bottom: 60px;
}

.learning-section::before {
  content: '';
  position: absolute;
  left: -40px; /* 对齐垂直线 */
  top: 24px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: white;
  border: 3px solid #ba003f;
  z-index: 2;
}

/* 每个部分有不同颜色的指示点 */
.self-assessment::before {
  border-color: #ba003f;
}

.basics-section::before {
  border-color: #bd4379;
}

.step-by-step-section::before {
  border-color: #c0669e;
}

.more-examples-section::before {
  border-color: #9e77ad;
}

.practice-section::before {
  border-color: #7988bb;
}

.more-knowledge-section::before {
  border-color: #3498db;
}

/* 部分标题样式增强 */
.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.section-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background-color: #ba003f;
  color: white;
  font-size: 16px;
  font-weight: 700;
  border-radius: 50%;
  margin-right: 12px;
}

/* 对各部分应用不同的标题数字背景色 */
.self-assessment .section-number {
  background-color: #ba003f;
}

.basics-section .section-number {
  background-color: #bd4379;
}

.step-by-step-section .section-number {
  background-color: #c0669e;
}

.more-examples-section .section-number {
  background-color: #9e77ad;
}

.practice-section .section-number {
  background-color: #7988bb;
}

.more-knowledge-section .section-number {
  background-color: #3498db;
}
</style> 