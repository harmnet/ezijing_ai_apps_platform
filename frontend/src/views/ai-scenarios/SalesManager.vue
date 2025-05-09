<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>销售经理 <span class="position-category">市场与营销类</span></h1>
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
              <li>制定销售策略和销售计划，确保销售目标的达成</li>
              <li>管理和培训销售团队，提升团队整体销售能力</li>
              <li>开发和维护客户关系，挖掘客户需求并提供解决方案</li>
              <li>进行市场调研和竞争分析，把握市场动向</li>
              <li>分析销售数据，制定销售预测和改进措施</li>
              <li>参与产品定价和销售方案设计</li>
              <li>与市场、产品等部门协作，确保销售活动的顺利开展</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>优秀的沟通和谈判能力，能够有效说服客户</li>
              <li>出色的团队管理和领导能力</li>
              <li>良好的数据分析能力，能够基于数据制定决策</li>
              <li>项目管理能力，能够同时处理多个销售项目</li>
              <li>解决问题的能力，能够应对销售过程中的各种挑战</li>
              <li>熟悉CRM系统和销售工具的使用</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>销售经理需要与多个部门和角色密切合作：</p>
            <ul>
              <li><strong>市场部门</strong>：协作开展营销活动，获取销售线索</li>
              <li><strong>产品部门</strong>：了解产品特性，提供市场反馈</li>
              <li><strong>客户服务</strong>：确保客户满意度和续约率</li>
              <li><strong>财务部门</strong>：处理合同、报价和收款事宜</li>
              <li><strong>高层管理</strong>：汇报销售业绩和市场动态</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>销售经理的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>区域销售总监</li>
              <li>全国销售总监</li>
              <li>商务拓展总监</li>
              <li>销售副总裁</li>
              <li>首席营收官(CRO)</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于销售经理的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 营销文案生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-text-line"></i>
            </div>
            <div class="function-content">
              <h3>营销文案生成</h3>
              <p>快速生成针对不同产品和目标客户的营销文案，提高销售转化率。</p>
              <div class="function-tags">
                <span class="tag">文案</span>
                <span class="tag">营销</span>
              </div>
              <router-link to="/text-creation/marketing/copywriting-generator" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 广告语生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-advertisement-line"></i>
            </div>
            <div class="function-content">
              <h3>广告语生成</h3>
              <p>生成吸引人的广告标语和宣传语，用于产品推广和品牌建设。</p>
              <div class="function-tags">
                <span class="tag">广告</span>
                <span class="tag">营销</span>
              </div>
              <router-link to="/text-creation/marketing/ad-slogan" class="use-function-btn">
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
              <p>快速生成专业的销售演示PPT，用于客户提案和产品展示。</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">提案</span>
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
              <p>分析销售数据趋势，发现潜在机会和问题，辅助销售决策制定。</p>
              <div class="function-tags">
                <span class="tag">数据</span>
                <span class="tag">分析</span>
              </div>
              <router-link to="/ai-office/data-analysis" class="use-function-btn">
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
              <p>自动整理客户会议记录，提取关键信息和后续行动项。</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">客户管理</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
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
              <p>快速总结市场报告、竞品分析等长篇文档的核心内容。</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">信息提取</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
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
  name: 'SalesManager',
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