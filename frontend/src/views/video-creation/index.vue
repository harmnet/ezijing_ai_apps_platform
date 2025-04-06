<template>
  <div class="content">
    <router-view v-if="$route.path !== '/video-creation'"></router-view>
    <div class="category-container" v-else>
      <!-- AI文生视频 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-file-text-line"></i>
          <h3 class="category-title">AI文生视频</h3>
        </div>
        <p class="category-desc">通过文字描述智能生成视频内容，只需输入您想要的场景、风格和主题，即可快速创建符合需求的短视频、宣传片等多种视频内容。</p>
        <div class="category-button">
          <router-link to="/video-creation/text-to-video">开始创作 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
      
      <!-- AI图生视频 -->
      <div class="category-section">
        <div class="category-header">
          <i class="ri-image-line"></i>
          <h3 class="category-title">AI图生视频</h3>
        </div>
        <p class="category-desc">基于图片快速生成视频，上传您的照片或设计作品，AI将为其赋予生命力，创造动态效果，适用于产品展示、营销宣传等多种场景。</p>
        <div class="category-button">
          <router-link to="/video-creation/image-to-video">开始创作 <i class="ri-arrow-right-line"></i></router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VideoCreation'
}
</script>

<style scoped>
:root {
  --zijing-red: #ba003f;
  --zijing-red-light: rgba(186, 0, 63, 0.1);
  --zijing-red-hover: #d4185b;
}

.category-container {
  display: flex;
  flex-direction: row;
  gap: 24px;
  padding: 32px;
  margin: 20px;
  justify-content: space-between;
  align-items: stretch;
  min-height: 420px;
}

.category-section {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(186, 0, 63, 0.08);
  transition: all 0.3s ease;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-top: 4px solid #ba003f;
  width: 45%;
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

@media (max-width: 1024px) {
  .category-container {
    flex-direction: column;
    padding: 20px;
  }
  
  .category-section {
    width: 100%;
    margin-bottom: 24px;
    min-height: 320px;
  }
}
</style> 