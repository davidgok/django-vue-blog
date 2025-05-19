<template>
    <div>    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">      <div class="container position-relative px-4 px-lg-5">        <div class="row gx-4 gx-lg-5 justify-content-center">          <div class="col-md-10 col-lg-8 col-xl-7">            <div class="page-heading">              <h1>카테고리 관리</h1>              <span class="subheading">블로그 카테고리를 관리하세요</span>            </div>          </div>        </div>      </div>    </header>    <div class="container px-4 px-lg-5">      <div class="row gx-4 gx-lg-5 justify-content-center">        <div class="col-md-10 col-lg-8 col-xl-7">
          <div v-if="errorMessage" class="alert alert-danger mb-4">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="alert alert-success mb-4">
            {{ successMessage }}
          </div>

          <!-- 카테고리 관리 -->
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0"><i class="fas fa-tags me-2"></i> 카테고리 관리</h5>
            </div>
            <div class="card-body">
              <!-- 카테고리 추가 폼 -->
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <div class="d-flex align-items-center">
                    <i class="fas fa-plus me-2"></i>
                    <strong>카테고리 추가</strong>
                    <span class="ms-auto">{{ newCategory.name.length }} / 100</span>
                  </div>
                </div>
                <div class="card-body">
                  <form @submit.prevent="validateAndAddCategory">
                    <div class="mb-3">
                      <label for="categoryName" class="form-label">카테고리 이름</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        id="categoryName" 
                        v-model.trim="newCategory.name" 
                        placeholder="새 카테고리 이름을 입력하세요"
                        required
                      >
                    </div>
                    <div class="mb-3">
                      <label for="categorySlug" class="form-label">슬러그 (URL)</label>
                      <div class="input-group">
                        <input 
                          type="text" 
                          class="form-control" 
                          id="categorySlug" 
                          v-model.trim="newCategory.slug" 
                          placeholder="category-slug"
                          aria-describedby="slugHelp"
                          required
                        >
                        <button 
                          @click.prevent="generateSlug" 
                          type="button" 
                          class="btn btn-outline-secondary"
                        >
                          자동 생성
                        </button>
                      </div>
                      <div id="slugHelp" class="form-text">
                        URL에 사용될 영문 식별자입니다. 입력하지 않으면 자동으로 생성됩니다.
                      </div>
                    </div>
                    <button 
                      type="submit" 
                      class="btn btn-primary" 
                      :disabled="isLoading || !newCategory.name.trim()"
                    >
                      <span v-if="isLoading" class="spinner-border spinner-border-sm me-1"></span>
                      카테고리 추가
                    </button>
                  </form>
                </div>
              </div>

              <!-- 기존 카테고리 목록 -->
              <div v-if="isLoading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">카테고리 정보를 불러오는 중입니다...</p>
              </div>
              
              <div v-else>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="mb-0">카테고리 목록</h5>
                  <span class="badge bg-primary">{{ categories.length }}개</span>
                </div>
                
                <div v-if="categories.length === 0" class="alert alert-info">
                  <i class="fas fa-info-circle me-2"></i>
                  등록된 카테고리가 없습니다. 위 폼을 통해 새 카테고리를 추가해보세요.
                </div>
                
                <div v-else class="list-group mb-4">
                  <div 
                    v-for="category in categories" 
                    :key="category.id" 
                    class="list-group-item"
                  >
                    <div v-if="category.isEditing">
                      <!-- 편집 모드 -->
                      <div class="mb-3">
                        <label class="form-label">카테고리 이름</label>
                        <input 
                          type="text" 
                          class="form-control" 
                          v-model="category.editName"
                        >
                      </div>
                      <div class="mb-3">
                        <label class="form-label">슬러그 (URL)</label>
                        <input 
                          type="text" 
                          class="form-control" 
                          v-model="category.editSlug"
                          disabled
                        >
                        <div class="form-text">슬러그는 변경할 수 없습니다.</div>
                      </div>
                      <div>
                        <button @click="saveCategory(category)" class="btn btn-success btn-sm me-2">
                          <i class="fas fa-check me-1"></i> 저장
                        </button>
                        <button @click="cancelEdit(category)" class="btn btn-secondary btn-sm">
                          <i class="fas fa-times me-1"></i> 취소
                        </button>
                      </div>
                    </div>
                    <div v-else>
                      <!-- 일반 모드 -->
                      <div class="d-flex justify-content-between align-items-center">
                        <div>
                          <h5 class="mb-1">{{ category.name }}</h5>
                          <p class="mb-1 text-muted small">
                            <span class="fst-italic">/{{ category.slug }}</span>
                          </p>
                        </div>
                        <div>
                          <button @click="startEdit(category)" class="btn btn-outline-secondary btn-sm me-2">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button @click="deleteCategory(category.id)" class="btn btn-outline-danger btn-sm">
                            <i class="fas fa-trash"></i>
                          </button>
                        </div>
                      </div>
                      <div class="mt-2">
                        <span class="badge bg-light text-dark">글 0개</span>
                      </div>
                    </div>
                  </div>
                </div>
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
import { POST_BG } from '../assets/img/placeholder.js';
import slugify from '../utils/slugify';

export default {
  name: 'CategoryManagePage',
  data() {
    return {
      categories: [],
      newCategory: {
        name: '',
        slug: ''
      },
      isLoading: false,
      errorMessage: '',
      successMessage: '',
      backgroundImage: POST_BG
    };
  },
  created() {
    this.checkAuthentication();
    this.fetchCategories();
  },
  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        this.$router.push('/login');
        return false;
      }
      return true;
    },
    async fetchCategories() {
      try {
        this.isLoading = true;
        const response = await api.categories.getAll();
        this.categories = response.data.map(category => ({
          ...category,
          isEditing: false,
          editName: category.name,
          editSlug: category.slug
        }));
      } catch (error) {
        console.error('카테고리를 불러오는데 실패했습니다:', error);
        this.errorMessage = '카테고리를 불러오는데 실패했습니다. 나중에 다시 시도해주세요.';
      } finally {
        this.isLoading = false;
      }
    },
    generateSlug() {
      if (this.newCategory.name.trim()) {
        this.newCategory.slug = slugify(this.newCategory.name, 'category');
      } else {
        this.errorMessage = '카테고리 이름을 먼저 입력해주세요.';
      }
    },
    startEdit(category) {
      category.isEditing = true;
      category.editName = category.name;
      category.editSlug = category.slug;
    },
    cancelEdit(category) {
      category.isEditing = false;
    },
    async saveCategory(category) {
      if (!category.editName.trim()) return;
      
      try {
        this.startLoading();
        
        const response = await api.categories.update(category.slug, {
          name: category.editName,
          slug: category.slug
        });
        
        category.name = response.data.name;
        category.isEditing = false;
        
        this.successMessage = '카테고리가 성공적으로 수정되었습니다.';
      } catch (error) {
        this.handleError(error, '카테고리 수정 실패');
      } finally {
        this.finishLoading();
      }
    },
    async deleteCategory(categoryId) {
      if (!confirm('이 카테고리를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
        return;
      }
      
      try {
        this.startLoading();
        
        const category = this.categories.find(c => c.id === categoryId);
        if (!category) return;
        
        await api.categories.delete(category.slug);
        
        this.categories = this.categories.filter(c => c.id !== categoryId);
        this.successMessage = '카테고리가 성공적으로 삭제되었습니다.';
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = '이 카테고리에 연결된 글이 있어 삭제할 수 없습니다.';
        } else {
          this.errorMessage = '카테고리 삭제 중 오류가 발생했습니다.';
        }
      } finally {
        this.finishLoading();
      }
    },
    async validateAndAddCategory() {
      if (!this.newCategory.name.trim()) {
        this.errorMessage = '카테고리 이름을 입력해주세요.';
        return;
      }
      
      try {
        this.startLoading();
        
        if (!this.checkAuthentication()) return;
        
        // 카테고리 생성 데이터
        const categoryData = {
          name: this.newCategory.name.trim(),
          slug: this.newCategory.slug || '' // 자동 생성될 수 있음
        };
        
        // API 서비스의 categories.create 함수 사용
        const response = await api.categories.create(categoryData);
        
        // 새 카테고리를 목록에 추가
        this.categories.push({
          ...response.data,
          isEditing: false,
          editName: response.data.name,
          editSlug: response.data.slug
        });
        
        // 폼 초기화
        this.newCategory = {
          name: '',
          slug: ''
        };
        
        this.successMessage = '카테고리가 성공적으로 추가되었습니다.';
      } catch (error) {
        console.error('카테고리 추가 실패:', error);
        this.handleError(error, '카테고리 추가 실패');
      } finally {
        this.finishLoading();
      }
    },
    // 공통으로 사용되는 유틸리티 메서드들
    startLoading() {
      this.isLoading = true;
      this.errorMessage = '';
      this.successMessage = '';
    },
    finishLoading() {
      this.isLoading = false;
    },
    handleError(error, prefix = '오류') {
      console.error(`${prefix}:`, error);
      
      if (error.response && error.response.data) {
        console.error('서버 응답 데이터:', error.response.data);
        
        if (typeof error.response.data === 'object') {
          const messages = [];
          for (const field in error.response.data) {
            if (field === 'slug') {
              messages.push(`슬러그(URL): ${error.response.data[field]}`);
            } else if (field === 'name') {
              messages.push(`카테고리 이름: ${error.response.data[field]}`);
            } else {
              messages.push(`${field}: ${error.response.data[field]}`);
            }
          }
          this.errorMessage = messages.join(' / ');
        } else {
          this.errorMessage = '서버 오류: ' + error.response.data;
        }
      } else if (error.message) {
        this.errorMessage = error.message;
      } else {
        this.errorMessage = '알 수 없는 오류가 발생했습니다. 다시 시도해주세요.';
      }
    }
  }
}
</script>

<style scoped>
.list-group-item {
  transition: background-color 0.2s;
  margin-bottom: 0.5rem;
  border-radius: 0.25rem;
}
.list-group-item:hover {
  background-color: #f8f9fa;
}
</style> 