#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字人PPT讲解视频配置文件
基于小冰AI Beings API封装
"""

XIAOBING_REGION = "https://openapi.xiaoice.com/vh/"
# 创建PPT讲解视频生成任务 请求路径
XIAOBING_PPT_SUBMIT_REQUEST_URL = XIAOBING_REGION + "/openapi/video/task/v2/ppt/submit"
# 查询任务结果 请求路径
XIAOBING_TASK_DETAIL_REQUEST_URL = XIAOBING_REGION + "/openapi/video/task/v2/detail"
XIAOBING_DIGITAL_HUMAN_SUB_KEY = "282cd94b697e48e6aca6d20bbdaf0d0f"
XIAOBING_REQUEST_HEADERS = {
    "subscription-key": XIAOBING_DIGITAL_HUMAN_SUB_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

from dataclasses import dataclass, field
from typing import List, Optional
import logging
import json
import os
from urllib.parse import urlparse


@dataclass
class OpenApiBaseAttributes:
    x: Optional[int] = None
    y: Optional[int] = None


@dataclass
class OpenApiBackgroundMusic:
    mediaUrl: str  # 背景音乐下载url，格式：mp3/wav，最大50M
    volume: float = 1.0  # float，1代表原始音量，0为静音，音量取值范围0-1
    speed: float = 1.0  # float，1代表原始速度，倍速取值范围0-3
    loop: bool = True  # 是否循环播放，默认true循环


@dataclass
class OpenApiVirtualHumanAttributes(OpenApiBaseAttributes):
    width: Optional[int] = None  # 宽度，默认为0.75 * defaultWidth
    height: Optional[int] = (
        None  # 高度，默认为0.75* defaultHeight，宽高任意一个未填时将取默认值。宽高必须按比例缩放，数据精度造成的误差将会做近似容错处理。
    )
    forceMattingType: int = 0


@dataclass
class OpenApiVirtualHuman:
    virtualHumanId: str  # 虚拟人id，查询数字资产接口返回结果中的virtualHumanId
    virtualHumanPostureId: (
        str  # 姿势id，查询播报数字员工详情接口中返回结果中的姿势bizId
    )
    attributes: OpenApiVirtualHumanAttributes  # 虚拟人属性
    zIndex: int = 20


@dataclass
class OpenApiTts:
    voiceId: str  # 虚拟人详情里面声音信息中提供的结果(detailDigitalEmployee)，VoiceInfo 对象里面的 voiceId 字段
    rate: float = 1.0  # 语速，默认1， 取值范围 >=0.6, <=1.5
    pitch: float = 1.0  # 语调，默认1， 取值范围 >=0.6, <=1.5
    volume: int = 50  # 音量，默认50，取值范围 >=0 <=100


@dataclass
class OpenApiDisplayTextAttributes(OpenApiBaseAttributes):
    font: int = 1  # 字体，见字体列表
    fontSize: int = 44  # 字号，字体大小设置，1-200
    fontColor: str = (
        "#ff3c3c"  # 字体颜色，字符串形式十六进制色号，"0x000000" -> "0xFFFFFF"
    )
    fontColorOpacity: float = 1.0  # 字体透明度，float，取值范围0-1，默认为1
    angle: int = 0  # 角度，顺时针叠加角度，取值0，90，180，270。默认0不旋转
    bold: bool = False  # 加粗，默认false
    italic: bool = False  # 斜体，默认false
    underline: bool = False  # 下划线，默认false
    spacing: int = 0  # 字间距，默认0
    fontPath: Optional[str] = None  # 字体源地址，如https://xxxxx.ttf
    shadowOn: bool = False  # 是否开启阴影
    shadowColor: Optional[str] = None  # 阴影颜色
    shadowOffsetX: Optional[int] = None  # 阴影偏移水平距离
    shadowOffsetY: Optional[int] = None  # 阴影偏移垂直距离
    strokeOn: bool = False  # 是否开启描边
    strokeColor: Optional[str] = None  # 字体描边颜色 格式：#f0f0f0f0(RGBA)
    strokeWidth: Optional[float] = None  # 字体描边宽度
    backgroundColor: Optional[str] = None  # 背景颜色 格式：#f0f0f0f0(RGBA)
    radius: Optional[int] = None  # 背景边框圆弧的大小
    visible: bool = True


@dataclass
class OpenApiCaption:
    topLeft: bool = False  # 范围内居左
    topRight: bool = False  # 指每行字幕在字幕框的范围内的对齐方式，范围内居右
    topCenter: bool = False  # 范围内居中
    zIndex: int = 60
    attributes: Optional[OpenApiDisplayTextAttributes] = (
        None  # 字幕属性（结构与DisplayText相同）可用字段包含x, y，加粗，斜体，下划线，字号，字间距。不填时，默认画面居中，y轴画面底部留白1倍字号。字体默认6，微软雅黑。字间距默认0。字号默认40，单位像素。字幕组件宽度自动填充，默认17x字宽+16x字间距
    )


@dataclass
class OpenApiBackgroundImage:
    mediaUrl: str  # 仅支持JPG，PNG，GIF格式，最大支持10M的文件


@dataclass
class OpenApiScene:
    virtualHuman: OpenApiVirtualHuman  # 虚拟人信息
    tts: OpenApiTts  # 声音信息
    backgroundImage: Optional[OpenApiBackgroundImage] = (
        None  # 背景图片，背景图片将会自动拉伸至覆盖全屏，没有背景图片时默认填充白色背景
    )
    caption: Optional[OpenApiCaption] = None  # 字幕信息，此字段不传时画面中不显示字幕
    voiceText: Optional[str] = (
        None  # 本段场景内将要播报的内容，若PPT信息中设置了取PPT中的备注文本，则此字段无效，即使PPT中某页没有备注文本也不取此字段
    )


@dataclass
class OpenApiVideoCreationDetail:
    scenes: List[OpenApiScene]  # 视频场景列表
    backgroundMusic: Optional[OpenApiBackgroundMusic] = None  # 全局背景音乐


@dataclass
class OpenApiPPTAttributes(OpenApiBaseAttributes):
    width: Optional[int] = None  # ppt在视频画面中的宽，默认值会适配画布的宽高
    height: Optional[int] = None  # ppt在视频画面中的高，默认值会适配画布的宽高


class ConvertType(str):
    IMG = "IMG"
    VIDEO = "VIDEO"


@dataclass
class OpenApiPPTInfo:
    pptUrl: str  # PPT的URL地址
    convertType: ConvertType  # 转换类型，枚举值: IMG或者VIDEO。IMG只保留图片不保留动画。VIDEO保留 PPT中的动画视频，制作PPT时请使用自动播放动画
    getText: bool  # 是否获取备注文本作为虚拟人讲解文本。某页备注为空时此场景静音，没有播报音频
    singlePageSecond: int = (
        3  # 默认3秒。当保留动画时设置每页转换的时长。为保证动画完整性，此时长应大于等于制作PPT动画时设置的时长
    )
    attributes: Optional[OpenApiPPTAttributes] = None  # ppt在视频画面中的位置和大小


# 字体列表
FONT_DICT = {
    "FZHei-B01S": 1,
    "FZKai-Z03S": 2,
    "FZShuSong-Z01S": 3,
    "WenQuanYi MicroHei": 4,
    "WenQuanYi Zen Hei Mono": 5,
    "Microsoft YaHei": 6,
    "Yuanti SC": 7,
    "Roboto Bold": 8,
    "Roboto": 9,
    "Source Han Sans CN": 10,
    "Source Han Serif SC": 11,
    "KaiTi": 12,
    "阿里巴巴普惠体M": 13,
    "SiYuanJianTi": 14,
    "SiYuanCuTi": 15,
    "AlimamaShuHeiTi-Bold": 16,
    "HanBiaoXiaoAiShuangGouJianTi": 17,
    "RiXiKeAiNaiLaoTi": 18,
    "HaiYanXingQiuBianLiDian": 19,
    "BaoTuCunLangTi": 20,
    "RenJianHuangTangYouGuGuai": 21,
    "GuoJiaYiJiBaoHuDongWu": 22,
    "FangFangYuanYuanTi": 23,
    "NanYiWangJiChuCiHeNi": 24,
    "GaoQingPingYinTi": 25,
    "LangHuaTaoTao": 26,
    "DiShiNiZaiTaoDeGongZhu": 27,
    "HanBiaoFenBiZhongHeiTi": 28,
    "HanBiaoGuiFuTi": 29,
    "HanBiaoNeiYuanCuHeiTi": 30,
    "HanBiaoShuangjianTi": 31,
    "HanBiaoTuiFeiTi": 32,
    "HanBiaoXiHeiTi": 33,
    "HanChengBoBoKongXinXingKaiti": 34,
    "HanChengBoBoLiuYeKongXinti": 35,
    "HanChengWangTianXiBingXueYingXiong": 36,
    "HanChengWangTianXiWeiMeiXingShu": 37,
    "BUPianBuYi QuanDouShiNi": 38,
    "AOWuAoWuGeiNiTang": 39,
    "JiJianZhuYi": 40,
    "WanWuJieNiWeiLaiKeQi": 41,
    "BaoTuJianYuanTi": 42,
    "QingTianKeAiXiangNiTi": 43,
    "NanGouDongFangPin ChangGui": 44,
    "NanGouMingShiGaoJian": 45,
    "NanGouShiYunXinLi": 46,
    "NanGouShiDaiHei": 47,
    "NanGouXieYuHei ChangGui": 48,
    "NanGouYuXiangZhenXian": 49,
    "RuanTangKeAiTi": 50,
    "WoXiHuanDeWenRouShiNi": 51,
    "WoQueDingNiJiuShiWeiYi": 52,
    "GaoBaiShouZhang": 53,
    "XiFengXieYang": 54,
    "TianYouWanZhongXingHei": 55,
    "ShanHeiYuanKuoRenJianYanHuo": 56,
    "YueLiangShuiLeWoBushui": 57,
    "BaoTuXiaoBiaoTi": 58,
    "JinRiXianDingXinDong": 59,
    "YanKaiBaiWen": 60,
    "ShengYeBoBoNaiDong": 61,
    "BaoTuCuHeiTi": 62,
    "ChongLangXingKai": 63,
    "GaoQingBiaoTiTi": 64,
    "HanBiaoBeiShiTi": 65,
    "HanBiaoGongZiTi": 66,
    "HanBiaoXiYuanTi": 67,
    "HanBiaoLaoJiaoPianTi": 68,
    "HanBiaoWaiXianHeiTi": 69,
    "HanBiaoZhaoYuanCuTi": 70,
    "HanChengDaoFengKaiShu": 71,
    "HanChengBoBoMoXingKai": 72,
    "HanChengSanNianErBan": 73,
    "HanChengQingFengJiYue": 74,
    "HanChengWngFeiJieCanLanTongNian": 75,
    "HanChengTanFaSheXingShu": 76,
    "HanChengBoBoXingKaiZiTi": 77,
    "HanChengHuaHuaXingKaiXingBan": 78,
    "HanChengBoBoZhuiLangTi": 79,
    "HanChenWangTianXiMaoBiXiaoKai": 80,
    "HanChengWangTianXiKuaiShu": 81,
    "NanGouLiuZhiWenKaiShu": 82,
    "NanGouLongYingBei": 83,
    "NanGouQianHei-H": 84,
    "NanGouWangMeiHei": 85,
    "NGzhenman-G": 86,
    "NanGouZhongShengXingShu": 87,
    "NanGouZhongHuaKai": 88,
    "NanGouBinYingBiKaiShu": 89,
    "NanGouHuangNianHuKaiShu": 90,
    "NanGouRiManFeng": 91,
    "NanGouQinDiaoHanGu": 92,
    "NanGouShuFangChaoXingShu": 93,
    "NanGouWuBian": 94,
    "NanGouWangXiaoLongBangHang": 95,
    "NanGouLiPingShouXie": 96,
    "HanGouXiaoLaoKaiShu": 97,
    "YeGenYouMengDuTi ChangGui": 98,
    "YeGenYouShangRuiBoHei1.0 ChangGui": 99,
    "YeGenYouWeiGangChongAn ChangGui": 100,
    "XianHeiTi": 101,
    "HanChengWangTianXiChaoJingTi": 102,
    "AnJingChenMaoBiXingShu": 103,
    "Nom Na Tong": 104,
    "Boon Regular": 105,
    "Gulzar": 106,
    "UKIJEs": 107,
    "UKIJEsBold": 108,
    "UKIJEsC": 109,
    "UKIJEsN": 110,
    "UKIJEsQ": 111,
    "UKIJEsT": 112,
}

# 默认TTS语音配置
DEFAULT_TTS = {
    "voiceId": "VH_XIAOBING_zh-CN_zhcnv2_F53947-zovQmXN79vG00q6b",
    "rate": 1,
    "pitch": 1,
    "volume": 100
}

# 默认字幕配置
DEFAULT_CAPTION = {
    "topCenter": True,
    "zIndex": 60,
    "attributes": {
        "visible": True,
        "fontColor": "#FFFFFF",
        "spacing": 1,
        "italic": False,
        "underline": False,
        "bold": True,
        "y": 1000,
        "fontSize": 36,
        "font": FONT_DICT["Microsoft YaHei"]
    }
}

# 默认背景音乐
DEFAULT_BACKGROUND_MUSIC = {
    "mediaUrl": "https://virtualman.oss-cn-beijing.aliyuncs.com/media_upload/1a1789ea-25bf-437b-acd2-fdc08a265087.MP3",
    "volume": 0.3,
    "speed": 1,
    "loop": True
}

# 支持的视频分辨率
SUPPORTED_RESOLUTIONS = {
    "720p": {"width": 1280, "height": 720},
    "1080p": {"width": 1920, "height": 1080},
    "480p": {"width": 854, "height": 480}
}

# 数字人ID和姿势ID映射表
DEFAULT_VIRTUAL_HUMANS = {
    "default": {
        "virtualHumanId": "VHP3S1EF7",
        "name": "默认数字人",
        "postures": {
            "right": "aMiAX96rMqNS",  # 右侧站立姿势
            "left": "d5nJE6EI0txK"    # 左侧站立姿势
        }
    },
    "business_man": {
        "virtualHumanId": "VHFXQGGVG",
        "name": "商务男士",
        "postures": {
            "center": "bKnPeXPndZCR"  # 中间站立姿势
        }
    },
    "business_woman": {
        "virtualHumanId": "VHT1NU4H7",
        "name": "商务女士",
        "postures": {
            "center": "kOBCsOYhcdIi"  # 中间站立姿势
        }
    }
}

def generate_request_body(ppt_url, title, virtual_human_id=None, virtual_human_posture_id=None,
                      text_script=None, background_music_url=None, background_image_url=None,
                      show_caption=True, resolution="720p", convert_type="VIDEO", tts_params=None):
    """
    生成请求体
    :param ppt_url: PPT文件URL
    :param title: 视频标题
    :param virtual_human_id: 虚拟人ID
    :param virtual_human_posture_id: 虚拟人姿势ID
    :param text_script: 讲解文本
    :param background_music_url: 背景音乐URL
    :param background_image_url: 背景图片URL
    :param show_caption: 是否显示字幕
    :param resolution: 视频分辨率
    :param convert_type: 转换类型，VIDEO或IMG
    :param tts_params: TTS参数
    :return: 请求体
    """
    logger = logging.getLogger(__name__)
    
    try:
        # 检查PPT URL是否为本地URL
        parsed_url = urlparse(ppt_url)
        is_local_url = parsed_url.netloc in ['localhost', '127.0.0.1'] or parsed_url.netloc.startswith('localhost:') or parsed_url.netloc.startswith('127.0.0.1:')
        
        if is_local_url:
            # 如果是本地URL，需要上传到OSS
            logger.info(f"检测到本地PPT URL，准备上传到OSS: {ppt_url}")
            try:
                # 从URL中提取文件路径
                file_path = parsed_url.path
                if file_path.startswith('/'):
                    file_path = file_path[1:]
                file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), file_path)
                
                # 上传到OSS
                oss_url = upload_to_oss(file_path)
                if oss_url:
                    logger.info(f"PPT文件已上传到OSS: {oss_url}")
                    ppt_url = oss_url
                else:
                    logger.error("PPT文件上传到OSS失败")
            except Exception as e:
                logger.error(f"上传PPT到OSS时发生错误: {str(e)}")
        
        # 获取分辨率配置
        resolution_config = SUPPORTED_RESOLUTIONS.get(resolution, SUPPORTED_RESOLUTIONS["720p"])
        width = resolution_config["width"]
        height = resolution_config["height"]

        # 构建场景数据
        scene = {
            "virtualHuman": {
                "virtualHumanId": virtual_human_id or DEFAULT_VIRTUAL_HUMANS["default"]["virtualHumanId"],
                "virtualHumanPostureId": virtual_human_posture_id or DEFAULT_VIRTUAL_HUMANS["default"]["postures"]["right"],
                "attributes": {
                    "width": int(height * 0.32),  # 根据高度等比例设置宽度
                    "height": height,
                    "x": int(width * 0.79),  # 放置在右侧
                    "y": int(height * 0.29),  # 垂直位置偏移
                    "forceMattingType": 0
                },
                "zIndex": 20
            },
            "tts": tts_params or DEFAULT_TTS,
            "voiceText": text_script,
        }

        # 添加字幕配置
        if show_caption:
            scene["caption"] = {
                "topCenter": True,
                "topLeft": False,
                "topRight": False,
                "zIndex": 60,
                "attributes": {
                    "visible": True,
                    "fontColor": "#FFFFFF",
                    "spacing": 1,
                    "italic": False,
                    "underline": False,
                    "bold": True,
                    "y": int(height * 0.93),  # 放置在底部
                    "fontSize": int(height * 0.033)  # 根据高度等比例设置字号
                }
            }

        # 添加背景图片配置
        if background_image_url:
            scene["backgroundImage"] = {
                "mediaUrl": background_image_url
            }

        # 构建完整请求体
        request_body = {
            "outputVideoName": title,
            "width": width,
            "height": height,
            "creationDetail": {
                "scenes": [scene],
                "backgroundMusic": {
                    "mediaUrl": background_music_url or DEFAULT_BACKGROUND_MUSIC["mediaUrl"],
                    "volume": DEFAULT_BACKGROUND_MUSIC["volume"],
                    "speed": DEFAULT_BACKGROUND_MUSIC["speed"],
                    "loop": DEFAULT_BACKGROUND_MUSIC["loop"]
                }
            },
            "pptInfo": {
                "pptUrl": ppt_url,
                "convertType": convert_type,  # 使用传入的转换类型
                "getText": True,
                "singlePageSecond": 5,  # 与测试代码一致，设为5秒
                "attributes": {
                    "width": width,
                    "height": height,
                    "x": 0,
                    "y": 0
                }
            }
        }

        # 记录完整的请求体
        logger.info("生成的请求体详情：")
        logger.info(json.dumps(request_body, ensure_ascii=False, indent=2))

        return request_body
    except Exception as e:
        logger.error(f"生成请求体时发生错误: {str(e)}")
        raise