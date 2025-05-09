<template>
  <div class="content">
    <router-view v-if="$route.path !== '/ai-office'"></router-view>
    <div v-else>
      <div class="category-container">
        <!-- 营销文案创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-advertisement-line"></i>
            <h3 class="category-title">营销文案创作</h3>
          </div>
          <p class="category-desc">快速生成各类营销文案，包括产品描述、品牌宣传、活动推广等，提升营销效果和转化率。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/marketing/copywriting-generator'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 文档结构撰写 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-list-2-line"></i>
            <h3 class="category-title">文档结构撰写</h3>
          </div>
          <p class="category-desc">快速生成专业文档结构大纲，帮助梳理思路，构建逻辑清晰的文档框架，提高写作效率。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/copywriting/document-structure'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 长文档撰写 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-draft-line"></i>
            <h3 class="category-title">长文档撰写</h3>
          </div>
          <p class="category-desc">AI辅助创作长篇文档，自动生成内容丰富、结构完整的专业文章，提高内容创作效率和质量。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/copywriting/longform'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 文章校对 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-check-line"></i>
            <h3 class="category-title">文章校对</h3>
          </div>
          <p class="category-desc">智能检查文章中的拼写、语法错误，提供修改建议，确保文章准确无误，提升专业性。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/revision/proofreading'" target="_blank">开始校对 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 文章润色 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-pen-nib-line"></i>
            <h3 class="category-title">文章润色</h3>
          </div>
          <p class="category-desc">AI智能优化文章表达，提升语言流畅度和可读性，使文章更加生动有吸引力，提高传播效果。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/revision/refinement'" target="_blank">开始润色 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>

        <!-- 文档总结 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-reduce-line"></i>
            <h3 class="category-title">文档总结</h3>
          </div>
          <p class="category-desc">快速提取文档核心要点，生成简洁明了的摘要，节省阅读时间，提高信息获取效率。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/revision/summary'" target="_blank">开始总结 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- AI PPT创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-slideshow-line"></i>
            <h3 class="category-title">AI PPT创作</h3>
          </div>
          <p class="category-desc">使用AI技术快速生成专业演示文稿，只需简单输入主题和大纲，即可自动生成内容丰富、逻辑清晰的PPT。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/ai-office/integration-test'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 智能会议纪要 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-list-line"></i>
            <h3 class="category-title">智能会议纪要</h3>
          </div>
          <p class="category-desc">利用AI技术快速整理会议内容，自动识别关键议题、行动项和决策要点，将冗长会议转化为结构化纪要。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/ai-office/meeting-minutes'" target="_blank">开始创建 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 智能合同检查 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-search-line"></i>
            <h3 class="category-title">智能合同检查</h3>
          </div>
          <p class="category-desc">利用AI技术智能审查合同内容，自动识别可能存在风险的条款，分析权利义务平衡性，提供专业修改建议。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/ai-office/legal/contract-check'" target="_blank">开始检查 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 智能数据分析 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-bar-chart-line"></i>
            <h3 class="category-title">智能数据分析</h3>
          </div>
          <p class="category-desc">利用AI技术智能分析各类数据，快速发现数据中的模式和趋势，生成直观的数据可视化图表，助力数据驱动决策。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/ai-office/data-analysis'" target="_blank">开始分析 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 智能招聘JD生成 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-list-3-line"></i>
            <h3 class="category-title">智能招聘JD生成</h3>
          </div>
          <p class="category-desc">利用AI技术快速生成专业的招聘职位描述，只需填写岗位基本信息，即可自动生成包含职责、要求和福利的完整JD。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/ai-office/jd-maker'" target="_blank">开始创建 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 智能简历优化 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-text-line"></i>
            <h3 class="category-title">智能简历优化</h3>
          </div>
          <p class="category-desc">利用AI技术智能优化个人简历，从结构、内容、关键词等多方面提升简历质量，增加求职成功率，提供专业优化建议。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/ai-office/cv-optimize'" target="_blank">开始优化 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIOfficeSuite',
  data() {
    return {
      window: window
    }
  }
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
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  padding: 24px;
  margin: 16px;
}

.category-section {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(186, 0, 63, 0.08);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  border-top: 4px solid #ba003f;
  min-height: 320px;
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
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 16px;
  position: relative;
}

.category-header i {
  font-size: 32px;
  margin-bottom: 12px;
  color: #ba003f;
  background: rgba(186, 0, 63, 0.08);
  padding: 12px;
  border-radius: 50%;
  height: 64px;
  width: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.category-section:hover .category-header i {
  background: rgba(186, 0, 63, 0.12);
  transform: scale(1.05);
}

.category-title {
  font-size: 18px;
  margin: 0;
  color: #333;
  font-weight: 600;
  position: relative;
  padding-bottom: 10px;
}

.category-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 3px;
  background: #ba003f;
  border-radius: 2px;
  opacity: 0;
  transition: all 0.3s ease;
}

.category-section:hover .category-title::after {
  opacity: 1;
  width: 60px;
}

.category-desc {
  color: #666;
  margin: 16px 0;
  line-height: 1.5;
  font-size: 14px;
  text-align: center;
  flex-grow: 1;
}

.category-button {
  margin-top: auto;
  text-align: center;
  padding-top: 16px;
}

.category-button a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #ba003f;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 90%;
  gap: 6px;
  position: relative;
  overflow: hidden;
}

.category-button a i {
  transition: transform 0.3s ease;
}

.category-button a:hover {
  background: #d4185b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(186, 0, 63, 0.2);
}

.category-button a:hover i {
  transform: translateX(4px);
}

@media (max-width: 1440px) {
  .category-container {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1280px) {
  .category-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .category-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .category-container {
    grid-template-columns: 1fr;
    padding: 16px;
  }
  
  .category-section {
    min-height: 280px;
  }
}
</style> 