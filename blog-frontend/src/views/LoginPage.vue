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
import api from '../services/api';
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
      
      console.log('로그인 시도:', this.loginForm.username);
      
      try {
        const response = await api.auth.login({
          username: this.loginForm.username,
          password: this.loginForm.password
        });
        
        console.log('로그인 응답:', response.data);
        
        // JWT 토큰 인증을 위한 처리
        if (!response.data.access || !response.data.refresh) {
          throw new Error('서버에서 인증 토큰을 받지 못했습니다.');
        }
        
        // 토큰과 사용자 이름을 로컬 스토리지에 저장
        localStorage.setItem('accessToken', response.data.access);
        localStorage.setItem('refreshToken', response.data.refresh);
        localStorage.setItem('username', this.loginForm.username);
        
        // 추가 디버깅 정보
        console.log('인증 정보 저장 완료. 액세스 토큰:', response.data.access.substring(0, 10) + '...');
        
        // 리다이렉트 처리 추가
        const redirectPath = this.$route.query.redirect || '/';
        this.$router.push(redirectPath);
      } catch (error) {
        console.error('로그인 실패:', error);
        
        if (error.response) {
          console.error('서버 응답:', error.response.status, error.response.data);
          
          if (error.response.status === 400) {
            if (error.response.data.non_field_errors) {
              this.errorMessage = error.response.data.non_field_errors[0];
            } else {
              this.errorMessage = '입력한 정보가 올바르지 않습니다. 다시 확인해주세요.';
            }
          } else if (error.response.status === 401) {
            this.errorMessage = '로그인에 실패했습니다. 사용자 이름과 비밀번호를 확인해주세요.';
          } else {
            this.errorMessage = '로그인 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
          }
        } else if (error.request) {
          this.errorMessage = '서버에 연결할 수 없습니다. 인터넷 연결을 확인하고 다시 시도해주세요.';
        } else {
          this.errorMessage = error.message || '알 수 없는 오류가 발생했습니다.';
        }
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