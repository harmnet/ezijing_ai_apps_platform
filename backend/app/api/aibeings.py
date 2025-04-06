from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.aibeing_service import AIBeingService
import logging
import os
import uuid
import requests
import oss2
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)
aibeings_bp = Blueprint('aibeings', __name__)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'ppt', 'pptx', 'pdf', 'jpg', 'jpeg', 'png', 'mp4', 'mp3'}

# 上传文件临时保存目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uploads')

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件类型是否允许上传"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_oss(file_path, object_name):
    """上传文件到阿里云OSS
    
    Args:
        file_path: 本地文件路径
        object_name: OSS中的对象名称
        
    Returns:
        OSS访问URL
    """
    try:
        # 从环境变量获取OSS配置
        access_key_id = os.environ.get('ALIYUN_OSS_ACCESS_KEY_ID')
        access_key_secret = os.environ.get('ALIYUN_OSS_ACCESS_KEY_SECRET')
        endpoint = os.environ.get('ALIYUN_OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
        bucket_name = os.environ.get('ALIYUN_OSS_BUCKET_NAME', 'ezijingai')
        
        if not (access_key_id and access_key_secret and bucket_name):
            logger.error("OSS配置不完整")
            return None
        
        # 创建OSS认证和Bucket实例
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        
        # 上传文件
        result = bucket.put_object_from_file(object_name, file_path)
        
        # 检查上传结果
        if result.status == 200:
            logger.info(f"文件上传到OSS成功: {object_name}")
            # 构建访问URL
            return f"https://{bucket_name}.{endpoint}/{object_name}"
        else:
            logger.error(f"文件上传到OSS失败: {result.status}")
            return None
            
    except Exception as e:
        logger.error(f"上传到OSS时发生错误: {str(e)}")
        return None

@aibeings_bp.route('/upload', methods=['POST'])
def upload_file():
    """处理数字人相关文件上传请求"""
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return jsonify({'error': '没有文件部分'}), 400
        
        file = request.files['file']
        
        # 检查文件是否为空
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 检查文件类型是否允许
        if not allowed_file(file.filename):
            return jsonify({'error': f'文件类型不允许。允许的类型: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # 安全地获取文件名并添加UUID前缀以避免文件名冲突
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存文件到临时目录
        file.save(file_path)
        
        # 上传到阿里云OSS
        oss_path = f"media_upload/customize/user-upload/scene/pdf/{unique_filename}"
        oss_url = upload_to_oss(file_path, oss_path)
        
        logger.info(f"数字人文件上传成功: {file_path}, OSS URL: {oss_url}")
        
        # 如果上传到OSS成功，返回OSS URL
        if oss_url:
            return jsonify({
                'message': '文件上传成功',
                'filename': unique_filename,
                'url': oss_url
            })
        else:
            # 如果上传到OSS失败，返回本地URL
            file_url = f"/uploads/{unique_filename}"
            return jsonify({
                'message': '文件上传到本地成功（OSS上传失败）',
                'filename': unique_filename,
                'url': file_url
            })
        
    except Exception as e:
        logger.error(f"数字人文件上传失败: {str(e)}")
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500

@aibeings_bp.route('/aibeings', methods=['GET'])
def get_aibeings():
    """
    获取数字人列表API
    
    请求参数:
    - page: 页码，默认为1
    - per_page: 每页数量，默认为20
    - type: 类型过滤
    - status: 状态过滤
    
    返回:
    {
        "code": 0,
        "data": {
            "items": [数字人对象列表],
            "page": 当前页码,
            "per_page": 每页数量,
            "total_pages": 总页数,
            "total_count": 总记录数
        },
        "message": "success"
    }
    """
    try:
        # 获取请求参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 构建过滤条件
        filters = {}
        if 'type' in request.args and request.args.get('type'):
            filters['type'] = request.args.get('type')
        if 'status' in request.args and request.args.get('status'):
            filters['status'] = request.args.get('status')
            
        # 调用服务获取数据
        aibeings, total_pages, total_count = AIBeingService.get_all_aibeings(
            page=page, 
            per_page=per_page,
            filters=filters
        )
        
        # 构建响应数据
        response_data = {
            "code": 0,
            "data": {
                "items": aibeings,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "total_count": total_count
            },
            "message": "success"
        }
        
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"获取数字人列表时出错: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取数字人列表失败: {str(e)}",
            "data": None
        }), 500

@aibeings_bp.route('/aibeings/<int:aibeing_id>', methods=['GET'])
def get_aibeing(aibeing_id):
    """
    获取单个数字人详情API
    
    路径参数:
    - aibeing_id: 数字人ID
    
    返回:
    {
        "code": 0,
        "data": 数字人对象,
        "message": "success"
    }
    """
    try:
        aibeing = AIBeingService.get_aibeing_by_id(aibeing_id)
        
        if not aibeing:
            return jsonify({
                "code": 404,
                "message": f"未找到ID为{aibeing_id}的数字人",
                "data": None
            }), 404
            
        return jsonify({
            "code": 0,
            "data": aibeing,
            "message": "success"
        })
    except Exception as e:
        logger.error(f"获取数字人详情时出错: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"获取数字人详情失败: {str(e)}",
            "data": None
        }), 500

@aibeings_bp.route('/aibeings', methods=['POST'])
@jwt_required()
def create_aibeing():
    """
    创建数字人API
    
    请求体:
    {
        "name": "数字人名称",
        "avatar": "头像URL",
        "description": "描述",
        "type": "类型",
        "status": "状态",
        "config": {}  // 配置信息
    }
    
    返回:
    {
        "code": 0,
        "data": 新创建的数字人对象,
        "message": "success"
    }
    """
    try:
        # 获取当前用户
        current_user = get_jwt_identity()
        
        # 获取请求数据
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name', 'type']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "code": 400,
                    "message": f"缺少必填字段: {field}",
                    "data": None
                }), 400
        
        # 创建数字人
        new_aibeing = AIBeingService.create_aibeing(data)
        
        return jsonify({
            "code": 0,
            "data": new_aibeing,
            "message": "数字人创建成功"
        }), 201
    except Exception as e:
        logger.error(f"创建数字人时出错: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"创建数字人失败: {str(e)}",
            "data": None
        }), 500

@aibeings_bp.route('/aibeings/<int:aibeing_id>', methods=['PUT'])
@jwt_required()
def update_aibeing(aibeing_id):
    """
    更新数字人API
    
    路径参数:
    - aibeing_id: 数字人ID
    
    请求体:
    {
        "name": "数字人名称",
        "avatar": "头像URL",
        "description": "描述",
        "type": "类型",
        "status": "状态",
        "config": {}  // 配置信息
    }
    
    返回:
    {
        "code": 0,
        "data": 更新后的数字人对象,
        "message": "success"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 更新数字人
        updated_aibeing = AIBeingService.update_aibeing(aibeing_id, data)
        
        if not updated_aibeing:
            return jsonify({
                "code": 404,
                "message": f"未找到ID为{aibeing_id}的数字人",
                "data": None
            }), 404
            
        return jsonify({
            "code": 0,
            "data": updated_aibeing,
            "message": "数字人更新成功"
        })
    except Exception as e:
        logger.error(f"更新数字人时出错: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"更新数字人失败: {str(e)}",
            "data": None
        }), 500

@aibeings_bp.route('/aibeings/<int:aibeing_id>', methods=['DELETE'])
@jwt_required()
def delete_aibeing(aibeing_id):
    """
    删除数字人API
    
    路径参数:
    - aibeing_id: 数字人ID
    
    返回:
    {
        "code": 0,
        "data": null,
        "message": "success"
    }
    """
    try:
        # 删除数字人
        success = AIBeingService.delete_aibeing(aibeing_id)
        
        if not success:
            return jsonify({
                "code": 404,
                "message": f"未找到ID为{aibeing_id}的数字人",
                "data": None
            }), 404
            
        return jsonify({
            "code": 0,
            "data": None,
            "message": "数字人删除成功"
        })
    except Exception as e:
        logger.error(f"删除数字人时出错: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"删除数字人失败: {str(e)}",
            "data": None
        }), 500

@aibeings_bp.route('/ppt-demo', methods=['POST'])
def ppt_demo():
    """PPT讲解视频生成演示"""
    try:
        data = request.json
        logger.info(f"接收到PPT讲解请求: {data}")
        
        # 生成任务ID
        task_id = f"task_{uuid.uuid4().hex}"
        
        # 从请求中获取关键信息
        ppt_url = data.get('pptUrl', '')
        output_video_name = data.get('outputVideoName', 'PPT讲解视频')
        scenes = data.get('scenes', [])
        
        # 创建任务信息
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_info = {
            "taskId": task_id,
            "status": "Processing",
            "progress": 0,
            "createdAt": current_time,
            "completedAt": None,
            "pptUrl": ppt_url,
            "outputVideoName": output_video_name,
            "scenesCount": len(scenes),
            "result": None
        }
        
        # 导入任务状态管理模块并添加任务到数据库
        try:
            from app.api.aibeings_task_status import add_task_to_database
            add_task_to_database(task_id, task_info)
            logger.info(f"成功添加任务到数据库: {task_id}")
        except Exception as import_error:
            logger.warning(f"无法添加任务到数据库: {str(import_error)}")
        
        # 返回任务信息
        return jsonify({
            'taskId': task_id,
            'status': 'Processing',
            'message': '任务已提交，正在处理中...'
        })
    except Exception as e:
        logger.error(f"PPT讲解请求处理失败: {str(e)}")
        return jsonify({'error': f'处理失败: {str(e)}'}), 500 