import axios from 'axios';

// API端点配置
export const API_ENDPOINTS = {
  CHAT: '/api/v1/llm/chat',
  CHAT_STREAM: '/api/v1/llm/chat/stream', 
  MODELS: '/api/v1/llm/models'
};

// 默认参数配置
export const DEFAULT_PARAMS = {
  temperature: 0.7,
  max_tokens: 2000,
  stream: false,
  return_reasoning: false
};

// API调用工具类
export class LLMApi {
  // 获取模型列表
  static async getModels() {
    try {
      const response = await axios.get(API_ENDPOINTS.MODELS);
      if (response.data.status === 'success') {
        return response.data.data;
      }
      throw new Error(response.data.message || '获取模型列表失败');
    } catch (error) {
      console.error('获取模型列表失败:', error);
      throw error;
    }
  }

  // 普通聊天请求
  static async chat(messages, model, params = {}) {
    try {
      const requestParams = {
        ...DEFAULT_PARAMS,
        ...params,
        messages,
        model
      };

      const response = await axios.post(API_ENDPOINTS.CHAT, requestParams);
      if (response.data.status === 'success') {
        return response.data.data;
      }
      throw new Error(response.data.message || '聊天请求失败');
    } catch (error) {
      console.error('聊天请求失败:', error);
      throw error;
    }
  }

  // 流式聊天请求
  static async chatStream(messages, model, params = {}, onData, onError) {
    try {
      const requestParams = {
        ...DEFAULT_PARAMS,
        ...params,
        messages,
        model,
        stream: true
      };

      console.log('流式请求参数:', JSON.stringify(requestParams, null, 2));

      // 使用fetch API发送请求
      const controller = new AbortController();
      const signal = controller.signal;
      
      console.log('发送流式请求到:', API_ENDPOINTS.CHAT_STREAM);
      
      // 直接使用流式专用接口
      const response = await fetch(API_ENDPOINTS.CHAT_STREAM, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
          'Accept-Encoding': 'identity'  // 明确拒绝压缩，确保流式传输正常
        },
        body: JSON.stringify(requestParams),
        signal
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`HTTP error! status: ${response.status}, response: ${errorText}`);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      
      // 使用ReadableStream处理响应，不使用response.text()
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      
      // 使用递归处理流
      const readChunk = async () => {
        try {
          // 读取下一个数据块
          const { done, value } = await reader.read();
          
          if (done) {
            console.log('流式读取完成');
            return;
          }
          
          // 解码数据
          const chunk = decoder.decode(value, { stream: true });
          console.log(`收到数据块: ${chunk.length}字节`);
          buffer += chunk;
          
          // 分割行
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // 保留最后一个可能不完整的行
          
          // 处理每行内容
          let hadValidData = false;
          for (const line of lines) {
            const trimmedLine = line.trim();
            if (!trimmedLine) continue;
            
            if (trimmedLine.startsWith('data:')) {
              const dataContent = trimmedLine.substring(5).trim();
              
              if (dataContent === '[DONE]') {
                console.log('收到流结束标记');
                continue;
              }
              
              try {
                const jsonData = JSON.parse(dataContent);
                console.log('解析的数据:', jsonData);
                hadValidData = true;
                
                // 立即调用回调，不等待下一个块
                onData && onData(jsonData);
              } catch (e) {
                console.error('解析JSON失败:', e, dataContent);
              }
            }
          }
          
          // 递归调用，继续读取下一个块
          // 直接递归容易导致堆栈溢出，使用setTimeout
          setTimeout(() => readChunk(), 0);
          
        } catch (error) {
          console.error('读取流数据失败:', error);
          onError && onError(error);
        }
      };
      
      // 开始读取流
      readChunk();
      
      // 返回控制对象
      return {
        cancel: () => {
          console.log('取消流式请求');
          controller.abort();
        }
      };
    } catch (error) {
      console.error('流式请求失败:', error);
      onError && onError(error);
      
      return {
        cancel: () => console.log('请求已失败，无法取消')
      };
    }
  }

  // 流式聊天请求，包含思考过程
  static async chatWithReasoning(messages, model, params = {}, onData, onError) {
    // 只对R1模型启用思考过程
    const useReasoning = model.includes('r1');
    
    try {
      console.log('使用chatWithReasoning，模型:', model, '启用思考:', useReasoning);
      console.log('消息数量:', messages.length);
      
      // 确保参数是深拷贝
      const requestParams = {
        ...DEFAULT_PARAMS,
        ...JSON.parse(JSON.stringify(params)),
        stream: true, // 强制使用流式响应
        enable_reasoning: useReasoning // 设置思考过程参数
      };
      
      console.log('调用流式接口，请求参数:', JSON.stringify(requestParams, null, 2));
      
      // 调用流式接口
      return await this.chatStream(
        messages,
        model,
        requestParams,
        onData,
        onError
      );
    } catch (error) {
      console.error('流式聊天请求失败:', error);
      onError && onError(error);
      
      // 返回一个空的控制对象
      return {
        cancel: () => console.log('请求已失败，无法取消')
      };
    }
  }
}

// 导出工具函数
export const api = {
  getModels: LLMApi.getModels,
  chat: LLMApi.chat,
  chatStream: LLMApi.chatStream,
  chatWithReasoning: LLMApi.chatWithReasoning,
  
  // 测试函数，用于浏览器控制台调试
  testStreamApi: async (model = 'deepseek-r1-vol') => {
    console.log(`开始测试流式API，模型: ${model}`);
    try {
      await LLMApi.chatWithReasoning(
        [{ role: 'user', content: '请推荐三本计算机科学的经典书籍并说明它们的特点' }],
        model,
        { temperature: 0.7, max_tokens: 2000 },
        (data) => {
          console.log('收到流式数据回调:', data);
          if (data.choices && data.choices[0]) {
            const choice = data.choices[0];
            if (choice.delta) {
              if (choice.delta.reasoning_content) {
                console.log('收到思考内容:', choice.delta.reasoning_content);
              }
              if (choice.delta.content) {
                console.log('收到回复内容:', choice.delta.content);
              }
            }
          }
        },
        (error) => {
          console.error('测试API出错:', error);
        }
      );
      console.log('流式请求完成');
    } catch (error) {
      console.error('测试API异常:', error);
    }
  },
  
  // 使用原生方式测试后端的SSE格式
  testRawStream: async (model = 'deepseek-v3-vol') => {
    console.log(`开始测试原生流式请求，模型: ${model}`);
    
    const requestParams = {
      messages: [{ role: 'user', content: '简短介绍一下你自己' }],
      model: model,
      temperature: 0.7,
      max_tokens: 100,
      stream: true
    };
    
    // 原生fetch实现
    console.log('使用fetch方式测试');
    fetch('/api/v1/llm/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(requestParams),
    }).then(response => {
      console.log('响应状态:', response.status);
      console.log('响应头:', response.headers);
      
      // 读取响应体
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      
      // 记录接收的所有数据，用于分析
      let allReceived = '';
      
      // 处理函数
      const processText = async () => {
        try {
          const { value, done } = await reader.read();
          if (done) {
            console.log('原始流式读取完成');
            console.log('完整接收的数据:', allReceived);
            return;
          }
          
          const text = decoder.decode(value);
          console.log('原始数据块:', text);
          allReceived += text;
          
          // 继续读取
          processText();
        } catch (error) {
          console.error('读取中断:', error);
        }
      };
      
      processText();
    }).catch(error => {
      console.error('原生fetch请求错误:', error);
    });
    
    // 同时测试XMLHttpRequest方式
    console.log('使用XMLHttpRequest方式测试');
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/llm/chat/stream', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'text/event-stream');
    
    // 监听状态变化
    xhr.onreadystatechange = function() {
      console.log(`XMLHttpRequest状态变化: readyState=${xhr.readyState}, status=${xhr.status}`);
    };
    
    // 记录所有接收的数据
    let allData = '';
    
    // 监听进度
    xhr.onprogress = function(event) {
      if (xhr.status === 200) {
        console.log(`进度: loaded=${event.loaded}, total=${event.total || '未知'}`);
        const newData = xhr.responseText.substring(allData.length);
        if (newData.length > 0) {
          console.log('新接收的数据:', newData);
          allData = xhr.responseText;
        }
      }
    };
    
    xhr.onload = function() {
      if (xhr.status === 200) {
        console.log('XHR请求完成，完整响应:', xhr.responseText);
      } else {
        console.error('XHR请求失败:', xhr.status);
      }
    };
    
    xhr.onerror = function() {
      console.error('XHR网络错误');
    };
    
    xhr.send(JSON.stringify(requestParams));
    
    return '测试原生流式请求已启动，请查看控制台输出';
  }
};

/**
 * 测试原始流式响应格式
 * 用于调试和检查服务器的流式响应
 */
function testRawStream() {
  const url = `/api/v1/llm/chat/stream?t=${Date.now()}`;
  
  console.log('%c正在测试原始流式响应...', 'color: blue; font-weight: bold');
  console.log('请求URL:', url);
  
  // 创建简单的测试消息
  const testData = {
    messages: [
      {
        role: 'user',
        content: '你好，请简单自我介绍'
      }
    ],
    model: 'gpt-3.5-turbo',
    temperature: 0.7,
    max_tokens: 100,
    stream: true
  };
  
  // 使用原生fetch API进行测试
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    },
    body: JSON.stringify(testData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }
    
    console.log('%c获取到响应:', 'color: green; font-weight: bold');
    console.log('状态码:', response.status);
    console.log('Content-Type:', response.headers.get('Content-Type'));
    console.log('Transfer-Encoding:', response.headers.get('Transfer-Encoding'));
    
    // 读取原始流
    const reader = response.body.getReader();
    let chunks = [];
    let totalSize = 0;
    
    return new Promise((resolve, reject) => {
      function readStream() {
        reader.read().then(({ done, value }) => {
          if (done) {
            console.log('原始流式读取完成');
            console.log('完整接收的数据:', allReceived);
            return;
          }
          
          // 记录收到的数据块
          totalSize += value.length;
          chunks.push(value);
          
          // 将ArrayBuffer转换为字符串
          const chunk = new TextDecoder().decode(value);
          console.log('%c收到数据块 (' + value.length + ' 字节):', 'color: purple');
          console.log('%c' + chunk.replace(/\n/g, '\\n'), 'color: #888');
          
          // 继续读取
          readStream();
        }).catch(error => {
          console.error('读取流失败:', error);
          reject(error);
        });
      }
      
      readStream();
    });
  })
  .then(chunks => {
    // 合并所有块并转换为文本
    const allBytes = new Uint8Array(chunks.reduce((totalLength, chunk) => totalLength + chunk.length, 0));
    let position = 0;
    for (const chunk of chunks) {
      allBytes.set(chunk, position);
      position += chunk.length;
    }
    
    const fullText = new TextDecoder().decode(allBytes);
    
    console.log('%c完整响应内容:', 'color: blue; font-weight: bold');
    console.log('%c' + fullText.replace(/\n/g, '\\n'), 'color: #333');
    
    // 尝试按SSE格式解析
    console.log('%c按SSE格式分解:', 'color: blue; font-weight: bold');
    const events = fullText.split('\n\n').filter(Boolean);
    
    events.forEach((event, index) => {
      console.log(`%c事件 #${index + 1}:`, 'color: #009688; font-weight: bold');
      console.log(event.replace(/\n/g, '\\n'));
      
      // 尝试提取并解析JSON数据
      const dataMatch = event.match(/^data: (.+)$/m);
      if (dataMatch && dataMatch[1]) {
        try {
          const jsonData = JSON.parse(dataMatch[1]);
          console.log('解析后的JSON:', jsonData);
        } catch (e) {
          console.warn('JSON解析失败:', dataMatch[1]);
        }
      }
    });
  })
  .catch(error => {
    console.error('%c测试失败:', 'color: red; font-weight: bold', error);
  });
}

// 导出接口
export default {
  chat: LLMApi.chat,
  chatStream: LLMApi.chatStream,
  chatWithReasoning: LLMApi.chatWithReasoning,
  testRawStream  // 添加新函数到导出
};