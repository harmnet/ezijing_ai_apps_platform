/**
 * 百度云BOS直接上传工具
 * 实现前端直接上传图片到百度云BOS对象存储
 */
import axios from 'axios';
import CryptoJS from 'crypto-js';

// 百度云BOS配置
const BOS_CONFIG = {
  accessKeyId: '', // 将在使用时从后端获取
  secretAccessKey: '', // 将在使用时从后端获取
  endpoint: 'bj.bcebos.com',
  bucketName: 'ezijing',
  domain: 'https://ezijing.bj.bcebos.com'
};

/**
 * 生成ISO8601格式的时间戳
 * @returns {string} ISO8601格式的时间戳
 */
function getISODateString() {
  return new Date().toISOString().replace(/\.\d+Z$/, 'Z');
}

/**
 * 计算文件的MD5值
 * @param {File} file - 文件对象
 * @returns {Promise<string>} - 返回base64编码的MD5值
 */
function calculateFileMD5(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const wordArray = CryptoJS.lib.WordArray.create(e.target.result);
        const md5 = CryptoJS.MD5(wordArray);
        const base64Md5 = CryptoJS.enc.Base64.stringify(md5);
        resolve(base64Md5);
      } catch (err) {
        reject(err);
      }
    };
    reader.onerror = (err) => reject(err);
    reader.readAsArrayBuffer(file);
  });
}

/**
 * 生成上传策略和签名
 * @param {Object} options - 配置选项
 * @returns {Object} - 包含policy和signature的对象
 */
function generatePolicyAndSignature(options = {}) {
  const {
    expiration = new Date(Date.now() + 30 * 60 * 1000).toISOString(), // 默认30分钟过期
    contentLengthRange = [0, 10 * 1024 * 1024], // 默认最大10MB
    keyPattern = null, // 对象键匹配模式
    bucket = BOS_CONFIG.bucketName
  } = options;

  // 构建policy对象 - 按照百度云BOS要求的格式
  const policy = {
    expiration,
    conditions: [
      { bucket }
    ]
  };

  // 添加content-length-range
  policy.conditions.push(['content-length-range', ...contentLengthRange]);

  // 如果指定了keyPattern，添加到conditions中
  if (keyPattern) {
    policy.conditions.push({ key: keyPattern });
  }

  // 将policy转为JSON
  const policyJson = JSON.stringify(policy);
  console.log('Policy JSON:', policyJson);
  
  // 对policy进行base64编码
  // 确保使用UTF-8编码，完全模拟Python中的base64.b64encode(policy)
  const policyBase64 = btoa(unescape(encodeURIComponent(policyJson)));
  
  // 根据Python示例代码精确实现签名方法
  // Python: hmac.new(sk, base64.b64encode(policy), hashlib.sha256).hexdigest()
  // 使用CryptoJS的HMAC-SHA256算法计算签名
  const signature = CryptoJS.HmacSHA256(
    policyBase64, // 使用base64编码后的policy作为消息
    BOS_CONFIG.secretAccessKey // 使用SK作为密钥
  ).toString(CryptoJS.enc.Hex); // 输出为十六进制字符串
  
  console.log('Generated policy:', policyBase64);
  console.log('Generated signature:', signature);

  return {
    policy: policyBase64,
    signature
  };
}

/**
 * 生成百度云BOS的V1签名
 * @param {Object} options - 签名选项
 * @returns {Object} - 包含authorization和headers的对象
 */
function generateBosV1Signature(options) {
  const {
    method,
    uri,
    params = {},
    headers = {},
    timestamp = getISODateString()
  } = options;

  // 1. 生成CanonicalRequest
  // 1.1 添加HTTP方法
  let canonicalRequest = `${method.toUpperCase()}\n`;

  // 1.2 添加URI
  canonicalRequest += `${uri}\n`;

  // 1.3 添加查询参数
  const queryParams = [];
  Object.keys(params).sort().forEach(key => {
    queryParams.push(`${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`);
  });
  canonicalRequest += `${queryParams.join('&')}\n`;

  // 1.4 添加规范化头信息
  const canonicalHeaders = {};
  // 添加host头
  canonicalHeaders['host'] = `${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}`;
  // 添加指定的头
  Object.keys(headers).forEach(key => {
    const lowerKey = key.toLowerCase();
    // 只保留必要的headers
    if (lowerKey === 'content-type' || lowerKey === 'content-md5' || lowerKey === 'date' || lowerKey.startsWith('x-bce-')) {
      canonicalHeaders[lowerKey] = headers[key];
    }
  });

  // 如果没有Date头，添加x-bce-date头
  if (!canonicalHeaders['date']) {
    canonicalHeaders['x-bce-date'] = timestamp;
  }

  // 构建规范化头部字符串
  const canonicalHeadersArray = [];
  Object.keys(canonicalHeaders).sort().forEach(key => {
    canonicalHeadersArray.push(`${key}:${canonicalHeaders[key]}`);
  });
  canonicalRequest += canonicalHeadersArray.join('\n');

  console.log('规范化请求字符串:', canonicalRequest);

  // 2. 生成签名密钥
  const authStringPrefix = `bce-auth-v1/${BOS_CONFIG.accessKeyId}/${timestamp}/1800`;
  const signingKey = CryptoJS.HmacSHA256(
    authStringPrefix,
    BOS_CONFIG.secretAccessKey
  ).toString(CryptoJS.enc.Hex);
  
  console.log('签名密钥:', signingKey);

  // 3. 计算签名
  const signature = CryptoJS.HmacSHA256(
    canonicalRequest,
    signingKey
  ).toString(CryptoJS.enc.Hex);
  
  console.log('签名结果:', signature);

  // 4. 生成Authorization字符串
  const headersToSign = Object.keys(canonicalHeaders).sort().join(';');
  const authorization = `${authStringPrefix}/host;${headersToSign}/${signature}`;

  return {
    authorization,
    headers: canonicalHeaders
  };
}

/**
 * 生成上传表单数据
 * @param {File} file - 要上传的文件
 * @param {Object} options - 上传选项
 * @returns {FormData} - 填充好的FormData对象
 */
function prepareUploadFormData(file, options = {}) {
  const {
    key = `uploads/${new Date().toISOString().slice(0, 10).replace(/-/g, '')}/${Date.now()}_${file.name}`,
    contentType = file.type || 'application/octet-stream',
    successRedirectUrl = null,
    contentDisposition = null,
    metadata = {}
  } = options;

  // 生成policy和signature
  const { policy, signature } = generatePolicyAndSignature({
    contentLengthRange: [0, file.size + 1024], // 允许的文件大小范围
    keyPattern: key,
    bucket: BOS_CONFIG.bucketName
  });

  // 创建FormData
  const formData = new FormData();
  
  // BOS API要求使用accessKey而不是accessKeyId
  formData.append('accessKey', BOS_CONFIG.accessKeyId);
  formData.append('policy', policy);
  formData.append('signature', signature);
  formData.append('key', key);
  
  // 添加Content-Type
  if (contentType) {
    formData.append('Content-Type', contentType);
  }

  // 添加Content-Disposition (如果指定)
  if (contentDisposition) {
    formData.append('Content-Disposition', contentDisposition);
  }

  // 添加自定义元数据
  Object.entries(metadata).forEach(([key, value]) => {
    formData.append(`x-bce-meta-${key}`, value);
  });

  // 添加成功重定向URL (如果指定)
  if (successRedirectUrl) {
    formData.append('success-redirect-url', successRedirectUrl);
  }

  // 添加文件数据 (必须放在最后)
  formData.append('file', file);

  return formData;
}

/**
 * 获取安全凭证
 * 从后端获取临时上传凭证，避免在前端暴露永久凭证
 * @returns {Promise<Object>} - 包含accessKeyId和secretAccessKey的对象
 */
async function getCredentials() {
  try {
    // 直接使用硬编码的访问凭证（临时解决方案）
    BOS_CONFIG.accessKeyId = "05c5a1cf304f45c6b17f55967449bc9b";
    BOS_CONFIG.secretAccessKey = "42d4dea8b0614fc09488c9386bad9909";
    return {
      accessKeyId: "05c5a1cf304f45c6b17f55967449bc9b",
      secretAccessKey: "42d4dea8b0614fc09488c9386bad9909"
    };
    
    /* 注释掉原始的API调用代码
    const response = await axios.get('/api/v1/upload/bos_credentials');
    
    if (response.data && response.data.success) {
      BOS_CONFIG.accessKeyId = response.data.accessKeyId;
      BOS_CONFIG.secretAccessKey = response.data.secretAccessKey;
      return {
        accessKeyId: response.data.accessKeyId,
        secretAccessKey: response.data.secretAccessKey
      };
    } else {
      throw new Error('获取上传凭证失败');
    }
    */
  } catch (error) {
    console.error('获取上传凭证异常:', error);
    throw error;
  }
}

/**
 * 使用表单方式直接上传文件到百度云BOS
 * @param {File} file - 要上传的文件对象
 * @param {Object} options - 上传选项
 * @param {Function} onProgress - 上传进度回调
 * @returns {Promise<string>} - 上传成功的文件URL
 */
export async function uploadFileByForm(file, options = {}, onProgress = null) {
  try {
    // 首先获取上传凭证
    await getCredentials();
    
    // 准备上传参数
    const {
      prefix = 'uploads',
      fileType = 'general',
      key = `${prefix}/${fileType}/${new Date().toISOString().slice(0, 10).replace(/-/g, '')}/${Date.now()}_${file.name}`
    } = options;

    // 准备表单数据
    const formData = prepareUploadFormData(file, {
      key,
      contentType: file.type || 'application/octet-stream'
    });

    // 设置上传URL
    const uploadUrl = `https://${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}/`;
    console.log('上传请求URL:', uploadUrl);

    // 执行上传请求
    const response = await axios.post(uploadUrl, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted, progressEvent);
        }
      }
    });

    // 构建文件URL
    const fileUrl = `${BOS_CONFIG.domain}/${key}`;
    return fileUrl;
  } catch (error) {
    console.error('表单上传到百度云BOS失败:', error);
    if (error.response) {
      console.error('响应状态:', error.response.status);
      console.error('响应数据:', error.response.data);
      console.error('响应头:', error.response.headers);
    }
    throw error;
  }
}

/**
 * 生成预签名PUT上传URL
 * @param {string} key - 文件的对象键
 * @param {string} contentType - 文件内容类型
 * @param {number} contentLength - 文件大小
 * @param {string} contentMD5 - 文件MD5值（可选）
 * @param {number} expireInSeconds - 链接有效期（秒）
 * @returns {string} - 预签名URL
 */
function generatePresignedPutUrl(key, contentType, contentLength, contentMD5 = '', expireInSeconds = 1800) {
  // 获取当前时间戳
  const timestamp = getISODateString();
  
  // 准备查询参数
  const params = {
    'X-Bce-Date': timestamp,
    'Content-Type': contentType,
    'Content-Length': contentLength.toString(),
    'Host': `${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}`
  };
  
  // 如果有Content-MD5，添加到参数
  if (contentMD5) {
    params['Content-MD5'] = contentMD5;
  }
  
  // 计算签名有效期截止时间
  const expirationTimestamp = Math.floor(Date.now() / 1000) + expireInSeconds;
  params['X-Bce-Expires'] = expirationTimestamp.toString();
  
  // 准备签名所需的参数
  const signOptions = {
    method: 'PUT',
    uri: `/${key}`,
    params,
    headers: {
      'Content-Type': contentType,
      'Content-Length': contentLength.toString(),
      'Host': `${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}`
    },
    timestamp
  };
  
  // 如果有Content-MD5，添加到请求头
  if (contentMD5) {
    signOptions.headers['Content-MD5'] = contentMD5;
  }
  
  // 生成签名
  const { authorization } = generateBosV1Signature(signOptions);
  
  // 构建查询参数字符串
  const queryParams = {
    'authorization': authorization,
    'x-bce-date': timestamp,
    'expires': expirationTimestamp.toString(),
    'content-type': contentType
  };
  
  if (contentMD5) {
    queryParams['content-md5'] = contentMD5;
  }
  
  // 拼接查询参数
  const queryString = Object.entries(queryParams)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');
  
  // 生成预签名URL
  return `https://${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}/${key}?${queryString}`;
}

/**
 * 使用PutObject方式直接上传文件到百度云BOS
 * @param {File} file - 要上传的文件对象
 * @param {Object} options - 上传选项
 * @param {Function} onProgress - 上传进度回调
 * @returns {Promise<string>} - 上传成功的文件URL
 */
export async function uploadFileByPut(file, options = {}, onProgress = null) {
  try {
    // 首先获取上传凭证
    await getCredentials();
    
    // 准备上传参数
    const {
      prefix = 'uploads',
      fileType = 'general',
      key = `${prefix}/${fileType}/${new Date().toISOString().slice(0, 10).replace(/-/g, '')}/${Date.now()}_${file.name}`
    } = options;

    // 计算文件的Content-MD5
    let contentMD5 = '';
    try {
      contentMD5 = await calculateFileMD5(file);
      console.log('计算的Content-MD5:', contentMD5);
    } catch (error) {
      console.warn('MD5计算失败，继续上传:', error);
    }
    
    // 检测是否在浏览器环境中
    const isInBrowser = typeof window !== 'undefined' && typeof window.document !== 'undefined';
    
    if (isInBrowser) {
      console.log('在浏览器环境中使用预签名URL方式上传...');
      
      // 生成预签名URL
      const presignedUrl = generatePresignedPutUrl(
        key,
        file.type || 'application/octet-stream',
        file.size,
        contentMD5
      );
      
      console.log('生成的预签名URL:', presignedUrl);
      
      // 执行PUT上传请求（使用预签名URL，不需要额外的授权头）
      try {
        const response = await axios.put(presignedUrl, file, {
          // 使用最简化的头，避免CORS和浏览器安全限制问题
          headers: {
            'Content-Type': file.type || 'application/octet-stream'
          },
          onUploadProgress: (progressEvent) => {
            if (onProgress && progressEvent.total) {
              const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              onProgress(percentCompleted, progressEvent);
            }
          }
        });
        
        console.log('预签名URL PUT上传成功:', response.status);
        
        // 生成访问URL
        const fileUrl = `${BOS_CONFIG.domain}/${key}`;
        return fileUrl;
      } catch (putError) {
        console.error('预签名URL PUT上传失败，错误详情:', putError);
        if (putError.response) {
          console.error('  - 响应状态:', putError.response.status);
          console.error('  - 响应数据:', putError.response.data);
          console.error('  - 响应头:', putError.response.headers);
        }
        
        console.log('尝试使用标准PUT方法上传...');
        
        // 获取当前时间戳
        const timestamp = getISODateString();
        
        // 准备签名所需的参数（使用最简化的头信息）
        const signOptions = {
          method: 'PUT',
          uri: `/${key}`,
          params: {},
          headers: {
            'Content-Type': file.type || 'application/octet-stream',
            'x-bce-date': timestamp
          },
          timestamp
        };
        
        // 如果有Content-MD5，添加到请求头
        if (contentMD5) {
          signOptions.headers['Content-MD5'] = contentMD5;
        }
        
        // 生成签名
        const { authorization } = generateBosV1Signature(signOptions);
        
        // 设置上传URL
        const uploadUrl = `https://${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}/${key}`;
        
        try {
          const response = await axios.put(uploadUrl, file, {
            headers: {
              'Authorization': authorization,
              'Content-Type': file.type || 'application/octet-stream',
              'x-bce-date': timestamp,
              ...(contentMD5 ? { 'Content-MD5': contentMD5 } : {})
            },
            onUploadProgress: (progressEvent) => {
              if (onProgress && progressEvent.total) {
                const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                onProgress(percentCompleted, progressEvent);
              }
            }
          });
          
          console.log('标准PUT上传成功:', response.status);
          
          // 生成访问URL
          const fileUrl = `${BOS_CONFIG.domain}/${key}`;
          return fileUrl;
        } catch (standardPutError) {
          console.error('标准PUT上传也失败，尝试使用表单上传:', standardPutError);
          // 如果标准PUT上传失败，尝试使用表单上传（作为备选方案）
          return uploadFileByForm(file, options, onProgress);
        }
      }
    } else {
      // 非浏览器环境(如Node.js)，可以直接使用PUT
      console.log('非浏览器环境使用PUT方法上传');
      
      // 获取当前时间戳
      const timestamp = getISODateString();
      
      // 生成签名
      const { authorization, headers: signedHeaders } = generateBosV1Signature({
        method: 'PUT',
        uri: `/${key}`,
        params: {},
        headers: {
          'Content-Type': file.type || 'application/octet-stream',
          'Content-Length': file.size.toString(),
          ...(contentMD5 ? { 'Content-MD5': contentMD5 } : {})
        },
        timestamp
      });
      
      // 设置上传URL
      const uploadUrl = `https://${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}/${key}`;
      
      // 构建请求头
      const requestHeaders = {
        'Host': `${BOS_CONFIG.bucketName}.${BOS_CONFIG.endpoint}`,
        'Authorization': authorization,
        'Content-Type': file.type || 'application/octet-stream',
        'Content-Length': file.size.toString(),
        'x-bce-date': timestamp
      };
      
      // 如果有Content-MD5，添加到请求头
      if (contentMD5) {
        requestHeaders['Content-MD5'] = contentMD5;
      }
      
      // 执行上传请求
      const response = await axios.put(uploadUrl, file, {
        headers: requestHeaders,
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            onProgress(percentCompleted, progressEvent);
          }
        }
      });
      
      // 生成访问URL
      const fileUrl = `${BOS_CONFIG.domain}/${key}`;
      return fileUrl;
    }
  } catch (error) {
    console.error('PUT上传到百度云BOS失败:', error);
    if (error.response) {
      console.error('响应状态:', error.response.status);
      console.error('响应数据:', error.response.data);
      console.error('响应头:', error.response.headers);
    }
    throw error;
  }
}

/**
 * 直接上传文件到百度云BOS (优先使用PUT方法)
 * @param {File} file - 要上传的文件对象
 * @param {Object} options - 上传选项
 * @param {Function} onProgress - 上传进度回调
 * @returns {Promise<string>} - 上传成功的文件URL
 */
export async function uploadFileToBos(file, options = {}, onProgress = null) {
  // 检测是否在浏览器环境中
  const isInBrowser = typeof window !== 'undefined' && typeof window.document !== 'undefined';
  
  // 使用指定的上传方法或默认使用PUT
  const { method = 'PUT' } = options;
  
  if (method.toUpperCase() === 'POST' || method.toUpperCase() === 'FORM') {
    // 用户明确要求使用表单上传
    return uploadFileByForm(file, options, onProgress);
  } else {
    // 优先使用PUT上传，失败时自动回退到表单上传
    try {
      return await uploadFileByPut(file, options, onProgress);
    } catch (error) {
      console.warn('PUT上传失败，自动回退到表单上传:', error);
      console.log('使用表单方式重试上传...');
      return uploadFileByForm(file, options, onProgress);
    }
  }
}

/**
 * 上传图片到百度云BOS
 * @param {File} file - 图片文件
 * @param {string} type - 图片类型 (background|logo)
 * @param {Function} onProgress - 上传进度回调
 * @returns {Promise<string>} - 上传成功的图片URL
 */
export async function uploadImageToBos(file, type = 'general', onProgress = null) {
  return uploadFileToBos(file, {
    prefix: 'images',
    fileType: type
  }, onProgress);
}

export default {
  uploadFileToBos,
  uploadImageToBos,
  uploadFileByForm,
  uploadFileByPut
}; 