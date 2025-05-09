<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>人才发展专员 <span class="position-category">人力资源类</span></h1>
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
              <li>设计、开发和实施员工培训与发展项目</li>
              <li>制定员工职业发展规划和晋升路径</li>
              <li>组织领导力培训和人才梯队建设</li>
              <li>协助绩效管理体系的建立和优化</li>
              <li>进行培训需求分析和效果评估</li>
              <li>设计和实施学习发展解决方案</li>
              <li>管理内部培训资源和外部培训供应商</li>
              <li>为组织能力建设和人才保留提供专业支持</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>优秀的培训设计和授课能力</li>
              <li>出色的项目管理和组织协调能力</li>
              <li>良好的人际沟通和影响力</li>
              <li>教育学和成人学习理论知识</li>
              <li>数据分析能力，能够评估培训效果</li>
              <li>创新思维和问题解决能力</li>
              <li>熟悉学习管理系统(LMS)和在线培训工具</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>人才发展专员需要与多个部门和角色密切合作：</p>
            <ul>
              <li><strong>人力资源部门</strong>：协调招聘、绩效、薪酬等相关工作</li>
              <li><strong>业务部门</strong>：了解业务需求，定制培训方案</li>
              <li><strong>管理层</strong>：支持领导力发展，推动组织变革</li>
              <li><strong>外部培训供应商</strong>：管理培训资源和合作关系</li>
              <li><strong>员工</strong>：提供职业辅导和发展支持</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>人才发展专员的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>人才发展经理</li>
              <li>培训总监</li>
              <li>组织发展总监</li>
              <li>学习与发展负责人</li>
              <li>人力资源总监</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于人才发展专员的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 培训文档撰写 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-text-line"></i>
            </div>
            <div class="function-content">
              <h3>培训文档撰写</h3>
              <p>快速生成培训大纲、课程计划和培训手册，提高培训材料开发效率。</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">培训</span>
              </div>
              <router-link to="/ai-tools/document-writer" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 长文创作 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-article-line"></i>
            </div>
            <div class="function-content">
              <h3>长文创作</h3>
              <p>撰写培训案例、发展指南和最佳实践手册，提供全面的学习资源。</p>
              <div class="function-tags">
                <span class="tag">写作</span>
                <span class="tag">内容</span>
              </div>
              <router-link to="/ai-tools/long-form-writer" class="use-function-btn">
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
              <p>快速生成培训课件、发展规划展示和内部分享PPT。</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">培训</span>
              </div>
              <router-link to="/ai-tools/ai-ppt" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 招聘JD生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-user-line"></i>
            </div>
            <div class="function-content">
              <h3>招聘JD生成</h3>
              <p>创建内部职位描述和发展路径，帮助员工了解职业晋升要求。</p>
              <div class="function-tags">
                <span class="tag">人才</span>
                <span class="tag">职位规划</span>
              </div>
              <router-link to="/ai-tools/job-description" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- AI会议纪要 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>AI会议纪要</h3>
              <p>自动整理培训会议和绩效评估会议记录，提取关键信息。</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">记录</span>
              </div>
              <router-link to="/ai-tools/meeting-summary" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 简历优化 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-contacts-line"></i>
            </div>
            <div class="function-content">
              <h3>简历优化</h3>
              <p>帮助员工优化职业发展资料，提升内部晋升和转岗的成功率。</p>
              <div class="function-tags">
                <span class="tag">职业</span>
                <span class="tag">发展</span>
              </div>
              <router-link to="/ai-tools/resume-optimizer" class="use-function-btn">
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
  name: 'TalentDevelopmentSpecialist',
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
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
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
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 30px;
}

.detail-item {
  margin-bottom: 30px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

.detail-item p {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 15px;
}

.detail-item ul {
  padding-left: 20px;
  margin-bottom: 0;
}

.detail-item li {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 8px;
}

.detail-item li:last-child {
  margin-bottom: 0;
}

.ai-functions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.function-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 25px;
  display: flex;
  transition: transform 0.3s, box-shadow 0.3s;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.function-icon {
  width: 50px;
  height: 50px;
  background-color: #f0f5ff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.function-icon i {
  font-size: 24px;
  color: #ba003f;
}

.function-content {
  flex-grow: 1;
}

.function-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.function-content p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 12px;
}

.function-tags {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.tag {
  font-size: 12px;
  padding: 3px 8px;
  background-color: #f2f2f2;
  color: #666;
  border-radius: 4px;
  margin-right: 8px;
  margin-bottom: 8px;
}

.use-function-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #ba003f;
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.use-function-btn i {
  margin-left: 5px;
}

.use-function-btn:hover {
  background-color: #d4004a;
}

@media (max-width: 1100px) {
  .ai-functions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .ai-functions-grid {
    grid-template-columns: 1fr;
  }
  
  .position-header {
    padding: 30px 0 20px;
    margin-bottom: 30px;
  }
  
  .position-header h1 {
    font-size: 28px;
  }
  
  .section-title {
    font-size: 22px;
  }
  
  .detail-card {
    padding: 20px;
  }
}
</style> 