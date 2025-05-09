<template>
  <div class="case-background" id="marketing-plan">
    <h2 class="section-title">产品市场营销策划</h2>
    
    <div class="background-content">
      <!-- 营销策划知识 -->
      <div class="content-block">
        <h3>营销策划的定义</h3>
        <p>营销策划（Marketing Planning）是指企业根据市场环境和自身条件，为实现营销目标而制定的系统性行动方案。它是将营销理念转化为具体执行措施的过程，涵盖市场分析、目标设定、策略制定和战术实施等多个环节。有效的营销策划能够帮助企业明确市场定位、优化资源配置、提高营销效率，并最终实现销售目标和品牌建设。</p>
        <p>从策略层面，营销策划包含对目标市场、竞争策略、品牌定位和营销组合（产品、价格、渠道、促销）的规划；从执行层面，则涉及具体营销活动的设计、资源分配、时间安排和效果评估等内容。</p>
      </div>
      
      <div class="content-block">
        <h3>「0糖」系列营销目标</h3>
        <p>根据前期的市场调研和用户画像分析，「0糖」系列的营销目标设定为：</p>
        <ul class="challenge-list">
          <li><span class="highlight">品牌知名度目标</span> - 6个月内将产品知名度从0提升至40%，品牌偏好度达到25%</li>
          <li><span class="highlight">销售业绩目标</span> - 实现首年销售目标3亿元，其中线上销售占比35%</li>
          <li><span class="highlight">渠道覆盖目标</span> - 实体零售特别是新零售渠道铺货率达到60%</li>
          <li><span class="highlight">品牌形象目标</span> - 构建"健康生活方式倡导者"的品牌形象，使目标消费者对产品核心卖点的认知率达到70%</li>
          <li><span class="highlight">用户转化目标</span> - 试饮用户的复购率达到30%，品牌忠诚度提升15%</li>
        </ul>
      </div>
      
      <div class="content-block">
        <h3>营销策略框架</h3>
        <p>基于对市场环境和目标消费者的深入分析，「0糖」系列的营销策略框架构建如下：</p>
        <div class="marketing-framework">
          <div class="framework-item">
            <div class="framework-icon">🎯</div>
            <div class="framework-content">
              <h4>目标市场聚焦</h4>
              <p>将主要营销资源集中于25-35岁的都市白领和健身爱好者等核心消费群体，通过精准定位提高营销效率。</p>
            </div>
          </div>
          <div class="framework-item">
            <div class="framework-icon">🔍</div>
            <div class="framework-content">
              <h4>差异化战略</h4>
              <p>突出"甜感平衡技术"的独特优势，强调"健康无糖不减口感"的产品差异化卖点，区别于市场上其他无糖饮料。</p>
            </div>
          </div>
          <div class="framework-item">
            <div class="framework-icon">📣</div>
            <div class="framework-content">
              <h4>整合营销传播</h4>
              <p>线上线下多渠道协同推广，结合社交媒体、KOL合作、线下活动等多种方式，形成传播合力。</p>
            </div>
          </div>
          <div class="framework-item">
            <div class="framework-icon">🤝</div>
            <div class="framework-content">
              <h4>场景化营销</h4>
              <p>围绕办公、健身、社交等关键消费场景设计营销活动，提高品牌与消费者生活方式的关联度。</p>
            </div>
          </div>
          <div class="framework-item">
            <div class="framework-icon">📊</div>
            <div class="framework-content">
              <h4>数据驱动优化</h4>
              <p>建立营销效果监测体系，通过实时数据分析持续优化营销策略和资源分配。</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- AI辅助营销策划工具 -->
      <div class="content-block highlight-block">
        <h3>AI辅助营销策划工具</h3>
        <p>现代营销策划已经可以借助AI工具显著提升效率和创意水平。针对「0糖」系列的营销策划，我们可以利用紫荆AI平台提供的以下工具：</p>
        
        <div class="ai-tools-section">
          <div class="tools-category">
            <h4>内容创作效率提升</h4>
            <div class="tool-cards">
              <div class="tool-card" @click="navigateTo('广告语创作', '/text-creation/marketing/ad-slogan')">
                <div class="tool-icon">✏️</div>
                <div class="tool-info">
                  <h5>广告语创作</h5>
                  <p>快速生成吸引人的产品广告语和宣传口号，突出"0糖"产品特性</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('营销文案创作', '/text-creation/marketing/copywriting-generator')">
                <div class="tool-icon">📝</div>
                <div class="tool-info">
                  <h5>营销文案创作</h5>
                  <p>生成产品详情页、宣传册等营销文本，全面展示产品优势</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('公众号创作', '/text-creation/new-media/wechat')">
                <div class="tool-icon">📱</div>
                <div class="tool-info">
                  <h5>公众号创作</h5>
                  <p>创作关于健康生活方式、无糖饮品的专业公众号内容</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
            </div>
          </div>
          
          <div class="tools-category">
            <h4>视觉创意效率提升</h4>
            <div class="tool-cards">
              <div class="tool-card" @click="navigateTo('智能商品图设计', '/image-creation/image-to-painter')">
                <div class="tool-icon">🖼️</div>
                <div class="tool-info">
                  <h5>智能商品图设计</h5>
                  <p>为「0糖」系列产品创建专业的商品图，突出产品包装设计</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('文生图', '/image-creation/text-to-image')">
                <div class="tool-icon">🎨</div>
                <div class="tool-info">
                  <h5>文生图</h5>
                  <p>根据营销文案创建相关的视觉内容，支持社交媒体传播</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('在线图形设计', '/image-creation/online-design')">
                <div class="tool-icon">📊</div>
                <div class="tool-info">
                  <h5>在线图形设计</h5>
                  <p>设计营销宣传材料、海报和banner等营销图形</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
            </div>
          </div>
          
          <div class="tools-category">
            <h4>视频内容创作</h4>
            <div class="tool-cards">
              <div class="tool-card" @click="navigateTo('文生视频', '/video-creation/text-to-video')">
                <div class="tool-icon">🎬</div>
                <div class="tool-info">
                  <h5>文生视频</h5>
                  <p>根据产品描述和广告文案生成简短的产品宣传视频</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
              <div class="tool-card" @click="navigateTo('数字人视频制作', '/digital-human/video-creation')">
                <div class="tool-icon">👤</div>
                <div class="tool-info">
                  <h5>数字人视频制作</h5>
                  <p>创建数字代言人介绍产品特点和健康价值</p>
                </div>
                <div class="tool-action">使用</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 示例营销策划案例 -->
      <div class="content-block">
        <h3>「0糖」系列典型营销场景设计</h3>
        <p>基于目标用户画像和产品特性，我们为「0糖」系列设计了以下典型营销场景：</p>
        
        <div class="marketing-scenarios">
          <div class="scenario-card">
            <div class="scenario-header">
              <div class="scenario-icon">💼</div>
              <h4>办公场景营销</h4>
            </div>
            <div class="scenario-content">
              <h5>目标：打造办公室健康饮品首选</h5>
              <div class="scenario-tactics">
                <div class="tactic-item">
                  <span class="tactic-label">传播渠道：</span>
                  <span class="tactic-content">企业福利渠道、办公大楼广告、社交媒体职场话题</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">核心卖点：</span>
                  <span class="tactic-content">零糖零负担，保持清醒专注力，健康办公新选择</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">营销活动：</span>
                  <span class="tactic-content">"办公活力加油站"—企业白领试饮活动，提供免费样品和健康饮品指南</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">推荐AI工具：</span>
                  <span class="tactic-content">
                    <a class="tool-link" @click="navigateTo('公众号创作', '/text-creation/new-media/wechat')">公众号创作</a>
                    <a class="tool-link" @click="navigateTo('营销文案创作', '/text-creation/marketing/copywriting-generator')">营销文案创作</a>
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="scenario-card">
            <div class="scenario-header">
              <div class="scenario-icon">🏋️‍♀️</div>
              <h4>健身场景营销</h4>
            </div>
            <div class="scenario-content">
              <h5>目标：成为健身爱好者的运动饮品伙伴</h5>
              <div class="scenario-tactics">
                <div class="tactic-item">
                  <span class="tactic-label">传播渠道：</span>
                  <span class="tactic-content">健身房合作、运动APP广告、健身KOL代言</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">核心卖点：</span>
                  <span class="tactic-content">零糖不长肉，自然健康成分，运动补充好选择</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">营销活动：</span>
                  <span class="tactic-content">"健身零负担挑战"—与健身社群合作的21天健康饮品打卡活动</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">推荐AI工具：</span>
                  <span class="tactic-content">
                    <a class="tool-link" @click="navigateTo('小红书笔记创作', '/text-creation/new-media/xiaohongshu')">小红书笔记创作</a>
                    <a class="tool-link" @click="navigateTo('智能图形设计', '/image-creation/intelligent-design')">智能图形设计</a>
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="scenario-card">
            <div class="scenario-header">
              <div class="scenario-icon">🥂</div>
              <h4>社交场景营销</h4>
            </div>
            <div class="scenario-content">
              <h5>目标：打造年轻人社交聚会时尚饮品</h5>
              <div class="scenario-tactics">
                <div class="tactic-item">
                  <span class="tactic-label">传播渠道：</span>
                  <span class="tactic-content">社交媒体话题、娱乐场所合作、时尚活动赞助</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">核心卖点：</span>
                  <span class="tactic-content">时尚潮流饮品，健康不发胖，品味生活新方式</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">营销活动：</span>
                  <span class="tactic-content">"0糖漂流瓶"—社交媒体创意分享活动，鼓励用户创造0糖饮品的创意混搭</span>
                </div>
                <div class="tactic-item">
                  <span class="tactic-label">推荐AI工具：</span>
                  <span class="tactic-content">
                    <a class="tool-link" @click="navigateTo('短视频脚本创作', '/text-creation/new-media/short-video')">短视频脚本创作</a>
                    <a class="tool-link" @click="navigateTo('文生视频', '/video-creation/text-to-video')">文生视频</a>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 营销策划制作工具 -->
      <div class="content-block">
        <h3>互动式营销策划工具</h3>
        <p>使用下面的工具，快速生成「0糖」系列产品的营销策划方案。根据您的营销目标和偏好，AI将为您定制专业的营销策略。</p>
        
        <div class="marketing-plan-maker">
          <div class="plan-form">
            <div class="form-section">
              <h4>步骤1：设定营销目标</h4>
              <div class="form-group">
                <label>选择主要营销目标 <span class="required">*</span></label>
                <div class="checkbox-group">
                  <div class="checkbox-item" v-for="(goal, index) in marketingGoals" :key="index">
                    <input type="checkbox" :id="'goal-' + index" v-model="selectedGoals" :value="goal">
                    <label :for="'goal-' + index">{{ goal }}</label>
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <label>预期营销周期 <span class="required">*</span></label>
                <div class="radio-group">
                  <div class="radio-item" v-for="(period, index) in marketingPeriods" :key="index">
                    <input type="radio" :id="'period-' + index" v-model="selectedPeriod" :value="period">
                    <label :for="'period-' + index">{{ period }}</label>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="form-section">
              <h4>步骤2：选择营销渠道</h4>
              <div class="form-group">
                <label>主要营销渠道 <span class="required">*</span></label>
                <div class="checkbox-group channels-group">
                  <div class="checkbox-item" v-for="(channel, index) in marketingChannels" :key="index">
                    <input type="checkbox" :id="'channel-' + index" v-model="selectedChannels" :value="channel">
                    <label :for="'channel-' + index">{{ channel }}</label>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="form-section">
              <h4>步骤3：营销亮点</h4>
              <div class="form-group">
                <label>产品主要卖点 <span class="required">*</span></label>
                <textarea 
                  v-model="productSellingPoints" 
                  placeholder="描述产品的主要卖点和差异化优势..." 
                  rows="3"></textarea>
              </div>
              
              <div class="form-group">
                <label>目标受众特征 <span class="required">*</span></label>
                <textarea 
                  v-model="targetAudience" 
                  placeholder="描述您的目标受众的特征..." 
                  rows="3"></textarea>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button class="reset-btn" @click="resetPlanForm">
              <span>🔄</span> 重置
            </button>
            <button class="generate-btn" @click="generateMarketingPlan" :disabled="!isPlanFormValid">
              <span>✨</span> 生成营销策划
            </button>
          </div>
          
          <!-- 生成的策划方案 -->
          <div class="plan-result" v-if="showPlanResult">
            <h4>「0糖」系列产品营销策划方案</h4>
            <div class="plan-detail">
              <div class="plan-summary">
                <div class="summary-icon">📋</div>
                <div class="summary-content">
                  <h5>策划概述</h5>
                  <p>基于您选择的营销目标和渠道，以下是为「0糖」系列定制的营销策划方案，突出产品的无糖健康特性以及目标受众需求。</p>
                </div>
              </div>
              
              <div class="plan-section">
                <h5>营销目标</h5>
                <ul class="section-list">
                  <li v-for="(goal, index) in selectedGoals" :key="index">{{ goal }}</li>
                </ul>
              </div>
              
              <div class="plan-section">
                <h5>核心策略</h5>
                <p>{{ generatedCoreStrategy }}</p>
              </div>
              
              <div class="plan-section">
                <h5>渠道策略</h5>
                <div class="channel-strategies">
                  <div class="channel-card" v-for="(channel, index) in selectedChannels" :key="index">
                    <div class="channel-name">{{ channel }}</div>
                    <div class="channel-tactic">{{ getChannelTactic(channel) }}</div>
                  </div>
                </div>
              </div>
              
              <div class="plan-section">
                <h5>创意亮点</h5>
                <p>{{ generatedCreativeHighlight }}</p>
              </div>
              
              <div class="plan-section">
                <h5>执行时间表</h5>
                <div class="timeline">
                  <div class="timeline-item" v-for="(phase, index) in marketingPhases" :key="index">
                    <div class="timeline-point"></div>
                    <div class="timeline-content">
                      <div class="phase-title">{{ phase.title }}</div>
                      <div class="phase-desc">{{ phase.description }}</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="plan-section ai-tools-recommendations">
                <h5>推荐的AI工具</h5>
                <div class="tool-cards small">
                  <div class="tool-card" v-for="(tool, index) in recommendedTools" :key="index" @click="navigateTo(tool.name, tool.path)">
                    <div class="tool-icon">{{ tool.icon }}</div>
                    <div class="tool-info">
                      <h5>{{ tool.name }}</h5>
                      <p>{{ tool.description }}</p>
                    </div>
                    <div class="tool-action">使用</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="plan-actions">
              <button class="download-btn" @click="downloadMarketingPlan">
                <span>📥</span> 下载完整方案
              </button>
              <button class="share-btn" @click="showShareModal = true">
                <span>🔗</span> 分享方案
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 营销效果分析 -->
      <div class="content-block">
        <h3>营销效果评估</h3>
        <p>有效的营销策划必须建立科学的效果评估机制。针对「0糖」系列，我们设计了以下关键指标体系：</p>
        
        <div class="metrics-table">
          <div class="table-row header">
            <div class="cell">指标类别</div>
            <div class="cell">关键指标</div>
            <div class="cell">监测方法</div>
            <div class="cell">目标值</div>
          </div>
          <div class="table-row">
            <div class="cell category">品牌影响力</div>
            <div class="cell">
              <span>品牌知名度</span>
              <span>品牌好感度</span>
              <span>社交媒体声量</span>
            </div>
            <div class="cell">
              <span>市场调研</span>
              <span>NPS调查</span>
              <span>社媒监测工具</span>
            </div>
            <div class="cell">
              <span>40%</span>
              <span>35分</span>
              <span>50万+提及</span>
            </div>
          </div>
          <div class="table-row">
            <div class="cell category">销售业绩</div>
            <div class="cell">
              <span>销售额</span>
              <span>市场份额</span>
              <span>渠道覆盖率</span>
            </div>
            <div class="cell">
              <span>销售系统</span>
              <span>市场报告</span>
              <span>渠道统计</span>
            </div>
            <div class="cell">
              <span>3亿元</span>
              <span>5%</span>
              <span>60%</span>
            </div>
          </div>
          <div class="table-row">
            <div class="cell category">用户行为</div>
            <div class="cell">
              <span>试用转化率</span>
              <span>复购率</span>
              <span>用户活跃度</span>
            </div>
            <div class="cell">
              <span>会员系统</span>
              <span>消费数据</span>
              <span>APP互动</span>
            </div>
            <div class="cell">
              <span>30%</span>
              <span>25%</span>
              <span>45%</span>
            </div>
          </div>
          <div class="table-row">
            <div class="cell category">营销效率</div>
            <div class="cell">
              <span>营销ROI</span>
              <span>客户获取成本</span>
              <span>内容互动率</span>
            </div>
            <div class="cell">
              <span>财务分析</span>
              <span>营销支出/新客户</span>
              <span>平台数据</span>
            </div>
            <div class="cell">
              <span>3.5:1</span>
              <span>≤30元</span>
              <span>4.5%</span>
            </div>
          </div>
        </div>
        
        <div class="ai-analysis-tip">
          <div class="tip-icon">💡</div>
          <div class="tip-content">
            <h4>AI辅助营销分析</h4>
            <p>使用<a class="tool-link" @click="navigateTo('智能数据分析', '/ai-office/data-analysis')">智能数据分析</a>工具，可将营销数据转化为可视化报表和洞察，帮助持续优化营销策略。</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分享模态框 -->
    <div class="share-modal" v-if="showShareModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>分享营销策划方案</h3>
          <button class="close-btn" @click="showShareModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="share-options">
            <div class="share-option" @click="shareVia('微信')">
              <div class="option-icon">📱</div>
              <div class="option-name">微信</div>
            </div>
            <div class="share-option" @click="shareVia('邮件')">
              <div class="option-icon">✉️</div>
              <div class="option-name">邮件</div>
            </div>
            <div class="share-option" @click="shareVia('链接')">
              <div class="option-icon">🔗</div>
              <div class="option-name">复制链接</div>
            </div>
            <div class="share-option" @click="shareVia('二维码')">
              <div class="option-icon">📷</div>
              <div class="option-name">二维码</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 营销目标选项
const marketingGoals = [
  '提高品牌知名度和曝光度',
  '增加产品销售和市场份额',
  '树立健康饮品的品牌形象',
  '吸引并留住目标消费群体',
  '提高用户忠诚度和复购率'
];

// 营销周期选项
const marketingPeriods = [
  '短期（1-3个月）',
  '中期（3-6个月）',
  '长期（6-12个月）'
];

// 营销渠道选项
const marketingChannels = [
  '社交媒体营销',
  '内容营销',
  '关键意见领袖(KOL)合作',
  '线下活动与体验',
  '电商平台推广',
  '传统媒体广告',
  '搜索引擎营销'
];

// 表单数据
const selectedGoals = ref([]);
const selectedPeriod = ref('');
const selectedChannels = ref([]);
const productSellingPoints = ref('');
const targetAudience = ref('');

// 营销策划结果
const showPlanResult = ref(false);
const generatedCoreStrategy = ref('');
const generatedCreativeHighlight = ref('');
const marketingPhases = ref([]);
const recommendedTools = ref([]);

// 分享模态框
const showShareModal = ref(false);

// 表单验证
const isPlanFormValid = computed(() => {
  return selectedGoals.value.length > 0 && 
         selectedPeriod.value && 
         selectedChannels.value.length > 0 && 
         productSellingPoints.value.trim() !== '' && 
         targetAudience.value.trim() !== '';
});

// 生成营销策划
const generateMarketingPlan = () => {
  if (!isPlanFormValid.value) {
    alert('请完成所有必填字段后再生成营销策划！');
    return;
  }
  
  // 生成核心策略
  const strategyTemplates = [
    `通过${selectedChannels.value.slice(0, 2).join('和')}渠道，重点突出"0糖"产品的健康特性和口感优势，针对${targetAudience.value.slice(0, 20)}人群，打造差异化健康饮品形象。`,
    `采用整合营销传播策略，结合${selectedChannels.value.slice(0, 2).join('和')}，强化"0糖不减口感"的产品卖点，建立与目标消费者的情感连接。`,
    `以"健康生活方式"为核心理念，通过${selectedChannels.value.slice(0, 2).join('和')}渠道，传递产品价值，满足${targetAudience.value.slice(0, 20)}人群的健康饮品需求。`
  ];
  generatedCoreStrategy.value = strategyTemplates[Math.floor(Math.random() * strategyTemplates.length)];
  
  // 生成创意亮点
  const creativeTemplates = [
    `"零糖生活挑战"活动，鼓励消费者分享使用"0糖"产品的健康生活方式，通过社交媒体创造话题传播。`,
    `与健身、瑜伽等健康生活方式KOL合作，推出"健康饮品搭配指南"内容系列，提供专业饮品选择建议。`,
    `打造"0糖实验室"创意互动体验区，让消费者亲身体验不含糖也能保持美味的产品特性，增强品牌记忆。`
  ];
  generatedCreativeHighlight.value = creativeTemplates[Math.floor(Math.random() * creativeTemplates.length)];
  
  // 生成执行时间表
  generateMarketingPhases();
  
  // 生成推荐工具
  generateRecommendedTools();
  
  // 显示结果
  showPlanResult.value = true;
};

// 获取渠道策略
const getChannelTactic = (channel) => {
  const tactics = {
    '社交媒体营销': '通过抖音、小红书等平台创建"0糖生活"话题，鼓励用户分享健康饮品搭配创意。',
    '内容营销': '制作"无糖生活指南"系列内容，包括健康饮食知识、无糖饮品搭配方案等专业内容。',
    '关键意见领袖(KOL)合作': '与健身、健康生活方式KOL合作，展示"0糖"产品在日常生活中的应用场景。',
    '线下活动与体验': '在商场、健身中心举办"0糖体验站"，提供产品试饮和健康生活方式咨询。',
    '电商平台推广': '在各大电商平台开展限时特惠、新品首发等活动，提高产品曝光和转化。',
    '传统媒体广告': '在地铁、电梯等高流量场所投放产品广告，强调"零糖不减口感"的产品卖点。',
    '搜索引擎营销': '优化关键词策略，确保用户搜索"健康饮品"、"无糖饮料"等词时能看到产品信息。'
  };
  
  return tactics[channel] || '定制化渠道推广策略，最大化营销效果。';
};

// 生成营销阶段
const generateMarketingPhases = () => {
  if (selectedPeriod.value.includes('短期')) {
    marketingPhases.value = [
      { title: '第1-2周: 准备阶段', description: '完成营销物料制作、渠道铺设和KOL合作洽谈' },
      { title: '第3-6周: 启动阶段', description: '产品正式上市，启动社交媒体和KOL营销活动' },
      { title: '第7-10周: 强化阶段', description: '根据初期反馈优化策略，加强渠道推广力度' },
      { title: '第11-12周: 评估阶段', description: '收集数据，评估营销效果，为下阶段做准备' }
    ];
  } else if (selectedPeriod.value.includes('中期')) {
    marketingPhases.value = [
      { title: '第1个月: 市场导入', description: '产品上市，启动全渠道推广，建立品牌初始认知' },
      { title: '第2-3个月: 市场培育', description: '深化渠道合作，举办线下体验活动，强化产品差异化优势' },
      { title: '第4-5个月: 市场扩展', description: '拓展更多销售渠道，推出会员激励计划，提高用户留存' },
      { title: '第6个月: 效果评估', description: '全面评估营销效果，优化长期策略' }
    ];
  } else {
    marketingPhases.value = [
      { title: '第1-2个月: 品牌建立', description: '产品上市，全渠道营销启动，建立初始品牌形象' },
      { title: '第3-5个月: 市场渗透', description: '扩大渠道覆盖，增加产品曝光，提高市场渗透率' },
      { title: '第6-8个月: 品牌强化', description: '深化品牌理念传播，推出衍生产品，增强用户粘性' },
      { title: '第9-11个月: 市场巩固', description: '优化产品结构，细分市场策略，提高市场份额' },
      { title: '第12个月: 战略调整', description: '全面评估年度营销效果，制定下一年度营销战略' }
    ];
  }
};

// 生成推荐工具
const generateRecommendedTools = () => {
  const allTools = [
    { name: '广告语创作', path: '/text-creation/marketing/ad-slogan', icon: '✏️', description: '为"0糖"系列创建吸引人的广告语和宣传口号' },
    { name: '营销文案创作', path: '/text-creation/marketing/copywriting-generator', icon: '📝', description: '生成产品详情页和宣传资料的专业营销文案' },
    { name: '公众号创作', path: '/text-creation/new-media/wechat', icon: '📱', description: '创建"0糖"产品的健康生活方式公众号内容' },
    { name: '小红书笔记创作', path: '/text-creation/new-media/xiaohongshu', icon: '📔', description: '生成适合小红书平台的种草笔记和推广内容' },
    { name: '短视频脚本创作', path: '/text-creation/new-media/short-video', icon: '🎬', description: '编写引人入胜的短视频营销脚本' },
    { name: '文生图', path: '/image-creation/text-to-image', icon: '🎨', description: '根据营销文案生成相关的视觉创意内容' },
    { name: '智能图形设计', path: '/image-creation/intelligent-design', icon: '🖌️', description: '设计"0糖"产品的营销海报和宣传图' },
    { name: '文生视频', path: '/video-creation/text-to-video', icon: '🎥', description: '将营销文案转化为短视频内容' }
  ];
  
  // 根据选择的渠道和目标，推荐相关工具
  const toolSet = new Set();
  
  if (selectedChannels.value.includes('社交媒体营销')) {
    toolSet.add('小红书笔记创作');
    toolSet.add('短视频脚本创作');
    toolSet.add('文生图');
  }
  
  if (selectedChannels.value.includes('内容营销')) {
    toolSet.add('公众号创作');
    toolSet.add('营销文案创作');
  }
  
  if (selectedChannels.value.includes('电商平台推广')) {
    toolSet.add('智能商品图设计');
    toolSet.add('广告语创作');
  }
  
  // 确保至少有3个推荐工具
  const selectedToolNames = Array.from(toolSet);
  while (selectedToolNames.length < 3) {
    const randomTool = allTools[Math.floor(Math.random() * allTools.length)].name;
    if (!selectedToolNames.includes(randomTool)) {
      selectedToolNames.push(randomTool);
    }
  }
  
  // 限制最多5个工具
  const limitedToolNames = selectedToolNames.slice(0, 5);
  
  // 从allTools中找出对应的完整工具信息
  recommendedTools.value = allTools.filter(tool => limitedToolNames.includes(tool.name));
};

// 重置表单
const resetPlanForm = () => {
  selectedGoals.value = [];
  selectedPeriod.value = '';
  selectedChannels.value = [];
  productSellingPoints.value = '';
  targetAudience.value = '';
  showPlanResult.value = false;
};

// 导航到工具页面
const navigateTo = (toolName, path) => {
  alert(`即将跳转到"${toolName}"工具，实际环境中将导航到: http://localhost:8018${path}`);
  // 实际环境中应该使用路由导航
  // router.push(path);
};

// 下载营销策划
const downloadMarketingPlan = () => {
  alert('营销策划方案下载功能尚未实现');
};

// 分享营销策划
const shareVia = (method) => {
  alert(`通过${method}分享功能尚未实现`);
  showShareModal.value = false;
};
</script>

<style scoped>
.case-background {
  margin-bottom: 60px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
  position: relative;
  padding-bottom: 15px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: #c62828; /* 紫荆红 */
}

.background-content {
  display: flex;
  flex-direction: column;
}

.content-block {
  margin-bottom: 30px;
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.content-block h3 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 18px;
  color: #333;
  position: relative;
  padding-bottom: 10px;
}

.content-block h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background-color: #c62828; /* 紫荆红 */
}

.content-block p {
  font-size: 16px;
  line-height: 1.7;
  color: #444;
  margin-bottom: 15px;
}

.highlight-block {
  background-color: #fff9f9;
  border-left: 4px solid #c62828;
}

.challenge-list {
  padding-left: 0;
  list-style-type: none;
  margin-bottom: 20px;
}

.challenge-list li {
  margin-bottom: 12px;
  line-height: 1.6;
  font-size: 15px;
  color: #444;
  padding-left: 25px;
  position: relative;
}

.highlight {
  color: #c62828;
  font-weight: 600;
  margin-right: 5px;
}

/* 营销框架 */
.marketing-framework {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 25px;
}

.framework-item {
  display: flex;
  align-items: flex-start;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.framework-icon {
  font-size: 24px;
  margin-right: 15px;
  min-width: 24px;
}

.framework-content {
  flex: 1;
}

.framework-content h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.framework-content p {
  font-size: 15px;
  color: #555;
  margin: 0;
  line-height: 1.5;
}

/* AI工具部分 */
.ai-tools-section {
  margin-top: 25px;
}

.tools-category {
  margin-bottom: 25px;
}

.tools-category h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.tool-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.tool-cards.small {
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}

.tool-card {
  display: flex;
  align-items: center;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.tool-card:hover {
  background-color: #f0f4ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-color: #4a6fe3;
}

.tool-icon {
  font-size: 24px;
  margin-right: 12px;
  min-width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-info {
  flex: 1;
}

.tool-info h5 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.tool-info p {
  font-size: 13px;
  color: #666;
  margin: 0;
  line-height: 1.4;
}

.tool-action {
  color: #4a6fe3;
  font-size: 14px;
  font-weight: 600;
  padding: 5px 10px;
  border: 1px solid #4a6fe3;
  border-radius: 4px;
  opacity: 0.8;
  transition: all 0.2s;
}

.tool-card:hover .tool-action {
  opacity: 1;
  background-color: #4a6fe3;
  color: white;
}

/* 营销场景 */
.marketing-scenarios {
  margin-top: 25px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.scenario-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.scenario-header {
  background-color: #4a6fe3;
  color: white;
  padding: 15px;
  display: flex;
  align-items: center;
}

.scenario-icon {
  font-size: 24px;
  margin-right: 12px;
}

.scenario-header h4 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.scenario-content {
  padding: 15px;
}

.scenario-content h5 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
}

.scenario-tactics {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tactic-item {
  display: flex;
  align-items: flex-start;
  font-size: 14px;
  line-height: 1.5;
}

.tactic-label {
  font-weight: 600;
  color: #444;
  min-width: 80px;
  margin-right: 8px;
}

.tactic-content {
  color: #555;
  flex: 1;
}

.tool-link {
  color: #4a6fe3;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  margin-right: 10px;
}

.tool-link:hover {
  text-decoration: underline;
}

/* 营销策划工具 */
.marketing-plan-maker {
  margin-top: 25px;
}

.plan-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.form-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
}

.form-section h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.required {
  color: #c62828;
  margin-left: 3px;
}

.checkbox-group, .radio-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.channels-group {
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
}

.checkbox-item, .radio-item {
  display: flex;
  align-items: center;
}

.checkbox-item input, .radio-item input {
  margin-right: 8px;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 25px;
}

.generate-btn, .reset-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s;
}

.generate-btn {
  background-color: #4a6fe3;
  color: white;
}

.generate-btn:hover {
  background-color: #3b5dd1;
}

.generate-btn:disabled {
  background-color: #b8c2cc;
  cursor: not-allowed;
}

.reset-btn {
  background-color: #f0f0f0;
  color: #666;
}

.reset-btn:hover {
  background-color: #e0e0e0;
}

.generate-btn span, .reset-btn span {
  margin-right: 8px;
}

/* 策划结果 */
.plan-result {
  margin-top: 40px;
  border-top: 1px dashed #ddd;
  padding-top: 25px;
}

.plan-result h4 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.plan-detail {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 25px;
}

.plan-summary {
  display: flex;
  align-items: flex-start;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.summary-icon {
  font-size: 28px;
  margin-right: 15px;
}

.summary-content {
  flex: 1;
}

.summary-content h5 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

.summary-content p {
  font-size: 15px;
  color: #555;
  line-height: 1.6;
  margin: 0;
}

.plan-section {
  margin-bottom: 25px;
}

.plan-section h5 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
  display: flex;
  align-items: center;
}

.section-list {
  padding-left: 20px;
}

.section-list li {
  margin-bottom: 8px;
  font-size: 14px;
  color: #555;
}

.channel-strategies {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.channel-card {
  background-color: white;
  border-radius: 6px;
  padding: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.channel-name {
  font-weight: 600;
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
}

.channel-tactic {
  font-size: 13px;
  color: #555;
  line-height: 1.5;
}

.timeline {
  position: relative;
  margin-left: 20px;
}

.timeline:before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 7px;
  width: 2px;
  background-color: #d1d8e0;
}

.timeline-item {
  position: relative;
  padding-left: 30px;
  margin-bottom: 20px;
}

.timeline-point {
  position: absolute;
  top: 3px;
  left: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #4a6fe3;
  z-index: 1;
}

.phase-title {
  font-weight: 600;
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
}

.phase-desc {
  font-size: 13px;
  color: #555;
  line-height: 1.5;
}

.ai-tools-recommendations {
  margin-top: 30px;
}

.plan-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 25px;
}

.download-btn, .share-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s;
}

.download-btn {
  background-color: #2ecc71;
  color: white;
}

.download-btn:hover {
  background-color: #27ae60;
}

.share-btn {
  background-color: #3498db;
  color: white;
}

.share-btn:hover {
  background-color: #2980b9;
}

.download-btn span, .share-btn span {
  margin-right: 8px;
}

/* 营销效果评估表格 */
.metrics-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1.5fr 1fr;
}

.table-row.header {
  background-color: #4a6fe3;
  color: white;
}

.table-row:nth-child(even):not(.header) {
  background-color: #f5f7ff;
}

.table-row:nth-child(odd):not(.header) {
  background-color: white;
}

.cell {
  padding: 12px 15px;
  font-size: 14px;
  border: 1px solid #e0e6ed;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.cell.category {
  font-weight: 600;
  color: #333;
}

.table-row.header .cell {
  font-weight: 600;
  border-color: #4a6fe3;
}

.cell span {
  margin-bottom: 5px;
}

.ai-analysis-tip {
  margin-top: 25px;
  display: flex;
  align-items: flex-start;
  background-color: #f0f4ff;
  border-radius: 8px;
  padding: 15px;
}

.tip-icon {
  font-size: 24px;
  margin-right: 15px;
}

.tip-content {
  flex: 1;
}

.tip-content h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.tip-content p {
  font-size: 14px;
  color: #555;
  margin: 0;
}

/* 分享模态框 */
.share-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 20px;
}

.share-options {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.share-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f5f7ff;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.share-option:hover {
  background-color: #e6ecff;
  transform: translateY(-2px);
}

.option-icon {
  font-size: 28px;
  margin-bottom: 10px;
}

.option-name {
  font-size: 14px;
  color: #333;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .tool-cards, .marketing-scenarios, .channel-strategies {
    grid-template-columns: 1fr;
  }
  
  .table-row {
    grid-template-columns: 1fr;
  }
  
  .table-row.header {
    display: none;
  }
  
  .cell.category {
    background-color: #f0f4ff;
  }
  
  .share-options {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style> 