import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null,
    isAuthenticated: false,
    token: localStorage.getItem('token') || '',
    apps: []
  },
  getters: {
    getUser: state => state.user,
    isAuthenticated: state => state.isAuthenticated,
    getApps: state => state.apps
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      state.isAuthenticated = !!user;
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    logout(state) {
      state.user = null;
      state.isAuthenticated = false;
      state.token = '';
      localStorage.removeItem('token');
    },
    setApps(state, apps) {
      state.apps = apps;
    }
  },
  actions: {
    // 登录
    login({ commit }, { token, user }) {
      commit('setToken', token);
      commit('setUser', user);
    },
    // 退出登录
    logout({ commit }) {
      commit('logout');
    },
    // 获取应用列表
    fetchApps({ commit }) {
      // 这里通常会调用API
      // 示例：
      // const response = await api.getApps();
      // commit('setApps', response.data);
      
      // 临时模拟数据
      const mockApps = [
        { id: 1, name: '示例应用1', description: '这是一个示例应用' },
        { id: 2, name: '示例应用2', description: '这是另一个示例应用' }
      ];
      commit('setApps', mockApps);
    }
  },
  modules: {
    // 可以添加模块化的store
  }
}); 