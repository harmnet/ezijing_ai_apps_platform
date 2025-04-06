<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <img src="/logo.png" alt="Logo" class="logo" />
        <h1>人工智能应用平台</h1>
      </div>
      <div class="login-form">
        <h2>账号登录</h2>
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名" />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码" />
        </div>
        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>
        <button class="login-btn" @click="handleLogin">登录</button>
        <div class="login-footer">
          <p>还没有账号？ <a href="#">立即注册</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    const username = ref('');
    const password = ref('');
    const rememberMe = ref(false);

    const handleLogin = () => {
      // 这里应该有实际的登录逻辑
      console.log('登录信息:', {
        username: username.value,
        password: password.value,
        rememberMe: rememberMe.value
      });
      
      // 模拟登录成功后跳转到首页
      router.push('/');
    };

    return {
      username,
      password,
      rememberMe,
      handleLogin
    };
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4ecfb 100%);
}

.login-container {
  width: 400px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.login-header {
  padding: 24px;
  text-align: center;
  background-color: #f9f9f9;
  border-bottom: 1px solid #eee;
}

.logo {
  height: 60px;
  margin-bottom: 10px;
}

.login-header h1 {
  font-size: 20px;
  color: #333;
  margin: 0;
}

.login-form {
  padding: 30px;
}

.login-form h2 {
  font-size: 24px;
  color: #333;
  margin: 0 0 24px 0;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  height: 40px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0 12px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  border-color: #ba003f;
  outline: none;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember-me {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.remember-me input {
  margin-right: 8px;
}

.remember-me span {
  font-size: 14px;
  color: #666;
}

.forgot-password {
  font-size: 14px;
  color: #ba003f;
  text-decoration: none;
}

.login-btn {
  width: 100%;
  height: 44px;
  background-color: #ba003f;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #d4154f;
}

.login-footer {
  margin-top: 20px;
  text-align: center;
}

.login-footer p {
  font-size: 14px;
  color: #666;
}

.login-footer a {
  color: #ba003f;
  text-decoration: none;
  font-weight: 500;
}
</style> 