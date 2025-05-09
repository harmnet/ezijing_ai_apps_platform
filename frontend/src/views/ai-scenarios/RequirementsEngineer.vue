<template>
  <div class="position-detail-container">
    <!-- 页面头部 -->
    <div class="position-header">
      <div class="container">
        <div class="back-link" @click="goBack">
          <i class="ri-arrow-left-line"></i> 返回职务列表
        </div>
        <h1>需求工程师 <span class="position-category">产品与研发类</span></h1>
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
              <li>负责收集、分析、整理和管理产品需求，确保需求的清晰、完整和可跟踪性</li>
              <li>与业务方、用户和相关干系人充分沟通，准确理解和提炼业务价值与用户需求</li>
              <li>编写高质量的需求文档，包括需求规格说明书、用例、用户故事和验收标准</li>
              <li>协助制定需求优先级，并参与需求评审，确保需求可实现性</li>
              <li>跟踪需求实现过程，及时处理需求实现过程中出现的问题</li>
              <li>组织并参与需求验收测试，确保需求实现符合预期</li>
              <li>建立并维护需求管理系统，确保需求的可追溯性和变更管理</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>必备技能</h3>
            <ul>
              <li>具备扎实的需求分析与管理能力，熟悉常用的需求分析工具和方法</li>
              <li>优秀的沟通表达和文档编写能力，能够清晰准确地表达复杂需求</li>
              <li>良好的逻辑思维能力和系统性思考能力，能够从混乱信息中提炼核心需求</li>
              <li>熟悉软件开发生命周期和敏捷开发方法论，理解需求在开发流程中的定位</li>
              <li>具备项目管理基础知识，能够协调多方资源推进需求落地</li>
              <li>对技术实现有基本了解，能够评估需求的技术可行性</li>
              <li>具备数据分析能力，能够通过数据验证需求价值</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>工作界面</h3>
            <p>需求工程师需要与多个角色紧密协作：</p>
            <ul>
              <li><strong>产品经理：</strong>提供产品战略和愿景，共同确定需求优先级和产品路线图</li>
              <li><strong>UX/UI设计师：</strong>传递用户需求和业务要求，共同讨论用户体验方案</li>
              <li><strong>开发工程师：</strong>澄清需求细节，解答开发过程中的需求问题</li>
              <li><strong>测试工程师：</strong>提供测试用例的输入，确保需求的可测试性</li>
              <li><strong>业务分析师：</strong>共同分析业务流程和规则，确保需求符合业务目标</li>
              <li><strong>项目经理：</strong>协调需求变更对项目计划的影响，确保需求按计划交付</li>
              <li><strong>利益相关者：</strong>持续沟通需求进展，管理期望和反馈</li>
            </ul>
          </div>

          <div class="detail-item">
            <h3>职业发展路径</h3>
            <p>需求工程师的职业发展通常可以向以下方向发展：</p>
            <ul>
              <li><strong>初级需求工程师：</strong>负责基础需求收集和文档编写，在资深需求工程师指导下工作</li>
              <li><strong>中级需求工程师：</strong>独立负责需求分析和管理，能够处理中等复杂度的项目需求</li>
              <li><strong>高级需求工程师：</strong>主导复杂项目的需求工作，优化需求流程，指导初级需求工程师</li>
              <li><strong>需求架构师：</strong>负责构建企业级需求框架，制定需求管理标准和最佳实践</li>
              <li><strong>业务分析总监：</strong>从战略层面规划需求管理体系，推动组织级的需求能力建设</li>
              <li><strong>产品/项目经理：</strong>横向发展为产品经理或项目经理，负责更广泛的产品和项目管理职责</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- AI功能应用部分 -->
      <div class="position-section">
        <h2 class="section-title">
          <i class="ri-robot-line"></i> AI辅助功能推荐
        </h2>
        <p class="section-desc">基于需求工程师的工作职责和技能需求，以下AI功能可以显著提升工作效率：</p>

        <div class="ai-functions-grid">
          <!-- 文档结构撰写 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-file-list-3-line"></i>
            </div>
            <div class="function-content">
              <h3>文档结构撰写</h3>
              <p>AI帮助快速创建需求文档框架，提供标准化的文档结构模板，提高需求文档规范性</p>
              <div class="function-tags">
                <span class="tag">文档</span>
                <span class="tag">结构化</span>
              </div>
              <router-link to="/text-creation/copywriting/document-structure" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>
          
          <!-- 文档总结 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-draft-line"></i>
            </div>
            <div class="function-content">
              <h3>文档总结</h3>
              <p>将冗长的会议记录、用户反馈和需求讨论总结为关键要点，快速提炼核心需求信息</p>
              <div class="function-tags">
                <span class="tag">总结</span>
                <span class="tag">信息提取</span>
              </div>
              <router-link to="/text-creation/revision/summary" class="use-function-btn">
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
              <p>自动记录并整理需求调研会议内容，确保不遗漏任何重要的需求点和决策</p>
              <div class="function-tags">
                <span class="tag">会议</span>
                <span class="tag">协作</span>
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
              <p>快速生成需求演示文稿，高效呈现需求分析结果和方案建议</p>
              <div class="function-tags">
                <span class="tag">演示</span>
                <span class="tag">汇报</span>
              </div>
              <router-link to="/ai-office/ppt" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>
          
          <!-- 文章校对 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-error-warning-line"></i>
            </div>
            <div class="function-content">
              <h3>文章校对</h3>
              <p>检查需求文档中的拼写、语法和表达错误，确保需求表述准确无误</p>
              <div class="function-tags">
                <span class="tag">校对</span>
                <span class="tag">质量控制</span>
              </div>
              <router-link to="/text-creation/revision/proofreading" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>
          
          <!-- 文章润色 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-quill-pen-line"></i>
            </div>
            <div class="function-content">
              <h3>文章润色</h3>
              <p>优化需求描述的表达方式，使需求文档更专业、更易理解</p>
              <div class="function-tags">
                <span class="tag">润色</span>
                <span class="tag">文档优化</span>
              </div>
              <router-link to="/text-creation/revision/polish" class="use-function-btn">
                立即使用 <i class="ri-arrow-right-line"></i>
              </router-link>
            </div>
          </div>
          
          <!-- 长文创作 -->
          <div class="function-card">
            <div class="function-icon">
              <i class="ri-book-3-line"></i>
            </div>
            <div class="function-content">
              <h3>长文创作</h3>
              <p>协助撰写详尽的需求规格说明书、用例文档和需求分析报告</p>
              <div class="function-tags">
                <span class="tag">创作</span>
                <span class="tag">长文档</span>
              </div>
              <router-link to="/text-creation/copywriting/long-form" class="use-function-btn">
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
              <p>根据需求描述生成示意图，直观呈现产品功能和用户界面设计构想</p>
              <div class="function-tags">
                <span class="tag">图像</span>
                <span class="tag">可视化</span>
              </div>
              <router-link to="/image-generation" class="use-function-btn">
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
  name: 'RequirementsEngineer',
  methods: {
    goBack() {
      this.$router.push('/ai-scenarios');
    },
    navigateTo(path) {
      this.$router.push(path);
    }
  }
};
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

@media screen and (max-width: 768px) {
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