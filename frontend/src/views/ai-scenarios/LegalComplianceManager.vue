<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>法务合规经理 <span class="position-category">法务与风控类</span></h1>
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
              <li>负责公司法律事务管理，确保公司运营合规性</li>
              <li>审查和起草各类商业合同、协议和法律文件</li>
              <li>识别和评估业务相关法律风险，提供预防和解决方案</li>
              <li>开展合规培训，增强员工法律意识和风险防范能力</li>
              <li>管理外部法律顾问和合作律所，控制法律服务成本</li>
              <li>处理公司诉讼、仲裁和其他法律纠纷事务</li>
              <li>跟踪和研究行业相关法律法规，确保公司政策和实践的及时更新</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>法律或相关专业学士以上学历，具有法律职业资格证书</li>
              <li>5年以上企业法律合规管理经验，熟悉公司相关业务领域法律法规</li>
              <li>熟练掌握合同法、公司法、知识产权法等商业法律知识</li>
              <li>具备良好的法律分析能力和风险评估能力</li>
              <li>优秀的沟通协调能力和谈判技巧</li>
              <li>出色的写作能力，能够起草和审阅各类法律文件</li>
              <li>具有较强的商业敏感度和解决问题的能力</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>法务合规经理需要熟练使用多种工具和系统：</p>
            <ul>
              <li><strong>合同管理系统</strong>：合同模板库、合同审批流程、合同归档与检索</li>
              <li><strong>法律数据库</strong>：法规查询、案例研究、法律动态追踪</li>
              <li><strong>合规风控系统</strong>：风险识别、合规审查、内控管理</li>
              <li><strong>诉讼案件管理平台</strong>：案件跟踪、证据管理、诉讼进程监控</li>
              <li><strong>法律知识管理系统</strong>：法律文档库、法律知识沉淀与共享</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>与其他岗位的协作</h3>
            <p>法务合规经理需要与公司多个角色密切合作：</p>
            <ul>
              <li><strong>高级管理层</strong>：提供法律合规建议，参与重大决策的法律风险评估</li>
              <li><strong>业务部门</strong>：审核业务合同，解决业务活动中的法律问题</li>
              <li><strong>财务经理</strong>：协作处理税务合规、财务合规和审计事宜</li>
              <li><strong>内部审计师</strong>：配合内部调查，提供法律支持和建议</li>
              <li><strong>人力资源部门</strong>：处理劳动法律事务，员工合规培训</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>法务合规经理的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>法务专员 → 法务经理 → 高级法务经理 → 法律总监/总法律顾问</li>
              <li>法务合规经理 → 合规总监 → 首席合规官(CCO)</li>
              <li>企业法务 → 专业律所律师 → 合伙人</li>
              <li>法务合规经理 → 业务部门管理 → 公司高管</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于法务合规经理的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 合同检查 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-search-line"></i>
            </div>
            <div class="function-content">
              <h3>合同检查</h3>
              <p>AI辅助审核合同条款，快速识别潜在风险点、模糊条款和法律漏洞</p>
              <div class="function-tags">
                <span class="tag">合同</span>
                <span class="tag">风控</span>
              </div>
              <router-link to="/ai-office/legal/contract-check" class="use-function-btn">
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
              <p>AI辅助生成法律文件结构，快速创建合规政策、法律意见书等专业文档框架</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">模板</span>
              </div>
              <router-link to="/text-creation/copywriting/document-structure" class="use-function-btn">
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
              <p>快速总结法规文件、判决书和法律报告，提取关键法律要点和合规要求</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">摘要</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 长文创作 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-book-2-line"></i>
            </div>
            <div class="function-content">
              <h3>长文创作</h3>
              <p>辅助撰写法律分析报告、合规指南和内部政策文件，提高文档专业性</p>
              <div class="function-tags">
                <span class="tag">创作</span>
                <span class="tag">报告</span>
              </div>
              <router-link to="/text-creation/copywriting/long-form" class="use-function-btn">
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
              <p>自动记录法务会议内容，提取法律讨论要点和合规决策事项</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">记录</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文章校对 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-error-warning-line"></i>
            </div>
            <div class="function-content">
              <h3>文章校对</h3>
              <p>检查法律文件中的专业术语、语法和表述准确性，确保文档专业严谨</p>
              <div class="function-tags">
                <span class="tag">校对</span>
                <span class="tag">润色</span>
              </div>
              <router-link to="/text-creation/revision/proofreading" class="use-function-btn">
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
  name: 'LegalComplianceManager',
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
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

.detail-item {
  margin-bottom: 30px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item h3 {
  font-size: 20px;
  font-weight: 600;
  color: #ba003f;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #eee;
}

.detail-item ul {
  padding-left: 20px;
}

.detail-item li {
  margin-bottom: 10px;
  line-height: 1.6;
}

.ai-functions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.function-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.function-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  background-color: rgba(186, 0, 63, 0.05);
}

.function-icon i {
  font-size: 32px;
  color: #ba003f;
}

.function-content {
  padding: 20px;
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
  margin-bottom: 16px;
}

.function-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  font-size: 12px;
  background-color: #f5f5f5;
  color: #666;
  padding: 4px 8px;
  border-radius: 4px;
}

.use-function-btn {
  display: inline-flex;
  align-items: center;
  color: #ba003f;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.use-function-btn i {
  margin-left: 4px;
  transition: transform 0.2s ease;
}

.use-function-btn:hover {
  color: #d4185b;
}

.use-function-btn:hover i {
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .ai-functions-grid {
    grid-template-columns: 1fr;
  }
  
  .position-header h1 {
    font-size: 28px;
  }
  
  .detail-card {
    padding: 20px;
  }
}
</style> 