<template>
  <div class="ppt-video-container">
    <h2 class="page-title">数字人PPT讲解视频生成</h2>
    
    <div class="content-wrapper">
      <!-- 上传部分 -->
      <div class="upload-section">
        <h3>1. 上传PPT文件</h3>
        
        <div 
          class="upload-area" 
          @click="triggerFileInput" 
          @dragover.prevent 
          @drop.prevent="handleDrop"
        >
          <input 
            type="file" 
            ref="fileInput" 
            style="display: none;" 
            @change="handleFileChange"
            accept=".ppt,.pptx"
          />
          
          <div v-if="!selectedFile" class="upload-placeholder">
            <i class="el-icon-upload"></i>
            <div class="upload-text">
              <p>点击或拖拽文件到此处上传</p>
              <small>支持PPT、PPTX格式，文件大小不超过100MB</small>
              </div>
                </div>
          
          <div v-else class="file-info">
            <div class="file-icon">
              <i class="el-icon-document"></i>
                </div>
            <div class="file-details">
              <div class="file-name">{{ selectedFile.name }}</div>
              <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
              <div class="upload-status">
                <span :class="statusClass">
                  <i :class="statusIcon"></i>
                  {{ uploadStatus }}
                </span>
                </div>
              <el-progress 
                v-if="isUploading" 
                :percentage="uploadProgress" 
                :format="percentFormat"
              ></el-progress>
              </div>
            <div class="file-actions">
              <el-button 
                type="danger" 
                size="small" 
                circle 
                @click.stop="removeFile"
                :disabled="isUploading"
              >
                <i class="el-icon-delete"></i>
              </el-button>
            </div>
          </div>
        </div>
        
        <div class="upload-actions">
          <div style="display: flex; justify-content: center; width: 100%;">
            <el-button 
              type="primary" 
              @click="uploadFile" 
              :disabled="!canUpload"
              :loading="isUploading"
              style="margin-right: 10px;"
            >
              上传文件
            </el-button>
            <el-button 
              type="info" 
              @click="resetForm"
              :disabled="isUploading || !selectedFile"
              style="margin-left: 10px;"
            >
              重置
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 修改视频名称样式 -->
      <el-form-item label="视频名称" style="margin-top: 25px; margin-bottom: 25px;" v-if="uploadedUrl">
          <el-input 
          v-model="videoName" 
          placeholder="请输入视频名称" 
          :maxlength="50"
          show-word-limit
          style="font-size: 16px; font-weight: 500;"
        >
          <template #prepend>
            <div style="background-color: #f56c6c; color: white; padding: 0 10px;">名称</div>
          </template>
        </el-input>
        </el-form-item>

      <!-- 数字人选择部分 -->
      <div class="digital-humans-section">
        <h3>2. 选择数字人形象</h3>
        
        <div class="digital-human-container" ref="digitalHumansContainer">
          <div v-if="loadingDigitalHumans" class="loading-container">
            <el-skeleton :rows="3" animated />
                </div>
          <template v-else>
            <div class="digital-humans-slider">
              <div class="slider-arrow left" @click="scrollLeft">
                <i class="el-icon-arrow-left" style="font-size: 18px;"></i>
              </div>
              
              <div class="digital-humans-list" ref="digitalHumansList">
                <div
                  v-for="human in digitalHumans"
                  :key="human.bizId"
                  class="digital-human-item"
                  :class="{ 'selected': selectedDigitalHuman && selectedDigitalHuman.bizId === human.bizId }"
                  @click="selectDigitalHuman(human)"
                >
                  <div class="human-image">
                    <img v-if="human.summaryImage" :src="human.summaryImage" :alt="human.name">
                    <div v-else class="no-image">无图片</div>
                </div>
                  <div class="human-info">
                    <div class="human-name">{{ human.name }}</div>
                    <div class="human-desc">{{ human.industry || '未知行业' }}</div>
                    <div class="human-actions">
                      <el-button type="text" size="small" @click.stop="viewDigitalHumanVideo(human)">
                        <i class="el-icon-video-play"></i> 预览
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="slider-arrow right" @click="scrollRight">
                <i class="el-icon-arrow-right" style="font-size: 18px;"></i>
                </div>
            </div>
          </template>
        </div>

        <!-- 隐藏数字人详情数据 -->
        <div v-if="selectedDigitalHuman && selectedDigitalHuman.detailData" class="human-detail-raw-data" style="display: none;">
          <h4>数字人详情数据</h4>
          
          <!-- 添加关键信息展示区域 -->
          <div class="key-info-panel">
            <div class="key-info-item">
              <span class="key-label">数字人ID (bizId):</span>
              <span class="key-value">{{ selectedDigitalHuman.bizId }}</span>
                </div>
            <div class="key-info-item">
              <span class="key-label">虚拟人ID (virtualHumanId):</span>
              <span class="key-value">{{ selectedDigitalHuman.detailData.virtualHumanId }}</span>
            </div>
            <div class="key-info-item">
              <span class="key-label">支持透明背景:</span>
              <span class="key-value">{{ selectedDigitalHuman.detailData.supportTransparency ? '是' : '否' }}</span>
            </div>
            <div class="key-info-item">
              <span class="key-label">姿势数量:</span>
              <span class="key-value">{{ selectedDigitalHuman.detailData.postureInfos?.length || 0 }}</span>
            </div>
            <div class="key-info-item">
              <span class="key-label">语音数量:</span>
              <span class="key-value">{{ selectedDigitalHuman.detailData.voiceInfos?.length || 0 }}</span>
            </div>
          </div>
          
          <el-collapse>
            <el-collapse-item title="查看完整数据" name="1">
              <pre class="raw-data-content">{{ JSON.stringify(selectedDigitalHuman.detailData, null, 2) }}</pre>
            </el-collapse-item>
          </el-collapse>
                </div>

        <!-- 姿势和语音选择区域 -->
        <div v-if="selectedDigitalHuman" class="selection-container">
          <h4>选择数字人姿势</h4>
          <div class="posture-options" style="min-height: 280px;">
            <div class="slider-container">
              <div class="slider-arrow left" @click="scrollPostureLeft">
                <i class="el-icon-arrow-left" style="font-size: 18px;"></i>
                </div>
              
              <div class="posture-list" ref="posturesList">
                <el-radio-group v-model="selectedPosture" class="posture-radio-group">
                  <el-radio 
                    v-for="posture in selectedDigitalHuman.postures" 
                    :key="posture.bizId || posture.postureId || posture.id"
                    :label="posture"
                    class="posture-radio"
                  >
                    <div class="posture-radio-content">
                      <div class="posture-preview" v-if="posture.previewPicture">
                        <el-image 
                          :src="posture.previewPicture" 
                          :alt="posture.name || '姿势预览'"
                          fit="cover"
                          style="width: 140px; height: 140px; border-radius: 4px;"
                        >
                          <template #error>
                            <div class="image-placeholder-small">
                              <i class="el-icon-picture-outline"></i>
                </div>
                          </template>
                        </el-image>
                      </div>
                      <div class="posture-info">
                        <span class="posture-name">{{ posture.name || (posture.type ? `${posture.type}姿态` : '默认姿态') }}</span>
                      </div>
                    </div>
                  </el-radio>
            </el-radio-group>
          </div>
              
              <div class="slider-arrow right" @click="scrollPostureRight">
                <i class="el-icon-arrow-right" style="font-size: 18px;"></i>
                </div>
          </div>
          </div>

          <h4>选择数字人语音</h4>
          <div class="voice-options" style="min-height: 320px;">
            <div class="slider-container">
              <div class="slider-arrow left" @click="scrollVoiceLeft">
                <i class="el-icon-arrow-left" style="font-size: 18px;"></i>
              </div>
              
              <div class="voice-list" ref="voicesList">
                <el-radio-group v-model="selectedVoice" class="voice-radio-group">
                  <el-radio 
                    v-for="voice in selectedDigitalHuman.voiceInfos" 
                    :key="voice.voiceId || voice.bizId"
                    :label="voice"
                    class="voice-radio"
                  >
                    <div class="voice-radio-content">
                      <div class="voice-info-container">
                        <span class="voice-name">{{ voice.displayName || voice.name || '默认语音' }}</span>
                        <span class="voice-info">{{ voice.gender === '男' ? '男声' : voice.gender === '女' ? '女声' : '' }} | {{ voice.language || '' }}</span>
                </div>
                      <div class="audio-player-container" @click.stop>
                        <audio-player 
                          v-if="voice.auditionFile" 
                          :src="voice.auditionFile" 
                          class="audio-player"
                        ></audio-player>
                </div>
                    </div>
                  </el-radio>
            </el-radio-group>
          </div>
              
              <div class="slider-arrow right" @click="scrollVoiceRight">
                <i class="el-icon-arrow-right" style="font-size: 18px;"></i>
        </div>
            </div>
          </div>
                </div>
              </div>
              
      <!-- 请求体内容展示区域(隐藏) -->
      <div class="request-body-section" v-if="requestBody">
        <h4>数字人视频请求体</h4>
        <!-- 隐藏请求地址 -->
        <div class="request-info" style="display: none;">
          <div class="request-url">
            <span class="label">请求地址：</span>
            <span class="value">https://openapi.xiaoice.com/vh/openapi/video/task/v2/ppt/submit</span>
            <el-button 
              type="text" 
              size="small" 
              @click="copyRequestUrl" 
              class="copy-btn"
            >
              复制
                  </el-button>
                </div>
              </div>
            
        <!-- 隐藏请求体内容 -->
        <div class="request-body-container" style="display: none;">
          <div class="request-body-header">
            <span>请求体内容</span>
            <el-button 
              type="text" 
              size="small" 
              @click="copyRequestBody" 
              class="copy-btn"
            >
              复制请求体
            </el-button>
            </div>
          <div class="request-body-content">{{ formattedRequestBody }}</div>
          </div>
          
        <!-- 任务结果展示区域 -->
        <div v-if="taskResult" class="task-result-container">
          <h4>任务提交结果</h4>
          <pre class="task-result-content">{{ formattedTaskResult }}</pre>
            </div>
            
        <!-- 任务状态查询结果展示区域 -->
        <div v-if="taskStatusResult" class="task-status-container">
          <h4>任务状态查询结果</h4>
          <div class="task-key-info">
            <div class="task-key-info-item">
              <span class="task-key-info-label">任务状态:</span>
              <span class="task-key-info-value" :class="getStatusClass(taskStatusResult.data?.status)">{{ getStatusText(taskStatusResult.data?.status) }}</span>
            </div>
            <div class="task-key-info-item">
              <span class="task-key-info-label">任务进度:</span>
              <span class="task-key-info-value">{{ formatProgress(taskStatusResult.data?.progress) }}</span>
              <span class="task-key-info-progress">
                <el-progress 
                  v-if="taskStatusResult.data?.progress"
                  :percentage="Number(taskStatusResult.data.progress)"
                  :status="taskStatusResult.data?.status === 'COMPLETED' ? 'success' : 
                          (taskStatusResult.data?.status === 'ERROR' || taskStatusResult.data?.status === 'error') ? 'exception' : ''"
                ></el-progress>
              </span>
          </div>
        </div>
          <pre class="task-status-content" style="display: none;">{{ formattedTaskStatusResult }}</pre>
          
          <!-- 添加查看视频按钮 -->
          <div class="view-video-button" v-if="taskStatusResult.data && taskStatusResult.data.status === 'COMPLETED' && taskStatusResult.data.output_url">
            <el-button 
              type="primary" 
              icon="el-icon-video-play" 
              @click="viewGeneratedVideo"
            >
              查看生成的视频
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 任务按钮区域(单独显示) -->
      <div class="submit-task-container" v-if="requestBody" style="margin-top: 20px; display: block;">
                <el-button 
          type="success" 
          @click="submitVideoTask" 
          :disabled="!requestBody"
          :loading="submittingTask"
          class="submit-task-btn"
        >
          提交视频生成任务
                </el-button>
                <el-button 
          type="primary" 
          @click="queryTaskStatus" 
          :disabled="!taskResult || !taskResult.data"
          :loading="queryingTaskStatus"
          class="query-status-btn"
        >
          刷新任务状态
                </el-button>
        </div>
      </div>
          
    <!-- 视频播放器弹窗 -->
    <el-dialog
      title="视频播放"
      v-model="videoDialogVisible"
      width="70%"
      center
    >
      <div class="video-player-container">
        <video
          v-if="selectedVideoUrl"
          class="video-player"
          controls
          autoplay
        >
          <source :src="selectedVideoUrl" type="video/mp4" />
          您的浏览器不支持视频播放
        </video>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import AudioPlayer from '../../components/AudioPlayer.vue';

export default {
  name: 'PPTVideo',
  components: {
    AudioPlayer
  },
  setup() {
    // 文件上传相关
    const fileInput = ref(null);
    const selectedFile = ref(null);
    const selectedFileName = ref('');
    const selectedFileSize = ref(0);
    const uploadStatus = ref('');
    const uploadProgress = ref(0);
    const isUploading = ref(false);
    const uploadedUrl = ref('');
    
    // 数字人相关
    const digitalHumans = ref([]);
    const loadingDigitalHumans = ref(false);
    const selectedDigitalHuman = ref(null);
    const digitalHumansContainer = ref(null);
    const digitalHumansList = ref(null);
    
    // 姿势相关
    const selectedPosture = ref(null);
    
    // 语音相关
    const voices = ref([]);
    const loadingVoices = ref(false);
    const selectedVoice = ref(null);
    
    // 视频播放相关
    const videoDialogVisible = ref(false);
    const selectedVideoUrl = ref('');
    
    // 请求体相关
    const requestBody = ref(null);
    
    // 任务提交相关
    const submittingTask = ref(false);
    const taskResult = ref(null);
    
    // 查询任务状态相关
    const queryingTaskStatus = ref(false);
    const taskStatusResult = ref(null);
    
    // 滚动相关
    const posturesList = ref(null);
    const voicesList = ref(null);
    
    // 视频设置相关
    const videoName = ref(`数字人演示视频-${new Date().toISOString().slice(0, 10)}`);
    const scriptContent = ref('');
    const resolution = ref('720P');
    
    // 计算属性
    const canUpload = computed(() => {
      return (
        selectedFile.value && 
        selectedDigitalHuman.value && 
        !isUploading.value
      );
    });

    const statusClass = computed(() => {
      const statusMap = {
        '准备上传': 'status-default',
        '上传中': 'status-info animate-spin',
        '上传成功': 'status-success',
        '上传失败': 'status-error'
      };
      return statusMap[uploadStatus.value] || 'status-default';
    });

    const statusIcon = computed(() => {
      const iconMap = {
        '准备上传': 'el-icon-upload2',
        '上传中': 'el-icon-loading',
        '上传成功': 'el-icon-check',
        '上传失败': 'el-icon-close'
      };
      return iconMap[uploadStatus.value] || 'el-icon-upload2';
    });

    // 计算属性：是否可以生成请求体
    const canGenerateRequest = computed(() => {
      return uploadedUrl.value && 
             selectedDigitalHuman.value && 
             selectedPosture.value && 
             selectedVoice.value;
    });
    
    // 计算属性：格式化的请求体
    const formattedRequestBody = computed(() => {
      if (!requestBody.value) return '';
      return JSON.stringify(requestBody.value, null, 2);
    });

    // 任务结果格式化
    const formattedTaskResult = computed(() => {
      if (!taskResult.value) return '';
      return JSON.stringify(taskResult.value, null, 2);
    });

    // 计算属性：格式化任务状态查询结果
    const formattedTaskStatusResult = computed(() => {
      return taskStatusResult.value ? JSON.stringify(taskStatusResult.value, null, 2) : '';
    });

    // 格式化进度为百分比
    const formatProgress = (progress) => {
      if (!progress && progress !== 0) return '0.00%';
      return `${Number(progress).toFixed(2)}%`;
    };

    // 获取任务状态对应的状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'COMPLETED': '已完成',
        'PROCESSING': '处理中',
        'FAILED': '失败',
        'ERROR': '错误',
        'error': '错误',
        'QUEUED': '排队中',
        'PENDING': '等待中'
      };
      return statusMap[status] || status;
    };

    // 任务状态样式类
    const getStatusClass = (status) => {
      if (!status) return '';
      if (status === 'COMPLETED') return 'status-completed';
      if (status === 'PROCESSING' || status === 'QUEUED' || status === 'PENDING') return 'status-processing';
      return 'status-error';
    };

    // 生命周期钩子
    onMounted(() => {
      fetchDigitalHumans();
    });

    // 数字人相关方法
    const fetchDigitalHumans = async () => {
      loadingDigitalHumans.value = true;
      
      try {
        console.log('开始获取数字人列表...');
        // 始终请求真实数据
        const response = await axios.get('/api/v1/digital_human/ppt/humans');
        console.log('获取数字人列表响应:', response.data);
        
        if (response.data.code === 200) {
          digitalHumans.value = response.data.data.records || [];
          console.log('成功获取数字人列表，数量:', digitalHumans.value.length);
        } else {
          throw new Error(response.data.message || '获取数字人列表失败');
        }
      } catch (error) {
        console.error('获取数字人列表出错:', error);
        ElMessage.error('获取数字人列表失败，请稍后重试');
        digitalHumans.value = [];
      } finally {
        loadingDigitalHumans.value = false;
      }
    };
    
    const viewDigitalHumanVideo = (human) => {
      if (human.projectVideo) {
        selectedVideoUrl.value = human.projectVideo;
        videoDialogVisible.value = true;
      } else {
        ElMessage.info('该数字人暂无演示视频');
      }
    };
    
    const selectDigitalHuman = (human) => {
      selectedDigitalHuman.value = human;
      // 重置姿势和语音选择
      selectedPosture.value = null;
      selectedVoice.value = null;
      // 获取该数字人的姿态列表和详细信息
      fetchDigitalHumanDetail(human.bizId);
    };
    
    // 获取数字人详细信息
    const fetchDigitalHumanDetail = async (humanId) => {
      try {
        console.log('开始获取数字人详情:', humanId);
        const response = await axios.get(`/api/v1/digital_human/ppt/human/${humanId}`);
        console.log('数字人详情API返回数据:', JSON.stringify(response.data, null, 2));
        
        if (response.data.code === 200) {
          // 保存完整的原始数据
          const humanData = response.data.data;
          
          // 获取姿势信息 - 直接使用API返回的数据
          const postures = humanData.postureInfos || [];
          console.log('姿势数据列表:', JSON.stringify(postures, null, 2));
          
          // 获取语音信息 - 直接使用API返回的数据
          const voiceInfos = humanData.voiceInfos || [];
          console.log('语音数据列表:', JSON.stringify(voiceInfos, null, 2));
          
          // 更新数字人对象，保存原始数据用于展示
          selectedDigitalHuman.value = {
            ...selectedDigitalHuman.value,
            postures: postures,
            voiceInfos: voiceInfos,
            detailData: humanData  // 保存完整的原始数据
          };
          
          // 默认选择第一个姿势和语音，如果有
          if (postures.length > 0) {
            selectedPosture.value = postures[0];
            console.log('默认选择姿势:', JSON.stringify(selectedPosture.value, null, 2));
          }
          
          if (voiceInfos.length > 0) {
            // 尝试选择与性别匹配的语音
            const humanGender = humanData.gender || '';
            const matchingVoice = voiceInfos.find(voice => voice.gender === humanGender);
            
            if (matchingVoice) {
              selectedVoice.value = matchingVoice;
              console.log('选择性别匹配的语音:', JSON.stringify(matchingVoice, null, 2));
            } else {
              selectedVoice.value = voiceInfos[0];
              console.log('未找到性别匹配的语音，使用第一个:', JSON.stringify(voiceInfos[0], null, 2));
            }
          }
          
          console.log('更新后的数字人数据:', JSON.stringify(selectedDigitalHuman.value, null, 2));
          ElMessage.success(`成功获取"${selectedDigitalHuman.value.name}"的详细信息`);
        } else {
          ElMessage.error(`获取数字人详情失败: ${response.data.message || '未知错误'}`);
        }
      } catch (error) {
        console.error('获取数字人详情信息失败:', error);
        ElMessage.error('获取数字人详情失败，请稍后重试');
      }
    };
    
    // 获取可用的语音列表
    const fetchVoices = async () => {
      loadingVoices.value = true;
      selectedVoice.value = null;
      
      try {
        const response = await axios.get('/api/v1/digital_human/ppt/voices');
        if (response.data.code === 0) {
          voices.value = response.data.data || [];
          
          // 如果有可用的语音，默认选择第一个
          if (voices.value.length > 0) {
            selectedVoice.value = voices.value[0];
        } else {
            createDefaultVoices();
          }
        } else {
          throw new Error(response.data.message || '获取语音列表失败');
        }
      } catch (error) {
        console.error('获取语音列表失败:', error);
        ElMessage.warning('获取语音列表失败，将使用默认语音');
        createDefaultVoices();
      } finally {
        loadingVoices.value = false;
      }
    };
    
    // 创建默认语音列表作为备用
    const createDefaultVoices = () => {
      voices.value = [
        {
          voiceId: "default_voice_id_1",
          name: "默认中文女声",
          language: "中文",
          supportInteractive: true
        },
        {
          voiceId: "default_voice_id_2",
          name: "默认中文男声",
          language: "中文",
          supportInteractive: true
        },
        {
          voiceId: "default_voice_id_3",
          name: "默认英文女声",
          language: "英文",
          supportInteractive: true
        }
      ];
      
      // 默认选择第一个语音
      selectedVoice.value = voices.value[0];
    };
    
    // 文件上传相关方法
    const triggerFileInput = () => {
      fileInput.value.click();
    };
    
    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (file) {
        validateAndSetFile(file);
      }
    };
    
    const handleDrop = (event) => {
      const file = event.dataTransfer.files[0];
      if (file) {
        validateAndSetFile(file);
      }
    };
    
    const validateAndSetFile = (file) => {
      // 验证文件类型 - 放宽类型检查
      const allowedTypes = [
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/octet-stream', // 添加通用二进制文件类型
        'application/powerpoint',
        'application/mspowerpoint',
        'application/x-mspowerpoint'
      ];
      const fileExt = file.name.split('.').pop().toLowerCase();
      
      // 只通过文件扩展名判断，放宽类型检查
      if (!['ppt', 'pptx'].includes(fileExt)) {
        ElMessage.error('只支持上传PPT文件(.ppt, .pptx)');
        return;
      }
      
      // 验证文件大小 (100MB)
      const maxSize = 100 * 1024 * 1024;
      if (file.size > maxSize) {
        ElMessage.error('文件大小不能超过100MB');
        return;
      }
      
      selectedFile.value = file;
      uploadStatus.value = '准备上传';
      uploadProgress.value = 0;
      uploadedUrl.value = '';
      
      console.log('文件已验证通过:', file.name, '类型:', file.type, '扩展名:', fileExt);
    };
    
    const uploadFile = async () => {
      if (!selectedFile.value) {
        ElMessage.warning('请选择PPT文件');
        return;
      }
      
      if (!selectedDigitalHuman.value) {
        ElMessage.warning('请选择数字人');
        return;
      }
      
      isUploading.value = true;
      uploadStatus.value = '上传中';
      uploadProgress.value = 0;
      
      // 真实上传逻辑
      try {
        const formData = new FormData();
        formData.append('file', selectedFile.value);
        formData.append('digitalHumanId', selectedDigitalHuman.value.bizId);
        
        console.log('开始上传文件:', selectedFile.value.name);
        console.log('文件类型:', selectedFile.value.type);
        console.log('文件大小:', selectedFile.value.size);
        
        const response = await axios.post('/api/v1/digital_human/ppt/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            uploadProgress.value = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
          },
          // 增加超时时间，处理大文件
          timeout: 120000 // 2分钟超时
        });
        
        console.log('上传响应:', response.data);
        
        if (response.data.code === 0) {
          uploadStatus.value = '上传成功';
          uploadedUrl.value = response.data.data.url;
          } else {
          throw new Error(response.data.message || '上传失败');
          }
        } catch (error) {
        console.error('上传文件失败:', error);
        uploadStatus.value = '上传失败';
        
        // 提供更详细的错误信息
        let errorMsg = '文件上传失败';
        if (error.response) {
          errorMsg += `: ${error.response.status} ${error.response.statusText}`;
          console.error('错误详情:', error.response.data);
        } else if (error.request) {
          errorMsg += ': 服务器未响应，请检查网络连接';
        } else if (error.message) {
          errorMsg += `: ${error.message}`;
        }
        
        ElMessage.error(errorMsg);
        } finally {
        isUploading.value = false;
      }
    };
    
    // 公共辅助方法
    const removeFile = () => {
      selectedFile.value = null;
      uploadStatus.value = '';
      uploadProgress.value = 0;
      uploadedUrl.value = '';
      // 重置文件输入框，允许重新选择同一个文件
      fileInput.value.value = '';
    };
    
    const resetForm = () => {
      removeFile();
      selectedDigitalHuman.value = null;
    };
    
    const copyUrl = () => {
      if (uploadedUrl.value) {
        navigator.clipboard.writeText(uploadedUrl.value)
          .then(() => {
            ElMessage.success('已复制到剪贴板');
          })
          .catch(() => {
            ElMessage.error('复制失败，请手动复制');
          });
      }
    };
    
    const percentFormat = (percent) => {
      return `${percent}%`;
    };
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B';
      
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    const scrollLeft = () => {
      if (digitalHumansList.value) {
        digitalHumansList.value.scrollBy({ left: -200, behavior: 'smooth' });
      }
    };
    
    const scrollRight = () => {
      if (digitalHumansList.value) {
        digitalHumansList.value.scrollBy({ left: 200, behavior: 'smooth' });
      }
    };

    // 滚动姿势列表
    const scrollPostureLeft = () => {
      if (posturesList.value) {
        posturesList.value.scrollBy({ left: -200, behavior: 'smooth' });
      }
    };
    
    const scrollPostureRight = () => {
      if (posturesList.value) {
        posturesList.value.scrollBy({ left: 200, behavior: 'smooth' });
      }
    };
    
    // 滚动语音列表
    const scrollVoiceLeft = () => {
      if (voicesList.value) {
        voicesList.value.scrollBy({ left: -200, behavior: 'smooth' });
      }
    };
    
    const scrollVoiceRight = () => {
      if (voicesList.value) {
        voicesList.value.scrollBy({ left: 200, behavior: 'smooth' });
      }
    };

    // 生成请求体
    const generateRequestBody = () => {
      if (!uploadedUrl.value || !selectedDigitalHuman.value || !selectedPosture.value || !selectedVoice.value) {
        ElMessage.warning('请确保所有必要信息已完成');
        return null;
      }
      
      // 获取数字人相关ID
      const virtualHumanId = selectedDigitalHuman.value.bizId || "";
      const virtualHumanPostureId = selectedPosture.value.bizId || selectedPosture.value.postureId || "";
      const voiceId = selectedVoice.value.voiceId || selectedVoice.value.bizId || "";
      
      // 创建符合后端要求的请求体
      const body = {
        outputVideoName: videoName.value || `数字人演示视频-${new Date().toISOString().slice(0, 10)}`,
        width: 1920,
        height: 1080,
        pptUrl: uploadedUrl.value,
        convertType: "VIDEO",
        virtualHumanId: virtualHumanId,
        virtualHumanPostureId: virtualHumanPostureId,
        voiceId: voiceId,
        showCaption: true,
        creationDetail: {
          scenes: [
            {
              virtualHuman: {
                attributes: {
                  width: 344,
                  height: 1080,
                  x: 1517,
                  y: 309,
                  forceMattingType: 0
                },
                virtualHumanId: virtualHumanId,
                virtualHumanPostureId: virtualHumanPostureId,
                zIndex: 20
              },
              tts: {
                voiceId: voiceId,
                rate: 1,
                pitch: 1,
                volume: 50
              },
              voiceText: "PPT中设置了取备注文本，此字段无效，字幕坐标不传时默认居中",
              caption: {
                topRight: true,
                topLeft: false,
                topCenter: true,
                zIndex: 60,
                attributes: {
                  visible: true,
                  fontColor: "#333333",
                  spacing: 1,
                  italic: false,
                  underline: false,
                  bold: true,
                  y: 1000,
                  fontSize: 44
                }
              }
            }
          ]
        },
        pptInfo: {
          pptUrl: uploadedUrl.value,
          convertType: "VIDEO",
          getText: true,
          singlePageSecond: 5,
          attributes: {
            width: 1920,
            height: 1080,
            x: 0,
            y: 0
          }
        }
      };
      
      requestBody.value = body;
      return body;
    };

    // 每当选择改变时，尝试生成请求体
    watch([uploadedUrl, selectedDigitalHuman, selectedPosture, selectedVoice], () => {
      if (canGenerateRequest.value) {
        generateRequestBody();
      } else {
        requestBody.value = null;
      }
    });
    
    // 复制请求地址
    const copyRequestUrl = () => {
      navigator.clipboard.writeText('https://openapi.xiaoice.com/vh/openapi/video/task/v2/ppt/submit')
        .then(() => {
          ElMessage.success('请求地址已复制到剪贴板');
        })
        .catch(() => {
          ElMessage.error('复制失败，请手动复制');
        });
    };
    
    // 复制请求体
    const copyRequestBody = () => {
      if (requestBody.value) {
        navigator.clipboard.writeText(JSON.stringify(requestBody.value, null, 2))
          .then(() => {
            ElMessage.success('请求体已复制到剪贴板');
          })
          .catch(() => {
            ElMessage.error('复制失败，请手动复制');
          });
      }
    };

    // 提交视频生成任务
    const submitVideoTask = async () => {
      if (!requestBody.value) {
        ElMessage.warning('请先选择文件并设置所有必要参数');
        return;
      }
      
      submittingTask.value = true;
      
      try {
        const response = await axios.post('/api/v1/digital_human/ppt/submit_task', requestBody.value);
        if (response.status === 200 && response.data) {
          ElMessage.success('提交任务成功！');
          taskResult.value = response.data;
          // 自动查询一次状态
          setTimeout(queryTaskStatus, 1000);
          } else {
          ElMessage.error(`提交任务失败: ${response.data?.message || '未知错误'}`);
        }
      } catch (error) {
        console.error('提交任务错误:', error);
        ElMessage.error(`提交任务错误: ${error.response?.data?.message || error.message || '未知错误'}`);
      } finally {
        submittingTask.value = false;
      }
    };

    // 查询任务状态方法
    const queryTaskStatus = async () => {
      if (!taskResult.value || !taskResult.value.data) {
        ElMessage.warning('请先提交任务获取任务ID');
        return;
      }
      
      const taskId = taskResult.value.data;
      queryingTaskStatus.value = true;
      
      try {
        // 通过后端API代理查询任务状态
        const response = await axios.get(
          `/api/v1/digital_human/ppt/task/${taskId}`,
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        
        taskStatusResult.value = response.data;
        
        // 检查响应中是否包含错误信息
        if (response.data.data && response.data.data.status === 'error') {
          console.error('任务状态查询返回错误:', response.data.data.error);
          ElMessage.warning('查询任务状态返回错误，请查看详细信息');
          } else {
          ElMessage.success('任务状态查询成功');
          
          // 检查任务是否已完成
          if (response.data.data && response.data.data.status === 'COMPLETED' && response.data.data.output_url) {
            ElMessage.success('视频已生成完成，可以点击"查看视频"按钮观看');
          }
        }
      } catch (error) {
        console.error('查询任务状态失败:', error);
        taskStatusResult.value = {
          error: true,
          message: error.message || '查询任务状态失败',
          response: error.response ? error.response.data : null
        };
        ElMessage.error('查询任务状态失败，请查看详细信息');
      } finally {
        queryingTaskStatus.value = false;
      }
    };

    // 添加打开生成视频的方法
    const viewGeneratedVideo = () => {
      if (taskStatusResult.value && 
          taskStatusResult.value.data && 
          taskStatusResult.value.data.status === 'COMPLETED' && 
          taskStatusResult.value.data.output_url) {
        selectedVideoUrl.value = taskStatusResult.value.data.output_url;
        videoDialogVisible.value = true;
      } else {
        ElMessage.warning('视频尚未生成完成或未找到视频URL');
      }
    };

    return {
      // 引用
      fileInput,
      digitalHumansContainer,
      digitalHumansList,
      posturesList,
      voicesList,
      // 状态
      selectedFile,
      selectedFileName,
      selectedFileSize,
      uploadStatus,
      uploadProgress,
      isUploading,
      uploadedUrl,
      digitalHumans,
      loadingDigitalHumans,
      selectedDigitalHuman,
      selectedPosture,
      selectedVoice,
      videoName,
      videoDialogVisible,
      selectedVideoUrl,
      requestBody,
      submittingTask,
      taskResult,
      queryingTaskStatus,
      taskStatusResult,
      // 计算属性
      canUpload,
      statusClass,
      statusIcon,
      canGenerateRequest,
      formattedRequestBody,
      formattedTaskResult,
      formattedTaskStatusResult,
      // 格式化函数
      formatProgress,
      getStatusText,
      getStatusClass,
      // 方法
      fetchDigitalHumans,
      viewDigitalHumanVideo,
      selectDigitalHuman,
      fetchDigitalHumanDetail,
      fetchVoices,
      triggerFileInput,
      handleFileChange,
      handleDrop,
      validateAndSetFile,
      uploadFile,
      removeFile,
      resetForm,
      copyUrl,
      percentFormat,
      formatFileSize,
      scrollLeft,
      scrollRight,
      scrollPostureLeft,
      scrollPostureRight,
      scrollVoiceLeft,
      scrollVoiceRight,
      generateRequestBody,
      copyRequestUrl,
      copyRequestBody,
      submitVideoTask,
      queryTaskStatus,
      viewGeneratedVideo
    };
  }
};
</script>

<style scoped>
.ppt-video-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 30px;
  font-size: 24px;
  color: #303133;
}

.upload-section {
  margin-bottom: 30px;
}

.upload-area {
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #f9f9f9;
}

.upload-area:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-placeholder i {
  font-size: 48px;
  color: #909399;
  margin-bottom: 16px;
}

.upload-text p {
  margin: 0 0 8px;
  font-size: 16px;
  color: #606266;
}

.upload-text small {
  color: #909399;
}

.file-info {
  display: flex;
  align-items: center;
  text-align: left;
}

.file-icon {
  font-size: 40px;
  color: #e6a23c;
  margin-right: 16px;
}

.file-details {
  flex: 1;
}

.file-name {
  font-weight: bold;
  margin-bottom: 4px;
  word-break: break-all;
}

.file-size {
  color: #909399;
  font-size: 14px;
}

.file-actions {
  margin-left: 16px;
}

.remove-btn {
  background: none;
  border: none;
  color: #f56c6c;
  cursor: pointer;
  font-size: 18px;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.3s;
}

.remove-btn:hover {
  background-color: rgba(245, 108, 108, 0.1);
}

.status-container {
  margin: 20px 0;
  padding: 12px;
  border-radius: 4px;
  background-color: #f5f7fa;
}

.status-indicator {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.status-indicator i {
  margin-right: 8px;
  font-size: 18px;
}

/* 添加上传动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.animate-spin i {
  animation: spin 1s linear infinite;
}

.status-default { /* 默认/选择文件后的状态 */
  color: #909399;
}

.status-info {
  color: #409eff;
}

.status-success {
  color: #67c23a;
}

.status-error {
  color: #f56c6c;
}

.progress-bar {
  margin-top: 12px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 24px 0;
}

.url-section {
  margin-top: 20px;
  padding: 16px;
  border-radius: 4px;
  background-color: #ecf5ff;
  border: 1px solid #d9ecff;
}

.url-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-weight: bold;
  color: #409eff;
}

.url-header i {
  margin-right: 8px;
}

.url-input {
  margin-bottom: 8px;
}

.url-note {
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}

/* 数字人和语音共享样式 */
.digital-human-section {
  margin: 30px 0;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  border: 1px solid #ebeef5;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.loading-indicator {
  display: flex;
  align-items: center;
  color: #909399;
  font-size: 14px;
}

.loading-indicator i {
  margin-right: 8px;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  text-align: center;
}

/* 数字人列表滑动容器样式 */
.digital-humans-slider {
  display: flex;
  align-items: center;
  position: relative;
}

.digital-humans-list {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 10px 0;
  /* 隐藏滚动条但保持功能 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.digital-humans-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.slider-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  cursor: pointer;
  z-index: 2;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.slider-arrow.left {
  left: 5px;
}

.slider-arrow.right {
  right: 5px;
}

.digital-human-item {
  flex: 0 0 120px; /* 减小宽度 */
  margin-right: 10px;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.digital-human-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.digital-human-item.selected {
  border: 2px solid #409eff;
}

.human-image {
  height: 100px; /* 减小图片高度 */
  width: 100%;
  overflow: hidden;
}

.human-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.human-info {
  padding: 6px;
}

.human-name {
  font-size: 12px;
  font-weight: bold;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.human-desc {
  font-size: 10px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.human-actions {
  display: flex;
  justify-content: center;
  margin-top: 2px;
}

.human-actions .el-button--text {
  padding: 2px;
  font-size: 10px;
}

/* 视频播放器 */
.video-player-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.video-player {
  width: 100%;
  max-height: 70vh;
  border-radius: 4px;
}

/* 数字人详细信息样式 */
.digital-human-details {
  margin-top: 20px;
  padding: 16px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.digital-human-details h4 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  color: #303133;
}

/* 请求体相关样式 */
.request-generator-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.generate-btn {
  padding: 10px 24px;
}

.request-body-section {
  margin-top: 30px;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  border: 1px solid #ebeef5;
}

.request-body-section h4 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  color: #303133;
}

.request-info {
  margin-bottom: 16px;
  padding: 12px;
  background-color: #ecf5ff;
  border-radius: 4px;
}

.request-url {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.request-url .label {
  font-weight: bold;
  margin-right: 8px;
  color: #303133;
}

.request-url .value {
  font-family: monospace;
  color: #409eff;
  word-break: break-all;
}

.copy-btn {
  margin-left: 8px;
}

.request-body-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.request-body-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #dcdfe6;
}

.request-body-content {
  margin: 0;
  padding: 16px;
  background-color: #ffffff;
  color: #606266;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.6;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 500px;
  overflow-y: auto;
}

/* 添加任务提交相关样式 */
.submit-task-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.submit-task-btn,
.query-status-btn {
  padding: 12px 20px;
  font-size: 16px;
  background-color: #f56c6c !important; /* 紫荆红色 */
  border-color: #f56c6c !important; /* 紫荆红色边框 */
}

.submit-task-btn:hover,
.query-status-btn:hover {
  background-color: #f78989 !important; /* 紫荆红色浅色 */
  border-color: #f78989 !important;
}

.task-result-container {
  margin-top: 20px;
  padding: 16px;
  border-radius: 8px;
  background-color: #f0f9eb;
  border: 1px solid #e1f3d8;
}

.task-result-container h4 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  color: #67c23a;
}

.task-result-content {
  margin: 0;
  padding: 16px;
  background-color: #ffffff;
  color: #606266;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.6;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.task-status-container {
  margin-top: 20px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

/* 添加任务状态关键信息样式 */
.task-key-info {
  margin: 15px 0;
  padding: 15px;
  background-color: #f0f9eb;
  border-radius: 8px;
  border: 1px solid #e1f3d8;
}

.task-key-info-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.task-key-info-label {
  font-weight: bold;
  min-width: 100px;
  color: #303133;
}

.task-key-info-value {
  color: #409eff;
  font-weight: 500;
}

.task-key-info-value.status-completed {
  color: #67c23a;
}

.task-key-info-value.status-error {
  color: #f56c6c;
}

.task-key-info-value.status-processing {
  color: #e6a23c;
}

.task-key-info-progress {
  margin-left: 15px;
  flex: 1;
}

.task-status-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 12px;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #ddd;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  white-space: pre-wrap;
  line-height: 1.5;
  color: #333;
}

.query-status-btn {
  margin-left: 10px;
}

.view-video-button {
  margin-top: 20px;
  text-align: center;
}

/* 添加姿势和语音选择的样式 */
.posture-selection-section,
.voice-selection-section {
  margin-top: 25px;
  margin-bottom: 25px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.posture-selection-section h4,
.voice-selection-section h4 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  color: #303133;
}

.posture-options,
.voice-options {
  width: 100%;
}

.posture-radio-group,
.voice-radio-group {
  display: flex;
  flex-wrap: nowrap;
  width: 100%;
}

.posture-radio,
.voice-radio {
  margin: 0 15px 15px 0 !important;
  min-width: 300px; /* 进一步增加语音选项的宽度到300px */
  flex: 0 0 auto;
}

.posture-radio .el-radio__label,
.voice-radio .el-radio__label {
  width: 100%;
  min-width: 200px;
  padding-left: 10px;
  padding-bottom: 10px;
}

.posture-radio-content,
.voice-radio-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s;
  background-color: white;
  height: auto;
  min-height: 200px; /* 再次增加姿势选项的高度 */
}

.posture-radio-content:hover,
.voice-radio-content:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-color: #f56c6c; /* 改为紫荆红色 */
}

.posture-radio-content {
  justify-content: space-between;
  text-align: center;
}

.voice-radio-content {
  height: auto;
  min-height: 240px; /* 再次增加语音选项的高度 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  text-align: center;
}

.posture-preview {
  display: flex;
  justify-content: center;
  margin-bottom: 15px; /* 增加间距 */
}

.posture-preview img {
  width: 140px; /* 增加图片尺寸 */
  height: 140px; /* 增加图片尺寸 */
  object-fit: cover;
}

.posture-info {
  padding: 8px 0;
  text-align: center;
}

.posture-name {
  font-weight: 500;
  color: #303133;
  display: block;
  text-align: center;
  font-size: 14px; /* 增加字体大小 */
}

.voice-info-container {
  margin-bottom: 15px; /* 增加间距 */
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px dashed #e4e7ed;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 80px;
  justify-content: center;
}

.voice-name {
  font-weight: 500;
  color: #303133;
  display: block;
  margin-bottom: 10px; /* 增加间距 */
  font-size: 16px; /* 增加字体大小 */
  text-align: center;
}

.voice-info {
  font-size: 14px; /* 增加字体大小 */
  color: #606266;
  display: block;
  line-height: 1.4; /* 增加行高 */
  text-align: center;
}

.audio-player-container {
  border-top: 1px solid #f0f0f0;
  padding-top: 15px; /* 增加内边距 */
  margin-top: auto;
  text-align: center;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.audio-player {
  width: 100%;
  height: 45px; /* 增加音频播放器高度 */
}

/* 原始数据显示区域样式 */
.human-details-section {
  margin-top: 25px;
  margin-bottom: 25px;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.human-details-section h4 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  color: #303133;
}

.details-container {
  width: 100%;
}

.details-content {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 300px;
  overflow-y: auto;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.human-detail-raw-data {
  margin: 20px 0;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background-color: #fff;
  padding: 15px;
}

.human-detail-raw-data h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
  color: #333;
}

.raw-data-content {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  color: #444;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 400px;
  overflow-y: auto;
  background-color: #f7f7f7;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

/* 添加关键信息面板样式 */
.key-info-panel {
  margin: 10px 0 15px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.key-info-item {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.key-info-item:last-child {
  margin-bottom: 0;
}

.key-label {
  font-weight: bold;
  min-width: 180px;
  color: #606266;
}

.key-value {
  font-family: 'Courier New', Courier, monospace;
  color: #409eff;
  word-break: break-all;
}

.image-placeholder-small {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
}

/* 修复语音选择问题，确保正确的z-index */
.el-radio {
  z-index: 0;
}

.el-radio__input {
  z-index: 1;
}

/* 滑动容器样式 */
.slider-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}

.posture-list,
.voice-list {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 10px 0;
  width: calc(100% - 80px);
  /* 隐藏滚动条但保持功能 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.posture-list {
  min-height: 250px;
  height: auto;
}

.voice-list {
  min-height: 300px;
  height: auto;
}

.posture-list::-webkit-scrollbar,
.voice-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

/* 确保Radio选中样式正确 */
.el-radio.is-bordered.is-checked {
  border-color: #409eff;
}

/* 设置选择区域的边距 */
.posture-options,
.voice-options {
  margin-bottom: 20px;
}

/* 设置按钮区域样式 */
.submit-task-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 25px;
  margin-bottom: 25px;
}

.submit-task-btn,
.query-status-btn {
  padding: 12px 20px;
  font-size: 16px;
}

.submit-task-btn {
  min-width: 180px;
}

.query-status-btn {
  min-width: 150px;
}

/* 确保任务状态区域样式正确 */
.task-result-container,
.task-status-container {
  margin-top: 25px;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e1f3d8;
}

.task-result-container h4,
.task-status-container h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
}

.task-result-content,
.task-status-content {
  max-height: 300px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 15px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}

/* 确保图标显示正确 */
.el-icon-delete:before {
  content: "\e6d7";
}

.el-icon-arrow-left:before {
  content: "\e6dc";
}

.el-icon-arrow-right:before {
  content: "\e6dd";
}

/* 添加图标基础样式 */
[class^="el-icon-"], [class*=" el-icon-"] {
  font-family: 'element-icons' !important;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>