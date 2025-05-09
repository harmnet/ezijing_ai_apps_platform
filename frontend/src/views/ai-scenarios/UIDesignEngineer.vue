<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>UI设计工程师 <span class="position-category">产品与研发类</span></h1>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="container">
      <!-- 职位详情部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-profile-line"></i> 职位详细介绍
        </h2>
        <div class="detail-card">
          <div class="detail-item">
            <h3>岗位职责</h3>
            <ul>
              <li>设计用户界面和交互体验，确保产品视觉美观且易用</li>
              <li>创建界面原型、线框图和高保真视觉设计</li>
              <li>制定和维护设计系统、组件库和设计规范</li>
              <li>与产品、研发团队协作，确保设计方案顺利落地</li>
              <li>进行用户调研和可用性测试，持续优化设计</li>
              <li>分析行业趋势和用户反馈，提出设计改进方案</li>
              <li>参与产品视觉识别系统和品牌形象设计</li>
              <li>贯彻用户体验原则，确保设计符合用户需求</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>扎实的视觉设计功底和审美能力</li>
              <li>精通主流设计工具（如Figma、Sketch、Adobe系列）</li>
              <li>熟悉UI设计规范和交互设计原则</li>
              <li>良好的沟通能力和团队协作精神</li>
              <li>了解前端技术实现原理，具备一定的技术敏感度</li>
              <li>能够理解用户体验设计流程和方法论</li>
              <li>注重细节，持续学习和探索新设计趋势</li>
              <li>能够接受反馈并不断改进设计方案</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>UI设计工程师需要与多个角色密切合作：</p>
            <ul>
              <li><strong>产品经理</strong>：理解产品需求和目标用户，共同确定产品视觉方向</li>
              <li><strong>UX设计师</strong>：协作制定用户体验策略和交互流程</li>
              <li><strong>研发工程师</strong>：沟通设计实现细节，确保视觉效果在产品中正确呈现</li>
              <li><strong>测试工程师</strong>：确认UI实现是否符合设计规范</li>
              <li><strong>市场营销</strong>：配合品牌形象和营销活动设计</li>
              <li><strong>内容运营</strong>：协调产品内容展示和视觉呈现</li>
              <li><strong>设计总监</strong>：汇报设计方案，获取专业指导</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>UI设计工程师的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>高级UI设计师</li>
              <li>视觉设计总监</li>
              <li>用户体验设计师</li>
              <li>设计系统专家</li>
              <li>创意总监</li>
              <li>产品设计负责人</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于UI设计工程师的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 文生图 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-image-line"></i>
            </div>
            <div class="function-content">
              <h3>文生图</h3>
              <p>通过文字描述快速生成设计灵感和UI界面原型，加速设计构思过程。</p>
              <div class="function-tags">
                <span class="tag">图像生成</span>
                <span class="tag">创意灵感</span>
              </div>
              <router-link to="/image-creation/text-to-image" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 图片风格调整 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-contrast-2-line"></i>
            </div>
            <div class="function-content">
              <h3>图片风格调整</h3>
              <p>快速调整设计作品的视觉风格，探索不同色彩和设计语言的表现效果。</p>
              <div class="function-tags">
                <span class="tag">风格转换</span>
                <span class="tag">视觉优化</span>
              </div>
              <router-link to="/image-creation/image-to-image" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 图片局部重绘 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-brush-line"></i>
            </div>
            <div class="function-content">
              <h3>图片局部重绘</h3>
              <p>精确修改设计稿的特定区域，快速调整界面元素和细节，提高迭代效率。</p>
              <div class="function-tags">
                <span class="tag">局部编辑</span>
                <span class="tag">精细调整</span>
              </div>
              <router-link to="/image-creation/image-redraw" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 在线图片设计 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-layout-line"></i>
            </div>
            <div class="function-content">
              <h3>在线图片设计</h3>
              <p>使用AI辅助创建界面布局、图标和视觉元素，提高设计效率和创意表现。</p>
              <div class="function-tags">
                <span class="tag">图像设计</span>
                <span class="tag">创意助手</span>
              </div>
              <router-link to="/image-creation/online-design" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 智能图形设计 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-ai-generate"></i>
            </div>
            <div class="function-content">
              <h3>智能图形设计</h3>
              <p>使用AI技术快速生成高质量UI元素和视觉设计，只需描述需求即可自动创建所需内容。</p>
              <div class="function-tags">
                <span class="tag">智能生成</span>
                <span class="tag">效率工具</span>
              </div>
              <router-link to="/image-creation/intelligent-design" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- AI PPT创作 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-slideshow-line"></i>
            </div>
            <div class="function-content">
              <h3>AI PPT创作</h3>
              <p>快速生成设计提案和作品展示PPT，高效呈现设计方案和创意理念。</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">提案</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- AI会议纪要 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>AI会议纪要</h3>
              <p>自动记录设计评审会议内容，提取关键反馈和决策，确保设计迭代方向明确。</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">协作</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UIDesignEngineer',
  methods: {
    goBack() {
      this.$router.push('/ai-scenarios');
    }
  }
}
</script>

<style scoped>
.position-detail-container {
  padding-bottom: 60px;
}

.position-header {
  background-color: #f5f5f5;
  padding: 40px 0 30px;
  margin-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #666;
  margin-bottom: 20px;
  cursor: pointer;
  transition: color 0.2s;
}

.back-link:hover {
  color: #ba003f;
}

.back-link i {
  margin-right: 5px;
}

.position-header h1 {
  font-size: 36px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.position-category {
  font-size: 16px;
  font-weight: normal;
  color: #666;
  margin-left: 10px;
}

.position-section {
  margin-bottom: 50px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.section-title i {
  margin-right: 10px;
  color: #ba003f;
}

.section-desc {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
}

.detail-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

.detail-item {
  margin-bottom: 30px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item h3 {
  font-size: 20px;
  font-weight: 600;
  color: #ba003f;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #eee;
}

.detail-item ul {
  padding-left: 20px;
}

.detail-item li {
  margin-bottom: 10px;
  line-height: 1.6;
}

.ai-functions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.function-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.function-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  background-color: rgba(186, 0, 63, 0.05);
}

.function-icon i {
  font-size: 32px;
  color: #ba003f;
}

.function-content {
  padding: 20px;
  flex: 1;
}

.function-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.function-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.function-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  font-size: 12px;
  background-color: #f5f5f5;
  color: #666;
  padding: 4px 8px;
  border-radius: 4px;
}

.use-function-btn {
  display: inline-flex;
  align-items: center;
  color: #ba003f;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.use-function-btn i {
  margin-left: 4px;
  transition: transform 0.2s ease;
}

.use-function-btn:hover {
  color: #d4185b;
}

.use-function-btn:hover i {
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .ai-functions-grid {
    grid-template-columns: 1fr;
  }
  
  .position-header h1 {
    font-size: 28px;
  }
  
  .detail-card {
    padding: 20px;
  }
}
</style> 