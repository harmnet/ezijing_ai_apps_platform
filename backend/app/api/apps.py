from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import api_blueprint
from app.models.app import AIApp

@api_blueprint.route('/apps', methods=['GET'])
def get_apps():
    """获取所有公开的应用"""
    apps = AIApp.query.filter_by(is_public=True, status='active').all()
    return jsonify({
        'status': 'success',
        'data': [app.to_dict() for app in apps]
    }), 200

@api_blueprint.route('/apps/<int:app_id>', methods=['GET'])
def get_app(app_id):
    """根据ID获取应用详情"""
    app = AIApp.query.get_or_404(app_id)
    if not app.is_public and not (get_jwt_identity() == app.creator_id):
        return jsonify({
            'status': 'error',
            'message': '无权访问此应用'
        }), 403
    
    return jsonify({
        'status': 'success',
        'data': app.to_dict()
    }), 200

@api_blueprint.route('/apps', methods=['POST'])
@jwt_required()
def create_app():
    """创建新应用"""
    data = request.get_json()
    
    # 验证必要字段
    required_fields = ['name', 'app_type']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'缺少必要字段: {field}'
            }), 400
    
    # 创建新应用
    new_app = AIApp(
        name=data['name'],
        description=data.get('description', ''),
        icon_url=data.get('icon_url', ''),
        app_type=data['app_type'],
        api_endpoint=data.get('api_endpoint', ''),
        creator_id=get_jwt_identity(),
        is_public=data.get('is_public', True)
    )
    
    db.session.add(new_app)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '应用创建成功',
        'data': new_app.to_dict()
    }), 201

@api_blueprint.route('/apps/<int:app_id>', methods=['PUT'])
@jwt_required()
def update_app(app_id):
    """更新应用信息"""
    app = AIApp.query.get_or_404(app_id)
    
    # 验证权限
    if get_jwt_identity() != app.creator_id:
        return jsonify({
            'status': 'error',
            'message': '您没有权限更新此应用'
        }), 403
    
    data = request.get_json()
    
    # 更新应用信息
    if 'name' in data:
        app.name = data['name']
    if 'description' in data:
        app.description = data['description']
    if 'icon_url' in data:
        app.icon_url = data['icon_url']
    if 'app_type' in data:
        app.app_type = data['app_type']
    if 'api_endpoint' in data:
        app.api_endpoint = data['api_endpoint']
    if 'is_public' in data:
        app.is_public = data['is_public']
    if 'status' in data:
        app.status = data['status']
        
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '应用更新成功',
        'data': app.to_dict()
    }), 200

@api_blueprint.route('/apps/<int:app_id>', methods=['DELETE'])
@jwt_required()
def delete_app(app_id):
    """删除应用"""
    app = AIApp.query.get_or_404(app_id)
    
    # 验证权限
    if get_jwt_identity() != app.creator_id:
        return jsonify({
            'status': 'error',
            'message': '您没有权限删除此应用'
        }), 403
    
    db.session.delete(app)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '应用已成功删除'
    }), 200 