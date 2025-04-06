<template>
  <div class="scenarios-container">
    <div class="page-header">
      <h1>AI应用典型场景</h1>
      <p class="description">根据不同的业务角色和场景，我们提供了一系列AI应用示例，帮助您更好地理解如何在实际工作中应用AI技术。</p>
    </div>
    
    <div class="scenarios-grid">
      <!-- HR场景 -->
      <div class="scenario-card">
        <div class="scenario-icon">
          <i class="ri-user-search-line"></i>
        </div>
        <div class="scenario-content">
          <h3>HR常见业务场景</h3>
          <p>包括招聘筛选、员工培训、绩效评估、人才发展等HR工作中的AI应用场景。</p>
          <router-link to="/ai-scenarios/hr" class="view-btn">查看场景 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- 产品营销场景 -->
      <div class="scenario-card">
        <div class="scenario-icon">
          <i class="ri-advertisement-line"></i>
        </div>
        <div class="scenario-content">
          <h3>产品营销常见业务场景</h3>
          <p>包括内容创作、市场调研、活动策划、品牌推广等产品营销工作中的AI应用场景。</p>
          <router-link to="/ai-scenarios/marketing" class="view-btn">查看场景 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- 企业行政场景 -->
      <div class="scenario-card">
        <div class="scenario-icon">
          <i class="ri-building-line"></i>
        </div>
        <div class="scenario-content">
          <h3>企业行政常见业务场景</h3>
          <p>包括文档管理、会议安排、资源协调、流程优化等企业行政工作中的AI应用场景。</p>
          <router-link to="/ai-scenarios/admin" class="view-btn">查看场景 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- 市场运营场景 -->
      <div class="scenario-card">
        <div class="scenario-icon">
          <i class="ri-line-chart-line"></i>
        </div>
        <div class="scenario-content">
          <h3>市场运营常见业务场景</h3>
          <p>包括数据分析、用户运营、渠道管理、增长策略等市场运营工作中的AI应用场景。</p>
          <router-link to="/ai-scenarios/operation" class="view-btn">查看场景 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- 产品研发场景 -->
      <div class="scenario-card">
        <div class="scenario-icon">
          <i class="ri-code-box-line"></i>
        </div>
        <div class="scenario-content">
          <h3>产品研发常见业务场景</h3>
          <p>包括需求分析、产品设计、代码生成、测试优化等产品研发工作中的AI应用场景。</p>
          <router-link to="/ai-scenarios/product" class="view-btn">查看场景 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScenariosList'
}
</script>

<style scoped>
.scenarios-container {
  max-width: 1200px;
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
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.scenario-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  border-left: 4px solid #ba003f;
}

.scenario-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.scenario-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: rgba(186, 0, 63, 0.05);
}

.scenario-icon i {
  font-size: 32px;
  color: #ba003f;
}

.scenario-content {
  padding: 20px;
  flex: 1;
}

.scenario-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.scenario-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.view-btn {
  display: inline-flex;
  align-items: center;
  color: #ba003f;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.view-btn i {
  margin-left: 4px;
  transition: transform 0.2s ease;
}

.view-btn:hover {
  color: #d4185b;
}

.view-btn:hover i {
  transform: translateX(4px);
}
</style> 