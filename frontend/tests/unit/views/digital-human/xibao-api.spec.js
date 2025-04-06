import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import axios from 'axios';
import * as path from 'path';
import { fileURLToPath } from 'url';

// 预先定义AUTH_HEADER
const AUTH_HEADER = {
  'subscription-key': '282cd94b697e48e6aca6d20bbdaf0d0f',
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};

// 定义正确的API路径
const baseURL = 'https://openapi.xiaoice.com';
const API_PATH_PREFIX = '/vh/openapi';

// 手动模拟axios
vi.mock('axios', () => ({
  default: vi.fn(),
  get: vi.fn(),
  create: vi.fn(() => ({
    get: vi.fn(),
    defaults: {
      headers: {}
    },
    interceptors: {
      request: {
        use: vi.fn()
      },
      response: {
        use: vi.fn()
      }
    }
  }))
}));

// 创建模拟的createPptVideoTask函数
const createMockPptVideoTask = async (data) => {
  console.log('模拟调用createPptVideoTask', data);
  // 使用mock axios
  await axios({
    method: 'post',
    url: `${baseURL}${API_PATH_PREFIX}/video/task/v2/ppt/submit`,
    headers: AUTH_HEADER,
    data: data,
    timeout: 60000
  });
  return axios.__mockedResponse;
};

// 创建模拟的getTaskStatus函数
const createMockGetTaskStatus = async (taskId) => {
  console.log('模拟调用getTaskStatus', taskId);
  // 使用mock axios
  await axios({
    method: 'get',
    url: `${baseURL}${API_PATH_PREFIX}/video/task/status`,
    headers: AUTH_HEADER,
    params: { taskId }
  });
  return axios.__mockedResponse;
};

describe('xibao-api函数模拟测试', () => {
  beforeEach(() => {
    // 重置所有模拟
    vi.resetAllMocks();
    
    // 设置console.log和console.error的mock以避免测试输出过多日志
    vi.spyOn(console, 'log').mockImplementation(() => {});
    vi.spyOn(console, 'error').mockImplementation(() => {});
  });
  
  afterEach(() => {
    // 恢复console.log和console.error
    console.log.mockRestore();
    console.error.mockRestore();
  });
  
  it('测试createPptVideoTask函数 - 成功场景', async () => {
    // 模拟请求数据
    const mockRequestData = {
      outputVideoName: '测试视频',
      width: 1920,
      height: 1080,
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
              virtualHumanId: 'VHP3S1EF7',
              virtualHumanPostureId: 'aMiAX96rMqNS',
              zIndex: 20
            },
            tts: {
              voiceId: '101-master-ugdr',
              rate: 1,
              pitch: 1,
              volume: 50
            },
            voiceText: "测试语音文本"
          }
        ]
      },
      pptInfo: {
        pptUrl: 'https://example.com/test.ppt',
        convertType: "VIDEO",
        getText: true,
        singlePageSecond: 5
      }
    };
    
    // 模拟成功响应
    const mockResponse = {
      status: 200,
      data: {
        code: 0,
        message: "success",
        data: "test-task-123456"
      }
    };
    
    // 设置axios模拟返回
    axios.mockResolvedValue(mockResponse);
    axios.__mockedResponse = mockResponse.data;
    
    // 调用模拟的API函数
    const result = await createMockPptVideoTask(mockRequestData);
    
    // 验证axios调用
    expect(axios).toHaveBeenCalledWith({
      method: 'post',
      url: `${baseURL}${API_PATH_PREFIX}/video/task/v2/ppt/submit`,
      headers: AUTH_HEADER,
      data: mockRequestData,
      timeout: 60000
    });
    
    // 验证结果
    expect(result).toEqual(mockResponse.data);
  });
  
  it('测试createPptVideoTask函数 - 失败场景', async () => {
    // 模拟请求数据
    const mockRequestData = {
      // 简化的数据结构
      outputVideoName: '测试视频',
      pptInfo: {
        pptUrl: 'https://example.com/test.ppt'
      }
    };
    
    // 模拟错误响应
    const mockError = {
      response: {
        status: 400,
        data: {
          code: 1001,
          message: '参数错误'
        }
      }
    };
    
    // 设置axios模拟抛出错误
    axios.mockRejectedValue(mockError);
    
    // 调用模拟的API函数并期望抛出错误
    await expect(createMockPptVideoTask(mockRequestData)).rejects.toEqual(mockError);
    
    // 验证axios调用
    expect(axios).toHaveBeenCalledWith({
      method: 'post',
      url: `${baseURL}${API_PATH_PREFIX}/video/task/v2/ppt/submit`,
      headers: AUTH_HEADER,
      data: mockRequestData,
      timeout: 60000
    });
  });
  
  it('测试getTaskStatus函数 - 成功场景', async () => {
    // 模拟任务ID
    const mockTaskId = 'test-task-123456';
    
    // 模拟成功响应
    const mockResponse = {
      status: 200,
      data: {
        code: 0,
        message: "success",
        data: {
          status: "FINISHED",
          resultUrl: "https://example.com/video.mp4"
        }
      }
    };
    
    // 设置axios模拟返回
    axios.mockResolvedValue(mockResponse);
    axios.__mockedResponse = mockResponse.data;
    
    // 调用模拟的API函数
    const result = await createMockGetTaskStatus(mockTaskId);
    
    // 验证axios调用
    expect(axios).toHaveBeenCalledWith({
      method: 'get',
      url: `${baseURL}${API_PATH_PREFIX}/video/task/status`,
      headers: AUTH_HEADER,
      params: { taskId: mockTaskId }
    });
    
    // 验证结果
    expect(result).toEqual(mockResponse.data);
  });
  
  it('测试API认证头部配置是否正确', () => {
    // 验证AUTH_HEADER包含必要字段
    expect(AUTH_HEADER).toHaveProperty('subscription-key');
    expect(AUTH_HEADER).toHaveProperty('Content-Type');
    expect(AUTH_HEADER).toHaveProperty('Accept');
    
    // 验证值是否正确
    expect(AUTH_HEADER['subscription-key']).toBe('282cd94b697e48e6aca6d20bbdaf0d0f');
    expect(AUTH_HEADER['Content-Type']).toBe('application/json');
    expect(AUTH_HEADER['Accept']).toBe('application/json');
  });
}); 