from flask import Blueprint

# 创建v1版本API蓝图
api_v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/v1')

# 导入LLM模块
from app.api.v1.llm.chat import bp as llm_bp
from app.api.v1.llm.deepseek_volcano_stream import bp as deepseek_volcano_bp

# 注册LLM蓝图
api_v1_blueprint.register_blueprint(llm_bp)
api_v1_blueprint.register_blueprint(deepseek_volcano_bp) 