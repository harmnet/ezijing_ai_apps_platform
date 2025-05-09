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
        <h1 class="main-title">市场活动策划 <span class="scenario-category">市场营销实践</span></h1>
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
            <img src="@/assets/images/scenarios/marketing-specialist-new.png" alt="市场专员" />
          </div>
          <div class="role-info">
            <h3>市场专员 - 张明</h3>
            <p>你是一家快速成长的消费电子品牌"科技先锋"的市场专员。你的主要职责是负责公司产品的市场推广活动策划与执行，包括活动创意、文案撰写、视觉设计协调和社交媒体传播等工作。你已在公司工作一年，拥有良好的文案功底和市场敏感度。</p>
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
            <p>昨天下午，你的直属领导、市场部经理李总在部门例会上临时安排了一项重要任务：公司即将在下个月推出全新的智能手表产品线"TechWatch Pro"，需要你负责策划一场线上线下结合的新品发布营销活动。李总希望这次活动能够提升品牌在年轻消费群体中的知名度，突出产品的科技感和实用性，同时带动产品的首发销量。</p>
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
              <h3>常规任务：5天内完成初稿</h3>
              <p>李总要求你在5天内完成完整的活动策划方案初稿，包括活动主题、创意构思、执行计划、预算规划和预期效果等内容。虽然时间相对充裕，但考虑到整体工作质量和创意性要求，你仍然需要合理规划各环节的时间分配。</p>
            </div>
          </div>
        </div>
      </div>

      <!-- AI辅助任务梳理部分 -->
      <div class="section ai-section">
        <div class="ai-workflow-card">
          <div class="ai-header">
            <div class="ai-title" style="text-align: center; width: 100%;">
              <p class="task-content" style="text-align: center; color: #ffffff;">突如其来的重任让张明陷入困境——领导临时交代的市场活动策划，正常需要至少两周才能完成！时间紧迫，任务繁重，他该如何破局？别担心，AI技术正在改变工作方式！现在，我们可以借助人工智能的超强分析能力和创意思维，将不可能变为可能。告别加班熬夜，提升效率与创意质量，让AI成为你的得力助手。跟随以下5个步骤，一起体验AI协作的魔力，轻松完成市场活动策划！</p>
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
                    placeholder="请小组讨论，输入张明获取到的初始任务信息。" 
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
                <h4>梳理任务，补充任务信息</h4>
                <p class="task-content">我们需要结合获取到的初始任务信息，在我们力所能及的范围内尽可能地将任务信息进行完善。考虑领导可能提到的时间要求、质量要求、成本要求，以及相关部门的其他有效输入信息等。这一步是行动前的重要基础工作，对后续任务执行的效率和质量至关重要。</p>
                
                <!-- 用户输入的初步补充信息 -->
                <div class="input-container" v-if="showStepCompleted[0]">
                  <textarea 
                    v-model="userSupplementInfo" 
                    placeholder="请小组讨论，输入任务的补充信息。" 
                    rows="6"
                    class="task-input"
                    :disabled="isAnalyzing || taskInfoCompleted"
                    maxlength="500"
                  ></textarea>
                  
                  <div class="input-footer">
                    <span class="character-count" :class="{ 'warning': userSupplementInfo.length > 400 }">
                      {{ userSupplementInfo.length }}/500字
                    </span>
                  </div>
                </div>

                <!-- 第二步状态调试信息 -->
                <div v-if="showStepCompleted[0] && debugMode" class="debug-info">
                  步骤1完成状态: {{ showStepCompleted[0] }}<br>
                  分析中: {{ isAnalyzing }}<br>
                  任务信息已完成: {{ taskInfoCompleted }}
                </div>
                
                <!-- AI辅助梳理按钮 -->
                <div class="button-container" v-if="showStepCompleted[0]">
                  <button 
                    class="product-info-btn" 
                    @click="showProductInfo"
                  >
                    <i class="ri-information-line"></i> 查看产品信息
                  </button>
                  <button 
                    class="ai-assist-btn" 
                    @click="getAIAssistance" 
                    :disabled="isAnalyzing || !initialTask.trim() || !userSupplementInfo.trim() || taskInfoCompleted"
                  >
                    <i class="ri-ai-generate"></i> AI辅助梳理
                  </button>
                </div>
                
                <!-- 产品信息弹窗 -->
                <div v-if="productInfoVisible" class="product-info-modal">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h3>产品信息详情</h3>
                      <div class="modal-actions">
                        <button class="copy-btn" @click="copyProductInfo">
                          <i class="ri-file-copy-line"></i> 复制信息
                        </button>
                        <span class="close-btn" @click="hideProductInfo">&times;</span>
                      </div>
                    </div>
                    <div class="modal-body">
                      <div class="product-image">
                        <img 
                          src="@/assets/images/scenarios/techwatch-pro.png" 
                          alt="TechWatch Pro" 
                          onerror="this.src='https://via.placeholder.com/300x300?text=TechWatch+Pro'; this.style.display='block';" 
                        />
                      </div>
                      <div class="product-details">
                        <h4>产品核心卖点</h4>
                        <ul>
                          <li><strong>超长续航能力：</strong>单次充电可使用7天，采用高效锂电池和智能电量管理系统，满足商务出差和旅行用户需求</li>
                          <li><strong>AI健康管理功能：</strong>包括高精度心率监测、睡眠分析、压力监测、呼吸训练和全天候活动跟踪，配合专业算法提供个性化健康建议</li>
                          <li><strong>全新交互体验：</strong>支持手势控制和语音助手，配备高清触控屏幕，操作更流畅直观</li>
                          <li><strong>智能连接功能：</strong>无缝连接手机，智能推送消息、来电提醒，可直接接听电话和回复消息</li>
                          <li><strong>防水防尘设计：</strong>达到IP68级别，可在水下50米使用，适合游泳和潜水爱好者</li>
                        </ul>
                        
                        <h4>目标用户群体</h4>
                        <ul>
                          <li><strong>年轻商务人士：</strong>25-40岁，重视效率和专业形象，需要智能设备辅助工作和健康管理</li>
                          <li><strong>健康生活爱好者：</strong>关注身体健康数据，热爱运动，注重生活品质的消费者</li>
                          <li><strong>科技早期采用者：</strong>喜欢尝试新技术产品，对智能穿戴设备有浓厚兴趣的人群</li>
                        </ul>
                        
                        <h4>产品定位与价格</h4>
                        <p>TechWatch Pro 定位为中高端智能手表市场，零售价格区间为1499-1999元人民币（根据配置不同），与同类产品相比具有更高的性价比和更全面的功能。</p>
                      </div>
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
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>细化拆解任务</h4>
                <p>请先尝试输入你认为应该如何细化拆解当前任务，然后点击"AI辅助任务拆解"按钮获取更全面的建议。</p>
                
                <!-- 用户输入框 -->
                <div class="input-container" v-if="showStepCompleted[1]">
                  <textarea 
                    v-model="userTaskBreakdown" 
                    placeholder="请输入你认为应该如何细化拆解这个市场活动策划任务，例如：'活动主题设计、目标受众分析、营销渠道选择、预算规划...'等" 
                    rows="4"
                    class="task-input"
                    :disabled="isAnalyzingBreakdown || tasksGenerated"
                  ></textarea>
                </div>
                
                <!-- AI辅助按钮 -->
                <div class="button-container" v-if="showStepCompleted[1]">
                  <button 
                    class="ai-assist-btn" 
                    @click="getAITaskBreakdown" 
                    :disabled="isAnalyzingBreakdown || !fullTaskInfo.trim() || !userTaskBreakdown.trim() || tasksGenerated"
                  >
                    <i class="ri-ai-generate"></i> AI辅助任务拆解
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

            <div class="step">
              <div class="step-number">4</div>
              <div class="step-content">
                <h4>设置工作任务优先级及计划</h4>
                <p>请先输入你的项目时间要求和其他约束条件，然后点击"AI辅助生成工作计划"按钮获取合理的任务优先级和时间安排。</p>
                
                <!-- 用户输入框 -->
                <div class="input-container" v-if="showStepCompleted[2]">
                  <textarea 
                    v-model="userTaskConstraints" 
                    placeholder="请输入项目的时间要求和约束条件，例如：'总工期7天，第3天需要完成主视觉设计，第5天需要完成文案内容，每天工作8小时...'等" 
                    rows="4"
                    class="task-input"
                    :disabled="isAnalyzingPlan || planGenerated"
                  ></textarea>
                </div>
                
                <!-- AI辅助按钮 -->
                <div class="button-container" v-if="showStepCompleted[2]">
                  <button 
                    class="ai-assist-btn" 
                    @click="getAITaskPlan" 
                    :disabled="isAnalyzingPlan || !taskBreakdownResult || !userTaskConstraints.trim() || planGenerated"
                  >
                    <i class="ri-ai-generate"></i> AI辅助生成工作计划
                  </button>
                </div>
                
                <!-- 加载状态 -->
                <div v-if="isAnalyzingPlan" class="ai-analysis-section">
                  <div class="analyzing-indicator">
                    <!-- 步骤式进度指示器 -->
                    <div class="step-progress-container">
                      <div 
                        v-for="(step, index) in planProcessingSteps" 
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
                        <div class="step-line" v-if="index < planProcessingSteps.length - 1"></div>
                      </div>
                    </div>
                    
                    <!-- 处理中动画 -->
                    <div class="spinner" v-if="!planProcessingError"></div>
                    
                    <!-- 当前处理步骤文本 -->
                    <p v-if="!planProcessingError" class="processing-status">
                      {{ planProcessingSteps[planProcessingStep].title }}中...
                    </p>
                    
                    <!-- 错误提示 -->
                    <p v-if="planProcessingError" class="error-message">
                      <i class="ri-error-warning-line"></i> {{ planProcessingError }}
                    </p>
                  </div>
                </div>
                
                <!-- 工作计划结果 -->
                <div v-if="taskPlanResult" class="task-plan-section">
                  <div class="task-plan-result">
                    <h5>工作计划表</h5>
                    
                    <!-- 工作计划表格 -->
                    <div class="plan-table-container">
                      <div class="table-actions">
                        <button class="download-btn" @click="downloadTableAsCSV">
                          <i class="ri-download-line"></i> 下载表格
                        </button>
                      </div>
                      <table class="plan-table">
                        <thead>
                          <tr>
                            <th>任务名称</th>
                            <th>优先级</th>
                            <th>预计耗时</th>
                            <th>结束时间</th>
                            <th>系统功能</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(task, index) in parsedTaskPlan" :key="index">
                            <td>{{ task.taskName }}</td>
                            <td>
                              <span :class="'priority-badge priority-' + task.priority.toLowerCase()">
                                {{ task.priority }}
                              </span>
                            </td>
                            <td>{{ task.duration }}</td>
                            <td>{{ task.endDate }}</td>
                            <td>
                              <a 
                                v-if="task.systemFeature && task.systemLink" 
                                :href="task.systemLink" 
                                target="_blank" 
                                class="system-feature-link"
                              >
                                <i class="ri-link"></i> {{ task.systemFeature }}
                              </a>
                              <span v-else-if="task.systemFeature" class="system-feature-badge">
                                <i class="ri-tools-fill"></i> {{ task.systemFeature }}
                              </span>
                              <span v-else>-</span>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    
                    <!-- 编辑按钮 -->
                    <div class="plan-actions">
                      <!-- 确认并继续按钮 -->
                      <button 
                        class="continue-btn" 
                        @click="continueToStep5"
                        :disabled="!planGenerated"
                      >
                        <i class="ri-arrow-right-line"></i> 确认并继续
                      </button>
                    </div>
                    
                    <!-- 保存成功提示 -->
                    <div v-if="planGenerated" class="saved-message">
                      <i class="ri-checkbox-circle-line"></i> 工作计划已生成，请确认并继续下一步
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">5</div>
              <div class="step-content">
                <h4>执行任务，获得结论</h4>
                <p>根据工作计划中设定的优先级和时间安排，执行各项任务，特别是以下可以使用系统功能的任务：</p>
                
                <!-- 系统功能任务列表 -->
                <div v-if="showStepCompleted[3]" class="system-tasks-section">
                  <div v-if="systemTasks.length > 0" class="system-tasks-list">
                    <div v-for="(task, index) in systemTasks" :key="index" class="system-task-card">
                      <div class="task-info">
                        <div class="task-header">
                          <h6>{{ task.taskName }}</h6>
                          <span :class="'priority-badge priority-' + task.priority.toLowerCase()">
                            {{ task.priority }}
                          </span>
                        </div>
                        <div class="task-details">
                          <p><strong>预计耗时:</strong> {{ task.duration }}</p>
                          <p><strong>负责人:</strong> {{ task.assignee }}</p>
                          <p><strong>执行时间:</strong> {{ task.startDate }} - {{ task.endDate }}</p>
                        </div>
                      </div>
                      <div class="task-action">
                        <a 
                          :href="task.systemLink" 
                          target="_blank" 
                          class="start-task-btn"
                        >
                          <i class="ri-external-link-line"></i> {{ task.systemFeature }}
                        </a>
                      </div>
                    </div>
                  </div>
                  
                  <div v-else class="no-system-tasks">
                    <i class="ri-information-line"></i>
                    <p>工作计划中未找到可使用系统功能的任务。你可以返回上一步添加系统功能相关任务，或直接前往系统功能列表查找所需工具。</p>
                    <a href="/practical-scenario" class="browse-features-btn">
                      <i class="ri-apps-line"></i> 浏览功能列表
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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
      
      // 步骤控制
      showStepCompleted: [false, false, false, false, false],
      
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
      processingStep: 0,  // 变更为数字，表示当前处理到第几步
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
        { title: '拆解任务模块', completed: false, current: false },
        { title: '关联系统功能', completed: false, current: false },
        { title: '生成最终拆解', completed: false, current: false }
      ],
      breakdownProcessingError: '',
      
      // 第四步相关数据
      userTaskConstraints: '',
      isAnalyzingPlan: false,
      taskPlanResult: '',
      parsedTaskPlan: [],
      planGenerated: false,
      editingPlan: false,
      editableTaskPlan: '',
      taskPlanSaved: false,
      totalDays: 7, // 默认总天数
      planProcessingStep: 0,
      planProcessingSteps: [
        { title: '启动AI助手', completed: false, current: false },
        { title: '分析任务拆解', completed: false, current: false },
        { title: '规划任务优先级', completed: false, current: false },
        { title: '安排时间线', completed: false, current: false },
        { title: '生成工作计划', completed: false, current: false }
      ],
      planProcessingError: '',
      
      // 第五步相关数据
      systemTasks: [],
      completionProgress: 0,
      
      // 产品信息相关
      productInfoVisible: false,
    }
  },
  computed: {
    // 判断是否可以生成完整任务信息（检查必填字段是否已填写）
    canGenerateTaskInfo() {
      if (!this.taskFields.length) return false;
      
      // 检查所有必填字段是否已填写
      return !this.taskFields.some(field => field.required && !field.value.trim());
    }
  },
  mounted() {
    // 页面加载完成后直接重置所有状态
    setTimeout(() => {
      this.clearAllStoredData();
      this.loaded = true;
      // 添加监听器
      this.setupWatchers && this.setupWatchers();
      // 添加甘特图行高调整
      this.$nextTick(() => {
        if (this.parsedTaskPlan && this.parsedTaskPlan.length > 0) {
          setTimeout(() => this.adjustGanttRowHeights && this.adjustGanttRowHeights(), 300);
        }
      });
    }, 100)
  },
  methods: {
    // 弹出重置确认框
    confirmReset() {
      if (confirm('确定要重置所有输入内容吗？此操作无法撤销。')) {
        this.clearAllStoredData();
        // 刷新页面以确保UI完全重置
        window.location.reload();
      }
    },

    // 清除所有存储的数据
    clearAllStoredData() {
      // 先移除初始化标记，确保下次刷新时也会清除数据
      localStorage.removeItem('marketingCampaignInitialized');
      
      // 清除所有数据项
      localStorage.removeItem('marketingCampaignInitialTask');
      localStorage.removeItem('marketingCampaignSupplementInfo');
      localStorage.removeItem('marketingCampaignTaskFields');
      localStorage.removeItem('marketingCampaignFullTaskInfo');
      localStorage.removeItem('marketingCampaignTaskInfoSaved');
      localStorage.removeItem('marketingCampaignStep1Completed');
      localStorage.removeItem('marketingCampaignStep2Completed');
      localStorage.removeItem('marketingCampaignAIAnalysis');
      localStorage.removeItem('marketingCampaignBreakdownResult');
      localStorage.removeItem('marketingCampaignUserBreakdown');
      localStorage.removeItem('marketingCampaignBreakdownSaved');
      localStorage.removeItem('marketingCampaignPlanResult');
      localStorage.removeItem('marketingCampaignUserConstraints');
      localStorage.removeItem('marketingCampaignPlanSaved');
      localStorage.removeItem('marketingCampaignSystemTasks');
      localStorage.removeItem('marketingCampaignCompletionProgress');
      localStorage.removeItem('marketingCampaignStep4Completed');
      localStorage.removeItem('marketingCampaignStep5Completed');
      
      // 重置所有状态
      this.initialTask = '';
      this.userSupplementInfo = '';
      this.taskFields = [];
      this.fullTaskInfo = '';
      this.taskInfoCompleted = false;
      this.taskInfoSaved = false;
      this.showStepCompleted = [false, false, false, false, false];
      this.userTaskBreakdown = '';
      this.isAnalyzingBreakdown = false;
      this.taskBreakdownResult = '';
      this.parsedTaskBreakdown = [];
      this.tasksGenerated = false;
      this.editingBreakdown = false;
      this.editableTaskBreakdown = '';
      this.taskBreakdownSaved = false;
      this.userTaskConstraints = '';
      this.isAnalyzingPlan = false;
      this.taskPlanResult = '';
      this.parsedTaskPlan = [];
      this.planGenerated = false;
      this.editingPlan = false;
      this.editableTaskPlan = '';
      this.taskPlanSaved = false;
      this.totalDays = 7;
      this.systemTasks = [];
      this.completionProgress = 0;
      
      console.log('所有数据已重置');
    },
    
    // 加载存储的数据
    loadStoredData() {
      const savedInitialTask = localStorage.getItem('marketingCampaignInitialTask');
      if (savedInitialTask) {
        this.initialTask = savedInitialTask;
        
        // 恢复第一步完成状态
        const step1Completed = localStorage.getItem('marketingCampaignStep1Completed');
        if (step1Completed === 'true') {
          this.showStepCompleted[0] = true;
        }
      }
      
      const savedSupplementInfo = localStorage.getItem('marketingCampaignSupplementInfo');
      if (savedSupplementInfo) {
        this.userSupplementInfo = savedSupplementInfo;
      }
      
      // 重置任务信息完成状态，确保能继续编辑
      const savedFullTaskInfo = localStorage.getItem('marketingCampaignFullTaskInfo');
      const savedTaskInfoSaved = localStorage.getItem('marketingCampaignTaskInfoSaved');
      
      // 仅当任务信息已保存时才标记为完成
      this.taskInfoCompleted = savedFullTaskInfo && savedTaskInfoSaved === 'true';
      
      if (savedFullTaskInfo) {
        this.fullTaskInfo = savedFullTaskInfo;
        
        if (savedTaskInfoSaved === 'true') {
          this.taskInfoSaved = true;
          this.showStepCompleted[1] = true;
        }
      }
      
      const savedTaskFields = localStorage.getItem('marketingCampaignTaskFields');
      if (savedTaskFields) {
        try {
          this.taskFields = JSON.parse(savedTaskFields);
          
          // 如果有已保存的任务字段，标记第二步部分完成
          if (this.taskFields.length > 0 && !this.taskInfoCompleted) {
            this.showStepCompleted[1] = true;
          }
        } catch (e) {
          console.error('解析保存的任务字段时出错:', e);
        }
      }
      
      // 加载第三步数据
      const savedBreakdownResult = localStorage.getItem('marketingCampaignBreakdownResult');
      if (savedBreakdownResult) {
        this.taskBreakdownResult = savedBreakdownResult;
        try {
          this.parsedTaskBreakdown = JSON.parse(savedBreakdownResult);
          this.tasksGenerated = true;
          
          const breakdownSaved = localStorage.getItem('marketingCampaignBreakdownSaved');
          if (breakdownSaved === 'true') {
            this.taskBreakdownSaved = true;
            this.showStepCompleted[2] = true;
          }
        } catch (e) {
          console.error('解析任务拆解数据出错:', e);
        }
      }
      
      const savedUserBreakdown = localStorage.getItem('marketingCampaignUserBreakdown');
      if (savedUserBreakdown) {
        this.userTaskBreakdown = savedUserBreakdown;
      }
      
      // 加载第四步数据
      const savedPlanResult = localStorage.getItem('marketingCampaignPlanResult');
      if (savedPlanResult) {
        this.taskPlanResult = savedPlanResult;
        try {
          this.parsedTaskPlan = JSON.parse(savedPlanResult);
          this.planGenerated = true;
          
          // 计算总天数
          this.calculateTotalDays();
          
          const planSaved = localStorage.getItem('marketingCampaignPlanSaved');
          if (planSaved === 'true') {
            this.taskPlanSaved = true;
            this.showStepCompleted[3] = true;
          }
        } catch (e) {
          console.error('解析工作计划数据出错:', e);
        }
      }
      
      const savedUserConstraints = localStorage.getItem('marketingCampaignUserConstraints');
      if (savedUserConstraints) {
        this.userTaskConstraints = savedUserConstraints;
      }
      
      // 加载第四步完成状态
      const step4Completed = localStorage.getItem('marketingCampaignStep4Completed');
      if (step4Completed === 'true') {
        this.showStepCompleted[3] = true;
      }
      
      // 加载系统任务
      const savedSystemTasks = localStorage.getItem('marketingCampaignSystemTasks');
      if (savedSystemTasks) {
        try {
          this.systemTasks = JSON.parse(savedSystemTasks);
        } catch (e) {
          console.error('解析系统任务数据出错:', e);
        }
      }
      
      // 加载完成进度
      const savedProgress = localStorage.getItem('marketingCampaignCompletionProgress');
      if (savedProgress) {
        this.completionProgress = parseInt(savedProgress) || 0;
        
        // 如果进度为100%，标记第五步完成
        if (this.completionProgress >= 100) {
          this.showStepCompleted[4] = true;
        }
      }
      
      // 加载第五步完成状态
      const step5Completed = localStorage.getItem('marketingCampaignStep5Completed');
      if (step5Completed === 'true') {
        this.showStepCompleted[4] = true;
      }
    },
    
    // 设置数据监听器
    setupWatchers() {
      // 监听初始任务变化，自动保存
      this.$watch('initialTask', (newVal) => {
        if (newVal.trim()) {
          localStorage.setItem('marketingCampaignInitialTask', newVal);
        }
      });
      
      // 监听补充信息变化，自动保存
      this.$watch('userSupplementInfo', (newVal) => {
        if (newVal.trim()) {
          localStorage.setItem('marketingCampaignSupplementInfo', newVal);
        }
      });
    },
    
    goBack() {
      this.$router.push('/practical-scenario')
    },
    
    // 从第一步过渡到第二步
    continueToNextStep() {
      if (!this.initialTask.trim()) return;
      
      // 保存到本地存储
      localStorage.setItem('marketingCampaignInitialTask', this.initialTask);
      
      // 标记第一步完成
      this.showStepCompleted[0] = true;
      localStorage.setItem('marketingCampaignStep1Completed', 'true');
      
      // 确保第二步相关状态正确
      this.taskInfoCompleted = false;
      
      console.log('继续到下一步，第一步完成状态:', this.showStepCompleted[0]);
      
      // 滚动到第二步
      setTimeout(() => {
        const secondStep = document.querySelector('.workflow-steps .step:nth-child(2)');
        if (secondStep) {
          secondStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 500);
    },
    
    // 重置当前步骤（用于调试）
    resetCurrentStep() {
      this.taskInfoCompleted = false;
      this.isAnalyzing = false;
      localStorage.removeItem('marketingCampaignFullTaskInfo');
      localStorage.removeItem('marketingCampaignTaskInfoSaved');
    },
    
    // 获取AI辅助分析
    async getAIAssistance() {
      if (this.isAnalyzing || !this.initialTask.trim() || !this.userSupplementInfo.trim()) return;
      
      this.isAnalyzing = true;
      this.aiResponse = '';
      this.processingError = '';
      
      // 重置所有步骤状态
      this.processingSteps.forEach((step, i) => {
        step.completed = false;
        step.current = i === 0;  // 第一步为当前步骤
      });
      this.processingStep = 0;
      
      try {
        // 构建提示词，要求大模型返回结构化的内容，更加关注已有信息
        const prompt = `你是一位资深的项目管理专家和营销策划顾问。请仔细阅读并理解以下市场活动策划任务信息，并帮助梳理出完整的任务框架。

## 初始任务信息:
${this.initialTask}

## 用户补充的信息:
${this.userSupplementInfo}

我需要你详细分析这两部分信息，确保不遗漏任何关键点（特别是产品卖点、目标用户、活动目标等），并整理出5个核心任务信息项。这5个信息项应该能够完整覆盖市场活动策划所需的关键要素。

对于这5个信息项，请遵循以下规则：
1. 如果初始任务或用户补充信息中已包含相关内容，请提取并填充到对应字段中
2. 如果某项关键信息缺失，则留空并提供合适的引导提示
3. 所有必要的产品特性、目标用户特征等关键信息必须被保留和归类
4. 确保这5个信息项能够涵盖完成一个专业市场活动策划的核心要素
5. 注意：我会在你的5个信息项之后自动添加一个"其他需要完善的内容"项，所以你不需要包含这类通用的补充字段

请以下面的JSON格式返回5个信息项：
{
  "fields": [
    {
      "label": "信息项的名称（如'产品核心卖点及特性'）",
      "value": "从初始任务或用户补充信息中提取的已有内容",
      "placeholder": "用户应该在此项填写的内容提示",
      "required": true或false（此项是否必填）
    },
    {...},
    {...},
    {...},
    {...}
  ],
  "analysis": "对任务的整体分析和建议，以及如何通过这5个方面完整描述任务"
}

非常重要：你的返回必须是严格有效的JSON格式，不要有任何额外的文本说明。同时，确保不丢失任何产品卖点、目标用户、活动目标等关键信息，这些都应该被合理地归类到5个信息项中。`;

        // 等待一会儿再进入下一步，显示当前步骤的状态
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 进入第二步
        this.completeCurrentStep();
        
        // 准备API请求参数
        const requestData = {
          model: 'deepseek-v3', // 使用DeepSeek-V3模型
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.2, // 降低temperature以获得更确定的结构化输出
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

        // 等待一会儿再进入下一步，显示当前步骤的状态
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 进入第三步
        this.completeCurrentStep();

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
                
                // 等待一会儿再进入下一步，显示当前步骤的状态
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // 进入第四步
                this.completeCurrentStep();
                
                // 处理数据并进入下一阶段
                this.processAIResponse();
                
                // 完成所有步骤
                await new Promise(resolve => setTimeout(resolve, 1000));
                this.completeCurrentStep();
                
                // 结束分析状态
                setTimeout(() => {
                  this.isAnalyzing = false;
                }, 500);
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
                    // 等待一会儿再进入下一步，显示当前步骤的状态
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                    // 进入第四步
                    this.completeCurrentStep();
                    
                    // 处理数据并进入下一阶段
                    this.processAIResponse();
                    
                    // 完成所有步骤
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    this.completeCurrentStep();
                    
                    // 结束分析状态
                    setTimeout(() => {
                      this.isAnalyzing = false;
                    }, 500);
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
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
            this.processingError = '处理过程出错，请重试';
            this.isAnalyzing = false;
          }
        };
        
        // 开始读取流
        readStream();
        
      } catch (error) {
        console.error("请求出错:", error);
        this.processingError = '处理过程出错，请重试';
        this.isAnalyzing = false;
      }
    },
    
    // 完成当前步骤并进入下一步
    completeCurrentStep() {
      // 标记当前步骤为已完成
      if (this.processingStep < this.processingSteps.length) {
        this.processingSteps[this.processingStep].completed = true;
        this.processingSteps[this.processingStep].current = false;
      }
      
      // 前进到下一步
      this.processingStep++;
      
      // 如果还有下一步，标记为当前步骤
      if (this.processingStep < this.processingSteps.length) {
        this.processingSteps[this.processingStep].current = true;
      }
    },
    
    // 处理AI响应，提取任务字段
    processAIResponse() {
      if (!this.aiResponse) return;
      
      try {
        // 尝试从响应中提取JSON
        const jsonMatch = this.aiResponse.match(/(\{[\s\S]*\})/);
        if (jsonMatch && jsonMatch[0]) {
          const jsonStr = jsonMatch[0];
          const data = JSON.parse(jsonStr);
          
          if (data.fields && Array.isArray(data.fields)) {
            // 复制AI返回的字段
            this.taskFields = [...data.fields];
            
            // 添加"任务时限"字段
            this.taskFields.push({
              label: "任务时限",
              value: "5天",
              placeholder: "请输入任务的时间限制，例如：几天或具体日期",
              required: true
            });
            
            // 添加"其他需要完善的内容"字段
            this.taskFields.push({
              label: "其他需要完善的内容",
              value: "",
              placeholder: "请输入任何其他你认为需要补充的信息，如特殊要求、注意事项、参考案例等",
              required: false
            });
            
            // 保存到本地存储
            localStorage.setItem('marketingCampaignTaskFields', JSON.stringify(this.taskFields));
            localStorage.setItem('marketingCampaignAIAnalysis', data.analysis || '');
          }
        } else {
          console.error('无法从AI响应中提取有效的JSON');
          this.processingError = '无法解析AI返回的结果，请重试';
        }
      } catch (error) {
        console.error('处理AI响应时出错:', error);
        this.processingError = '处理AI返回结果时出错，请重试';
      }
    },
    
    // 生成完整任务信息
    async generateFullTaskInfo() {
      if (!this.canGenerateTaskInfo) return;
      
      this.isGeneratingTaskInfo = true;
      
      try {
        // 构建用户已填写的字段内容
        const fieldsContent = this.taskFields.map(field => {
          return `${field.label}: ${field.value}`;
        }).join('\n\n');
        
        // 构建提示词，要求大模型生成描述性任务文字
        const prompt = `你是一位资深的项目管理专家和营销策划顾问。请基于以下信息，整理出一段清晰、完整的市场活动策划任务描述。

## 初始任务信息:
${this.initialTask}

## 用户补充的信息:
${this.userSupplementInfo}

## 用户填写的5个关键任务信息项:
${fieldsContent}

请将上述所有信息整合为一段连贯、专业的任务描述性文字。这不是完整的任务书或策划案，而是对任务本身的清晰描述。要求：
1. 整合所有关键信息，包括产品特性、目标用户、营销目标等
2. 保持专业、简洁的语言风格
3. 确保描述全面但不冗余
4. 突出关键点，使人一读就能理解任务的核心内容
5. 篇幅适中，通常不超过500字

请直接输出文字内容，不需要添加标题或格式。`;

        // 准备API请求参数
        const requestData = {
          model: 'deepseek-v3', // 使用DeepSeek-V3模型
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.3,
          max_tokens: 1000
        };

        // 创建一个用于显示流式输出的变量
        this.fullTaskInfo = '';
        this.taskInfoCompleted = true;
        
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
                this.isGeneratingTaskInfo = false;
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
                    this.isGeneratingTaskInfo = false;
                    // 格式化文本内容，增强可读性
                    this.fullTaskInfo = this.fullTaskInfo
                      // 确保标点符号后有适当的换行
                      .replace(/([。！？；])\s*/g, '$1\n')
                      // 为数字列表添加换行
                      .replace(/(\d+)[.、]([^，。！？；\n])/g, '\n$1.$2')
                      // 压缩多余的换行
                      .replace(/\n{3,}/g, '\n\n');
                    
                    // 保存到本地存储
                    localStorage.setItem('marketingCampaignFullTaskInfo', this.fullTaskInfo);
                    
                    // 滚动到文本框底部，方便用户阅读完整内容
                    this.$nextTick(() => {
                      const textarea = document.querySelector('.editable-task-info');
                      if (textarea) {
                        textarea.scrollTop = textarea.scrollHeight;
                      }
                    });
                    
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理内容增量
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      this.fullTaskInfo += deltaContent;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.isGeneratingTaskInfo = false;
          }
        };
        
        // 开始读取流
        readStream();
        
      } catch (error) {
        console.error("请求出错:", error);
        this.isGeneratingTaskInfo = false;
      }
    },
    
    // 完成任务信息生成（移除此方法，已合并到generateFullTaskInfo中）
    finishTaskInfoGeneration(content) {
      // 此方法内容已合并到generateFullTaskInfo中的流处理逻辑里
    },
    
    // 保存完整任务信息
    saveTaskInfo() {
      if (!this.fullTaskInfo.trim()) return;
      
      this.taskInfoSaved = true;
      this.showStepCompleted[1] = true;
      
      // 保存到本地存储
      localStorage.setItem('marketingCampaignTaskInfoSaved', 'true');
      localStorage.setItem('marketingCampaignStep2Completed', 'true');
      
      // 显示成功消息并滚动到下一步
      setTimeout(() => {
        const thirdStep = document.querySelector('.workflow-steps .step:nth-child(3)');
        if (thirdStep) {
          thirdStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 500);
    },
    
    // 获取AI辅助任务拆解
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
      
      // 模拟步骤进度更新
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
系统功能列表（营销活动策划推荐使用的AI工具）：

文本内容创作：
(1) 广告语创作 - http://123.57.71.66:8018/text-creation/marketing/ad-slogan
(2) 公众号文章创作 - http://123.57.71.66:8018/text-creation/new-media/wechat
(3) 微博文章创作 - http://123.57.71.66:8018/text-creation/new-media/weibo
(4) 小红书笔记创作 - http://123.57.71.66:8018/text-creation/new-media/xiaohongshu
(5) 短视频脚本创作 - http://123.57.71.66:8018/text-creation/new-media/short-video
(6) 直播脚本创作 - http://123.57.71.66:8018/text-creation/new-media/livestream
(7) 营销文案创作 - http://123.57.71.66:8018/text-creation/marketing/copywriting-generator

图形内容创作：
(1) 产品商品图设计 - http://123.57.71.66:8018/image-creation/image-to-painter
(2) 文生图 - http://123.57.71.66:8018/image-creation/text-to-image

视频内容创作：
(1) 高级数字人产品口播视频制作 - http://123.57.71.66:8018/digital-human/advance-video

演示文稿创作：
(1) 营销方案汇报PPT创作 - http://123.57.71.66:8018/ai-office/integration-test`;

        // 构建提示词
        const prompt = `你是一位资深的项目管理专家和营销策划顾问。请帮我针对以下市场活动策划任务进行细化拆解。

## 完整任务信息:
${this.fullTaskInfo}

## 用户对任务拆解的初步想法:
${this.userTaskBreakdown}

## 系统功能列表:
${systemFeatures}

请基于以上信息，将市场活动策划任务拆解为模块和子任务。请遵循以下要求：

1. 总共拆解出至少12个子任务，最多不超过15个子任务
2. 每个任务必须具体、清晰，易于执行
3. 必须包含以下所有系统功能对应的任务（每个功能必须单独设置一个任务）：
   - 广告语创作
   - 公众号文章创作
   - 微博文章创作
   - 小红书笔记创作
   - 短视频脚本创作
   - 直播脚本创作
   - 产品商品图设计
   - 高级数字人产品口播视频制作
   - 营销文案创作
   - 营销方案汇报PPT创作
4. 任务拆解要合理、全面，覆盖市场活动策划的关键环节
5. 不要包含任务优先级和执行计划（这将在后续步骤中处理）
6. 结合用户的初步想法和完整任务信息

非常重要的规则：
1. 请勿将多个系统功能合并到同一个任务中，例如不要出现"微博文章创作/公众号文章创作/小红书文章创作"这样的合并
2. 每个系统功能必须对应一个单独的任务
3. 每个任务必须只使用一个系统功能（如果适用）

对于每个任务，如果它可以使用我们的系统功能来完成，请标注出相应的系统功能名称和链接。

请以下面的JSON格式返回拆解结果：

\`\`\`json
[
  {
    "title": "主要模块1名称（如'目标受众分析'）",
    "subtasks": [
      {
        "task": "子任务1描述",
        "systemFeature": "相关系统功能名称（如果适用）",
        "systemLink": "系统功能链接（如果适用）"
      },
      "子任务2描述（无关联系统功能的任务直接用字符串表示）",
      ...
    ]
  },
  {
    "title": "主要模块2名称",
    "subtasks": [
      ...
    ]
  },
  ...
]
\`\`\`

请特别注意：
1. 确保每个指定的系统功能都被使用且每个功能单独对应一个任务
2. 必须确保JSON格式有效，可以被前端直接解析
3. 如果子任务不关联系统功能，可以直接用字符串表示，不需要对象结构
4. 关联系统功能的任务必须提供systemFeature和systemLink字段`;

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

        // 模拟分析任务信息完成
        setTimeout(() => updateProcessingStep(2), 2500);
        // 模拟拆解任务模块完成
        setTimeout(() => updateProcessingStep(3), 5000);
        // 模拟关联系统功能完成
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
      this.isAnalyzingBreakdown = false;
      
      try {
        // 提取JSON内容
        const jsonMatch = content.match(/```json\s*([\s\S]*?)\s*```/) || content.match(/\[\s*\{[\s\S]*\}\s*\]/);
        let jsonStr = '';
        
        if (jsonMatch && jsonMatch[1]) {
          jsonStr = jsonMatch[1];
        } else if (jsonMatch && jsonMatch[0]) {
          jsonStr = jsonMatch[0];
        } else {
          jsonStr = content.trim();
        }
        
        // 解析JSON
        const parsedData = JSON.parse(jsonStr);
        
        if (Array.isArray(parsedData) && parsedData.length > 0) {
          // 处理数据，确保每个子任务有一致的数据结构
          const processedData = parsedData.map(module => {
            // 确保subtasks是数组
            if (!Array.isArray(module.subtasks)) {
              module.subtasks = [];
            }
            
            // 处理子任务，确保格式一致
            module.subtasks = module.subtasks.map(subtask => {
              // 如果子任务是字符串，保持原样
              if (typeof subtask === 'string') {
                return subtask;
              }
              
              // 如果子任务是对象，确保所需字段存在
              if (typeof subtask === 'object') {
                return {
                  task: subtask.task || '',
                  systemFeature: subtask.systemFeature || '',
                  systemLink: subtask.systemLink || ''
                };
              }
              
              return subtask;
            });
            
            return module;
          });
          
          this.parsedTaskBreakdown = processedData;
          this.taskBreakdownResult = JSON.stringify(processedData, null, 2);
          this.tasksGenerated = true;
          
          // 保存到本地存储
          localStorage.setItem('marketingCampaignBreakdownResult', this.taskBreakdownResult);
          localStorage.setItem('marketingCampaignUserBreakdown', this.userTaskBreakdown);
        } else {
          console.error('解析的任务拆解数据不是有效的数组');
        }
      } catch (error) {
        console.error('处理任务拆解结果出错:', error);
        // 尝试直接显示原始结果
        this.taskBreakdownResult = content;
      }
    },
    
    // 开始编辑任务拆解结果
    startEditingBreakdown() {
      this.editableTaskBreakdown = this.taskBreakdownResult;
      this.editingBreakdown = true;
    },
    
    // 取消编辑
    cancelEditingBreakdown() {
      this.editingBreakdown = false;
    },
    
    // 保存任务拆解
    saveTaskBreakdown() {
      try {
        // 验证JSON格式是否有效
        const parsed = JSON.parse(this.editableTaskBreakdown);
        
        if (Array.isArray(parsed) && parsed.length > 0) {
          this.parsedTaskBreakdown = parsed;
          this.taskBreakdownResult = this.editableTaskBreakdown;
          this.editingBreakdown = false;
          this.taskBreakdownSaved = true;
          this.showStepCompleted[2] = true;
          
          // 保存到本地存储
          localStorage.setItem('marketingCampaignBreakdownResult', this.taskBreakdownResult);
          localStorage.setItem('marketingCampaignBreakdownSaved', 'true');
          
          // 滚动到下一步
          setTimeout(() => {
            const fourthStep = document.querySelector('.workflow-steps .step:nth-child(4)');
            if (fourthStep) {
              fourthStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          }, 500);
        } else {
          alert('数据格式有误，请确保是有效的任务拆解JSON数组');
        }
      } catch (error) {
        alert('JSON格式无效，请检查您的编辑内容');
        console.error('保存任务拆解时出错:', error);
      }
    },
    
    // 计算总天数
    calculateTotalDays() {
      if (!this.parsedTaskPlan || this.parsedTaskPlan.length === 0) return;
      
      let maxEndDay = 0;
      this.parsedTaskPlan.forEach(task => {
        const endDay = this.getTaskEndDay(task);
        if (endDay > maxEndDay) {
          maxEndDay = endDay;
        }
      });
      
      this.totalDays = Math.max(7, maxEndDay); // 至少7天
    },
    
    // 获取任务的开始天数（用于甘特图）
    getTaskStartDay(task) {
      if (!task.startDate) return 1;
      
      // 从"第X天"格式中提取数字
      const match = task.startDate.match(/第(\d+)天/);
      if (match && match[1]) {
        return parseInt(match[1]);
      }
      
      return 1;
    },
    
    // 获取任务的结束天数（用于计算总天数）
    getTaskEndDay(task) {
      if (!task.endDate) return 7;
      
      // 从"第X天"格式中提取数字
      const match = task.endDate.match(/第(\d+)天/);
      if (match && match[1]) {
        return parseInt(match[1]);
      }
      
      return 7;
    },
    
    // 获取任务的持续天数（用于甘特图宽度）
    getTaskDurationDays(task) {
      const startDay = this.getTaskStartDay(task);
      const endDay = this.getTaskEndDay(task);
      return Math.max(1, endDay - startDay + 1); // 至少1天
    },
    
    // 获取AI辅助任务计划
    async getAITaskPlan() {
      if (this.isAnalyzingPlan || !this.taskBreakdownResult || !this.userTaskConstraints.trim()) return;
      
      this.isAnalyzingPlan = true;
      this.planGenerated = false;
      this.planProcessingError = '';
      
      // 初始化处理步骤
      this.planProcessingStep = 0;
      this.planProcessingSteps.forEach(step => {
        step.completed = false;
        step.current = false;
      });
      this.planProcessingSteps[0].current = true;
      
      // 模拟步骤进度更新
      const updateProcessingStep = (step) => {
        if (step > 0 && step <= this.planProcessingSteps.length) {
          this.planProcessingSteps[step - 1].completed = true;
          this.planProcessingSteps[step - 1].current = false;
        }
        
        this.planProcessingStep = step;
        
        if (step < this.planProcessingSteps.length) {
          this.planProcessingSteps[step].current = true;
        }
      };
      
      try {
        // 模拟启动AI助手完成
        setTimeout(() => updateProcessingStep(1), 800);
        
        // 构建提示词
        const prompt = `你是一位资深的项目管理专家和营销策划顾问。请帮我为以下市场活动策划任务制定一个详细的工作计划。

## 完整任务信息:
${this.fullTaskInfo}

## 任务拆解结果:
${this.taskBreakdownResult}

## 用户提供的时间和约束条件:
${this.userTaskConstraints}

请基于以上信息，为每个任务分配优先级、预计耗时和结束时间。要求：

1. 合理安排任务优先级，考虑任务的依赖关系和重要性
2. 为每个任务分配适当的时间，确保整体计划符合用户提供的时间约束
3. 如果任务可以使用系统功能完成，保留其系统功能信息
4. 结束时间请使用"第X天"的格式，便于直观理解

请以下面的JSON格式返回工作计划：

\`\`\`json
[
  {
    "taskName": "任务名称1",
    "priority": "高/中/低",
    "duration": "预计耗时（如2小时、0.5天等）",
    "endDate": "结束时间（如第X天）",
    "systemFeature": "相关系统功能名称（如果适用）",
    "systemLink": "系统功能链接（如果适用）"
  },
  {
    "taskName": "任务名称2",
    ...
  },
  ...
]
\`\`\`

注意：
1. 优先级只能是"高"、"中"、"低"三个级别之一
2. 确保计划的合理性和可行性，避免时间冲突或不切实际的安排
3. 任务顺序应按照计划执行的先后顺序排列
4. 一定要合理分配任务，确保能在总体时间范围内完成所有任务
5. 根据任务拆解结果中的系统功能信息，正确关联对应的系统功能和链接`;

        // 准备API请求参数
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.3,
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

        // 模拟分析任务拆解完成
        setTimeout(() => updateProcessingStep(2), 2500);
        // 模拟规划任务优先级完成
        setTimeout(() => updateProcessingStep(3), 5000);
        // 模拟安排时间线完成
        setTimeout(() => updateProcessingStep(4), 7500);

        // 处理流式响应
        let planContent = '';
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
                this.processPlanResult(planContent);
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
                    this.processPlanResult(planContent);
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    // 处理内容增量
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      planContent += deltaContent;
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.planProcessingError = "读取流出错，请重试";
            this.isAnalyzingPlan = false;
          }
        };
        
        // 开始读取流
        readStream();
        
      } catch (error) {
        console.error("请求出错:", error);
        this.planProcessingError = "请求出错，请重试";
        this.isAnalyzingPlan = false;
      }
    },
    
    // 处理工作计划结果
    processPlanResult(content) {
      this.isAnalyzingPlan = false;
      
      try {
        // 提取JSON内容
        const jsonMatch = content.match(/```json\s*([\s\S]*?)\s*```/) || content.match(/\[\s*\{[\s\S]*\}\s*\]/);
        let jsonStr = '';
        
        if (jsonMatch && jsonMatch[1]) {
          jsonStr = jsonMatch[1];
        } else if (jsonMatch && jsonMatch[0]) {
          jsonStr = jsonMatch[0];
        } else {
          jsonStr = content.trim();
        }
        
        // 解析JSON
        const parsedData = JSON.parse(jsonStr);
        
        if (Array.isArray(parsedData) && parsedData.length > 0) {
          this.parsedTaskPlan = parsedData;
          this.taskPlanResult = JSON.stringify(parsedData, null, 2);
          this.planGenerated = true;
          
          // 计算总天数
          this.calculateTotalDays();
          
          // 提取系统功能任务
          this.extractSystemTasks();
          
          // 保存到本地存储
          localStorage.setItem('marketingCampaignPlanResult', this.taskPlanResult);
          localStorage.setItem('marketingCampaignUserConstraints', this.userTaskConstraints);
          
          // 标记第四步完成
          this.showStepCompleted[3] = true;
          localStorage.setItem('marketingCampaignStep4Completed', 'true');
          
          // 调整甘特图行高
          setTimeout(() => this.adjustGanttRowHeights(), 300);
        } else {
          console.error('解析的工作计划数据不是有效的数组');
        }
      } catch (error) {
        console.error('处理工作计划结果出错:', error);
        // 尝试直接显示原始结果
        this.taskPlanResult = content;
      }
    },
    
    // 开始编辑工作计划
    startEditingPlan() {
      this.editableTaskPlan = this.taskPlanResult;
      this.editingPlan = true;
    },
    
    // 取消编辑
    cancelEditingPlan() {
      this.editingPlan = false;
    },
    
    // 保存工作计划
    saveTaskPlan() {
      try {
        // 验证JSON格式是否有效
        const parsed = JSON.parse(this.editableTaskPlan);
        
        if (Array.isArray(parsed) && parsed.length > 0) {
          this.parsedTaskPlan = parsed;
          this.taskPlanResult = this.editableTaskPlan;
          this.editingPlan = false;
          this.taskPlanSaved = true;
          this.showStepCompleted[3] = true;
          
          // 重新计算总天数
          this.calculateTotalDays();
          
          // 保存到本地存储
          localStorage.setItem('marketingCampaignPlanResult', this.taskPlanResult);
          localStorage.setItem('marketingCampaignPlanSaved', 'true');
          
          // 添加这一行：调整甘特图行高
          setTimeout(() => this.adjustGanttRowHeights(), 300);
          
          // 滚动到下一步
          setTimeout(() => {
            const fifthStep = document.querySelector('.workflow-steps .step:nth-child(5)');
            if (fifthStep) {
              fifthStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          }, 500);
        } else {
          alert('数据格式有误，请确保是有效的工作计划JSON数组');
        }
      } catch (error) {
        alert('JSON格式无效，请检查您的编辑内容');
        console.error('保存工作计划时出错:', error);
      }
    },
    
    // 从第三步继续到第四步
    continueToStep4() {
      // 滚动到第四步
      setTimeout(() => {
        const fourthStep = document.querySelector('.workflow-steps .step:nth-child(4)');
        if (fourthStep) {
          fourthStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 300);
    },
    
    // 下载表格为CSV文件
    downloadTableAsCSV() {
      if (!this.parsedTaskPlan || this.parsedTaskPlan.length === 0) {
        alert('没有可下载的数据');
        return;
      }
      
      // 构建CSV内容
      let csvContent = '任务名称,优先级,预计耗时,结束时间,系统功能\r\n';
      
      this.parsedTaskPlan.forEach(task => {
        const systemFeature = task.systemFeature || '';
        const row = [
          `"${task.taskName}"`,
          `"${task.priority}"`,
          `"${task.duration}"`,
          `"${task.endDate}"`,
          `"${systemFeature}"`
        ].join(',');
        
        csvContent += row + '\r\n';
      });
      
      // 创建下载链接
      const encodedUri = encodeURI('data:text/csv;charset=utf-8,' + csvContent);
      const link = document.createElement('a');
      link.setAttribute('href', encodedUri);
      link.setAttribute('download', '市场活动工作计划.csv');
      document.body.appendChild(link);
      
      // 触发下载
      link.click();
      
      // 清理
      document.body.removeChild(link);
    },
    
    // 计算甘特图行高（已不使用）
    adjustGanttRowHeights() {
      // 此方法不再使用，但保留方法体以免引用它的地方报错
      console.log("甘特图功能已移除");
    },
    
    // 下载甘特图为图片（已不使用）
    downloadGanttAsImage() {
      // 此方法不再使用，但保留方法体以免引用它的地方报错
      console.log("甘特图功能已移除");
    },
    
    // 获取任务的开始天数（已不使用）
    getTaskStartDay(task) {
      if (!task.startDate) return 1;
      
      // 从"第X天"格式中提取数字
      const match = task.startDate.match(/第(\d+)天/);
      if (match && match[1]) {
        return parseInt(match[1]);
      }
      
      return 1;
    },
    
    // 获取任务的结束天数（用于计算总天数）
    getTaskEndDay(task) {
      if (!task.endDate) return 7;
      
      // 从"第X天"格式中提取数字
      const match = task.endDate.match(/第(\d+)天/);
      if (match && match[1]) {
        return parseInt(match[1]);
      }
      
      return 7;
    },
    
    // 获取任务的持续天数（已不使用）
    getTaskDurationDays(task) {
      const startDay = this.getTaskStartDay(task);
      const endDay = this.getTaskEndDay(task);
      return Math.max(1, endDay - startDay + 1); // 至少1天
    },
    
    // 从第四步继续到第五步
    continueToStep5() {
      if (!this.planGenerated) return;
      
      // 提取系统功能任务
      this.extractSystemTasks();
      
      // 滚动到第五步
      setTimeout(() => {
        const fifthStep = document.querySelector('.workflow-steps .step:nth-child(5)');
        if (fifthStep) {
          fifthStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 300);
    },
    
    // 提取包含系统功能的任务
    extractSystemTasks() {
      if (!this.parsedTaskPlan || this.parsedTaskPlan.length === 0) return;
      
      // 过滤出包含systemFeature和systemLink的任务
      this.systemTasks = this.parsedTaskPlan.filter(task => 
        task.systemFeature && task.systemLink
      );
      
      // 保存到本地存储
      localStorage.setItem('marketingCampaignSystemTasks', JSON.stringify(this.systemTasks));
    },
    
    // 标记任务为已完成
    markTasksComplete() {
      // 如果已经100%完成，不再增加
      if (this.completionProgress >= 100) return;
      
      // 否则，每次增加20%，最多至100%
      this.completionProgress = Math.min(100, this.completionProgress + 20);
      
      // 保存到本地存储
      localStorage.setItem('marketingCampaignCompletionProgress', this.completionProgress.toString());
      
      // 如果达到100%，标记第五步完成
      if (this.completionProgress >= 100) {
        this.showStepCompleted[4] = true;
        localStorage.setItem('marketingCampaignStep5Completed', 'true');
        
        // 滚动到"AI辅助成果"部分
        setTimeout(() => {
          const resultsSection = document.querySelector('.ai-results-section');
          if (resultsSection) {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 500);
      }
    },
    
    // 直接从任务拆解继续到第四步
    continueToStep4FromBreakdown() {
      if (!this.taskBreakdownResult) return;
      
      // 标记任务拆解已保存
      this.taskBreakdownSaved = true;
      this.showStepCompleted[2] = true;
      
      // 保存到本地存储
      localStorage.setItem('marketingCampaignBreakdownSaved', 'true');
      
      // 滚动到第四步
      setTimeout(() => {
        const fourthStep = document.querySelector('.workflow-steps .step:nth-child(4)');
        if (fourthStep) {
          fourthStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 300);
    },
    
    // 显示产品信息
    showProductInfo() {
      this.productInfoVisible = true;
    },
    
    // 隐藏产品信息
    hideProductInfo() {
      this.productInfoVisible = false;
    },
    
    // 复制产品信息
    copyProductInfo() {
      const productInfo = `
【TechWatch Pro 产品信息】

产品核心卖点:
• 超长续航能力: 单次充电可使用7天，采用高效锂电池和智能电量管理系统，满足商务出差和旅行用户需求
• AI健康管理功能: 包括高精度心率监测、睡眠分析、压力监测、呼吸训练和全天候活动跟踪，配合专业算法提供个性化健康建议
• 全新交互体验: 支持手势控制和语音助手，配备高清触控屏幕，操作更流畅直观
• 智能连接功能: 无缝连接手机，智能推送消息、来电提醒，可直接接听电话和回复消息
• 防水防尘设计: 达到IP68级别，可在水下50米使用，适合游泳和潜水爱好者

目标用户群体:
• 年轻商务人士: 25-40岁，重视效率和专业形象，需要智能设备辅助工作和健康管理
• 健康生活爱好者: 关注身体健康数据，热爱运动，注重生活品质的消费者
• 科技早期采用者: 喜欢尝试新技术产品，对智能穿戴设备有浓厚兴趣的人群

产品定位与价格:
TechWatch Pro 定位为中高端智能手表市场，零售价格区间为1499-1999元人民币（根据配置不同），与同类产品相比具有更高的性价比和更全面的功能。
      `;
      
      // 检查navigator.clipboard是否可用
      if (navigator.clipboard && navigator.clipboard.writeText) {
        // 使用现代API复制文本
        navigator.clipboard.writeText(productInfo)
          .then(() => {
            this.showCopySuccess();
          })
          .catch(err => {
            console.error('使用Clipboard API复制失败:', err);
            this.fallbackCopyText(productInfo);
          });
      } else {
        // 回退到传统方法
        this.fallbackCopyText(productInfo);
      }
    },
    
    // 显示复制成功提示
    showCopySuccess() {
      // 创建一个临时元素显示复制成功
      const notification = document.createElement('div');
      notification.className = 'copy-notification';
      notification.innerHTML = '<i class="ri-check-line"></i> 产品信息已复制到剪贴板';
      document.body.appendChild(notification);
      
      // 2秒后移除通知
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 2000);
    },
    
    // 传统复制方法（作为后备方案）
    fallbackCopyText(text) {
      try {
        // 创建临时textarea元素
        const textArea = document.createElement('textarea');
        textArea.value = text;
        
        // 设置样式使元素不可见
        textArea.style.position = 'fixed';
        textArea.style.top = '0';
        textArea.style.left = '0';
        textArea.style.width = '2em';
        textArea.style.height = '2em';
        textArea.style.padding = '0';
        textArea.style.border = 'none';
        textArea.style.outline = 'none';
        textArea.style.boxShadow = 'none';
        textArea.style.background = 'transparent';
        
        // 添加到DOM
        document.body.appendChild(textArea);
        
        // 选择文本
        textArea.select();
        textArea.setSelectionRange(0, text.length); // 兼容移动设备
        
        // 执行复制命令
        const successful = document.execCommand('copy');
        
        // 移除临时元素
        document.body.removeChild(textArea);
        
        if (successful) {
          this.showCopySuccess();
        } else {
          alert('复制失败，请手动复制');
        }
      } catch (err) {
        console.error('复制失败:', err);
        alert('复制失败，请手动复制');
      }
    },
    
    // 根据字段标签返回适当的行数
    getFieldRows(label) {
      // 为"产品核心卖点及特性"增加高度
      if (label === "产品核心卖点及特性") {
        return 4;
      }
      // 为特定字段减少高度
      else if (
        label === "活动核心目标" || 
        label === "产品定位与价格策略" || 
        label === "线上线下活动形式需求" || 
        label === "任务时限"
      ) {
        return 1;
      }
      // 其他字段保持默认高度
      return 2;
    },
  },
  updated() {
    // 在组件更新后检查是否需要调整甘特图行高
    if (this.parsedTaskPlan && this.parsedTaskPlan.length > 0 && this.taskPlanResult) {
      this.adjustGanttRowHeights();
    }
  },
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
  background-image: url('../../../public/backgrounds/marketing-header-bg.jpeg');
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
  margin: 0 0 15px;
  color: #333;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
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
  align-items: center;
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

.ai-analysis-section {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fd;
  border-radius: 8px;
  border: 1px solid #e1e4e8;
}

.analyzing-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(58, 97, 134, 0.2);
  border-radius: 50%;
  border-top-color: #3a6186;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  margin-top: 15px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(to right, #89253e, #e6b980);
  border-radius: 4px;
  transition: width 0.3s ease;
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
</style> 