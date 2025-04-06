<template>
  <div class="scenarios-page">
    <div class="page-header">
      <h1>HR常见业务场景</h1>
      <p class="description">人力资源管理工作中的常见挑战，AI可以为HR专业人员提供智能化解决方案，显著提升工作效率和决策质量</p>
    </div>

    <div class="scenarios-list">
      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-file-text-line"></i>
          </div>
          <h3>招聘职位描述生成</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">在招聘环节中，精准的职位描述是吸引合适候选人的关键。AI可以根据岗位需求快速生成专业、全面的招聘JD，覆盖职责、要求、技能和福利等方面，帮助HR团队节省大量编写时间，提高招聘精准度，吸引更合适的人才。通过AI生成的JD模板，HR可以进一步调整和完善，使其更贴合企业文化和具体需求。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/jd-maker" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用AI招聘JD生成功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-file-paper-2-line"></i>
          </div>
          <h3>劳动合同审核</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">劳动合同的合规性和完整性对企业至关重要。AI可协助HR专业人员快速审核合同条款，识别潜在法律风险，确保合同符合最新劳动法规定。系统能自动检测不平等条款、模糊表述和缺失项，并提供修改建议，大大降低了因合同问题引发劳动纠纷的风险。使用AI辅助审核后，HR团队可将更多精力集中在员工关系维护和战略性工作上，提升人力资源管理整体效能。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/legal/contract-check" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用合同检查功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-questionnaire-line"></i>
          </div>
          <h3>员工培训计划</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">设计有效的员工培训计划需要对知识点进行系统化组织。AI能够帮助HR和培训经理快速开发专业的培训PPT，自动生成结构化的培训课件，包括学习目标、关键内容和互动环节。这不仅提高了培训材料的质量和专业性，也大幅缩短了准备时间。通过AI辅助培训设计，企业可以迅速响应技能缺口，实现更灵活的人才发展策略，同时确保培训内容的一致性和高质量水平。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/ppt" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用AI培训PPT生成功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-chat-4-line"></i>
          </div>
          <h3>会议纪要与决策追踪</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">HR部门经常需要参与和组织各类会议，包括招聘面试讨论、绩效评估会议和团队沟通等。AI会议纪要功能能够自动记录并整理会议内容，提取关键决策点和行动项目，确保所有重要信息都被准确记录。这不仅提升了会议效率，还为HR提供了清晰的记录跟踪工具，便于后续决策执行和进度监控。HR团队可将精力集中在深度分析和战略性讨论上，而不是文字记录工作。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/meeting-minutes" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用AI会议纪要功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-bar-chart-grouped-line"></i>
          </div>
          <h3>员工满意度分析</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">理解员工满意度和敬业度对留住人才至关重要。AI数据分析功能可帮助HR团队深入挖掘员工调查结果，识别趋势和关键影响因素。系统自动处理大量数据，生成可视化报告，帮助HR发现问题根源和改进机会。通过AI驱动的数据分析，HR团队能够制定更有针对性的员工保留策略，提升组织文化，降低人才流失率。这种基于数据的决策方法大大提高了HR工作的战略价值和影响力。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/data-analysis" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用AI数据分析功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-profile-line"></i>
          </div>
          <h3>求职简历优化</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">在人才招聘过程中，HR经常需要指导内部员工或候选人改进简历，使其更具竞争力。AI简历优化工具能够全面分析简历结构、内容、关键词等要素，给出专业建议，提升简历通过筛选系统的几率。对HR和招聘专员而言，这一工具也能用于评估收到的简历质量，快速识别合适人选的亮点和潜在不足。帮助企业建立更高效的简历处理流程，提高人才筛选的准确性和效率。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/cv-optimize" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用AI简历优化功能
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HRScenarios'
}
</script>

<style scoped>
.scenarios-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 48px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.page-header .description {
  font-size: 16px;
  color: #666;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.scenarios-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.scenario-item {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
}

.scenario-header {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: rgba(186, 0, 63, 0.05);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.scenario-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background-color: #ba003f;
  margin-right: 16px;
}

.scenario-icon i {
  font-size: 24px;
  color: #fff;
}

.scenario-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.scenario-content {
  padding: 24px;
}

.scenario-desc {
  font-size: 16px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 24px;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
}

.action-button {
  display: inline-flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #ba003f;
  color: white;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #9a0035;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.2);
}

.action-button i {
  margin-right: 6px;
}
</style> 