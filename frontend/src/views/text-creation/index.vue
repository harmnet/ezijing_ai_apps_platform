<template>
  <div class="text-creation-page">
    <div class="page-header">
      <div class="page-nav">
        <h2></h2>
      </div>
    </div>
    
    <!-- 如果当前是文本创作首页，显示分类和工具卡片 -->
    <div v-if="isHomePage" class="category-container">
      <!-- 营销创作 -->
      <div class="category-section">
        <div class="category-title-wrapper">
          <h3 class="category-title">
            <i class="ri-advertisement-line"></i>
            营销创作
          </h3>
        </div>
        <div class="tool-cards">
          <div class="tool-card">
            <router-link to="/text-creation/marketing/ad-slogan">
              <div class="tool-icon">
                <i class="ri-chat-quote-line"></i>
              </div>
              <div class="tool-info">
                <h4>广告语生成</h4>
                <p>快速生成吸引眼球的产品广告语</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/marketing/copywriting-generator">
              <div class="tool-icon">
                <i class="ri-file-paper-2-line"></i>
              </div>
              <div class="tool-info">
                <h4>营销文案生成</h4>
                <p>创建有效的产品营销文案和推广内容</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- 新媒体内容创作 -->
      <div class="category-section">
        <div class="category-title-wrapper">
          <h3 class="category-title">
            <i class="ri-smartphone-line"></i>
            新媒体内容创作
          </h3>
        </div>
        <div class="tool-cards">
          <div class="tool-card">
            <router-link to="/text-creation/new-media/wechat">
              <div class="tool-icon">
                <i class="ri-wechat-line"></i>
              </div>
              <div class="tool-info">
                <h4>公众号文章</h4>
                <p>创作符合公众号平台特点的高质量文章</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/new-media/weibo">
              <div class="tool-icon">
                <i class="ri-weibo-line"></i>
              </div>
              <div class="tool-info">
                <h4>微博文章</h4>
                <p>创作适合微博平台的热门内容</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/new-media/xiaohongshu">
              <div class="tool-icon">
                <i class="ri-book-open-line"></i>
              </div>
              <div class="tool-info">
                <h4>小红书文章</h4>
                <p>创作符合小红书平台特点的种草笔记</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/new-media/short-video">
              <div class="tool-icon">
                <i class="ri-video-line"></i>
              </div>
              <div class="tool-info">
                <h4>短视频脚本</h4>
                <p>创作吸引人的短视频内容脚本</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/new-media/livestream">
              <div class="tool-icon">
                <i class="ri-live-line"></i>
              </div>
              <div class="tool-info">
                <h4>直播脚本</h4>
                <p>策划有趣的直播内容和互动话术</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- 文案创作 -->
      <div class="category-section">
        <div class="category-title-wrapper">
          <h3 class="category-title">
            <i class="ri-draft-line"></i>
            文案创作
          </h3>
        </div>
        <div class="tool-cards">
          <div class="tool-card">
            <router-link to="/text-creation/copywriting/document-structure">
              <div class="tool-icon">
                <i class="ri-file-list-3-line"></i>
              </div>
              <div class="tool-info">
                <h4>文档结构撰写</h4>
                <p>生成专业文档的结构和框架</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/copywriting/longform">
              <div class="tool-icon">
                <i class="ri-article-line"></i>
              </div>
              <div class="tool-info">
                <h4>长文创作</h4>
                <p>撰写内容丰富、逻辑清晰的长篇文章</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/copywriting/poetry">
              <div class="tool-icon">
                <i class="ri-quill-pen-line"></i>
              </div>
              <div class="tool-info">
                <h4>诗歌创作</h4>
                <p>创作富有情感和韵律的诗歌作品</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- 文本修订 -->
      <div class="category-section">
        <div class="category-title-wrapper">
          <h3 class="category-title">
            <i class="ri-edit-line"></i>
            文本修订
          </h3>
        </div>
        <div class="tool-cards">
          <div class="tool-card">
            <router-link to="/text-creation/revision/proofreading">
              <div class="tool-icon">
                <i class="ri-error-warning-line"></i>
              </div>
              <div class="tool-info">
                <h4>文章校对</h4>
                <p>检查并修正文章中的错误</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/revision/refinement">
              <div class="tool-icon">
                <i class="ri-markup-line"></i>
              </div>
              <div class="tool-info">
                <h4>文章润色</h4>
                <p>提升文章的表达质量和语言流畅度</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/revision/summary">
              <div class="tool-icon">
                <i class="ri-file-search-line"></i>
              </div>
              <div class="tool-info">
                <h4>文档总结</h4>
                <p>提炼长篇文档的关键内容和要点</p>
              </div>
            </router-link>
          </div>
          
          <!-- 添加合同检查卡片 -->
          <router-link to="/text-creation/legal/contract-check" class="tool-card">
            <div class="card-icon">
              <i class="ri-file-search-line"></i>
            </div>
            <div class="card-content">
              <h4>合同检查</h4>
              <p>上传合同文件，AI智能审查合同条款问题并给出专业修改建议</p>
            </div>
          </router-link>
        </div>
      </div>
      
      <!-- 学术文案 -->
      <div class="category-section">
        <div class="category-title-wrapper">
          <h3 class="category-title">
            <i class="ri-book-2-line"></i>
            学术文案
          </h3>
        </div>
        <div class="tool-cards">
          <div class="tool-card">
            <router-link to="/text-creation/academic/paper-abstract">
              <div class="tool-icon">
                <i class="ri-draft-2-line"></i>
              </div>
              <div class="tool-info">
                <h4>论文大纲编写</h4>
                <p>规划完整的论文结构和研究框架</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/academic/report-summary">
              <div class="tool-icon">
                <i class="ri-file-paper-line"></i>
              </div>
              <div class="tool-info">
                <h4>报告摘要</h4>
                <p>总结研究报告的主要内容和结论</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/academic/search">
              <div class="tool-icon">
                <i class="ri-search-line"></i>
              </div>
              <div class="tool-info">
                <h4>学术搜索</h4>
                <p>智能搜索学术论文、研究报告等学术资源</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/academic/plagiarism">
              <div class="tool-icon">
                <i class="ri-file-shield-2-line"></i>
              </div>
              <div class="tool-info">
                <h4>文本查重</h4>
                <p>智能检测文本相似度，确保文本原创性</p>
              </div>
            </router-link>
          </div>
          <div class="tool-card">
            <router-link to="/text-creation/academic/translation">
              <div class="tool-icon">
                <i class="ri-translate-2"></i>
              </div>
              <div class="tool-info">
                <h4>翻译</h4>
                <p>准确翻译学术文本和专业术语</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 如果是子页面，显示子路由内容 -->
    <router-view v-else></router-view>
  </div>
</template>

<script>
export default {
  name: 'TextCreation',
  computed: {
    // 判断是否在文本创作首页
    isHomePage() {
      return this.$route.path === '/text-creation';
    }
  }
}
</script>

<style scoped>
.text-creation-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-nav h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

/* 文本创作中心特有样式 */
.category-container {
  padding: 20px 0;
}

.category-section {
  margin-bottom: 40px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  padding: 25px;
  overflow: hidden;
  border-top: 4px solid var(--primary-color, #ba003f);
}

.category-title-wrapper {
  margin-bottom: 20px;
}

.category-title {
  font-size: 22px;
  margin: 0;
  display: flex;
  align-items: center;
  color: #333;
}

.category-title i {
  margin-right: 12px;
  font-size: 24px;
  color: var(--primary-color, #ba003f);
}

.tool-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.tool-card {
  flex: 0 0 calc(33.33% - 14px);
  border-radius: 10px;
  background: #f9f9f9;
  padding: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #eee;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  border-color: #ddd;
}

/* 添加链接样式，使其填充整个卡片 */
.tool-card a {
  text-decoration: none;
  color: inherit;
  display: flex;
  width: 100%;
  height: 100%;
}

.tool-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(186, 0, 63, 0.08);
  border-radius: 10px;
  margin-right: 15px;
  font-size: 22px;
  color: var(--primary-color, #ba003f);
}

.tool-info {
  flex: 1;
}

.tool-info h4 {
  margin: 0 0 5px;
  font-size: 16px;
}

.tool-info p {
  margin: 0;
  font-size: 13px;
  color: #666;
  line-height: 1.3;
}

@media (max-width: 1024px) {
  .tool-card {
    flex: 0 0 calc(50% - 10px);
  }
}

@media (max-width: 768px) {
  .tool-card {
    flex: 0 0 100%;
  }
}
</style> 