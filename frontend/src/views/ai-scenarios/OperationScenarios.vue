<template>
  <div class="scenarios-page">
    <div class="page-header">
      <h1>市场运营常见业务场景</h1>
      <p class="description">针对市场运营工作中的常见挑战，AI可以提供高效智能的解决方案，帮助运营人员提升工作效率和决策质量。点击下方按钮，即可体验系统现有功能！</p>
    </div>

    <div class="scenarios-list">
      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-user-voice-line"></i>
          </div>
          <h3>用户洞察与分析</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">深入理解用户是市场运营的基础，但传统分析方法往往耗时且难以挖掘深层洞察。AI数据分析功能可以高效处理大量用户数据，自动识别行为模式、偏好特征和转化障碍，生成多维度的用户画像和分层分析。系统能从非结构化的用户反馈中提取关键信息，发现潜在需求和痛点，为精准运营策略提供数据支持。这帮助运营团队更深入理解目标受众，制定差异化的运营方案，提高用户参与度和转化率，实现精细化运营，大幅提升营销资源利用效率和投入产出比。</p>
          <div class="action-buttons">
            <router-link to="/ai-office/data-analysis" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用数据分析功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-line-chart-line"></i>
          </div>
          <h3>营销活动策划</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">高效的营销活动策划需要创意、数据和执行力的完美结合，但传统策划流程耗时且难以保证创意质量。AI营销策划助手可根据产品特点、目标受众和营销目标，生成完整的活动方案，包括创意主题、传播渠道、视觉元素、内容框架和执行时间表。系统会分析历史活动数据和行业成功案例，提供有针对性的策略建议，确保活动既具创意吸引力，又有可量化的效果预期。这使运营团队能够快速生成高质量的活动方案，减少头脑风暴和反复修改的时间，提高策划效率和执行成功率。</p>
          <div class="action-buttons">
            <router-link to="/text-creation/copywriting/longform" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用文案生成功能
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-global-line"></i>
          </div>
          <h3>社媒内容创作</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">优质的社媒内容是品牌声量和用户互动的关键，但持续产出高质量、多样化的内容对运营团队是巨大挑战。AI社媒内容创作功能根据不同平台特性（如微信公众号、小红书、抖音等）自动生成符合平台调性的内容。系统能创作多种形式的内容，从图文文案到短视频脚本，从种草文章到话题互动，同时保持品牌语调一致性和内容新鲜度。这大大减轻了运营团队的创作压力，确保内容发布频率和质量，提高社媒账号活跃度和粉丝互动率，使品牌社媒矩阵运营更加高效专业。</p>
          <div class="action-buttons">
            <router-link to="/text-creation/new-media/xiaohongshu" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用小红书文案生成
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-wechat-line"></i>
          </div>
          <h3>公众号文章创作</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">微信公众号是品牌内容营销的重要阵地，但持续输出高质量、有深度的文章对内容创作者要求很高。AI公众号文章生成功能可以根据文章主题、目标读者和传播目的，创作结构完整、层次分明的专业文章。系统会自动构建文章框架，生成引人入胜的开头和有力的结尾，充实中间论述部分，并添加适当的数据支持、案例分析和图片建议。生成的文章不仅传递核心信息，还能符合微信平台的传播规律，提高阅读和分享意愿。这为运营团队提供了强大的内容生产工具，大幅提高公众号运营效率和内容质量。</p>
          <div class="action-buttons">
            <router-link to="/text-creation/new-media/wechat" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用公众号文章生成
            </router-link>
          </div>
        </div>
      </div>

      <div class="scenario-item">
        <div class="scenario-header">
          <div class="scenario-icon">
            <i class="ri-video-line"></i>
          </div>
          <h3>短视频内容策划</h3>
        </div>
        <div class="scenario-content">
          <p class="scenario-desc">短视频已成为当代营销的主流形式，但创作能吸引眼球且有传播力的短视频内容需要专业技能和创意灵感。AI短视频脚本生成功能可以根据营销目标、产品特点和目标平台，创作结构完整、节奏紧凑的视频脚本。系统会设计引人入胜的开场钩子、清晰的产品展示、有说服力的价值传达和强有力的行动召唤，形成完整的短视频叙事结构。同时考虑不同平台（如抖音、快手、视频号）的内容特性和用户喜好，优化脚本的传播效果。这使运营团队能够快速产出专业的短视频策划方案，大大缩短内容创作周期，提高视频营销效率。</p>
          <div class="action-buttons">
            <router-link to="/text-creation/new-media/short-video-script" class="action-button">
              <i class="ri-arrow-right-line"></i> 使用短视频脚本生成
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OperationScenarios'
}
</script>

<style scoped>
.scenarios-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 48px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.page-header .description {
  font-size: 16px;
  color: #666;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.scenarios-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.scenario-item {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
}

.scenario-header {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: rgba(186, 0, 63, 0.05);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.scenario-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background-color: #ba003f;
  margin-right: 16px;
}

.scenario-icon i {
  font-size: 24px;
  color: #fff;
}

.scenario-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.scenario-content {
  padding: 24px;
}

.scenario-desc {
  font-size: 16px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 24px;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
}

.action-button {
  display: inline-flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #ba003f;
  color: white;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #9a0035;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.2);
}

.action-button i {
  margin-right: 6px;
}
</style> 