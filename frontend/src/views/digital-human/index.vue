<template>
  <div class="digital-human-container">
    <h1 v-if="$route.name === 'DigitalHumanList'" class="page-title">AI数字人功能中心</h1>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'DigitalHumanLayout'
}
</script>

<style scoped>
.digital-human-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 28px;
}

@media (max-width: 768px) {
  .digital-human-container {
    padding: 15px;
  }
  
  .page-title {
    font-size: 24px;
  }
}
</style> 