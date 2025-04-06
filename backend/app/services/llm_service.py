#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫荆AI平台大模型调用服务
实现了对多种大模型API的统一调用接口

支持的模型包括：
1. 硅基流动API (DeepSeek系列模型)
2. 火山引擎API (Volcano Engine) - 使用OpenAI兼容接口
3. 通义千问API (阿里云DashScope)

主要功能：
- 提供统一的API接口格式，简化多模型调用
- 自动处理不同API之间的兼容性差异
- 统一响应格式，使各种模型返回一致的结果结构
- 支持模型列表查询
- 自动检测和处理超长上下文，避免API调用失败
"""

import json
import os
import requests
from flask import current_app
import time

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI库未安装，火山引擎API将无法使用。请运行 pip install openai")

# 支持的模型配置
MODEL_CONFIG = {
    "deepseek-r1-sf": {
        "token_limit": 65536,
        "description": "DeepSeek R1-64K (硅基流动)",
        "api_type": "siliconflow",
        "base_url": "https://api.siliconflow.cn/v1",
        "provider": "硅基流动",
        "model_id": "Pro/deepseek-ai/DeepSeek-R1"
    },
    "deepseek-v3-sf": {
        "token_limit": 65536,
        "description": "DeepSeek V3-64K (硅基流动)",
        "api_type": "siliconflow",
        "base_url": "https://api.siliconflow.cn/v1",
        "provider": "硅基流动",
        "model_id": "Pro/deepseek-ai/DeepSeek-V3"
    },
    "deepseek-r1-vol": {
        "token_limit": 65536,
        "description": "DeepSeek R1-64K (火山引擎)",
        "api_type": "volcano",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "provider": "火山引擎",
        "model_id": "deepseek-r1-250120"
    },
    "deepseek-v3-vol": {
        "token_limit": 65536,
        "description": "DeepSeek V3-64K (火山引擎)",
        "api_type": "volcano",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "provider": "火山引擎",
        "model_id": "deepseek-v3-250324"
    },
    "qwq-32b": {
        "token_limit": 32768,
        "description": "通义千问-32B (硅基流动)",
        "api_type": "siliconflow",
        "base_url": "https://api.siliconflow.cn/v1",
        "provider": "硅基流动",
        "model_id": "Qwen/QwQ-32B"
    },
    "doubao-pro": {
        "token_limit": 32768,
        "description": "豆包-Pro (火山引擎)",
        "api_type": "volcano",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "provider": "火山引擎",
        "model_id": "doubao-pro-32k-241215"
    },
    "qwen-max": {
        "token_limit": 32768,
        "description": "通义千问-Max (阿里云)",
        "api_type": "dashscope",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "provider": "阿里云",
        "model_id": "qwen-max-latest"
    }
}

def num_tokens_from_string(string, model="gpt-3.5-turbo"):
    """
    估算字符串的token数量
    简单估算: 英文约4字符/token，中文约1.5字符/token
    """
    try:
        # 尝试使用tiktoken库进行精确估算 
        import tiktoken
        
        # 为不同的模型选择正确的编码器
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(string)
        return len(tokens)
    except Exception:
        # 如果tiktoken不可用或发生错误，使用简单估算
        # 检测是否主要是中文文本
        chinese_char_count = sum(1 for c in string if '\u4e00' <= c <= '\u9fff')
        chinese_ratio = chinese_char_count / max(1, len(string))
        
        if chinese_ratio > 0.5:
            # 主要是中文，使用1.5字符/token的比率
            return int(len(string) / 1.5)
        else:
            # 主要是英文，使用4字符/token的比率
            return int(len(string) / 4)

def standardize_response(response, model):
    """标准化API响应，确保输出格式一致"""
    try:
        # 确保有choices字段
        if "choices" not in response:
            response["choices"] = []
        
        # 确保每个choice中有message和finish_reason
        for i, choice in enumerate(response.get("choices", [])):
            if "message" not in choice:
                choice["message"] = {"role": "assistant", "content": ""}
            if "finish_reason" not in choice:
                choice["finish_reason"] = "stop"
            if "index" not in choice:
                choice["index"] = i
        
        # 确保有usage字段
        if "usage" not in response:
            response["usage"] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        else:
            usage = response["usage"]
            if "prompt_tokens" not in usage:
                usage["prompt_tokens"] = 0
            if "completion_tokens" not in usage:
                usage["completion_tokens"] = 0
            if "total_tokens" not in usage:
                usage["total_tokens"] = 0
        
        # 添加模型信息
        response["model"] = model
        
        return response
    except Exception as e:
        # 如果出错，返回基本结构
        return {
            "choices": [{
                "message": {"role": "assistant", "content": "处理响应时出错"},
                "finish_reason": "error",
                "index": 0
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            },
            "model": model,
            "error": str(e)
        }

class SiliconFlowAPI:
    """硅基流动API调用类"""
    
    def __init__(self, api_key, base_url="https://api.siliconflow.cn/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages, model_id, temperature=0.7, 
                      max_tokens=2000, top_p=1.0, frequency_penalty=0.0, 
                      presence_penalty=0.0, stop=None):
        """聊天接口 - 发送请求并获取模型回复"""
        
        url = f"{self.base_url}/chat/completions"
        
        # 估算所有消息的token数
        all_text = " ".join([msg.get("content", "") for msg in messages])
        estimated_tokens = num_tokens_from_string(all_text)
        
        # 检查是否超过模型限制 (保留安全余量)
        model_config = next((cfg for model, cfg in MODEL_CONFIG.items() 
                           if cfg["model_id"] == model_id), None)
        
        if model_config and estimated_tokens > (model_config["token_limit"] - max_tokens - 100):
            return {
                "error": {
                    "message": f"输入文本过长，估计token数为{estimated_tokens}，超过模型限制",
                    "type": "context_length_exceeded",
                    "param": "messages",
                    "code": "context_length_exceeded"
                }
            }

        # 构建请求参数
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        
        if stop:
            payload["stop"] = stop
            
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            if response.status_code == 200:
                return standardize_response(response.json(), model_id)
            else:
                return {
                    "error": {
                        "message": f"API调用失败: {response.text}",
                        "type": "api_error",
                        "code": response.status_code
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "message": f"API调用异常: {str(e)}",
                    "type": "api_error",
                    "code": "connection_error"
                }
            }

class VolcanoAPI:
    """火山引擎API调用类 - 使用OpenAI兼容接口"""
    
    def __init__(self, api_key, base_url="https://ark.cn-beijing.volces.com/api/v3"):
        self.api_key = api_key
        self.base_url = base_url
        print(f"初始化火山引擎API，baseURL: {base_url}, API密钥: {self.api_key[:8]}...")
        
        if not OPENAI_AVAILABLE:
            print("警告：OpenAI库未安装，火山引擎API将直接使用备用HTTP请求方式")
            # 设置备用方式的headers
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            self.client = None
            return
            
        # 直接使用备用HTTP请求方式而不尝试初始化OpenAI客户端
        # 这样可以避免出现"初始化OpenAI客户端失败"的错误
        self.client = None
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages, model_id, temperature=0.7, 
                      max_tokens=2000, top_p=1.0, frequency_penalty=0.0, 
                      presence_penalty=0.0, stop=None):
        """聊天接口 - 使用HTTP请求方式发送请求并获取模型回复"""
        
        # 直接使用备用方法发送请求，不再显示错误日志
        return self.chat_completion_fallback(
            messages, model_id, temperature, max_tokens, 
            top_p, frequency_penalty, presence_penalty, stop
        )
    
    def chat_completion_fallback(self, messages, model_id, temperature=0.7, 
                      max_tokens=2000, top_p=1.0, frequency_penalty=0.0, 
                      presence_penalty=0.0, stop=None):
        """备用方法：使用requests库直接调用API"""
        print("使用备用方法调用火山引擎API")
        url = f"{self.base_url}/chat/completions"
        
        # 添加系统消息如果不存在
        has_system = any(msg.get("role") == "system" for msg in messages)
        if not has_system:
            messages = [{"role": "system", "content": "你是人工智能助手"}] + messages
        
        # 构建请求参数
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        
        if stop:
            payload["stop"] = stop
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                return standardize_response(response.json(), model_id)
            else:
                return {
                    "error": {
                        "message": f"API调用失败: {response.text}",
                        "type": "api_error",
                        "code": response.status_code
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "message": f"API调用异常: {str(e)}",
                    "type": "api_error",
                    "code": "connection_error"
                }
            }

class DashscopeAPI:
    """阿里云DashScope API调用类"""
    
    def __init__(self, api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages, model_id, temperature=0.7, 
                      max_tokens=2000, top_p=1.0, frequency_penalty=0.0, 
                      presence_penalty=0.0, stop=None):
        """聊天接口 - 发送请求并获取模型回复"""
        
        url = f"{self.base_url}/chat/completions"
        
        # 估算所有消息的token数
        all_text = " ".join([msg.get("content", "") for msg in messages])
        estimated_tokens = num_tokens_from_string(all_text)
        
        # 检查是否超过模型限制 (保留安全余量)
        model_config = next((cfg for model, cfg in MODEL_CONFIG.items() 
                           if cfg["model_id"] == model_id), None)
        
        if model_config and estimated_tokens > (model_config["token_limit"] - max_tokens - 100):
            return {
                "error": {
                    "message": f"输入文本过长，估计token数为{estimated_tokens}，超过模型限制",
                    "type": "context_length_exceeded",
                    "param": "messages",
                    "code": "context_length_exceeded"
                }
            }

        # 构建请求参数
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }
        
        if stop:
            payload["stop"] = stop
            
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            if response.status_code == 200:
                return standardize_response(response.json(), model_id)
            else:
                return {
                    "error": {
                        "message": f"API调用失败: {response.text}",
                        "type": "api_error",
                        "code": response.status_code
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "message": f"API调用异常: {str(e)}",
                    "type": "api_error",
                    "code": "connection_error"
                }
            }

def get_api_client(model_name):
    """获取API客户端实例"""
    
    model_info = MODEL_CONFIG.get(model_name)
    if not model_info:
        return None, {"error": "未知的模型名称"}
    
    # 获取API密钥
    env_key = f"{model_info['api_type'].upper()}_API_KEY"
    api_key = os.environ.get(env_key, "")
    print(f"从环境变量获取API密钥 {env_key}: {'成功' if api_key else '失败'}")
    
    if not api_key:
        # 使用默认API密钥
        if model_info["api_type"] == "siliconflow":
            api_key = "sk-bivnwauskdbvpspvmdorrgkrpwlyfxbfcezqsfsevowzubdj"
        elif model_info["api_type"] == "volcano":
            # 根据不同模型选择不同API密钥
            if "doubao" in model_info["model_id"]:
                api_key = "YOUR_DOUBAO_API_KEY"
            else:
                # 使用用户提供的有效密钥
                api_key = "YOUR_VOLCANO_API_KEY"
            print(f"使用默认火山引擎API密钥: {api_key[:4]}...{api_key[-4:]}")
        elif model_info["api_type"] == "dashscope":
            api_key = "sk-1f4bdb8a73ee47809ee148a977c39737"
        print(f"使用默认API密钥: {api_key[:8]}...")
    
    # 创建对应的API客户端
    if model_info["api_type"] == "siliconflow":
        return SiliconFlowAPI(api_key, model_info["base_url"]), model_info
    elif model_info["api_type"] == "volcano":
        return VolcanoAPI(api_key, model_info["base_url"]), model_info
    elif model_info["api_type"] == "dashscope":
        return DashscopeAPI(api_key, model_info["base_url"]), model_info
    else:
        return None, {"error": "不支持的API类型"}

def get_available_models():
    """获取可用模型列表"""
    models = []
    for model_name, config in MODEL_CONFIG.items():
        models.append({
            "id": model_name,
            "name": config["description"],
            "provider": config["provider"],
            "token_limit": config["token_limit"],
            "api_type": config["api_type"],
            "model_id": config["model_id"]
        })
    return models

def chat_completion(model_name, messages, temperature=0.7, max_tokens=2000, 
                   top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stream=False):
    """统一的聊天接口"""
    
    # 获取API客户端
    client, model_info = get_api_client(model_name)
    if not client:
        return model_info
    
    # 调用对应的模型API
    return client.chat_completion(
        messages=messages,
        model_id=model_info["model_id"],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=None
    ) 