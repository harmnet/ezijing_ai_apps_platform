import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化SQLAlchemy
db = SQLAlchemy()
# 初始化JWT
jwt = JWTManager()
# 初始化Migrate
migrate = Migrate()

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
    
    # 初始化扩展
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # 这里我们使用条件导入，以便于迁移过程能够成功运行
    # 即使某些依赖模块不存在，也不会影响基本的数据库操作
    if config_name != 'migrations':
        try:
            # 注册蓝图
            from app.api import api_blueprint
            from app.auth import auth_blueprint
            
            app.register_blueprint(api_blueprint)
            app.register_blueprint(auth_blueprint)
            
            # 手动导入和注册数字人PPT讲解视频蓝图
            from app.api.digital_human.ppt_video import digital_human_ppt_bp
            app.register_blueprint(digital_human_ppt_bp)
            
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
            
            # 添加兼容性路由 - 将老路径映射到新路径
            from flask import request, redirect
            
            @app.route('/api/digital-human/create-ppt-video', methods=['POST'])
            def redirect_to_ppt_video_api():
                """兼容性路由，将旧API请求转发到新API"""
                from app.api.digital_human.ppt_video import api_create_ppt_video_task
                # 直接调用目标视图函数
                return api_create_ppt_video_task()
        except ImportError as e:
            app.logger.warning(f"某些模块导入失败，但不影响基本功能: {str(e)}")
    
    return app 