import { mount, shallowMount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import AdSlogan from '@/views/text-creation/marketing/AdSlogan.vue';

// Mock axios
vi.mock('axios');

// Mock window alert and UI库
global.alert = vi.fn();

describe('AdSlogan.vue', () => {
  let wrapper;
  
  beforeEach(() => {
    // 重置 axios 模拟
    vi.resetAllMocks();
    
    // 模拟 API 响应
    axios.get.mockResolvedValue({
      data: {
        status: 'success',
        data: [
          { id: 'deepseek-v3-vol', name: 'DeepSeek V3', provider: 'volcano' },
          { id: 'qwen-max-sf', name: 'Qwen Max', provider: 'silicon_flow' }
        ]
      }
    });
    
    axios.post.mockResolvedValue({
      data: {
        status: 'success',
        data: {
          choices: [
            {
              message: {
                content: '1. 第一条广告语\n2. 第二条广告语\n3. 第三条广告语'
              }
            }
          ]
        }
      }
    });
    
    // 创建组件实例
    wrapper = shallowMount(AdSlogan, {
      global: {
        stubs: ['el-select', 'el-option', 'el-input', 'el-button', 'el-form', 'el-form-item'],
        mocks: {
          $message: {
            success: vi.fn(),
            error: vi.fn()
          },
          $notify: vi.fn()
        }
      }
    });
  });
  
  it('正确渲染组件', () => {
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find('.ad-slogan-page').exists()).toBe(true);
  });
  
  it('设置默认模型', () => {
    expect(wrapper.vm.selectedModel).toBeTruthy();
    wrapper.vm.selectedModel = 'deepseek-v3-vol';
    expect(wrapper.vm.selectedModel).toBe('deepseek-v3-vol');
  });
  
  it('构建提示词应包含产品名称', () => {
    wrapper.vm.productName = '测试产品';
    
    const prompt = wrapper.vm.buildPrompt();
    expect(prompt).toContain('测试产品');
  });
}); 