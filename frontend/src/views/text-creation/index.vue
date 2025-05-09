<template>
  <div class="content">
    <router-view v-if="$route.path !== '/text-creation'"></router-view>
    <div v-else>
      <div class="category-container">
        <!-- 第一行：文本创作基础工具 -->
        <!-- 广告语创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-chat-quote-line"></i>
            <h3 class="category-title">AI广告语创作</h3>
          </div>
          <p class="category-desc">快速生成吸引眼球的产品广告语，提升营销效果，轻松获得创意文案，增强品牌影响力。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/marketing/ad-slogan'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 公众号创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-wechat-line"></i>
            <h3 class="category-title">AI公众号创作</h3>
          </div>
          <p class="category-desc">创作符合公众号平台特点的高质量文章，吸引读者，提高转化和互动，增加粉丝留存率。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/new-media/wechat'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 微博文章创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-weibo-line"></i>
            <h3 class="category-title">AI微博文章创作</h3>
          </div>
          <p class="category-desc">创作适合微博平台的热门内容，获得更多关注和互动，提升账号影响力，增加话题讨论度。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/new-media/weibo'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 小红书笔记创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-book-open-line"></i>
            <h3 class="category-title">AI小红书笔记创作</h3>
          </div>
          <p class="category-desc">创作符合小红书平台特点的种草笔记，吸引目标用户，提高转化和收藏，增强内容曝光度。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/new-media/xiaohongshu'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 短视频脚本创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-video-line"></i>
            <h3 class="category-title">AI短视频脚本创作</h3>
          </div>
          <p class="category-desc">创作吸引人的短视频内容脚本，提升内容质量，让视频创作更加高效，增强观众留存率。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/new-media/short-video'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>

        <!-- 第二行：专业文本工具 -->
        <!-- 直播脚本创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-live-line"></i>
            <h3 class="category-title">AI直播脚本创作</h3>
          </div>
          <p class="category-desc">策划有趣的直播内容和互动话术，提高直播质量和观众留存，增加销售转化，打造专业直播体验。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/new-media/livestream'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 诗歌创作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-quill-pen-line"></i>
            <h3 class="category-title">AI诗歌创作</h3>
          </div>
          <p class="category-desc">创作富有情感和韵律的诗歌作品，抒发情感，展现文学素养和艺术美感，传递深层次的思想内涵。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/text-creation/copywriting/poetry'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 文本修订 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-edit-line"></i>
            <h3 class="category-title">AI文本修订优化</h3>
          </div>
          <p class="category-desc">检查并修正文章中的错误，优化语言表达，提高文本质量和可读性，使内容更加专业流畅。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- 长文档写作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-text-line"></i>
            <h3 class="category-title">AI长文档写作</h3>
          </div>
          <p class="category-desc">辅助创作长篇文档、论文和报告，提供结构化写作建议，生成专业内容，节省大量写作时间。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- 多语言翻译 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-translate-2"></i>
            <h3 class="category-title">AI多语言翻译</h3>
          </div>
          <p class="category-desc">智能翻译多种语言内容，保持原文意图和风格，适用于商务文档、网站内容和日常沟通等场景。</p>
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
  name: 'TextCreation',
  data() {
    return {
      window: window
    }
  },
  mounted() {
    // 确保页面加载时滚动到顶部
    window.scrollTo(0, 0);
  }
}
</script>

<style scoped>
:root {
  --zijing-red: #ba003f;
  --zijing-red-light: rgba(186, 0, 63, 0.1);
  --zijing-red-hover: #d4185b;
}

.content {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 0;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  color: #333;
}

.category-container {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  padding: 20px;
  margin: 0;
  width: 100%;
  box-sizing: border-box;
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
  height: 100%;
  justify-content: space-between;
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
  margin-top: 16px;
  text-align: center;
  padding-top: 0;
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
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }
}

@media (max-width: 1280px) {
  .category-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
  }
}

@media (max-width: 992px) {
  .category-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    padding: 20px;
    margin: 12px;
  }
}

@media (max-width: 768px) {
  .category-container {
    grid-template-columns: 1fr;
    padding: 16px;
    margin: 8px;
    gap: 16px;
  }
  
  .category-section {
    min-height: 280px;
  }
}

@media (max-width: 480px) {
  .category-container {
    grid-template-columns: 1fr;
    gap: 15px;
    padding: 12px;
    margin: 0;
  }
  
  .category-section {
    min-height: 250px;
    padding: 18px;
  }
  
  .category-title {
    font-size: 16px;
  }
  
  .category-desc {
    margin: 12px 0;
    font-size: 13px;
  }
}
</style> 