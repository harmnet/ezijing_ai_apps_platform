from flask import Blueprint, jsonify, request
from app.utils.logger import logger

template_suit_bp = Blueprint('template_suit', __name__)

@template_suit_bp.route('/template_component/suit/select', methods=['GET'])
def select_template_component():
    """处理模板组件套装选择请求，返回模拟数据"""
    logger.info("接收到模板组件套装选择请求")
    
    # 模拟模板组件数据
    template_components = [
        {
            "id": "101",
            "name": "商务风格模板1",
            "description": "适合商务演示的简洁模板",
            "thumbnail": "https://img.alicdn.com/imgextra/i4/O1CN01DLQsLY1HKlYG8OzZe_!!6000000000739-0-tps-1080-810.jpg",
            "style_id": "1",
            "scene_id": "1",
            "colour_id": "1"
        },
        {
            "id": "102",
            "name": "创意风格模板2",
            "description": "适合创意展示的动态模板",
            "thumbnail": "https://img.alicdn.com/imgextra/i4/O1CN01cBGbQD1hRG6r9rxTd_!!6000000004275-0-tps-1080-810.jpg",
            "style_id": "2",
            "scene_id": "2",
            "colour_id": "2"
        },
        {
            "id": "103",
            "name": "教育风格模板3",
            "description": "适合教育培训的清晰模板",
            "thumbnail": "https://img.alicdn.com/imgextra/i1/O1CN01uZwy9H1WtzCoxA7qW_!!6000000002856-0-tps-1080-810.jpg",
            "style_id": "3",
            "scene_id": "3",
            "colour_id": "3"
        },
        {
            "id": "104",
            "name": "科技风格模板4",
            "description": "适合科技产品的现代模板",
            "thumbnail": "https://img.alicdn.com/imgextra/i2/O1CN01BNQSyj1YWQ27NLZMD_!!6000000003064-0-tps-1080-810.jpg",
            "style_id": "4",
            "scene_id": "1",
            "colour_id": "4"
        },
        {
            "id": "105",
            "name": "简约风格模板5",
            "description": "适合各种场景的极简模板",
            "thumbnail": "https://img.alicdn.com/imgextra/i1/O1CN01DsQebI1qpcnqwXuLJ_!!6000000005537-0-tps-1080-810.jpg",
            "style_id": "1",
            "scene_id": "4",
            "colour_id": "1"
        },
        {
            "id": "106",
            "name": "市场营销模板",
            "description": "适合营销方案的专业模板",
            "thumbnail": "https://img.alicdn.com/imgextra/i3/O1CN01aaO7CU1Gg5THJeD7X_!!6000000000659-0-tps-1080-810.jpg",
            "style_id": "1",
            "scene_id": "2",
            "colour_id": "3"
        },
        {
            "id": "107",
            "name": "年终总结模板",
            "description": "适合年终汇报的精美模板",
            "thumbnail": "https://img.alicdn.com/imgextra/i2/O1CN01bVrFww1YWGx8z2TDc_!!6000000003064-0-tps-1080-810.jpg",
            "style_id": "2",
            "scene_id": "1",
            "colour_id": "2"
        }
    ]
    
    # 模拟响应数据
    response_data = {
        "code": 0,
        "data": template_components,
        "msg": "ok"
    }
    
    logger.info(f"返回模拟模板组件数据: {len(template_components)}个")
    return jsonify(response_data)

@template_suit_bp.route('/template_component/suit/search', methods=['GET'])
def get_template_suits():
    """处理模板套装搜索请求，返回模拟数据"""
    logger.info("接收到模板套装搜索请求")
    
    # 获取查询参数
    query_params = request.args.to_dict()
    
    # 提取分页参数
    page = int(query_params.get('page', 1))
    page_size = int(query_params.get('page_size', 10))
    
    # 模拟模板套装列表
    suits = [
        {
            "id": 81,
            "cover_img": "https://img.alicdn.com/imgextra/i4/O1CN01DLQsLY1HKlYG8OzZe_!!6000000000739-0-tps-1080-810.jpg"
        },
        {
            "id": 80,
            "cover_img": "https://img.alicdn.com/imgextra/i4/O1CN01cBGbQD1hRG6r9rxTd_!!6000000004275-0-tps-1080-810.jpg"
        },
        {
            "id": 79,
            "cover_img": "https://img.alicdn.com/imgextra/i1/O1CN01uZwy9H1WtzCoxA7qW_!!6000000002856-0-tps-1080-810.jpg"
        },
        {
            "id": 78,
            "cover_img": "https://img.alicdn.com/imgextra/i2/O1CN01BNQSyj1YWQ27NLZMD_!!6000000003064-0-tps-1080-810.jpg"
        },
        {
            "id": 77,
            "cover_img": "https://img.alicdn.com/imgextra/i1/O1CN01DsQebI1qpcnqwXuLJ_!!6000000005537-0-tps-1080-810.jpg"
        },
        {
            "id": 76,
            "cover_img": "https://img.alicdn.com/imgextra/i3/O1CN01aaO7CU1Gg5THJeD7X_!!6000000000659-0-tps-1080-810.jpg"
        },
        {
            "id": 75,
            "cover_img": "https://img.alicdn.com/imgextra/i2/O1CN01bVrFww1YWGx8z2TDc_!!6000000003064-0-tps-1080-810.jpg"
        },
        {
            "id": 74,
            "cover_img": "https://img.alicdn.com/imgextra/i3/O1CN01Mn5Z7M1yA8lQ8eGpq_!!6000000006538-0-tps-1080-810.jpg"
        },
        {
            "id": 73,
            "cover_img": "https://img.alicdn.com/imgextra/i3/O1CN01zHQfGG24lqhBHzWoE_!!6000000007432-0-tps-1080-810.jpg"
        },
        {
            "id": 72,
            "cover_img": "https://img.alicdn.com/imgextra/i1/O1CN01qc9Xzh1YGp2NkdNQu_!!6000000003042-0-tps-1080-810.jpg"
        }
    ]
    
    # 计算起始和结束索引
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(suits))
    
    # 裁剪列表
    page_suits = suits[start_idx:end_idx]
    
    # 构造返回数据
    response_data = {
        "code": 0,
        "data": {
            "pagination": {
                "total": len(suits),
                "current_page": page,
                "page_size": page_size
            },
            "list": page_suits
        },
        "msg": "ok"
    }
    
    logger.info(f"返回模板套装列表: {len(page_suits)}条记录, 总记录数: {len(suits)}")
    return jsonify(response_data)

@template_suit_bp.route('/ai/chat/v2/task/', methods=['POST'])
def create_task():
    """处理创建任务请求，返回模拟数据"""
    logger.info("接收到创建任务请求")
    
    # 获取请求数据
    data = request.get_json(silent=True) or {}
    
    # 生成一个随机任务ID
    import time
    import random
    task_id = f"task_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # 模拟任务创建响应
    response_data = {
        "code": 0,
        "data": {
            "task_id": task_id
        },
        "msg": "ok"
    }
    
    logger.info(f"返回模拟任务ID: {task_id}")
    return jsonify(response_data)

@template_suit_bp.route('/generate/data', methods=['POST'])
def generate_outline():
    """处理生成大纲请求，返回模拟数据"""
    logger.info("接收到生成大纲请求")
    
    # 获取请求数据
    data = request.get_json(silent=True) or {}
    task_id = data.get('task_id', '')
    
    # 模拟大纲数据
    outline_data = {
        "content": [
            {
                "title": "第一部分：介绍",
                "content": [
                    "项目背景",
                    "项目目标",
                    "项目范围"
                ]
            },
            {
                "title": "第二部分：分析",
                "content": [
                    "市场分析",
                    "竞争对手分析",
                    "SWOT分析"
                ]
            },
            {
                "title": "第三部分：方案",
                "content": [
                    "实施策略",
                    "时间线",
                    "资源分配"
                ]
            },
            {
                "title": "第四部分：结论",
                "content": [
                    "预期效果",
                    "风险管控",
                    "未来展望"
                ]
            }
        ]
    }
    
    # 模拟响应数据
    response_data = {
        "code": 0,
        "data": outline_data,
        "msg": "ok"
    }
    
    logger.info(f"返回模拟大纲数据，任务ID: {task_id}")
    return jsonify(response_data)

@template_suit_bp.route('/ai/chat/v2/outline/save', methods=['POST'])
def save_outline():
    """处理保存大纲请求，返回模拟数据"""
    logger.info("接收到保存大纲请求")
    
    # 获取请求数据
    data = request.get_json(silent=True) or {}
    task_id = data.get('task_id', '')
    
    # 模拟响应数据
    response_data = {
        "code": 0,
        "data": {
            "task_id": task_id,
            "status": "success"
        },
        "msg": "ok"
    }
    
    logger.info(f"大纲保存成功，任务ID: {task_id}")
    return jsonify(response_data)

@template_suit_bp.route('/design/v2/save', methods=['POST'])
def save_design():
    """处理保存设计请求，返回模拟数据"""
    logger.info("接收到保存设计请求")
    
    # 获取请求数据
    if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
        data = request.form.to_dict()
    elif request.content_type and 'application/json' in request.content_type:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()
    
    task_id = data.get('task_id', '')
    template_id = data.get('template_id', '')
    suit_id = data.get('suit_id', '')
    name = data.get('name', '未命名演示文稿')
    
    logger.info(f"保存设计数据: task_id={task_id}, template_id={template_id}, suit_id={suit_id}, name={name}")
    
    # 生成一个随机作品ID
    import time
    import random
    work_id = f"work_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # 模拟作品生成响应
    response_data = {
        "code": 0,
        "data": {
            "id": work_id,
            "name": name,
            "url": f"https://example.com/preview/{work_id}.html"
        },
        "msg": "ok"
    }
    
    logger.info(f"返回模拟作品ID: {work_id}")
    return jsonify(response_data)

@template_suit_bp.route('/generate/work', methods=['POST'])
def generate_work():
    """处理生成作品请求，返回模拟数据"""
    logger.info("接收到生成作品请求")
    
    # 获取请求数据
    if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
        data = request.form.to_dict()
    elif request.content_type and 'application/json' in request.content_type:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()
    
    logger.info(f"请求内容类型: {request.content_type}")
    logger.info(f"请求体原始数据: {request.get_data(as_text=True)}")
    logger.info(f"请求数据处理后: {data}")
    
    task_id = data.get('task_id', '')
    template_id = data.get('template_id', '')
    suit_id = data.get('suit_id', '')
    name = data.get('name', '未命名演示文稿')
    
    logger.info(f"生成作品数据: task_id={task_id}, template_id={template_id}, suit_id={suit_id}, name={name}")
    
    # 确保task_id存在
    if not task_id:
        logger.error("缺少task_id参数")
        return jsonify({
            "code": 40001,
            "msg": "缺少必要参数task_id",
            "data": None
        }), 400
    
    # 确保template_id存在
    if not template_id and not suit_id:
        logger.error("缺少template_id或suit_id参数")
        return jsonify({
            "code": 40001,
            "msg": "缺少必要参数template_id或suit_id",
            "data": None
        }), 400
    
    # 生成一个随机作品ID
    import time
    import random
    work_id = f"work_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # 模拟作品生成响应
    response_data = {
        "code": 0,
        "data": {
            "id": work_id,
            "name": name,
            "url": f"https://example.com/preview/{work_id}.html"
        },
        "msg": "ok"
    }
    
    logger.info(f"返回模拟作品ID: {work_id}")
    return jsonify(response_data)

@template_suit_bp.route('/download/export/file', methods=['GET'])
def download_file():
    """处理下载文件请求，返回模拟文件数据"""
    logger.info("接收到下载文件请求")
    
    work_id = request.args.get('id', '')
    logger.info(f"下载文件: work_id={work_id}")
    
    # 创建一个简单的PPT文件内容（只是一个示例，实际上应该返回真实的PPTX文件）
    from flask import Response
    import io
    
    # 创建一个简单的二进制数据作为示例
    dummy_data = io.BytesIO()
    dummy_data.write(b"This is a dummy PPTX file content")
    dummy_data.seek(0)
    
    return Response(
        dummy_data,
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment;filename=presentation_{work_id}.pptx"}
    )

 