<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
      <div class="container px-4 px-lg-5">
        <router-link class="navbar-brand" to="/">블로그</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          메뉴
          <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ms-auto py-4 py-lg-0">
            <li class="nav-item"><router-link class="nav-link px-lg-3 py-3 py-lg-4" to="/">홈</router-link></li>
            <li class="nav-item"><router-link class="nav-link px-lg-3 py-3 py-lg-4" to="/categories">카테고리</router-link></li>
            
            <!-- 로그인한 사용자 메뉴 -->
            <template v-if="isLoggedIn">
              <li class="nav-item"><router-link class="nav-link px-lg-3 py-3 py-lg-4" to="/write">글 작성</router-link></li>
              <li class="nav-item"><router-link class="nav-link px-lg-3 py-3 py-lg-4" to="/manage">관리</router-link></li>
              <li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="#" @click.prevent="logout">로그아웃</a></li>
            </template>
            
            <!-- 로그인하지 않은 사용자 메뉴 -->
            <template v-else>
              <li class="nav-item"><router-link class="nav-link px-lg-3 py-3 py-lg-4" to="/login">로그인</router-link></li>
              <li class="nav-item"><router-link class="nav-link px-lg-3 py-3 py-lg-4" to="/register">회원가입</router-link></li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
    
    <!-- Page Content -->
    <router-view/>
    
    <!-- Footer -->
    <footer class="border-top">
      <div class="container px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <ul class="list-inline text-center">
              <li class="list-inline-item">
                <a href="#!">
                  <span class="fa-stack fa-lg">
                    <i class="fas fa-circle fa-stack-2x"></i>
                    <i class="fab fa-twitter fa-stack-1x fa-inverse"></i>
                  </span>
                </a>
              </li>
              <li class="list-inline-item">
                <a href="#!">
                  <span class="fa-stack fa-lg">
                    <i class="fas fa-circle fa-stack-2x"></i>
                    <i class="fab fa-facebook-f fa-stack-1x fa-inverse"></i>
                  </span>
                </a>
              </li>
              <li class="list-inline-item">
                <a href="#!">
                  <span class="fa-stack fa-lg">
                    <i class="fas fa-circle fa-stack-2x"></i>
                    <i class="fab fa-github fa-stack-1x fa-inverse"></i>
                  </span>
                </a>
              </li>
            </ul>
            <div class="small text-center text-muted fst-italic">Copyright &copy; Your Website 2023</div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import initNavbarScroll from './assets/scripts.js';

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false
    };
  },
  mounted() {
    initNavbarScroll();
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      // 로컬 스토리지에서 토큰 확인
      const token = localStorage.getItem('token');
      this.isLoggedIn = !!token;
    },
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      this.isLoggedIn = false;
      // 로그아웃 후 홈페이지로 이동
      this.$router.push('/');
    }
  },
  watch: {
    // 라우트 변경 시마다 로그인 상태 확인
    '$route'() {
      this.checkLoginStatus();
    }
  }
}
</script>

<style>
/* 전역 스타일은 assets/styles.css에 있습니다 */
</style>
