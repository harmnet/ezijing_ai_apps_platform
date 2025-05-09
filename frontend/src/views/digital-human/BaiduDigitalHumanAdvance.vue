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
            <input
              id="videoTitle"
              v-model="formData.title"
              class="form-control"
              placeholder="请输入视频标题（最多30字）"
              maxlength="30"
              @input="trimTitle"
            />
            <div class="input-helper-text" v-if="formData.title">已输入 {{ formData.title.length }}/30 字</div>
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
                <div class="digital-human-actions">
                  <button class="demo-button" @click.stop="previewDigitalHumanVideo(human)" title="查看演示视频">
                    <i class="ri-video-line"></i>
                  </button>
              </div>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-control-label required">音色选择 <span class="voice-filter-info">({{ getSelectedHumanGender() === '女' ? '女' : '男'}}性音色)</span></label>
            
            <div class="voice-list multi-column-list">
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
            <div class="template-grid">
              <div 
                v-for="template in templateOptions" 
                :key="template.id"
                class="template-card"
                :class="{ 'selected': formData.templateId === template.id }"
                @click="selectTemplate(template.id)"
              >
                <div class="template-card-preview">
                  <img :src="template.previewImage" :alt="template.name">
                </div>
                <div class="template-info">
                  <div class="template-name">{{ template.name }}</div>
                  <div class="template-ratio">{{ template.ratio }}</div>
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
        
        <!-- 步骤4：设置视频参数 -->
        <div v-if="currentStep === 4" class="step-content-panel">
          <div class="section-title">
            <i class="ri-settings-3-line"></i>
            <span>设置视频参数</span>
          </div>
          
          <!-- 上传区域容器（横向排列） -->
          <div class="upload-container-flex">
            <!-- 背景图片上传部分 -->
            <div class="form-group flex-item">
              <label class="form-control-label required">上传背景图片</label>
              <!-- 背景图片上传区域 -->
              <div class="background-upload-container">
                <div class="background-upload-area" @click="triggerFileUpload" :class="{'has-image': formData.backgroundImageUrl, 'uploading': isUploading}">
                  <input type="file" ref="fileInput" style="display: none;" accept="image/*" @change="handleFileUpload" />
                  <div v-if="!formData.backgroundImageUrl && !isUploading" class="upload-placeholder">
                    <i class="ri-image-add-line"></i>
                    <span>点击上传背景图片</span>
                    <span class="upload-tip">建议尺寸与视频分辨率一致</span>
                  </div>
                  <div v-else-if="isUploading" class="upload-loading">
                    <i class="ri-loader-4-line spinning"></i>
                    <span>图片上传中... {{uploadProgress}}%</span>
                    <div class="progress-bar">
                      <div class="progress-bar-inner" :style="{width: uploadProgress + '%'}"></div>
                    </div>
                  </div>
                  <div v-else class="background-preview">
                    <img :src="formData.backgroundImageUrl" alt="背景图片预览" />
                    <div class="background-actions">
                      <button class="action-icon-button" @click.stop="removeBackground" title="移除背景图片">
                        <i class="ri-delete-bin-line"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Logo上传部分 -->
            <div class="form-group flex-item">
              <label class="form-control-label">上传Logo</label>
              <!-- Logo上传区域 -->
              <div class="logo-upload-container">
                <div class="logo-upload-area" @click="triggerLogoFileUpload" :class="{'has-image': formData.logoParams.imageUrl, 'uploading': isUploadingLogo}">
                  <input type="file" ref="logoFileInput" style="display: none;" accept="image/*" @change="handleLogoFileUpload" />
                  <div v-if="!formData.logoParams.imageUrl && !isUploadingLogo" class="upload-placeholder">
                    <i class="ri-image-add-line"></i>
                    <span>点击上传Logo</span>
                    <span class="upload-tip">建议使用透明背景PNG格式</span>
                  </div>
                  <div v-else-if="isUploadingLogo" class="upload-loading">
                    <i class="ri-loader-4-line spinning"></i>
                    <span>Logo上传中... {{logoUploadProgress}}%</span>
                    <div class="progress-bar">
                      <div class="progress-bar-inner" :style="{width: logoUploadProgress + '%'}"></div>
                    </div>
                  </div>
                  <div v-else class="logo-preview">
                    <img :src="formData.logoParams.imageUrl" alt="Logo预览" />
                    <div class="logo-actions">
                      <button class="action-icon-button" @click.stop="removeLogo" title="移除Logo">
                        <i class="ri-delete-bin-line"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="formData.logoParams.imageUrl" class="logo-position-selector">
                <label class="form-control-label">Logo位置：</label>
                <div class="position-options">
                  <div 
                    class="position-option" 
                    :class="{ 'active': formData.logoParams.position === 'top-left' }"
                    @click="formData.logoParams.position = 'top-left'"
                  >左上角</div>
                  <div 
                    class="position-option" 
                    :class="{ 'active': formData.logoParams.position === 'top-right' }"
                    @click="formData.logoParams.position = 'top-right'"
                  >右上角</div>
                  <div 
                    class="position-option" 
                    :class="{ 'active': formData.logoParams.position === 'bottom-left' }"
                    @click="formData.logoParams.position = 'bottom-left'"
                  >左下角</div>
                  <div 
                    class="position-option" 
                    :class="{ 'active': formData.logoParams.position === 'bottom-right' }"
                    @click="formData.logoParams.position = 'bottom-right'"
                  >右下角</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 新增：片头片尾视频上传区域 -->
          <div class="upload-container-flex video-upload-section">
            <!-- 片头视频上传 -->
            <div class="form-group flex-item">
              <label class="form-control-label">上传片头视频 <span class="optional-field-hint">(选填)</span></label>
              <div class="video-upload-container">
                <div class="video-upload-area" @click="triggerOpeningVideoUpload" :class="{'has-video': formData.openingMaterial.fileUrl, 'uploading': isUploadingOpening}">
                  <input type="file" ref="openingVideoInput" style="display: none;" accept="video/*" @change="handleOpeningVideoUpload" />
                  <div v-if="!formData.openingMaterial.fileUrl && !isUploadingOpening" class="upload-placeholder">
                    <i class="ri-film-line"></i>
                    <span>点击上传片头视频</span>
                    <span class="upload-tip">支持MP4, MOV格式, 小于50MB</span>
                  </div>
                  <div v-else-if="isUploadingOpening" class="upload-loading">
                    <i class="ri-loader-4-line spinning"></i>
                    <span>片头上传中...</span>
                  </div>
                  <div v-else class="video-preview">
                    <video :src="formData.openingMaterial.fileUrl" controls></video>
                    <div class="video-actions">
                      <button class="action-icon-button" @click.stop="removeOpeningVideo" title="移除片头视频">
                        <i class="ri-delete-bin-line"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 片尾视频上传 -->
            <div class="form-group flex-item">
              <label class="form-control-label">上传片尾视频 <span class="optional-field-hint">(选填)</span></label>
              <div class="video-upload-container">
                <div class="video-upload-area" @click="triggerEndingVideoUpload" :class="{'has-video': formData.endingMaterial.fileUrl, 'uploading': isUploadingEnding}">
                  <input type="file" ref="endingVideoInput" style="display: none;" accept="video/*" @change="handleEndingVideoUpload" />
                  <div v-if="!formData.endingMaterial.fileUrl && !isUploadingEnding" class="upload-placeholder">
                    <i class="ri-film-line"></i>
                    <span>点击上传片尾视频</span>
                    <span class="upload-tip">支持MP4, MOV格式, 小于50MB</span>
                  </div>
                  <div v-else-if="isUploadingEnding" class="upload-loading">
                    <i class="ri-loader-4-line spinning"></i>
                    <span>片尾上传中...</span>
                  </div>
                  <div v-else class="video-preview">
                    <video :src="formData.endingMaterial.fileUrl" controls></video>
                    <div class="video-actions">
                      <button class="action-icon-button" @click.stop="removeEndingVideo" title="移除片尾视频">
                        <i class="ri-delete-bin-line"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 新增：背景音乐上传区域 -->
          <div class="form-group bgm-upload-section">
            <label class="form-control-label">上传背景音乐 <span class="optional-field-hint">(选填)</span></label>
            <div class="bgm-upload-container">
              <div class="audio-upload-area" @click="triggerBgmUpload" :class="{'has-audio': formData.bgmParams.bgmUrl, 'uploading': isUploadingBgm}">
                <input type="file" ref="bgmFileInput" style="display: none;" accept="audio/*" @change="handleBgmUpload" />
                <div v-if="!formData.bgmParams.bgmUrl && !isUploadingBgm" class="upload-placeholder">
                  <i class="ri-music-2-line"></i>
                  <span>点击上传背景音乐</span>
                  <span class="upload-tip">支持MP3, WAV, OGG格式, 小于10MB</span>
                </div>
                <div v-else-if="isUploadingBgm" class="upload-loading">
                  <i class="ri-loader-4-line spinning"></i>
                  <span>背景音乐上传中...</span>
                </div>
                <div v-else class="audio-preview">
                  <div class="audio-info">
                    <i class="ri-music-2-fill"></i>
                    <span class="audio-name">背景音乐</span>
                  </div>
                  <audio :src="formData.bgmParams.bgmUrl" controls></audio>
                  <div class="audio-actions">
                    <button class="action-icon-button" @click.stop="removeBgm" title="移除背景音乐">
                      <i class="ri-delete-bin-line"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- 背景音乐音量控制（仅当上传了音乐时显示） -->
            <div v-if="formData.bgmParams.bgmUrl" class="bgm-volume-control">
              <label class="form-control-label">背景音乐音量:</label>
              <div class="volume-slider-container">
                <i class="ri-volume-down-line"></i>
                <input 
                  type="range" 
                  min="0" 
                  max="100" 
                  step="1"
                  v-model="formData.bgmParams.volume" 
                  class="volume-slider" 
                />
                <i class="ri-volume-up-line"></i>
                <span class="volume-value">{{ formData.bgmParams.volume }}%</span>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-control-label">视频分辨率</label>
            <div class="resolution-info">
              <div class="resolution-display">
                {{ getResolutionLabel(formData.videoParams.width, formData.videoParams.height) }}
              </div>
              <div class="resolution-note">
                <i class="ri-information-line"></i>
                分辨率根据所选模板自动设置
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
        
        <!-- 步骤5：提交任务 -->
        <div v-if="currentStep === 5" class="step-container">
          <div class="task-summary-container">
            <h3 class="summary-title">任务摘要信息</h3>
            
            <div class="task-summary-grid">
              <!-- 文本内容区 -->
              <div class="summary-section">
                <h4 class="section-title">文本内容</h4>
                <div class="section-content">
                  <div class="form-item">
                    <span class="label">视频标题:</span>
                    <span class="value">{{ formData.title || '未设置' }}</span>
                  </div>
                  <div class="form-item">
                    <span class="label">文本内容:</span>
                    <div class="text-content" :class="{ 'expanded': textExpanded }">
                      {{ formData.text || '未填写' }}
                    </div>
                    <el-button v-if="formData.text && formData.text.length > 50" 
                               type="text" 
                               @click="toggleTextExpand">
                      {{ textExpanded ? '收起' : '展开全文' }}
                    </el-button>
                  </div>
                </div>
          </div>
          
              <!-- 数字人音色区 -->
              <div class="summary-section">
                <h4 class="section-title">数字人与音色</h4>
                <div class="section-content">
                  <div class="form-item">
                    <span class="label">选择的数字人:</span>
                    <div class="digital-human-preview">
                      <img :src="getSelectedHumanAvatar()" alt="数字人头像" v-if="formData.figureId" class="avatar-preview" />
                      <span>{{ getHumanName(formData.figureId) || '未选择' }}</span>
                    </div>
                  </div>
                  <div class="form-item">
                    <span class="label">选择的音色:</span>
                    <span class="value">{{ getVoiceName(formData.ttsParams.person) || '未选择' }}</span>
                  </div>
                  <div class="form-item">
                    <span class="label">语速:</span>
                    <span class="value">{{ formData.ttsParams.speed }}</span>
                  </div>
                  <div class="form-item">
                    <span class="label">音量:</span>
                    <span class="value">{{ formData.ttsParams.volume }}</span>
                  </div>
                  <div class="form-item">
                    <span class="label">音调:</span>
                    <span class="value">{{ formData.ttsParams.pitch }}</span>
                  </div>
                </div>
              </div>
              
              <!-- 模板选择区 -->
              <div class="summary-section">
                <h4 class="section-title">模板选择</h4>
                <div class="section-content">
                  <div class="form-item template-preview">
                    <img :src="getSelectedTemplatePreview()" alt="模板预览" v-if="formData.templateId" class="template-preview-image" />
                    <span v-else>未选择模板</span>
                </div>
                </div>
              </div>
              
              <!-- 视频参数区 -->
              <div class="summary-section">
                <h4 class="section-title">视频参数</h4>
                <div class="section-content">
                  <div class="form-item">
                    <span class="label">分辨率:</span>
                    <span class="value">{{ formData.videoParams.resolution || getResolutionLabel(formData.videoParams.width, formData.videoParams.height) }}</span>
                </div>
                  
                  <div class="form-item" v-if="formData.backgroundImageUrl">
                    <span class="label">背景图片:</span>
                    <div class="image-preview">
                      <img :src="formData.backgroundImageUrl" alt="背景图片" class="small-preview" />
              </div>
                </div>
                  
                  <div class="form-item" v-if="formData.logoParams.imageUrl">
                    <span class="label">Logo:</span>
                    <div class="image-preview">
                      <img :src="formData.logoParams.imageUrl" alt="Logo" class="small-preview" />
                      <span class="value">位置: {{ getLogoPositionName(formData.logoParams.position) }}</span>
              </div>
                </div>
                  
                  <div class="form-item" v-if="formData.openingMaterial.fileUrl">
                    <span class="label">片头视频:</span>
                    <span class="value">已上传</span>
              </div>
                  
                  <div class="form-item" v-if="formData.endingMaterial.fileUrl">
                    <span class="label">片尾视频:</span>
                    <span class="value">已上传</span>
                </div>
                  
                  <div class="form-item" v-if="formData.bgmParams.bgmUrl">
                    <span class="label">背景音乐:</span>
                    <span class="value">已上传 (音量: {{ formData.bgmParams.volume }}%)</span>
              </div>
                  
                  <div class="form-item">
                    <span class="label">字幕:</span>
                    <span class="value">{{ formData.videoParams.subtitles ? '开启' : '关闭' }}</span>
                </div>
                  
                  <div class="form-item" v-if="formData.videoParams.subtitles">
                    <span class="label">字幕颜色:</span>
                    <span class="color-preview" :style="{ backgroundColor: formData.videoParams.subtitlesOptions.fontColor }"></span>
                    <span class="value">{{ formData.videoParams.subtitlesOptions.fontColor }}</span>
                </div>
              </div>
            </div>
          </div>
          
            <!-- 操作按钮 -->
          <div class="action-buttons">
              <el-button type="primary" plain @click="prevStep">上一步</el-button>
              <el-button type="primary" @click="submitTask" :loading="submitting">
                {{ submitting ? '提交中...' : '提交任务' }}
              </el-button>
          </div>
        </div>
        
          <!-- 任务状态显示 -->
          <div v-if="taskId" class="task-status-container">
            <h3 class="task-status-title">
              <i class="el-icon-video-camera"></i> 任务状态
            </h3>
            
            <div class="task-info">
              <div class="task-info-item">
                <span class="label">任务ID:</span>
                <span class="value">{{ taskId }}</span>
              </div>
              <div class="task-info-item">
                <span class="label">状态:</span>
                <span class="value status-badge" :class="getStatusClass(taskResult.status)">
                  {{ getStatusText(taskResult.status) }}
                </span>
              </div>
              <div class="task-info-item" v-if="taskResult.progress">
                <span class="label">进度:</span>
                <el-progress :percentage="taskResult.progress"></el-progress>
              </div>
            </div>
            
            <div v-if="taskResult.status === 'success'" class="video-result">
              <div class="preview-container">
                <video ref="videoPlayer" controls class="result-video">
                  <source :src="taskResult.videoUrl" type="video/mp4">
                  您的浏览器不支持视频播放
                </video>
              </div>
              
              <div class="video-actions">
                <el-button type="primary" @click="downloadVideo" icon="el-icon-download">
                  下载视频
                </el-button>
                <el-button type="success" @click="copyVideoLink" icon="el-icon-link">
                  复制视频链接
                </el-button>
              </div>
            </div>
            
            <el-alert
              v-if="taskResult.status === 'error'"
              title="任务失败"
              type="error"
              :description="taskResult.errorInfo || '视频生成失败，请重试'"
              show-icon
            ></el-alert>
          </div>
        </div>
        
        <!-- 步骤6：查看结果 -->
        <div v-if="currentStep === 6" class="step-content-panel">
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
  
  <!-- 数字人演示视频预览弹窗 -->
  <div v-if="showDigitalHumanPreview" class="preview-modal-overlay" @click.self="closeDigitalHumanPreview">
    <div class="preview-modal">
      <div class="preview-modal-header">
        <h3>{{ previewDigitalHuman?.name }} 数字人演示</h3>
        <button class="close-button" @click="closeDigitalHumanPreview">
          <i class="ri-close-line"></i>
        </button>
      </div>
      <div class="preview-modal-content">
        <video id="digital-human-preview-video" controls autoplay class="preview-video">
          <source :src="previewDigitalHuman?.demoVideo" type="video/mp4">
          您的浏览器不支持视频播放
        </video>
      </div>
    </div>
  </div>
</template>

<script>
import digitalHumanAPI from '../../utils/digitalHumanAPI';
import { ref, computed, onMounted, watch } from 'vue';

export default {
  name: 'BaiduDigitalHuman',
  setup() {
    // 状态定义
    const currentStep = ref(1);
    const formData = ref({
      currentStep: 1,
      figureId: '211808',
      templateId: 't-pf4kqasspwzwyexyte121',
      text: '',
      ttsParams: {
        person: '',
        speed: 5,
        volume: 9,
        pitch: 5
      },
      videoParams: {
        width: 540,
        height: 960,
        transparent: false,
        autoAction: true,
        subtitles: true,
        subtitlesOptions: {
          fontSize: 16,
          fontColor: '#FFFFFF',
        },
      },
      subtitleParams: {
        enabled: true,
        fontSize: 16,
        fontColor: '#FFFFFF'
      },
      logoParams: {
        enabled: false,
        imageUrl: '',
        position: 'bottom-right',
        logoUrl: '' // 添加logoUrl用于提交
      },
      backgroundImageUrl: '',
      materialUrl: '', // 添加背景图的OSS URL
      callbackUrl: '',
      // 片头片尾材质对象
      openingMaterial: {
        fileUrl: ''
      },
      endingMaterial: {
        fileUrl: ''
      },
      // 添加背景音乐参数
      bgmParams: {
        bgmUrl: '',
        volume: 50 // 背景音乐音量，默认50%
      }
    });
    
    // 模板选项
    const templateOptions = ref([
      { 
        id: 't-pf4kqasspwzwyexyte121', 
        name: '模板1', 
        ratio: '9:16', 
        isVertical: true,
        previewImage: '/images/templates/1_8c5a2e7.png' 
      },
      { 
        id: 't-af4keqsspfzwyexyte123', 
        name: '模板2', 
        ratio: '9:16', 
        isVertical: true,
        previewImage: '/images/templates/2_755cd08.png' 
      },
      { 
        id: 't-ad4eeqsspfzwyqxyte125', 
        name: '模板3', 
        ratio: '9:16', 
        isVertical: true,
        previewImage: '/images/templates/3_c730e57.png' 
      },
      { 
        id: 't-cd4eeqsspfzwyqxyte127', 
        name: '模板4', 
        ratio: '9:16', 
        
        isVertical: true,
        previewImage: '/images/templates/4_d542bdf.png' 
      }
    ]);
    
    const digitalHumans = ref([
      { 
        id: '211808', 
        name: '芝晗', 
        gender: 'female', 
        posture: '站姿', 
        background: '透明', 
        avatar: '/images/211808.png',
        demoVideo: 'https://digital-human-pipeline-output.cdn.bcebos.com/67e22d9801474b378b60aefe_689.mp4'
      },
      { 
        id: '211809', 
        name: '海霖', 
        gender: 'male', 
        posture: '站姿', 
        background: '透明', 
        avatar: '/images/211809.png',
        demoVideo: 'https://digital-human-pipeline-output.cdn.bcebos.com/67e224b58d362b07266182eb_167.mp4'
      },
      { 
        id: '211807', 
        name: '芝怡', 
        gender: 'female', 
        posture: '站姿', 
        background: '透明', 
        avatar: '/images/211807.png',
        demoVideo: 'https://digital-human-pipeline-output.cdn.bcebos.com/67e22cc201474b378b60aefd_428.mp4'
      },
      { 
        id: '211801', 
        name: '海昱', 
        gender: 'male', 
        posture: '站姿', 
        background: '透明', 
        avatar: '/images/211801.png',
        demoVideo: 'https://digital-human-pipeline-output.cdn.bcebos.com/67e2285101474b378b60aefa_939.mp4'
      },
      { 
        id: '1081', 
        name: '清馨', 
        gender: 'female', 
        posture: '站姿', 
        background: '透明', 
        avatar: '/images/1081.png',
        demoVideo: 'https://meta-human-editor-prd.cdn.bcebos.com/91eacc90-a5cc-444b-997c-d33afdcada8f/0b3b3910-adbb-475b-a2e7-b73aead54a0a/%E6%B8%85%E9%A6%A8%E7%AB%99%E5%A7%BF-%E6%B0%B4%E5%8D%B0.mp4'
      },
      { 
        id: '1112', 
        name: '清缘', 
        gender: 'female', 
        posture: '站姿', 
        background: '透明', 
        avatar: '/images/1112.png',
        demoVideo: 'https://meta-human-editor-prd.cdn.bcebos.com/91eacc90-a5cc-444b-997c-d33afdcada8f/2c9ef751-b607-45a9-bb29-43d939ed27ff/%E6%B8%85%E7%BC%98%E7%AB%99%E5%A7%BF-%E6%B0%B4%E5%8D%B0.mp4'
      }
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
    const isUploading = ref(false); // 添加上传状态变量
    const uploadProgress = ref(0);
    const taskResult = ref(null);
    const taskStatus = ref(null);
    const errorMessage = ref('');
    const autoQueryInterval = ref(null);
    const audioPlayer = ref(null);
    const videoPlayer = ref(null);
    const fileInput = ref(null);
    const logoFileInput = ref(null); // 添加Logo的文件输入ref
    // 新增：片头片尾视频相关 ref
    const openingVideoInput = ref(null);
    const endingVideoInput = ref(null);
    const isUploadingOpening = ref(false);
    const isUploadingEnding = ref(false);
    const bgmFileInput = ref(null); // 添加背景音乐上传的ref
    const isUploadingBgm = ref(false); // 添加背景音乐上传状态
    const isUploadingLogo = ref(false); // logo上传状态
    const logoUploadProgress = ref(0);
    
    // 分辨率选项
    const resolutionOptions = ref([
      { label: '720p (1280x720)', value: '1280x720' },
      { label: '1080p (1920x1080)', value: '1920x1080' },
      { label: '竖屏 (720x1280)', value: '720x1280' },
      { label: '竖屏 (1080x1920)', value: '1080x1920' }
    ]);

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
      
      // 默认选择第一个音色
      if (activeVoices.value.length > 0) {
        formData.value.ttsParams.person = activeVoices.value[0].id;
      }
    };
    
    const nextStep = () => {
      if (currentStep.value < 6) {
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
        // 总是默认选择第一个音色
        if (activeVoices.value.length > 0) {
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
    
    // 处理标题输入，去除首尾空格
    const trimTitle = () => {
      if (formData.value.title) {
        formData.value.title = formData.value.title.trim();
      }
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
    
    const getTemplateName = (templateId) => {
      const template = templateOptions.value.find(t => t.id === templateId);
      return template ? `${template.name} (${template.ratio})` : templateId;
    };
    
    const getVoiceName = (voiceId) => {
      const allVoices = [...femaleVoices.value, ...maleVoices.value];
      const voice = allVoices.find(v => v.id === voiceId);
      return voice ? voice.name : voiceId;
    };
    
    const submitTask = async () => {
      // 检查输入
      if (!formData.value.text.trim()) {
        alert('请输入文本内容');
        return;
      }
      
      // 不再强制要求背景图片
      // if (!formData.value.backgroundImageUrl) {
      //   alert('请上传背景图片');
      //   return;
      // }
      
      isSubmitting.value = true;
      
      const params = {
        figureId: formData.value.figureId,
        templateId: formData.value.templateId,
        text: formData.value.text,
        ttsParams: { ...formData.value.ttsParams },
        videoParams: {
          width: formData.value.videoParams.width,
          height: formData.value.videoParams.height,
          transparent: formData.value.videoParams.transparent,
          autoAction: formData.value.videoParams.autoAction,
          subtitles: formData.value.videoParams.subtitles,
          subtitlesOptions: { ...formData.value.videoParams.subtitlesOptions }
        },
        // 恢复materialUrl参数传递
        materialUrl: formData.value.materialUrl || formData.value.backgroundImageUrl
      };
      
      // 添加标题参数（如果有）
      if (formData.value.title) {
        params.title = formData.value.title;
      }
      
      // 如果启用了Logo，使用logoUrl参数
      if (formData.value.logoParams.enabled && formData.value.logoParams.imageUrl) {
        params.logoParams = {
          logoUrl: formData.value.logoParams.logoUrl || formData.value.logoParams.imageUrl,
          position: formData.value.logoParams.position
        };
      }
      
      // 添加片头视频参数（如果有）
      if (formData.value.openingMaterial && formData.value.openingMaterial.fileUrl) {
        params.openingMaterial = {
          fileUrl: formData.value.openingMaterial.fileUrl,
          mediaType: 'VIDEO'
        };
      }
      
      // 添加片尾视频参数（如果有）
      if (formData.value.endingMaterial && formData.value.endingMaterial.fileUrl) {
        params.endingMaterial = {
          fileUrl: formData.value.endingMaterial.fileUrl,
          mediaType: 'VIDEO'
        };
      }
      
      // 添加背景音乐参数（如果有）
      if (formData.value.bgmParams && formData.value.bgmParams.bgmUrl) {
        params.bgmParams = {
          bgmUrl: formData.value.bgmParams.bgmUrl,
          volume: formData.value.bgmParams.volume || 50
        };
      }
      
      console.log('提交任务参数:', JSON.stringify(params));
      
      try {
        const response = await digitalHumanAPI.submitVideoTask(params);
        
        if (response.data.success) {
          taskResult.value = response.data.data;
          console.log('任务提交成功:', taskResult.value);
          
          startAutoQuery();
          currentStep.value = 6;
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
        currentStep: 1,
        figureId: '211808',  // 重置时也清空数字人选择
        templateId: 't-pf4kqasspwzwyexyte121', // 修改默认模板ID
        text: '',
        ttsParams: {
          person: '',
          speed: 5,
          volume: 9,
          pitch: 5
        },
        videoParams: {
          width: 540,
          height: 960,
          transparent: false,
          autoAction: true,
          subtitles: true,
          subtitlesOptions: {
            fontSize: 16,
            fontColor: '#FFFFFF',
          },
        },
        subtitleParams: {
          enabled: true,
          fontSize: 16,
          fontColor: '#FFFFFF'
        },
        logoParams: {
          enabled: false,
          imageUrl: '',
          position: 'bottom-right'
        },
        backgroundImageUrl: '',
        callbackUrl: '',
        openingMaterial: {
          fileUrl: ''
        },
        endingMaterial: {
          fileUrl: ''
        },
        // 添加背景音乐参数重置
        bgmParams: {
          bgmUrl: '',
          volume: 50
        }
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
    
    // 背景图片上传相关方法
    const triggerFileUpload = () => {
      console.log('触发背景图片上传按钮点击');
      if (isUploading.value) {
        console.log('正在上传中，忽略点击');
        return;
      }
      if (fileInput.value) {
        console.log('fileInput存在', fileInput.value);
        fileInput.value.click();
      } else {
        console.error('fileInput不存在!');
      }
    };
    
    // 处理背景图片上传
    const handleFileUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      
      // 检查文件类型
      if (!file.type.match('image.*')) {
        showError('文件类型错误', '请上传图片文件', '', '支持的格式：JPG、PNG、JPEG');
        return;
      }
      
      // 检查文件大小 (10MB 限制)
      if (file.size > 10 * 1024 * 1024) {
        showError('文件过大', '图片大小不能超过10MB', '', '请压缩图片后重试');
        return;
      }
      
      isUploading.value = true;
      uploadProgress.value = 0;
      
      try {
        // 使用百度云直接上传接口，带进度显示
        const response = await digitalHumanAPI.uploadImageToBaiduBOS(file, 'background', {
          onProgress: (percent) => {
            uploadProgress.value = percent;
            console.log(`背景图片上传进度: ${percent}%`);
          }
        });
        
        if (response.data && response.data.data && response.data.data.url) {
          formData.value.backgroundImageUrl = response.data.data.url;
          // 重要：同时设置materialUrl，确保提交任务时使用
          formData.value.materialUrl = response.data.data.url;
          console.log('背景图片上传成功：', response.data.data.url);
        } else {
          throw new Error(response.data?.message || '上传失败');
        }
      } catch (error) {
        console.error('背景图片上传错误：', error);
        showError(
          '上传失败',
          '背景图片上传失败',
          error.response?.data?.message || error.message || '未知错误',
          '请检查网络连接和图片格式，然后重试',
          true
        );
      } finally {
        isUploading.value = false;
        uploadProgress.value = 0;
      }
    };
    
    const removeBackground = (event) => {
      event.stopPropagation(); // 阻止事件冒泡
      formData.value.backgroundImageUrl = '';
      formData.value.materialUrl = ''; // 同时清除materialUrl
    };
    
    // Logo上传相关方法
    const triggerLogoFileUpload = () => {
      console.log('触发Logo上传按钮点击');
      if (isUploading.value) {
        console.log('正在上传中，忽略点击');
        return;
      }
      if (logoFileInput.value) {
        console.log('logoFileInput存在', logoFileInput.value);
        logoFileInput.value.click();
      } else {
        console.error('logoFileInput不存在!');
      }
    };
    
    const handleLogoFileUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      
      // 检查文件类型
      if (!file.type.match('image.*')) {
        showError('文件类型错误', '请上传图片文件', '', '支持的格式：JPG、PNG、JPEG');
        return;
      }
      
      // 检查文件大小 (5MB 限制)
      if (file.size > 5 * 1024 * 1024) {
        showError('文件过大', 'Logo图片大小不能超过5MB', '', '请压缩图片后重试');
        return;
      }
      
      isUploadingLogo.value = true;
      logoUploadProgress.value = 0;
      
      try {
        // 使用百度云接口上传，带进度显示
        const response = await digitalHumanAPI.uploadImageToBaiduBOS(file, 'logo', {
          onProgress: (percent) => {
            logoUploadProgress.value = percent;
            console.log(`Logo上传进度: ${percent}%`);
          },
          retryCount: 2
        });
        
        if (response.data && response.data.data && response.data.data.url) {
          formData.value.logoParams.imageUrl = response.data.data.url;
          // 重要：同时设置logoUrl，确保提交任务时使用
          formData.value.logoParams.logoUrl = response.data.data.url;
          formData.value.logoParams.enabled = true;
          console.log('Logo上传成功：', response.data.data.url);
        } else {
          throw new Error(response.data?.message || '上传失败');
        }
      } catch (error) {
        console.error('Logo上传错误：', error);
        showError(
          '上传失败',
          'Logo上传失败',
          error.response?.data?.message || error.message || '未知错误',
          '请检查网络连接和图片格式，然后重试',
          true
        );
      } finally {
        isUploadingLogo.value = false;
        logoUploadProgress.value = 0;
      }
    };
    
    const removeLogo = (event) => {
      event.stopPropagation(); // 阻止事件冒泡
      formData.value.logoParams.imageUrl = '';
      formData.value.logoParams.enabled = false;
      formData.value.logoParams.logoUrl = ''; // 同时清除logoUrl
    };
    
    // 添加数字人预览相关的状态
    const showDigitalHumanPreview = ref(false);
    const previewDigitalHuman = ref(null);
    
    // 显示数字人演示视频的方法
    const previewDigitalHumanVideo = (human) => {
      if (human && human.demoVideo) {
        previewDigitalHuman.value = human;
        showDigitalHumanPreview.value = true;
      } else {
        console.error('无法预览数字人视频，未找到演示视频链接');
      }
    };
    
    // 关闭数字人预览弹窗
    const closeDigitalHumanPreview = () => {
      showDigitalHumanPreview.value = false;
      // 停止视频播放
      const previewVideo = document.getElementById('digital-human-preview-video');
      if (previewVideo) {
        previewVideo.pause();
      }
    };
    
    // 生命周期钩子
    onMounted(() => {
      initVoices();
    });
    
    // 添加模板选择方法
    const selectTemplate = (templateId) => {
      formData.value.templateId = templateId;
      
      // 根据选择的模板调整视频分辨率
      const selectedTemplate = templateOptions.value.find(t => t.id === templateId);
      if (selectedTemplate && selectedTemplate.isVertical) {
        // 如果是竖屏模板，默认设置为竖屏分辨率
        formData.value.videoParams.width = 1080;
        formData.value.videoParams.height = 1920;
      } else {
        // 如果是横屏模板，默认设置为横屏分辨率
        formData.value.videoParams.width = 1920;
        formData.value.videoParams.height = 1080;
      }
    };
    
    // 片头视频上传相关方法
    const triggerOpeningVideoUpload = () => {
      if (isUploadingOpening.value) return;
      openingVideoInput.value?.click();
    };
    
    const handleOpeningVideoUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
    
      // 验证文件类型 (例如：MP4, MOV)
      const allowedTypes = ['video/mp4', 'video/quicktime'];
      if (!allowedTypes.includes(file.type)) {
        alert('请上传 MP4 或 MOV 格式的视频文件');
        return;
      }
    
      // 验证文件大小（例如：限制为50MB）
      if (file.size > 50 * 1024 * 1024) {
        alert('片头视频大小不能超过50MB');
        return;
      }
    
      try {
        isUploadingOpening.value = true;
        // 改用 uploadVideoToOSS 方法
        const response = await digitalHumanAPI.uploadVideoToOSS(file, 'opening-video'); 
    
        if (response.data.success) {
          formData.value.openingMaterial.fileUrl = response.data.data.url;
          console.log('片头视频上传成功:', formData.value.openingMaterial.fileUrl);
        } else {
          alert(`片头上传失败: ${response.data.message || '未知错误'}`);
          formData.value.openingMaterial.fileUrl = '';
        }
      } catch (error) {
        console.error('上传片头视频失败:', error);
        alert('上传片头视频过程中发生错误');
        formData.value.openingMaterial.fileUrl = '';
      } finally {
        isUploadingOpening.value = false;
      }
      event.target.value = ''; // 重置文件输入
    };
    
    const removeOpeningVideo = (event) => {
      event?.stopPropagation();
      formData.value.openingMaterial.fileUrl = '';
    };
    
    // 片尾视频上传相关方法
    const triggerEndingVideoUpload = () => {
      if (isUploadingEnding.value) return;
      endingVideoInput.value?.click();
    };
    
    const handleEndingVideoUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
    
      const allowedTypes = ['video/mp4', 'video/quicktime'];
      if (!allowedTypes.includes(file.type)) {
        alert('请上传 MP4 或 MOV 格式的视频文件');
        return;
      }
    
      if (file.size > 50 * 1024 * 1024) {
        alert('片尾视频大小不能超过50MB');
        return;
      }
    
      try {
        isUploadingEnding.value = true;
        // 改用 uploadVideoToOSS 方法
        const response = await digitalHumanAPI.uploadVideoToOSS(file, 'ending-video');
    
        if (response.data.success) {
          formData.value.endingMaterial.fileUrl = response.data.data.url;
          console.log('片尾视频上传成功:', formData.value.endingMaterial.fileUrl);
        } else {
          alert(`片尾上传失败: ${response.data.message || '未知错误'}`);
          formData.value.endingMaterial.fileUrl = '';
        }
      } catch (error) {
        console.error('上传片尾视频失败:', error);
        alert('上传片尾视频过程中发生错误');
        formData.value.endingMaterial.fileUrl = '';
      } finally {
        isUploadingEnding.value = false;
      }
      event.target.value = ''; // 重置文件输入
    };
    
    const removeEndingVideo = (event) => {
      event?.stopPropagation();
      formData.value.endingMaterial.fileUrl = '';
    };
    
    // 添加背景音乐上传相关方法
    const triggerBgmUpload = () => {
      if (isUploadingBgm.value) return;
      bgmFileInput.value?.click();
    };
    
    const handleBgmUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
    
      // 验证文件类型 (例如：MP3, WAV, OGG)
      const allowedTypes = ['audio/mp3', 'audio/mpeg', 'audio/wav', 'audio/ogg'];
      if (!allowedTypes.includes(file.type)) {
        alert('请上传 MP3, WAV 或 OGG 格式的音频文件');
        return;
      }
    
      // 验证文件大小（例如：限制为10MB）
      if (file.size > 10 * 1024 * 1024) {
        alert('背景音乐大小不能超过10MB');
        return;
      }
    
      try {
        isUploadingBgm.value = true;
        // 使用视频上传API，但标记类型为bgm
        const response = await digitalHumanAPI.uploadVideoToOSS(file, 'bgm');
    
        if (response.data.success) {
          formData.value.bgmParams.bgmUrl = response.data.data.url;
          console.log('背景音乐上传成功:', formData.value.bgmParams.bgmUrl);
        } else {
          alert(`背景音乐上传失败: ${response.data.message || '未知错误'}`);
          formData.value.bgmParams.bgmUrl = '';
        }
      } catch (error) {
        console.error('上传背景音乐失败:', error);
        alert('上传背景音乐过程中发生错误');
        formData.value.bgmParams.bgmUrl = '';
      } finally {
        isUploadingBgm.value = false;
      }
      event.target.value = ''; // 重置文件输入
    };
    
    const removeBgm = (event) => {
      event?.stopPropagation();
      formData.value.bgmParams.bgmUrl = '';
    };
    
    // 添加展开/收起文字的状态
    const textExpanded = ref(false);

    // 切换文本展开/收起状态
    const toggleTextExpand = () => {
      textExpanded.value = !textExpanded.value;
    };

    // 获取选中数字人的头像
    const getSelectedHumanAvatar = () => {
      const selectedHuman = digitalHumans.value.find(h => h.id === formData.value.figureId);
      return selectedHuman ? selectedHuman.avatar : '';
    };

    // 获取选中模板的预览图
    const getSelectedTemplatePreview = () => {
      const selectedTemplate = templateOptions.value.find(t => t.id === formData.value.templateId);
      return selectedTemplate ? selectedTemplate.previewImage : '';
    };

    // 获取Logo位置的名称
    const getLogoPositionName = (position) => {
      const positionMap = {
        'top-left': '左上角',
        'top-right': '右上角',
        'bottom-left': '左下角',
        'bottom-right': '右下角'
      };
      return positionMap[position] || position;
    };
    
    // 返回模板中需要使用的内容
    return {
      currentStep,
      formData,
      digitalHumans,
      femaleVoices,
      maleVoices,
      activeVoices,
      isSubmitting,
      isQuerying,
      isUploading,
      uploadProgress,
      taskResult,
      taskStatus,
      errorMessage,
      audioPlayer,
      videoPlayer,
      fileInput,
      templateOptions,
      logoFileInput, // 导出 logoFileInput
      // 新增导出
      openingVideoInput,
      endingVideoInput,
      isUploadingOpening,
      isUploadingEnding,
      bgmFileInput, // 添加bgmFileInput
      isUploadingBgm, // 添加isUploadingBgm
      isUploadingLogo, // logo上传状态
      logoUploadProgress, // Logo上传进度
      
      // 方法
      nextStep,
      prevStep,
      selectDigitalHuman,
      selectVoice,
      previewVoice,
      getVoicePreviewUrl,
      getHumanName,
      getTemplateName,
      getVoiceName,
      getSelectedHumanGender,
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
      triggerFileUpload,
      handleFileUpload,
      removeBackground,
      showDigitalHumanPreview,
      previewDigitalHuman,
      previewDigitalHumanVideo,
      closeDigitalHumanPreview,
      trimTitle,
      selectTemplate,
      triggerLogoFileUpload,
      handleLogoFileUpload,
      removeLogo,
      // 新增方法导出
      triggerOpeningVideoUpload,
      handleOpeningVideoUpload,
      removeOpeningVideo,
      triggerEndingVideoUpload,
      handleEndingVideoUpload,
      removeEndingVideo,
      triggerBgmUpload, // 添加triggerBgmUpload
      handleBgmUpload, // 添加handleBgmUpload
      removeBgm, // 添加removeBgm
      textExpanded,
      toggleTextExpand,
      getSelectedHumanAvatar,
      getSelectedTemplatePreview,
      getLogoPositionName
    };
  }
};
</script>

<style scoped>
@import '../../assets/css/text-creation-common.css';

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
  max-height: 250px; /* 提高高度，从220px增加到250px */
  overflow-y: auto; /* 超出时添加滚动 */
  padding: 10px; /* 增加内边距 */
  border: 1px solid #eee;
  border-radius: 8px;
}

.digital-human-card.compact-card {
  width: auto;
  margin: 0;
  padding: 10px; /* 增加内边距 */
  border: 2px solid transparent;
  border-radius: 8px;
  transition: all 0.2s;
  position: relative; /* 添加相对定位，便于预览按钮的绝对定位 */
  display: flex;
  flex-direction: column;
  align-items: center;
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
  width: 85px; /* 增加头像尺寸，从70px增加到85px */
  height: 85px; /* 增加头像尺寸，从70px增加到85px */
  margin: 0 auto 8px; /* 增加底部间距 */
  border-radius: 50%;
  overflow: hidden;
}

.compact-card .human-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 改为contain，确保头像完全显示 */
  object-position: center top; /* 居中并靠上对齐 */
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
  grid-template-columns: repeat(4, 1fr); /* 修改为4列 */
  gap: 10px;
  max-height: 300px;
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
  background-color: #fdeaea;
  color: #ef5350;
}

.status-unknown {
  background-color: #f5f5f5;
  color: #9e9e9e;
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
  /* 移动端样式 */
}

/* 背景图片上传样式 */
.background-upload-container {
  margin-top: 10px;
}

.background-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px; /* 固定高度 */
}

.background-upload-area:hover {
  border-color: var(--primary-color, #ba003f);
  background-color: rgba(186, 0, 63, 0.05);
}

.background-upload-area.has-image {
  border-style: solid;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #666;
  height: 100%;
  justify-content: center;
  width: 100%;
}

.upload-placeholder i {
  font-size: 48px;
  color: #aaa;
}

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.background-preview {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.background-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  display: block;
}

.background-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.action-icon-button {
  background-color: rgba(0, 0, 0, 0.5);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.action-icon-button:hover {
  background-color: rgba(0, 0, 0, 0.7);
  transform: scale(1.1);
}

.background-thumbnail {
  max-width: 150px;
  max-height: 100px;
  overflow: hidden;
  border-radius: 4px;
  margin-top: 8px;
}

.background-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Logo上传样式 */
.logo-upload-container {
  margin-top: 10px;
}

.logo-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px; /* 匹配背景图片上传区域高度 */
}

.logo-upload-area:hover {
  border-color: var(--primary-color, #ba003f);
  background-color: rgba(186, 0, 63, 0.05);
}

.logo-upload-area.has-image {
  border-style: solid;
  padding: 0;
  position: relative;
  overflow: hidden;
  min-height: auto;
  max-height: 120px;
}

.logo-preview {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 6px;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  display: block;
}

.logo-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.logo-position-selector {
  margin-top: 10px;
}

.position-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
}

.position-option {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.position-option:hover {
  border-color: #007bff;
  background-color: rgba(0, 123, 255, 0.05);
}

.position-option.active {
  border-color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  color: #007bff;
}

/* 分辨率展示样式 */
.resolution-info {
  background-color: #f5f7fa;
  border-radius: 6px;
  padding: 12px 15px;
  margin-top: 8px;
}

.resolution-display {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.resolution-note {
  font-size: 13px;
  color: #666;
  margin-top: 5px;
  display: flex;
  align-items: center;
}

.resolution-note i {
  margin-right: 5px;
  color: #007bff;
}

/* 数字人卡片新增的预览按钮样式 */
.digital-human-actions {
  position: absolute;
  top: 5px;
  right: 5px;
  z-index: 10;
}

.demo-button {
  background-color: rgba(186, 0, 63, 0.8); /* 更深的背景色 */
  color: white; /* 白色图标 */
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: absolute;
  top: 5px;
  right: 5px;
  transition: all 0.2s;
  padding: 0;
  opacity: 0.85;
  font-size: 14px;
}

.demo-button:hover {
  opacity: 1;
  transform: scale(1.1);
}

/* 预览弹窗样式 */
.preview-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.preview-modal {
  background: white;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
}

.preview-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #e6e9ed;
}

.preview-modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.close-button:hover {
  color: #333;
}

.preview-modal-content {
  padding: 0;
}

.preview-video {
  width: 100%;
  display: block;
}

/* 调整数字人卡片的样式，添加相对定位以支持绝对定位的子元素 */
.digital-human-card {
  position: relative;
}

/* 表单辅助样式 */
.optional-field-hint {
  font-size: 12px;
  color: #999;
  font-weight: normal;
  margin-left: 5px;
}

.input-helper-text {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  text-align: right;
}

.no-voices-found {
  margin-top: 10px;
  text-align: center;
  color: #999;
}

/* 模板选择样式 */
.template-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 8px;
  border: 1px solid #eee;
  border-radius: 8px;
}

.template-card {
  position: relative;
  outline: 2px solid transparent; 
  outline-offset: -2px;
  border-radius: 6px;
  overflow: hidden;
  transition: outline-color 0.2s;
  background-color: #f9f9f9;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.template-card:hover {
  outline-color: rgba(186, 0, 63, 0.5); /* 改变outline颜色进行高亮 */
}

.template-card.selected {
  outline-color: var(--primary-color, #ba003f); /* 使用outline表示选中 */
  background-color: rgba(186, 0, 63, 0.05);
}

/* 为模板卡片内的预览区使用更具体的选择器 */
.template-card .template-card-preview {
  width: 100%;
  position: relative;
  overflow: hidden;
  aspect-ratio: 9 / 16;
  background-color: #eee;
}

.template-card .template-card-preview img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.template-info {
  padding: 6px;
  flex-shrink: 0;
}

.template-name {
  font-weight: 500;
  font-size: 13px;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.template-ratio {
  color: #666;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .template-grid {
    grid-template-columns: repeat(3, 1fr); /* 中等屏幕3列 */
  }
}

@media (max-width: 768px) {
  .template-grid {
    grid-template-columns: repeat(2, 1fr); /* 小屏幕2列 */
  }
}

/* 上传中的状态样式 */
.upload-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #1976d2;
  height: 100%;
  width: 100%;
}

.upload-loading i {
  font-size: 24px;
  margin-bottom: 8px;
}

.background-upload-area.uploading,
.logo-upload-area.uploading {
  border-color: #1976d2;
  background-color: rgba(25, 118, 210, 0.05);
  cursor: wait;
}

.spinning {
  animation: spinner-rotate 1s linear infinite;
}

@keyframes spinner-rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 显式上传按钮样式 */
.explicit-upload-button {
  background-color: #f5f7fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.explicit-upload-button:hover {
  background-color: #e9ebee;
}

/* 横向排列的上传容器 */
.upload-container-flex {
  display: flex;
  flex-direction: row;
  gap: 20px;
  margin-bottom: 20px;
}

/* 每个上传区域项 */
.flex-item {
  flex: 1;
  min-width: 0; /* 防止flex项溢出 */
}

/* 在小屏幕上改为纵向 */
@media (max-width: 768px) {
  .upload-container-flex {
    flex-direction: column;
    gap: 10px;
  }
}

/* 操作按钮容器 */
.operations-container {
  display: flex;
  gap: 15px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.operation-item {
  flex: 1;
  min-width: 150px;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  width: 100%;
}

.action-button:hover {
  background-color: #d32f2f;
}

/* 修改现有上传按钮样式 */
.explicit-upload-button {
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 10px;
  width: 100%;
  transition: background-color 0.3s;
}

.explicit-upload-button:hover {
  background-color: #1565c0;
}

/* 新增：片头片尾视频上传区域 */
.video-upload-container {
  margin-top: 10px;
}

.video-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px; /* 固定高度 */
}

.video-upload-area:hover {
  border-color: var(--primary-color, #ba003f);
  background-color: rgba(186, 0, 63, 0.05);
}

.video-upload-area.has-video {
  border-style: solid;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #666;
  height: 100%;
  justify-content: center;
  width: 100%;
}

.upload-placeholder i {
  font-size: 48px;
  color: #aaa;
}

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.video-preview {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-preview video {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  display: block;
}

.video-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.action-icon-button {
  background-color: rgba(0, 0, 0, 0.5);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.action-icon-button:hover {
  background-color: rgba(0, 0, 0, 0.7);
  transform: scale(1.1);
}

.video-thumbnail {
  max-width: 150px;
  max-height: 100px;
  overflow: hidden;
  border-radius: 4px;
  margin-top: 8px;
}

.video-thumbnail video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 在原有样式文件末尾添加 */

/* 片头片尾视频上传区域特定样式 */
.video-upload-section {
  margin-top: 20px; /* 与上方区域增加间距 */
}

.video-upload-container {
  margin-top: 10px;
}

.video-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px; /* 固定高度，与背景/logo一致 */
  position: relative; /* 为了预览和加载状态 */
  overflow: hidden;
  background-color: #fafafa;
}

.video-upload-area:hover {
  border-color: var(--primary-color, #ba003f);
  background-color: rgba(186, 0, 63, 0.02);
}

.video-upload-area.has-video {
  border-style: solid;
  padding: 0;
}

.video-upload-area.uploading {
  border-color: #1976d2;
  background-color: rgba(25, 118, 210, 0.05);
  cursor: wait;
}

/* 视频预览样式 */
.video-preview {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #000;
}

.video-preview video {
  max-width: 100%;
  max-height: 100%;
  display: block;
  object-fit: contain;
}

.video-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 5px;
  z-index: 1;
}

/* 移除按钮等图标按钮样式复用 */
.action-icon-button {
  /* 样式已在之前定义，可复用 */
}

/* 背景音乐上传样式 */
.bgm-upload-container {
  margin-top: 10px;
}

.audio-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 100px; /* 音频上传区域高度小一点 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
}

.audio-upload-area:hover {
  border-color: var(--primary-color, #ba003f);
  background-color: rgba(186, 0, 63, 0.05);
}

.audio-upload-area.has-audio {
  border-style: solid;
  padding: 12px;
  position: relative;
}

.audio-preview {
  width: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
}

.audio-preview .audio-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
  align-self: flex-start;
}

.audio-preview .audio-info i {
  font-size: 24px;
  color: var(--primary-color, #ba003f);
}

.audio-preview .audio-name {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.audio-preview audio {
  width: 100%;
  max-width: 100%;
  height: 40px;
}

/* 音量控制样式优化 */
.bgm-volume-control {
  margin-top: 15px;
  background-color: #f9f9f9;
  padding: 10px 15px;
  border-radius: 8px;
}

.volume-slider-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.volume-slider {
  flex: 1;
  height: 5px;
  accent-color: var(--primary-color, #ba003f);
}

.volume-value {
  font-size: 14px;
  font-weight: bold;
  min-width: 40px;
  text-align: right;
  color: #555;
}

/* 通用上传相关样式(被误删恢复) */
.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #666;
  height: 100%;
  justify-content: center;
  width: 100%;
}

.upload-placeholder i {
  font-size: 48px;
  color: #aaa;
}

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.audio-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.audio-preview {
  width: 100%;
}

/* 任务摘要和提交页样式 */
.task-summary-container {
  margin-bottom: 30px;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.summary-title {
  font-size: 18px;
  margin-bottom: 20px;
  color: #409EFF;
  border-bottom: 1px solid #EBEEF5;
  padding-bottom: 10px;
}

.task-summary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.summary-section {
  background-color: #F8F9FA;
  border-radius: 6px;
  padding: 15px;
}

.section-title {
  font-size: 16px;
  color: #606266;
  margin-bottom: 12px;
  font-weight: 500;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-item {
  display: flex;
  align-items: flex-start;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.label {
  font-weight: 500;
  color: #606266;
  width: 100px;
  flex-shrink: 0;
}

.value {
  color: #303133;
  flex-grow: 1;
}

.text-content {
  max-height: 60px;
  overflow: hidden;
  color: #303133;
  line-height: 1.5;
  transition: max-height 0.3s;
  
  &.expanded {
    max-height: 300px;
    overflow-y: auto;
  }
}

.digital-human-preview {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-preview {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.template-preview {
  display: flex;
  justify-content: center;
}

.template-preview-image {
  max-width: 100%;
  max-height: 150px; /* 增加高度从80px到150px */
  object-fit: contain;
  border-radius: 4px;
}

.small-preview {
  max-width: 80px;
  max-height: 60px;
  border-radius: 4px;
}

.image-preview {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-preview {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  margin-right: 8px;
  vertical-align: middle;
  border: 1px solid #dcdfe6;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 任务状态容器样式 */
.task-status-container {
  margin-top: 30px;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.task-status-title {
  font-size: 18px;
  margin-bottom: 20px;
  color: #409EFF;
  border-bottom: 1px solid #EBEEF5;
  padding-bottom: 10px;
}

.task-info {
  margin-bottom: 20px;
}

.task-info-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.status-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 14px;
  
  &.status-success {
    background-color: #67C23A;
    color: white;
  }
  
  &.status-error {
    background-color: #F56C6C;
    color: white;
  }
  
  &.status-processing {
    background-color: #E6A23C;
    color: white;
  }
  
  &.status-waiting {
    background-color: #909399;
    color: white;
  }
}

.video-result {
  margin-top: 20px;
}

.preview-container {
  width: 100%;
  margin-bottom: 15px;
}

.result-video {
  width: 100%;
  max-height: 400px;
  border-radius: 6px;
}

.video-actions {
  display: flex;
  gap: 10px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .task-summary-grid {
    grid-template-columns: 1fr;
  }
}

/* 任务摘要中的模板预览容器，注意这里使用更具体的选择器以避免与上面的冲突 */
.summary-section .template-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  padding: 8px;
  border-radius: 4px;
  min-height: 160px;
}

.summary-section .template-preview-image {
  max-width: 100%;
  max-height: 150px;
  object-fit: contain;
  border-radius: 4px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #eee;
  border-radius: 4px;
  margin-top: 8px;
  overflow: hidden;
}

.progress-bar-inner {
  height: 100%;
  background-color: #4caf50;
  border-radius: 4px;
  transition: width 0.3s ease;
}
</style> 