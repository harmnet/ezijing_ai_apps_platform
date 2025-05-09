<template>
  <div class="content">
    <router-view v-if="$route.path !== '/productivity-center'"></router-view>
    <div v-else>
      <div class="category-container">
        <!-- 知识库问答 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-question-answer-line"></i>
            <h3 class="category-title">知识库问答</h3>
          </div>
          <p class="category-desc">基于企业或个人知识库的智能问答系统，支持上传和分析文档，提供准确的答案和深度洞察，助力决策和研究。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/ai-office/knowledge-qa'" target="_blank">开始使用 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 学术搜索 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-search-line"></i>
            <h3 class="category-title">学术搜索</h3>
          </div>
          <p class="category-desc">专业的学术文献智能搜索工具，支持多语言翻译和精准检索，轻松获取学术资源，提高研究效率。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/academic/translation'" target="_blank">开始搜索 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- AI辅助写论文 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-paper-2-line"></i>
            <h3 class="category-title">AI辅助写论文</h3>
          </div>
          <p class="category-desc">集成AI智能写作技术，辅助学术论文的撰写过程，提供文献引用、格式规范、逻辑优化等多方面支持，提升论文质量。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- AI辅助写研究报告 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-chart-line"></i>
            <h3 class="category-title">AI辅助写研究报告</h3>
          </div>
          <p class="category-desc">通过AI分析数据和行业洞察，辅助生成专业研究报告，包括市场趋势、行业分析、数据解读等，提高报告撰写效率和专业度。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductivityCenter',
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
  grid-template-columns: repeat(4, 1fr);
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

.category-button a.coming-soon {
  background: #6c757d;
  cursor: default;
}

.category-button a.coming-soon:hover {
  background: #6c757d;
  transform: none;
  box-shadow: none;
}

.category-button a.coming-soon:hover i {
  transform: none;
}

@media (max-width: 1440px) {
  .category-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1280px) {
  .category-container {
    grid-template-columns: repeat(2, 1fr);
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