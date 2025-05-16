<template>
  <div>
    <!-- Page Header -->
    <header class="masthead" style="background-image: url('/assets/img/home-bg.jpg')">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>비밀번호 찾기</h1>
              <span class="subheading">이메일을 입력하여 비밀번호 재설정 링크를 받으세요</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="container px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-sm">
            <div class="card-body p-4">
              <h4 class="card-title text-center mb-4">비밀번호 찾기</h4>
              
              <!-- Alert Messages -->
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>
              <div v-if="successMessage" class="alert alert-success">
                {{ successMessage }}
              </div>

              <!-- Form -->
              <form @submit.prevent="handleForgotPassword">
                <div class="mb-3">
                  <label for="email" class="form-label">이메일</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="email"
                    placeholder="가입한 이메일 주소를 입력하세요"
                    required
                  >
                  <div class="form-text">
                    가입시 사용한 이메일 주소를 입력하면 비밀번호 재설정 링크를 보내드립니다.
                  </div>
                </div>
                
                <div class="d-grid mb-3">
                  <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    비밀번호 재설정 링크 전송
                  </button>
                </div>
                
                <div class="text-center">
                  <router-link to="/login" class="text-decoration-none">로그인 페이지로 돌아가기</router-link>
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

export default {
  name: 'ForgotPasswordPage',
  data() {
    return {
      email: '',
      isSubmitting: false,
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async handleForgotPassword() {
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        await axios.post('http://localhost:8001/api/auth/password-reset/', {
          email: this.email
        });
        
        this.successMessage = '비밀번호 재설정 링크가 이메일로 전송되었습니다. 받은편지함을 확인해주세요.';
        this.email = '';
      } catch (error) {
        console.error('비밀번호 찾기 요청 실패:', error);
        
        if (error.response && error.response.data) {
          // 서버에서 반환한 에러 메시지 표시
          if (typeof error.response.data === 'object') {
            const messages = [];
            for (const field in error.response.data) {
              messages.push(`${field}: ${error.response.data[field]}`);
            }
            this.errorMessage = messages.join('\n');
          } else {
            this.errorMessage = error.response.data;
          }
        } else {
          this.errorMessage = '서버와 통신 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
}
</style> 