"""添加研究报告表

Revision ID: add_research_reports_table
Revises: add_academic_papers_table
Create Date: 2025-04-08 14:15:00.123456

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_research_reports_table'
down_revision = 'add_academic_papers_table'  # 根据实际情况设置前一个迁移版本
branch_labels = None
depends_on = None


def upgrade():
    # 创建研究报告表
    op.create_table(
        'research_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('outline', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('doc_id', sa.String(length=255), nullable=True),
        sa.Column('document_status', sa.String(length=20), nullable=False, server_default='none'),
        sa.Column('status_message', sa.String(length=255), nullable=True),
        sa.Column('download_url', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 添加索引以提高查询性能
    op.create_index(op.f('ix_research_reports_user_id'), 'research_reports', ['user_id'], unique=False)
    op.create_index(op.f('ix_research_reports_doc_id'), 'research_reports', ['doc_id'], unique=False)
    op.create_index(op.f('ix_research_reports_created_at'), 'research_reports', ['created_at'], unique=False)


def downgrade():
    # 删除索引
    op.drop_index(op.f('ix_research_reports_created_at'), table_name='research_reports')
    op.drop_index(op.f('ix_research_reports_doc_id'), table_name='research_reports')
    op.drop_index(op.f('ix_research_reports_user_id'), table_name='research_reports')
    
    # 删除表
    op.drop_table('research_reports') 