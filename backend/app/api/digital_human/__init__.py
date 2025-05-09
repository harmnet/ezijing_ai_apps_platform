# 数字人相关API接口包
from .ppt_video import digital_human_ppt_bp
from app.api.digital_human.baidu_digital_human import baidu_digital_human_bp

# 导出蓝图列表
blueprints = [
    digital_human_ppt_bp,
    baidu_digital_human_bp
]

def init_app(app):
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix='/api/v1/digital_human')