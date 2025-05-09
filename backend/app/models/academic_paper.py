"""
学术论文模型定义
包含论文大纲和生成的论文记录
"""

import logging
from datetime import datetime
from app import db

class AcademicPaper(db.Model):
    """学术论文模型"""
    __tablename__ = 'academic_papers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    query = db.Column(db.Text, nullable=False)  # 用户输入的查询/主题
    outline = db.Column(db.Text, nullable=True)  # 生成的论文大纲
    content = db.Column(db.Text, nullable=True)  # 生成的论文内容
    doc_id = db.Column(db.String(255), nullable=True)  # 百度文心API返回的文档ID
    query_id = db.Column(db.String(255), nullable=True)  # 研报大纲接口返回的queryID
    document_status = db.Column(db.String(20), default='none')  # none, generating, completed, failed
    status_message = db.Column(db.String(255), nullable=True)  # 状态描述或错误信息
    download_url = db.Column(db.String(512), nullable=True)  # 下载链接
    callback_url = db.Column(db.String(512), nullable=True)  # 回调通知地址
    
    # 时间戳 - 使用本地时间而非UTC时间
    created_at = db.Column(db.DateTime, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    
    def __repr__(self):
        return f'<AcademicPaper {self.id}: {self.title}>'
    
    def to_dict(self):
        """转换为字典，用于API响应"""
        # 记录对象中的时间戳值，方便调试
        logging.info(f"to_dict - ID: {self.id}, created_at类型: {type(self.created_at)}, created_at值: {self.created_at}")
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'query': self.query,
            'outline': self.outline,
            'has_content': bool(self.content),  # 不直接返回内容，只返回是否有内容
            'doc_id': self.doc_id,
            'query_id': self.query_id,
            'document_status': self.document_status,
            'status_message': self.status_message,
            'download_url': self.download_url,
            'created_at': self.created_at.isoformat() if self.created_at else datetime.now().isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else datetime.now().isoformat()
        } 