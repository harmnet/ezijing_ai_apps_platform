<template>
  <div class="app">
    <el-config-provider>
      <router-view />
    </el-config-provider>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body, html {
  margin: 0;
  padding: 0;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
  height: 100%;
}

* {
  box-sizing: border-box;
}

.app {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

a {
  text-decoration: none;
  color: inherit;
}
</style> 