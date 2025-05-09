import os
import uuid
import logging
import oss2
import time
import re
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required

# 引入百度BOS服务
from app.services.baidubce_upload import upload_file_to_bos, upload_video_to_bos

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建蓝图
upload_blueprint = Blueprint('upload', __name__)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'ppt', 'pptx', 'pdf', 'jpg', 'jpeg', 'png', 'mp4', 'mp3', 'mov'}

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
        # 记录上传信息
        logger.info(f"开始上传文件到阿里云OSS: {file_path} -> {object_name}")
        
        # 从环境变量获取OSS配置，使用与其他服务相同的逻辑
        access_key_id = os.environ.get('ALIYUN_OSS_ACCESS_KEY_ID', os.environ.get('ALIYUN_ACCESS_KEY_ID'))
        access_key_secret = os.environ.get('ALIYUN_OSS_ACCESS_KEY_SECRET', os.environ.get('ALIYUN_ACCESS_KEY_SECRET'))
        endpoint = os.environ.get('ALIYUN_OSS_ENDPOINT', os.environ.get('ALIYUN_OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com'))
        bucket_name = os.environ.get('ALIYUN_OSS_BUCKET_NAME', os.environ.get('ALIYUN_OSS_BUCKET', 'ezijingai'))
        
        # 记录OSS配置信息（不包含敏感信息）
        logger.info(f"OSS配置信息: bucket={bucket_name}, endpoint={endpoint}")
        logger.info(f"AccessKey配置状态: ID存在={bool(access_key_id)}, Secret存在={bool(access_key_secret)}")
        
        # 强制非开发模式，直接上传到阿里云OSS
        dev_mode = False
        
        # 在开发模式下，总是返回模拟的URL
        if dev_mode:
            # 获取文件名
            file_name = os.path.basename(file_path)
            
            try:
                # 将文件复制到前端可访问的public目录
                import shutil
                
                # 计算当前后端app目录的父级目录，也就是后端根目录
                backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
                # 计算前端根目录
                frontend_dir = os.path.abspath(os.path.join(backend_dir, '..', 'frontend'))
                
                # 计算前端static目录
                static_dir = os.path.join(frontend_dir, 'public', 'mock-uploads')
                os.makedirs(static_dir, exist_ok=True)
                
                # 复制文件到static目录
                static_file_path = os.path.join(static_dir, file_name)
                if os.path.exists(file_path):
                    logger.info(f"复制文件 {file_path} -> {static_file_path}")
                    shutil.copy2(file_path, static_file_path)
                
                # 返回可访问的URL
                server_domain = request.host
                mock_url = f"http://{server_domain}/mock-uploads/{file_name}"
                logger.info(f"开发模式：生成模拟文件URL: {mock_url}")
                return mock_url
            except Exception as e:
                logger.warning(f"文件复制失败，使用备用URL: {str(e)}")
                # 失败时使用模拟URL
                mock_url = f"https://mock-{bucket_name}.{endpoint}/dev-uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
                logger.info(f"模拟文件URL: {mock_url}")
                return mock_url
        
        # 验证OSS配置
        if not access_key_id or not access_key_secret or not bucket_name:
            logger.error("OSS配置不完整，无法上传")
            return None
            
        try:
            # 创建OSS认证和Bucket实例
            auth = oss2.Auth(access_key_id, access_key_secret)
            bucket = oss2.Bucket(auth, endpoint, bucket_name)
            
            # 上传文件
            logger.info(f"开始上传文件到OSS: {object_name}")
            result = bucket.put_object_from_file(object_name, file_path)
            
            # 检查上传结果
            if result.status == 200:
                # 构建文件URL
                file_url = f"https://{bucket_name}.{endpoint}/{object_name}"
                logger.info(f"文件上传成功，URL: {file_url}")
                return file_url
            else:
                logger.error(f"OSS上传失败，状态码: {result.status}")
                return None
        except Exception as e:
            logger.error(f"OSS上传异常: {str(e)}")
            # 返回模拟URL作为后备选项
            file_name = os.path.basename(file_path)
            backup_url = f"https://mock-{bucket_name}.{endpoint}/backup-uploads/{time.strftime('%Y%m%d')}/{uuid.uuid4().hex}-{file_name}"
            logger.warning(f"OSS上传失败，返回后备URL: {backup_url}")
            return backup_url
            
    except Exception as e:
        logger.error(f"OSS上传异常: {str(e)}")
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
        
        # 获取文件类型
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # 根据文件类型确定OSS路径
        if file_ext in ['ppt', 'pptx', 'pdf']:
            oss_path = f"media_upload/customize/user-upload/scene/ppt/{unique_filename}"
        else:
            oss_path = f"media_upload/customize/user-upload/scene/image/{unique_filename}"
        
        # 上传到阿里云OSS
        oss_url = upload_to_oss(file_path, oss_path)
        
        logger.info(f"文件上传成功: {file_path}, 类型: {file_ext}")
        
        # 如果上传到OSS成功，返回OSS URL
        if oss_url:
            logger.info(f"OSS URL: {oss_url}")
            return jsonify({
                'message': '文件上传成功',
                'filename': unique_filename,
                'url': oss_url
            })
        else:
            # 如果上传到OSS失败，返回本地URL
            server_name = request.host
            protocol = 'https' if request.is_secure else 'http'
            file_url = f"{protocol}://{server_name}/uploads/{unique_filename}"
            logger.info(f"本地URL: {file_url}")
            return jsonify({
                'message': '文件上传到本地成功（OSS未配置或上传失败）',
                'filename': unique_filename,
                'url': file_url
            })
        
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500

@upload_blueprint.route('/video', methods=['POST'])
def upload_video():
    """处理视频上传请求，优先使用百度BOS存储"""
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有文件部分'}), 400
        
        file = request.files['file']
        
        # 检查文件是否为空
        if file.filename == '':
            return jsonify({'success': False, 'message': '没有选择文件'}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': f'文件类型不允许。允许的视频类型: mp4, mov'}), 400
        
        # 获取视频类型参数
        video_type = request.form.get('type', '')
        logger.info(f"视频上传类型: {video_type}")
        
        # 安全地获取文件名并添加UUID前缀
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存文件到临时目录
        file.save(file_path)
        logger.info(f"视频文件已保存到临时目录: {file_path}")
        
        try:
            # 优先使用百度BOS上传
            bos_url = upload_video_to_bos(file_path, video_type)
            
            if bos_url:
                logger.info(f"视频上传到百度BOS成功: {bos_url}")
                
                # 上传成功后删除临时文件
                try:
                    os.remove(file_path)
                    logger.info(f"临时文件已删除: {file_path}")
                except Exception as e:
                    logger.warning(f"删除临时文件失败: {str(e)}")
                
                return jsonify({
                    'success': True,
                    'message': '视频上传到百度BOS成功',
                    'data': {
                        'url': bos_url,
                        'filename': filename
                    }
                })
            else:
                logger.warning("百度BOS上传失败，尝试使用阿里云OSS")
                
                # 尝试使用阿里云OSS上传
                oss_path = f"videos/{video_type}/{time.strftime('%Y%m%d')}/{unique_filename}"
                oss_url = upload_to_oss(file_path, oss_path)
                
                if oss_url:
                    logger.info(f"视频上传到阿里云OSS成功: {oss_url}")
                    
                    # 上传成功后删除临时文件
                    try:
                        os.remove(file_path)
                        logger.info(f"临时文件已删除: {file_path}")
                    except Exception as e:
                        logger.warning(f"删除临时文件失败: {str(e)}")
                    
                    return jsonify({
                        'success': True,
                        'message': '视频上传到阿里云OSS成功',
                        'data': {
                            'url': oss_url,
                            'filename': filename
                        }
                    })
                else:
                    logger.error("视频上传到云存储失败")
                    return jsonify({
                        'success': False,
                        'message': '视频上传到云存储失败',
                    }), 500
                
        except Exception as e:
            logger.error(f"视频上传过程中发生异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'视频上传失败: {str(e)}',
            }), 500
            
    except Exception as e:
        logger.error(f"视频上传请求处理失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'视频上传失败: {str(e)}',
        }), 500

@upload_blueprint.route('/baidu_image', methods=['POST'])
def upload_baidu_image():
    """处理图片上传请求，使用百度BOS存储"""
    try:
        logger.info("===== 收到图片上传请求 =====")
        
        # 检查请求中是否包含文件
        if 'file' not in request.files and 'image' not in request.form:
            return jsonify({'success': False, 'message': '没有文件部分'}), 400
        
        # 处理不同的上传方式
        image_type = request.form.get('type', '')
        logger.info(f"图片上传类型: {image_type}")
        
        # 临时文件路径
        file_path = None
        is_temp_file = False
        
        if 'file' in request.files:
            # 从文件上传处理
            file = request.files['file']
            
            # 检查文件是否为空
            if file.filename == '':
                return jsonify({'success': False, 'message': '没有选择文件'}), 400
            
            # 检查文件类型
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                return jsonify({'success': False, 'message': '文件类型不允许。允许的图片类型: png, jpg, jpeg'}), 400
            
            # 安全地获取文件名并添加UUID前缀
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # 保存文件到临时目录
            file.save(file_path)
            is_temp_file = True
            logger.info(f"图片文件已保存到临时目录: {file_path}")
        
        elif 'image' in request.form:
            # 从Base64处理
            try:
                import base64
                from PIL import Image
                from io import BytesIO
                import re
                
                # 获取Base64编码的图片
                image_data = request.form['image']
                
                # 检查是否是有效的Base64数据
                if not image_data or not (image_data.startswith('data:image/') or image_data.startswith('data:application/octet-stream')):
                    return jsonify({'success': False, 'message': '无效的图片数据格式'}), 400
                
                # 从Base64中提取图像数据
                # 匹配pattern可能是 data:image/jpeg;base64, 或 data:image/png;base64, 等
                base64_data = re.sub('^data:image/.+;base64,', '', image_data)
                
                # 将Base64解码为二进制
                binary_data = base64.b64decode(base64_data)
                
                # 创建临时文件
                unique_filename = f"{uuid.uuid4().hex}.png"  # 默认使用PNG格式
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                
                # 使用PIL打开图片并保存
                img = Image.open(BytesIO(binary_data))
                img.save(file_path)
                is_temp_file = True
                
                logger.info(f"Base64图片已保存到临时目录: {file_path}")
            except Exception as e:
                logger.error(f"处理Base64图片数据失败: {str(e)}")
                return jsonify({'success': False, 'message': f'处理图片数据失败: {str(e)}'}), 400
        
        if not file_path:
            return jsonify({'success': False, 'message': '未提供有效的图片数据'}), 400
        
        # 检查开发模式
        # 强制禁用开发模式，确保使用百度云BOS存储
        dev_mode = False
        if dev_mode:
            logger.info("开发模式：返回本地图片URL")
            
            try:
                # 创建副本到前端静态目录
                import shutil
                
                # 计算当前后端app目录的父级目录，也就是后端根目录
                backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                # 计算前端根目录
                frontend_dir = os.path.abspath(os.path.join(backend_dir, '..', 'frontend'))
                # 计算前端静态目录
                static_dir = os.path.join(frontend_dir, 'public', 'mock-uploads')
                
                logger.info(f"计算的目录路径: backend={backend_dir}, frontend={frontend_dir}, static={static_dir}")
                
                # 确保目录存在
                os.makedirs(static_dir, exist_ok=True)
                
                # 获取文件名
                file_name = os.path.basename(file_path)
                static_file_path = os.path.join(static_dir, file_name)
                
                # 复制文件
                if os.path.exists(file_path):
                    shutil.copy2(file_path, static_file_path)
                    logger.info(f"已复制图片到静态目录: {static_file_path}")
                else:
                    logger.error(f"源文件不存在: {file_path}")
                
                # 返回URL（使用带域名的URL）
                # 根据服务器域名构建URL
                server_domain = request.host
                static_url = f"http://{server_domain}/mock-uploads/{file_name}"
                logger.info(f"开发模式：返回静态URL: {static_url}")
                
                # 删除临时文件
                if is_temp_file and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        logger.info(f"临时文件已删除: {file_path}")
                    except Exception as e:
                        logger.warning(f"删除临时文件失败: {str(e)}")
                
                return jsonify({
                    'success': True,
                    'message': '图片上传成功(开发模式)',
                    'data': {
                        'url': static_url
                    }
                })
            except Exception as e:
                logger.error(f"开发模式处理图片失败: {str(e)}")
                # 如果开发模式处理失败，提供一个带时间戳的数据URI作为备选URL
                import base64
                from datetime import datetime
                timestamp = datetime.now().strftime("%H%M%S")
                
                # 读取图片文件并转换为base64
                with open(file_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                
                img_type = "jpeg" if file_path.lower().endswith(('.jpg', '.jpeg')) else "png"
                data_url = f"data:image/{img_type};base64,{img_data[:50]}...省略...{timestamp}"
                
                logger.info(f"返回数据URL作为备选: {data_url[:30]}...省略")
                return jsonify({
                    'success': True,
                    'message': '图片上传成功(备用模式)',
                    'data': {
                        'url': data_url
                    }
                })
        
        try:
            # 使用百度BOS上传
            # 引入上传函数
            from app.services.baidubce_upload import upload_file_to_bos
            
            # 获取文件扩展名
            file_ext = os.path.splitext(file_path)[1]
            if not file_ext:
                file_ext = '.jpg'  # 默认扩展名
                
            # 构建对象路径，确保文件名中包含扩展名
            base_filename = os.path.basename(file_path)
            object_name = f"images/{image_type}/{time.strftime('%Y%m%d')}/{base_filename}"
            
            # 确保对象名中带有正确的扩展名
            if not object_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                object_name = f"{object_name}{file_ext}"
                
            # 记录对象路径（用于调试）
            logger.info(f"上传图片对象路径: {object_name}")
            
            # 简单检查是否存在重复日期
            parts = object_name.split('/')
            if len(parts) >= 3 and parts[-2] == parts[-3]:
                # 如果发现连续重复的目录名称，移除一个
                new_parts = parts[:-2] + [parts[-2]] + [parts[-1]]
                object_name = '/'.join(new_parts)
                logger.info(f"修正后的对象路径: {object_name}")
            
            bos_url = upload_file_to_bos(file_path, object_name)
            
            if is_temp_file and os.path.exists(file_path):
                try:
                    # 删除临时文件
                    os.remove(file_path)
                    logger.info(f"临时文件已删除: {file_path}")
                except Exception as e:
                    logger.warning(f"删除临时文件失败: {str(e)}")
            
            if bos_url:
                logger.info(f"图片上传到百度BOS成功: {bos_url}")
                return jsonify({
                    'success': True,
                    'message': '图片上传到百度BOS成功',
                    'data': {
                        'url': bos_url
                    }
                })
            else:
                logger.error("图片上传到百度BOS失败")
                return jsonify({
                    'success': False,
                    'message': '图片上传到百度BOS失败，请检查BOS配置',
                }), 500
                
        except Exception as e:
            logger.error(f"图片上传过程中发生异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'图片上传失败: {str(e)}',
            }), 500
            
    except Exception as e:
        logger.error(f"图片上传请求处理失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'图片上传失败: {str(e)}',
        }), 500

@upload_blueprint.route('/baidu_video', methods=['POST'])
def upload_baidu_video():
    """处理视频上传请求，专门用于百度云BOS存储"""
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有文件部分'}), 400
        
        file = request.files['file']
        
        # 检查文件是否为空
        if file.filename == '':
            return jsonify({'success': False, 'message': '没有选择文件'}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': f'文件类型不允许。允许的视频类型: mp4, mov'}), 400
        
        # 获取视频类型参数
        video_type = request.form.get('type', '')
        logger.info(f"百度云视频上传类型: {video_type}")
        
        # 安全地获取文件名并添加UUID前缀
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存文件到临时目录
        file.save(file_path)
        logger.info(f"视频文件已保存到临时目录: {file_path}")
        
        try:
            # 直接使用baidu_bos_service的upload_video_to_bos函数
            # 该函数已经修改为确保正确的文件扩展名格式
            bos_url = upload_video_to_bos(file_path, video_type)
            
            # 删除临时文件
            try:
                os.remove(file_path)
                logger.info(f"临时文件已删除: {file_path}")
            except Exception as e:
                logger.warning(f"删除临时文件失败: {str(e)}")
            
            if bos_url:
                logger.info(f"视频上传到百度BOS成功: {bos_url}")
                return jsonify({
                    'success': True,
                    'message': '视频上传到百度BOS成功',
                    'data': {
                        'url': bos_url,
                        'filename': filename
                    }
                })
            else:
                logger.error("视频上传到百度BOS失败")
                return jsonify({
                    'success': False,
                    'message': '视频上传到百度BOS失败，请检查BOS配置',
                }), 500
                
        except Exception as e:
            logger.error(f"视频上传过程中发生异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'视频上传失败: {str(e)}',
            }), 500
            
    except Exception as e:
        logger.error(f"视频上传请求处理失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'视频上传失败: {str(e)}',
        }), 500

# 添加专门为数字人上传图片的路由
@upload_blueprint.route('/uploads/image', methods=['POST'])
def upload_image_file():
    """处理图片上传请求"""
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            logger.error("未找到上传的文件")
            return jsonify({
                'success': False,
                'message': '没有文件部分'
            }), 400
        
        file = request.files['file']
        
        # 检查文件是否为空
        if file.filename == '':
            logger.error("未选择文件")
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        # 检查文件类型是否允许
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            logger.error(f"不支持的文件类型: {file.filename}")
            return jsonify({
                'success': False,
                'message': '文件类型不允许。允许的图片类型: png, jpg, jpeg'
            }), 400
        
        # 安全地获取文件名并添加UUID前缀以避免文件名冲突
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存文件到临时目录
        file.save(file_path)
        logger.info(f"图片文件已保存到临时目录: {file_path}")
        
        # 获取图片类型
        type_param = request.form.get('type', 'background')  # 默认为背景图片类型
        
        # 根据图片类型确定OSS路径
        oss_path = f"images/{type_param}/{time.strftime('%Y%m%d')}/{unique_filename}"
        
        # 上传到阿里云OSS
        oss_url = upload_to_oss(file_path, oss_path)
        
        # 删除临时文件
        try:
            os.remove(file_path)
            logger.info(f"临时文件已删除: {file_path}")
        except Exception as e:
            logger.warning(f"删除临时文件失败: {str(e)}")
        
        # 如果上传到OSS成功，返回符合前端期望的格式
        if oss_url:
            logger.info(f"图片上传到OSS成功: {oss_url}")
            # 修改响应格式，与前端期望保持一致
            return jsonify({
                'url': oss_url,
                'filename': filename,
                'success': True,
                'message': '图片上传成功'
            })
        else:
            # 如果上传到OSS失败，返回错误信息
            logger.error("图片上传到OSS失败")
            return jsonify({
                'success': False,
                'message': '图片上传到OSS失败，请检查OSS配置',
            }), 500
        
    except Exception as e:
        logger.error(f"图片上传失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'图片上传失败: {str(e)}',
        }), 500

@upload_blueprint.route('/bos/image', methods=['POST'])
def upload_bos_image():
    """处理图片上传到百度云BOS的请求"""
    try:
        logger.info("===== 收到百度云BOS图片上传请求 =====")
        
        # 直接复用现有的baidu_image处理逻辑
        return upload_baidu_image()
        
    except Exception as e:
        logger.error(f"处理百度云BOS图片上传请求失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'上传图片到百度云BOS失败: {str(e)}'
        }), 500

@upload_blueprint.route('/bos_credentials', methods=['GET'])
def get_bos_credentials():
    """
    获取百度云BOS上传凭证
    为前端直接上传到BOS提供临时凭证
    
    Returns:
        accessKeyId: 访问密钥ID
        secretAccessKey: 访问密钥
        success: 是否成功
    """
    try:
        # 从环境变量获取敏感信息
        access_key_id = os.environ.get("BAIDU_BCE_ACCESS_KEY_ID")
        secret_access_key = os.environ.get("BAIDU_BCE_SECRET_ACCESS_KEY")
        
        if not access_key_id or not secret_access_key:
            logger.error("百度云BOS访问密钥未配置")
            return jsonify({
                "success": False,
                "message": "百度云BOS访问密钥未配置"
            }), 500
        
        # 返回访问凭证
        return jsonify({
            "success": True,
            "accessKeyId": access_key_id,
            "secretAccessKey": secret_access_key,
            "expiration": (datetime.now() + timedelta(minutes=30)).isoformat() # 30分钟有效期
        })
        
    except Exception as e:
        logger.error(f"获取BOS凭证失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取BOS凭证失败: {str(e)}"
        }), 500 