<template>
  <div>
    <!-- Page Header -->
    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>회원가입</h1>
              <span class="subheading">블로그에 가입하고 다양한 기능을 이용하세요</span>
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
              <div v-if="successMessage" class="alert alert-success">
                {{ successMessage }}
              </div>
              <form @submit.prevent="handleRegister">
                <div class="form-floating mb-3">
                  <input 
                    type="text" 
                    class="form-control" 
                    id="username" 
                    v-model="registerForm.username" 
                    placeholder="사용자 이름"
                    required
                  >
                  <label for="username">사용자 이름</label>
                  <div class="form-text">영문, 숫자, 밑줄(_)만 사용 가능합니다.</div>
                </div>
                <div class="form-floating mb-3">
                  <input 
                    type="email" 
                    class="form-control" 
                    id="email" 
                    v-model="registerForm.email" 
                    placeholder="이메일 주소"
                    required
                  >
                  <label for="email">이메일 주소</label>
                </div>
                <div class="form-floating mb-3">
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="registerForm.password" 
                    placeholder="비밀번호"
                    required
                  >
                  <label for="password">비밀번호</label>
                  <div class="form-text">8자 이상의 문자, 숫자, 특수문자를 포함해야 합니다.</div>
                </div>
                <div class="form-floating mb-3">
                  <input 
                    type="password" 
                    class="form-control" 
                    id="passwordConfirm" 
                    v-model="registerForm.passwordConfirm" 
                    placeholder="비밀번호 확인"
                    required
                  >
                  <label for="passwordConfirm">비밀번호 확인</label>
                </div>
                <div class="form-check mb-3">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    id="termsAgreed" 
                    v-model="registerForm.termsAgreed"
                    required
                  >
                  <label class="form-check-label" for="termsAgreed">
                    <router-link to="/terms" class="text-decoration-none" target="_blank">이용약관</router-link>에 동의합니다
                  </label>
                </div>
                <div class="d-grid">
                  <button 
                    class="btn btn-primary btn-lg" 
                    type="submit"
                    :disabled="isLoading"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    회원가입
                  </button>
                </div>
                <hr class="my-4">
                <div class="text-center">
                  <router-link to="/login" class="small text-decoration-none">이미 계정이 있으신가요? 로그인</router-link>
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
import { ABOUT_BG } from '../assets/img/placeholder.js';

export default {
  name: 'RegisterPage',
  data() {
    return {
      registerForm: {
        username: '',
        email: '',
        password: '',
        passwordConfirm: '',
        termsAgreed: false
      },
      isLoading: false,
      errorMessage: '',
      successMessage: '',
      backgroundImage: ABOUT_BG
    }
  },
  methods: {
    async handleRegister() {
      // 기본 유효성 검사
      if (this.registerForm.password !== this.registerForm.passwordConfirm) {
        this.errorMessage = '비밀번호가 일치하지 않습니다.';
        return;
      }
      
      this.isLoading = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        // Django REST 회원가입 API를 호출
        await axios.post('http://localhost:8001/api/auth/register/', {
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password
        });
        
        // 성공 메시지 표시
        this.successMessage = '회원가입이 완료되었습니다. 잠시 후 로그인 페이지로 이동합니다.';
        
        // 3초 후에 로그인 페이지로 리다이렉트
        setTimeout(() => {
          this.$router.push('/login');
        }, 3000);
      } catch (error) {
        console.error('회원가입 실패:', error);
        if (error.response && error.response.data) {
          // 서버에서 반환한 에러 메시지 표시
          const errorData = error.response.data;
          if (errorData.username) {
            this.errorMessage = `사용자 이름 오류: ${errorData.username[0]}`;
          } else if (errorData.email) {
            this.errorMessage = `이메일 오류: ${errorData.email[0]}`;
          } else if (errorData.password) {
            this.errorMessage = `비밀번호 오류: ${errorData.password[0]}`;
          } else {
            this.errorMessage = '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.';
          }
        } else {
          this.errorMessage = '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.';
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

.form-text {
  font-size: 0.8rem;
  color: #6c757d;
}
</style> 