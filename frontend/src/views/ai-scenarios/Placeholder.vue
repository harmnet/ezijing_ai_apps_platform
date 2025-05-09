<template>
  <div class="placeholder-container">
    <div class="placeholder-content">
      <i class="ri-tools-line placeholder-icon"></i>
      <h2>页面开发中</h2>
      <p>该功能正在开发中，敬请期待...</p>
      <router-link to="/ai-scenarios" class="back-button">
        返回场景列表
      </router-link>
    </div>
  </div>
</template>

<script setup>
// 占位符组件，用于尚未开发的页面
</script>

<style scoped>
.placeholder-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;
  padding: 20px;
}

.placeholder-content {
  text-align: center;
  background: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}

.placeholder-icon {
  font-size: 48px;
  color: #ba003f;
  margin-bottom: 16px;
}

h2 {
  font-size: 24px;
  color: #333;
  margin: 0 0 16px 0;
}

p {
  font-size: 16px;
  color: #666;
  margin: 0 0 24px 0;
}

.back-button {
  display: inline-block;
  background: #ba003f;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  text-decoration: none;
  transition: background 0.3s;
}

.back-button:hover {
  background: #d4004d;
}
</style> 