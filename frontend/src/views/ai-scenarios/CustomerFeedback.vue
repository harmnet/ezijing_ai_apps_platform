<template>
  <div class="marketing-campaign-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-bg-overlay"></div>
      <div class="container">
        <div class="header-actions">
          <div class="back-link" @click="goBack">
            <i class="ri-arrow-left-line"></i> 返回场景列表
          </div>
          <button class="reset-button" @click="confirmReset">
            <i class="ri-refresh-line"></i> 重置场景
          </button>
        </div>
        <h1 class="main-title">产品方案编写 <span class="scenario-category">产品经理实践</span></h1>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="container">
      <!-- 角色介绍部分 -->
      <div class="section role-section">
        <h2 class="section-title">
          <i class="ri-user-line"></i> 你的角色
        </h2>
        <div class="role-card">
          <div class="role-avatar">
            <img src="@/assets/images/scenarios/customer-feedback-bg.png" alt="产品助理" />
          </div>
          <div class="role-info">
            <h3>
              初级产品助理 - 小林
              <button class="job-info-btn" @click="goToProductManager">
                <i class="ri-file-user-line"></i> 查看岗位介绍
              </button>
            </h3>
            <p>你是一家科技公司"创新科技"的初级产品助理，入职刚满8个月。你的主要工作是协助产品经理完成产品文档编写、用户需求收集和产品功能梳理等基础工作。虽然你有扎实的产品理论知识，但实际工作经验还较为欠缺。这是你第一次被单独委派负责一份重要的产品方案编写任务。</p>
          </div>
        </div>
      </div>

      <!-- 任务背景部分 -->
      <div class="section task-section">
        <h2 class="section-title">
          <i class="ri-task-line"></i> 任务背景
        </h2>
        <div class="task-card">
          <div class="task-content">
            <p>今天是周四下午，你正在整理自己的周报，产品经理李哥突然把你叫到办公室，神情严肃地告诉你："下周三有一个非常重要的客户要来公司，公司需要现场递交'智能客户营销综合平台SCM'的产品方案。这个方案我实在抽不出时间做，只能交给你负责了。要在下周一上班前发到我邮箱，我要检查一下。"你满口答应后回到座位，心里开始发慌。后来你从同事小王那里得知，公司其实只要求李哥在下周二下班前提交方案，李哥是为了给自己预留修改时间，才让你周一上班前就交稿。你意识到这是你入职以来面临的最大挑战，也是证明自己能力的绝佳机会。</p>
          </div>
        </div>
      </div>

      <!-- 任务提交时间 -->
      <div class="section deadline-section">
        <h2 class="section-title">
          <i class="ri-time-line"></i> 任务时限
        </h2>
        <div class="deadline-card">
          <div class="deadline-content">
            <div class="deadline-icon">
              <i class="ri-alarm-warning-line"></i>
            </div>
            <div class="deadline-info">
              <h3>紧急任务：周末加班完成</h3>
              <p>从周四下午接到任务到下周一上班前提交初稿，实际上你只有周末两天的时间。考虑到产品方案需要包含产品定位、用户分析、功能列表、交互流程和技术要求等多个方面，且你没有相关项目经验，这个时间极其紧迫。虽然李哥给自己留了缓冲时间，但你知道方案质量不好还是会让你难堪，必须高效利用周末时间，才能按时完成这份挑战性的任务。</p>
            </div>
          </div>
        </div>
      </div>

      <!-- AI辅助任务梳理部分 -->
      <div class="section ai-section">
        <div class="ai-workflow-card">
          <div class="ai-header">
            <div class="ai-title" style="text-align: center; width: 100%;">
              <p class="task-content" style="text-align: center; color: #ffffff;">突如其来的重任让小林陷入焦虑——作为一名初级产品助理，如何在周末时间内完成一份专业的产品方案？平时都是辅助角色，现在却要独立承担这么重要的任务！时间紧迫，经验有限，该如何破局？别担心，AI技术正在改变工作方式！现在，我们可以借助人工智能的超强分析能力和逻辑思维，将不可能变为可能。告别加班焦虑，提升工作效率与文档质量，让AI成为新人产品助理的得力帮手。跟随以下5个步骤，一起体验AI协作的魔力，高效完成产品方案编写！</p>
            </div>
          </div>
          
          <div class="workflow-steps">
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>获取初始任务</h4>
                <p class="task-content">一般情况下，我们从领导处获取的任务往往是相对模糊且不够详细的。领导可能只会提供核心要求和关键期望，而非完整的任务说明书。在这一步，我们需要先记录并确认已获得的初始任务信息，为后续深入分析打下基础。</p>
                
                <div class="input-container">
                  <textarea 
                    v-model="initialTask" 
                    placeholder="请小组讨论，输入你接收到的第一手原始的任务信息。" 
                    rows="3"
                    class="task-input"
                    maxlength="300"
                  ></textarea>
                  
                  <div class="input-footer">
                    <span class="character-count" :class="{ 'warning': initialTask.length > 250 }">
                      {{ initialTask.length }}/300字
                    </span>
                    <button class="next-step-btn" @click="continueToNextStep" :disabled="!initialTask.trim()">
                      <i class="ri-arrow-right-line"></i> 继续下一步
                    </button>
                  </div>
                </div>
                
                <div v-if="showStepCompleted[0]" class="saved-message">
                  <i class="ri-checkbox-circle-line"></i> 任务信息已保存，可继续下一步
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4>明确任务目标</h4>
                <p class="task-content">在获取到初始任务后，我们需要与指派任务的领导进一步确认本次任务的核心目标是什么。明确任务目标对于后续工作的方向和重点至关重要，避免因理解偏差导致的返工。在这一步，请记录与领导沟通后确认的核心任务目标。</p>
                
                <!-- 用户输入的任务目标 -->
                <div class="input-container" v-if="showStepCompleted[0]">
                  <textarea 
                    v-model="taskGoal" 
                    placeholder="请小组讨论，输入与领导沟通后明确的任务核心目标。" 
                    rows="3"
                    class="task-input"
                    :disabled="isAnalyzingGoal || taskGoalCompleted"
                    maxlength="300"
                  ></textarea>
                  
                  <div class="input-footer">
                    <span class="character-count" :class="{ 'warning': taskGoal.length > 250 }">
                      {{ taskGoal.length }}/300字
                    </span>
                  </div>
                </div>

                <!-- AI辅助梳理按钮 -->
                <div class="button-container" v-if="showStepCompleted[0]">
                  <button 
                    class="ai-assist-btn" 
                    @click="showCommonGoalsDrawer"
                  >
                    <i class="ri-file-list-line"></i> 查看常见产品方案的任务目标
                  </button>
                  <button 
                    class="ai-assist-btn" 
                    @click="getAIGoalAssistance" 
                    :disabled="isOptimizing || !taskGoal.trim() || taskGoalCompleted"
                  >
                    <i class="ri-ai-generate"></i> AI辅助目标优化
                  </button>
                </div>
                
                <!-- 常见产品方案的任务目标抽屉 -->
                <div class="drawer-container" v-if="commonGoalsDrawerVisible">
                  <div class="drawer-overlay" @click="hideCommonGoalsDrawer"></div>
                  <div class="drawer-content">
                    <div class="drawer-header">
                      <h3>产品方案通用目标参考</h3>
                      <button class="drawer-close" @click="hideCommonGoalsDrawer">
                        <i class="ri-close-line"></i>
                      </button>
                    </div>
                    <div class="drawer-body">
                      <div class="goal-intro">
                        <p>编写产品方案的主要目的是通过系统性、专业化的文档打动潜在客户，促进销售转化。根据行业实践，一份优秀的产品方案通常应包含以下核心目标：</p>
                      </div>
                    
                      <div class="goal-reference">
                        <h4>1. 全面展示产品价值与竞争优势</h4>
                        <p>全面、清晰地展示产品的特色和核心竞争优势，重点凸显产品的强大功能性、易用性和稳定性等显著特点。通过详实的产品架构、功能模块和技术特性描述，让客户充分理解产品如何满足其业务需求并优于竞品方案。</p>
                        <div class="goal-tips">
                          <strong>核心要点：</strong>
                          <ul>
                            <li>产品的关键差异化特性</li>
                            <li>核心功能模块详细说明</li>
                            <li>与竞品的优势对比</li>
                            <li>技术架构先进性</li>
                          </ul>
                        </div>
                      </div>
                      
                      <div class="goal-reference">
                        <h4>2. 展示公司综合实力</h4>
                        <p>通过产品方案有效展示公司的研发能力、技术积累、行业经验和服务水平等综合实力。突出团队专业背景、成功案例和客户口碑，增强客户对公司的信任度和认可度，为产品背书。</p>
                        <div class="goal-tips">
                          <strong>核心要点：</strong>
                          <ul>
                            <li>公司核心技术能力与研发实力</li>
                            <li>成功案例与客户见证</li>
                            <li>专业服务体系</li>
                            <li>行业经验与专业背景</li>
                          </ul>
                        </div>
                      </div>
                      
                      <div class="goal-reference">
                        <h4>3. 明确产品落地实施路径</h4>
                        <p>提供清晰、可行的产品实施方案和落地步骤，包括部署流程、数据迁移、人员培训和上线计划等环节。通过专业、完整的交付流程规划，帮助客户构建对产品落地的信心，降低客户感知风险。</p>
                        <div class="goal-tips">
                          <strong>核心要点：</strong>
                          <ul>
                            <li>实施步骤与时间规划</li>
                            <li>可能的风险与应对措施</li>
                            <li>实施资源需求</li>
                            <li>验收标准与成功指标</li>
                          </ul>
                        </div>
                      </div>
                      
                      <div class="goal-reference">
                        <h4>4. 提供清晰的配置清单与报价</h4>
                        <p>详细列出产品配置清单和价格体系，包括基础模块、可选组件、服务项目和定制开发等内容。通过透明、合理的报价方案，帮助客户明确采购内容和预算需求，便于在客户内部推动决策流程。</p>
                        <div class="goal-tips">
                          <strong>核心要点：</strong>
                          <ul>
                            <li>产品模块与组件详细配置</li>
                            <li>清晰的报价结构</li>
                            <li>可选项与升级路径</li>
                            <li>维保与服务费用说明</li>
                          </ul>
                        </div>
                      </div>
                      
                      <div class="goal-reference">
                        <h4>5. 突显产品使用价值与投资回报</h4>
                        <p>清晰阐述产品使用后能为客户带来的具体业务价值和投资回报，量化展示效率提升、成本节约或收入增长等方面的收益。通过价值论证坚定客户的购买决心，促进销售转化。</p>
                        <div class="goal-tips">
                          <strong>核心要点：</strong>
                          <ul>
                            <li>量化的业务价值指标</li>
                            <li>投资回报周期分析</li>
                            <li>客户案例中的价值实现</li>
                            <li>长期价值与持续收益</li>
                          </ul>
                        </div>
                      </div>
                      
                      <div class="goal-conclusion">
                        <p>以上五个核心目标相互补充、缺一不可，共同构成一份完整、专业的产品方案框架。根据不同产品特性和客户需求，可适当调整各部分的重点和篇幅，但总体目标应保持一致：通过专业、全面的产品方案，充分展示产品价值，赢得客户信任与认可。</p>
                      </div>
                    </div>
                    <div class="drawer-footer">
                      <button class="close-drawer-btn" @click="hideCommonGoalsDrawer">关闭</button>
                    </div>
                  </div>
                </div>
                
                <!-- AI分析结果 -->
                <div v-if="isOptimizing" class="ai-analysis-section">
                  <div class="analyzing-indicator">
                    <div class="spinner"></div>
                    <p>AI正在分析和优化任务目标...</p>
                    <div class="progress-bar-container">
                      <div class="progress-bar" :style="{ width: optimizationProgress + '%' }"></div>
                    </div>
                    <span class="progress-text">{{ optimizationProgress }}%</span>
                  </div>
                </div>
                
                <!-- 目标优化结果 -->
                <div v-if="optimizedGoal && !isOptimizing" class="task-result-section">
                  <div class="result-heading">
                    <h5>优化后的任务目标</h5>
                    <div class="improvement-badge">AI优化建议</div>
                  </div>
                  <div class="optimized-goal-container">
                    <div class="optimized-goal-content">
                      <p v-html="formattedOptimizedGoal"></p>
                    </div>
                    <div class="task-actions">
                      <button 
                        class="save-goal-btn" 
                        @click="saveTaskGoal" 
                        :disabled="taskGoalCompleted"
                      >
                        <i class="ri-save-line"></i> 确认并继续
                      </button>
                    </div>
                  </div>
                </div>
                
                <div v-if="taskGoalCompleted" class="saved-message">
                  <i class="ri-checkbox-circle-line"></i> 任务目标已确认，可继续下一步
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>编写产品方案目录结构</h4>
                <p class="task-content">一份专业的产品方案需要有清晰的目录结构，帮助决策者快速了解方案内容和逻辑。在这一步，我们需要确定产品方案的章节结构和内容安排，为后续的详细撰写提供框架。一个好的目录结构应该包含产品概述、市场分析、产品特性、技术架构、实施计划和投资回报等关键部分。</p>

                <!-- 第二步状态调试信息 -->
                <div v-if="showStepCompleted[0] && debugMode" class="debug-info">
                  步骤1完成状态: {{ showStepCompleted[0] }}<br>
                  分析中: {{ isAnalyzing }}<br>
                  任务信息已完成: {{ taskInfoCompleted }}
                </div>
                
                <!-- 按钮区域 -->
                <div class="button-container" v-if="showStepCompleted[0]">
                  <button 
                    class="ai-assist-btn" 
                    @click="showDocumentStructureDrawer"
                  >
                    <i class="ri-file-list-line"></i> 查看常见产品方案目录结构
                  </button>
                  <button 
                    class="ai-assist-btn" 
                    @click="openAIDocumentStructure"
                  >
                    <i class="ri-ai-generate"></i> AI辅助编写目录
                  </button>
                </div>
                
                <!-- 产品方案目录输入框 -->
                <div class="input-container" v-if="showStepCompleted[0]">
                  <textarea 
                    v-model="productStructure" 
                    placeholder="请输入产品方案目录结构..." 
                    rows="12"
                    class="task-input"
                  ></textarea>
                  
                  <div class="input-footer">
                    <span class="character-count" :class="{ 'warning': productStructure.length > 500 }">
                      {{ productStructure.length }}/800字
                    </span>
                  </div>
                </div>

                <!-- 结构化产品方案目录按钮 -->
                <div class="button-container buttons-justify-between" v-if="showStepCompleted[0]">
                  <button 
                    class="ai-assist-btn" 
                    @click="polishProductOutline"
                    :disabled="!productStructure.trim() || isPolishing"
                  >
                    <i class="ri-magic-line"></i> AI润色产品方案目录
                    <div v-if="isPolishing" class="button-spinner"></div>
                  </button>
                  <button 
                    class="ai-assist-btn" 
                    @click="structureProductOutline"
                    :disabled="!productStructure.trim()"
                    v-if="!showPolishedResult"
                  >
                    <i class="ri-list-check-2"></i> 结构化产品方案目录
                  </button>
                </div>
                
                <!-- 润色后的结果文本框 -->
                <div class="polished-result-container" v-if="showPolishedResult">
                  <div class="polished-result-header">
                    <h4><i class="ri-magic-line"></i> 润色后的目录结构</h4>
                    <button class="close-polished-btn" @click="closePolishedResult" v-if="!isPolishing">
                      <i class="ri-close-line"></i>
                    </button>
                  </div>
                  <div class="input-container">
                    <textarea 
                      v-model="polishedStructure" 
                      placeholder="正在生成润色后的目录结构..." 
                      rows="12"
                      class="task-input polished-input"
                      :disabled="isPolishing"
                    ></textarea>
                    
                    <div class="input-footer">
                      <span class="character-count" :class="{ 'warning': polishedStructure.length > 500 }">
                        {{ polishedStructure.length }}/800字
                      </span>
                    </div>
                  </div>
                  
                  <!-- 结构化按钮移至新文本框下方 -->
                  <div class="button-container center-btn">
                    <button 
                      class="ai-assist-btn" 
                      @click="structurePolishedOutline"
                      :disabled="!polishedStructure.trim() || isPolishing"
                    >
                      <i class="ri-list-check-2"></i> 结构化产品方案目录
                    </button>
                  </div>
                </div>
                
                <!-- 添加结构化目录展示区域在步骤3中 -->
                <div class="structured-outline-container" v-if="structuredOutline.length > 0">
                  <!-- 删除整个结构化目录区域 -->
                </div>
                
                <!-- 常见产品方案目录结构抽屉 -->
                <div class="drawer-container" v-if="documentStructureDrawerVisible">
                  <div class="drawer-overlay" @click="hideDocumentStructureDrawer"></div>
                  <div class="drawer-content">
                    <div class="drawer-header">
                      <h3>常见产品方案目录结构</h3>
                      <button class="drawer-close" @click="hideDocumentStructureDrawer">
                        <i class="ri-close-line"></i>
                      </button>
                    </div>
                    <div class="drawer-body">
                      <div class="structure-intro">
                        <p>以下是几种常见的产品方案目录结构模板，你可以根据实际需求和项目特点进行选择和调整：</p>
                      </div>
                      <div class="structure-content">
                        <div class="structure-title-container">
                          <h4>标准产品方案目录结构</h4>
                          <button class="copy-structure-btn" style="display:none;" @click="copyStandardStructure">
                            <i class="ri-file-copy-line"></i> 复制
                          </button>
                        </div>
                        <div class="structure-item">
                          <p><strong>一、公司介绍</strong></p>
                          <ul>
                            <li>公司背景与发展历程</li>
                            <li>核心团队与技术能力</li>
                            <li>行业经验与成功案例</li>
                        </ul>
                          <p><strong>二、建设必要性和合理性分析</strong></p>
                          <ul>
                            <li>（一）政策背景介绍
                              <ul>
                                <li>相关行业政策与法规解读</li>
                                <li>政策支持与发展趋势</li>
                        </ul>
                            </li>
                            <li>（二）建设必要性介绍
                              <ul>
                                <li>行业痛点与挑战分析</li>
                                <li>市场需求与发展机遇</li>
                              </ul>
                            </li>
                            <li>（三）建设合理性介绍
                              <ul>
                                <li>技术可行性分析</li>
                                <li>投资回报评估</li>
                                <li>竞争优势对比</li>
                              </ul>
                            </li>
                          </ul>
                          <p><strong>三、建设目标</strong></p>
                          <ul>
                            <li>总体目标与愿景</li>
                            <li>阶段性目标与关键指标</li>
                            <li>预期成效与价值</li>
                          </ul>
                          <p><strong>四、建设内容</strong></p>
                          <ul>
                            <li>（一）产品技术架构
                              <ul>
                                <li>整体架构设计</li>
                                <li>核心技术说明</li>
                                <li>系统安全保障</li>
                              </ul>
                            </li>
                            <li>（二）产品功能架构及核心功能模块
                              <ul>
                                <li>功能模块详解</li>
                                <li>用户交互流程</li>
                                <li>特色功能与创新点</li>
                              </ul>
                            </li>
                            <li>（三）实施落地路线
                              <ul>
                                <li>项目实施计划与里程碑</li>
                                <li>资源配置与分工</li>
                                <li>风险管控措施</li>
                              </ul>
                            </li>
                            <li>（四）培训体系设计
                              <ul>
                                <li>培训计划与课程设置</li>
                                <li>培训方式与工具</li>
                                <li>效果评估机制</li>
                              </ul>
                            </li>
                            <li>（五）售后服务体系
                              <ul>
                                <li>服务等级与响应机制</li>
                                <li>问题处理流程</li>
                                <li>持续优化与升级支持</li>
                              </ul>
                            </li>
                          </ul>
                          <p><strong>五、产品清单及报价</strong></p>
                          <ul>
                            <li>产品配置清单</li>
                            <li>服务项目明细</li>
                            <li>价格方案与付款计划</li>
                          </ul>
                        </div>
                        
                        <h4 style="margin-top: 20px;">另一种常见的产品方案结构</h4>
                        <div class="structure-item">
                          <p><strong>一、执行摘要</strong> - 方案核心内容概述</p>
                          <p><strong>二、项目背景</strong> - 项目来源与客户需求</p>
                          <p><strong>三、需求分析</strong> - 详细的用户需求解读</p>
                          <p><strong>四、解决方案</strong></p>
                          <p>（一）整体架构</p>
                          <p>（二）功能模块设计</p>
                          <p>（三）技术路线选择</p>
                          <p>（四）系统性能指标</p>
                          <p><strong>五、实施计划</strong></p>
                          <p>（一）项目周期与里程碑</p>
                          <p>（二）团队配置</p>
                          <p>（三）风险管理</p>
                          <p><strong>六、成本与投资回报</strong></p>
                          <p><strong>七、附录</strong> - 相关资质证明与案例</p>
                      </div>
                      </div>
                    </div>
                    <div class="drawer-footer">
                      <button class="close-drawer-btn" @click="hideDocumentStructureDrawer">关闭</button>
                    </div>
                  </div>
                </div>
                
                <!-- AI分析结果与表单 -->
                <div v-if="isAnalyzing || taskFields.length > 0" class="ai-analysis-section">
                  <!-- 加载中状态 -->
                  <div v-if="isAnalyzing && !taskFields.length" class="analyzing-indicator">
                    <!-- 步骤式进度指示器 -->
                    <div class="step-progress-container">
                      <div 
                        v-for="(step, index) in processingSteps" 
                        :key="index"
                        class="step-item"
                        :class="{
                          'step-completed': step.completed,
                          'step-current': step.current
                        }"
                      >
                        <div class="step-circle">
                          <i v-if="step.completed" class="ri-check-line"></i>
                          <span v-else>{{ index + 1 }}</span>
                        </div>
                        <div class="step-title">{{ step.title }}</div>
                        <div class="step-line" v-if="index < processingSteps.length - 1"></div>
                      </div>
                    </div>
                    
                    <!-- 处理中动画 -->
                    <div class="spinner" v-if="!processingError"></div>
                    
                    <!-- 当前处理步骤文本 -->
                    <p v-if="!processingError" class="processing-status">
                      {{ processingSteps[processingStep].title }}中...
                    </p>
                    
                    <!-- 错误提示 -->
                    <p v-if="processingError" class="error-message">
                      <i class="ri-error-warning-line"></i> {{ processingError }}
                    </p>
                  </div>
                  
                  <!-- AI分析完成后的表单 -->
                  <div v-if="taskFields.length > 0" class="task-fields-form">
                    <h5>请完善以下任务信息</h5>
                    
                    <div 
                      v-for="(field, index) in taskFields" 
                      :key="index" 
                      class="task-field"
                    >
                      <label>{{ field.label }} <span v-if="field.required" class="required">*</span></label>
                      <textarea 
                        v-model="field.value" 
                        :placeholder="field.placeholder" 
                        :rows="getFieldRows(field.label)"
                        :disabled="taskInfoCompleted"
                      ></textarea>
                    </div>
                    
                    <!-- 生成按钮和加载动画 -->
                    <div class="button-container generate-btn-container" v-if="!taskInfoCompleted">
                      <button 
                        class="generate-btn" 
                        @click="generateFullTaskInfo" 
                        :disabled="!canGenerateTaskInfo || isGeneratingTaskInfo"
                      >
                        <i class="ri-file-text-line"></i> 生成完整任务信息
                      </button>
                    </div>
                    
                    <!-- 生成任务信息的加载状态 -->
                    <div v-if="isGeneratingTaskInfo" class="analyzing-indicator task-generating">
                      <div class="spinner"></div>
                      <p>AI正在输出完整任务信息...</p>
                    </div>
                  </div>
                </div>
                
                <!-- 生成的完整任务信息 -->
                <div v-if="taskInfoCompleted" class="full-task-info">
                  <h5>完整任务信息 <span v-if="isGeneratingTaskInfo" class="streaming-indicator">流式输出中...</span></h5>
                  <div class="editable-task-container">
                    <textarea 
                      v-model="fullTaskInfo" 
                      rows="12"
                      class="editable-task-info"
                      :disabled="isGeneratingTaskInfo"
                    ></textarea>
                    <div class="edit-controls">
                      <span class="edit-indicator" v-if="!isGeneratingTaskInfo">可编辑</span>
                      <button class="save-edit-btn" @click="saveTaskInfo" v-if="!isGeneratingTaskInfo">
                        <i class="ri-check-line"></i> 确认并继续
                      </button>
                    </div>
                  </div>
                  
                  <div v-if="taskInfoSaved" class="saved-message">
                    <i class="ri-checkbox-circle-line"></i> 完整任务信息已保存，可继续下一步
                  </div>
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">4</div>
              <div class="step-content">
                <h4>逐个章节内容编写</h4>
                <p>在这一步，我们将对产品方案的每个章节进行逐一编写，确保内容全面、专业且有逻辑性。</p>
                
                <!-- 结构化目录展示区域始终保留在步骤4中 -->
                <div class="structured-outline-container" v-if="structuredOutline.length > 0">
                  <div class="structured-outline-header">
                    <h4><i class="ri-file-list-3-line"></i> 结构化产品方案目录</h4>
                    <div class="outline-actions">
                      <!-- 移除复制按钮 -->
                    </div>
                  </div>
                  
                  <div class="structured-outline-content">
                    <div 
                      v-for="(item, index) in displayedOutlineItems" 
                      :key="'item-' + index"
                      class="outline-item"
                      :class="{'level-1': item.level === 1, 'level-2': item.level === 2, 'level-3': item.level === 3, 'level-4': item.level === 4}"
                    >
                      <div class="outline-item-header">
                        <div class="outline-item-title-section">
                          <i 
                            :class="hasChildren(index) ? (item.expanded ? 'ri-arrow-down-s-line' : 'ri-arrow-right-s-line') : 'ri-checkbox-blank-circle-line'" 
                            class="toggle-icon" 
                            :style="hasChildren(index) ? '' : 'opacity: 0.3; font-size: 0.8em;'"
                            @click="hasChildren(index) ? toggleOutlineItem(getActualIndex(index)) : null"
                          ></i>
                          <span class="outline-item-title">{{ item.title }}</span>
                        </div>
                        <div class="outline-item-actions">
                          <button 
                            type="button"
                            class="outline-icon-btn add-same-level-btn" 
                            title="新增同级目录" 
                            @click.prevent="addSameLevelOutlineItem(getActualIndex(index))"
                          >
                            <i class="ri-add-line"></i>
                          </button>
                          <button 
                            type="button"
                            class="outline-icon-btn add-sub-level-btn" 
                            title="新增下级目录" 
                            @click.prevent="addSubLevelOutlineItem(getActualIndex(index))"
                          >
                            <i class="ri-git-branch-line"></i>
                          </button>
                          <button 
                            type="button"
                            class="outline-icon-btn ai-btn" 
                            title="AI创作" 
                            @click.prevent="aiCreateOutlineContent(item, getActualIndex(index))"
                          >
                            <i class="ri-ai-generate"></i>
                          </button>
                          <button 
                            type="button"
                            class="outline-icon-btn edit-btn" 
                            title="编写内容" 
                            @click.prevent="editOutlineItemContent(item)"
                          >
                            <i class="ri-edit-line"></i>
                          </button>
                          <button 
                            type="button"
                            class="outline-icon-btn delete-btn" 
                            title="删除" 
                            @click.prevent="removeOutlineItem(getActualIndex(index))"
                          >
                            <i class="ri-delete-bin-line"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 添加导出文档按钮 -->
                  <div class="export-button-container">
                    <button class="export-document-btn" @click="exportDocument">
                      <i class="ri-file-word-2-line"></i> 导出文档
                    </button>
                  </div>
                </div>
                
                <!-- 用户输入框 - 仅在未生成结构化目录时显示 -->
                <div class="input-container" v-if="showStepCompleted[1] && structuredOutline.length === 0">
                  <textarea 
                    v-model="userTaskBreakdown" 
                    placeholder="请按顺序列出您需要编写的章节内容..." 
                    rows="4"
                    class="task-input"
                    :disabled="isAnalyzingBreakdown || tasksGenerated"
                  ></textarea>
                </div>
                
                <!-- AI辅助按钮 - 仅在未生成结构化目录时显示 -->
                <div class="button-container" v-if="showStepCompleted[1] && structuredOutline.length === 0">
                  <button 
                    class="ai-assist-btn" 
                    @click="getAITaskBreakdown" 
                    :disabled="isAnalyzingBreakdown || !fullTaskInfo.trim() || !userTaskBreakdown.trim() || tasksGenerated"
                  >
                    <i class="ri-ai-generate"></i> AI辅助内容编写
                  </button>
                </div>
                
                <!-- 加载状态 -->
                <div v-if="isAnalyzingBreakdown" class="ai-analysis-section">
                  <div class="analyzing-indicator">
                    <!-- 步骤式进度指示器 -->
                    <div class="step-progress-container">
                      <div 
                        v-for="(step, index) in breakdownProcessingSteps" 
                        :key="index"
                        class="step-item"
                        :class="{
                          'step-completed': step.completed,
                          'step-current': step.current
                        }"
                      >
                        <div class="step-circle">
                          <i v-if="step.completed" class="ri-check-line"></i>
                          <span v-else>{{ index + 1 }}</span>
                        </div>
                        <div class="step-title">{{ step.title }}</div>
                        <div class="step-line" v-if="index < breakdownProcessingSteps.length - 1"></div>
                      </div>
                    </div>
                    
                    <!-- 处理中动画 -->
                    <div class="spinner" v-if="!breakdownProcessingError"></div>
                    
                    <!-- 当前处理步骤文本 -->
                    <p v-if="!breakdownProcessingError" class="processing-status">
                      {{ breakdownProcessingSteps[breakdownProcessingStep].title }}中...
                    </p>
                    
                    <!-- 错误提示 -->
                    <p v-if="breakdownProcessingError" class="error-message">
                      <i class="ri-error-warning-line"></i> {{ breakdownProcessingError }}
                    </p>
                  </div>
                </div>
                
                <!-- 任务拆解结果 -->
                <div v-if="taskBreakdownResult" class="task-breakdown-section">
                  <div class="task-breakdown-result">
                    <h5>任务拆解结果</h5>
                    <div class="task-tree">
                      <!-- 第一层任务 -->
                      <div v-for="(mainTask, mainIndex) in parsedTaskBreakdown" :key="'main-'+mainIndex" class="main-task">
                        <div class="main-task-header">
                          <span class="task-number">{{ mainIndex + 1 }}</span>
                          <h6>{{ mainTask.title }}</h6>
                        </div>
                        
                        <!-- 第二层子任务 -->
                        <div class="subtasks">
                          <div v-for="(subTask, subIndex) in mainTask.subtasks" :key="'sub-'+mainIndex+'-'+subIndex" class="subtask">
                            <span class="subtask-bullet">•</span>
                            <span class="subtask-content">
                              {{ subTask.task || subTask }}
                              <a 
                                v-if="subTask.systemFeature && subTask.systemLink" 
                                :href="subTask.systemLink" 
                                target="_blank" 
                                class="system-feature-link"
                              >
                                <i class="ri-link"></i> {{ subTask.systemFeature }}
                              </a>
                              <span v-else-if="subTask.systemFeature" class="system-feature-badge">
                                <i class="ri-tools-fill"></i> {{ subTask.systemFeature }}
                              </span>
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 编辑按钮 -->
                    <div class="breakdown-actions">
                      <button 
                        v-if="!editingBreakdown && !taskBreakdownSaved" 
                        class="continue-btn" 
                        @click="continueToStep4FromBreakdown"
                        style="margin-right: 12px;"
                      >
                        <i class="ri-arrow-right-line"></i> 确认并继续
                      </button>
                      <button 
                        v-if="!editingBreakdown && !taskBreakdownSaved" 
                        class="edit-breakdown-btn" 
                        @click="startEditingBreakdown"
                      >
                        <i class="ri-edit-line"></i> 编辑拆解结果
                      </button>
                      <!-- 确认和保存 -->
                      <div v-if="editingBreakdown" class="edit-controls">
                        <button class="cancel-edit-btn" @click="cancelEditingBreakdown">
                          <i class="ri-close-line"></i> 取消
                        </button>
                        <button class="save-edit-btn" @click="saveTaskBreakdown">
                          <i class="ri-check-line"></i> 保存并继续
                        </button>
                      </div>
                    </div>
                    
                    <!-- 编辑区域 -->
                    <div v-if="editingBreakdown" class="breakdown-edit-area">
                      <textarea 
                        v-model="editableTaskBreakdown" 
                        rows="12"
                        class="editable-breakdown"
                        placeholder="编辑任务拆解内容，请保持JSON格式不变"
                      ></textarea>
                      <div class="edit-tip">请保持JSON格式，编辑时注意不要破坏结构</div>
                    </div>
                    
                    <!-- 保存成功提示 -->
                    <div v-if="taskBreakdownSaved" class="saved-message">
                      <i class="ri-checkbox-circle-line"></i> 任务拆解已保存，可继续下一步
                    </div>
                  </div>
                </div>
              </div>
            </div>
                </div>
                </div>
      </div>
    </div>
    
    <!-- 章节内容编辑弹窗 -->
    <div class="edit-dialog-container" v-if="editDialogVisible">
      <div class="edit-dialog-overlay" @click="closeEditDialog"></div>
      <div class="edit-dialog-content">
        <div class="edit-dialog-header">
          <h3>{{ currentEditItem ? currentEditItem.title : '编辑章节内容' }}</h3>
          <button class="edit-dialog-close" @click="closeEditDialog">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="edit-dialog-body">
          <textarea 
            v-model="editContent" 
            placeholder="请输入章节内容..."
            rows="12"
            class="edit-dialog-textarea"
          ></textarea>
        </div>
        <div class="edit-dialog-footer">
          <button class="cancel-edit-dialog-btn" @click="closeEditDialog">取消</button>
          <button class="save-edit-dialog-btn" @click="saveOutlineItemContent">保存</button>
        </div>
      </div>
    </div>

    <!-- AI创作弹窗 -->
    <div class="edit-dialog-container" v-if="aiCreateDialogVisible">
      <div class="edit-dialog-overlay" @click="closeAICreateDialog"></div>
      <div class="edit-dialog-content ai-create-dialog">
        <div class="edit-dialog-header">
          <h3>AI智能创作 - {{ currentEditItem ? currentEditItem.title : '' }}</h3>
          <button class="edit-dialog-close" @click="closeAICreateDialog" :disabled="isGeneratingAI">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="edit-dialog-body">
          <div class="ai-create-section">
            <div class="ai-create-input">
              <label for="ai-prompt">创作提示词</label>
              <textarea 
                id="ai-prompt"
                v-model="aiPrompt" 
                placeholder="请输入对AI的创作要求，例如：为这部分内容创作一段专业的介绍..."
                rows="4"
                class="ai-prompt-textarea"
              ></textarea>
            </div>
            
            <div class="file-upload-section">
              <label class="file-upload-label">参考附件</label>
              <div class="file-upload-area">
                <div class="file-upload-box" v-if="!uploadedFileName">
                  <input 
                    type="file" 
                    id="reference-file" 
                    class="file-input" 
                    @change="handleFileUpload"
                    accept=".pdf"
                  />
                  <label for="reference-file" class="file-upload-button">
                    <i class="ri-upload-2-line"></i> 上传附件
                  </label>
                  <div class="file-hint">仅支持PDF格式文件</div>
                </div>
                <div class="file-preview" v-else>
                  <div class="file-info">
                    <i class="ri-file-text-line"></i>
                    <span class="file-name">{{ uploadedFileName }}</span>
                    <div class="file-actions">
                      <button class="file-remove-btn" @click="removeUploadedFile" title="移除文件">
                        <i class="ri-delete-bin-line"></i> 删除
                      </button>
                    </div>
                  </div>
                  <div v-if="isFileProcessing" class="file-processing">
                    <div class="processing-spinner"></div>
                    <span>文件处理中...</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="ai-action">
              <button class="ai-generate-btn" @click="generateAIContent" :disabled="isGeneratingAI">
                <i class="ri-ai-generate"></i> AI智能生成
                <div v-if="isGeneratingAI" class="button-spinner"></div>
              </button>
            </div>
            
            <div class="ai-create-result" v-if="showAIResult || isGeneratingAI">
              <div class="ai-result-header">
                <h4>生成内容</h4>
              </div>
              <div class="ai-result-content">
                <div v-if="isGeneratingAI" class="ai-generating">
                  <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
                <textarea 
                  v-model="aiGeneratedContent" 
                  placeholder="AI生成的内容将显示在这里..."
                  rows="8"
                  class="ai-result-textarea"
                  :disabled="isGeneratingAI"
                ></textarea>
              </div>
            </div>
          </div>
        </div>
        <div class="edit-dialog-footer">
          <button class="cancel-edit-dialog-btn" @click="closeAICreateDialog" :disabled="isGeneratingAI">取消</button>
          <button class="save-edit-dialog-btn zijing-red-btn" @click="saveAIGeneratedContent" :disabled="isGeneratingAI || !aiGeneratedContent.trim()">保存</button>
        </div>
      </div>
    </div>

    <!-- 添加目录项弹窗 -->
    <Teleport to="body">
      <div class="global-modal" v-if="addItemDialogVisible" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center; z-index: 9999;">
        <div class="global-modal-backdrop" @click="closeAddItemDialog" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></div>
        <div class="global-modal-container" style="position: relative; background-color: white; border-radius: 8px; box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); width: 90%; max-width: 500px; padding: 20px; z-index: 10000;">
          <div class="global-modal-content">
            <div class="global-modal-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #EBEEF5;">
              <h3 class="global-modal-title" style="margin: 0; font-size: 18px; color: #303133;">{{ isAddingSameLevel ? '新增同级目录' : '新增下级目录' }}</h3>
              <button class="global-modal-close" @click="closeAddItemDialog" style="background: none; border: none; font-size: 16px; color: #909399; cursor: pointer;">
                <i class="ri-close-line"></i>
              </button>
            </div>
            <div class="global-modal-body" style="margin-bottom: 20px;">
              <div class="global-form-group" style="margin-bottom: 15px;">
                <label for="new-item-title" style="display: block; margin-bottom: 8px; font-size: 14px; color: #606266;">目录标题</label>
                <input 
                  type="text" 
                  id="new-item-title" 
                  v-model="newItemTitle"
                  placeholder="请输入目录标题..."
                  class="global-form-control"
                  style="width: 100%; padding: 8px 12px; box-sizing: border-box; border: 1px solid #DCDFE6; border-radius: 4px; font-size: 14px; color: #606266;"
                />
              </div>
              
              <div class="global-form-group" v-if="parentItemInfo" style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 8px; font-size: 14px; color: #606266;">所属上级目录</label>
                <div class="global-parent-info" style="padding: 8px 12px; background-color: #F5F7FA; border-radius: 4px; font-size: 14px; color: #606266;">{{ parentItemInfo }}</div>
              </div>
            </div>
            <div class="global-modal-footer" style="display: flex; justify-content: flex-end; padding-top: 10px; border-top: 1px solid #EBEEF5;">
              <button class="global-btn global-btn-cancel" @click="closeAddItemDialog" style="padding: 8px 16px; background-color: #F5F7FA; border: 1px solid #DCDFE6; border-radius: 4px; font-size: 14px; color: #606266; margin-right: 10px; cursor: pointer;">取消</button>
              <button class="global-btn global-btn-primary" @click="saveNewOutlineItem" :disabled="!newItemTitle.trim()" style="padding: 8px 16px; background-color: #409EFF; border: 1px solid #409EFF; border-radius: 4px; font-size: 14px; color: white; cursor: pointer;">保存</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
// 引入背景图片
import bgImage from '@/assets/images/backgrounds/marketing-header-bg.jpeg'

export default {
  name: 'MarketingCampaign',
  data() {
    return {
      loaded: false,
      initialTask: '',
      
      // 调试模式
      debugMode: false,
      
      // 步骤控制 - 只保留4个步骤
      showStepCompleted: [false, false, false, false],
      
      // 第二步相关数据
      userSupplementInfo: '',
      isAnalyzing: false,
      isGeneratingTaskInfo: false,
      taskFields: [],
      fullTaskInfo: '',
      taskInfoCompleted: false,
      taskInfoSaved: false,
      aiResponse: '',
      
      // AI处理进度跟踪
      processingStep: 0,  
      processingSteps: [
        { title: '启动AI助手', completed: false, current: false },
        { title: '分析任务信息', completed: false, current: false },
        { title: '获取分析结果', completed: false, current: false },
        { title: '生成任务表单', completed: false, current: false }
      ],
      processingError: '',
      
      // 第三步相关数据
      userTaskBreakdown: '',
      isAnalyzingBreakdown: false,
      taskBreakdownResult: '',
      parsedTaskBreakdown: [],
      tasksGenerated: false,
      editingBreakdown: false,
      editableTaskBreakdown: '',
      taskBreakdownSaved: false,
      breakdownProcessingStep: 0,
      breakdownProcessingSteps: [
        { title: '启动AI助手', completed: false, current: false },
        { title: '分析任务信息', completed: false, current: false },
        { title: '编写章节内容', completed: false, current: false },
        { title: '组织文档结构', completed: false, current: false },
        { title: '生成最终内容', completed: false, current: false }
      ],
      breakdownProcessingError: '',
      
      // 产品信息相关
      productInfoVisible: false,
      
      // 第二步相关数据
      taskGoal: '',
      isAnalyzingGoal: false,
      taskGoalCompleted: false,
      optimizedGoal: '',
      
      // 常见产品方案的任务目标抽屉
      commonGoalsDrawerVisible: false,
      
      isOptimizing: false,
      optimizationProgress: 0,
      
      // 第三步相关数据
      documentStructureDrawerVisible: false,
      
      // 新增变量
      productStructure: '',
      structuredOutline: [],
      
      // 添加编辑弹窗相关数据
      editDialogVisible: false,
      currentEditItem: null,
      editContent: '',
      
      // 新增变量
      isPolishing: false,
      showPolishedResult: false,
      polishedStructure: '',
      
      // AI创作弹窗相关数据
      aiCreateDialogVisible: false,
      aiPrompt: '',
      showAIResult: false,
      aiGeneratedContent: '',
      isGeneratingAI: false,
      uploadedFile: null, // 上传的附件
      uploadedFileName: '', // 上传的附件名称
      uploadedFileContent: '', // 上传的附件内容
      isFileProcessing: false, // 附件处理中状态
      
      // 添加目录项弹窗相关数据
      addItemDialogVisible: false,
      isAddingSameLevel: false,
      parentItemInfo: '',
      newItemTitle: '',
      currentEditIndex: -1,
      documentId: '', // 添加文档ID字段，用于知识问答API
    }
  },
  computed: {
    // 判断是否可以生成完整任务信息（检查必填字段是否已填写）
    canGenerateTaskInfo() {
      if (!this.taskFields.length) return false;
      
      // 检查所有必填字段是否已填写
      return !this.taskFields.some(field => field.required && !field.value.trim());
    },
    
    // 格式化优化后的任务目标，将换行符转换为HTML
    formattedOptimizedGoal() {
      if (!this.optimizedGoal) return '';
      
      // 替换换行符为<br>标签
      return this.optimizedGoal
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.+)$/, '<p>$1</p>');
    },
    
    // 确定哪些目录项应该显示
    displayedOutlineItems() {
      // 如果没有目录项，返回空数组
      if (!this.structuredOutline.length) return [];
      
      // 筛选应该显示的目录项
      return this.structuredOutline.filter((item, index) => {
        // 第一级目录始终显示
        if (item.level === 1) return true;
        
        // 对于其他级别的目录，需要检查所有上级目录是否都处于展开状态
        let currentLevel = item.level;
        let currentIndex = index;
        
        // 从当前项往前查找，确保所有上级目录都是展开的
        while (currentLevel > 1) {
          let parentFound = false;
          
          // 向前查找上一级目录
          for (let i = currentIndex - 1; i >= 0; i--) {
            if (this.structuredOutline[i].level < currentLevel) {
              // 找到了上一级目录，检查其展开状态
              if (!this.structuredOutline[i].expanded) {
                return false; // 如果任一上级目录是折叠的，则不显示
              }
              
              // 更新为检查再上一级
              currentLevel = this.structuredOutline[i].level;
              currentIndex = i;
              parentFound = true;
              break;
            }
          }
          
          // 如果未找到上级，说明目录结构可能有问题，返回true保证显示
          if (!parentFound) return true;
        }
        
        // 所有上级目录都是展开的，显示此项
        return true;
      });
    }
  },
  mounted() {
    // 页面加载完成后执行重置场景操作
    this.clearAllStoredData(); // <--- 修改：确保完全重置

    // 移除之前的 resetScene 方法调用和 setTimeout 逻辑
    // this.resetScene(); // 移除
    // setTimeout(() => { ... }, 100); // 移除

    this.loaded = true; // 标记为已加载
  },
  methods: {
    // 移除 resetScene 方法，因为逻辑已合并到 mounted
    // resetScene() { ... },
    
    // 弹出重置确认框
    confirmReset() {
      if (confirm('确定要重置所有输入内容吗？此操作无法撤销。')) {
        this.clearAllStoredData();
        // 刷新页面以确保UI完全重置
        window.location.reload();
      }
    },
    
    // 清除除了结构化大纲以外的所有存储数据
    clearAllStoredDataExceptOutline() {
      // 先移除初始化标记，确保下次刷新时也会清除数据
      localStorage.removeItem('marketingCampaignInitialized');
      
      // 清除所有数据项 - 只保留4个步骤相关的，但不清除structuredOutline
      localStorage.removeItem('marketingCampaignInitialTask');
      localStorage.removeItem('marketingCampaignTaskGoal');
      localStorage.removeItem('marketingCampaignSupplementInfo');
      localStorage.removeItem('marketingCampaignTaskFields');
      localStorage.removeItem('marketingCampaignFullTaskInfo');
      localStorage.removeItem('marketingCampaignTaskInfoSaved');
      localStorage.removeItem('marketingCampaignStep1Completed');
      localStorage.removeItem('marketingCampaignStep2Completed');
      localStorage.removeItem('marketingCampaignStep3Completed');
      localStorage.removeItem('marketingCampaignStep4Completed');
      localStorage.removeItem('marketingCampaignAIAnalysis');
      localStorage.removeItem('marketingCampaignBreakdownResult');
      localStorage.removeItem('marketingCampaignUserBreakdown');
      localStorage.removeItem('marketingCampaignTaskBreakdownSaved');
      
      // 不移除structuredOutline
      // localStorage.removeItem('marketingCampaignStructuredOutline');
    },
    
    // 跳转到产品经理页面
    goToProductManager() {
      window.open('http://123.57.71.66:8018/ai-scenarios/product-manager', '_blank');
    },

    // 清除所有存储的数据
    clearAllStoredData() {
      // 先移除初始化标记，确保下次刷新时也会清除数据
      localStorage.removeItem('marketingCampaignInitialized');
      
      // 清除所有数据项 - 只保留4个步骤相关的
      localStorage.removeItem('marketingCampaignInitialTask');
      localStorage.removeItem('marketingCampaignTaskGoal');
      localStorage.removeItem('marketingCampaignSupplementInfo');
      localStorage.removeItem('marketingCampaignTaskFields');
      localStorage.removeItem('marketingCampaignFullTaskInfo');
      localStorage.removeItem('marketingCampaignTaskInfoSaved');
      localStorage.removeItem('marketingCampaignStep1Completed');
      localStorage.removeItem('marketingCampaignStep2Completed');
      localStorage.removeItem('marketingCampaignStep3Completed');
      localStorage.removeItem('marketingCampaignStep4Completed');
      localStorage.removeItem('marketingCampaignAIAnalysis');
      localStorage.removeItem('marketingCampaignBreakdownResult');
      localStorage.removeItem('marketingCampaignUserBreakdown');
      localStorage.removeItem('marketingCampaignBreakdownSaved');
      localStorage.removeItem('marketingCampaignStructuredOutline');
      
      // 重置所有状态 - 只保留需要的状态
      this.initialTask = '';
      this.taskGoal = '';
      this.userSupplementInfo = '';
      this.taskFields = [];
      this.fullTaskInfo = '';
      this.taskInfoCompleted = false;
      this.taskInfoSaved = false;
      this.userTaskBreakdown = '';
      this.taskBreakdownResult = '';
      this.parsedTaskBreakdown = [];
      this.tasksGenerated = false;
      this.taskBreakdownSaved = false;
      this.showStepCompleted = [false, false, false, false];
      this.productStructure = '';
      this.structuredOutline = [];
    },
    
    // 返回场景列表
    goBack() {
      this.$router.push('/ai-scenarios');
    },
    
    // 获取字段行数
    getFieldRows(label) {
      // 根据字段标签决定文本框的行数
      if (label.includes('详细说明') || label.includes('目标')) {
        return 5;
      }
      return 3;
    },
    
    // 继续到下一步
    continueToNextStep() {
      if (!this.initialTask.trim()) {
        this.$message.warning('请先输入初始任务信息');
        return;
      }
      
      localStorage.setItem('marketingCampaignInitialTask', this.initialTask);
      localStorage.setItem('marketingCampaignStep1Completed', 'true');
      
      this.showStepCompleted[0] = true;
    },
    
    // 显示常见产品方案的任务目标抽屉
    showCommonGoalsDrawer() {
      this.commonGoalsDrawerVisible = true;
    },
    
    // 隐藏常见产品方案的任务目标抽屉
    hideCommonGoalsDrawer() {
      this.commonGoalsDrawerVisible = false;
    },
    
    // 显示产品方案目录结构抽屉
    showDocumentStructureDrawer() {
      this.documentStructureDrawerVisible = true;
    },
    
    // 隐藏产品方案目录结构抽屉
    hideDocumentStructureDrawer() {
      this.documentStructureDrawerVisible = false;
    },
    
    // 保存任务信息
    saveTaskInfo() {
      if (!this.fullTaskInfo.trim()) {
        this.$message.warning('请先生成完整任务信息');
        return;
      }
      
      localStorage.setItem('marketingCampaignFullTaskInfo', this.fullTaskInfo);
      localStorage.setItem('marketingCampaignTaskInfoSaved', 'true');
      localStorage.setItem('marketingCampaignStep2Completed', 'true');
      
      this.taskInfoSaved = true;
      this.showStepCompleted[1] = true;
    },
    
    // 开始编辑任务拆解结果
    startEditingBreakdown() {
      this.editableTaskBreakdown = this.taskBreakdownResult;
      this.editingBreakdown = true;
    },
    
    // 取消编辑任务拆解结果
    cancelEditingBreakdown() {
      this.editingBreakdown = false;
    },
    
    // 保存任务拆解结果并继续
    saveTaskBreakdown() {
      try {
        // 尝试解析编辑后的JSON
        JSON.parse(this.editableTaskBreakdown);
        
        // 保存编辑结果
        this.taskBreakdownResult = this.editableTaskBreakdown;
        this.parsedTaskBreakdown = JSON.parse(this.editableTaskBreakdown);
        this.editingBreakdown = false;
        this.taskBreakdownSaved = true;
        
        // 保存到localStorage
        localStorage.setItem('marketingCampaignBreakdownResult', this.taskBreakdownResult);
        localStorage.setItem('marketingCampaignBreakdownSaved', 'true');
        localStorage.setItem('marketingCampaignStep3Completed', 'true');
        
        this.showStepCompleted[2] = true;
      } catch (error) {
        this.$message.error('JSON格式无效，请检查您的编辑');
      }
    },
    
    // 继续到步骤4
    continueToStep4FromBreakdown() {
      localStorage.setItem('marketingCampaignBreakdownSaved', 'true');
      localStorage.setItem('marketingCampaignStep3Completed', 'true');
      
      this.taskBreakdownSaved = true;
      this.showStepCompleted[2] = true;
    },
    
    // 获取AI辅助目标优化
    async getAIGoalAssistance() {
      if (this.isOptimizing || !this.taskGoal.trim()) return;
      
      this.isOptimizing = true;
      this.optimizationProgress = 0;
      
      const progressInterval = setInterval(() => {
        if (this.optimizationProgress < 90) {
          this.optimizationProgress += Math.floor(Math.random() * 10);
        }
      }, 600);
      
      try {
        // 构建提示词
        const prompt = `作为产品方案编写专家，请根据以下信息优化产品方案的任务目标，使其更加专业、全面、有说服力。

任务目标:
${this.taskGoal}

请注意:
1. 保持原始目标的核心内容，但使表达更专业、更有说服力
2. 确保优化后的目标全面涵盖产品价值、公司实力、落地路径等关键要点
3. 以清晰的结构组织内容，便于阅读和理解
4. 保持简洁，控制在300-500字之间
5. 使用中文回复`;
        
        // 准备API请求参数
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.2,
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
        let resultContent = '';
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 读取数据流
            while (true) {
              const { value, done } = await reader.read();
              
              if (done) {
                console.log("流读取完成");
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
                break;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理内容增量
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                  resultContent += deltaContent;
                  this.optimizedGoal = resultContent;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
        
        this.optimizedGoal = resultContent;
        this.taskGoalCompleted = true;
        localStorage.setItem('marketingCampaignTaskGoal', this.taskGoal);
        localStorage.setItem('marketingCampaignOptimizedGoal', this.optimizedGoal);
        
      } catch (error) {
        console.error("请求出错:", error);
        this.$message.error("请求出错，请重试");
      } finally {
        clearInterval(progressInterval);
        this.optimizationProgress = 100;
        this.isOptimizing = false;
      }
    },
    
    // 结构化产品方案目录
    structureProductOutline() {
      if (!this.productStructure.trim()) {
        this.$message({
          message: '请先输入产品方案目录结构',
          type: 'warning'
        });
        return;
      }
      
      try {
        // 分割每一行
        const lines = this.productStructure.split('\n').filter(line => line.trim());
        const result = [];
        
        // Markdown标题格式正则表达式
        const headingRegex = /^(#{1,4})\s+(.+)$/;
        
        // 检测标题级别的正则表达式
        const levelOneRegex = /^(第)?[一二三四五六七八九十]+[、：:]/;
        const levelTwoRegex = /^[（][一二三四五六七八九十]+[）][、：:]/;
        const levelThreeRegex = /^[0-9]+\.\s/;  // 改进第三级目录匹配，匹配"1. "这样的格式
        const levelFourRegex = /^[（][0-9]+[）]\s/;  // 匹配"（1） "这样的格式
        
        lines.forEach(line => {
          const trimmedLine = line.trim();
          let level = 4; // 默认级别
          let title = trimmedLine;
          
          // 先尝试匹配Markdown标题格式
          const match = trimmedLine.match(headingRegex);
          if (match) {
            // 根据#的数量确定级别
            level = match[1].length;
            title = match[2].trim(); // 获取标题文本
            console.log(`Markdown格式: "${title}" => 级别 ${level}`);
          } else if (trimmedLine.startsWith('#')) {
            // 处理可能的格式错误，如"# 标题"之间没有空格
            const hashCount = trimmedLine.match(/^#+/)[0].length;
            level = Math.min(hashCount, 4); // 最多支持4级
            title = trimmedLine.substring(hashCount).trim();
            console.log(`Markdown格式(修正): "${title}" => 级别 ${level}`);
          } else {
            // 如果不是Markdown格式，使用传统格式判断
            // 判断标题级别
            if (levelOneRegex.test(trimmedLine)) {
              level = 1;
            } else if (levelTwoRegex.test(trimmedLine)) {
              level = 2;
            } else if (levelThreeRegex.test(trimmedLine)) {
              level = 3;
            } else if (levelFourRegex.test(trimmedLine)) {
              level = 4;
            }
            console.log(`传统格式: "${trimmedLine}" => 级别 ${level}`);
          }
          
          // 创建目录项
          result.push({
            title: title,
            level: level,
            expanded: level === 1, // 默认只展开一级标题
            content: '', // 初始内容为空
          });
        });
        
        this.structuredOutline = result;
        
        // 存储到localStorage
        localStorage.setItem('marketingCampaignStructuredOutline', JSON.stringify(this.structuredOutline));
        
        // 显示成功消息
        this.$message({
          message: '目录结构化处理成功',
          type: 'success'
        });
        
        // 确保显示步骤4
        this.showStepCompleted[0] = true;
        this.showStepCompleted[1] = true;
        
        // 自动滚动到步骤4的结构化目录区域
        this.$nextTick(() => {
          const step4 = document.querySelector('.step:nth-child(4)');
          if (step4) {
            step4.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      } catch (error) {
        console.error('解析目录结构失败:', error);
        this.$message({
          message: '目录结构化处理失败，请检查输入格式',
          type: 'error'
        });
      }
    },
    
    // 切换目录项的展开/折叠状态
    toggleOutlineItem(index) {
      console.log('切换目录项展开状态', index);
      if (index >= 0 && index < this.structuredOutline.length) {
        const currentItem = this.structuredOutline[index];
        const newExpandedState = !currentItem.expanded;
        currentItem.expanded = newExpandedState;
        
        // 寻找所有子目录项
        const currentLevel = currentItem.level;
        let i = index + 1;
        
        // 如果是折叠操作，则同时折叠所有子目录
        if (!newExpandedState) {
          while (i < this.structuredOutline.length && this.structuredOutline[i].level > currentLevel) {
            this.structuredOutline[i].expanded = false;
            i++;
          }
        }
        
        // 保存状态到localStorage
        this.saveOutlineToLocalStorage();
      }
    },
    
    // 保存大纲到本地存储
    saveOutlineToLocalStorage() {
      localStorage.setItem('marketingCampaignStructuredOutline', JSON.stringify(this.structuredOutline));
    },
    
    // 编辑目录项内容
    editOutlineItemContent(item) {
      // 打开编辑弹窗
      this.currentEditItem = item;
      this.editContent = item.content || '';
      this.editDialogVisible = true;
    },
    
    // 保存编辑的内容
    saveOutlineItemContent() {
      if (this.currentEditItem) {
        // 保存内容到结构化目录
        this.currentEditItem.content = this.editContent;
        
        // 保存到localStorage
        localStorage.setItem('marketingCampaignStructuredOutline', JSON.stringify(this.structuredOutline));
        
        // 关闭弹窗
        this.closeEditDialog();
        
        // 显示成功消息
        this.$message({
          message: '章节内容已保存',
          type: 'success'
        });
      }
    },
    
    // 关闭编辑弹窗
    closeEditDialog() {
      this.editDialogVisible = false;
      this.currentEditItem = null;
      this.editContent = '';
    },
    
    // 复制结构化目录
    copyStructuredOutline() {
      const outlineText = this.structuredOutline
        .map(item => item.title)
        .join('\n');
      
      navigator.clipboard.writeText(outlineText)
        .then(() => {
          this.$message({
            message: '目录已复制到剪贴板',
            type: 'success'
          });
        })
        .catch(err => {
          console.error('复制失败:', err);
          this.$message({
            message: '复制失败，请手动复制',
            type: 'error'
          });
        });
    },
    
    // 重置结构化目录
    resetStructuredOutline() {
      this.structuredOutline = [];
      localStorage.removeItem('marketingCampaignStructuredOutline');
      this.$message({
        message: '已重置结构化目录',
        type: 'success'
      });
    },
    
    // 获取AI辅助任务拆解 - 恢复真实API调用
    async getAITaskBreakdown() {
      if (this.isAnalyzingBreakdown || !this.fullTaskInfo.trim() || !this.userTaskBreakdown.trim()) return;
      
      this.isAnalyzingBreakdown = true;
      this.tasksGenerated = false;
      this.breakdownProcessingError = '';
      
      // 初始化处理步骤
      this.breakdownProcessingStep = 0;
      this.breakdownProcessingSteps.forEach(step => {
        step.completed = false;
        step.current = false;
      });
      this.breakdownProcessingSteps[0].current = true;
      
      // 更新处理步骤
      const updateProcessingStep = (step) => {
        if (step > 0 && step <= this.breakdownProcessingSteps.length) {
          this.breakdownProcessingSteps[step - 1].completed = true;
          this.breakdownProcessingSteps[step - 1].current = false;
        }
        
        this.breakdownProcessingStep = step;
        
        if (step < this.breakdownProcessingSteps.length) {
          this.breakdownProcessingSteps[step].current = true;
        }
      };
      
      try {
        // 模拟启动AI助手完成
        setTimeout(() => updateProcessingStep(1), 800);
        
        // 系统功能列表
        const systemFeatures = `
系统功能列表（可用于内容创作的AI工具）：

文本内容创作：
(1) 文档结构撰写 - http://123.57.71.66:8018/text-creation/copywriting/document-structure
(2) 公众号文章创作 - http://123.57.71.66:8018/text-creation/new-media/wechat
(3) 产品调研报告 - http://123.57.71.66:8018/text-creation/copywriting/product-research
(4) 产品方案生成 - http://123.57.71.66:8018/text-creation/copywriting/product-solution
(5) 技术文档创作 - http://123.57.71.66:8018/text-creation/copywriting/technical-doc
(6) 营销方案创作 - http://123.57.71.66:8018/text-creation/marketing/copywriting-generator

图形内容创作：
(1) 产品示意图设计 - http://123.57.71.66:8018/image-creation/image-to-painter
(2) 文生图 - http://123.57.71.66:8018/image-creation/text-to-image

演示文稿创作：
(1) 产品方案PPT创作 - http://123.57.71.66:8018/ai-office/integration-test`;

        // 构建提示词 - 更新为章节内容编写方向
        const prompt = `你是一位资深的产品经理和技术方案撰写专家。请帮我针对以下产品方案的章节进行内容规划和编写建议。

## 完整任务信息:
${this.fullTaskInfo}

## 用户对章节内容编写的初步想法:
${this.userTaskBreakdown}

## 系统功能列表:
${systemFeatures}

请基于以上信息，为产品方案的各个章节提供详细的内容编写建议。请遵循以下要求：

1. 建议每个章节的核心内容和重点，确保内容专业、全面且有说服力
2. 为每个章节提供编写大纲和关键点
3. 关注产品方案的逻辑性和连贯性，确保各章节之间衔接自然
4. 考虑如何将各种系统功能应用于不同章节的内容编写

非常重要的规则：
1. 针对每个章节提供具体的内容编写建议，而不是空泛的指导
2. 确保建议符合产品方案的专业性要求
3. 提供章节间内容的关联性建议

请以下面的JSON格式返回结果：

\`\`\`json
[
  {
    "title": "章节类别1（如'公司介绍部分'）",
    "description": "该部分的整体编写思路和重点",
    "subtasks": [
      {
        "name": "子章节1名称",
        "description": "该子章节的详细编写建议",
        "systemFeature": "相关系统功能名称（如果适用）",
        "systemLink": "系统功能链接（如果适用）"
      },
      {
        "name": "子章节2名称",
        "description": "该子章节的详细编写建议"
      }
    ]
  },
  {
    "title": "章节类别2",
    "description": "该部分的整体编写思路和重点",
    "subtasks": [
      ...
    ]
  }
]
\`\`\`

请确保返回的JSON格式正确，可以被前端直接解析。`;

        // 准备API请求参数
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.2,
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

        // 更新处理步骤
        setTimeout(() => updateProcessingStep(2), 2500);
        setTimeout(() => updateProcessingStep(3), 5000);
        setTimeout(() => updateProcessingStep(4), 7500);

        // 处理流式响应
        let breakdownContent = '';
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
                updateProcessingStep(5); // 完成最后一步
                this.processBreakdownResult(breakdownContent);
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
                    updateProcessingStep(5); // 完成最后一步
                    this.processBreakdownResult(breakdownContent);
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理内容增量
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      breakdownContent += deltaContent;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.breakdownProcessingError = "读取流出错，请重试";
            this.isAnalyzingBreakdown = false;
          }
        };
        
        // 开始读取流
        readStream();
        
      } catch (error) {
        console.error("请求出错:", error);
        this.breakdownProcessingError = "请求出错，请重试";
        this.isAnalyzingBreakdown = false;
      }
    },
    
    // 处理任务拆解结果
    processBreakdownResult(content) {
      try {
        console.log("原始内容:", content);
        
        // 提取JSON部分
        const jsonMatch = content.match(/```json\s*([\s\S]*?)\s*```/) || 
                         content.match(/```\s*([\s\S]*?)\s*```/) ||
                         content.match(/\[\s*\{[\s\S]*\}\s*\]/);
        
        if (!jsonMatch) {
          throw new Error("未找到有效的JSON格式内容");
        }
        
        const jsonContent = jsonMatch[1] || jsonMatch[0];
        console.log("提取的JSON:", jsonContent);
        
        // 解析JSON
        const parsedData = JSON.parse(jsonContent);
        console.log("解析后的数据:", parsedData);
        
        // 保存处理结果
        this.taskBreakdownResult = JSON.stringify(parsedData);
        this.parsedTaskBreakdown = parsedData;
          this.tasksGenerated = true;
        this.isAnalyzingBreakdown = false;
          
        // 存储到localStorage
          localStorage.setItem('marketingCampaignBreakdownResult', this.taskBreakdownResult);
          localStorage.setItem('marketingCampaignUserBreakdown', this.userTaskBreakdown);
        
      } catch (error) {
        console.error("处理任务拆解结果失败:", error);
        this.breakdownProcessingError = "处理结果失败，请重试";
        this.isAnalyzingBreakdown = false;
      }
    },
    
    // 打开AI文档结构生成
    openAIDocumentStructure() {
      // 构建URL参数
      const params = new URLSearchParams();
      params.append('source', 'customer-feedback');
      
      if (this.fullTaskInfo) {
        params.append('taskInfo', this.fullTaskInfo);
      }
      
      console.log("跳转参数:", params.toString());
      
      // 打开新窗口并传递参数
      const url = `http://123.57.71.66:8018/text-creation/copywriting/document-structure?${params.toString()}`;
      window.open(url, '_blank');
    },
    
    // 复制标准产品方案目录结构
    copyStandardStructure() {
      const structureText = `## 一、公司介绍
- 公司背景与发展历程
- 核心团队与技术能力
- 行业经验与成功案例

## 二、建设必要性和合理性分析
### （一）政策背景介绍
- 相关行业政策与法规解读
- 政策支持与发展趋势

### （二）建设必要性介绍
- 行业痛点与挑战分析
- 市场需求与发展机遇

### （三）建设合理性介绍
- 技术可行性分析
- 投资回报评估
- 竞争优势对比

## 三、建设目标
- 总体目标与愿景
- 阶段性目标与关键指标
- 预期成效与价值

## 四、建设内容
### （一）产品技术架构
- 整体架构设计
- 核心技术说明
- 系统安全保障

### （二）产品功能架构及核心功能模块
- 功能模块详解
- 用户交互流程
- 特色功能与创新点

### （三）实施落地路线
- 项目实施计划与里程碑
- 资源配置与分工
- 风险管控措施

### （四）培训体系设计
- 培训计划与课程设置
- 培训方式与工具
- 效果评估机制

### （五）售后服务体系
- 服务等级与响应机制
- 问题处理流程
- 持续优化与升级支持

## 五、产品清单及报价
- 产品配置清单
- 服务项目明细
- 价格方案与付款计划`;
      
      navigator.clipboard.writeText(structureText)
        .then(() => {
          this.$message({
            message: '产品方案目录结构（Markdown格式）已复制到剪贴板',
            type: 'success'
          });
        })
        .catch(err => {
          console.error('复制失败:', err);
          this.$message({
            message: '复制失败，请手动复制',
            type: 'error'
          });
        });
    },
    
    // 润色产品方案目录
    async polishProductOutline() {
      if (!this.productStructure.trim()) {
        this.$message.warning('请先输入产品方案目录内容');
        return;
      }
      
      this.isPolishing = true;
      this.showPolishedResult = true;  // 显示润色结果文本框
      this.polishedStructure = ''; // 清空之前的润色结果
      
      try {
        // 构建提示词
        const prompt = `你是一位专业的产品文档撰写专家。请帮我润色优化以下产品方案的目录结构，使其更加专业、完整和具有逻辑性。

请注意以下要求：
1. 保持原有目录的核心内容和主要结构，并适当完善和补充
2. 使用标准的Markdown标题格式，一级标题使用#，二级标题使用##，三级标题使用###，四级标题使用####
3. 确保目录层次清晰，结构合理
4. 使用简洁、专业的语言描述每个标题
5. 不要添加额外的解释或说明文字，直接输出Markdown格式的目录结构

以下是原始目录结构：

${this.productStructure}

请直接输出润色后的Markdown格式目录，不要包含任何解释、引言或结论。`;
        
        // 请求参数
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.1,
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
        while (true) {
          const { value, done } = await reader.read();
          
          if (done) {
            console.log("润色完成，流读取完成");
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
                break;
              }
              
              try {
                const data = JSON.parse(dataStr);
                
                // 处理内容增量
                if (data.choices && data.choices[0]?.delta?.content) {
                  const deltaContent = data.choices[0].delta.content;
                  // 将内容实时添加到polishedStructure中
                  this.polishedStructure += deltaContent;
                }
              } catch (error) {
                console.error("解析数据出错:", error);
              }
            }
          }
        }
        
        // 完成后显示成功消息
        if (this.polishedStructure.trim()) {
          this.$message.success('产品方案目录润色成功');
          
          // 自动滚动到润色结果文本框
          this.$nextTick(() => {
            const textarea = document.querySelector('.polished-input');
            if (textarea) {
              textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
              // 聚焦到文本框
              textarea.focus();
            }
          });
        } else {
          this.$message.warning('润色结果为空，请重试');
          this.showPolishedResult = false; // 隐藏润色结果框
        }
      } catch (error) {
        console.error("润色产品方案目录失败:", error);
        this.$message.error(`润色失败: ${error.message}`);
        this.showPolishedResult = false; // 出错时隐藏润色结果框
      } finally {
        this.isPolishing = false;
      }
    },
    structurePolishedOutline() {
      if (!this.polishedStructure.trim()) {
        this.$message({
          message: '请先输入润色后的目录结构',
          type: 'warning'
        });
        return;
      }
      
      try {
        // 分割每一行
        const lines = this.polishedStructure.split('\n').filter(line => line.trim());
        const result = [];
        
        // Markdown标题格式正则表达式
        const headingRegex = /^(#{1,4})\s+(.+)$/;
        
        console.log('开始分析目录结构：');
        
        // 根据Markdown格式判断级别
        lines.forEach((line, idx) => {
          const trimmedLine = line.trim();
          let level = 0;
          let title = trimmedLine;
          
          // 匹配Markdown标题格式 (#, ##, ###, ####)
          const match = trimmedLine.match(headingRegex);
          if (match) {
            // 根据#的数量确定级别
            level = match[1].length;
            title = match[2].trim(); // 获取标题文本
            console.log(`识别级别: 行 ${idx+1} "${title}" => 级别 ${level}`);
          } else if (trimmedLine.startsWith('#')) {
            // 处理可能的格式错误，如"# 标题"之间没有空格
            const hashCount = trimmedLine.match(/^#+/)[0].length;
            level = Math.min(hashCount, 4); // 最多支持4级
            title = trimmedLine.substring(hashCount).trim();
            console.log(`识别级别(修正): 行 ${idx+1} "${title}" => 级别 ${level}`);
          } else {
            // 如果没有Markdown格式，则尝试使用原来的逻辑
            console.log(`非Markdown格式: "${trimmedLine}"`);
            
            // 使用原有的规则进行判断 (省略具体实现)
            level = 4; // 默认为最低级别
          }
          
          // 确保有有效的级别
          if (level === 0) {
            level = 4; // 未识别的默认为最低级别
          }
          
          // 创建目录项
          result.push({
            title: title,
            level: level,
            expanded: level === 1, // 默认只展开一级标题
            content: '', // 初始内容为空
          });
        });
        
        this.structuredOutline = result;
        
        // 存储到localStorage
        localStorage.setItem('marketingCampaignStructuredOutline', JSON.stringify(this.structuredOutline));
        
        // 显示成功消息
        this.$message({
          message: '目录结构化处理成功',
          type: 'success'
        });
        
        // 确保显示步骤4
        this.showStepCompleted[0] = true;
        this.showStepCompleted[1] = true;
        
        // 自动滚动到步骤4的结构化目录区域
        this.$nextTick(() => {
          const step4 = document.querySelector('.step:nth-child(4)');
          if (step4) {
            step4.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      } catch (error) {
        console.error('解析目录结构失败:', error);
        this.$message({
          message: '目录结构化处理失败，请检查输入格式',
          type: 'error'
        });
      }
    },
    closePolishedResult() {
      this.showPolishedResult = false;
      this.polishedStructure = '';
    },
    aiCreateOutlineContent(item, index) {
      // 打开AI创作弹窗
      this.currentEditItem = item;
      this.aiCreateDialogVisible = true;
      this.showAIResult = false;
      this.aiGeneratedContent = '';
      
      // 如果已有内容，自动生成优化提示词
      if (item.content && item.content.trim()) {
        this.aiPrompt = `请优化以下"${item.title}"部分的内容，使其更加专业、条理清晰且内容丰富：\n\n${item.content}`;
      } else {
        // 根据标题自动生成合适的提示词
        this.aiPrompt = `请为产品方案中的"${item.title}"部分创作专业的内容，要求：\n1. 内容专业、准确、全面\n2. 语言流畅，逻辑清晰\n3. 结构合理，层次分明\n4. 根据标题特点，突出重点内容`;
      }
    },
    
    // 生成AI内容
    generateAIContent() {
      if (!this.aiPrompt.trim() || this.isGeneratingAI) return;
      
      this.isGeneratingAI = true;
      this.showAIResult = true;
      this.aiGeneratedContent = '';
      
      // 禁用关闭按钮和遮罩层点击
      const closeBtn = document.querySelector('.edit-dialog-close');
      if (closeBtn) closeBtn.setAttribute('disabled', 'disabled');
      
      const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
      const saveBtn = document.querySelector('.save-edit-dialog-btn');
      if (cancelBtn) cancelBtn.style.opacity = "0.5";
      if (saveBtn) saveBtn.style.opacity = "0.5";
      
      // 构建API请求参数
      let requestURL = '/api/v1/v1/deepseek_volcano/chat';
      let requestData;
      let headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      };
      
      // 如果有上传文件且有文档ID，使用知识问答API
      if (this.uploadedFileName && this.documentId) {
        requestURL = `/api/knowledge/chat?documentId=${this.documentId}&question=${encodeURIComponent(this.aiPrompt)}`;
        
        // 知识问答API使用GET请求，不需要设置请求体
        fetch(requestURL, {
          method: 'GET',
          headers: headers
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP错误 ${response.status}`);
          }
          
          // 处理流式响应
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let buffer = '';
          
          // 递归函数处理读取
          const processStream = () => {
            reader.read().then(({ value, done }) => {
              if (done) {
                console.log("知识问答流读取完成");
                this.isGeneratingAI = false;
                
                // 启用按钮
                const closeBtn = document.querySelector('.edit-dialog-close');
                if (closeBtn) closeBtn.removeAttribute('disabled');
                
                const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
                const saveBtn = document.querySelector('.save-edit-dialog-btn');
                if (cancelBtn) cancelBtn.style.opacity = "1";
                if (saveBtn) saveBtn.style.opacity = "1";
                
                return;
              }
              
              // 解码并处理新数据
              buffer += decoder.decode(value, { stream: true });
              
              // 处理SSE数据
              const lines = buffer.split('\n\n');
              buffer = lines.pop() || '';
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const dataStr = line.slice(6);
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理内容增量
                    if (data.content) {
                      this.aiGeneratedContent += data.content;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                } else if (line.startsWith('event: end')) {
                  // 处理结束事件
                  this.isGeneratingAI = false;
                  
                  // 启用按钮
                  const closeBtn = document.querySelector('.edit-dialog-close');
                  if (closeBtn) closeBtn.removeAttribute('disabled');
                  
                  const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
                  const saveBtn = document.querySelector('.save-edit-dialog-btn');
                  if (cancelBtn) cancelBtn.style.opacity = "1";
                  if (saveBtn) saveBtn.style.opacity = "1";
                  
                  return;
                }
              }
              
              // 继续读取流
              processStream();
            })
            .catch(error => {
              console.error("读取流出错:", error);
              this.isGeneratingAI = false;
              
              // 启用按钮
              const closeBtn = document.querySelector('.edit-dialog-close');
              if (closeBtn) closeBtn.removeAttribute('disabled');
              
              const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
              const saveBtn = document.querySelector('.save-edit-dialog-btn');
              if (cancelBtn) cancelBtn.style.opacity = "1";
              if (saveBtn) saveBtn.style.opacity = "1";
            });
          };
          
          // 开始读取流
          processStream();
        })
        .catch(error => {
          console.error("知识问答API调用失败:", error);
          this.$message.error("生成内容失败，请重试");
          this.isGeneratingAI = false;
          
          // 启用按钮
          const closeBtn = document.querySelector('.edit-dialog-close');
          if (closeBtn) closeBtn.removeAttribute('disabled');
          
          const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
          const saveBtn = document.querySelector('.save-edit-dialog-btn');
          if (cancelBtn) cancelBtn.style.opacity = "1";
          if (saveBtn) saveBtn.style.opacity = "1";
        });
      } else {
        // 使用普通的大模型API
        // 构建提示词
        let prompt = this.aiPrompt;
        
        // 如果有上传文件内容但没有文档ID（本地读取的内容）
        if (this.uploadedFileContent && !this.documentId) {
          prompt = `参考以下附件内容，${this.aiPrompt}\n\n附件内容(${this.uploadedFileName}):\n${this.uploadedFileContent}`;
        }
        
        requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.2,
          max_tokens: 2000
        };

        // 发送请求到后端API
        fetch(requestURL, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(requestData)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP错误 ${response.status}`);
          }
          
          // 处理流式响应
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let buffer = '';
          
          // 递归函数处理读取
          const processStream = () => {
            reader.read().then(({ value, done }) => {
              if (done) {
                console.log("流读取完成");
                this.isGeneratingAI = false;
                
                // 启用按钮
                const closeBtn = document.querySelector('.edit-dialog-close');
                if (closeBtn) closeBtn.removeAttribute('disabled');
                
                const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
                const saveBtn = document.querySelector('.save-edit-dialog-btn');
                if (cancelBtn) cancelBtn.style.opacity = "1";
                if (saveBtn) saveBtn.style.opacity = "1";
                
                return;
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
                    this.isGeneratingAI = false;
                    
                    // 启用按钮
                    const closeBtn = document.querySelector('.edit-dialog-close');
                    if (closeBtn) closeBtn.removeAttribute('disabled');
                    
                    const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
                    const saveBtn = document.querySelector('.save-edit-dialog-btn');
                    if (cancelBtn) cancelBtn.style.opacity = "1";
                    if (saveBtn) saveBtn.style.opacity = "1";
                    
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理内容增量
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      this.aiGeneratedContent += deltaContent;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
              
              // 继续读取流
              processStream();
            })
            .catch(error => {
              console.error("读取流出错:", error);
              this.isGeneratingAI = false;
              
              // 启用按钮
              const closeBtn = document.querySelector('.edit-dialog-close');
              if (closeBtn) closeBtn.removeAttribute('disabled');
              
              const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
              const saveBtn = document.querySelector('.save-edit-dialog-btn');
              if (cancelBtn) cancelBtn.style.opacity = "1";
              if (saveBtn) saveBtn.style.opacity = "1";
            });
          };
          
          // 开始读取流
          processStream();
        })
        .catch(error => {
          console.error("生成AI内容失败:", error);
          this.$message.error("生成内容失败，请重试");
          this.isGeneratingAI = false;
          
          // 启用按钮
          const closeBtn = document.querySelector('.edit-dialog-close');
          if (closeBtn) closeBtn.removeAttribute('disabled');
          
          const cancelBtn = document.querySelector('.cancel-edit-dialog-btn');
          const saveBtn = document.querySelector('.save-edit-dialog-btn');
          if (cancelBtn) cancelBtn.style.opacity = "1";
          if (saveBtn) saveBtn.style.opacity = "1";
        });
      }
    },
    
    // 保存AI生成的内容
    saveAIGeneratedContent() {
      if (this.currentEditItem && this.aiGeneratedContent.trim()) {
        // 保存内容到结构化目录
        this.currentEditItem.content = this.aiGeneratedContent;
        
        // 保存到localStorage
        localStorage.setItem('marketingCampaignStructuredOutline', JSON.stringify(this.structuredOutline));
        
        // 关闭弹窗
        this.closeAICreateDialog();
        
        // 显示成功消息
        this.$message({
          message: 'AI创作内容已保存',
          type: 'success'
        });
      }
    },
    
    // 关闭AI创作弹窗
    closeAICreateDialog() {
      this.aiCreateDialogVisible = false;
      this.currentEditItem = null;
      this.aiPrompt = '';
      this.aiGeneratedContent = '';
      this.showAIResult = false;
      this.uploadedFile = null;
      this.uploadedFileName = '';
      this.uploadedFileContent = '';
      this.documentId = ''; // 添加清除文档ID
      this.isFileProcessing = false;
    },
    
    // 处理文件上传
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      this.uploadedFile = file;
      this.uploadedFileName = file.name;
      this.isFileProcessing = true;
      
      // 检查文件类型和大小
      const fileExtension = file.name.split('.').pop().toLowerCase();
      const isValidType = fileExtension === "pdf";
      const isLessThan2M = file.size / 1024 / 1024 < 2;
      
      if (!isValidType) {
        this.$message.error('只支持PDF格式文件');
        this.removeUploadedFile();
        return;
      }
      
      if (!isLessThan2M) {
        this.$message.error('文件大小不能超过2MB');
        this.removeUploadedFile();
        return;
      }
      
      // 创建FormData对象
      const formData = new FormData();
      formData.append('file', file);
      
      // 发送到后端API
      fetch('/api/knowledge/upload', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('文件上传失败');
        }
        return response.json();
      })
      .then(data => {
        if (data.success) {
          this.$message.success('附件上传成功');
          this.documentId = data.documentId; // 保存文档ID
          this.uploadedFileContent = '已成功上传并解析文件内容，AI将参考该内容进行创作';
        } else {
          throw new Error(data.message || '文件上传失败');
        }
      })
      .catch(error => {
        console.error('上传文件失败:', error);
        this.$message.error("上传PDF文件失败，请确保文件格式正确且不超过2MB");
        this.removeUploadedFile();
      })
      .finally(() => {
        this.isFileProcessing = false;
      });
    },
    
    // 移除上传的文件
    removeUploadedFile() {
      this.uploadedFile = null;
      this.uploadedFileName = '';
      this.uploadedFileContent = '';
      this.documentId = ''; // 清空文档ID
      
      // 重置文件输入框
      const fileInput = document.getElementById('reference-file');
      if (fileInput) {
        fileInput.value = '';
      }
    },
    
    // 添加同级目录项
    addSameLevelOutlineItem(index) {
      console.log('添加同级目录', index);
      const currentItem = this.structuredOutline[index];
      
      // 显示提示消息，帮助调试
      this.$message.info(`正在添加"${currentItem.title}"的同级目录`);
      
      this.currentEditIndex = index;
      this.isAddingSameLevel = true;
      this.newItemTitle = '';
      this.parentItemInfo = currentItem.level === 1 ? '一级目录' : `"${this.getParentTitle(currentItem)}"下的${this.getLevelName(currentItem.level)}`;
      this.addItemDialogVisible = true;
      
      // 强制DOM更新后聚焦输入框
      this.$nextTick(() => {
        const inputEl = document.getElementById('new-item-title');
        if (inputEl) {
          console.log('聚焦到输入框');
          inputEl.focus();
        } else {
          console.log('未找到输入框元素');
        }
      });
    },
    
    // 添加下级目录项
    addSubLevelOutlineItem(index) {
      console.log('添加下级目录', index);
      const currentItem = this.structuredOutline[index];
      
      // 显示提示消息，帮助调试
      this.$message.info(`正在添加"${currentItem.title}"的下级目录`);
      
      this.currentEditIndex = index;
      this.isAddingSameLevel = false;
      this.newItemTitle = '';
      this.parentItemInfo = `"${currentItem.title}"`;
      this.addItemDialogVisible = true;
      
      // 如果当前项未展开，自动展开
      if (!currentItem.expanded) {
        currentItem.expanded = true;
        this.saveOutlineToLocalStorage();
      }
      
      // 强制DOM更新后聚焦输入框
      this.$nextTick(() => {
        const inputEl = document.getElementById('new-item-title');
        if (inputEl) {
          console.log('聚焦到输入框');
          inputEl.focus();
        } else {
          console.log('未找到输入框元素');
        }
      });
    },
    
    // 获取父级目录标题
    getParentTitle(item) {
      // 根据当前项的级别查找其父级目录
      const level = item.level;
      const index = this.structuredOutline.indexOf(item);
      
      if (level === 1 || index === -1) return ''; // 一级目录没有父级
      
      // 从当前项往前查找，直到找到级别小于当前级别的项
      for (let i = index - 1; i >= 0; i--) {
        if (this.structuredOutline[i].level < level) {
          return this.structuredOutline[i].title;
        }
      }
      
      return '';
    },
    
    // 获取级别名称
    getLevelName(level) {
      switch (level) {
        case 1: return '一级目录';
        case 2: return '二级目录';
        case 3: return '三级目录';
        case 4: return '四级目录';
        default: return '目录';
      }
    },
    
    // 保存新增的目录项
    saveNewOutlineItem() {
      if (!this.newItemTitle.trim()) return;
      
      const index = this.currentEditIndex;
      const currentItem = this.structuredOutline[index];
      
      // 创建新的目录项
      const newItem = {
        title: this.newItemTitle,
        level: this.isAddingSameLevel ? currentItem.level : Math.min(currentItem.level + 1, 4), // 最大支持4级目录
        expanded: false,
        content: '',
      };
      
      // 确定插入位置
      let insertIndex = index + 1;
      
      if (!this.isAddingSameLevel) {
        // 如果是添加子级目录，需要找到合适的插入位置
        // 查找当前目录项的最后一个子项的位置
        const currentLevel = currentItem.level;
        const nextLevel = currentLevel + 1;
        
        for (let i = index + 1; i < this.structuredOutline.length; i++) {
          if (this.structuredOutline[i].level <= currentLevel) {
            // 找到了同级或上级，插入到这里前面
            insertIndex = i;
            break;
          }
          
          // 继续查找
          insertIndex = i + 1;
        }
      } else {
        // 如果是添加同级目录，需要找到当前目录及其所有子目录的最后一个位置
        const currentLevel = currentItem.level;
        
        for (let i = index + 1; i < this.structuredOutline.length; i++) {
          if (this.structuredOutline[i].level <= currentLevel) {
            // 找到了同级或上级，插入到这里前面
            insertIndex = i;
            break;
          }
          
          // 继续查找
          insertIndex = i + 1;
        }
      }
      
      // 插入新的目录项
      this.structuredOutline.splice(insertIndex, 0, newItem);
      
      // 保存到localStorage
      localStorage.setItem('marketingCampaignStructuredOutline', JSON.stringify(this.structuredOutline));
      
      // 关闭弹窗
      this.closeAddItemDialog();
      
      // 显示成功消息
      this.$message({
        message: '目录项已添加',
        type: 'success'
      });
    },
    
    // 关闭添加目录项弹窗
    closeAddItemDialog() {
      this.addItemDialogVisible = false;
      this.isAddingSameLevel = false;
      this.parentItemInfo = '';
      this.newItemTitle = '';
      this.currentEditIndex = -1;
    },
    
    removeOutlineItem(index) {
      // 删除指定索引的目录项及其所有子项
      if (confirm('确定要删除此目录项吗？此操作将同时删除其所有子目录项。')) {
        const currentItem = this.structuredOutline[index];
        const currentLevel = currentItem.level;
        
        // 找出要删除的项的范围
        let deleteCount = 1; // 至少删除当前项
        for (let i = index + 1; i < this.structuredOutline.length; i++) {
          if (this.structuredOutline[i].level <= currentLevel) {
            break; // 遇到同级或更高级的项，停止
          }
          deleteCount++; // 继续计数子项
        }
        
        // 删除这些项
        this.structuredOutline.splice(index, deleteCount);
        
        // 如果数组为空，清空本地存储
        if (this.structuredOutline.length === 0) {
          localStorage.removeItem('marketingCampaignStructuredOutline');
          this.$message.success('目录已清空');
        } else {
          // 否则更新本地存储
          this.saveOutlineToLocalStorage();
          this.$message.success('目录项已删除');
        }
      }
    },
    exportDocument() {
      // 检查是否有内容可以导出
      if (this.structuredOutline.length === 0) {
        this.$message.warning('没有内容可导出，请先创建产品方案目录');
        return;
      }

      // 创建一个新的文档内容
      let docContent = `<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
      <head>
      <meta charset='utf-8'>
      <title>产品方案文档</title>
      </head>
      <body>
      <h1 style="text-align: center;">产品方案文档</h1>
      `;

      // 遍历所有目录项
      this.structuredOutline.forEach(item => {
        // 根据目录级别设置不同的标题级别
        let headingLevel = item.level + 1;
        if (headingLevel > 6) headingLevel = 6; // HTML最大标题级别为h6

        docContent += `<h${headingLevel}>${item.title}</h${headingLevel}>\n`;
        
        // 如果有内容，添加内容段落
        if (item.content) {
          // 将换行符转换为HTML换行
          const formattedContent = item.content.replace(/\n/g, '<br>');
          docContent += `<p>${formattedContent}</p>\n`;
        }
      });

      // 结束文档
      docContent += `</body></html>`;

      // 创建Blob
      const blob = new Blob([docContent], { type: 'application/msword' });
      
      // 创建下载链接
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = '产品方案文档.doc'; // 设置文件名
      
      // 点击链接下载文件
      document.body.appendChild(link);
      link.click();
      
      // 清理
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
      
      this.$message.success('文档导出成功');
    },
    createOutlineWithAI(index) {
      // 获取当前目录项
      const currentItem = this.structuredOutline[index];
      
      // 显示加载状态
      this.$message.loading({ content: 'AI正在创作内容...', duration: 0, key: 'aiCreating' });
      
      // 这里是AI创作的模拟实现，实际项目中应该调用后端API
      setTimeout(() => {
        // 模拟AI生成内容
        let aiGeneratedContent = '';
        
        // 根据目录项标题生成不同的内容
        if (currentItem.title.includes('背景')) {
          aiGeneratedContent = '本产品旨在解决用户在日常工作中遇到的效率问题。通过市场调研发现，当前市场缺乏简单易用且功能完善的解决方案。';
        } else if (currentItem.title.includes('目标')) {
          aiGeneratedContent = '1. 提升用户工作效率30%\n2. 降低操作复杂度\n3. 优化用户体验\n4. 增强产品竞争力';
        } else if (currentItem.title.includes('功能')) {
          aiGeneratedContent = '核心功能包括：\n- 智能数据分析\n- 自动化工作流\n- 多平台数据同步\n- 实时协作编辑';
        } else if (currentItem.title.includes('方案')) {
          aiGeneratedContent = '实施方案分为三个阶段：\n第一阶段：需求分析与原型设计\n第二阶段：核心功能开发与测试\n第三阶段：优化与上线';
        } else {
          aiGeneratedContent = '这是AI自动生成的内容，基于"' + currentItem.title + '"主题。在实际项目中，这里将通过调用AI接口生成更加智能和定制化的内容。';
        }
        
        // 更新内容
        this.structuredOutline[index].content = aiGeneratedContent;
        
        // 保存到本地存储
        localStorage.setItem('structuredOutline', JSON.stringify(this.structuredOutline));
        
        // 关闭加载提示并显示成功消息
        this.$message.success({ content: 'AI创作完成！', key: 'aiCreating' });
      }, 1500); // 模拟API调用延迟
    },
    findParentIndex(index) {
      const currentItem = this.structuredOutline[index];
      const currentLevel = currentItem.level;
      
      // 如果是一级目录，没有父级
      if (currentLevel === 1) return -1;
      
      // 从当前项向前查找，找到第一个级别比它小的项
      for (let i = index - 1; i >= 0; i--) {
        if (this.structuredOutline[i].level < currentLevel) {
          return i;
        }
      }
      
      // 未找到父级（不应该发生）
      return -1;
    },
    
    // 检查目录项是否有子项
    hasChildren(realIndex) {
      const index = this.getActualIndex(realIndex);
      
      // 如果是数组的最后一项，则肯定没有子项
      if (index >= this.structuredOutline.length - 1) return false;
      
      const currentLevel = this.structuredOutline[index].level;
      const nextItem = this.structuredOutline[index + 1];
      
      // 如果下一项的级别比当前项高，则有子项
      return nextItem && nextItem.level > currentLevel;
    },
    
    // 获取显示项在原始数组中的实际索引
    getActualIndex(displayIndex) {
      // 如果使用的是原始数组来显示，则索引相同
      if (this.displayedOutlineItems === this.structuredOutline) {
        return displayIndex;
      }
      
      // 否则需要查找实际索引
      const displayItem = this.displayedOutlineItems[displayIndex];
      return this.structuredOutline.findIndex(item => item === displayItem);
    },
    
    // 保存目录到本地存储
    saveOutlineToLocalStorage() {
      localStorage.setItem('marketingCampaignStructuredOutline', JSON.stringify(this.structuredOutline));
    }
  }
}
</script>

<style scoped>
.marketing-campaign-container {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #333;
  line-height: 1.6;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
}

.page-header {
  position: relative;
  padding: 40px 0;
  margin-bottom: 40px;
  border-bottom: 1px solid #eee;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  width: 100%;
  color: #fff;
  min-height: 260px;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.header-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('../../../public/backgrounds/customer-feedback-bg.jpeg');
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  z-index: 0;
}

.header-bg-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3); /* 减小蒙版透明度 */
  z-index: 1; /* 确保叠加层位于内容之下 */
}

.page-header .container {
  position: relative;
  z-index: 2; /* 确保内容在叠加层之上 */
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
  position: relative; /* 添加相对定位，作为子元素绝对定位的参考 */
}

.back-link {
  display: flex;
  align-items: center;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  position: absolute; /* 使用绝对定位 */
  left: 0; /* 靠左对齐 */
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%); /* 垂直居中 */
}

.back-link:hover {
  color: #ffcccc;
}

.back-link i {
  margin-right: 5px;
}

.reset-button {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background: none;
  border: 1px solid #fff;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  position: absolute; /* 使用绝对定位 */
  right: 0; /* 靠右对齐 */
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%); /* 垂直居中 */
}

.reset-button:hover {
  border-color: #ffcccc;
  color: #ffcccc;
}

.reset-button i {
  margin-right: 5px;
}

.main-title {
  font-size: 36px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 16px;
  text-align: center;
}

.scenario-category {
  display: inline-block;
  font-size: 18px;
  font-weight: normal;
  color: #fff;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 50px;
  margin-left: 15px;
  vertical-align: middle;
}

.section {
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #89253e;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.section-title i {
  margin-right: 10px;
  font-size: 26px;
}

.role-card,
.task-card,
.deadline-card,
.ai-workflow-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 25px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.role-card:hover,
.task-card:hover,
.deadline-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.role-card {
  display: flex;
  align-items: flex-start;
}

.role-avatar {
  flex: 0 0 33.33%;
  max-width: 33.33%;
  overflow: hidden;
  margin-right: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  border: 2px solid #fff;
  background-color: #fff;
  height: auto;
  display: flex;
  align-items: center;
}

.role-avatar img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
}

.role-info {
  flex: 0 0 calc(66.67% - 20px);
  max-width: calc(66.67% - 20px);
}

.role-info h3 {
  font-size: 22px;
  color: #333;
  margin: 0 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.job-info-btn {
  font-size: 14px;
  background-color: #f8f9fd;
  border: 1px solid #e1e4e8;
  color: #555;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  margin-left: 15px;
  transition: all 0.2s ease;
}

.job-info-btn:hover {
  background-color: #e6e8ef;
  border-color: #cfd3da;
}

.job-info-btn i {
  margin-right: 5px;
}

.task-content,
.role-info p {
  color: #555;
  font-size: 16px;
  line-height: 1.7;
}

.task-content ul {
  padding-left: 20px;
  margin: 15px 0;
}

.task-content li {
  margin-bottom: 8px;
}

.deadline-card {
  background-color: #fff9f9;
  border-left: 4px solid #e74c3c;
}

.deadline-content {
  display: flex;
  align-items: flex-start;
}

.deadline-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background-color: #e74c3c;
  border-radius: 50%;
  margin-right: 20px;
  flex-shrink: 0;
}

.deadline-icon i {
  font-size: 28px;
  color: #fff;
}

.deadline-info h3 {
  font-size: 18px;
  margin: 0 0 10px;
  color: #e74c3c;
}

.deadline-info p {
  color: #555;
  font-size: 16px;
  line-height: 1.7;
  margin: 0;
}

.ai-workflow-card {
  background-color: #f8f9fd;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  border: 1px solid #e6e9ed;
  overflow: hidden;
}

.ai-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;  /* 增加间距 */
  padding: 25px;  /* 增加内边距 */
  background: linear-gradient(135deg, #89253e 0%, #a93e4f 100%);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.ai-icon {
  background-color: #ffffff;
  color: #89253e;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  font-size: 22px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ai-title {
  flex-grow: 1;
}

.ai-title h3 {
  color: #ffffff;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 5px 0;
}

.ai-title p {
  font-size: 18px !important;  /* 增加字体大小 */
  line-height: 1.8 !important;  /* 调整行高 */
  color: #ffffff;
  margin: 0;
  opacity: 0.9;
}

.workflow-steps {
  padding: 25px;
}

.workflow-steps {
  margin: 30px 0;
}

.step {
  display: flex;
  margin-bottom: 30px;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  font-weight: bold;
  border-radius: 50%;
  flex-shrink: 0;
  margin-right: 20px;
}

.step .step-content {
  flex-grow: 1;
}

.step .step-content h4 {
  font-size: 18px;
  margin: 0 0 10px;
  color: #89253e;
}

.step .step-content p {
  margin-top: 0;
  margin-bottom: 15px;
  color: #555;
}

.ai-results-section {
  margin-top: 40px;
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.ai-results-section h3 {
  font-size: 20px;
  color: #3a6186;
  margin: 0 0 15px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin: 20px 0;
}

.result-item {
  background-color: #f8f9fd;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.result-item i {
  font-size: 40px;
  color: #3a6186;
  margin-bottom: 15px;
}

.result-item h4 {
  font-size: 18px;
  margin: 0 0 10px;
  color: #3a6186;
}

.result-item p {
  color: #555;
  font-size: 15px;
  line-height: 1.5;
  margin: 0;
}

.conclusion {
  margin-top: 25px;
  padding: 15px;
  background-color: #f0f7ff;
  border-radius: 6px;
  color: #4a6baf;
  font-size: 16px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .role-card {
    flex-direction: column;
  }
  
  .role-avatar {
    margin: 0 auto 20px;
  }
  
  .deadline-content {
    flex-direction: column;
  }
  
  .deadline-icon {
    margin: 0 auto 20px;
  }
  
  .deadline-info {
    text-align: center;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
  
  .header-actions {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .reset-button {
    margin-top: 10px;
  }
}

.input-container {
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #e1e4e8;
  overflow: hidden;
  margin-top: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.task-input {
  width: 100%;
  padding: 15px;
  border: none;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  resize: vertical;
  min-height: 120px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.task-input:focus {
  outline: none;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f8f9fd;
  border-top: 1px solid #e1e4e8;
}

.character-count {
  font-size: 13px;
  color: #666;
}

.character-count.warning {
  color: #e74c3c;
}

.save-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.save-btn i {
  margin-right: 5px;
}

.saved-message {
  display: flex;
  align-items: center;
  margin-top: 15px;
  padding: 10px 15px;
  background-color: #fff8eb;
  border-radius: 4px;
  color: #e6b980;
  font-weight: 500;
}

.saved-message i {
  margin-right: 8px;
  font-size: 18px;
}

/* 新增的第二步相关样式 */
.button-container {
  margin: 15px 0;
  display: flex;
  justify-content: space-between;
}

.ai-assist-btn {
  display: flex;
  align-items: center;
  padding: 10px 18px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.ai-assist-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.ai-assist-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.ai-assist-btn i {
  margin-right: 8px;
  font-size: 18px;
}

.reference-btn {
  display: flex;
  align-items: center;
  padding: 10px 18px;
  background: #f8f9fd;
  border: 1px solid #e1e4e8;
  color: #333;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.reference-btn:hover {
  background: #f0f2f8;
  border-color: #c8cdd5;
}

.reference-btn i {
  margin-right: 8px;
  font-size: 18px;
}

.drawer-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #aaa;
  cursor: pointer;
  transition: color 0.3s;
}

.drawer-close:hover {
  color: #89253e;
}

.ai-analysis-section {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fd;
  border-radius: 8px;
  border: 1px solid #e0e4ea;
}

.analyzing-indicator {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 30px 0;
}

.analyzing-indicator p {
  margin-top: 15px;
  color: #555;
  font-size: 15px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #89253e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.task-fields-form h5 {
  font-size: 17px;
  color: #3a6186;
  margin: 0 0 15px;
}

.task-field {
  margin-bottom: 15px;
}

.task-field label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #444;
}

.task-field .required {
  color: #e74c3c;
  margin-left: 4px;
}

.task-field textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
  line-height: 1.5;
  resize: vertical;
  font-family: inherit;
  background-color: #fff;
}

.task-field textarea:focus {
  outline: none;
  border-color: #3a6186;
  box-shadow: 0 0 0 2px rgba(58, 97, 134, 0.1);
}

.generate-btn {
  display: flex;
  align-items: center;
  padding: 10px 18px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.generate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.generate-btn i {
  margin-right: 8px;
}

.full-task-info {
  margin-top: 25px;
}

.full-task-info h5 {
  font-size: 17px;
  color: #3a6186;
  margin: 0 0 15px;
  font-weight: 600;
}

.editable-task-container {
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
  margin-bottom: 15px;
}

.editable-task-info {
  width: 100%;
  padding: 15px;
  font-size: 15px;
  line-height: 1.6;
  min-height: 200px;
  border: none;
  resize: vertical;
  font-family: inherit;
  white-space: pre-line;
  text-align: justify;
  color: #333;
  background-color: #fff;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.editable-task-info:focus {
  outline: none;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.edit-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f8f9fd;
  border-top: 1px solid #e1e4e8;
}

.edit-indicator {
  font-size: 13px;
  color: #666;
  font-style: italic;
}

.save-edit-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.save-edit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.save-edit-btn i {
  margin-right: 5px;
}

/* 添加下一步按钮样式 */
.next-step-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.next-step-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.next-step-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.next-step-btn i {
  margin-right: 5px;
}

/* 调试信息样式 */
.debug-info {
  margin: 10px 0;
  padding: 10px;
  background-color: #f8f9e9;
  border: 1px dashed #ccc;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
  color: #333;
}

/* 任务信息生成中样式 */
.task-generating {
  margin-top: 20px;
  background-color: #f7f7fa;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

/* 清除缓存链接样式 */
.clear-cache-link {
  display: inline-block;
  margin-top: 30px;
  font-size: 12px;
  color: #999;
  text-decoration: none;
  cursor: pointer;
}

.clear-cache-link:hover {
  color: #3a6186;
  text-decoration: underline;
}

/* 任务拆解结果样式 */
.task-breakdown-section {
  margin-top: 20px;
}

.task-breakdown-result {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.task-breakdown-result h5 {
  font-size: 17px;
  color: #3a6186;
  margin: 0 0 15px;
}

.task-tree {
  margin-bottom: 20px;
}

.main-task {
  margin-bottom: 20px;
  border: 1px solid #eee;
  border-radius: 6px;
  overflow: hidden;
}

.main-task-header {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  background: linear-gradient(to right, #f0f4f9, #f8f9fd);
  border-bottom: 1px solid #eee;
}

.task-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #3a6186, #89253e);
  color: #fff;
  font-weight: bold;
  border-radius: 50%;
  margin-right: 12px;
  flex-shrink: 0;
  font-size: 12px;
}

.main-task-header h6 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.subtasks {
  padding: 12px 15px;
}

.subtask {
  display: flex;
  margin-bottom: 8px;
}

.subtask:last-child {
  margin-bottom: 0;
}

.subtask-bullet {
  color: #3a6186;
  font-size: 18px;
  line-height: 1.2;
  margin-right: 10px;
  flex-shrink: 0;
}

.subtask-content {
  color: #555;
  font-size: 14px;
  line-height: 1.5;
}

.breakdown-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.edit-breakdown-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-breakdown-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.edit-breakdown-btn i {
  margin-right: 5px;
}

.breakdown-edit-area {
  margin-top: 15px;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  overflow: hidden;
}

.editable-breakdown {
  width: 100%;
  padding: 15px;
  font-size: 14px;
  line-height: 1.6;
  min-height: 200px;
  border: none;
  resize: vertical;
  font-family: monospace;
}

.editable-breakdown:focus {
  outline: none;
}

.edit-tip {
  padding: 8px 12px;
  background-color: #f8f9fd;
  color: #666;
  font-size: 12px;
  border-top: 1px solid #e1e4e8;
}

.edit-controls {
  display: flex;
  gap: 10px;
}

.cancel-edit-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background-color: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-edit-btn:hover {
  background-color: #e0e0e0;
}

.cancel-edit-btn i {
  margin-right: 5px;
}

/* 系统功能标识样式 */
.system-feature-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 6px;
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
  border-radius: 4px;
  color: #1890ff;
  font-size: 12px;
  margin-left: 8px;
  white-space: nowrap;
}

.system-feature-badge i {
  margin-right: 4px;
  font-size: 14px;
}

.system-feature-link {
  display: inline-flex;
  align-items: center;
  padding: 2px 6px;
  background-color: #f0f5ff;
  border: 1px solid #adc6ff;
  border-radius: 4px;
  color: #2f54eb;
  font-size: 12px;
  margin-left: 8px;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.3s;
}

.system-feature-link:hover {
  background-color: #d6e4ff;
  color: #1d39c4;
}

.system-feature-link i {
  margin-right: 4px;
  font-size: 14px;
}

/* 工作计划表格样式 */
.task-plan-section {
  margin-top: 20px;
}

.task-plan-result {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.task-plan-result h5 {
  font-size: 17px;
  color: #3a6186;
  margin: 0 0 15px;
}

.plan-table-container {
  overflow-x: auto;
  margin-bottom: 25px;
}

.plan-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #eee;
  font-size: 14px;
}

.plan-table th {
  background-color: #f8f9fd;
  padding: 12px 15px;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #e1e4e8;
  white-space: nowrap;
}

.plan-table td {
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
  color: #555;
}

.plan-table tr:last-child td {
  border-bottom: none;
}

.plan-table tr:hover {
  background-color: #f9fafc;
}

/* 优先级标签样式 */
.priority-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
  white-space: nowrap;
}

.priority-高 {
  background-color: #fff2f0;
  color: #89253e;
  border: 1px solid #ffccc7;
}

.priority-中 {
  background-color: #fcf8e3;
  color: #e6b980;
  border: 1px solid #faebcc;
}

.priority-低 {
  background-color: #fff8eb;
  color: #e6b980;
  border: 1px solid #f8e3c5;
}

/* 甘特图样式 - 已不使用 */
.gantt-chart-container {
  display: none; /* 隐藏甘特图容器 */
}

/* 移除后不再需要的甘特图相关样式代码 */

/* 继续按钮样式 */
.continue-btn {
  display: inline-flex;
  align-items: center;
  margin-left: 15px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.continue-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.continue-btn i {
  margin-right: 5px;
}

/* 甘特图标题栏样式 */
.gantt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f8f9fd;
  border-bottom: 1px solid #eee;
}

.gantt-header h6 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

/* 表格操作栏 */
.table-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

/* 下载按钮样式 */
.download-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background-color: #fff8eb;
  color: #89253e;
  border: 1px solid #fbe5c8;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.download-btn:hover {
  background-color: #ffefd1;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.download-btn i {
  margin-right: 5px;
}

/* 修复甘特图文字重叠问题 */
.gantt-bar {
  position: absolute;
  height: 100%;
  border-radius: 4px;
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #fff;
  padding: 0 5px;
  min-width: 30px;
  overflow: hidden;
}

.gantt-bar-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  display: inline-block;
}

.gantt-row {
  height: 30px;
  margin-bottom: 10px;
  position: relative;
}

/* 系统功能任务列表样式 */
.system-tasks-section {
  margin-top: 20px;
}

.system-tasks-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.system-task-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.system-task-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.task-info {
  padding: 15px;
  flex-grow: 1;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.task-header h6 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.task-details p {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.task-action {
  padding: 12px 15px;
  background-color: #f8f9fd;
  border-top: 1px solid #eee;
  text-align: center;
}

.start-task-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  width: 100%;
}

.start-task-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.start-task-btn i {
  margin-right: 5px;
}

.no-system-tasks {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  margin-bottom: 30px;
}

.no-system-tasks i {
  font-size: 40px;
  color: #aaa;
  margin-bottom: 10px;
}

.no-system-tasks p {
  color: #666;
  margin-bottom: 15px;
}

.browse-features-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 15px;
  background-color: #fff8eb;
  color: #89253e;
  border: 1px solid #fbe5c8;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.browse-features-btn:hover {
  background-color: #ffefd1;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.browse-features-btn i {
  margin-right: 5px;
}

/* 任务完成进度样式 */
.task-completion-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-top: 20px;
}

.task-completion-section h6 {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.task-completion-section p {
  color: #555;
  margin-bottom: 15px;
}

.completion-progress {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.progress-bar {
  flex-grow: 1;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
  margin-right: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #89253e, #e6b980);
  border-radius: 5px;
  transition: width 0.5s ease;
}

.progress-percentage {
  font-weight: 600;
  color: #89253e;
  min-width: 40px;
  text-align: right;
}

.mark-complete-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.mark-complete-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.mark-complete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.mark-complete-btn i {
  margin-right: 5px;
}

/* AI辅助任务梳理区域样式 */
.ai-section {
  position: relative;
  border-radius: 12px;
  padding: 35px;  /* 增加内边距 */
  margin: 0 auto 30px;  /* 添加左右居中 */
  background-color: #f8f9fd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px dashed #89253e;
  max-width: 90%;  /* 控制宽度 */
}

.ai-section::before {
  content: "AI协助高效工作";
  position: absolute;
  top: -16px;  /* 调整位置 */
  left: 50%;  /* 水平居中 */
  transform: translateX(-50%);  /* 水平居中 */
  padding: 0 20px;
  height: 36px;  /* 增加高度 */
  line-height: 36px;
  background: linear-gradient(135deg, #89253e 0%, #a93e4f 100%);
  color: #ffffff;
  font-size: 18px;  /* 增加字体大小 */
  font-weight: 600;
  border-radius: 6px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
  z-index: 10;  /* 确保在最上层 */
}

.ai-section::after {
  content: "";
  display: none;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-item input,
.form-item textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  font-size: 15px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-item input:focus,
.form-item textarea:focus {
  border-color: #89253e;
  box-shadow: 0 0 0 3px rgba(137, 37, 62, 0.1);
  outline: none;
}

/* 产品信息弹窗样式 */
.product-info-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 85%;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.modal-actions {
  display: flex;
  align-items: center;
}

.copy-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  margin-right: 12px;
  transition: all 0.2s;
}

.copy-btn:hover {
  background-color: #e9e9e9;
}

.copy-btn i {
  margin-right: 5px;
}

.close-btn {
  font-size: 24px;
  color: #aaa;
  cursor: pointer;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #89253e;
}

.modal-body {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 30px;
}

.product-image {
  flex: 0 0 35%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.product-image img {
  width: 100%;
  max-width: 350px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  object-fit: contain;
}

.product-details {
  flex: 1;
  min-width: 280px;
}

.product-details h4 {
  font-size: 18px;
  color: #89253e;
  margin: 20px 0 15px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.product-details h4:first-child {
  margin-top: 0;
}

.product-details ul {
  padding-left: 20px;
  margin-bottom: 20px;
}

.product-details li {
  margin-bottom: 10px;
  line-height: 1.6;
}

.product-details strong {
  font-weight: 600;
  color: #333;
}

.product-details p {
  line-height: 1.7;
  color: #555;
}

@media (max-width: 768px) {
  .modal-body {
    flex-direction: column;
  }
  
  .product-image {
    flex: 0 0 100%;
    margin-bottom: 20px;
  }
  
  .product-details {
    flex: 0 0 100%;
  }
  
  .modal-content {
    max-width: 95%;
    padding: 15px;
  }
}

/* 进度条样式 */
.progress-bar-container {
  width: 100%;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  margin: 10px 0;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #4caf50;
  border-radius: 5px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
  display: block;
  text-align: center;
}

/* 添加延迟过渡效果，使进度条更流畅 */
.analyzing-indicator p {
  margin-top: 15px;
  font-size: 15px;
  color: #555;
  text-align: center;
  transition: opacity 0.3s ease;
}

/* 增强加载中的样式 */
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(137, 37, 62, 0.1);
  border-radius: 50%;
  border-top-color: #89253e;
  animation: spin 1s ease-in-out infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 步骤式进度指示器样式 */
.step-progress-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 30px 0;
  position: relative;
  padding: 0 10px;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
  flex: 1;
  transition: all 0.4s ease;
}

.step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  color: #666;
  border: 2px solid #e0e0e0;
  margin-bottom: 10px;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-size: 16px;
  position: relative;
  z-index: 5;
}

.step-title {
  font-size: 14px;
  color: #666;
  text-align: center;
  transition: all 0.4s ease;
  white-space: nowrap;
  transform-origin: center top;
}

.step-line {
  position: absolute;
  top: 18px; /* 半高度，与圆圈中心对齐 */
  right: -50%;
  width: 100%;
  height: 2px;
  background-color: #e0e0e0;
  z-index: 1;
}

/* 当前步骤 */
.step-current .step-circle {
  background-color: #fff;
  border-color: #89253e;
  color: #89253e;
  box-shadow: 0 0 0 4px rgba(137, 37, 62, 0.1);
  transform: scale(1.4);
  font-size: 18px;
  width: 42px;
  height: 42px;
  font-weight: 700;
  z-index: 10;
}

.step-current .step-title {
  color: #89253e;
  font-weight: 700;
  font-size: 16px;
  transform: scale(1.2);
  margin-top: 5px;
}

/* 已完成步骤 */
.step-completed .step-circle {
  background-color: #89253e;
  border-color: #89253e;
  color: white;
}

.step-completed .step-line {
  background-color: #89253e;
}

.step-completed .step-title {
  color: #333;
}

/* 处理状态文本 */
.processing-status {
  margin-top: 20px;
  font-size: 16px;
  color: #333;
  text-align: center;
}

/* 错误消息 */
.error-message {
  margin-top: 20px;
  font-size: 16px;
  color: #e74c3c;
  text-align: center;
  background-color: #fef0f0;
  padding: 10px 15px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-message i {
  margin-right: 8px;
  font-size: 18px;
}

/* 加载中的样式 */
.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(137, 37, 62, 0.1);
  border-radius: 50%;
  border-top-color: #89253e;
  animation: spin 1s ease-in-out infinite;
  margin: 20px auto 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.product-info-btn {
  display: flex;
  align-items: center;
  padding: 10px 18px;
  background: linear-gradient(135deg, #3a6186, #89253e);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.product-info-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.product-info-btn i {
  margin-right: 8px;
  font-size: 18px;
}

.copy-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 10px 15px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  z-index: 2000;
  animation: fadeInOut 2s ease-in-out;
}

.copy-notification i {
  margin-right: 8px;
  color: #7cfc00;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(20px); }
  20% { opacity: 1; transform: translateY(0); }
  80% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-20px); }
}

/* 生成按钮容器右对齐 */
.generate-btn-container {
  display: flex;
  justify-content: flex-end;
}

/* 添加新样式到component的style部分 */
.streaming-indicator {
  font-size: 14px;
  color: #ff6b00;
  font-weight: normal;
  margin-left: 10px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.6;
  }
}

.editable-task-info {
  transition: background-color 0.3s;
}

.editable-task-info:disabled {
  background-color: #f9f9f9;
  cursor: default;
}

.task-result-section {
  margin-top: 20px;
  background-color: #f8f9fd;
  border-radius: 8px;
  border: 1px solid #e0e4ea;
  overflow: hidden;
}

.result-heading {
  padding: 15px 20px;
  background-color: #f0f3f8;
  border-bottom: 1px solid #e0e4ea;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-heading h5 {
  font-size: 17px;
  color: #333;
  margin: 0;
}

.improvement-badge {
  font-size: 12px;
  background-color: #89253e;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.optimized-goal-container {
  padding: 20px;
}

.optimized-goal-content {
  background-color: white;
  border-radius: 6px;
  border: 1px solid #e9ecf1;
  padding: 15px;
  margin-bottom: 15px;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  max-height: 300px;
  overflow-y: auto;
}

.optimized-goal-content p {
  margin-bottom: 15px;
}

.optimized-goal-content p:last-child {
  margin-bottom: 0;
}

.task-actions {
  display: flex;
  justify-content: flex-end;
}

.save-goal-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #e6b980);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.save-goal-btn:hover {
  background: linear-gradient(135deg, #761f35, #d9a165);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.save-goal-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.save-goal-btn i {
  margin-right: 5px;
}

/* 常见产品方案的任务目标抽屉样式 */
.drawer-container {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: flex;
  pointer-events: none;
}

.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 1;
  transition: opacity 0.3s ease;
  pointer-events: auto;
}

.drawer-content {
  position: fixed;
  top: 0;
  right: 0;
  width: 450px;
  max-width: 90%;
  height: 100%;
  background-color: #fff;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  transform: translateX(0);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  pointer-events: auto;
  overflow: hidden;
}

.drawer-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drawer-header h3 {
  font-size: 20px;
  color: #333;
  margin: 0;
}

.drawer-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.goal-intro {
  margin-bottom: 20px;
}

.goal-intro p {
  font-size: 15px;
  line-height: 1.6;
  color: #555;
}

.goal-reference {
  margin-bottom: 20px;
}

.goal-reference h4 {
  font-size: 18px;
  color: #89253e;
  margin-bottom: 10px;
}

.goal-reference p {
  font-size: 15px;
  line-height: 1.6;
  color: #555;
}

.goal-tips {
  margin-top: 10px;
}

.goal-tips ul {
  padding-left: 20px;
  margin-bottom: 10px;
}

.goal-tips li {
  margin-bottom: 5px;
  font-size: 14px;
  color: #666;
}

.goal-conclusion {
  margin-top: 15px;
  font-size: 15px;
  line-height: 1.6;
  color: #555;
}

.drawer-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  background-color: #f8f9fd;
}

.close-drawer-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background-color: #89253e;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.close-drawer-btn:hover {
  background-color: #721a31;
}

.close-drawer-btn i {
  margin-right: 5px;
}

.optimization-progress {
  display: flex;
  flex-direction: column;
  width: 120px;
}
.progress-text {
  font-size: 12px;
  margin-bottom: 5px;
  text-align: center;
}

/* 常见产品方案目录结构抽屉样式 */
.drawer-container {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: flex;
  pointer-events: none;
}

.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 1;
  transition: opacity 0.3s ease;
  pointer-events: auto;
}

.drawer-content {
  position: fixed;
  top: 0;
  right: 0;
  width: 450px;
  max-width: 90%;
  height: 100%;
  background-color: #fff;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  transform: translateX(0);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  pointer-events: auto;
  overflow: hidden;
}

.drawer-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drawer-header h3 {
  font-size: 20px;
  color: #333;
  margin: 0;
}

.drawer-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.structure-intro {
  margin-bottom: 20px;
}

.structure-intro p {
  font-size: 15px;
  line-height: 1.6;
  color: #555;
}

.drawer-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  background-color: #f8f9fd;
}

.close-drawer-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background-color: #89253e;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.close-drawer-btn:hover {
  background-color: #721a31;
}

.close-drawer-btn i {
  margin-right: 5px;
}

.structure-content {
  margin-top: 20px;
}

.structure-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  line-height: 1.6;
}

.structure-item p {
  margin: 8px 0;
}

/* 添加按钮居中的样式 */
.center-btn {
  display: flex;
  justify-content: center;
  margin: 15px 0;
}

/* 结构化目录样式 */
.structured-outline-container {
  margin-top: 20px;
  border: 1px solid #e0e4ea;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.structured-outline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #f8f9fd;
  border-bottom: 1px solid #e0e4ea;
}

.structured-outline-header h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
  display: flex;
  align-items: center;
}

.structured-outline-header h4 i {
  margin-right: 8px;
  color: #89253e;
}

.outline-actions {
  display: flex;
  gap: 10px;
}

.outline-action-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background-color: #f0f2f8;
  border: 1px solid #dce0e6;
  border-radius: 4px;
  color: #555;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.outline-action-btn:hover {
  background-color: #e5e8ef;
}

.outline-action-btn i {
  margin-right: 5px;
}

.structured-outline-content {
  padding: 15px;
  max-height: 800px; /* 增加高度 */
  overflow-y: auto;
}

.outline-item {
  margin-bottom: 10px;
  border-left: 2px solid transparent;
  transition: all 0.2s;
}

.outline-item:last-child {
  margin-bottom: 0;
}

.outline-item:hover {
  border-left-color: #89253e;
}

.outline-item.level-1 {
  margin-left: 0;
  border-left: 3px solid #89253e;
}

.outline-item.level-2 {
  margin-left: 30px;
  border-left: 3px solid #a93e4f;
}

.outline-item.level-3 {
  margin-left: 60px;
  border-left: 3px solid #cb6678;
}

.outline-item.level-4 {
  margin-left: 90px;
  border-left: 3px solid #e8a2a9;
}

.outline-item-header {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: #f8f9fd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.outline-item-header:hover {
  background-color: #eef0f7;
}

.toggle-icon {
  margin-right: 8px;
  font-size: 18px;
  color: #89253e;
  transition: transform 0.3s;
}

.outline-item-title {
  font-weight: 500;
  color: #333;
}

.outline-item-content {
  margin-top: 8px;
  margin-left: 25px;
  padding: 10px;
  background-color: #f8f9fd;
  border-radius: 4px;
  border-left: 2px solid #e0e4ea;
}

.outline-item-actions {
  margin-bottom: 10px;
}

.outline-edit-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background: linear-gradient(135deg, #89253e, #a93e4f);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.outline-edit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.outline-edit-btn i {
  margin-right: 5px;
}

.outline-item-description {
  margin-top: 8px;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #e0e4ea;
}

.outline-item-placeholder {
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px dashed #dce0e6;
  color: #999;
  font-style: italic;
}

.outline-item-placeholder i {
  margin-right: 5px;
  color: #89253e;
}

/* 修改样式部分 */
.structure-title-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.copy-structure-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background-color: #f0f2f8;
  border: 1px solid #dce0e6;
  border-radius: 4px;
  color: #555;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-structure-btn:hover {
  background-color: #e5e8ef;
}

.copy-structure-btn i {
  margin-right: 5px;
}

.outline-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background-color: #f8f9fd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.outline-item-title {
  font-weight: 500;
  color: #333;
  flex-grow: 1;
}

.outline-item-actions {
  display: flex;
  align-items: center;
}

/* 章节内容编辑弹窗样式 */
.edit-dialog-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1100;
  display: flex;
  justify-content: center;
  align-items: center;
}

.edit-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1101;
}

.edit-dialog-content {
  position: relative;
  width: 80%;
  /* 注释掉这个属性，以便ai-create-dialog类的max-width能生效 */
  /* max-width: 700px; */
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1102;
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.edit-dialog-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.edit-dialog-header h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 80%;
}

.edit-dialog-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #aaa;
  cursor: pointer;
  transition: color 0.3s;
}

.edit-dialog-close:hover {
  color: #89253e;
}

.edit-dialog-body {
  padding: 20px;
  flex-grow: 1;
  overflow-y: auto;
}

.edit-dialog-textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
  line-height: 1.6;
  resize: vertical;
  min-height: 250px;
  font-family: inherit;
}

.edit-dialog-textarea:focus {
  outline: none;
  border-color: #89253e;
  box-shadow: 0 0 0 2px rgba(137, 37, 62, 0.1);
}

.edit-dialog-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #f8f9fa;
}

.cancel-edit-dialog-btn {
  padding: 8px 16px;
  background-color: #f0f0f0;
  color: #555;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.cancel-edit-dialog-btn:hover {
  background-color: #e0e0e0;
}

.save-edit-dialog-btn {
  background-color: #c10d0c;
  border-color: #c10d0c;
  color: #fff;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid transparent;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.save-edit-dialog-btn:not(:disabled):hover {
  background-color: #d81e06;
  border-color: #d81e06;
}

.save-edit-dialog-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 添加左右对齐的按钮容器样式 */
.buttons-justify-between {
  display: flex;
  justify-content: space-between;
  margin: 15px 0;
}

/* 添加按钮中的加载动画样式 */
.button-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: button-spin 1s linear infinite;
  margin-left: 8px;
}

@keyframes button-spin {
  to { transform: rotate(360deg); }
}

.polished-result-container {
  margin-top: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.polished-result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.polished-result-header h4 {
  font-size: 17px;
  color: #333;
  margin: 0;
}

.close-polished-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #aaa;
  cursor: pointer;
  transition: color 0.3s;
}

.close-polished-btn:hover {
  color: #89253e;
}

.polished-input {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
  line-height: 1.6;
  resize: vertical;
  min-height: 120px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.polished-input:focus {
  outline: none;
}

.polished-input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f8f9fd;
  border-top: 1px solid #e1e4e8;
}

.polished-character-count {
  font-size: 13px;
  color: #666;
}

.polished-character-count.warning {
  color: #e74c3c;
}

/* 图标按钮样式 */
.outline-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background-color: #f8f9fd;
  color: #666;
  margin-left: 5px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  z-index: 10;
}

.outline-icon-btn:hover {
  background-color: #eef0f7;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.outline-icon-btn:active {
  transform: translateY(0);
  box-shadow: none;
}

.outline-icon-btn i {
  font-size: 18px;
}

.outline-icon-btn.edit-btn:hover {
  color: #3a6186;
}

.outline-icon-btn.delete-btn:hover {
  color: #e74c3c;
}

.outline-icon-btn.ai-btn:hover {
  color: #89253e;
}

.outline-item-actions {
  display: flex;
  align-items: center;
}

/* 导出文档按钮样式 */
.export-button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.export-document-btn {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background: linear-gradient(135deg, #89253e, #3a6186);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.export-document-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.export-document-btn i {
  margin-right: 8px;
  font-size: 20px;
}

/* 添加新的样式 */
.outline-item-title-section {
  display: flex;
  align-items: center;
  flex-grow: 1;
}

.outline-icon-btn.add-same-level-btn:hover {
  color: #4caf50;
}

.outline-icon-btn.add-sub-level-btn:hover {
  color: #2196f3;
}

.ai-create-dialog {
  max-width: 1400px !important; /* 原来是700px，增加一倍，添加!important确保优先级 */
  width: 90%;
}

.ai-create-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ai-create-input label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.ai-prompt-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
  line-height: 1.5;
  resize: vertical;
  font-family: inherit;
  background-color: #fff;
}

.ai-prompt-textarea:focus {
  outline: none;
  border-color: #89253e;
  box-shadow: 0 0 0 2px rgba(137, 37, 62, 0.1);
}

.ai-action {
  display: flex;
  justify-content: flex-end;
}

.ai-generate-btn {
  display: flex;
  align-items: center;
  padding: 10px 18px;
  background: linear-gradient(135deg, #89253e, #3a6186);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.ai-generate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.ai-generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.ai-generate-btn i {
  margin-right: 8px;
  font-size: 18px;
}

.ai-create-result {
  margin-top: 10px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.ai-result-header {
  padding: 10px 15px;
  background-color: #f8f9fd;
  border-bottom: 1px solid #eee;
}

.ai-result-header h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.ai-result-content {
  padding: 15px;
  position: relative;
}

.ai-generating {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 5;
}

.typing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
}

.typing-indicator span {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #89253e;
  margin: 0 3px;
  opacity: 0.6;
  animation: typing 1s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.ai-result-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
  line-height: 1.5;
  resize: vertical;
  font-family: inherit;
  background-color: #fff;
  min-height: 200px;
}

.ai-result-textarea:focus {
  outline: none;
  border-color: #89253e;
  box-shadow: 0 0 0 2px rgba(137, 37, 62, 0.1);
}

.ai-result-textarea:disabled {
  background-color: #f9f9f9;
  cursor: wait;
}

.new-item-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
}

.new-item-input:focus {
  border-color: #89253e;
  outline: none;
  box-shadow: 0 0 0 2px rgba(137, 37, 62, 0.1);
}

.parent-item-info {
  padding: 10px;
  background-color: #f8f9fd;
  border-radius: 4px;
  border: 1px solid #e0e4ea;
  color: #555;
}

/* 导出文档按钮样式 */
.zijing-red-btn {
  background-color: #c10d0c !important;
  border-color: #c10d0c !important;
}

.zijing-red-btn:hover:not(:disabled) {
  background-color: #d81e06 !important;
  border-color: #d81e06 !important;
}

.file-remove-btn {
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 12px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.file-remove-btn:hover {
  background-color: #f78989;
}

.file-remove-btn i {
  margin-right: 3px;
}

/* 添加目录项弹窗样式 */
.add-item-dialog-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.edit-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  background-color: transparent;
  z-index: 9998;
}

.edit-dialog-content {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 500px;
  padding: 20px;
  z-index: 10000;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.edit-dialog-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #EBEEF5;
}

.edit-dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.edit-dialog-close {
  background: none;
  border: none;
  font-size: 16px;
  color: #909399;
  cursor: pointer;
  transition: color 0.3s;
}

.edit-dialog-close:hover {
  color: #89253e;
}

.edit-dialog-body {
  padding: 20px;
  flex-grow: 1;
  margin-bottom: 20px;
}

.form-item {
  margin-bottom: 15px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.edit-dialog-footer {
  padding: 15px 20px;
  border-top: 1px solid #EBEEF5;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #F5F7FA;
}

.outline-icon-btn.add-same-level-btn {
  background-color: #e8f5e9;
  border-color: #4caf50;
  color: #4caf50;
}

.outline-icon-btn.add-sub-level-btn {
  background-color: #e3f2fd;
  border-color: #2196f3;
  color: #2196f3;
}

.outline-icon-btn.add-same-level-btn:hover,
.outline-icon-btn.add-sub-level-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 5px rgba(0,0,0,0.15);
}

.edit-dialog-content {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 450px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  z-index: 10000;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
}

.edit-dialog-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
}

.edit-dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.edit-dialog-close {
  background: none;
  border: none;
  font-size: 20px;
  color: #888;
  cursor: pointer;
  transition: color 0.2s;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
}

.edit-dialog-close:hover {
  color: #e53935;
}

.edit-dialog-body {
  padding: 20px;
  flex-grow: 1;
}

.form-item {
  margin-bottom: 15px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-item input,
.form-item .parent-item-info {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}

.form-item input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.parent-item-info {
  background-color: #f5f7f9;
  color: #555;
}

.edit-dialog-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #f8f9fa;
}

/* 文件上传区域样式 */
.file-upload-section {
  margin-top: 15px;
  margin-bottom: 15px;
}

.file-upload-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.file-upload-area {
  border: 1px dashed #ddd;
  border-radius: 4px;
  padding: 15px;
  background-color: #f9f9f9;
}

.file-upload-box {
  text-align: center;
}

.file-input {
  display: none;
}

.file-upload-button {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #555;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.file-upload-button:hover {
  background-color: #e0e0e0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.file-upload-button i {
  margin-right: 5px;
  font-size: 16px;
}

.file-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.file-preview {
  padding: 5px;
}

.file-info {
  display: flex;
  align-items: center;
  padding: 8px;
  background: #f0f0f0;
  border-radius: 4px;
}

.file-info i {
  font-size: 18px;
  color: #555;
  margin-right: 8px;
}

.file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}

.file-actions {
  display: flex;
  align-items: center;
}

.file-remove-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  transition: color 0.2s;
  padding: 4px;
}

.file-remove-btn:hover {
  color: #e53935;
}

.file-processing {
  display: flex;
  align-items: center;
  margin-top: 8px;
  padding: 5px;
  font-size: 13px;
  color: #555;
}

.processing-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top-color: #2196f3;
  border-radius: 50%;
  margin-right: 8px;
  animation: processing-spin 1s linear infinite;
}

@keyframes processing-spin {
  to { transform: rotate(360deg); }
}

/* 全局弹窗样式 */
.global-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.global-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.global-modal-container {
  position: relative;
  z-index: 2;
  max-width: 90%;
  width: 500px;
}

.global-modal-content {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.global-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.global-modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.global-modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.global-modal-close:hover {
  background-color: #f5f5f5;
  color: #333;
}

.global-modal-body {
  padding: 20px;
}

.global-modal-footer {
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #eee;
}

.global-form-group {
  margin-bottom: 16px;
}

.global-form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.global-form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.global-form-control:focus {
  border-color: #4a66e0;
  outline: none;
}

.global-parent-info {
  padding: 10px;
  background-color: #f5f7f9;
  border-radius: 4px;
  color: #666;
}

.global-btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.global-btn-primary {
  background-color: #4a66e0;
  color: white;
}

.global-btn-primary:hover {
  background-color: #3a56d0;
}

.global-btn-primary:disabled {
  background-color: #a8b2e0;
  cursor: not-allowed;
}

.global-btn-cancel {
  background-color: #f5f5f5;
  color: #666;
}

.global-btn-cancel:hover {
  background-color: #e8e8e8;
}

/* 添加新的样式用于修复新增目录弹窗 */
.add-item-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.add-item-modal .global-modal-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  margin: 0 auto;
}

.add-item-modal .global-modal-content {
  padding: 20px;
}

.add-item-modal .global-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.add-item-modal .global-modal-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.add-item-modal .global-modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
}

.add-item-modal .global-form-group {
  margin-bottom: 15px;
}

.add-item-modal .global-form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.add-item-modal .global-form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.add-item-modal .global-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-size: 14px;
  cursor: pointer;
  margin-left: 10px;
}

.add-item-modal .global-btn-cancel {
  background-color: #f5f5f5;
  color: #666;
}

.add-item-modal .global-btn-primary {
  background-color: #1890ff;
  color: white;
}

.add-item-modal .global-modal-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.add-item-modal .global-parent-info {
  background-color: #f5f7fa;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
}

.save-edit-dialog-btn {
  background-color: #c10d0c;
  border-color: #c10d0c;
  color: #fff;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid transparent;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.save-edit-dialog-btn:not(:disabled):hover {
  background-color: #d81e06;
  border-color: #d81e06;
}

.save-edit-dialog-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cancel-edit-dialog-btn {
  background-color: #f5f7fa;
  border-color: #dcdfe6;
  color: #606266;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-edit-dialog-btn:not(:disabled):hover {
  background-color: #f0f2f5;
  color: #409eff;
}

.cancel-edit-dialog-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.file-remove-btn {
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 12px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.file-remove-btn:hover {
  background-color: #f78989;
}

.file-remove-btn i {
  margin-right: 3px;
}
</style> 

/* 添加目录项弹窗样式 */
.add-item-dialog-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.edit-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  background-color: transparent;
  z-index: 9998;
}

.edit-dialog-content {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 500px;
  padding: 20px;
  z-index: 10000;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.edit-dialog-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #EBEEF5;
}

.edit-dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.edit-dialog-close {
  background: none;
  border: none;
  font-size: 16px;
  color: #909399;
  cursor: pointer;
  transition: color 0.3s;
}

.edit-dialog-close:hover {
  color: #89253e;
}

.edit-dialog-body {
  padding: 20px;
  flex-grow: 1;
  margin-bottom: 20px;
}

.form-item {
  margin-bottom: 15px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.edit-dialog-footer {
  padding: 15px 20px;
  border-top: 1px solid #EBEEF5;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #F5F7FA;
}

.outline-icon-btn.add-same-level-btn {
  background-color: #e8f5e9;
  border-color: #4caf50;
  color: #4caf50;
}

.outline-icon-btn.add-sub-level-btn {
  background-color: #e3f2fd;
  border-color: #2196f3;
  color: #2196f3;
}

.outline-icon-btn.add-same-level-btn:hover,
.outline-icon-btn.add-sub-level-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 5px rgba(0,0,0,0.15);
}

.edit-dialog-content {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 450px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  z-index: 10000;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
}

.edit-dialog-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
}

.edit-dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.edit-dialog-close {
  background: none;
  border: none;
  font-size: 20px;
  color: #888;
  cursor: pointer;
  transition: color 0.2s;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
}

.edit-dialog-close:hover {
  color: #e53935;
}

.edit-dialog-body {
  padding: 20px;
  flex-grow: 1;
}

.form-item {
  margin-bottom: 15px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-item input,
.form-item .parent-item-info {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}

.form-item input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.parent-item-info {
  background-color: #f5f7f9;
  color: #555;
}

.edit-dialog-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #f8f9fa;
}

/* 文件上传区域样式 */
.file-upload-section {
  margin-top: 15px;
  margin-bottom: 15px;
}

.file-upload-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.file-upload-area {
  border: 1px dashed #ddd;
  border-radius: 4px;
  padding: 15px;
  background-color: #f9f9f9;
}

.file-upload-box {
  text-align: center;
}

.file-input {
  display: none;
}

.file-upload-button {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #555;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.file-upload-button:hover {
  background-color: #e0e0e0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.file-upload-button i {
  margin-right: 5px;
  font-size: 16px;
}

.file-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.file-preview {
  padding: 5px;
}

.file-info {
  display: flex;
  align-items: center;
  padding: 8px;
  background: #f0f0f0;
  border-radius: 4px;
}

.file-info i {
  font-size: 18px;
  color: #555;
  margin-right: 8px;
}

.file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}

.file-actions {
  display: flex;
  align-items: center;
}

.file-remove-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  transition: color 0.2s;
  padding: 4px;
}

.file-remove-btn:hover {
  color: #e53935;
}

.file-processing {
  display: flex;
  align-items: center;
  margin-top: 8px;
  padding: 5px;
  font-size: 13px;
  color: #555;
}

.processing-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top-color: #2196f3;
  border-radius: 50%;
  margin-right: 8px;
  animation: processing-spin 1s linear infinite;
}

@keyframes processing-spin {
  to { transform: rotate(360deg); }
}

/* 全局弹窗样式 */
.global-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.global-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.global-modal-container {
  position: relative;
  z-index: 2;
  max-width: 90%;
  width: 500px;
}

.global-modal-content {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.global-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.global-modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.global-modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.global-modal-close:hover {
  background-color: #f5f5f5;
  color: #333;
}

.global-modal-body {
  padding: 20px;
}

.global-modal-footer {
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #eee;
}

.global-form-group {
  margin-bottom: 16px;
}

.global-form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.global-form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.global-form-control:focus {
  border-color: #4a66e0;
  outline: none;
}

.global-parent-info {
  padding: 10px;
  background-color: #f5f7f9;
  border-radius: 4px;
  color: #666;
}

.global-btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.global-btn-primary {
  background-color: #4a66e0;
  color: white;
}

.global-btn-primary:hover {
  background-color: #3a56d0;
}

.global-btn-primary:disabled {
  background-color: #a8b2e0;
  cursor: not-allowed;
}

.global-btn-cancel {
  background-color: #f5f5f5;
  color: #666;
}

.global-btn-cancel:hover {
  background-color: #e8e8e8;
}

/* 添加新的样式用于修复新增目录弹窗 */
.add-item-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.add-item-modal .global-modal-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  margin: 0 auto;
}

.add-item-modal .global-modal-content {
  padding: 20px;
}

.add-item-modal .global-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.add-item-modal .global-modal-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.add-item-modal .global-modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
}

.add-item-modal .global-form-group {
  margin-bottom: 15px;
}

.add-item-modal .global-form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.add-item-modal .global-form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.add-item-modal .global-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-size: 14px;
  cursor: pointer;
  margin-left: 10px;
}

.add-item-modal .global-btn-cancel {
  background-color: #f5f5f5;
  color: #666;
}

.add-item-modal .global-btn-primary {
  background-color: #1890ff;
  color: white;
}

.add-item-modal .global-modal-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.add-item-modal .global-parent-info {
  background-color: #f5f7fa;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
}

.save-edit-dialog-btn {
  background-color: #c10d0c;
  border-color: #c10d0c;
  color: #fff;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid transparent;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.save-edit-dialog-btn:not(:disabled):hover {
  background-color: #d81e06;
  border-color: #d81e06;
}

.save-edit-dialog-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cancel-edit-dialog-btn {
  background-color: #f5f7fa;
  border-color: #dcdfe6;
  color: #606266;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-edit-dialog-btn:not(:disabled):hover {
  background-color: #f0f2f5;
  color: #409eff;
}

.cancel-edit-dialog-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.file-remove-btn {
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 12px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.file-remove-btn:hover {
  background-color: #f78989;
}

.file-remove-btn i {
  margin-right: 3px;
}