"""添加学术论文表

Revision ID: add_academic_papers_table
Revises: create_auth_tables
Create Date: 2023-07-21 14:25:04.123456

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_academic_papers_table'
down_revision = 'create_auth_tables'  # 根据实际情况设置前一个迁移版本
branch_labels = None
depends_on = None


def upgrade():
    # 创建学术论文表
    op.create_table(
        'academic_papers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('query', sa.Text(), nullable=False),
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
    op.create_index(op.f('ix_academic_papers_user_id'), 'academic_papers', ['user_id'], unique=False)
    op.create_index(op.f('ix_academic_papers_doc_id'), 'academic_papers', ['doc_id'], unique=False)
    op.create_index(op.f('ix_academic_papers_created_at'), 'academic_papers', ['created_at'], unique=False)


def downgrade():
    # 删除索引
    op.drop_index(op.f('ix_academic_papers_created_at'), table_name='academic_papers')
    op.drop_index(op.f('ix_academic_papers_doc_id'), table_name='academic_papers')
    op.drop_index(op.f('ix_academic_papers_user_id'), table_name='academic_papers')
    
    # 删除表
    op.drop_table('academic_papers') 