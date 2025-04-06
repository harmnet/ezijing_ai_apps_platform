<template>
  <div class="digital-human-layout">
    <el-card class="menu-card">
      <div class="menu-header">
        <h2>数字人功能</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="digital-human-menu"
        router
      >
        <el-menu-item index="/digital-human">
          <el-icon><Grid /></el-icon>
          <span>数字人功能</span>
        </el-menu-item>
        <el-menu-item index="/digital-human/list">
          <el-icon><List /></el-icon>
          <span>数字人列表</span>
        </el-menu-item>
        <el-menu-item index="/digital-human/quick-start">
          <el-icon><Document /></el-icon>
          <span>快速入门示例</span>
        </el-menu-item>
        <el-menu-item index="/digital-human/dh-demo">
          <el-icon><VideoPlay /></el-icon>
          <span>PPT讲解视频</span>
        </el-menu-item>
      </el-menu>
    </el-card>
    
    <div class="content-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { List, Document, VideoPlay, Grid } from '@element-plus/icons-vue';

export default {
  name: 'DigitalHumanLayout',
  components: {
    List,
    Document,
    VideoPlay,
    Grid
  },
  setup() {
    const route = useRoute();
    
    const activeMenu = computed(() => {
      return route.path;
    });
    
    return {
      activeMenu
    };
  }
};
</script>

<style scoped>
.digital-human-layout {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.menu-card {
  width: 250px;
  height: fit-content;
}

.menu-header {
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 15px;
}

.menu-header h2 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.digital-human-menu {
  border-right: none;
}

.content-container {
  flex: 1;
}

@media (max-width: 768px) {
  .digital-human-layout {
    flex-direction: column;
  }
  
  .menu-card {
    width: 100%;
  }
}
</style> 