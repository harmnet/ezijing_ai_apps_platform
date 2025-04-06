import os
import uuid
import logging
import oss2
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建蓝图
upload_blueprint = Blueprint('upload', __name__)

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
        bucket_name = os.environ.get('ALIYUN_OSS_BUCKET_NAME', 'virtualman')
        
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

@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传请求"""
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
        
        logger.info(f"文件上传成功: {file_path}, OSS URL: {oss_url}")
        
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
        logger.error(f"文件上传失败: {str(e)}")
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500 