<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>人才招聘经理 <span class="position-category">行政与管理类</span></h1>
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
              <li>设计并执行企业招聘策略，满足公司各部门的人才需求</li>
              <li>建立和优化招聘流程，提高招聘效率和候选人质量</li>
              <li>撰写和优化职位描述，确保准确反映岗位要求和公司文化</li>
              <li>通过多种渠道（招聘网站、社交平台、校园招聘、猎头等）寻找合适的人才</li>
              <li>筛选简历，组织和参与面试，评估候选人的专业能力和文化契合度</li>
              <li>与业务部门保持紧密沟通，了解人才需求并提供招聘进展反馈</li>
              <li>管理人才库，建立长期人才储备计划</li>
              <li>分析招聘数据，持续优化招聘策略和流程</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>人力资源、管理或相关专业学士及以上学历</li>
              <li>3年以上招聘或人力资源工作经验，熟悉招聘流程和最佳实践</li>
              <li>卓越的沟通能力和人际交往能力，善于与各层级人员有效沟通</li>
              <li>优秀的面试技巧和候选人评估能力</li>
              <li>组织协调能力强，能同时处理多个招聘需求</li>
              <li>熟悉各类招聘渠道和招聘工具的使用</li>
              <li>具备基本的数据分析能力，能利用数据指导招聘工作</li>
              <li>对行业人才市场和薪资水平有深入了解</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>人才招聘经理需要熟练使用多种工具和系统：</p>
            <ul>
              <li><strong>招聘管理系统(ATS)</strong>：简历筛选、候选人跟踪、招聘流程管理</li>
              <li><strong>人才库管理系统</strong>：人才数据存储、分类、检索</li>
              <li><strong>招聘网站与社交平台</strong>：发布职位、搜寻候选人、建立雇主品牌</li>
              <li><strong>HR信息系统</strong>：录入新员工信息、生成offer、入职流程管理</li>
              <li><strong>数据分析工具</strong>：招聘效率分析、渠道效果评估、成本分析</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>与其他岗位的协作</h3>
            <p>人才招聘经理需要与公司多个角色密切合作：</p>
            <ul>
              <li><strong>业务部门管理者</strong>：确认招聘需求、岗位要求和职责描述</li>
              <li><strong>人力资源团队</strong>：协同工作，确保招聘与其他HR流程的顺畅衔接</li>
              <li><strong>薪酬福利专员</strong>：确定合适的薪资范围和福利方案</li>
              <li><strong>行政专员</strong>：协调面试安排、办公场地和入职准备</li>
              <li><strong>法务合规经理</strong>：确保招聘过程符合劳动法规和公司政策</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>人才招聘经理的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>招聘专员 → 招聘主管 → 招聘经理 → 人才获取总监</li>
              <li>招聘经理 → 人力资源经理 → 人力资源总监 → 人力资源副总裁</li>
              <li>招聘经理 → 人才发展经理 → 组织发展总监</li>
              <li>招聘经理 → 猎头顾问 → 猎头公司合伙人</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于人才招聘经理的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 招聘JD生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>招聘JD生成</h3>
              <p>AI辅助快速创建专业、吸引人的职位描述，准确反映岗位要求和公司文化</p>
              <div class="function-tags">
                <span class="tag">招聘</span>
                <span class="tag">JD</span>
              </div>
              <router-link to="/ai-office/jd-maker" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 简历优化 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-user-line"></i>
            </div>
            <div class="function-content">
              <h3>简历优化</h3>
              <p>分析并优化简历内容，提升简历质量，帮助理解如何评估高质量简历</p>
              <div class="function-tags">
                <span class="tag">简历</span>
                <span class="tag">优化</span>
              </div>
              <router-link to="/ai-office/cv-optimize" class="use-function-btn">
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
              <p>快速创建招聘流程、面试评估标准等专业文档框架，提高工作效率</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">模板</span>
              </div>
              <router-link to="/text-creation/copywriting/document-structure" class="use-function-btn">
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
              <p>自动记录面试评估会议内容，提取关键决策要点，提高招聘团队协作效率</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">记录</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 营销文案生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-advertisement-line"></i>
            </div>
            <div class="function-content">
              <h3>营销文案生成</h3>
              <p>创建吸引人的招聘广告和社交媒体招聘文案，提升职位曝光和吸引力</p>
              <div class="function-tags">
                <span class="tag">文案</span>
                <span class="tag">招聘</span>
              </div>
              <router-link to="/text-creation/marketing/copywriting-generator" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 数据分析 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-bar-chart-box-line"></i>
            </div>
            <div class="function-content">
              <h3>数据分析</h3>
              <p>AI辅助分析招聘数据，识别招聘趋势、渠道效果和人才市场变化</p>
              <div class="function-tags">
                <span class="tag">数据</span>
                <span class="tag">分析</span>
              </div>
              <router-link to="/ai-office/data-analysis" class="use-function-btn">
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
  name: 'RecruitmentManager',
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