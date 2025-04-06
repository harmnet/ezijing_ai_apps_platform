<template>
  <div class="layout">
    <header-bar class="layout-header" />
    <div class="layout-container">
      <side-menu class="layout-sidebar" />
      <div class="layout-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar.vue'
import SideMenu from '@/components/SideMenu.vue'

export default {
  name: 'Layout',
  components: {
    HeaderBar,
    SideMenu
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.layout-header {
  width: 100%;
  z-index: 100;
}

.layout-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.layout-sidebar {
  height: 100%;
}

.layout-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
}
</style> 