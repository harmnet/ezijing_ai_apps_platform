<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>售后服务工程师 <span class="position-category">客户与运营类</span></h1>
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
              <li>为客户提供产品售后技术支持和问题解决方案</li>
              <li>响应和处理客户的技术咨询和故障报修</li>
              <li>进行产品故障诊断、分析和维修</li>
              <li>编写并更新产品使用手册和故障排除指南</li>
              <li>为客户提供产品使用培训和技术指导</li>
              <li>收集客户反馈，协助产品改进和升级</li>
              <li>维护客户关系，提升客户满意度和忠诚度</li>
              <li>与研发、生产等部门协作，解决产品质量和设计问题</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>相关专业背景，对公司产品有深入理解</li>
              <li>出色的问题诊断和解决能力</li>
              <li>良好的沟通能力和客户服务意识</li>
              <li>较强的技术文档编写能力</li>
              <li>团队协作精神和抗压能力</li>
              <li>善于倾听和理解客户需求</li>
              <li>熟练使用相关技术工具和测试设备</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>售后服务工程师需要与多个部门和角色密切合作：</p>
            <ul>
              <li><strong>客户</strong>：直接与客户沟通，了解问题并提供解决方案</li>
              <li><strong>研发部门</strong>：反馈产品问题，协助产品改进</li>
              <li><strong>质量部门</strong>：分析产品缺陷，提高产品质量</li>
              <li><strong>销售部门</strong>：协助解决客户售后问题，提升客户满意度</li>
              <li><strong>客户服务部门</strong>：共同维护客户关系</li>
              <li><strong>培训部门</strong>：提供产品技术培训材料和支持</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>售后服务工程师的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>高级售后服务工程师</li>
              <li>售后服务主管/经理</li>
              <li>客户服务总监</li>
              <li>技术支持专家</li>
              <li>产品经理</li>
              <li>客户成功经理</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于售后服务工程师的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 文档总结 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>文档总结</h3>
              <p>快速总结客户反馈和故障报告，提取关键信息，形成问题摘要</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">摘要</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文章润色 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-edit-line"></i>
            </div>
            <div class="function-content">
              <h3>文章润色</h3>
              <p>优化用户手册和技术文档，使其更加清晰易懂，提升用户体验</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">优化</span>
              </div>
              <router-link to="/text-creation/revision/refinement" class="use-function-btn">
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
              <p>生成产品手册、技术支持文档和故障排除指南的专业结构</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">结构</span>
              </div>
              <router-link to="/text-creation/copywriting/document-structure" class="use-function-btn">
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
              <p>撰写详细的产品使用指南和常见问题解决方案文档</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">创作</span>
              </div>
              <router-link to="/text-creation/copywriting/longform" class="use-function-btn">
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
              <p>自动记录客户沟通和内部技术会议内容，提取关键决策和行动项</p>
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
              <p>快速生成产品培训和技术支持演示文稿，提升培训效果</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">培训</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
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
  name: 'AfterSalesEngineer',
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