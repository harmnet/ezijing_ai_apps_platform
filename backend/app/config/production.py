import os
from datetime import timedelta

class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # 百度文心API配置
    WENCHAIN_PARTNER_ID = os.getenv('WENCHAIN_PARTNER_ID')
    WENCHAIN_API_SECRET = os.getenv('WENCHAIN_API_SECRET')
    
    # 上传文件保存位置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp')
    # 允许的文件类型
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4'} 