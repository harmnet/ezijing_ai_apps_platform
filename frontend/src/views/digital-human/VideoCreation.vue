<template>
  <div class="digital-human-video-creation">
    <div class="component-container">
      <BaiduDigitalHuman />
    </div>
  </div>
</template>

<script>
import BaiduDigitalHuman from './BaiduDigitalHuman.vue';

export default {
  name: 'DigitalHumanVideoCreation',
  components: {
    BaiduDigitalHuman
  }
};
</script>

<style scoped>
.digital-human-video-creation {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.component-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

@media (max-width: 768px) {
  .digital-human-video-creation {
    padding: 15px;
  }
  
  .component-container {
    padding: 15px;
  }
}
</style> 