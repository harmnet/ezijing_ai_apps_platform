<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>市场经理 <span class="position-category">市场与营销类</span></h1>
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
              <li>制定和执行市场营销策略和计划，确保市场目标的实现</li>
              <li>管理品牌形象和品牌推广活动，提升品牌知名度和美誉度</li>
              <li>负责市场调研和竞争分析，把握市场趋势和消费者洞察</li>
              <li>策划和管理营销活动，包括线上和线下推广活动</li>
              <li>监控和分析营销效果，优化营销策略和预算分配</li>
              <li>管理和培训市场团队，提升团队专业能力</li>
              <li>与销售、产品等部门协作，确保市场活动支持公司整体目标</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>出色的营销策略规划和执行能力</li>
              <li>优秀的创意思维和内容策划能力</li>
              <li>良好的数据分析能力，能够评估营销效果并做出优化</li>
              <li>项目管理能力，能够同时管理多个营销项目</li>
              <li>团队领导和协作能力，能够调动跨部门资源</li>
              <li>熟悉数字营销工具和社交媒体平台</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>市场经理需要与多个部门和角色密切合作：</p>
            <ul>
              <li><strong>销售部门</strong>：协调营销活动与销售目标的一致性</li>
              <li><strong>产品部门</strong>：了解产品特性，进行有效的市场定位</li>
              <li><strong>设计部门</strong>：合作开发营销视觉内容和品牌资产</li>
              <li><strong>公关部门</strong>：协调品牌信息的一致性和媒体关系</li>
              <li><strong>高层管理</strong>：汇报营销效果和市场趋势</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>市场经理的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>高级市场经理</li>
              <li>市场总监</li>
              <li>品牌总监</li>
              <li>市场营销副总裁</li>
              <li>首席营销官(CMO)</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于市场经理的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 营销文案生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-text-line"></i>
            </div>
            <div class="function-content">
              <h3>营销文案生成</h3>
              <p>快速生成针对不同产品和目标受众的营销文案，提高品牌传播效果。</p>
              <div class="function-tags">
                <span class="tag">文案</span>
                <span class="tag">营销</span>
              </div>
              <router-link to="/ai-tools/marketing-copy" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 广告语生成 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-advertisement-line"></i>
            </div>
            <div class="function-content">
              <h3>广告语生成</h3>
              <p>生成吸引人的广告标语和宣传语，用于产品推广和品牌建设。</p>
              <div class="function-tags">
                <span class="tag">广告</span>
                <span class="tag">营销</span>
              </div>
              <router-link to="/ai-tools/ad-slogan" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 公众号文章 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-wechat-line"></i>
            </div>
            <div class="function-content">
              <h3>公众号文章</h3>
              <p>生成高质量的公众号文章，满足品牌内容营销和用户互动需求。</p>
              <div class="function-tags">
                <span class="tag">内容</span>
                <span class="tag">社交媒体</span>
              </div>
              <router-link to="/ai-tools/wechat-article" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 小红书文章 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-book-open-line"></i>
            </div>
            <div class="function-content">
              <h3>小红书文章</h3>
              <p>生成符合小红书平台风格的内容，提升品牌在年轻用户群体中的曝光。</p>
              <div class="function-tags">
                <span class="tag">内容</span>
                <span class="tag">社交媒体</span>
              </div>
              <router-link to="/ai-tools/xiaohongshu-post" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 短视频脚本 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-movie-line"></i>
            </div>
            <div class="function-content">
              <h3>短视频脚本</h3>
              <p>生成适合抖音、快手等平台的短视频脚本，提升内容营销效果。</p>
              <div class="function-tags">
                <span class="tag">视频</span>
                <span class="tag">内容创作</span>
              </div>
              <router-link to="/ai-tools/short-video-script" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文生图 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-image-line"></i>
            </div>
            <div class="function-content">
              <h3>文生图</h3>
              <p>通过文字描述生成营销图片，快速创建品牌视觉内容。</p>
              <div class="function-tags">
                <span class="tag">图像</span>
                <span class="tag">视觉内容</span>
              </div>
              <router-link to="/ai-tools/text-to-image" class="use-function-btn">
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
              <p>快速生成专业的营销提案和市场分析报告PPT，提升汇报效率。</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">提案</span>
              </div>
              <router-link to="/ai-tools/ai-ppt" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 数据分析 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-bar-chart-line"></i>
            </div>
            <div class="function-content">
              <h3>数据分析</h3>
              <p>分析营销数据趋势，评估营销活动效果，优化市场投放策略。</p>
              <div class="function-tags">
                <span class="tag">数据</span>
                <span class="tag">分析</span>
              </div>
              <router-link to="/ai-tools/data-analysis" class="use-function-btn">
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
  name: 'MarketingManager',
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