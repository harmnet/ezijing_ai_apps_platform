<template>
  <div class="study-page">
    <div class="welcome-info">
      <h2>学习平台访问</h2>
      <p>系统已在新窗口中打开学习平台</p>
      <p>如果新窗口没有自动打开，请点击下方按钮</p>
      <button class="open-btn" @click="openNewWindow">打开学习平台</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Study',
  data() {
    return {
      targetUrl: 'http://211.145.63.214:88/student/studentCourse/Detail?currentTab=0&courseId=610675&course_student_id=3330&state=3&is_authorizedText=',
      hasOpened: false
    }
  },
  methods: {
    openNewWindow() {
      window.open(this.targetUrl, '_blank');
      this.hasOpened = true;
    }
  },
  mounted() {
    console.log('Study组件已加载，自动打开学习平台');
    // 组件加载时自动打开新窗口
    this.openNewWindow();
  }
}
</script>

<style scoped>
.study-page {
  width: 100%;
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  padding: 0;
  position: relative;
}

.welcome-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 20px;
}

.welcome-info h2 {
  margin-bottom: 20px;
  color: #333;
}

.welcome-info p {
  margin-bottom: 10px;
  color: #666;
  font-size: 15px;
  max-width: 500px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 20px;
}

.open-btn {
  background-color: #ba003f;
  color: white;
}

button:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
</style> 