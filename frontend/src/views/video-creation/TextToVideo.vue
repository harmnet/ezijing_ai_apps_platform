<template>
  <div class="longform-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2 class="page-title test-style">AI文生视频</h2>
    </div>
      <div class="page-actions">
        <button class="action-btn" title="历史记录" @click="showHistoryModal = true">
          <i class="ri-history-line icon-red"></i>
        </button>
        <button class="action-btn" title="创作小贴士" @click="showTips">
          <i class="ri-lightbulb-line icon-red"></i>
        </button>
      </div>
    </div>

    <!-- 主要内容区域 - 使用两列布局 -->
    <div class="main-layout">
      <!-- 左侧：输入参数 -->
      <div class="left-panel">
        <div class="section-header">
          <h3 class="section-title">
            <i class="ri-settings-3-line icon-red"></i>
            输入参数
          </h3>
        </div>

        <div class="form-group">
          <label for="prompt" class="required">文本提示词</label>
          <textarea 
            id="prompt" 
            v-model="formData.prompt"
            placeholder="请输入详细的视频描述，越具体越好，例如：'一只可爱的橙色小猫在阳光明媚的花园里玩耍，蓝天白云下，有许多蝴蝶在飞舞'"
            class="form-control"
            rows="5"
          ></textarea>
          <small class="form-text">提示词越详细越好，建议包含场景、光线、细节等描述</small>
        </div>

        <div class="form-group">
          <label>视频比例</label>
          <div class="radio-group">
            <label class="radio-item">
              <input type="radio" v-model="formData.ratio" value="16:9">
              <span class="radio-label">
                <i class="ri-movie-line"></i>
                16:9 (横屏)
              </span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.ratio" value="9:16">
              <span class="radio-label">
                <i class="ri-smartphone-line"></i>
                9:16 (竖屏)
              </span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.ratio" value="1:1">
              <span class="radio-label">
                <i class="ri-stop-line"></i>
                1:1 (正方形)
              </span>
            </label>
          </div>
        </div>
        
        <!-- 高级选项按钮 -->
        <button 
          type="button" 
          class="advanced-options-button" 
          @click="toggleAdvancedOptions"
        >
          <i class="ri-settings-4-line"></i>
          {{ showAdvancedOptions ? '隐藏高级选项' : '显示高级选项' }}
        </button>
        
        <!-- 高级选项面板 -->
        <div 
          class="advanced-options-panel" 
          :class="{ show: showAdvancedOptions }"
        >
          <h3>高级设置</h3>
          
          <div class="form-group">
            <label>视频时长</label>
            <div class="radio-group">
              <label class="radio-item">
                <input type="radio" v-model="formData.duration" value="3">
                <span class="radio-label">3秒</span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="formData.duration" value="5">
                <span class="radio-label">5秒</span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="formData.duration" value="10">
                <span class="radio-label">10秒</span>
              </label>
            </div>
          </div>
          
          <div class="form-group">
            <label>帧率</label>
            <div class="radio-group">
              <label class="radio-item">
                <input type="radio" v-model="formData.fps" value="24">
                <span class="radio-label">24 帧/秒</span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="formData.fps" value="30">
                <span class="radio-label">30 帧/秒</span>
              </label>
            </div>
          </div>
          
          <div class="form-group">
            <label>分辨率</label>
            <div class="radio-group">
              <label class="radio-item">
                <input type="radio" v-model="formData.resolution" value="480p">
                <span class="radio-label">480p (标清)</span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="formData.resolution" value="720p">
                <span class="radio-label">720p (高清)</span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="formData.resolution" value="1080p">
                <span class="radio-label">1080p (全高清)</span>
              </label>
            </div>
          </div>
          
          <div class="form-group">
            <label>水印</label>
            <div class="radio-group">
              <label class="radio-item">
                <input type="radio" v-model="formData.watermark" :value="false">
                <span class="radio-label">不添加</span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="formData.watermark" :value="true">
                <span class="radio-label">添加</span>
              </label>
            </div>
          </div>
        </div>

        <div class="usage-tips">
          <h4><i class="ri-information-line"></i> 使用说明</h4>
          <ul>
            <li>输入详细的文本提示词，描述您想要生成的视频内容</li>
            <li>生成的视频链接有效期为24小时，请及时下载保存</li>
            <li>视频生成通常需要1-2分钟，请耐心等待</li>
            <li>提示词越详细，生成的视频质量越高</li>
            <li>可以调整视频比例和高级参数以满足不同需求</li>
          </ul>
        </div>

        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="generateVideo" class="primary-button" :disabled="isLoading || !formData.prompt">
            <i class="ri-movie-2-line" v-if="!isLoading"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isLoading ? '生成中...' : '生成视频' }}
          </button>
          <button @click="resetForm" class="secondary-button">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>

      <!-- 右侧：生成结果 -->
      <div class="right-panel">
        <!-- 参考案例区域 -->
        <div class="reference-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-gallery-line icon-red"></i>
              参考案例
            </h3>
            <div class="scroll-buttons">
              <button class="scroll-btn" @click="scrollReferences('left')" title="向左滚动">
                <i class="ri-arrow-left-s-line"></i>
              </button>
              <button class="scroll-btn" @click="scrollReferences('right')" title="向右滚动">
                <i class="ri-arrow-right-s-line"></i>
              </button>
            </div>
          </div>
          <div class="reference-list" ref="referenceList">
            <div v-for="(example, index) in referenceExamples" 
                 :key="index" 
                 class="reference-card"
                 @click="applyExample(example)">
              <div class="reference-info">
                <h4>{{ example.title }}</h4>
                <p class="reference-desc">{{ example.description }}</p>
                <div class="reference-tags">
                  <span class="tag"><i class="ri-aspect-ratio-line"></i> {{ example.ratio }}</span>
                  <span class="tag"><i class="ri-time-line"></i> {{ example.duration }}秒</span>
                  <span class="tag"><i class="ri-film-line"></i> {{ example.fps }}帧/秒</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-movie-2-line icon-red"></i>
              视频预览
            </h3>
            <div class="status-indicator" :class="statusClass" v-if="taskStatus">
              {{ statusText }}
            </div>
          </div>

          <div class="result-content-wrapper">
            <!-- 加载中显示 -->
            <div class="loading-overlay" v-if="isLoading">
              <div class="loading-spinner"></div>
              <div class="loading-text">{{ loadingMessage }}</div>
              <!-- 移除进度条，仅显示加载动画和文本 -->
              <div class="loading-tips" v-if="showLoadingTips">
                <h4><i class="ri-information-line"></i> 生成视频中，您可以：</h4>
                <ul>
                  <li>查看参考案例获取创意灵感</li>
                  <li>提前准备下一个视频的提示词</li>
                  <li>视频生成时间与所需的复杂度和细节相关</li>
                </ul>
                <div class="loading-tips-actions">
                  <button @click="showLoadingTips = false" class="dismiss-tips-btn">
                    隐藏提示
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 视频播放器 -->
            <div v-if="videoURL" class="video-container">
              <!-- 真实视频播放器 -->
              <div v-if="!isMockVideo" class="real-video-wrapper">
                <div ref="plyrContainer" class="plyr-container"></div>
                <div v-if="videoError" class="video-error-message">
                  <i class="ri-error-warning-line"></i>
                  视频加载失败：{{videoErrorMessage}}
                  <button @click="tryAlternativePlayer" class="retry-button">
                    <i class="ri-refresh-line"></i> 尝试备用播放器
                  </button>
                </div>
              </div>
              
              <!-- 模拟视频显示 -->
              <div v-else class="mock-video-wrapper">
                <div class="mock-video-placeholder">
                  <i class="ri-film-line"></i>
                  <div class="mock-video-text">
                    <h3>模拟环境</h3>
                    <p>当前为开发测试环境，系统返回了模拟视频URL：</p>
                    <div class="mock-url">{{ videoURL }}</div>
                    <p>实际部署环境中将显示真实生成的视频。</p>
                  </div>
                </div>
                <div class="mock-actions">
                  <button @click="playDemoVideo" class="mock-action-button">
                    <i class="ri-play-circle-line"></i>
                    播放示例视频
                  </button>
                </div>
              </div>
              
              <div class="video-debug" v-if="showDebugInfo">
                <div class="debug-item">视频URL: {{videoURL}}</div>
                <div class="debug-item">状态: {{videoStatus}}</div>
                <div class="debug-item">环境: {{isMockVideo ? '模拟环境' : '实际环境'}}</div>
              </div>
              
              <div class="video-actions">
                <button @click="showPromptInfo = true" class="action-button prompt-button">
                  <i class="ri-lightbulb-line"></i>
                  查看提示词
                </button>

                <a :href="videoURL" download class="action-button">
                  <i class="ri-download-line"></i>
                  下载视频
                </a>
              </div>
            </div>
            
            <!-- 添加备用播放器容器 -->
            <div v-if="useAlternativePlayer && videoURL" class="video-container">
              <iframe 
                v-if="useAlternativePlayer" 
                :src="'https://ez-video-player.vercel.app/player?url=' + encodeURIComponent(videoURL)"
                class="video-element alt-player"
                allowfullscreen
              ></iframe>
              <div class="video-actions">
                <button @click="useAlternativePlayer = false" class="action-button">
                  <i class="ri-arrow-go-back-line"></i>
                  返回原始播放器
                </button>
              </div>
            </div>
            
            <!-- 空状态显示 -->
            <div class="empty-result" v-else-if="!isLoading && !videoURL">
              <div class="empty-content">
                <i class="ri-movie-2-line" style="font-size: 64px; color: #e9ecef;"></i>
                <div class="empty-message">{{ placeholderText }}</div>
              </div>
            </div>
          </div>

          <!-- 隐藏任务信息区域 -->
          <!--
          <div class="task-info" v-if="taskId">
            <div class="task-info-header">
              <h4>任务信息</h4>
              <button 
                @click="checkTaskStatus" 
                class="refresh-btn"
              >
                <i class="ri-refresh-line"></i>
                刷新状态
              </button>
            </div>
            <div class="task-info-content">
              <div class="info-item">
                <span class="info-label">任务ID：</span>
                <span class="info-value">{{ taskId }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">状态：</span>
                <span class="info-value" :class="{'text-error': taskStatus === 'error'}">{{ taskStatusText }}</span>
              </div>
              <div class="info-item" v-if="apiCallCount > 0">
                <span class="info-label">API调用：</span>
                <span class="info-value">{{ apiCallCount }}次</span>
              </div>
              <div class="info-item" v-if="lastApiResponse">
                <span class="info-label">最近响应：</span>
                <span class="info-value api-response" @click="toggleResponseDetails">
                  {{ lastApiResponse.substring(0, 40) }}{{ lastApiResponse.length > 40 ? '...' : '' }}
                  <i class="ri-arrow-down-s-line" v-if="!showResponseDetails"></i>
                  <i class="ri-arrow-up-s-line" v-if="showResponseDetails"></i>
                </span>
                <div class="api-response-details" v-if="showResponseDetails">
                  <pre>{{ lastApiResponse }}</pre>
                </div>
              </div>
              <div class="debug-buttons" v-if="taskId">
                <button class="debug-btn" @click="showTaskDebugInfo = !showTaskDebugInfo">
                  <i class="ri-bug-line"></i>
                  {{ showTaskDebugInfo ? '隐藏调试信息' : '显示调试信息' }}
                </button>
                <button class="debug-btn" @click="testDirectFetch">
                  <i class="ri-server-line"></i>
                  直接测试API
                </button>
              </div>
              <div class="task-debug-info" v-if="showTaskDebugInfo">
                <div class="debug-section">
                  <h5>请求参数:</h5>
                  <pre>{{ JSON.stringify(lastRequestData, null, 2) }}</pre>
                </div>
                <div class="debug-section">
                  <h5>API日志:</h5>
                  <div class="api-log-item" v-for="(log, index) in apiLogs" :key="index">
                    <div class="log-time">{{ log.time }}</div>
                    <div class="log-message" :class="{'log-error': log.isError}">{{ log.message }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          -->
        </div>
      </div>
    </div>

    <!-- 创作小贴士模态框 -->
    <div class="modal" v-if="showTipsModal">
      <div class="modal-content tips-modal">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line icon-red"></i> 创作小贴士</h3>
          <button class="close-btn" @click="showTipsModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <h4>如何写好视频提示词？</h4>
          <ul class="tips-list">
            <li>描述要具体，包含场景、物体、动作、光线等信息</li>
            <li>可以描述镜头的运动方式，如特写、远景、平移等</li>
            <li>视频生成比图像更复杂，提供更多细节会有更好的效果</li>
            <li>可以使用参考案例中的提示词作为参考，调整后生成您的创意</li>
          </ul>
          <h4>参考示例：</h4>
          <div class="example-list">
            <div class="example-item">
              <strong>场景描述：</strong>
              <p>一只橙色的小猫在阳光明媚的后院花园中嬉戏。它轻盈地在彩色花朵间跳跃，偶尔停下来好奇地观察飞舞的蝴蝶。阳光透过树叶洒在猫咪的毛发上，形成斑驳的光影。</p>
            </div>
            <div class="example-item">
              <strong>镜头描述：</strong>
              <p>镜头从远处慢慢推进，展现整个花园的美丽，然后聚焦在猫咪身上，最后特写猫咪好奇的眼神和微微摆动的尾巴。</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 提示词信息模态框 -->
    <div class="modal" v-if="showPromptInfo">
      <div class="modal-content tips-modal">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line icon-red"></i> 视频提示词</h3>
          <button class="close-btn" @click="showPromptInfo = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <h4>本视频使用的提示词</h4>
          <div class="prompt-display">
            <p>{{ formData.prompt }}</p>
          </div>
          
          <h4>视频参数</h4>
          <div class="video-params">
            <div class="param-item">
              <span class="param-label"><i class="ri-aspect-ratio-line"></i> 视频比例:</span>
              <span class="param-value">{{ formData.ratio }}</span>
            </div>
            <div class="param-item">
              <span class="param-label"><i class="ri-time-line"></i> 视频时长:</span>
              <span class="param-value">{{ formData.duration }}秒</span>
            </div>
            <div class="param-item">
              <span class="param-label"><i class="ri-film-line"></i> 帧率:</span>
              <span class="param-value">{{ formData.fps }}帧/秒</span>
            </div>
            <div class="param-item">
              <span class="param-label"><i class="ri-hd-line"></i> 分辨率:</span>
              <span class="param-value">{{ formData.resolution }}</span>
            </div>
          </div>
          
          <div class="prompt-actions">
            <button class="copy-button" @click="copyPromptToClipboard">
              <i class="ri-clipboard-line"></i> 复制提示词
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 历史记录模态框 -->
    <div v-if="showHistoryModal" class="history-modal">
      <div class="history-modal-content">
        <div class="history-modal-header">
          <h3>生成历史记录</h3>
          <button @click="showHistoryModal = false" class="close-btn">&times;</button>
        </div>
        <div class="history-modal-body">
          <div v-if="videoHistory.length === 0" class="no-history">
            暂无历史记录
          </div>
          <div v-for="(item, index) in videoHistory" :key="index" class="history-item">
            <div class="history-item-header">
              <div class="history-title">{{ item.title }}</div>
              <div class="history-time">{{ item.time }}</div>
              <div :class="['history-status', getStatusClass(item.status)]">
                {{ getStatusText(item.status) }}
              </div>
            </div>
            <div class="history-item-body">
              <div class="history-prompt">{{ item.prompt }}</div>
              <div class="history-details">
                <span>比例: {{ item.ratio }}</span>
                <span>时长: {{ item.duration }}秒</span>
                <span>分辨率: {{ item.resolution }}</span>
              </div>
            </div>
            <div class="history-item-footer">
              <!-- 根据状态显示不同按钮 -->
              <template v-if="item.status === 'success'">
                <div class="history-item-actions">
                  <button @click="playHistoryVideo(item)" class="action-btn play-btn">
                    <i class="fa fa-play"></i> 播放
                  </button>
                  <button @click="copyVideoUrl(item.videoURL)" class="action-btn copy-btn" style="background-color: #67C23A; color: white; padding: 4px 12px; margin-left: 10px; border-radius: 4px; border: none; font-weight: bold;">
                    <i class="fa fa-copy"></i> 复制地址
                  </button>
                  <div class="video-url" :title="item.videoURL">{{ formatVideoUrl(item.videoURL) }}</div>
                </div>
              </template>
              <template v-else-if="item.status === 'queued' || item.status === 'processing'">
                <button @click="checkHistoryTaskStatus(item)" class="action-btn refresh-btn">
                  <i class="fa fa-refresh"></i> 刷新
                </button>
              </template>
              <template v-else-if="item.status === 'failed'">
                <button class="action-btn error-btn" disabled>
                  <i class="fa fa-exclamation-triangle"></i> 失败
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { mapState } from 'vuex';
import Plyr from 'plyr';

export default {
  name: 'TextToVideo',
  data() {
    return {
      formData: {
        prompt: '',
        ratio: '16:9',
        duration: 3.0,
        fps: 30,
        resolution: '720p',
        watermark: false
      },
      isLoading: false,
      showAdvancedOptions: false,  // 添加此变量
      taskId: null,
      taskStatus: 'idle',
      taskProgress: 0,
      videoURL: null,
      videoError: false,
      videoErrorMessage: '',
      videoStatus: '',
      lastApiResponse: '',
      apiLogs: [],
      isMockVideo: false,
      showDebugInfo: false,
      useAlternativePlayer: false,
      showResponseDetails: false,
      showLoadingTips: true,
      apiCallCount: 0,
      ratioOptions: [],
      resolutionOptions: [],
      lastRequestData: null,
      player: null, // Plyr播放器实例
      // 添加参考案例数据
      referenceExamples: [
        {
          title: '海滩日落',
          description: '金色的阳光洒在海面上，形成闪烁的波光。海浪轻柔地拍打着沙滩，远处棕榈树剪影在微风中摇曳。天空从蓝色逐渐过渡到橙红色和紫色，呈现出壮观的日落景象。',
          ratio: '16:9',
          duration: '10',
          fps: '30',
          resolution: '1080p',
          watermark: false,
          prompt: '金色的阳光洒在海面上，形成闪烁的波光。海浪轻柔地拍打着沙滩，远处棕榈树剪影在微风中摇曳。天空从蓝色逐渐过渡到橙红色和紫色，呈现出壮观的日落景象。'
        },
        {
          title: '城市雨夜',
          description: '繁忙的城市街道在雨夜中格外迷人。雨滴落在路面上形成小水洼，反射着霓虹灯和车灯的光芒。行人撑着伞匆匆走过，车辆驶过时溅起水花。街边的店铺灯光透过雨雾显得朦胧而温暖。',
          ratio: '16:9',
          duration: '5',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '繁忙的城市街道在雨夜中格外迷人。雨滴落在路面上形成小水洼，反射着霓虹灯和车灯的光芒。行人撑着伞匆匆走过，车辆驶过时溅起水花。街边的店铺灯光透过雨雾显得朦胧而温暖。'
        },
        {
          title: '森林小溪',
          description: '阳光透过茂密的树叶，在森林地面形成斑驳的光影。清澈的小溪缓缓流过苔藓覆盖的石头，发出宁静的水声。偶尔有落叶顺流而下，小鸟在枝头欢快地歌唱，整个画面充满生机与宁静。',
          ratio: '16:9',
          duration: '5',
          fps: '24',
          resolution: '720p',
          watermark: false,
          prompt: '阳光透过茂密的树叶，在森林地面形成斑驳的光影。清澈的小溪缓缓流过苔藓覆盖的石头，发出宁静的水声。偶尔有落叶顺流而下，小鸟在枝头欢快地歌唱，整个画面充满生机与宁静。'
        },
        {
          title: '猫咪玩耍',
          description: '一只活泼的橘猫在阳光明媚的客厅里追逐着一个红色的毛线球。它敏捷地跳跃、翻滚，时而停下来用爪子拨弄毛线球，尾巴兴奋地摇摆。阳光通过窗户洒进来，照亮了猫咪蓬松的毛发和闪烁的眼睛。',
          ratio: '1:1',
          duration: '3',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '一只活泼的橘猫在阳光明媚的客厅里追逐着一个红色的毛线球。它敏捷地跳跃、翻滚，时而停下来用爪子拨弄毛线球，尾巴兴奋地摇摆。阳光通过窗户洒进来，照亮了猫咪蓬松的毛发和闪烁的眼睛。'
        },
        {
          title: '飘雪的小镇',
          description: '雪花轻轻飘落在欧式小镇的石板路和红砖房屋上。远处教堂的尖顶在雪中若隐若现，街灯散发着温暖的光芒。偶尔有戴着围巾的行人经过，留下一串脚印，很快又被新雪覆盖。整个小镇沉浸在宁静祥和的冬日氛围中。',
          ratio: '16:9',
          duration: '5',
          fps: '24',
          resolution: '1080p',
          watermark: false,
          prompt: '雪花轻轻飘落在欧式小镇的石板路和红砖房屋上。远处教堂的尖顶在雪中若隐若现，街灯散发着温暖的光芒。偶尔有戴着围巾的行人经过，留下一串脚印，很快又被新雪覆盖。整个小镇沉浸在宁静祥和的冬日氛围中。'
        },
        {
          title: '舞动的花朵',
          description: '一朵鲜艳的红色玫瑰在微风中轻轻摇曳，花瓣上的露珠在阳光下闪烁。背景是柔和模糊的绿色花园，偶尔有蝴蝶飞过。镜头慢慢推进，展现花朵精致的纹理和层次，色彩鲜明而富有生命力。',
          ratio: '9:16',
          duration: '3',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '一朵鲜艳的红色玫瑰在微风中轻轻摇曳，花瓣上的露珠在阳光下闪烁。背景是柔和模糊的绿色花园，偶尔有蝴蝶飞过。镜头慢慢推进，展现花朵精致的纹理和层次，色彩鲜明而富有生命力。'
        },
        {
          title: '未来城市',
          description: '未来城市的天际线充满了各种形状的高科技建筑，表面覆盖着发光的线条和全息投影。飞行汽车在建筑之间穿梭，地面上有磁悬浮列车高速行驶。城市被蓝色和紫色的霓虹灯光照亮，天空中有多个月亮或行星，呈现出科幻的未来感。',
          ratio: '16:9',
          duration: '5',
          fps: '30',
          resolution: '1080p',
          watermark: false,
          prompt: '未来城市的天际线充满了各种形状的高科技建筑，表面覆盖着发光的线条和全息投影。飞行汽车在建筑之间穿梭，地面上有磁悬浮列车高速行驶。城市被蓝色和紫色的霓虹灯光照亮，天空中有多个月亮或行星，呈现出科幻的未来感。'
        },
        {
          title: '星空下的草原',
          description: '广阔的草原上，高高的草随风轻轻摇曳。头顶是璀璨的星空，银河清晰可见，无数星星点缀其中。远处有几棵孤独的树木剪影，草原上偶尔有萤火虫闪烁。整个画面充满了宁静与壮观的对比。',
          ratio: '16:9',
          duration: '10',
          fps: '24',
          resolution: '1080p',
          watermark: false,
          prompt: '广阔的草原上，高高的草随风轻轻摇曳。头顶是璀璨的星空，银河清晰可见，无数星星点缀其中。远处有几棵孤独的树木剪影，草原上偶尔有萤火虫闪烁。整个画面充满了宁静与壮观的对比。'
        },
        {
          title: '潜水探索',
          description: '蓝色的海水中，阳光从水面透下来形成光柱。多彩的珊瑚礁栖息着各种鱼类，它们在珊瑚间穿梭。镜头跟随一条闪闪发光的热带鱼游动，展现海底世界的丰富多彩和神秘宁静。水中漂浮着细小的粒子，为画面增添了梦幻感。',
          ratio: '16:9',
          duration: '5',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '蓝色的海水中，阳光从水面透下来形成光柱。多彩的珊瑚礁栖息着各种鱼类，它们在珊瑚间穿梭。镜头跟随一条闪闪发光的热带鱼游动，展现海底世界的丰富多彩和神秘宁静。水中漂浮着细小的粒子，为画面增添了梦幻感。'
        },
        {
          title: '古老图书馆',
          description: '阳光透过高大的彩色玻璃窗照进古老图书馆，照亮漂浮在空气中的尘埃。木质书架上摆满了古旧的书籍，有些书架高达天花板。画面缓慢移动展示图书馆的宏伟建筑，包括精美的木雕装饰、古老的地球仪和老式阅读灯。空间散发出历史与知识的厚重感。',
          ratio: '16:9',
          duration: '5',
          fps: '24',
          resolution: '1080p',
          watermark: false,
          prompt: '阳光透过高大的彩色玻璃窗照进古老图书馆，照亮漂浮在空气中的尘埃。木质书架上摆满了古旧的书籍，有些书架高达天花板。画面缓慢移动展示图书馆的宏伟建筑，包括精美的木雕装饰、古老的地球仪和老式阅读灯。空间散发出历史与知识的厚重感。'
        }
      ],
      checkInterval: null,
      placeholderText: '在左侧填写提示词并点击生成视频，生成完成后将在此处显示',
      showTipsModal: false,
      showPromptInfo: false,
      loadingMessage: '正在创建任务...',
      loadingTips: [
        '高质量的提示词能够有效提升生成结果',
        '视频生成时间与复杂度和细节相关',
        '可以查看参考案例获取灵感',
        '上传参考图片可以引导AI更好地理解你的创意',
      ],
      currentTipIndex: 0,
      tipInterval: null,
      videoHistory: [], // 历史视频记录
      showHistoryModal: false, // 控制历史记录模态框显示
      retryCount: 0, // 确保重试计数器重置
      // 添加参考案例数据
      referenceExamples: [
        {
          title: '海滩日落',
          description: '金色的阳光洒在海面上，形成闪烁的波光。海浪轻柔地拍打着沙滩，远处棕榈树剪影在微风中摇曳。天空从蓝色逐渐过渡到橙红色和紫色，呈现出壮观的日落景象。',
          ratio: '16:9',
          duration: '10',
          fps: '30',
          resolution: '1080p',
          watermark: false,
          prompt: '金色的阳光洒在海面上，形成闪烁的波光。海浪轻柔地拍打着沙滩，远处棕榈树剪影在微风中摇曳。天空从蓝色逐渐过渡到橙红色和紫色，呈现出壮观的日落景象。'
        },
        {
          title: '城市雨夜',
          description: '繁忙的城市街道在雨夜中格外迷人。雨滴落在路面上形成小水洼，反射着霓虹灯和车灯的光芒。行人撑着伞匆匆走过，车辆驶过时溅起水花。街边的店铺灯光透过雨雾显得朦胧而温暖。',
          ratio: '16:9',
          duration: '5',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '繁忙的城市街道在雨夜中格外迷人。雨滴落在路面上形成小水洼，反射着霓虹灯和车灯的光芒。行人撑着伞匆匆走过，车辆驶过时溅起水花。街边的店铺灯光透过雨雾显得朦胧而温暖。'
        },
        {
          title: '森林小溪',
          description: '阳光透过茂密的树叶，在森林地面形成斑驳的光影。清澈的小溪缓缓流过苔藓覆盖的石头，发出宁静的水声。偶尔有落叶顺流而下，小鸟在枝头欢快地歌唱，整个画面充满生机与宁静。',
          ratio: '16:9',
          duration: '5',
          fps: '24',
          resolution: '720p',
          watermark: false,
          prompt: '阳光透过茂密的树叶，在森林地面形成斑驳的光影。清澈的小溪缓缓流过苔藓覆盖的石头，发出宁静的水声。偶尔有落叶顺流而下，小鸟在枝头欢快地歌唱，整个画面充满生机与宁静。'
        },
        {
          title: '猫咪玩耍',
          description: '一只活泼的橘猫在阳光明媚的客厅里追逐着一个红色的毛线球。它敏捷地跳跃、翻滚，时而停下来用爪子拨弄毛线球，尾巴兴奋地摇摆。阳光通过窗户洒进来，照亮了猫咪蓬松的毛发和闪烁的眼睛。',
          ratio: '1:1',
          duration: '3',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '一只活泼的橘猫在阳光明媚的客厅里追逐着一个红色的毛线球。它敏捷地跳跃、翻滚，时而停下来用爪子拨弄毛线球，尾巴兴奋地摇摆。阳光通过窗户洒进来，照亮了猫咪蓬松的毛发和闪烁的眼睛。'
        },
        {
          title: '飘雪的小镇',
          description: '雪花轻轻飘落在欧式小镇的石板路和红砖房屋上。远处教堂的尖顶在雪中若隐若现，街灯散发着温暖的光芒。偶尔有戴着围巾的行人经过，留下一串脚印，很快又被新雪覆盖。整个小镇沉浸在宁静祥和的冬日氛围中。',
          ratio: '16:9',
          duration: '5',
          fps: '24',
          resolution: '1080p',
          watermark: false,
          prompt: '雪花轻轻飘落在欧式小镇的石板路和红砖房屋上。远处教堂的尖顶在雪中若隐若现，街灯散发着温暖的光芒。偶尔有戴着围巾的行人经过，留下一串脚印，很快又被新雪覆盖。整个小镇沉浸在宁静祥和的冬日氛围中。'
        },
        {
          title: '舞动的花朵',
          description: '一朵鲜艳的红色玫瑰在微风中轻轻摇曳，花瓣上的露珠在阳光下闪烁。背景是柔和模糊的绿色花园，偶尔有蝴蝶飞过。镜头慢慢推进，展现花朵精致的纹理和层次，色彩鲜明而富有生命力。',
          ratio: '9:16',
          duration: '3',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '一朵鲜艳的红色玫瑰在微风中轻轻摇曳，花瓣上的露珠在阳光下闪烁。背景是柔和模糊的绿色花园，偶尔有蝴蝶飞过。镜头慢慢推进，展现花朵精致的纹理和层次，色彩鲜明而富有生命力。'
        },
        {
          title: '未来城市',
          description: '未来城市的天际线充满了各种形状的高科技建筑，表面覆盖着发光的线条和全息投影。飞行汽车在建筑之间穿梭，地面上有磁悬浮列车高速行驶。城市被蓝色和紫色的霓虹灯光照亮，天空中有多个月亮或行星，呈现出科幻的未来感。',
          ratio: '16:9',
          duration: '5',
          fps: '30',
          resolution: '1080p',
          watermark: false,
          prompt: '未来城市的天际线充满了各种形状的高科技建筑，表面覆盖着发光的线条和全息投影。飞行汽车在建筑之间穿梭，地面上有磁悬浮列车高速行驶。城市被蓝色和紫色的霓虹灯光照亮，天空中有多个月亮或行星，呈现出科幻的未来感。'
        },
        {
          title: '星空下的草原',
          description: '广阔的草原上，高高的草随风轻轻摇曳。头顶是璀璨的星空，银河清晰可见，无数星星点缀其中。远处有几棵孤独的树木剪影，草原上偶尔有萤火虫闪烁。整个画面充满了宁静与壮观的对比。',
          ratio: '16:9',
          duration: '10',
          fps: '24',
          resolution: '1080p',
          watermark: false,
          prompt: '广阔的草原上，高高的草随风轻轻摇曳。头顶是璀璨的星空，银河清晰可见，无数星星点缀其中。远处有几棵孤独的树木剪影，草原上偶尔有萤火虫闪烁。整个画面充满了宁静与壮观的对比。'
        },
        {
          title: '潜水探索',
          description: '蓝色的海水中，阳光从水面透下来形成光柱。多彩的珊瑚礁栖息着各种鱼类，它们在珊瑚间穿梭。镜头跟随一条闪闪发光的热带鱼游动，展现海底世界的丰富多彩和神秘宁静。水中漂浮着细小的粒子，为画面增添了梦幻感。',
          ratio: '16:9',
          duration: '5',
          fps: '30',
          resolution: '720p',
          watermark: false,
          prompt: '蓝色的海水中，阳光从水面透下来形成光柱。多彩的珊瑚礁栖息着各种鱼类，它们在珊瑚间穿梭。镜头跟随一条闪闪发光的热带鱼游动，展现海底世界的丰富多彩和神秘宁静。水中漂浮着细小的粒子，为画面增添了梦幻感。'
        },
        {
          title: '古老图书馆',
          description: '阳光透过高大的彩色玻璃窗照进古老图书馆，照亮漂浮在空气中的尘埃。木质书架上摆满了古旧的书籍，有些书架高达天花板。画面缓慢移动展示图书馆的宏伟建筑，包括精美的木雕装饰、古老的地球仪和老式阅读灯。空间散发出历史与知识的厚重感。',
          ratio: '16:9',
          duration: '5',
          fps: '24',
          resolution: '1080p',
          watermark: false,
          prompt: '阳光透过高大的彩色玻璃窗照进古老图书馆，照亮漂浮在空气中的尘埃。木质书架上摆满了古旧的书籍，有些书架高达天花板。画面缓慢移动展示图书馆的宏伟建筑，包括精美的木雕装饰、古老的地球仪和老式阅读灯。空间散发出历史与知识的厚重感。'
        }
      ],
      videoError: false,
      videoErrorMessage: '',
      videoStatus: '未加载',
      showDebugInfo: false,
      useAlternativePlayer: false,
      apiCallCount: 0,
      lastApiResponse: '',
      showResponseDetails: false,
      showTaskDebugInfo: false,
      lastRequestData: null,
      apiLogs: [],
      demoVideoUrl: 'https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4',
      isMockVideo: false,
    };
  },
  computed: {
    statusClass() {
      switch(this.taskStatus) {
        case 'queued': return 'status-queued';
        case 'running': 
        case 'processing': return 'status-running';
        case 'success': return 'status-success';
        case 'error':
        case 'failed': return 'status-error';
        default: return 'status-waiting';
      }
    },
    statusText() {
      switch(this.taskStatus) {
        case 'queued': return '排队中';
        case 'running':
        case 'processing': return '生成中';
        case 'success': return '生成成功';
        case 'error':
        case 'failed': return '生成失败';
        default: return '等待创建';
      }
    },
    taskStatusText() {
      if (!this.taskId) return '请填写文本提示词开始创建视频';
      
      switch(this.taskStatus) {
        case 'queued':
          return `任务排队中，请稍候...`;
        case 'running':
          return `正在生成视频...`;
        case 'success':
          return '视频生成成功，可以播放或下载';
        case 'error':
          return '视频生成失败，请重试';
        default:
          return '正在初始化任务...';
      }
    }
  },
  methods: {
    // 根据状态获取样式类名
    getStatusClass(status) {
      switch (status) {
        case 'success':
          return 'status-success';
        case 'failed':
        case 'error':
          return 'status-error';
        case 'processing':
          return 'status-processing';
        case 'queued':
          return 'status-queued';
        default:
          return 'status-unknown';
      }
    },
    
    // 根据状态获取显示文本
    getStatusText(status) {
      switch (status) {
        case 'success':
          return '生成成功';
        case 'failed':
        case 'error':
          return '生成失败';
        case 'processing':
          return '生成中';
        case 'queued':
          return '排队中';
        default:
          return status || '未知';
      }
    },
    
    toggleAdvancedOptions() {
      this.showAdvancedOptions = !this.showAdvancedOptions;
    },
    
    resetForm() {
      this.formData = {
        prompt: '',
        ratio: '16:9',
        duration: 3.0,
        fps: 30,
        resolution: '720p',
        watermark: false
      };
      this.showAdvancedOptions = false;
    },
    
    showTips() {
      this.showTipsModal = true;
    },
    
    async generateVideo() {
      if (!this.formData.prompt.trim()) {
        alert('请输入视频提示词');
        return;
      }
      
      this.isLoading = true;
      this.taskId = null;
      this.taskStatus = 'idle';
      this.taskProgress = 0;
      this.videoURL = null;
      this.videoError = false;
      this.showLoadingTips = true;
      this.loadingMessage = '正在创建视频任务，请稍候...';
      this.startLoadingTips();
      this.apiLogs = [];
      
      try {
        // 准备请求数据
        const requestData = {
          prompt: this.formData.prompt,
          ratio: this.formData.ratio,
          duration: parseFloat(this.formData.duration),
          fps: parseInt(this.formData.fps),
          resolution: this.formData.resolution,
          watermark: this.formData.watermark
        };
        
        this.lastRequestData = requestData;
        this.addApiLog(`开始创建视频任务: 提示词长度=${this.formData.prompt.length}, 比例=${this.formData.ratio}`);
        
        // 尝试最多重试2次
        let retries = 2;
        let response;
        
        while (retries >= 0) {
          try {
            console.log('发送创建任务请求:', requestData);
            response = await axios.post('/api/v1/text-to-videos/create', requestData, {
              timeout: 30000, // 30秒超时
              headers: this.getRequestHeaders()
            });
            break; // 成功则跳出循环
          } catch (error) {
            retries--;
            this.addApiLog(`API请求失败: ${error.message}，重试中...`, true);
            if (retries < 0) throw error;
            await new Promise(resolve => setTimeout(resolve, 2000)); // 等待2秒后重试
          }
        }
        
        this.lastApiResponse = JSON.stringify(response.data, null, 2);
        console.log('创建任务响应:', response.data); // 添加控制台日志，方便排查问题
        
        // 检查API返回格式，适配不同的返回结构
        // 1. 官方API格式 {id: "task-xxx", ...}
        if (response.data.id) {
          this.taskId = response.data.id;
          this.taskStatus = 'queued';
          this.loadingMessage = '任务已创建，正在处理...';
          this.addApiLog(`任务创建成功，ID: ${this.taskId}`);
          console.log('成功创建任务，ID:', this.taskId);
          
          // 立即添加到历史记录，状态为queued
          this.saveToHistory('queued');
          
          // 开始定期检查任务状态
          this.startPolling();
        }
        // 2. 旧格式 {code: 0, task_id: 'xxx', msg: 'xxx'}
        else if (response.data.code === 0) {
          this.taskId = response.data.task_id;
          this.taskStatus = 'queued';
          this.loadingMessage = '任务已创建，正在处理...';
          this.addApiLog(`任务创建成功，ID: ${this.taskId}`);
          console.log('成功创建任务，ID:', this.taskId);
          
          // 立即添加到历史记录，状态为queued
          this.saveToHistory('queued');
          
          // 开始定期检查任务状态
          this.startPolling();
        }
        // 3. 其他格式 {status: 'success', data: {task_id: 'xxx'}}
        else if (response.data.status === 'success') {
          this.taskId = response.data.data.task_id;
          this.taskStatus = 'queued';
          this.loadingMessage = '任务已创建，正在处理...';
          this.addApiLog(`任务创建成功，ID: ${this.taskId}`);
          console.log('成功创建任务，ID:', this.taskId);
          
          // 立即添加到历史记录，状态为queued
          this.saveToHistory('queued');
          
          // 开始定期检查任务状态
          this.startPolling();
        } else {
          this.isLoading = false;
          this.placeholderText = '创建任务失败，请重试';
          
          let errorMessage = '未知错误';
          if (response.data.error && response.data.error.message) {
            errorMessage = response.data.error.message;
          } else if (response.data.message) {
            errorMessage = response.data.message;
          } else if (response.data.msg) {
            errorMessage = response.data.msg;
          }
          
          this.addApiLog(`任务创建失败: ${errorMessage}`, true);
          alert('创建视频任务失败: ' + errorMessage);
          this.stopLoadingTips();
        }
      } catch (error) {
        this.isLoading = false;
        this.placeholderText = `创建任务出错: ${error.message || '未知错误'}`;
        this.addApiLog(`任务创建异常: ${error.message}`, true);
        alert(`创建视频任务异常: ${error.message}`);
        this.stopLoadingTips();
      }
    },
    
    startPolling() {
      // 如果已经有轮询定时器，先清除
      if (this.checkInterval) {
        clearInterval(this.checkInterval);
        this.checkInterval = null;
      }
      
      console.log('======== 启动任务状态轮询 ========');
      console.log('任务ID:', this.taskId);
      
      // 立即检查一次状态
      this.checkTaskStatus();
      
      // 设置定时器，每3秒检查一次任务状态
      this.checkInterval = setInterval(this.checkTaskStatus, 3000);
    },
    
    stopPolling() {
      if (this.checkInterval) {
        console.log('======== 停止任务状态轮询 ========');
        clearInterval(this.checkInterval);
        this.checkInterval = null;
      }
    },
    
    // 启动加载提示轮换
    startLoadingTips() {
      this.currentTipIndex = 0;
      
      // 如果已有定时器先清除
      if (this.tipInterval) {
        clearInterval(this.tipInterval);
      }
      
      // 设置定时器，每5秒轮换一次提示
      this.tipInterval = setInterval(() => {
        this.rotateTips();
      }, 5000);
    },
    
    // 轮换提示信息
    rotateTips() {
      this.currentTipIndex = (this.currentTipIndex + 1) % this.loadingTips.length;
      // 更新加载信息，移除进度百分比显示
      if (this.taskStatus === 'queued') {
        this.loadingMessage = `排队中... ${this.loadingTips[this.currentTipIndex]}`;
      } else if (this.taskStatus === 'running' || this.taskStatus === 'processing') {
        this.loadingMessage = `生成中... ${this.loadingTips[this.currentTipIndex]}`;
      }
    },
    
    // 停止加载提示轮换
    stopLoadingTips() {
      if (this.tipInterval) {
        clearInterval(this.tipInterval);
        this.tipInterval = null;
      }
    },
    
    // 获取统一的请求头
    getRequestHeaders() {
      return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      };
    },
    
    // 检查任务状态
    async checkTaskStatus(returnResponseOnly = false) {
      if (!this.taskId) {
        if (returnResponseOnly) return null;
        return;
      }
      
      this.addApiLog(`开始查询任务状态，ID: ${this.taskId}`);
      
      try {
        // 尝试最多重试2次
        let retries = 2;
        let response;
        
        while (retries >= 0) {
          try {
            console.log(`查询任务ID ${this.taskId} 的状态`);
            response = await axios.get(`/api/v1/text-to-videos/query?task_id=${this.taskId}`, {
              timeout: 10000, // 10秒超时
              headers: this.getRequestHeaders()
            });
            break; // 成功则跳出循环
          } catch (error) {
            retries--;
            this.addApiLog(`API查询状态失败: ${error.message}，重试中...`, true);
            if (retries < 0) throw error;
            await new Promise(resolve => setTimeout(resolve, 2000)); // 等待2秒后重试
          }
        }
        
        console.log('查询状态响应:', response.data); // 添加控制台日志，方便排查问题
        this.lastApiResponse = JSON.stringify(response.data, null, 2);
        
        // 检查API返回格式，适配不同的返回结构
        let taskStatus, taskProgress, videoUrl;
        
        // 后端自定义格式 {code: 0, task_id: '...', status: 'success', progress: 100, video_url: '...'}
        if (response.data.code === 0 && response.data.hasOwnProperty('status')) {
          // 后端实际使用的格式
          taskStatus = response.data.status;
          taskProgress = response.data.progress || 0;
          videoUrl = response.data.video_url;
          this.addApiLog(`任务状态: ${taskStatus}, 进度: ${taskProgress}%, 视频URL: ${videoUrl || '暂无'}`);
        }
        // 适配官方API返回格式 {id, model, status, content: {video_url}, ...}
        else if (response.data.id && response.data.status) {
          // 官方API格式
          // 状态映射：succeeded -> success, processing -> processing, failed -> failed
          const apiStatus = response.data.status;
          
          switch(apiStatus) {
            case 'succeeded':
              taskStatus = 'success';
              taskProgress = 100;
              break;
            case 'processing':
            case 'in_progress':
              taskStatus = 'processing';
              taskProgress = 50; // API没有提供具体进度，使用中间值
              break;
            case 'failed':
              taskStatus = 'failed';
              taskProgress = 0;
              break;
            case 'created':
            case 'pending':
              taskStatus = 'queued';
              taskProgress = 0;
              break;
            default:
              taskStatus = apiStatus;
              taskProgress = 0;
          }
          
          // 视频URL在content.video_url中
          if (response.data.content && response.data.content.video_url) {
            videoUrl = response.data.content.video_url;
          }
          
          this.addApiLog(`任务状态: ${taskStatus} (原始: ${apiStatus}), 视频URL: ${videoUrl || '暂无'}`);
        } else if (response.data.status === 'success' && response.data.data) {
          // 其他格式: {status: 'success', data: {status: 'xxx', progress: xx, video_url: 'xxx'}}
          const taskData = response.data.data;
          taskStatus = taskData.status;
          taskProgress = taskData.progress || 0;
          videoUrl = taskData.video_url;
          this.addApiLog(`任务状态: ${taskStatus}, 进度: ${taskProgress}%`);
        } else {
          this.addApiLog(`查询状态失败: 未知的API返回格式 ${JSON.stringify(response.data).slice(0, 100)}...`, true);
          if (returnResponseOnly) return null;
          
          this.isLoading = false;
          this.stopPolling();
          this.stopLoadingTips();
          alert('查询任务状态失败: 未知的API返回格式');
          return;
        }
        
        if (returnResponseOnly) {
          return {
            status: taskStatus,
            progress: taskProgress,
            videoURL: videoUrl
          };
        }
        
        // 更新任务状态和进度
        this.taskStatus = taskStatus;
        this.taskProgress = taskProgress;
        
        // 更新加载提示
        if (taskStatus === 'processing') {
          this.loadingMessage = `视频生成中，已完成 ${taskProgress}%...`;
        } else if (taskStatus === 'success') {
          this.loadingMessage = '视频生成成功，正在加载...';
        } else if (taskStatus === 'failed') {
          this.loadingMessage = '视频生成失败，请重试';
        } else {
          this.loadingMessage = `任务状态: ${taskStatus}`;
        }
        
        // 更新历史记录
        if (this.taskId) {
          const existingIndex = this.videoHistory.findIndex(item => item.taskId === this.taskId);
          if (existingIndex !== -1) {
            // 更新状态
            this.videoHistory[existingIndex].status = taskStatus;
            
            // 如果成功，更新视频URL
            if (taskStatus === 'success' && videoUrl) {
              this.videoHistory[existingIndex].videoURL = videoUrl;
            }
            
            // 保存到localStorage
            try {
              localStorage.setItem('videoHistory', JSON.stringify(this.videoHistory));
            } catch (e) {
              console.error('保存历史记录到localStorage失败:', e);
            }
          }
        }
        
        // 如果任务成功且有视频URL
        if (taskStatus === 'success' && videoUrl) {
          // 使用processVideoUrl方法处理视频URL
          const processedUrl = this.processVideoUrl(videoUrl);
          this.videoURL = processedUrl;
          
          this.addApiLog(`视频生成成功，原始URL: ${videoUrl}, 处理后URL: ${this.videoURL}`);
          
          // 测试视频URL是否可访问
          this.testVideoUrlAccessibility(this.videoURL);
          
          this.isLoading = false;
          this.stopPolling();
          this.stopLoadingTips();
          
          // 视频生成完成后保存到历史记录
          this.saveToHistory('success', this.videoURL);
        }
        // 如果任务失败
        else if (taskStatus === 'failed') {
          this.isLoading = false;
          
          let errorMessage = '未知错误';
          if (response.data.error && response.data.error.message) {
            errorMessage = response.data.error.message;
          } else if (response.data.message) {
            errorMessage = response.data.message;
          } else if (response.data.msg) {
            errorMessage = response.data.msg;
          }
          
          this.addApiLog(`任务失败: ${errorMessage}`, true);
          this.stopPolling();
          this.stopLoadingTips();
          alert('视频生成失败: ' + errorMessage);
          
          // 更新历史记录为失败状态
          this.saveToHistory('failed');
        }
        // 如果任务仍在处理中，继续轮询
        else {
          // 正在处理中，继续轮询
        }
      } catch (error) {
        this.addApiLog(`查询状态异常: ${error.message}`, true);
        if (returnResponseOnly) return null;
        
        // 发生异常，停止轮询
        this.isLoading = false;
        this.stopPolling();
        this.stopLoadingTips();
        alert(`查询任务状态异常: ${error.message}`);
      }
    },
    
    // 滚动参考案例列表
    scrollReferences(direction) {
      const container = this.$refs.referenceList;
      const scrollAmount = 300; // 每次滚动的像素数
      
      if (direction === 'left') {
        container.scrollLeft -= scrollAmount;
      } else {
        container.scrollLeft += scrollAmount;
      }
    },
    
    // 应用参考案例
    applyExample(example) {
      this.formData.prompt = example.prompt;
      this.formData.ratio = example.ratio;
      this.formData.duration = example.duration;
      this.formData.fps = example.fps;
      this.formData.resolution = example.resolution;
      this.formData.watermark = example.watermark;
      
      // 保持高级选项面板收起状态
      this.showAdvancedOptions = false;
      
      // 滚动到表单顶部
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
      
      this.addApiLog(`已应用参考案例: ${example.title}`);
    },
    
    // 视频加载出错处理
    handleVideoError(e) {
      this.videoError = true;
      this.videoStatus = '加载失败';
      
      // 获取详细错误信息
      const errorCode = e.detail ? e.detail.code : 0;
      let errorMessage = '';
      
      switch(errorCode) {
        case 1:
          errorMessage = '加载过程中被中止';
          break;
        case 2:
          errorMessage = '网络错误';
          break;
        case 3:
          errorMessage = '视频解码错误或格式不支持';
          break;
        case 4:
          errorMessage = '视频格式不支持或无法使用';
          break;
        default:
          errorMessage = '未知错误';
      }
      
      this.videoErrorMessage = errorMessage;
      console.error('视频加载错误:', errorMessage, '错误代码:', errorCode);
      
      // 显示直接下载链接
      this.showDirectDownloadLink();
    },
    
    // 视频成功加载
    handleVideoLoaded() {
      this.videoError = false;
      this.videoStatus = '生成成功';
      console.log('视频加载成功:', this.videoURL);
    },
    
    // 显示/隐藏调试信息
    toggleDebugInfo() {
      this.showDebugInfo = !this.showDebugInfo;
    },
    
    // 尝试备用播放器
    tryAlternativePlayer() {
      this.useAlternativePlayer = true;
    },
    
    // 切换显示API响应详情
    toggleResponseDetails() {
      this.showResponseDetails = !this.showResponseDetails;
    },
    
    // 添加API日志
    addApiLog(message, isError = false) {
      const now = new Date();
      const timeStr = `${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;
      this.apiLogs.unshift({
        time: timeStr,
        message,
        isError
      });
      
      // 限制日志数量
      if (this.apiLogs.length > 20) {
        this.apiLogs = this.apiLogs.slice(0, 20);
      }
      
      console.log(`[API ${isError ? 'ERROR' : 'LOG'}]: ${message}`);
    },
    
    // 直接测试API连接
    async testDirectFetch() {
      try {
        this.addApiLog('正在测试API连接...');
        
        // 测试比例API
        const ratiosResponse = await axios.get('/api/v1/text-to-videos/ratios');
        this.addApiLog(`比例API响应: ${JSON.stringify(ratiosResponse.data).substring(0, 100)}...`);
        
        // 测试分辨率API
        const resolutionsResponse = await axios.get('/api/v1/text-to-videos/resolutions');
        this.addApiLog(`分辨率API响应: ${JSON.stringify(resolutionsResponse.data).substring(0, 100)}...`);
        
        // 如果有任务ID，测试查询API
        if (this.taskId) {
          const queryResponse = await axios.get(`/api/v1/text-to-videos/query?task_id=${this.taskId}`);
          this.addApiLog(`任务查询响应: ${JSON.stringify(queryResponse.data)}`);
          
          // 更新状态
          if (queryResponse.data.status === 'success') {
            const taskData = queryResponse.data.data;
            this.taskStatus = taskData.status;
            this.lastApiResponse = JSON.stringify(queryResponse.data, null, 2);
            
            // 如果有视频URL但之前没显示，尝试更新
            if (taskData.video_url && !this.videoURL) {
              this.videoURL = taskData.video_url;
              this.addApiLog(`发现视频URL: ${taskData.video_url}`);
            }
          }
        }
        
        this.addApiLog('API测试完成');
      } catch (error) {
        this.addApiLog(`API测试错误: ${error.message}`, true);
        console.error('API测试错误:', error);
      }
    },
    
    // 播放示例视频
    playDemoVideo() {
      this.videoURL = this.demoVideoUrl;
      this.videoStatus = '示例视频';
      this.isMockVideo = false;
      this.addApiLog('播放示例视频');
    },
    
    // 检测是否模拟视频URL
    checkMockVideoUrl(url) {
      // 检查URL是否包含模拟标识
      const mockIdentifiers = ['example.com', 'mock-video', 'mock.video'];
      
      // 生产环境不启用模拟视频检测
      const isProduction = process.env.NODE_ENV === 'production';
      if (isProduction) {
        return false;
      }
      
      return mockIdentifiers.some(identifier => url.includes(identifier));
    },
    copyPromptToClipboard() {
      const tempInput = document.createElement('input');
      tempInput.value = this.formData.prompt;
      document.body.appendChild(tempInput);
      tempInput.select();
      document.execCommand('copy');
      document.body.removeChild(tempInput);
      alert('提示词已复制到剪贴板');
    },
    // 处理视频URL，确保能正确加载
    processVideoUrl(url) {
      if (!url) return '';
      
      console.log('处理视频URL:', url);
      this.addApiLog(`处理原始视频URL: ${url}`);
      
      // 移除可能的@前缀符号
      let processedUrl = url.trim();
      if (processedUrl.startsWith('@')) {
        processedUrl = processedUrl.substring(1);
        console.log('移除@前缀:', processedUrl);
        this.addApiLog(`移除@前缀: ${processedUrl}`);
      }
      
      // 检查并防止URL嵌套
      if (processedUrl.includes('/api/v1/text-to-videos/proxy-video')) {
        console.log('检测到嵌套URL，跳过处理');
        this.addApiLog(`检测到URL已经是代理URL，跳过处理，直接返回`);
        return processedUrl;
      }
      
      // 检查是否为模拟环境
      this.isMockVideo = this.checkMockVideoUrl(processedUrl);
      if (this.isMockVideo) {
        console.log('检测到模拟视频URL');
        this.updateVideoStatus('模拟环境');
        this.addApiLog('检测到模拟视频URL');
        return processedUrl; // 模拟环境直接返回处理后的URL
      }
      
      // 确保URL有正确的scheme
      if (!processedUrl.startsWith('http://') && !processedUrl.startsWith('https://')) {
        if (processedUrl.startsWith('//')) {
          processedUrl = 'https:' + processedUrl;
        } else {
          processedUrl = 'https://' + processedUrl.replace(/^\/+/, '');
        }
        console.log('添加https前缀:', processedUrl);
        this.addApiLog(`添加https前缀: ${processedUrl}`);
      }
      
      // 如果是来自火山引擎的URL，使用后端代理解决CORS问题
      if (processedUrl.includes('tos-cn-beijing.volces.com') || 
          processedUrl.includes('ark-content-generation-cn-beijing')) {
        // 保存原始URL (可能含有必要的授权参数)
        const proxyUrl = `/api/v1/text-to-videos/proxy-video?url=${encodeURIComponent(processedUrl)}`;
        console.log('使用后端代理:', proxyUrl);
        this.addApiLog(`使用后端代理访问视频: ${proxyUrl}`);
        return proxyUrl;
      }
      
      // 以下是处理其他URL的逻辑
      // 检查URL是否为视频文件格式
      const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.m3u8', '.mpd'];
      const hasVideoExtension = videoExtensions.some(ext => processedUrl.toLowerCase().includes(ext));
      
      if (!hasVideoExtension) {
        console.warn('URL可能不是视频文件格式，尝试添加.mp4后缀:', processedUrl);
        this.addApiLog(`警告：URL可能不是视频文件格式，尝试添加后缀`, true);
        
        // 如果URL没有文件扩展名，尝试添加.mp4
        if (!processedUrl.includes('?') && !processedUrl.split('/').pop().includes('.')) {
          processedUrl = processedUrl + '.mp4';
          console.log('添加MP4后缀:', processedUrl);
          this.addApiLog(`添加MP4后缀: ${processedUrl}`);
        }
      }
      
      // 注意：我们现在保留URL中的查询参数，因为它们可能包含必要的授权信息
      
      this.addApiLog(`最终处理后的视频URL: ${processedUrl}`);
      return processedUrl;
    },
    
    // 视频播放器错误处理
    handleVideoError(event) {
      console.error('视频加载错误:', event);
      this.videoError = true;
      
      // 获取详细的错误信息
      const video = event.target;
      
      // 获取网络状态码
      let errorMessage = '未知错误';
      
      if (video.error) {
        switch (video.error.code) {
          case 1:
            errorMessage = '加载过程被中止';
            break;
          case 2:
            errorMessage = '网络错误，无法下载视频';
            break;
          case 3:
            errorMessage = '视频解码错误';
            break;
          case 4:
            errorMessage = '视频格式不支持';
            break;
          default:
            errorMessage = `错误码: ${video.error.code}`;
        }
      }
      
      this.videoErrorMessage = errorMessage;
      this.addApiLog(`视频加载失败: ${errorMessage}`, true);
    },
    
    // 视频成功加载
    handleVideoLoaded() {
      console.log('视频加载成功');
      this.videoError = false;
      this.videoErrorMessage = '';
      this.videoStatus = '已加载';
      this.addApiLog('视频加载成功');
    },
    
    // 尝试备用播放器
    tryAlternativePlayer() {
      console.log('切换到备用播放器');
      this.useAlternativePlayer = true;
      this.addApiLog('已切换到备用播放器');
    },
    
    // 保存视频到历史记录
    saveToHistory(status = 'queued', videoURL = null) {
      // 创建一个历史记录项
      const historyItem = {
        taskId: this.taskId,
        videoURL: videoURL,
        prompt: this.formData.prompt,
        ratio: this.formData.ratio,
        duration: this.formData.duration,
        fps: this.formData.fps,
        resolution: this.formData.resolution,
        watermark: this.formData.watermark,
        time: new Date().toLocaleString(),
        title: `视频 ${this.videoHistory.length + 1}`,
        status: status
      };
      
      // 检查是否已存在相同taskId的记录
      const existingIndex = this.videoHistory.findIndex(item => item.taskId === this.taskId);
      
      if (existingIndex !== -1) {
        // 更新已有记录
        this.videoHistory[existingIndex] = {
          ...this.videoHistory[existingIndex],
          status: status,
          videoURL: videoURL || this.videoHistory[existingIndex].videoURL
        };
        console.log('已更新历史记录，状态:', status);
      } else {
        // 添加到历史记录中
        this.videoHistory.unshift(historyItem);
        console.log('已添加到历史记录，状态:', status);
      }
      
      // 限制历史记录最多5条
      if (this.videoHistory.length > 5) {
        this.videoHistory = this.videoHistory.slice(0, 5);
      }
      
      // 保存到localStorage
      try {
        localStorage.setItem('videoHistory', JSON.stringify(this.videoHistory));
      } catch (e) {
        console.error('保存历史记录到localStorage失败:', e);
      }
    },
    
    // 从历史记录中加载视频
    playHistoryVideo(historyItem) {
      if (!historyItem.videoURL) {
        alert('视频链接不可用');
        return;
      }
      
      // 处理视频URL，确保格式正确
      const processedUrl = this.processVideoUrl(historyItem.videoURL);
      
      // 设置当前视频URL
      this.videoURL = processedUrl;
      this.videoError = false;
      this.videoErrorMessage = '';
      this.useAlternativePlayer = false; // 初始使用原生播放器
      
      this.addApiLog(`播放历史视频，原始URL: ${historyItem.videoURL}, 处理后URL: ${processedUrl}`);
      
      // 设置任务ID和状态，便于刷新视频状态
      this.taskId = historyItem.taskId;
      this.taskStatus = 'success';
      
      // 更新历史记录中的URL
      const index = this.videoHistory.findIndex(item => item.taskId === historyItem.taskId);
      if (index !== -1 && this.videoHistory[index].videoURL !== processedUrl) {
        this.videoHistory[index].videoURL = processedUrl;
        
        // 保存到localStorage
        try {
          localStorage.setItem('videoHistory', JSON.stringify(this.videoHistory));
        } catch (e) {
          console.error('保存历史记录到localStorage失败:', e);
        }
      }
      
      // 关闭历史记录弹窗
      this.showHistoryModal = false;
      
      // Plyr播放器会通过watch videoURL的变化自动初始化
    },
    
    // 应用历史参数
    applyHistoryParams(historyItem) {
      this.formData.prompt = historyItem.prompt;
      this.formData.ratio = historyItem.ratio;
      this.formData.duration = historyItem.duration;
      this.formData.fps = historyItem.fps;
      this.formData.resolution = historyItem.resolution;
      this.formData.watermark = historyItem.watermark;
      
      this.showHistoryModal = false;
      console.log('已应用历史参数');
    },
    
    // 加载历史记录
    loadHistory() {
      try {
        const savedHistory = localStorage.getItem('videoHistory');
        if (savedHistory) {
          this.videoHistory = JSON.parse(savedHistory);
          console.log('已从localStorage加载历史记录，数量:', this.videoHistory.length);
        }
      } catch (e) {
        console.error('从localStorage加载历史记录失败:', e);
      }
    },
    checkHistoryTaskStatus(historyItem) {
      // 暂存当前任务ID
      const currentTaskId = this.taskId;
      
      // 临时设置任务ID为历史任务ID
      this.taskId = historyItem.taskId;
      
      this.addApiLog(`检查历史任务状态，任务ID: ${historyItem.taskId}`);
      
      // 查询状态
      this.checkTaskStatus(true).then(response => {
        if (response && response.status === 'success' && response.videoURL) {
          // 处理视频URL
          const processedUrl = this.processVideoUrl(response.videoURL);
          
          // 更新历史记录
          const index = this.videoHistory.findIndex(item => item.taskId === historyItem.taskId);
          if (index !== -1) {
            this.videoHistory[index].status = 'success';
            this.videoHistory[index].videoURL = processedUrl;
            
            this.addApiLog(`更新历史记录，任务ID: ${historyItem.taskId}, 状态: success, URL: ${processedUrl}`);
            
            // 保存到localStorage
            try {
              localStorage.setItem('videoHistory', JSON.stringify(this.videoHistory));
            } catch (e) {
              console.error('保存历史记录到localStorage失败:', e);
            }
          }
        } else if (response) {
          // 任务还在进行中或失败
          const index = this.videoHistory.findIndex(item => item.taskId === historyItem.taskId);
          if (index !== -1) {
            this.videoHistory[index].status = response.status;
            
            this.addApiLog(`更新历史记录，任务ID: ${historyItem.taskId}, 状态: ${response.status}`);
            
            // 保存到localStorage
            try {
              localStorage.setItem('videoHistory', JSON.stringify(this.videoHistory));
            } catch (e) {
              console.error('保存历史记录到localStorage失败:', e);
            }
          }
        }
      });
      
      // 恢复当前任务ID
      this.taskId = currentTaskId;
    },
    // 测试视频URL是否可访问
    testVideoUrlAccessibility(url) {
      if (!url) return;
      
      this.addApiLog(`测试视频URL可访问性: ${url}`);
      
      // 使用HEAD请求检查URL是否可访问及其Content-Type
      axios.head(url)
        .then(response => {
          const contentType = response.headers['content-type'] || '';
          const isVideo = contentType.includes('video/') || 
                          contentType.includes('application/octet-stream') ||
                          contentType.includes('binary/octet-stream');
          
          this.addApiLog(`视频URL测试成功，Content-Type: ${contentType}`);
          
          if (!isVideo) {
            this.addApiLog(`警告: URL返回的Content-Type不是视频格式: ${contentType}`, true);
          }
        })
        .catch(error => {
          this.addApiLog(`视频URL测试失败: ${error.message}`, true);
          console.error('视频URL测试失败:', error);
        });
    },
    // 初始化Plyr播放器
    initPlayer() {
      if (this.player) {
        this.destroyPlayer();
      }
      
      if (this.videoURL && !this.isMockVideo) {
        // 创建video元素
        const videoElement = document.createElement('video');
        
        // 尝试使用fetch获取视频并创建Blob URL，以解决可能的CORS问题
        this.fetchVideoAndCreateBlobUrl(this.videoURL).then(blobUrl => {
          videoElement.src = blobUrl;
          videoElement.crossOrigin = 'anonymous';
          videoElement.controls = true;
          videoElement.className = 'video-element';
          
          // 清空容器并添加video元素
          const container = this.$refs.plyrContainer;
          if (container) {
            container.innerHTML = '';
            container.appendChild(videoElement);
            
            // 初始化Plyr
            this.player = new Plyr(videoElement, {
              controls: [
                'play-large', 'play', 'progress', 'current-time', 'mute', 
                'volume', 'captions', 'settings', 'pip', 'fullscreen'
              ],
              i18n: {
                restart: '重新开始',
                play: '播放',
                pause: '暂停',
                seekLabel: '跳转至',
                volumeLabel: '音量',
                mute: '静音',
                unmute: '取消静音',
                enableCaptions: '启用字幕',
                disableCaptions: '禁用字幕',
                enterFullscreen: '全屏',
                exitFullscreen: '退出全屏',
                frameTitle: '视频播放器',
                captions: '字幕',
                settings: '设置',
                speed: '速度',
                normal: '正常',
                quality: '质量',
                loop: '循环',
                start: '开始',
                end: '结束',
                all: '全部',
                reset: '重置',
                disabled: '禁用',
                advertisement: '广告'
              }
            });
            
            // 添加事件监听
            this.player.on('error', this.handleVideoError);
            this.player.on('loadeddata', this.handleVideoLoaded);
            
            console.log('Plyr播放器初始化完成');
            this.addApiLog('Plyr播放器初始化完成');
          } else {
            console.error('找不到播放器容器元素');
            this.addApiLog('找不到播放器容器元素', true);
          }
        }).catch(error => {
          console.error('获取视频并创建Blob URL失败:', error);
          this.addApiLog(`获取视频并创建Blob URL失败: ${error.message}`, true);
          
          // 如果Blob方式失败，使用原始URL，添加视频下载按钮
          this.showDirectDownloadLink();
        });
      } else if (this.videoURL && this.isMockVideo) {
        // 对于模拟视频，直接使用URL
        const videoElement = document.createElement('video');
        videoElement.src = this.videoURL;
        videoElement.controls = true;
        videoElement.className = 'video-element';
        
        const container = this.$refs.plyrContainer;
        if (container) {
          container.innerHTML = '';
          container.appendChild(videoElement);
          console.log('模拟视频播放器初始化完成');
        }
      }
    },
    
    // 通过fetch获取视频并创建Blob URL
    async fetchVideoAndCreateBlobUrl(url) {
      this.addApiLog(`开始获取视频并创建Blob URL: ${url}`);
      
      try {
        // 显示加载消息
        const container = this.$refs.plyrContainer;
        if (container) {
          container.innerHTML = `
            <div class="video-loading-container">
              <div class="loading-spinner"></div>
              <p class="loading-text">视频加载中...</p>
            </div>
          `;
        }
        
        // 获取视频文件
        const response = await fetch(url, {
          method: 'GET',
          mode: 'cors',
          cache: 'no-cache'
        });
        
        if (!response.ok) {
          throw new Error(`HTTP错误，状态: ${response.status}`);
        }
        
        // 获取视频数据为Blob
        const blob = await response.blob();
        
        // 创建blob URL
        const blobUrl = URL.createObjectURL(blob);
        this.addApiLog(`成功创建Blob URL: ${blobUrl}`);
        
        return blobUrl;
      } catch (error) {
        this.addApiLog(`获取视频失败: ${error.message}`, true);
        throw error;
      }
    },
    
    // 显示直接下载链接
    showDirectDownloadLink() {
      const container = this.$refs.plyrContainer;
      if (container) {
        container.innerHTML = `
          <div class="video-error-container">
            <div class="video-error-icon">
              <i class="fa fa-exclamation-circle"></i>
            </div>
            <p class="video-error-text">视频无法在浏览器中直接播放，可能是由于跨域限制。</p>
            <div class="video-actions">
              <a href="${this.videoURL}" target="_blank" class="direct-download-btn">
                <i class="fa fa-download"></i> 下载视频
              </a>
              <a href="${this.videoURL}" target="_blank" class="direct-link-btn">
                <i class="fa fa-external-link"></i> 新窗口打开
              </a>
            </div>
          </div>
        `;
      }
    },
    
    // 销毁Plyr播放器
    destroyPlayer() {
      if (this.player) {
        this.player.destroy();
        this.player = null;
        
        // 清空容器
        if (this.$refs.plyrContainer) {
          this.$refs.plyrContainer.innerHTML = '';
        }
        
        console.log('Plyr播放器已销毁');
      }
    },
    // 格式化视频URL以便在UI中显示
    formatVideoUrl(url) {
      if (!url) return '';
      
      // 移除URL开头可能的@符号
      let cleanUrl = url;
      if (cleanUrl.startsWith('@')) {
        cleanUrl = cleanUrl.substring(1);
      }
      
      // 如果URL长度小于40，直接返回
      if (cleanUrl.length <= 40) return cleanUrl;
      
      // 否则截取前15个字符和后15个字符，中间用...连接
      const start = cleanUrl.substring(0, 15);
      const end = cleanUrl.substring(cleanUrl.length - 15);
      return `${start}...${end}`;
    },
    // 添加复制视频URL的方法
    copyVideoUrl(url) {
      if (!url) return;
      
      // 移除可能的@前缀符号
      let cleanUrl = url;
      if (cleanUrl.startsWith('@')) {
        cleanUrl = cleanUrl.substring(1);
        this.addApiLog(`复制前移除@前缀: ${cleanUrl}`);
      }
      
      // 创建临时textarea元素
      const textarea = document.createElement('textarea');
      textarea.value = cleanUrl;
      textarea.style.position = 'fixed';  // 避免滚动到底部
      document.body.appendChild(textarea);
      textarea.select();
      
      try {
        // 尝试复制文本到剪贴板
        const successful = document.execCommand('copy');
        if (successful) {
          alert('视频地址已复制到剪贴板');
          this.addApiLog('已复制视频地址到剪贴板');
        } else {
          alert('复制失败，请手动复制');
          this.addApiLog('复制视频地址失败', true);
        }
      } catch (err) {
        alert('复制失败: ' + err);
        this.addApiLog('复制视频地址出错: ' + err, true);
      }
      
      // 移除临时元素
      document.body.removeChild(textarea);
    },
    // 设置视频状态
    updateVideoStatus(status) {
      this.videoStatus = status;
      this.addApiLog(`视频状态更新: ${status}`);
    },
  },
  watch: {
    videoURL(newVal, oldVal) {
      if (newVal && newVal !== oldVal && !this.useAlternativePlayer) {
        // 在NextTick中初始化播放器，确保DOM已更新
        this.$nextTick(() => {
          this.initPlayer();
        });
      }
    },
    useAlternativePlayer(newVal) {
      if (!newVal) {
        // 如果从备用播放器切回原始播放器，重新初始化
        this.$nextTick(() => {
          this.initPlayer();
        });
      } else {
        // 如果切换到备用播放器，销毁原始播放器
        this.destroyPlayer();
      }
    }
  },
  beforeUnmount() {
    // 组件销毁前清理资源
    this.destroyPlayer();
    
    // 清除任务状态检查定时器
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }
  },
  created() {
    // 从localStorage加载历史记录
    try {
      const storedHistory = localStorage.getItem('videoHistory');
      if (storedHistory) {
        this.videoHistory = JSON.parse(storedHistory);
        console.log('从localStorage加载了', this.videoHistory.length, '条历史记录');
      }
    } catch (e) {
      console.error('加载历史记录失败:', e);
    }
    
    // 启动图标动画
    setInterval(() => {
      if (this.isLoading) {
        this.loadingIconRotation += 30;
        if (this.loadingIconRotation >= 360) {
          this.loadingIconRotation = 0;
        }
      }
    }, 100);
  }
}
</script>

<style scoped>
.longform-article-page {
  padding: 20px;
  max-width: 100%;
  overflow-x: hidden;
  background-color: #f8f9fa;
}

.main-layout {
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: flex-start; /* 确保上对齐 */
}

.left-panel {
  flex: 1.33; /* 从2减小到1.33 */
  min-width: 40%; /* 从60%减小到40% */
  max-width: 47%; /* 从70%减小到47% */
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.right-panel {
  flex: 0.9;
  display: flex;
  flex-direction: column;
  align-self: flex-start; /* 确保右侧面板顶部对齐 */
  max-width: 55%; /* 增加右侧面板最大宽度 */
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-nav h2 {
  font-size: 24px;
  color: #ba003f;
  margin: 0;
}

.test-style {
  border-bottom: 3px solid #ba003f;
  font-weight: bold;
  padding-bottom: 5px;
  text-shadow: 1px 1px 2px rgba(186, 0, 63, 0.2);
}

/* 页面头部按钮容器 */
.page-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 18px;
  cursor: pointer;
  transition: color 0.3s;
}

.action-btn:hover {
  color: #ba003f;
}

.result-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 18px;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group label.required::after {
  content: '*';
  color: #ba003f;
  margin-left: 4px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
  resize: vertical;
}

.form-control:focus {
  border-color: #ba003f;
  outline: none;
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.1);
}

.form-text {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #666;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.radio-item {
  flex: 0 0 auto;
  position: relative;
  cursor: pointer;
}

.radio-item input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.radio-label {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
}

.radio-label i {
  margin-right: 4px;
  color: #666;
}

.radio-item input:checked + .radio-label {
  background-color: rgba(186, 0, 63, 0.1);
  border-color: #ba003f;
  color: #ba003f;
}

.radio-item input:checked + .radio-label i {
  color: #ba003f;
}

.advanced-options-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 10px;
  background: none;
  border: 1px dashed #ddd;
  border-radius: 4px;
  color: #666;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 14px;
  transition: all 0.3s;
}

.advanced-options-button:hover {
  border-color: #ba003f;
  color: #ba003f;
}

.advanced-options-button i {
  margin-right: 8px;
  color: #ba003f;
}

.advanced-options-panel {
  background-color: #f9f9f9;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 20px;
  border: 1px solid #eee;
  display: none;
}

.advanced-options-panel.show {
  display: block;
}

.advanced-options-panel h3 {
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
}

.image-preview-container {
  width: 100%;
  height: 150px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.image-preview-container:hover {
  border-color: #ba003f;
}

.image-preview {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.image-preview-text {
  color: #999;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-preview-text i {
  font-size: 42px;
  margin-bottom: 10px;
  opacity: 0.7;
}

.remove-image-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(186, 0, 63, 0.8);
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-preview-container:hover .remove-image-btn {
  opacity: 1;
}

.upload-btn-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
  width: 100%;
}

.upload-button {
  width: 100%;
  padding: 10px 12px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
}

.upload-button:hover {
  background: #f0f0f0;
  border-color: #ba003f;
  color: #ba003f;
}

.upload-btn-wrapper input[type=file] {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.usage-tips {
  background-color: #f9f9f9;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 20px;
  border: 1px solid #eee;
}

.usage-tips h4 {
  font-size: 14px;
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 6px;
}

.usage-tips ul {
  margin: 0;
  padding-left: 24px;
}

.usage-tips li {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.primary-button {
  flex: 2;
  padding: 12px 20px;
  background-color: #ba003f !important;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 2px 6px rgba(186, 0, 63, 0.2);
}

.primary-button:hover:not(:disabled) {
  background-color: #d4185b !important;
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.3);
  transform: translateY(-1px);
}

.primary-button:disabled {
  background-color: #ddd;
  box-shadow: none;
  cursor: not-allowed;
}

.secondary-button {
  flex: 1;
  padding: 12px 20px;
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.secondary-button:hover {
  background-color: #f0f0f0;
  border-color: #ba003f;
  color: #ba003f;
}

.result-content-wrapper {
  position: relative;
  flex: 1;
  min-height: 350px;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(186, 0, 63, 0.2);
  border-top-color: #ba003f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.loading-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 20px;
}

.progress-container {
  width: 80%;
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.progress-bar {
  height: 100%;
  background-color: #ba003f;
  border-radius: 4px;
  transition: width 0.5s;
}

.progress-text {
  position: absolute;
  top: 10px;
  right: 0;
  font-size: 12px;
  color: #666;
}

.video-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  width: 100%;
  height: 100%;
}

.video-element {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #000;
  max-height: 600px;
}

.video-actions {
  display: flex;
  gap: 12px;
}

.action-button {
  padding: 8px 16px;
  background: white;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-decoration: none;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.action-button:hover {
  border-color: #ba003f;
  color: #ba003f;
}

.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 300px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
}

.empty-message {
  color: #666;
  font-size: 14px;
  margin-top: 16px;
}

.task-info {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 16px;
}

.task-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-info-header h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.refresh-btn {
  background: none;
  border: none;
  color: #ba003f;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-info-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  font-size: 13px;
}

.info-label {
  font-weight: 500;
  color: #666;
  width: 80px;
}

.info-value {
  color: #333;
  flex: 1;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-waiting {
  background-color: #eee;
  color: #666;
}

.status-queued {
  background-color: #e3f2fd;
  color: #0d47a1;
}

.status-running {
  background-color: #fff3e0;
  color: #e65100;
}

.status-success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-error {
  background-color: #ffebee;
  color: #c62828;
}

.status-processing {
  background-color: #e3f2fd;
  color: #1565c0;
}

.status-queued {
  background-color: #fff8e1;
  color: #f57f17;
}

.status-unknown {
  background-color: #f5f5f5;
  color: #616161;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 16px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-header h3 i {
  color: #ba003f;
}

.close-btn {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  font-size: 20px;
  padding: 4px;
}

.modal-body {
  padding: 16px;
}

.modal-body h4 {
  color: #212529;
  margin: 16px 0 8px;
}

.modal-body ul {
  margin: 0;
  padding-left: 20px;
}

.modal-body li {
  margin-bottom: 8px;
  color: #212529;
}

.example-list {
  margin-top: 16px;
}

.example-item {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #ba003f;
}

.example-item strong {
  color: #ba003f;
  display: block;
  margin-bottom: 8px;
  font-size: 15px;
}

.example-item p {
  margin: 0;
  color: #212529;
  font-size: 14px;
  line-height: 1.6;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1200px) {
  .right-panel {
    max-width: 100%;
  }
  
  .reference-card {
    flex: 0 0 220px;
  }
}

@media (max-width: 992px) {
  .main-layout {
    flex-direction: column;
  }
  
  .left-panel {
    max-width: 100%;
  }
  
  .right-panel {
    max-width: 100%;
  }
  
  .reference-card {
    flex: 0 0 240px;
  }
}

/* 添加图标紫荆红色样式 */
.icon-red {
  color: #ba003f !important;
}

/* 修改上传图片的样式 */
.image-preview-container {
  width: 100%;
  height: 150px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.image-preview-container:hover {
  border-color: #ba003f;
}

.image-preview {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.image-preview-text {
  color: #999;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-preview-text i {
  font-size: 42px;
  margin-bottom: 10px;
  opacity: 0.7;
}

.remove-image-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(186, 0, 63, 0.8);
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-preview-container:hover .remove-image-btn {
  opacity: 1;
}

.upload-btn-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
  width: 100%;
}

.upload-button {
  width: 100%;
  padding: 10px 12px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
}

.upload-button:hover {
  background: #f0f0f0;
  border-color: #ba003f;
  color: #ba003f;
}

.upload-btn-wrapper input[type=file] {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

/* 修改生成视频和重置按钮样式 */
.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.primary-button {
  flex: 2;
  padding: 12px 20px;
  background-color: #ba003f !important;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 2px 6px rgba(186, 0, 63, 0.2);
}

.primary-button:hover:not(:disabled) {
  background-color: #d4185b !important;
  box-shadow: 0 4px 8px rgba(186, 0, 63, 0.3);
  transform: translateY(-1px);
}

.primary-button:disabled {
  background-color: #ddd;
  box-shadow: none;
  cursor: not-allowed;
}

.secondary-button {
  flex: 1;
  padding: 12px 20px;
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.secondary-button:hover {
  background-color: #f0f0f0;
  border-color: #ba003f;
  color: #ba003f;
}

/* 优化小贴士模态框 */
.tips-modal {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.tips-list li {
  margin-bottom: 10px;
  line-height: 1.5;
}

.example-item {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #ba003f;
}

.example-item strong {
  color: #ba003f;
  display: block;
  margin-bottom: 8px;
  font-size: 15px;
}

.example-item p {
  margin: 0;
  color: #212529;
  font-size: 14px;
  line-height: 1.6;
}

/* 参考案例区域样式 */
.reference-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

.scroll-buttons {
  display: flex;
  gap: 8px;
}

.scroll-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid #ddd;
  background: white;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.scroll-btn:hover {
  border-color: #ba003f;
  color: #ba003f;
}

.reference-list {
  display: flex;
  overflow-x: auto;
  gap: 16px;
  padding: 8px 4px;
  scroll-behavior: smooth;
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.reference-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.reference-card {
  flex: 0 0 250px;
  border-radius: 8px;
  background-color: #f8f9fa;
  border: 1px solid #eee;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.reference-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-color: #ba003f;
}

.reference-info {
  padding: 12px;
}

.reference-info h4 {
  margin: 0 0 8px;
  color: #333;
  font-size: 16px;
}

.reference-desc {
  color: #666;
  font-size: 12px;
  margin: 0 0 10px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

.reference-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  background-color: rgba(186, 0, 63, 0.1);
  color: #ba003f;
  border-radius: 4px;
  font-size: 12px;
  gap: 4px;
}

.tag i {
  font-size: 14px;
}

/* 添加新的样式 */
.video-error-message {
  margin-top: 10px;
  padding: 12px;
  background-color: #ffebee;
  color: #b71c1c;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 14px;
}

.retry-button {
  margin-left: auto;
  background-color: #fff;
  border: 1px solid #b71c1c;
  color: #b71c1c;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.retry-button:hover {
  background-color: #ffcdd2;
}

.video-debug {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
}

.debug-item {
  margin-bottom: 5px;
  word-break: break-all;
}

.alt-player {
  border: none;
  width: 100%;
  height: 300px;
}

/* 添加任务信息区域新样式 */
.api-response {
  cursor: pointer;
  color: #0066cc;
  display: flex;
  align-items: center;
  gap: 4px;
}

.api-response-details {
  margin-top: 8px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

.api-response-details pre {
  margin: 0;
}

.debug-buttons {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.debug-btn {
  padding: 6px 10px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s;
}

.debug-btn:hover {
  border-color: #ba003f;
  color: #ba003f;
}

.task-debug-info {
  margin-top: 12px;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.debug-section {
  margin-bottom: 10px;
}

.debug-section h5 {
  margin: 0 0 8px;
  font-size: 13px;
  color: #333;
}

.debug-section pre {
  margin: 0;
  font-size: 12px;
  background-color: #fff;
  padding: 8px;
  border-radius: 4px;
  max-height: 150px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

.api-log-item {
  padding: 4px 0;
  font-size: 12px;
  display: flex;
  border-bottom: 1px dotted #ddd;
}

.log-time {
  flex: 0 0 60px;
  color: #999;
}

.log-message {
  flex: 1;
  word-break: break-all;
}

.log-error {
  color: #b71c1c;
}

.text-error {
  color: #b71c1c;
}

/* 添加模拟视频样式 */
.mock-video-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mock-video-placeholder {
  width: 100%;
  height: 300px;
  background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
  border-radius: 8px;
  border: 2px dashed #ba003f;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  padding: 20px;
  text-align: center;
}

.mock-video-placeholder i {
  font-size: 48px;
  margin-right: 20px;
  color: #ba003f;
}

.mock-video-text {
  text-align: left;
  max-width: 80%;
}

.mock-video-text h3 {
  color: #ba003f;
  margin: 0 0 10px 0;
}

.mock-video-text p {
  margin: 5px 0;
  color: #333;
}

.mock-url {
  font-family: monospace;
  padding: 8px;
  background: rgba(0,0,0,0.05);
  border-radius: 4px;
  margin: 10px 0;
  word-break: break-all;
  font-size: 12px;
  color: #666;
}

.mock-actions {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.mock-action-button {
  padding: 10px 16px;
  background-color: #ba003f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: all 0.3s;
}

.mock-action-button:hover {
  background-color: #d4185b;
  transform: translateY(-2px);
}

/* 示例视频模态框 */
.demo-video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.demo-video-content {
  width: 80%;
  max-width: 800px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.demo-video-header {
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.demo-video-header h3 {
  margin: 0;
  color: #333;
}

.close-demo-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.demo-video-player {
  width: 100%;
  height: auto;
  max-height: 70vh;
  background: #000;
}

.demo-video-footer {
  padding: 15px;
  text-align: center;
  font-size: 13px;
  color: #666;
}

.prompt-display {
  margin-bottom: 20px;
}

.video-params {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.param-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.param-label {
  font-weight: 500;
  color: #333;
}

.param-value {
  color: #666;
}

.prompt-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.copy-button {
  background-color: #ba003f;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.copy-button:hover {
  background-color: #d4185b;
}

.loading-tips {
  margin-top: 20px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  max-width: 400px;
  text-align: left;
}

.loading-tips h4 {
  margin-top: 0;
  margin-bottom: 12px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-tips h4 i {
  color: #ba003f;
}

.loading-tips ul {
  padding-left: 20px;
  margin-bottom: 0;
}

.loading-tips li {
  margin-bottom: 8px;
  color: #555;
}

.loading-tips-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.dismiss-tips-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 12px;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.3s;
}

.dismiss-tips-btn:hover {
  color: #ba003f;
}

.prompt-button {
  background-color: rgba(186, 0, 63, 0.15);
  color: #ba003f;
  font-weight: 500;
}

.prompt-button:hover {
  background-color: rgba(186, 0, 63, 0.25);
}

.prompt-display {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #eee;
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.prompt-display p {
  margin: 0;
  white-space: pre-wrap;
  line-height: 1.5;
}

/* 历史记录模态框样式 */
.history-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.history-modal-content {
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.history-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.history-modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.history-modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: calc(80vh - 60px);
}

.no-history {
  text-align: center;
  padding: 30px;
  color: #666;
}

.history-item {
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 16px;
  overflow: hidden;
  transition: all 0.3s;
}

.history-item:hover {
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.history-item-header {
  padding: 12px 16px;
  background-color: #f9f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.history-title {
  font-weight: bold;
  color: #333;
}

.history-time {
  color: #999;
  font-size: 12px;
}

.history-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-error {
  background-color: #ffebee;
  color: #c62828;
}

.status-processing {
  background-color: #e3f2fd;
  color: #1565c0;
}

.status-queued {
  background-color: #fff8e1;
  color: #f57f17;
}

.status-unknown {
  background-color: #f5f5f5;
  color: #616161;
}

.history-item-body {
  padding: 16px;
}

.history-prompt {
  margin-bottom: 12px;
  color: #333;
  line-height: 1.5;
}

.history-details {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}

.history-details span {
  color: #666;
  font-size: 13px;
}

.history-item-footer {
  padding: 12px 16px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.play-btn {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.play-btn:hover {
  background-color: #c8e6c9;
}

.refresh-btn {
  background-color: #e3f2fd;
  color: #1565c0;
}

.refresh-btn:hover {
  background-color: #bbdefb;
}

.error-btn {
  background-color: #ffebee;
  color: #c62828;
  opacity: 0.7;
  cursor: not-allowed;
}

.apply-btn {
  background-color: #f5f5f5;
  color: #424242;
  margin-left: auto;
}

.apply-btn:hover {
  background-color: #e0e0e0;
}

.plyr-container {
  width: 100%;
  height: 400px;
  background-color: #f8f8f8;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 0;
  align-self: flex-start;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-result {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  background-color: white;
}

/* 新的加载动画样式 */
.video-loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(186, 0, 63, 0.1);
  border-radius: 50%;
  border-top: 4px solid #ba003f;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-text {
  font-size: 16px;
  color: #666;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 改善Plyr播放器的外观 */
:deep(.plyr) {
  --plyr-color-main: #5E72E4;
  --plyr-range-thumb-background: #5E72E4;
  --plyr-video-control-color: white;
  --plyr-video-background: black;
  
  border-radius: 8px;
  overflow: hidden;
  width: 100%;
}

:deep(.plyr--video) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.plyr__control--overlaid) {
  background: rgba(94, 114, 228, 0.8);
}

:deep(.plyr__control--overlaid:hover) {
  background: rgba(94, 114, 228, 1);
}

.video-container {
  margin-top: 20px;
  margin-bottom: 30px;
  position: relative;
  width: 100%;
}

.history-item-actions {
  display: flex;
  align-items: center;
  width: 100%;
}

.video-url {
  margin-left: 10px;
  color: #666;
  font-size: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.copy-btn {
  margin-left: 5px;
  font-size: 14px;
  color: #666;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px 5px;
  transition: color 0.3s;
}

.copy-btn:hover {
  color: #ba003f;
}

/* 视频错误容器样式 */
.video-error-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 20px;
  background-color: #ffebee;
  border-radius: 8px;
  text-align: center;
}

.video-error-icon {
  font-size: 36px;
  color: #c62828;
  margin-bottom: 16px;
}

.video-error-text {
  font-size: 14px;
  color: #c62828;
  margin-bottom: 16px;
  max-width: 80%;
}

.video-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.direct-download-btn, .direct-link-btn {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: all 0.3s;
}

.direct-download-btn {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.direct-download-btn:hover {
  background-color: #c8e6c9;
}

.direct-link-btn {
  background-color: #e3f2fd;
  color: #1565c0;
}

.direct-link-btn:hover {
  background-color: #bbdefb;
}

.loading-message {
  padding: 20px;
  text-align: center;
  font-size: 16px;
  color: #666;
}

/* 视频加载样式 */
.video-loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 240px;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.video-loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #ba003f;
  border-radius: 50%;
  margin-bottom: 20px;
  animation: spin 1s linear infinite;
}

.video-loading-text {
  font-size: 18px;
  font-weight: 500;
  color: #444;
  text-align: center;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 视频加载动画样式 */
.video-loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  background-color: #f5f5f5;
  border-radius: 8px;
  color: #333;
}

.video-loading-animation {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.video-loading-pulse {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 3px solid rgba(186, 0, 63, 0.2);
  border-radius: 50%;
  animation: pulse 1.5s ease-out infinite;
}

.video-loading-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 24px;
  color: #ba003f;
  animation: fadeInOut 1.5s ease-in-out infinite;
}

.video-loading-text {
  font-size: 16px;
  color: #666;
  margin-top: 10px;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.8;
  }
  70% {
    transform: scale(1.1);
    opacity: 0.3;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.8;
  }
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
  }
  
  .left-panel {
    max-width: 100%;
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    margin-bottom: 20px;
  }
  
  .right-panel {
    max-width: 100%;
  }
  
  .reference-card {
    flex: 0 0 240px;
  }
}
</style> 
