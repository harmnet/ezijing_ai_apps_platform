import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
// 导入我们自定义的主题CSS，放在Element Plus的CSS之后以覆盖其样式
import './assets/theme.css';
// 导入通用组件样式
import './assets/styles/common-components.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import store from './store';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
// 导入Plyr播放器
import 'plyr/dist/plyr.css';

// 配置全局变量
window.APP_CONFIG = {
  // API地址 - 生产环境使用相对路径，方便Nginx代理
  API_BASE_URL: '',
  // 前端地址 - 通过当前域名动态获取，避免硬编码
  APP_BASE_URL: window.location.origin
};

// 配置axios - 使用相对路径以利用Vue代理
axios.defaults.baseURL = window.APP_CONFIG.API_BASE_URL;  // 不设置baseURL，使用相对路径
axios.defaults.timeout = 120000; // 120秒超时
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.common['Accept'] = 'application/json';
axios.defaults.withCredentials = false; // 不需要携带凭证

// 请求拦截器
axios.interceptors.request.use(
  config => {
    console.log(`发送${config.method.toUpperCase()}请求到: ${config.url}`);
    return config;
  },
  error => {
    console.error('请求拦截器错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
axios.interceptors.response.use(
  response => {
    console.log(`收到响应: ${response.status} ${response.statusText}`);
    return response;
  },
  error => {
    console.error('响应拦截器错误:', error);
    return Promise.reject(error);
  }
);

// Toast配置
const toastOptions = {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
};

const app = createApp(App);

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 临时禁用水合不匹配警告（仅用于开发阶段调试）
// 注意：在生产环境中，应该修复水合不匹配问题而不是禁用警告
if (process.env.NODE_ENV !== 'production') {
  app.config.warnHandler = (msg, instance, trace) => {
    // 过滤掉水合不匹配警告
    if (msg.includes('Hydration') || msg.includes('hydration')) {
      return;
    }
    // 其他警告正常显示
    console.warn(`[Vue warn]: ${msg}${trace ? `\nTrace: ${trace}` : ''}`);
  };
}

app.use(ElementPlus)
   .use(router)
   .use(store)
   .use(Toast, toastOptions)
   .mount('#app'); 