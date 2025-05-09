<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>研发工程师 <span class="position-category">产品与研发类</span></h1>
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
              <li>根据产品需求文档进行技术方案设计与实现</li>
              <li>编写高质量、可维护的代码，完成功能开发和性能优化</li>
              <li>解决开发过程中的技术难题，确保项目按时交付</li>
              <li>与产品、测试等团队协作，确保产品质量</li>
              <li>参与代码审查，不断优化代码结构和质量</li>
              <li>持续关注并实践最新的技术和开发方法</li>
              <li>编写技术文档，保障项目的可维护性</li>
              <li>排查和修复系统中的线上问题和缺陷</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>扎实的计算机科学基础知识，包括数据结构、算法和操作系统</li>
              <li>精通至少一种主流编程语言（如Java、Python、C++、JavaScript等）</li>
              <li>熟悉常用的开发框架和工具，有实际项目经验</li>
              <li>具备良好的代码编写习惯和代码风格</li>
              <li>具有较强的问题分析和解决能力</li>
              <li>熟悉软件开发生命周期和敏捷开发方法</li>
              <li>良好的沟通能力和团队协作精神</li>
              <li>自我驱动的学习能力，能够快速掌握新技术</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>研发工程师需要与多个角色密切合作：</p>
            <ul>
              <li><strong>产品经理</strong>：理解产品需求，协助评估技术可行性</li>
              <li><strong>需求工程师</strong>：了解需求细节，确保技术实现符合需求规格</li>
              <li><strong>UI/UX设计师</strong>：协作实现用户界面和交互体验</li>
              <li><strong>测试工程师</strong>：协作进行测试，修复Bug</li>
              <li><strong>DevOps工程师</strong>：协作部署和运维应用系统</li>
              <li><strong>架构师</strong>：遵循架构规范，参与技术方案设计</li>
              <li><strong>技术负责人</strong>：汇报开发进度，解决技术问题</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>研发工程师的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>高级研发工程师</li>
              <li>技术专家</li>
              <li>架构师</li>
              <li>技术经理</li>
              <li>技术总监</li>
              <li>CTO（首席技术官）</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于研发工程师的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 文档结构撰写 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>文档结构撰写</h3>
              <p>快速生成技术文档框架，规范技术方案和API文档结构，提高文档质量。</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">结构化</span>
              </div>
              <router-link to="/text-creation/copywriting/document-structure" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文档总结 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-draft-line"></i>
            </div>
            <div class="function-content">
              <h3>文档总结</h3>
              <p>快速提取和总结冗长的技术文档、会议记录和需求说明的关键信息。</p>
              <div class="function-tags">
                <span class="tag">总结</span>
                <span class="tag">信息提取</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
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
              <p>检查技术文档中的拼写、语法错误，确保技术文档的准确性和专业性。</p>
              <div class="function-tags">
                <span class="tag">校对</span>
                <span class="tag">质量控制</span>
              </div>
              <router-link to="/text-creation/revision/proofreading" class="use-function-btn">
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
              <p>自动记录开发会议内容，提取关键决策和行动项，确保团队协作顺畅。</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">协作</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 长文创作 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-book-3-line"></i>
            </div>
            <div class="function-content">
              <h3>长文创作</h3>
              <p>辅助编写详细的技术方案文档、系统架构说明书和开发指南。</p>
              <div class="function-tags">
                <span class="tag">创作</span>
                <span class="tag">技术文档</span>
              </div>
              <router-link to="/text-creation/copywriting/longform" class="use-function-btn">
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
              <p>快速生成技术分享PPT、项目汇报演示文稿，提高技术交流效率。</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">汇报</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 数据分析 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-bar-chart-line"></i>
            </div>
            <div class="function-content">
              <h3>数据分析</h3>
              <p>分析系统性能数据和用户行为数据，发现优化方向，辅助技术决策。</p>
              <div class="function-tags">
                <span class="tag">数据</span>
                <span class="tag">分析</span>
              </div>
              <router-link to="/ai-office/data-analysis" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文生图 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-image-line"></i>
            </div>
            <div class="function-content">
              <h3>文生图</h3>
              <p>生成系统架构图、流程图和技术示意图，提高技术交流的直观性。</p>
              <div class="function-tags">
                <span class="tag">图表</span>
                <span class="tag">可视化</span>
              </div>
              <router-link to="/image-creation/text-to-image" class="use-function-btn">
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
  name: 'DevelopmentEngineer',
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