<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>采购经理 <span class="position-category">供应链与物流类</span></h1>
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
              <li>制定采购策略和采购计划，确保物资供应满足公司需求</li>
              <li>管理供应商关系，评估和筛选合格供应商</li>
              <li>进行供应商谈判，获取最优的采购条件和价格</li>
              <li>优化采购流程，降低采购成本，提高采购效率</li>
              <li>监控市场动态，分析原材料价格趋势和供应风险</li>
              <li>协调生产、库存和采购计划，确保生产连续性</li>
              <li>参与制定和实施采购预算，控制采购支出</li>
              <li>处理采购合同和文档，确保采购过程合规</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>优秀的谈判和沟通能力，能够与供应商建立良好的合作关系</li>
              <li>扎实的成本分析能力，能够评估总体拥有成本</li>
              <li>较强的数据分析能力，能够基于数据作出采购决策</li>
              <li>良好的合同管理和风险评估能力</li>
              <li>项目管理能力，能够同时处理多个采购项目</li>
              <li>熟悉供应链管理和ERP系统</li>
              <li>对相关行业的市场和供应链有深入了解</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>采购经理需要与多个部门和角色密切合作：</p>
            <ul>
              <li><strong>生产部门</strong>：了解生产需求和计划，确保物料及时供应</li>
              <li><strong>仓储物流</strong>：协调物料入库和库存管理</li>
              <li><strong>品质部门</strong>：确保采购物料符合质量标准</li>
              <li><strong>财务部门</strong>：处理采购预算、付款和成本控制</li>
              <li><strong>研发部门</strong>：参与新产品的材料选型和成本优化</li>
              <li><strong>供应商</strong>：维护供应商关系，进行价格谈判和合约管理</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>采购经理的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>高级采购经理</li>
              <li>采购总监</li>
              <li>供应链总监</li>
              <li>运营总监</li>
              <li>首席采购官(CPO)</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于采购经理的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 合同检查 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-search-line"></i>
            </div>
            <div class="function-content">
              <h3>合同检查</h3>
              <p>快速审核采购合同条款，识别潜在风险点，确保合同条款有利于企业。</p>
              <div class="function-tags">
                <span class="tag">合同</span>
                <span class="tag">风险控制</span>
              </div>
              <router-link to="/ai-office/legal/contract-check" class="use-function-btn">
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
              <p>分析采购数据趋势，评估供应商表现，优化采购决策和成本控制。</p>
              <div class="function-tags">
                <span class="tag">数据</span>
                <span class="tag">分析</span>
              </div>
              <router-link to="/ai-office/data-analysis" class="use-function-btn">
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
              <p>快速总结供应商资料、市场报告、产品规格等长篇文档的核心内容。</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">信息提取</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
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
              <p>自动整理供应商会议和谈判记录，提取关键信息和后续行动项。</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">供应商管理</span>
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
              <p>快速生成专业的采购报告和供应商分析PPT，用于内部汇报和决策支持。</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">报告</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
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
              <p>检查并修正采购规范、询价单和供应商沟通文档中的错误，提高专业性。</p>
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
  name: 'PurchasingManager',
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