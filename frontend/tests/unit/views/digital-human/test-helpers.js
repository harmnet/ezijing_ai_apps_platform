/**
 * 数字人API测试辅助函数
 */

/**
 * 创建模拟的请求数据
 * @param {Object} options - 配置选项
 * @returns {Object} - 模拟请求数据
 */
export const createMockRequestData = (options = {}) => {
  const defaultOptions = {
    outputVideoName: '测试视频',
    pptUrl: 'https://example.com/test.ppt',
    sceneCount: 1,
    withBgm: true
  };
  
  const config = { ...defaultOptions, ...options };
  
  // 创建基本场景
  const createScene = (position = 'right') => {
    const params = position === 'right' 
      ? { width: 344, height: 1080, x: 1517, y: 309, postureId: 'aMiAX96rMqNS' }
      : { width: 319, height: 1536, x: -53, y: 346, postureId: 'd5nJE6EI0txK' };
    
    return {
      virtualHuman: {
        attributes: {
          width: params.width,
          height: params.height,
          x: params.x,
          y: params.y,
          forceMattingType: 0
        },
        virtualHumanId: 'VHP3S1EF7',
        virtualHumanPostureId: params.postureId,
        zIndex: 20
      },
      tts: {
        voiceId: '101-master-ugdr',
        rate: 1,
        pitch: 1,
        volume: 50
      },
      voiceText: `这是测试场景 ${position === 'right' ? '右侧' : '左侧'}`
    };
  };
  
  // 生成场景数组
  const scenes = [];
  for (let i = 0; i < config.sceneCount; i++) {
    scenes.push(createScene(i % 2 === 0 ? 'right' : 'left'));
  }
  
  // 构建完整请求对象
  const requestData = {
    outputVideoName: config.outputVideoName,
    width: 1920,
    height: 1080,
    creationDetail: {
      scenes: scenes
    },
    pptInfo: {
      pptUrl: config.pptUrl,
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
  
  // 添加背景音乐(如果需要)
  if (config.withBgm) {
    requestData.creationDetail.backgroundMusic = {
      mediaUrl: "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/1a1789ea-25bf-437b-acd2-fdc08a265087.MP3",
      volume: 0.3,
      speed: 1,
      loop: true
    };
  }
  
  return requestData;
};

/**
 * 创建模拟的元素UI组件
 * @returns {Object} - 模拟的ElementPlus UI组件
 */
export const createMockElementUI = () => {
  let mockLoading = null;
  
  return {
    ElMessage: {
      success: vi.fn(),
      error: vi.fn(),
      info: vi.fn(),
      warning: vi.fn()
    },
    ElLoading: {
      service: vi.fn(() => {
        mockLoading = {
          close: vi.fn()
        };
        return mockLoading;
      })
    },
    ElMessageBox: {
      confirm: vi.fn(() => Promise.resolve())
    },
    mockLoading
  };
};

/**
 * 创建模拟的API响应
 * @param {String} type - 响应类型 success|error
 * @param {Object} options - 配置选项
 * @returns {Object} - 模拟API响应
 */
export const createMockApiResponse = (type = 'success', options = {}) => {
  if (type === 'success') {
    return {
      code: 0,
      message: "success",
      data: options.data || "test-task-123456"
    };
  } else {
    return {
      code: options.code || 1001,
      message: options.message || "请求参数错误",
      data: null
    };
  }
};

/**
 * 创建模拟的任务状态响应
 * @param {String} status - 任务状态 PROCESSING|FINISHED|FAILED
 * @param {Object} options - 配置选项
 * @returns {Object} - 模拟任务状态响应
 */
export const createMockTaskStatusResponse = (status = 'FINISHED', options = {}) => {
  const response = {
    code: 0,
    message: "success",
    data: {
      status: status
    }
  };
  
  if (status === 'FINISHED') {
    response.data.resultUrl = options.videoUrl || "https://example.com/video.mp4";
  } else if (status === 'FAILED') {
    response.data.errorMessage = options.errorMessage || "任务处理失败";
  }
  
  return response;
};

/**
 * 等待指定的毫秒数
 * @param {Number} ms - 等待毫秒数
 * @returns {Promise} 
 */
export const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * 模拟表单组件的事件触发
 * @param {Object} wrapper - Vue Test Utils包装器
 * @param {String} selector - CSS选择器
 * @param {String} eventName - 事件名称
 * @param {*} value - 事件值
 */
export const triggerEvent = async (wrapper, selector, eventName, value) => {
  const element = wrapper.find(selector);
  await element.trigger(eventName, value);
};

/**
 * 模拟表单输入
 * @param {Object} wrapper - Vue Test Utils包装器
 * @param {String} selector - CSS选择器
 * @param {*} value - 输入值
 */
export const setInputValue = async (wrapper, selector, value) => {
  const input = wrapper.find(selector);
  await input.setValue(value);
};

export default {
  createMockRequestData,
  createMockElementUI,
  createMockApiResponse,
  createMockTaskStatusResponse,
  wait,
  triggerEvent,
  setInputValue
}; 