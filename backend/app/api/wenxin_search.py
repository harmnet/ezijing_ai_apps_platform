"""
文心AI综合搜索服务
提供调用百度文心平台AI搜索能力的接口
"""

import os
import json
import time
import hashlib
import logging
import requests
from flask import Blueprint, request, Response, stream_with_context, current_app, jsonify

# 创建蓝图
wenxin_search_bp = Blueprint('wenxin_search', __name__)

# 配置日志
logger = logging.getLogger(__name__)

# API认证参数
PARTNER_ID = "8980934e767f5acfa1c7cd92"
PARTNER_KEY = "N64IJm!e#iAWsac"
BASE_URL = "https://wenchain.baidu.com/wenchain/partner"

def generate_timestamp():
    """生成毫秒级时间戳"""
    return int(time.time() * 1000)

def generate_auth(partner_id, partner_key, ts):
    """生成认证签名"""
    string_to_sign = f"{partner_id}+{partner_key}+{ts}"
    return hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()

@wenxin_search_bp.route('/ai-search', methods=['POST'])
def ai_search():
    """
    AI综合搜索接口
    接收用户查询并调用文心API进行AI搜索
    
    请求参数:
    {
        "userID": "可选，用户ID",
        "userQuery": "必填，查询内容"
    }
    
    返回结果:
    Server-Sent Events格式的流式响应
    """
    try:
        data = request.get_json()
        
        # 验证必填参数
        if not data or 'userQuery' not in data or not data['userQuery'].strip():
            return jsonify({
                'errCode': 400001,
                'errMsg': '缺少必填参数 userQuery 或 userQuery 为空'
            }), 400
            
        user_query = data['userQuery']
        user_id = data.get('userID', '')  # 可选参数
        
        # 生成认证信息
        ts = generate_timestamp()
        auth = generate_auth(PARTNER_ID, PARTNER_KEY, ts)
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            "PartnerID": PARTNER_ID,
            "TS": str(ts),
            "Authorization": auth,
            "Version": "1.0.1"
        }
        
        # 构建请求体
        request_data = {
            "userQuery": user_query
        }
        
        # 如果提供了用户ID，则添加到请求中
        if user_id:
            request_data["userID"] = user_id
            
        logger.info(f"发送AI搜索请求: userQuery={user_query}, userID={user_id}")
        
        # 创建流式响应函数
        def generate():
            try:
                with requests.post(
                    f"{BASE_URL}/aisearch", 
                    headers=headers, 
                    json=request_data, 
                    stream=True
                ) as response:
                    # 检查响应状态
                    if response.status_code != 200:
                        logger.error(f"AI搜索请求失败: {response.status_code} - {response.text}")
                        # 返回错误信息
                        error_msg = f"event:error\ndata: {{\"errCode\":{response.status_code},\"errMsg\":\"请求失败: {response.text}\"}}\n\n"
                        yield error_msg
                        return
                    
                    # 解析并转发流式响应
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            logger.debug(f"接收到响应行: {decoded_line}")
                            yield decoded_line + '\n'
                            
                            # 如果是最后一条消息，添加额外的换行符
                            if 'event:lastMessage' in decoded_line:
                                yield '\n'
                                
                    # 确保响应正确终止
                    yield '\n'
                
            except Exception as e:
                logger.error(f"处理AI搜索请求时发生错误: {str(e)}")
                error_msg = f"event:error\ndata: {{\"errCode\":500,\"errMsg\":\"服务器内部错误: {str(e)}\"}}\n\n"
                yield error_msg
        
        # 返回流式响应
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',  # 禁用Nginx缓冲
                'Connection': 'keep-alive'
            }
        )
        
    except Exception as e:
        logger.exception(f"AI搜索接口发生异常: {str(e)}")
        return jsonify({
            'errCode': 500,
            'errMsg': f"服务器内部错误: {str(e)}"
        }), 500

# 添加一个测试接口，便于检查接口是否正常注册
@wenxin_search_bp.route('/test', methods=['GET'])
def test():
    """测试接口是否正常注册"""
    return jsonify({
        'status': 'ok',
        'message': 'AI搜索服务正常运行'
    }) 