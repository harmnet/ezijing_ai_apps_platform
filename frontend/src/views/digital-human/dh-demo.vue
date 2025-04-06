<template>
  <div class="dh-demo-container">
    <h2 class="title">数字人PPT讲解视频生成</h2>
    
    <el-form ref="formRef" :model="form" label-width="120px" class="form-container">
      <el-form-item label="视频名称">
        <el-input v-model="form.outputVideoName" placeholder="请输入生成视频的名称"></el-input>
      </el-form-item>
      
      <el-form-item label="PPT文件">
        <el-upload
          class="upload-demo"
          action="/api/v1/aibeings/upload" 
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :before-upload="beforeUpload"
          :limit="1"
          accept=".ppt,.pptx"
        >
          <el-button type="primary">选择PPT文件</el-button>
          <template #tip>
            <div class="el-upload__tip">选择文件后会自动上传到OSS</div>
          </template>
        </el-upload>
        <div v-if="form.pptUrl" class="uploaded-file-info">
          <p><el-icon><Document /></el-icon> 已上传: {{ form.pptFileName }}</p>
          <p class="file-url">文件链接: {{ form.pptUrl }}</p>
        </div>
      </el-form-item>
      
      <!-- 场景配置区域 -->
      <div class="scenes-container">
        <h3>场景配置 <el-tooltip content="每个场景对应PPT的一页，可以配置不同的数字人位置和播报内容"><el-icon><QuestionFilled /></el-icon></el-tooltip></h3>
        
        <el-tabs v-model="activeScene" type="card" class="scene-tabs" closable @tab-remove="removeScene" @tab-click="handleTabClick">
          <el-tab-pane 
            v-for="(scene, index) in form.scenes" 
            :key="index"
            :label="`场景 ${index + 1}`"
            :name="index.toString()"
          >
            <!-- 调试信息 -->
            <div class="debug-info" style="background: #f8f8f8; padding: 5px; margin-bottom: 10px; font-size: 12px; border-left: 2px solid #409EFF;">
              数据检查: 宽度={{ scene.attributes?.width }}, 高度={{ scene.attributes?.height }}, 
              X={{ scene.attributes?.x }}, Y={{ scene.attributes?.y }},
              姿势={{ getPositionType(scene) }}
            </div>
            
            <el-form-item label="数字人">
              <el-select v-model="scene.virtualHumanId" placeholder="选择数字人">
                <el-option label="默认数字人(VHP3S1EF7)" value="VHP3S1EF7"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="姿势">
              <el-select 
                v-model="scene.virtualHumanPostureId" 
                placeholder="选择数字人姿势"
                @change="() => handlePostureChange(parseInt(activeScene))"
              >
                <el-option label="右侧站立(aMiAX96rMqNS)" value="aMiAX96rMqNS"></el-option>
                <el-option label="左侧站立(d5nJE6EI0txK)" value="d5nJE6EI0txK"></el-option>
              </el-select>
              <span class="default-value-hint">当前位置: {{ getPositionType(scene) }}</span>
            </el-form-item>
            
            <el-form-item label="数字人位置">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="宽度">
                    <el-input
                      type="number"
                      v-model="scene.attributes.width"
                      placeholder="宽度"
                      @change="(val) => updateDimensionValue(parseInt(activeScene), 'width', val)"
                    ></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="高度">
                    <el-input
                      type="number"
                      v-model="scene.attributes.height"
                      placeholder="高度"
                      @change="(val) => updateDimensionValue(parseInt(activeScene), 'height', val)"
                    ></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="X坐标">
                    <el-input
                      type="number"
                      v-model="scene.attributes.x"
                      placeholder="X坐标"
                      @change="(val) => updateDimensionValue(parseInt(activeScene), 'x', val)"
                    ></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="Y坐标">
                    <el-input
                      type="number"
                      v-model="scene.attributes.y"
                      placeholder="Y坐标"
                      @change="(val) => updateDimensionValue(parseInt(activeScene), 'y', val)"
                    ></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form-item>
            
            <el-form-item label="语音">
              <el-select v-model="scene.voiceId" placeholder="选择语音">
                <el-option label="默认语音(101-master-ugdr)" value="101-master-ugdr"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="语音文本">
              <el-input 
                v-model="scene.voiceText" 
                type="textarea" 
                :rows="3" 
                placeholder="输入此场景的语音文本（如果PPT有备注，可以不填写）"
              ></el-input>
              <span class="help-text">* 注意：如果PPT中设置了备注，会优先使用PPT备注作为语音文本</span>
            </el-form-item>
            
            <el-form-item label="显示字幕">
              <el-switch v-model="scene.enableCaption" @change="toggleCaption(index)"></el-switch>
            </el-form-item>
            
            <template v-if="scene.enableCaption && scene.caption">
              <el-row :gutter="16">
                <el-col :span="12">
                  <el-form-item label="字幕字号">
                    <el-input
                      type="number"
                      v-model="scene.caption.attributes.fontSize"
                      placeholder="字幕字号"
                      @change="(val) => updateCaptionValue(parseInt(activeScene), 'fontSize', val)"
                    ></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="字幕Y坐标">
                    <el-input
                      type="number"
                      v-model="scene.caption.attributes.y"
                      placeholder="字幕Y坐标"
                      @change="(val) => updateCaptionValue(parseInt(activeScene), 'y', val)"
                    ></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="字体颜色">
                <el-color-picker 
                  v-model="scene.caption.attributes.fontColor" 
                  show-alpha
                ></el-color-picker>
              </el-form-item>
              
              <el-form-item label="字体样式">
                <el-checkbox v-model="scene.caption.attributes.bold">粗体</el-checkbox>
                <el-checkbox v-model="scene.caption.attributes.italic">斜体</el-checkbox>
                <el-checkbox v-model="scene.caption.attributes.underline">下划线</el-checkbox>
              </el-form-item>
            </template>
            
            <el-form-item label="字幕位置">
              <el-select v-model="scene.captionPosition" @change="updateCaptionPosition(parseInt(activeScene))">
                <el-option label="左上" value="topLeft"></el-option>
                <el-option label="居中" value="topCenter"></el-option>
                <el-option label="右上" value="topRight"></el-option>
              </el-select>
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
        
        <div class="scene-actions">
          <el-button type="primary" plain @click="addScene">
            <el-icon><Plus /></el-icon> 添加场景
          </el-button>
          <el-button type="info" plain @click="copyLastScene" :disabled="form.scenes.length === 0">
            <el-icon><CopyDocument /></el-icon> 复制最后一个场景
          </el-button>
        </div>
      </div>
      
      <!-- 背景音乐配置 -->
      <el-divider>背景音乐配置</el-divider>
      
      <el-form-item label="启用背景音乐">
        <el-switch v-model="form.enableBgm"></el-switch>
      </el-form-item>
      
      <template v-if="form.enableBgm">
        <el-form-item label="音乐URL">
          <el-input v-model="form.bgm.mediaUrl" placeholder="输入背景音乐URL">
            <template #append>
              <el-button @click="setBgmDefaultUrl">使用默认</el-button>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="音量">
          <el-slider v-model="form.bgm.volume" :min="0" :max="1" :step="0.1" show-stops></el-slider>
        </el-form-item>
        
        <el-form-item label="循环播放">
          <el-switch v-model="form.bgm.loop"></el-switch>
        </el-form-item>
      </template>
      
      <!-- PPT配置 -->
      <el-divider>PPT配置</el-divider>
      
      <el-form-item label="每页停留时间">
        <el-input-number v-model="form.pptInfo.singlePageSecond" :min="1" :max="30" :step="1"></el-input-number> 秒
      </el-form-item>
      
      <el-form-item label="读取PPT备注">
        <el-switch v-model="form.pptInfo.getText"></el-switch>
        <span class="help-text ml-10">开启后，将优先使用PPT备注作为语音文本</span>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="generateRequestData">生成请求参数</el-button>
        <el-button type="success" @click="submitForm" :disabled="!requestReady">发送请求</el-button>
        <el-button @click="resetForm">重置</el-button>
        <el-button type="info" @click="testApiConnection">测试API连接</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 请求参数展示区 -->
    <div v-if="requestReady" class="request-preview">
      <h3>请求参数预览</h3>
      <p>请确认以下参数无误后点击"发送请求"按钮</p>
      
      <el-tabs type="border-card">
        <el-tab-pane label="请求头">
          <el-card shadow="never" class="request-card">
            <pre>{{ JSON.stringify(requestHeaders, null, 2) }}</pre>
          </el-card>
        </el-tab-pane>
        <el-tab-pane label="请求体">
          <el-card shadow="never" class="request-card">
            <pre>{{ JSON.stringify(requestData, null, 2) }}</pre>
          </el-card>
        </el-tab-pane>
        <el-tab-pane label="请求URL">
          <el-card shadow="never" class="request-card">
            <div>{{ requestUrl }}</div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <div v-if="resultInfo.taskId" class="result-container">
      <h3>任务信息</h3>
      <p>任务ID: {{ resultInfo.taskId }}</p>
      <p>状态: {{ resultInfo.status }}</p>
      <el-button type="primary" @click="checkTaskStatus" :disabled="resultInfo.status === '已完成'">
        刷新状态
      </el-button>
      
      <div v-if="resultInfo.videoUrl" class="video-container">
        <h3>生成视频</h3>
        <video :src="resultInfo.videoUrl" controls width="100%"></video>
        <p>
          <el-button type="success" @click="downloadVideo">下载视频</el-button>
        </p>
      </div>
    </div>
    
    <!-- 请求参数和结果展示区 -->
    <el-collapse v-model="activeNames" class="debug-panel">
      <el-collapse-item title="请求参数" name="1">
        <pre>{{ JSON.stringify(requestData, null, 2) }}</pre>
      </el-collapse-item>
      <el-collapse-item title="返回结果" name="2" v-if="apiResponse">
        <pre>{{ JSON.stringify(apiResponse, null, 2) }}</pre>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
import axios from 'axios';
import { 
  Document, 
  Plus, 
  CopyDocument, 
  QuestionFilled 
} from '@element-plus/icons-vue';
import { createPptVideoTask, getTaskStatus, testApiConnection } from './xibao-api';

// 添加导入常量
import xibaoApi from './xibao-api';

export default {
  name: 'DhDemo',
  components: {
    Document,
    Plus,
    CopyDocument,
    QuestionFilled
  },
  data() {
    const defaultParams = {
      right: {
        width: 344,
        height: 1080,
        x: 1517,
        y: 309,
        postureId: 'aMiAX96rMqNS'
      },
      left: {
        width: 319,
        height: 1536,
        x: -53,
        y: 346,
        postureId: 'd5nJE6EI0txK'
      },
      caption: {
        fontSize: 44,
        y: 1000,
        fontColor: "#ff3c3c",
        bold: true
      }
    };
    
    // 预先创建场景数据
    const rightScene = {
      virtualHumanId: 'VHP3S1EF7',
      virtualHumanPostureId: defaultParams.right.postureId,
      voiceId: '101-master-ugdr',
      attributes: {
        width: defaultParams.right.width,
        height: defaultParams.right.height,
        x: defaultParams.right.x,
        y: defaultParams.right.y,
        forceMattingType: 0
      },
      voiceText: "PPT中设置了取备注文本，此字段无效，字幕坐标不传时默认居中",
      enableCaption: true,
      captionPosition: 'topCenter',
      caption: {
        topRight: false,
        topLeft: false,
        topCenter: true,
        zIndex: 60,
        attributes: {
          visible: true,
          fontColor: defaultParams.caption.fontColor,
          spacing: 1,
          italic: false,
          underline: false,
          bold: defaultParams.caption.bold,
          y: defaultParams.caption.y,
          fontSize: defaultParams.caption.fontSize
        }
      },
      backgroundImage: {
        mediaUrl: "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/e07aea3c-d5f6-4de9-b086-d18610bcf5b0.jpg"
      }
    };
    
    const leftScene = {
      virtualHumanId: 'VHP3S1EF7',
      virtualHumanPostureId: defaultParams.left.postureId,
      voiceId: '101-master-ugdr',
      attributes: {
        width: defaultParams.left.width,
        height: defaultParams.left.height,
        x: defaultParams.left.x,
        y: defaultParams.left.y,
        forceMattingType: 0
      },
      voiceText: "PPT中设置了取备注文本，即使本页PPT没有备注，也不会去这个字段哦",
      enableCaption: true,
      captionPosition: 'topCenter',
      caption: {
        topRight: false,
        topLeft: false,
        topCenter: true,
        zIndex: 60,
        attributes: {
          visible: true,
          fontColor: defaultParams.caption.fontColor,
          spacing: 1,
          italic: false,
          underline: false,
          bold: defaultParams.caption.bold,
          y: defaultParams.caption.y,
          fontSize: defaultParams.caption.fontSize
        }
      },
      backgroundImage: {
        mediaUrl: "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/e07aea3c-d5f6-4de9-b086-d18610bcf5b0.jpg"
      }
    };
    
    const thirdScene = {
      virtualHumanId: 'VHP3S1EF7',
      virtualHumanPostureId: defaultParams.right.postureId,
      voiceId: '101-master-ugdr',
      attributes: {
        width: defaultParams.right.width,
        height: defaultParams.right.height,
        x: 1500, // 稍微调整位置与默认不同
        y: defaultParams.right.y,
        forceMattingType: 0
      },
      voiceText: "场景数量少于PPT页数时，后面几页中的场景参数都取最后这个场景的哦",
      enableCaption: true,
      captionPosition: 'topCenter',
      caption: {
        topRight: false,
        topLeft: false,
        topCenter: true,
        zIndex: 60,
        attributes: {
          visible: true,
          fontColor: defaultParams.caption.fontColor,
          spacing: 1,
          italic: false,
          underline: false,
          bold: defaultParams.caption.bold,
          y: defaultParams.caption.y,
          fontSize: defaultParams.caption.fontSize
        }
      },
      backgroundImage: {
        mediaUrl: "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/e07aea3c-d5f6-4de9-b086-d18610bcf5b0.jpg"
      }
    };
    
    return {
      // 表单数据
      form: {
        outputVideoName: 'PPT讲解视频测试',
        width: 1920,
        height: 1080,
        pptUrl: '',
        pptFileName: '',
        // 初始只有1个场景，上传PPT后会根据页数动态生成
        scenes: [
          rightScene
        ],
        enableBgm: true,
        bgm: {
          mediaUrl: "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/1a1789ea-25bf-437b-acd2-fdc08a265087.MP3",
          volume: 0.3,
          speed: 1,
          loop: true
        },
        pptInfo: {
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
      },
      // 当前活动场景选项卡
      activeScene: "0",
      // 请求数据
      requestData: null,
      // 是否已生成请求参数
      requestReady: false,
      // API响应
      apiResponse: null,
      // 任务结果信息
      resultInfo: {
        taskId: '',
        status: '',
        videoUrl: ''
      },
      // 折叠面板激活项
      activeNames: [],
      // API密钥
      subKey: '282cd94b697e48e6aca6d20bbdaf0d0f',
      // 轮询间隔(毫秒)
      pollInterval: 5000,
      // 轮询定时器
      pollTimer: null,
      // 默认参数
      defaultParams: defaultParams,
      // 请求相关
      requestHeaders: null,
      requestUrl: '',
    };
  },
  created() {
    // 在控制台输出检查是否正确初始化
    console.log('创建组件时场景数据:', JSON.stringify(this.form.scenes));
  },
  mounted() {
    // 在挂载后再次检查场景数据
    console.log('挂载组件后场景数据:', JSON.stringify(this.form.scenes));
  },
  methods: {
    // 创建默认场景配置
    createDefaultScene(position = 'right') {
      const params = this.defaultParams[position];
      
      // 设定不同场景的默认文本
      let defaultText = "PPT中设置了取备注文本，此字段无效，字幕坐标不传时默认居中";
      if (position === 'left') {
        defaultText = "PPT中设置了取备注文本，即使本页PPT没有备注，也不会去这个字段哦";
      }
      
      return {
        virtualHumanId: 'VHP3S1EF7',
        virtualHumanPostureId: params.postureId,
        voiceId: '101-master-ugdr',
        attributes: {
          width: params.width,
          height: params.height,
          x: params.x,
          y: params.y,
          forceMattingType: 0
        },
        voiceText: defaultText,
        enableCaption: true,
        captionPosition: 'topCenter',
        caption: {
          topRight: false,
          topLeft: false,
          topCenter: true,
          zIndex: 60,
          attributes: {
            visible: true,
            fontColor: this.defaultParams.caption.fontColor,
            spacing: 1,
            italic: false,
            underline: false,
            bold: this.defaultParams.caption.bold,
            y: this.defaultParams.caption.y,
            fontSize: this.defaultParams.caption.fontSize
          }
        },
        backgroundImage: {
          mediaUrl: "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/e07aea3c-d5f6-4de9-b086-d18610bcf5b0.jpg"
        }
      };
    },
    
    // 添加新场景
    addScene() {
      const position = this.form.scenes.length % 2 === 0 ? 'right' : 'left';
      this.form.scenes.push(this.createDefaultScene(position));
      this.$nextTick(() => {
        this.activeScene = (this.form.scenes.length - 1).toString();
      });
    },
    
    // 复制最后一个场景
    copyLastScene() {
      if (this.form.scenes.length > 0) {
        const lastScene = this.form.scenes[this.form.scenes.length - 1];
        const newScene = JSON.parse(JSON.stringify(lastScene)); // 深拷贝
        this.form.scenes.push(newScene);
        this.$nextTick(() => {
          this.activeScene = (this.form.scenes.length - 1).toString();
        });
      }
    },
    
    // 移除场景
    removeScene(name) {
      const index = parseInt(name);
      if (index >= 0 && index < this.form.scenes.length) {
        this.form.scenes.splice(index, 1);
        
        // 重新设置活动选项卡
        if (this.form.scenes.length > 0) {
          const newIndex = Math.min(index, this.form.scenes.length - 1);
          this.activeScene = newIndex.toString();
        }
      }
    },
    
    // 处理选项卡点击
    handleTabClick(tab) {
      this.activeScene = tab.props.name;
    },
    
    // 更新场景数据
    updateScene(index) {
      // 确保数据更新
      const scene = this.form.scenes[index];
      
      // 确保所有值都是数值类型 - 主要针对从input组件获取的字符串值
      if (scene.attributes) {
        scene.attributes.width = Number(scene.attributes.width) || this.defaultParams.right.width;
        scene.attributes.height = Number(scene.attributes.height) || this.defaultParams.right.height;
        scene.attributes.x = Number(scene.attributes.x) || this.defaultParams.right.x;
        scene.attributes.y = Number(scene.attributes.y) || this.defaultParams.right.y;
      }
      
      // 处理字幕属性
      if (scene.caption && scene.caption.attributes) {
        scene.caption.attributes.fontSize = Number(scene.caption.attributes.fontSize) || this.defaultParams.caption.fontSize;
        scene.caption.attributes.y = Number(scene.caption.attributes.y) || this.defaultParams.caption.y;
      }
      
      // 强制Vue更新DOM - 使用直接赋值方式
      this.$nextTick(() => {
        if (scene.attributes) {
          // 在Vue 3中，直接赋值即可
          scene.attributes = {...scene.attributes};
        }
        
        if (scene.caption && scene.caption.attributes) {
          // 在Vue 3中，直接赋值即可
          scene.caption.attributes = {...scene.caption.attributes};
        }
        
        // 输出日志，方便调试
        console.log(`更新场景 ${index}:`, JSON.stringify(scene));
      });
    },
    
    // 切换字幕显示
    toggleCaption(index) {
      const scene = this.form.scenes[index];
      
      if (!scene.enableCaption) {
        // 如果关闭字幕，将caption设为null
        scene.caption = null;
      } else {
        // 使用默认字幕配置 - 使用Vue的响应式方法设置属性
        const caption = {
          topRight: false,
          topLeft: false,
          topCenter: true,
          zIndex: 60,
          attributes: {
            visible: true,
            fontColor: this.defaultParams.caption.fontColor,
            spacing: 1,
            italic: false,
            underline: false,
            bold: this.defaultParams.caption.bold,
            y: this.defaultParams.caption.y,
            fontSize: this.defaultParams.caption.fontSize
          }
        };
        
        scene.caption = caption;
        scene.captionPosition = 'topCenter';
        
        console.log(`启用场景 ${index} 的字幕:`, JSON.stringify(scene.caption));
      }
    },
    
    // 更新字幕位置
    updateCaptionPosition(index) {
      const scene = this.form.scenes[index];
      if (!scene.caption) {
        return;
      }
      
      // 重置所有位置
      scene.caption.topLeft = false;
      scene.caption.topCenter = false;
      scene.caption.topRight = false;
      
      // 设置选中的位置
      scene.caption[scene.captionPosition] = true;
      
      console.log(`更新场景 ${index} 字幕位置: ${scene.captionPosition}`);
    },
    
    // 设置默认背景音乐URL
    setBgmDefaultUrl() {
      this.form.bgm.mediaUrl = "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/1a1789ea-25bf-437b-acd2-fdc08a265087.MP3";
    },
    
    // 文件上传前处理
    beforeUpload(file) {
      const isPPT = file.type === 'application/vnd.ms-powerpoint' || 
                    file.type === 'application/vnd.openxmlformats-officedocument.presentationml.presentation';
      if (!isPPT) {
        this.$message.error('只能上传PPT或PPTX文件!');
        return false;
      }
      
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        this.$message.error('文件大小不能超过10MB!');
        return false;
      }
      
      this.$message.info('正在上传文件到OSS...');
      return true;
    },
    
    // 文件上传成功
    async handleUploadSuccess(response) {
      if (response && response.url) {
        this.form.pptUrl = response.url;
        this.form.pptFileName = response.filename;
        this.$message.success('文件上传成功!');
        
        // 上传成功后获取PPT页数并生成场景
        try {
          // 显示加载提示
          this.$message.info('正在分析PPT页数...');
          
          // 调用后端API获取PPT页数
          const pptInfoResponse = await axios.post('/api/v1/aibeings/ppt/info', {
            pptUrl: response.url
          }, {
            headers: {
              'Content-Type': 'application/json'
            },
            timeout: 30000 // 30秒超时
          });
          
          console.log('PPT信息获取结果:', pptInfoResponse);
          
          if (pptInfoResponse.data && pptInfoResponse.data.pageCount) {
            const pageCount = pptInfoResponse.data.pageCount;
            this.$message.info(`检测到PPT有${pageCount}页，正在生成对应场景...`);
            this.generateScenesFromPPT(pageCount);
          } else {
            console.warn('获取PPT页数失败，页数信息为空', pptInfoResponse.data);
            // 临时用模拟页数代替
            const defaultPageCount = 4; // 默认生成4页
            this.$message.warning(`无法自动检测PPT页数，使用默认${defaultPageCount}页创建场景`);
            this.generateScenesFromPPT(defaultPageCount);
          }
        } catch (error) {
          console.error('获取PPT信息失败:', error.response || error);
          // 临时用模拟页数代替
          const defaultPageCount = 4; // 默认生成4页
          this.$message.warning(`获取PPT页数失败，使用默认${defaultPageCount}页创建场景`);
          this.generateScenesFromPPT(defaultPageCount);
        }
      } else {
        this.$message.error('文件上传成功，但未获取到URL');
      }
    },
    
    // 根据PPT页数生成场景
    generateScenesFromPPT(pageCount) {
      // 保存第一个场景作为模板
      const templateScene = JSON.parse(JSON.stringify(this.form.scenes[0]));
      
      // 清空现有场景并添加第一个场景
      this.form.scenes = [templateScene];
      
      // 根据页数添加场景（页数-1，因为已经有1个场景了）
      for (let i = 1; i < pageCount; i++) {
        // 深拷贝模板场景并添加到列表
        const newScene = JSON.parse(JSON.stringify(templateScene));
        
        // 可以根据奇偶性交替左右姿势
        if (i % 2 === 1) {
          newScene.virtualHumanPostureId = this.defaultParams.left.postureId;
          // 更新相关位置属性
          newScene.attributes.width = this.defaultParams.left.width;
          newScene.attributes.height = this.defaultParams.left.height;
          newScene.attributes.x = this.defaultParams.left.x;
          newScene.attributes.y = this.defaultParams.left.y;
        }
        
        // 添加到场景列表
        this.form.scenes.push(newScene);
      }
      
      this.$message.success(`已根据PPT页数生成${pageCount}个场景`);
      console.log(`已生成${pageCount}个场景:`, JSON.stringify(this.form.scenes));
    },
    
    // 文件上传失败
    handleUploadError(error) {
      console.error('文件上传失败:', error);
      this.$message.error('文件上传失败，请重试');
    },
    
    // 生成请求数据
    generateRequestData() {
      if (!this.form.pptUrl) {
        this.$message.error('请先上传PPT文件');
        return;
      }
      
      // 准备场景数据
      const scenes = this.form.scenes.map(scene => {
        // 构建场景对象
        const sceneObj = {
          virtualHuman: {
            attributes: {
              width: scene.attributes.width,
              height: scene.attributes.height,
              x: scene.attributes.x,
              y: scene.attributes.y,
              forceMattingType: 0
            },
            virtualHumanId: scene.virtualHumanId,
            virtualHumanPostureId: scene.virtualHumanPostureId,
            zIndex: 20
          },
          tts: {
            voiceId: scene.voiceId,
            rate: 1,
            pitch: 1,
            volume: 50
          },
          voiceText: scene.voiceText,
          backgroundImage: scene.backgroundImage
        };
        
        // 如果启用了字幕，添加字幕配置
        if (scene.enableCaption && scene.caption) {
          sceneObj.caption = scene.caption;
        }
        
        return sceneObj;
      });
      
      // 构建完整请求数据
      const requestObj = {
        outputVideoName: this.form.outputVideoName,
        width: this.form.width,
        height: this.form.height,
        creationDetail: {
          scenes: scenes
        },
        pptInfo: {
          pptUrl: this.form.pptUrl,
          convertType: this.form.pptInfo.convertType,
          getText: this.form.pptInfo.getText,
          singlePageSecond: this.form.pptInfo.singlePageSecond,
          attributes: this.form.pptInfo.attributes
        }
      };
      
      // 如果启用背景音乐，添加背景音乐配置
      if (this.form.enableBgm) {
        requestObj.creationDetail.backgroundMusic = this.form.bgm;
      }
      
      this.requestData = requestObj;
      
      // 从导入的xibaoApi中获取常量
      this.requestHeaders = xibaoApi.AUTH_HEADER;
      this.requestUrl = 'https://openapi.xiaoice.com/vh/openapi/video/task/v2/ppt/submit';
      
      this.requestReady = true;
    },
    
    // 提交表单
    async submitForm() {
      if (!this.requestReady) {
        this.$message.error('请先生成请求参数');
        return;
      }
      
      try {
        this.$message.info('正在发送请求...');
        
        // 记录请求开始时间
        const startTime = Date.now();
        console.log('开始提交任务时间:', new Date(startTime).toLocaleTimeString());
        
        // 添加加载效果
        const loading = this.$loading({
          lock: true,
          text: '正在提交任务，可能需要较长时间...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        
        try {
          // 使用封装的API函数发送请求
          const response = await createPptVideoTask(this.requestData);
          
          // 记录请求结束时间
          const endTime = Date.now();
          console.log('请求完成时间:', new Date(endTime).toLocaleTimeString());
          console.log('请求耗时:', (endTime - startTime) / 1000, '秒');
          
          this.apiResponse = response;
          
          // 关闭加载
          loading.close();
          
          if (response && response.data) {
            this.$message.success('任务已提交，正在处理中...');
            this.resultInfo.taskId = response.data; // 根据返回示例，任务ID在data字段中
            this.resultInfo.status = '处理中';
            
            // 开始轮询任务状态
            this.startPolling();
          } else {
            this.$message.error('创建任务失败: 未获取到有效的任务ID');
            console.error('API响应无效:', response);
          }
        } catch (error) {
          // 关闭加载
          loading.close();
          
          console.error('任务提交失败:', error);
          
          // 详细错误处理
          if (error.response) {
            // 服务器返回了错误状态码
            console.error('服务器错误状态:', error.response.status);
            console.error('服务器错误信息:', error.response.data);
            this.apiResponse = error.response.data;
            this.$message.error(`提交失败 (${error.response.status}): ${error.response.data?.message || '服务器返回错误'}`);
          } else if (error.message === 'Network Error') {
            // 网络错误处理
            this.apiResponse = { error: 'Network Error', details: '网络连接失败，可能原因：代理配置问题、目标服务器不可达、CORS限制、请求数据过大' };
            this.$message.error('网络错误: 无法连接到API服务器。请检查网络连接和代理配置。');
            
            // 显示网络错误诊断提示
            this.$confirm('网络错误可能有以下原因:<br>1. 代理服务器配置问题<br>2. 网络连接不稳定<br>3. 数据包过大<br>4. API服务器暂时不可用<br><br>是否查看请求数据进行排查?', '连接诊断', {
              confirmButtonText: '查看请求数据',
              cancelButtonText: '取消',
              type: 'warning',
              dangerouslyUseHTMLString: true
            }).then(() => {
              this.activeNames = ['1']; // 展开请求参数面板
              console.log('请求数据大小:', JSON.stringify(this.requestData).length, '字节');
              
              // 检查请求数据大小
              if (JSON.stringify(this.requestData).length > 5000000) {
                this.$message.warning('请求数据过大，可能导致网络超时。请考虑减小数据量或分批提交。');
              }
            }).catch(() => {});
          } else {
            // 其他错误
            this.apiResponse = { error: error.message };
            this.$message.error(`提交失败: ${error.message}`);
          }
        }
      } catch (outerError) {
        console.error('提交过程发生意外错误:', outerError);
        this.$message.error('提交过程发生意外错误，请查看控制台日志');
      }
    },
    
    // 重置表单
    resetForm() {
      const rightScene = this.createDefaultScene('right');
      
      this.form = {
        outputVideoName: 'PPT讲解视频测试',
        width: 1920,
        height: 1080,
        pptUrl: '',
        pptFileName: '',
        scenes: [rightScene], // 只保留一个默认场景
        enableBgm: true,
        bgm: {
          mediaUrl: "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/1a1789ea-25bf-437b-acd2-fdc08a265087.MP3",
          volume: 0.3,
          speed: 1,
          loop: true
        },
        pptInfo: {
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
      
      this.activeScene = "0";
      this.requestData = null;
      this.requestReady = false;
      this.apiResponse = null;
      
      // 停止轮询
      if (this.pollTimer) {
        clearInterval(this.pollTimer);
        this.pollTimer = null;
      }
      
      this.resultInfo = {
        taskId: '',
        status: '',
        videoUrl: ''
      };
      
      // 打印重置后的场景数据以便调试
      console.log('重置后的场景数据:', JSON.stringify(this.form.scenes));
    },
    
    // 开始轮询任务状态
    startPolling() {
      if (this.pollTimer) {
        clearInterval(this.pollTimer);
      }
      
      this.pollTimer = setInterval(() => {
        this.checkTaskStatus();
      }, this.pollInterval);
    },
    
    // 检查任务状态
    async checkTaskStatus() {
      if (!this.resultInfo.taskId) return;
      
      try {
        // 使用封装的API函数查询状态
        const response = await getTaskStatus(this.resultInfo.taskId);
        
        this.apiResponse = response;
        
        if (response && response.data) {
          // 更新状态
          this.resultInfo.status = response.data.status || '处理中';
          
          // 如果已完成，获取下载链接
          if (response.data.status === 'FINISHED' && response.data.resultUrl) {
            this.resultInfo.status = '已完成';
            this.resultInfo.videoUrl = response.data.resultUrl;
            
            // 停止轮询
            if (this.pollTimer) {
              clearInterval(this.pollTimer);
              this.pollTimer = null;
            }
            
            this.$message.success('视频生成完成!');
          } else if (response.data.status === 'FAILED') {
            this.resultInfo.status = '失败';
            
            // 停止轮询
            if (this.pollTimer) {
              clearInterval(this.pollTimer);
              this.pollTimer = null;
            }
            
            this.$message.error('视频生成失败!');
          }
        }
      } catch (error) {
        console.error('获取任务状态失败:', error);
        this.$message.error(`获取任务状态失败: ${error.message}`);
      }
    },
    
    // 下载视频
    downloadVideo() {
      if (this.resultInfo.videoUrl) {
        const a = document.createElement('a');
        a.href = this.resultInfo.videoUrl;
        a.download = `${this.form.outputVideoName}.mp4`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
    },
    getPositionType(scene) {
      if (scene.virtualHumanPostureId === 'aMiAX96rMqNS') {
        return 'right'; // 右侧站立姿势
      } else if (scene.virtualHumanPostureId === 'd5nJE6EI0txK') {
        return 'left'; // 左侧站立姿势
      } else {
        // 默认值
        return 'right';
      }
    },
    // 当姿势改变时自动更新位置
    handlePostureChange(index) {
      const scene = this.form.scenes[index];
      const positionType = this.getPositionType(scene);
      const params = this.defaultParams[positionType];
      
      // 更新位置属性 - 确保使用数值类型
      if (scene.attributes) {
        // 先提取值，确保是数值类型
        const newWidth = Number(params.width);
        const newHeight = Number(params.height);
        const newX = Number(params.x);
        const newY = Number(params.y);
        
        // 直接赋值
        scene.attributes.width = newWidth;
        scene.attributes.height = newHeight;
        scene.attributes.x = newX;
        scene.attributes.y = newY;
        
        // 确保Vue检测到变化
        this.$nextTick(() => {
          console.log(`姿势变更，更新位置 ${index}:`, JSON.stringify(scene.attributes));
          
          // 使用直接赋值强制更新
          scene.attributes = {
            ...scene.attributes,
            width: newWidth,
            height: newHeight,
            x: newX,
            y: newY
          };
        });
      }
    },
    // 更新维度值
    updateDimensionValue(index, dimension, value) {
      const scene = this.form.scenes[index];
      if (scene.attributes) {
        scene.attributes[dimension] = Number(value) || 0;
        this.updateScene(index);
      }
    },
    // 更新字幕值
    updateCaptionValue(index, attribute, value) {
      const scene = this.form.scenes[index];
      if (scene.caption && scene.caption.attributes) {
        scene.caption.attributes[attribute] = Number(value) || 0;
        this.updateScene(index);
      }
    },
    // 测试API连接
    async testApiConnection() {
      try {
        this.$message.info('正在测试与小冰API的连接...');
        const result = await testApiConnection();
        console.log('API连接测试结果:', result);
        this.$message.success(`API连接测试完成! 状态码: ${result.status}`);
      } catch (error) {
        console.error('API连接测试失败:', error);
        this.$message.error(`API连接测试失败: ${error.message}`);
      }
    },
  },
  beforeUnmount() {
    // 组件销毁前清除定时器
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
  }
};
</script>

<style scoped>
.dh-demo-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #303133;
}

.form-container {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.uploaded-file-info {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #f0f9eb;
  border-radius: 4px;
  border-left: 3px solid #67c23a;
}

.file-url {
  font-size: 12px;
  color: #909399;
  word-break: break-all;
}

.scenes-container {
  margin: 20px 0;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 4px;
}

.scene-tabs {
  margin-bottom: 20px;
}

.scene-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.position-container {
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
}

.help-text {
  font-size: 12px;
  color: #909399;
  margin-left: 10px;
}

.ml-10 {
  margin-left: 10px;
}

.default-value-hint {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  padding: 2px 5px;
  background-color: #f5f7fa;
  border-radius: 2px;
  border-left: 2px solid #e6a23c;
}

.request-preview {
  margin-top: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f0f6ff;
  border-radius: 4px;
}

.request-card {
  margin-top: 15px;
}

.result-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f0f9eb;
  border-radius: 4px;
}

.video-container {
  margin-top: 20px;
}

.debug-panel {
  margin-top: 30px;
}

pre {
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

.mb-2 {
  margin-bottom: 8px;
}
</style> 