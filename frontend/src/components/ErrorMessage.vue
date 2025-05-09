<template>
  <div class="error-message-container" v-if="showError">
    <div class="error-card">
      <div class="error-header">
        <i class="error-icon">&#9888;</i>
        <h3 class="error-title">{{ title || '发生错误' }}</h3>
        <button class="close-button" @click="close">×</button>
      </div>
      <div class="error-content">
        <p class="error-message">{{ message }}</p>
        <div class="error-details" v-if="details">
          <h4 class="details-title">详细信息:</h4>
          <p class="details-content">{{ details }}</p>
        </div>
        <div class="error-suggestions" v-if="suggestions">
          <h4 class="suggestions-title">建议解决方案:</h4>
          <p class="suggestions-content">{{ suggestions }}</p>
        </div>
      </div>
      <div class="error-footer">
        <button class="retry-button" @click="retry" v-if="showRetry">重试</button>
        <button class="ok-button" @click="close">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
  // 错误标题
  title: {
    type: String,
    default: ''
  },
  // 错误消息
  message: {
    type: String,
    required: true
  },
  // 错误代码
  code: {
    type: [Number, String],
    default: null
  },
  // 详细信息
  details: {
    type: String,
    default: ''
  },
  // 解决建议
  suggestions: {
    type: String,
    default: ''
  },
  // 是否显示
  show: {
    type: Boolean,
    default: true
  },
  // 是否显示重试按钮
  showRetry: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'retry']);

// 计算是否显示错误
const showError = computed(() => {
  return props.show && props.message;
});

// 关闭错误提示
const close = () => {
  emit('close');
};

// 重试操作
const retry = () => {
  emit('retry');
};
</script>

<style scoped>
.error-message-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.error-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
  animation: slide-in 0.3s ease;
}

@keyframes slide-in {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.error-header {
  background-color: #ffebee;
  color: #c62828;
  padding: 16px;
  display: flex;
  align-items: center;
  position: relative;
}

.error-icon {
  font-size: 24px;
  margin-right: 12px;
}

.error-title {
  font-size: 18px;
  margin: 0;
  flex-grow: 1;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #c62828;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  position: absolute;
  right: 12px;
  top: 12px;
}

.close-button:hover {
  background-color: rgba(198, 40, 40, 0.1);
}

.error-content {
  padding: 20px;
}

.error-message {
  font-size: 16px;
  margin: 0 0 12px;
  line-height: 1.5;
  color: #333;
}

.error-details, .error-suggestions {
  background-color: #f5f5f5;
  border-radius: 6px;
  padding: 12px;
  margin-top: 12px;
}

.details-title, .suggestions-title {
  font-size: 14px;
  margin: 0 0 6px;
  color: #666;
}

.details-content, .suggestions-content {
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
  color: #333;
  white-space: pre-line;
}

.error-footer {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #eee;
}

.retry-button, .ok-button {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.ok-button {
  background-color: #f44336;
  color: white;
  border: none;
}

.ok-button:hover {
  background-color: #d32f2f;
}

.retry-button {
  background-color: transparent;
  color: #666;
  border: 1px solid #ddd;
}

.retry-button:hover {
  background-color: #f5f5f5;
  color: #333;
}
</style> 