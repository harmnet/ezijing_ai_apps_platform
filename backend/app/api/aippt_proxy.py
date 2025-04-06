"""
AIPPT API代理模块
用于转发前端请求到AIPPT的API服务，解决跨域问题
"""

import requests
import logging
import json
import time
import hmac
import hashlib
import base64
import sys
from flask import Blueprint, request, Response, jsonify, current_app
from datetime import datetime

# 创建蓝图
aippt_proxy_bp = Blueprint('aippt_proxy', __name__)

# 配置日志记录器
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger('aippt_proxy')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# AIPPT API信息
AIPPT_API_BASE = 'https://co.aippt.cn/api'
API_KEY = '673e95c065226'
SECRET_KEY = '7bVcH15FeB1zTy08PN5n3YtmRxsVXjEv'

# Token缓存
token_cache = {
    'token': None,
    'expire_time': 0
}

def generate_aippt_signature(method, uri, timestamp, api_key, api_secret):
    """
    生成AIPPT API的签名
    参数：
    - method: 请求方法（GET、POST等）
    - uri: 请求的URI路径 (格式应为 /api/xxx/)
    - timestamp: 时间戳
    - api_key: API密钥
    - api_secret: API密钥对应的密钥
    """
    # 标准化URI格式
    # 1. 去掉可能存在的/api前缀
    if uri.startswith('/api/'):
        uri = uri[4:]
    elif uri.startswith('api/'):
        uri = uri[3:]

    # 2. 确保以/开头
    if not uri.startswith('/'):
        uri = '/' + uri
    
    # 3. 确保以/结尾
    if not uri.endswith('/'):
        uri = uri + '/'
    
    # 4. 添加/api前缀，构造最终签名URI
    final_uri = '/api' + uri
    
    # 构造签名字符串
    string_to_sign = f"{method}@{final_uri}@{timestamp}"
    logger.debug(f"签名字符串：{string_to_sign}")
    
    # 使用HMAC-SHA1算法和密钥对字符串进行签名，完全按照官方文档要求
    hmac_sha1 = hmac.new(
        api_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha1
    )
    
    # 将结果转为Base64编码，按照官方文档要求
    signature = base64.b64encode(hmac_sha1.digest()).decode('utf-8')
    logger.debug(f"生成的签名: {signature}")
    
    return signature

def get_cached_token():
    """获取缓存的token，如果过期则返回None"""
    global token_cache
    now = int(time.time())
    
    # 检查缓存的token是否存在且未过期（预留1小时安全边界）
    if token_cache['token'] and now < token_cache['expire_time'] - 3600:
        logger.info(f"使用缓存的token: {token_cache['token'][:10]}...")
        logger.info(f"token过期时间: {datetime.fromtimestamp(token_cache['expire_time']).strftime('%Y-%m-%d %H:%M:%S')}")
        return token_cache['token']
    
    return None

def fetch_new_token():
    """获取新的token"""
    global token_cache
    
    logger.info("正在获取新token...")
    
    # 构造API请求
    uri = '/api/grant/token/'
    params = {
        'uid': '1',
        'channel': 'ezijing'
    }
    
    # 获取AIPPT API需要的请求头
    timestamp = int(time.time())
    headers = get_aippt_headers('GET', uri)
    
    # 构建目标URL
    target_url = f"{AIPPT_API_BASE}/grant/token/"
    
    try:
        # 发送GET请求
        response = requests.get(
            target_url,
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"获取token失败，状态码: {response.status_code}")
            return None
        
        data = response.json()
        
        if data['code'] == 0 and data['data'] and data['data']['token']:
            # 更新缓存
            now = int(time.time())
            token_cache['token'] = data['data']['token']
            # 官方文档指明token有效期为30天
            token_cache['expire_time'] = now + (data['data']['time_expire'] or 30 * 24 * 3600)
            
            logger.info(f"获取到新token: {token_cache['token'][:10]}...")
            logger.info(f"token过期时间: {datetime.fromtimestamp(token_cache['expire_time']).strftime('%Y-%m-%d %H:%M:%S')}")
            
            return token_cache['token']
        else:
            logger.error(f"获取token响应错误: {data['msg']}")
            return None
    except Exception as e:
        logger.error(f"获取token异常: {str(e)}")
        return None

def get_aippt_headers(method, uri, token=None):
    """获取AIPPT API请求头"""
    timestamp = int(time.time())
    signature = generate_aippt_signature(method, uri, timestamp, API_KEY, SECRET_KEY)
    
    headers = {
        'x-api-key': API_KEY,
        'x-timestamp': str(timestamp),
        'x-signature': signature,
        'x-channel': '',  # 根据官方示例添加空的x-channel头
        'Accept': 'application/json'
    }
    
    # 添加token，如果提供了的话
    if token:
        token = token.strip()  # 去除可能的前后空格
        if token:
            logger.debug(f"请求头中添加token: {token[:10]}...")
            headers['x-token'] = token
    
    return headers

@aippt_proxy_bp.route('/test', methods=['GET'])
def test_proxy():
    """测试代理是否正常工作"""
    logger.info("调用测试接口: /test")
    return jsonify({
        'code': 0,
        'msg': 'AIPPT代理服务正常工作',
        'data': {
            'api_key': API_KEY,
            'timestamp': int(time.time())
        }
    })

@aippt_proxy_bp.route('/api-test', methods=['GET'])
def api_test():
    """测试真实API调用"""
    logger.info("测试真实API调用")
    
    try:
        # 构造API请求
        uri = '/api/grant/token/'
        params = {
            'uid': '1',
            'channel': 'ezijing'
        }
        
        # 获取AIPPT API需要的请求头
        headers = get_aippt_headers('GET', uri)
        
        # 构建目标URL
        target_url = f"{AIPPT_API_BASE}/grant/token/"
        
        logger.info(f"发送请求到: {target_url}?uid=1&channel=ezijing")
        logger.info(f"请求头: {headers}")
        
        # 发送GET请求
        aippt_response = requests.get(
            target_url,
            headers=headers,
            params=params,
            timeout=30
        )
        
        logger.info(f"API响应状态码: {aippt_response.status_code}")
        
        try:
            response_data = aippt_response.json()
            logger.info(f"API响应内容: {json.dumps(response_data, ensure_ascii=False)}")
            return jsonify(response_data)
        except Exception as e:
            logger.error(f"解析响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析响应失败: {str(e)}',
                'raw': aippt_response.text
            })
    
    except Exception as e:
        logger.error(f"API测试失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'API测试失败: {str(e)}'
        }), 500

@aippt_proxy_bp.route('/', defaults={'path': ''})
@aippt_proxy_bp.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_aippt_api(path):
    """代理AIPPT API的请求"""
    logger.debug(f"收到代理请求: {request.method} {path}")
    logger.debug(f"请求头: {dict(request.headers)}")
    
    if request.method == 'OPTIONS':
        return handle_options_request()
    
    # 处理获取token的请求
    if path == 'grant/token' and request.method == 'GET':
        # 检查是否有缓存的有效token
        cached_token = get_cached_token()
        if cached_token:
            # 如果有缓存的有效token，直接返回
            logger.info("使用缓存的token响应请求")
            return jsonify({
                'code': 0,
                'data': {
                    'api_key': API_KEY,
                    'uid': '1',
                    'token': cached_token,
                    'time_expire': token_cache['expire_time'] - int(time.time())
                },
                'msg': 'ok'
            })
        else:
            # 否则获取新的token
            new_token = fetch_new_token()
            if new_token:
                return jsonify({
                    'code': 0,
                    'data': {
                        'api_key': API_KEY,
                        'uid': '1',
                        'token': new_token,
                        'time_expire': token_cache['expire_time'] - int(time.time())
                    },
                    'msg': 'ok'
                })
    
    # 特殊处理路径，直接使用对应的处理函数
    if path == 'design/v2/save' and request.method == 'POST':
        logger.info("检测到设计保存请求，使用特殊处理方式")
        # 获取token
        token = get_cached_token() or fetch_new_token()
        if not token:
            return jsonify({
                "code": 40010, 
                "msg": "Token获取失败",
                "data": None
            }), 401
        
        # 生成时间戳和签名
        timestamp = str(int(time.time()))
        signature = generate_aippt_signature(request.method, f'/api/{path}/', int(timestamp), API_KEY, SECRET_KEY)
        
        # 构建目标URL
        target_url = f"{AIPPT_API_BASE}/{path}"
        logger.info(f"目标URL: {target_url}")
        
        # 构建请求头
        headers = {
            'x-api-key': API_KEY,
            'x-channel': '',
            'x-token': token,
            'x-timestamp': timestamp,
            'x-signature': signature,
            'Accept': 'application/json',
            'User-Agent': 'AIOffice/1.0'
        }
        
        return handle_design_save(request, token, headers, target_url)
    
    # 特殊处理任务创建请求，模仿exact-doc-test的方式处理
    if path == 'ai/chat/v2/task/' and request.method == 'POST':
        logger.info("收到任务创建请求，使用特殊处理方式")
        
        # 从请求中获取任务数据
        task_data = {}
        if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
            task_data = request.form.to_dict()
        elif request.content_type and 'application/json' in request.content_type:
            task_data = request.get_json(silent=True) or {}
        else:
            # 尝试获取form数据
            task_data = request.form.to_dict()
            # 如果没有form数据，尝试从body解析JSON
            if not task_data:
                try:
                    body_data = request.get_json(silent=True)
                    if body_data:
                        task_data = body_data
                except:
                    pass
        
        logger.info(f"任务数据: {task_data}")
        
        # 只处理包含title和type的任务
        if not task_data.get('title'):
            return jsonify({
                'code': 40001,
                'msg': '缺少必要参数title',
                'data': None
            }), 400
        
        # 第一步：获取新token
        logger.info("步骤1: 获取新token")
        token_uri = '/api/grant/token/'
        token_timestamp = int(time.time())
        token_signature = generate_aippt_signature('GET', token_uri, token_timestamp, API_KEY, SECRET_KEY)
        
        token_headers = {
            'x-api-key': API_KEY,
            'x-timestamp': str(token_timestamp),
            'x-signature': token_signature,
            'Accept': 'application/json'
        }
        
        token_url = f"{AIPPT_API_BASE}/grant/token/"
        token_params = {
            'uid': '1',
            'channel': ''
        }
        
        try:
            # 发送获取token请求
            token_response = requests.get(
                token_url,
                headers=token_headers,
                params=token_params,
                timeout=30
            )
            
            token_result = token_response.json()
            if token_result['code'] != 0 or not token_result.get('data') or not token_result['data'].get('token'):
                logger.error(f"获取token失败: {token_result.get('msg')}")
                return jsonify(token_result)
            
            new_token = token_result['data']['token']
            logger.info(f"成功获取新token: {new_token[:10]}...")
            
            # 第二步：使用新token创建任务
            logger.info("步骤2: 使用新token创建任务")
            task_uri = '/api/ai/chat/v2/task/'
            task_timestamp = int(time.time())
            task_signature = generate_aippt_signature('POST', task_uri, task_timestamp, API_KEY, SECRET_KEY)
            
            task_headers = {
                'x-api-key': API_KEY,
                'x-timestamp': str(task_timestamp),
                'x-signature': task_signature,
                'x-token': new_token,
                'x-channel': '',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
            
            # 使用前端传来的title和type，默认值处理
            final_task_data = {
                'title': task_data.get('title', '人工智能应用'),
                'type': task_data.get('type', '1'),
                'content': task_data.get('content', ''),
                'id': task_data.get('id', '')
            }
            
            logger.info(f"创建任务URL: {AIPPT_API_BASE}/ai/chat/v2/task/")
            logger.info(f"任务请求头: {task_headers}")
            logger.info(f"任务数据: {final_task_data}")
            
            # 发送任务创建请求
            task_response = requests.post(
                f"{AIPPT_API_BASE}/ai/chat/v2/task/",
                headers=task_headers,
                data=final_task_data,
                timeout=30
            )
            
            try:
                task_result = task_response.json()
                logger.info(f"任务创建响应: {json.dumps(task_result, ensure_ascii=False)}")
                return jsonify(task_result)
            except Exception as e:
                logger.error(f"解析任务响应失败: {str(e)}")
                return jsonify({
                    'code': -1,
                    'msg': f'解析任务响应失败: {str(e)}',
                    'raw': task_response.text
                })
        
        except Exception as e:
            logger.error(f"创建任务过程异常: {str(e)}", exc_info=True)
            return jsonify({
                'code': -1,
                'msg': f'创建任务失败: {str(e)}'
            }), 500
    
    # 特殊处理生成大纲数据请求，模仿exact-doc-test的方式处理
    if path == 'generate/data' and request.method == 'POST':
        logger.info("收到生成大纲数据请求，使用特殊处理方式")
        
        # 从请求中获取任务数据
        tree_data = {}
        if request.content_type and 'multipart/form-data' in request.content_type:
            tree_data = request.form.to_dict()
        elif request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
            tree_data = request.form.to_dict()
        elif request.content_type and 'application/json' in request.content_type:
            tree_data = request.get_json(silent=True) or {}
        
        logger.info(f"生成大纲数据: {tree_data}")
        
        # 只处理包含task_id的请求
        if not tree_data.get('task_id'):
            return jsonify({
                'code': 40001,
                'msg': '缺少必要参数task_id',
                'data': None
            }), 400
        
        # 第一步：获取新token
        logger.info("步骤1: 获取新token")
        token_uri = '/api/grant/token/'
        token_timestamp = int(time.time())
        token_signature = generate_aippt_signature('GET', token_uri, token_timestamp, API_KEY, SECRET_KEY)
        
        token_headers = {
            'x-api-key': API_KEY,
            'x-timestamp': str(token_timestamp),
            'x-signature': token_signature,
            'Accept': 'application/json'
        }
        
        token_url = f"{AIPPT_API_BASE}/grant/token/"
        token_params = {
            'uid': '1',
            'channel': ''
        }
        
        try:
            # 发送获取token请求
            token_response = requests.get(
                token_url,
                headers=token_headers,
                params=token_params,
                timeout=30
            )
            
            token_result = token_response.json()
            if token_result['code'] != 0 or not token_result.get('data') or not token_result['data'].get('token'):
                logger.error(f"获取token失败: {token_result.get('msg')}")
                return jsonify(token_result)
            
            new_token = token_result['data']['token']
            logger.info(f"成功获取新token: {new_token[:10]}...")
            
            # 第二步：使用新token获取树形结构数据
            logger.info("步骤2: 使用新token获取大纲数据")
            data_uri = '/api/generate/data/'
            data_timestamp = int(time.time())
            data_signature = generate_aippt_signature('POST', data_uri, data_timestamp, API_KEY, SECRET_KEY)
            
            data_headers = {
                'x-api-key': API_KEY,
                'x-timestamp': str(data_timestamp),
                'x-signature': data_signature,
                'x-token': new_token,
                'x-channel': '',
                'Accept': 'application/json'
            }
            
            # 使用multipart/form-data格式
            data_url = f"{AIPPT_API_BASE}/generate/data/"
            
            logger.info(f"获取大纲数据URL: {data_url}")
            logger.info(f"数据请求头: {data_headers}")
            logger.info(f"请求数据: {tree_data}")
            
            # 发送数据请求
            data_response = requests.post(
                data_url,
                headers=data_headers,
                data=tree_data,  # 使用form表单数据
                timeout=30
            )
            
            try:
                data_result = data_response.json()
                logger.info(f"大纲数据响应: {json.dumps(data_result, ensure_ascii=False)}")
                return jsonify(data_result)
            except Exception as e:
                logger.error(f"解析大纲数据响应失败: {str(e)}")
                return jsonify({
                    'code': -1,
                    'msg': f'解析大纲数据响应失败: {str(e)}',
                    'raw': data_response.text
                })
        
        except Exception as e:
            logger.error(f"获取大纲数据过程异常: {str(e)}", exc_info=True)
            return jsonify({
                'code': -1,
                'msg': f'获取大纲数据失败: {str(e)}'
            }), 500
    
    # 特殊处理保存大纲请求
    if path == 'ai/chat/v2/outline/save' and request.method == 'POST':
        logger.info("收到保存大纲请求，使用特殊处理方式")
        
        # 从请求中获取数据
        outline_data = {}
        if request.content_type and 'multipart/form-data' in request.content_type:
            outline_data = request.form.to_dict()
            logger.info(f"收到multipart/form-data格式数据: {outline_data}")
        elif request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
            outline_data = request.form.to_dict()
            logger.info(f"收到application/x-www-form-urlencoded格式数据: {outline_data}")
        elif request.content_type and 'application/json' in request.content_type:
            outline_data = request.get_json(silent=True) or {}
            logger.info(f"收到application/json格式数据: {outline_data}")
        else:
            logger.warning(f"未知的Content-Type: {request.content_type}")
            outline_data = {}
            # 尝试从多种可能的格式中解析数据
            try:
                outline_data = request.get_json(silent=True) or {}
            except:
                pass
            if not outline_data:
                try:
                    outline_data = request.form.to_dict()
                except:
                    pass
            if not outline_data:
                try:
                    outline_data = dict(request.values)
                except:
                    pass
        
        logger.info(f"保存大纲数据: {outline_data}")
        
        # 检查必要参数
        if not outline_data.get('task_id') or not outline_data.get('content'):
            return jsonify({
                'code': 40001,
                'msg': '缺少必要参数task_id或content',
                'data': None
            }), 400
        
        # 第一步：获取新token
        logger.info("步骤1: 获取新token")
        token_uri = '/api/grant/token/'
        token_timestamp = int(time.time())
        token_signature = generate_aippt_signature('GET', token_uri, token_timestamp, API_KEY, SECRET_KEY)
        
        token_headers = {
            'x-api-key': API_KEY,
            'x-timestamp': str(token_timestamp),
            'x-signature': token_signature,
            'Accept': 'application/json'
        }
        
        token_url = f"{AIPPT_API_BASE}/grant/token/"
        token_params = {
            'uid': '1',
            'channel': ''
        }
        
        try:
            # 发送获取token请求
            token_response = requests.get(
                token_url,
                headers=token_headers,
                params=token_params,
                timeout=30
            )
            
            token_result = token_response.json()
            if token_result['code'] != 0 or not token_result.get('data') or not token_result['data'].get('token'):
                logger.error(f"获取token失败: {token_result.get('msg')}")
                return jsonify(token_result)
            
            new_token = token_result['data']['token']
            logger.info(f"成功获取新token: {new_token[:10]}...")
            
            # 第二步：使用新token保存大纲
            logger.info("步骤2: 使用新token保存大纲")
            outline_uri = '/api/ai/chat/v2/outline/save/'
            outline_timestamp = int(time.time())
            outline_signature = generate_aippt_signature('POST', outline_uri, outline_timestamp, API_KEY, SECRET_KEY)
            
            outline_headers = {
                'x-api-key': API_KEY,
                'x-timestamp': str(outline_timestamp),
                'x-signature': outline_signature,
                'x-token': new_token,
                'x-channel': '',
                'Accept': 'application/json'
            }
            
            # 保存大纲URL
            outline_url = f"{AIPPT_API_BASE}/ai/chat/v2/outline/save/"
            
            logger.info(f"保存大纲URL: {outline_url}")
            logger.info(f"请求头: {outline_headers}")
            logger.info(f"请求数据: {outline_data}")
            
            # 如果请求是multipart/form-data格式的
            if request.content_type and 'multipart/form-data' in request.content_type:
                # 去掉Content-Type头，让requests自动处理
                outline_response = requests.post(
                    outline_url,
                    headers=outline_headers,
                    data=outline_data,
                    files={},  # 空文件字典，让requests设置正确的multipart边界
                    timeout=30
                )
            elif request.content_type and 'application/json' in request.content_type:
                # 对于JSON请求，使用json参数而不是data参数
                outline_headers['Content-Type'] = 'application/json'
                outline_response = requests.post(
                    outline_url,
                    headers=outline_headers,
                    json=outline_data,  # 使用json参数让requests自动处理JSON序列化
                    timeout=30
                )
            else:
                # 尝试直接使用application/x-www-form-urlencoded格式，完全按照官方示例
                try:
                    # 检查content字段是否是JSON字符串格式
                    task_id = outline_data.get('task_id')
                    content = outline_data.get('content')
                    
                    # 按照官方示例的格式组织数据
                    data = {}
                    data['task_id'] = task_id
                    
                    # 确保content是字符串格式
                    if isinstance(content, dict):
                        content = json.dumps(content)
                    data['content'] = content
                    
                    logger.info(f"使用官方示例格式发送请求：{data}")
                    
                    # 使用urlencode编码数据
                    outline_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    outline_response = requests.post(
                        outline_url,
                        headers=outline_headers,
                        data=data,
                        timeout=30
                    )
                except Exception as e:
                    logger.error(f"使用官方示例格式发送请求失败: {str(e)}")
                    # 回退到原来的方式
                    outline_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    outline_response = requests.post(
                        outline_url,
                        headers=outline_headers,
                        data=outline_data,
                        timeout=30
                    )
            
            try:
                outline_result = outline_response.json()
                logger.info(f"保存大纲响应: {json.dumps(outline_result, ensure_ascii=False)}")
                return jsonify(outline_result)
            except Exception as e:
                logger.error(f"解析保存大纲响应失败: {str(e)}")
                return jsonify({
                    'code': -1,
                    'msg': f'解析保存大纲响应失败: {str(e)}',
                    'raw': outline_response.text
                })
        
        except Exception as e:
            logger.error(f"保存大纲过程异常: {str(e)}", exc_info=True)
            return jsonify({
                'code': -1,
                'msg': f'保存大纲失败: {str(e)}'
            }), 500
    
    # 特殊处理模板相关请求
    if request.method == 'GET' and path in ['template_component/suit/select', 'template/recommend/list', 'template_component/suit/search']:
        try:
            # 获取查询参数
            query_params = {}
            for key, value in request.args.to_dict().items():
                if value:
                    query_params[key] = value
            
            # 构建带查询参数的URL
            query_string = ""
            if query_params:
                query_string = "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])
            
            # 获取新token
            logger.info("步骤1: 获取新token")
            token_uri = '/api/grant/token/'
            token_timestamp = int(time.time())
            token_signature = generate_aippt_signature('GET', token_uri, token_timestamp, API_KEY, SECRET_KEY)
            
            token_headers = {
                'x-api-key': API_KEY,
                'x-timestamp': str(token_timestamp),
                'x-signature': token_signature,
                'Accept': 'application/json'
            }
            
            token_url = f"{AIPPT_API_BASE}/grant/token/"
            token_params = {
                'uid': '1',
                'channel': ''
            }
            
            # 发送获取token请求
            token_response = requests.get(
                token_url,
                headers=token_headers,
                params=token_params,
                timeout=30
            )
            
            token_result = token_response.json()
            if token_result['code'] != 0 or not token_result.get('data') or not token_result['data'].get('token'):
                logger.error(f"获取token失败: {token_result.get('msg')}")
                return jsonify(token_result)
            
            new_token = token_result['data']['token']
            logger.info(f"成功获取新token: {new_token[:10]}...")
            
            # 构建请求URL和头部
            template_uri = f"/api/{path}/" 
            template_timestamp = int(time.time())
            template_signature = generate_aippt_signature('GET', template_uri, template_timestamp, API_KEY, SECRET_KEY)
            
            template_headers = {
                'x-api-key': API_KEY,
                'x-timestamp': str(template_timestamp),
                'x-signature': template_signature,
                'x-token': new_token,
                'x-channel': '',
                'Accept': 'application/json'
            }
            
            # 构造请求URL
            template_url = f"{AIPPT_API_BASE}/{path}/{query_string}"
            
            logger.info(f"模板请求URL: {template_url}")
            logger.info(f"请求头: {template_headers}")
            
            # 发送请求
            template_response = requests.get(
                template_url,
                headers=template_headers,
                timeout=30
            )
            
            try:
                template_result = template_response.json()
                logger.info(f"模板响应: {json.dumps(template_result, ensure_ascii=False)}")
                return jsonify(template_result)
            except Exception as e:
                logger.error(f"解析模板响应失败: {str(e)}")
                return jsonify({
                    'code': -1,
                    'msg': f'解析模板响应失败: {str(e)}',
                    'raw': template_response.text
                })
        except Exception as e:
            logger.error(f"处理模板请求时出错: {str(e)}", exc_info=True)
            return jsonify({
                'code': -1,
                'msg': f'处理模板请求时出错: {str(e)}'
            }), 500
    
    # 构建正确的目标URL
    # 如果path是以api开头，则需要移除，因为AIPPT_API_BASE已经包含了/api
    if path.startswith('api/'):
        path = path[4:]
    
    # 确保URL以/结尾，这是API接口要求的
    if not path.endswith('/'):
        path = path + '/'
    
    target_url = f"{AIPPT_API_BASE}/{path}"
    method = request.method
    
    # 获取原始请求中的查询参数
    params = request.args.to_dict()
    
    # 统一处理URI格式
    # 确保URI格式符合签名规范，以斜杠开始和结束
    uri = '/api/' + path
    if not uri.startswith('/'):
        uri = '/' + uri
    if not uri.endswith('/'):
        uri = uri + '/'
    
    # 获取用户请求中的token (可能以不同格式提供)
    token = None
    # 直接使用get方法检查x-token头
    token = request.headers.get('x-token')
    if not token:
        # 检查大写版本
        token = request.headers.get('X-Token')
    
    if token:
        logger.info(f"从请求头中获取到token: {token[:10]}...")
    
    # 如果请求中没有提供token，使用缓存的token
    if not token:
        token = get_cached_token()
        if token:
            logger.info(f"请求中未提供token，使用缓存的token: {token[:10]}...")
    
    # 对于创建任务的请求，总是获取新的token以确保有效性
    if path == 'ai/chat/v2/task/' and method == 'POST':
        logger.info("这是创建任务的请求，获取新的token以确保成功")
        fresh_token = fetch_new_token()
        if fresh_token:
            logger.info(f"获取到新token用于创建任务: {fresh_token[:10]}...")
            token = fresh_token
    
    logger.info(f"签名URI: {uri}")
    
    # 生成请求头（使用最新的签名算法）
    timestamp = int(time.time())
    signature = generate_aippt_signature(method, uri, timestamp, API_KEY, SECRET_KEY)
    
    # 构造符合AIPPT API要求的请求头
    headers = {
        'x-api-key': API_KEY,
        'x-timestamp': str(timestamp),
        'x-signature': signature
    }
    
    # 添加x-channel头（可能为空），这是API要求的
    headers['x-channel'] = request.headers.get('x-channel', '')
    
    # 添加其他需要的头
    if 'Accept' in request.headers:
        headers['Accept'] = request.headers.get('Accept')
    else:
        headers['Accept'] = 'application/json'
    
    # 添加token到请求头（如果有）
    if token:
        token = token.strip()  # 去除可能的前后空格
        if token:
            logger.debug(f"请求头中添加token: {token[:10]}...")
            headers['x-token'] = token
    
    logger.info(f"代理AIPPT请求: {method} {target_url}")
    logger.info(f"请求头: {headers}")
    if params:
        logger.info(f"参数: {params}")
    
    try:
        # 发送请求到AIPPT API
        aippt_response = make_request_to_aippt(method, target_url, headers, params, request)
        
        # 处理响应
        response_data = None
        try:
            response_data = aippt_response.json()
            logger.info(f"AIPPT响应内容: {json.dumps(response_data, ensure_ascii=False)}")
            
            # 检查token是否失效（返回码43103表示token不合法）
            if response_data.get('code') == 43103 and 'token不合法' in str(response_data.get('msg', '')):
                logger.warning("Token不合法，尝试获取新token并重试请求")
                
                # 获取新token
                new_token = fetch_new_token()
                if new_token:
                    logger.info(f"已获取新token，重试请求: {new_token[:10]}...")
                    
                    # 更新请求头中的token
                    headers['x-token'] = new_token
                    
                    # 重新生成签名（时间戳会变化）
                    timestamp = int(time.time())
                    headers['x-timestamp'] = str(timestamp)
                    signature = generate_aippt_signature(method, uri, timestamp, API_KEY, SECRET_KEY)
                    headers['x-signature'] = signature
                    
                    # 重新发送请求
                    aippt_response = make_request_to_aippt(method, target_url, headers, params, request)
                    
                    try:
                        response_data = aippt_response.json()
                        logger.info(f"使用新token重试后的响应: {json.dumps(response_data, ensure_ascii=False)}")
                    except Exception as e:
                        logger.info(f"解析重试响应失败: {str(e)}")
        except Exception as e:
            logger.info(f"AIPPT响应不是JSON格式: {str(e)}")
            logger.info(f"原始响应前500字符: {aippt_response.text[:500]}")
        
        # 构造响应对象，保留原始状态码和响应头
        response = Response(
            aippt_response.content,
            status=aippt_response.status_code
        )
        
        # 复制响应头
        for key, value in aippt_response.headers.items():
            if key.lower() not in ['content-length', 'connection', 'transfer-encoding']:
                response.headers[key] = value
        
        # 添加CORS头
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, x-api-key, x-token, x-timestamp, x-signature, x-channel, Accept'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        
        return response
    
    except requests.RequestException as e:
        # 记录网络请求异常
        logger.error(f"AIPPT网络请求失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'AIPPT网络请求失败: {str(e)}',
            'error_type': 'network_error'
        }), 502  # Bad Gateway
    except Exception as e:
        # 记录其他异常
        logger.error(f"代理AIPPT请求处理失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'代理请求处理失败: {str(e)}',
            'error_type': 'server_error'
        }), 500  # Internal Server Error

def make_request_to_aippt(method, target_url, headers, params, original_request):
    """发送请求到AIPPT API"""
    if method == 'GET':
        # 发送GET请求
        aippt_response = requests.get(
            target_url,
            headers=headers,
            params=params,
            timeout=30
        )
        logger.info(f"GET请求已发送到: {target_url}")
    elif method == 'POST':
        # 对于POST请求，需要传递表单数据或JSON
        content_type = original_request.headers.get('Content-Type', '').lower()
        logger.info(f"POST请求内容类型: {content_type}")
        
        # 创建一个新的请求头字典，确保不修改原始headers
        req_headers = headers.copy()
        
        # 处理JSON请求
        if 'application/json' in content_type:
            # JSON请求
            try:
                data = original_request.get_json(silent=True) or {}
                logger.info(f"JSON数据: {json.dumps(data, ensure_ascii=False)}")
                
                # 确保请求头包含正确的Content-Type
                req_headers['Content-Type'] = 'application/json'
                
                # 发送JSON格式的请求
                aippt_response = requests.post(
                    target_url,
                    headers=req_headers,
                    json=data,
                    timeout=30
                )
                logger.info(f"JSON POST请求已发送到: {target_url}")
            except Exception as e:
                logger.error(f"处理JSON请求时出错: {str(e)}")
                raise
        
        # 处理文件上传
        elif 'multipart/form-data' in content_type:
            # 文件上传请求
            files = {}
            form_data = {}
            
            # 处理表单数据
            for key, value in original_request.form.items():
                form_data[key] = value
                logger.info(f"表单字段: {key} = {value if len(str(value)) < 100 else f'{str(value)[:100]}...'}")
            
            # 处理文件
            for key, file in original_request.files.items():
                if file and file.filename:
                    file_content = file.read()
                    logger.info(f"文件: {key} = {file.filename} ({len(file_content)} 字节)")
                    files[key] = (file.filename, file_content, file.content_type)
                    file.close()
            
            # 不要在headers中添加Content-Type，requests会自动处理multipart边界
            # 删除Content-Type头让requests库自动处理
            if 'Content-Type' in req_headers:
                del req_headers['Content-Type']
                logger.info("从请求头中移除了Content-Type，让requests库自动处理")
            
            # 发送请求
            logger.info(f"发送multipart/form-data请求到: {target_url}")
            logger.info(f"表单字段数量: {len(form_data)}, 文件数量: {len(files)}")
            
            aippt_response = requests.post(
                target_url,
                headers=req_headers,
                data=form_data,
                files=files,
                timeout=30
            )
            logger.info(f"Multipart POST请求已发送")
        
        # 处理普通表单请求
        else:
            # 普通表单请求或未指定类型
            form_data = {}
            
            # 尝试从表单中获取数据
            if original_request.form:
                form_data = original_request.form.to_dict()
                logger.info(f"表单数据: {form_data}")
            
            # 如果没有表单数据，尝试从JSON中获取
            if not form_data:
                try:
                    json_data = original_request.get_json(silent=True)
                    if json_data:
                        form_data = json_data
                        logger.info(f"使用JSON数据作为表单数据: {form_data}")
                except Exception as e:
                    logger.warning(f"尝试解析JSON失败: {str(e)}")
            
            # 设置正确的Content-Type头
            req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            # 检查是否有文件
            has_files = False
            files = {}
            if original_request.files:
                for key, file in original_request.files.items():
                    if file and file.filename:
                        has_files = True
                        file_content = file.read()
                        logger.info(f"检测到文件: {key} = {file.filename} ({len(file_content)} 字节)")
                        files[key] = (file.filename, file_content, file.content_type)
                        file.close()
            
            # 如果有文件，使用multipart/form-data
            if has_files:
                logger.info(f"发现文件，以multipart方式处理请求")
                # 移除Content-Type，让requests自动处理
                if 'Content-Type' in req_headers:
                    del req_headers['Content-Type']
                    logger.info("从请求头中移除了Content-Type，让requests库自动处理")
                
                # 发送带文件的请求
                aippt_response = requests.post(
                    target_url,
                    headers=req_headers,
                    data=form_data,
                    files=files,
                    timeout=30
                )
                logger.info(f"带文件的POST请求已发送到: {target_url}")
            else:
                # 只有表单数据，没有文件
                logger.info(f"无文件请求，使用普通form数据")
                aippt_response = requests.post(
                    target_url,
                    headers=req_headers,
                    data=form_data,
                    timeout=30
                )
    elif method == 'PUT':
        # 处理PUT请求
        content_type = original_request.headers.get('Content-Type', '').lower()
        logger.info(f"PUT请求内容类型: {content_type}")
        
        if 'application/json' in content_type:
            data = original_request.get_json() or {}
            logger.info(f"PUT JSON数据: {json.dumps(data, ensure_ascii=False)}")
            
            # 确保请求头包含正确的Content-Type
            req_headers = headers.copy()
            req_headers['Content-Type'] = 'application/json'
            
            aippt_response = requests.put(
                target_url,
                headers=req_headers,
                json=data,
                timeout=30
            )
        else:
            # 普通表单PUT请求
            form_data = original_request.form.to_dict()
            logger.info(f"PUT表单数据: {form_data}")
            
            # 设置正确的Content-Type
            req_headers = headers.copy()
            req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            aippt_response = requests.put(
                target_url,
                headers=req_headers,
                data=form_data,
                timeout=30
            )
        logger.info(f"PUT请求已发送到: {target_url}")
    elif method == 'DELETE':
        # 处理DELETE请求
        aippt_response = requests.delete(
            target_url,
            headers=headers,
            params=params,
            timeout=30
        )
        logger.info(f"DELETE请求已发送到: {target_url}")
    else:
        # 其他HTTP方法暂不支持
        logger.warning(f"不支持的HTTP方法: {method}")
        raise ValueError(f"不支持的HTTP方法: {method}")
    
    # 记录响应状态
    logger.info(f"AIPPT响应状态码: {aippt_response.status_code}")
    
    return aippt_response

def handle_options_request():
    """处理预检请求"""
    response = Response('')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, x-api-key, x-token, x-timestamp, x-signature, x-channel, Accept'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@aippt_proxy_bp.route('/direct-task-create', methods=['GET'])
def direct_task_create():
    """完全按照官方文档示例创建任务"""
    logger.info("按官方示例直接创建任务")
    
    try:
        # 获取token
        token = get_cached_token() or fetch_new_token()
        if not token:
            logger.error("无法获取token")
            return jsonify({
                'code': -1,
                'msg': '无法获取token'
            }), 500
        
        logger.info(f"使用token: {token}")
        
        # 构造API请求 - 完全按照官方示例
        url = f"{AIPPT_API_BASE}/ai/chat/v2/task"
        
        # 设置请求头，测试不同的格式
        headers = {
            'x-api-key': API_KEY,
            'x-channel': '', # 尝试正常的键值对格式
            'x-token': token
        }
        
        # 准备表单数据
        form_data = {
            'content': '',
            'id': '',
            'title': '人工智能在教育领域的应用',
            'type': '1'
        }
        
        logger.info(f"请求URL: {url}")
        logger.info(f"请求头: {headers}")
        logger.info(f"表单数据: {form_data}")
        
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            data=form_data,
            timeout=30
        )
        
        logger.info(f"响应状态码: {response.status_code}")
        logger.info(f"响应头: {dict(response.headers)}")
        
        try:
            result = response.json()
            logger.info(f"响应内容: {json.dumps(result, ensure_ascii=False)}")
            return jsonify(result)
        except Exception as e:
            logger.error(f"解析响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析响应失败: {str(e)}',
                'raw': response.text
            })
    
    except Exception as e:
        logger.error(f"直接API测试失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'直接API测试失败: {str(e)}'
        }), 500

@aippt_proxy_bp.route('/raw-request-test', methods=['GET'])
def raw_request_test():
    """使用原始请求格式测试API调用"""
    logger.info("使用原始请求格式测试API调用")
    
    try:
        # 获取有效token
        token = get_cached_token() or fetch_new_token()
        if not token:
            logger.error("无法获取token")
            return jsonify({
                'code': -1,
                'msg': '无法获取token'
            }), 500
        
        # 准备请求
        url = f"{AIPPT_API_BASE}/ai/chat/v2/task"
        uri = '/api/ai/chat/v2/task/'
        method = 'POST'
        timestamp = int(time.time())
        
        # 生成签名
        signature = generate_aippt_signature(method, uri, timestamp, API_KEY, SECRET_KEY)
        
        # 请求头，包含完整的认证信息
        headers = {
            'x-api-key': API_KEY,
            'x-timestamp': str(timestamp),
            'x-signature': signature,
            'x-token': token,
            'x-channel': '',  # 添加空的x-channel头
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        logger.info(f"使用token: {token}")
        logger.info(f"请求URL: {url}")
        logger.info(f"请求头: {headers}")
        
        # 准备JSON数据
        json_data = {
            'content': '',
            'id': '',
            'title': '人工智能在教育领域的应用',
            'type': '1'
        }
        
        logger.info(f"JSON数据: {json_data}")
        logger.info(f"签名字符串: {method}@{uri}@{timestamp}")
        
        # 发送请求 - 使用json参数而不是data参数
        response = requests.post(
            url,
            headers=headers,
            json=json_data,  # 使用json参数发送JSON格式的数据
            timeout=30
        )
        
        logger.info(f"响应状态码: {response.status_code}")
        logger.info(f"响应头: {dict(response.headers)}")
        
        try:
            result = response.json()
            logger.info(f"响应内容: {json.dumps(result, ensure_ascii=False)}")
            return jsonify(result)
        except Exception as e:
            logger.error(f"解析响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析响应失败: {str(e)}',
                'raw': response.text
            })
    
    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'测试失败: {str(e)}'
        }), 500

@aippt_proxy_bp.route('/signature-test', methods=['GET'])
def signature_test():
    """测试签名算法"""
    logger.info("测试修改后的签名算法")
    
    try:
        # 构造API请求
        uri = '/api/grant/token/'
        params = {
            'uid': '1',
            'channel': 'ezijing'
        }
        
        # 获取时间戳
        timestamp = int(time.time())
        
        # 生成签名
        signature = generate_aippt_signature('GET', uri, timestamp, API_KEY, SECRET_KEY)
        
        # 构建请求头
        headers = {
            'x-api-key': API_KEY,
            'x-timestamp': str(timestamp),
            'x-signature': signature,
            'Accept': 'application/json'
        }
        
        # 构建目标URL
        target_url = f"{AIPPT_API_BASE}/grant/token/"
        
        logger.info(f"发送请求到: {target_url}?uid=1&channel=ezijing")
        logger.info(f"请求头: {headers}")
        
        # 发送GET请求
        response = requests.get(
            target_url,
            headers=headers,
            params=params,
            timeout=30
        )
        
        logger.info(f"API响应状态码: {response.status_code}")
        
        try:
            result = response.json()
            logger.info(f"API响应内容: {json.dumps(result, ensure_ascii=False)}")
            
            # 如果获取成功，更新token缓存
            if result['code'] == 0 and result['data'] and result['data'].get('token'):
                token_cache['token'] = result['data']['token']
                token_cache['expire_time'] = int(time.time()) + (result['data'].get('time_expire') or 30 * 24 * 3600)
                logger.info(f"已更新token缓存, 有效期至: {datetime.fromtimestamp(token_cache['expire_time']).strftime('%Y-%m-%d %H:%M:%S')}")
            
            return jsonify(result)
        except Exception as e:
            logger.error(f"解析响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析响应失败: {str(e)}',
                'raw': response.text
            })
    
    except Exception as e:
        logger.error(f"签名算法测试失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'签名算法测试失败: {str(e)}'
        }), 500

@aippt_proxy_bp.route('/exact-doc-test', methods=['GET'])
def exact_doc_test():
    """按照官方文档示例精确测试API调用流程"""
    logger.info("按照官方文档示例精确测试API调用流程")
    
    try:
        # 第一步：获取token
        logger.info("步骤1: 获取token")
        # token请求URI
        token_uri = '/api/grant/token/'
        timestamp = int(time.time())
        
        # 生成token请求签名
        signature = generate_aippt_signature('GET', token_uri, timestamp, API_KEY, SECRET_KEY)
        
        # token请求头
        headers = {
            'x-api-key': API_KEY,
            'x-timestamp': str(timestamp),
            'x-signature': signature,
            'Accept': 'application/json'
        }
        
        # token请求URL和参数
        token_url = f"{AIPPT_API_BASE}/grant/token/"
        params = {
            'uid': '1',
            'channel': ''  # 空的channel参数
        }
        
        logger.info(f"Token请求URL: {token_url}")
        logger.info(f"Token请求头: {headers}")
        logger.info(f"Token请求参数: {params}")
        
        # 发送token请求
        token_response = requests.get(
            token_url,
            headers=headers,
            params=params,
            timeout=30
        )
        
        logger.info(f"Token响应状态码: {token_response.status_code}")
        
        # 解析token响应
        try:
            token_result = token_response.json()
            logger.info(f"Token响应内容: {json.dumps(token_result, ensure_ascii=False)}")
            
            if token_result['code'] != 0 or not token_result.get('data') or not token_result['data'].get('token'):
                logger.error(f"获取token失败: {token_result['msg']}")
                return jsonify(token_result)
            
            # 获取token
            token = token_result['data']['token']
            logger.info(f"成功获取token: {token}")
            
            # 第二步：创建任务
            logger.info("步骤2: 创建任务")
            # 任务请求URI
            task_uri = '/api/ai/chat/v2/task/'
            task_timestamp = int(time.time())
            
            # 生成任务请求签名
            task_signature = generate_aippt_signature('POST', task_uri, task_timestamp, API_KEY, SECRET_KEY)
            
            # 任务请求头
            task_headers = {
                'x-api-key': API_KEY,
                'x-timestamp': str(task_timestamp),
                'x-signature': task_signature,
                'x-token': token,
                'x-channel': '',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
            
            # 任务请求URL和数据
            task_url = f"{AIPPT_API_BASE}/ai/chat/v2/task/"
            task_data = {
                'title': '人工智能在教育领域的应用',
                'type': '1',
                'content': '',
                'id': ''
            }
            
            logger.info(f"任务请求URL: {task_url}")
            logger.info(f"任务请求头: {task_headers}")
            logger.info(f"任务请求数据: {task_data}")
            
            # 发送任务请求
            task_response = requests.post(
                task_url,
                headers=task_headers,
                data=task_data,
                timeout=30
            )
            
            logger.info(f"任务响应状态码: {task_response.status_code}")
            
            # 解析任务响应
            try:
                task_result = task_response.json()
                logger.info(f"任务响应内容: {json.dumps(task_result, ensure_ascii=False)}")
                return jsonify(task_result)
            except Exception as e:
                logger.error(f"解析任务响应失败: {str(e)}")
                return jsonify({
                    'code': -1,
                    'msg': f'解析任务响应失败: {str(e)}',
                    'raw': task_response.text
                })
        except Exception as e:
            logger.error(f"解析token响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析token响应失败: {str(e)}',
                'raw': token_response.text
            })
    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'测试失败: {str(e)}'
        }), 500 

def forward_request(path, method, original_request, token=None):
    """转发请求给AIPPT API并处理响应"""
    timestamp = int(time.time())
    uri = f"/api/{path}{'' if path.endswith('/') else '/'}"
    
    logger.debug(f"签名字符串：{method}@{uri}@{timestamp}")
    signature = generate_aippt_signature(method, uri, timestamp, API_KEY, SECRET_KEY)
    
    # 目标URL
    target_url = f"{AIPPT_API_BASE}/{path}"
    logger.info(f"{method}请求URL: {target_url}")
    
    # 构建请求头
    headers = {
        'x-api-key': API_KEY,
        'x-timestamp': str(timestamp),
        'x-signature': signature,
        'Accept': 'application/json',
        'x-channel': '', # 添加空的x-channel头
    }
    
    # 如果有token，添加到请求头
    if token:
        headers['x-token'] = token
        logger.debug(f"使用token: {token[:10]}...")
    
    # 添加原始请求的部分头字段（排除某些敏感或已处理的头）
    excluded_headers = [
        'host', 'content-length', 'connection', 'x-forwarded-for',
        'x-real-ip', 'x-api-key', 'x-signature', 'x-timestamp', 'x-token', 'x-channel'
    ]
    
    # 添加原始请求的其他头字段
    for header, value in original_request.headers.items():
        if header.lower() not in excluded_headers:
            headers[header] = value
    
    # 特殊处理一些特定路径
    special_paths = [
        'design/v2/save', 
        'generate/work',
        'ai/chat/v2/outline/save'
    ]
    
    # 如果是特殊处理的路径，直接使用特殊处理函数
    for special_path in special_paths:
        if path.endswith(special_path):
            logger.info(f"特殊处理路径: {path}")
            if 'design/v2/save' in path:
                return handle_design_save(original_request, token, headers, target_url)
            elif 'generate/work' in path:
                return handle_generate_work(original_request, token, headers, target_url)
            elif 'ai/chat/v2/outline/save' in path:
                return handle_outline_save(original_request, token, headers, target_url)
    
    # 获取URL参数
    params = {}
    if method in ['GET', 'DELETE']:
        params = original_request.args.to_dict()
    
    # 根据不同的HTTP方法处理请求
    aippt_response = None
    
    if method == 'GET':
        # 处理GET请求
        aippt_response = requests.get(
            target_url,
            headers=headers,
            params=params,
            timeout=30
        )
        logger.info(f"GET请求已发送到: {target_url}，参数: {params}")
    elif method == 'POST':
        # 处理POST请求
        content_type = original_request.headers.get('Content-Type', '').lower()
        logger.info(f"POST请求内容类型: {content_type}")
        
        # 处理JSON格式请求
        if 'application/json' in content_type:
            data = original_request.get_json(silent=True) or {}
            logger.info(f"JSON数据: {json.dumps(data, ensure_ascii=False)}")
            
            # 确保请求头包含正确的Content-Type
            req_headers = headers.copy()
            req_headers['Content-Type'] = 'application/json'
            
            aippt_response = requests.post(
                target_url,
                headers=req_headers,
                json=data,
                timeout=30
            )
            logger.info(f"JSON POST请求已发送到: {target_url}")
        
        # 处理multipart/form-data请求
        elif 'multipart/form-data' in content_type:
            logger.info(f"处理multipart/form-data请求")
            form_data = {}
            files = {}
            
            # 处理表单字段
            if original_request.form:
                form_data = original_request.form.to_dict()
                logger.info(f"表单字段: {form_data}")
            
            # 处理文件
            if original_request.files:
                for key, file in original_request.files.items():
                    if file.filename:
                        logger.info(f"处理文件: {key} = {file.filename}")
                        file_content = file.read()
                        files[key] = (file.filename, file_content, file.content_type)
                        file.close()
            
            # 移除可能导致冲突的Content-Type头
            req_headers = headers.copy()
            if 'Content-Type' in req_headers:
                del req_headers['Content-Type']
                logger.info("从请求头中移除了Content-Type，让requests库自动处理")
            
            # 发送请求
            logger.info(f"发送multipart/form-data请求到: {target_url}")
            logger.info(f"表单字段数量: {len(form_data)}, 文件数量: {len(files)}")
            
            aippt_response = requests.post(
                target_url,
                headers=req_headers,
                data=form_data,
                files=files,
                timeout=30
            )
            logger.info(f"Multipart POST请求已发送")
        
        # 处理application/x-www-form-urlencoded请求
        elif 'application/x-www-form-urlencoded' in content_type:
            logger.info(f"处理application/x-www-form-urlencoded请求")
            form_data = original_request.form.to_dict()
            logger.info(f"表单数据: {form_data}")
            
            # 设置正确的Content-Type
            req_headers = headers.copy()
            req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            # 发送请求
            aippt_response = requests.post(
                target_url,
                headers=req_headers,
                data=form_data,
                timeout=30
            )
            logger.info(f"application/x-www-form-urlencoded POST请求已发送到: {target_url}")

# 特殊处理函数: 设计保存
def handle_design_save(request, token, headers, target_url):
    """特殊处理设计保存请求"""
    logger.info("特殊处理设计保存请求")
    logger.info(f"入参token: {token[:10] if token else 'None'}...")
    logger.info(f"入参headers: {headers}")
    
    # 获取请求数据
    form_data = {}
    if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
        form_data = request.form.to_dict()
        logger.info(f"表单数据(urlencoded): {form_data}")
    elif request.content_type and 'application/json' in request.content_type:
        form_data = request.get_json(silent=True) or {}
        logger.info(f"JSON数据: {json.dumps(form_data, ensure_ascii=False)}")
    else:
        # 尝试获取form数据
        form_data = request.form.to_dict()
        logger.info(f"表单数据(default): {form_data}")
    
    # 设置必要的请求头
    req_headers = headers.copy()
    req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    # 检查是否有token，如果没有尝试获取
    if 'x-token' not in req_headers or not req_headers['x-token']:
        logger.warning("请求头中缺少token，尝试获取新token")
        new_token = get_cached_token() or fetch_new_token()
        if new_token:
            req_headers['x-token'] = new_token
            logger.info(f"已添加新token: {new_token[:10]}...")
            
            # 更新签名（时间戳会变化）
            timestamp = int(time.time())
            req_headers['x-timestamp'] = str(timestamp)
            uri = '/api/design/v2/save/'
            signature = generate_aippt_signature('POST', uri, timestamp, API_KEY, SECRET_KEY)
            req_headers['x-signature'] = signature
    
    # 检查必要的参数
    if not form_data.get('task_id'):
        return jsonify({
            'code': 40001,
            'msg': '缺少必要参数task_id',
            'data': None
        }), 400
    
    if not form_data.get('template_id'):
        return jsonify({
            'code': 40001,
            'msg': '缺少必要参数template_id',
            'data': None
        }), 400
    
    # 日志记录完整请求
    logger.info(f"设计保存请求: {target_url}")
    logger.info(f"请求头: {req_headers}")
    logger.info(f"表单数据: {form_data}")
    
    # 发送请求
    try:
        response = requests.post(
            target_url,
            headers=req_headers,
            data=form_data,
            timeout=30
        )
        
        logger.info(f"设计保存响应: 状态码={response.status_code}")
        
        # 处理响应
        try:
            result = response.json()
            logger.info(f"响应数据: {json.dumps(result, ensure_ascii=False)}")
            
            # 检查token是否失效（返回码43103表示token不合法）
            if result.get('code') == 43103 and 'token不合法' in str(result.get('msg', '')):
                logger.warning("Token不合法，尝试获取新token并重试请求")
                
                # 获取新token
                new_token = fetch_new_token()
                if new_token:
                    logger.info(f"已获取新token，重试设计保存请求: {new_token[:10]}...")
                    
                    # 更新请求头中的token
                    req_headers['x-token'] = new_token
                    
                    # 重新生成签名（时间戳会变化）
                    timestamp = int(time.time())
                    req_headers['x-timestamp'] = str(timestamp)
                    uri = '/api/design/v2/save/'
                    signature = generate_aippt_signature('POST', uri, timestamp, API_KEY, SECRET_KEY)
                    req_headers['x-signature'] = signature
                    
                    # 重新发送请求
                    logger.info(f"使用新token重试设计保存请求: {target_url}")
                    logger.info(f"重试请求头: {req_headers}")
                    retry_response = requests.post(
                        target_url,
                        headers=req_headers,
                        data=form_data,
                        timeout=30
                    )
                    
                    try:
                        retry_result = retry_response.json()
                        logger.info(f"使用新token重试后的响应状态码: {retry_response.status_code}")
                        logger.info(f"使用新token重试后的响应: {json.dumps(retry_result, ensure_ascii=False)}")
                        return jsonify(retry_result)
                    except Exception as e:
                        logger.error(f"解析重试响应失败: {str(e)}")
                        return jsonify({
                            'code': -1,
                            'msg': f'解析重试响应失败: {str(e)}',
                            'raw': retry_response.text
                        })
                else:
                    logger.error("获取新token失败，无法重试请求")
            
            return jsonify(result)
        except Exception as e:
            logger.error(f"解析JSON响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析响应失败: {str(e)}',
                'raw': response.text
            })
    except Exception as e:
        logger.error(f"设计保存请求失败: {str(e)}")
        return jsonify({
            'code': -1,
            'msg': f'请求失败: {str(e)}'
        }), 500

# 特殊处理函数: 生成作品
def handle_generate_work(request, token, headers, target_url):
    """特殊处理生成作品请求"""
    logger.info("特殊处理生成作品请求")
    
    # 获取请求数据
    form_data = {}
    if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
        form_data = request.form.to_dict()
        logger.info(f"表单数据(urlencoded): {form_data}")
    elif request.content_type and 'application/json' in request.content_type:
        form_data = request.get_json(silent=True) or {}
        logger.info(f"JSON数据: {json.dumps(form_data, ensure_ascii=False)}")
    else:
        # 尝试获取form数据
        form_data = request.form.to_dict()
        logger.info(f"表单数据(default): {form_data}")
    
    # 设置必要的请求头
    req_headers = headers.copy()
    req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    # 检查必要的参数
    if not form_data.get('task_id'):
        return jsonify({
            'code': 40001,
            'msg': '缺少必要参数task_id',
            'data': None
        }), 400
    
    if not form_data.get('template_id'):
        return jsonify({
            'code': 40001,
            'msg': '缺少必要参数template_id',
            'data': None
        }), 400
    
    # 日志记录完整请求
    logger.info(f"生成作品请求: {target_url}")
    logger.info(f"请求头: {req_headers}")
    logger.info(f"表单数据: {form_data}")
    
    # 发送请求
    try:
        response = requests.post(
            target_url,
            headers=req_headers,
            data=form_data,
            timeout=30
        )
        
        logger.info(f"生成作品响应: 状态码={response.status_code}")
        
        # 处理响应
        try:
            result = response.json()
            logger.info(f"响应数据: {json.dumps(result, ensure_ascii=False)}")
            return jsonify(result)
        except Exception as e:
            logger.error(f"解析JSON响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析响应失败: {str(e)}',
                'raw': response.text
            })
    except Exception as e:
        logger.error(f"生成作品请求失败: {str(e)}")
        return jsonify({
            'code': -1,
            'msg': f'请求失败: {str(e)}'
        }), 500

# 特殊处理函数: 保存大纲
def handle_outline_save(request, token, headers, target_url):
    """特殊处理保存大纲请求"""
    logger.info("特殊处理保存大纲请求")
    
    # 获取请求数据
    form_data = {}
    if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
        form_data = request.form.to_dict()
        logger.info(f"表单数据(urlencoded): {form_data}")
    elif request.content_type and 'application/json' in request.content_type:
        form_data = request.get_json(silent=True) or {}
        logger.info(f"JSON数据: {json.dumps(form_data, ensure_ascii=False)}")
    else:
        # 尝试获取form数据
        form_data = request.form.to_dict()
        logger.info(f"表单数据(default): {form_data}")
    
    # 设置必要的请求头
    req_headers = headers.copy()
    req_headers['Content-Type'] = 'application/json'
    
    # 检查必要的参数
    if not form_data.get('task_id'):
        return jsonify({
            'code': 40001,
            'msg': '缺少必要参数task_id',
            'data': None
        }), 400
    
    if not form_data.get('content'):
        return jsonify({
            'code': 40001,
            'msg': '缺少必要参数content',
            'data': None
        }), 400
    
    # 日志记录完整请求
    logger.info(f"保存大纲请求: {target_url}")
    logger.info(f"请求头: {req_headers}")
    logger.info(f"表单数据: {form_data}")
    
    # 发送请求
    try:
        response = requests.post(
            target_url,
            headers=req_headers,
            json=form_data,  # 这里使用json参数而不是data
            timeout=30
        )
        
        logger.info(f"保存大纲响应: 状态码={response.status_code}")
        
        # 处理响应
        try:
            result = response.json()
            logger.info(f"响应数据: {json.dumps(result, ensure_ascii=False)}")
            return jsonify(result)
        except Exception as e:
            logger.error(f"解析JSON响应失败: {str(e)}")
            return jsonify({
                'code': -1,
                'msg': f'解析响应失败: {str(e)}',
                'raw': response.text
            })
    except Exception as e:
        logger.error(f"保存大纲请求失败: {str(e)}")
        return jsonify({
            'code': -1,
            'msg': f'请求失败: {str(e)}'
        }), 500 

@aippt_proxy_bp.route('/grant/code', methods=['GET'])
def get_aippt_code():
    """获取AIPPT授权码，用于前端集成AIPPT UI
    
    参数:
    - uid: 用户ID
    - channel: 渠道标识
    
    返回:
    - code: 授权码
    - time_expire: 过期时间（秒）
    """
    logger.info("接收到获取AIPPT授权码请求")
    
    # 获取请求参数
    uid = request.args.get('uid', '1')  # 默认为1
    channel = request.args.get('channel', 'ezijing')  # 默认为ezijing
    
    logger.info(f"请求参数: uid={uid}, channel={channel}")
    
    # 构造API请求
    uri = '/api/grant/code/'
    timestamp = int(time.time())
    signature = generate_aippt_signature('GET', uri, timestamp, API_KEY, SECRET_KEY)
    
    headers = {
        'x-api-key': API_KEY,
        'x-timestamp': str(timestamp),
        'x-signature': signature,
        'Accept': 'application/json'
    }
    
    # 构建目标URL
    target_url = f"{AIPPT_API_BASE}/grant/code/"
    
    # 构建URL参数
    params = {
        'uid': uid,
        'channel': channel
    }
    
    logger.info(f"发送请求到: {target_url}?uid={uid}&channel={channel}")
    logger.info(f"请求头: {headers}")
    
    try:
        # 发送GET请求
        response = requests.get(
            target_url,
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"获取授权码失败，状态码: {response.status_code}")
            return jsonify({
                'code': -1,
                'msg': f'获取授权码失败，状态码: {response.status_code}',
                'data': None
            }), 500
        
        data = response.json()
        logger.info(f"授权码响应: {json.dumps(data, ensure_ascii=False)}")
        
        if data['code'] == 0 and data.get('data') and data['data'].get('code'):
            logger.info(f"成功获取授权码: {data['data']['code'][:10]}...")
            return jsonify(data)
        else:
            logger.error(f"获取授权码响应错误: {data.get('msg', '未知错误')}")
            return jsonify(data)
    
    except Exception as e:
        logger.error(f"获取授权码异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': -1,
            'msg': f'获取授权码异常: {str(e)}',
            'data': None
        }), 500