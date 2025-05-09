<template>
  <div class="case-studies-list">
    <div class="cases-container">
      <!-- 市场营销案例卡片 -->
      <div class="case-card" @click="navigateToCase('marketing')">
        <div class="case-banner">
          <img src="@/assets/images/case-studies/marketing-case-bg.jpeg" alt="营销案例">
          <div class="case-tag">市场营销</div>
        </div>
        <div class="case-content">
          <h2 class="case-title">AI市场营销综合应用案例：某汽森林「0糖」新品上市战</h2>
          <p class="case-description">
            本案例详细展示了某知名饮料品牌如何运用AI技术进行新产品上市营销策划，包含市场分析、目标用户洞察、
            竞品分析、创意策略制定、多渠道投放与效果评估的全流程，实现品牌声量提升和销量突破。
          </p>
          <div class="case-footer">
            <div class="case-tags">
              <span>大语言模型</span>
              <span>市场分析</span>
              <span>用户洞察</span>
              <span>创意营销</span>
            </div>
            <div class="read-more">
              查看详情 <i class="ri-arrow-right-line"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- 零售案例卡片 -->
      <div class="case-card coming-soon">
        <div class="case-banner">
          <img src="@/assets/images/case-studies/retail-case-bg.jpeg" alt="零售案例">
          <div class="case-tag">零售行业</div>
          <div class="coming-soon-label">即将推出</div>
        </div>
        <div class="case-content">
          <h2 class="case-title">AI驱动的全渠道零售转型：某国际快消品牌的数字化之旅</h2>
          <p class="case-description">
            本案例将详细展示某国际快消品牌如何利用人工智能技术重塑其零售体验，从智能供应链管理到
            个性化推荐系统，全面提升用户体验与运营效率。
          </p>
          <div class="case-footer">
            <div class="case-tags">
              <span>智能推荐</span>
              <span>需求预测</span>
              <span>用户画像</span>
              <span>全渠道零售</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 金融案例卡片 -->
      <div class="case-card coming-soon">
        <div class="case-banner">
          <img src="@/assets/images/case-studies/finance-case-bg.jpeg" alt="金融案例">
          <div class="case-tag">金融科技</div>
          <div class="coming-soon-label">即将推出</div>
        </div>
        <div class="case-content">
          <h2 class="case-title">AI辅助投资决策：某头部基金的智能资产配置实践</h2>
          <p class="case-description">
            本案例将展示某头部基金如何将大语言模型与传统金融模型结合，构建智能投资决策支持系统，
            提升投资效率与风险管理能力。
          </p>
          <div class="case-footer">
            <div class="case-tags">
              <span>金融大模型</span>
              <span>风险评估</span>
              <span>资产配置</span>
              <span>量化分析</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 物流行业案例卡片（新增） -->
      <div class="case-card coming-soon">
        <div class="case-banner">
          <img src="@/assets/images/case-studies/logistics-case-bg.jpeg" alt="物流案例">
          <div class="case-tag">物流行业</div>
          <div class="coming-soon-label">即将推出</div>
        </div>
        <div class="case-content">
          <h2 class="case-title">AI赋能智慧物流：某电商平台的供应链优化实践</h2>
          <p class="case-description">
            本案例将展示某领先电商平台如何利用人工智能技术优化其物流供应链网络，
            包括智能路径规划、库存预测、无人仓储系统与最后一公里配送的创新解决方案。
          </p>
          <div class="case-footer">
            <div class="case-tags">
              <span>路径优化</span>
              <span>需求预测</span>
              <span>智能调度</span>
              <span>无人仓储</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 旅游行业案例卡片（新增） -->
      <div class="case-card coming-soon">
        <div class="case-banner">
          <img src="@/assets/images/case-studies/tourism-case-bg.jpeg" alt="旅游案例">
          <div class="case-tag">旅游行业</div>
          <div class="coming-soon-label">即将推出</div>
        </div>
        <div class="case-content">
          <h2 class="case-title">AI驱动的文旅体验革新：某景区的数字化转型之路</h2>
          <p class="case-description">
            本案例将展示某知名景区如何运用AI技术打造沉浸式文化体验，通过个性化推荐、智能导览、
            数字孪生与AR/VR技术，为游客提供全新的旅游体验，同时实现景区精细化运营。
          </p>
          <div class="case-footer">
            <div class="case-tags">
              <span>智能导览</span>
              <span>沉浸体验</span>
              <span>文化传承</span>
              <span>数字营销</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 冰雪行业案例卡片（新增） -->
      <div class="case-card coming-soon">
        <div class="case-banner">
          <img src="@/assets/images/case-studies/winter-sports-case-bg.jpeg" alt="冰雪行业案例">
          <div class="case-tag">冰雪行业</div>
          <div class="coming-soon-label">即将推出</div>
        </div>
        <div class="case-content">
          <h2 class="case-title">AI助力冰雪产业发展：某滑雪场的智慧运营实践</h2>
          <p class="case-description">
            本案例将展示某知名滑雪场如何运用人工智能技术优化场地管理、客流预测与安全保障，
            同时通过智能教练系统与个性化体验设计，提升游客满意度与运营效率。
          </p>
          <div class="case-footer">
            <div class="case-tags">
              <span>智能场景</span>
              <span>安全管理</span>
              <span>个性化教学</span>
              <span>体验设计</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';

export default {
  name: 'CaseStudiesList',
  setup() {
    const router = useRouter();

    const navigateToCase = (caseId) => {
      router.push(`/ai-case-studies/${caseId}`);
    };

    return {
      navigateToCase
    };
  }
};
</script>

<style scoped>
.case-studies-list {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.cases-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  box-sizing: border-box;
}

.case-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  justify-content: space-between;
}

.case-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}

.case-banner {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.case-banner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.case-card:hover .case-banner img {
  transform: scale(1.05);
}

.case-tag {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(186, 0, 63, 0.9);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  z-index: 2;
}

.case-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.case-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.4;
}

.case-description {
  color: #555;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.case-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.case-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.case-tags span {
  background: #f5f5f5;
  color: #666;
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 12px;
}

.read-more {
  color: #ba003f;
  font-weight: 500;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}

.read-more:hover {
  color: #d4185b;
}

/* 即将推出样式 */
.coming-soon {
  opacity: 0.6;
  pointer-events: none;
  position: relative;
  filter: grayscale(70%);
}

.coming-soon-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-15deg);
  background-color: rgba(186, 0, 63, 0.9);
  color: white;
  font-weight: bold;
  padding: 8px 20px;
  font-size: 18px;
  border-radius: 4px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 3;
}

/* 响应式调整 */
@media (max-width: 1600px) {
  .cases-container {
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
  }
  
  .case-banner {
    height: 170px;
  }
  
  .case-tag {
    padding: 5px 10px;
    font-size: 13px;
  }
}

@media (max-width: 1440px) {
  .cases-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
  }
  
  .case-banner {
    height: 180px;
  }
  
  .case-title {
    font-size: 17px;
  }
}

@media (max-width: 1200px) {
  .cases-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
  }
  
  .case-title {
    font-size: 17px;
  }
  
  .case-banner {
    height: 190px;
  }
}

@media (max-width: 992px) {
  .cases-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .case-studies-list {
    padding: 16px;
  }
  
  .case-banner {
    height: 170px;
  }
  
  .case-content {
    padding: 18px;
  }
}

@media (max-width: 768px) {
  .cases-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .case-studies-list {
    padding: 15px;
  }
  
  .case-banner {
    height: 200px;
  }
  
  .case-title {
    font-size: 18px;
  }
  
  .case-description {
    font-size: 14px;
    -webkit-line-clamp: 3;
  }
}

@media (max-width: 480px) {
  .case-banner {
    height: 160px;
  }
  
  .case-content {
    padding: 18px;
  }
  
  .case-title {
    font-size: 17px;
  }
  
  .case-studies-list {
    padding: 12px;
  }
}
</style> 