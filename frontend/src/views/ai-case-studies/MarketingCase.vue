<template>
  <div class="marketing-case">
    <!-- 主内容区域 -->
    <div class="main-content">
      <div class="case-header">
        <div class="header-overlay"></div>
        <div class="header-content">
          <div class="case-title-area">
            <h1>AI市场营销综合应用案例：某汽森林「0糖」新品上市战</h1>
            <div class="case-meta">
              <div class="case-tag">市场营销</div>
              <div class="case-date">发布日期: 2024年11月</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 案例内容区域 -->
      <div class="case-content">
        <!-- 第一步：案例背景 -->
        <div id="background" class="section">
          <CaseBackground />
        </div>
        
        <!-- 其他步骤内容将在这里添加 -->
        <div id="research" class="section" style="margin-top: 30px;">
          <MarketResearch />
        </div>
        
        <div id="userProfile" class="section" style="margin-top: 30px;">
          <UserProfile />
        </div>
        
        <div id="planning" class="section" style="margin-top: 30px;">
          <MarketingPlan />
        </div>
        
        <div id="copywriting" class="section" style="margin-top: 30px;">
          <CopywritingCreation />
        </div>
        
        <div id="channelContent" class="section" style="margin-top: 30px;">
          <ChannelContent />
        </div>
      </div>
    </div>
    
    <!-- 右侧固定导航 -->
    <div class="side-navigation">
      <div class="nav-title">案例流程</div>
      <div class="nav-steps">
        <div 
          v-for="(stage, index) in stages" 
          :key="index"
          class="nav-step" 
          :class="{ 'active': activeStep === index + 1 }"
          @click="scrollToSection(stage.id)">
          <div class="step-icon">
            <span>{{ getStepIcon(stage.id) }}</span>
          </div>
          <div class="step-title">{{ stage.title }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, onUnmounted } from 'vue';
import CaseBackground from './CaseBackground.vue';
import MarketResearch from './MarketResearch.vue';
import UserProfile from './UserProfile.vue';
import MarketingPlan from './MarketingPlan.vue';
import CopywritingCreation from './CopywritingCreation.vue';
import ChannelContent from './ChannelContent.vue';

// 流程阶段数据
const stages = reactive([
  { id: 'background', title: '案例背景' },
  { id: 'research', title: '产品市场调研' },
  { id: 'userProfile', title: '用户画像分析' },
  { id: 'planning', title: '产品市场营销策划' },
  { id: 'copywriting', title: '广告语与营销文案创作' },
  { id: 'channelContent', title: '渠道营销内容创作' }
]);

// 当前活跃步骤
const activeStep = ref(1);

// 为每个步骤获取对应的图标（使用emoji表情）
const getStepIcon = (stepId) => {
  const iconMap = {
    background: '💡', // 灯泡表示背景/想法
    research: '🔍',   // 放大镜表示调研
    userProfile: '👤', // 用户表示用户画像
    planning: '📋',    // 策划表
    copywriting: '✏️',  // 铅笔表示文案创作
    channelContent: '📱' // 手机表示渠道内容
  };
  
  return iconMap[stepId] || '📄'; // 默认文档图标
};

// 滚动到对应部分的方法
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
    
    // 设置当前活跃步骤
    stages.forEach((stage, index) => {
      if (stage.id === sectionId) {
        activeStep.value = index + 1;
      }
    });
  }
};

// 检测滚动位置，更新当前活跃步骤
const checkScrollPosition = () => {
  // 获取所有内容区块
  const sections = stages.map(stage => document.getElementById(stage.id));
  
  // 过滤掉不存在的区块
  const validSections = sections.filter(section => section !== null);
  
  if (validSections.length === 0) return;
  
  // 获取当前滚动位置
  const scrollPosition = window.scrollY + 200; // 添加偏移量，使高亮更准确
  
  // 找到当前在视口中的区块
  for (let i = 0; i < validSections.length; i++) {
    const section = validSections[i];
    const sectionTop = section.offsetTop;
    const sectionBottom = sectionTop + section.offsetHeight;
    
    if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
      activeStep.value = i + 1;
      break;
    }
  }
};

// 监听滚动事件
onMounted(() => {
  window.addEventListener('scroll', checkScrollPosition);
  
  // 初始检查
  setTimeout(checkScrollPosition, 200);
});

// 组件卸载前移除事件监听
onUnmounted(() => {
  window.removeEventListener('scroll', checkScrollPosition);
});
</script>

<style scoped>
@import '@/assets/css/study-case.css';

/* 整体布局 */
.marketing-case {
  display: flex;
  justify-content: flex-start;
  position: relative;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* 主内容区域 */
.main-content {
  width: calc(100% - 240px);
  padding-right: 30px;
}

/* 右侧导航 */
.side-navigation {
  width: 220px;
  position: fixed;
  right: calc((100% - 1400px) / 2 + 20px);
  top: 100px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 15px;
  z-index: 100;
  max-height: calc(100vh - 150px);
  overflow-y: auto;
}

.nav-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 15px;
  text-align: center;
}

.nav-steps {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.nav-step {
  display: flex;
  align-items: center;
  padding: 12px 10px;
  background-color: #f8f8f8;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-step:hover {
  transform: translateX(-5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.nav-step.active {
  background-color: #fff;
  border-left: 3px solid #c62828;
  box-shadow: 0 2px 8px rgba(198, 40, 40, 0.15);
}

.step-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 32px;
  height: 32px;
  min-width: 32px;
  background-color: #e0e0e0;
  color: #555;
  border-radius: 50%;
  margin-right: 10px;
  transition: all 0.3s ease;
  box-sizing: border-box;
  padding: 0;
  line-height: 1;
  font-size: 16px;
}

.nav-step.active .step-icon {
  background-color: #c62828;
  color: #fff;
}

.step-title {
  font-size: 14px;
  font-weight: 500;
  color: #555;
  transition: all 0.3s ease;
  line-height: 1.4;
}

.nav-step.active .step-title {
  color: #c62828;
}

/* 头部样式 */
.case-header {
  position: relative;
  height: 360px;
  border-radius: 12px;
  margin-bottom: 40px;
  background-image: url('@/assets/images/marketing-case-cover-new.jpeg');
  background-size: cover;
  background-position: center;
  overflow: hidden;
}

.header-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.4));
  z-index: 1;
}

.header-content {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px;
}

.case-title-area {
  max-width: 90%;
}

.case-title-area h1 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 20px;
  line-height: 1.3;
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 1100px;
}

.case-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.case-tag {
  background-color: rgba(24, 144, 255, 0.8);
  color: #ffffff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.case-date {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

/* 案例内容区域 */
.case-content {
  background-color: #fff;
  border-radius: 10px;
  padding: 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

/* 区块样式 */
.section {
  scroll-margin-top: 30px;
}

/* 标题样式，与CaseBackground组件保持一致 */
.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
  position: relative;
  padding-bottom: 15px;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #c62828; /* 紫荆红 */
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .side-navigation {
    right: 20px;
  }
}

@media (max-width: 1024px) {
  .marketing-case {
    flex-direction: column;
  }
  
  .main-content {
    width: 100%;
    padding-right: 0;
  }
  
  .side-navigation {
    position: sticky;
    top: 0;
    right: auto;
    width: 100%;
    margin-bottom: 20px;
    max-height: none;
    z-index: 100;
  }
  
  .nav-steps {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .nav-step {
    width: calc(33.33% - 7px);
  }
  
  .case-content {
    padding: 30px;
  }
}

@media (max-width: 768px) {
  .case-header {
    height: 280px;
  }
  
  .case-title-area {
    max-width: 100%;
  }
  
  .case-title-area h1 {
    font-size: 24px;
  }
  
  .header-content {
    padding: 30px 20px;
  }
  
  .nav-step {
    width: calc(50% - 5px);
  }
  
  .case-content {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .nav-step {
    width: 100%;
  }
}
</style> 