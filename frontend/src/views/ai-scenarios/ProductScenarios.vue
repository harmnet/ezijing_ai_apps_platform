<template>
  <div class="scenarios-page">
    <div class="page-header">
      <h1>产品研发常见业务场景</h1>
      <p class="description">针对产品研发过程中的常见挑战，AI可以提供高效智能的解决方案，帮助产品团队提升创新效率和决策质量。点击下方按钮，即可体验系统现有功能！</p>
    </div>

    <div class="scenarios-list">
      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-file-list-3-line"></i>
          </div>
          <h3>需求文档撰写</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">高质量的需求文档是产品成功的基础，但撰写全面、清晰的需求说明往往耗时且需要专业技能。AI需求文档生成功能可以根据产品创意、目标用户和核心功能点，快速生成结构完整的产品需求文档。系统自动组织内容架构，包括产品概述、用户场景、功能描述、交互流程和非功能需求等关键部分，确保文档的完整性和逻辑性。这大大减轻了产品经理的写作负担，缩短了需求分析到文档输出的时间，提高了团队沟通效率，保证研发过程中的需求一致性，加速产品从概念到开发的转化过程。</p>
          <div class="action-buttons">
            <router-link to="/text-creation/copywriting/document-structure" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用文档结构生成功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-user-search-line"></i>
          </div>
          <h3>用户洞察分析</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">深入理解用户是产品创新的关键，但传统用户研究方法耗时且难以从大量数据中提炼关键洞察。AI用户洞察分析功能可以高效处理用户反馈、访谈记录和调研数据，自动识别共性问题、情感倾向和潜在需求。系统能够对用户评论进行多维度分类，提取关键词和热点话题，生成可视化的用户画像和需求地图。这帮助产品团队快速把握用户真实痛点和偏好，优化产品功能设计，提高用户满意度和留存率。通过数据驱动的用户洞察，产品决策更加精准，创新方向更符合市场需求，大幅降低产品迭代风险。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/data-analysis" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用数据分析功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-flow-chart"></i>
          </div>
          <h3>产品方案设计</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">完整的产品方案是研发团队的指南针，但设计兼顾用户体验和技术可行性的方案需要跨领域知识和丰富经验。AI产品方案设计功能可以根据产品目标和用户需求，生成全面的产品设计方案，包括功能框架、用户流程、界面布局和交互逻辑。系统会基于产品类型和行业最佳实践，提供适合的设计模式和用户体验建议，同时考虑技术实现的可行性和复杂度。这帮助产品团队快速搭建产品框架，缩短方案设计周期，减少设计与开发之间的沟通成本，提高产品设计的专业性和完整性，使产品开发过程更加高效和有方向性。</p>
          <div class="action-buttons">
            <router-link to="/text-creation/copywriting/longform" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用文档生成功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-presentation-line"></i>
          </div>
          <h3>产品演示与路演</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">产品演示是向内外部展示产品价值的关键环节，但制作专业、吸引人的演示材料需要大量时间和设计技能。AI产品演示PPT生成功能可以根据产品特点、演示目的和听众特性，自动创建结构清晰、视觉精美的演示文稿。系统会智能组织内容框架，设计符合产品调性的页面布局，生成有说服力的论述和引人注目的数据展示方式，让产品故事更加生动和有吸引力。这大大减轻了产品经理准备演示材料的工作量，提高路演和汇报的专业度和说服力，无论是内部评审还是客户展示，都能更好地传达产品价值和亮点，提高项目推进效率。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/ai-ppt" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用AI PPT生成功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-code-box-line"></i>
          </div>
          <h3>技术方案评估</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">技术方案的质量直接影响产品功能实现和性能表现，但全面评估技术方案需要专业知识和系统思维。AI技术方案评估功能可以分析产品需求和技术实现方案之间的匹配度，评估技术架构的合理性和扩展性，识别潜在的性能瓶颈和安全风险。系统会结合行业最佳实践和技术发展趋势，提供针对性的优化建议和替代方案，帮助产品和技术团队作出更明智的技术决策。这加速了方案评审过程，降低了技术风险，提高了产品开发的质量和效率，减少后期返工和修改的可能性，使产品能够按时、高质量地交付，更好地满足用户需求和业务目标。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/integration-test" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用系统集成测试功能
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductScenarios'
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