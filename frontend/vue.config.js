module.exports = {
  devServer: {
    port: 8018,
    open: false,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:9000',
        changeOrigin: true,
        secure: false,
        ws: false,
        pathRewrite: {
          '^/api': '/api' // 保持API路径不变
        },
        onProxyReq: function(proxyReq, req, res) {
          console.log('[proxy]:' + req.method + ' ' + req.url);
        },
        onProxyRes: function(proxyRes, req, res) {
          console.log('[proxy res]:' + proxyRes.statusCode + ' ' + req.url);
          // 为SSE响应添加特殊处理
          if ((req.url.includes('/deepseek_volcano/chat') || req.url.includes('/knowledge/chat')) && 
              req.headers['accept'] && 
              req.headers['accept'].includes('text/event-stream')) {
            console.log('[流式响应]:开始处理SSE流 ' + req.url);
            proxyRes.headers['Cache-Control'] = 'no-cache, no-transform';
            proxyRes.headers['X-Accel-Buffering'] = 'no';
            delete proxyRes.headers['Content-Length'];
          }
        },
        onError: function(err, req, res) {
          console.log('[proxy error]:' + err);
        },
        // 添加流式处理所需配置
        proxyTimeout: 3600000, // 1小时超时（毫秒）
        timeout: 3600000,      // 1小时超时（毫秒）
        buffer: false          // 禁用缓冲
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
    },
    // 添加静态资源目录配置
    static: {
      directory: __dirname + '/public',
      publicPath: '/'
    }
  },
  transpileDependencies: true,
  lintOnSave: false,
  // 添加Vue特性标志定义
  configureWebpack: {
    plugins: [
      // 使用DefinePlugin定义特性标志
      new (require('webpack').DefinePlugin)({
        __VUE_PROD_DEVTOOLS__: false,
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
      })
    ]
  }
} 