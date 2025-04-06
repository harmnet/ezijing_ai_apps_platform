from datetime import datetime
from app import db

class PPTVideoTask(db.Model):
    """
    数字人PPT视频任务记录模型
    用于存储数字人微课制作的历史记录
    """
    __tablename__ = 'ppt_video_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    ppt_url = db.Column(db.String(500), nullable=False, comment='PPT文件URL')
    text_script = db.Column(db.Text, nullable=True, comment='讲解文本')
    title = db.Column(db.String(255), nullable=False, comment='视频标题')
    virtual_human_id = db.Column(db.String(50), nullable=False, comment='数字人ID')
    virtual_human_posture_id = db.Column(db.String(50), nullable=False, comment='姿势ID')
    resolution = db.Column(db.String(20), nullable=False, comment='视频分辨率')
    convert_type = db.Column(db.String(20), nullable=False, comment='转换类型')
    task_id = db.Column(db.String(50), unique=True, nullable=False, comment='任务ID')
    status = db.Column(db.String(20), default='creating', comment='任务状态')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    completed_at = db.Column(db.DateTime, nullable=True, comment='完成时间')
    video_url = db.Column(db.String(500), nullable=True, comment='视频URL')
    thumbnail_url = db.Column(db.String(500), nullable=True, comment='缩略图URL')
    
    def __repr__(self):
        return f'<PPTVideoTask {self.task_id}>'
    
    def to_dict(self):
        """
        将模型转换为字典
        """
        return {
            'id': self.id,
            'ppt_url': self.ppt_url,
            'text_script': self.text_script,
            'title': self.title,
            'virtual_human_id': self.virtual_human_id,
            'virtual_human_posture_id': self.virtual_human_posture_id,
            'resolution': self.resolution,
            'convert_type': self.convert_type,
            'task_id': self.task_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'video_url': self.video_url,
            'thumbnail_url': self.thumbnail_url
        } 