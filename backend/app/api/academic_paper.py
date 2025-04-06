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
from flask import Blueprint, request, Response, current_app, jsonify, stream_with_context
import logging

academic_paper_bp = Blueprint('academic_paper', __name__)

class WenchainClient:
    """百度文心API客户端"""
    
    def __init__(self, partner_id, api_secret):
        self.partner_id = partner_id.strip()
        self.api_secret = api_secret.strip()  # 确保API密钥不含有空格
        self.base_url = "https://wenchain.baidu.com/wenchain/partner"
    
    def _generate_timestamp(self):
        # 获取当前UTC时间
        utc_now = datetime.utcnow()
        # 转换为北京时间 (UTC+8)
        beijing_time = utc_now + timedelta(hours=8)
        # 转换为毫秒级时间戳
        ts_milliseconds = int(beijing_time.timestamp() * 1000)
        # 记录生成的时间戳
        logging.info(f"UTC时间: {utc_now}")
        logging.info(f"北京时间: {beijing_time}")
        logging.info(f"毫秒级时间戳TS: {ts_milliseconds}")
        return ts_milliseconds
    
    def _generate_auth_header(self, ts):
        # 生成认证头 - 正确格式: MD5(PartnerID+PartnerKey+TS)
        # 注意保留+号，这里使用字符串拼接
        string_to_sign = self.partner_id + self.api_secret + str(ts)
        
        # 使用MD5生成签名
        signature = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()
        
        # 记录生成的认证头
        logging.info(f"签名字符串格式: PartnerID+PartnerKey+TS")
        logging.info(f"签名字符串长度: {len(string_to_sign)}")
        logging.info(f"MD5签名: {signature}")
        
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
        
        # 记录完整的请求信息用于调试
        logging.info(f"发送请求到百度文心API: URL={url}")
        logging.info(f"使用PartnerID: {self.partner_id}")
        logging.info(f"时间戳TS: {ts}, 对应时间: {datetime.utcnow() + timedelta(hours=15)}")
        logging.info(f"Authorization: {auth}")
        
        data = {"userQuery": query}
        logging.info(f"请求体: {json.dumps(data)}")
        
        try:
            # 使用流式响应
            response = requests.post(url, headers=headers, json=data, stream=True)
            
            # 记录响应状态和头信息
            logging.info(f"百度文心API响应状态码: {response.status_code}")
            logging.info(f"百度文心API响应头: {response.headers}")
            
            if response.status_code != 200:
                logging.error(f"百度文心API请求失败: {response.status_code} - {response.text}")
                return None
                
            # 处理流式响应
            content = ""
            all_content = []
            saved_content = None  # 用于保存有效的大纲内容
            
            # 用于解析SSE格式
            current_event = None
            current_data = ""
            
            for line in response.iter_lines():
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
                # 返回所有消息用于调试
                return json.dumps(all_content)
            
            return content
        except Exception as e:
            logging.error(f"请求异常: {str(e)}")
            return None

@academic_paper_bp.route('/paper_outline', methods=['POST'])
def paper_outline():
    query = request.json.get("query", "")
    if not query:
        return jsonify({"status": "error", "message": "查询不能为空"})
    
    # 初始化日志记录
    logging.info(f"收到论文大纲生成请求: {query}")
    start_time = time.time()
    
    # 从环境变量获取API凭证
    partner_id = os.environ.get("WENCHAIN_PARTNER_ID", "").strip()
    partner_key = os.environ.get("WENCHAIN_API_SECRET", "").strip()
    
    if not partner_id or not partner_key:
        logging.error("未配置百度文心API凭证")
        return jsonify({"status": "error", "message": "未配置API凭证"})
    
    # 生成北京时区的毫秒级时间戳 (UTC+8)
    # 获取当前UTC时间
    utc_now = datetime.utcnow()
    # 转换为北京时间 (UTC+8)
    beijing_time = utc_now + timedelta(hours=8)
    # 转换为毫秒级时间戳
    ts_milliseconds = int(beijing_time.timestamp() * 1000)
    
    logging.info(f"UTC时间: {utc_now}")
    logging.info(f"北京时间: {beijing_time}")
    logging.info(f"毫秒级时间戳TS: {ts_milliseconds}")
    
    # 生成认证签名 - 正确格式: MD5(PartnerID+PartnerKey+TS)
    # 注意保留+号，这里使用字符串拼接
    string_to_sign = partner_id + partner_key + str(ts_milliseconds)
    logging.info(f"签名字符串格式: PartnerID+PartnerKey+TS")
    logging.info(f"签名字符串长度: {len(string_to_sign)}")
    
    # 使用MD5生成签名
    signature = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()
    logging.info(f"MD5签名: {signature}")
    
    # 准备请求
    url = "https://wenchain.baidu.com/wenchain/partner/paperoutline"
    headers = {
        "Content-Type": "application/json",
        "PartnerID": partner_id,
        "TS": str(ts_milliseconds),
        "Authorization": signature,
        "Accept": "text/event-stream"  # 明确指定接受SSE格式
    }
    
    data = {"userQuery": query}
    
    # 记录请求信息
    logging.info(f"发送请求: URL={url}, PartnerID={partner_id}, TS={ts_milliseconds}, Auth={signature}")
    
    try:
        # 使用流式请求
        response = requests.post(url, headers=headers, json=data, stream=True, timeout=15)
        
        # 检查响应
        logging.info(f"响应状态码: {response.status_code}, 内容类型: {response.headers.get('Content-Type')}")
        
        if response.status_code != 200:
            logging.error(f"请求失败: {response.status_code} - {response.text}")
            return jsonify({
                "status": "error",
                "message": f"API请求失败，状态码: {response.status_code}",
                "details": response.text
            })
        
        # 处理SSE流式响应
        sse_content = []
        outline_content = None
        has_error = False
        
        # 收集所有SSE消息
        for line in response.iter_lines():
            if not line:
                continue
            
            line_str = line.decode('utf-8')
            sse_content.append(line_str)
            
            # 检查是否包含错误消息
            if 'errCode' in line_str and ('TS expires' in line_str or 'Authorization' in line_str):
                logging.warning(f"认证错误: {line_str}")
                has_error = True
                continue
            
            # 检查是否有有效内容
            if '"raw"' in line_str and '"data"' in line_str and 'null' not in line_str:
                try:
                    # 提取data部分
                    if line_str.startswith('data: '):
                        data_json = json.loads(line_str[6:])
                        if data_json.get('raw') and data_json['raw'] and data_json['raw'].get('data'):
                            outline_content = data_json['raw']['data']
                            logging.info(f"找到有效内容: {outline_content[:100]}...")
                except Exception as e:
                    logging.error(f"解析SSE内容出错: {str(e)}")
        
        # 如果找到了有效内容，返回
        if outline_content:
            logging.info(f"成功获取论文大纲内容，长度: {len(outline_content)}")
            return jsonify({
                "status": "success",
                "message": "成功生成论文大纲",
                "data": outline_content
            })
        
        # 返回原始SSE内容用于调试
        sse_text = "\n".join(sse_content)
        logging.info(f"未找到有效内容，返回原始SSE响应: {len(sse_text)} 字节")
        
        # 如果遇到认证错误，返回错误状态
        if has_error:
            return jsonify({
                "status": "error", 
                "message": "API认证失败",
                "data": sse_text,
                "raw_response": {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content_type": response.headers.get("Content-Type", ""),
                    "timestamp_used": ts_milliseconds,
                    "auth_used": signature
                }
            })
        
        # 否则返回成功状态
        return jsonify({
            "status": "success", 
            "message": "API调用成功，但未找到有效内容",
            "data": sse_text,
            "raw_response": {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_type": response.headers.get("Content-Type", ""),
                "timestamp_used": ts_milliseconds,
                "auth_used": signature
            }
        })
                
    except Exception as e:
        logging.error(f"请求失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"请求文心API时出错",
            "error_details": str(e)
        })

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
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>论文大纲生成测试</h1>
        <p>输入论文主题，生成大纲结构</p>
        
        <textarea id="query" placeholder="请输入论文主题，例如：人工智能在医疗领域的应用"></textarea>
        <button class="button" id="generate">生成大纲</button>
        
        <h3>结果：</h3>
        <div id="result">结果将在这里显示...</div>
        
        <script>
            document.getElementById('generate').addEventListener('click', async function() {
                const query = document.getElementById('query').value.trim();
                if (!query) {
                    alert('请输入论文主题');
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
    return Response(test_html, mimetype='text/html')