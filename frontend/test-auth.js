/**
 * API鉴权测试脚本
 * 用法: node test-auth.js
 */

const CryptoJS = require('crypto-js');
const https = require('https');
const http = require('http');
const url = require('url');

// 鉴权参数
const API_KEY = '673e95c065226';
const SECRET_KEY = '7bVcH15FeB1zTy08PN5n3YtmRxsVXjEv';

// 生成签名
function generateSignature(method, uri, timestamp, secretKey) {
  // 确保URI以/结尾
  if (!uri.endsWith('/')) {
    uri = uri + '/';
  }
  
  // 1. 创建待签名字符串
  const stringToSign = `${method}@${uri}@${timestamp}`;
  console.log('待签名字符串:', stringToSign);
  
  // 2. 使用HMAC-SHA1算法和SecretKey计算签名
  const hmacSha1 = CryptoJS.HmacSHA1(stringToSign, secretKey);
  
  // 3. 将签名结果转为Base64编码
  return CryptoJS.enc.Base64.stringify(hmacSha1);
}

// 发起API请求
function makeRequest(options, callback) {
  const parsedUrl = url.parse(options.url);
  const httpModule = parsedUrl.protocol === 'https:' ? https : http;
  
  const requestOptions = {
    hostname: parsedUrl.hostname,
    port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
    path: parsedUrl.path,
    method: options.method,
    headers: options.headers || {}
  };
  
  const req = httpModule.request(requestOptions, (res) => {
    let data = '';
    
    res.on('data', (chunk) => {
      data += chunk;
    });
    
    res.on('end', () => {
      try {
        const result = JSON.parse(data);
        callback(null, { statusCode: res.statusCode, headers: res.headers, data: result });
      } catch (error) {
        callback(null, { statusCode: res.statusCode, headers: res.headers, data: data });
      }
    });
  });
  
  req.on('error', (error) => {
    callback(error);
  });
  
  req.end();
}

// 测试获取token
function testGetToken() {
  console.log('========== API鉴权测试开始 ==========');
  console.log('API Key:', API_KEY);
  console.log('Secret Key:', SECRET_KEY.substring(0, 5) + '...[已隐藏]');
  
  const timestamp = Math.floor(Date.now() / 1000);
  const uri = '/api/grant/token';
  const method = 'GET';
  
  // 生成签名
  const signature = generateSignature(method, uri, timestamp, SECRET_KEY);
  console.log('生成的签名:', signature);
  
  // 构造请求头
  const headers = {
    'x-api-key': API_KEY,
    'x-timestamp': timestamp,
    'x-signature': signature
  };
  
  // 构造请求URL
  const params = new URLSearchParams({
    uid: '1',
    channel: 'ezijing'
  });
  const requestUrl = `https://co.aippt.cn${uri}?${params.toString()}`;
  
  console.log('请求URL:', requestUrl);
  console.log('请求头:', headers);
  
  // 发起请求
  makeRequest({
    url: requestUrl,
    method: method,
    headers: headers
  }, (error, response) => {
    if (error) {
      console.error('请求错误:', error.message);
    } else {
      console.log('响应状态码:', response.statusCode);
      console.log('响应数据:', JSON.stringify(response.data, null, 2));
      
      if (response.statusCode === 200 && response.data.code === 0) {
        console.log('API鉴权成功，Token:', response.data.data.token);
      } else {
        console.error('API鉴权失败:', response.data.msg || '未知错误');
      }
    }
    
    console.log('========== API鉴权测试结束 ==========');
  });
}

// 执行测试
testGetToken(); 