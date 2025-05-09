<template>
  <div class="text-creation-page">
    <!-- 分步骤视频合成流程 -->
    <div class="main-container">
      <!-- 左侧步骤条 -->
      <DigitalHumanSteps :currentStep="currentStep" />
      
      <!-- 右侧内容区 -->
      <div class="step-content-container wide-content">
        <!-- 步骤1：输入文本内容 -->
        <div v-if="currentStep === 1" class="step-content-panel">
          <div class="section-title">
            <i class="ri-chat-1-line"></i>
            <span>输入文本内容</span>
          </div>
          
          <div class="form-group">
            <label for="videoTitle" class="form-control-label">视频标题 <span class="optional-field-hint">(选填)</span></label>
            <div class="title-input-container">
              <input
                id="videoTitle"
                v-model="formData.title"
                class="form-control title-input"
                placeholder="请输入视频标题（最多30字）"
                maxlength="30"
                @input="trimTitle"
              />
              <div class="input-helper-text inline-helper-text" v-if="formData.title">已输入 {{ formData.title.length }}/30 字</div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="textContent" class="form-control-label required">文本内容</label>
            <textarea
              id="textContent"
              v-model="formData.text"
              class="form-control taller-textarea"
              placeholder="请输入要数字人播报的文本内容"
              rows="20" 
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
            <div class="digital-human-carousel">
              <button 
                class="carousel-nav prev-button" 
                @click="prevHumanPage" 
                :disabled="currentHumanPage === 0"
                :class="{ 'disabled': currentHumanPage === 0 }"
              >
                <i class="ri-arrow-left-s-line"></i>
              </button>
              
              <div class="digital-human-grid fixed-grid">
                <div 
                  v-for="human in displayedHumans" 
                  :key="human.id"
                  class="digital-human-card compact-card"
                  :class="{ 'selected': formData.figureId === human.id }"
                  @click="selectDigitalHuman(human.id)"
                >
                  <div class="human-avatar">
                    <img :src="human.avatar" :alt="human.name">
                  </div>
                  <div class="human-name">{{ human.name }}</div>
                  <div class="digital-human-actions">
                    <button class="demo-button" @click.stop="previewDigitalHumanVideo(human)" title="查看演示视频">
                      <i class="ri-play-circle-fill"></i>
                      <span>演示</span>
                    </button>
                  </div>
                </div>
              </div>
              
              <button 
                class="carousel-nav next-button" 
                @click="nextHumanPage" 
                :disabled="currentHumanPage >= Math.ceil(digitalHumans.length / humansPerPage) - 1"
                :class="{ 'disabled': currentHumanPage >= Math.ceil(digitalHumans.length / humansPerPage) - 1 }"
              >
                <i class="ri-arrow-right-s-line"></i>
              </button>
            </div>
            
            <!-- 分页指示器 -->
            <div class="pagination-dots" v-if="totalHumanPages > 1">
              <span 
                v-for="page in totalHumanPages" 
                :key="page" 
                class="pagination-dot"
                :class="{ 'active': currentHumanPage === page - 1 }"
                @click="setHumanPage(page - 1)"
              ></span>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-control-label required">音色选择 <span class="voice-filter-info">({{ getSelectedHumanGender() === '女' ? '女' : '男'}}性音色)</span></label>
            
            <div class="voice-list fixed-column-list">
              <div 
                v-for="voice in activeVoices" 
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
        
        <!-- 步骤3：选择模板 -->
        <div v-if="currentStep === 3" class="step-content-panel">
          <div class="section-title">
            <i class="ri-layout-2-line"></i>
            <span>选择模板</span>
          </div>
          
          <div class="form-group">
            <label class="form-control-label required">模板选择</label>
            <div class="template-selection-tips">
              <i class="ri-information-line"></i>
              <span>选择适合您内容的模板，不同模板有不同的视频比例和表现形式。</span>
            </div>
            <div class="template-container">
              <div class="template-grid">
                <div 
                  v-for="template in templateOptions" 
                  :key="template.id"
                  class="template-card"
                  :class="{ 
                    'selected': formData.templateId === template.id,
                    'disabled': template.disabled
                  }"
                  @click="!template.disabled && selectTemplate(template.id)"
                >
                  <div class="template-card-preview">
                    <img :src="template.previewImage" :alt="template.name">
                    <div v-if="template.disabled" class="coming-soon-overlay">
                      <span>即将推出</span>
                    </div>
                  </div>
                  <div class="template-info">
                    <div class="template-name-row">
                      <span class="template-name">
                        <i class="ri-layout-4-line"></i>
                        {{ template.name }}
                      </span>
                      <span class="template-ratio">
                        <i class="ri-aspect-ratio-line"></i>
                        {{ template.ratio }}
                      </span>
                    </div>
                  </div>
                </div>
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
        
        <!-- 步骤4：视频参数 -->
        <div v-if="currentStep === 4" class="step-content-panel">
          <div class="section-title">
            <i class="ri-settings-3-line"></i>
            <span>视频参数设置</span>
          </div>
          
          <!-- 背景图片和Logo上传区域 -->
          <div class="form-group">
            <div class="upload-container-flex">
              <!-- 背景图片上传 -->
              <div class="flex-item">
                <label class="form-control-label">背景图片</label>
                <div 
                  class="background-upload-area"
                  :class="{'has-image': formData.backgroundImageUrl, 'uploading': isUploading}"
                  @click="triggerFileUpload"
                >
                  <template v-if="!formData.backgroundImageUrl && !isUploading">
                    <div class="upload-placeholder">
                      <i class="ri-image-add-line"></i>
                      <span>点击上传背景图片</span>
                      <div class="upload-tip">支持JPG、PNG格式，建议尺寸与视频分辨率相同，小于5MB</div>
                    </div>
                  </template>
                  <template v-else-if="isUploading">
                    <div class="upload-loading">
                      <i class="ri-loader-4-line animate-spin"></i>
                      <span>图片上传中... {{uploadProgress}}%</span>
                      <div class="progress-bar">
                        <div class="progress-bar-inner" :style="{width: uploadProgress + '%'}"></div>
                      </div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="background-preview">
                      <img :src="formData.backgroundImageUrl" alt="背景图片预览" />
                      <div class="background-actions">
                        <button class="action-icon-button" @click.stop="removeBackground($event)" title="移除背景图片">
                          <i class="ri-delete-bin-line"></i>
                        </button>
                      </div>
                    </div>
                  </template>
                </div>
              </div>

              <!-- Logo上传 -->
              <div class="flex-item">
                <label class="form-control-label">Logo图片</label>
                <div 
                  class="logo-upload-area"
                  :class="{'has-image': formData.logoParams.imageUrl, 'uploading': isUploadingLogo}"
                  @click="triggerLogoFileUpload"
                >
                  <template v-if="!formData.logoParams.imageUrl && !isUploadingLogo">
                    <div class="upload-placeholder">
                      <i class="ri-image-add-line"></i>
                      <span>点击上传Logo</span>
                      <div class="upload-tip">支持JPG、PNG格式，建议尺寸200x200像素，小于2MB</div>
                    </div>
                  </template>
                  <template v-else-if="isUploadingLogo">
                    <div class="upload-loading">
                      <i class="ri-loader-4-line animate-spin"></i>
                      <span>Logo上传中... {{logoUploadProgress}}%</span>
                      <div class="progress-bar">
                        <div class="progress-bar-inner" :style="{width: logoUploadProgress + '%'}"></div>
                      </div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="logo-preview">
                      <img :src="formData.logoParams.imageUrl" alt="Logo预览" />
                      <div class="logo-actions">
                        <button class="action-icon-button" @click.stop="removeLogo($event)" title="移除Logo">
                          <i class="ri-delete-bin-line"></i>
                        </button>
                      </div>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 片头片尾设置 - 完全禁用功能 -->
          <div class="form-group media-uploads-group">
            <label class="form-control-label">
              片头片尾设置
              <span class="feature-status disabled-feature">(功能未开放)</span>
            </label>
            <div class="upload-container-flex">
              <!-- 片头视频上传 - 完全禁用 -->
              <div class="flex-item">
                <div class="media-card disabled-card">
                  <div class="media-card-header">
                    <i class="ri-video-line"></i>
                    <span>片头视频</span>
                  </div>
                  <div class="video-upload-area disabled-upload-area">
                    <div class="upload-placeholder">
                      <i class="ri-video-upload-line"></i>
                      <span>上传片头视频</span>
                      <div class="upload-tip">仅支持MP4格式，建议5-10秒，小于50MB</div>
                      <div class="disabled-overlay">
                        <span>功能未开放</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 片尾视频上传 - 完全禁用 -->
              <div class="flex-item">
                <div class="media-card disabled-card">
                  <div class="media-card-header">
                    <i class="ri-video-line"></i>
                    <span>片尾视频</span>
                  </div>
                  <div class="video-upload-area disabled-upload-area">
                    <div class="upload-placeholder">
                      <i class="ri-video-upload-line"></i>
                      <span>上传片尾视频</span>
                      <div class="upload-tip">仅支持MP4格式，建议5-10秒，小于50MB</div>
                      <div class="disabled-overlay">
                        <span>功能未开放</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 背景音乐 - 完全禁用功能 -->
          <div class="form-group media-uploads-group">
            <label class="form-control-label">
              背景音乐设置
              <span class="feature-status disabled-feature">(功能未开放)</span>
            </label>
            <div class="media-card audio-card disabled-card">
              <div class="media-card-header">
                <i class="ri-music-line"></i>
                <span>背景音乐</span>
              </div>
              <div class="audio-upload-area disabled-upload-area">
                <div class="upload-placeholder">
                  <i class="ri-music-line"></i>
                  <span>上传背景音乐</span>
                  <div class="upload-tip">支持MP3格式，小于10MB</div>
                  <div class="disabled-overlay">
                    <span>功能未开放</span>
                  </div>
                </div>
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
        
        <!-- 步骤5：提交任务 -->
        <div v-if="currentStep === 5" class="step-content-panel">
          <div class="section-title">
            <i class="ri-upload-cloud-line"></i>
            <span>提交任务</span>
          </div>
          
          <div class="task-summary-container">
            <h3 class="summary-title">任务信息摘要</h3>
            
            <div class="task-summary-grid">
              <!-- 基础信息 -->
              <div class="summary-section">
                <h4 class="section-title">基础信息</h4>
                <div class="section-content">
                  <div class="form-item">
                    <div class="label">视频标题</div>
                    <div class="value">{{ formData.title || '无标题' }}</div>
                  </div>
                  <div class="form-item">
                    <div class="label">文本内容</div>
                    <div :class="['text-content', textExpanded ? 'expanded' : '']">{{ formData.text }}</div>
                    <button v-if="formData.text.length > 100" class="text-expand-btn" @click="toggleTextExpand">
                      {{ textExpanded ? '收起' : '展开' }}
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- 视频形象 -->
              <div class="summary-section">
                <h4 class="section-title">视频形象</h4>
                <div class="section-content">
                  <div class="form-item">
                    <div class="label">数字人</div>
                    <div class="value">{{ getHumanName(formData.figureId) }}</div>
                  </div>
                  <div class="form-item">
                    <div class="label">音色</div>
                    <div class="value">{{ getVoiceName(formData.ttsParams.person) }}</div>
                  </div>
                  <div class="form-item">
                    <div class="label">模板</div>
                    <div class="value">{{ getTemplateName(formData.templateId) }}</div>
                  </div>
                </div>
              </div>
              
              <!-- 视频参数 -->
              <div class="summary-section">
                <h4 class="section-title">视频参数</h4>
                <div class="section-content">
                  <div class="form-item">
                    <div class="label">分辨率</div>
                    <div class="value">{{ getResolutionLabel(formData.videoParams.width, formData.videoParams.height) }}</div>
                  </div>
                  <div class="form-item">
                    <div class="label">字幕</div>
                    <div class="value">{{ formData.subtitleParams.enabled ? '显示' : '不显示' }}</div>
                  </div>
                  <div class="form-item" v-if="formData.subtitleParams.enabled">
                    <div class="label">字幕样式</div>
                    <div class="value">
                      {{ formData.subtitleParams.fontSize }}px, 
                      <span class="color-box" :style="{backgroundColor: formData.subtitleParams.fontColor}"></span>
                      {{ formData.subtitleParams.fontColor }}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 附加元素 -->
              <div class="summary-section">
                <h4 class="section-title">附加元素</h4>
                <div class="section-content">
                  <div class="form-item">
                    <div class="label">Logo水印</div>
                    <div class="value">{{ formData.logoParams.enabled ? ('已添加，位置：' + getLogoPositionName(formData.logoParams.position)) : '未添加' }}</div>
                  </div>
                  <div class="form-item">
                    <div class="label">片头视频</div>
                    <div class="value">{{ formData.openingMaterial.fileUrl ? '已添加' : '未添加' }}</div>
                  </div>
                  <div class="form-item">
                    <div class="label">片尾视频</div>
                    <div class="value">{{ formData.endingMaterial.fileUrl ? '已添加' : '未添加' }}</div>
                  </div>
                  <div class="form-item">
                    <div class="label">背景音乐</div>
                    <div class="value">{{ formData.bgmParams.bgmUrl ? ('已添加，音量：' + formData.bgmParams.volume + '%') : '未添加' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="secondary-button" @click="prevStep">
              <i class="ri-arrow-left-line"></i>
              <span>上一步</span>
            </button>
            <button 
              class="primary-button"
              @click="submitTask"
              :disabled="isSubmitting"
            >
              <i v-if="isSubmitting" class="ri-loader-4-line animate-spin"></i>
              <span>{{ isSubmitting ? '提交中...' : '提交任务' }}</span>
            </button>
          </div>
        </div>
        
        <!-- 步骤6：查看结果 -->
        <div v-if="currentStep === 6" class="step-content-panel">
          <div class="section-title">
            <i class="ri-video-line"></i>
            <span>查看结果</span>
          </div>
          
          <div class="task-result-container">
            <!-- 任务ID和状态 -->
            <div class="task-info-card">
              <div class="task-info-header">
                <div class="task-id-section">
                  <div class="task-id-label">任务ID：</div>
                  <div class="task-id-value">{{ taskResult?.taskId || '未知' }}</div>
                  <div :class="['task-status', getStatusClass(taskStatus?.status)]">
                    {{ getStatusText(taskStatus?.status) }}
                  </div>
                </div>
                
                <!-- 提交和更新时间 -->
                <div class="task-time-section">
                  <div class="time-item">
                    <div class="time-label">提交时间：</div>
                    <div class="time-value">{{ taskStatus?.createTime ? formatTime(taskStatus.createTime) : '未知' }}</div>
                  </div>
                  <div class="time-item">
                    <div class="time-label">更新时间：</div>
                    <div class="time-value">{{ taskStatus?.updateTime ? formatTime(taskStatus.updateTime) : '未知' }}</div>
                  </div>
                </div>
              </div>
              
              <!-- 处理中状态指示器（当状态为PROCESSING时显示） -->
              <div v-if="taskStatus?.status === 'GENERATING'" class="task-processing-section">
                <div class="processing-indicator">
                  <i class="ri-loader-4-line animate-spin"></i>
                  <span>视频生成中，请稍候...</span>
                </div>
                <div class="processing-tip">系统正在自动刷新任务状态，您无需手动操作</div>
                <div class="processing-explanation">
                  <h4>视频生成说明：</h4>
                  <ul>
                    <li>数字人视频生成分为多个步骤：文本分析、语音合成、视频渲染等</li>
                    <li>根据文本长度和选定的模板不同，生成时间约为1-10分钟</li>
                    <li>复杂内容可能需要更长时间，请耐心等待</li>
                  </ul>
                </div>
              </div>
              
              <!-- 提交中状态（当状态为SUBMIT时显示） -->
              <div v-if="taskStatus?.status === 'SUBMIT'" class="task-processing-section">
                <div class="processing-indicator">
                  <i class="ri-file-upload-line animate-pulse"></i>
                  <span>任务提交中，请稍候...</span>
                </div>
                <div class="processing-tip">系统正在处理您的任务，即将开始生成</div>
                <div class="processing-explanation">
                  <h4>任务提交说明：</h4>
                  <ul>
                    <li>系统正在接收您的任务数据并做初步处理</li>
                    <li>此阶段通常持续几秒钟，请耐心等待</li>
                    <li>提交成功后将自动进入排队或生成阶段</li>
                  </ul>
                </div>
              </div>
              
              <!-- 等待中状态（当状态为WAITING时显示） -->
              <div v-if="taskStatus?.status === 'WAITING'" class="task-processing-section">
                <div class="processing-indicator">
                  <i class="ri-timer-line animate-pulse"></i>
                  <span>任务排队中，请稍候...</span>
                </div>
                <div class="processing-tip">系统正在自动刷新任务状态，您无需手动操作</div>
                <div class="processing-explanation">
                  <h4>任务排队说明：</h4>
                  <ul>
                    <li>您的任务已提交成功，正在等待系统处理</li>
                    <li>当前系统任务较多，您的任务已进入排队队列</li>
                    <li>通常等待时间为1-3分钟，请耐心等待</li>
                  </ul>
                </div>
              </div>
              
              <!-- 未查询到状态时的显示 -->
              <div v-if="!taskStatus || !taskStatus.status" class="task-processing-section">
                <div class="processing-indicator">
                  <i class="ri-loader-4-line animate-spin"></i>
                  <span>正在获取任务状态，请稍候...</span>
                </div>
                <div class="processing-tip">首次加载可能需要较长时间，请耐心等待</div>
              </div>
              
              <!-- 失败原因（当状态为FAILED时显示） -->
              <div v-if="taskStatus?.status === 'FAILED'" class="task-error-section">
                <h3 class="error-title">失败原因</h3>
                <div class="error-message">{{ taskStatus.message || '未知错误' }}</div>
              </div>
            </div>
            
            <!-- 视频预览（当状态为SUCCESS时显示） -->
            <div v-if="taskStatus?.status === 'SUCCESS'" class="video-preview-section">
              <h3 class="preview-title">视频预览</h3>
              <div class="video-player-container compact-video">
                <video 
                  ref="videoPlayer"
                  class="preview-video-player" 
                  controls 
                  :src="taskStatus.videoUrl"
                ></video>
              </div>
              
              <div class="video-actions-container">
                <button class="action-button download-button" @click="downloadVideo">
                  <i class="ri-download-line"></i>
                  <span>下载视频</span>
                </button>
                <button class="action-button history-button" disabled>
                  <i class="ri-history-line"></i>
                  <span>查看历史任务</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- 数字人演示视频预览弹窗 -->
  <DigitalHumanPreviewModal 
    :show="showDigitalHumanPreview"
    :digital-human="previewDigitalHuman"
    @close="closeDigitalHumanPreview"
  />
  
  <!-- 文件上传输入 -->
  <input
    type="file"
    ref="fileInput"
    style="display: none"
    accept="image/*"
    @change="handleFileUpload"
  />
  
  <input
    type="file"
    ref="logoFileInput"
    style="display: none"
    accept="image/*"
    @change="handleLogoFileUpload"
  />
  
  <!-- 以下三个input元素保留但设置为禁用状态 -->
  <input
    type="file"
    ref="openingVideoInput"
    style="display: none"
    accept="video/mp4"
    @change="handleOpeningVideoUpload"
    disabled
  />
  
  <input
    type="file"
    ref="endingVideoInput"
    style="display: none"
    accept="video/mp4"
    @change="handleEndingVideoUpload"
    disabled
  />
  
  <input
    type="file"
    ref="bgmFileInput"
    style="display: none"
    accept="audio/mpeg,audio/mp3,audio/wav,audio/ogg"
    @change="handleBgmUpload"
    disabled
  />
</template>

<script>
import { onMounted, ref } from 'vue';
import DigitalHumanSteps from '@/components/digital-human/DigitalHumanSteps.vue';
import DigitalHumanPreviewModal from '@/components/digital-human/DigitalHumanPreviewModal.vue';
import useDigitalHumanData from '@/composables/useDigitalHumanData';
import useDigitalHumanLogic from '@/composables/useDigitalHumanLogic';
import useDigitalHumanBosUpload from '@/composables/useDigitalHumanBosUpload';

export default {
  name: 'BaiduDigitalHumanAdvance',
  components: {
    DigitalHumanSteps,
    DigitalHumanPreviewModal
  },
  setup() {
    // 上传状态变量
    const isUploading = ref(false);
    const uploadProgress = ref(0);
    const isUploadingLogo = ref(false);
    const logoUploadProgress = ref(0);
    const isUploadingOpening = ref(false);
    const isUploadingEnding = ref(false);
    const isUploadingBgm = ref(false);
    
    // 文件上传DOM引用
    const fileInput = ref(null);
    const logoFileInput = ref(null);
    const openingVideoInput = ref(null);
    const endingVideoInput = ref(null);
    const bgmFileInput = ref(null);
    
    // 获取数据和方法
    const data = useDigitalHumanData();
    
    // 向data添加上传状态和文件输入引用
    const enhancedData = {
      ...data,
      isUploading,
      uploadProgress,
      isUploadingLogo,
      logoUploadProgress,
      isUploadingOpening,
      isUploadingEnding,
      isUploadingBgm,
      fileInput,
      logoFileInput,
      openingVideoInput,
      endingVideoInput,
      bgmFileInput
    };
    
    const logic = useDigitalHumanLogic(enhancedData);
    const upload = useDigitalHumanBosUpload(enhancedData);
    
    // 在组件挂载后初始化音色选项
    onMounted(() => {
      logic.initVoices();
    });
    
    // 返回所有需要的数据和方法
    return {
      // 状态
      ...data,
      isUploading,
      uploadProgress,
      isUploadingLogo,
      logoUploadProgress,
      isUploadingOpening,
      isUploadingEnding,
      isUploadingBgm,
      
      // 引用
      fileInput,
      logoFileInput,
      openingVideoInput,
      endingVideoInput,
      bgmFileInput,
      
      // 业务逻辑
      ...logic,
      
      // 上传功能
      ...upload
    };
  }
};
</script>

<style>
@import '@/assets/css/digital-human-advance.css';

/* 视频生成说明样式 */
.processing-explanation {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9fb;
  border-radius: 8px;
  border-left: 4px solid #4e9eff;
}

.processing-explanation h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 16px;
}

.processing-explanation ul {
  padding-left: 20px;
  margin: 0;
}

.processing-explanation li {
  margin-bottom: 8px;
  color: #555;
  line-height: 1.5;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style> 