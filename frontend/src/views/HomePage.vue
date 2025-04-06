<template>
  <div class="home-page">
    <section class="hero-section">
      <h1>欢迎使用人工智能应用平台</h1>
      <p>探索AI的无限可能，助力您的创作与工作</p>
      <div class="hero-actions">
        <button class="primary-btn">立即体验</button>
        <button class="secondary-btn">了解更多</button>
      </div>
    </section>

    <section class="feature-cards">
      <h2>热门功能</h2>
      <div class="card-grid">
        <div class="feature-card" v-for="(feature, index) in featuredItems" :key="index">
          <div class="card-icon" :style="{ backgroundColor: feature.bgColor }">
            <i :class="feature.icon"></i>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
          <router-link :to="feature.link" class="card-link">
            立即使用 <i class="ri-arrow-right-line"></i>
          </router-link>
        </div>
      </div>
    </section>

    <section class="recent-section">
      <h2>最近使用</h2>
      <div class="recent-list">
        <div class="empty-state" v-if="recentItems.length === 0">
          <i class="ri-history-line"></i>
          <p>暂无最近使用的功能</p>
        </div>
        <div class="recent-item" v-for="(item, index) in recentItems" :key="index">
          <div class="recent-icon">
            <i :class="item.icon"></i>
          </div>
          <div class="recent-details">
            <h3>{{ item.title }}</h3>
            <p>{{ item.lastUsed }}</p>
          </div>
          <button class="action-btn">
            <i class="ri-arrow-right-s-line"></i>
          </button>
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
      featuredItems: [
        {
          title: 'AI对话',
          description: '与AI助手进行自然语言对话，获取信息和帮助',
          icon: 'ri-chat-3-line',
          link: '/ai-chat',
          bgColor: '#e6f7ff'
        },
        {
          title: 'AI文生图',
          description: '通过文字描述生成精美图像，释放创意潜能',
          icon: 'ri-image-line',
          link: '/image-creation/text-to-image',
          bgColor: '#fff2e8'
        },
        {
          title: 'AI文本创作',
          description: '生成高质量的文本内容，提升写作效率',
          icon: 'ri-file-text-line',
          link: '/text-creation',
          bgColor: '#f6ffed'
        },
        {
          title: 'AI PPT',
          description: '快速生成专业演示文稿，省时高效',
          icon: 'ri-slideshow-line',
          link: '/ai-office/ppt',
          bgColor: '#fff0f6'
        }
      ],
      recentItems: [
        {
          title: 'AI对话',
          icon: 'ri-chat-3-line',
          lastUsed: '最近使用：今天 10:30'
        },
        {
          title: 'AI文生图',
          icon: 'ri-image-line',
          lastUsed: '最近使用：昨天 15:45'
        }
      ]
    }
  }
}
</script>

<style scoped>
.home-page {
  padding: 0;
  overflow-y: auto;
  height: 100%;
}

.hero-section {
  text-align: center;
  padding: 40px 20px;
  margin-bottom: 40px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4ecfb 100%);
  border-radius: 12px;
}

.hero-section h1 {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.hero-section p {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.primary-btn {
  background-color: #ba003f;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.primary-btn:hover {
  background-color: #d4154f;
}

.secondary-btn {
  background-color: white;
  color: #333;
  border: 1px solid #ddd;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.secondary-btn:hover {
  border-color: #ba003f;
  color: #ba003f;
}

h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.feature-card {
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.card-icon i {
  font-size: 28px;
  color: #333;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

.feature-card p {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  min-height: 40px;
}

.card-link {
  display: inline-flex;
  align-items: center;
  color: #ba003f;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
}

.card-link i {
  margin-left: 4px;
  transition: transform 0.2s;
}

.card-link:hover i {
  transform: translateX(4px);
}

.recent-list {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.recent-item {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.recent-item:last-child {
  border-bottom: none;
}

.recent-item:hover {
  background-color: #f9f9f9;
}

.recent-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.recent-icon i {
  font-size: 20px;
  color: #666;
}

.recent-details {
  flex: 1;
}

.recent-details h3 {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
  color: #333;
}

.recent-details p {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.action-btn {
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.action-btn i {
  font-size: 20px;
  color: #999;
  transition: color 0.2s;
}

.action-btn:hover i {
  color: #ba003f;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #999;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
}
</style> 