from datetime import datetime
from app import db

class AppCase(db.Model):
    """
    AI应用案例模型
    用于存储AI应用案例的基本信息
    """
    __tablename__ = 'app_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, comment='案例名称')
    case_type = db.Column(db.String(50), nullable=False, comment='案例类型')
    industry = db.Column(db.String(100), nullable=False, comment='所在行业')
    study_hours = db.Column(db.Float, nullable=True, comment='学时')
    tags = db.Column(db.String(500), nullable=True, comment='主要标签，多个标签以逗号分隔')
    cover_url = db.Column(db.String(500), nullable=True, comment='封面图片地址')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    updated_by = db.Column(db.String(100), nullable=True, comment='更新人')
    
    def __repr__(self):
        return f'<AppCase {self.name}>'
    
    def to_dict(self):
        """
        将模型转换为字典
        """
        return {
            'id': self.id,
            'name': self.name,
            'case_type': self.case_type,
            'industry': self.industry,
            'study_hours': self.study_hours,
            'tags': self.tags,
            'cover_url': self.cover_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by
        } 