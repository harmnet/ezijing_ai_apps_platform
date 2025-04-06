<template>
  <div class="content">
    <router-view v-if="$route.path !== '/ai-office'"></router-view>
    <div class="category-container" v-else>
      <!-- AI PPT创作 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-slideshow-line"></i>
          <h3 class="category-title">AI PPT创作</h3>
        </div>
        <p class="category-desc">使用AI技术快速生成专业演示文稿，只需简单输入主题和大纲，即可自动生成内容丰富、逻辑清晰的PPT，大幅提升工作效率。</p>
        <div class="category-buttons">
          <router-link to="/ai-office/integration-test" class="primary-button">开始创作 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- AI会议纪要 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-file-list-line"></i>
          <h3 class="category-title">AI会议纪要</h3>
        </div>
        <p class="category-desc">利用AI技术快速整理会议内容，自动识别关键议题、行动项和决策要点，将冗长会议转化为结构化纪要，提高团队沟通效率。</p>
        <div class="category-buttons">
          <router-link to="/ai-office/meeting-minutes" class="primary-button">开始创作 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- AI合同检查 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-file-search-line"></i>
          <h3 class="category-title">AI合同检查</h3>
        </div>
        <p class="category-desc">利用AI技术智能审查合同内容，自动识别可能存在风险的条款，分析权利义务平衡性，提供专业修改建议，帮助降低合同风险。</p>
        <div class="category-buttons">
          <router-link to="/ai-office/legal/contract-check" class="primary-button">开始检查 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- AI数据分析 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-bar-chart-line"></i>
          <h3 class="category-title">AI数据分析</h3>
        </div>
        <p class="category-desc">利用AI技术智能分析各类数据，快速发现数据中的模式和趋势，生成直观的数据可视化图表，助力数据驱动决策。</p>
        <div class="category-buttons">
          <router-link to="/ai-office/data-analysis" class="primary-button">开始分析 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- AI招聘JD生成 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-file-list-3-line"></i>
          <h3 class="category-title">AI招聘JD生成</h3>
        </div>
        <p class="category-desc">利用AI技术快速生成专业的招聘职位描述，只需填写岗位基本信息，即可自动生成包含职责、要求和福利的完整JD，提高招聘效率。</p>
        <div class="category-buttons">
          <router-link to="/ai-office/jd-maker" class="primary-button">开始创建 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- AI简历优化 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-file-text-line"></i>
          <h3 class="category-title">AI简历优化</h3>
        </div>
        <p class="category-desc">利用AI技术智能优化个人简历，从结构、内容、关键词等多方面提升简历质量，增加求职成功率。只需上传简历，即可获得专业优化建议。</p>
        <div class="category-buttons">
          <router-link to="/ai-office/cv-optimize" class="primary-button">开始优化 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIOfficeSuite'
}
</script>

<style scoped>
:root {
  --zijing-red: #ba003f;
  --zijing-red-light: rgba(186, 0, 63, 0.1);
  --zijing-red-hover: #d4185b;
}

.category-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  padding: 32px;
  margin: 20px;
}

.category-section {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(186, 0, 63, 0.08);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  border-top: 4px solid #ba003f;
  min-height: 200px;
  position: relative;
  overflow: hidden;
}

.category-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: linear-gradient(180deg, rgba(186, 0, 63, 0.03) 0%, rgba(186, 0, 63, 0) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.category-section:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 36px rgba(186, 0, 63, 0.12);
}

.category-section:hover::before {
  opacity: 1;
}

.category-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.category-header i {
  font-size: 28px;
  color: var(--zijing-red, #ba003f);
  margin-right: 16px;
}

.category-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.category-desc {
  color: #666;
  margin-bottom: 24px;
  line-height: 1.6;
  flex-grow: 1;
}

.category-buttons {
  margin-top: auto;
  display: flex;
  gap: 12px;
}

.primary-button {
  display: inline-flex;
  align-items: center;
  color: #fff;
  background-color: var(--zijing-red, #ba003f);
  padding: 10px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
}

.primary-button:hover {
  background-color: var(--zijing-red-hover, #d4185b);
}

.secondary-button {
  display: inline-flex;
  align-items: center;
  color: var(--zijing-red, #ba003f);
  background-color: rgba(186, 0, 63, 0.1);
  padding: 10px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
}

.secondary-button:hover {
  background-color: rgba(186, 0, 63, 0.2);
}

.primary-button i, .secondary-button i {
  margin-left: 8px;
  font-size: 16px;
}

.coming-soon {
  background-color: #f0f0f0 !important;
  color: #999 !important;
  cursor: not-allowed;
}

.coming-soon:hover {
  background-color: #f0f0f0 !important;
}

@media (max-width: 1200px) {
  .category-container {
    grid-template-columns: 1fr;
  }
  
  .category-buttons {
    flex-direction: column;
  }
}
</style> 