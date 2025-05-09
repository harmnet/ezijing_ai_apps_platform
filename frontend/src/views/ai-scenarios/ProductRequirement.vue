<template>
  <div class="product-requirement-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回场景列表
        </div>
        <h1>产品需求分析与规划 <span class="scenario-category">产品管理实践</span></h1>
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
            <img src="@/assets/images/scenarios/product-requirement.jpeg" alt="产品经理" />
          </div>
          <div class="role-info">
            <h3>产品经理 - 张明</h3>
            <p>你是一家互联网科技公司"智联科技"的产品经理。作为产品部门的骨干成员，你负责产品需求分析、用户调研、产品规划与设计等工作。你擅长分析用户需求，将业务目标转化为产品功能，并与开发团队紧密合作推动产品落地。你在公司工作三年，参与了多个成功产品的规划与迭代，对产品生命周期管理有丰富经验。</p>
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
            <p>昨天下午，产品部门总监刘总在产品战略会议上宣布，公司将在下个季度推出一款面向企业客户的数据分析平台，以满足中小企业快速增长的数据可视化和决策支持需求。</p>
            <p>刘总将这个项目的前期需求分析和产品规划工作交给了你，希望你能够通过市场调研和竞品分析，梳理出清晰的产品定位、核心功能和发展路线图。</p>
            <p>刘总只给了你几点非常模糊的方向：</p>
            <ul>
              <li>产品应该"易用且功能强大"，降低中小企业使用数据分析工具的门槛</li>
              <li>需要考虑与公司现有的企业服务生态如何整合</li>
              <li>要有"创新点"，但同时要保证核心功能的稳定可靠</li>
              <li>要考虑未来扩展的可能性，留出产品成长的空间</li>
              <li>要在合理的开发周期内可实现，控制开发成本</li>
            </ul>
            <p>刘总对你说："这是一个重要的战略项目，请你用两周时间做好充分的调研和分析，然后给出一个全面的产品需求文档和规划方案。记得考虑用户体验、技术可行性和商业价值这几个维度。"</p>
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
              <h3>紧急项目：两周内完成需求分析与规划</h3>
              <p>刘总希望你在两周内完成这份产品需求分析和规划方案，因为公司需要尽快确定产品路线图以便安排研发资源。考虑到需要进行大量的市场调研、用户访谈、竞品分析，并且要兼顾用户体验、技术可行性和商业价值多个维度，传统的方式很难在短时间内产出高质量的完整方案。同时，由于产品定位针对的是数据分析这一专业性较强的领域，需要结合多学科知识才能制定出合理的产品架构和功能设计。</p>
            </div>
          </div>
        </div>
      </div>

      <!-- AI辅助任务梳理部分 -->
      <div class="section ai-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助任务梳理
        </h2>
        <div class="ai-workflow-card">
          <h3>运用提示词工程，让AI协助你完成任务</h3>
          <p>面对这项要求全面且时间紧迫的产品需求分析与规划任务，你决定利用AI的能力来提高工作效率和质量。以下是使用提示词工程方法与AI协作进行产品需求分析与规划的流程：</p>
          
          <div class="workflow-steps">
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>需求背景整理与分析框架构建</h4>
                <p>首先，利用AI帮助你整理和分析项目背景，构建一个全面的产品需求分析框架。</p>
                <div class="prompt-example">
                  <div class="prompt-title">示例提示词：</div>
                  <div class="prompt-content">
                    <p>你是一位拥有10年经验的资深产品经理和产品战略专家。我正在负责为一家互联网科技公司开发一款面向中小企业的数据分析平台。项目目标是降低中小企业使用数据分析的门槛，同时提供强大的分析功能。</p>
                    <p>我的领导给出的方向很模糊：</p>
                    <ul>
                      <li>产品应该"易用且功能强大"</li>
                      <li>需要与公司现有企业服务生态整合</li>
                      <li>要有创新点，同时保证核心功能稳定可靠</li>
                      <li>考虑未来扩展可能性</li>
                      <li>控制开发周期和成本</li>
                    </ul>
                    <p>请帮我构建一个全面的产品需求分析框架，包括：</p>
                    <ol>
                      <li>我应该从哪些维度分析这个产品需求</li>
                      <li>在每个维度上，有哪些关键问题需要回答</li>
                      <li>如何平衡易用性与功能强大这两个看似矛盾的目标</li>
                      <li>如何定义和评估产品的创新点</li>
                      <li>如何结构化地组织这些分析结果，形成一个逻辑清晰的产品需求分析文档</li>
                    </ol>
                    <p>请提供一个结构化的分析框架，帮助我系统地思考这个产品的各个方面。</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4>用户需求与场景分析</h4>
                <p>基于第一步的框架，引导AI帮助你深入分析目标用户的需求和使用场景。</p>
                <div class="prompt-example">
                  <div class="prompt-title">示例提示词：</div>
                  <div class="prompt-content">
                    <p>基于我们的产品需求分析框架，现在需要深入分析中小企业在数据分析方面的具体需求和使用场景。</p>
                    <p>请帮我识别并详细描述5-6个不同类型的目标用户画像和他们的核心使用场景。每个用户画像应包含：</p>
                    <ul>
                      <li>用户角色（如：小型电商公司运营经理、中型制造企业财务主管等）</li>
                      <li>用户特点（技术水平、工作挑战、决策模式等）</li>
                      <li>典型业务场景（需要解决什么问题、处理什么类型的数据）</li>
                      <li>关键需求点（效率需求、分析深度需求、可视化需求等）</li>
                      <li>痛点和挑战（当前解决方案的不足）</li>
                    </ul>
                    <p>然后，对于每个用户画像，请创建一个详细的用例场景，描述：</p>
                    <ol>
                      <li>用户在什么具体情境下需要使用我们的数据分析平台</li>
                      <li>他们希望通过平台完成什么具体目标</li>
                      <li>操作流程中可能遇到的障碍和期望获得的帮助</li>
                      <li>成功的标准和指标是什么</li>
                    </ol>
                    <p>请确保这些用户画像和场景：</p>
                    <ul>
                      <li>覆盖中小企业数据分析的多种典型需求</li>
                      <li>具有足够的细节和真实性</li>
                      <li>能够帮助我们发现潜在的产品差异化机会</li>
                      <li>能够指导后续的产品功能设计</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>产品功能结构与思维导图</h4>
                <p>利用AI帮助你构建产品的功能结构，并生成清晰的思维导图。</p>
                <div class="prompt-example">
                  <div class="prompt-title">示例提示词：</div>
                  <div class="prompt-content">
                    <p>基于前面的用户需求分析，现在我需要构建一个完整的产品功能结构，并以思维导图的形式呈现。</p>
                    <p>请帮我创建一个详细的思维导图结构，展示这款面向中小企业的数据分析平台应该包含的所有关键功能模块和子功能。思维导图应该：</p>
                    <ol>
                      <li>从核心产品定位出发，分解为主要功能模块（一级节点）</li>
                      <li>每个主要功能模块进一步分解为具体功能点（二级节点）</li>
                      <li>必要时提供更深层次的功能细节（三级节点）</li>
                      <li>标明每个功能的优先级（必要功能、重要功能、锦上添花功能）</li>
                      <li>指出哪些功能属于产品差异化或创新点</li>
                    </ol>
                    <p>思维导图应该涵盖以下几个方面的功能：</p>
                    <ul>
                      <li>数据接入与管理功能</li>
                      <li>数据处理与转换功能</li>
                      <li>数据分析与挖掘功能</li>
                      <li>数据可视化与仪表盘功能</li>
                      <li>报表生成与共享功能</li>
                      <li>用户权限与协作功能</li>
                      <li>系统设置与集成功能</li>
                    </ul>
                    <p>请以文本形式描述这个思维导图的完整结构，使用缩进和编号来表示层级关系，这样我可以轻松地将其转换为可视化的思维导图。对于每个关键功能点，简要说明其目的和价值。</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">4</div>
              <div class="step-content">
                <h4>用户交互流程设计</h4>
                <p>借助AI的帮助，设计关键用户交互流程，并生成流程图。</p>
                <div class="prompt-example">
                  <div class="prompt-title">示例提示词：</div>
                  <div class="prompt-content">
                    <p>基于我们已经确定的产品功能结构，现在需要设计几个核心用户交互流程，确保用户体验的流畅性和易用性。请帮我详细设计以下5个关键用户流程，并以流程图的形式表达：</p>
                    <ol>
                      <li><strong>数据源连接与导入流程</strong>：用户如何连接数据源或导入数据到平台</li>
                      <li><strong>数据分析报表创建流程</strong>：用户如何从原始数据创建分析报表</li>
                      <li><strong>仪表盘定制与共享流程</strong>：用户如何创建、定制和共享仪表盘</li>
                      <li><strong>异常数据监控与告警设置流程</strong>：用户如何设置数据监控规则和告警</li>
                      <li><strong>团队协作与权限管理流程</strong>：管理员如何设置团队成员权限和协作方式</li>
                    </ol>
                    <p>对于每个流程，请提供：</p>
                    <ul>
                      <li>详细的步骤描述，从起点到终点</li>
                      <li>每个步骤的用户操作和系统响应</li>
                      <li>可能的分支路径和处理方式</li>
                      <li>关键决策点和用户提示</li>
                      <li>如何体现"易用性"的设计考虑</li>
                    </ul>
                    <p>请以文本形式描述这些流程图，使用清晰的步骤标记和缩进来表示流程的层次和分支，这样我可以轻松地将其转换为可视化的流程图。对于复杂的决策点，请使用"如果...那么..."的格式来表示条件分支。</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">5</div>
              <div class="step-content">
                <h4>产品规划与路线图</h4>
                <p>指导AI帮助你制定产品发展规划和阶段性路线图。</p>
                <div class="prompt-example">
                  <div class="prompt-title">示例提示词：</div>
                  <div class="prompt-content">
                    <p>基于前面的需求分析和功能设计，现在需要制定一个产品规划路线图，合理安排功能的开发优先级和发布节奏。假设我们计划在12个月内分3个主要版本发布产品。</p>
                    <p>请帮我创建一个详细的产品路线图，包括：</p>
                    <ol>
                      <li>产品的三个主要发布阶段（MVP、V1.0、V2.0）</li>
                      <li>每个阶段的核心目标和价值主张</li>
                      <li>每个阶段要实现的具体功能和特性</li>
                      <li>主要的技术挑战和风险点</li>
                      <li>关键的评估指标和成功标准</li>
                    </ol>
                    <p>请考虑以下因素来确定功能的优先级和排序：</p>
                    <ul>
                      <li>用户价值：解决最核心的用户痛点和需求</li>
                      <li>技术复杂度：技术实现的难易程度和风险</li>
                      <li>依赖关系：功能之间的前置依赖</li>
                      <li>市场差异化：能够产生竞争优势的差异化功能</li>
                      <li>资源限制：开发资源和时间的合理分配</li>
                    </ul>
                    <p>对于每个发布阶段，请提供：</p>
                    <ul>
                      <li>该阶段的时间点和持续时间</li>
                      <li>详细的功能清单和优先级</li>
                      <li>用户价值和商业价值的阐述</li>
                      <li>潜在风险和应对策略</li>
                    </ul>
                    <p>最后，请给出一些关于如何灵活调整路线图以应对市场变化和用户反馈的建议。</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">6</div>
              <div class="step-content">
                <h4>产品需求文档(PRD)撰写</h4>
                <p>最后，整合前面的所有分析和设计，利用AI协助撰写完整的产品需求文档。</p>
                <div class="prompt-example">
                  <div class="prompt-title">示例提示词：</div>
                  <div class="prompt-content">
                    <p>现在我需要将前面所有的分析、设计和规划整合成一份完整、专业的产品需求文档(PRD)。请帮我编写一份结构清晰、内容全面的PRD文档大纲，包括以下部分：</p>
                    <ol>
                      <li><strong>文档概述</strong>：文档目的、适用范围、相关人员和参考文档</li>
                      <li><strong>产品概述</strong>：产品愿景、目标和定位，核心价值主张，关键成功指标</li>
                      <li><strong>市场分析</strong>：目标市场规模，竞品分析，市场机会和挑战</li>
                      <li><strong>用户分析</strong>：目标用户画像，用户需求和痛点，用户旅程地图</li>
                      <li><strong>产品功能</strong>：功能模块概述，详细功能说明，功能优先级</li>
                      <li><strong>用户界面</strong>：信息架构，关键页面描述，交互原则</li>
                      <li><strong>用户流程</strong>：核心用户流程图和说明，边界条件和异常处理</li>
                      <li><strong>非功能需求</strong>：性能要求，安全要求，兼容性要求，可扩展性要求</li>
                      <li><strong>产品规划</strong>：发布计划，迭代路线图，评估指标</li>
                      <li><strong>附录</strong>：术语表，参考资料，变更记录</li>
                    </ol>
                    <p>对于每个部分，请提供：</p>
                    <ul>
                      <li>该部分应包含的具体内容和要点</li>
                      <li>合适的图表和可视化建议</li>
                      <li>撰写时的注意事项和最佳实践</li>
                    </ul>
                    <p>请尽量使用专业、清晰的产品经理语言，同时确保文档结构逻辑性强，便于团队成员理解和执行。特别注意突出产品的差异化优势和创新点，以及如何平衡易用性和功能强大这两个关键目标。</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="ai-results-section">
            <h3>AI辅助成果</h3>
            <p>通过上述提示词工程方法与AI协作，你在两周内高效完成了一份全面、专业的产品需求分析与规划方案，包括：</p>
            <div class="results-grid">
              <div class="result-item">
                <i class="ri-file-text-line"></i>
                <h4>需求分析文档</h4>
                <p>全面的市场分析、用户需求分析、竞品分析和产品定位分析</p>
              </div>
              <div class="result-item">
                <i class="ri-mind-map"></i>
                <h4>产品功能思维导图</h4>
                <p>清晰展示产品功能结构、层级关系和优先级的思维导图</p>
              </div>
              <div class="result-item">
                <i class="ri-flow-chart"></i>
                <h4>用户交互流程图</h4>
                <p>详细的核心用户操作流程图，确保产品易用性和良好体验</p>
              </div>
              <div class="result-item">
                <i class="ri-road-map-line"></i>
                <h4>产品路线图</h4>
                <p>分阶段的产品开发计划，包括功能优先级和发布时间表</p>
              </div>
            </div>
            <p class="conclusion">这种AI辅助方法不仅帮助你高效完成了复杂的产品需求分析与规划工作，还通过结构化的提示引导AI提供了深入的洞察和创新思路。你的方案得到了刘总的高度认可，他特别赞赏了你对市场需求的深入理解、产品功能的合理规划以及产品路线图的清晰展示。这份方案将作为公司开发数据分析平台的重要基础，而你提出的产品创新点也将成为产品的核心竞争优势。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductRequirement',
  data() {
    return {
      loaded: false
    }
  },
  mounted() {
    // 页面加载完成后设置状态
    setTimeout(() => {
      this.loaded = true
    }, 100)
  },
  methods: {
    goBack() {
      this.$router.push('/practical-scenario')
    }
  }
}
</script>

<style scoped>
.product-requirement-container {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #333;
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: #fff;
  padding: 30px 0;
  margin-bottom: 30px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #fff;
  font-size: 14px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.back-link:hover {
  opacity: 0.8;
}

.back-link i {
  margin-right: 5px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  margin: 0;
}

.scenario-category {
  font-size: 16px;
  font-weight: normal;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 5px 12px;
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
  color: #6a11cb;
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
  flex-shrink: 0;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 20px;
  border: 3px solid #fff;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

.role-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.role-info h3 {
  font-size: 20px;
  margin: 0 0 10px;
  color: #333;
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
  background-color: #f5f0ff;
  border-left: 4px solid #6a11cb;
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
  background-color: #6a11cb;
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
  color: #6a11cb;
}

.deadline-info p {
  color: #555;
  font-size: 16px;
  line-height: 1.7;
  margin: 0;
}

.ai-workflow-card {
  background-color: #f8f9fd;
}

.ai-workflow-card h3 {
  font-size: 20px;
  color: #6a11cb;
  margin: 0 0 15px;
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
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: #fff;
  font-weight: bold;
  border-radius: 50%;
  flex-shrink: 0;
  margin-right: 20px;
}

.step-content {
  flex-grow: 1;
}

.step-content h4 {
  font-size: 18px;
  margin: 0 0 10px;
  color: #6a11cb;
}

.prompt-example {
  margin-top: 15px;
  background-color: #fff;
  border-radius: 6px;
  border: 1px solid #e1e4e8;
  overflow: hidden;
}

.prompt-title {
  background-color: #f1f2f6;
  padding: 10px 15px;
  font-weight: 500;
  color: #6a11cb;
  border-bottom: 1px solid #e1e4e8;
}

.prompt-content {
  padding: 15px;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}

.prompt-content p, 
.prompt-content ul,
.prompt-content ol {
  margin-bottom: 10px;
}

.prompt-content ul,
.prompt-content ol {
  padding-left: 20px;
}

.prompt-content li {
  margin-bottom: 5px;
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
  color: #6a11cb;
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
  color: #6a11cb;
  margin-bottom: 15px;
}

.result-item h4 {
  font-size: 18px;
  margin: 0 0 10px;
  color: #6a11cb;
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
  background-color: #f5f0ff;
  border-radius: 6px;
  color: #6a11cb;
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
}
</style> 