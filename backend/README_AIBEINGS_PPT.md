# 小冰AI Beings数字人PPT讲解功能

本模块提供了对小冰AI Beings数字人PPT讲解视频功能的封装，可以通过简单的API调用生成数字人PPT讲解视频。

## 功能特点

- 支持上传PPT/PPTX文件，自动生成数字人讲解视频
- 支持自定义讲解文案（可选，默认自动从PPT备注生成）
- 支持选择不同的数字人形象和姿势
- 支持设置数字人位置（左、中、右）
- 支持自定义TTS语音参数（音量、语速、音调）
- 支持自定义字幕样式（大小、颜色、位置）
- 支持设置视频分辨率（720p/1080p）
- 支持任务进度查询和结果获取

## 使用步骤

### 1. 初始化环境

确保已安装所有依赖：

```bash
pip install -r requirements.txt
```

### 2. 导入模块

```python
from app.services.aibeings_ppt_video import (
    create_ppt_video_task, 
    query_ppt_video_task,
    get_digital_humans, 
    get_digital_human_postures,
    DEFAULT_VIRTUAL_HUMANS
)
```

### 3. 创建PPT讲解视频任务

```python
# 创建视频任务
result = create_ppt_video_task(
    ppt_file_path='/path/to/your/presentation.pptx',  # PPT文件路径
    text_script='这是一段自定义讲解文案，将由数字人进行讲解',  # 可选，不提供则自动生成
    virtual_human_id=DEFAULT_VIRTUAL_HUMANS["default"]["virtualHumanId"],  # 数字人ID
    virtual_human_posture_id=DEFAULT_VIRTUAL_HUMANS["default"]["postures"]["right"],  # 数字人姿势ID
    title='我的PPT讲解视频',  # 视频标题
    resolution='1080p',  # 视频分辨率：720p或1080p
    caption_config={  # 字幕配置
        "topCenter": True,
        "attributes": {
            "fontColor": "#ff3c3c",
            "fontSize": 40,
            "bold": True
        }
    },
    tts_config={  # TTS语音配置
        "voiceId": "101-master-ugdr",
        "rate": 1,
        "pitch": 1,
        "volume": 50
    },
    single_page_seconds=5,  # 单页PPT显示时间（秒）
    virtual_human_position="right"  # 数字人位置：left、center、right
)

# 获取任务ID
task_id = result['task_id']
print(f"任务创建成功，任务ID: {task_id}")
```

### 4. 查询任务状态

```python
# 查询任务状态
status_result = query_ppt_video_task(task_id)

# 输出状态信息
print(f"任务状态: {status_result['status']}")
print(f"处理进度: {status_result['progress']}%")

# 如果任务完成，获取视频URL
if status_result['status'] == 'success' and 'video_url' in status_result:
    print(f"视频URL: {status_result['video_url']}")
```

## API说明

### 1. 创建PPT讲解视频任务

```python
create_ppt_video_task(
    ppt_file_path, 
    text_script=None, 
    virtual_human_id=None,
    virtual_human_posture_id=None, 
    title="PPT讲解视频",
    resolution="1080p",
    caption_config=None,
    tts_config=None,
    single_page_seconds=5,
    virtual_human_position="right"
)
```

**参数说明：**

- `ppt_file_path`：PPT文件路径，支持.ppt和.pptx格式
- `text_script`：讲解文本脚本，如果不提供，将自动从PPT备注获取讲解
- `virtual_human_id`：数字人ID，不提供则使用默认数字人
- `virtual_human_posture_id`：数字人姿势ID，不提供则根据位置自动选择
- `title`：视频标题，默认为"PPT讲解视频"
- `resolution`：视频分辨率，支持"720p"或"1080p"，默认为"1080p"
- `caption_config`：字幕配置，不提供则使用默认配置
- `tts_config`：TTS语音配置，不提供则使用默认配置
- `single_page_seconds`：单页PPT显示时间（秒），默认为5秒
- `virtual_human_position`：数字人位置，支持"left"、"center"、"right"，默认为"right"

**返回值：**

返回一个字典，包含以下字段：
- `task_id`：任务ID，用于后续查询任务状态
- `status`：初始状态，通常为"created"
- `create_time`：任务创建时间戳
- `title`：视频标题
- `message`：任务创建结果消息

### 2. 查询任务状态

```python
query_ppt_video_task(task_id)
```

**参数说明：**

- `task_id`：任务ID，由create_ppt_video_task返回

**返回值：**

返回一个字典，包含以下字段：
- `task_id`：任务ID
- `status`：任务状态，可能的值有：
  - `pending`：等待中
  - `processing`：处理中
  - `success`：成功完成
  - `failed`：处理失败
- `progress`：处理进度百分比（0-100）
- `create_time`：任务创建时间戳
- `message`：状态描述信息
- `video_url`：（仅当status为"success"时）生成的视频URL

### 3. 获取可用的数字人列表

```python
get_digital_humans()
```

**返回值：**

返回一个包含所有可用数字人信息的列表，每个数字人信息包含：
- `id`：数字人ID
- `name`：数字人名称
- 其他API返回的属性

### 4. 获取数字人姿势列表

```python
get_digital_human_postures(virtual_human_id)
```

**参数说明：**

- `virtual_human_id`：数字人ID

**返回值：**

返回指定数字人可用的姿势列表，每个姿势包含：
- `id`：姿势ID
- `name`：姿势名称
- 其他API返回的属性

### 5. 默认数字人配置

模块提供了默认的数字人和姿势配置，可以直接使用：

```python
DEFAULT_VIRTUAL_HUMANS = {
    "default": {
        "virtualHumanId": "VHP3S1EF7",
        "postures": {
            "right": "aMiAX96rMqNS",  # 右侧站立姿势
            "left": "d5nJE6EI0txK"    # 左侧站立姿势
        }
    },
    "business_man": {
        "virtualHumanId": "VHFXQGGVG",
        "postures": {
            "center": "bKnPeXPndZCR"  # 中间站立姿势
        }
    },
    "business_woman": {
        "virtualHumanId": "VHT1NU4H7",
        "postures": {
            "center": "kOBCsOYhcdIi"  # 中间站立姿势
        }
    }
}
```

## 测试脚本

项目包含一个测试脚本`test_aibeings_ppt_video.py`，可以用于测试功能是否正常：

```bash
# 使用模拟模式测试
python test_aibeings_ppt_video.py --mock

# 使用实际API测试，指定PPT文件
python test_aibeings_ppt_video.py --ppt_path /path/to/your/presentation.pptx
```

## 实现原理

本模块实现了对小冰AI Beings API的完整封装：

1. **文件上传**：首先将PPT文件上传到小冰云存储，获取文件URL
2. **场景配置**：根据参数配置数字人、字幕、TTS等场景元素
3. **任务创建**：调用视频创建API，提交完整的场景配置
4. **任务查询**：定期查询任务状态，获取最终视频URL

## 高级配置示例

### 1. 自定义字幕样式

```python
caption_config = {
    "topCenter": True,  # 顶部居中
    "zIndex": 60,       # 层级
    "attributes": {
        "visible": True,
        "fontColor": "#ff3c3c",  # 红色
        "spacing": 1,
        "italic": False,
        "underline": False,
        "bold": True,
        "y": 1000,              # 垂直位置
        "fontSize": 44          # 字体大小
    }
}
```

### 2. 自定义TTS配置

```python
tts_config = {
    "voiceId": "101-master-ugdr",  # 语音ID
    "rate": 1.2,                   # 语速
    "pitch": 1.1,                  # 音调
    "volume": 60                   # 音量
}
```

## 故障排除

1. **文件上传失败**
   - 检查PPT文件是否存在且格式正确
   - 确保API Key有效且有足够权限
   - 检查文件大小是否超过限制（通常为30MB）

2. **任务创建失败**
   - 检查API参数是否正确，特别是数字人ID和姿势ID
   - 确认PPT内容符合要求，不包含违规内容
   - 查看日志文件`logs/aibeings_api_debug.log`获取详细错误信息

3. **视频生成慢**
   - 任务通常需要5-15分钟处理，取决于PPT的复杂度和页数
   - 分辨率越高，处理时间越长

## 注意事项

- API调用受到小冰平台限制，请合理使用
- 生成的视频有保存期限，请及时下载
- 请不要上传含有违规内容的PPT或提供违规讲解文案
- 单个PPT文件不要太大或页数过多，否则可能导致处理失败 