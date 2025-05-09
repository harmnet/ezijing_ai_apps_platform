<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>客户主管 <span class="position-category">客户与运营类</span></h1>
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
              <li>负责建立并维护与关键客户的长期稳定合作关系</li>
              <li>深入了解客户业务需求，提供匹配的产品和解决方案</li>
              <li>制定并执行客户服务计划，确保客户满意度</li>
              <li>协调内部资源，确保客户问题得到及时有效解决</li>
              <li>收集和分析客户反馈，推动产品和服务改进</li>
              <li>定期进行客户拜访，组织客户会议和活动</li>
              <li>监控客户健康度指标，防范客户流失风险</li>
              <li>挖掘客户的增值和交叉销售机会，提升客户价值</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>出色的人际沟通和关系管理能力</li>
              <li>良好的商业敏感度和客户需求理解能力</li>
              <li>问题解决能力和冲突处理能力</li>
              <li>项目管理和时间管理能力</li>
              <li>数据分析和洞察能力</li>
              <li>谈判技巧和影响力</li>
              <li>团队协作精神和资源协调能力</li>
              <li>主动学习和适应变化的能力</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>客户主管需要与多个部门和角色密切合作：</p>
            <ul>
              <li><strong>销售团队</strong>：协作完成收入目标，共享客户信息</li>
              <li><strong>产品部门</strong>：传递客户需求，推动产品改进</li>
              <li><strong>技术支持</strong>：协调技术资源解决客户问题</li>
              <li><strong>客户成功团队</strong>：确保客户获得最佳使用体验</li>
              <li><strong>市场部门</strong>：协作开展客户活动和营销计划</li>
              <li><strong>高层管理</strong>：汇报重要客户情况和战略建议</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>客户主管的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li>高级客户主管</li>
              <li>客户成功经理</li>
              <li>客户关系总监</li>
              <li>业务发展经理</li>
              <li>客户体验总监</li>
              <li>销售总监</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于客户主管的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 文档总结 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>文档总结</h3>
              <p>快速总结客户会议记录、需求文档和反馈报告，提取关键信息</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">摘要</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- AI会议纪要 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-text-line"></i>
            </div>
            <div class="function-content">
              <h3>AI会议纪要</h3>
              <p>自动记录客户会议内容，生成结构化会议记录，跟踪行动项和决策点</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">记录</span>
              </div>
              <router-link to="/ai-office/meeting-minutes" class="use-function-btn">
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
              <p>快速生成客户汇报、产品演示和解决方案提案PPT，提升沟通效果</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">提案</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
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
              <p>分析客户使用数据和商业指标，发现趋势和洞察，优化客户策略</p>
              <div class="function-tags">
                <span class="tag">数据</span>
                <span class="tag">分析</span>
              </div>
              <router-link to="/ai-office/data-analysis" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 长文创作 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-article-line"></i>
            </div>
            <div class="function-content">
              <h3>长文创作</h3>
              <p>撰写客户案例研究、成功故事和定制化解决方案文档</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">创作</span>
              </div>
              <router-link to="/text-creation/copywriting/longform" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 合同检查 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-search-line"></i>
            </div>
            <div class="function-content">
              <h3>合同检查</h3>
              <p>AI辅助审核客户合同条款，标识潜在风险点与注意事项</p>
              <div class="function-tags">
                <span class="tag">合同</span>
                <span class="tag">风控</span>
              </div>
              <router-link to="/ai-office/legal/contract-check" class="use-function-btn">
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
              <p>创作面向客户的企业动态、产品更新和行业洞察内容，保持客户互动</p>
              <div class="function-tags">
                <span class="tag">内容</span>
                <span class="tag">营销</span>
              </div>
              <router-link to="/text-creation/new-media/wechat" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>

          <!-- 文档结构撰写 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-draft-line"></i>
            </div>
            <div class="function-content">
              <h3>文档结构撰写</h3>
              <p>生成客户服务计划、季度回顾报告和业务提案的专业结构</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">结构</span>
              </div>
              <router-link to="/text-creation/copywriting/document-structure" class="use-function-btn">
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
  name: 'CustomerManager',
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