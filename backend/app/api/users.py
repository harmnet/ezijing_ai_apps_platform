from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import api_blueprint
from app.models.user import User

@api_blueprint.route('/users/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """获取当前用户的个人资料"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'status': 'success',
        'data': user.to_dict()
    }), 200

@api_blueprint.route('/users/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """更新当前用户的个人资料"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    
    # 更新用户信息
    if 'username' in data:
        # 检查用户名是否已被使用
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({
                'status': 'error',
                'message': '用户名已被使用'
            }), 400
        user.username = data['username']
    
    if 'email' in data:
        # 检查邮箱是否已被使用
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({
                'status': 'error',
                'message': '邮箱已被使用'
            }), 400
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '个人资料更新成功',
        'data': user.to_dict()
    }), 200

@api_blueprint.route('/users/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改当前用户的密码"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    
    # 验证请求数据
    if not all(k in data for k in ('current_password', 'new_password')):
        return jsonify({
            'status': 'error',
            'message': '缺少必要字段'
        }), 400
    
    # 验证当前密码
    if not user.verify_password(data['current_password']):
        return jsonify({
            'status': 'error',
            'message': '当前密码不正确'
        }), 400
    
    # 设置新密码
    user.password = data['new_password']
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '密码修改成功'
    }), 200 