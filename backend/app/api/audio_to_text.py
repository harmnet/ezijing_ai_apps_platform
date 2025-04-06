import os
import logging
import tempfile
import json
from flask import Blueprint, request, jsonify, current_app, render_template_string, Response, stream_with_context
from werkzeug.utils import secure_filename
from dashscope import MultiModalConversation

# 创建蓝图
audio_to_text_bp = Blueprint('audio_to_text', __name__)

# 设置日志
logger = logging.getLogger(__name__)

# 允许的音频文件格式
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}

def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML模板，用于测试API
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>音频转文本 - 测试页面</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-container {
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .file-input {
            display: block;
            margin: 15px 0;
        }
        .submit-btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .submit-btn:hover {
            background-color: #45a049;
        }
        .result {
            background-color: #e9f7ef;
            border-left: 5px solid #4CAF50;
            padding: 15px;
            margin-top: 20px;
            display: none;
        }
        .error {
            background-color: #f8d7da;
            border-left: 5px solid #dc3545;
            padding: 15px;
            margin-top: 20px;
            display: none;
        }
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .streaming-result {
            font-family: monospace;
            white-space: pre-wrap;
            padding: 10px;
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 20px;
            min-height: 100px;
            max-height: 300px;
            overflow-y: auto;
        }
        .switch-container {
            display: flex;
            align-items: center;
            margin: 10px 0;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            margin-right: 10px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #2196F3;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
    </style>
</head>
<body>
    <h1>音频转文本</h1>
    <div class="form-container">
        <form id="audioForm" enctype="multipart/form-data">
            <p>请选择要转换的音频文件：</p>
            <input type="file" id="audioFile" name="audio_file" accept=".mp3,.wav,.ogg,.flac,.m4a" class="file-input" required>
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" id="streamingMode" checked>
                    <span class="slider"></span>
                </label>
                <span>流式输出模式</span>
            </div>
            <button type="submit" class="submit-btn">开始转换</button>
        </form>
    </div>
    
    <div id="loading" class="loading">
        <div class="spinner"></div>
        <p>正在处理音频，请稍候...</p>
    </div>
    
    <div id="streamingOutput" class="streaming-result" style="display: none;">
        <p>转录结果：</p>
        <div id="streamingText"></div>
    </div>
    
    <div id="result" class="result">
        <h3>转换结果：</h3>
        <p id="transcription"></p>
    </div>
    
    <div id="error" class="error">
        <h3>错误信息：</h3>
        <p id="errorMessage"></p>
    </div>
    
    <script>
        document.getElementById('audioForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            var formData = new FormData();
            var fileInput = document.getElementById('audioFile');
            var isStreaming = document.getElementById('streamingMode').checked;
            
            if (fileInput.files.length === 0) {
                showError('请选择一个音频文件');
                return;
            }
            
            formData.append('audio_file', fileInput.files[0]);
            formData.append('streaming', isStreaming);
            
            // 显示加载状态
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            if (isStreaming) {
                // 流式输出模式
                document.getElementById('streamingOutput').style.display = 'block';
                document.getElementById('streamingText').textContent = '';
                
                // 使用fetch API的流式处理
                fetch('/api/v1/api/audio-to-text', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('网络响应错误');
                    }
                    
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    let buffer = '';
                    
                    // 开始读取流
                    function readStream() {
                        return reader.read().then(({ done, value }) => {
                            // 流结束
                            if (done) {
                                document.getElementById('loading').style.display = 'none';
                                return;
                            }
                            
                            // 解码收到的数据
                            const text = decoder.decode(value, { stream: true });
                            buffer += text;
                            
                            // 处理收到的数据行
                            const lines = buffer.split('\n');
                            buffer = lines.pop(); // 保留可能不完整的最后一行
                            
                            for (const line of lines) {
                                if (line.trim() === '') continue;
                                
                                try {
                                    if (line.startsWith('data: ')) {
                                        const jsonData = JSON.parse(line.substring(6));
                                        
                                        if (jsonData.code === 200 && jsonData.data && jsonData.data.text) {
                                            const streamingText = document.getElementById('streamingText');
                                            streamingText.textContent = jsonData.data.text;
                                            streamingText.scrollTop = streamingText.scrollHeight;
                                        } else if (jsonData.code !== 200) {
                                            showError(jsonData.message || '转换失败');
                                            document.getElementById('loading').style.display = 'none';
                                            document.getElementById('streamingOutput').style.display = 'none';
                                            return;
                                        }
                                    }
                                } catch (e) {
                                    console.error('解析数据失败:', e, line);
                                }
                            }
                            
                            // 继续读取
                            return readStream();
                        });
                    }
                    
                    return readStream();
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('streamingOutput').style.display = 'none';
                    showError('请求失败: ' + error.message);
                });
            } else {
                // 非流式输出模式（原有的实现）
                fetch('/api/v1/api/audio-to-text', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    
                    if (data.code === 200) {
                        document.getElementById('transcription').textContent = data.data.text;
                        document.getElementById('result').style.display = 'block';
                    } else {
                        showError(data.message || '转换失败');
                    }
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    showError('请求失败: ' + error.message);
                });
            }
        });
        
        function showError(message) {
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('error').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@audio_to_text_bp.route('/audio-to-text-test', methods=['GET'])
def test_page():
    """测试页面"""
    return render_template_string(HTML_TEMPLATE)

@audio_to_text_bp.route('/api/audio-to-text', methods=['POST'])
def convert_audio_to_text():
    """将上传的音频文件转换为文本"""
    try:
        # 检查是否上传了文件
        if 'audio_file' not in request.files:
            return jsonify({'code': 400, 'message': '未找到音频文件'}), 400
        
        file = request.files['audio_file']
        
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({'code': 400, 'message': '未选择文件'}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({'code': 400, 'message': f'不支持的文件类型，请上传 {", ".join(ALLOWED_EXTENSIONS)} 格式的文件'}), 400
        
        # 获取是否使用流式输出
        is_streaming = request.form.get('streaming', 'false').lower() == 'true'
        
        # 创建临时文件保存上传的音频
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp:
            file.save(temp.name)
            temp_path = temp.name
        
        try:
            # 设置API KEY
            os.environ['DASHSCOPE_API_KEY'] = 'sk-1f4bdb8a73ee47809ee148a977c39737'
            
            # 准备请求
            audio_file_path = f"file://{temp_path}"
            messages = [
                {
                    "role": "system", 
                    "content": [{"text": "你是一个将音频转换为文本的助手，请准确转录音频内容。"}]
                },
                {
                    "role": "user",
                    "content": [{"audio": audio_file_path}, {"text": "音频里在说什么?"}],
                }
            ]
            
            if is_streaming:
                # 流式输出模式
                def generate():
                    full_text = ""
                    try:
                        # 调用流式API
                        response = MultiModalConversation.call(
                            model="qwen-audio-turbo-latest", 
                            messages=messages,
                            stream=True,
                            incremental_output=True,
                            result_format="message"
                        )
                        
                        # 返回事件流格式的响应
                        for chunk in response:
                            logger.info(f"Received chunk: {chunk}")
                            try:
                                if chunk.status_code == 200:
                                    # 获取增量文本
                                    try:
                                        content = chunk.output.choices[0].message.content
                                        
                                        if isinstance(content, list) and len(content) > 0:
                                            if hasattr(content[0], 'text'):
                                                new_text = content[0].text
                                            elif isinstance(content[0], dict) and 'text' in content[0]:
                                                new_text = content[0]['text']
                                            else:
                                                new_text = str(content)
                                        elif isinstance(content, dict) and 'text' in content:
                                            new_text = content['text']
                                        else:
                                            new_text = str(content)
                                        
                                        # 如果收到空数组或无效内容，跳过
                                        if new_text == "[]" or not new_text:
                                            continue
                                            
                                        # 累积文本而不是替换
                                        if not full_text:
                                            full_text = new_text
                                        else:
                                            # 避免重复添加相同的内容
                                            if new_text not in full_text:
                                                full_text += new_text
                                        
                                        # 发送事件流数据
                                        data = json.dumps({
                                            'code': 200,
                                            'message': '转换中',
                                            'data': {
                                                'text': full_text
                                            }
                                        })
                                        yield f"data: {data}\n\n"
                                    except Exception as e:
                                        logger.error(f"处理块数据时出错: {str(e)}")
                                        error_data = json.dumps({
                                            'code': 500,
                                            'message': f'处理响应块失败: {str(e)}'
                                        })
                                        yield f"data: {error_data}\n\n"
                                else:
                                    # 处理错误状态
                                    error_data = json.dumps({
                                        'code': chunk.status_code,
                                        'message': chunk.message if hasattr(chunk, 'message') else '处理失败'
                                    })
                                    yield f"data: {error_data}\n\n"
                            except Exception as e:
                                logger.error(f"处理响应块时出错: {str(e)}")
                                error_data = json.dumps({
                                    'code': 500,
                                    'message': f'处理响应块失败: {str(e)}'
                                })
                                yield f"data: {error_data}\n\n"
                        
                        # 如果最终文本为空，提供友好提示
                        if not full_text:
                            full_text = "无法识别音频内容，请检查音频质量或尝试使用其他音频文件。"
                        
                        # 发送完成消息
                        final_data = json.dumps({
                            'code': 200,
                            'message': '转换完成',
                            'data': {
                                'text': full_text
                            }
                        })
                        yield f"data: {final_data}\n\n"
                    except Exception as e:
                        logger.exception("流式处理异常")
                        error_data = json.dumps({
                            'code': 500,
                            'message': f'服务器处理异常: {str(e)}'
                        })
                        yield f"data: {error_data}\n\n"
                    finally:
                        # 删除临时文件
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                
                return Response(
                    stream_with_context(generate()),
                    mimetype="text/event-stream"
                )
            else:
                # 非流式输出模式
                # 调用API
                response = MultiModalConversation.call(model="qwen-audio-turbo-latest", messages=messages)
                
                # 处理响应
                if response.status_code == 200:
                    # 添加详细日志记录，便于调试
                    logger.info(f"DashScope API响应: {response}")
                    
                    # 尝试安全地获取文本内容
                    try:
                        # 首先记录输出结构，便于调试
                        logger.info(f"响应输出: {response.output}")
                        logger.info(f"choices: {response.output.choices}")
                        logger.info(f"message: {response.output.choices[0].message}")
                        logger.info(f"content: {response.output.choices[0].message.content}")
                        
                        # 检查内容是否为列表或字典
                        content = response.output.choices[0].message.content
                        if isinstance(content, list) and len(content) > 0:
                            # 如果是列表，检查第一个元素
                            if hasattr(content[0], 'text'):
                                result = content[0].text
                            elif isinstance(content[0], dict) and 'text' in content[0]:
                                result = content[0]['text']
                            else:
                                # 尝试将整个内容作为结果
                                result = str(content)
                        elif isinstance(content, dict) and 'text' in content:
                            # 如果是字典，直接获取text字段
                            result = content['text']
                        else:
                            # 如果无法解析，则返回原始响应内容的字符串表示
                            result = str(content)
                        
                        return jsonify({
                            'code': 200,
                            'message': '转换成功',
                            'data': {
                                'text': result
                            }
                        })
                    except Exception as e:
                        logger.exception(f"解析API响应失败: {str(e)}")
                        logger.error(f"原始响应: {response}")
                        return jsonify({
                            'code': 500, 
                            'message': f'解析响应失败: {str(e)}',
                            'data': {
                                'original_response': str(response)
                            }
                        }), 500
                else:
                    logger.error(f"DashScope API调用失败: {response.status_code}, {response.message}")
                    return jsonify({'code': 500, 'message': f'API调用失败: {response.message}'}), 500
        
        except Exception as e:
            logger.exception("音频转文本处理异常")
            return jsonify({'code': 500, 'message': f'服务器处理异常: {str(e)}'}), 500
        
        finally:
            # 在非流式模式下删除临时文件（流式模式在生成器结束时删除）
            if not is_streaming and os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except Exception as e:
        logger.exception("音频转文本请求异常")
        return jsonify({'code': 500, 'message': f'服务器请求异常: {str(e)}'}), 500 