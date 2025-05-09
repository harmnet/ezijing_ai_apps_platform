<template>
  <!-- 数字人演示视频预览弹窗 -->
  <div v-if="show" class="preview-modal-overlay" @click.self="closeModal">
    <div class="preview-modal digital-human-preview-modal">
      <div class="preview-modal-header">
        <h3>{{ digitalHuman?.name }} 数字人演示</h3>
        <button class="close-button" @click="closeModal">
          <i class="ri-close-line"></i>
        </button>
      </div>
      <div class="preview-modal-content">
        <div class="video-container">
          <video id="digital-human-preview-video" controls autoplay class="preview-video">
            <source :src="digitalHuman?.demoVideo" type="video/mp4">
            您的浏览器不支持视频播放
          </video>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DigitalHumanPreviewModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    digitalHuman: {
      type: Object,
      default: null
    }
  },
  methods: {
    closeModal() {
      // 停止视频播放
      const previewVideo = document.getElementById('digital-human-preview-video');
      if (previewVideo) {
        previewVideo.pause();
      }
      
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
/* 数字人预览弹窗特定样式 */
.digital-human-preview-modal {
  width: 80%;
  max-width: 720px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.preview-modal-content {
  padding: 0;
  position: relative;
  overflow: hidden;
  flex: 1;
}

.video-container {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9宽高比 */
  overflow: hidden;
}

.preview-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  background-color: #000;
}

@media (max-width: 768px) {
  .digital-human-preview-modal {
    width: 95%;
    max-height: 80vh;
  }
}
</style> 