module.exports = {
  devServer: {
    port: 8018,
    open: false,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:9000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api' // 保持API路径不变
        }
      },
      '/aippt-api': {
        target: 'https://co.aippt.cn',
        changeOrigin: true,
        secure: true,
        pathRewrite: {
          '^/aippt-api': '/api' // 将/aippt-api重写为/api
        },
        logLevel: 'debug',
        onProxyReq: (proxyReq, req, res) => {
          console.log('【AIPPT代理请求】', new Date().toLocaleTimeString(), req.method, req.url);
          // 记录请求头部信息
          console.log('请求头:', req.headers);
        },
        onProxyRes: (proxyRes, req, res) => {
          console.log('【AIPPT代理响应】', new Date().toLocaleTimeString(), req.method, req.url, proxyRes.statusCode);
        },
        onError: (err, req, res) => {
          console.error('【AIPPT代理错误】', new Date().toLocaleTimeString(), req.method, req.url, err.message);
        }
      },
      '/aippt-proxy': {
        target: 'http://127.0.0.1:9000',  // 指向我们的后端服务
        changeOrigin: true,
        pathRewrite: {
          '^/aippt-proxy': '/aippt-proxy' // 保持路径不变
        },
        logLevel: 'debug'
      },
      '/xiaoice-api': {
        target: 'https://openapi.xiaoice.com',
        changeOrigin: true,
        ws: true, // 支持websocket
        secure: true, // 使用https
        pathRewrite: {
          '^/xiaoice-api': '' // 不保留任何前缀，直接访问目标服务器
        },
        logLevel: 'debug', // 添加调试日志
        onProxyReq: (proxyReq, req, res) => {
          // 记录代理请求详情
          console.log('【代理请求】', new Date().toLocaleTimeString(), req.method, req.url);
        },
        onProxyRes: (proxyRes, req, res) => {
          // 记录代理响应详情
          console.log('【代理响应】', new Date().toLocaleTimeString(), req.method, req.url, proxyRes.statusCode);
        },
        onError: (err, req, res) => {
          // 记录代理错误
          console.error('【代理错误】', new Date().toLocaleTimeString(), req.method, req.url, err.message);
        },
        // 添加请求超时设置
        proxyTimeout: 120000, // 120秒
        timeout: 120000 // 120秒
      }
    }
  },
  transpileDependencies: true,
  lintOnSave: false
} 