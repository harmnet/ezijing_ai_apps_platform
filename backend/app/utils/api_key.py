#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API密钥管理模块
"""

def get_api_key(service_name="volcano"):
    """
    获取API密钥
    :param service_name: 服务名称
    :return: API密钥
    """
    if service_name == "volcano":
        return "03824a7c-e453-4ccd-b356-e7f80a793add"
    else:
        return None 