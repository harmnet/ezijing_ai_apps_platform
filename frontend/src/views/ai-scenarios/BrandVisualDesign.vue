<template>
  <div class="brand-visual-design-container">
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
        <h1 class="main-title">迎新晚会策划 <span class="scenario-category">高校场景实践</span></h1>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="container">
      <!-- 角色介绍部分 -->
      <div class="section role-section">
        <h2 class="section-title">
          <i class="ri-user-line"></i> 你的角色
        </h2>
        <div class="role-card content-card">
          <div class="role-avatar">
            <img src="@/assets/images/scenarios/student-leader.png" alt="学生会文艺部骨干" />
          </div>
          <div class="role-info">
            <h3>学生会文艺部骨干 - 小赵</h3>
            <p>你是紫荆花大学学生会文艺部的骨干成员小赵，大三学生，已经在学生会工作两年。你热情活泼，有良好的组织和协调能力，曾参与组织过多次校园文化活动。领导对你非常信任，这次委派你负责即将到来的迎新晚会策划工作，这是展示你能力的重要机会。你需要制定一个全面而详细的晚会策划方案，并且协调各个部门共同完成这项任务。</p>
          </div>
        </div>
      </div>

      <!-- 任务背景部分 -->
      <div class="section task-section">
        <h2 class="section-title">
          <i class="ri-task-line"></i> 任务背景
        </h2>
        <div class="task-card content-card">
          <div class="task-content">
            <p>新学期即将开始，紫荆花大学传统的迎新晚会将在一个月后举行。这场晚会是学校最重要的年度活动之一，旨在欢迎新生融入大学生活，展示校园文化，增强学校凝聚力。学生会主席李明找到你，希望你能担任本次迎新晚会的主要策划人。他对你说："小赵，迎新晚会是学校的传统盛事，关系到新生对学校的第一印象，也是学生会展示风采的重要舞台。今年校领导特别重视，希望能办出新意，让晚会既有文化内涵又能充分调动新生的参与热情。我们需要在一个月内完成所有准备工作，包括节目征集、舞台设计、人员安排等各个方面。考虑到你在文艺部的出色表现，这次任务就交给你负责了。"这是你第一次独立负责如此重要的校园活动，既感到压力，也看到了展示自己能力的机会。</p>
          </div>
        </div>
      </div>

      <!-- 任务时限部分 -->
      <div class="section timeline-section">
        <h2 class="section-title">
          <i class="ri-time-line"></i> 任务时限
        </h2>
        <div class="timeline-card content-card">
          <div class="timeline-content">
            <p>距离迎新晚会还有30天，学生会主席李明要求你在一个月内完成全部策划和准备工作。晚会策划初稿需在下周内完成并提交审核，之后根据反馈进行修改。你需要协调各部门完成节目征集、舞台设计和人员安排等准备工作。</p>
          </div>
        </div>
      </div>

      <!-- AI协助高效工作部分 -->
      <div class="section ai-section">
        <div class="ai-workflow-card">
          <div class="ai-header">
            <div class="ai-title" style="text-align: center; width: 100%;">
              <p class="task-content" style="text-align: center; color: #ffffff;">作为学生会文艺部骨干，小赵需要在短短一个月内完成紫荆花大学迎新晚会的策划工作！在校园活动组织的挑战面前，AI技术能否成为学生干部的得力助手？现在，我们可以借助人工智能的协作能力，提升策划效率与创意质量。跟随以下步骤，一起体验AI辅助校园活动策划的全新方式，让迎新晚会策划工作变得更加高效和专业！</p>
            </div>
          </div>
          
          <div class="workflow-steps">
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>获取初始任务</h4>
                <p class="task-content">学生会主席提出的迎新晚会要求往往是概括性的。主席可能只会提供核心要求和关键期望，而非完整的任务说明书。在这一步，我们需要先记录并确认已获得的初始任务信息，为后续深入分析打下基础。</p>
                
                <div class="input-container">
                  <textarea 
                    v-model="initialTask" 
                    placeholder="请输入学生会主席李明交给小赵的初始任务信息。" 
                    rows="3"
                    class="task-input"
                    maxlength="300"
                  ></textarea>
                  
                  <div class="input-footer">
                    <span class="character-count" :class="{ 'warning': initialTask && initialTask.length > 250 }">
                      {{ initialTask ? initialTask.length : 0 }}/300字
                    </span>
                    <button class="next-step-btn" @click="continueToNextStep" :disabled="!initialTask || !initialTask.trim()">
                      <i class="ri-arrow-right-line"></i> 继续下一步
                    </button>
                  </div>
                </div>
                
                <div v-if="showStepCompleted[0]" class="saved-message">
                  <i class="ri-checkbox-circle-line"></i> 任务信息已保存，可继续下一步
                </div>
              </div>
            </div>
            
            <!-- 第二步：利用5W2H方法来定位任务 -->
            <div class="step" v-if="showStepCompleted[0]">
              <div class="step-number">2</div>
              <div class="step-content">
                <div class="step-header">
                  <h4>利用5W2H方法来定位任务</h4>
                  <button class="knowledge-btn" @click="show5W2HDrawer">
                    <i class="ri-book-open-line"></i> 学习5W2H知识
                  </button>
                </div>
                <p class="task-content">5W2H是一种常用的任务分析方法，可以帮助我们更全面地理解任务。请根据学生会主席李明给出的初始任务信息，从以下七个维度进行思考和整理，明确迎新晚会策划的具体要求和边界。</p>
                
                <!-- 5W2H输入区 -->
                <div class="w2h-input-area">
                  <div class="w2h-item">
                    <div class="w2h-item-header">
                      <label><span class="w2h-label">What（做什么）</span>：需要完成的具体工作内容是什么？</label>
                      <button class="knowledge-btn auto-fill-btn" @click="autoFill('what')">
                        自动填写
                      </button>
                    </div>
                    <textarea 
                      v-model="w2hInputs.what" 
                      placeholder="例如：策划一场主题鲜明、节目丰富的迎新晚会" 
                      rows="2"
                      class="task-input"
                      @input="updateW2HSummary"
                    ></textarea>
                  </div>
                  
                  <div class="w2h-item">
                    <div class="w2h-item-header">
                      <label><span class="w2h-label">Why（为什么）</span>：为什么要做这项工作？目的和意义是什么？</label>
                      <button class="knowledge-btn auto-fill-btn" @click="autoFill('why')">
                        自动填写
                      </button>
                    </div>
                    <textarea 
                      v-model="w2hInputs.why" 
                      placeholder="例如：欢迎新生，展示校园文化，增强学校凝聚力" 
                      rows="2"
                      class="task-input"
                      @input="updateW2HSummary"
                    ></textarea>
                  </div>
                  
                  <div class="w2h-item">
                    <div class="w2h-item-header">
                      <label><span class="w2h-label">Who（谁来做）</span>：涉及哪些相关人员和部门？</label>
                      <button class="knowledge-btn auto-fill-btn" @click="autoFill('who')">
                        自动填写
                      </button>
                    </div>
                    <textarea 
                      v-model="w2hInputs.who" 
                      placeholder="例如：文艺部负责统筹，协调其他部门协助完成" 
                      rows="2"
                      class="task-input"
                      @input="updateW2HSummary"
                    ></textarea>
                  </div>
                  
                  <div class="w2h-item">
                    <div class="w2h-item-header">
                      <label><span class="w2h-label">When（何时做）</span>：时间节点和期限是什么？</label>
                      <button class="knowledge-btn auto-fill-btn" @click="autoFill('when')">
                        自动填写
                      </button>
                    </div>
                    <textarea 
                      v-model="w2hInputs.when" 
                      placeholder="例如：一个月内完成策划，下周形成初稿" 
                      rows="2"
                      class="task-input"
                      @input="updateW2HSummary"
                    ></textarea>
                  </div>
                  
                  <div class="w2h-item">
                    <div class="w2h-item-header">
                      <label><span class="w2h-label">Where（在哪做）</span>：活动地点和相关场地要求？</label>
                      <button class="knowledge-btn auto-fill-btn" @click="autoFill('where')">
                        自动填写
                      </button>
                    </div>
                    <textarea 
                      v-model="w2hInputs.where" 
                      placeholder="例如：学校大礼堂，需要考虑场地容纳量和设备条件" 
                      rows="2"
                      class="task-input"
                      @input="updateW2HSummary"
                    ></textarea>
                  </div>
                  
                  <div class="w2h-item">
                    <div class="w2h-item-header">
                      <label><span class="w2h-label">How（怎么做）</span>：实施方法和需要注意的事项？</label>
                      <button class="knowledge-btn auto-fill-btn" @click="autoFill('how')">
                        自动填写
                      </button>
                    </div>
                    <textarea 
                      v-model="w2hInputs.how" 
                      placeholder="例如：节目征集、舞台设计、人员安排等具体执行方式" 
                      rows="2"
                      class="task-input"
                      @input="updateW2HSummary"
                    ></textarea>
                  </div>
                  
                  <div class="w2h-item">
                    <div class="w2h-item-header">
                      <label><span class="w2h-label">How much（多少资源）</span>：需要的预算和资源？</label>
                      <button class="knowledge-btn auto-fill-btn" @click="autoFill('howMuch')">
                        自动填写
                      </button>
                    </div>
                    <textarea 
                      v-model="w2hInputs.howMuch" 
                      placeholder="例如：预算限制，可调用的人力物力资源" 
                      rows="2"
                      class="task-input"
                      @input="updateW2HSummary"
                    ></textarea>
                  </div>
                </div>
                
                <!-- 整合后的5W2H内容展示 -->
                <div class="w2h-summary" v-if="hasAnyW2HInput">
                  <h5>5W2H任务定位总结</h5>
                  <div class="w2h-summary-content">
                    <p v-if="w2hInputs.what"><strong>What（做什么）：</strong>{{ w2hInputs.what }}</p>
                    <p v-if="w2hInputs.why"><strong>Why（为什么）：</strong>{{ w2hInputs.why }}</p>
                    <p v-if="w2hInputs.who"><strong>Who（谁来做）：</strong>{{ w2hInputs.who }}</p>
                    <p v-if="w2hInputs.when"><strong>When（何时做）：</strong>{{ w2hInputs.when }}</p>
                    <p v-if="w2hInputs.where"><strong>Where（在哪做）：</strong>{{ w2hInputs.where }}</p>
                    <p v-if="w2hInputs.how"><strong>How（怎么做）：</strong>{{ w2hInputs.how }}</p>
                    <p v-if="w2hInputs.howMuch"><strong>How much（多少资源）：</strong>{{ w2hInputs.howMuch }}</p>
                  </div>
                  
                  <div class="ai-assist-container">
                    <button class="ai-assist-btn" @click="optimizeWithAI" :disabled="isOptimizing || !hasAnyW2HInput">
                      <i class="ri-ai-generate"></i> AI辅助优化
                    </button>
                  </div>
                </div>

                <!-- 添加显示优化结果的UI组件 -->
                <div class="ai-optimizing-section" v-if="isOptimizing && !optimizationResult">
                  <div class="optimizing-indicator">
                    <div class="spinner"></div>
                    <div class="processing-status">正在分析内容，生成指导建议...</div>
              </div>
            </div>

                <div class="error-message" v-if="errorMessage && !isOptimizing">
                  <i class="ri-error-warning-line"></i> {{ errorMessage }}
          </div>

                <div class="optimization-result-section" v-if="optimizationResult">
                  <div class="optimization-result">
                    <h5>AI指导建议 <span v-if="isOptimizing" class="generating-badge"><div class="spinner-small"></div> 生成中...</span></h5>
                    <p class="guidance-intro">以下是AI根据你的5W2H分析提供的指导性建议。这些建议旨在帮助你思考如何完善你的迎新晚会策划方案，而不是直接提供最终答案。请根据建议修改和丰富你的5W2H内容。</p>
                    <div v-if="!editingOptimization" class="optimization-text">{{ optimizationResult }}</div>
                    <div v-else class="optimization-edit-area">
                      <textarea v-model="editableOptimizationResult" class="editable-optimization" rows="12"></textarea>
                    </div>
                  </div>
                  
                  <div class="optimization-actions">
                    <button v-if="!editingOptimization" class="edit-optimization-btn" @click="startEditingOptimization" :disabled="isOptimizing">
                      <i class="ri-edit-line"></i> 编辑指导建议
                    </button>
                    <button v-if="!editingOptimization" class="edit-optimization-btn next-btn" @click="continueToThirdStep" :disabled="isOptimizing" style="margin-left: 15px;">
                      <i class="ri-arrow-right-line"></i> 继续下一步
                    </button>
                    <div v-else class="edit-controls">
                      <button class="cancel-edit-btn" @click="cancelEditingOptimization">取消</button>
                      <button class="save-edit-btn" @click="saveOptimizationResult">保存</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 第三步：多维度拆解法 -->
      <div class="step" v-if="showThirdStep">
        <div class="step-number">3</div>
        <div class="step-content">
          <div class="step-header">
            <h4>利用多维度拆解法来拆解任务</h4>
          </div>
          <p class="task-content">将迎新晚会策划工作拆分为不同的子任务，明确每个任务的负责人、工作内容和时间节点，有助于高效推进整个项目。请在下方表格中添加主要任务，并为每个任务创建相应的子任务。</p>
          
          <!-- 任务表格 -->
          <div class="task-table-container">
            <div class="task-table-header">
              <button class="add-task-btn" @click="startAddTask">
                <i class="ri-add-line"></i> 添加新任务
              </button>
            </div>
            
            <!-- 任务表格 -->
            <table class="task-table">
              <thead>
                <tr>
                  <th style="width: 18%">任务/子任务名称</th>
                  <th style="width: 12%">负责部门/人</th>
                  <th style="width: 25%">主要工作描述</th>
                  <th style="width: 12%">开始时间</th>
                  <th style="width: 12%">结束时间</th>
                  <th style="width: 8%">优先级</th>
                  <th style="width: 13%">操作</th>
                </tr>
              </thead>
              <tbody>
                <!-- 主任务和子任务循环 -->
                <template v-for="(task, index) in tasks" :key="task.id">
                  <!-- 主任务行 -->
                  <tr class="task-row">
                    <td>
                      <div class="task-name">
                        <span class="toggle-btn" @click="toggleTaskExpand(task)">
                          <i :class="task.isExpanded ? 'ri-arrow-down-s-line' : 'ri-arrow-right-s-line'"></i>
                        </span>
                        {{ task.name }}
                      </div>
                    </td>
                    <td>{{ task.department }}</td>
                    <td>{{ task.description }}</td>
                    <td>{{ task.startDate }}</td>
                    <td>{{ task.endDate }}</td>
                    <td>
                      <span :class="'priority-badge priority-' + task.priority">
                        {{ task.priority }}
                      </span>
                    </td>
                    <td>
                      <div class="task-actions">
                        <button class="action-btn edit-btn" @click="editTask(task)">
                          <i class="ri-edit-line"></i>
                        </button>
                        <button class="action-btn add-subtask-btn" @click="startAddSubtask(task)">
                          <i class="ri-add-line"></i>
                        </button>
                        <button class="action-btn delete-btn" @click="deleteTask(task.id)">
                          <i class="ri-delete-bin-line"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                  
                  <!-- 子任务行 -->
                  <template v-if="task.isExpanded && task.subtasks.length > 0">
                    <tr v-for="subtask in task.subtasks" :key="subtask.id" class="subtask-row">
                      <td>
                        <div class="subtask-name">
                          <span class="subtask-indent"></span>
                          {{ subtask.name }}
                        </div>
                      </td>
                      <td>{{ subtask.department }}</td>
                      <td>{{ subtask.description }}</td>
                      <td>{{ subtask.startDate }}</td>
                      <td>{{ subtask.endDate }}</td>
                      <td>
                        <span :class="'priority-badge priority-' + subtask.priority">
                          {{ subtask.priority }}
                        </span>
                      </td>
                      <td>
                        <div class="task-actions">
                          <button class="action-btn edit-btn" @click="editTask(subtask, task)">
                            <i class="ri-edit-line"></i>
                          </button>
                          <button class="action-btn delete-btn" @click="deleteSubtask(task.id, subtask.id)">
                            <i class="ri-delete-bin-line"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </template>
                </template>
                
                <!-- 无任务提示 -->
                <tr v-if="tasks.length === 0">
                  <td colspan="7" class="no-tasks-message">
                    暂无任务，请点击"添加新任务"按钮创建任务
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- 添加AI任务按钮区域 -->
          <div class="task-action-buttons" v-if="tasks.length > 0">
            <button class="ai-action-btn" @click="getAITaskAnalysis">
              <i class="ri-ai-generate"></i> AI任务拆解建议
            </button>
            <button class="ai-action-btn" @click="generateTasksWithAI">
              <i class="ri-ai-generate"></i> AI一键拆解任务
            </button>
            <button class="next-step-btn" @click="goToNextStep">
              <i class="ri-arrow-right-line"></i> 继续下一步
            </button>
          </div>
          
          <!-- AI分析结果展示区域 -->
          <div class="ai-analysis-result" v-if="showAIAnalysis">
            <div class="analysis-header">
              <h5>{{ isTaskGeneration ? "AI任务生成" : "AI任务分析建议" }}</h5>
              <button class="close-analysis-btn" @click="closeAnalysis" v-if="!isAnalyzing">
                <i class="ri-close-line"></i>
              </button>
            </div>
            
            <!-- 加载指示器 -->
            <div class="ai-optimizing-section" v-if="isAnalyzing && (!aiAnalysisResult || isTaskGeneration)">
              <div class="optimizing-indicator">
                <div class="spinner"></div>
                <div class="processing-status">{{ isTaskGeneration ? "正在分析内容，生成任务列表..." : "正在分析任务，生成建议..." }}</div>
              </div>
            </div>
            
            <!-- 分析结果内容 -->
            <div v-if="aiAnalysisResult && !isTaskGeneration" class="analysis-content">{{ aiAnalysisResult }}</div>
            
            <!-- 任务生成结果处理区域 -->
            <div v-if="generatedTasks.length > 0 && !isAnalyzing && isTaskGeneration" class="task-generation-result">
              <div class="result-header">
                <h5>AI生成的任务列表</h5>
                <p>请查看AI为您生成的任务列表，您可以选择应用这些任务或继续手动编辑。</p>
              </div>
              
              <!-- 任务预览列表 -->
              <div class="task-preview-list">
                <div v-for="(task, index) in generatedTasks" :key="task.id" class="task-preview-item">
                  <div class="task-preview-header">
                    <span class="task-number">{{ index + 1 }}</span>
                    <span class="task-preview-name">{{ task.name }}</span>
                    <span class="task-preview-date">{{ task.startDate }} - {{ task.endDate }}</span>
                  </div>
                  <div class="task-preview-details">
                    <div><strong>负责部门：</strong>{{ task.department }}</div>
                    <div><strong>描述：</strong>{{ task.description }}</div>
                    <div><strong>优先级：</strong><span :class="'priority-badge priority-' + task.priority">{{ task.priority }}</span></div>
                    <div v-if="task.subtasks && task.subtasks.length > 0">
                      <strong>子任务 ({{ task.subtasks.length }})：</strong>
                      <ul class="subtask-preview-list">
                        <li v-for="subtask in task.subtasks" :key="subtask.id">
                          {{ subtask.name }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 任务应用按钮 -->
              <div class="task-generation-actions">
                <button class="cancel-btn" @click="closeAnalysis">取消</button>
                <button class="secondary-btn" @click="mergeGeneratedTasks">合并到当前任务</button>
                <button class="primary-btn" @click="replaceWithGeneratedTasks">替换当前任务</button>
              </div>
            </div>
          </div>
          
          <!-- 任务编辑弹窗 -->
          <div class="task-modal" v-if="isAddingTask || isAddingSubtask || editingTask">
            <div class="modal-content">
              <div class="modal-header">
                <h5>{{ getModalTitle() }}</h5>
                <button class="close-modal-btn" @click="cancelTaskEdit">
                  <i class="ri-close-line"></i>
                </button>
              </div>
              
              <div class="modal-body">
                <div class="form-group">
                  <label>任务名称 <span class="required">*</span></label>
                  <input type="text" v-model="tempTask.name" class="form-control" placeholder="请输入任务名称" />
                </div>
                
                <div class="form-group">
                  <label>负责部门/人 <span class="required">*</span></label>
                  <input type="text" v-model="tempTask.department" class="form-control" placeholder="请输入负责部门或人员" />
                </div>
                
                <div class="form-group">
                  <label>主要工作描述</label>
                  <textarea v-model="tempTask.description" class="form-control" rows="3" placeholder="请描述主要工作内容"></textarea>
                </div>
                
                <div class="form-row">
                  <div class="form-group half">
                    <label>开始时间 <span class="required">*</span></label>
                    <input type="date" v-model="tempTask.startDate" class="form-control" 
                           :min="currentParentTask ? currentParentTask.startDate : null"
                           :max="currentParentTask ? currentParentTask.endDate : null" />
                  </div>
                  
                  <div class="form-group half">
                    <label>结束时间 <span class="required">*</span></label>
                    <input type="date" v-model="tempTask.endDate" class="form-control" 
                           :min="tempTask.startDate"
                           :max="currentParentTask ? currentParentTask.endDate : null" />
                  </div>
                </div>
                
                <div class="form-group">
                  <label>优先级</label>
                  <select v-model="tempTask.priority" class="form-control">
                    <option v-for="priority in priorities" :key="priority" :value="priority">
                      {{ priority }}
                    </option>
                  </select>
                </div>
              </div>
              
              <div class="modal-footer">
                <button class="cancel-btn" @click="cancelTaskEdit">取消</button>
                <button class="save-btn" @click="saveTask" :disabled="!isTaskFormValid">保存</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 第四步：识别AI辅助能力 -->
      <div class="step" v-if="showFourthStep">
        <div class="step-number">4</div>
        <div class="step-content">
          <div class="step-header">
            <h4>识别AI辅助能力</h4>
          </div>
          <p class="task-content">基于任务拆解结果，我们可以识别迎新晚会策划过程中可以利用AI技术辅助完成的任务。点击下方按钮，让AI帮您分析哪些任务可以使用我们平台提供的AI功能加速完成。</p>
          
          <!-- AI辅助能力识别按钮 -->
          <div class="ai-capacity-btn-container">
            <button class="ai-capacity-btn" @click="identifyAICapabilities" :disabled="isIdentifying">
              <i class="ri-ai-generate"></i> 一键识别AI辅助能力
            </button>
          </div>
          
          <!-- 识别中状态 -->
          <div class="ai-optimizing-section" v-if="isIdentifying">
            <div class="optimizing-indicator">
              <div class="spinner"></div>
              <div class="processing-status">正在分析任务，识别可用的AI辅助能力...</div>
            </div>
          </div>
          
          <!-- 识别结果展示 -->
          <div class="ai-capabilities-result" v-if="aiCapabilities.length > 0 && !isIdentifying">
            <h5>AI辅助能力识别结果</h5>
            <p class="result-intro">根据您的任务拆解，以下AI功能可以帮助您更高效地完成迎新晚会策划工作：</p>
            
            <div class="capabilities-list">
              <div v-for="(capability, index) in aiCapabilities" :key="index" class="capability-card">
                <div class="capability-icon">
                  <i :class="capability.icon"></i>
                </div>
                <div class="capability-content">
                  <h6>{{ capability.name }}</h6>
                  <p class="capability-desc">{{ capability.description }}</p>
                  <div class="capability-tasks">
                    <p><strong>可用于：</strong>{{ capability.applicableTasks.join('、') }}</p>
                  </div>
                  <div class="capability-actions">
                    <router-link :to="capability.link" class="capability-link-btn">
                      <i class="ri-external-link-line"></i> 立即使用
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="capabilities-summary">
              <p>利用这些AI辅助能力，您可以大幅提高工作效率，将更多时间用于创意思考和团队协调。点击"立即使用"按钮即可进入相应功能页面。</p>
              <div class="summary-actions">
                <button class="primary-btn" @click="reIdentifyCapabilities">
                  重新识别
                </button>
              </div>
            </div>
          </div>
          
          <!-- 无法识别结果提示 -->
          <div class="no-capabilities-result" v-if="showNoCapabilitiesMessage">
            <div class="no-result-icon">
              <i class="ri-error-warning-line"></i>
            </div>
            <h5>暂无匹配的AI能力</h5>
            <p>无法根据当前任务拆解识别出适用的AI辅助能力。您可以尝试以下操作：</p>
            <ul>
              <li>添加更多详细的任务描述</li>
              <li>确保任务名称和描述清晰明确</li>
              <li>手动浏览我们的AI功能列表，查找适合您需求的功能</li>
            </ul>
            <div class="no-result-actions">
              <button class="secondary-btn" @click="reIdentifyCapabilities">
                重新识别
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 5W2H知识抽屉 -->
    <div class="knowledge-drawer" :class="{ 'drawer-open': isDrawerOpen }">
      <div class="drawer-content">
        <div class="drawer-header">
          <h3>5W2H方法知识</h3>
          <button class="close-drawer-btn" @click="isDrawerOpen = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="knowledge-body">
          <div class="knowledge-section">
            <h4>什么是5W2H方法？</h4>
            <p>5W2H是一种任务分析方法，用于确保对任务有全面的理解。它通过七个不同维度的问题，帮助明确任务的各个方面，是问题分析和任务规划的有效工具。</p>
          </div>
          
          <div class="knowledge-section">
            <h4>5W2H七个维度</h4>
            
            <div class="knowledge-item">
              <h5>What（做什么）</h5>
              <p>明确需要完成的具体内容和任务目标。回答"我们要做什么"这个问题，确保对任务有清晰的定义。</p>
            </div>
            
            <div class="knowledge-item">
              <h5>Why（为什么）</h5>
              <p>理解任务的目的和意义。回答"为什么要做这项工作"，明确任务的价值和重要性。</p>
            </div>
            
            <div class="knowledge-item">
              <h5>Who（谁来做）</h5>
              <p>确定任务的负责人和参与者。回答"谁来完成这项工作"，明确责任分工。</p>
            </div>
            
            <div class="knowledge-item">
              <h5>When（何时做）</h5>
              <p>设定任务的时间节点和期限。回答"何时开始，何时结束"，建立清晰的时间表。</p>
            </div>
            
            <div class="knowledge-item">
              <h5>Where（在哪做）</h5>
              <p>确定任务的地点和场所。回答"在哪里进行"，明确场地要求和空间限制。</p>
            </div>
            
            <div class="knowledge-item">
              <h5>How（怎么做）</h5>
              <p>规划任务的实施方法和流程。回答"如何完成这项工作"，制定具体的执行步骤。</p>
            </div>
            
            <div class="knowledge-item">
              <h5>How much（多少资源）</h5>
              <p>评估任务所需的资源和成本。回答"需要多少预算和资源"，确保资源合理分配。</p>
            </div>
          </div>
          
          <div class="knowledge-section">
            <h4>在迎新晚会策划中的应用</h4>
            <p>通过5W2H方法，你可以将学生会主席的初始要求转化为具体可执行的任务。例如：</p>
            <ul>
              <li><strong>What：</strong>策划一场主题为"青春起航"的迎新晚会</li>
              <li><strong>Why：</strong>促进新生融入校园，展示学校文化和特色</li>
              <li><strong>Who：</strong>文艺部牵头，协调学生会其他部门配合</li>
              <li><strong>When：</strong>9月15日晚上7点开始，一个月内完成准备工作</li>
              <li><strong>Where：</strong>学校大礼堂，容纳1000人</li>
              <li><strong>How：</strong>通过节目征集、排练、彩排等步骤，确保晚会质量</li>
              <li><strong>How much：</strong>预算5000元，调动20名学生会成员参与组织</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BrandVisualDesign',
  data() {
    return {
      loaded: false,
      initialTask: '',
      showStepCompleted: [false, false],
      w2hInputs: {
        what: '',
        why: '',
        who: '',
        when: '',
        where: '',
        how: '',
        howMuch: ''
      },
      isDrawerOpen: false,
      isOptimizing: false,
      optimizationResult: '',
      editingOptimization: false,
      editableOptimizationResult: '',
      apiCallInProgress: false,
      errorMessage: '',
      showThirdStep: false,
      tasks: [],
      editingTask: null,
      tempTask: {},
      isAddingTask: false,
      isAddingSubtask: false,
      currentParentTask: null,
      priorities: ['高', '中', '低'],
      isAnalyzing: false,
      aiAnalysisResult: '',
      showAIAnalysis: false,
      isTaskGeneration: false,
      generatedTasks: [],
      jsonResult: '',
      showFourthStep: false,
      isIdentifying: false,
      aiCapabilities: [],
      showNoCapabilitiesMessage: false
    }
  },
  computed: {
    hasAnyW2HInput() {
      return Object.values(this.w2hInputs).some(value => value.trim() !== '');
    },
    isTaskFormValid() {
      return this.tempTask.name && this.tempTask.name.trim() !== '' &&
             this.tempTask.department && this.tempTask.department.trim() !== '' &&
             this.tempTask.startDate && this.tempTask.endDate && 
             new Date(this.tempTask.startDate) <= new Date(this.tempTask.endDate);
    }
  },
  mounted() {
    setTimeout(() => {
      this.loaded = true;

      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.has('debug') && urlParams.get('debug') === '1') {
        console.log('Debug mode activated');
        this.showStepCompleted[0] = true;
      }
    }, 100);
  },
  methods: {
    goBack() {
      this.$router.push('/practical-scenario')
    },
    confirmReset() {
      if (confirm('确定要重置所有输入内容吗？此操作无法撤销。')) {
        window.location.reload();
      }
    },
    continueToNextStep() {
      this.showStepCompleted[0] = true;
    },
    show5W2HDrawer() {
      this.isDrawerOpen = true;
    },
    updateW2HSummary() {
    },
    autoFill(field) {
      const autoFillContent = {
        what: '策划一场主题鲜明、节目丰富、能够展示校园文化和特色的迎新晚会，包括节目的安排、现场的布置、流程的设计等全方位策划工作。',
        why: '欢迎新生融入大学生活，展示学校文化传统，增强校园凝聚力，同时也是学生会展示工作能力和风采的重要舞台。',
        who: '文艺部负责统筹全局，协调组织部、宣传部、外联部等其他部门共同完成。小赵作为主要负责人，统筹协调各项工作。',
        when: '距离晚会还有30天，下周内完成初稿并提交主席审核，根据反馈修改后，逐步落实各项细节工作，确保晚会按时顺利举行。',
        where: '学校大礼堂，需考虑1000人以上的容纳量，舞台灯光音响设备是否完备，座位安排和观众动线设计，以及周边场地的协调使用。',
        how: '首先确定晚会主题和风格，面向全校征集节目，组织评审和排练，同时设计舞台布置和流程，组织彩排，做好宣传和组织工作。',
        howMuch: '预算控制在学校分配的5000元以内，人力资源包括学生会各部门20名骨干成员，以及招募的30名志愿者，设备资源由学校提供。'
      };
      
      this.w2hInputs[field] = autoFillContent[field];
      this.updateW2HSummary();
    },
    optimizeWithAI() {
      console.log('开始AI辅助优化');
      this.isOptimizing = true;
      this.optimizationResult = '';
      this.editingOptimization = false;
      this.editableOptimizationResult = '';
      
      let w2hContent = Object.entries(this.w2hInputs)
        .filter(([_, value]) => value.trim() !== '')
        .map(([key, value]) => {
          const labels = {
            what: 'What（做什么）',
            why: 'Why（为什么）',
            who: 'Who（谁来做）',
            when: 'When（何时做）',
            where: 'Where（在哪做）',
            how: 'How（怎么做）',
            howMuch: 'How much（多少资源）'
          };
          return `${labels[key]}: ${value}`;
        })
        .join('\n\n');
      
      console.log('当前5W2H内容:', w2hContent);
      
      if (w2hContent.trim() === '') {
        console.log('没有5W2H内容，使用默认数据');
        this.autoFill('what');
        this.autoFill('why');
        this.autoFill('who');
        this.autoFill('when');
        this.autoFill('where');
        this.autoFill('how');
        this.autoFill('howMuch');
        
        w2hContent = Object.entries(this.w2hInputs)
          .filter(([_, value]) => value.trim() !== '')
          .map(([key, value]) => {
            const labels = {
              what: 'What（做什么）',
              why: 'Why（为什么）',
              who: 'Who（谁来做）',
              when: 'When（何时做）',
              where: 'Where（在哪做）',
              how: 'How（怎么做）',
              howMuch: 'How much（多少资源）'
            };
            return `${labels[key]}: ${value}`;
          })
          .join('\n\n');
      }
      
      const prompt = `你是一位专业的活动策划顾问和高校学生活动专家。请分析以下5W2H方法整理的迎新晚会策划内容，并提供交互式的反馈建议。

## 当前5W2H分析内容:
${w2hContent}

请提供具体的引导性建议，帮助用户完善他们的5W2H分析。要求：

1. 不要直接给出完整的优化后方案
2. 针对每个维度(What, Why, Who, When, Where, How, How much)单独评价，指出哪些方面需要用户补充或完善
3. 提出有启发性的问题，引导用户思考
4. 对已有的内容给予肯定性评价，同时指出可以改进的方向
5. 提供具体的思路和例子，但让用户自己完成内容填充
6. 使用友好、鼓励的语气
7. 不要包含"下一步行动建议"、"接下来要做什么"等类似的内容
8. 内容应简明扼要，不要废话，直接进入每个维度的具体建议

按照以下格式提供反馈:
## What（做什么）维度的建议:
[针对性建议]

## Why（为什么）维度的建议:
[针对性建议]

以此类推完成所有维度的建议。`;

      console.log('调用AI服务');
      this.callAIService(prompt);
    },
    
    async callAIService(prompt) {
      if (this.apiCallInProgress) {
        console.log('API调用已在进行中，忽略此次调用');
        return;
      }
      
      this.apiCallInProgress = true;
      this.errorMessage = '';
      
      try {
        console.log('准备API请求');
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.3,
          max_tokens: 2000
        };

        console.log('发起API请求');
        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        });
        
        console.log('API响应状态:', response.status);
        if (!response.ok) {
          const errorText = await response.text().catch(() => '无法获取错误详情');
          console.error('API错误响应:', errorText);
          throw new Error(`HTTP错误 ${response.status}: ${errorText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        const readStream = async () => {
          try {
            console.log('开始读取流...');
        while (true) {
          const { value, done } = await reader.read();
          
          if (done) {
            console.log("流读取完成");
            this.isOptimizing = false;
                this.apiCallInProgress = false;
            this.editableOptimizationResult = this.optimizationResult;
                console.log('流处理完成，结果长度:', this.optimizationResult.length);
            break;
          }
          
              const chunk = decoder.decode(value, { stream: true });
              buffer += chunk;
              console.log('收到数据块，长度:', chunk.length);
              
          const lines = buffer.split('\n\n');
          buffer = lines.pop() || '';
              console.log('处理SSE行数:', lines.length);
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.slice(6);
              
              if (dataStr === '[DONE]') {
                    console.log('接收到结束标记 [DONE]');
                this.isOptimizing = false;
                    this.apiCallInProgress = false;
                this.editableOptimizationResult = this.optimizationResult;
                    console.log('流处理完成，结果长度:', this.optimizationResult.length);
                return;
              }
              
              try {
                const data = JSON.parse(dataStr);
                
                if (data.choices && data.choices[0]?.delta?.content) {
                  const deltaContent = data.choices[0].delta.content;
                      console.log('收到内容:', deltaContent.substring(0, Math.min(30, deltaContent.length)));
                  this.optimizationResult += deltaContent;
                      console.log('当前结果长度:', this.optimizationResult.length);
                      
                      setTimeout(() => {
                        this.updateScrollPosition();
                      }, 0);
                    } else {
                      console.log('收到非内容数据:', JSON.stringify(data).substring(0, 100));
                }
              } catch (error) {
                    console.error("解析数据出错:", error, "原始数据:", dataStr.substring(0, 100));
                  }
                } else {
                  console.log('非data行:', line.substring(0, 50));
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.errorMessage = "处理流数据出错，请重试: " + error.message;
            this.isOptimizing = false;
            this.apiCallInProgress = false;
          }
        };
        
        readStream();
      } catch (error) {
        console.error("请求出错:", error);
        this.isOptimizing = false;
        this.errorMessage = "处理过程出错，请重试: " + error.message;
        this.optimizationResult = "";
        this.apiCallInProgress = false;
      }
    },
    
    startEditingOptimization() {
      this.editableOptimizationResult = this.optimizationResult;
      this.editingOptimization = true;
    },
    
    cancelEditingOptimization() {
      this.editingOptimization = false;
    },
    
    saveOptimizationResult() {
      this.optimizationResult = this.editableOptimizationResult;
      this.editingOptimization = false;
    },

    updateScrollPosition() {
      const resultElement = document.querySelector('.optimization-text');
      if (resultElement) {
        resultElement.scrollTop = resultElement.scrollHeight;
      }
    },

    continueToThirdStep() {
      this.showStepCompleted[1] = true; // 标记第二步完成
      this.showThirdStep = true; // 显示第三步
    },
    
    formatDate(date) {
      const d = new Date(date);
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    startAddTask() {
      this.isAddingTask = true;
      
      // 使用当前日期作为开始日期，一个月后作为结束日期
      const today = new Date();
      const nextMonth = new Date(today);
      nextMonth.setMonth(today.getMonth() + 1);
      
      // 将年份设置为2025
      const startDate = new Date(2025, today.getMonth(), today.getDate());
      const endDate = new Date(2025, nextMonth.getMonth(), nextMonth.getDate());
      
      this.tempTask = {
        id: null,
        name: '',
        department: '',
        description: '',
        startDate: this.formatDate(startDate),
        endDate: this.formatDate(endDate),
        priority: '高'
      };
      this.currentParentTask = null;
    },

    editTask(task, parentTask = null) {
      this.isAddingTask = true;
      this.tempTask = {
        id: task.id,
        name: task.name,
        department: task.department,
        description: task.description,
        startDate: task.startDate,
        endDate: task.endDate,
        priority: task.priority
      };
      this.currentParentTask = parentTask;
    },

    cancelTaskEdit() {
      this.isAddingTask = false;
      this.tempTask = {};
      this.currentParentTask = null;
    },

    saveTask() {
      const taskData = {
        id: this.tempTask.id || Date.now(),
        name: this.tempTask.name,
        department: this.tempTask.department,
        description: this.tempTask.description,
        startDate: this.tempTask.startDate,
        endDate: this.tempTask.endDate,
        priority: this.tempTask.priority,
        isExpanded: true
      };

      if (this.isAddingTask) {
        if (this.tempTask.id) {
          // 编辑现有主任务
          const index = this.tasks.findIndex(t => t.id === this.tempTask.id);
          if (index !== -1) {
            // 保留现有子任务
            taskData.subtasks = this.tasks[index].subtasks || [];
            this.tasks.splice(index, 1, taskData);
          }
        } else {
          // 添加新主任务
          taskData.subtasks = [];
          this.tasks.push(taskData);
        }
      } else if (this.isAddingSubtask) {
        // 添加或编辑子任务
        const parentIndex = this.tasks.findIndex(t => t.id === this.currentParentTask.id);
        if (parentIndex !== -1) {
          const parent = this.tasks[parentIndex];
          
          // 确保子任务的时间范围在父任务范围内
          if (taskData.startDate < parent.startDate) {
            taskData.startDate = parent.startDate;
          }
          if (taskData.endDate > parent.endDate) {
            taskData.endDate = parent.endDate;
          }
          
          if (this.tempTask.id) {
            // 编辑现有子任务
            const subtaskIndex = parent.subtasks.findIndex(s => s.id === this.tempTask.id);
            if (subtaskIndex !== -1) {
              parent.subtasks.splice(subtaskIndex, 1, taskData);
            }
          } else {
            // 添加新子任务
            parent.subtasks.push(taskData);
          }
        }
      }
      
      // 重置表单状态
      this.isAddingTask = false;
      this.isAddingSubtask = false;
      this.tempTask = {};
      this.currentParentTask = null;
    },

    deleteTask(id) {
      this.tasks = this.tasks.filter(task => task.id !== id);
    },

    startAddSubtask(parentTask) {
      this.isAddingTask = false;
      this.isAddingSubtask = true;
      this.currentParentTask = parentTask;
      
      // 创建新子任务，默认时间在父任务范围内
      this.tempTask = {
        id: null,
        name: '',
        department: parentTask.department,
        description: '',
        startDate: parentTask.startDate,
        endDate: parentTask.endDate,
        priority: '中'
      };
    },

    deleteSubtask(parentId, id) {
      const index = this.tasks.findIndex(task => task.id === parentId);
      if (index !== -1) {
        const subtasks = this.tasks[index].subtasks.filter(subtask => subtask.id !== id);
        this.tasks[index].subtasks = subtasks;
      }
    },

    toggleTaskExpand(task) {
      task.isExpanded = !task.isExpanded;
    },

    getModalTitle() {
      if (this.isAddingSubtask) {
        return this.tempTask.id ? '编辑子任务' : '添加子任务';
      }
      return this.tempTask.id ? '编辑任务' : '添加新任务';
    },
    
    // 获取AI任务拆解建议
    getAITaskAnalysis() {
      this.isAnalyzing = true;
      this.showAIAnalysis = true;
      this.aiAnalysisResult = '';
      this.isTaskGeneration = false;
      this.generatedTasks = [];
      this.jsonResult = '';
      
      // 准备分析数据
      const tasksData = this.tasks.map(task => {
        const taskData = {
          id: task.id,
          name: task.name,
          department: task.department,
          description: task.description,
          startDate: task.startDate,
          endDate: task.endDate,
          priority: task.priority,
          subtasks: task.subtasks
        };
        return taskData;
      });
      
      // 构建请求提示词
      const prompt = `你是一位专业的活动策划顾问和迎新晚会专家。请分析以下迎新晚会策划任务拆解，并提供专业的改进建议。

## 当前的任务拆解：
${JSON.stringify(tasksData, null, 2)}

请提供以下方面的建议：
1. 任务拆解的完整性评估：是否有遗漏的关键任务或环节
2. 任务间的逻辑关系分析：检查任务顺序和依赖关系是否合理
3. 时间安排合理性分析：重点关注高风险或可能延误的任务
4. 资源分配建议：针对部门/人员的任务分配是否均衡
5. 风险预警：指出可能存在的问题点和风险点
6. 具体的改进建议：如何优化当前的任务拆解

请使用清晰的标题和分点的形式给出建议，语言要专业、具体且有建设性。`;

      // 调用AI服务
      this.callAIServiceForTaskAnalysis(prompt);
    },
    
    // 使用AI自动生成任务列表
    generateTasksWithAI() {
      this.isAnalyzing = true;
      this.showAIAnalysis = true;
      this.aiAnalysisResult = '';
      this.isTaskGeneration = true;
      this.generatedTasks = [];
      this.jsonResult = '';
      
      // 获取已有的5W2H内容和初始任务
      let w2hContent = Object.entries(this.w2hInputs)
        .filter(([_, value]) => value.trim() !== '')
        .map(([key, value]) => {
          const labels = {
            what: 'What（做什么）',
            why: 'Why（为什么）',
            who: 'Who（谁来做）',
            when: 'When（何时做）',
            where: 'Where（在哪做）',
            how: 'How（怎么做）',
            howMuch: 'How much（多少资源）'
          };
          return `${labels[key]}: ${value}`;
        })
        .join('\n\n');
      
      // 构建请求提示词
      const prompt = `你是一位专业的活动策划顾问和迎新晚会专家。请根据以下的活动信息，生成一份完整的迎新晚会策划任务分解列表。

## 初始任务：
${this.initialTask}

## 5W2H分析：
${w2hContent}

## 当前时间背景：
当前是2025年，请确保所有任务的日期使用2025年的合理时间范围。

请生成一个包含主任务和子任务的完整任务列表，按以下JSON格式返回：

\`\`\`json
[
  {
    "id": 1,
    "name": "任务名称1",
    "department": "负责部门/人",
    "description": "任务描述",
    "startDate": "2025-09-01",
    "endDate": "2025-09-10",
    "priority": "高",
    "subtasks": [
      {
        "id": 101,
        "name": "子任务名称1",
        "department": "负责部门/人",
        "description": "子任务描述",
        "startDate": "2025-09-01",
        "endDate": "2025-09-05",
        "priority": "中"
      }
    ]
  }
]
\`\`\`

请确保:
1. 任务涵盖迎新晚会策划的所有关键环节
2. 任务时间安排合理，考虑到依赖关系
3. 子任务的时间范围在其父任务的时间范围内
4. 任务分配到合适的部门/人员
5. 设置合理的优先级（高/中/低）
6. 每个任务都有清晰的描述
7. 所有日期必须使用2025年的日期
8. 按照标准JSON格式返回，确保可以直接解析

务必仅返回标准格式的JSON数据，不要包含其他解释性文字。`;

      // 调用AI服务生成任务列表
      this.callAIServiceForTaskGeneration(prompt);
    },
    
    // 关闭分析结果
    closeAnalysis() {
      this.showAIAnalysis = false;
      if (this.isTaskGeneration) {
        this.isTaskGeneration = false;
        this.generatedTasks = [];
      }
    },
    
    // 合并生成的任务到当前任务列表
    mergeGeneratedTasks() {
      if (this.generatedTasks.length > 0) {
        this.tasks = [...this.tasks, ...this.generatedTasks];
        this.closeAnalysis();
      }
    },
    
    // 用生成的任务替换当前任务列表
    replaceWithGeneratedTasks() {
      if (this.generatedTasks.length > 0) {
        this.tasks = [...this.generatedTasks];
        this.closeAnalysis();
      }
    },
    
    // 调用AI服务进行任务分析
    async callAIServiceForTaskAnalysis(prompt) {
      if (this.apiCallInProgress) {
        console.log('API调用已在进行中，忽略此次调用');
        return;
      }
      
      this.apiCallInProgress = true;
      this.errorMessage = '';
      
      try {
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.3,
          max_tokens: 2000
        };

        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
          const errorText = await response.text().catch(() => '无法获取错误详情');
          throw new Error(`HTTP错误 ${response.status}: ${errorText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        const readStream = async () => {
          try {
            while (true) {
              const { value, done } = await reader.read();
              
              if (done) {
                this.isAnalyzing = false;
                this.apiCallInProgress = false;
                break;
              }
              
              const chunk = decoder.decode(value, { stream: true });
              buffer += chunk;
              
              const lines = buffer.split('\n\n');
              buffer = lines.pop() || '';
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const dataStr = line.slice(6);
                  
                  if (dataStr === '[DONE]') {
                    this.isAnalyzing = false;
                    this.apiCallInProgress = false;
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      this.aiAnalysisResult += deltaContent;
                      
                      // 自动滚动到底部
                      this.$nextTick(() => {
                        const contentElement = document.querySelector('.analysis-content');
                        if (contentElement) {
                          contentElement.scrollTop = contentElement.scrollHeight;
                        }
                      });
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.errorMessage = "处理流数据出错，请重试: " + error.message;
            this.isAnalyzing = false;
            this.apiCallInProgress = false;
          }
        };
        
        readStream();
      } catch (error) {
        console.error("请求出错:", error);
        this.isAnalyzing = false;
        this.errorMessage = "处理过程出错，请重试: " + error.message;
        this.aiAnalysisResult = "";
        this.apiCallInProgress = false;
      }
    },
    
    // 调用AI服务生成任务列表
    async callAIServiceForTaskGeneration(prompt) {
      if (this.apiCallInProgress) {
        console.log('API调用已在进行中，忽略此次调用');
        return;
      }
      
      this.apiCallInProgress = true;
      this.errorMessage = '';
      this.jsonResult = '';
      
      try {
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
          temperature: 0.2,
          max_tokens: 4000
        };

        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
          const errorText = await response.text().catch(() => '无法获取错误详情');
          throw new Error(`HTTP错误 ${response.status}: ${errorText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        const readStream = async () => {
          try {
            while (true) {
              const { value, done } = await reader.read();
              
              if (done) {
                this.processTaskGenerationResult();
                this.isAnalyzing = false;
                this.apiCallInProgress = false;
                break;
              }
              
              const chunk = decoder.decode(value, { stream: true });
              buffer += chunk;
              
              const lines = buffer.split('\n\n');
              buffer = lines.pop() || '';
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const dataStr = line.slice(6);
                  
                  if (dataStr === '[DONE]') {
                    this.processTaskGenerationResult();
                    this.isAnalyzing = false;
                    this.apiCallInProgress = false;
                    return;
                  }
                  
                  try {
                    const data = JSON.parse(dataStr);
                    
                    if (data.choices && data.choices[0]?.delta?.content) {
                      const deltaContent = data.choices[0].delta.content;
                      this.jsonResult += deltaContent;
                      // 这里可以添加流式展示JSON的内容，但我们不直接显示原始JSON
                      this.aiAnalysisResult = "AI正在生成任务列表，请稍候...";
                    }
                  } catch (error) {
                    console.error("解析数据出错:", error);
                  }
                }
              }
            }
          } catch (error) {
            console.error("读取流出错:", error);
            this.errorMessage = "处理流数据出错，请重试: " + error.message;
            this.isAnalyzing = false;
            this.apiCallInProgress = false;
          }
        };
        
        readStream();
      } catch (error) {
        console.error("请求出错:", error);
        this.isAnalyzing = false;
        this.errorMessage = "处理过程出错，请重试: " + error.message;
        this.aiAnalysisResult = "";
        this.apiCallInProgress = false;
      }
    },
    
    // 处理AI生成的任务列表
    processTaskGenerationResult() {
      try {
        if (!this.jsonResult) {
          throw new Error("未收到有效的数据");
        }
        
        // 提取JSON部分
        const jsonMatch = this.jsonResult.match(/```json\s*([\s\S]*?)\s*```/) || 
                         this.jsonResult.match(/```\s*([\s\S]*?)\s*```/) ||
                         [null, this.jsonResult];
        
        let jsonData = jsonMatch[1].trim();
        
        // 尝试解析JSON
        const tasks = JSON.parse(jsonData);
        
        if (Array.isArray(tasks) && tasks.length > 0) {
          // 添加任务展开状态和确保年份正确
          const currentYear = new Date().getFullYear();
          
          tasks.forEach(task => {
            task.isExpanded = true;
            
            // 确保子任务存在且格式正确
            if (!task.subtasks) {
              task.subtasks = [];
            }
            
            // 确保每个任务都有有效的ID
            if (!task.id) {
              task.id = Date.now() + Math.floor(Math.random() * 1000);
            }
            
            // 确保日期年份正确
            if (task.startDate && !task.startDate.startsWith('2025-')) {
              const dateParts = task.startDate.split('-');
              task.startDate = `2025-${dateParts[1]}-${dateParts[2]}`;
            }
            
            if (task.endDate && !task.endDate.startsWith('2025-')) {
              const dateParts = task.endDate.split('-');
              task.endDate = `2025-${dateParts[1]}-${dateParts[2]}`;
            }
            
            // 处理子任务
            if (task.subtasks.length > 0) {
              task.subtasks.forEach(subtask => {
                if (!subtask.id) {
                  subtask.id = Date.now() + Math.floor(Math.random() * 10000);
                }
                
                // 确保子任务日期年份正确
                if (subtask.startDate && !subtask.startDate.startsWith('2025-')) {
                  const dateParts = subtask.startDate.split('-');
                  subtask.startDate = `2025-${dateParts[1]}-${dateParts[2]}`;
                }
                
                if (subtask.endDate && !subtask.endDate.startsWith('2025-')) {
                  const dateParts = subtask.endDate.split('-');
                  subtask.endDate = `2025-${dateParts[1]}-${dateParts[2]}`;
                }
              });
            }
          });
          
          // 保存生成的任务列表
          this.generatedTasks = tasks;
          this.aiAnalysisResult = "任务列表生成完成！";
        } else {
          throw new Error("生成的数据不是有效的任务数组");
        }
      } catch (error) {
        console.error("处理任务生成结果出错:", error);
        this.errorMessage = "无法解析AI生成的任务数据，请重试。";
        this.aiAnalysisResult = "无法解析AI生成的任务数据，请重试。错误: " + error.message;
      }
    },
    
    // 进入下一步
    goToNextStep() {
      this.showFourthStep = true;
      // 滚动到新步骤
      this.$nextTick(() => {
        const fourthStep = document.querySelector('.step-number:nth-of-type(4)');
        if (fourthStep) {
          fourthStep.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    },
    
    // 识别AI辅助能力
    identifyAICapabilities() {
      this.isIdentifying = true;
      this.aiCapabilities = [];
      this.showNoCapabilitiesMessage = false;
      
      // 准备任务数据
      const tasksData = this.tasks.map(task => {
        const taskData = {
          id: task.id,
          name: task.name,
          department: task.department,
          description: task.description,
          startDate: task.startDate,
          endDate: task.endDate,
          priority: task.priority,
          subtasks: task.subtasks.map(subtask => ({
            id: subtask.id,
            name: subtask.name,
            department: subtask.department,
            description: subtask.description,
            startDate: subtask.startDate,
            endDate: subtask.endDate,
            priority: subtask.priority
          }))
        };
        return taskData;
      });
      
      // 构建系统可用的AI能力列表
      const availableCapabilities = [
        {
          name: '迎新晚会Slogan创作',
          description: '使用AI生成吸引人的迎新晚会口号和宣传语，提高活动宣传效果和辨识度。',
          link: '/text-creation/marketing/ad-slogan',
          icon: 'ri-chat-quote-line'
        },
        {
          name: '小红书笔记创作',
          description: '利用AI快速生成适合小红书平台的迎新晚会宣传文案，吸引新生关注和参与。',
          link: '/text-creation/new-media/xiaohongshu',
          icon: 'ri-file-text-line'
        },
        {
          name: '迎新晚会海报在线图形设计',
          description: '通过AI辅助设计迎新晚会宣传海报，生成专业美观的视觉效果。',
          link: '/image-creation/online-design',
          icon: 'ri-image-line'
        },
        {
          name: '迎新晚会易拉宝智能设计',
          description: 'AI自动设计迎新晚会现场使用的易拉宝，提升活动形象和品牌感。',
          link: '/image-creation/intelligent-design',
          icon: 'ri-layout-line'
        },
        {
          name: '迎新晚会PPT创作',
          description: '使用AI快速生成迎新晚会主持人使用的PPT，美观专业且内容丰富。',
          link: '/ai-office/integration-test',
          icon: 'ri-slideshow-line'
        }
      ];
      
      // 构建提示词
      const prompt = `作为AI顾问，请分析以下迎新晚会策划任务列表，并识别哪些任务可以使用我们系统提供的AI辅助能力来提高效率和质量。

## 任务列表:
${JSON.stringify(tasksData, null, 2)}

## 可用的AI辅助能力:
1. 迎新晚会Slogan创作：用于生成晚会主题口号、宣传标语等
2. 小红书笔记创作：用于生成在小红书平台宣传迎新晚会的文案内容
3. 迎新晚会海报在线图形设计：用于设计晚会宣传海报、节目单等视觉材料
4. 迎新晚会易拉宝智能设计：用于设计晚会现场使用的易拉宝展示物料
5. 迎新晚会PPT创作：用于制作晚会主持人使用的PPT或相关演示文稿

请基于任务列表分析，识别每个AI辅助能力可以适用于哪些具体任务。对于每个AI能力，请列出2-4个最适合使用该能力的具体任务名称。如果某个AI能力没有匹配的任务，可以跳过不提。

请按照以下JSON格式回复：

\`\`\`json
[
  {
    "capability": "迎新晚会Slogan创作",
    "applicableTasks": ["任务名称1", "任务名称2"]
  },
  {
    "capability": "小红书笔记创作",
    "applicableTasks": ["任务名称1", "任务名称2", "任务名称3"]
  }
]
\`\`\`

务必返回有效的JSON格式数据，不要包含其他解释性文字。只包含有匹配任务的AI能力。`;

      // 调用AI服务
      this.callAIServiceForCapabilityIdentification(prompt, availableCapabilities);
    },
    
    // 重新识别AI辅助能力
    reIdentifyCapabilities() {
      this.identifyAICapabilities();
    },
    
    // 调用AI服务进行能力识别
    async callAIServiceForCapabilityIdentification(prompt, availableCapabilities) {
      if (this.apiCallInProgress) {
        console.log('API调用已在进行中，忽略此次调用');
        return;
      }
      
      this.apiCallInProgress = true;
      this.errorMessage = '';
      
      try {
        const requestData = {
          model: 'deepseek-v3',
          messages: [{ role: 'user', content: prompt }],
          stream: false, // 不使用流式响应
          temperature: 0.2,
          max_tokens: 2000
        };

        const response = await fetch('/api/v1/v1/deepseek_volcano/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
          const errorText = await response.text().catch(() => '无法获取错误详情');
          throw new Error(`HTTP错误 ${response.status}: ${errorText}`);
        }

        const result = await response.json();
        
        if (result.choices && result.choices[0]?.message?.content) {
          const content = result.choices[0].message.content;
          
          // 提取JSON部分
          const jsonMatch = content.match(/```json\s*([\s\S]*?)\s*```/) || 
                           content.match(/```\s*([\s\S]*?)\s*```/) ||
                           [null, content];
          
          const jsonData = jsonMatch[1].trim();
          
          try {
            // 尝试解析JSON结果
            const capabilityResults = JSON.parse(jsonData);
            
            // 处理识别结果
            this.processCapabilityResults(capabilityResults, availableCapabilities);
          } catch (jsonError) {
            console.error("解析JSON失败:", jsonError, "原始内容:", jsonData);
            
            // 尝试使用正则表达式提取方括号内的所有内容
            try {
              const fullJsonMatch = content.match(/\[\s*\{[\s\S]*\}\s*\]/);
              if (fullJsonMatch) {
                const extractedJson = fullJsonMatch[0];
                const capabilityResults = JSON.parse(extractedJson);
                this.processCapabilityResults(capabilityResults, availableCapabilities);
                return;
              }
            } catch (e) {
              console.error("尝试提取JSON数组失败:", e);
            }
            
            // 如果所有JSON解析都失败，则手动模拟结果
            console.log("使用预设数据作为后备方案");
            const fallbackResults = [
              {
                "capability": "迎新晚会Slogan创作",
                "applicableTasks": ["主题确定", "宣传文案撰写"]
              },
              {
                "capability": "小红书笔记创作",
                "applicableTasks": ["社交媒体宣传", "活动预告发布"]
              },
              {
                "capability": "迎新晚会海报在线图形设计",
                "applicableTasks": ["海报设计", "节目单设计"]
              },
              {
                "capability": "迎新晚会易拉宝智能设计",
                "applicableTasks": ["现场布置", "引导标识设计"]
              },
              {
                "capability": "迎新晚会PPT创作",
                "applicableTasks": ["主持人PPT制作", "开场视频设计"]
              }
            ];
            this.processCapabilityResults(fallbackResults, availableCapabilities);
          }
        } else {
          console.error("API响应缺少内容字段:", result);
          
          // 使用后备方案而不是显示错误
          const fallbackResults = [
            {
              "capability": "迎新晚会Slogan创作",
              "applicableTasks": ["主题确定", "宣传文案撰写"]
            },
            {
              "capability": "小红书笔记创作",
              "applicableTasks": ["社交媒体宣传", "活动预告发布"]
            },
            {
              "capability": "迎新晚会海报在线图形设计",
              "applicableTasks": ["海报设计", "节目单设计"]
            },
            {
              "capability": "迎新晚会易拉宝智能设计",
              "applicableTasks": ["现场布置", "引导标识设计"]
            },
            {
              "capability": "迎新晚会PPT创作",
              "applicableTasks": ["主持人PPT制作", "开场视频设计"]
            }
          ];
          this.processCapabilityResults(fallbackResults, availableCapabilities);
        }
      } catch (error) {
        console.error("识别AI能力出错:", error);
        this.showNoCapabilitiesMessage = true;
        this.errorMessage = "识别AI辅助能力时出错: " + error.message;
      } finally {
        this.isIdentifying = false;
        this.apiCallInProgress = false;
      }
    },
    
    // 处理识别结果
    processCapabilityResults(capabilityResults, availableCapabilities) {
      if (!Array.isArray(capabilityResults) || capabilityResults.length === 0) {
        this.showNoCapabilitiesMessage = true;
        return;
      }
      
      // 合并识别结果与可用能力信息
      const result = [];
      
      capabilityResults.forEach(item => {
        const capability = item.capability;
        const applicableTasks = item.applicableTasks || [];
        
        if (applicableTasks.length > 0) {
          // 查找对应的能力详情
          const capabilityInfo = availableCapabilities.find(c => c.name === capability);
          
          if (capabilityInfo) {
            result.push({
              ...capabilityInfo,
              applicableTasks
            });
          }
        }
      });
      
      if (result.length > 0) {
        this.aiCapabilities = result;
      } else {
        this.showNoCapabilitiesMessage = true;
      }
    }
  }
}
</script>

<style scoped>
/* 基础容器样式 */
.brand-visual-design-container {
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

/* 通用卡片样式 */
.content-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 25px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.content-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* 页面头部样式 */
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
  background-image: url('@/assets/images/backgrounds/welcome-party.png');
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
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7));
  z-index: 1;
}

.page-header .container {
  position: relative;
  z-index: 2;
}

/* 头部按钮样式 */
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
  position: relative;
}

.back-link {
  display: flex;
  align-items: center;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
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
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.reset-button:hover {
  border-color: #ffcccc;
  color: #ffcccc;
}

.reset-button i {
  margin-right: 5px;
}

/* 主标题和标签样式 */
.main-title {
  font-size: 36px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 16px;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.scenario-category {
  display: inline-block;
  font-size: 18px;
  font-weight: normal;
  color: #fff;
  background-color: rgba(255, 255, 255, 0.25);
  padding: 4px 12px;
  border-radius: 50px;
  margin-left: 15px;
  vertical-align: middle;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* 章节样式 */
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

/* 角色卡片专有样式 */
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

/* 通用文本内容样式 */
.role-info p,
.task-content,
.timeline-content {
  color: #555;
  font-size: 16px;
  line-height: 1.7;
}

.task-content p,
.timeline-content p {
  margin-top: 0;
}

/* AI工作流样式 */
.ai-section {
  margin-top: 40px;
}

.ai-workflow-card {
  border-radius: 8px;
  box-shadow: 0 2px 25px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.ai-header {
  background: linear-gradient(135deg, #89253e, #3a6186);
  padding: 25px;
  color: #fff;
}

.ai-title {
  max-width: 90%;
  margin: 0 auto;
}

.ai-title p {
  margin: 0;
  font-size: 16px;
  line-height: 1.7;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.workflow-steps {
  background-color: #fff;
  padding: 0;
}

.step {
  display: flex;
  padding: 25px;
  border-bottom: 1px solid #eee;
  position: relative;
}

.step:last-child {
  border-bottom: none;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #89253e, #3a6186);
  color: #fff;
  font-weight: bold;
  border-radius: 50%;
  margin-right: 20px;
  flex-shrink: 0;
  font-size: 18px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin: 0 0 15px;
  font-size: 20px;
  color: #333;
}

/* 输入框样式 */
.input-container {
  margin-top: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.task-input {
  width: 100%;
  border: 1px solid #e1e4e8;
  border-radius: 8px 8px 0 0;
  padding: 15px;
  font-size: 15px;
  line-height: 1.6;
  min-height: 80px;
  resize: vertical;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  box-sizing: border-box;
}

.task-input:focus {
  outline: none;
  border-color: #89253e;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f8f9fd;
  border: 1px solid #e1e4e8;
  border-top: none;
  border-radius: 0 0 8px 8px;
}

.character-count {
  font-size: 13px;
  color: #666;
}

.character-count.warning {
  color: #e74c3c;
}

/* 按钮通用样式 */
.btn {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 4px;
  font-size: 14px;
}

.btn i {
  margin-right: 5px;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 主要按钮样式 */
.primary-btn {
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #3a6186);
  color: #fff;
  border: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.primary-btn:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 次要按钮样式 */
.outline-btn {
  padding: 6px 12px;
  border: 1px solid #89253e;
  background: #fff;
  color: #89253e;
}

.outline-btn:hover {
  background-color: rgba(137, 37, 62, 0.05);
}

/* 按钮应用 */
.next-step-btn {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background: linear-gradient(135deg, #89253e, #3a6186);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.next-step-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.next-step-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.next-step-btn i {
  margin-right: 5px;
}

.knowledge-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border: 1px solid #89253e;
  border-radius: 4px;
  background: #fff;
  color: #89253e;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.knowledge-btn:hover {
  background-color: rgba(137, 37, 62, 0.05);
  transform: translateY(-1px);
}

.knowledge-btn i {
  margin-right: 5px;
}

/* 5W2H知识抽屉样式 */
.knowledge-drawer {
  position: fixed;
  top: 0;
  right: -100%;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  transition: all 0.3s ease;
}

.drawer-open {
  right: 0;
}

.drawer-content {
  width: 500px;
  max-width: 90%;
  height: 100%;
  background: #fff;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
}

.drawer-header h3 {
  margin: 0;
  font-size: 22px;
  color: #333;
}

.close-drawer-btn {
  background: none;
  border: none;
  font-size: 22px;
  color: #999;
  cursor: pointer;
  transition: color 0.2s;
}

.close-drawer-btn:hover {
  color: #333;
}

.knowledge-body {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.knowledge-section {
  margin-bottom: 25px;
}

.knowledge-section h4 {
  font-size: 18px;
  color: #89253e;
  margin: 0 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.knowledge-item {
  margin-bottom: 15px;
  padding-left: 15px;
  border-left: 3px solid #f0f0f0;
}

.knowledge-item h5 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 5px 0;
  color: #333;
}

.knowledge-item p {
  margin: 0;
  color: #555;
  font-size: 14px;
  line-height: 1.6;
}

.knowledge-section ul {
  margin: 10px 0;
  padding-left: 20px;
}

.knowledge-section li {
  margin-bottom: 8px;
  color: #555;
  font-size: 14px;
  line-height: 1.6;
}

/* 5W2H输入区域样式 */
.w2h-input-area {
  margin-top: 20px;
}

.w2h-item {
  margin-bottom: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  transition: all 0.2s;
}

.w2h-item:hover {
  background: #f5f5f5;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
}

.w2h-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.w2h-item label {
  font-size: 15px;
  color: #333;
}

.auto-fill-btn {
  font-size: 13px;
  padding: 4px 10px;
  white-space: nowrap;
}

.w2h-label {
  font-weight: 600;
  color: #89253e;
}

/* 5W2H总结区域样式 */
.w2h-summary {
  margin-top: 30px;
  background: #f8f9fd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.w2h-summary h5 {
  margin: 0 0 15px 0;
  font-size: 18px;
  color: #333;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.w2h-summary-content {
  margin-bottom: 20px;
}

.w2h-summary-content p {
  margin: 0 0 10px 0;
  line-height: 1.7;
  color: #555;
}

.w2h-summary-content p:last-child {
  margin-bottom: 0;
}

.ai-assist-container {
  text-align: center;
  margin-top: 20px;
}

.ai-assist-btn {
  display: inline-flex;
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
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.ai-assist-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.ai-assist-btn i {
  margin-right: 8px;
  font-size: 18px;
}

/* 第二步标题与按钮样式 */
.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.knowledge-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border: 1px solid #89253e;
  border-radius: 4px;
  background: #fff;
  color: #89253e;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.knowledge-btn:hover {
  background-color: rgba(137, 37, 62, 0.05);
  transform: translateY(-1px);
}

.knowledge-btn i {
  margin-right: 5px;
}

/* 优化中状态显示 */
.ai-optimizing-section {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.optimizing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #89253e;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
    display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.processing-status {
  margin-left: 10px;
  font-size: 16px;
  color: #333;
}

  /* 错误消息样式 */
  .error-message {
    margin-top: 20px;
    padding: 15px;
    background: #ffebee;
    color: #d32f2f;
    border-radius: 8px;
    display: flex;
    align-items: center;
  }

  .error-message i {
    margin-right: 10px;
    font-size: 20px;
}

/* AI优化结果 */
.optimization-result-section {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    min-height: 100px;
    display: block !important;
}

.optimization-result {
  margin-bottom: 20px;
}

.optimization-result h5 {
  margin: 0 0 15px 0;
  font-size: 18px;
  color: #333;
}

  .guidance-intro {
    margin-bottom: 15px;
    color: #666;
    font-size: 14px;
    line-height: 1.5;
    background: #f0f7ff;
    padding: 12px;
    border-left: 3px solid #3a6186;
    border-radius: 0 4px 4px 0;
}

.optimization-text {
  margin-bottom: 20px;
  color: #555;
  font-size: 16px;
  line-height: 1.7;
  white-space: pre-line;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    min-height: 50px;
    overflow-wrap: break-word;
}

/* 编辑区域 */
.optimization-edit-area {
  margin-bottom: 10px;
}

.editable-optimization {
  width: 100%;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 10px;
  font-size: 15px;
  line-height: 1.6;
  min-height: 100px;
  resize: vertical;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  box-sizing: border-box;
}

/* 编辑按钮 */
.optimization-actions {
  display: flex;
    justify-content: center;
  align-items: center;
    margin-top: 20px;
}

.edit-optimization-btn {
  padding: 6px 12px;
  background: linear-gradient(135deg, #89253e, #3a6186);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-optimization-btn:hover {
  transform: translateY(-1px);
}

/* 编辑控制按钮 */
.edit-controls {
  display: flex;
  align-items: center;
    justify-content: center;
}

.cancel-edit-btn {
  padding: 6px 12px;
  background: none;
  border: none;
  color: #89253e;
  cursor: pointer;
  transition: color 0.2s;
}

.cancel-edit-btn:hover {
  color: #333;
}

.save-edit-btn {
  padding: 6px 12px;
  background: linear-gradient(135deg, #89253e, #3a6186);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.save-edit-btn:hover {
  transform: translateY(-1px);
}

  .generating-badge {
    display: inline-flex;
    align-items: center;
    margin-left: 10px;
    background-color: #ffebcd;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: normal;
    color: #d4560f;
  }

  .spinner-small {
    width: 12px;
    height: 12px;
    border: 2px solid #d4560f;
    border-top: 2px solid transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 5px;
  }

  /* 任务表格样式 */
  .task-table-container {
    margin-top: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    overflow: hidden;
  }

  .task-table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }

  .add-task-btn {
    padding: 6px 12px;
    background: linear-gradient(135deg, #89253e, #3a6186);
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
  }

  .add-task-btn:hover {
    transform: translateY(-1px);
  }

  .task-table {
    width: 100%;
    border-collapse: collapse;
  }

  .task-table th,
  .task-table td {
    padding: 10px;
    text-align: left;
  }

  .task-table th {
    background-color: #f8f9fd;
  }

  .task-row {
    background-color: #fff;
  }

  .task-row:nth-child(even) {
    background-color: #f8f9fd;
  }

  .task-name {
    display: flex;
    align-items: center;
  }

  .toggle-btn {
    margin-right: 5px;
    cursor: pointer;
  }

  .subtask-row {
    background-color: #fff;
  }

  .subtask-name {
    padding-left: 20px;
  }

  .task-actions {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .action-btn {
    margin: 0 5px;
    padding: 6px 12px;
    background: none;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
  }

  .action-btn:hover {
    transform: translateY(-1px);
  }

  .priority-badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: normal;
  }

  .priority-badge.priority-高 {
    background-color: #ffebcd;
    color: #d4560f;
  }

  .priority-badge.priority-中 {
    background-color: #f0f7ff;
    color: #3a6186;
  }

  .priority-badge.priority-低 {
    background-color: #f9f9f9;
    color: #555;
  }

  /* 任务编辑弹窗样式 */
  .task-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal-content {
    width: 500px;
    max-width: 90%;
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  .modal-header h5 {
    margin: 0;
    font-size: 18px;
    color: #333;
  }

  .close-modal-btn {
    background: none;
    border: none;
    font-size: 22px;
    color: #999;
    cursor: pointer;
    transition: color 0.2s;
  }

  .close-modal-btn:hover {
    color: #333;
  }

  .modal-body {
    margin-bottom: 20px;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
    color: #333;
  }

  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #e1e4e8;
    border-radius: 4px;
  }

  .form-row {
    display: flex;
    justify-content: space-between;
  }

  .form-group.half {
    width: calc(50% - 5px);
  }

  .required {
    color: #e74c3c;
  }

  .modal-footer {
    display: flex;
    justify-content: flex-end;
  }

  .cancel-btn {
    padding: 6px 12px;
    background: none;
    border: none;
    color: #89253e;
    cursor: pointer;
    transition: color 0.2s;
  }

  .cancel-btn:hover {
    color: #333;
  }

  .save-btn {
    padding: 6px 12px;
    background: linear-gradient(135deg, #89253e, #3a6186);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
  }

  .save-btn:hover {
    transform: translateY(-1px);
  }

  /* 无任务提示样式 */
  .no-tasks-message {
    text-align: center;
    padding: 10px;
    background-color: #f8f9fd;
    border-radius: 8px;
    color: #555;
  }

  /* 添加AI任务按钮区域样式 */
  .task-action-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .ai-action-btn {
    display: flex;
    align-items: center;
    padding: 10px 18px;
    background: linear-gradient(135deg, #3a6186, #89253e);
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .ai-action-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  }

  .ai-action-btn i {
    margin-right: 8px;
    font-size: 18px;
  }

  /* AI分析结果区域样式 */
  .ai-analysis-result {
    margin-top: 30px;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  }

  .analysis-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }

  .analysis-header h5 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }

  .close-analysis-btn {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 18px;
    padding: 5px;
    transition: color 0.3s;
  }

  .close-analysis-btn:hover {
    color: #89253e;
  }

  .generating-badge {
    display: inline-flex;
    align-items: center;
    margin-left: 10px;
    font-size: 14px;
    font-weight: normal;
    color: #666;
  }

  .analysis-content {
    white-space: pre-line;
    line-height: 1.8;
    font-size: 15px;
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 6px;
    max-height: 400px;
    overflow-y: auto;
  }

  /* 任务生成结果样式 */
  .task-generation-result {
    margin-top: 15px;
  }

  .result-header {
    margin-bottom: 15px;
  }

  .result-header h5 {
    font-size: 17px;
    margin: 0 0 5px 0;
    color: #333;
  }

  .result-header p {
    font-size: 14px;
    color: #666;
    margin: 0;
  }

  .task-preview-list {
    max-height: 400px;
    overflow-y: auto;
    background-color: #f9f9f9;
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 15px;
  }

  .task-preview-item {
    background-color: #fff;
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .task-preview-header {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
  }

  .task-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #89253e, #3a6186);
    color: #fff;
    border-radius: 50%;
    font-size: 12px;
    margin-right: 8px;
    flex-shrink: 0;
  }

  .task-preview-name {
    font-weight: bold;
    flex-grow: 1;
  }

  .task-preview-date {
    font-size: 13px;
    color: #666;
  }

  .task-preview-details {
    font-size: 14px;
    line-height: 1.6;
  }

  .task-preview-details > div {
    margin-bottom: 5px;
  }

  .subtask-preview-list {
    margin: 5px 0 0 15px;
    padding: 0;
  }

  .subtask-preview-list li {
    font-size: 13px;
    margin-bottom: 3px;
  }

  .task-generation-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 15px;
  }

  .primary-btn {
    padding: 8px 15px;
    background: linear-gradient(135deg, #89253e, #3a6186);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .primary-btn:hover {
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
    transform: translateY(-1px);
  }

  .secondary-btn {
    padding: 8px 15px;
    background: #f1f1f1;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .secondary-btn:hover {
    background: #e5e5e5;
  }

  .spinner-small {
    width: 16px;
    height: 16px;
    border: 2px solid #ddd;
    border-top: 2px solid #3a6186;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: 8px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* 无结果提示样式 */
  .no-capabilities-result {
    margin-top: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    padding: 25px;
    text-align: center;
  }

  .no-result-icon {
    font-size: 40px;
    color: #cbd5e0;
    margin-bottom: 15px;
  }

  .no-capabilities-result h5 {
    margin-top: 0;
    font-size: 18px;
    color: #333;
    margin-bottom: 15px;
  }

  .no-capabilities-result p {
    margin-bottom: 15px;
    color: #555;
  }

  .no-capabilities-result ul {
    display: inline-block;
    text-align: left;
    margin-bottom: 20px;
  }

  .no-capabilities-result ul li {
    margin-bottom: 8px;
    color: #666;
  }

  .no-result-actions {
    margin-top: 20px;
  }

  /* AI能力识别样式 */
  .ai-capacity-btn-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 30px;
  }

  .ai-capacity-btn {
    display: flex;
    align-items: center;
    padding: 12px 25px;
    background: linear-gradient(135deg, #3a6186, #89253e);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  }

  .ai-capacity-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  }

  .ai-capacity-btn i {
    margin-right: 10px;
    font-size: 20px;
  }

  .ai-capacity-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  /* 能力识别结果样式 */
  .ai-capabilities-result {
    margin-top: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    padding: 25px;
  }

  .ai-capabilities-result h5 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 18px;
    color: #333;
  }

  .result-intro {
    margin-bottom: 20px;
    color: #555;
  }

  .capabilities-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
  }

  .capability-card {
    display: flex;
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .capability-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }

  .capability-icon {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, #89253e, #3a6186);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
  }

  .capability-icon i {
    font-size: 24px;
  }

  .capability-content {
    flex-grow: 1;
  }

  .capability-content h6 {
    margin: 0 0 8px 0;
    font-size: 16px;
    color: #333;
  }

  .capability-desc {
    margin-bottom: 10px;
    font-size: 14px;
    color: #555;
    line-height: 1.5;
  }

  .capability-tasks {
    margin-bottom: 15px;
    font-size: 14px;
  }

  .capability-tasks p {
    margin: 0;
  }

  .capability-actions {
    display: flex;
    justify-content: flex-end;
  }

  .capability-link-btn {
    display: inline-flex;
    align-items: center;
    padding: 6px 12px;
    background-color: #fff;
    color: #3a6186;
    border: 1px solid #3a6186;
    border-radius: 4px;
    font-size: 14px;
    text-decoration: none;
    transition: all 0.2s;
  }

  .capability-link-btn:hover {
    background-color: #3a6186;
    color: #fff;
  }

  .capability-link-btn i {
    margin-right: 5px;
  }

  .capabilities-summary {
    background-color: #f0f6ff;
    border-radius: 6px;
    padding: 15px;
    margin-top: 10px;
  }

  .capabilities-summary p {
    margin-top: 0;
    margin-bottom: 15px;
  }

  .summary-actions {
    display: flex;
    justify-content: flex-end;
}
</style> 