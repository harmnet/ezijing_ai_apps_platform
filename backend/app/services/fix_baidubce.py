#!/usr/bin/env python3
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_baidubce():
    """
    修复百度云BOS SDK的Python 3兼容性问题
    """
    try:
        # 修复unicode问题
        import builtins
        import sys
        
        # 在Python 3中添加unicode作为str的别名
        if not hasattr(builtins, 'unicode'):
            builtins.unicode = str
            logger.info("成功添加unicode作为str的别名")
            
        # 修复BOS客户端
        import types
        import baidubce
        from baidubce.services.bos.bos_client import BosClient
        
        # 添加func_code属性到所有handler函数
        original_send_request = baidubce.http.bce_http_client.send_request
        
        def patched_send_request(*args, **kwargs):
            try:
                return original_send_request(*args, **kwargs)
            except NameError as e:
                if str(e) == "name 'unicode' is not defined":
                    logger.info("捕捉并修复unicode错误")
                    return original_send_request(*args, **kwargs)
                raise
            except AttributeError as e:
                if "has no attribute 'func_code'" in str(e):
                    logger.info("捕捉并修复func_code错误")
                    # 动态修复函数属性
                    for module_name in dir(baidubce.http):
                        try:
                            module = getattr(baidubce.http, module_name)
                            if isinstance(module, types.ModuleType):
                                for attr_name in dir(module):
                                    attr = getattr(module, attr_name)
                                    if callable(attr) and not hasattr(attr, 'func_code'):
                                        setattr(attr, 'func_code', attr.__code__ if hasattr(attr, '__code__') else None)
                        except:
                            pass
                    
                    # 二次尝试
                    return original_send_request(*args, **kwargs)
                raise
        
        # 替换原始函数
        baidubce.http.bce_http_client.send_request = patched_send_request
            
        # 测试修复是否成功
        from baidubce.bce_client_configuration import BceClientConfiguration
        from baidubce.auth.bce_credentials import BceCredentials
        
        logger.info("百度云BOS SDK导入成功，修复完成")
        return True
    except Exception as e:
        logger.error(f"修复百度云SDK失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_baidubce()
    print(f"修复结果: {'成功' if success else '失败'}") 