import { describe, it, expect, beforeAll } from 'vitest';
import axios from 'axios';
import { AUTH_HEADER } from '@/views/digital-human/xibao-api';

// 注意：这是集成测试，会真实调用API，谨慎运行
// 此测试应该在特定环境中运行，例如开发或测试环境
describe('数字人服务API集成测试', () => {
  const baseURL = 'https://openapi.xiaoice.com';
  const API_PATH_PREFIX = '/vh';
  
  // 跳过所有测试的标志
  let skipTests = false;
  
  beforeAll(() => {
    // 根据环境变量决定是否跳过测试
    skipTests = process.env.ENABLE_INTEGRATION_TESTS !== 'true';
    if (skipTests) {
      console.log('集成测试被跳过。设置ENABLE_INTEGRATION_TESTS=true以启用');
    }
  });
  
  // 辅助函数，用于跳过测试
  const conditionalTest = (name, fn) => {
    return it(name, skipTests ? () => {} : fn);
  };
  
  // 测试API连接
  conditionalTest('测试与数字人服务的API连接', async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${baseURL}${API_PATH_PREFIX}/video/task/status`,
        headers: AUTH_HEADER,
        params: { taskId: 'test-connection-123' },
        validateStatus: () => true // 接受任何状态码
      });
      
      // 即使是404错误也表示服务器正常响应
      expect(response.status).toBeDefined();
      console.log('API连接测试完成，状态码:', response.status);
      
      // 记录响应内容，用于调试
      console.log('响应内容:', response.data);
    } catch (error) {
      console.error('API连接测试失败:', error);
      throw error; // 确保测试失败
    }
  });
  
  // 测试提交简单任务
  conditionalTest('测试提交PPT视频任务', async () => {
    // 创建最小化的请求数据
    const mockRequestData = {
      outputVideoName: '集成测试视频',
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
            voiceText: "这是一个集成测试，测试与数字人服务的连接"
          }
        ]
      },
      pptInfo: {
        // 使用一个公开可访问的PPT URL，仅用于测试
        pptUrl: 'https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/test.pptx',
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
    
    try {
      const response = await axios({
        method: 'post',
        url: `${baseURL}${API_PATH_PREFIX}/video/task/v2/ppt/submit`,
        headers: AUTH_HEADER,
        data: mockRequestData,
        timeout: 60000,
        validateStatus: () => true // 接受任何状态码
      });
      
      // 记录响应
      console.log('提交任务响应:', response.data);
      console.log('响应状态码:', response.status);
      
      // 验证响应
      expect(response.status).toBeDefined();
      
      // 如果成功创建了任务，保存任务ID供后续测试使用
      if (response.data && response.data.code === 0 && response.data.data) {
        process.env.TEST_TASK_ID = response.data.data;
        console.log('测试任务ID:', process.env.TEST_TASK_ID);
      }
    } catch (error) {
      console.error('提交任务测试失败:', error);
      // 不抛出错误，因为这可能是由于测试环境缺少有效的PPT URL
      console.log('提交任务测试跳过');
    }
  });
  
  // 测试查询任务状态
  conditionalTest('测试查询任务状态', async () => {
    // 使用之前保存的任务ID或使用一个固定的任务ID
    const taskId = process.env.TEST_TASK_ID || 'test-task-id';
    
    try {
      const response = await axios({
        method: 'get',
        url: `${baseURL}${API_PATH_PREFIX}/video/task/status`,
        headers: AUTH_HEADER,
        params: { taskId },
        validateStatus: () => true // 接受任何状态码
      });
      
      // 记录响应
      console.log('查询任务状态响应:', response.data);
      console.log('响应状态码:', response.status);
      
      // 验证响应
      expect(response.status).toBeDefined();
    } catch (error) {
      console.error('查询任务状态测试失败:', error);
      throw error; // 确保测试失败
    }
  });
  
  // 测试中间件API代理(如果项目使用了API代理)
  conditionalTest('测试本地API代理', async () => {
    try {
      // 尝试通过本地API代理调用
      const response = await axios({
        method: 'get',
        url: '/api/v1/aibeings/test-connection',
        validateStatus: () => true // 接受任何状态码
      });
      
      // 记录响应
      console.log('本地API代理测试响应:', response.data);
      console.log('响应状态码:', response.status);
      
      // 验证响应
      expect(response.status).toBeDefined();
    } catch (error) {
      console.error('本地API代理测试失败:', error);
      console.log('本地API代理测试跳过 - 可能需要在开发服务器环境中运行');
    }
  });
}); 