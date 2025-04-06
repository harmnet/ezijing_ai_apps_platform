<template>
  <div class="content">
    <div class="category-container">
      <!-- AI数字人微课制作 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-presentation-line"></i>
          <h3 class="category-title">AI数字人微课制作</h3>
        </div>
        <p class="category-desc">通过上传PPT和讲解文稿，使用AI数字人自动生成专业微课讲解视频。支持多种数字人形象选择，实现高效快捷的教学内容创作。</p>
        <div class="category-button">
          <router-link to="/digital-human/ppt-video">开始制作 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- AI数字人形象克隆 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-user-follow-line"></i>
          <h3 class="category-title">AI数字人形象克隆</h3>
        </div>
        <p class="category-desc">通过上传照片和视频，快速创建个人专属数字人形象。利用AI技术实现高度还原的面部表情和动作，打造独特的数字化分身。</p>
        <div class="category-button">
          <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
        </div>
      </div>
      
      <!-- AI数字人声音克隆 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-voiceprint-line"></i>
          <h3 class="category-title">AI数字人声音克隆</h3>
        </div>
        <p class="category-desc">通过录制少量语音样本，生成与本人声音高度相似的AI语音。支持多语言合成，可应用于视频配音、内容创作和个性化语音助手等场景。</p>
        <div class="category-button">
          <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
        </div>
      </div>

      <!-- AI数字人视频制作 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-movie-line"></i>
          <h3 class="category-title">AI数字人视频制作</h3>
        </div>
        <p class="category-desc">结合文字脚本和AI数字人，一键生成专业讲解视频。支持多场景背景、丰富手势动作和表情变化，让视频内容更加生动自然。</p>
        <div class="category-button">
          <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
        </div>
      </div>
      
      <!-- AI数字人直播 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-live-line"></i>
          <h3 class="category-title">AI数字人直播</h3>
        </div>
        <p class="category-desc">使用AI数字人进行实时直播互动，支持文字转语音、实时问答和表情动作生成。适用于教育培训、产品展示和在线活动等场景，提升直播效果。</p>
        <div class="category-button">
          <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
        </div>
      </div>
      
      <!-- AI交互式数字人 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-robot-line"></i>
          <h3 class="category-title">AI交互式数字人</h3>
        </div>
        <p class="category-desc">打造智能交互的AI数字人助手，支持自然语言对话、知识问答和个性化推荐。可嵌入网站、APP和线下展示屏幕，提供沉浸式交互体验。</p>
        <div class="category-button">
          <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DigitalHumanFunctionalList'
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
  grid-template-columns: repeat(3, 1fr);
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
  min-height: 400px;
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
  margin-bottom: 24px;
  position: relative;
}

.category-header i {
  font-size: 42px;
  margin-bottom: 16px;
  color: #ba003f;
  background: rgba(186, 0, 63, 0.08);
  padding: 16px;
  border-radius: 50%;
  height: 80px;
  width: 80px;
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
  font-size: 22px;
  margin: 0;
  color: #333;
  font-weight: 600;
  position: relative;
  padding-bottom: 12px;
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
  margin: 20px 0;
  line-height: 1.6;
  font-size: 15px;
  text-align: center;
  flex-grow: 1;
}

.category-button {
  margin-top: auto;
  text-align: center;
  padding-top: 20px;
}

.category-button a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #ba003f;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 85%;
  gap: 8px;
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

@media (max-width: 1280px) {
  .category-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .category-container {
    grid-template-columns: 1fr;
    padding: 20px;
  }
  
  .category-section {
    min-height: 320px;
  }
}
</style> 