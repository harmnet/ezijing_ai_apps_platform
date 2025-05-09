import { ref } from 'vue';

export default function useDigitalHumanData() {
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
      height: 960
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
    },
    // 以下是不可选择的模板
    { 
      id: 'non-selectable-1', 
      name: '模板5 (即将推出)', 
      ratio: '9:16', 
      isVertical: true,
      previewImage: '/images/templates/image (4)_a9ef435.png',
      disabled: true 
    },
    { 
      id: 'non-selectable-2', 
      name: '模板6 (即将推出)', 
      ratio: '9:16', 
      isVertical: true,
      previewImage: '/images/templates/image (5)_4f18cab.png',
      disabled: true 
    },
    { 
      id: 'non-selectable-3', 
      name: '模板7 (即将推出)', 
      ratio: '16:9', 
      isVertical: false,
      previewImage: '/images/templates/5_5708421.png',
      disabled: true 
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
  const isUploading = ref(false);
  const taskResult = ref(null);
  const taskStatus = ref(null);
  const errorMessage = ref('');
  const autoQueryInterval = ref(null);
  const audioPlayer = ref(null);
  const videoPlayer = ref(null);
  const fileInput = ref(null);
  const logoFileInput = ref(null);
  const openingVideoInput = ref(null);
  const endingVideoInput = ref(null);
  const isUploadingOpening = ref(false);
  const isUploadingEnding = ref(false);
  const bgmFileInput = ref(null);
  const isUploadingBgm = ref(false);
  
  // 分辨率选项
  const resolutionOptions = ref([
    { label: '720p (1280x720)', value: '1280x720' },
    { label: '1080p (1920x1080)', value: '1920x1080' },
    { label: '竖屏 (720x1280)', value: '720x1280' },
    { label: '竖屏 (1080x1920)', value: '1080x1920' }
  ]);

  // 添加数字人预览相关的状态
  const showDigitalHumanPreview = ref(false);
  const previewDigitalHuman = ref(null);
  
  // 添加展开/收起文字的状态
  const textExpanded = ref(false);

  // 数字人翻页相关数据
  const currentHumanPage = ref(0);
  const humansPerPage = ref(4);
  const displayedHumans = ref([]);

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
    taskResult,
    taskStatus,
    errorMessage,
    audioPlayer,
    videoPlayer,
    fileInput,
    templateOptions,
    logoFileInput,
    openingVideoInput,
    endingVideoInput,
    isUploadingOpening,
    isUploadingEnding,
    bgmFileInput,
    isUploadingBgm,
    resolutionOptions,
    showDigitalHumanPreview,
    previewDigitalHuman,
    textExpanded,
    autoQueryInterval,
    currentHumanPage,
    humansPerPage,
    displayedHumans
  };
} 