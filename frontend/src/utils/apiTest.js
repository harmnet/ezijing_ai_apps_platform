import axios from 'axios';

/**
 * 简化版API连通性测试
 * 仅测试API能否响应，不检查具体字段结构
 */
export async function testApiConnection() {
  try {
    // 测试步骤1：检查模型列表API
    console.log('测试步骤1：检查模型列表API连通性...');
    
    try {
      const modelResponse = await axios.get('/api/v1/llm/models', { timeout: 8000 });
      console.log('模型列表API响应状态码:', modelResponse.status);
      
      // 只要能获取到响应就认为成功
      if (modelResponse.status >= 200 && modelResponse.status < 300) {
        console.log('模型列表API连接成功');
        
        // 尝试获取模型列表，但不强制要求
        let models = [];
        try {
          if (modelResponse.data && modelResponse.data.data && Array.isArray(modelResponse.data.data)) {
            models = modelResponse.data.data;
            console.log(`成功获取${models.length}个模型`);
          }
        } catch (e) {
          console.warn('解析模型列表失败，但不影响测试:', e);
        }
        
        // 测试步骤2：测试聊天API
        console.log('测试步骤2：检查聊天API连通性...');
        
        // 使用默认模型ID或从列表中获取
        const testModelId = models.length > 0 ? models[0].id : 'deepseek-v3-vol';
        
        const testRequest = {
          model: testModelId,
          messages: [{ role: 'user', content: '你好' }],
          temperature: 0.7,
          max_tokens: 5
        };
        
        try {
          const chatResponse = await axios.post('/api/v1/llm/chat', testRequest, { timeout: 8000 });
          console.log('聊天API响应状态码:', chatResponse.status);
          
          // 只要收到响应且状态码正常就视为成功
          if (chatResponse.status >= 200 && chatResponse.status < 300) {
            return {
              success: true,
              models: models,
              message: 'API连通性测试通过！服务器响应正常',
            };
          } else {
            return {
              success: false,
              error: `聊天API测试失败，响应状态码: ${chatResponse.status}`
            };
          }
        } catch (error) {
          console.error('聊天API请求失败:', error.message);
          return {
            success: false,
            error: '聊天API请求失败: ' + (error.message || '未知错误')
          };
        }
      } else {
        return {
          success: false,
          error: `模型列表API测试失败，响应状态码: ${modelResponse.status}`
        };
      }
    } catch (error) {
      console.error('模型列表API请求失败:', error.message);
      return {
        success: false,
        error: '模型列表API请求失败: ' + (error.message || '未知错误')
      };
    }
  } catch (error) {
    console.error('API测试过程中发生异常:', error);
    return {
      success: false,
      error: '测试过程中发生异常: ' + (error.message || '未知错误')
    };
  }
} 