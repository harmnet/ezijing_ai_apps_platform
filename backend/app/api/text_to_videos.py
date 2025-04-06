#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文生视频API路由
"""

from flask import Blueprint, request, jsonify, current_app, Response
from app.services.interface_text_to_videos import create_video_task as old_create_video_task, query_video_task as old_query_video_task, get_supported_ratios, get_supported_resolutions
# 导入新的SDK版本的功能
from app.services.volcano_sdk_videos import create_video_task as sdk_create_video_task, query_video_task as sdk_query_video_task
import traceback
import json
import base64
import requests
import re
import urllib.parse

text_to_videos = Blueprint('text_to_videos', __name__)

# 是否启用新版SDK接口
USE_SDK_API = True

@text_to_videos.route('/text-to-videos/create', methods=['POST'])
def create_video_api():
    """创建视频生成任务的API端点"""
    try:
        # 获取并验证请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "缺少请求数据",
                "code": 400
            }), 400

        # 提取参数
        prompt = data.get('prompt')
        # 如果是图生视频模式且没有提示词，使用默认提示词
        if not prompt and not data.get('image'):
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: prompt或image",
                "code": 400
            }), 400
            
        # 提取其他参数
        ratio = data.get('ratio', '16:9')
        duration = float(data.get('duration', 3))
        fps = int(data.get('fps', 30))
        
        # 处理分辨率参数，确保是字符串格式并带有'p'后缀
        resolution = data.get('resolution', '720p')
        if isinstance(resolution, int) or (isinstance(resolution, str) and resolution.isdigit()):
            resolution = f"{resolution}p"
        
        watermark = data.get('watermark', False)
        
        # 处理上传的图片
        image = None
        if 'image' in data and data['image']:
            # 图片已经是Base64格式，直接使用
            image = data['image']
            if not image.startswith('data:image'):
                # 如果不是完整的Data URL格式，添加前缀
                image = f"data:image/jpeg;base64,{image}"
        
        # 记录请求日志
        current_app.logger.info(f"创建视频任务请求: 提示词长度={len(prompt) if prompt else 0}, 是否有图片={image is not None}")
        
        # 根据配置选择API实现
        if USE_SDK_API:
            # 使用新的SDK接口
            current_app.logger.info("使用火山引擎SDK接口创建视频任务")
            result = sdk_create_video_task(
                prompt=prompt,
                ratio=ratio,
                duration=duration,
                fps=fps,
                resolution=resolution,
                watermark=watermark,
                image=image
            )
        else:
            # 使用原有接口
            current_app.logger.info("使用原有接口创建视频任务")
            result = old_create_video_task(
                prompt=prompt,
                ratio=ratio,
                duration=duration,
                fps=fps,
                resolution=resolution,
                watermark=watermark,
                image=image
            )
        
        # 检查响应是否包含错误
        if result.get('status') == 'error':
            return jsonify(result), 400
            
        # 返回成功结果
        return jsonify(result)

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"创建视频任务API错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@text_to_videos.route('/text-to-videos/query', methods=['GET'])
def query_video_api():
    """查询视频生成任务状态的API端点"""
    try:
        # 获取任务ID
        task_id = request.args.get('task_id')
        if not task_id:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: task_id",
                "code": 400
            }), 400
            
        # 根据配置选择API实现
        if USE_SDK_API and not task_id.startswith('mock-video-task-'):
            # 如果是SDK接口创建的任务，使用SDK接口查询
            current_app.logger.info(f"使用火山引擎SDK接口查询任务: {task_id}")
            result = sdk_query_video_task(task_id)
        else:
            # 使用原有接口
            current_app.logger.info(f"使用原有接口查询任务: {task_id}")
            result = old_query_video_task(task_id)
        
        # 检查响应是否包含错误
        if result.get('status') == 'error':
            return jsonify(result), 400
            
        # 返回查询结果
        return jsonify(result)

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"查询视频任务API错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@text_to_videos.route('/text-to-videos/proxy-video')
def proxy_video():
    """代理视频请求，解决CORS问题"""
    try:
        # 获取视频URL
        video_url = request.args.get('url')
        if not video_url:
            current_app.logger.error("代理视频请求缺少URL参数")
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: url",
                "code": 400
            }), 400
            
        # 记录原始请求URL
        current_app.logger.info(f"收到视频代理请求，原始URL: {video_url}")
        
        # 递归处理多层嵌套URL
        max_depth = 10  # 最大递归深度
        depth = 0
        original_url = video_url  # 保存原始URL用于日志记录
        
        def decode_nested_url(url, current_depth):
            if current_depth >= max_depth:
                current_app.logger.error(f"URL嵌套过深，已达最大递归深度{max_depth}，原始URL: {original_url}")
                return url
                
            current_app.logger.info(f"解析URL (第{current_depth+1}层): {url[:100]}...")
            
            # 检测是否为代理URL（多种可能的格式）
            proxy_patterns = [
                # 基本形式
                r'/api/v1/text-to-videos/proxy-video\?url=(.+)',
                # 不带前导斜杠的形式
                r'api/v1/text-to-videos/proxy-video\?url=(.+)',
                # 完整域名形式（可能多次编码）
                r'https?.*?/api/v1/text-to-videos/proxy-video\?url=(.+)'
            ]
            
            is_nested = False
            for pattern in proxy_patterns:
                match = re.search(pattern, url)
                if match:
                    is_nested = True
                    nested_url = match.group(1)
                    current_app.logger.info(f"发现嵌套URL (第{current_depth+1}层), 模式: {pattern}")
                    
                    # 解码URL
                    try:
                        decoded_url = urllib.parse.unquote(nested_url)
                        # 如果解码前后一致，可能需要更多次解码（对于多次编码的URL）
                        decode_count = 1
                        while decoded_url != nested_url and decode_count < 5:  # 最多解码5次
                            nested_url = decoded_url
                            decoded_url = urllib.parse.unquote(nested_url)
                            decode_count += 1
                            
                        current_app.logger.info(f"解码URL (解码{decode_count}次): {decoded_url[:100]}...")
                        
                        # 递归处理可能仍嵌套的URL
                        return decode_nested_url(decoded_url, current_depth + 1)
                    except Exception as e:
                        current_app.logger.error(f"URL解码失败: {str(e)}")
                        return url
            
            # 如果没有匹配任何嵌套模式，返回当前URL
            if not is_nested:
                current_app.logger.info(f"未检测到更多嵌套，最终URL: {url[:100]}...")
                return url
        
        # 开始递归解析URL
        video_url = decode_nested_url(video_url, depth)
        current_app.logger.info(f"解析后的最终URL: {video_url[:100]}...")
        
        # 移除可能的@前缀
        if video_url.startswith('@'):
            video_url = video_url[1:]
            current_app.logger.info(f"移除@前缀后的URL: {video_url}")
            
        # 确保URL有正确的scheme
        if not video_url.startswith('http://') and not video_url.startswith('https://'):
            current_app.logger.warning(f"URL缺少协议前缀: {video_url}")
            if video_url.startswith('//'):
                video_url = 'https:' + video_url
                current_app.logger.info(f"添加https:前缀: {video_url}")
            else:
                video_url = 'https://' + video_url.lstrip('/')
                current_app.logger.info(f"添加https://前缀: {video_url}")
                
        current_app.logger.info(f"处理后的视频URL: {video_url}")
            
        # 安全检查，确保只代理允许的域名
        allowed_domains = [
            'ark-content-generation-cn-beijing.tos-cn-beijing.volces.com',
            'tos-cn-beijing.volces.com'
        ]
        
        # 更健壮的域名检查
        try:
            parsed_url = urllib.parse.urlparse(video_url)
            hostname = parsed_url.netloc
            
            # 检查URL是否属于允许的域名
            is_allowed = False
            for domain in allowed_domains:
                if domain in hostname:
                    is_allowed = True
                    break
                    
            current_app.logger.info(f"域名检查: {hostname}, 是否允许: {is_allowed}")
        except Exception as e:
            current_app.logger.error(f"URL解析错误: {str(e)}")
            is_allowed = False
                
        if not is_allowed:
            current_app.logger.warning(f"尝试代理非法域名URL: {hostname}")
            return jsonify({
                "status": "error",
                "message": "安全限制：只能代理火山引擎视频URL",
                "code": 403
            }), 403
            
        # 请求视频内容
        try:
            current_app.logger.info(f"开始请求视频内容: {video_url}")
            response = requests.get(
                video_url,
                stream=True,
                timeout=300,  # 5分钟超时
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Range': 'bytes=0-'  # 支持断点续传
                }
            )
            
            current_app.logger.info(f"视频请求状态码: {response.status_code}")
            current_app.logger.info(f"视频响应头: {dict(response.headers)}")
            
            if not response.ok:
                current_app.logger.error(f"代理视频请求失败，状态码: {response.status_code}, 响应: {response.text[:200]}")
                return jsonify({
                    "status": "error",
                    "message": f"获取视频失败，状态码: {response.status_code}",
                    "code": response.status_code
                }), response.status_code
                
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"请求视频时发生网络错误: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"网络错误: {str(e)}",
                "code": 500
            }), 500
            
        # 准备响应头
        headers = {
            'Content-Type': response.headers.get('Content-Type', 'video/mp4'),
            'Content-Length': response.headers.get('Content-Length', ''),
            'Accept-Ranges': 'bytes',
            'Access-Control-Allow-Origin': '*',  # 允许任何源访问
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Range',
            'Cache-Control': 'public, max-age=86400'  # 缓存1天
        }
        
        if 'Content-Range' in response.headers:
            headers['Content-Range'] = response.headers['Content-Range']
            
        current_app.logger.info(f"代理视频成功，返回响应头: {headers}")
        
        # 返回视频流
        return Response(
            response.iter_content(chunk_size=1024*8),
            status=response.status_code,
            headers=headers
        )

    except Exception as e:
        # 记录详细错误日志
        current_app.logger.error(f"代理视频请求错误: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@text_to_videos.route('/text-to-videos/ratios', methods=['GET'])
def get_ratios_api():
    """获取支持的视频比例列表的API端点"""
    try:
        ratios = get_supported_ratios()
        return jsonify({
            "status": "success",
            "data": {
                "ratios": ratios
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取视频比例列表错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500


@text_to_videos.route('/text-to-videos/resolutions', methods=['GET'])
def get_resolutions_api():
    """获取支持的视频分辨率列表的API端点"""
    try:
        resolutions = get_supported_resolutions()
        return jsonify({
            "status": "success",
            "data": {
                "resolutions": resolutions
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取视频分辨率列表错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"服务器内部错误: {str(e)}",
            "code": 500
        }), 500 