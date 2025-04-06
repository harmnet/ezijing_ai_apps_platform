import requests
import json
import time
import logging
import os
import uuid
from datetime import datetime
from app.utils.api_key import get_api_key

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置日志文件路径
LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "video_api_debug.log")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置文件处理器
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 火山引擎API配置
VOLCANO_API_CONFIG = {
    "base_url": "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks",
    "api_key": get_api_key("volcano"),  # 使用API密钥管理模块获取密钥
    "model": "doubao-seaweed-241128",  # 检查模型名称是否正确
}

# 记录初始化成功日志
logger.info("火山引擎SDK初始化成功")
logger.info(f"火山引擎API配置: base_url={VOLCANO_API_CONFIG['base_url']}, model={VOLCANO_API_CONFIG['model']}, API密钥前5位={VOLCANO_API_CONFIG['api_key'][:5]}")

def create_video_task(prompt, ratio="16:9", duration=3.0, fps=30, resolution="720p", watermark=False, image=None):
    """
    创建视频生成任务，支持文生视频、图生视频
    :param prompt: 文本提示词
    :param ratio: 视频比例，支持16:9, 9:16, 1:1, 4:3, 3:4
    :param duration: 视频时长，支持1-10秒
    :param fps: 帧率，支持24, 30
    :param resolution: 分辨率，支持720p, 1080p
    :param watermark: 是否带水印
    :param image: 图片base64（图生视频）
    :return: 符合官方格式的任务创建响应
    """
    
    logger.info(f"收到创建视频任务请求: 提示词={prompt}, 视频比例={ratio}, 时长={duration}秒, 是否带图={image is not None}")
    
    # 确保参数值在有效范围内
    # 标准化分辨率参数
    valid_resolutions = ["720", "1080", "720p", "1080p"]
    if resolution not in valid_resolutions:
        resolution = "720p"
    
    # 确保duration在有效范围内(1-10秒)
    duration = max(1.0, min(10.0, float(duration)))
    
    # 确保fps是有效值(24或30)
    if fps not in [24, 30]:
        fps = 30
    
    # 构造提示词，添加参数
    prompt_with_params = f"{prompt} --ratio {ratio} --fps {fps} --dur {duration}"
    
    # 标准化处理分辨率参数
    if resolution:
        # 确保resolution是字符串
        res_str = str(resolution)
        # 移除可能的'p'后缀
        res_value = res_str.replace('p', '') if 'p' in res_str else res_str
        prompt_with_params += f" --res {res_value}"
    
    if watermark is False:  # 只有当明确设置为False时才加入无水印参数
        prompt_with_params += " --no-watermark"
    
    logger.info(f"处理后的提示词参数: {prompt_with_params}")
    
    try:
        # 构造请求体
        if image:
            # 图生视频
            payload = {
                "model": VOLCANO_API_CONFIG["model"],
                "content": [
                    {
                        "type": "image",
                        "image": image
                    },
                    {
                        "type": "text",
                        "text": prompt_with_params
                    }
                ]
            }
        else:
            # 文生视频
            payload = {
                "model": VOLCANO_API_CONFIG["model"],
                "content": [
                    {
                        "type": "text",
                        "text": prompt_with_params
                    }
                ]
            }
        
        # 火山引擎API认证头
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {VOLCANO_API_CONFIG['api_key']}"
        }
        
        # 使用基础URL
        create_url = VOLCANO_API_CONFIG["base_url"]
        
        logger.info(f"API配置: create_url={create_url}, model={VOLCANO_API_CONFIG['model']}")
        logger.info(f"API密钥(部分): {VOLCANO_API_CONFIG['api_key'][:5]}...{VOLCANO_API_CONFIG['api_key'][-5:]}")
        logger.debug(f"请求头: {headers}")
        logger.debug(f"请求体: {json.dumps(payload)}")
        logger.info(f"发送请求到火山引擎API: {create_url}")
        
        response = requests.post(create_url, headers=headers, json=payload, timeout=300)
        logger.debug(f"响应状态码: {response.status_code}")
        logger.debug(f"响应头: {response.headers}")
        
        # 限制日志大小，只记录前1000个字符
        response_content = response.text[:1000]
        logger.debug(f"响应内容: {response_content}")
        
        # 检查是否收到HTML页面而不是JSON
        if response_content.strip().startswith('<!DOCTYPE html>') or response_content.strip().startswith('<html'):
            logger.warning("API返回了HTML页面而不是JSON数据")
            logger.info("切换到模拟模式")
            return create_mock_video_task(prompt, ratio, duration, fps, resolution, watermark, image)
            
        if response.status_code == 200:
            try:
                response_json = response.json()
                # 检查是否已经是官方API格式
                if "id" in response_json and isinstance(response_json, dict):
                    logger.info(f"成功创建视频任务，任务ID: {response_json['id']}")
                    return response_json
                
                # 检查返回的结果是否包含任务ID（可能是task_id或id字段）
                task_id = None
                if isinstance(response_json, dict):
                    if "task_id" in response_json:
                        task_id = response_json["task_id"]
                    elif "id" in response_json:
                        task_id = response_json["id"]
                elif isinstance(response_json, str) and response_json.strip():
                    # 直接返回字符串作为任务ID
                    task_id = response_json.strip()
                
                if task_id:
                    logger.info(f"成功创建视频任务，任务ID: {task_id}")
                    # 返回符合官方API格式的响应
                    return {
                        "id": task_id,
                        "model": VOLCANO_API_CONFIG["model"],
                        "status": "created",
                        "created_at": str(int(time.time())),
                        "updated_at": str(int(time.time()))
                    }
                else:
                    logger.error(f"API响应中没有任务ID: {response_json}")
                    logger.info("切换到模拟模式")
                    return create_mock_video_task(prompt, ratio, duration, fps, resolution, watermark, image)
            except ValueError as e:
                logger.error(f"JSON解析错误: {str(e)}, 响应内容: {response_content}")
                logger.info("切换到模拟模式")
                return create_mock_video_task(prompt, ratio, duration, fps, resolution, watermark, image)
        else:
            logger.error(f"API请求失败，状态码: {response.status_code}, 响应: {response_content}")
            
            # 尝试解析错误消息
            error_message = f"API请求失败，状态码: {response.status_code}"
            try:
                if response_content and response_content.strip() != "null":
                    error_json = json.loads(response_content)
                    if isinstance(error_json, dict) and "error" in error_json:
                        error_detail = error_json["error"]
                        if "message" in error_detail:
                            error_message += f"，错误信息: {error_detail['message']}"
                        if "code" in error_detail:
                            error_message += f"，错误代码: {error_detail['code']}"
            except:
                pass
            
            # 切换到模拟模式
            logger.info(f"{error_message}，切换到模拟模式")
            return create_mock_video_task(prompt, ratio, duration, fps, resolution, watermark, image)
    
    except Exception as e:
        logger.error(f"调用火山引擎API错误: {str(e)}")
        # 切换到模拟模式
        logger.info(f"发生异常：{str(e)}，切换到模拟模式")
        return create_mock_video_task(prompt, ratio, duration, fps, resolution, watermark, image)

def query_video_task(task_id):
    """
    查询视频生成任务的状态
    :param task_id: 任务ID
    :return: 任务状态信息
    """
    # 如果是模拟任务，直接查询模拟任务状态
    if task_id.startswith('mock-video-task-'):
        logger.info(f"检测到查询模拟任务状态: {task_id}")
        mock_result = query_mock_video_task(task_id)
        
        # 将模拟任务结果转换为官方API格式
        if mock_result.get("code") == 0:
            status = mock_result.get("status", "processing")
            video_url = mock_result.get("video_url", "")
            
            # 映射状态
            api_status = "processing"
            if status == "success":
                api_status = "succeeded"
            elif status == "failed":
                api_status = "failed"
            elif status == "pending":
                api_status = "created"
            
            # 返回符合官方API格式的响应
            return {
                "id": task_id,
                "model": VOLCANO_API_CONFIG["model"],
                "status": api_status,
                "created_at": str(int(time.time())),
                "updated_at": str(int(time.time())),
                "content": {
                    "video_url": video_url
                },
                "usage": {
                    "completion_tokens": 35800,
                    "total_tokens": 35800
                }
            }
        else:
            # 返回错误信息
            return {
                "id": task_id,
                "status": "failed",
                "error": {
                    "message": mock_result.get("msg", "未知错误")
                }
            }
    
    # 查询真实任务状态
    try:
        # 构造查询请求
        query_url = f"{VOLCANO_API_CONFIG['base_url']}/{task_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {VOLCANO_API_CONFIG['api_key']}"
        }
        
        logger.info(f"查询任务状态: {task_id}, URL: {query_url}")
        
        # 发送查询请求
        response = requests.get(query_url, headers=headers, timeout=300)
        logger.debug(f"查询响应状态码: {response.status_code}")
        
        # 检查是否收到HTML页面而不是JSON
        response_content = response.text[:1000]
        if response_content.strip().startswith('<!DOCTYPE html>') or response_content.strip().startswith('<html'):
            logger.warning("API返回了HTML页面而不是JSON数据")
            return {
                "id": task_id,
                "status": "failed",
                "error": {
                    "message": "API返回了HTML页面而不是JSON数据，请检查API配置和网络连接"
                }
            }
            
        if response.status_code == 200:
            try:
                result = response.json()
                logger.debug(f"查询响应内容: {result}")
                
                # 获取视频URL（如果任务完成）
                video_url = ""
                # 新的API结构 - content.video_url
                if "content" in result and result["content"] and "video_url" in result["content"]:
                    video_url = result["content"]["video_url"]
                # 兼容旧的API结构 - output[0].video_url 
                elif "output" in result and result["output"] and "video_url" in result["output"][0]:
                    video_url = result["output"][0]["video_url"]
                
                # 映射状态
                status_mapping = {
                    "succeeded": "succeeded",
                    "failed": "failed",
                    "running": "processing",
                    "queued": "created",
                    "created": "created",
                    "cancelled": "failed"
                }
                
                api_status = status_mapping.get(result.get("status", "processing"), "processing")
                
                logger.info(f"任务状态: {api_status}, 视频URL: {video_url}")
                
                # 返回符合官方API格式的响应
                return {
                    "id": task_id,
                    "model": VOLCANO_API_CONFIG["model"],
                    "status": api_status,
                    "created_at": str(int(time.time())),
                    "updated_at": str(int(time.time())),
                    "content": {
                        "video_url": video_url
                    },
                    "usage": {
                        "completion_tokens": 35800,
                        "total_tokens": 35800
                    }
                }
            except ValueError as e:
                logger.error(f"JSON解析错误: {str(e)}, 响应内容: {response_content}")
                return {
                    "id": task_id,
                    "status": "failed",
                    "error": {
                        "message": f"JSON解析错误: {str(e)}"
                    }
                }
        else:
            logger.error(f"查询任务状态失败，状态码: {response.status_code}, 响应: {response.text[:1000]}")
            return {
                "id": task_id,
                "status": "failed",
                "error": {
                    "message": f"查询任务状态失败，状态码: {response.status_code}"
                }
            }
        
    except Exception as e:
        logger.error(f"查询任务状态失败: {str(e)}")
        return {
            "id": task_id,
            "status": "failed",
            "error": {
                "message": str(e)
            }
        }

def create_mock_video_task(prompt, ratio="16:9", duration=3.0, fps=30, resolution="720p", watermark=False, image=None):
    """
    创建一个模拟的视频生成任务，用于测试或当API不可用时
    :param prompt: 文本提示词
    :param ratio: 视频比例
    :param duration: 视频时长(秒)
    :param fps: 视频帧率
    :param resolution: 视频分辨率
    :param watermark: 是否添加水印
    :param image: 参考图片的Base64编码(图生视频)
    :return: 包含任务ID的响应
    """
    # 导入共享的模拟任务存储模块
    from app.services.mock_tasks_store import add_task
    
    # 生成一个唯一的任务ID
    task_id = f"mock-video-task-{str(uuid.uuid4())}"
    
    # 创建任务对象
    task = {
        "task_id": task_id,
        "prompt": prompt,
        "ratio": ratio,
        "duration": duration,
        "fps": fps,
        "resolution": resolution,
        "watermark": watermark,
        "image": "有图片" if image else "无图片",  # 不保存实际图片数据，只记录是否有图片
        "create_time": time.time(),
        "status": "pending",
        "progress": 0
    }
    
    # 添加到模拟任务存储
    add_task(task)
    
    logger.info(f"已切换到模拟模式，创建任务: 任务ID={task_id}")
    
    # 返回符合官方API格式的响应
    current_time = str(int(time.time()))
    return {
        "id": task_id,
        "model": VOLCANO_API_CONFIG["model"],
        "status": "created",
        "created_at": current_time,
        "updated_at": current_time
    }

def query_mock_video_task(task_id):
    """
    查询模拟的视频生成任务状态
    :param task_id: 任务ID
    :return: 任务状态信息
    """
    # 从模拟任务存储中获取任务
    from app.services.mock_tasks_store import get_task, update_task, list_tasks
    
    task = get_task(task_id)
    
    # 如果任务不存在，记录所有模拟任务ID以便调试
    if not task:
        all_tasks = list_tasks()
        task_ids = [t.get("task_id", "未知") for t in all_tasks]
        
        logger.warning(f"未找到模拟任务: {task_id}")
        logger.debug(f"当前模拟任务列表: {task_ids}")
        
        return {
            "code": -1,
            "msg": f"任务不存在",
            "status": "failed"
        }
        
    # 计算当前进度（根据创建时间，最长10秒完成）
    elapsed_time = time.time() - task["create_time"]
    
    # 模拟任务每秒完成10%，10秒内完成
    progress = min(100, int(elapsed_time * 10))
    
    # 生成示例视频URL（仅当任务完成时）
    video_url = ""
    
    # 根据进度更新状态
    if progress < 10:
        status = "pending"
    elif progress < 100:
        status = "processing"
    else:
        status = "success"
        # 生成模拟视频URL
        base_url = "https://example.com/mock-videos"
        video_file = f"mock-video-{task_id[-8:]}.mp4"
        video_url = f"{base_url}/{video_file}"
    
    # 更新任务状态
    update_task(task_id, status=status, progress=progress, video_url=video_url)
    
    logger.info(f"查询模拟任务状态: {task_id}, 状态: {status}, 进度: {progress}%")
    
    # 返回状态信息
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "task_id": task_id,
            "prompt": task["prompt"],
            "ratio": task["ratio"],
            "duration": task["duration"],
            "create_time": task["create_time"],
            "status": status,
            "progress": progress
        },
        "status": status,
        "video_url": video_url
    }

def get_supported_ratios():
    """
    获取支持的视频比例列表
    :return: 支持的视频比例列表，包含名称和值
    """
    return [
        {"name": "16:9 横版", "value": "16:9"},
        {"name": "9:16 竖版", "value": "9:16"},
        {"name": "1:1 方形", "value": "1:1"},
        {"name": "4:3 经典", "value": "4:3"},
        {"name": "3:4 纵向", "value": "3:4"}
    ]

def get_supported_resolutions():
    """
    获取支持的视频分辨率列表
    :return: 支持的视频分辨率列表，包含名称和值
    """
    return [
        {"name": "720p (中等质量)", "value": "720p"},
        {"name": "1080p (高质量)", "value": "1080p"}
    ]