<template>
  <div>
    <!-- Page Header -->
    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>로그인</h1>
              <span class="subheading">계정에 로그인하여 블로그를 이용하세요</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="container px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card my-5">
            <div class="card-body p-4 p-lg-5">
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>
              <form @submit.prevent="handleLogin">
                <div class="form-floating mb-3">
                  <input 
                    type="text" 
                    class="form-control" 
                    id="username" 
                    v-model="loginForm.username" 
                    placeholder="사용자 이름"
                    required
                  >
                  <label for="username">사용자 이름</label>
                </div>
                <div class="form-floating mb-3">
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="loginForm.password" 
                    placeholder="비밀번호"
                    required
                  >
                  <label for="password">비밀번호</label>
                </div>
                <div class="form-check mb-3">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="rememberMe" 
                    v-model="loginForm.rememberMe"
                  >
                  <label class="form-check-label" for="rememberMe">
                    로그인 상태 유지
                  </label>
                </div>
                <div class="d-grid">
                  <button 
                    class="btn btn-primary btn-lg" 
                    type="submit"
                    :disabled="isLoading"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    로그인
                  </button>
                </div>
                <hr class="my-4">
                <div class="text-center">
                  <router-link to="/forgot-password" class="small text-decoration-none">비밀번호를 잊으셨나요?</router-link>
                </div>
                <div class="text-center mt-2">
                  <router-link to="/register" class="small text-decoration-none">계정이 없으신가요? 회원가입</router-link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { HOME_BG } from '../assets/img/placeholder.js';

export default {
  name: 'LoginPage',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        rememberMe: false
      },
      isLoading: false,
      errorMessage: '',
      backgroundImage: HOME_BG
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        // Django REST 인증 API를 호출
        const response = await axios.post('http://localhost:8001/api/auth/login/', {
          username: this.loginForm.username,
          password: this.loginForm.password
        });
        
        // 토큰을 로컬 스토리지에 저장
        localStorage.setItem('token', response.data.token);
        
        // 성공 시 홈 페이지로 리다이렉트
        this.$router.push('/');
      } catch (error) {
        console.error('로그인 실패:', error);
        this.errorMessage = '사용자 이름 또는 비밀번호가 올바르지 않습니다.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style> 