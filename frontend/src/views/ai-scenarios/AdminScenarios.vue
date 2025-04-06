<template>
  <div class="scenarios-page">
    <div class="page-header">
      <h1>企业行政常见业务场景</h1>
      <p class="description">针对企业行政工作中的常见场景，AI可以提供智能化解决方案，大幅提升行政工作效率和专业度。点击下方按钮，即可体验系统现有功能！</p>
    </div>

    <div class="scenarios-list">
      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-calendar-check-line"></i>
          </div>
          <h3>会议纪要生成</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">会议纪要是企业日常运作的重要文档，但人工整理费时费力且容易遗漏重点。AI会议纪要生成功能可以自动从会议录音或笔记中提取关键信息，生成结构化的会议纪要，包括会议主题、参会人员、讨论要点、决策事项和行动计划。这大大减轻了行政人员的工作负担，确保会议成果得到有效记录和追踪，提高团队协作效率和决策落实率。系统会根据企业需求自动调整纪要格式和详细程度，确保输出符合公司规范。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/meeting-minutes" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用会议纪要生成功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-file-list-3-line"></i>
          </div>
          <h3>工作报告生成</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">定期工作报告是企业管理中不可或缺的环节，但撰写格式规范、内容全面的报告往往耗时耗力。AI工作报告生成功能可以根据输入的工作内容要点，智能组织内容结构，生成专业的周报、月报或季度报告。系统会自动突出工作成果与价值，合理安排内容层次，添加适当的数据支持和图表展示，使报告更具说服力和可读性。这使行政人员能够在短时间内完成高质量的报告撰写，减少重复性工作，提高工作报告的专业水准和管理参考价值。</p>
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
            <i class="ri-mail-send-line"></i>
          </div>
          <h3>商务邮件撰写</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">专业的商务邮件是企业对外沟通的重要窗口，直接影响企业形象和合作效果。AI邮件撰写助手能根据沟通目的、收件对象和核心内容，生成语言得体、结构清晰、表达精准的商务邮件。无论是客户邀请、供应商协商、合作伙伴沟通还是内部通知，系统都能生成符合商务礼仪和企业调性的邮件内容。这帮助行政人员高效处理日常邮件沟通，确保邮件质量一致性，减少沟通歧义，提高邮件回复率和沟通效率，让商务交流更加专业高效。</p>
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
            <i class="ri-file-paper-2-line"></i>
          </div>
          <h3>合同审核优化</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">合同审核是企业行政管理中的关键环节，但传统人工审核费时费力且易出纰漏。AI合同审核功能可以快速分析合同文本，自动识别关键条款、权利义务、风险点和法律合规性问题。系统能根据企业自定义的审核标准，对合同条款提出修改建议，指出潜在风险，确保合同内容符合公司利益和法律要求。这不仅提高了合同审核的效率和准确性，也降低了企业法律风险，为行政人员和法务团队提供了强大的辅助工具，使合同管理更加规范化和智能化。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/legal/contract-check" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用合同审核功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-presentation-line"></i>
          </div>
          <h3>培训材料制作</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">优质的培训材料是企业人才发展的重要保障，但制作专业、吸引人的培训PPT耗时且要求专业技能。AI培训PPT生成功能可根据培训主题和内容要点，自动设计结构合理、视觉吸引的培训演示文稿。系统会根据内容类型选择合适的版式和图表，自动生成适当的图片建议，调整文字排版，使培训材料既专业又具有视觉吸引力。这使行政人员和培训专员能够快速准备高质量的培训材料，减少设计时间，提高培训效果，促进企业知识高效传递和员工技能提升。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/ai-ppt" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用AI PPT生成功能
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminScenarios'
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
  margin-top: 24px;
}

.action-button {
  padding: 12px 24px;
  background-color: #ba003f;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #9a0033;
}

.action-button i {
  margin-right: 8px;
}
</style> 