import os
import uuid
import logging
import time
import json
from flask import request, jsonify, current_app, Response
from werkzeug.utils import secure_filename
from . import knowledge_bp
import PyPDF2
import docx
from flask import stream_with_context
from app.services.llm_service import get_api_client

# 设置日志记录
logger = logging.getLogger(__name__)

# 设置日志级别为DEBUG以确保捕获所有日志
logger.setLevel(logging.DEBUG)

# 记录模块加载信息
logger.info("知识库模块开始加载")
UPLOAD_DIR = "/opt/ezijing_ai_apps_platform/backend/uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# 记录模块加载信息
logger.info("知识库模块初始化完成")
logger.info(f"上传目录设置为: {UPLOAD_DIR}")

# 存储上传的文档和其ID的映射
document_store = {}

def allowed_file(filename):
    """检查文件是否为允许的类型"""
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@knowledge_bp.route('/upload', methods=['POST'])
def upload_document():
    """处理文档上传请求"""
    logger.info("收到文档上传请求，路径: /api/knowledge/upload")
    
    if 'file' not in request.files:
        logger.error("未找到文件")
        return jsonify({'success': False, 'message': '未找到文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        logger.error("未选择文件")
        return jsonify({'success': False, 'message': '未选择文件'}), 400
    
    if not allowed_file(file.filename):
        logger.error(f"不支持的文件类型: {file.filename}")
        return jsonify({'success': False, 'message': '只支持PDF文档'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # 安全地获取文件名并生成唯一ID
            filename = secure_filename(file.filename)
            document_id = str(uuid.uuid4())
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            # 构建保存路径
            save_path = os.path.join(UPLOAD_DIR, f"{document_id}.{file_extension}")
            file.save(save_path)
            
            # 解析文档内容
            document_text = extract_text_from_document(save_path, file_extension)
            
            # 存储文档信息
            document_store[document_id] = {
                'filename': filename,
                'path': save_path,
                'content': document_text,
                'upload_time': time.time()
            }
            
            logger.info(f"文档上传成功: {filename}, ID: {document_id}")
            return jsonify({
                'success': True, 
                'message': '文档上传成功',
                'documentId': document_id,
                'filename': filename
            }), 200
        except Exception as e:
            logger.exception(f"文档上传处理失败: {str(e)}")
            return jsonify({'success': False, 'message': f'文档处理失败: {str(e)}'}), 500
    
    return jsonify({'success': False, 'message': '未知错误'}), 400

def extract_text_from_document(file_path, extension):
    """从文档中提取文本内容"""
    try:
        text = ""
        if extension == 'pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
        elif extension in ['doc', 'docx']:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        return text
    except Exception as e:
        logger.exception(f"文档内容提取失败: {str(e)}")
        raise Exception(f"文档内容提取失败: {str(e)}")

@knowledge_bp.route('/chat', methods=['GET'])
def chat_with_document():
    """处理基于文档的问答请求，使用流式响应"""
    document_id = request.args.get('documentId')
    question = request.args.get('question')
    
    if not document_id or not question:
        logger.error("缺少必要的参数: documentId或question")
        return jsonify({'error': '缺少必要的参数'}), 400
    
    if document_id not in document_store:
        logger.error(f"未找到文档ID: {document_id}")
        return jsonify({'error': '未找到对应的文档'}), 404
    
    document_info = document_store[document_id]
    document_content = document_info['content']
    filename = document_info['filename']
    
    # 获取API客户端，默认使用DeepSeek-V3
    model_name = "deepseek-v3-vol"
    client, api_error = get_api_client(model_name)
    
    if not client:
        logger.error(f"获取API客户端失败: {api_error}")
        return jsonify({
            "status": "error",
            "message": api_error.get('error', '获取API客户端失败')
        }), 500
    
    # 构建提示词
    prompt = f"""我需要你扮演一个专业的文档分析助手，基于我提供的文档内容回答问题。

文档标题: {filename}

文档内容:
{document_content[:10000]}  # 为避免超过token限制，截取前10000个字符

请基于上述文档内容回答以下问题，仅使用文档中包含的信息进行回答。如果无法在文档中找到答案，请明确说明。

问题: {question}

回答:"""
    
    # 构建消息
    messages = [
        {"role": "system", "content": "你是一个专业的文档问答助手，负责从文档中提取相关信息以回答用户问题。"},
        {"role": "user", "content": prompt}
    ]
    
    # 使用流式响应
    def generate_response():
        try:
            # 获取正确的模型ID
            from app.services.llm_service import MODEL_CONFIG
            model_config = MODEL_CONFIG.get(model_name)
            real_model_id = model_config["model_id"]
            
            logger.info(f"调用模型API，模型: {model_name}, 实际模型ID: {real_model_id}")
            
            # 使用流式生成
            stream_gen = client.chat_stream(
                model=real_model_id,
                messages=messages,
                temperature=0.3,  # 使用较低的温度，确保回答更准确
                max_tokens=2000
            )
            
            # 发送开始事件
            yield "data: " + json.dumps({"type": "start"}) + "\n\n"
            
            # 逐步输出生成的内容
            for chunk in stream_gen:
                if chunk and "choices" in chunk and chunk["choices"]:
                    delta = chunk["choices"][0].get("delta", {})
                    if "content" in delta and delta["content"]:
                        content = delta["content"]
                        yield "data: " + json.dumps({"content": content}) + "\n\n"
            
            # 发送结束事件
            yield "event: end\ndata: {}\n\n"
            
        except Exception as e:
            logger.exception(f"处理聊天请求失败: {str(e)}")
            error_data = {"error": str(e)}
            yield "data: " + json.dumps(error_data) + "\n\n"
            yield "event: end\ndata: {}\n\n"
    
    response = Response(
        stream_with_context(generate_response()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Content-Type': 'text/event-stream',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )
    
    return response 