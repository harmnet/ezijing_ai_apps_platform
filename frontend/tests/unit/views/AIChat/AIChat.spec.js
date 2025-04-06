import { mount, shallowMount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import AIChat from '@/views/AIChat.vue';

// Mock axios
vi.mock('axios');

// Mock clipboard API
Object.defineProperty(navigator, 'clipboard', {
  value: {
    writeText: vi.fn().mockImplementation(() => Promise.resolve())
  },
  configurable: true
});

describe('AIChat.vue', () => {
  let wrapper;
  
  beforeEach(() => {
    // 重置所有模拟
    vi.resetAllMocks();
    
    // 模拟 axios 响应
    axios.get.mockResolvedValue({
      data: {
        status: 'success',
        data: [
          { id: 'deepseek-v3-vol', name: 'DeepSeek V3', provider: 'volcano' },
          { id: 'qwen-max-sf', name: 'Qwen Max', provider: 'silicon_flow' }
        ]
      }
    });
    
    // 创建组件实例，使用浅渲染
    wrapper = shallowMount(AIChat, {
      global: {
        stubs: ['el-input', 'el-button', 'el-select']
      }
    });
  });
  
  it('渲染AI对话组件', () => {
    expect(wrapper.exists()).toBe(true);
  });
  
  it('设置用户输入', () => {
    wrapper.vm.userInput = '你好，AI';
    expect(wrapper.vm.userInput).toBe('你好，AI');
  });
}); 