<template>
  <header class="header">
    <div class="logo-container">
      <img src="/logo.png" alt="Logo" class="logo" @click="goToHomePage" />
      <h1 class="site-title">人工智能应用与高效办公实践教学平台</h1>
    </div>
    <div class="header-right">
      <div class="user-actions">
        <button class="action-btn">
          <i class="ri-notification-3-line"></i>
        </button>
        <button class="action-btn">
          <i class="ri-settings-3-line"></i>
        </button>
        <div class="user-profile">
          <span class="username">段小飞</span>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'HeaderBar',
  setup() {
    const router = useRouter()
    
    const goToHomePage = () => {
      router.push('/')
    }
    
    return {
      goToHomePage
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 100;
  width: 100%;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px;
  margin-right: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}

.logo:hover {
  transform: scale(1.05);
}

.site-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-actions {
  display: flex;
  align-items: center;
}

.action-btn {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-left: 5px;
  transition: background-color 0.2s;
}

.action-btn i {
  font-size: 20px;
  color: #666;
}

.action-btn:hover {
  background-color: #f5f5f5;
}

.user-profile {
  display: flex;
  align-items: center;
  margin-left: 15px;
  padding: 5px 10px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: #f5f5f5;
}

.username {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}
</style> 