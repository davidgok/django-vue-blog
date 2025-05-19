<template>
  <div>
    <!-- Page Header -->
    <header v-if="post" class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="post-heading">
              <h1>{{ post.title }}</h1>
              <h2 v-if="post.subtitle" class="subheading">{{ post.subtitle }}</h2>
              <span class="meta">
                Posted by {{ post.author?.username || '익명' }} on {{ formatDate(post.created_at) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Loading Indicator -->
    <div v-if="loading" class="container px-4 px-lg-5 mt-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-7 text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-else-if="error" class="container px-4 px-lg-5 mt-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-7">
          <div class="alert alert-danger">
            {{ error }}
          </div>
        </div>
      </div>
    </div>

    <!-- Post Content -->
    <article v-else-if="post" class="mb-4">
      <div class="container px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="mb-3">
              <span class="badge bg-info me-2">{{ post.category_name }}</span>
            </div>
            <div class="post-content" v-html="post.content"></div>
          </div>
        </div>
      </div>
    </article>

    <!-- Comments Section -->
    <section v-if="post" class="mb-5">
      <div class="container px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="card bg-light">
              <div class="card-body">
                <!-- Comment form -->
                <form class="mb-4">
                  <textarea class="form-control" rows="3" placeholder="댓글을 남겨보세요!"></textarea>
                </form>
                <!-- Comments will appear here -->
                <div class="text-center fst-italic text-muted">
                  아직 댓글이 없습니다. 첫 댓글을 남겨보세요!
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import api from '../services/api';
import { POST_BG } from '../assets/img/placeholder.js';

export default {
  data() {
    return {
      post: null,
      loading: true,
      error: null,
      backgroundImage: POST_BG
    }
  },
  created() {
    this.fetchPost();
  },
  methods: {
    async fetchPost() {
      try {
        this.loading = true;
        const slug = this.$route.params.slug;
        const response = await api.posts.get(slug);
        this.post = response.data;
      } catch (error) {
        console.error('게시글을 불러오는데 실패했습니다:', error);
        this.error = '게시글을 불러오는데 실패했습니다.';
      } finally {
        this.loading = false;
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

<style scoped>
.post-content {
  margin-top: 20px;
  line-height: 1.6;
}
</style> 