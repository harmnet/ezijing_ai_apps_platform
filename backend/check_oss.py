#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查阿里云OSS配置
"""

import oss2

# 阿里云OSS配置
access_key_id = 'LTAI5tMVdYzk5fVrmjQVk1Ga'
access_key_secret = 'OKUYiiO9WOw5bJpRTfJa7F76Ayygdk'
endpoint = 'oss-cn-beijing.aliyuncs.com'
bucket_name = 'ezijingai'

def check_oss_config():
    """检查OSS配置并列出存储桶"""
    auth = oss2.Auth(access_key_id, access_key_secret)
    
    # 列出所有存储桶
    print('正在连接阿里云OSS...')
    service = oss2.Service(auth, f'http://{endpoint}')
    
    print('您账号中的存储桶:')
    for bucket in oss2.BucketIterator(service):
        print(f' - {bucket.name}')
    
    # 检查目标存储桶是否存在
    print(f'\n检查存储桶 "{bucket_name}" 是否存在...')
    bucket = oss2.Bucket(auth, f'http://{endpoint}', bucket_name)
    
    try:
        bucket.get_bucket_info()
        print(f'✅ 存储桶 "{bucket_name}" 存在且可访问')
    except oss2.exceptions.NoSuchBucket:
        print(f'❌ 存储桶 "{bucket_name}" 不存在')
    except Exception as e:
        print(f'❌ 访问存储桶时出错: {str(e)}')

if __name__ == '__main__':
    check_oss_config() 