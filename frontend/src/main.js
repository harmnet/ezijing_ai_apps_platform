import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import store from './store';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
// 导入Plyr播放器
import 'plyr/dist/plyr.css';

// 配置axios
axios.defaults.baseURL = 'http://127.0.0.1:9000';
axios.defaults.timeout = 30000; // 30秒超时
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.common['Accept'] = 'application/json';
axios.defaults.withCredentials = false; // 不需要携带凭证

// 请求拦截器
axios.interceptors.request.use(
  config => {
    console.log(`发送${config.method.toUpperCase()}请求到: ${config.baseURL}${config.url}`);
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

app.use(ElementPlus)
   .use(router)
   .use(store)
   .use(Toast, toastOptions)
   .mount('#app'); 