<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>产品经理 <span class="position-category">产品与研发类</span></h1>
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
              <li>负责产品的全生命周期管理，包括规划、设计、开发和迭代</li>
              <li>收集和分析用户需求，转化为产品功能和规格说明</li>
              <li>制定产品路线图和发展策略，确保产品与公司战略一致</li>
              <li>撰写详细的产品需求文档（PRD）和用户故事</li>
              <li>与设计、开发和测试团队紧密合作，确保产品按计划交付</li>
              <li>分析用户数据和市场反馈，持续优化产品体验</li>
              <li>跟踪竞品动态，分析竞争优势与劣势</li>
              <li>协调跨部门资源，推动产品目标达成</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>优秀的产品思维和用户同理心，能够理解并满足用户潜在需求</li>
              <li>出色的沟通和表达能力，能够清晰地传达产品愿景和需求</li>
              <li>扎实的分析能力，能够基于数据做出合理的决策</li>
              <li>良好的项目管理能力，能够协调多方资源推进项目</li>
              <li>较强的抗压能力和问题解决能力，能够处理产品开发中的各种挑战</li>
              <li>熟悉产品设计和开发流程，了解基础技术原理</li>
              <li>掌握常用的产品管理工具和方法论</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>产品经理需要与多个部门和角色密切合作：</p>
            <ul>
              <li><strong>用户研究团队</strong>：获取用户洞察和需求验证</li>
              <li><strong>UI/UX设计团队</strong>：协作设计产品界面和用户体验</li>
              <li><strong>研发团队</strong>：沟通技术实现和功能开发</li>
              <li><strong>测试团队</strong>：确保产品质量和稳定性</li>
              <li><strong>市场营销团队</strong>：配合产品推广和市场策略</li>
              <li><strong>销售团队</strong>：提供产品信息支持和获取客户反馈</li>
              <li><strong>客户服务团队</strong>：了解用户问题和改进建议</li>
              <li><strong>公司管理层</strong>：汇报产品战略和发展进度</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>产品经理的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>高级产品经理</li>
              <li>产品总监</li>
              <li>产品副总裁</li>
              <li>首席产品官(CPO)</li>
              <li>创业公司创始人/联合创始人</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于产品经理的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 文档结构撰写 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>文档结构撰写</h3>
              <p>快速生成产品需求文档(PRD)、用户故事和产品规格说明的结构框架。</p>
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
              <p>快速总结市场研究报告、用户反馈和竞品分析，提取关键信息辅助决策。</p>
              <div class="function-tags">
                <span class="tag">总结</span>
                <span class="tag">信息提取</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
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
              <p>快速生成产品演示、路线图和进度汇报PPT，用于内部沟通和决策支持。</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">汇报</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
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
              <p>自动整理产品评审会、需求讨论和迭代计划会议的记录，提取关键决策和行动项。</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">协作</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
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
              <p>分析产品使用数据和市场趋势，发现用户行为模式，优化产品决策。</p>
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
              <p>通过文字描述快速生成产品原型概念图和界面设计草图，加速设计构思。</p>
              <div class="function-tags">
                <span class="tag">设计</span>
                <span class="tag">原型</span>
              </div>
              <router-link to="/image-creation/text-to-image" class="use-function-btn">
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
              <p>生成专业的产品团队招聘JD，帮助吸引合适的产品、设计和技术人才。</p>
              <div class="function-tags">
                <span class="tag">招聘</span>
                <span class="tag">团队建设</span>
              </div>
              <router-link to="/ai-office/jd-maker" class="use-function-btn">
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
              <p>检查并修正产品文档、需求说明和用户手册中的错误，提高专业性。</p>
              <div class="function-tags">
                <span class="tag">校对</span>
                <span class="tag">质量控制</span>
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
  name: 'ProductManager',
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