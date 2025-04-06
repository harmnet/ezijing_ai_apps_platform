from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.auth import auth_blueprint
from app.models.user import User
from app import db

@auth_blueprint.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    # 验证数据
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({
            'status': 'error',
            'message': '缺少必要字段'
        }), 400
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'status': 'error',
            'message': '用户名已被使用'
        }), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'status': 'error',
            'message': '邮箱已被使用'
        }), 400
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.password = data['password']
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '注册成功'
    }), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    # 验证数据
    if not all(k in data for k in ('username', 'password')):
        return jsonify({
            'status': 'error',
            'message': '缺少用户名或密码'
        }), 400
    
    # 查询用户
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({
            'status': 'error',
            'message': '用户名或密码错误'
        }), 401
    
    # 检查用户是否激活
    if not user.is_active:
        return jsonify({
            'status': 'error',
            'message': '账户已被禁用，请联系管理员'
        }), 403
    
    # 生成令牌
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'status': 'success',
        'message': '登录成功',
        'data': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
    }), 200

@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新访问令牌"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    
    return jsonify({
        'status': 'success',
        'data': {
            'access_token': access_token
        }
    }), 200 