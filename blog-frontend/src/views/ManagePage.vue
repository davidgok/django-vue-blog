<template>
  <div>
    <!-- 페이지 헤더 -->
    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>블로그 관리</h1>
              <span class="subheading">블로그 설정 및 콘텐츠를 관리하세요</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 메인 컨텐츠 -->
    <div class="container px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5">
        <!-- 사이드바 메뉴 -->
        <div class="col-lg-3 mb-4">
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white">
              <i class="fas fa-cogs me-2"></i> 관리 메뉴
            </div>
            <div class="list-group list-group-flush">
              <a 
                href="#" 
                @click.prevent="setActivePage('dashboard')" 
                :class="['list-group-item list-group-item-action', activePage === 'dashboard' ? 'active' : '']"
              >
                <i class="fas fa-tachometer-alt me-2"></i> 블로그 관리 홈
              </a>
              <a 
                href="#" 
                @click.prevent="setActivePage('posts')" 
                :class="['list-group-item list-group-item-action', activePage === 'posts' ? 'active' : '']"
              >
                <i class="fas fa-file-alt me-2"></i> 글 관리
              </a>
              <a 
                href="#" 
                @click.prevent="setActivePage('categories')" 
                :class="['list-group-item list-group-item-action', activePage === 'categories' ? 'active' : '']"
              >
                <i class="fas fa-tags me-2"></i> 카테고리 관리
              </a>
              <a 
                href="#" 
                @click.prevent="setActivePage('profile')" 
                :class="['list-group-item list-group-item-action', activePage === 'profile' ? 'active' : '']"
              >
                <i class="fas fa-user me-2"></i> 프로필 설정
              </a>
              <a 
                href="#" 
                @click.prevent="setActivePage('settings')" 
                :class="['list-group-item list-group-item-action', activePage === 'settings' ? 'active' : '']"
              >
                <i class="fas fa-cog me-2"></i> 블로그 설정
              </a>
            </div>
          </div>
        </div>

        <!-- 메인 컨텐츠 영역 -->
        <div class="col-lg-9">
          <!-- 알림 메시지 -->
          <div v-if="errorMessage" class="alert alert-danger mb-4">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="alert alert-success mb-4">
            {{ successMessage }}
          </div>

          <!-- 대시보드 -->
          <div v-if="activePage === 'dashboard'" class="card shadow-sm mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0"><i class="fas fa-tachometer-alt me-2"></i> 블로그 현황</h5>
            </div>
            <div class="card-body">
              <!-- 로딩 중 표시 -->
              <div v-if="loadingStats" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">통계 정보를 불러오는 중입니다...</p>
              </div>
              
              <div v-else>
                <div class="row g-4">
                  <div class="col-md-4">
                    <div class="border rounded p-3 text-center">
                      <div class="display-4 text-primary mb-2">{{ stats.posts }}</div>
                      <div class="text-muted">전체 글</div>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="border rounded p-3 text-center">
                      <div class="display-4 text-success mb-2">{{ stats.categories }}</div>
                      <div class="text-muted">카테고리</div>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="border rounded p-3 text-center">
                      <div class="display-4 text-info mb-2">{{ stats.comments }}</div>
                      <div class="text-muted">댓글</div>
                    </div>
                  </div>
                </div>

                <h5 class="mt-4 mb-3">최근 활동</h5>
                
                <!-- 최근 활동이 없는 경우 -->
                <div v-if="recentActivities.length === 0" class="text-center p-4 border rounded bg-light">
                  <i class="fas fa-info-circle text-muted mb-2 fa-2x"></i>
                  <p class="text-muted mb-0">아직 활동 내역이 없습니다. 새 글을 작성하거나 카테고리를 추가해보세요!</p>
                </div>
                
                <!-- 네트워크 오류 발생 시 -->
                <div v-else-if="statsError" class="alert alert-warning">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  활동 내역을 불러오는 중 문제가 발생했습니다. <button class="btn btn-sm btn-outline-primary ms-2" @click="fetchData">다시 시도</button>
                </div>
                
                <!-- 최근 활동 목록 -->
                <ul v-else class="list-group">
                  <li v-for="(activity, index) in recentActivities" :key="index" class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <i :class="[activity.icon, 'me-2', activity.color]"></i>
                        {{ activity.text }}
                      </div>
                      <small class="text-muted">{{ activity.time }}</small>
                    </div>
                  </li>
                </ul>
                
                <!-- 카테고리별 통계 차트 (시각화 추가 옵션) -->
                <div v-if="categoryStats.length > 0" class="mt-4">
                  <h5 class="mb-3">카테고리별 글 수</h5>
                  <div class="border rounded p-3">
                    <div v-for="stat in categoryStats" :key="stat.id" class="mb-2">
                      <div class="d-flex justify-content-between mb-1">
                        <span>{{ stat.name }}</span>
                        <span class="badge bg-primary">{{ stat.post_count }}</span>
                      </div>
                      <div class="progress" style="height: 10px">
                        <div 
                          class="progress-bar" 
                          role="progressbar" 
                          :style="{ width: getPercentage(stat.post_count) + '%' }" 
                          :aria-valuenow="stat.post_count" 
                          aria-valuemin="0" 
                          :aria-valuemax="getTotalPosts()">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 글 관리 -->
          <div v-if="activePage === 'posts'" class="card shadow-sm mb-4">
            <div class="card-header bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="fas fa-file-alt me-2"></i> 글 관리</h5>
                <router-link to="/write" class="btn btn-primary btn-sm">
                  <i class="fas fa-plus me-1"></i> 새 글 작성
                </router-link>
              </div>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="input-group">
                  <input 
                    type="text" 
                    class="form-control" 
                    placeholder="글 제목 검색..." 
                    v-model="postSearchQuery"
                  >
                  <button class="btn btn-outline-secondary" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                  <button @click="refreshPosts" class="btn btn-outline-primary" type="button" :disabled="loadingPosts">
                    <i class="fas fa-sync-alt" :class="{'fa-spin': loadingPosts}"></i>
                    새로고침
                  </button>
                </div>
              </div>

              <!-- 로딩 중 표시 -->
              <div v-if="loadingPosts" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">게시물 목록을 불러오는 중입니다...</p>
              </div>
              
              <!-- 게시물이 없는 경우 -->
              <div v-else-if="posts.length === 0" class="text-center p-5 border rounded bg-light">
                <i class="fas fa-pen-fancy mb-3 text-muted" style="font-size: 2rem;"></i>
                <h5>작성한 게시물이 없습니다</h5>
                <p class="text-muted">새 글을 작성해보세요!</p>
                <router-link to="/write" class="btn btn-primary">
                  <i class="fas fa-plus me-1"></i> 첫 게시물 작성하기
                </router-link>
              </div>

              <!-- 게시물 목록 -->
              <div v-else class="table-responsive">
                <table class="table table-striped table-hover">
                  <thead>
                    <tr>
                      <th>제목</th>
                      <th>카테고리</th>
                      <th>작성일</th>
                      <th>상태</th>
                      <th>관리</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="post in filteredPosts" :key="post.id">
                      <td>{{ post.title }}</td>
                      <td>{{ post.category_name }}</td>
                      <td>{{ formatDate(post.created_at) }}</td>
                      <td>
                        <span 
                          :class="[
                            'badge', 
                            post.is_published ? 'bg-success' : 'bg-secondary'
                          ]"
                        >
                          {{ post.is_published ? '공개' : '비공개' }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <router-link :to="`/post/${post.slug}`" class="btn btn-outline-primary">
                            <i class="fas fa-eye"></i>
                          </router-link>
                          <button @click="editPost(post)" class="btn btn-outline-secondary">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button @click="deletePost(post.id)" class="btn btn-outline-danger">
                            <i class="fas fa-trash"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- 카테고리 관리 -->
          <div v-if="activePage === 'categories'" class="card shadow-sm mb-4">
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
                    <span class="ms-auto">{{ newCategoryName.length }} / 100</span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="input-group">
                    <input 
                      type="text" 
                      class="form-control" 
                      v-model="newCategoryName" 
                      placeholder="새 카테고리 이름을 입력하세요"
                      @keyup.enter="addCategory"
                    >
                    <button 
                      class="btn btn-primary" 
                      type="button" 
                      @click="addCategory"
                      :disabled="loadingCategories || !newCategoryName.trim()"
                    >
                      <span v-if="loadingCategories" class="spinner-border spinner-border-sm me-1"></span>
                      추가
                    </button>
                  </div>
                </div>
              </div>

              <!-- 기존 카테고리 목록 -->
              <div class="list-group mb-4">
                <div class="list-group-item bg-light">
                  <div class="d-flex justify-content-between align-items-center">
                    <div><strong>카테고리 이름</strong></div>
                    <div><strong>글 수</strong></div>
                    <div><strong>관리</strong></div>
                  </div>
                </div>
                <div v-for="category in categories" :key="category.id" class="list-group-item">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <i v-if="!category.isEditing" class="fas fa-tag me-2"></i>
                      <input 
                        v-if="category.isEditing" 
                        type="text" 
                        class="form-control form-control-sm" 
                        v-model="category.editName"
                      >
                      <span v-else>{{ category.name }}</span>
                    </div>
                    <div>{{ getCategoryPostCount(category.id) }}</div>
                    <div>
                      <div v-if="category.isEditing" class="btn-group btn-group-sm">
                        <button @click="saveCategory(category)" class="btn btn-success">
                          <i class="fas fa-check"></i>
                        </button>
                        <button @click="cancelEdit(category)" class="btn btn-secondary">
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                      <div v-else class="btn-group btn-group-sm">
                        <button @click="startEditCategory(category)" class="btn btn-outline-secondary">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button @click="deleteCategory(category.id)" class="btn btn-outline-danger">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 프로필 설정 -->
          <div v-if="activePage === 'profile'" class="card shadow-sm mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0"><i class="fas fa-user me-2"></i> 프로필 설정</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="updateProfile">
                <div class="mb-3">
                  <label class="form-label">사용자 이름</label>
                  <input type="text" class="form-control" v-model="profile.username">
                </div>
                <div class="mb-3">
                  <label class="form-label">이메일</label>
                  <input type="email" class="form-control" v-model="profile.email" readonly>
                  <div class="form-text">이메일 주소는 변경할 수 없습니다.</div>
                </div>
                <div class="mb-3">
                  <label class="form-label">이름</label>
                  <input type="text" class="form-control" v-model="profile.name">
                </div>
                <div class="mb-3">
                  <label class="form-label">자기 소개</label>
                  <textarea class="form-control" v-model="profile.bio" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="loadingCategories">
                  <span v-if="loadingCategories" class="spinner-border spinner-border-sm me-1"></span>
                  프로필 업데이트
                </button>
              </form>
            </div>
          </div>

          <!-- 블로그 설정 -->
          <div v-if="activePage === 'settings'" class="card shadow-sm mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0"><i class="fas fa-cog me-2"></i> 블로그 설정</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="saveSettings">
                <div class="mb-3">
                  <label class="form-label">블로그 제목</label>
                  <input type="text" class="form-control" v-model="settings.title" placeholder="블로그 제목을 입력하세요 (선택사항)">
                  <div class="form-text">비워두면 'null'로 표시됩니다.</div>
                </div>
                <div class="mb-3">
                  <label class="form-label">블로그 부제목</label>
                  <input type="text" class="form-control" v-model="settings.subtitle" placeholder="블로그 부제목을 입력하세요 (선택사항)">
                  <div class="form-text">블로그 메인 페이지에 표시될 부제목입니다. 입력하지 않으면 표시되지 않습니다.</div>
                </div>
                <div class="mb-3">
                  <label class="form-label">메인 페이지 표시 글 수</label>
                  <select class="form-select" v-model="settings.postsPerPage">
                    <option value="5">5개</option>
                    <option value="10">10개</option>
                    <option value="15">15개</option>
                    <option value="20">20개</option>
                  </select>
                </div>
                <div class="mb-3 form-check">
                  <input type="checkbox" class="form-check-input" id="allowComments" v-model="settings.allowComments">
                  <label class="form-check-label" for="allowComments">댓글 허용</label>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="loadingCategories">
                  <span v-if="loadingCategories" class="spinner-border spinner-border-sm me-1"></span>
                  설정 저장
                </button>
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
import { POST_BG } from '../assets/img/placeholder.js';
import { slugify } from '../utils/slugify';

export default {
  name: 'ManagePage',
  data() {
    return {
      activePage: 'dashboard',
      isLoading: false,
      loadingStats: false,  // 대시보드 로딩 상태
      loadingPosts: false,  // 글 목록 로딩 상태
      loadingCategories: false,  // 카테고리 로딩 상태
      statsError: false,    // 통계 로딩 에러 상태
      errorMessage: '',
      successMessage: '',
      backgroundImage: POST_BG,
      
      // 대시보드 데이터
      stats: {
        posts: 0,
        categories: 0,
        comments: 0
      },
      recentActivities: [],
      categoryStats: [], // 카테고리별 통계 정보
      
      // 글 관리 데이터
      posts: [],
      postSearchQuery: '',
      
      // 카테고리 관리 데이터
      categories: [],
      newCategoryName: '',
      
      // 프로필 설정
      profile: {
        username: '',
        email: '',
        name: '',
        bio: ''
      },
      
      // 블로그 설정
      settings: {
        title: 'Clean Blog',
        subtitle: 'A Blog Theme by Start Bootstrap',
        postsPerPage: '10',
        allowComments: true
      }
    };
  },
  computed: {
    filteredPosts() {
      if (!this.postSearchQuery) {
        return this.posts;
      }
      
      const query = this.postSearchQuery.toLowerCase();
      return this.posts.filter(post => 
        post.title.toLowerCase().includes(query) || 
        post.content.toLowerCase().includes(query)
      );
    }
  },
  created() {
    this.checkAuthentication();
    // 대시보드가 기본 활성화되어 있으므로 대시보드 데이터만 로드
    this.fetchStats();
  },
  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        // 인증되지 않은 사용자는 로그인 페이지로 리다이렉트
        this.$router.push('/login');
        return;
      }
    },
    async fetchData() {
      this.fetchStats();
      this.fetchPosts();
      this.fetchCategories();
      this.fetchProfile();
      this.fetchSettings();
    },
    async fetchStats() {
      try {
        this.loadingStats = true;
        this.statsError = false;
        
        // API 서비스를 통한 통계 정보 호출
        const response = await api.stats.get();
        
        // 서버에서 받은 데이터로 통계 및 최근 활동 업데이트
        this.stats = response.data.stats;
        this.recentActivities = response.data.recent_activities || [];
        
        // 카테고리별 게시물 수 정보 저장 (나중에 활용할 수 있음)
        this.categoryStats = response.data.category_stats || [];
        
        this.loadingStats = false;
      } catch (error) {
        console.error('통계 정보를 불러오는데 실패했습니다:', error);
        
        // API 호출 실패 시 기본 데이터 표시
        this.stats = {
          posts: 0,
          categories: 0,
          comments: 0
        };
        
        // 기본 활동 내역 제공
        this.recentActivities = [
          { 
            text: '블로그를 시작합니다!', 
            icon: 'fas fa-rocket', 
            color: 'text-primary', 
            time: '방금 전' 
          },
          { 
            text: '첫 글을 작성해보세요.', 
            icon: 'fas fa-pen', 
            color: 'text-info', 
            time: '방금 전' 
          },
          { 
            text: '카테고리를 추가해보세요.', 
            icon: 'fas fa-folder-plus', 
            color: 'text-success', 
            time: '방금 전' 
          }
        ];
        
        this.categoryStats = [];
        this.loadingStats = false;
        this.statsError = true;
      }
    },
    async fetchPosts() {
      try {
        this.loadingPosts = true;
        this.errorMessage = '';
        
        // 내 게시물 API 호출
        const response = await api.posts.getMyPosts();
        this.posts = response.data;
        
        // 게시물 수 확인 및 로깅
        console.log(`${this.posts.length}개의 게시물을 불러왔습니다.`);
        
        this.loadingPosts = false;
      } catch (error) {
        console.error('글 목록을 불러오는데 실패했습니다:', error);
        
        if (error.response && error.response.status === 401) {
          this.showMessage('인증 정보가 만료되었습니다. 다시 로그인해주세요.', true);
          localStorage.removeItem('accessToken');
          this.$router.push('/login');
        } else if (error.response && error.response.status === 404) {
          this.showMessage('API 엔드포인트를 찾을 수 없습니다.', true);
        } else {
          this.showMessage('글 목록을 불러오는데 실패했습니다.', true);
        }
        
        // 빈 배열로 설정
        this.posts = [];
        this.loadingPosts = false;
      }
    },
    async fetchCategories() {
      try {
        this.loadingCategories = true;
        const response = await api.categories.getAll();
        // 카테고리에 편집 상태 속성 추가
        this.categories = response.data.map(category => ({
          ...category,
          isEditing: false,
          editName: category.name
        }));
        this.loadingCategories = false;
      } catch (error) {
        console.error('카테고리를 불러오는데 실패했습니다:', error);
        this.errorMessage = '카테고리를 불러오는데 실패했습니다.';
        this.loadingCategories = false;
      }
    },
    async fetchProfile() {
      try {
        // 프로필 정보 API 호출
        const response = await api.user.getProfile();
        this.profile = response.data;
      } catch (error) {
        console.error('프로필 정보를 불러오는데 실패했습니다:', error);
        // API 엔드포인트가 아직 구현되지 않았거나 호출에 실패한 경우 임시 데이터 사용
        this.profile = {
          username: 'user123',
          email: 'user@example.com',
          name: '홍길동',
          bio: '블로그 운영자입니다.'
        };
      }
    },
    async fetchSettings() {
      try {
        const response = await api.settings.get();
        this.settings = response.data;
      } catch (error) {
        console.error('블로그 설정을 불러오는데 실패했습니다:', error);
        // 기본 설정 유지
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    async addCategory() {
      if (!this.newCategoryName.trim()) return;
      
      try {
        this.loadingCategories = true;
        this.errorMessage = '';
        this.successMessage = '';
        
        const slugName = slugify(this.newCategoryName);
        
        const response = await api.categories.create({
          name: this.newCategoryName,
          slug: slugName
        });
        
        // 새 카테고리를 목록에 추가 (편집 상태 속성 포함)
        this.categories.push({
          ...response.data,
          isEditing: false,
          editName: response.data.name
        });
        
        this.newCategoryName = '';
        this.successMessage = '카테고리가 성공적으로 추가되었습니다.';
        
        // 통계 업데이트
        this.stats.categories++;
      } catch (error) {
        console.error('카테고리 추가 실패:', error);
        
        if (error.response && error.response.data) {
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
          this.errorMessage = '카테고리 추가 중 오류가 발생했습니다.';
        }
      } finally {
        this.loadingCategories = false;
      }
    },
    startEditCategory(category) {
      // 편집 시작
      category.isEditing = true;
      category.editName = category.name;
    },
    cancelEdit(category) {
      // 편집 취소
      category.isEditing = false;
    },
    async saveCategory(category) {
      try {
        this.loadingCategories = true;
        this.errorMessage = '';
        this.successMessage = '';
        
        // 이름이 변경된 경우에만 API 호출
        if (category.name !== category.editName) {
          const response = await api.categories.update(category.slug, {
            name: category.editName,
            slug: category.slug
          });
          
          // 카테고리 이름 업데이트
          category.name = response.data.name;
        }
        
        // 편집 모드 종료
        category.isEditing = false;
        this.successMessage = '카테고리가 성공적으로 수정되었습니다.';
      } catch (error) {
        console.error('카테고리 수정 실패:', error);
        this.errorMessage = '카테고리 수정 중 오류가 발생했습니다.';
      } finally {
        this.loadingCategories = false;
      }
    },
    async deleteCategory(categoryId) {
      if (!confirm('이 카테고리를 삭제하시겠습니까? 연결된 글이 있으면 삭제할 수 없습니다.')) {
        return;
      }
      
      try {
        this.loadingCategories = true;
        this.errorMessage = '';
        this.successMessage = '';
        
        const category = this.categories.find(c => c.id === categoryId);
        
        if (!category) return;
        
        await api.categories.delete(category.slug);
        
        // 삭제된 카테고리를 목록에서 제거
        this.categories = this.categories.filter(c => c.id !== categoryId);
        this.successMessage = '카테고리가 성공적으로 삭제되었습니다.';
        
        // 통계 업데이트
        this.stats.categories--;
      } catch (error) {
        console.error('카테고리 삭제 실패:', error);
        
        if (error.response && error.response.status === 400) {
          this.errorMessage = '이 카테고리에 연결된 글이 있어 삭제할 수 없습니다.';
        } else {
          this.errorMessage = '카테고리 삭제 중 오류가 발생했습니다.';
        }
      } finally {
        this.loadingCategories = false;
      }
    },
    getCategoryPostCount(categoryId) {
      // 서버에서 받은 카테고리별 게시물 수 정보를 사용
      const categoryStat = this.categoryStats.find(stat => stat.id === categoryId);
      return categoryStat ? categoryStat.post_count : 0;
    },
    async editPost(post) {
      // 글 편집 페이지로 이동
      this.$router.push(`/write?edit=${post.id}`);
    },
    async deletePost(postId) {
      if (!confirm('이 글을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
        return;
      }
      
      try {
        this.loadingPosts = true;
        this.errorMessage = '';
        this.successMessage = '';
        
        const post = this.posts.find(p => p.id === postId);
        
        if (!post) {
          this.errorMessage = '삭제할 게시물을 찾을 수 없습니다.';
          return;
        }

        if (!post.slug) {
          this.errorMessage = '게시물 식별자가 유효하지 않습니다.';
          return;
        }
        
        console.log(`게시물 삭제 요청: ID=${post.id}, 제목=${post.title}, 슬러그=${post.slug}`);
        
        // 실제로 존재하는 게시물인지 확인하기 위해 먼저 조회
        try {
          await api.posts.get(post.slug);
        } catch (fetchError) {
          if (fetchError.response && fetchError.response.status === 404) {
            console.error(`게시물 ${post.slug}이(가) 서버에 존재하지 않습니다`);
            // 로컬 목록에서만 제거
            this.posts = this.posts.filter(p => p.id !== postId);
            this.errorMessage = `게시물 ${post.title}이(가) 이미 삭제되었습니다. 목록을 갱신합니다.`;
            return;
          }
        }
        
        // 삭제 API 호출
        await api.posts.delete(post.slug);
        
        // 삭제된 글을 목록에서 제거
        this.posts = this.posts.filter(p => p.id !== postId);
        this.successMessage = '글이 성공적으로 삭제되었습니다.';
        
        // 통계 업데이트
        this.stats.posts--;
      } catch (error) {
        console.error('글 삭제 실패:', error);
        
        if (error.response && error.response.status === 404) {
          this.errorMessage = '삭제할 게시물을 찾을 수 없습니다. 다시 시도하거나 페이지를 새로고침해 주세요.';
          // 로컬 목록에서 삭제
          const post = this.posts.find(p => p.id === postId);
          if (post) {
            this.posts = this.posts.filter(p => p.id !== postId);
            this.errorMessage += ' (목록에서 제거됨)';
          }
        } else {
          this.errorMessage = '글 삭제 중 오류가 발생했습니다: ' + 
                             (error.response && error.response.data ? 
                              JSON.stringify(error.response.data) : error.message);
        }
      } finally {
        this.loadingPosts = false;
      }
    },
    async updateProfile() {
      try {
        this.loadingCategories = true;
        this.errorMessage = '';
        this.successMessage = '';
        
        // API로 프로필 업데이트
        await api.user.updateProfile(this.profile);
        
        this.successMessage = '프로필이 성공적으로 업데이트되었습니다.';
      } catch (error) {
        console.error('프로필 업데이트 실패:', error);
        this.errorMessage = '프로필 업데이트 중 오류가 발생했습니다.';
      } finally {
        this.loadingCategories = false;
      }
    },
    async saveSettings() {
      try {
        this.loadingCategories = true;
        this.errorMessage = '';
        this.successMessage = '';
        
        // API로 설정 업데이트
        const response = await api.settings.update(this.settings);
        
        // 설정 저장 성공
        this.successMessage = '블로그 설정이 성공적으로 저장되었습니다.';
        
        // 메인 페이지에 설정 적용을 위해 이벤트 발생 또는 로컬 스토리지에 저장
        localStorage.setItem('blogSettings', JSON.stringify(response.data));
      } catch (error) {
        console.error('설정 저장 실패:', error);
        this.errorMessage = '설정 저장 중 오류가 발생했습니다.';
      } finally {
        this.loadingCategories = false;
      }
    },
    getPercentage(postCount) {
      const total = this.getTotalPosts();
      if (total === 0) return 0;
      return Math.round((postCount / total) * 100);
    },
    getTotalPosts() {
      // 모든 카테고리의 글 수 합계
      return this.categoryStats.reduce((sum, stat) => sum + stat.post_count, 0);
    },
    refreshPosts() {
      console.log("게시물 목록 새로고침");
      this.fetchPosts();
      this.successMessage = "게시물 목록을 새로고침했습니다.";
      setTimeout(() => {
        this.successMessage = '';
      }, 2000);
    },
    showMessage(message, isError = false, duration = 3000) {
      if (isError) {
        this.errorMessage = message;
        this.successMessage = '';
      } else {
        this.successMessage = message;
        this.errorMessage = '';
      }
      
      setTimeout(() => {
        if (isError) {
          this.errorMessage = '';
        } else {
          this.successMessage = '';
        }
      }, duration);
    },
    setActivePage(page) {
      // 이전 페이지와 같은 경우 중복 로드 방지
      if (this.activePage === page) return;
      
      this.activePage = page;
      
      // 각 페이지에 필요한 데이터만 선택적으로 로드
      switch(page) {
        case 'dashboard':
          this.fetchStats();
          break;
        case 'posts':
          this.fetchPosts();
          break;
        case 'categories':
          this.fetchCategories();
          break;
        case 'profile':
          this.fetchProfile();
          break;
        case 'settings':
          this.fetchSettings();
          break;
      }
    }
  }
}
</script>

<style scoped>
.card {
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.list-group-item {
  transition: background-color 0.2s;
}
.list-group-item:hover {
  background-color: #f8f9fa;
}
.list-group-item.active {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style> 