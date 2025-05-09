<template>
  <!-- 左侧步骤条 -->
  <div class="steps-container slim-steps">
    <!-- 步骤指示器 -->
    <div class="creation-steps">
      <!-- 步骤1 -->
      <div class="creation-step" :class="{'step-completed': currentStep > 1, 'step-current': currentStep === 1}">
        <div class="step-indicator">
          <i v-if="currentStep > 1" class="ri-check-line"></i>
          <i v-else-if="currentStep === 1" class="ri-edit-line"></i>
          <span v-else>1</span>
        </div>
        <div class="step-content">
          <div class="step-name">输入文本</div>
          <div class="step-description">添加内容</div>
        </div>
      </div>
      <!-- 步骤2 -->
      <div class="creation-step" :class="{'step-completed': currentStep > 2, 'step-current': currentStep === 2}">
        <div class="step-indicator">
          <i v-if="currentStep > 2" class="ri-check-line"></i>
          <i v-else-if="currentStep === 2" class="ri-user-voice-line"></i>
          <span v-else>2</span>
        </div>
        <div class="step-content">
          <div class="step-name">形象音色</div>
          <div class="step-description">选择配置</div>
        </div>
      </div>
      <!-- 步骤3 - 新增选择模板步骤 -->
      <div class="creation-step" :class="{'step-completed': currentStep > 3, 'step-current': currentStep === 3}">
        <div class="step-indicator">
          <i v-if="currentStep > 3" class="ri-check-line"></i>
          <i v-else-if="currentStep === 3" class="ri-layout-2-line"></i>
          <span v-else>3</span>
        </div>
        <div class="step-content">
          <div class="step-name">选择模板</div>
          <div class="step-description">背景配置</div>
        </div>
      </div>
      <!-- 步骤4 - 原步骤3 -->
      <div class="creation-step" :class="{'step-completed': currentStep > 4, 'step-current': currentStep === 4}">
        <div class="step-indicator">
          <i v-if="currentStep > 4" class="ri-check-line"></i>
          <i v-else-if="currentStep === 4" class="ri-settings-3-line"></i>
          <span v-else>4</span>
        </div>
        <div class="step-content">
          <div class="step-name">视频参数</div>
          <div class="step-description">调整设置</div>
        </div>
      </div>
      <!-- 步骤5 - 原步骤4 -->
      <div class="creation-step" :class="{'step-completed': currentStep > 5, 'step-current': currentStep === 5}">
        <div class="step-indicator">
          <i v-if="currentStep > 5" class="ri-check-line"></i>
          <i v-else-if="currentStep === 5" class="ri-upload-cloud-line"></i>
          <span v-else>5</span>
        </div>
        <div class="step-content">
          <div class="step-name">提交任务</div>
          <div class="step-description">确认信息</div>
        </div>
      </div>
      <!-- 步骤6 - 原步骤5 -->
      <div class="creation-step" :class="{'step-completed': currentStep > 6, 'step-current': currentStep === 6}">
        <div class="step-indicator">
          <i v-if="currentStep > 6" class="ri-check-line"></i>
          <i v-else-if="currentStep === 6" class="ri-video-line"></i>
          <span v-else>6</span>
        </div>
        <div class="step-content">
          <div class="step-name">查看结果</div>
          <div class="step-description">获取视频</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DigitalHumanSteps',
  props: {
    currentStep: {
      type: Number,
      required: true
    }
  }
}
</script> 