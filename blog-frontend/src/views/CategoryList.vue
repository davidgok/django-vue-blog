<template>
  <div>
    <!-- Page Header -->
    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>카테고리</h1>
              <span class="subheading">전체 카테고리 목록</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
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
          <div v-else-if="categories.length === 0" class="text-center my-5">
            <p class="fst-italic text-muted">아직 카테고리가 없습니다.</p>
          </div>
          <div v-else>
            <div class="card mb-4">
              <div class="card-header fw-bold">전체 카테고리</div>
              <div class="card-body">
                <ul class="list-group list-group-flush">
                  <li v-for="category in categories" :key="category.id" class="list-group-item d-flex justify-content-between align-items-center">
                    {{ category.name }}
                    <span class="badge bg-primary rounded-pill">카테고리</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';
import { ABOUT_BG } from '../assets/img/placeholder.js';

export default {
  data() {
    return {
      categories: [],
      loading: true,
      error: null,
      backgroundImage: ABOUT_BG
    }
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        this.loading = true;
        const response = await api.categories.getAll();
        this.categories = response.data;
      } catch (error) {
        console.error('카테고리 목록을 불러오는데 실패했습니다:', error);
        this.error = '카테고리 목록을 불러오는데 실패했습니다.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script> 