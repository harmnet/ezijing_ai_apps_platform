import { watch, computed, onMounted } from 'vue';
import digitalHumanAPI from '../utils/digitalHumanAPI';

export default function useDigitalHumanLogic(data) {
  // 解构出所需状态
  const {
    currentStep,
    formData,
    digitalHumans,
    femaleVoices,
    maleVoices,
    activeVoices,
    taskResult,
    taskStatus,
    audioPlayer,
    autoQueryInterval,
    currentHumanPage,
    humansPerPage,
    displayedHumans,
    showDigitalHumanPreview,
    previewDigitalHuman
  } = data;

  // 将计算属性改为方法
  const getSelectedHumanGender = () => {
    const selectedHuman = digitalHumans.value.find(h => h.id === formData.value.figureId);
    return selectedHuman?.gender === 'female' ? '女' : '男';
  };
  
  // 初始化音色选项
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
    
    // 初始化数字人分页
    updateDisplayedHumans();
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
  
  // 获取语音预览URL
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
    const template = data.templateOptions.value.find(t => t.id === templateId);
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
    
    data.isSubmitting.value = true;
    
    const params = {
      figureId: formData.value.figureId,
      templateId: formData.value.templateId,
      text: formData.value.text,
      driveType: "TEXT",
      ttsParams: { 
        person: formData.value.ttsParams.person,
        speed: Number(formData.value.ttsParams.speed),
        volume: Number(formData.value.ttsParams.volume),
        pitch: Number(formData.value.ttsParams.pitch)
      },
      videoParams: {
        width: Number(formData.value.videoParams.width),
        height: Number(formData.value.videoParams.height)
      }
    };
    
    // 添加标题参数（如果有）
    if (formData.value.title) {
      params.title = formData.value.title;
    }
    
    // 注：根据新需求，移除了subtitleParams参数
    
    // 处理Logo参数，只需要logoUrl
    if (formData.value.logoParams.logoUrl || formData.value.logoParams.imageUrl) {
      params.logoParams = {
        logoUrl: formData.value.logoParams.logoUrl || formData.value.logoParams.imageUrl
      };
    }
    
    // 注意：片头视频、片尾视频和背景音乐功能已禁用，不提交这些参数
    // 即使表单中可能存在这些值，也不会添加到请求参数中
    
    // 添加背景图片参数（如果有）
    if (formData.value.backgroundImageUrl) {
      params.materialUrl = formData.value.materialUrl || formData.value.backgroundImageUrl;
    }
    
    console.log('=== 提交任务参数 ===');
    console.log(JSON.stringify(params, null, 2));
    console.log('=== 确认参数中包含driveType ===');
    console.log('driveType:', params.driveType);
    console.log('=== formData 内容 ===');
    console.log('figureId:', formData.value.figureId);
    console.log('templateId:', formData.value.templateId);
    console.log('text长度:', formData.value.text.length);
    console.log('ttsParams:', JSON.stringify(formData.value.ttsParams));
    console.log('backgroundImageUrl:', formData.value.backgroundImageUrl);
    console.log('materialUrl:', formData.value.materialUrl);
    
    try {
      console.log('开始调用API...');
      const response = await digitalHumanAPI.submitVideoTask(params);
      console.log('API返回结果:', response);
      
      if (response.data.success) {
        taskResult.value = response.data.data;
        console.log('任务提交成功:', taskResult.value);
        
        startAutoQuery();
        currentStep.value = 6;
      } else {
        data.errorMessage.value = response.data.message || '任务提交失败';
        console.error('任务提交失败，错误信息:', data.errorMessage.value);
        console.error('返回的完整数据:', response.data);
        alert(data.errorMessage.value);
      }
    } catch (error) {
      console.error('提交任务出错:', error);
      console.error('错误详情:', error.response ? error.response.data : error.message);
      data.errorMessage.value = error.response?.data?.message || '网络错误，请稍后重试';
      alert(data.errorMessage.value);
    } finally {
      data.isSubmitting.value = false;
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
      data.isQuerying.value = true;
    }
    
    try {
      const response = await digitalHumanAPI.queryVideoTask(taskResult.value.taskId);
      
      if (response.data.success) {
        taskStatus.value = response.data.data;
        console.log('任务状态:', taskStatus.value);
      } else {
        data.errorMessage.value = response.data.message || '查询任务失败';
        if (showLoading) {
          alert(data.errorMessage.value);
        } else {
          console.error(data.errorMessage.value);
        }
      }
    } catch (error) {
      console.error('查询任务出错:', error);
      data.errorMessage.value = error.response?.data?.message || '网络错误，请稍后重试';
      if (showLoading) {
        alert(data.errorMessage.value);
      } else {
        console.error(data.errorMessage.value);
      }
    } finally {
      if (showLoading) {
        data.isQuerying.value = false;
      }
    }
  };
  
  const resetForm = () => {
    formData.value = {
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
    const found = data.resolutionOptions.value.find(option => option.value === resolution);
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
  
  // 添加模板选择方法
  const selectTemplate = (templateId) => {
    formData.value.templateId = templateId;
    
    // 根据选择的模板调整视频分辨率
    const selectedTemplate = data.templateOptions.value.find(t => t.id === templateId);
    if (selectedTemplate) {
      if (selectedTemplate.ratio === '9:16' || selectedTemplate.isVertical) {
        // 如果是竖屏模板(9:16)，默认设置为竖屏分辨率
        formData.value.videoParams.width = 1080;
        formData.value.videoParams.height = 1920;
      } else if (selectedTemplate.ratio === '16:9' || !selectedTemplate.isVertical) {
        // 如果是横屏模板(16:9)，默认设置为横屏分辨率
        formData.value.videoParams.width = 1920;
        formData.value.videoParams.height = 1080;
      } else if (selectedTemplate.ratio === '1:1') {
        // 如果是方形模板(1:1)，默认设置为正方形分辨率
        formData.value.videoParams.width = 1080;
        formData.value.videoParams.height = 1080;
      } else {
        // 其他比例模板，默认设置为竖屏分辨率
        formData.value.videoParams.width = 1080;
        formData.value.videoParams.height = 1920;
      }
    }
  };
  
  // 添加展开/收起文字的方法
  const toggleTextExpand = () => {
    data.textExpanded.value = !data.textExpanded.value;
  };

  // 获取选中数字人的头像
  const getSelectedHumanAvatar = () => {
    const selectedHuman = digitalHumans.value.find(h => h.id === formData.value.figureId);
    return selectedHuman ? selectedHuman.avatar : '';
  };

  // 获取选中模板的预览图
  const getSelectedTemplatePreview = () => {
    const selectedTemplate = data.templateOptions.value.find(t => t.id === formData.value.templateId);
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
  
  // 显示数字人演示视频的方法
  const previewDigitalHumanVideo = (human) => {
    if (human && human.demoVideo) {
      data.previewDigitalHuman.value = human;
      data.showDigitalHumanPreview.value = true;
    } else {
      console.error('无法预览数字人视频，未找到演示视频链接');
    }
  };
  
  // 关闭数字人预览弹窗
  const closeDigitalHumanPreview = () => {
    data.showDigitalHumanPreview.value = false;
    data.previewDigitalHuman.value = null;
  };
  
  // 更新显示的数字人列表
  const updateDisplayedHumans = () => {
    const start = currentHumanPage.value * humansPerPage.value;
    const end = start + humansPerPage.value;
    data.displayedHumans.value = digitalHumans.value.slice(start, end);
  };
  
  // 前往上一页数字人
  const prevHumanPage = () => {
    if (currentHumanPage.value > 0) {
      currentHumanPage.value--;
      updateDisplayedHumans();
    }
  };
  
  // 前往下一页数字人
  const nextHumanPage = () => {
    const maxPage = Math.ceil(digitalHumans.value.length / humansPerPage.value) - 1;
    if (currentHumanPage.value < maxPage) {
      currentHumanPage.value++;
      updateDisplayedHumans();
    }
  };
  
  // 设置指定页码
  const setHumanPage = (page) => {
    const maxPage = Math.ceil(digitalHumans.value.length / humansPerPage.value) - 1;
    if (page >= 0 && page <= maxPage) {
      currentHumanPage.value = page;
      updateDisplayedHumans();
    }
  };
  
  // 计算总页数
  const totalHumanPages = computed(() => {
    return Math.ceil(digitalHumans.value.length / humansPerPage.value);
  });

  return {
    getSelectedHumanGender,
    initVoices,
    nextStep,
    prevStep,
    selectDigitalHuman,
    selectVoice,
    getVoicePreviewUrl,
    trimTitle,
    previewVoice,
    getHumanName,
    getTemplateName,
    getVoiceName,
    submitTask,
    startAutoQuery,
    stopAutoQuery,
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
    selectTemplate,
    toggleTextExpand,
    getSelectedHumanAvatar,
    getSelectedTemplatePreview,
    getLogoPositionName,
    previewDigitalHumanVideo,
    closeDigitalHumanPreview,
    prevHumanPage,
    nextHumanPage,
    setHumanPage,
    totalHumanPages,
    updateDisplayedHumans
  };
} 