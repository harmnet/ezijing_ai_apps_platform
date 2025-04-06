<template>
  <div class="longform-article-page">
    <div class="page-header">
      <div class="page-nav">
        <h2>AI文生图</h2>
      </div>
      <div class="page-actions">
        <button class="action-btn" title="创作小贴士" @click="showTips">
          <i class="ri-lightbulb-line"></i>
        </button>
      </div>
    </div>

    <!-- 警告消息 -->
    <div class="api-status-warning" v-if="apiStatus === 'unavailable'">
      <i class="ri-error-warning-line"></i>
      <div class="warning-content">
        <span class="warning-title">后端服务不可用</span>
        <p class="warning-message">{{ error || '无法连接到后端API服务' }}</p>
        <div class="warning-actions">
          <button @click="testApiAvailability" class="retry-button">
            <i class="ri-refresh-line"></i> 重试连接
          </button>
          <a href="http://localhost:9000/api/v1/text_to_image/volcano/info" target="_blank" class="test-link">
            测试API链接
          </a>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 - 使用两列布局 -->
    <div class="main-container">
      <!-- 左侧：输入参数 -->
      <div class="input-section">
        <div class="section-header">
          <h3 class="section-title">
            <i class="ri-settings-3-line"></i>
            输入参数
          </h3>
        </div>

        <div class="form-group">
          <label for="prompt" class="required">提示词</label>
          <textarea 
            id="prompt" 
            v-model="formData.prompt"
            placeholder="请输入详细的图像描述，例如：一只可爱的熊猫在竹林中吃着竹子，阳光明媚..."
            class="form-control"
            rows="6"
          ></textarea>
        </div>

        <div class="form-group">
          <label>图片风格</label>
          <div class="radio-group">
            <label class="radio-item">
              <input type="radio" v-model="formData.style" value="realistic">
              <span class="radio-label">
                <i class="ri-camera-lens-line"></i>
                写实
              </span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.style" value="cartoon">
              <span class="radio-label">
                <i class="ri-brush-3-line"></i>
                卡通
              </span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.style" value="painting">
              <span class="radio-label">
                <i class="ri-paint-brush-line"></i>
                绘画
              </span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.style" value="digital">
              <span class="radio-label">
                <i class="ri-computer-line"></i>
                数字艺术
              </span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.style" value="chinese">
              <span class="radio-label">
                <i class="ri-ink-bottle-line"></i>
                国风
              </span>
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>图片数量</label>
          <div class="radio-group">
            <label class="radio-item">
              <input type="radio" v-model="formData.count" value="1">
              <span class="radio-label">1张</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.count" value="2">
              <span class="radio-label">2张</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.count" value="4">
              <span class="radio-label">4张</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.count" value="6">
              <span class="radio-label">6张</span>
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>长宽比</label>
          <div class="radio-group">
            <label class="radio-item">
              <input type="radio" v-model="formData.aspectRatio" value="1:1">
              <span class="radio-label">1:1</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.aspectRatio" value="16:9">
              <span class="radio-label">16:9</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.aspectRatio" value="9:16">
              <span class="radio-label">9:16</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.aspectRatio" value="4:3">
              <span class="radio-label">4:3</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="formData.aspectRatio" value="3:4">
              <span class="radio-label">3:4</span>
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
            <label>清晰度</label>
            <div class="slider-container">
              <input 
                type="range" 
                min="1" 
                max="10" 
                v-model="formData.clarity" 
                class="range-slider"
              >
              <span>{{ formData.clarity }}</span>
            </div>
            <small>较高的清晰度可能生成更多细节，但需要更长处理时间</small>
          </div>
          
          <div class="form-group">
            <label>创意程度</label>
            <div class="slider-container">
              <input 
                type="range" 
                min="1" 
                max="10" 
                v-model="formData.creativity" 
                class="range-slider"
              >
              <span>{{ formData.creativity }}</span>
            </div>
            <small>较高的创意程度会生成更有想象力的图像，但可能不太符合现实</small>
          </div>
          
          <div class="form-group">
            <label for="negative-prompt">负面提示词（可选）</label>
            <textarea 
              id="negative-prompt" 
              v-model="formData.negativePrompt"
              placeholder="请输入不希望出现在图像中的元素，例如：模糊、变形、低质量..."
              class="form-control"
              rows="3"
            ></textarea>
            <small>常用负面词：模糊、扭曲、变形、低质量、噪点、过度饱和</small>
          </div>
        </div>

        <!-- 生成按钮 -->
        <div class="action-buttons">
          <button @click="generateImage" class="btn btn-primary" :disabled="isLoading">
            <i class="ri-magic-line" v-if="!isLoading"></i>
            <i class="ri-loader-4-line spinning" v-else></i>
            {{ isLoading ? '生成中...' : '生成图像' }}
          </button>
          <button @click="resetForm" class="btn btn-secondary">
            <i class="ri-refresh-line"></i>
            重置
          </button>
        </div>
      </div>

      <!-- 右侧：生成结果 -->
      <div class="right-column">
        <!-- 参考案例区域 -->
        <div class="reference-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-gallery-line"></i>
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
                  <span class="tag"><i class="ri-brush-line"></i> {{ getStyleLabel(example.style) }}</span>
                  <span class="tag"><i class="ri-aspect-ratio-line"></i> {{ example.aspectRatio }}</span>
                  <span class="tag"><i class="ri-image-line"></i> {{ example.count }}张</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="result-section">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-image-line"></i>
              生成结果
            </h3>
            <div class="action-buttons" v-if="generatedImages.length > 0">
              <button @click="generateImage" class="primary-button" :disabled="isLoading">
                <i class="ri-refresh-line" v-if="!isLoading"></i>
                <i class="ri-loader-4-line spinning" v-else></i>
                {{ isLoading ? '生成中...' : '重新生成' }}
              </button>
              <button @click="showPrompt" class="secondary-button">
                <i class="ri-file-text-line"></i>
                查看提示词
              </button>
            </div>
          </div>

          <!-- 增强提示词区域 -->
          <div class="enhanced-prompt-section" v-if="enhancedPrompt">
            <div class="enhanced-prompt-header">
              <h4><i class="ri-magic-line"></i> AI增强提示词</h4>
              <button @click="toggleEnhancedPrompt" class="toggle-button">
                {{ showEnhancedPrompt ? '收起' : '展开' }}
              </button>
            </div>
            <div class="enhanced-prompt-content" v-if="showEnhancedPrompt">
              <p>{{ enhancedPrompt }}</p>
            </div>
          </div>

          <div class="images-grid">
            <div v-for="(image, index) in generatedImages" 
                 :key="index" 
                 class="image-card">
              <div class="image-container" :class="getImageClass(image)">
                <img :src="image.url" alt="生成的图片" loading="lazy" />
              </div>
              <div class="image-actions">
                <button @click="downloadImage(image.url, index)" title="下载图片">
                  <i class="ri-download-line"></i>
                </button>
                <button @click="regenerateImage(index)" title="重新生成此图片">
                  <i class="ri-refresh-line"></i>
                </button>
              </div>
            </div>
          </div>
          
          <div class="loading-indicator" v-if="isLoading">
            <div class="spinner"></div>
            <p>AI正在创作中，请稍候...</p>
          </div>
          
          <div class="error-message" v-if="error">
            <i class="ri-error-warning-line"></i>
            <p>{{ error }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 提示词对话框 -->
    <div class="modal" v-if="showPromptDialog">
      <div class="modal-content">
        <div class="modal-header">
          <h3>当前提示词</h3>
          <button @click="showPromptDialog = false" class="close-button">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <p class="prompt-text">{{ formData.prompt }}</p>
          
          <div v-if="enhancedPrompt" class="enhanced-prompt-full">
            <h4>AI增强提示词</h4>
            <p>{{ enhancedPrompt }}</p>
          </div>
          
          <div v-if="formData.negativePrompt" class="negative-prompt">
            <h4>负面提示词</h4>
            <p>{{ formData.negativePrompt }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 创作小贴士对话框 -->
    <div class="modal" v-if="showTipsDialog">
      <div class="modal-content tips-modal">
        <div class="modal-header">
          <h3><i class="ri-lightbulb-line"></i> 创作小贴士</h3>
          <button @click="showTipsDialog = false" class="close-button">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="tips-section">
            <h4>提示词技巧</h4>
            <ul>
              <li>提供详细的场景描述，包括场景、主体、动作、表情等</li>
              <li>指定艺术风格，如油画、水彩、素描、动漫等</li>
              <li>描述光照条件，如"阳光明媚"、"黄昏时分"、"月光下"</li>
              <li>提及视角和构图，如"俯视角"、"特写镜头"、"全景视图"</li>
            </ul>
          </div>
          
          <div class="tips-section">
            <h4>最佳实践</h4>
            <ul>
              <li>尝试不同的长宽比以获得最适合场景的构图</li>
              <li>生成多张图片以比较效果并选择最佳成果</li>
              <li>对于概念清晰的场景，增加清晰度值</li>
              <li>对于创意性的想法，提高创意程度值</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TextToImage',
  
  data() {
    return {
      formData: {
        prompt: '',
        style: 'realistic',
        clarity: 7,
        creativity: 5,
        negativePrompt: '',
        count: 4,
        aspectRatio: '1:1'
      },
      showAdvancedOptions: false,
      isLoading: false,
      error: null,
      generatedImages: [],
      showPromptDialog: false,
      showTipsDialog: false,
      showEnhancedPrompt: false,
      enhancedPrompt: '',
      apiStatus: 'unknown', // 'unknown', 'available', 'unavailable'
      apiCheckInterval: null, // 用于存储API检查的定时器ID
      referenceExamples: [
        {
          title: '梦幻森林',
          description: '一片神秘的森林，萤火虫在空中飞舞，月光透过树叶洒落在苔藓地面上，营造出梦幻般的氛围。远处有一座小木屋，温暖的灯光从窗户中透出。',
          style: 'realistic',
          aspectRatio: '16:9',
          count: 1,
          prompt: '一片神秘的森林，萤火虫在空中飞舞，月光透过树叶洒落在苔藓地面上，营造出梦幻般的氛围。远处有一座小木屋，温暖的灯光从窗户中透出。',
          clarity: 8,
          creativity: 7
        },
        {
          title: '未来城市',
          description: '一座充满科技感的未来城市，高耸的玻璃建筑反射着霓虹灯光，飞行器在建筑之间穿梭，街道上充满全息投影广告。',
          style: 'digital',
          aspectRatio: '16:9',
          count: 1,
          prompt: '一座充满科技感的未来城市，高耸的玻璃建筑反射着霓虹灯光，飞行器在建筑之间穿梭，街道上充满全息投影广告。',
          clarity: 9,
          creativity: 8
        },
        {
          title: '水墨山水',
          description: '一幅传统中国水墨画，远山含黛，近处溪流潺潺，几只白鹤在天空盘旋，一叶扁舟在水面轻荡。',
          style: 'chinese',
          aspectRatio: '4:3',
          count: 1,
          prompt: '一幅传统中国水墨画，远山含黛，近处溪流潺潺，几只白鹤在天空盘旋，一叶扁舟在水面轻荡。',
          clarity: 7,
          creativity: 6
        },
        {
          title: '可爱宠物',
          description: '一只戴着贝雷帽的橘猫，坐在画架前，爪子上沾着颜料，正在认真地作画。周围散落着画笔和调色板。',
          style: 'cartoon',
          aspectRatio: '1:1',
          count: 1,
          prompt: '一只戴着贝雷帽的橘猫，坐在画架前，爪子上沾着颜料，正在认真地作画。周围散落着画笔和调色板。',
          clarity: 8,
          creativity: 9
        },
        {
          title: '美食静物',
          description: '一份精致的下午茶，包含手工制作的马卡龙、水果塔和红丝绒蛋糕。搭配着白瓷茶具和新鲜的玫瑰花。',
          style: 'realistic',
          aspectRatio: '1:1',
          count: 1,
          prompt: '一份精致的下午茶，包含手工制作的马卡龙、水果塔和红丝绒蛋糕。搭配着白瓷茶具和新鲜的玫瑰花。',
          clarity: 9,
          creativity: 6
        },
        {
          title: '童话场景',
          description: '一座由糖果和饼干建成的城堡，棉花糖云朵漂浮在天空中，巧克力河流环绕城堡流淌，小精灵在空中飞舞。',
          style: 'cartoon',
          aspectRatio: '4:3',
          count: 1,
          prompt: '一座由糖果和饼干建成的城堡，棉花糖云朵漂浮在天空中，巧克力河流环绕城堡流淌，小精灵在空中飞舞。',
          clarity: 7,
          creativity: 9
        },
        {
          title: '人物肖像',
          description: '一位身着复古礼服的年轻女子，站在玫瑰花园中，金色的阳光洒在她的长发上，营造出柔美的氛围。',
          style: 'painting',
          aspectRatio: '3:4',
          count: 1,
          prompt: '一位身着复古礼服的年轻女子，站在玫瑰花园中，金色的阳光洒在她的长发上，营造出柔美的氛围。',
          clarity: 9,
          creativity: 7
        },
        {
          title: '机械世界',
          description: '一个由齿轮、管道和蒸汽组成的蒸汽朋克风格房间，铜制的机械装置在运转，墙上挂着复古的时钟和仪表。',
          style: 'digital',
          aspectRatio: '16:9',
          count: 1,
          prompt: '一个由齿轮、管道和蒸汽组成的蒸汽朋克风格房间，铜制的机械装置在运转，墙上挂着复古的时钟和仪表。',
          clarity: 8,
          creativity: 8
        },
        {
          title: '抽象艺术',
          description: '一幅充满动感的抽象画，蓝色和金色的漩涡交织在一起，形成流动的能量场，点缀着星光般的亮点。',
          style: 'digital',
          aspectRatio: '1:1',
          count: 1,
          prompt: '一幅充满动感的抽象画，蓝色和金色的漩涡交织在一起，形成流动的能量场，点缀着星光般的亮点。',
          clarity: 7,
          creativity: 10
        },
        {
          title: '自然风光',
          description: '日出时分的薰衣草田，紫色的花海一望无际，金色的阳光洒在花田上，远处是连绵的山脉和淡淡的晨雾。',
          style: 'realistic',
          aspectRatio: '16:9',
          count: 1,
          prompt: '日出时分的薰衣草田，紫色的花海一望无际，金色的阳光洒在花田上，远处是连绵的山脉和淡淡的晨雾。',
          clarity: 9,
          creativity: 6
        }
      ]
    }
  },

  mounted() {
    // 在组件挂载后测试API可用性
    this.testApiAvailability();
    
    // 设置定期检查API状态（每30秒检查一次）
    this.apiCheckInterval = setInterval(() => {
      this.testApiAvailability();
    }, 30000);
  },

  beforeUnmount() {
    // 组件卸载前清除定时器
    if (this.apiCheckInterval) {
      clearInterval(this.apiCheckInterval);
    }
  },

  methods: {
    showTips() {
      this.showTipsDialog = true
    },

    showPrompt() {
      this.showPromptDialog = true
    },

    toggleAdvancedOptions() {
      this.showAdvancedOptions = !this.showAdvancedOptions
    },

    resetForm() {
      this.formData = {
        prompt: '',
        style: 'realistic',
        clarity: 7,
        creativity: 5,
        negativePrompt: '',
        count: 4,
        aspectRatio: '1:1'
      }
      this.showAdvancedOptions = false
    },

    async generateImage() {
      if (!this.formData.prompt.trim()) {
        this.error = '请输入提示词'
        return
      }

      // 检查API可用性
      if (this.apiStatus === 'unavailable') {
        this.error = '后端服务不可用，请确保后端服务已启动并且运行在9000端口'
        return
      }

      this.isLoading = true
      this.error = null

      try {
        const { width, height } = this.calculateDimensions(this.formData.aspectRatio)

        const response = await this.callGenerateAPI({
          ...this.formData,
          width,
          height
        })

        this.handleGenerateResponse(response)
      } catch (error) {
        this.error = `生成失败：${error.message || '未知错误'}`
        console.error('生成失败详情:', error);
        
        // 提供更具体的错误信息和解决方案
        if (error.message && error.message.includes('fetch')) {
          this.error = '无法连接到后端服务，请确保：\n1. 后端服务已启动并运行在9000端口\n2. 后端API路由正确配置'
        } else if (error.message && error.message.includes('JSON')) {
          this.error = '服务器返回了无效的数据格式，可能是后端服务出现问题'
        }
      } finally {
        this.isLoading = false
      }
    },

    calculateDimensions(aspectRatio) {
      const dimensions = {
        '1:1': { width: 1024, height: 1024 },
        '16:9': { width: 1024, height: 576 },
        '9:16': { width: 576, height: 1024 },
        '4:3': { width: 1024, height: 768 },
        '3:4': { width: 768, height: 1024 }
      }
      return dimensions[aspectRatio] || dimensions['1:1']
    },

    async callGenerateAPI(params) {
      // 调用我们新创建的火山引擎文生图接口
      try {
        const response = await fetch('http://localhost:9000/api/v1/text_to_image/volcano', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            prompt: params.prompt,
            width: params.width,
            height: params.height,
            count: parseInt(params.count),
            scale: params.style === 'realistic' ? 4.0 : 3.5,
            steps: params.clarity ? Math.max(15, Math.min(50, params.clarity * 5)) : 25,
            use_sr: true,
            return_url: true,
            add_watermark: false
          })
        })
  
        // 首先尝试获取响应文本
        const responseText = await response.text();
        
        // 检查响应是否为JSON
        let responseData;
        try {
          responseData = JSON.parse(responseText);
        } catch (e) {
          console.error('非法JSON响应:', responseText);
          throw new Error(`服务器返回了非法的响应: ${responseText.substring(0, 100)}${responseText.length > 100 ? '...' : ''}`);
        }
        
        if (!response.ok) {
          throw new Error(responseData.error || '未知错误');
        }
        
        return responseData;
      } catch (error) {
        console.error('API调用错误:', error);
        throw error;
      }
    },

    handleGenerateResponse(response) {
      // 处理火山引擎API返回的数据
      if (response.success && response.data?.images) {
        // 火山引擎API返回格式
        this.generatedImages = response.data.images.map(image => ({ 
          url: image.url,
          aspectRatio: this.formData.aspectRatio
        }))
        
        // 如果有增强提示词，显示增强后的提示词
        if (response.data.enhanced_prompt) {
          this.enhancedPrompt = response.data.enhanced_prompt;
          // 默认展开增强提示词显示
          this.showEnhancedPrompt = true;
        } else {
          this.enhancedPrompt = '';
        }
      } else if (response.data?.image_urls) {
        // MiniMax API 返回格式
        this.generatedImages = response.data.image_urls.map(url => ({ 
          url,
          aspectRatio: this.formData.aspectRatio
        }))
        this.enhancedPrompt = '';
      } else if (response.images) {
        // 可能的其他API返回格式
        this.generatedImages = response.images.map(url => ({
          url,
          aspectRatio: this.formData.aspectRatio
        }))
        this.enhancedPrompt = '';
      } else if (response.base64) {
        // Base64格式图片
        this.generatedImages = response.base64.map(base64 => ({
          url: `data:image/png;base64,${base64}`,
          aspectRatio: this.formData.aspectRatio
        }))
        this.enhancedPrompt = '';
      } else {
        this.enhancedPrompt = '';
        throw new Error("返回数据格式不正确");
      }
    },

    downloadImage(url, index) {
      const fileName = `AI生成图片_${new Date().toISOString().slice(0,10)}_${index + 1}.jpg`;
      
      // 如果是远程URL，需要先获取图片
      if (url.startsWith('http')) {
        fetch(url)
          .then(response => response.blob())
          .then(blob => {
            const blobUrl = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
          })
          .catch(error => {
            console.error('下载图片失败:', error);
            this.error = '下载图片失败';
          });
      } else {
        // 本地Base64图片直接下载
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    },

    async regenerateImage(index) {
      // 实现单张图片重新生成的逻辑
      // TODO: 调用API重新生成单张图片
    },

    applyExample(example) {
      this.formData = {
        ...this.formData,
        prompt: example.prompt,
        style: example.style,
        count: example.count,
        aspectRatio: example.aspectRatio,
        clarity: example.clarity,
        creativity: example.creativity
      }
      // 滚动到表单顶部
      this.$nextTick(() => {
        document.querySelector('.input-section').scrollIntoView({ behavior: 'smooth' })
      })
    },

    scrollReferences(direction) {
      const container = this.$refs.referenceList
      const scrollAmount = 320 // 一次滚动一个卡片的宽度加间距
      
      if (direction === 'left') {
        container.scrollBy({
          left: -scrollAmount,
          behavior: 'smooth'
        })
      } else {
        container.scrollBy({
          left: scrollAmount,
          behavior: 'smooth'
        })
      }
    },

    getStyleLabel(style) {
      const styleMap = {
        'realistic': '写实',
        'cartoon': '卡通',
        'painting': '绘画',
        'digital': '数字艺术',
        'chinese': '国风'
      }
      return styleMap[style] || style
    },

    getImageClass(image) {
      // 根据图片长宽比返回合适的类名
      const aspectRatio = image.aspectRatio || this.formData.aspectRatio
      
      if (aspectRatio === '16:9') {
        return 'landscape-image'
      } else if (aspectRatio === '9:16') {
        return 'portrait-image'
      } else if (aspectRatio === '4:3') {
        return 'landscape-image-mild'
      } else if (aspectRatio === '3:4') {
        return 'portrait-image-mild'
      } else {
        return 'square-image'
      }
    },

    toggleEnhancedPrompt() {
      this.showEnhancedPrompt = !this.showEnhancedPrompt
    },

    // 添加测试API可用性的方法
    async testApiAvailability() {
      try {
        console.log('正在检测后端API可用性...');
        const response = await fetch('http://localhost:9000/api/v1/text_to_image/volcano/info');
        
        if (response.ok) {
          const data = await response.json();
          console.log('API服务可用:', data);
          this.apiStatus = 'available';
          // 清除之前可能存在的错误信息
          if (this.error && this.error.includes('后端服务不可用')) {
            this.error = null;
          }
        } else {
          console.error('API服务返回错误状态码:', response.status, response.statusText);
          this.apiStatus = 'unavailable';
          this.error = `后端服务返回错误 (${response.status}): ${response.statusText}`;
        }
      } catch (error) {
        console.error('API检测失败:', error);
        this.apiStatus = 'unavailable';
        this.error = `无法连接到后端服务 (http://localhost:9000): ${error.message}`;
      }
    }
  }
}
</script>

<style scoped>
.longform-article-page {
  padding: 24px;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-nav h2 {
  font-size: 24px;
  color: #212529;
  margin: 0;
}

.action-btn {
  background: none;
  border: none;
  color: #ba003f;
  cursor: pointer;
  padding: 8px;
  font-size: 20px;
  transition: color 0.3s;
}

.action-btn:hover {
  color: #d4004d;
}

.main-container {
  display: flex;
  gap: 24px;
}

.input-section {
  width: 320px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.right-column {
  flex: 1;
  min-width: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  color: #212529;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title i {
  color: #ba003f;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #212529;
}

.form-group label.required::after {
  content: '*';
  color: #ba003f;
  margin-left: 4px;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #ba003f;
  outline: none;
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.1);
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.form-group small {
  display: block;
  margin-top: 4px;
  color: #6c757d;
  font-size: 12px;
}

.advanced-options-button {
  width: 100%;
  padding: 10px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  color: #212529;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 16px 0;
  transition: all 0.3s;
}

.advanced-options-button:hover {
  background: #e9ecef;
}

.advanced-options-panel {
  background: #f8f9fa;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 16px;
  display: none;
}

.advanced-options-panel.show {
  display: block;
}

.advanced-options-panel h3 {
  font-size: 16px;
  color: #ba003f;
  margin: 0 0 16px 0;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.range-slider {
  flex: 1;
  height: 4px;
  background: #e9ecef;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
}

.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: #ba003f;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
}

.range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  background: #d4004d;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-primary {
  background: #ba003f;
  color: white;
  border: none;
  flex: 2;
}

.btn-primary:hover:not(:disabled) {
  background: #d4004d;
}

.btn-secondary {
  background: white;
  color: #212529;
  border: 1px solid #e9ecef;
  flex: 1;
}

.btn-secondary:hover {
  background: #e9ecef;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.result-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-height: 600px;
}

.result-content-wrapper {
  position: relative;
  min-height: 400px;
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
  width: 40px;
  height: 40px;
  border: 4px solid #e9ecef;
  border-top-color: #ba003f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 16px;
  color: #212529;
}

.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.empty-content {
  text-align: center;
}

.empty-image {
  width: 128px;
  height: 128px;
  margin-bottom: 16px;
}

.empty-message {
  color: #6c757d;
  font-size: 14px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 24px;
}

.image-card {
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.image-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.image-container {
  position: relative;
  width: 100%;
  padding-bottom: 100%; /* 默认1:1比例 */
  overflow: hidden;
}

.image-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 不同图片比例的样式 */
.landscape-image {
  padding-bottom: 56.25%; /* 16:9 */
}

.portrait-image {
  padding-bottom: 177.78%; /* 9:16 */
}

.landscape-image-mild {
  padding-bottom: 75%; /* 4:3 */
}

.portrait-image-mild {
  padding-bottom: 133.33%; /* 3:4 */
}

.square-image {
  padding-bottom: 100%; /* 1:1 */
}

.prompt-section {
  margin-bottom: 16px;
}

.prompt-content {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 14px;
  color: #212529;
  white-space: pre-wrap;
}

.prompt-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
}

.meta-item {
  padding: 6px 12px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 13px;
}

.meta-label {
  font-weight: 500;
  color: #ba003f;
}

.meta-value {
  color: #212529;
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
  margin-bottom: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 4px;
}

.example-item strong {
  color: #ba003f;
  display: block;
  margin-bottom: 4px;
}

.example-item p {
  margin: 0;
  color: #212529;
  font-size: 14px;
  line-height: 1.5;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.blur-content {
  filter: blur(3px);
  pointer-events: none;
}

@media (max-width: 1024px) {
  .main-container {
    flex-direction: column;
  }

  .input-section {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .image-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}

.radio-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.radio-item {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
  flex: 1;
  min-width: 100px;
}

.radio-item input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-label {
  width: 100%;
  padding: 8px 16px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 20px;
  font-size: 14px;
  color: #212529;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.radio-label i {
  font-size: 16px;
  color: #6c757d;
  transition: all 0.3s;
}

.radio-item:hover .radio-label {
  border-color: #ba003f;
  color: #ba003f;
}

.radio-item:hover .radio-label i {
  color: #ba003f;
}

.radio-item input[type="radio"]:checked + .radio-label {
  background: #ba003f;
  border-color: #ba003f;
  color: white;
}

.radio-item input[type="radio"]:checked + .radio-label i {
  color: white;
}

.radio-item input[type="radio"]:focus + .radio-label {
  box-shadow: 0 0 0 2px rgba(186, 0, 63, 0.1);
}

.reference-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.reference-list {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 4px;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

.reference-list::-webkit-scrollbar {
  height: 8px;
}

.reference-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.reference-list::-webkit-scrollbar-thumb {
  background: #ba003f;
  border-radius: 4px;
}

.reference-card {
  flex: 0 0 300px;
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
}

.reference-card:hover {
  transform: translateY(-4px);
  border: 1px solid #ba003f;
}

.reference-info {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.reference-info h4 {
  margin: 0 0 12px 0;
  color: #212529;
  font-size: 16px;
}

.reference-desc {
  margin: 0 0 12px 0;
  color: #6c757d;
  font-size: 14px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.reference-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 12px;
  color: #ba003f;
}

.tag i {
  font-size: 14px;
}

.scroll-buttons {
  display: flex;
  gap: 8px;
}

.scroll-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid #e9ecef;
  background: white;
  color: #ba003f;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.scroll-btn:hover {
  background: #ba003f;
  color: white;
  border-color: #ba003f;
}

.scroll-btn i {
  font-size: 20px;
}

.primary-button {
  padding: 10px 16px;
  background: #ba003f;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.primary-button:hover:not(:disabled) {
  background: #d4004d;
}

.primary-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.secondary-button {
  padding: 10px 16px;
  background: white;
  color: #ba003f;
  border: 1px solid #ba003f;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.secondary-button:hover {
  background: rgba(186, 0, 63, 0.1);
}

.enhanced-prompt-section {
  margin-top: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.enhanced-prompt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.enhanced-prompt-header h4 {
  font-size: 18px;
  color: #212529;
  margin: 0;
}

.toggle-button {
  background: none;
  border: none;
  color: #ba003f;
  cursor: pointer;
  font-size: 16px;
  padding: 0;
}

.enhanced-prompt-content {
  margin-bottom: 16px;
}

.images-grid {
  margin-top: 16px;
  margin-bottom: 16px;
}

.image-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.image-actions button {
  background: none;
  border: none;
  color: #ba003f;
  cursor: pointer;
  padding: 0;
  font-size: 16px;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e9ecef;
  border-top-color: #ba003f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  margin-top: 16px;
  color: #ba003f;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.error-message i {
  font-size: 16px;
}

.api-status-warning {
  background-color: #fff3cd;
  color: #856404;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  border: 1px solid #ffeeba;
}

.api-status-warning i {
  font-size: 24px;
  color: #e0a800;
  margin-top: 2px;
}

.warning-content {
  flex: 1;
}

.warning-title {
  font-weight: bold;
  font-size: 16px;
  display: block;
  margin-bottom: 4px;
}

.warning-message {
  margin: 0 0 10px 0;
  white-space: pre-line;
}

.warning-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.retry-button {
  background-color: #e0a800;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #d39e00;
}

.test-link {
  color: #856404;
  text-decoration: underline;
  font-size: 14px;
}
</style>