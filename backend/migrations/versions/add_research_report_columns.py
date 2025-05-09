"""添加研究报告相关列到学术论文表

Revision ID: add_research_report_columns
Revises: add_academic_papers_table
Create Date: 2023-08-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_research_report_columns'
down_revision = 'add_academic_papers_table'  # 前一个迁移版本是创建学术论文表
branch_labels = None
depends_on = None


def upgrade():
    """添加研究报告相关列"""
    # 添加 query_id 列，用于存储研究报告大纲接口返回的 queryID
    op.add_column('academic_papers',
                  sa.Column('query_id', sa.String(length=255), nullable=True))
    
    # 添加 callback_url 列，用于存储回调通知地址
    op.add_column('academic_papers',
                  sa.Column('callback_url', sa.String(length=512), nullable=True))
    
    # 为 query_id 添加索引以提高查询性能
    op.create_index(op.f('ix_academic_papers_query_id'), 'academic_papers', ['query_id'], unique=False)


def downgrade():
    """回滚操作"""
    # 删除索引
    op.drop_index(op.f('ix_academic_papers_query_id'), table_name='academic_papers')
    
    # 删除列
    op.drop_column('academic_papers', 'callback_url')
    op.drop_column('academic_papers', 'query_id') 