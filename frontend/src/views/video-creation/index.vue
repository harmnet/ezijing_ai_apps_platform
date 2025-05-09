<template>
  <div class="content">
    <router-view v-if="$route.path !== '/video-creation'"></router-view>
    <div v-else>
      <div class="category-container">
        <!-- 第一行：视频生成工具 -->
        <!-- 文生视频 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-file-text-line"></i>
            <h3 class="category-title">AI文生视频</h3>
          </div>
          <p class="category-desc">通过文字描述智能生成视频内容，只需输入您想要的场景、风格和主题，即可快速创建符合需求的短视频。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/video-creation/text-to-video'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 图生视频 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-image-line"></i>
            <h3 class="category-title">AI图生视频</h3>
          </div>
          <p class="category-desc">基于图片快速生成视频，上传您的照片或设计作品，AI将为其赋予生命力，创造动态效果，适用于产品展示和创意内容。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/video-creation/image-to-video'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 数字人视频制作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-user-voice-line"></i>
            <h3 class="category-title">基础数字人视频</h3>
          </div>
          <p class="category-desc">快速创建数字人视频内容，支持多种数字人模型和场景，轻松生成演讲、讲解等专业视频，提升内容表现力和沟通效果。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/digital-human/video-creation'" target="_blank">开始制作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 高级数字人视频 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-user-star-line"></i>
            <h3 class="category-title">高级数字人视频</h3>
          </div>
          <p class="category-desc">提供更高质量的数字人视频定制，支持高级表情、动作和场景，打造媲美真人的视频效果，适用于专业宣传和品牌营销。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/digital-human/advance-video'" target="_blank">开始制作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 克隆数字人 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-user-settings-line"></i>
            <h3 class="category-title">克隆数字人视频</h3>
          </div>
          <p class="category-desc">通过上传照片和语音样本，创建个性化的数字人克隆，实现专属数字分身视频制作，打造个人专属数字形象。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>

        <!-- 第二行：扩展工具 -->
        <!-- 123数字人视频制作 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-numbers-line"></i>
            <h3 class="category-title">123数字人视频</h3>
          </div>
          <p class="category-desc">三步极速创建数字人视频，提供模板化制作流程，无需专业知识即可快速完成视频创作，为初学者提供便捷的视频制作体验。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- 数字人语音合成 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-mic-line"></i>
            <h3 class="category-title">数字人语音合成</h3>
          </div>
          <p class="category-desc">智能合成自然逼真的数字人语音，支持多种音色和情感表达，可用于视频配音和语音内容创作，赋予视频更加丰富的表达能力。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- 数字人微课视频 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-video-chat-line"></i>
            <h3 class="category-title">数字人微课视频</h3>
          </div>
          <p class="category-desc">专为教育和培训设计的数字人视频创作工具，轻松制作专业微课内容，提升学习体验，打造互动式教学视频。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- 交互式数字人 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-chat-smile-3-line"></i>
            <h3 class="category-title">交互式数字人</h3>
          </div>
          <p class="category-desc">创建可实时互动的数字人角色，适用于客服、导购、展示等交互场景，提升用户参与感和沟通效率。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- 数字人直播 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-live-fill"></i>
            <h3 class="category-title">数字人直播</h3>
          </div>
          <p class="category-desc">提供24小时不间断的数字人直播服务，支持脚本预设和实时互动，无需真人操作，为品牌和内容创作者提供全天候的在线存在感。</p>
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
  name: 'VideoCreation',
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