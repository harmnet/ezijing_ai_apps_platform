<template>
  <div class="content">
    <router-view v-if="$route.path !== '/image-creation'"></router-view>
    <div v-else>
      <div class="category-container">
        <!-- 第一行 -->
        <!-- 在线图形设计 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-pencil-ruler-2-line"></i>
            <h3 class="category-title">在线图形设计</h3>
          </div>
          <p class="category-desc">专业的图形设计工具，使用AI辅助快速创建精美的视觉内容，包括海报、Logo、社交媒体配图等多种设计需求。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/online-design'" target="_blank">开始设计 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 智能图形设计 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-ai-generate"></i>
            <h3 class="category-title">智能图形设计</h3>
          </div>
          <p class="category-desc">基于AI技术的智能图形设计工具，只需输入关键词和需求，即可快速生成高质量的视觉内容，大幅提升设计效率。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/intelligent-design'" target="_blank">开始设计 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- AI商品图设计 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-image-edit-fill"></i>
            <h3 class="category-title">AI商品图设计</h3>
          </div>
          <p class="category-desc">智能生成专业商品展示图，一键美化产品图片，提升商品视觉吸引力，适用于电商、产品宣传等多种场景，快速创建高质量商品展示效果。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/image-to-painter'" target="_blank">开始设计 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- 智能抠图 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-scissors-cut-line"></i>
            <h3 class="category-title">AI智能抠图</h3>
          </div>
          <p class="category-desc">一键自动识别并抠除图片背景，支持精细调整和边缘优化，生成透明背景图片，快速实现复杂图像抠图，适用于产品图处理和创意合成。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/image-matting'" target="_blank">开始抠图 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- AI图片转设计 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-artboard-2-line"></i>
            <h3 class="category-title">AI图片转设计</h3>
          </div>
          <p class="category-desc">将普通图片转换为专业设计作品，支持多种设计风格和模板选择，一键生成海报、宣传图、社交媒体图片等多种设计素材。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/image-to-design'" target="_blank">开始设计 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>

        <!-- 第二行 -->
        <!-- AI文生图 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-text-wrap"></i>
            <h3 class="category-title">AI文生图</h3>
          </div>
          <p class="category-desc">通过文字描述生成符合需求的创意图像，让创作更加快捷。支持多种AI模型，可根据详细提示词生成高质量图像。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/text-to-image'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- AI图片风格调整 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-image-edit-line"></i>
            <h3 class="category-title">AI图片风格调整</h3>
          </div>
          <p class="category-desc">通过AI技术实现图像风格转换，支持多种艺术风格如油画、水彩画、素描等，让普通照片焕发艺术魅力，为图片增添多样化的视觉效果。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/image-to-image'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- AI局部重绘 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-brush-line"></i>
            <h3 class="category-title">AI局部重绘</h3>
          </div>
          <p class="category-desc">精准选择图像区域进行智能重绘，可用于去除不需要的元素、替换背景或添加新内容，保持图像整体和谐性的同时实现创意编辑。</p>
          <div class="category-button">
            <a :href="window.location.origin + '/image-creation/image-redraw'" target="_blank">开始创作 <i class="ri-arrow-right-line"></i></a>
          </div>
        </div>
        
        <!-- AI扩图 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-crop-line"></i>
            <h3 class="category-title">AI扩图</h3>
          </div>
          <p class="category-desc">智能扩展图像边界，自动填充合理内容。可用于调整图像比例、扩展画面空间、适配更大尺寸，保持画面连贯性和自然感。</p>
          <div class="category-button">
            <a class="coming-soon">即将推出 <i class="ri-time-line"></i></a>
          </div>
        </div>
        
        <!-- AI上色 -->
        <div class="category-section">
          <div class="category-header">
            <i class="ri-palette-line"></i>
            <h3 class="category-title">AI上色</h3>
          </div>
          <p class="category-desc">为黑白照片、素描、线稿等自动添加自然逼真的色彩。可智能识别主体，根据场景和内容特点生成合理色彩，赋予老照片和艺术作品新生命。</p>
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
  name: 'ImageCreation',
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