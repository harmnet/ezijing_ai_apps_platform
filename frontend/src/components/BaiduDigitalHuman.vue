<template>
  <div class="text-creation-page">
    <!-- 分步骤视频合成流程 -->
    <div class="main-container">
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
          <!-- 步骤3 -->
          <div class="creation-step" :class="{'step-completed': currentStep > 3, 'step-current': currentStep === 3}">
            <div class="step-indicator">
              <i v-if="currentStep > 3" class="ri-check-line"></i>
              <i v-else-if="currentStep === 3" class="ri-settings-3-line"></i>
              <span v-else>3</span>
            </div>
            <div class="step-content">
              <div class="step-name">视频参数</div>
              <div class="step-description">调整设置</div>
            </div>
          </div>
          <!-- 步骤4 -->
          <div class="creation-step" :class="{'step-completed': currentStep > 4, 'step-current': currentStep === 4}">
            <div class="step-indicator">
              <i v-if="currentStep > 4" class="ri-check-line"></i>
              <i v-else-if="currentStep === 4" class="ri-upload-cloud-line"></i>
              <span v-else>4</span>
            </div>
            <div class="step-content">
              <div class="step-name">提交任务</div>
              <div class="step-description">确认信息</div>
            </div>
          </div>
          <!-- 步骤5 -->
          <div class="creation-step" :class="{'step-completed': currentStep > 5, 'step-current': currentStep === 5}">
            <div class="step-indicator">
              <i v-if="currentStep > 5" class="ri-check-line"></i>
              <i v-else-if="currentStep === 5" class="ri-video-line"></i>
              <span v-else>5</span>
            </div>
            <div class="step-content">
              <div class="step-name">查看结果</div>
              <div class="step-description">获取视频</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧内容区 -->
      <div class="step-content-container wide-content">
        <!-- 步骤1：输入文本内容 -->
        <div v-if="currentStep === 1" class="step-content-panel">
          <div class="section-title">
            <i class="ri-chat-1-line"></i>
            <span>输入文本内容</span>
          </div>
          <div class="form-group">
            <label for="textContent" class="form-control-label required">文本内容</label>
            <textarea
              id="textContent"
              v-model="formData.text"
              class="form-control"
              placeholder="请输入要数字人播报的文本内容"
              rows="10" 
            ></textarea>
          </div>
          <div class="action-buttons">
            <button class="primary-button" @click="nextStep" :disabled="!formData.text">
              <span>下一步</span>
              <i class="ri-arrow-right-line"></i>
            </button>
          </div>
        </div>
        
        <!-- 步骤2：选择数字人和音色 -->
        <div v-if="currentStep === 2" class="step-content-panel">
          <div class="section-title">
            <i class="ri-user-voice-line"></i>
            <span>选择数字人和音色</span>
          </div>
          
          <div class="form-group">
            <label class="form-control-label required">数字人选择</label>
            <div class="digital-human-grid inline-grid">
              <div 
                v-for="human in digitalHumans" 
                :key="human.id"
                class="digital-human-card compact-card"
                :class="{ 'selected': formData.figureId === human.id }"
                @click="selectDigitalHuman(human.id)"
              >
                <div class="human-avatar">
                  <img :src="human.avatar" :alt="human.name">
                </div>
                <div class="human-name">{{ human.name }}</div>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-control-label required">机位选择</label>
            <div class="camera-options">
              <div
                class="camera-option"
                :class="{ 'active': formData.camera === 'half_body' }"
                @click="selectCamera('half_body')"
              >
                <i class="ri-layout-left-2-line"></i>
                <span>半身</span>
              </div>
              <div
                class="camera-option"
                :class="{ 'active': formData.camera === 'full_body' }"
                @click="selectCamera('full_body')"
              >
                <i class="ri-layout-bottom-2-line"></i>
                <span>全身</span>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-control-label required">音色选择 <span class="voice-filter-info">({{ getSelectedHumanGender() === '女' ? '女' : '男'}}性音色)</span></label>
            
            <div class="voice-filter">
              <input 
                type="text" 
                v-model="voiceSearchText" 
                placeholder="搜索音色名称或风格"
                class="form-control voice-search-input"
              />
            </div>
            
            <div class="voice-list multi-column-list">
              <div 
                v-for="voice in filteredActiveVoices" 
                :key="voice.id"
                class="voice-item compact-voice-item"
                :class="{ 'selected': formData.ttsParams.person === voice.id }"
                @click="selectVoice(voice.id)"
              >
                <div class="voice-icon">
                  <i class="ri-voice-recognition-line"></i>
                </div>
                <div class="voice-info">
                  <div class="voice-name">{{ voice.name }}</div>
                  <div class="voice-desc">{{ voice.gender }} · {{ voice.style }}</div>
                </div>
                <div class="voice-preview">
                  <button 
                    class="preview-button"
                    @click.stop="previewVoice(voice.id)"
                    title="试听音色"
                    :disabled="!getVoicePreviewUrl(voice.id)" 
                  >
                    <i class="ri-play-circle-line"></i>
                  </button>
                </div>
              </div>
            </div>
            
            <div v-if="filteredActiveVoices.length === 0" class="no-voices-found">
              <div class="empty-content">
                <div class="empty-image">
                  <i class="ri-error-warning-line"></i>
                </div>
                <div class="empty-message">没有找到匹配的音色</div>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="secondary-button" @click="prevStep">
              <i class="ri-arrow-left-line"></i>
              <span>上一步</span>
            </button>
            <button class="primary-button" @click="nextStep">
              <span>下一步</span>
              <i class="ri-arrow-right-line"></i>
            </button>
          </div>
        </div>
        
        <!-- 步骤3：设置视频参数 -->
        <div v-if="currentStep === 3" class="step-content-panel">
          <div class="section-title">
            <i class="ri-settings-3-line"></i>
            <span>设置视频参数</span>
          </div>
          
          <div class="form-group">
            <label class="form-control-label">视频分辨率</label>
            <div class="resolution-options">
              <div
                v-for="option in resolutionOptions"
                :key="option.value"
                class="resolution-option"
                :class="{ 'active': isResolutionSelected(option.value) }"
                @click="selectResolution(option.value)"
              >
                {{ option.label }}
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-control-label">视频选项</label>
            <div class="checkbox-group">
              <div class="checkbox-item" :class="{ 'checkbox-active': formData.videoParams.transparent }" @click="formData.videoParams.transparent = !formData.videoParams.transparent">
                <input type="checkbox" id="transparent" v-model="formData.videoParams.transparent" style="display: none;" />
                <label class="checkbox-label" for="transparent">透明背景</label>
              </div>
              
              <div class="checkbox-item" :class="{ 'checkbox-active': formData.autoAnimoji }" @click="formData.autoAnimoji = !formData.autoAnimoji">
                <input type="checkbox" id="autoAnimoji" v-model="formData.autoAnimoji" style="display: none;" />
                <label class="checkbox-label" for="autoAnimoji">自动添加动作</label>
              </div>
              
              <div class="checkbox-item" :class="{ 'checkbox-active': formData.subtitleParams.enabled }" @click="formData.subtitleParams.enabled = !formData.subtitleParams.enabled">
                <input type="checkbox" id="subtitleEnabled" v-model="formData.subtitleParams.enabled" style="display: none;" />
                <label class="checkbox-label" for="subtitleEnabled">显示字幕</label>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="secondary-button" @click="prevStep">
              <i class="ri-arrow-left-line"></i>
              <span>上一步</span>
            </button>
            <button class="primary-button" @click="nextStep">
              <span>下一步</span>
              <i class="ri-arrow-right-line"></i>
            </button>
          </div>
        </div>
        
        <!-- 步骤4：提交任务 -->
        <div v-if="currentStep === 4" class="step-content-panel">
          <div class="section-title">
            <i class="ri-upload-cloud-line"></i>
            <span>提交任务</span>
          </div>
          
          <div class="task-summary-container">
            <h3 class="summary-heading">
              <i class="ri-file-list-3-line"></i>
              任务信息确认
            </h3>
            
            <div class="task-summary">
              <div class="summary-item">
                <div class="summary-label">
                  <i class="ri-text"></i>
                  文本内容:
                </div>
                <div class="summary-value text-value">
                  {{ formData.text.length > 100 ? formData.text.substring(0, 100) + '...' : formData.text }}
                </div>
              </div>
              <div class="summary-item">
                <div class="summary-label">
                  <i class="ri-user-line"></i>
                  数字人形象:
                </div>
                <div class="summary-value">{{ getHumanName(formData.figureId) }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">
                  <i class="ri-volume-up-line"></i>
                  音色:
                </div>
                <div class="summary-value">{{ getVoiceName(formData.ttsParams.person) }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">
                  <i class="ri-camera-line"></i>
                  机位选择:
                </div>
                <div class="summary-value">{{ getCameraName(formData.camera) }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">
                  <i class="ri-aspect-ratio-line"></i>
                  视频分辨率:
                </div>
                <div class="summary-value">{{ getResolutionLabel(formData.videoParams.width, formData.videoParams.height) }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">
                  <i class="ri-settings-3-line"></i>
                  高级选项:
                </div>
                <div class="summary-value">
                  <span v-if="formData.videoParams.transparent" class="summary-tag">
                    <i class="ri-contrast-drop-line"></i>
                    透明背景
                  </span>
                  <span v-if="formData.autoAnimoji" class="summary-tag">
                    <i class="ri-emotion-line"></i>
                    自动添加动作
                  </span>
                  <span v-if="formData.subtitleParams.enabled" class="summary-tag">
                    <i class="ri-subtitle"></i>
                    显示字幕
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="secondary-button" @click="prevStep">
              <i class="ri-arrow-left-line"></i>
              <span>上一步</span>
            </button>
            <button class="primary-button submit-button" @click="submitTask" :disabled="isSubmitting">
              <i v-if="isSubmitting" class="ri-loader-4-line spinning"></i>
              <span>{{ isSubmitting ? '提交中...' : '确认提交' }}</span>
            </button>
          </div>
        </div>
        
        <!-- 步骤5：查看结果 -->
        <div v-if="currentStep === 5" class="step-content-panel">
          <div class="section-title">
            <i class="ri-video-line"></i>
            <span>任务结果</span>
          </div>
          
          <div v-if="taskResult" class="task-result-info">
            <div class="result-card">
              <div class="result-header">
                <h3>
                  <i class="ri-information-line"></i>
                  任务信息
                </h3>
                <div class="task-status-badge" :class="getStatusClass(taskStatus?.status)">
                  <i v-if="taskStatus?.status === 'PROCESSING'" class="ri-loader-4-line spinning"></i>
                  <i v-else-if="taskStatus?.status === 'SUCCESS'" class="ri-check-line"></i>
                  <i v-else-if="taskStatus?.status === 'FAILED'" class="ri-close-line"></i>
                  <i v-else class="ri-question-line"></i>
                  {{ getStatusText(taskStatus?.status) }}
                </div>
              </div>
              
              <div class="result-info-grid">
                <div class="info-item">
                  <div class="info-label">
                    <i class="ri-fingerprint-line"></i>
                    任务ID:
                  </div>
                  <div class="info-value">
                    <span class="task-id">{{ taskResult.taskId }}</span>
                  </div>
                </div>
              </div>
              
              <div class="task-actions">
                <button class="action-button refresh-button" @click="queryTask" :disabled="isQuerying">
                  <i v-if="isQuerying" class="ri-loader-4-line spinning"></i>
                  <i v-else class="ri-refresh-line"></i>
                  <span>{{ isQuerying ? '查询中...' : '刷新状态' }}</span>
                </button>
              </div>
            </div>
            
            <div v-if="taskStatus?.videoUrl" class="video-result-card">
              <h3 class="video-result-title">
                <i class="ri-movie-line"></i>
                视频预览
              </h3>
              <div class="video-container">
                <video ref="videoPlayer" controls class="video-player">
                  <source :src="taskStatus.videoUrl" :type="taskStatus.videoUrl.endsWith('.webm') ? 'video/webm' : 'video/mp4'">
                  您的浏览器不支持视频播放
                </video>
              </div>
              <div class="video-actions">
                <div v-if="taskResult?.status === 'SUCCEED'" class="btn-group">
                  <a v-if="taskResult?.video_url" :href="taskResult.video_url" target="_blank" class="primary-btn">
                    <i class="ri-download-line"></i>
                    下载视频
                  </a>
                </div>
                <div v-else-if="taskResult?.status === 'FAILED'" class="error-message">
                  <i class="ri-error-warning-line"></i>
                  任务生成失败，请重试
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="empty-result">
            <div class="empty-content">
              <div class="empty-image">
                <i class="ri-vidicon-2-line"></i>
              </div>
              <div class="empty-message">暂无任务结果，请先提交任务</div>
              <button class="primary-button back-button" @click="currentStep = 1">
                <i class="ri-arrow-left-line"></i>
                <span>返回创建任务</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import digitalHumanAPI from '../utils/digitalHumanAPI';
import { ref, computed, onMounted, watch } from 'vue';

export default {
  name: 'BaiduDigitalHuman',
  setup() {
    // 状态定义
    const currentStep = ref(1);
    const formData = ref({
      text: '',
      figureId: 'A2A_V2-xinxin',
      driveType: 'TEXT',
      ttsParams: {
        person: '5132',
        speed: '5',
        volume: '5',
        pitch: '5'
      },
      videoParams: {
        width: 1080,
        height: 1920,
        transparent: false
      },
      camera: 'half_body',
      autoAnimoji: true,
      subtitleParams: {
        enabled: false,
        subtitlePolicy: 'SRT'
      },
      backgroundImageUrl: '',
      callbackUrl: ''
    });
    
    const digitalHumans = ref([
      { id: 'A2A_V2-xinxin', name: '梓欣', gender: 'female', avatar: 'https://bce.bdstatic.com/doc/bce-doc/AI_DH/image%2089_8dc1165.png' },
      { id: 'A2A_V2-xixi', name: '筱萱', gender: 'female', avatar: 'https://bce.bdstatic.com/doc/bce-doc/AI_DH/image%2090_2cae36d.png' },
      { id: 'A2A_V2-xiaomeng2', name: '乔雅', gender: 'female', avatar: 'https://bce.bdstatic.com/doc/bce-doc/AI_DH/image%2091_70a3d4d.png' },
      { id: 'A2A_V2-aning', name: '嘉睿', gender: 'male', avatar: 'https://bce.bdstatic.com/doc/bce-doc/AI_DH/%E5%98%89%E7%9D%BF-2_34e59dc.png' },
      { id: 'A2A_V2-aning_red', name: '嘉霖', gender: 'male', avatar: 'https://bce.bdstatic.com/doc/bce-doc/AI_DH/image%2094_10f09cc.png' },
      { id: 'A2A_V2-gaoming', name: '纪楚', gender: 'male', avatar: 'https://bce.bdstatic.com/doc/bce-doc/AI_DH/image%2095_ed96bc7.png' }
    ]);
    
    const femaleVoices = ref([
      { id: 'CAP_4146', name: '度禧禧', gender: '女声', style: '温柔甜美', previewUrl: 'https://meta-human-editor-prd.cdn.bcebos.com/1a71e60c-bbe0-482b-81fb-4889524acbc3/1e9d042c-f9d7-417f-88d3-4209f5516338/4146.wav' },
      { id: 'BV502_streaming', name: '度小夏', gender: '女声', style: '标准音', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/075ca6ce61d49629f62c520734b9e70e.wav' },
      { id: '7011_moxingxiaoxiao_16k', name: '专业靠谱爽朗女', gender: '女声', style: '专业娴熟/沉稳冷静/激情饱满', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/314a0e551c40beaead431bb4a30c7f43.wav' },
      { id: '7011_moxingkangxi_16k', name: '热情悦耳女主播', gender: '女声', style: '元气活力/权威靠谱/激情饱满', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/6cd5a9da434866bf285ddf6fe0411bbc.wav' },
      { id: '7011_moxinghuanhuan_16k', name: '自信活泼小姐姐', gender: '女声', style: '元气活力/权威靠谱/沉稳冷静', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/e7e878850475aaf2f34f299d4850ff90.wav' },
      { id: '7011_vc0020_16k', name: '自然朴实小妹妹', gender: '女声', style: '专业娴熟/亲和力强/权威靠谱', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/ec2da60778a9dad8f973c976876e50a4.wav' },
      { id: '7011_vc0053_16k', name: '专注真诚大姐姐', gender: '女声', style: '专业娴熟/亲和力强/权威靠谱', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/73ffa1c551a7f1b4b252f89e48909036.wav' },
      { id: '7011_vc0033_16k', name: '职业霸气御姐', gender: '女声', style: '专业娴熟/权威靠谱/沉稳冷静', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/0c4a0336a2c3f0f77cad7b841a8fa15e.wav' },
      { id: '7011_vc0019_16k', name: '知性优雅叙事女声', gender: '女声', style: '专业娴熟/亲和力强/沉稳冷静', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/5a4d90dad835e2347e99ec4746f265ca.wav' },
      { id: '7011_vc0048_16k', name: '幽默东北大妹子', gender: '女声', style: '亲和力强/权威靠谱/激情饱满', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/86d9023df2473565cd6a0b3ee6a11e59.wav' },
      { id: '7011_vc0114_16k', name: '温柔亲和女主播', gender: '女声', style: '元气活力/权威靠谱/激情饱满', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/b2ef65039c63cad57ffed13dd8867dcd.wav' },
      { id: '7011_vc0100_16k', name: '北京口音女声', gender: '女声', style: '亲和力强/权威靠谱/沉稳冷静', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/b1ea9bae92b4b003b239527594a20ef8.wav' }
    ]);
    
    const maleVoices = ref([
      { id: 'CAP_4193', name: '度泽言', gender: '男声', style: '温柔青年', previewUrl: 'https://meta-human-editor-prd.cdn.bcebos.com/1a71e60c-bbe0-482b-81fb-4889524acbc3/a545f018-54a1-4a89-a279-2c56a901bd5b/4193.wav' },
      { id: 'CAP_4195', name: '度怀安', gender: '男声', style: '磁性深情', previewUrl: 'https://meta-human-editor-prd.cdn.bcebos.com/1a71e60c-bbe0-482b-81fb-4889524acbc3/029dd3eb-1bd9-455b-a5fe-3cc3d32f85c3/4195.wav' },
      { id: '4001', name: '度小科', gender: '男声', style: '权威靠谱', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/6765196a1b6b66e8357fb833dad02404.wav' },
      { id: '7011_moxingchuyi_16k', name: '专业自信男主播', gender: '男声', style: '专业娴熟/亲和力强/沉稳冷静', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/91affdc041d5b0dc6665408cf3b33a27.wav' },
      { id: '7011_vc0104_16k', name: '自信坦诚大男孩', gender: '男声', style: '专业娴熟/元气活力/幽默有趣', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/f2af2ed9c71b950c753a6db96ad92c1c.wav' },
      { id: '7011_vc0041_16k', name: '直接果断男主播', gender: '男声', style: '亲和力强/元气活力/幽默有趣', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/6c94172414c967a06d5a14030e2790da.wav' },
      { id: '7011_vc0049_16k', name: '硬朗自信小哥哥', gender: '男声', style: '元气活力/幽默有趣/激情饱满', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/7027e7bf631cb34fa5b079ba71709b3b.wav' },
      { id: '7011_vc0147_16k', name: '雄浑宽广男主播', gender: '男声', style: '专业娴熟/权威靠谱/沉稳冷静', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/cd71c7fb34ccfe009082d8b2ac3eee4a.wav' },
      { id: '7011_vc0079_16k', name: '头头是道讲解员', gender: '男声', style: '亲和力强/元气活力/激情饱满', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/faf238c938ec771252217912c50d96ad.wav' },
      { id: '7011_vc0067_16k', name: '东北磁性男声', gender: '男声', style: '专业商务', previewUrl: 'https://digital-human-pipeline-output.cdn.bcebos.com/de3759ffdedde37d69bbcaab8662c37b.wav' }
    ]);
    
    const activeVoices = ref([]);
    const isSubmitting = ref(false);
    const isQuerying = ref(false);
    const taskResult = ref(null);
    const taskStatus = ref(null);
    const errorMessage = ref('');
    const autoQueryInterval = ref(null);
    const voiceSearchText = ref('');
    const audioPlayer = ref(null);
    const videoPlayer = ref(null);
    
    // 分辨率选项
    const resolutionOptions = ref([
      { label: '720p (1280x720)', value: '1280x720' },
      { label: '1080p (1920x1080)', value: '1920x1080' },
      { label: '竖屏 (720x1280)', value: '720x1280' },
      { label: '竖屏 (1080x1920)', value: '1080x1920' }
    ]);
    
    // 计算属性
    const filteredActiveVoices = computed(() => {
      if (!voiceSearchText.value) {
        return activeVoices.value;
      }
      const searchText = voiceSearchText.value.toLowerCase();
      return activeVoices.value.filter(voice => 
        voice.name.toLowerCase().includes(searchText) || 
        voice.style.toLowerCase().includes(searchText)
      );
    });

    // 将计算属性改为方法
    const getSelectedHumanGender = () => {
      const selectedHuman = digitalHumans.value.find(h => h.id === formData.value.figureId);
      return selectedHuman?.gender === 'female' ? '女' : '男';
    };
    
    // 方法定义
    const initVoices = () => {
      const selectedHuman = digitalHumans.value.find(h => h.id === formData.value.figureId);
      if (selectedHuman) {
        if (selectedHuman.gender === 'female') {
          activeVoices.value = femaleVoices.value;
        } else {
          activeVoices.value = maleVoices.value;
        }
      } else {
        activeVoices.value = femaleVoices.value;
      }
    };
    
    const nextStep = () => {
      if (currentStep.value < 5) {
        currentStep.value++;
      }
    };
    
    const prevStep = () => {
      if (currentStep.value > 1) {
        currentStep.value--;
      }
    };
    
    const selectDigitalHuman = (humanId) => {
      formData.value.figureId = humanId;
      const selectedHuman = digitalHumans.value.find(h => h.id === humanId);
      if (selectedHuman) {
        activeVoices.value = selectedHuman.gender === 'female' ? femaleVoices.value : maleVoices.value;
        const currentVoiceExists = activeVoices.value.some(v => v.id === formData.value.ttsParams.person);
        if (!currentVoiceExists && activeVoices.value.length > 0) {
          formData.value.ttsParams.person = activeVoices.value[0].id;
        }
      } else {
        activeVoices.value = femaleVoices.value;
        if (activeVoices.value.length > 0) {
           formData.value.ttsParams.person = activeVoices.value[0].id;
        }
      }
    };
    
    const selectVoice = (voiceId) => {
      formData.value.ttsParams.person = voiceId;
    };
    
    // 关键方法：获取语音预览URL
    const getVoicePreviewUrl = (voiceId) => {
      const allVoices = [...femaleVoices.value, ...maleVoices.value];
      const voice = allVoices.find(v => v.id === voiceId);
      return voice && voice.previewUrl ? voice.previewUrl : '';
    };
    
    const previewVoice = (voiceId) => {
      console.log('预览音色:', voiceId);
      
      // 停止之前正在播放的音频
      if (audioPlayer.value) {
        audioPlayer.value.pause();
        audioPlayer.value = null;
      }
      
      const previewUrl = getVoicePreviewUrl(voiceId);
      console.log('音频URL:', previewUrl);
      
      if (previewUrl) {
        try {
          // 创建新的音频对象
          audioPlayer.value = new Audio(previewUrl);
          
          // 添加错误处理
          audioPlayer.value.onerror = (e) => {
            console.error('播放音频失败:', e, previewUrl);
            alert(`音频加载失败: ${previewUrl}`);
            audioPlayer.value = null;
          };
          
          // 添加加载事件
          audioPlayer.value.onloadeddata = () => {
            console.log('音频已加载，准备播放');
          };
          
          // 添加播放结束事件
          audioPlayer.value.onended = () => {
            console.log('音频播放完成');
          };
          
          // 播放音频
          console.log('开始播放音频:', previewUrl);
          
          // 使用promise处理播放
          const playPromise = audioPlayer.value.play();
          
          if (playPromise !== undefined) {
            playPromise
              .then(() => {
                console.log('音频开始播放成功');
              })
              .catch(e => {
                console.error('播放音频失败:', e);
                alert('无法播放试听音频，请检查音频链接或浏览器设置。');
                audioPlayer.value = null;
              });
          }
        } catch (err) {
          console.error('创建音频播放器失败:', err);
          alert('音频播放器初始化失败，请稍后再试。');
        }
      } else {
        const allVoices = [...femaleVoices.value, ...maleVoices.value];
        const voice = allVoices.find(v => v.id === voiceId);
        alert(`音色 ${voice ? voice.name : voiceId} 暂无试听音频链接。`);
      }
    };
    
    const getHumanName = (humanId) => {
      const human = digitalHumans.value.find(h => h.id === humanId);
      return human ? human.name : humanId;
    };
    
    const getVoiceName = (voiceId) => {
      const allVoices = [...femaleVoices.value, ...maleVoices.value];
      const voice = allVoices.find(v => v.id === voiceId);
      return voice ? voice.name : voiceId;
    };
    
    const getCameraName = (camera) => {
      const cameraMap = {
        'half_body': '半身',
        'full_body': '全身'
      };
      return cameraMap[camera] || '未选择';
    };
    
    const submitTask = async () => {
      if (!formData.value.text) {
        alert('请输入文本内容');
        return;
      }
      
      isSubmitting.value = true;
      errorMessage.value = '';
      
      try {
        const response = await digitalHumanAPI.submitVideoTask(formData.value);
        
        if (response.data.success) {
          taskResult.value = response.data.data;
          console.log('任务提交成功:', taskResult.value);
          
          startAutoQuery();
          currentStep.value = 5;
        } else {
          errorMessage.value = response.data.message || '任务提交失败';
          alert(errorMessage.value);
        }
      } catch (error) {
        console.error('提交任务出错:', error);
        errorMessage.value = error.response?.data?.message || '网络错误，请稍后重试';
        alert(errorMessage.value);
      } finally {
        isSubmitting.value = false;
      }
    };
    
    const startAutoQuery = () => {
      stopAutoQuery();
      
      autoQueryInterval.value = setInterval(() => {
        if (taskResult.value && taskResult.value.taskId) {
          queryTask(false);
          
          if (taskStatus.value && (taskStatus.value.status === 'SUCCESS' || taskStatus.value.status === 'FAILED')) {
            stopAutoQuery();
          }
        } else {
          stopAutoQuery();
        }
      }, 5000);
    };
    
    const stopAutoQuery = () => {
      if (autoQueryInterval.value) {
        clearInterval(autoQueryInterval.value);
        autoQueryInterval.value = null;
      }
    };
    
    const queryTask = async (showLoading = true) => {
      if (!taskResult.value || !taskResult.value.taskId) {
        alert('请先提交任务');
        return;
      }
      
      if (showLoading) {
        isQuerying.value = true;
      }
      
      try {
        const response = await digitalHumanAPI.queryVideoTask(taskResult.value.taskId);
        
        if (response.data.success) {
          taskStatus.value = response.data.data;
          console.log('任务状态:', taskStatus.value);
        } else {
          errorMessage.value = response.data.message || '查询任务失败';
          if (showLoading) {
            alert(errorMessage.value);
          } else {
            console.error(errorMessage.value);
          }
        }
      } catch (error) {
        console.error('查询任务出错:', error);
        errorMessage.value = error.response?.data?.message || '网络错误，请稍后重试';
        if (showLoading) {
          alert(errorMessage.value);
        } else {
          console.error(errorMessage.value);
        }
      } finally {
        if (showLoading) {
          isQuerying.value = false;
        }
      }
    };
    
    const resetForm = () => {
      formData.value = {
        text: '',
        figureId: 'A2A_V2-xinxin',
        driveType: 'TEXT',
        ttsParams: {
          person: '5132',
          speed: '5',
          volume: '5',
          pitch: '5'
        },
        videoParams: {
          width: 1080,
          height: 1920,
          transparent: false
        },
        camera: 'half_body',
        autoAnimoji: true,
        subtitleParams: {
          enabled: false,
          subtitlePolicy: 'SRT'
        },
        backgroundImageUrl: '',
        callbackUrl: ''
      };
      taskResult.value = null;
      taskStatus.value = null;
      currentStep.value = 1;
    };
    
    const getStatusText = (status) => {
      const statusMap = {
        'PROCESSING': '处理中',
        'SUCCESS': '成功',
        'FAILED': '失败',
        null: '未知'
      };
      return statusMap[status] || status;
    };
    
    const getStatusClass = (status) => {
      if (!status) return 'status-unknown';
      const statusLower = status.toLowerCase();
      if (statusLower === 'processing') return 'status-processing';
      if (statusLower === 'success') return 'status-success';
      if (statusLower === 'failed') return 'status-failed';
      return 'status-unknown';
    };
    
    const formatTime = (timeString) => {
      if (!timeString) return '';
      try {
        const date = new Date(timeString);
        return `${date.getFullYear()}-${padZero(date.getMonth() + 1)}-${padZero(date.getDate())} ${padZero(date.getHours())}:${padZero(date.getMinutes())}:${padZero(date.getSeconds())}`;
      } catch (e) {
        return timeString;
      }
    };
    
    const padZero = (num) => {
      return num < 10 ? `0${num}` : `${num}`;
    };
    
    const downloadVideo = () => {
      // 下载视频的实现
      if (taskStatus.value && taskStatus.value.videoUrl) {
        const link = document.createElement('a');
        link.href = taskStatus.value.videoUrl;
        link.download = `digital-human-video-${taskResult.value.taskId}.mp4`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        alert('视频尚未生成，无法下载');
      }
    };
    
    const copyVideoLink = () => {
      // 复制视频链接的实现
      if (taskStatus.value && taskStatus.value.videoUrl) {
        navigator.clipboard.writeText(taskStatus.value.videoUrl)
          .then(() => {
            alert('视频链接已复制到剪贴板');
          })
          .catch(err => {
            console.error('无法复制链接:', err);
            alert('复制链接失败，请手动复制');
          });
      } else {
        alert('视频尚未生成，无法复制链接');
      }
    };
    
    const getResolutionLabel = (width, height) => {
      const resolution = `${width}x${height}`;
      const found = resolutionOptions.value.find(option => option.value === resolution);
      return found ? found.label : `${width}x${height}`;
    };
    
    const selectResolution = (resolution) => {
      const [width, height] = resolution.split('x');
      formData.value.videoParams.width = parseInt(width);
      formData.value.videoParams.height = parseInt(height);
    };
    
    const isResolutionSelected = (resolution) => {
      return `${formData.value.videoParams.width}x${formData.value.videoParams.height}` === resolution;
    };
    
    // 相机设置
    const selectCamera = (camera) => {
      formData.value.camera = camera;
    };
    
    // 生命周期钩子
    onMounted(() => {
      initVoices();
    });
    
    // 返回模板中需要使用的内容
    return {
      currentStep,
      formData,
      digitalHumans,
      femaleVoices,
      maleVoices,
      activeVoices,
      filteredActiveVoices,
      isSubmitting,
      isQuerying,
      taskResult,
      taskStatus,
      errorMessage,
      voiceSearchText,
      videoPlayer,
      
      // 方法
      nextStep,
      prevStep,
      selectDigitalHuman,
      selectVoice,
      previewVoice,
      getVoicePreviewUrl,
      getHumanName,
      getVoiceName,
      getSelectedHumanGender,
      getCameraName,
      submitTask,
      queryTask,
      resetForm,
      getStatusText,
      getStatusClass,
      formatTime,
      downloadVideo,
      copyVideoLink,
      getResolutionLabel,
      selectResolution,
      isResolutionSelected,
      resolutionOptions,
      selectCamera
    };
  }
};
</script>

<style scoped>
@import '../assets/css/text-creation-common.css';

/* 主容器布局调整 */
.main-container {
  display: flex;
  gap: 15px;
  height: 100%;
}

/* 左侧步骤条变窄 */
.steps-container.slim-steps {
  width: 200px; /* 调小左侧宽度 */
  flex-shrink: 0;
  margin-bottom: 0; /* 移除底部间距，因为右侧会滚动 */
}

/* 右侧内容区变宽 */
.step-content-container.wide-content {
  flex-grow: 1; /* 占据剩余宽度 */
  max-height: calc(100vh - 120px); /* 限制高度，留出顶部导航空间 */
  overflow-y: auto; /* 内容超出时允许滚动 */
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

/* 步骤内容面板 */
.step-content-panel {
  padding: 20px;
  height: auto;
  display: flex;
  flex-direction: column;
}

/* 表单组样式 */
.form-group {
  margin-bottom: 20px;
  flex-shrink: 0;
}

/* 优化数字人选择布局 */
.digital-human-grid.inline-grid {
  display: grid; 
  grid-template-columns: repeat(6, 1fr); /* 六列布局 */
  gap: 15px; /* 增加间距 */
  max-height: 220px; /* 提高高度，原来是150px */
  overflow-y: auto; /* 超出时添加滚动 */
  padding: 10px; /* 增加内边距 */
  border: 1px solid #eee;
  border-radius: 8px;
}

.digital-human-card.compact-card {
  width: auto;
  margin: 0;
  padding: 8px; /* 增加内边距 */
  border: 2px solid transparent;
  border-radius: 8px;
  transition: all 0.2s;
}

.digital-human-card.compact-card:hover {
  background-color: #f9f9f9;
  transform: translateY(-2px);
}

.digital-human-card.compact-card.selected {
  border-color: var(--primary-color, #ba003f);
  background-color: rgba(186, 0, 63, 0.05);
}

.compact-card .human-avatar {
  width: 70px; /* 增加头像尺寸，原来是50px */
  height: 70px; /* 增加头像尺寸，原来是50px */
  margin: 0 auto 8px; /* 增加底部间距 */
  border-radius: 50%;
  overflow: hidden;
}

.compact-card .human-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.compact-card .human-name {
  font-size: 13px; /* 增大字体 */
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 优化音色选择列表布局，适应更多音色 */
.voice-list.multi-column-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 三列 */
  gap: 10px;
  max-height: 300px; /* 增加高度，显示更多音色 */
  overflow-y: auto;
  padding: 5px;
  border: 1px solid #eee;
  border-radius: 8px;
}

.voice-item.compact-voice-item {
  padding: 8px 10px;
  border: 2px solid #eee;
  border-radius: 8px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
}

.voice-item.compact-voice-item:hover {
  border-color: var(--primary-color, #ba003f);
  background-color: #f9f9f9;
  transform: translateY(-2px);
}

.voice-item.compact-voice-item.selected {
  border-color: var(--primary-color, #ba003f);
  background-color: rgba(186, 0, 63, 0.05);
}

.voice-icon {
  font-size: 20px;
  color: #666;
  margin-right: 10px;
  flex-shrink: 0;
}

.voice-info {
  flex: 1;
  min-width: 0; /* 防止flex子项溢出 */
}

.voice-name {
  font-weight: bold;
  color: #333;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.voice-desc {
  color: #666;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.voice-preview {
  margin-left: 8px;
  flex-shrink: 0;
}

/* 试听按钮强调 */
.preview-button {
  background: none;
  border: none;
  color: var(--primary-color, #ba003f);
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  transition: transform 0.2s;
  line-height: 1;
}

.preview-button:hover {
  transform: scale(1.2);
}

.preview-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 音色过滤器 */
.voice-filter {
  margin-bottom: 10px;
}

.voice-search-input {
  padding: 8px 12px;
  border-radius: 20px;
  border: 1px solid #ddd;
  width: 100%;
  font-size: 14px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%23999' viewBox='0 0 16 16'%3E%3Cpath d='M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: 10px center;
  background-size: 16px;
  padding-left: 32px;
}

.voice-filter-info {
  font-size: 12px;
  color: #666;
  background-color: #f0f0f0;
  padding: 2px 8px;
  border-radius: 10px;
  margin-left: 8px;
}

/* 动作按钮 */
.action-buttons {
  margin-top: auto; /* 推到底部 */
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .digital-human-grid.inline-grid {
    grid-template-columns: repeat(4, 1fr); /* 四列 */
    max-height: 280px; /* 响应式调整高度 */
  }
  
  .voice-list.multi-column-list {
    grid-template-columns: repeat(2, 1fr); /* 两列 */
  }
}

@media (max-width: 768px) { 
  .main-container {
    flex-direction: column;
  }
  
  .steps-container.slim-steps {
    width: 100%;
    margin-bottom: 15px;
  }
  
  .step-content-container.wide-content {
    max-height: none;
  }
  
  .digital-human-grid.inline-grid {
    grid-template-columns: repeat(3, 1fr); /* 三列 */
    max-height: 330px; /* 在移动端增加更多高度 */
  }
  
  .voice-list.multi-column-list {
    grid-template-columns: 1fr; /* 单列 */
  }
}

/* 机位选择样式 */
.camera-options {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.camera-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  width: 100px;
  height: 100px;
}

.camera-option i {
  font-size: 2rem;
  margin-bottom: 10px;
}

.camera-option.active {
  border-color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  color: #007bff;
}

.resolution-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.resolution-option {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.resolution-option.active {
  border-color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  color: #007bff;
}

/* 提交任务和查看结果步骤样式优化 */
.task-summary-container {
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 20px;
}

.summary-heading {
  font-size: 20px;
  color: #333;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}

.summary-heading i {
  margin-right: 8px;
  color: var(--primary-color, #ba003f);
}

.task-summary {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.summary-item {
  padding: 12px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.summary-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.summary-label {
  font-weight: bold;
  color: #555;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
}

.summary-label i {
  margin-right: 6px;
  color: var(--primary-color, #ba003f);
  font-size: 16px;
}

.summary-value {
  font-size: 15px;
  color: #333;
  line-height: 1.5;
}

.text-value {
  max-height: 80px;
  overflow-y: auto;
  white-space: pre-line;
  padding: 8px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
}

.summary-tag {
  display: inline-flex;
  align-items: center;
  background-color: rgba(186, 0, 63, 0.1);
  color: var(--primary-color, #ba003f);
  border-radius: 16px;
  padding: 4px 10px;
  margin-right: 8px;
  margin-bottom: 6px;
  font-size: 13px;
}

.summary-tag i {
  margin-right: 4px;
}

.submit-button {
  background-color: var(--primary-color, #ba003f);
  font-size: 16px;
  padding: 10px 20px;
  transition: all 0.3s;
}

.submit-button:hover {
  background-color: darken(var(--primary-color, #ba003f), 10%);
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.3);
}

/* 查看结果样式 */
.task-result-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  transition: transform 0.3s;
}

.result-card:hover {
  transform: translateY(-4px);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}

.result-header h3 {
  font-size: 18px;
  margin: 0;
  display: flex;
  align-items: center;
}

.result-header h3 i {
  margin-right: 8px;
  color: var(--primary-color, #ba003f);
}

.task-status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.task-status-badge i {
  margin-right: 6px;
}

.status-processing {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status-success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-failed {
  background-color: #ffebee;
  color: #c62828;
}

.status-unknown {
  background-color: #f5f5f5;
  color: #757575;
}

.result-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.info-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 12px;
}

.info-label {
  font-weight: bold;
  color: #666;
  font-size: 14px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
}

.info-label i {
  margin-right: 6px;
  color: var(--primary-color, #ba003f);
}

.info-value {
  font-size: 15px;
  color: #333;
}

.task-id {
  font-family: monospace;
  background-color: #f0f0f0;
  padding: 3px 6px;
  border-radius: 4px;
}

.task-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:hover {
  background-color: #eee;
  transform: translateY(-2px);
}

.action-button i {
  margin-right: 6px;
}

.refresh-button {
  background-color: #e3f2fd;
  color: #1976d2;
}

.refresh-button:hover {
  background-color: #bbdefb;
}

.video-result-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  overflow: hidden;
}

.video-result-title {
  font-size: 18px;
  margin-top: 0;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}

.video-result-title i {
  margin-right: 8px;
  color: var(--primary-color, #ba003f);
}

.video-container {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
  background-color: #000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.video-player {
  width: 100%;
  display: block;
}

.video-actions {
  display: flex;
  gap: 12px;
}

.download-button {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.download-button:hover {
  background-color: #c8e6c9;
}

.copy-button {
  background-color: #e3f2fd;
  color: #1976d2;
}

.copy-button:hover {
  background-color: #bbdefb;
}

.empty-result {
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-content {
  text-align: center;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-image {
  font-size: 80px;
  color: #ccc;
  margin-bottom: 20px;
}

.empty-message {
  font-size: 18px;
  color: #888;
  margin-bottom: 20px;
}

.back-button {
  margin-top: 16px;
}

@media (max-width: 768px) {
  .camera-options {
    grid-template-columns: 1fr;
  }
  
  .result-info-grid {
    grid-template-columns: 1fr;
  }
}
</style> 