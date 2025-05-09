#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI应用案例API
提供案例的CRUD操作
"""

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.app_case import AppCase
from datetime import datetime

app_case_bp = Blueprint('app_case', __name__)

@app_case_bp.route('/app-cases', methods=['GET'])
def get_app_cases():
    """获取AI应用案例列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        case_type = request.args.get('case_type')
        industry = request.args.get('industry')
        
        # 构建查询
        query = AppCase.query
        
        # 应用过滤条件
        if case_type:
            query = query.filter(AppCase.case_type == case_type)
        if industry:
            query = query.filter(AppCase.industry == industry)
        
        # 执行分页查询
        pagination = query.order_by(AppCase.updated_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # 构造响应数据
        result = {
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages,
            'items': [case.to_dict() for case in pagination.items]
        }
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    
    except Exception as e:
        current_app.logger.error(f"获取AI应用案例列表失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"获取案例列表失败: {str(e)}"
        }), 500

@app_case_bp.route('/app-cases/<int:case_id>', methods=['GET'])
def get_app_case(case_id):
    """获取单个AI应用案例详情"""
    try:
        case = AppCase.query.get(case_id)
        if not case:
            return jsonify({
                'status': 'error',
                'message': f"案例不存在，ID: {case_id}"
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': case.to_dict()
        })
    
    except Exception as e:
        current_app.logger.error(f"获取AI应用案例详情失败，ID: {case_id}, 错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"获取案例详情失败: {str(e)}"
        }), 500

@app_case_bp.route('/app-cases', methods=['POST'])
def create_app_case():
    """创建新的AI应用案例"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': "缺少请求数据"
            }), 400
        
        # 验证必要字段
        required_fields = ['name', 'case_type', 'industry']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'status': 'error',
                    'message': f"缺少必要字段: {field}"
                }), 400
        
        # 创建新案例
        new_case = AppCase(
            name=data['name'],
            case_type=data['case_type'],
            industry=data['industry'],
            study_hours=data.get('study_hours'),
            tags=data.get('tags'),
            cover_url=data.get('cover_url'),
            updated_by=data.get('updated_by')
        )
        
        # 保存到数据库
        db.session.add(new_case)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': "案例创建成功",
            'data': new_case.to_dict()
        }), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"创建AI应用案例数据库错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"数据库错误: {str(e)}"
        }), 500
    except Exception as e:
        current_app.logger.error(f"创建AI应用案例失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"创建案例失败: {str(e)}"
        }), 500

@app_case_bp.route('/app-cases/<int:case_id>', methods=['PUT'])
def update_app_case(case_id):
    """更新AI应用案例"""
    try:
        # 查找案例
        case = AppCase.query.get(case_id)
        if not case:
            return jsonify({
                'status': 'error',
                'message': f"案例不存在，ID: {case_id}"
            }), 404
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': "缺少请求数据"
            }), 400
        
        # 更新字段
        if 'name' in data:
            case.name = data['name']
        if 'case_type' in data:
            case.case_type = data['case_type']
        if 'industry' in data:
            case.industry = data['industry']
        if 'study_hours' in data:
            case.study_hours = data['study_hours']
        if 'tags' in data:
            case.tags = data['tags']
        if 'cover_url' in data:
            case.cover_url = data['cover_url']
        if 'updated_by' in data:
            case.updated_by = data['updated_by']
        
        # 更新时间自动更新
        case.updated_at = datetime.now()
        
        # 保存更改
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': "案例更新成功",
            'data': case.to_dict()
        })
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"更新AI应用案例数据库错误，ID: {case_id}, 错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"数据库错误: {str(e)}"
        }), 500
    except Exception as e:
        current_app.logger.error(f"更新AI应用案例失败，ID: {case_id}, 错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"更新案例失败: {str(e)}"
        }), 500

@app_case_bp.route('/app-cases/<int:case_id>', methods=['DELETE'])
def delete_app_case(case_id):
    """删除AI应用案例"""
    try:
        # 查找案例
        case = AppCase.query.get(case_id)
        if not case:
            return jsonify({
                'status': 'error',
                'message': f"案例不存在，ID: {case_id}"
            }), 404
        
        # 删除案例
        db.session.delete(case)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f"案例已成功删除，ID: {case_id}"
        })
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"删除AI应用案例数据库错误，ID: {case_id}, 错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"数据库错误: {str(e)}"
        }), 500
    except Exception as e:
        current_app.logger.error(f"删除AI应用案例失败，ID: {case_id}, 错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"删除案例失败: {str(e)}"
        }), 500 