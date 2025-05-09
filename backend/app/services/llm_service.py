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
import sys
import logging

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
        "base_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "provider": "火山引擎",
        "model_id": "deepseek-r1-250120"
    },
    "deepseek-v3-vol": {
        "token_limit": 65536,
        "description": "DeepSeek V3-64K (火山引擎)",
        "api_type": "volcano",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
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
            
            # 处理思考型模型的思考内容
            if "message" in choice and "reasoning_content" in choice["message"]:
                # 可以选择在这里合并思考内容和最终内容
                reasoning = choice["message"].get("reasoning_content", "")
                content = choice["message"].get("content", "")
                
                # 注意：我们保留原始思考内容，但确保content字段一定存在有效内容
                if not content.strip() and reasoning.strip():
                    choice["message"]["content"] = "思考过程：\n" + reasoning
            
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
    
    def chat(self, model, messages, temperature=0.7, max_tokens=2000):
        """兼容VolcanoAPI的chat方法，用于统一API接口"""
        return self.chat_completion(
            messages=messages,
            model_id=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None,
            stream=False
        )
    
    def chat_completion(self, messages, model_id, temperature=0.7, 
                      max_tokens=2000, top_p=1.0, frequency_penalty=0.0, 
                      presence_penalty=0.0, stop=None, stream=False):
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
    """火山引擎API客户端"""
    def __init__(self, api_key, api_base="https://ark.cn-beijing.volces.com/api/v3/chat/completions"):
        self.api_base = api_base
        self.api_key = api_key
        self.timeout = 120  # 设置较长的超时时间，单位秒
        self.logger = logging.getLogger("volcano-api")
        self.logger.setLevel(logging.DEBUG)
    
    def chat(self, model, messages, temperature=0.7, max_tokens=2000):
        """发送聊天请求到火山引擎API"""
        if "r1" in model:
            self.logger.info(f"使用R1模型: {model}")
            # R1模型使用更长超时
            self.timeout = 180
            
        url = self.api_base
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": model,
            "input_type": "chat",
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": max_tokens
            },
            "messages": messages
        }
        
        try:
            self.logger.debug(f"发送请求到火山引擎API: {url}, 模型: {model}")
            start_time = time.time()
            
            response = requests.post(
                url, 
                headers=headers, 
                json=payload,
                timeout=self.timeout
            )
            
            duration = time.time() - start_time
            self.logger.debug(f"火山引擎API响应耗时: {duration:.2f}秒")
            
            # 检查HTTP响应状态
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # R1模型特殊处理，记录是否包含思考过程
            if "r1" in model and "output" in result:
                if "choices" in result["output"] and len(result["output"]["choices"]) > 0:
                    if "message" in result["output"]["choices"][0]:
                        message = result["output"]["choices"][0]["message"]
                        has_content = "content" in message and message["content"]
                        has_reasoning = "reasoning_content" in message and message["reasoning_content"]
                        self.logger.info(f"R1模型响应: 包含content: {has_content}, 包含reasoning_content: {has_reasoning}")
            
            # 统一转换为通用格式
            return self._convert_response(result)
            
        except requests.exceptions.Timeout:
            self.logger.error(f"请求超时: 模型={model}, 超时设置={self.timeout}秒")
            raise Exception(f"火山引擎API请求超时 (>{self.timeout}秒)")
            
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"连接错误: {str(e)}")
            raise Exception(f"无法连接到火山引擎API: {str(e)}")
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {str(e)}, 状态码: {response.status_code}")
            error_detail = f"状态码: {response.status_code}"
            try:
                error_json = response.json()
                error_detail += f", 错误信息: {json.dumps(error_json, ensure_ascii=False)}"
            except:
                error_detail += f", 响应内容: {response.text[:200]}"
                
            raise Exception(f"火山引擎API请求失败: {error_detail}")
            
        except Exception as e:
            self.logger.error(f"请求出错: {str(e)}")
            raise Exception(f"火山引擎API请求异常: {str(e)}")
    
    def chat_stream(self, model, messages, temperature=0.7, max_tokens=2000, stream_options=None):
        """流式请求火山引擎API"""
        if "r1" in model:
            self.logger.info(f"使用R1模型流式请求: {model}")
            # R1模型使用更长超时
            self.timeout = 180
            
        url = self.api_base
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "text/event-stream"  # 明确要求SSE格式
        }
        
        # 配置stream_options
        if stream_options is None:
            stream_options = {}
        
        include_usage = stream_options.get("include_usage", False)
        self.logger.info(f"流式请求配置: include_usage={include_usage}")
        
        # 按照官方文档格式构建payload
        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }
        
        # 添加可选参数
        if temperature != 0.7:
            payload["temperature"] = temperature
        
        if max_tokens != 2000:
            payload["max_tokens"] = max_tokens
        
        # 如果需要包含token用量信息
        if include_usage:
            payload["stream_options"] = {"include_usage": True}
        
        # 为R1模型添加return_reasoning参数，启用思考过程返回
        if "r1" in model.lower():
            self.logger.info("启用R1模型思考过程返回")
            payload["return_reasoning"] = True
        
        try:
            self.logger.debug(f"发送流式请求到火山引擎API: {url}, 模型: {model}, 参数: {json.dumps(payload, ensure_ascii=False)[:200]}...")
            start_time = time.time()
            response_content = ""
            
            # 发送SSE请求
            response = requests.post(
                url, 
                headers=headers, 
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            
            self.logger.debug(f"收到流式响应，状态码: {response.status_code}, 内容类型: {response.headers.get('Content-Type', '')}")
            response.raise_for_status()
            
            # 处理SSE响应流
            for line in response.iter_lines():
                if not line:
                    continue
                
                line_text = line.decode('utf-8')
                self.logger.debug(f"收到SSE行: {line_text[:100]}")
                
                # 处理[DONE]结束标记
                if line_text.strip() == "data: [DONE]" or line_text.strip() == "[DONE]":
                    self.logger.info("收到SSE流结束标记")
                    break
                
                # 解析SSE行
                if line_text.startswith("data: "):
                    data_content = line_text[6:].strip()
                    
                    try:
                        # 解析SSE数据
                        json_data = json.loads(data_content)
                        self.logger.debug(f"解析SSE数据: {json.dumps(json_data, ensure_ascii=False)[:100]}...")
                        
                        # 直接传递解析后的JSON数据
                        yield json_data
                        
                        # 提取内容用于日志统计
                        if "choices" in json_data and json_data["choices"]:
                            choice = json_data["choices"][0]
                            if "delta" in choice and "content" in choice["delta"]:
                                content = choice["delta"]["content"]
                                if content:
                                    response_content += content
                    
                    except json.JSONDecodeError as e:
                        self.logger.error(f"解析SSE数据JSON出错: {str(e)}, 数据: {data_content[:200]}")
                    except Exception as e:
                        self.logger.error(f"处理SSE数据出错: {str(e)}")
                
                # 尝试直接解析JSON行
                elif line_text.startswith("{") and line_text.endswith("}"):
                    try:
                        json_data = json.loads(line_text)
                        self.logger.debug(f"解析直接JSON数据: {json.dumps(json_data, ensure_ascii=False)[:100]}...")
                        
                        # 直接传递解析后的JSON数据
                        yield json_data
                        
                        # 提取内容用于日志统计
                        if "choices" in json_data and json_data["choices"]:
                            choice = json_data["choices"][0]
                            if "delta" in choice and "content" in choice["delta"]:
                                content = choice["delta"]["content"]
                                if content:
                                    response_content += content
                    except json.JSONDecodeError as e:
                        self.logger.error(f"解析直接JSON数据出错: {str(e)}, 数据: {line_text[:200]}")
                    except Exception as e:
                        self.logger.error(f"处理直接JSON数据出错: {str(e)}")
            
            # 记录统计信息
            duration = time.time() - start_time
            self.logger.info(f"流式响应完成, 耗时: {duration:.2f}秒, 内容长度: {len(response_content)}字符")
            
        except requests.exceptions.Timeout:
            self.logger.error(f"流式请求超时: 模型={model}, 超时设置={self.timeout}秒")
            error_data = {
                "error": {
                    "message": f"火山引擎API流式请求超时 (>{self.timeout}秒)",
                    "type": "timeout"
                }
            }
            yield error_data
            
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"流式连接错误: {str(e)}")
            error_data = {
                "error": {
                    "message": f"无法连接到火山引擎API: {str(e)}",
                    "type": "connection_error"
                }
            }
            yield error_data
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"流式HTTP错误: {str(e)}, 状态码: {response.status_code}")
            error_detail = f"状态码: {response.status_code}"
            try:
                error_json = response.json()
                error_detail += f", 错误信息: {json.dumps(error_json, ensure_ascii=False)}"
            except:
                error_detail += f", 响应内容: {response.text[:200]}"
                
            error_data = {
                "error": {
                    "message": f"火山引擎API流式请求失败: {error_detail}",
                    "type": "http_error"
                }
            }
            yield error_data
            
        except Exception as e:
            self.logger.error(f"流式请求处理异常: {str(e)}")
            error_data = {
                "error": {
                    "message": f"火山引擎API流式请求异常: {str(e)}",
                    "type": "unknown_error"
                }
            }
            yield error_data
    
    def _convert_response(self, response):
        """将火山引擎API响应转换为统一格式"""
        try:
            if "output" in response:
                output = response["output"]
                # 火山引擎格式转换为OpenAI格式
                return {
                    "id": output.get("id", ""),
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": response.get("model", ""),
                    "choices": output.get("choices", [])
                }
            return response
        except Exception as e:
            self.logger.error(f"转换响应格式出错: {str(e)}")
            return response
            
    def _convert_stream_response(self, response, is_r1_model=False):
        """将火山引擎流式响应转换为统一格式"""
        try:
            if "output" in response:
                output = response["output"]
                
                # 火山引擎流式格式转换
                result = {
                    "data": {
                        "id": output.get("id", ""),
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": response.get("model", ""),
                        "choices": []
                    }
                }
                
                # 处理choices
                if "choices" in output and len(output["choices"]) > 0:
                    choice = output["choices"][0]
                    
                    # 提取delta部分
                    if "delta" in choice:
                        delta = choice["delta"]
                        result_choice = {
                            "index": choice.get("index", 0),
                            "delta": {}
                        }
                        
                        # 常规content字段
                        if "content" in delta:
                            result_choice["delta"]["content"] = delta["content"]
                            
                        # R1模型的思考过程
                        if is_r1_model and "reasoning_content" in delta:
                            result_choice["delta"]["reasoning_content"] = delta["reasoning_content"]
                            
                        result["data"]["choices"].append(result_choice)
                
                return result
                
            return {"data": response}
        except Exception as e:
            self.logger.error(f"转换流式响应格式出错: {str(e)}")
            return {"data": response}

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
                      presence_penalty=0.0, stop=None, stream=False):
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
                api_key = "026f661d-3948-42e1-acdd-81e64e62da1b"
            else:
                # 使用用户提供的有效密钥
                api_key = "03824a7c-e453-4ccd-b356-e7f80a793add"
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
                   top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, 
                   stream=False, stream_options=None):
    """统一的聊天接口"""
    
    # 添加日志记录
    logger = logging.getLogger("chat_completion")
    logger.setLevel(logging.DEBUG)
    
    logger.info(f"chat_completion调用: model_name={model_name}, temperature={temperature}, max_tokens={max_tokens}, stream={stream}(类型:{type(stream)})")
    if stream:
        logger.info(f"流式选项: {json.dumps(stream_options, ensure_ascii=False) if stream_options else 'None'}")
    
    # 获取API客户端
    client, model_info = get_api_client(model_name)
    if not client:
        logger.error(f"获取API客户端失败: {model_info}")
        return model_info
    
    logger.info(f"已获取API客户端: {type(client).__name__}, 模型信息: {json.dumps(model_info, ensure_ascii=False)}")
    
    # 调用对应的模型API
    api_type = model_info.get("api_type")
    logger.info(f"API类型: {api_type}")
    
    # 根据不同的API类型调用不同的方法
    try:
        if api_type == "volcano":
            # 火山引擎API使用新的chat方法
            if stream:
                logger.info(f"调用火山引擎流式API: model={model_info['model_id']}")
                result = client.chat_stream(
                    model=model_info["model_id"],
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream_options=stream_options
                )
                logger.info(f"火山引擎流式API返回结果类型: {type(result).__name__}")
                return result
            else:
                logger.info(f"调用火山引擎普通API: model={model_info['model_id']}")
                result = client.chat(
                    model=model_info["model_id"],
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                logger.info(f"火山引擎普通API返回结果类型: {type(result).__name__}")
                return result
        else:
            # 其他API类型仍然使用旧方法
            logger.info(f"调用其他API类型: {api_type}, model_id={model_info['model_id']}")
            result = client.chat_completion(
                messages=messages,
                model_id=model_info["model_id"],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=None,
                stream=stream
            )
            logger.info(f"其他API类型返回结果类型: {type(result).__name__}")
            return result
    except Exception as e:
        logger.exception(f"调用API出错: {str(e)}")
        return {
            "error": {
                "message": f"调用API出错: {str(e)}",
                "type": "api_error",
                "code": "call_error"
            }
        } 