from flask import Blueprint, request, Response, current_app, jsonify
import requests
import logging
from bs4 import BeautifulSoup
import re
import urllib.parse

# 创建代理蓝图
proxy_blueprint = Blueprint('proxy', __name__)

# 设置日志
logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = [
    'text/html', 
    'text/css', 
    'application/javascript', 
    'text/javascript',
    'image/jpeg', 
    'image/png', 
    'image/gif', 
    'image/svg+xml',
    'application/json',
    'application/xml',
    'text/xml',
    'font/woff',
    'font/woff2',
    'font/ttf',
    'application/font-woff',
    'application/x-font-woff'
]

@proxy_blueprint.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy():
    """
    代理服务，将请求转发到指定URL并返回响应
    """
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'error': '未提供目标URL'}), 400
    
    method = request.method
    logger.info(f"[代理请求] {method} {target_url}")
    
    # 对于OPTIONS请求，返回CORS头部
    if method == 'OPTIONS':
        response = Response('')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24小时
        return response
    
    try:
        # 复制原始请求头
        headers = {}
        for header, value in request.headers:
            # 跳过某些特定头信息
            if header.lower() not in ['host', 'content-length', 'transfer-encoding', 'connection', 'cookie']:
                headers[header] = value
        
        # 添加常见请求头
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
        headers['Referer'] = target_url
        
        # 删除Accept-Encoding，让requests库处理编码
        if 'Accept-Encoding' in headers:
            del headers['Accept-Encoding']
        
        # 添加Cookie支持
        cookies = {}
        if request.cookies:
            cookies = request.cookies.to_dict()
        
        # 准备请求参数
        kwargs = {
            'headers': headers,
            'cookies': cookies,
            'timeout': 15,
            'allow_redirects': True,
            'verify': False,  # 不验证SSL证书
        }
        
        # 处理查询参数
        parsed_url = urllib.parse.urlparse(target_url)
        orig_params = urllib.parse.parse_qs(parsed_url.query)
        
        # 合并请求URL上的参数
        for key, value in request.args.items():
            if key != 'url':  # 排除url参数
                orig_params[key] = [value]
        
        # 更新URL查询参数
        updated_query = urllib.parse.urlencode(orig_params, doseq=True)
        parts = list(parsed_url)
        parts[4] = updated_query
        final_url = urllib.parse.urlunparse(parts)
        
        # 处理请求数据
        if method in ['POST', 'PUT', 'PATCH']:
            if request.content_type and 'application/json' in request.content_type:
                kwargs['json'] = request.get_json(silent=True)
            else:
                kwargs['data'] = request.get_data()
        
        logger.info(f"[请求详情] URL: {final_url}")
        logger.info(f"[请求详情] 头信息: {headers}")
        
        # 发送请求
        target_response = requests.request(
            method=method,
            url=final_url,
            **kwargs
        )
        
        logger.info(f"[目标响应] 状态码: {target_response.status_code}, 内容类型: {target_response.headers.get('Content-Type', '未知')}")
        
        # 准备响应头
        response_headers = {}
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        
        for header, value in target_response.headers.items():
            if header.lower() not in excluded_headers:
                response_headers[header] = value
        
        # 添加CORS和iframe嵌入相关的头信息
        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response_headers['Access-Control-Allow-Headers'] = '*'
        response_headers['Access-Control-Allow-Credentials'] = 'true'
        response_headers['X-Frame-Options'] = 'ALLOWALL'
        
        # 显式设置安全头部，允许iframe嵌入
        response_headers['Content-Security-Policy'] = "frame-ancestors *"
        
        # 获取响应内容
        content = target_response.content
        content_type = target_response.headers.get('Content-Type', '')
        
        # 处理内容类型和编码
        charset = None
        if 'charset=' in content_type:
            charset_match = re.search(r'charset=([^\s;]+)', content_type)
            if charset_match:
                charset = charset_match.group(1)
        
        # 对HTML内容进行处理
        if 'text/html' in content_type and content:
            try:
                # 使用正确的编码解析HTML
                decoded_content = content.decode(charset or 'utf-8', errors='replace')
                soup = BeautifulSoup(decoded_content, 'html.parser')
                
                # 如果没有发现<base>标签，添加base标签以正确解析相对路径
                base_url = urllib.parse.urljoin(target_url, '/')
                if not soup.find('base'):
                    base_tag = soup.new_tag('base', href=base_url)
                    if soup.head:
                        soup.head.insert(0, base_tag)
                    elif soup.html:
                        head_tag = soup.new_tag('head')
                        head_tag.append(base_tag)
                        soup.html.insert(0, head_tag)
                
                # 处理script、link和img标签的路径问题
                for tag in soup.find_all(['script', 'link', 'img', 'a', 'iframe', 'form']):
                    # 处理script的src属性
                    if tag.name == 'script' and tag.has_attr('src') and not tag['src'].startswith(('http', 'https', '//')):
                        tag['src'] = urllib.parse.urljoin(base_url, tag['src'])
                    
                    # 处理link的href属性
                    elif tag.name == 'link' and tag.has_attr('href') and not tag['href'].startswith(('http', 'https', '//')):
                        tag['href'] = urllib.parse.urljoin(base_url, tag['href'])
                    
                    # 处理img的src属性
                    elif tag.name == 'img' and tag.has_attr('src') and not tag['src'].startswith(('http', 'https', '//')):
                        tag['src'] = urllib.parse.urljoin(base_url, tag['src'])
                    
                    # 处理a标签的href属性，添加代理前缀
                    elif tag.name == 'a' and tag.has_attr('href'):
                        if not tag['href'].startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                            if not tag['href'].startswith(('http', 'https', '//')):
                                absolute_url = urllib.parse.urljoin(base_url, tag['href'])
                                tag['href'] = f"/api/v1/proxy/?url={urllib.parse.quote(absolute_url)}"
                            else:
                                tag['href'] = f"/api/v1/proxy/?url={urllib.parse.quote(tag['href'])}"
                    
                    # 处理form的action属性
                    elif tag.name == 'form' and tag.has_attr('action'):
                        if not tag['action'].startswith(('http', 'https', '//')):
                            absolute_url = urllib.parse.urljoin(base_url, tag['action'])
                            tag['action'] = f"/api/v1/proxy/?url={urllib.parse.quote(absolute_url)}"
                        else:
                            tag['action'] = f"/api/v1/proxy/?url={urllib.parse.quote(tag['action'])}"
                
                # 添加调试信息
                debug_div = soup.new_tag('div')
                debug_div['id'] = 'proxy-debug-info'
                debug_div['style'] = 'position:fixed; left:10px; bottom:10px; background:rgba(0,0,0,0.7); color:white; padding:5px 10px; font-size:12px; z-index:9999; border-radius:4px;'
                debug_div.string = f"通过代理加载: {target_url}"
                if soup.body:
                    soup.body.insert(len(soup.body.contents), debug_div)
                
                # 添加JS以避免跨域问题
                script_tag = soup.new_tag('script')
                script_tag.string = """
                (function() {
                  // 处理动态加载的资源，添加代理前缀
                  const originalOpen = XMLHttpRequest.prototype.open;
                  XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
                    if (url && !url.startsWith('/api/v1/proxy') && 
                        !url.startsWith('http://localhost') && 
                        !url.startsWith('https://localhost') && 
                        !url.startsWith('http://127.0.0.1') && 
                        !url.startsWith('https://127.0.0.1') && 
                        !url.startsWith('#')) {
                      const proxyUrl = '/api/v1/proxy/?url=' + encodeURIComponent(url);
                      return originalOpen.call(this, method, proxyUrl, async, user, password);
                    }
                    return originalOpen.apply(this, arguments);
                  };
                  console.log('代理脚本已加载，替换动态请求路径');
                })();
                """
                if soup.body:
                    soup.body.append(script_tag)
                
                # 转换回HTML字符串
                content = str(soup).encode('utf-8')
                logger.info(f"[处理完成] HTML内容修改成功，长度: {len(content)}字节")
            except Exception as e:
                logger.error(f"[处理失败] HTML处理错误: {str(e)}", exc_info=True)
        
        # 创建响应
        response = Response(
            content,
            status=target_response.status_code,
            headers=response_headers
        )
        
        # 处理响应Cookies
        if target_response.cookies:
            for cookie in target_response.cookies:
                # 修改domain和path
                cookie_options = {
                    'path': '/',
                    'secure': False,
                    'httponly': cookie.has_nonstandard_attr('httponly')
                }
                response.set_cookie(cookie.name, cookie.value, **cookie_options)
        
        return response
                
    except requests.RequestException as e:
        logger.error(f"[请求错误] 请求目标URL失败: {str(e)}", exc_info=True)
        return jsonify({
            'error': '代理请求失败',
            'message': str(e),
            'target_url': target_url
        }), 500
    except Exception as e:
        logger.error(f"[系统错误] 代理服务发生未知错误: {str(e)}", exc_info=True)
        return jsonify({
            'error': '代理服务错误',
            'message': str(e)
        }), 500

@proxy_blueprint.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': '代理服务找不到请求的路径'}), 404

@proxy_blueprint.errorhandler(500)
def server_error(e):
    return jsonify({'error': '代理服务内部错误'}), 500 