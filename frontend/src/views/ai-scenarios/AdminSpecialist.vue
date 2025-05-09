<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>行政专员 <span class="position-category">行政与管理类</span></h1>
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
              <li>负责公司日常行政事务的管理和协调</li>
              <li>组织安排公司会议、活动、接待等工作</li>
              <li>管理和维护办公环境，协调办公设备采购和维修</li>
              <li>负责公司文件的收发、整理、归档和管理</li>
              <li>协助处理员工福利、工作餐、办公用品等后勤保障工作</li>
              <li>负责与物业、安保等外部服务机构的沟通和协调</li>
              <li>支持其他部门的行政需求，确保公司运营的顺畅</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>大专及以上学历，行政管理、人力资源或相关专业优先</li>
              <li>2年以上行政工作经验，熟悉办公室行政管理流程</li>
              <li>熟练操作办公软件，包括Word、Excel、PowerPoint等</li>
              <li>良好的沟通协调能力和团队合作精神</li>
              <li>细致耐心，有较强的责任心和服务意识</li>
              <li>工作条理清晰，有良好的时间管理和组织能力</li>
              <li>具备基本的财务知识，能处理日常报销等工作</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>行政专员需要熟练使用多种工具和系统：</p>
            <ul>
              <li><strong>办公自动化系统</strong>：会议室预订、用车申请、办公用品管理等</li>
              <li><strong>文档管理系统</strong>：公司文件收发、存档与检索</li>
              <li><strong>行政管理工具</strong>：考勤系统、访客管理、门禁管理</li>
              <li><strong>费用报销系统</strong>：日常报销、预算管理、费用统计</li>
              <li><strong>沟通协作工具</strong>：邮件系统、即时通讯、会议安排</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>与其他岗位的协作</h3>
            <p>行政专员需要与公司多个角色密切合作：</p>
            <ul>
              <li><strong>人力资源部门</strong>：协作处理员工入职、离职手续和福利管理</li>
              <li><strong>财务部门</strong>：配合处理日常报销、费用管理和预算执行</li>
              <li><strong>各业务部门</strong>：支持会议组织、活动策划和后勤保障</li>
              <li><strong>公司管理层</strong>：协助安排行程、准备会议材料和文件管理</li>
              <li><strong>外部服务商</strong>：管理与物业、餐饮、办公设备等供应商的关系</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>行政专员的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>行政专员 → 高级行政专员 → 行政主管 → 行政经理</li>
              <li>行政专员 → 办公室主任 → 行政总监</li>
              <li>行政专员 → 行政助理 → 总裁助理/总经理助理</li>
              <li>行政专员 → 人事行政专员 → 人力资源专员</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于行政专员的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- AI会议纪要 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-text-line"></i>
            </div>
            <div class="function-content">
              <h3>AI会议纪要</h3>
              <p>自动记录会议内容，生成结构化会议记录与决策要点，提高会议效率</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">记录</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- AI PPT创作 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-slideshow-line"></i>
            </div>
            <div class="function-content">
              <h3>AI PPT创作</h3>
              <p>快速生成公司会议、培训、活动等场合所需的专业PPT，节省制作时间</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">制作</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
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
              <p>辅助创建公司规章制度、工作流程、行政通知等规范化文档</p>
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
              <p>快速总结会议纪要、工作报告等长文档，提取关键信息，提高阅读效率</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">摘要</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
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
              <p>AI辅助审核办公场所租赁、设备采购等合同，标识潜在风险点</p>
              <div class="function-tags">
                <span class="tag">合同</span>
                <span class="tag">审核</span>
              </div>
              <router-link to="/ai-office/legal/contract-check" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 招聘JD生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-user-search-line"></i>
            </div>
            <div class="function-content">
              <h3>招聘JD生成</h3>
              <p>协助人力资源部门快速创建专业的职位描述，提高招聘效率</p>
              <div class="function-tags">
                <span class="tag">招聘</span>
                <span class="tag">人事</span>
              </div>
              <router-link to="/ai-office/jd-maker" class="use-function-btn">
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
  name: 'AdminSpecialist',
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