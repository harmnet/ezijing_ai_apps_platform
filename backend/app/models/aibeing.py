from datetime import datetime
from app import db

class AIBeing(db.Model):
    """数字人模型定义"""
    __tablename__ = 'ai_beings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='数字人名称')
    avatar = db.Column(db.String(255), comment='数字人头像URL')
    description = db.Column(db.Text, comment='数字人描述')
    type = db.Column(db.String(50), nullable=False, comment='数字人类型')
    status = db.Column(db.String(20), default='active', comment='状态：active, inactive')
    config = db.Column(db.JSON, comment='数字人配置信息')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'description': self.description,
            'type': self.type,
            'status': self.status,
            'config': self.config,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<AIBeing {self.name}>' 