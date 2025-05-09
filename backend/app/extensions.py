"""
扩展模块，用于存放共享的Flask扩展实例
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# 初始化SQLAlchemy
db = SQLAlchemy()

# 初始化JWT
jwt = JWTManager()

# 初始化Migrate
migrate = Migrate() 