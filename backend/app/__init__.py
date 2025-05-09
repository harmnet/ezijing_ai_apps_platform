import os
import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import time
from app.extensions import db, jwt, migrate
from app.api.digital_human import init_app as init_digital_human
from app.utils.logger import setup_image_redraw_logger

# 设置日志目录
LOG_DIR = os.environ.get('LOG_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# 设置日志配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# 获取根日志器并设置级别
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# 确保所有子日志器也使用DEBUG级别
for handler in root_logger.handlers:
    handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.info("应用启动，日志系统已初始化")

# 加载环境变量
load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # 配置
    app_settings = os.getenv('APP_SETTINGS', 'app.config.development.DevelopmentConfig')
    app.config.from_object(app_settings)
    
    # 设置文件上传配置
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 限制上传文件大小为50MB
    
    # 确保临时文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 应用CORS - 使用最简单的配置，允许所有来源
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # 数据库和认证初始化
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # 初始化数字人API模块
    init_digital_human(app)
    
    # 初始化图像重绘专用日志记录器
    setup_image_redraw_logger(app)
    app.logger.info("已初始化图像重绘专用日志记录器")
    
    # 这里我们使用条件导入，以便于迁移过程能够成功运行
    # 即使某些依赖模块不存在，也不会影响基本的数据库操作
    if config_name != 'migrations':
        try:
            # 禁用流式响应的压缩，确保SSE可以正确工作
            @app.after_request
            def disable_compression_for_sse(response):
                """禁用SSE响应的压缩，以确保流式传输能够正常工作"""
                if response.mimetype == 'text/event-stream':
                    # 设置为无压缩
                    response.headers['Content-Encoding'] = 'identity'
                    # 确保其他与流式传输相关的头部设置正确
                    response.headers['Cache-Control'] = 'no-cache'
                    response.headers['X-Accel-Buffering'] = 'no'
                    response.headers['Connection'] = 'keep-alive'
                    # 记录日志
                    app.logger.debug("已禁用SSE响应的压缩")
                return response
            
            # 注册蓝图
            from app.api import api_blueprint
            from app.auth import auth_blueprint
            
            app.register_blueprint(api_blueprint)
            app.register_blueprint(auth_blueprint)
            
            # 注册文件上传蓝图
            try:
                from app.api.uploads.upload_routes import upload_bp
                app.register_blueprint(upload_bp, url_prefix='/api/v1/uploads')
                app.logger.info("文件上传蓝图已注册，用于处理OSS文件上传")
            except Exception as e:
                app.logger.error(f"注册文件上传蓝图失败: {str(e)}")
            
            # 注册百度云存储上传蓝图
            try:
                from app.api.upload import upload_blueprint as baidubce_upload_bp
                app.register_blueprint(baidubce_upload_bp, url_prefix='/api/v1/upload')
                app.logger.info("百度云存储上传蓝图已注册，用于处理BOS文件上传")
            except Exception as e:
                app.logger.error(f"注册百度云存储上传蓝图失败: {str(e)}")
            
            # 注册AIPPT代理蓝图
            try:
                from app.api.aippt_proxy import aippt_proxy_bp
                app.register_blueprint(aippt_proxy_bp, url_prefix='/aippt-proxy')
                app.logger.info("AIPPT代理蓝图已注册")
            except Exception as e:
                app.logger.error(f"注册AIPPT代理蓝图失败: {str(e)}")
            
            # 注册模板套装搜索蓝图
            try:
                # 启用模板套装搜索蓝图，处理模板相关请求
                from app.api.template_suit import template_suit_bp
                app.register_blueprint(template_suit_bp, url_prefix='/aippt-proxy')
                app.logger.info("模板套装搜索蓝图已注册，用于处理模板相关请求")
            except Exception as e:
                app.logger.error(f"注册模板套装搜索蓝图失败: {str(e)}")
            
            # 注册LLM API蓝图
            try:
                from app.api.llm_api import llm_api_bp
                app.register_blueprint(llm_api_bp, url_prefix='/api/v1/llm')
                app.logger.info("LLM API蓝图已注册，用于处理大模型交互请求")
            except Exception as e:
                app.logger.error(f"注册LLM API蓝图失败: {str(e)}")
            
            # 注册音频转文本蓝图
            try:
                from app.api.audio_to_text import audio_to_text_bp
                app.register_blueprint(audio_to_text_bp, url_prefix='/api/v1')
                app.logger.info("音频转文本蓝图已注册")
            except Exception as e:
                app.logger.error(f"注册音频转文本蓝图失败: {str(e)}")
            
            # 注册文件对话蓝图
            try:
                from app.api.file_chat import file_chat_bp
                app.register_blueprint(file_chat_bp, url_prefix='/api/v1/file_chat')
                app.logger.info("文件对话蓝图已注册")
            except Exception as e:
                app.logger.error(f"注册文件对话蓝图失败: {str(e)}")
            
            # 注册文心AI搜索蓝图
            try:
                from app.api.wenxin_search import wenxin_search_bp
                app.register_blueprint(wenxin_search_bp, url_prefix='/api/v1/wenxin')
                app.logger.info("文心AI搜索蓝图已注册，用于处理AI综合搜索请求")
            except Exception as e:
                app.logger.error(f"注册文心AI搜索蓝图失败: {str(e)}")
            
            # 注册知识库问答蓝图
            try:
                from app.api.knowledge import knowledge_bp
                app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
                app.logger.info("知识库问答蓝图已注册，用于处理文档上传和问答请求")
            except Exception as e:
                app.logger.error(f"注册知识库问答蓝图失败: {str(e)}")
            
            # 注册阿里云图片重绘蓝图
            try:
                from app.api.image_redraw import image_redraw
                app.register_blueprint(image_redraw, url_prefix='/api/v1')
                app.logger.info("阿里云图片重绘蓝图已注册")
            except Exception as e:
                app.logger.error(f"注册阿里云图片重绘蓝图失败: {str(e)}")
                
            # 注册专门的阿里云图片上传蓝图
            try:
                from app.api.aliyun_upload import aliyun_upload_bp
                app.register_blueprint(aliyun_upload_bp, url_prefix='/api/images')
                app.logger.info("阿里云图片上传专用蓝图已注册 - 用于处理前端的图片上传请求")
            except Exception as e:
                app.logger.error(f"注册阿里云图片上传专用蓝图失败: {str(e)}")
                
            # 注册AI应用案例蓝图
            try:
                from app.api.app_case import app_case_bp
                app.register_blueprint(app_case_bp, url_prefix='/api/v1')
                app.logger.info("AI应用案例蓝图已注册，用于管理案例信息")
            except Exception as e:
                app.logger.error(f"注册AI应用案例蓝图失败: {str(e)}")
            
            # 添加兼容性路由 - 将老路径映射到新路径
            from flask import request, redirect
            
            @app.route('/api/digital-human/create-ppt-video', methods=['POST'])
            def redirect_to_ppt_video_api():
                """兼容性路由，将旧API请求转发到新API"""
                from app.api.digital_human.ppt_video import api_create_ppt_video_task
                # 直接调用目标视图函数
                return api_create_ppt_video_task()
                
            # 添加兼容性路由 - 处理论文大纲请求
            @app.route('/api/academic/paper_outline', methods=['POST', 'OPTIONS'])
            def handle_paper_outline():
                """兼容性路由，将请求转发到正确的API路径"""
                from app.api.academic_paper import paper_outline, paper_outline_options
                if request.method == 'OPTIONS':
                    return paper_outline_options()
                return paper_outline()
                
            # 添加兼容性路由 - 处理论文生成请求
            @app.route('/api/academic/generate-paper', methods=['POST', 'OPTIONS'])
            def handle_generate_paper():
                """兼容性路由，将请求转发到正确的API路径"""
                from app.api.academic_paper import generate_paper, generate_paper_options
                if request.method == 'OPTIONS':
                    return generate_paper_options()
                return generate_paper()
                
            # 添加兼容性路由 - 处理大纲生成论文请求
            @app.route('/api/academic/paper_from_outline', methods=['POST', 'OPTIONS'])
            def handle_paper_from_outline():
                """兼容性路由，将请求转发到正确的API路径"""
                from app.api.academic_paper import paper_from_outline, generate_paper_options
                if request.method == 'OPTIONS':
                    return generate_paper_options()
                return paper_from_outline()
            
            # 添加兼容性路由 - 将请求转发到正确的API路径
            @app.route('/api/v1/llm/file_chat', methods=['POST', 'OPTIONS'])
            def handle_file_chat():
                """兼容性路由，支持文件上传到LLM API"""
                app.logger.info("收到文件上传校对请求")
                if request.method == 'OPTIONS':
                    response = app.make_default_options_response()
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
                    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                    return response
                
                from app.api.llm import file_chat
                return file_chat()
            
            # 添加学术论文专用蓝图
            try:
                from app.api.academic_paper import academic_paper_bp
                app.register_blueprint(academic_paper_bp, url_prefix='/api/v1/academic')
                app.logger.info("学术论文蓝图已注册，用于处理论文生成和历史记录请求")
            except Exception as e:
                app.logger.error(f"注册学术论文蓝图失败: {str(e)}")
        except ImportError as e:
            app.logger.warning(f"某些模块导入失败，但不影响基本功能: {str(e)}")
    
    return app 