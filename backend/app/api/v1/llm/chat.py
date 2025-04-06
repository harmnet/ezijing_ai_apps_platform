@bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        print("\n=== 收到新的聊天请求 ===")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if not data or 'messages' not in data:
            print("错误：请求数据格式不正确")
            return jsonify({'error': 'Invalid request format'}), 400
            
        messages = data['messages']
        print(f"\n=== 处理消息 ===")
        print(f"消息数量: {len(messages)}")
        for i, msg in enumerate(messages):
            print(f"消息 {i+1}: {msg.get('role', 'unknown')} - {msg.get('content', '')[:100]}...")
        
        # 获取模型ID，如果没有提供则使用默认值
        model_id = data.get('model', 'skylark2-pro')
        print(f"\n=== 使用模型 ===")
        print(f"模型ID: {model_id}")
        
        # 获取API密钥
        api_key = os.getenv('VOLCANO_API_KEY')
        if not api_key:
            print("错误：未找到火山引擎API密钥")
            return jsonify({'error': 'API key not configured'}), 500
        print(f"API密钥: {api_key[:8]}...")
        
        # 初始化API
        print("\n=== 初始化API ===")
        print("baseURL: https://ark.cn-beijing.volces.com/api/v3")
        api = VolcengineAPI(api_key)
        
        # 调用API
        print("\n=== 调用API ===")
        print("开始发送请求到火山引擎...")
        response = api.chat(messages, model_id)
        print(f"API响应状态码: {response.status_code}")
        print(f"API响应头: {dict(response.headers)}")
        print(f"API响应内容: {response.text[:500]}...")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print("\n=== 解析响应数据 ===")
                print(f"响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                # 提取内容
                content = None
                if isinstance(response_data, dict):
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        content = response_data['choices'][0].get('message', {}).get('content')
                    elif 'data' in response_data:
                        content = response_data['data']
                elif isinstance(response_data, str):
                    content = response_data
                
                print(f"\n=== 提取的内容 ===")
                print(f"内容: {content[:200] if content else 'None'}")
                
                if content:
                    return jsonify({
                        'choices': [{
                            'message': {
                                'role': 'assistant',
                                'content': content
                            }
                        }]
                    })
                else:
                    print("错误：无法从响应中提取内容")
                    return jsonify({'error': 'No content in response'}), 500
                    
            except json.JSONDecodeError as e:
                print(f"错误：解析响应JSON失败 - {str(e)}")
                print(f"原始响应: {response.text[:500]}")
                return jsonify({'error': 'Invalid JSON response'}), 500
        else:
            print(f"错误：API请求失败，状态码: {response.status_code}")
            print(f"错误响应: {response.text[:500]}")
            return jsonify({'error': f'API request failed with status {response.status_code}'}), response.status_code
            
    except Exception as e:
        print(f"\n=== 发生异常 ===")
        print(f"异常类型: {type(e).__name__}")
        print(f"异常信息: {str(e)}")
        import traceback
        print(f"堆栈跟踪:\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500 