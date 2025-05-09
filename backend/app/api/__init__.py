from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

# 添加CORS响应处理装饰器
@api_blueprint.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 导入LLM蓝图
from app.api.llm import llm_blueprint

# 导入文生图蓝图
from app.api.text_to_images import text_to_images

# 导入火山引擎文生图蓝图
from app.api.text_to_images_volcano import text_to_images_volcano

# 导入文生视频蓝图
from app.api.text_to_videos import text_to_videos

# 导入图生视频蓝图
from app.api.image_to_videos import image_to_videos

# 导入代理服务蓝图
from app.api.proxy import proxy_blueprint

# 导入阿里云图片风格调整蓝图
from app.api.image_style import image_style

# 导入阿里云图片重绘蓝图
from app.api.image_redraw import image_redraw

# 导入数字人蓝图
from app.api.aibeings import aibeings_bp

# 导入PPT信息获取蓝图
from app.api.aibeings_ppt_info import aibeings_ppt_info_bp

# 导入数字人任务状态查询蓝图
from app.api.aibeings_task_status import aibeings_task_status_bp

# 导入文件上传蓝图
from app.api.upload import upload_blueprint

# 导入论文大纲编写蓝图
from app.api.academic_paper import academic_paper_bp

# 导入音频转文本蓝图
from app.api.audio_to_text import audio_to_text_bp

# 导入v1版本API蓝图
from app.api.v1 import api_v1_blueprint

# 导入创客贴API蓝图
from app.api.chuangkit import chuangkit_bp

# 注册v1版本API蓝图
api_blueprint.register_blueprint(api_v1_blueprint)

# 注册LLM蓝图
api_blueprint.register_blueprint(llm_blueprint, url_prefix='/llm')

# 注册文生图蓝图（直接在根路由下，不加前缀）
api_blueprint.register_blueprint(text_to_images)

# 注册火山引擎文生图蓝图（直接在根路由下，不加前缀）
api_blueprint.register_blueprint(text_to_images_volcano)

# 注册文生视频蓝图（直接在根路由下，不加前缀）
api_blueprint.register_blueprint(text_to_videos)

# 注册图生视频蓝图（直接在根路由下，不加前缀）
api_blueprint.register_blueprint(image_to_videos)

# 注册代理服务蓝图
api_blueprint.register_blueprint(proxy_blueprint, url_prefix='/proxy')

# 注册阿里云图片风格调整蓝图（直接在根路由下，不加前缀）
api_blueprint.register_blueprint(image_style)

# 注册阿里云图片重绘蓝图（直接在根路由下，不加前缀）
api_blueprint.register_blueprint(image_redraw)

# 注册数字人蓝图
api_blueprint.register_blueprint(aibeings_bp, url_prefix='/aibeings')

# 注册PPT信息获取蓝图
api_blueprint.register_blueprint(aibeings_ppt_info_bp, url_prefix='/aibeings')

# 注册数字人任务状态查询蓝图
api_blueprint.register_blueprint(aibeings_task_status_bp, url_prefix='/aibeings')

# 注册文件上传蓝图
api_blueprint.register_blueprint(upload_blueprint, url_prefix='/upload')

# 注册论文大纲编写蓝图
api_blueprint.register_blueprint(academic_paper_bp, url_prefix='/academic')

# 注册音频转文本蓝图
api_blueprint.register_blueprint(audio_to_text_bp)

# 注册创客贴API蓝图
api_blueprint.register_blueprint(chuangkit_bp, url_prefix='/chuangkit')

# 推迟导入视图，避免循环引用
from app.api import apps, users 