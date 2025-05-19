<template>
  <div>
    <!-- Page Header -->
    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>비밀번호 재설정</h1>
              <span class="subheading">새로운 비밀번호를 설정하세요</span>
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
              <h4 class="card-title text-center mb-4">새 비밀번호 설정</h4>
              
              <!-- Alert Messages -->
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>
              <div v-if="successMessage" class="alert alert-success">
                {{ successMessage }}
              </div>

              <!-- Form -->
              <form @submit.prevent="handleResetPassword">
                <div class="mb-3">
                  <label for="password" class="form-label">새 비밀번호</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    v-model="password"
                    placeholder="새 비밀번호를 입력하세요"
                    required
                  >
                  <div class="form-text">
                    최소 8자 이상, 영문, 숫자, 특수문자 조합으로 만들어주세요.
                  </div>
                </div>
                
                <div class="mb-4">
                  <label for="password_confirm" class="form-label">비밀번호 확인</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password_confirm"
                    v-model="passwordConfirm"
                    placeholder="비밀번호를 다시 입력하세요"
                    required
                  >
                </div>
                
                <div class="d-grid mb-3">
                  <button type="submit" class="btn btn-primary" :disabled="isSubmitting || password !== passwordConfirm">
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    비밀번호 변경하기
                  </button>
                </div>
                
                <div v-if="password !== passwordConfirm && password && passwordConfirm" class="alert alert-warning">
                  비밀번호가 일치하지 않습니다.
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
import api from '../services/api';
import { HOME_BG } from '../assets/img/placeholder.js';

export default {
  name: 'ResetPasswordPage',
  data() {
    return {
      password: '',
      passwordConfirm: '',
      isSubmitting: false,
      errorMessage: '',
      successMessage: '',
      token: '',
      uid: '',
      backgroundImage: HOME_BG
    };
  },
  created() {
    // URL에서 토큰과 UID 가져오기
    const query = this.$route.query;
    this.token = query.token || '';
    this.uid = query.uid || '';
    
    if (!this.token || !this.uid) {
      this.errorMessage = '유효하지 않은 비밀번호 재설정 링크입니다. 다시 시도해주세요.';
    }
  },
  methods: {
    async handleResetPassword() {
      if (this.password !== this.passwordConfirm) {
        this.errorMessage = '비밀번호가 일치하지 않습니다.';
        return;
      }
      
      if (!this.token || !this.uid) {
        this.errorMessage = '유효하지 않은 비밀번호 재설정 링크입니다. 다시 시도해주세요.';
        return;
      }
      
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        await api.auth.resetPassword({
          token: this.token,
          uid: this.uid,
          new_password: this.password
        });
        
        this.successMessage = '비밀번호가 성공적으로 변경되었습니다. 잠시 후 로그인 페이지로 이동합니다.';
        this.password = '';
        this.passwordConfirm = '';
        
        // 성공 후 로그인 페이지로 이동
        setTimeout(() => {
          this.$router.push('/login');
        }, 3000);
      } catch (error) {
        console.error('비밀번호 재설정 실패:', error);
        this.handleError(error);
      } finally {
        this.isSubmitting = false;
      }
    },
    
    handleError(error) {
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
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
}
</style> 