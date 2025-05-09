<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>内部审计师 <span class="position-category">财务与风控类</span></h1>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="container">
      <!-- 职位详情部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-profile-line"></i> 职位详细介绍
        </h2>
        <div class="detail-card">
          <div class="detail-item">
            <h3>岗位职责</h3>
            <ul>
              <li>设计并执行内部审计计划，评估公司内部控制体系的有效性</li>
              <li>识别业务流程中的风险点，并提出合理的改进建议</li>
              <li>审查财务报表和运营数据，确保数据的准确性和完整性</li>
              <li>监督公司各部门对内部控制制度的执行情况</li>
              <li>调查潜在的欺诈行为，保障公司资产安全</li>
              <li>评估公司是否遵守相关法律法规和内部政策</li>
              <li>编写审计报告，向管理层提交审计发现和改进建议</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>会计、审计或财务相关专业学士及以上学历</li>
              <li>持有CIA（注册内部审计师）、CPA或ACCA等专业认证优先</li>
              <li>3年以上内部审计或相关领域工作经验</li>
              <li>熟悉内部控制框架（如COSO）和风险管理原则</li>
              <li>良好的数据分析能力和批判性思维</li>
              <li>精通审计软件和数据分析工具</li>
              <li>优秀的沟通能力和报告撰写能力</li>
              <li>高度的职业道德和独立性</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>内部审计师需要与多个部门和系统交互：</p>
            <ul>
              <li><strong>审计计划与程序文档</strong>：审计工作底稿、审计清单、风险评估表</li>
              <li><strong>内部控制评估工具</strong>：控制矩阵、流程图、缺陷追踪系统</li>
              <li><strong>数据分析平台</strong>：异常交易筛选、模式识别、趋势分析工具</li>
              <li><strong>合规监控系统</strong>：法规变更追踪、合规检查清单</li>
              <li><strong>审计报告模板</strong>：发现问题汇总、改进建议、跟进措施</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>与其他岗位的协作</h3>
            <p>内部审计师需要与公司多个角色密切合作：</p>
            <ul>
              <li><strong>财务经理</strong>：协作审查财务报表，评估财务控制有效性</li>
              <li><strong>法务合规经理</strong>：共同确保公司活动符合法律法规要求</li>
              <li><strong>IT管理人员</strong>：评估信息系统安全和IT控制措施</li>
              <li><strong>业务部门负责人</strong>：获取业务流程信息，沟通审计发现</li>
              <li><strong>高级管理层</strong>：报告重大审计发现并提供改进建议</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>内部审计师的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>初级审计员 → 高级审计员 → 审计经理 → 审计总监 → 首席审计官</li>
              <li>内部审计师 → 风险管理专家 → 企业风险管理总监</li>
              <li>内部审计师 → 合规专员 → 合规总监</li>
              <li>内部审计师 → 外部审计师 → 审计合伙人</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于内部审计师的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 数据分析 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-bar-chart-line"></i>
            </div>
            <div class="function-content">
              <h3>数据分析</h3>
              <p>AI辅助分析审计数据，快速识别异常交易和风险模式，提供数据洞察。</p>
              <div class="function-tags">
                <span class="tag">数据</span>
                <span class="tag">分析</span>
              </div>
              <router-link to="/ai-office/data-analysis" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 合同检查 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-search-line"></i>
            </div>
            <div class="function-content">
              <h3>合同检查</h3>
              <p>AI辅助审核合同条款合规性，标识潜在风险点与不合理条款。</p>
              <div class="function-tags">
                <span class="tag">合同</span>
                <span class="tag">合规</span>
              </div>
              <router-link to="/ai-office/legal/contract-check" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文档总结 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>文档总结</h3>
              <p>快速总结审计报告、政策文件等文档，提取关键信息和合规要点。</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">摘要</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- AI会议纪要 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-text-line"></i>
            </div>
            <div class="function-content">
              <h3>AI会议纪要</h3>
              <p>自动记录审计会议内容，生成结构化会议记录与审计发现要点。</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">记录</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文档结构撰写 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-draft-line"></i>
            </div>
            <div class="function-content">
              <h3>文档结构撰写</h3>
              <p>AI辅助生成审计报告文档结构，提供专业审计报告模板。</p>
              <div class="function-tags">
                <span class="tag">报告</span>
                <span class="tag">模板</span>
              </div>
              <router-link to="/text-creation/copywriting/document-structure" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InternalAuditor',
  methods: {
    goBack() {
      this.$router.push('/ai-scenarios');
    }
  }
}
</script>

<style scoped>
.position-detail-container {
  padding-bottom: 60px;
}

.position-header {
  background-color: #f5f5f5;
  padding: 40px 0 30px;
  margin-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #666;
  margin-bottom: 20px;
  cursor: pointer;
  transition: color 0.2s;
}

.back-link:hover {
  color: #ba003f;
}

.back-link i {
  margin-right: 5px;
}

.position-header h1 {
  font-size: 36px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.position-category {
  font-size: 16px;
  font-weight: normal;
  color: #666;
  margin-left: 10px;
}

.position-section {
  margin-bottom: 50px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 10px;
  color: #ba003f;
}

.section-desc {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
}

.detail-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 30px;
}

.detail-item {
  margin-bottom: 25px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  position: relative;
  padding-left: 15px;
}

.detail-item h3::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 18px;
  background-color: #ba003f;
  border-radius: 2px;
}

.detail-item p {
  font-size: 16px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 10px;
}

.detail-item ul {
  padding-left: 20px;
}

.detail-item li {
  font-size: 15px;
  color: #555;
  line-height: 1.8;
  margin-bottom: 8px;
}

.ai-functions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.function-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  padding: 25px;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.function-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background-color: rgba(186, 0, 63, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  flex-shrink: 0;
}

.function-icon i {
  font-size: 30px;
  color: #ba003f;
}

.function-content {
  flex: 1;
}

.function-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.function-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.function-tags {
  display: flex;
  margin-bottom: 15px;
}

.tag {
  background-color: #f5f5f5;
  color: #666;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 4px;
  margin-right: 8px;
}

.use-function-btn {
  display: inline-flex;
  align-items: center;
  color: #ba003f;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.use-function-btn:hover {
  color: #d43f6d;
}

.use-function-btn i {
  margin-left: 5px;
  transition: transform 0.2s;
}

.use-function-btn:hover i {
  transform: translateX(3px);
}
</style> 