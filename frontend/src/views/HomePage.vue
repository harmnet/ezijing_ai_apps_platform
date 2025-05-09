<template>
  <div class="home-page">
    <section class="learning-path">
      <div class="section-header-container">
        <h2 class="section-title">你的AI应用能力进阶之旅</h2>
        <p class="section-description">从零基础到AI应用专家，通过"三阶段"、"六篇章"构建循序渐进的学习路径，每一步都是能力的飞跃</p>
      </div>
      
      <div class="path-container">
        <!-- 入门层次 -->
        <div class="path-level beginner">
          <div class="level-header">
            <h3>第一阶段：入门 <span class="level-tag">基础起步</span></h3>
          </div>
          <div class="level-modules">
            <div class="module">
              <div class="module-icon">
                <i class="ri-book-read-line"></i>
              </div>
              <div class="module-content">
                <h4>01 准备篇</h4>
                <p>零门槛掌握AI基础知识，建立人工智能思维模式</p>
                <router-link to="/prepare-study" class="module-link">开启AI之旅 <i class="ri-arrow-right-line"></i></router-link>
              </div>
            </div>
            <div class="module">
              <div class="module-icon">
                <i class="ri-chat-1-line"></i>
              </div>
              <div class="module-content">
                <h4>02 基础对话篇</h4>
                <p>找到AI时代的人机对话"关键钥匙"，掌握AI黄金对话技巧，养成超出一般人群的基础技能。</p>
                <a href="/prompt-case" target="_blank" class="module-link">开始学习 <i class="ri-arrow-right-line"></i></a>
              </div>
            </div>
          </div>
        </div>

        <!-- 熟练层次 -->
        <div class="path-level intermediate">
          <div class="level-header">
            <h3>第二阶段：熟练 <span class="level-tag">能力提升</span></h3>
          </div>
          <div class="level-modules">
            <div class="module">
              <div class="module-icon">
                <i class="ri-rocket-line"></i>
              </div>
              <div class="module-content">
                <h4>03 效率飞跃篇</h4>
                <p>掌握40余个效率起飞神器，实现"躺平"也能高质量高效产出。</p>
                <router-link to="/increase-efficiency" class="module-link">效率倍增 <i class="ri-arrow-right-line"></i></router-link>
              </div>
            </div>
            <div class="module">
              <div class="module-icon">
                <i class="ri-file-list-3-line"></i>
              </div>
              <div class="module-content">
                <h4>04 场景实战篇</h4>
                <p>直达10个典型场景，探知AI如何辅助"头大"的职场人士分分钟分析问题，解决问题，满足客户和领导的需求。</p>
                <router-link to="/practical-scenario" class="module-link">场景实践 <i class="ri-arrow-right-line"></i></router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 精通层次 -->
        <div class="path-level advanced">
          <div class="level-header">
            <h3>第三阶段：精通 <span class="level-tag">创新突破</span></h3>
          </div>
          <div class="level-modules">
            <div class="module">
              <div class="module-icon">
                <i class="ri-file-paper-2-line"></i>
              </div>
              <div class="module-content">
                <h4>05 综合案例实战篇</h4>
                <p>真实参与10个不同行业的真实项目案例，灵活运用AI工具，完成职业人士的AI全面应用，让你脱颖而出。</p>
                <router-link to="/ai-case-studies" class="module-link">案例探索 <i class="ri-arrow-right-line"></i></router-link>
              </div>
            </div>
            <div class="module">
              <div class="module-icon">
                <i class="ri-lightbulb-flash-line"></i>
              </div>
              <div class="module-content">
                <h4>06 专业生产力提升篇</h4>
                <p>打造个人专属AI工作系统，让1人=10人团队产出，实现职业生涯的指数级跃升</p>
                <a :href="window.location.origin + '/productivity-center'" target="_blank" class="module-link">突破极限 <i class="ri-arrow-right-line"></i></a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      loaded: false,
      window: window
    }
  },
  mounted() {
    // 页面加载完成后设置状态
    setTimeout(() => {
      this.loaded = true
    }, 100)
  }
}
</script>

<style scoped>
.home-page {
  padding: 0;
  overflow-y: auto;
  height: 100%;
  color: #333;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #fff;
}

/* 顶部主题区域 */
.hero-section {
  text-align: center;
  padding: 120px 20px;
  margin-bottom: 40px;
  background: none;
  border-radius: 0;
  position: relative;
  overflow: hidden;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('../assets/images/home/hero-banner.png');
  background-size: cover;
  background-position: center top;
  opacity: 1;
  z-index: 0;
  filter: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.8s ease-out;
  color: #fff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  margin-top: 170px;
}

.hero-section h1 {
  font-size: 36px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 16px;
}

.hero-section p {
  font-size: 18px;
  color: #ffffff;
  margin-bottom: 30px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.primary-btn {
  background-color: #C74B50;
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 6px;
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  text-decoration: none;
  display: inline-block;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.primary-btn:hover {
  background-color: #A22A2F;
  transform: translateY(-2px);
}

.secondary-btn {
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.5);
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(5px);
}

.secondary-btn:hover {
  background-color: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.7);
  color: #fff;
  transform: translateY(-2px);
}

/* 学习路径区域 - 全新优化 */
.learning-path {
  padding: 60px 0 80px;
  background-color: #FAFAFA;
  position: relative;
  overflow: hidden;
  margin-bottom: 60px;
  text-align: center;
}

.learning-path::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(circle at 10% 10%, rgba(186, 0, 63, 0.03) 0%, transparent 60%),
                    radial-gradient(circle at 90% 90%, rgba(177, 136, 101, 0.03) 0%, transparent 60%);
  z-index: 0;
}

/* 添加新的容器样式 */
.section-header-container {
  width: 90%;
  max-width: 980px;
  margin: 0 auto 60px;
  text-align: center;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.section-title {
  font-size: 38px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 20px;
  color: #BA003F;
  position: relative;
  z-index: 1;
  letter-spacing: -0.5px;
  width: 100%;
  display: block;
}

.section-title::after {
  content: '';
  display: none; /* 隐藏红色下划线 */
}

.section-description {
  font-size: 18px;
  color: #555;
  text-align: center;
  max-width: 700px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  font-weight: 500;
  line-height: 1.6;
}

.path-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
  width: 90%;
  max-width: 980px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.path-level {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  padding: 0;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  animation: fadeInUp 0.6s ease-out;
  overflow: hidden;
  position: relative;
}

.path-level.beginner {
  animation-delay: 0.1s;
}

.path-level.intermediate {
  animation-delay: 0.3s;
}

.path-level.advanced {
  animation-delay: 0.5s;
}

.path-level:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08);
}

.level-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 30px;
  position: relative;
  text-align: center;
  overflow: hidden;
}

/* 为标题区域添加渐变效果 */
.beginner .level-header {
  background: linear-gradient(135deg, #BA003F 0%, #DD4B4F 50%, #E06366 100%);
}

.intermediate .level-header {
  background: linear-gradient(135deg, #8E6B4F 0%, #B18865 50%, #D0A787 100%);
}

.advanced .level-header {
  background: linear-gradient(135deg, #7A0032 0%, #BA003F 50%, #D4003E 100%);
}

/* 创建六边形背景图案 */
.level-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.07;
  z-index: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='200' height='200' viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.3'%3E%3Cpath d='M100 0l50 30v60l-50 30-50-30V30z'/%3E%3Cpath d='M160 70l20 12v24l-20 12-20-12V82z' fill-opacity='0.2'/%3E%3Cpath d='M40 140l30 18v36l-30 18-30-18v-36z' fill-opacity='0.4'/%3E%3C/g%3E%3C/svg%3E");
  background-size: 200px 200px;
  background-position: center center;
}

.beginner .level-header::before {
  background-position: 10% 30%;
}

.intermediate .level-header::before {
  background-position: 70% 50%;
}

.advanced .level-header::before {
  background-position: 20% 60%;
}

.level-tag {
  font-size: 13px;
  background-color: rgba(255, 255, 255, 0.25);
  padding: 3px 10px;
  border-radius: 20px;
  margin-left: 10px;
  font-weight: 500;
  vertical-align: middle;
  letter-spacing: 0.5px;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(5px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.level-icon {
  display: none; /* 隐藏图标 */
}

.level-header h3 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  color: white;
  position: relative;
  z-index: 1;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.level-modules {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  padding: 30px;
}

.module {
  display: flex;
  background-color: #FAFAFA;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

/* 添加1/4圆形装饰和渐变背景 */
.module::after {
  content: '';
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  opacity: 0.15;
  z-index: 0;
  transition: all 0.3s ease;
}

.beginner .module {
  background: linear-gradient(135deg, #FAFAFA 0%, #FFF1F3 100%);
}

.beginner .module::after {
  background: #BA003F;
}

.intermediate .module {
  background: linear-gradient(135deg, #FAFAFA 0%, #F9F3EF 100%);
}

.intermediate .module::after {
  background: #B18865;
}

.advanced .module {
  background: linear-gradient(135deg, #FAFAFA 0%, #FFE8EE 100%);
}

.advanced .module::after {
  background: #950031;
}

.module:hover::after {
  width: 120px;
  height: 120px;
  opacity: 0.2;
}

.beginner .module:hover {
  background: linear-gradient(135deg, #FFF5F7 0%, #FFE8EC 100%);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(186, 0, 63, 0.1);
}

.intermediate .module:hover {
  background: linear-gradient(135deg, #FAF7F4 0%, #F5EBE0 100%);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(177, 136, 101, 0.1);
}

.advanced .module:hover {
  background: linear-gradient(135deg, #FFF5F8 0%, #FFE0E8 100%);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(186, 0, 63, 0.1);
}

.module-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 22px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
  z-index: 1;
}

.beginner .module-icon {
  background: linear-gradient(135deg, #BA003F, #DD4B4F);
  color: white;
}

.intermediate .module-icon {
  background: linear-gradient(135deg, #B18865, #C8A080);
  color: white;
}

.advanced .module-icon {
  background: linear-gradient(135deg, #950031, #BA003F);
  color: white;
}

.module-icon::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0));
  border-radius: 50%;
}

.module-icon i {
  position: relative;
  z-index: 1;
  font-size: 24px;
}

.module-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.module-content h4 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.beginner .module-content h4 {
  color: #BA003F;
}

.intermediate .module-content h4 {
  color: #B18865;
}

.advanced .module-content h4 {
  color: #BA003F;
}

.module-content p {
  font-size: 15px;
  color: #666;
  margin: 0 0 16px 0;
  line-height: 1.6;
}

.module-link {
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  position: relative;
  padding-bottom: 2px;
}

.beginner .module-link {
  color: #BA003F;
}

.intermediate .module-link {
  color: #B18865;
}

.advanced .module-link {
  color: #BA003F;
}

.module-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  transition: width 0.3s ease;
}

.beginner .module-link::after {
  background-color: #BA003F;
}

.intermediate .module-link::after {
  background-color: #B18865;
}

.advanced .module-link::after {
  background-color: #BA003F;
}

.module-link:hover::after {
  width: calc(100% - 24px); /* 留出箭头的空间 */
}

.module-link i {
  margin-left: 4px;
  transition: transform 0.2s;
}

.module-link:hover i {
  transform: translateX(4px);
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .hero-section {
    padding: 40px 20px;
  }
  
  .hero-section h1 {
    font-size: 28px;
  }
  
  .hero-section p {
    font-size: 16px;
  }
  
  .path-level {
    padding: 0;
  }
  
  .level-modules {
    grid-template-columns: 1fr;
    padding: 20px;
  }
  
  .section-title {
    font-size: 28px;
  }
  
  .level-header {
    padding: 15px 20px;
  }
  
  .level-icon {
    width: 50px;
    height: 50px;
  }

  .section-description {
    font-size: 16px;
    margin-bottom: 40px;
  }
}

/* 过渡效果 */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style> 