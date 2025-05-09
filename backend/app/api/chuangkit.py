from flask import Blueprint, request, jsonify
import requests
import hashlib
import time
import logging

# 创建蓝图
chuangkit_bp = Blueprint('chuangkit', __name__)

# 设置常量
APP_ID = '54d9adec77d0402794018d166110f3dd'
APP_SECRET = '08097010E0EF4B85EE2B8CE438328249'
API_BASE_URL = 'https://gw.chuangkit.com/openplatform'

# 设置日志
logger = logging.getLogger(__name__)

@chuangkit_bp.route('/token', methods=['GET'])
def get_token():
    """
    获取创客贴API Token
    """
    try:
        # 获取当前时间戳
        timestamp = int(time.time() * 1000)
        
        # 生成签名
        # 签名字符串格式: appId&${APP_ID}timestamp&${TIMESTAMP}#${APP_SECRET}
        sign_str = f"appId&{APP_ID}timestamp&{timestamp}#{APP_SECRET}"
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
        
        logger.info(f"获取Token请求参数: api_id={APP_ID}, timestamp={timestamp}, sign={sign}")
        
        # 请求创客贴API
        response = requests.get(
            f"{API_BASE_URL}/openApi/getApiToken.do",
            params={
                'api_id': APP_ID,
                'timestamp': timestamp,
                'sign': sign
            }
        )
        
        # 记录响应
        logger.info(f"创客贴Token响应: {response.status_code} - {response.text}")
        
        # 检查响应
        if response.status_code == 200:
            response_data = response.json()
            if response_data['body']['code'] == 200:
                return jsonify({
                    'status': 'success',
                    'data': response_data['body']['data']
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': response_data['body']['msg']
                }), 400
        else:
            return jsonify({
                'status': 'error',
                'message': f"API请求失败，状态码: {response.status_code}"
            }), response.status_code
            
    except Exception as e:
        logger.error(f"获取Token异常: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"服务器错误: {str(e)}"
        }), 500

@chuangkit_bp.route('/tags', methods=['POST'])
def get_tags():
    """
    获取场景标签信息
    """
    try:
        data = request.json
        
        if not data or not data.get('token') or not data.get('kind_id'):
            return jsonify({
                'status': 'error',
                'message': "请求参数不完整，需要token和kind_id"
            }), 400
        
        # 记录请求
        logger.info(f"获取标签请求: {data}")
        
        # 请求创客贴API
        response = requests.post(
            f"{API_BASE_URL}/api/aidesign/getRepoTagInfo.do",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # 记录响应
        logger.info(f"创客贴标签响应: {response.status_code} - {response.text}")
        
        # 检查响应
        if response.status_code == 200:
            response_data = response.json()
            if response_data['body']['code'] == 200:
                return jsonify({
                    'status': 'success',
                    'data': response_data['body']['data']
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': response_data['body']['msg']
                }), 400
        else:
            return jsonify({
                'status': 'error',
                'message': f"API请求失败，状态码: {response.status_code}"
            }), response.status_code
            
    except Exception as e:
        logger.error(f"获取标签异常: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"服务器错误: {str(e)}"
        }), 500

@chuangkit_bp.route('/generate', methods=['POST'])
def generate_design():
    """
    提交AI设计生成任务
    """
    try:
        data = request.json
        
        if not data or not data.get('token') or not data.get('prompt') or not data.get('kind_id'):
            return jsonify({
                'status': 'error',
                'message': "请求参数不完整，需要token、prompt和kind_id"
            }), 400
        
        # 记录请求
        logger.info(f"生成设计请求: {data}")
        
        # 请求创客贴API
        response = requests.post(
            f"{API_BASE_URL}/api/aidesign/addChatReplaceMarkTask.do",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # 记录响应
        logger.info(f"创客贴生成设计响应: {response.status_code} - {response.text}")
        
        # 检查响应
        if response.status_code == 200:
            response_data = response.json()
            if response_data['body']['code'] == 200:
                return jsonify({
                    'status': 'success',
                    'data': response_data['body']['data']
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': response_data['body']['msg']
                }), 400
        else:
            return jsonify({
                'status': 'error',
                'message': f"API请求失败，状态码: {response.status_code}"
            }), response.status_code
            
    except Exception as e:
        logger.error(f"生成设计异常: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"服务器错误: {str(e)}"
        }), 500

@chuangkit_bp.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    获取任务状态（这个API需要根据创客贴实际提供的接口进行修改）
    暂时提供一个模拟的实现
    """
    try:
        # 获取token参数
        token = request.args.get('token')
        if not token:
            return jsonify({
                'status': 'error',
                'message': "缺少token参数"
            }), 400
            
        # 这里应该调用创客贴提供的任务状态查询API
        # 由于文档中没有提供，这里返回一个模拟的响应
        # 实际实现应该根据创客贴的API进行调整
        
        # 模拟任务处理中或完成的响应
        import random
        status = random.choice(['processing', 'completed'])
        
        if status == 'completed':
            return jsonify({
                'status': 'success',
                'data': {
                    'task_id': task_id,
                    'status': 'completed',
                    'imageUrl': f"https://picsum.photos/seed/{task_id}/400/600",
                    'width': 1242,
                    'height': 1660,
                    'md5': hashlib.md5(task_id.encode('utf-8')).hexdigest().upper()
                }
            })
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'task_id': task_id,
                    'status': 'processing'
                }
            })
            
    except Exception as e:
        logger.error(f"获取任务状态异常: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"服务器错误: {str(e)}"
        }), 500 