<template>
  <div>
    <!-- Page Header-->
    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>{{ blogSettings.title }}</h1>
              <span class="subheading">{{ blogSettings.subtitle }}</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content-->
    <div class="container px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-7">
          <div v-if="loading" class="text-center my-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-else-if="error" class="alert alert-danger">
            {{ error }}
          </div>
          <div v-else>
            <!-- Post preview -->
            <div v-for="post in posts" :key="post.id" class="post-preview">
              <router-link :to="`/post/${post.slug}`">
                <h2 class="post-title">{{ post.title }}</h2>
                <h3 v-if="post.subtitle" class="post-subtitle">{{ post.subtitle }}</h3>
              </router-link>
              <p class="post-meta">
                게시일
                <a href="#!">{{ post.author ? post.author.username : '익명' }}</a>
                {{ formatDate(post.created_at) }}
                카테고리: {{ post.category_name }}
              </p>
              <hr class="my-4" />
            </div>
            
            <!-- Pager -->
            <div class="d-flex justify-content-end mb-4">
              <a class="btn btn-primary text-uppercase" href="#!">과거 게시물 →</a>
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
  data() {
    return {
      posts: [],
      loading: true,
      error: null,
      backgroundImage: HOME_BG,
      blogSettings: {
        title: '블로그',
        subtitle: ''
      }
    }
  },
  created() {
    this.fetchPosts();
    this.fetchBlogSettings();
  },
  methods: {
    async fetchPosts() {
      try {
        this.loading = true;
        const response = await axios.get('http://localhost:8001/api/posts/');
        this.posts = response.data;
        this.loading = false;
      } catch (error) {
        console.error('글 목록을 불러오는데 실패했습니다:', error);
        this.error = '게시글 목록을 불러오는데 실패했습니다.';
        this.loading = false;
      }
    },
    async fetchBlogSettings() {
      try {
        const response = await axios.get('http://localhost:8001/api/settings/');
        // API에서 반환한 설정값으로 업데이트
        this.blogSettings = response.data;
      } catch (error) {
        console.error('블로그 설정을 불러오는데 실패했습니다:', error);
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
}
</script> 