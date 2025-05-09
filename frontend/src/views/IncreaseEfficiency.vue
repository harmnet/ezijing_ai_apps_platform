<template>
  <div class="increase-efficiency-container">
    <div class="header">
      <h1 class="main-title">效率飞跃篇：AI应用效率倍增</h1>
      <p class="sub-title">40+AI工具提升工作效率，实现个人与团队的生产力飞跃</p>
    </div>

    <div class="content-section">
      <!-- 主题一：文本内容创作效率提升 -->
      <section class="topic-section">
        <h2 class="topic-title">
          <span class="topic-number">01</span>
          文本内容创作效率提升
        </h2>
        <div class="topic-content">
          <div class="tools-grid">
            <div class="tool-item" @click="openTool('/text-creation/marketing/ad-slogan')">
              <div class="tool-icon"><i class="ri-advertisement-line"></i></div>
              <div class="tool-info">
                <h4>广告语创作</h4>
                <p>一键生成多个高质量广告语，提升转化率</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/new-media/wechat')">
              <div class="tool-icon"><i class="ri-wechat-line"></i></div>
              <div class="tool-info">
                <h4>公众号创作</h4>
                <p>5分钟完成一篇高质量公众号文章的极致体验</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/new-media/weibo')">
              <div class="tool-icon"><i class="ri-weibo-line"></i></div>
              <div class="tool-info">
                <h4>微博文章创作</h4>
                <p>30秒生成爆款微博，快速提升话题热度</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/new-media/xiaohongshu')">
              <div class="tool-icon"><i class="ri-book-open-line"></i></div>
              <div class="tool-info">
                <h4>小红书笔记创作</h4>
                <p>3分钟打造10w+互动的小红书爆款笔记</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/new-media/short-video')">
              <div class="tool-icon"><i class="ri-video-line"></i></div>
              <div class="tool-info">
                <h4>短视频脚本创作</h4>
                <p>快速生成吸睛短视频脚本，助力内容出圈</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/new-media/livestream')">
              <div class="tool-icon"><i class="ri-live-line"></i></div>
              <div class="tool-info">
                <h4>直播脚本创作</h4>
                <p>打造高转化直播话术，轻松提升销售业绩</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/copywriting/poetry')">
              <div class="tool-icon"><i class="ri-quill-pen-line"></i></div>
              <div class="tool-info">
                <h4>诗歌创作</h4>
                <p>1分钟内创作专业级诗歌，展现文学魅力</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-edit-line"></i></div>
              <div class="tool-info">
                <h4>文本修订</h4>
                <p>智能一键优化文本，提升专业度与表达力</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 主题二：图形内容创作效率提升 -->
      <section class="topic-section">
        <h2 class="topic-title">
          <span class="topic-number">02</span>
          图形内容创作效率提升
        </h2>
        <div class="topic-content">
          <div class="tools-grid">
            <div class="tool-item" @click="openTool('/image-creation/online-design')">
              <div class="tool-icon"><i class="ri-brush-line"></i></div>
              <div class="tool-info">
                <h4>在线图形设计</h4>
                <p>专业级在线设计工具，10分钟完成高端视觉</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/image-creation/intelligent-design')">
              <div class="tool-icon"><i class="ri-ai-generate"></i></div>
              <div class="tool-info">
                <h4>智能图形设计</h4>
                <p>AI一键生成设计作品，3秒获得多套方案</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/image-creation/image-to-painter')">
              <div class="tool-icon"><i class="ri-shopping-bag-line"></i></div>
              <div class="tool-info">
                <h4>智能商品图设计</h4>
                <p>5分钟生成专业电商图，提升点击转化率</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/image-creation/image-matting')">
              <div class="tool-icon"><i class="ri-scissors-cut-line"></i></div>
              <div class="tool-info">
                <h4>智能抠图</h4>
                <p>3秒钟精准抠图，媲美专业设计师水准</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-image-edit-line"></i></div>
              <div class="tool-info">
                <h4>图片智能转设计</h4>
                <p>一键将普通照片变身精美设计作品</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/image-creation/text-to-image')">
              <div class="tool-icon"><i class="ri-file-text-fill"></i></div>
              <div class="tool-info">
                <h4>文生图</h4>
                <p>文字描述秒变精美图像，创意无限可能</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/image-creation/image-to-image')">
              <div class="tool-icon"><i class="ri-image-2-line"></i></div>
              <div class="tool-info">
                <h4>智能风格调整</h4>
                <p>一键转换图片风格，打造艺术视觉效果</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/image-creation/image-redraw')">
              <div class="tool-icon"><i class="ri-edit-2-line"></i></div>
              <div class="tool-info">
                <h4>智能局部重绘</h4>
                <p>精准修改图片细节，告别复杂PS操作</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-fullscreen-line"></i></div>
              <div class="tool-info">
                <h4>智能扩图</h4>
                <p>突破图片边界限制，一键实现完美扩展</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-palette-line"></i></div>
              <div class="tool-info">
                <h4>智能上色</h4>
                <p>黑白照片秒变彩色，重现历史珍贵画面</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 主题三：音视频内容创作效率提升 -->
      <section class="topic-section">
        <h2 class="topic-title">
          <span class="topic-number">03</span>
          音视频内容创作效率提升
        </h2>
        <div class="topic-content">
          <div class="tools-grid">
            <div class="tool-item" @click="openTool('/video-creation/text-to-video')">
              <div class="tool-icon"><i class="ri-file-text-line"></i></div>
              <div class="tool-info">
                <h4>文生视频</h4>
                <p>文字描述5分钟生成专业视频，零技术门槛</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/video-creation/image-to-video')">
              <div class="tool-icon"><i class="ri-image-line"></i></div>
              <div class="tool-info">
                <h4>图生视频</h4>
                <p>静态图片秒变动态视频，让内容活起来</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/digital-human/video-creation')">
              <div class="tool-icon"><i class="ri-user-voice-line"></i></div>
              <div class="tool-info">
                <h4>基础数字人视频制作</h4>
                <p>10分钟获得专业数字人视频，节省90%成本</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/digital-human/advance-video')">
              <div class="tool-icon"><i class="ri-user-star-line"></i></div>
              <div class="tool-info">
                <h4>高级数字人视频制作</h4>
                <p>定制化高质量数字人视频，媲美明星效果</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-user-settings-line"></i></div>
              <div class="tool-info">
                <h4>克隆数字人视频制作</h4>
                <p>30分钟克隆真人数字分身，打造专属形象</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-numbers-line"></i></div>
              <div class="tool-info">
                <h4>123数字人视频制作</h4>
                <p>三步极速创建数字人视频，效率提升300%</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-mic-line"></i></div>
              <div class="tool-info">
                <h4>数字人语音合成</h4>
                <p>逼真数字人声音合成，无法与真人区分</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-video-chat-line"></i></div>
              <div class="tool-info">
                <h4>数字人微课视频制作</h4>
                <p>一键生成专业教学视频，提升学习体验</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-chat-smile-3-line"></i></div>
              <div class="tool-info">
                <h4>交互式数字人</h4>
                <p>打造能实时互动的数字人，提升用户粘性</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>

            <div class="tool-item disabled">
              <div class="tool-icon"><i class="ri-live-fill"></i></div>
              <div class="tool-info">
                <h4>数字人直播</h4>
                <p>24小时不间断直播，无需真人在线</p>
              </div>
              <div class="tool-arrow"><i class="ri-lock-line"></i></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 主题四：办公效率提升 -->
      <section class="topic-section">
        <h2 class="topic-title">
          <span class="topic-number">04</span>
          办公效率提升
        </h2>
        <div class="topic-content">
          <div class="tools-grid">
            <div class="tool-item" @click="openTool('/text-creation/marketing/copywriting-generator')">
              <div class="tool-icon"><i class="ri-article-line"></i></div>
              <div class="tool-info">
                <h4>营销文案创作</h4>
                <p>3分钟生成高转化营销文案，提升销售效果</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/copywriting/document-structure')">
              <div class="tool-icon"><i class="ri-file-list-3-line"></i></div>
              <div class="tool-info">
                <h4>文档结构撰写</h4>
                <p>1分钟生成专业文档结构，告别写作焦虑</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/copywriting/longform')">
              <div class="tool-icon"><i class="ri-book-2-line"></i></div>
              <div class="tool-info">
                <h4>长文档撰写</h4>
                <p>10分钟完成万字专业文档，效率提升500%</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/revision/proofreading')">
              <div class="tool-icon"><i class="ri-error-warning-fill"></i></div>
              <div class="tool-info">
                <h4>文章校对</h4>
                <p>一键发现并修正100%文章错误，确保专业</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/revision/refinement')">
              <div class="tool-icon"><i class="ri-magic-line"></i></div>
              <div class="tool-info">
                <h4>文章润色</h4>
                <p>一键提升文章表达质量，媲美专业编辑</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/text-creation/revision/summary')">
              <div class="tool-icon"><i class="ri-file-reduce-line"></i></div>
              <div class="tool-info">
                <h4>文档总结</h4>
                <p>5秒提炼万字文档精华，节省90%阅读时间</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/ai-office/integration-test')">
              <div class="tool-icon"><i class="ri-slideshow-line"></i></div>
              <div class="tool-info">
                <h4>AI PPT创作</h4>
                <p>5分钟生成专业级PPT，节省8小时制作时间</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/ai-office/meeting-minutes')">
              <div class="tool-icon"><i class="ri-file-list-line"></i></div>
              <div class="tool-info">
                <h4>智能会议纪要</h4>
                <p>自动生成结构化会议记录，提升协作效率</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/ai-office/legal/contract-check')">
              <div class="tool-icon"><i class="ri-file-paper-2-line"></i></div>
              <div class="tool-info">
                <h4>智能合同检查</h4>
                <p>30秒检测合同风险，避免潜在法律纠纷</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/ai-office/data-analysis')">
              <div class="tool-icon"><i class="ri-bar-chart-line"></i></div>
              <div class="tool-info">
                <h4>智能数据分析</h4>
                <p>5分钟获得专业数据洞察，辅助决策制定</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/ai-office/jd-maker')">
              <div class="tool-icon"><i class="ri-user-search-line"></i></div>
              <div class="tool-info">
                <h4>智能招聘JD生成</h4>
                <p>3分钟生成专业招聘JD，吸引优质人才</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/ai-office/cv-optimize')">
              <div class="tool-icon"><i class="ri-file-user-line"></i></div>
              <div class="tool-info">
                <h4>智能简历优化</h4>
                <p>一键优化简历，提升面试通过率300%</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>

            <div class="tool-item" @click="openTool('/ai-office/knowledge-qa')">
              <div class="tool-icon"><i class="ri-question-answer-line"></i></div>
              <div class="tool-info">
                <h4>AI知识库问答</h4>
                <p>智能知识库问答，快速获取专业领域解答</p>
              </div>
              <div class="tool-arrow"><i class="ri-arrow-right-line"></i></div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IncreaseEfficiency',
  data() {
    return {
      appBaseUrl: ''
    }
  },
  mounted() {
    window.scrollTo(0, 0);
    // 设置基础URL，并提供本地开发环境的备用值
    this.appBaseUrl = window.APP_CONFIG?.APP_BASE_URL || window.location.origin;
  },
  methods: {
    openTool(path) {
      if (path) {
        const url = `${this.appBaseUrl}${path}`;
        window.open(url, '_blank');
      }
    }
  }
}
</script>

<style scoped>
.increase-efficiency-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  color: #333;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 50px;
}

.main-title {
  font-size: 36px;
  font-weight: 700;
  color: #C74B50;
  margin-bottom: 16px;
}

.sub-title {
  font-size: 18px;
  color: #666;
}

.content-section {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.topic-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  padding: 30px;
}

.topic-title {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 30px;
  border-bottom: 1px solid #eee;
  padding-bottom: 16px;
}

.topic-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #C74B50;
  color: white;
  border-radius: 50%;
  margin-right: 16px;
  font-size: 18px;
  font-weight: 700;
}

.topic-content {
  padding: 10px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.tool-item {
  display: flex;
  align-items: center;
  background: #f9f9f9;
  border-radius: 10px;
  padding: 16px;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
}

.tool-item:hover:not(.disabled) {
  background: #f1f1f1;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.tool-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #C74B50;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.tool-icon i {
  font-size: 24px;
}

.tool-info {
  flex: 1;
}

.tool-info h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
}

.tool-info p {
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.tool-arrow {
  width: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.tool-arrow i {
  font-size: 20px;
  color: #C74B50;
}

.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.disabled .tool-icon {
  background: #999;
}

.disabled .tool-arrow i {
  color: #999;
}

@media (max-width: 768px) {
  .prepare-study-container {
    padding: 20px 16px;
  }
  
  .main-title {
    font-size: 28px;
  }
  
  .topic-title {
    font-size: 20px;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
  }
}
</style> 