#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
论文大纲编写API
通过百度文心API生成论文大纲
支持流式响应，将百度文心API的SSE结果转发给客户端
"""

import os
import json
import time
import requests
import hashlib
import base64
from urllib.parse import quote
from datetime import datetime, timedelta
from flask import Blueprint, request, Response, current_app, jsonify, stream_with_context, Request
import logging
import re
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.academic_paper import AcademicPaper
from sqlalchemy import text

academic_paper_bp = Blueprint('academic_paper', __name__)

# 添加对OPTIONS请求的处理
@academic_paper_bp.route('/paper_outline', methods=['OPTIONS'])
def paper_outline_options():
    """处理OPTIONS请求"""
    resp = jsonify({})
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return resp, 200

@academic_paper_bp.route('/generate-paper', methods=['OPTIONS'])
def generate_paper_options():
    """处理OPTIONS请求"""
    resp = jsonify({})
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return resp, 200

class WenchainClient:
    """百度文心API客户端"""
    
    def __init__(self, partner_id=None, api_secret=None):
        # 使用传入的凭证或默认使用硬编码的凭证
        self.partner_id = partner_id.strip() if partner_id else "8980934e767f5acfa1c7cd92"
        self.api_secret = api_secret.strip() if api_secret else "N64IJm!e#iAWsac"  # 硬编码的API密钥
        self.base_url = "https://wenchain.baidu.com/wenchain/partner"
        logging.info(f"初始化文心API客户端 PartnerID: {self.partner_id}")
    
    def _generate_timestamp(self):
        """
        生成当前北京时间的毫秒级时间戳
        文心API要求时间戳10分钟内有效
        """
        # 获取当前UTC时间
        utc_now = datetime.utcnow()
        # 转换为北京时间 (UTC+8)
        beijing_time = utc_now + timedelta(hours=8)
        # 转换为毫秒级时间戳
        ts_milliseconds = int(beijing_time.timestamp() * 1000)
        
        # 记录生成的时间戳
        logging.info("=" * 50)
        logging.info("时间戳生成详情:")
        logging.info(f"UTC时间: {utc_now}")
        logging.info(f"北京时间: {beijing_time}")
        logging.info(f"毫秒级时间戳TS: {ts_milliseconds}")
        logging.info("注意：文心API要求时间戳必须是当前时间的10分钟内")
        logging.info("=" * 50)
        
        return ts_milliseconds
    
    def _generate_auth_header(self, ts):
        """
        生成认证头 - 格式: MD5(PartnerID+PartnerKey+TS)
        这里的+号是字符串的一部分，需要保留
        """
        # 构造签名字符串，保留+号
        string_to_sign = f"{self.partner_id}+{self.api_secret}+{str(ts)}"
        
        # 使用MD5生成签名
        signature = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()
        
        # 记录生成的认证头
        logging.info("=" * 50)
        logging.info("签名参数详情:")
        logging.info(f"PartnerID: {self.partner_id}")
        logging.info(f"PartnerKey: {self.api_secret}")
        logging.info(f"TS: {ts}")
        logging.info(f"拼接后的字符串: {string_to_sign}")
        logging.info(f"MD5签名结果: {signature}")
        logging.info("=" * 50)
        
        return signature
    
    def paper_outline(self, query, callback=None):
        """
        生成论文大纲
        
        Args:
            query: 用户查询字符串
            callback: 处理流式响应的回调函数
            
        Returns:
            Response对象 (当callback为None时)
        """
        # 增加日志
        logging.info(f"开始为查询生成论文大纲: '{query}'")
        
        # 检查参数
        if not query or not isinstance(query, str) or len(query.strip()) == 0:
            logging.error("无效的查询参数")
            return "无效的查询参数，请提供有效的研究主题"
            
        url = f"{self.base_url}/paperoutline"
        
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 准备请求头和请求体
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth,
            "Version": "1.0.1"  # 添加版本号，确保API兼容性
        }
        
        # 记录完整的请求信息用于调试
        logging.info("=" * 50)
        logging.info("请求头详细信息:")
        logging.info(f"Content-Type: {headers['Content-Type']}")
        logging.info(f"PartnerID: {headers['PartnerID']}")
        logging.info(f"TS: {headers['TS']}")
        logging.info(f"Authorization: {headers['Authorization']}")
        logging.info(f"Version: {headers['Version']}")
        logging.info(f"签名字符串: {self.partner_id + self.api_secret + str(ts)}")
        logging.info("=" * 50)
        logging.info(f"发送请求到百度文心API: URL={url}")
        
        data = {"userQuery": query}
        logging.info(f"请求体: {json.dumps(data)}")
        
        # 使用缓存检查是否有过去相同查询的结果
        cache_key = f"outline_{hashlib.md5(query.encode('utf-8')).hexdigest()}"
        cached_result = self._check_cache(cache_key)
        if cached_result:
            logging.info(f"从缓存找到结果，直接返回: {cache_key}")
            return cached_result
            
        try:
            # 使用流式响应
            response = requests.post(url, headers=headers, json=data, stream=True, timeout=30)
            
            # 记录响应状态和头信息
            logging.info(f"百度文心API响应状态码: {response.status_code}")
            logging.info(f"百度文心API响应头: {response.headers}")
            
            if response.status_code != 200:
                error_msg = f"百度文心API请求失败: HTTP {response.status_code}"
                logging.error(f"{error_msg} - {response.text}")
                # 创建一个简单的错误提示大纲
                error_outline = f"""# 生成论文大纲时出错

## 错误信息
- HTTP状态码: {response.status_code}
- 错误详情: {response.text[:100]}...

## 可能的原因
- API服务暂时不可用
- API凭证可能过期
- 网络连接问题

## 建议的解决方案
- 请稍后重试
- 联系系统管理员
"""
                return error_outline
                
            # 处理流式响应
            content = ""
            all_content = []
            saved_content = None  # 用于保存有效的大纲内容
            
            # 用于解析SSE格式
            current_event = None
            current_data = ""
            
            # 增加超时控制
            response_timeout = 60  # 60秒超时
            start_time = time.time()
            
            for line in response.iter_lines():
                # 检查超时
                if time.time() - start_time > response_timeout:
                    logging.error("处理响应超时，已超过60秒")
                    if content:
                        # 如果已经有部分内容，返回已处理的内容
                        self._save_to_cache(cache_key, content)
                        return content
                    else:
                        # 返回一个备用的大纲模板
                        fallback = self._generate_fallback_outline(query, error_msg)
                        self._save_to_cache(cache_key, fallback)
                        return fallback
                        
                if not line:
                    # 空行表示一个SSE消息的结束，处理当前消息
                    if current_data and current_event:
                        logging.debug(f"完整SSE消息: event={current_event}, data={current_data}")
                        
                        # 处理data部分
                        if current_event == "message" and current_data:
                            try:
                                data_obj = json.loads(current_data)
                                logging.debug(f"解析SSE数据: {data_obj}")
                                
                                # 记录每个消息以便调试
                                all_content.append(data_obj)
                                
                                # 如果有raw字段，提取内容
                                if data_obj.get("raw") and data_obj["raw"] and data_obj["raw"].get("data"):
                                    content_part = data_obj["raw"]["data"]
                                    logging.info(f"找到原始内容数据: {content_part[:100]}...")
                                    content += content_part
                                    if callback:
                                        callback(content_part)
                                    # 保存这个有效内容
                                    saved_content = data_obj
                                
                                # 处理actionContent字段但忽略"执行完成"
                                elif data_obj.get("actionContent") and data_obj["actionContent"] != "执行完成":
                                    content_part = data_obj["actionContent"]
                                    content += content_part
                                    if callback:
                                        callback(content_part)
                                        
                                # 检查是否有错误信息
                                if data_obj.get("errCode") and data_obj["errCode"] != 0:
                                    error_msg = data_obj.get("errMsg", "未知错误")
                                    logging.error(f"API返回错误: {data_obj['errCode']} - {error_msg}")
                                    # 返回一个备用的大纲模板
                                    fallback = self._generate_fallback_outline(query, error_msg)
                                    self._save_to_cache(cache_key, fallback)
                                    return fallback
                            except json.JSONDecodeError as e:
                                logging.error(f"JSON解析错误: {e} - {current_data}")
                        
                        # 重置当前消息
                        current_event = None
                        current_data = ""
                    continue
                    
                line_str = line.decode('utf-8')
                logging.debug(f"接收到原始数据行: {line_str}")
                
                # 解析SSE格式
                if line_str.startswith("event:"):
                    current_event = line_str[6:].strip()
                elif line_str.startswith("data:"):
                    current_data = line_str[5:].strip()
            
            # 最后处理流式响应的结果
            logging.info(f"收到 {len(all_content)} 条SSE消息")
            
            # 如果没有找到内容但有保存的消息，尝试从最后一条提取
            if not content and all_content:
                logging.info("没有直接找到内容，尝试从所有响应中提取")
                # 尝试从所有消息中提取有用信息
                extracted_content = self._extract_outline_from_responses(all_content)
                if extracted_content:
                    self._save_to_cache(cache_key, extracted_content)
                    return extracted_content
                # 没找到内容，返回备用大纲
                fallback = self._generate_fallback_outline(query)
                self._save_to_cache(cache_key, fallback)
                return fallback
            
            if not content:
                logging.error("没有找到任何有效内容")
                # 返回一个备用的大纲模板
                fallback = self._generate_fallback_outline(query)
                self._save_to_cache(cache_key, fallback)
                return fallback
                
            # 保存到缓存
            self._save_to_cache(cache_key, content)
            return content
        except requests.exceptions.Timeout:
            error_msg = "请求百度文心API超时"
            logging.error(error_msg)
            # 返回一个备用的大纲模板
            fallback = self._generate_fallback_outline(query, error_msg)
            self._save_to_cache(cache_key, fallback)
            return fallback
        except requests.exceptions.ConnectionError:
            error_msg = "无法连接到百度文心API服务"
            logging.error(error_msg)
            # 返回一个备用的大纲模板
            fallback = self._generate_fallback_outline(query, error_msg)
            self._save_to_cache(cache_key, fallback)
            return fallback
        except Exception as e:
            error_msg = str(e)
            logging.error(f"请求异常: {error_msg}")
            # 返回一个备用的大纲模板
            fallback = self._generate_fallback_outline(query, error_msg)
            self._save_to_cache(cache_key, fallback)
            return fallback
            
    def _check_cache(self, key):
        """检查缓存中是否有结果"""
        cache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', f"{key}.json")
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    # 检查缓存是否过期 (24小时)
                    if time.time() - cache_data['timestamp'] < 86400:
                        return cache_data['content']
        except Exception as e:
            logging.error(f"读取缓存出错: {e}")
        return None
        
    def _save_to_cache(self, key, content):
        """保存结果到缓存"""
        try:
            cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
            os.makedirs(cache_dir, exist_ok=True)
            
            cache_file = os.path.join(cache_dir, f"{key}.json")
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': time.time(),
                    'content': content
                }, f, ensure_ascii=False)
        except Exception as e:
            logging.error(f"保存缓存出错: {e}")
            
    def _generate_fallback_outline(self, query, error_msg=None):
        """生成一个备用的大纲模板"""
        # 从查询中提取关键词
        keywords = [word for word in query.split() if len(word) > 1]
        if not keywords:
            keywords = ["研究主题"]
            
        # 创建标题
        title = f"# {query}"
        
        # 如果有错误信息，创建一个带有错误提示的大纲
        if error_msg:
            return f"""{title}

## 注意：系统生成大纲时遇到问题
- 错误信息: {error_msg}
- 以下是系统自动生成的基础大纲，您可以根据需要修改

## 一、引言
- 研究背景
- 研究意义
- 研究目的与问题

## 二、文献综述
- 概念界定
- 国内外研究现状
- 研究评述

## 三、研究方法
- 研究设计
- 数据收集
- 分析方法

## 四、研究结果
- 主要发现
- 数据分析
- 结果讨论

## 五、结论与建议
- 研究总结
- 研究局限
- 未来研究方向

## 参考文献
- 国内文献
- 国外文献
"""
        
        # 创建一个基本的大纲模板
        return f"""{title}

## 一、引言
### 1.1 研究背景
   - {query}的发展历程
   - 当前研究现状
   - 存在的问题与挑战

### 1.2 研究意义
   - 理论意义
   - 实践意义
   - 社会价值

### 1.3 研究目的与问题
   - 主要研究目标
   - 关键研究问题
   - 研究范围界定

## 二、文献综述
### 2.1 概念界定
   - {keywords[0] if keywords else '关键概念'}的定义
   - 相关理论基础
   - 概念框架

### 2.2 国内外研究现状
   - 国际研究进展
   - 国内研究成果
   - 研究方法比较

### 2.3 研究评述
   - 现有研究的成就
   - 研究中存在的问题
   - 本研究的切入点

## 三、研究方法
### 3.1 研究设计
   - 研究框架
   - 研究假设
   - 变量定义

### 3.2 数据收集
   - 研究对象
   - 数据来源
   - 收集方法

### 3.3 分析方法
   - 定量分析方法
   - 定性分析方法
   - 模型构建

## 四、研究结果
### 4.1 主要发现
   - 关键结果展示
   - 假设验证
   - 结果解释

### 4.2 数据分析
   - 统计分析
   - 图表展示
   - 数据解读

### 4.3 结果讨论
   - 与现有研究的对比
   - 结果的理论意义
   - 实践启示

## 五、结论与建议
### 5.1 研究总结
   - 主要结论
   - 理论贡献
   - 实践价值

### 5.2 研究局限
   - 方法局限
   - 样本局限
   - 其他限制因素

### 5.3 未来研究方向
   - 理论扩展方向
   - 方法改进建议
   - 新的研究问题

## 参考文献
- 国内文献
- 国外文献
"""
    
    def _extract_outline_from_responses(self, responses):
        """
        从响应消息列表中提取大纲内容
        
        Args:
            responses: 响应消息列表
            
        Returns:
            提取的大纲内容或None
        """
        try:
            # 按不同的字段尝试提取内容
            for resp in responses:
                # 尝试提取常见字段
                if isinstance(resp, dict):
                    # 检查raw.data字段
                    if resp.get("raw") and resp["raw"].get("data"):
                        return resp["raw"]["data"]
                    
                    # 检查data字段
                    if resp.get("data") and isinstance(resp["data"], str):
                        return resp["data"]
                    
                    # 检查content字段
                    if resp.get("content") and isinstance(resp["content"], str):
                        return resp["content"]
                    
                    # 检查actionContent字段
                    if resp.get("actionContent") and isinstance(resp["actionContent"], str):
                        return resp["actionContent"]
            
            # 如果没有找到任何内容，返回None
            return None
        except Exception as e:
            logging.error(f"提取大纲内容时出错: {str(e)}")
            return None
    
    def generate_full_paper(self, query, outline):
        """
        根据大纲生成完整论文 - 使用outlinetopaper接口
        
        Args:
            query: 用户查询字符串
            outline: 论文大纲
            
        Returns:
            生成的论文内容
        """
        # 首先调用paperoutline接口获取queryID
        query_id = self._get_query_id_from_outline(query)
        
        if not query_id:
            return "生成论文失败：无法获取有效的queryID"
            
        logging.info(f"[论文生成]成功获取queryID: {query_id}")
        
        # 转换大纲为规范的markdown格式
        markdown_outline = self._convert_outline_to_markdown(outline)
        logging.info(f"[论文生成]转换后的markdown大纲:\n{markdown_outline}")
        
        # 然后使用获取到的queryID调用outlinetopaper接口生成论文
        url = f"{self.base_url}/outlinetopaper"
        
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth
        }
        
        # 构建请求体 - 严格按照官方文档参数规范
        data = {
            "queryID": query_id,                # 必填项，使用paperoutline接口返回的queryID
            "userQuery": query.strip(),         # 非必填项，用户描述
            "outline": markdown_outline         # 必填项，markdown内容
        }
        
        logging.info("=" * 80)
        logging.info("[论文生成]开始请求:")
        logging.info(f"请求URL: {url}")
        logging.info(f"请求头: PartnerID={self.partner_id}, TS={ts}, Auth={auth}")
        logging.info(f"请求参数: {json.dumps(data, ensure_ascii=False)}")
        logging.info("=" * 80)
        
        try:
            # 发送请求，使用标准模式而非流式传输
            response = requests.post(url, headers=headers, json=data)
            
            # 记录响应状态和详情
            logging.info(f"[论文生成]API响应状态码: {response.status_code}")
            logging.info(f"[论文生成]API响应头: {response.headers}")
            logging.info(f"[论文生成]API响应内容: {response.text[:1000]}")
            
            if response.status_code != 200:
                error_msg = f"API请求失败：HTTP {response.status_code}"
                logging.error(f"[论文生成]{error_msg} - {response.text}")
                return f"生成论文失败：{error_msg}"
            
            # 尝试解析JSON响应
            try:
                resp_data = response.json()
                
                # 检查错误码
                if resp_data.get("errCode", 0) != 0:
                    error_msg = resp_data.get("errMsg", "未知错误")
                    error_code = resp_data.get("errCode")
                    
                    logging.error(f"[论文生成]API返回错误: {error_code} - {error_msg}")
                    
                    # 如果是TS过期，重新尝试一次
                    if error_code == 200003:  # TS expires
                        logging.info("[论文生成]时间戳过期，重新尝试...")
                        time.sleep(1)  # 等待1秒
                        return self.generate_full_paper(query, outline)  # 重试一次
                    
                    # 如果是参数错误，尝试最后一种方案 - 直接使用paperoutline生成全文
                    if error_code == 200004:  # Params error
                        logging.error(f"[论文生成]参数错误详情: {json.dumps(data, ensure_ascii=False)}")
                        logging.info("[论文生成]尝试使用paperoutline直接生成全文...")
                        return self._generate_full_paper_with_paperoutline(query, outline)
                        
                    # 返回明确的错误信息
                    return f"生成论文失败: 错误码 {error_code}, {error_msg}"
                
                # 处理成功响应
                if resp_data.get("raw") and isinstance(resp_data["raw"], dict):
                    # 检查是否有docID字段，这通常表示异步生成
                    if resp_data["raw"].get("docID"):
                        doc_id = resp_data["raw"]["docID"]
                        logging.info(f"[论文生成]获取到docID: {doc_id}")
                        return f"论文生成任务已提交，文档ID: {doc_id}，完整论文生成后可通过此ID获取"
                    
                    # 检查是否有直接的内容返回
                    if resp_data["raw"].get("data"):
                        content = resp_data["raw"]["data"]
                        logging.info(f"[论文生成]获取到论文内容，长度: {len(content)}")
                        return content
                
                # 检查其他字段中是否有内容
                if resp_data.get("actionContent") and resp_data["actionContent"] != "执行完成" and resp_data["actionContent"] != "正在执行中":
                    content = resp_data["actionContent"]
                    logging.info(f"[论文生成]从actionContent获取内容，长度: {len(content)}")
                    return content
                
                # 没有找到具体内容，但API调用成功，返回原始响应供调试
                logging.warning("[论文生成]响应中没有找到有效内容")
                return f"API调用成功但未返回预期内容。API响应: {json.dumps(resp_data)}"
                
            except json.JSONDecodeError:
                error_msg = "响应不是有效的JSON格式"
                logging.error(f"[论文生成]{error_msg}: {response.text[:200]}")
                return f"生成论文失败: {error_msg}"
                
        except Exception as e:
            error_msg = str(e)
            logging.error(f"[论文生成]请求异常: {error_msg}")
            return f"生成论文时发生错误: {error_msg}"
            
    def _convert_outline_to_markdown(self, outline):
        """
        将大纲转换为规范的markdown格式，遵循层级结构
        
        Args:
            outline: 原始大纲文本
            
        Returns:
            规范的markdown格式大纲
        """
        # 如果大纲已经是markdown格式，直接返回
        if outline.startswith('#'):
            return outline
            
        lines = outline.strip().split('\n')
        markdown_lines = []
        
        # 标题层级计数
        chapter_count = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                markdown_lines.append('')
                continue
                
            # 判断标题层级
            if line.startswith('一、') or line.startswith('二、') or line.startswith('三、') or \
               line.startswith('四、') or line.startswith('五、') or line.startswith('六、') or \
               line.startswith('七、') or re.match(r'^[一二三四五六七八九十]+[、\.]', line) or \
               re.match(r'^[1-9][0-9]*[、\.]', line) and not re.match(r'^[1-9][0-9]*\.[1-9][0-9]*', line):
                # 一级标题 - 只有第一个章节标题用一个#，其余用##
                chapter_count += 1
                if chapter_count == 1:
                    markdown_lines.append(f'# {line}')
                else:
                    markdown_lines.append(f'## {line}')
            elif re.match(r'^[1-9][0-9]*\.[1-9][0-9]*', line):
                # 二级标题 - 用##或###，根据是否是第一章来决定
                if chapter_count == 1:
                    markdown_lines.append(f'## {line}')
                else:
                    markdown_lines.append(f'### {line}')
            else:
                # 文本描述或其他内容
                markdown_lines.append(line)
                
        return '\n'.join(markdown_lines)
        
    def _generate_full_paper_with_paperoutline(self, query, outline):
        """
        使用paperoutline接口直接生成完整论文
        
        Args:
            query: 用户查询字符串
            outline: 论文大纲
            
        Returns:
            生成的论文内容
        """
        url = f"{self.base_url}/paperoutline"
        
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth
        }
        
        # 设计更明确的提示语，强调要生成完整论文而非大纲
        user_query = f"""我需要一篇关于"{query}"的完整学术论文，不是大纲，请根据以下大纲生成完整详细的论文内容。

大纲结构如下：
{outline}

注意：
1. 请生成完整的学术论文，包含所有章节的详细内容，不要只返回大纲
2. 针对每个章节和小节，撰写详细的内容，每个章节内容至少500字
3. 论文格式应包含：标题、摘要、关键词、引言、正文各章节、结论和参考文献
4. 内容要有学术性和专业性，包含适当的引用和参考文献
5. 语言要流畅、逻辑性强，避免重复和冗余
6. 直接输出完整论文的内容，不要输出"下面是论文内容"之类的提示
7. 不要再输出大纲结构

重点：这是一个生成完整学术论文的任务，不是生成大纲的任务，请直接输出一篇完整的学术论文。"""
        
        data = {"userQuery": user_query}
        
        logging.info("=" * 80)
        logging.info("[论文生成-备选方案]尝试使用paperoutline直接生成论文:")
        logging.info(f"请求URL: {url}")
        logging.info(f"请求参数: {json.dumps(data, ensure_ascii=False)}")
        logging.info("=" * 80)
        
        try:
            # 发送请求
            response = requests.post(url, headers=headers, json=data, stream=True)
            
            # 记录响应状态
            logging.info(f"[论文生成-备选方案]API响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                logging.error(f"[论文生成-备选方案]API请求失败: {response.status_code}")
                return "生成论文失败: API请求错误"
            
            # 处理流式响应
            content = ""
            all_data_objects = []
            
            # 解析SSE格式
            current_event = None
            current_data = ""
            
            for line in response.iter_lines():
                if not line:
                    # 空行表示一个SSE消息的结束，处理当前消息
                    if current_data and current_event:
                        logging.debug(f"[论文生成-备选方案]完整SSE消息: event={current_event}, data={current_data[:100]}...")
                        
                        # 处理data部分
                        if current_event == "message" and current_data:
                            try:
                                data_obj = json.loads(current_data)
                                all_data_objects.append(data_obj)
                                
                                # 提取raw.data中的内容
                                if data_obj.get("raw") and data_obj["raw"] and data_obj["raw"].get("data"):
                                    content_part = data_obj["raw"]["data"]
                                    content += content_part
                                    logging.debug(f"[论文生成-备选方案]从raw.data获取内容: {len(content_part)}字符")
                                
                                # 提取actionContent中的内容
                                elif data_obj.get("actionContent") and data_obj["actionContent"] != "执行完成" and data_obj["actionContent"] != "正在执行中":
                                    content_part = data_obj["actionContent"]
                                    content += content_part
                                    logging.debug(f"[论文生成-备选方案]从actionContent获取内容: {len(content_part)}字符")
                            except json.JSONDecodeError as e:
                                logging.error(f"[论文生成-备选方案]JSON解析错误: {e} - {current_data[:100]}")
                        
                        # 重置当前消息
                        current_event = None
                        current_data = ""
                    continue
                    
                line_str = line.decode('utf-8')
                
                # 解析SSE格式
                if line_str.startswith("event:"):
                    current_event = line_str[6:].strip()
                elif line_str.startswith("data:"):
                    current_data = line_str[5:].strip()
            
            # 记录接收到的所有数据对象数量
            logging.info(f"[论文生成-备选方案]总共收到{len(all_data_objects)}个数据对象")
            
            # 如果上面的方法没有提取到内容，尝试从完整响应中提取
            if not content:
                logging.warning("[论文生成-备选方案]未从流式响应中提取到内容，尝试从完整响应中提取")
                # 分析所有收集的数据对象
                for data_obj in all_data_objects:
                    if data_obj.get("raw") and data_obj["raw"] and data_obj["raw"].get("data"):
                        content += data_obj["raw"]["data"]
                    elif data_obj.get("actionContent") and data_obj["actionContent"] != "执行完成" and data_obj["actionContent"] != "正在执行中":
                        content += data_obj["actionContent"]
            
            # 清理内容，移除描述性标记、整理格式
            content = self._clean_paper_content(content)
            
            if content:
                # 检查内容是否仍然是大纲格式
                if self._is_outline_format(content):
                    logging.warning("[论文生成-备选方案]返回内容仍是大纲格式，尝试添加更多内容生成指示")
                    # 如果仍然只有大纲，给用户明确提示
                    return f"""生成的内容仍是大纲格式，需要手动展开。建议参考以下大纲撰写完整论文：

{content}

请按此大纲展开撰写，每个章节需详细阐述相关内容。"""
                else:
                    logging.info(f"[论文生成-备选方案]成功生成论文内容，长度: {len(content)}")
                    return content
            else:
                return "生成论文失败: 未获取到有效内容"
                
        except Exception as e:
            error_msg = str(e)
            logging.error(f"[论文生成-备选方案]请求异常: {error_msg}")
            return f"生成论文时发生错误: {error_msg}"
            
    def _is_outline_format(self, content):
        """
        判断内容是否仍是大纲格式而非详细论文
        
        Args:
            content: 生成的内容
            
        Returns:
            布尔值，True表示是大纲格式
        """
        # 计算内容中标题行的比例
        lines = content.split('\n')
        title_count = 0
        non_empty_lines = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            non_empty_lines += 1
            
            # 统计以#开头的markdown标题行
            if line.startswith('#'):
                title_count += 1
                
            # 统计数字编号开头的行
            elif re.match(r'^(\d+\.)+\s', line):
                title_count += 1
        
        # 如果标题行占比超过50%或者总行数少于30行，认为是大纲格式
        if non_empty_lines > 0:
            title_ratio = title_count / non_empty_lines
            logging.info(f"[论文生成-备选方案]内容分析: 总行数={non_empty_lines}, 标题行数={title_count}, 标题占比={title_ratio:.2f}")
            
            if title_ratio > 0.5 or non_empty_lines < 30:
                return True
                
        # 每个章节应有足够的内容，计算平均每节内容的字符数
        content_blocks = re.split(r'^#+ ', content, flags=re.MULTILINE)[1:]  # 分割各章节
        if content_blocks:
            avg_block_size = sum(len(block) for block in content_blocks) / len(content_blocks)
            logging.info(f"[论文生成-备选方案]章节分析: 章节数={len(content_blocks)}, 平均每节字符数={avg_block_size:.2f}")
            
            # 如果平均每节内容少于200字符，认为是大纲格式
            if avg_block_size < 200:
                return True
                
        return False

    def _get_query_id_from_outline(self, query):
        """
        调用paperoutline接口获取queryID
        
        Args:
            query: 用户查询字符串
            
        Returns:
            获取到的queryID或None
        """
        url = f"{self.base_url}/paperoutline"
        
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 准备请求头和请求体
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth
        }
        
        data = {"userQuery": query}
        
        logging.info("=" * 80)
        logging.info("[获取queryID]正在请求paperoutline接口:")
        logging.info(f"请求URL: {url}")
        logging.info(f"请求参数: {json.dumps(data, ensure_ascii=False)}")
        logging.info("=" * 80)
        
        try:
            # 发送请求
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code != 200:
                logging.error(f"[获取queryID]请求失败: HTTP {response.status_code}")
                return None
            
            # 从响应中提取queryID
            try:
                # 尝试从响应头中获取queryID
                query_id = response.headers.get("QueryID") or response.headers.get("queryID")
                if query_id:
                    logging.info(f"[获取queryID]从响应头中获取到queryID: {query_id}")
                    return query_id
                
                # 尝试从非SSE响应中获取
                try:
                    resp_data = response.json()
                    if resp_data.get("queryID"):
                        query_id = resp_data["queryID"]
                        logging.info(f"[获取queryID]从响应JSON中获取到queryID: {query_id}")
                        return query_id
                    
                    # 尝试从raw字段获取
                    if resp_data.get("raw") and isinstance(resp_data["raw"], dict) and resp_data["raw"].get("queryID"):
                        query_id = resp_data["raw"]["queryID"]
                        logging.info(f"[获取queryID]从raw字段获取到queryID: {query_id}")
                        return query_id
                except:
                    # 如果解析JSON失败，可能是SSE响应
                    pass
                
                # 如果响应是SSE格式，逐行解析
                # 保存响应内容便于调试
                content = response.text
                logging.info(f"[获取queryID]收到响应: {content[:500]}...")
                
                # 解析响应中的JSON对象，寻找queryID
                import re
                json_objects = re.findall(r'data:\s*({.*?})(?:\n|$)', content)
                for json_obj in json_objects:
                    try:
                        data_obj = json.loads(json_obj)
                        if data_obj.get("queryID"):
                            query_id = data_obj["queryID"]
                            logging.info(f"[获取queryID]从SSE消息中找到queryID: {query_id}")
                            return query_id
                        
                        # 尝试从raw字段获取
                        if data_obj.get("raw") and isinstance(data_obj["raw"], dict) and data_obj["raw"].get("queryID"):
                            query_id = data_obj["raw"]["queryID"]
                            logging.info(f"[获取queryID]从SSE消息的raw字段找到queryID: {query_id}")
                            return query_id
                            
                        # 尝试从logID获取
                        if data_obj.get("logID"):
                            query_id = data_obj["logID"]
                            logging.info(f"[获取queryID]使用logID作为queryID: {query_id}")
                            return query_id
                    except:
                        continue
                
                # 如果都未能找到有效的queryID，生成一个时间戳作为后备方案
                fallback_id = f"fallback_{int(time.time())}"
                logging.warning(f"[获取queryID]未找到有效queryID，使用后备ID: {fallback_id}")
                return fallback_id
                
            except Exception as e:
                logging.error(f"[获取queryID]解析响应失败: {str(e)}")
                return None
                
        except Exception as e:
            logging.error(f"[获取queryID]请求异常: {str(e)}")
            return None

    def _clean_paper_content(self, content):
        """清理论文内容，移除【描述】等标记"""
        if not content:
            return content
        
        # 移除【描述】标记及其内容
        import re
        clean_content = re.sub(r'【描述】.*?(\n|$)', '', content)
        
        # 移除多余的空行
        clean_content = re.sub(r'\n{3,}', '\n\n', clean_content)
        
        return clean_content

    def download_paper(self, doc_id):
        """
        下载论文文档
        
        Args:
            doc_id: 文档ID
            
        Returns:
            文档下载链接
        """
        base_url = "https://wenchain.baidu.com/wenchain/partner"
        url = f"{base_url}/download"
        
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth,
            "Version": "1.0.1" # 添加版本号
        }
        
        # 准备请求体
        data = {
            "docID": doc_id
        }
        
        logging.info("=" * 80)
        logging.info("[论文下载]开始请求:")
        logging.info(f"请求URL: {url}")
        logging.info(f"请求头: PartnerID={self.partner_id}, TS={ts}, Auth={auth}")
        logging.info(f"请求参数: {json.dumps(data, ensure_ascii=False)}")
        logging.info("=" * 80)
        
        try:
            # 发送请求
            response = requests.post(url, headers=headers, json=data)
            
            # 记录响应状态和详情
            logging.info(f"[论文下载]API响应状态码: {response.status_code}")
            logging.info(f"[论文下载]API响应头: {response.headers}")
            logging.info(f"[论文下载]API响应内容: {response.text[:1000]}")
            
            if response.status_code != 200:
                error_msg = f"API请求失败：HTTP {response.status_code}"
                logging.error(f"[论文下载]{error_msg} - {response.text}")
                return f"下载论文失败：{error_msg}"
            
            # 解析JSON响应
            try:
                resp_data = response.json()
                
                # 检查错误码
                if resp_data.get("errCode", 0) != 0:
                    error_msg = resp_data.get("errMsg", "未知错误")
                    error_code = resp_data.get("errCode")
                    
                    logging.error(f"[论文下载]API返回错误: {error_code} - {error_msg}")
                    return f"下载论文失败: 错误码 {error_code}, {error_msg}"
                
                # 提取下载链接 - 首先检查data.downloadLink
                if resp_data.get("data") and resp_data["data"].get("downloadLink"):
                    download_link = resp_data["data"]["downloadLink"]
                    logging.info(f"[论文下载]成功获取下载链接(data): {download_link}")
                    return download_link
                
                # 如果data中没有，检查raw字段中的download_link
                if resp_data.get("raw") and isinstance(resp_data["raw"], dict) and resp_data["raw"].get("download_link"):
                    download_link = resp_data["raw"]["download_link"]
                    logging.info(f"[论文下载]成功获取下载链接(raw): {download_link}")
                    return download_link
                
                # 检查错误信息中显示的格式：可能是在嵌套的raw字段中
                import re
                if resp_data.get("raw"):
                    raw_str = str(resp_data["raw"])
                    # 直接在raw字符串中查找URL
                    url_matches = re.findall(r'https?://[^\s"\']+', raw_str)
                    if url_matches:
                        download_link = url_matches[0]
                        logging.info(f"[论文下载]从raw字段中提取到URL: {download_link[:100]}...")
                        return download_link
                
                # 尝试在整个响应文本中查找URL
                url_matches = re.findall(r'https?://[^\s"\']+', response.text)
                if url_matches:
                    download_link = url_matches[0]
                    logging.info(f"[论文下载]从响应文本中提取到URL: {download_link[:100]}...")
                    return download_link
                
                # 没有找到下载链接
                logging.warning("[论文下载]响应中没有找到下载链接")
                logging.warning(f"[论文下载]完整响应: {json.dumps(resp_data, ensure_ascii=False)[:2000]}")
                return f"API调用成功但未返回下载链接。API响应: {json.dumps(resp_data, ensure_ascii=False)[:500]}..."
                
            except json.JSONDecodeError:
                error_msg = "响应不是有效的JSON格式"
                logging.error(f"[论文下载]{error_msg}: {response.text[:200]}")
                
                # 尝试从原始响应中提取URL
                import re
                url_matches = re.findall(r'https?://[^\s"\']+', response.text)
                if url_matches:
                    download_link = url_matches[0]
                    logging.info(f"[论文下载]从无效JSON响应中提取到URL: {download_link[:100]}...")
                    return download_link
                
                return f"下载论文失败: {error_msg}"
                
        except Exception as e:
            error_msg = str(e)
            logging.error(f"[论文下载]请求异常: {error_msg}")
            return f"下载论文时发生错误: {error_msg}"

    def check_document_status(self, doc_id):
        """
        检查文档生成状态
        
        Args:
            doc_id: 文档ID
            
        Returns:
            包含状态信息的字典: {"document_status": "generating/completed/failed", "message": "状态描述"}
        """
        if not doc_id:
            logging.error("[状态检查]文档ID为空")
            return {
                "document_status": "failed",
                "message": "文档ID不能为空"
            }
            
        logging.info(f"[状态检查]开始检查文档状态: {doc_id}")
        
        # 尝试下载文档来检查状态
        try:
            result = self.download_paper(doc_id)
            
            # 如果成功获取下载链接，说明文档已生成完成
            if isinstance(result, str) and result.startswith('http'):
                logging.info(f"[状态检查]文档已生成完成: {doc_id}")
                return {
                    "document_status": "completed",
                    "message": "文档已生成完成，可以下载"
                }
            else:
                # 检查是否包含特定错误码
                if "错误码 200009" in result or "File is generating" in result:
                    logging.info(f"[状态检查]文档正在生成中: {doc_id}")
                    return {
                        "document_status": "generating",
                        "message": "文档正在生成中，请稍后再试"
                    }
                else:
                    logging.error(f"[状态检查]文档生成失败: {doc_id}, 错误: {result}")
                    return {
                        "document_status": "failed",
                        "message": f"文档生成失败: {result}"
                    }
        except Exception as e:
            error_msg = str(e)
            logging.error(f"[状态检查]检查状态时出错: {error_msg}")
            return {
                "document_status": "failed",
                "message": f"检查状态失败: {error_msg}"
            }

    # 添加研报大纲生成方法
    def report_outline(self, content, rebuild_times=0, callback=None):
        """
        生成智能研报大纲
        
        Args:
            content: 用户指令内容
            rebuild_times: 重新生成次数，默认为0
            callback: 处理流式响应的回调函数
            
        Returns:
            Response对象 (当callback为None时)
        """
        url = f"{self.base_url}/wktradereportoutline"
        
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 准备请求头和请求体
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth,
            "Version": "1.0.1"
        }
        
        # 记录完整的请求信息用于调试
        logging.info("=" * 50)
        logging.info("研报大纲请求详细信息:")
        logging.info(f"请求URL: {url}")
        logging.info(f"Content-Type: {headers['Content-Type']}")
        logging.info(f"PartnerID: {headers['PartnerID']}")
        logging.info(f"TS: {headers['TS']}")
        logging.info(f"Authorization: {headers['Authorization']}")
        logging.info(f"Version: {headers['Version']}")
        logging.info(f"签名字符串: {self.partner_id + self.api_secret + str(ts)}")
        logging.info("=" * 50)
        
        data = {
            "content": content,
            "rebuildTimes": rebuild_times
        }
        logging.info(f"请求体: {json.dumps(data)}")
        
        try:
            # 使用流式响应
            response = requests.post(url, headers=headers, json=data, stream=True)
            
            # 记录响应状态和头信息
            logging.info(f"研报大纲API响应状态码: {response.status_code}")
            logging.info(f"研报大纲API响应头: {response.headers}")
            
            if response.status_code != 200:
                logging.error(f"研报大纲API请求失败: {response.status_code} - {response.text}")
                return None
                
            # 处理流式响应
            content = ""
            all_content = []
            saved_data = {} # 用于保存完整数据
            query_id = None # 用于保存queryID
            
            # 用于解析SSE格式
            current_event = None
            current_data = ""
            
            for line in response.iter_lines():
                if not line:
                    # 空行表示一个SSE消息的结束，处理当前消息
                    if current_data and current_event:
                        logging.debug(f"完整SSE消息: event={current_event}, data={current_data}")
                        
                        # 处理data部分
                        if current_data:
                            try:
                                data_obj = json.loads(current_data)
                                logging.debug(f"解析SSE数据: {data_obj}")
                                
                                # 记录每个消息以便调试
                                all_content.append(data_obj)
                                
                                # 提取queryID
                                if data_obj.get("queryID") and not query_id:
                                    query_id = data_obj["queryID"]
                                    logging.info(f"从消息中提取到queryID: {query_id}")
                                
                                # 提取raw字段中的outline内容
                                if data_obj.get("raw") and isinstance(data_obj["raw"], dict):
                                    # 从raw字段中提取queryID
                                    if data_obj["raw"].get("queryID") and not query_id:
                                        query_id = data_obj["raw"]["queryID"]
                                        logging.info(f"从raw字段中提取到queryID: {query_id}")
                                        
                                    if data_obj["raw"].get("outline"):
                                        outline_part = data_obj["raw"]["outline"]
                                        logging.info(f"找到大纲内容: {outline_part[:100]}...")
                                        content += outline_part
                                        if callback:
                                            callback(outline_part)
                                        
                                        # 保存大纲标题信息
                                        if data_obj["raw"].get("title"):
                                            saved_data["title"] = data_obj["raw"]["title"]
                                        if data_obj["raw"].get("subtitle"):
                                            saved_data["subtitle"] = data_obj["raw"]["subtitle"]
                                
                                # 处理actionContent字段但忽略"执行完成"和"正在执行中"
                                elif data_obj.get("actionContent") and data_obj["actionContent"] not in ["执行完成", "正在执行中"]:
                                    content_part = data_obj["actionContent"]
                                    content += content_part
                                    if callback:
                                        callback(content_part)
                            except json.JSONDecodeError as e:
                                logging.error(f"JSON解析错误: {e} - {current_data}")
                        
                        # 重置当前消息
                        current_event = None
                        current_data = ""
                    continue
                    
                line_str = line.decode('utf-8')
                logging.debug(f"接收到原始数据行: {line_str}")
                
                # 解析SSE格式
                if line_str.startswith("event:"):
                    current_event = line_str[6:].strip()
                elif line_str.startswith("data:"):
                    current_data = line_str[5:].strip()
            
            # 最后处理流式响应的结果
            logging.info(f"收到 {len(all_content)} 条SSE消息")
            
            # 如果没有找到内容但有保存的消息，尝试从最后一条提取
            if not content and saved_data:
                logging.info("没有直接找到内容，尝试从保存的数据中提取")
                if saved_data.get("title"):
                    content = f"# {saved_data['title']}\n\n"
                    if saved_data.get("subtitle"):
                        content += f"## {saved_data['subtitle']}\n\n"
            
            return {
                "content": content,
                "title": saved_data.get("title", ""),
                "subtitle": saved_data.get("subtitle", ""),
                "queryID": query_id
            }
        except Exception as e:
            logging.error(f"研报大纲请求异常: {str(e)}")
            return None

    def generate_full_report(self, title, outline, query_id=None):
        """
        根据大纲生成完整研报 - 调用百度文心接口
        
        Args:
            title: 研报标题
            outline: 研报大纲
            query_id: 大纲API返回的queryID (可选)
            
        Returns:
            生成的研报内容及文档ID
        """
        # 定义多种可能的API路径进行测试
        test_paths = [
            "/mdtotradereport",        # 根据文档名称猜测的路径（主要测试）
            "/wktradereportgenerate",  # 原来的路径
            "/tradereport",            # 简化路径猜测
            "/traderptgen",            # 简化路径猜测
            "/tradereport/generate",   # 带子路径猜测
            "/mdtotradereportgen"      # 变体路径猜测
        ]
        
        success_result = None
        all_errors = []
        
        # 循环尝试不同的API路径
        for api_path in test_paths:
            try:
                # 生成时间戳和认证头
                ts = self._generate_timestamp()
                auth = self._generate_auth_header(ts)
                
                # 构建完整URL
                url = f"{self.base_url}{api_path}"
                
                # 准备请求头
                headers = {
                    "Content-Type": "application/json",
                    "PartnerID": self.partner_id,
                    "TS": str(ts),
                    "Authorization": auth,
                    "Version": "1.0.1"
                }
                
                # 构建请求体
                data = {
                    "title": title.strip(),
                    "outline": outline
                }
                
                # 如果提供了queryID，添加到请求中
                if query_id:
                    data["queryID"] = query_id
                    logging.info(f"[研报生成][测试URL:{api_path}]使用queryID: {query_id}")
                
                logging.info("=" * 80)
                logging.info(f"[研报生成][测试URL:{api_path}]开始请求:")
                logging.info(f"请求URL: {url}")
                logging.info(f"请求头: PartnerID={self.partner_id}, TS={ts}, Auth={auth}")
                logging.info(f"请求参数: {json.dumps(data, ensure_ascii=False)[:500]}...")
                logging.info("=" * 80)
                print(f"[DEBUG][研报生成][测试URL:{api_path}]开始请求: {url}")
                
                # 发送请求
                start_time = time.time()
                response = requests.post(url, headers=headers, json=data, timeout=60)
                end_time = time.time()
                elapsed = end_time - start_time
                
                logging.info(f"[研报生成][测试URL:{api_path}]API请求耗时: {elapsed:.2f}秒, 状态码: {response.status_code}")
                print(f"[DEBUG][研报生成][测试URL:{api_path}]API请求耗时: {elapsed:.2f}秒, 状态码: {response.status_code}")
                
                # 检查响应状态码
                if response.status_code != 200:
                    error_msg = f"API请求返回错误状态码: {response.status_code}, 响应内容: {response.text}"
                    logging.error(f"[研报生成][测试URL:{api_path}]请求失败: {error_msg}")
                    print(f"[DEBUG][研报生成][测试URL:{api_path}]请求失败: {error_msg}")
                    all_errors.append(f"[{api_path}] {error_msg}")
                    continue  # 尝试下一个URL
                
                # 记录原始响应
                logging.info(f"[研报生成][测试URL:{api_path}]原始响应: {response.text}")
                print(f"[DEBUG][研报生成][测试URL:{api_path}]原始响应长度: {len(response.text)}")
                
                # 解析响应
                try:
                    # 判断响应是否为JSON
                    content_type = response.headers.get('Content-Type', '')
                    logging.info(f"[研报生成][测试URL:{api_path}]响应内容类型: {content_type}")
                    
                    result = None
                    if 'application/json' in content_type:
                        result = response.json()
                        logging.info(f"[研报生成][测试URL:{api_path}]响应JSON: {json.dumps(result, ensure_ascii=False)}")
                    else:
                        # 非JSON响应，尝试直接使用文本
                        result = response.text
                        logging.info(f"[研报生成][测试URL:{api_path}]非JSON响应: {result[:500]}...")
                        
                        # 尝试作为JSON解析
                        try:
                            result = json.loads(result)
                            logging.info(f"[研报生成][测试URL:{api_path}]成功将文本解析为JSON: {json.dumps(result, ensure_ascii=False)}")
                        except json.JSONDecodeError:
                            logging.info(f"[研报生成][测试URL:{api_path}]响应不是有效JSON，将作为字符串处理")
                    
                    # 检查响应是否包含所需数据 - 如果是字典类型
                    if isinstance(result, dict) and "error" in result:
                        error_msg = f"API返回错误: {result['error']}"
                        logging.error(f"[研报生成][测试URL:{api_path}]{error_msg}")
                        print(f"[DEBUG][研报生成][测试URL:{api_path}]{error_msg}")
                        all_errors.append(f"[{api_path}] {error_msg}")
                        continue  # 尝试下一个URL
                    
                    # 首先判断result的类型和内容
                    result_type = type(result).__name__
                    content_preview = str(result)[:200] if isinstance(result, str) else json.dumps(result, ensure_ascii=False)[:200]
                    logging.info(f"[研报生成][测试URL:{api_path}]结果类型: {result_type}, 内容摘要: {content_preview}")
                    print(f"[DEBUG][研报生成][测试URL:{api_path}]结果类型: {result_type}")
                    
                    doc_id = None
                    
                    # 如果result是字典，尝试获取docID字段
                    if isinstance(result, dict):
                        doc_id = result.get("docID")
                        logging.info(f"[研报生成][测试URL:{api_path}]从字典中提取的docID: {doc_id}")
                        
                        # 如果没有直接的docID字段，尝试在嵌套结构中查找
                        if not doc_id:
                            logging.info(f"[研报生成][测试URL:{api_path}]响应结构键值: {list(result.keys())}")
                            
                            # 尝试在其他可能的位置寻找docID
                            for key in ['data', 'result', 'response', 'resp', 'document', 'doc', 'id']:
                                if key in result and isinstance(result[key], dict) and 'docID' in result[key]:
                                    doc_id = result[key].get('docID')
                                    logging.info(f"[研报生成][测试URL:{api_path}]在嵌套结构{key}中找到docID: {doc_id}")
                                    break
                                elif key in result and isinstance(result[key], str) and len(result[key]) > 10:
                                    # 如果值是字符串且看起来像ID，也可以尝试使用
                                    doc_id = result[key]
                                    logging.info(f"[研报生成][测试URL:{api_path}]在嵌套结构{key}中找到可能的docID字符串: {doc_id}")
                                    break
                    
                    # 如果result本身就是字符串且看起来像docID，直接使用它
                    elif isinstance(result, str) and len(result) > 10:
                        doc_id = result.strip()
                        logging.info(f"[研报生成][测试URL:{api_path}]使用结果字符串作为docID: {doc_id}")
                    
                    if not doc_id:
                        logging.warning(f"[研报生成][测试URL:{api_path}]响应中未找到docID字段")
                        all_errors.append(f"[{api_path}] 响应中未找到docID字段")
                        continue  # 尝试下一个URL
                    
                    logging.info(f"[研报生成][测试URL:{api_path}]成功提取docID: {doc_id}")
                    print(f"[DEBUG][研报生成][测试URL:{api_path}]成功提取docID: {doc_id}")
                    
                    # 保存成功结果
                    success_result = (None, doc_id, f"research_report_generating_via_{api_path}")
                    logging.info(f"[研报生成]找到有效API路径: {api_path}")
                    print(f"[DEBUG][研报生成]找到有效API路径: {api_path}")
                    
                    # 成功找到有效API，跳出循环
                    break
                    
                except ValueError as e:
                    error_msg = f"解析响应JSON失败: {str(e)}, 响应内容: {response.text[:500]}..."
                    logging.error(f"[研报生成][测试URL:{api_path}]{error_msg}")
                    print(f"[DEBUG][研报生成][测试URL:{api_path}]{error_msg}")
                    all_errors.append(f"[{api_path}] {error_msg}")
                    continue  # 尝试下一个URL
                    
            except Exception as e:
                error_msg = str(e)
                logging.error(f"[研报生成][测试URL:{api_path}]请求异常: {error_msg}")
                print(f"[DEBUG][研报生成][测试URL:{api_path}]请求异常: {error_msg}")
                all_errors.append(f"[{api_path}] {error_msg}")
                continue  # 尝试下一个URL
        
        # 检查是否有成功结果
        if success_result:
            return success_result
        
        # 如果所有API路径都失败，返回错误
        error_summary = "\n".join(all_errors)
        logging.error(f"[研报生成]所有API路径都失败:\n{error_summary}")
        print(f"[DEBUG][研报生成]所有API路径都失败")
        return None, None, f"所有API路径都失败，请检查配置或网络连接"

    def download_report(self, doc_id):
        """
        下载生成的研报文件
        
        Args:
            doc_id: 文档ID
            
        Returns:
            下载链接或错误信息
        """
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 接口地址 - 根据官方文档调整
        # 原始接口: url = f"{self.base_url}/wktradereportdownload"
        url = f"{self.base_url}/trdreportdownload"
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth,
            "Version": "1.0.1"
        }
        
        # 构建请求体
        data = {
            "docID": doc_id
        }
        
        logging.info("=" * 80)
        logging.info("[研报下载]开始请求:")
        logging.info(f"请求URL: {url}")
        logging.info(f"请求参数: {json.dumps(data, ensure_ascii=False)}")
        logging.info("=" * 80)
        
        try:
            # 发送请求
            start_time = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=30)
            end_time = time.time()
            elapsed = end_time - start_time
            
            logging.info(f"[研报下载]API请求耗时: {elapsed:.2f}秒")
            
            # 检查响应
            if response.status_code != 200:
                error_msg = f"API请求返回错误状态码: {response.status_code}, 响应内容: {response.text}"
                logging.error(f"[研报下载]请求失败: {error_msg}")
                return None, error_msg
            
            # 记录原始响应
            logging.info(f"[研报下载]原始响应: {response.text}")
            
            # 解析响应
            try:
                # 判断响应是否为JSON
                content_type = response.headers.get('Content-Type', '')
                logging.info(f"[研报下载]响应内容类型: {content_type}")
                
                if 'application/json' in content_type:
                    result = response.json()
                    logging.info(f"[研报下载]响应结果: {json.dumps(result, ensure_ascii=False)}")
                else:
                    # 非JSON响应，尝试作为JSON解析
                    result = response.text
                    logging.info(f"[研报下载]非JSON响应: {result}")
                    try:
                        result = json.loads(result)
                        logging.info(f"[研报下载]成功将文本解析为JSON: {json.dumps(result, ensure_ascii=False)}")
                    except:
                        logging.info("[研报下载]响应不是有效JSON，将作为字符串处理")
                        # 检查是否是直接返回的下载链接
                        if result.startswith("http"):
                            return result, None
                
                # 检查响应是否包含所需数据
                if isinstance(result, dict) and "error" in result:
                    error_msg = f"API返回错误: {result['error']}"
                    logging.error(f"[研报下载]{error_msg}")
                    return None, error_msg
                
                # 提取下载链接
                download_url = None
                
                # 如果是字典
                if isinstance(result, dict):
                    download_url = result.get("downloadURL")
                    if not download_url and "download_url" in result:
                        download_url = result.get("download_url")
                    
                # 如果是字符串且看起来像URL
                elif isinstance(result, str) and (result.startswith("http") or result.startswith("https")):
                    download_url = result
                
                if not download_url:
                    error_msg = "响应中缺少downloadURL字段"
                    logging.warning(f"[研报下载]{error_msg}")
                    return None, error_msg
                    
                # 返回下载链接
                logging.info(f"[研报下载]成功获取下载链接: {download_url}")
                return download_url, None
                
            except ValueError as e:
                error_msg = f"解析响应JSON失败: {str(e)}, 响应内容: {response.text}"
                logging.error(f"[研报下载]{error_msg}")
                return None, error_msg
                
        except Exception as e:
            error_msg = str(e)
            logging.error(f"[研报下载]请求异常: {error_msg}")
            return None, f"下载研报时发生错误: {error_msg}"
    
    # 在check_document_status方法后面找一个适当的位置添加check_report_status方法
    def check_report_status(self, doc_id):
        """
        检查研报生成状态
        
        Args:
            doc_id: 文档ID
            
        Returns:
            状态信息字典
        """
        # 生成时间戳和认证头
        ts = self._generate_timestamp()
        auth = self._generate_auth_header(ts)
        
        # 接口地址 - 根据官方文档调整
        # 原始接口: url = f"{self.base_url}/wktradereportstatus"
        url = f"{self.base_url}/trdreportstatus"
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "PartnerID": self.partner_id,
            "TS": str(ts),
            "Authorization": auth,
            "Version": "1.0.1"
        }
        
        # 构建请求体
        data = {
            "docID": doc_id
        }
        
        logging.info("=" * 80)
        logging.info("[研报状态]开始请求:")
        logging.info(f"请求URL: {url}")
        logging.info(f"请求参数: {json.dumps(data, ensure_ascii=False)}")
        logging.info("=" * 80)
        
        try:
            # 发送请求
            start_time = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=30)
            end_time = time.time()
            elapsed = end_time - start_time
            
            logging.info(f"[研报状态]API请求耗时: {elapsed:.2f}秒")
            
            # 检查响应
            if response.status_code != 200:
                error_msg = f"API请求返回错误状态码: {response.status_code}, 响应内容: {response.text}"
                logging.error(f"[研报状态]请求失败: {error_msg}")
                return {
                    "document_status": "failed",
                    "message": error_msg
                }
            
            # 记录原始响应
            logging.info(f"[研报状态]原始响应: {response.text}")
            
            # 解析响应
            try:
                # 判断响应是否为JSON
                content_type = response.headers.get('Content-Type', '')
                logging.info(f"[研报状态]响应内容类型: {content_type}")
                
                if 'application/json' in content_type:
                    result = response.json()
                    logging.info(f"[研报状态]响应JSON: {json.dumps(result, ensure_ascii=False)}")
                else:
                    # 非JSON响应，尝试作为JSON解析
                    result = response.text
                    logging.info(f"[研报状态]非JSON响应: {result}")
                    try:
                        result = json.loads(result)
                        logging.info(f"[研报状态]成功将文本解析为JSON: {json.dumps(result, ensure_ascii=False)}")
                    except:
                        logging.info("[研报状态]响应不是有效JSON，将作为字符串处理")
                
                # 检查响应是否包含所需数据
                if isinstance(result, dict) and "error" in result:
                    error_msg = f"API返回错误: {result['error']}"
                    logging.error(f"[研报状态]{error_msg}")
                    return {
                        "document_status": "failed",
                        "message": error_msg
                    }
                
                # 提取状态信息
                status_info = {}
                
                # 处理字典类型的结果
                if isinstance(result, dict):
                    # 如果有status字段，提取状态
                    if "status" in result:
                        status = result["status"]
                        logging.info(f"[研报状态]提取的状态信息: {status}")
                        
                        if status == "completed":
                            status_info["document_status"] = "completed"
                        elif status == "generating":
                            status_info["document_status"] = "generating"
                        elif status == "failed":
                            status_info["document_status"] = "failed"
                            status_info["message"] = result.get("message", "生成失败")
                        else:
                            status_info["document_status"] = "unknown"
                            status_info["message"] = f"未知状态: {status}"
                    
                    # 保存完整的响应以便调试
                    status_info["api_response"] = result
                
                # 处理字符串类型的结果
                elif isinstance(result, str):
                    if "completed" in result.lower():
                        status_info["document_status"] = "completed"
                    elif "generating" in result.lower() or "processing" in result.lower():
                        status_info["document_status"] = "generating"
                    elif "failed" in result.lower() or "error" in result.lower():
                        status_info["document_status"] = "failed"
                        status_info["message"] = result
                    else:
                        status_info["document_status"] = "unknown"
                        status_info["message"] = f"未知状态信息: {result}"
                    
                    # 保存原始响应
                    status_info["raw_response"] = result
                
                # 如果没有找到状态信息，返回默认值
                if not status_info:
                    logging.warning(f"[研报状态]无法解析状态信息: {str(result)[:1000]}")
                    return {
                        "document_status": "unknown",
                        "message": "无法解析状态信息",
                        "raw_response": str(result)[:1000] if isinstance(result, str) else json.dumps(result, ensure_ascii=False)[:1000]
                    }
                
                logging.info(f"[研报状态]解析后的状态信息: {json.dumps(status_info, ensure_ascii=False)}")
                return status_info
                
            except ValueError as e:
                error_msg = f"解析响应JSON失败: {str(e)}, 响应内容: {response.text}"
                logging.error(f"[研报状态]{error_msg}")
                return {
                    "document_status": "failed",
                    "message": error_msg
                }
                
        except Exception as e:
            error_msg = str(e)
            logging.error(f"[研报状态]请求异常: {error_msg}")
            return {
                "document_status": "failed",
                "message": f"状态查询异常: {error_msg}"
            }

@academic_paper_bp.route('/paper_outline', methods=['POST'])
def paper_outline():
    """处理论文大纲生成请求 - 通过JSON API"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_id = data.get('user_id')  # 可选参数
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': '请提供论文主题'
            }), 400
        
        # 获取百度文心API的配置
        partner_id = current_app.config.get('WENCHAIN_PARTNER_ID')
        api_secret = current_app.config.get('WENCHAIN_API_SECRET')
        
        if not partner_id or not api_secret:
            current_app.logger.error("未配置百度文心API凭证")
            return jsonify({
                'status': 'error',
                'message': '服务配置错误，请联系管理员'
            }), 500
        
        # 记录请求信息
        current_app.logger.info(f"收到论文大纲请求: {query[:100]}...")
        
        # 创建文心API客户端
        client = WenchainClient(partner_id, api_secret)
        
        # 调用API生成大纲
        result = client.paper_outline(query)
        
        # 增加对返回内容的检查
        if not result:
            current_app.logger.error("API返回空结果")
            return jsonify({
                'status': 'error',
                'message': '无法生成论文大纲，请稍后重试'
            }), 500
            
        # 检查是否返回了错误信息
        if result.startswith('生成大纲失败') or '失败' in result or '错误' in result:
            current_app.logger.error(f"API返回错误信息: {result}")
            
            # 即使有错误，我们也以成功状态返回，但在前端会显示错误信息
            return jsonify({
                'status': 'error',
                'message': result,
                'data': f"# 大纲生成失败\n\n## 错误信息\n{result}\n\n## 建议\n请稍后重试或联系管理员。"
            })
        
        # 大纲生成成功
        try:
            # 从大纲中提取标题 - 尝试找到第一个# 开头的行
            title = query  # 默认使用查询作为标题
            if result:
                lines = result.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
            
            # 创建并保存记录
            paper = AcademicPaper(
                user_id=user_id,
                title=title,
                query=query,
                outline=result,
                document_status='none',  # 目前只有大纲，没有论文内容
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.session.add(paper)
            db.session.commit()
            
            # 记录成功信息
            current_app.logger.info(f"大纲生成成功，ID: {paper.id}")
            
            # 返回响应时包含记录ID
            return jsonify({
                'status': 'success',
                'data': result,
                'paper_id': paper.id
            })
        except Exception as e:
            current_app.logger.error(f"保存论文记录失败: {str(e)}")
            # 即使保存记录失败，也返回生成的大纲
            return jsonify({
                'status': 'success',
                'data': result,
                'message': '大纲生成成功，但保存历史记录失败'
            })
    except Exception as e:
        current_app.logger.error(f"生成论文大纲时发生错误: {str(e)}")
        # 增加更详细的错误日志
        import traceback
        current_app.logger.error(f"错误详情: {traceback.format_exc()}")
        
        return jsonify({
            'status': 'error',
            'message': f'服务异常: {str(e)}',
            'data': f"# 服务异常\n\n系统处理请求时发生错误。\n\n请稍后再试或联系管理员。"
        }), 500

@academic_paper_bp.route('/test_outline', methods=['GET'])
def test_outline():
    """
    测试论文大纲生成API的端点
    返回一个简单的HTML页面，可以直接在浏览器中测试
    """
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>论文大纲生成测试</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            #query { width: 100%; height: 100px; margin-bottom: 10px; }
            #result { white-space: pre-wrap; background: #f5f5f5; padding: 10px; min-height: 300px; border: 1px solid #ddd; }
            .button { padding: 10px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
            h1 { color: #c62828; } /* 紫荆红色 */
            
            /* 块状选择项样式 */
            .topic-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }
            .topic-item {
                background: #f0f0f0;
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .topic-item:hover {
                background: #e0e0e0;
                transform: translateY(-2px);
                box-shadow: 0 3px 5px rgba(0,0,0,0.1);
            }
            .topic-item.selected {
                background: #c6e6c6;
                border-color: #4CAF50;
            }
        </style>
    </head>
    <body>
        <h1>论文大纲生成测试</h1>
        <p>选择或输入论文主题，生成大纲结构</p>
        
        <div class="topic-grid">
            <div class="topic-item" onclick="selectTopic(this, '人工智能在医疗领域的应用及挑战')">人工智能在医疗领域的应用及挑战</div>
            <div class="topic-item" onclick="selectTopic(this, '可持续发展与绿色能源技术的未来趋势')">可持续发展与绿色能源技术的未来趋势</div>
            <div class="topic-item" onclick="selectTopic(this, '数字经济时代的隐私保护与数据安全')">数字经济时代的隐私保护与数据安全</div>
            <div class="topic-item" onclick="selectTopic(this, '全球气候变化对生物多样性的影响研究')">全球气候变化对生物多样性的影响研究</div>
        </div>
        
        <textarea id="query" placeholder="或者输入您自定义的论文主题"></textarea>
        <button class="button" id="generate">生成大纲</button>
        
        <h3>结果：</h3>
        <div id="result">结果将在这里显示...</div>
        
        <script>
            function selectTopic(element, topic) {
                // 移除所有选中状态
                document.querySelectorAll('.topic-item').forEach(item => {
                    item.classList.remove('selected');
                });
                
                // 添加选中状态
                element.classList.add('selected');
                
                // 设置文本框内容
                document.getElementById('query').value = topic;
            }
            
            document.getElementById('generate').addEventListener('click', async function() {
                const query = document.getElementById('query').value.trim();
                if (!query) {
                    alert('请选择或输入论文主题');
                    return;
                }
                
                const resultDiv = document.getElementById('result');
                resultDiv.textContent = "正在生成中，请稍候...";
                
                try {
                    const response = await fetch('/api/v1/academic/paper_outline', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ query })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    resultDiv.textContent = data.data;
                } catch (error) {
                    resultDiv.textContent = "生成大纲时出错: " + error.message;
                }
            });
        </script>
    </body>
    </html>
    """
    return test_html

@academic_paper_bp.route('/generate-paper', methods=['POST'])
def generate_paper():
    """处理论文大纲生成请求 - 通过JSON API"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': '请提供论文主题'
            }), 400
        
        # 获取百度文心API的配置
        partner_id = current_app.config.get('WENCHAIN_PARTNER_ID')
        api_secret = current_app.config.get('WENCHAIN_API_SECRET')
        
        if not partner_id or not api_secret:
            current_app.logger.error("未配置百度文心API凭证")
            return jsonify({
                'status': 'error',
                'message': '服务配置错误，请联系管理员'
            }), 500
        
        # 创建文心API客户端
        client = WenchainClient(partner_id, api_secret)
        
        # 调用API生成大纲
        result = client.paper_outline(query)
        
        if result:
            return jsonify({
                'status': 'success',
                'data': result
            })
        else:
            return jsonify({
                'status': 'error',
                'message': '生成论文大纲失败'
            }), 500
    except Exception as e:
        current_app.logger.error(f"生成论文大纲时发生错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'服务异常: {str(e)}'
        }), 500

# 添加新的API端点，用于从大纲生成完整论文
@academic_paper_bp.route('/paper_from_outline', methods=['POST'])
def paper_from_outline():
    """从大纲生成完整论文的API端点"""
    try:
        start_time = time.time()
        data = request.get_json()
        
        # 记录完整的请求参数
        logging.info(f"[/paper_from_outline] 收到请求参数: {json.dumps(data, ensure_ascii=False)}")
        
        # 支持两种参数名称: query 或 user_query 作为论文主题
        query = data.get('query', '')
        user_query = data.get('user_query', '')
        
        # 如果user_query有值，优先使用它
        if user_query and not query:
            query = user_query
            logging.info(f"[/paper_from_outline] 使用user_query作为查询参数: {query}")
        
        outline = data.get('outline', '')
        paper_id = data.get('paper_id')  # 可选，如果提供了，将更新对应的记录
        user_id = data.get('user_id')    # 可选，用于创建新记录
        
        if not query:
            logging.warning("[/paper_from_outline] 未提供论文主题")
            return jsonify({
                'status': 'error',
                'message': '请提供论文主题'
            }), 400
            
        if not outline:
            logging.warning("[/paper_from_outline] 未提供论文大纲")
            return jsonify({
                'status': 'error',
                'message': '请提供论文大纲'
            }), 400
        
        # 记录处理的参数
        logging.info(f"[/paper_from_outline] 处理参数: query={query}, outline长度={len(outline)}")
        
        # 获取百度文心API的配置
        partner_id = current_app.config.get('WENCHAIN_PARTNER_ID')
        api_secret = current_app.config.get('WENCHAIN_API_SECRET')
        
        if not partner_id or not api_secret:
            current_app.logger.error("未配置百度文心API凭证")
            return jsonify({
                'status': 'error',
                'message': '服务配置错误，请联系管理员'
            }), 500
        
        # 创建文心API客户端
        client = WenchainClient(partner_id, api_secret)
        
        # 调用API生成完整论文
        current_app.logger.info(f"[/paper_from_outline] 开始生成论文，主题: {query}")
        result = client.generate_full_paper(query, outline)
        end_time = time.time()
        
        process_time = end_time - start_time
        current_app.logger.info(f"论文生成完成，处理时间: {process_time:.2f}秒")
        current_app.logger.info(f"生成的论文内容长度: {len(result) if result else 0}")
        
        if result:
            # 检查结果是否包含文档ID而非直接内容
            if isinstance(result, dict) and 'doc_id' in result:
                doc_id = result.get('doc_id')
                content = None  # 内容将稍后获取
                document_status = 'generating'
                status_message = '正在生成中'
            elif isinstance(result, str) and "文档ID:" in result:
                # 从字符串中提取docID
                match = re.search(r'文档ID: ([a-f0-9]+)', result)
                if match:
                    doc_id = match.group(1)
                    content = None
                    document_status = 'generating'
                    status_message = '正在生成中'
                    logging.info(f"从返回字符串中提取到docID: {doc_id}")
                else:
                    content = result
            else:
                content = result
            
            # 保存或更新记录
            try:
                if paper_id:
                    # 更新已有记录
                    paper = AcademicPaper.query.get(paper_id)
                    if paper:
                        paper.content = content
                        paper.doc_id = doc_id
                        paper.document_status = document_status
                        paper.status_message = status_message
                        db.session.commit()
                        
                        logging.info(f"更新论文记录成功，ID: {paper.id}")
                    else:
                        logging.warning(f"未找到指定ID的论文记录: {paper_id}")
                        # 如果没找到，创建新记录
                        paper = AcademicPaper(
                            user_id=user_id,
                            title=query,  # 简单使用查询作为标题
                            query=query,
                            outline=outline,
                            content=content,
                            doc_id=doc_id,
                            document_status=document_status,
                            status_message=status_message,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        db.session.add(paper)
                        db.session.commit()
                        
                        logging.info(f"创建新论文记录成功，ID: {paper.id}")
                else:
                    # 从大纲中提取标题
                    title = query  # 默认使用查询作为标题
                    if outline:
                        lines = outline.split('\n')
                        for line in lines:
                            line = line.strip()
                            if line.startswith('# '):
                                title = line[2:].strip()
                                break
                    
                    # 创建新记录
                    paper = AcademicPaper(
                        user_id=user_id,
                        title=title,
                        query=query,
                        outline=outline,
                        content=content,
                        doc_id=doc_id,
                        document_status=document_status,
                        status_message=status_message,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.session.add(paper)
                    db.session.commit()
                    
                    logging.info(f"创建新论文记录成功，ID: {paper.id}")
                    
                paper_id = paper.id
                
            except Exception as e:
                logging.error(f"保存论文记录失败: {str(e)}")
                # 记录保存失败，但仍返回生成的内容
            
            # 返回结果
            if doc_id:
                # 返回文档ID供后续查询
                return jsonify({
                    'status': 'success',
                    'data': {
                        'doc_id': doc_id,
                        'paper_id': paper_id,
                        'document_status': document_status,
                        'message': '论文正在生成中，请稍后查询状态'
                    },
                    'process_time': process_time
                })
            else:
                # 直接返回内容
                return jsonify({
                    'status': 'success',
                    'data': result,
                    'paper_id': paper_id,
                    'process_time': process_time
                })
        else:
            return jsonify({
                'status': 'error',
                'message': '生成完整论文失败'
            }), 500
    except Exception as e:
        current_app.logger.error(f"生成完整论文时发生错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'服务异常: {str(e)}'
        }), 500

# 添加文档下载路由
@academic_paper_bp.route('/download_paper', methods=['OPTIONS'])
def download_paper_options():
    """处理OPTIONS请求"""
    return '', 200

@academic_paper_bp.route('/download_paper', methods=['POST'])
def download_paper():
    """
    根据文档ID下载论文
    
    请求参数:
        doc_id: 文档ID
        paper_id: 论文记录ID (可选)
        
    返回:
        成功: 下载链接
        失败: 错误信息
    """
    try:
        print("\n===== 下载论文请求 =====")
        data = request.get_json()
        print(f"请求数据: {data}")
        
        if not data:
            print("错误: 请求参数为空")
            return jsonify({
                "status": "error",
                "message": "请求参数为空",
                "process_time": 0
            }), 400
        
        # 获取文档ID
        doc_id = data.get('doc_id')
        paper_id = data.get('paper_id')  # 可选参数
        print(f"关键参数: doc_id={doc_id}, paper_id={paper_id}")
        
        if not doc_id:
            print("错误: 缺少文档ID参数")
            return jsonify({
                "status": "error",
                "message": "缺少文档ID参数",
                "process_time": 0
            }), 400
            
        # 记录开始时间
        start_time = time.time()
        logging.info(f"[论文下载]开始下载文档，ID: {doc_id}")
        
        # 获取API凭证
        partner_id = os.environ.get("WENCHAIN_PARTNER_ID", "").strip()
        partner_key = os.environ.get("WENCHAIN_API_SECRET", "").strip()
        
        # 创建客户端实例
        client = WenchainClient(partner_id, partner_key)
        
        # 调用下载方法
        print(f"调用API下载: doc_id={doc_id}")
        result = client.download_paper(doc_id)
        print(f"API返回结果长度: {len(str(result))}")
        if isinstance(result, str) and result.startswith('http'):
            print(f"成功获取下载链接: {result[:50]}...")
        else:
            print(f"未能获取有效下载链接: {result[:100]}")
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 如果提供了paper_id，且获取到了有效下载链接，更新数据库记录
        db_updated = False
        if paper_id and result and isinstance(result, str) and result.startswith('http'):
            logging.info(f"[下载API] 获取到有效下载链接，正在更新数据库: paper_id={paper_id}")
            print(f"获取到有效下载链接，开始更新数据库: paper_id={paper_id}")
            try:
                # 方法1: 使用ORM方式更新
                paper = db.session.query(AcademicPaper).filter(AcademicPaper.id == paper_id).with_for_update().first()
                if paper:
                    print(f"找到论文记录: id={paper.id}, 当前状态={paper.document_status}, 已有下载链接={bool(paper.download_url)}")
                    paper.download_url = result
                    paper.document_status = 'completed'
                    paper.status_message = '论文生成完成，可以下载'
                    from datetime import datetime
                    paper.updated_at = datetime.now()
                    try:
                        db.session.commit()
                        db_updated = True
                        logging.info(f"[下载API] ORM方式更新成功: paper_id={paper_id}")
                        print(f"ORM方式更新成功: paper_id={paper_id}")
                    except Exception as commit_error:
                        logging.error(f"[下载API] ORM提交失败: {str(commit_error)}")
                        print(f"ORM提交失败: {str(commit_error)}")
                        db.session.rollback()
                else:
                    logging.warning(f"[下载API] 未找到论文记录: paper_id={paper_id}")
                    print(f"未找到论文记录: paper_id={paper_id}")
            except Exception as e:
                logging.error(f"[下载API] ORM更新失败: {str(e)}")
                print(f"ORM更新失败: {str(e)}")
                db.session.rollback()
                
            # 如果ORM方式失败，使用原生SQL强制更新
            if not db_updated:
                try:
                    logging.info(f"[下载API] 尝试使用原生SQL更新: paper_id={paper_id}")
                    print(f"尝试使用原生SQL更新: paper_id={paper_id}")
                    from sqlalchemy import text
                    
                    # 构建更新SQL
                    update_sql = text("""
                        UPDATE academic_papers 
                        SET document_status = 'completed', 
                            status_message = '论文生成完成，可以下载', 
                            download_url = :download_url,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = :paper_id
                    """)
                    
                    # 执行SQL更新
                    with db.engine.connect() as conn:
                        result_update = conn.execute(update_sql, {"download_url": result, "paper_id": paper_id})
                        conn.commit()
                        affected_rows = result_update.rowcount
                        
                        if affected_rows > 0:
                            db_updated = True
                            logging.info(f"[下载API] SQL更新成功: paper_id={paper_id}, 影响行数={affected_rows}")
                            print(f"SQL更新成功: paper_id={paper_id}, 影响行数={affected_rows}")
                        else:
                            logging.warning(f"[下载API] SQL更新失败，无行受影响: paper_id={paper_id}")
                            print(f"SQL更新失败，无行受影响: paper_id={paper_id}")
                except Exception as sql_error:
                    logging.error(f"[下载API] SQL更新失败: {str(sql_error)}")
                    print(f"SQL更新失败: {str(sql_error)}")
            
            # 验证更新结果
            try:
                verify_paper = db.session.query(AcademicPaper).filter(AcademicPaper.id == paper_id).first()
                if verify_paper:
                    logging.info(f"[下载API] 验证结果: paper_id={paper_id}, 状态='{verify_paper.document_status}', 下载链接存在={bool(verify_paper.download_url)}")
                    print(f"验证结果: paper_id={paper_id}, 状态='{verify_paper.document_status}', 下载链接存在={bool(verify_paper.download_url)}")
                    if verify_paper.document_status != 'completed':
                        logging.error(f"[下载API] 状态验证失败！期望='completed', 实际='{verify_paper.document_status}'")
                        print(f"状态验证失败！期望='completed', 实际='{verify_paper.document_status}'")
                else:
                    logging.warning(f"[下载API] 验证失败，未找到记录: paper_id={paper_id}")
                    print(f"验证失败，未找到记录: paper_id={paper_id}")
            except Exception as e:
                logging.error(f"[下载API] 验证失败: {str(e)}")
                print(f"验证失败: {str(e)}")
                
        # 在返回结果中添加数据库更新状态
        response_data = {
            "status": "success",
            "data": result,
            "process_time": process_time
        }
        
        if paper_id:
            response_data["db_updated"] = db_updated
            
        print(f"返回响应: 下载链接长度={len(str(result))}, 数据库更新={db_updated}")
        print("===== 下载请求处理完成 =====\n")
            
        # 返回结果
        return jsonify(response_data)
    
    except Exception as e:
        logging.error(f"[论文下载]处理请求时出错: {str(e)}")
        print(f"处理请求异常: {str(e)}")
        print("===== 下载请求异常结束 =====\n")
        return jsonify({
            "status": "error",
            "message": f"处理请求时出错: {str(e)}",
            "process_time": 0
        }), 500

# 添加检查文档状态的接口
@academic_paper_bp.route('/check_paper_status', methods=['OPTIONS'])
def check_paper_status_options():
    """处理OPTIONS请求"""
    return '', 200

@academic_paper_bp.route('/check_paper_status', methods=['POST'])
def check_paper_status():
    """
    检查论文文档生成状态
    
    请求参数:
        doc_id: 文档ID
        paper_id: 论文记录ID (可选)
        
    返回:
        status: 文档状态 (generating/completed/failed)
        message: 状态描述
    """
    try:
        # 在专门的日志文件中记录此次调用的详细信息
        with open('backend/logs/paper_status_debug.log', 'a') as f:
            f.write(f"\n[{datetime.now()}] ==== 新的状态检查请求 ====\n")
            f.write(f"请求来源IP: {request.remote_addr}\n")
            f.write(f"请求头: {request.headers}\n")
        
        data = request.get_json()
        
        # 记录请求数据
        with open('backend/logs/paper_status_debug.log', 'a') as f:
            f.write(f"请求数据: {data}\n")
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "请求参数为空",
                "process_time": 0
            }), 400
        
        # 获取文档ID
        doc_id = data.get('doc_id')
        paper_id = data.get('paper_id')  # 可选参数
        
        # 记录关键参数
        with open('backend/logs/paper_status_debug.log', 'a') as f:
            f.write(f"文档ID: {doc_id}, 论文ID: {paper_id}\n")
        
        if not doc_id:
            return jsonify({
                "status": "error",
                "message": "缺少文档ID参数",
                "process_time": 0
            }), 400
            
        # 记录开始时间
        start_time = time.time()
        logging.info(f"[论文状态]开始检查文档状态，ID: {doc_id}")
        
        # 获取API凭证
        partner_id = os.environ.get("WENCHAIN_PARTNER_ID", "").strip()
        partner_key = os.environ.get("WENCHAIN_API_SECRET", "").strip()
        
        # 创建客户端实例
        client = WenchainClient(partner_id, partner_key)
        
        # 调用状态检查方法
        result = client.check_document_status(doc_id)
        
        # 记录API返回结果
        with open('backend/logs/paper_status_debug.log', 'a') as f:
            f.write(f"API状态检查结果: {result}\n")
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 如果提供了paper_id，更新数据库记录
        db_updated = False  # 标记数据库是否更新成功
        download_url = None # 保存下载URL
        
        if paper_id and result:
            try:
                # 方法1: 使用ORM方式更新
                logging.info(f"[状态检查] 尝试ORM方式更新数据库: paper_id={paper_id}")
                with open('backend/logs/paper_status_debug.log', 'a') as f:
                    f.write(f"开始ORM方式更新数据库: paper_id={paper_id}\n")
                
                # 确保使用新的会话查询
                paper = db.session.query(AcademicPaper).filter(AcademicPaper.id == paper_id).with_for_update().first()
                if paper:
                    old_status = paper.document_status
                    new_status = result.get('document_status', paper.document_status)
                    new_message = result.get('message', paper.status_message)
                    
                    logging.info(f"[状态检查] 当前状态: paper_id={paper_id}, 状态='{old_status}', 新状态='{new_status}'")
                    with open('backend/logs/paper_status_debug.log', 'a') as f:
                        f.write(f"状态对比: 旧='{old_status}', 新='{new_status}'\n")
                    
                    # 强制更新状态，不再比较是否相同
                    paper.document_status = new_status
                    paper.status_message = new_message
                    
                    # 强制更新时间戳
                    from datetime import datetime
                    paper.updated_at = datetime.now()
                    
                    logging.info(f"[状态检查] 状态已更新: paper_id={paper_id}, 从'{old_status}'到'{new_status}'")
                    
                    # 如果状态是已完成，尝试获取下载链接
                    if new_status == 'completed':
                        try:
                            logging.info(f"[状态检查] 状态为已完成，获取下载链接: paper_id={paper_id}, doc_id={doc_id}")
                            with open('backend/logs/paper_status_debug.log', 'a') as f:
                                f.write(f"状态为已完成，获取下载链接: paper_id={paper_id}, doc_id={doc_id}\n")
                            
                            download_result = client.download_paper(doc_id)
                            if download_result and isinstance(download_result, str) and download_result.startswith('http'):
                                paper.download_url = download_result
                                download_url = download_result
                                logging.info(f"[状态检查] 成功获取下载链接: paper_id={paper_id}, url={download_result[:30]}...")
                                with open('backend/logs/paper_status_debug.log', 'a') as f:
                                    f.write(f"成功获取下载链接: url={download_result[:50]}...\n")
                            else:
                                logging.warning(f"[状态检查] 下载API返回非链接内容: paper_id={paper_id}, 内容={download_result[:100]}...")
                                with open('backend/logs/paper_status_debug.log', 'a') as f:
                                    f.write(f"下载API返回非链接内容: 内容={download_result[:100]}...\n")
                        except Exception as e:
                            logging.error(f"[状态检查] 获取下载链接失败: paper_id={paper_id}, 错误: {str(e)}")
                            with open('backend/logs/paper_status_debug.log', 'a') as f:
                                f.write(f"获取下载链接失败: 错误: {str(e)}\n")
                    
                    # 提交事务
                    try:
                        db.session.commit()
                        db_updated = True
                        logging.info(f"[状态检查] ORM更新成功: paper_id={paper_id}")
                        with open('backend/logs/paper_status_debug.log', 'a') as f:
                            f.write(f"ORM更新成功提交: paper_id={paper_id}\n")
                        
                        # 二次验证更新结果
                        updated_paper = db.session.query(AcademicPaper).filter(AcademicPaper.id == paper_id).first()
                        if updated_paper:
                            logging.info(f"[状态检查] 验证结果: paper_id={paper_id}, 状态='{updated_paper.document_status}', 下载链接存在={bool(updated_paper.download_url)}")
                            with open('backend/logs/paper_status_debug.log', 'a') as f:
                                f.write(f"验证结果: 状态='{updated_paper.document_status}', 下载链接存在={bool(updated_paper.download_url)}\n")
                            if updated_paper.document_status != new_status:
                                logging.warning(f"[状态检查] 验证失败! 期望='{new_status}', 实际='{updated_paper.document_status}'")
                                with open('backend/logs/paper_status_debug.log', 'a') as f:
                                    f.write(f"验证失败! 期望='{new_status}', 实际='{updated_paper.document_status}'\n")
                    except Exception as commit_error:
                        logging.error(f"[状态检查] ORM提交失败: {str(commit_error)}")
                        with open('backend/logs/paper_status_debug.log', 'a') as f:
                            f.write(f"ORM提交失败: {str(commit_error)}\n")
                        db.session.rollback()
                        logging.info("[状态检查] 已回滚事务")
                else:
                    logging.warning(f"[状态检查] 未找到论文记录: paper_id={paper_id}")
                    with open('backend/logs/paper_status_debug.log', 'a') as f:
                        f.write(f"未找到论文记录: paper_id={paper_id}\n")
            except Exception as e:
                logging.error(f"[状态检查] ORM更新异常: paper_id={paper_id}, 错误: {str(e)}")
                with open('backend/logs/paper_status_debug.log', 'a') as f:
                    f.write(f"ORM更新异常: 错误: {str(e)}\n")
                try:
                    db.session.rollback()
                except Exception:
                    pass
                
            # 如果ORM方式失败，使用原生SQL强制更新
            if not db_updated and result.get('document_status'):
                try:
                    logging.info(f"[状态检查] 尝试SQL方式强制更新: paper_id={paper_id}")
                    with open('backend/logs/paper_status_debug.log', 'a') as f:
                        f.write(f"开始SQL方式强制更新: paper_id={paper_id}\n")
                    
                    # 构建SQL参数
                    sql_params = {
                        "paper_id": paper_id,
                        "status": result.get('document_status'),
                        "message": result.get('message', '')
                    }
                    
                    # 如果状态是已完成但没有下载链接，再次尝试获取
                    if result.get('document_status') == 'completed' and not download_url:
                        try:
                            logging.info(f"[SQL更新] 状态为已完成，获取下载链接: paper_id={paper_id}, doc_id={doc_id}")
                            with open('backend/logs/paper_status_debug.log', 'a') as f:
                                f.write(f"SQL更新: 状态为已完成，获取下载链接: paper_id={paper_id}\n")
                            
                            download_result = client.download_paper(doc_id)
                            if download_result and isinstance(download_result, str) and download_result.startswith('http'):
                                download_url = download_result
                                sql_params["download_url"] = download_url
                                logging.info(f"[SQL更新] 成功获取下载链接: paper_id={paper_id}, url={download_url[:30]}...")
                                with open('backend/logs/paper_status_debug.log', 'a') as f:
                                    f.write(f"SQL更新: 成功获取下载链接: url={download_url[:50]}...\n")
                            else:
                                logging.warning(f"[SQL更新] 下载API返回非链接内容: 内容={download_result[:100]}...")
                                with open('backend/logs/paper_status_debug.log', 'a') as f:
                                    f.write(f"SQL更新: 下载API返回非链接内容: 内容={download_result[:100]}...\n")
                        except Exception as e:
                            logging.error(f"[SQL更新] 获取下载链接失败: paper_id={paper_id}, 错误: {str(e)}")
                            with open('backend/logs/paper_status_debug.log', 'a') as f:
                                f.write(f"SQL更新: 获取下载链接失败: 错误: {str(e)}\n")
                    elif download_url:
                        sql_params["download_url"] = download_url
                        with open('backend/logs/paper_status_debug.log', 'a') as f:
                            f.write(f"SQL更新: 使用现有下载链接\n")
                    
                    # 构建更新SQL
                    download_url_clause = ", download_url = :download_url" if "download_url" in sql_params else ""
                    update_sql = f"""
                        UPDATE academic_papers 
                        SET document_status = :status, 
                            status_message = :message
                            {download_url_clause},
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = :paper_id
                    """
                    
                    with open('backend/logs/paper_status_debug.log', 'a') as f:
                        f.write(f"SQL更新语句: {update_sql}\n")
                        f.write(f"SQL参数: {sql_params}\n")
                    
                    # 执行SQL更新
                    from sqlalchemy import text
                    with db.engine.connect() as conn:
                        result_update = conn.execute(text(update_sql), sql_params)
                        conn.commit()
                        affected_rows = result_update.rowcount
                        
                        if affected_rows > 0:
                            db_updated = True
                            logging.info(f"[状态检查] SQL更新成功: paper_id={paper_id}, 影响行数={affected_rows}")
                            with open('backend/logs/paper_status_debug.log', 'a') as f:
                                f.write(f"SQL更新成功: 影响行数={affected_rows}\n")
                        else:
                            logging.warning(f"[状态检查] SQL更新失败，无行受影响: paper_id={paper_id}")
                            with open('backend/logs/paper_status_debug.log', 'a') as f:
                                f.write(f"SQL更新失败，无行受影响: paper_id={paper_id}\n")
                except Exception as sql_error:
                    logging.error(f"[状态检查] SQL更新失败: {str(sql_error)}")
                    with open('backend/logs/paper_status_debug.log', 'a') as f:
                        f.write(f"SQL更新异常: {str(sql_error)}\n")
        elif not paper_id:
            logging.warning("[状态更新] 缺少paper_id参数，无法更新数据库")
            with open('backend/logs/paper_status_debug.log', 'a') as f:
                f.write("缺少paper_id参数，无法更新数据库\n")
        
        # 在返回的数据中添加数据库更新状态和下载链接
        result['db_updated'] = db_updated
        if download_url:
            result['download_url'] = download_url
        
        # 记录最终返回结果
        with open('backend/logs/paper_status_debug.log', 'a') as f:
            f.write(f"最终返回结果: {result}\n")
            f.write(f"[{datetime.now()}] ==== 请求处理完成 ====\n\n")
        
        return jsonify({
            "status": "success",
            "data": result,
            "process_time": process_time
        })
    
    except Exception as e:
        logging.error(f"[论文状态]处理请求时出错: {str(e)}")
        with open('backend/logs/paper_status_debug.log', 'a') as f:
            f.write(f"处理请求时出错: {str(e)}\n")
            f.write(f"[{datetime.now()}] ==== 请求处理异常结束 ====\n\n")
        return jsonify({
            "status": "error",
            "message": f"处理请求时出错: {str(e)}",
            "process_time": 0
        }), 500

# 添加新的历史记录查询API
@academic_paper_bp.route('/history', methods=['OPTIONS'])
def history_options():
    """处理OPTIONS请求"""
    return '', 200

@academic_paper_bp.route('/history', methods=['GET'])
def get_paper_history():
    """
    获取论文生成历史记录
    
    参数:
        user_id: 用户ID (可选)
        page: 页码 (默认1)
        per_page: 每页数量 (默认10)
        force: 强制刷新状态 (可选，默认false)
        
    返回:
        历史记录列表，分页信息
    """
    try:
        # 获取参数
        user_id = request.args.get('user_id', type=int)  
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        force_refresh = request.args.get('force', 'false').lower() in ['true', '1', 'yes']
        
        # 使用直接的数据库连接
        from sqlalchemy import text
        
        # 计算分页参数
        offset = (page - 1) * per_page
        
        # 添加调试日志
        logging.info(f"获取论文历史记录, 页码: {page}, 每页数量: {per_page}, 强制刷新: {force_refresh}")
        
        # 构建SQL语句 - 确保明确选择created_at和updated_at字段
        if user_id:
            count_sql = text("SELECT COUNT(*) FROM academic_papers WHERE user_id = :user_id")
            query_sql = text("""
                SELECT id, user_id, title, query, outline, content, doc_id, 
                       document_status, status_message, download_url, 
                       created_at, updated_at 
                FROM academic_papers 
                WHERE user_id = :user_id 
                ORDER BY created_at DESC 
                LIMIT :limit OFFSET :offset
            """)
            count_params = {"user_id": user_id}
            query_params = {"user_id": user_id, "limit": per_page, "offset": offset}
        else:
            count_sql = text("SELECT COUNT(*) FROM academic_papers")
            query_sql = text("""
                SELECT id, user_id, title, query, outline, content, doc_id, 
                       document_status, status_message, download_url, 
                       created_at, updated_at 
                FROM academic_papers 
                ORDER BY created_at DESC 
                LIMIT :limit OFFSET :offset
            """)
            count_params = {}
            query_params = {"limit": per_page, "offset": offset}
            
        # 执行查询
        with db.engine.connect() as conn:
            # 获取总数
            total_result = conn.execute(count_sql, count_params)
            total = total_result.scalar()
            
            # 获取数据并记录原始结果
            result_proxy = conn.execute(query_sql, query_params)
            rows = result_proxy.fetchall()
            
            # 调试输出前5行数据的时间戳
            for i, row in enumerate(rows[:5]):
                logging.info(f"行 {i+1}, ID: {row[0]}, 创建时间: {row[10]}, 更新时间: {row[11]}")
        
        # 计算总页数
        pages = (total + per_page - 1) // per_page  # 向上取整
        
        # 如果请求强制刷新，则更新所有生成中的论文状态
        if force_refresh:
            logging.info(f"请求强制刷新论文状态，页码: {page}")
            
            # 创建文心API客户端
            partner_id = current_app.config.get('WENCHAIN_PARTNER_ID')
            api_secret = current_app.config.get('WENCHAIN_API_SECRET')
            client = WenchainClient(partner_id, api_secret)
            
            # 获取所有需要更新的论文ID和文档ID
            papers_to_update = []
            for row in rows:
                paper_id = row[0]
                doc_id = row[6]  # doc_id列
                document_status = row[7]  # document_status列
                
                # 只更新状态为"生成中"的论文
                if doc_id and document_status == 'generating':
                    papers_to_update.append((paper_id, doc_id))
            
            # 更新每篇论文的状态
            for paper_id, doc_id in papers_to_update:
                try:
                    logging.info(f"强制刷新论文状态: paper_id={paper_id}, doc_id={doc_id}")
                    
                    # 获取论文记录
                    paper = AcademicPaper.query.get(paper_id)
                    if not paper:
                        logging.warning(f"未找到论文记录，ID: {paper_id}")
                        continue
                        
                    # 调用API获取最新状态
                    status_result = client.check_document_status(doc_id)
                    if status_result:
                        old_status = paper.document_status
                        paper.document_status = status_result.get('document_status', paper.document_status)
                        paper.status_message = status_result.get('message', paper.status_message)
                        
                        # 如果状态是已完成，尝试获取下载链接
                        if paper.document_status == 'completed' and not paper.download_url:
                            try:
                                download_result = client.download_paper(doc_id)
                                if download_result and isinstance(download_result, str) and download_result.startswith('http'):
                                    paper.download_url = download_result
                                    logging.info(f"获取到论文下载链接: paper_id={paper_id}")
                            except Exception as e:
                                logging.error(f"获取下载链接失败: paper_id={paper_id}, 错误: {str(e)}")
                        
                        # 提交更新
                        db.session.commit()
                        logging.info(f"论文状态已更新: paper_id={paper_id}, 从 {old_status} 变为 {paper.document_status}")
                except Exception as e:
                    logging.error(f"更新论文状态失败: paper_id={paper_id}, 错误: {str(e)}")
                    # 继续处理下一条记录
            
            # 重新查询数据库获取最新状态
            with db.engine.connect() as conn:
                result_proxy = conn.execute(query_sql, query_params)
                rows = result_proxy.fetchall()
                logging.info("强制刷新后重新查询数据库")
        
        # 构建论文记录列表
        items = []
        for row in rows:
            # 转换为字典，记录原始时间值以便调试
            created_at = row[10]
            updated_at = row[11]
            
            # 记录时间值类型以便调试
            logging.info(f"ID: {row[0]}, created_at类型: {type(created_at)}, created_at值: {created_at}")
            
            paper = {
                'id': row[0],
                'user_id': row[1],
                'title': row[2],
                'query': row[3],
                'outline': row[4],
                'has_content': bool(row[5]),  # content
                'doc_id': row[6],
                'document_status': row[7],
                'status_message': row[8],
                'download_url': row[9],
                'created_at': created_at if isinstance(created_at, str) else (created_at.isoformat() if created_at else datetime.now().isoformat()),
                'updated_at': updated_at if isinstance(updated_at, str) else (updated_at.isoformat() if updated_at else datetime.now().isoformat())
            }
            items.append(paper)
        
        # 构建响应
        result = {
            'status': 'success',
            'data': {
                'items': items,
                'total': total,
                'pages': pages,
                'current_page': page,
                'per_page': per_page
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        logging.error(f"获取论文历史记录出错: {str(e)}\n{error_detail}")
        return jsonify({
            'status': 'error',
            'message': f"获取历史记录失败: {str(e)}"
        }), 500

@academic_paper_bp.route('/history/<int:paper_id>', methods=['GET'])
def get_paper_detail(paper_id):
    """
    获取单个论文记录详情
    
    参数:
        paper_id: 论文ID
        
    返回:
        论文详情
    """
    try:
        paper = AcademicPaper.query.get(paper_id)
        
        if not paper:
            return jsonify({
                'status': 'error',
                'message': '论文记录不存在'
            }), 404
            
        # 获取最新状态
        if paper.doc_id and paper.document_status == 'generating':
            # 创建文心API客户端
            partner_id = current_app.config.get('WENCHAIN_PARTNER_ID')
            api_secret = current_app.config.get('WENCHAIN_API_SECRET')
            client = WenchainClient(partner_id, api_secret)
            
            # 调用API检查状态
            try:
                # 最新的文档状态
                status_result = client.check_document_status(paper.doc_id)
                if status_result:
                    # 更新数据库中的状态
                    paper.document_status = status_result.get('document_status', paper.document_status)
                    paper.status_message = status_result.get('message', paper.status_message)
                    
                    # 如果状态是已完成，尝试获取下载链接
                    if paper.document_status == 'completed' and not paper.download_url:
                        download_result = client.download_paper(paper.doc_id)
                        if download_result and download_result.startswith('http'):
                            paper.download_url = download_result
                    
                    db.session.commit()
            except Exception as e:
                logging.error(f"更新论文状态出错: {str(e)}")
                # 错误时不影响正常获取记录
        
        return jsonify({
            'status': 'success',
            'data': paper.to_dict()
        })
        
    except Exception as e:
        logging.error(f"获取论文详情出错: {str(e)}")
        return jsonify({
            'status': 'error', 
            'message': f"获取论文详情失败: {str(e)}"
        }), 500

@academic_paper_bp.route('/history/<int:paper_id>', methods=['DELETE'])
def delete_paper_history(paper_id):
    """
    删除指定ID的论文记录
    
    参数:
        paper_id: 论文记录ID
        
    返回:
        成功或失败的响应
    """
    try:
        # 查询指定ID的论文记录
        paper = db.session.query(AcademicPaper).filter_by(id=paper_id).first()
        
        # 如果记录不存在，返回错误
        if not paper:
            return jsonify({
                'status': 'error',
                'message': f'未找到ID为{paper_id}的论文记录'
            }), 404
            
        # 删除记录
        db.session.delete(paper)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '论文记录已成功删除'
        })
        
    except Exception as e:
        logging.error(f"删除论文记录出错: {str(e)}")
        db.session.rollback()  # 发生错误时回滚事务
        return jsonify({
            'status': 'error',
            'message': f"删除论文记录失败: {str(e)}"
        }), 500

# 添加研报大纲路由
@academic_paper_bp.route('/report_outline', methods=['OPTIONS'])
def report_outline_options():
    """处理OPTIONS请求"""
    return '', 200

@academic_paper_bp.route('/report_outline', methods=['POST'])
def report_outline():
    """处理研报大纲生成请求 - 通过JSON API"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        rebuild_times = data.get('rebuild_times', 0)
        user_id = data.get('user_id')  # 可选参数
        
        if not content:
            return jsonify({
                'status': 'error',
                'message': '请提供研报主题'
            }), 400
        
        # 获取百度文心API的配置
        partner_id = current_app.config.get('WENCHAIN_PARTNER_ID', '8980934e767f5acfa1c7cd92')
        api_secret = current_app.config.get('WENCHAIN_API_SECRET', 'N64IJm!e#iAWsac')
        
        if not partner_id or not api_secret:
            current_app.logger.error("未配置百度文心API凭证")
            return jsonify({
                'status': 'error',
                'message': '服务配置错误，请联系管理员'
            }), 500
        
        # 创建文心API客户端
        client = WenchainClient(partner_id, api_secret)
        
        # 调用API生成大纲
        result = client.report_outline(content, rebuild_times)
        
        if result and result.get("content"):
            # 创建论文记录
            try:
                # 使用API返回的标题或默认使用请求内容作为标题
                title = result.get("title") or content
                
                # 获取queryID，这将在后续生成研报时使用
                query_id = result.get("queryID", "")
                
                # 创建并保存记录
                paper = AcademicPaper(
                    user_id=user_id,
                    title=title,
                    query=content,
                    outline=result["content"],
                    document_status='none',  # 目前只有大纲，没有研报内容
                    query_id=query_id,  # 保存queryID
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(paper)
                db.session.commit()
                
                # 返回响应时包含记录ID和queryID
                return jsonify({
                    'status': 'success',
                    'data': result["content"],
                    'title': result.get("title", ""),
                    'subtitle': result.get("subtitle", ""),
                    'paper_id': paper.id,
                    'queryID': query_id  # 包含queryID
                })
            except Exception as e:
                logging.error(f"保存研报记录失败: {str(e)}")
                # 即使保存记录失败，也返回生成的大纲
                return jsonify({
                    'status': 'success',
                    'data': result["content"],
                    'title': result.get("title", ""),
                    'subtitle': result.get("subtitle", ""),
                    'queryID': result.get("queryID", ""),  # 包含queryID
                    'message': '大纲生成成功，但保存历史记录失败'
                })
        else:
            return jsonify({
                'status': 'error',
                'message': '生成研报大纲失败'
            }), 500
    except Exception as e:
        current_app.logger.error(f"生成研报大纲时发生错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'服务异常: {str(e)}'
        }), 500

# 在文件末尾适当位置添加report_from_outline路由
@academic_paper_bp.route('/report_from_outline', methods=['POST'])
def report_from_outline():
    """从大纲生成研报的API端点"""
    try:
        start_time = time.time()
        data = request.get_json()
        
        # 记录完整的请求参数
        current_app.logger.info(f"[/report_from_outline] 收到请求参数: {json.dumps(data, ensure_ascii=False)}")
        print(f"[DEBUG] [/report_from_outline] 收到请求参数: {json.dumps(data, ensure_ascii=False)}")
        
        # 获取必要参数
        title = data.get('title', '')
        outline = data.get('outline', '')
        paper_id = data.get('paper_id')  # 可选，如果提供了，将更新对应的记录
        user_id = data.get('user_id')    # 可选，用于创建新记录
        query_id = data.get('queryID', '') # 可选，查询ID
        
        if not title:
            current_app.logger.warning("[/report_from_outline] 未提供研报标题")
            return jsonify({
                'status': 'error',
                'message': '请提供研报标题'
            }), 400
            
        if not outline:
            current_app.logger.warning("[/report_from_outline] 未提供研报大纲")
            return jsonify({
                'status': 'error',
                'message': '请提供研报大纲'
            }), 400
        
        # 记录处理的参数
        current_app.logger.info(f"[/report_from_outline] 处理参数: title={title}, outline长度={len(outline)}, paper_id={paper_id}")
        print(f"[DEBUG] [/report_from_outline] 处理参数: title={title}, outline长度={len(outline)}, paper_id={paper_id}")
        
        # 获取百度文心API的配置
        partner_id = current_app.config.get('WENCHAIN_PARTNER_ID')
        api_secret = current_app.config.get('WENCHAIN_API_SECRET')
        
        if not partner_id or not api_secret:
            current_app.logger.error("[/report_from_outline] 未配置百度文心API凭证")
            print("[DEBUG] [/report_from_outline] 未配置百度文心API凭证")
            return jsonify({
                'status': 'error',
                'message': '服务配置错误，请联系管理员'
            }), 500
        
        # 创建文心API客户端
        client = WenchainClient(partner_id, api_secret)
        
        # 调用API生成研报
        current_app.logger.info(f"[/report_from_outline] 开始生成研报，标题: {title}")
        print(f"[DEBUG] [/report_from_outline] 开始生成研报，标题: {title}")
        
        # 记录调用开始时间
        api_call_start = time.time()
        
        # 如果提供了queryID，传递给API调用
        if query_id:
            current_app.logger.info(f"[/report_from_outline] 使用queryID: {query_id}")
            print(f"[DEBUG] [/report_from_outline] 使用queryID: {query_id}")
            content, doc_id, status_message = client.generate_full_report(title, outline, query_id)
        else:
            current_app.logger.warning(f"[/report_from_outline] 未提供queryID，可能导致API调用失败")
            print(f"[DEBUG] [/report_from_outline] 未提供queryID，可能导致API调用失败")
            content, doc_id, status_message = client.generate_full_report(title, outline)
            
        api_call_end = time.time()
        api_call_duration = api_call_end - api_call_start
        
        end_time = time.time()
        process_time = end_time - start_time
        
        current_app.logger.info(f"[/report_from_outline] 研报生成请求完成，总处理时间: {process_time:.2f}秒, 实际API调用时间: {api_call_duration:.2f}秒, 文档ID: {doc_id}")
        print(f"[DEBUG] [/report_from_outline] 研报生成请求完成，总处理时间: {process_time:.2f}秒, 实际API调用时间: {api_call_duration:.2f}秒, 文档ID: {doc_id}")
        
        # 确定文档状态
        document_status = "generating"
        if status_message == "research_report_generating":
            document_status = "generating"
        elif not doc_id:
            document_status = "failed"
            current_app.logger.error(f"[/report_from_outline] 未能获取文档ID，请求失败")
            print(f"[DEBUG] [/report_from_outline] 未能获取文档ID，请求失败")
        else:
            current_app.logger.info(f"[/report_from_outline] 成功获取文档ID: {doc_id}")
            print(f"[DEBUG] [/report_from_outline] 成功获取文档ID: {doc_id}")
        
        # 保存或更新记录
        try:
            if paper_id:
                # 查找现有记录
                paper = AcademicPaper.query.get(paper_id)
                
                if paper:
                    # 更新记录
                    paper.title = title
                    paper.outline = outline
                    if doc_id:
                        paper.doc_id = doc_id
                        current_app.logger.info(f"[/report_from_outline] 更新记录的文档ID: {doc_id}")
                        print(f"[DEBUG] [/report_from_outline] 更新记录的文档ID: {doc_id}")
                    paper.document_status = document_status
                    paper.status_message = status_message
                    
                    # 如果有内容，也更新内容
                    if content:
                        paper.content = content
                        
                    db.session.commit()
                    current_app.logger.info(f"[/report_from_outline] 更新研报记录成功，ID: {paper.id}, 文档ID: {doc_id}")
                    print(f"[DEBUG] [/report_from_outline] 更新研报记录成功，ID: {paper.id}, 文档ID: {doc_id}")
                else:
                    current_app.logger.warning(f"[/report_from_outline] 未找到指定ID的论文记录: {paper_id}")
                    print(f"[DEBUG] [/report_from_outline] 未找到指定ID的论文记录: {paper_id}")
                    # 创建新记录
                    paper = AcademicPaper(
                        user_id=user_id,
                        title=title,
                        query=title,  # 使用标题作为查询
                        outline=outline,
                        content=content if content else None,
                        doc_id=doc_id,
                        document_status=document_status,
                        status_message=status_message,
                        query_id=query_id,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.session.add(paper)
                    db.session.commit()
                    current_app.logger.info(f"[/report_from_outline] 创建新研报记录成功，ID: {paper.id}, 文档ID: {doc_id}")
                    print(f"[DEBUG] [/report_from_outline] 创建新研报记录成功，ID: {paper.id}, 文档ID: {doc_id}")
                    paper_id = paper.id
            else:
                # 创建新记录
                paper = AcademicPaper(
                    user_id=user_id,
                    title=title,
                    query=title,  # 使用标题作为查询
                    outline=outline,
                    content=content if content else None,
                    doc_id=doc_id,
                    document_status=document_status,
                    status_message=status_message,
                    query_id=query_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(paper)
                db.session.commit()
                current_app.logger.info(f"[/report_from_outline] 创建新研报记录成功，ID: {paper.id}, 文档ID: {doc_id}")
                print(f"[DEBUG] [/report_from_outline] 创建新研报记录成功，ID: {paper.id}, 文档ID: {doc_id}")
                paper_id = paper.id
                
        except Exception as e:
            current_app.logger.error(f"[/report_from_outline] 保存研报记录失败: {str(e)}")
            print(f"[DEBUG] [/report_from_outline] 保存研报记录失败: {str(e)}")
            # 记录保存失败，但仍返回生成的内容
            return jsonify({
                'status': 'success',
                'message': '研报生成请求已提交，但保存记录失败',
                'data': {
                    'doc_id': doc_id,
                    'document_status': document_status
                }
            })
            
        # 返回成功响应
        response_data = {
            'status': 'success',
            'message': '研报生成请求已提交',
            'data': {
                'doc_id': doc_id,
                'document_status': document_status,
                'paper_id': paper_id
            }
        }
        current_app.logger.info(f"[/report_from_outline] 返回响应: {json.dumps(response_data, ensure_ascii=False)}")
        print(f"[DEBUG] [/report_from_outline] 返回响应: {json.dumps(response_data, ensure_ascii=False)}")
        return jsonify(response_data)
        
    except Exception as e:
        stack_trace = traceback.format_exc()
        current_app.logger.error(f"[/report_from_outline] 生成研报时发生错误: {str(e)}\n{stack_trace}")
        print(f"[DEBUG] [/report_from_outline] 生成研报时发生错误: {str(e)}\n{stack_trace}")
        return jsonify({
            'status': 'error',
            'message': f'服务异常: {str(e)}'
        }), 500

# 添加一个测试接口，用于测试状态更新功能
@academic_paper_bp.route('/test_update_status', methods=['POST'])
def test_update_status():
    """
    测试状态更新接口 - 仅用于开发测试
    
    请求参数:
        paper_id: 论文记录ID
    
    返回:
        更新结果
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "请求参数为空"
            }), 400
        
        # 获取论文ID
        paper_id = data.get('paper_id')
        
        if not paper_id:
            return jsonify({
                "status": "error",
                "message": "缺少paper_id参数"
            }), 400
        
        logging.info(f"[测试API] 开始强制更新状态: paper_id={paper_id}")
        
        # 尝试更新状态 - 使用ORM方式
        paper = db.session.query(AcademicPaper).filter(AcademicPaper.id == paper_id).with_for_update().first()
        if not paper:
            return jsonify({
                "status": "error",
                "message": f"未找到ID为{paper_id}的论文记录"
            }), 404
        
        # 记录更新前状态
        old_status = paper.document_status
        old_url = paper.download_url
        
        # 更新状态和下载链接
        paper.document_status = 'completed'
        paper.status_message = '论文生成完成，可以下载(测试更新)'
        paper.download_url = f"https://example.com/test-download-link/{paper_id}?t={int(time.time())}"
        
        # 强制更新时间戳
        from datetime import datetime
        paper.updated_at = datetime.now()
        
        try:
            # 提交更新
            db.session.commit()
            
            # 二次验证 - 使用查询方式而非get方法
            updated_paper = db.session.query(AcademicPaper).filter(AcademicPaper.id == paper_id).first()
            
            return jsonify({
                "status": "success",
                "message": "状态更新成功",
                "data": {
                    "paper_id": paper_id,
                    "old_status": old_status,
                    "new_status": updated_paper.document_status,
                    "old_url": old_url,
                    "new_url": updated_paper.download_url,
                    "updated_at": updated_paper.updated_at.isoformat() if updated_paper.updated_at else None
                }
            })
        except Exception as e:
            db.session.rollback()
            logging.error(f"[测试API] 更新失败: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"更新失败: {str(e)}"
            }), 500
        
    except Exception as e:
        logging.error(f"[测试API] 处理请求时出错: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"处理请求时出错: {str(e)}"
        }), 500