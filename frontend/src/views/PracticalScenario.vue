<template>
  <div class="practical-scenario-container">
    <div class="scenarios-grid">
      <!-- 场景1: 迎新晚会策划 -->
      <div class="scenario-card" @click="openScenario('brand-visual-design')">
        <div class="scenario-image">
          <img src="@/assets/images/backgrounds/welcome-party.png" alt="迎新晚会策划" />
          <div class="image-overlay">
            <h3>迎新晚会策划</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">活动策划</span>
            <span class="tag">流程设计</span>
            <span class="tag">资源协调</span>
          </div>
          <p>利用AI辅助快速生成完整的迎新晚会策划方案，包括主题创意、节目编排和资源调配计划。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-calendar-event-line"></i>
              <span>活动主题创意</span>
            </div>
            <div class="feature">
              <i class="ri-list-check-2"></i>
              <span>活动流程规划</span>
            </div>
            <div class="feature">
              <i class="ri-team-line"></i>
              <span>资源分配方案</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 场景2: 产品方案编写 -->
      <div class="scenario-card" @click="openScenario('customer-feedback')" style="cursor: pointer;">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/customer-feedback.jpeg" alt="产品方案编写" />
          <div class="image-overlay">
            <h3>产品方案编写</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">需求分析</span>
            <span class="tag">方案设计</span>
            <span class="tag">文档撰写</span>
          </div>
          <p>利用AI辅助，快速高效完成专业的产品方案文档编写，满足紧急任务需求。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-task-line"></i>
              <span>任务目标分析</span>
            </div>
            <div class="feature">
              <i class="ri-file-list-3-line"></i>
              <span>产品功能规划</span>
            </div>
            <div class="feature">
              <i class="ri-draft-line"></i>
              <span>方案文档生成</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 场景3: 市场活动策划 -->
      <div class="scenario-card" @click="openScenario('marketing-campaign')">
        <div class="scenario-image">
          <img src="@/assets/images/marketing-bg.jpg" alt="市场活动策划" />
          <div class="image-overlay">
            <h3>市场活动策划</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">任务梳理</span>
            <span class="tag">工作计划</span>
            <span class="tag">效率提升</span>
          </div>
          <p>利用AI辅助的五步流程方法，分分钟将领导模糊的需求转化为结构化执行方案。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-file-text-line"></i>
              <span>任务需求深度梳理</span>
            </div>
            <div class="feature">
              <i class="ri-mind-map"></i>
              <span>系统化任务拆解</span>
            </div>
            <div class="feature">
              <i class="ri-calendar-line"></i>
              <span>智能工作计划生成</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 场景4: 产品需求分析与规划 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/product-requirement.jpeg" alt="产品需求分析与规划" />
          <div class="image-overlay">
            <h3>产品需求分析与规划</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">文本整理</span>
            <span class="tag">思维导图</span>
            <span class="tag">文档生成</span>
          </div>
          <p>利用AI将零散的用户反馈、市场调研数据转化为结构化的产品需求文档和规划路线图，辅助产品决策。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-file-list-3-line"></i>
              <span>需求整理与分类</span>
            </div>
            <div class="feature">
              <i class="ri-mind-map"></i>
              <span>需求优先级分析</span>
            </div>
            <div class="feature">
              <i class="ri-road-map-line"></i>
              <span>产品路线图生成</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 场景5: 培训材料开发 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/training-material.jpeg" alt="培训材料开发" />
          <div class="image-overlay">
            <h3>培训材料开发</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">课程设计</span>
            <span class="tag">PPT生成</span>
            <span class="tag">教学视频</span>
          </div>
          <p>AI辅助快速开发企业内训课程，从课程大纲、PPT到培训手册，一站式生成完整培训资料包。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-book-open-line"></i>
              <span>课程内容设计</span>
            </div>
            <div class="feature">
              <i class="ri-slideshow-3-line"></i>
              <span>培训PPT生成</span>
            </div>
            <div class="feature">
              <i class="ri-video-line"></i>
              <span>视频脚本编写</span>
            </div>
          </div>
        </div>
        <div class="coming-soon-label">即将推出</div>
      </div>

      <!-- 场景6: 财务报告解读与决策支持 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/financial-report.jpeg" alt="财务报告解读与决策支持" />
          <div class="image-overlay">
            <h3>财务报告解读与决策支持</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">数据分析</span>
            <span class="tag">报告生成</span>
            <span class="tag">预测建议</span>
          </div>
          <p>AI辅助财务数据解读，自动生成财务分析报告，提供决策建议，让非财务人员也能快速理解财务状况。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-line-chart-line"></i>
              <span>财务数据可视化</span>
            </div>
            <div class="feature">
              <i class="ri-file-chart-line"></i>
              <span>财务报告摘要生成</span>
            </div>
            <div class="feature">
              <i class="ri-funds-box-line"></i>
              <span>业务决策建议</span>
            </div>
          </div>
        </div>
        <div class="coming-soon-label">即将推出</div>
      </div>

      <!-- 场景7: 研发文档撰写与管理 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/dev-documentation.jpeg" alt="研发文档撰写与管理" />
          <div class="image-overlay">
            <h3>研发文档撰写与管理</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">代码注释</span>
            <span class="tag">API文档</span>
            <span class="tag">用户手册</span>
          </div>
          <p>通过AI自动化技术文档生成流程，从代码注释到API文档再到最终用户手册，确保文档的一致性和完整性。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-code-line"></i>
              <span>代码分析与注释优化</span>
            </div>
            <div class="feature">
              <i class="ri-api-line"></i>
              <span>API接口文档生成</span>
            </div>
            <div class="feature">
              <i class="ri-file-paper-2-line"></i>
              <span>用户指南编写</span>
            </div>
          </div>
        </div>
        <div class="coming-soon-label">即将推出</div>
      </div>

      <!-- 场景8: 多语言内容本地化 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/multilingual-content.jpeg" alt="多语言内容本地化" />
          <div class="image-overlay">
            <h3>多语言内容本地化</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">翻译</span>
            <span class="tag">文化适配</span>
            <span class="tag">审校优化</span>
          </div>
          <p>AI辅助企业内容的多语言转换与文化本地化，确保营销、产品和服务内容在全球市场的准确传达。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-translate-2"></i>
              <span>专业内容翻译</span>
            </div>
            <div class="feature">
              <i class="ri-global-line"></i>
              <span>文化背景适配</span>
            </div>
            <div class="feature">
              <i class="ri-loop-left-line"></i>
              <span>多语言一致性检查</span>
            </div>
          </div>
        </div>
        <div class="coming-soon-label">即将推出</div>
      </div>

      <!-- 场景9: 品牌形象视觉设计 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/brand-design.jpeg" alt="品牌形象视觉设计" />
          <div class="image-overlay">
            <h3>品牌形象视觉设计</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">品牌设计</span>
            <span class="tag">图像生成</span>
            <span class="tag">风格指南</span>
          </div>
          <p>借助AI工具快速生成品牌视觉元素，从logo设计方案到品牌色彩搭配再到风格指南，提供丰富的创意选择。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-palette-line"></i>
              <span>品牌色彩方案</span>
            </div>
            <div class="feature">
              <i class="ri-compasses-2-line"></i>
              <span>Logo创意生成</span>
            </div>
            <div class="feature">
              <i class="ri-gallery-line"></i>
              <span>品牌视觉资产库</span>
            </div>
          </div>
        </div>
        <div class="coming-soon-label">即将推出</div>
      </div>

      <!-- 场景10: 招聘流程自动化 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/recruitment.jpeg" alt="招聘流程自动化" />
          <div class="image-overlay">
            <h3>招聘流程自动化</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">简历筛选</span>
            <span class="tag">面试问题</span>
            <span class="tag">人才评估</span>
          </div>
          <p>AI辅助人力资源团队优化招聘流程，从职位描述撰写、简历筛选到面试问题生成，提高招聘效率和质量。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-file-user-line"></i>
              <span>智能简历分析</span>
            </div>
            <div class="feature">
              <i class="ri-question-line"></i>
              <span>定制面试问题库</span>
            </div>
            <div class="feature">
              <i class="ri-user-star-line"></i>
              <span>候选人评估报告</span>
            </div>
          </div>
        </div>
        <div class="coming-soon-label">即将推出</div>
      </div>

      <!-- 场景11: 企业知识库构建与优化 -->
      <div class="scenario-card non-clickable">
        <div class="scenario-image">
          <img src="@/assets/images/scenarios/knowledge-base.jpeg" alt="企业知识库构建与优化" />
          <div class="image-overlay">
            <h3>企业知识库构建与优化</h3>
          </div>
        </div>
        <div class="scenario-content">
          <div class="scenario-tags">
            <span class="tag">知识整理</span>
            <span class="tag">智能问答</span>
            <span class="tag">内容更新</span>
          </div>
          <p>利用AI从企业各类文档中提取、整理知识点，构建结构化的企业知识库，并支持智能问答和自动内容更新。</p>
          <div class="ai-features">
            <div class="feature">
              <i class="ri-archive-drawer-line"></i>
              <span>知识点自动提取</span>
            </div>
            <div class="feature">
              <i class="ri-question-answer-line"></i>
              <span>智能问答系统</span>
            </div>
            <div class="feature">
              <i class="ri-refresh-line"></i>
              <span>内容时效性监控</span>
            </div>
          </div>
        </div>
        <div class="coming-soon-label">即将推出</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PracticalScenario',
  data() {
    return {
      loaded: false
    }
  },
  mounted() {
    // 页面加载完成后设置状态
    setTimeout(() => {
      this.loaded = true
    }, 100)
  },
  methods: {
    openScenario(scenarioType) {
      // 在新窗口中打开场景页面
      window.open(`/ai-scenarios/${scenarioType}`, '_blank');
    }
  }
}
</script>

<style scoped>
.practical-scenario-container {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 30px;
  width: 100%;
  box-sizing: border-box;
}

.scenario-card {
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scenario-card:nth-child(1),
.scenario-card:nth-child(2),
.scenario-card:nth-child(3) {
  cursor: pointer;
}

.scenario-card:nth-child(1):hover,
.scenario-card:nth-child(2):hover,
.scenario-card:nth-child(3):hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.scenario-image {
  height: 140px;
  overflow: hidden;
  position: relative;
}

.scenario-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.scenario-card:hover .scenario-image img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.75));
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px;
  transition: background-color 0.3s ease;
  text-align: center;
}

.image-overlay h3 {
  color: white;
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
  z-index: 2;
  line-height: 1.3;
  letter-spacing: 0.5px;
  padding: 0 10px;
}

.scenario-card:hover .image-overlay {
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.85));
}

.scenario-content {
  padding: 16px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.scenario-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.scenario-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}

.tag {
  background-color: #f0f0f0;
  color: #555;
  padding: 3px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
}

.tag:nth-child(3n+1) {
  background-color: #ffe8ee;
  color: #BA003F;
}

.tag:nth-child(3n+2) {
  background-color: #f0f7ff;
  color: #0066cc;
}

.tag:nth-child(3n+3) {
  background-color: #f5f0fc;
  color: #6b21a8;
}

.scenario-content p {
  font-size: 13px;
  color: #666;
  line-height: 1.5;
  margin: 10px 0 15px;
  flex-grow: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.ai-features {
  display: none;
}

.scenario-card:hover .ai-features {
  display: none;
}

.non-clickable {
  opacity: 0.7;
  pointer-events: none;
  filter: grayscale(70%);
  position: relative;
}

.non-clickable:hover {
  transform: none;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

/* 即将推出标记样式 */
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

@media (max-width: 1440px) {
  .scenarios-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }
}

@media (max-width: 1200px) {
  .scenarios-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
  }
  
  .image-overlay h3 {
    font-size: 20px;
  }
}

@media (max-width: 992px) {
  .scenarios-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .scenario-card {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .scenarios-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .scenario-card {
    max-width: 100%;
  }
  
  .image-overlay h3 {
    font-size: 18px;
  }
  
  .practical-scenario-container {
    padding: 15px;
  }
}

@media (max-width: 480px) {
  .scenarios-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .practical-scenario-container {
    padding: 12px;
  }
  
  .scenario-image {
    height: 130px;
  }
  
  .image-overlay h3 {
    font-size: 20px;
  }
}

.feature {
  display: flex;
  align-items: center;
  gap: 10px;
  visibility: hidden;
}

.feature i {
  font-size: 16px;
  color: #333;
}

.feature span {
  font-size: 13px;
  color: #333;
}
</style> 