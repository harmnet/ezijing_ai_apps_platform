<template>
  <div class="audio-player-container">
    <audio 
      :src="src" 
      controls
      class="audio-player"
    ></audio>
  </div>
</template>

<script>
export default {
  name: 'AudioPlayer',
  props: {
    src: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.audio-player-container {
  width: 100%;
}

.audio-player {
  width: 100%;
  height: 40px;
}
</style> 