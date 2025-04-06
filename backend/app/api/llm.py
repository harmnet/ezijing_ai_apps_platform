from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import llm_service
from app.services.file_service import extract_text_from_file, get_token_limit_for_model
import os

# 创建大模型API蓝图
llm_blueprint = Blueprint('llm', __name__)

@llm_blueprint.route('/models', methods=['GET'])
def get_models():
    """
    获取可用的大模型列表
    ---
    responses:
      200:
        description: 返回可用的大模型列表
    """
    models = llm_service.get_available_models()
    return jsonify({
        "status": "success",
        "data": models
    }), 200

@llm_blueprint.route('/file_chat', methods=['POST'])
def file_chat():
    """
    上传文件并与大模型对话
    ---
    parameters:
      - name: file
        in: formData
        type: file
        description: 要上传的文件（支持PDF, Word, Excel等格式）
      - name: model
        in: formData
        type: string
        description: 模型名称
      - name: prompt
        in: formData
        type: string
        description: 用户提示词
      - name: return_thinking
        in: formData
        type: boolean
        description: 是否返回思考过程
    responses:
      200:
        description: 返回模型回复内容
      400:
        description: 请求参数错误或文件格式不支持
      413:
        description: 文件内容过长，超出模型上下文限制
    """
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "未上传文件"
        }), 400
        
    file = request.files['file']
    
    # 检查文件是否有效
    if file.filename == '':
        return jsonify({
            "status": "error",
            "message": "文件名为空"
        }), 400
    
    # 获取其他参数
    model = request.form.get('model')
    prompt = request.form.get('prompt', '')
    return_thinking = request.form.get('return_thinking') == 'true'
    
    if not model:
        return jsonify({
            "status": "error",
            "message": "缺少model参数"
        }), 400
    
    # 保存文件到临时目录
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)
    
    try:
        # 从文件中提取文本
        extracted_text = extract_text_from_file(file_path)
        
        # 清理临时文件
        os.remove(file_path)
        
        if not extracted_text:
            return jsonify({
                "status": "error",
                "message": "无法从文件中提取文本"
            }), 400
        
        # 检查文本长度是否超出模型限制
        token_limit = get_token_limit_for_model(model)
        
        # 构建提示词（用户输入 + 文件内容）
        if prompt:
            full_prompt = f"{prompt}\n\n附件内容：\n{extracted_text}"
        else:
            full_prompt = f"请帮我分析以下文件内容：\n\n{extracted_text}"
        
        # 估算token数量（简单估算：每个汉字约1.5个token，每个英文单词约1个token）
        token_estimate = len(full_prompt) * 0.75  # 简单估算
        
        # 如果预估超过模型限制，则返回错误
        if token_estimate > token_limit * 0.9:  # 留10%的余量
            return jsonify({
                "status": "error",
                "message": f"文件内容过长，估计需要{int(token_estimate)}个token，超过模型支持的{token_limit}个token限制"
            }), 413
        
        # 构建聊天消息
        messages = [
            {"role": "system", "content": "你是一位专业的文档分析助手，请根据用户提供的文档内容进行分析和回答。"},
            {"role": "user", "content": full_prompt}
        ]
        
        # 调用大模型
        response = llm_service.chat_completion(
            model_name=model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        # 检查是否有错误
        if "error" in response:
            error_info = response["error"]
            error_message = "调用大模型API失败"
            
            # 检查error是否是字典对象
            if isinstance(error_info, dict) and "message" in error_info:
                error_message = error_info["message"]
            elif isinstance(error_info, str):
                error_message = error_info
            
            return jsonify({
                "status": "error",
                "message": error_message,
                "error": error_info
            }), 400
        
        # 如果请求返回思考过程，则在响应中包含思考过程
        if return_thinking and "thinking" not in response:
            response["thinking"] = [
                "分析文件内容...",
                "识别关键信息...",
                "组织回复结构...",
                "生成完整回答..."
            ]
        
        return jsonify({
            "status": "success",
            "data": response
        }), 200
    
    except Exception as e:
        # 确保临时文件被删除
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({
            "status": "error",
            "message": f"处理文件时出错: {str(e)}"
        }), 500

@llm_blueprint.route('/chat', methods=['POST'])
def chat():
    """
    与大模型进行对话
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            model:
              type: string
              description: 模型名称
            messages:
              type: array
              description: 对话历史
            temperature:
              type: number
              description: 温度参数
            max_tokens:
              type: integer
              description: 最大生成token数
    responses:
      200:
        description: 返回模型回复内容
      400:
        description: 请求参数错误
      500:
        description: 服务器内部错误
    """
    # 获取请求数据
    data = request.get_json()
    
    # 检查必要参数
    if not data:
        return jsonify({
            "status": "error",
            "message": "请求体不能为空"
        }), 400
        
    model = data.get('model')
    messages = data.get('messages')
    
    if not model:
        return jsonify({
            "status": "error",
            "message": "缺少model参数"
        }), 400
        
    if not messages or not isinstance(messages, list):
        return jsonify({
            "status": "error",
            "message": "缺少messages参数或格式错误"
        }), 400
    
    # 可选参数
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 2000)
    top_p = data.get('top_p', 1.0)
    frequency_penalty = data.get('frequency_penalty', 0.0)
    presence_penalty = data.get('presence_penalty', 0.0)
    stop = data.get('stop', None)
    
    # 调用大模型API
    print(f"\n=== 调用大模型API ({model}) ===")
    print(f"发送消息数: {len(messages)}")
    print(f"第一条消息: {messages[0]['role']} - {messages[0]['content'][:100]}...")
    
    api_client, model_info = llm_service.get_api_client(model)
    
    if api_client is None:
        return jsonify({
            "status": "error",
            "message": "无法创建API客户端，请检查模型名称和API密钥",
            "error": model_info.get("error", "未知错误")
        }), 400
    
    # 调用聊天接口
    response = api_client.chat_completion(
        messages=messages,
        model_id=model_info["model_id"],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    
    # 增加详细的响应日志
    print("\n=== 详细API响应日志 ===")
    print(f"响应类型: {type(response)}")
    print(f"响应字段: {list(response.keys()) if isinstance(response, dict) else '非字典类型'}")
    
    if isinstance(response, dict):
        if "choices" in response:
            print(f"choices数量: {len(response['choices'])}")
            if response['choices']:
                first_choice = response['choices'][0]
                print(f"第一个choice字段: {list(first_choice.keys()) if isinstance(first_choice, dict) else '非字典类型'}")
                
                if isinstance(first_choice, dict) and "message" in first_choice:
                    message = first_choice["message"]
                    print(f"消息角色: {message.get('role', 'unknown')}")
                    content = message.get('content', '')
                    print(f"消息内容 (前200字符): {content[:200]}...")
                    print(f"消息内容长度: {len(content)} 字符")
        
        if "error" in response:
            print(f"错误信息: {response['error']}")
    
    # 检查是否有错误
    if "error" in response:
        error_info = response["error"]
        error_message = "调用大模型API失败"
        
        # 检查error是否是字典对象
        if isinstance(error_info, dict) and "message" in error_info:
            error_message = error_info["message"]
        elif isinstance(error_info, str):
            error_message = error_info
            
        return jsonify({
            "status": "error",
            "message": error_message,
            "error": error_info
        }), 400
    
    return jsonify({
        "status": "success",
        "data": response
    }), 200 