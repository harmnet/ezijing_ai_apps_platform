<template>
  <div class="scenarios-container">
    <div class="page-header">
      <h1>企业常见职务一览</h1>
      <p class="description">以下职务按业务类别进行分组，帮助您快速了解不同岗位在日常工作中可以应用的AI功能场景。点击浏览感兴趣的职务，探索专属该岗位的智能化解决方案，提升工作效率。</p>
    </div>
    
    <!-- 市场与营销 - 新的左右布局 -->
    <div class="category-section category-marketing">
      <div class="category-image">
        <img :src="backgroundImages.marketing" alt="市场与营销" />
        <h2 class="category-title">01. 市场与营销</h2>
      </div>
      <div class="category-content">
        <div class="job-positions-list">
          <div class="position-card" @click="navigateTo('/ai-scenarios/sales-manager')">
            <h3>销售经理</h3>
            <p>负责制定销售策略、管理销售团队、开拓客户市场、达成销售目标，是企业与客户之间的关键桥梁。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/marketing-manager')">
            <h3>市场经理</h3>
            <p>负责市场调研分析、品牌推广、营销策略制定与执行，提升品牌影响力和市场份额。</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 供应链与物流 -->
    <div class="category-section category-supply-chain">
      <div class="category-image">
        <img :src="backgroundImages.supplyChain" alt="供应链与物流" />
        <h2 class="category-title">02. 供应链与物流</h2>
      </div>
      <div class="category-content">
        <div class="job-positions-list">
          <div class="position-card" @click="navigateTo('/ai-scenarios/purchasing-manager')">
            <h3>采购经理</h3>
            <p>负责供应商管理、采购策略制定、成本控制与谈判，确保原材料和产品的质量与供应稳定性。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/logistics-manager')">
            <h3>物流经理</h3>
            <p>负责物流网络规划、运输管理、配送效率优化，确保产品按时安全地送达客户手中。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/inventory-specialist')">
            <h3>库存管理专员</h3>
            <p>负责库存水平监控、仓储空间优化、库存周转率提升，平衡库存成本与供应需求。</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 产品与研发 -->
    <div class="category-section category-product-development">
      <div class="category-image">
        <img :src="backgroundImages.productDev" alt="产品与研发" />
        <h2 class="category-title">03. 产品与研发</h2>
      </div>
      <div class="category-content">
        <div class="job-positions-list">
          <div class="position-card" @click="navigateTo('/ai-scenarios/product-manager')">
            <h3>产品经理</h3>
            <p>负责产品规划、需求管理、功能设计和产品迭代，是连接市场、用户与技术团队的核心角色。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/brand-visual-design')">
            <h3>产品需求分析与规划</h3>
            <p>负责产品需求的收集、分析、整理和规划，确保产品功能满足市场和用户的需求，指导产品开发方向。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/requirements-engineer')">
            <h3>需求工程师</h3>
            <p>专注于需求收集、分析、整理和管理，确保产品功能符合用户期望和业务目标。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/development-engineer')">
            <h3>研发工程师</h3>
            <p>负责产品技术实现、架构设计、代码开发，将产品需求转化为可用的功能和系统。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/test-engineer')">
            <h3>测试工程师</h3>
            <p>负责产品质量保障、测试用例设计、缺陷管理，确保产品稳定性和用户体验。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/ui-design-engineer')">
            <h3>UI设计工程师</h3>
            <p>负责用户界面视觉设计、交互体验优化，创造美观易用的产品界面。</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 财务与风控 -->
    <div class="category-section category-finance">
      <div class="category-image">
        <img :src="backgroundImages.financeRisk" alt="财务与风控" />
        <h2 class="category-title">04. 财务与风控</h2>
      </div>
      <div class="category-content">
        <div class="job-positions-list">
          <div class="position-card" @click="navigateTo('/ai-scenarios/finance-manager')">
            <h3>财务经理</h3>
            <p>负责公司财务规划、财务分析与决策支持，确保企业财务管理符合规范与要求。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/internal-auditor')">
            <h3>内部审计师</h3>
            <p>负责内控评估、流程审计、风险监控，发现流程漏洞并提出改进建议，保障企业合规运营。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/legal-compliance-manager')">
            <h3>法务合规经理</h3>
            <p>负责法律风险防范、合同审核、争议处理，确保企业经营活动符合法律法规要求。</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 行政与管理 -->
    <div class="category-section category-admin">
      <div class="category-image">
        <img :src="backgroundImages.adminMgmt" alt="行政与管理" />
        <h2 class="category-title">05. 行政与管理</h2>
      </div>
      <div class="category-content">
        <div class="job-positions-list">
          <div class="position-card" @click="navigateTo('/ai-scenarios/admin-specialist')">
            <h3>行政专员</h3>
            <p>负责办公环境管理、行政事务协调、会议安排，为企业日常运营提供基础支持服务。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/recruitment-manager')">
            <h3>人才招聘经理</h3>
            <p>负责招聘流程设计、人才筛选、面试组织，为企业引进合适的人才资源。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/talent-development-specialist')">
            <h3>人才发展专员</h3>
            <p>负责员工培训、职业发展规划、绩效管理，提升员工能力和企业人才竞争力。</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 客户与运营 -->
    <div class="category-section category-customer">
      <div class="category-image">
        <img :src="backgroundImages.customerOps" alt="客户与运营" />
        <h2 class="category-title">06. 客户与运营</h2>
      </div>
      <div class="category-content">
        <div class="job-positions-list">
          <div class="position-card" @click="navigateTo('/ai-scenarios/after-sales-engineer')">
            <h3>售后服务工程师</h3>
            <p>负责产品售后支持、问题诊断与处理、用户培训，确保客户使用产品时获得良好体验。</p>
          </div>
          
          <div class="position-card" @click="navigateTo('/ai-scenarios/customer-manager')">
            <h3>客户主管</h3>
            <p>负责客户关系维护、需求挖掘、满意度提升，是企业与核心客户之间的直接联系人。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import marketingBgImage from '@/assets/images/types/marketing-type-bg.jpg';
import supplyChainBgImage from '@/assets/images/types/supply-chain-type-bg.jpg';
import productDevBgImage from '@/assets/images/types/product-dev-type-bg.jpg';
import financeRiskBgImage from '@/assets/images/types/finance-risk-type-bg.jpg';
import adminMgmtBgImage from '@/assets/images/types/admin-mgmt-type-bg.jpg';
import customerOpsBgImage from '@/assets/images/types/customer-ops-type-bg.jpg';

export default {
  name: 'ScenariosList',
  data() {
    return {
      isFinanceManagerActive: true,
      backgroundImages: {
        marketing: marketingBgImage,
        supplyChain: supplyChainBgImage,
        productDev: productDevBgImage,
        financeRisk: financeRiskBgImage,
        adminMgmt: adminMgmtBgImage,
        customerOps: customerOpsBgImage
      }
    }
  },
  methods: {
    navigateTo(path) {
      this.$router.push(path);
    },
    goToFinanceManager() {
      this.$router.push('/ai-scenarios/finance-manager')
    },
    showComingSoon() {
      alert('法务合规经理页面正在开发中');
    }
  }
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
  padding-bottom: 0;
  border-bottom: none;
}

/* 通用类别部分样式 */
.category-section {
  margin-bottom: 48px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  background-color: #fff;
}

.category-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

/* 各类别的左右布局 */
.category-marketing,
.category-supply-chain,
.category-product-development,
.category-finance,
.category-admin,
.category-customer {
  display: flex;
  min-height: 300px;
}

.category-image {
  width: 40%;
  position: relative;
  overflow: hidden;
}

.category-image::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4); /* 灰色蒙版 */
  z-index: 1;
}

.category-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
}

.category-image .category-title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 32px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  margin: 0;
  z-index: 2;
  text-align: center;
  width: 100%;
}

.category-content {
  width: 60%;
  padding: 30px;
}

/* 职务列表样式 */
.job-positions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 职务卡片样式 */
.job-positions-list .position-card {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.job-positions-list .position-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* 按类别设置职务卡片的边框颜色 */
.category-marketing .position-card {
  border-left: 4px solid #e83e8c;
}

.category-supply-chain .position-card {
  border-left: 4px solid #6610f2;
}

.category-product-development .position-card {
  border-left: 4px solid #28a745;
}

.category-finance .position-card {
  border-left: 4px solid #fd7e14;
}

.category-admin .position-card {
  border-left: 4px solid #17a2b8;
}

.category-customer .position-card {
  border-left: 4px solid #ba003f;
}

/* 职务名称样式 */
.job-positions-list .position-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
  padding-right: 24px;
  min-width: 100px;
  width: 30%;
  white-space: nowrap;
}

/* 按类别设置职务名称右侧分隔线颜色 */
.category-marketing .position-card h3 {
  border-right: 1px solid rgba(232, 62, 140, 0.3);
}

.category-supply-chain .position-card h3 {
  border-right: 1px solid rgba(102, 16, 242, 0.3);
}

.category-product-development .position-card h3 {
  border-right: 1px solid rgba(40, 167, 69, 0.3);
}

.category-finance .position-card h3 {
  border-right: 1px solid rgba(253, 126, 20, 0.3);
}

.category-admin .position-card h3 {
  border-right: 1px solid rgba(23, 162, 184, 0.3);
}

.category-customer .position-card h3 {
  border-right: 1px solid rgba(186, 0, 63, 0.3);
}

/* 职务描述样式 */
.job-positions-list .position-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 0;
  padding-left: 24px;
  flex: 1;
}

/* 其他类别的原有样式 */
.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 30px 30px 0 30px;
}

.category-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
  position: relative;
}

.category-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.category-icon i {
  font-size: 30px;
}

.job-positions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  padding: 0 30px 30px 30px;
}

.position-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  border-left: 4px solid #ba003f;
}

.position-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.position-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: rgba(186, 0, 63, 0.05);
}

.position-icon i {
  font-size: 32px;
  color: #ba003f;
}

.position-content {
  padding: 20px;
  flex: 1;
}

.position-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.position-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

/* 旧类别样式 */
.category-customer {
  border-top: 4px solid #ba003f;
}

.category-customer .category-icon {
  background-color: #ba003f;
  color: white;
}

/* 根据类别为职位卡片添加不同的边框颜色 */
.category-supply-chain .position-card {
  border-left-color: #6610f2;
}

.category-supply-chain .position-icon {
  background-color: rgba(102, 16, 242, 0.05);
}

.category-supply-chain .position-icon i {
  color: #6610f2;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .category-marketing,
  .category-supply-chain,
  .category-product-development,
  .category-finance,
  .category-admin,
  .category-customer {
    flex-direction: column;
  }
  
  .category-image, 
  .category-content {
    width: 100%;
  }
  
  .category-image {
    height: 200px;
  }
  
  .job-positions-grid {
    grid-template-columns: 1fr;
  }
  
  .category-section {
    padding: 0;
  }
}
</style> 