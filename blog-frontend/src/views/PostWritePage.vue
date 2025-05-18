<template>
  <div>
    <!-- 여기서는 App.vue의 네비게이션 바가 이미 렌더링되어 있습니다 -->
    
    <!-- 알림 메시지 (간결한 디자인) -->
    <div v-if="errorMessage" class="alert alert-danger rounded-0 mb-0 text-center py-2" style="z-index: 2000; position: relative;">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success rounded-0 mb-0 text-center py-2" style="z-index: 2000; position: relative;">
      {{ successMessage }}
    </div>
    
    <!-- 네비게이션 바와의 간격 조정 -->
    <div style="height: 56px;"></div>
    
    <!-- 티스토리 스타일 편집기 영역 -->
    <div class="container py-4">
      <!-- 카테고리 선택과 버튼 영역 - 고정 위치로 설정하고 z-index를 높임 -->
      <div class="d-flex align-items-center pb-3 mb-4 border-bottom" 
          style="z-index: 2000; background-color: #fff; position: sticky; top: 56px; padding-top: 15px; width: 100%;">
        <select 
          class="form-select form-select-sm border-0 text-muted bg-light rounded-pill"
          style="width: 150px;" 
          v-model="postForm.category"
        >
          <option value="" disabled selected>카테고리</option>
          <option 
            v-for="category in categories" 
            :key="category.id" 
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
        
        <!-- 오른쪽에 버튼들 -->
        <div class="ms-auto">
          <button
            type="button" 
            class="btn btn-sm btn-light rounded-pill px-3 border me-1"
            style="font-size: 0.85rem; background-color: #fff !important;"
            @click="saveAsDraft"
            :disabled="isSubmitting"
          >
            임시저장
          </button>
          <button
            type="button" 
            class="btn btn-sm btn-outline-danger rounded-pill px-3 border me-1"
            style="font-size: 0.85rem; background-color: #fff !important;"
            @click="confirmDelete"
            :disabled="isSubmitting"
          >
            삭제
          </button>
          <button
            type="button" 
            class="btn btn-sm btn-primary rounded-pill px-3"
            style="font-size: 0.85rem; background-color: #1eb4eb !important; border-color: #1eb4eb !important;"
            @click="submitPost"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
            완료
          </button>
        </div>
      </div>
      
      <!-- 제목 입력 (티스토리 스타일) -->
      <div class="pb-3 mb-4 position-relative" style="z-index: 900;">
        <input 
          type="text" 
          class="form-control border-0 fs-4 fw-medium p-0" 
          id="title" 
          v-model="postForm.title" 
          placeholder="제목을 입력하세요" 
          required
          style="outline: none; box-shadow: none; border-radius: 0;"
        >
      </div>
      
      <!-- 에디터 툴바 (티스토리 스타일) -->
      <div class="editor-toolbar d-flex py-2 px-3 bg-light rounded mb-4 align-items-center position-relative" style="z-index: 800;">
        <!-- 기본 서식 도구 -->
        <div class="btn-group me-2">
          <button @click.prevent="formatDoc('bold')" type="button" class="btn btn-sm btn-light">
            <strong>B</strong>
          </button>
          <button @click.prevent="formatDoc('italic')" type="button" class="btn btn-sm btn-light">
            <i>I</i>
          </button>
          <button @click.prevent="formatDoc('underline')" type="button" class="btn btn-sm btn-light">
            <u>U</u>
          </button>
          <button @click.prevent="formatDoc('strikeThrough')" type="button" class="btn btn-sm btn-light">
            S
          </button>
        </div>
        
        <!-- 정렬 도구 -->
        <div class="btn-group me-2">
          <button @click.prevent="formatDoc('justifyLeft')" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-align-left"></i>
          </button>
          <button @click.prevent="formatDoc('justifyCenter')" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-align-center"></i>
          </button>
          <button @click.prevent="formatDoc('justifyRight')" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-align-right"></i>
          </button>
        </div>
        
        <!-- 목록 도구 -->
        <div class="btn-group me-2">
          <button @click.prevent="formatDoc('insertUnorderedList')" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-list-ul"></i>
          </button>
          <button @click.prevent="formatDoc('insertOrderedList')" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-list-ol"></i>
          </button>
        </div>
        
        <!-- 미디어 및 특수 도구 -->
        <div class="btn-group me-2">
          <button @click.prevent="insertLink()" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-link"></i>
          </button>
          <button @click.prevent="insertImage()" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-image"></i>
          </button>
          <button @click.prevent="insertTable()" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-table"></i>
          </button>
          <button @click.prevent="insertHr()" type="button" class="btn btn-sm btn-light">
            <i class="fas fa-minus"></i>
          </button>
        </div>
        
        <!-- 글꼴 및 본문 스타일 (드롭다운) -->
        <div class="dropdown">
          <button class="btn btn-sm btn-light dropdown-toggle" type="button" data-bs-toggle="dropdown">
            <i class="fas fa-ellipsis-h"></i>
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click.prevent="formatFont('Arial')">Arial</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="formatFont('맑은 고딕')">맑은 고딕</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="formatFont('나눔고딕')">나눔고딕</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#" @click.prevent="formatHeading('h2')">제목 1</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="formatHeading('h3')">제목 2</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="formatHeading('h4')">제목 3</a></li>
          </ul>
        </div>
      </div>
      
      <!-- 에디터 콘텐츠 영역 (티스토리 스타일) -->
      <div 
        id="editor-content" 
        class="editor-content position-relative"
        contenteditable="true"
        @input="handleEditorInput"
        ref="editorContent"
        style="z-index: 500; margin-top: 15px;"
      ></div>
      
      <!-- 태그 입력 영역 (티스토리 스타일) -->
      <div class="py-3 border-top mt-5 mb-3 position-relative" style="z-index: 700;">
        <div class="d-flex align-items-center">
          <span class="text-muted me-2">#</span>
          <input
            type="text"
            class="form-control form-control-sm border-0"
            v-model="tagInput"
            @keydown.enter.prevent="addTag"
            placeholder="태그 입력 후 Enter"
            style="outline: none; box-shadow: none;"
          />
        </div>
        <div class="tags-list mt-3">
          <span v-for="(tag, index) in tags" :key="index" class="tag-item">
            #{{ tag }}
            <button @click.prevent="removeTag(index)" class="tag-remove">×</button>
          </span>
        </div>
      </div>
      
      <!-- 부가 설정 패널 (오프캔버스) -->
      <div class="offcanvas offcanvas-end" tabindex="-1" id="settingsOffcanvas">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title">글 설정</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <!-- 부제목 설정 -->
          <div class="mb-3">
            <label for="subtitle" class="form-label">부제목</label>
            <input 
              type="text" 
              class="form-control" 
              id="subtitle" 
              v-model="postForm.subtitle" 
              placeholder="부제목을 입력하세요" 
            >
          </div>
          
          <!-- 공개 설정 -->
          <div class="mb-3">
            <label class="form-label d-block">발행 설정</label>
            <div class="form-check form-switch">
              <input class="form-check-input" type="checkbox" id="publish-switch" v-model="postForm.is_published">
              <label class="form-check-label" for="publish-switch">
                {{ postForm.is_published ? '공개' : '비공개' }}
              </label>
            </div>
          </div>
          
          <!-- 썸네일 설정 -->
          <div class="mb-4">
            <label class="form-label">썸네일 이미지</label>
            <div class="thumbnail-container" @click="selectCoverImage">
              <div v-if="selectedCoverImage" class="thumbnail-preview" 
                :style="{ backgroundImage: `url('${selectedCoverImage}')` }">
              </div>
              <div v-else class="thumbnail-empty d-flex align-items-center justify-content-center">
                <i class="fas fa-image text-muted"></i>
              </div>
              <button class="btn btn-sm btn-light thumbnail-btn">
                이미지 선택
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { HOME_BG, POST_BG, ABOUT_BG, CONTACT_BG } from '../assets/img/placeholder.js';

export default {
  name: 'PostWritePage',
  data() {
    return {
      postForm: {
        title: '',
        subtitle: '',
        content: '',
        category: '',
        is_published: true,
        tags: '',
        cover_image: '',
        slug: ''
      },
      categories: [],
      isSubmitting: false,
      errorMessage: '',
      successMessage: '',
      tagInput: '',
      tags: [],
      backgroundImage: POST_BG,
      availableCoverImages: [HOME_BG, POST_BG, ABOUT_BG, CONTACT_BG],
      selectedCoverImage: null
    };
  },
  watch: {
    'postForm.title': function(newTitle) {
      // 제목이 변경될 때마다 slug 자동 생성
      this.postForm.slug = this.slugify(newTitle);
    }
  },
  created() {
    this.fetchCategories();
    this.checkAuthentication();
  },
  mounted() {
    // 초기 에디터 내용 설정
    if (this.$refs.editorContent) {
      this.$refs.editorContent.innerHTML = this.postForm.content;
    }
  },
  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('token');
      if (!token) {
        // 인증되지 않은 사용자는 로그인 페이지로 리다이렉트
        this.$router.push('/login');
        return;
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://localhost:8001/api/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('카테고리를 불러오는데 실패했습니다:', error);
        this.errorMessage = '카테고리를 불러오는데 실패했습니다. 나중에 다시 시도해주세요.';
      }
    },
    slugify(text) {
      // 텍스트가 없으면 빈 문자열 반환
      if (!text) return '';
      
      // 한글, 영문, 숫자를 URL 친화적인 형태로 변환
      return text
        .toString()
        .toLowerCase()
        .replace(/\s+/g, '-')     // 공백을 하이픈으로 변환
        .replace(/[^\w-]+/g, '')  // 영문, 숫자, 하이픈이 아닌 문자 제거
        .replace(/--+/g, '-')     // 여러 개의 하이픈을 하나로 변환
        .replace(/^-+/, '')       // 시작 부분의 하이픈 제거
        .replace(/-+$/, '');      // 끝 부분의 하이픈 제거
    },
    formatDoc(command, value = null) {
      document.execCommand(command, false, value);
      this.$refs.editorContent.focus();
      this.handleEditorInput();
    },
    formatFont(fontName) {
      if(fontName) {
        this.formatDoc('fontName', fontName);
      }
    },
    formatHeading(heading) {
      if(heading) {
        this.formatDoc('formatBlock', `<${heading}>`);
      }
    },
    insertLink() {
      const url = prompt('링크 URL을 입력하세요:', 'http://');
      if (url) {
        this.formatDoc('createLink', url);
      }
    },
    insertImage() {
      const url = prompt('이미지 URL을 입력하세요:', 'http://');
      if (url) {
        this.formatDoc('insertImage', url);
      }
    },
    insertTable() {
      const rows = prompt('행 수를 입력하세요:', '3');
      const cols = prompt('열 수를 입력하세요:', '3');
      
      if (rows && cols) {
        const table = document.createElement('table');
        table.border = '1';
        table.style.width = '100%';
        table.style.borderCollapse = 'collapse';
        
        for (let i = 0; i < rows; i++) {
          const row = table.insertRow();
          for (let j = 0; j < cols; j++) {
            const cell = row.insertCell();
            cell.innerHTML = '내용을 입력하세요';
            cell.style.border = '1px solid #ccc';
            cell.style.padding = '8px';
          }
        }
        
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        range.deleteContents();
        range.insertNode(table);
        this.handleEditorInput();
      }
    },
    insertHr() {
      this.formatDoc('insertHorizontalRule');
    },
    handleEditorInput() {
      // 에디터 내용을 form data에 업데이트
      this.postForm.content = this.$refs.editorContent.innerHTML;
    },
    addTag() {
      if (this.tagInput.trim() && !this.tags.includes(this.tagInput.trim())) {
        this.tags.push(this.tagInput.trim());
        this.tagInput = '';
        this.updateTagsInForm();
      }
    },
    removeTag(index) {
      this.tags.splice(index, 1);
      this.updateTagsInForm();
    },
    updateTagsInForm() {
      this.postForm.tags = this.tags.join(',');
    },
    selectCoverImage() {
      // 실제 구현에서는 여기서 이미지 선택 다이얼로그를 열어 이미지를 선택할 수 있게 합니다.
      // 이 예제에서는 간단히 사용 가능한 이미지 중 하나를 선택합니다.
      const randomIndex = Math.floor(Math.random() * this.availableCoverImages.length);
      this.selectedCoverImage = this.availableCoverImages[randomIndex];
      this.postForm.cover_image = this.selectedCoverImage;
    },
    saveAsDraft() {
      this.postForm.is_published = false;
      this.submitPost();
    },
    async submitPost() {
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.errorMessage = '로그인이 필요합니다.';
          this.$router.push('/login');
          return;
        }
        
        // 최종 내용 업데이트
        this.postForm.content = this.$refs.editorContent.innerHTML;
        this.updateTagsInForm();
        
        // 슬러그가 없는 경우 제목에서 생성
        if (!this.postForm.slug && this.postForm.title) {
          this.postForm.slug = this.slugify(this.postForm.title);
        }
        
        // 선택한 커버 이미지 설정
        if (this.selectedCoverImage) {
          this.postForm.cover_image = this.selectedCoverImage;
        }
        
        const response = await axios.post(
          'http://localhost:8001/api/posts/', 
          this.postForm,
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );
        
        this.successMessage = '글이 성공적으로 등록되었습니다.';
        // 성공 후 메시지 표시 후 홈페이지로 이동
        setTimeout(() => {
          this.$router.push(`/post/${response.data.slug}`);
        }, 1500);
      } catch (error) {
        console.error('글 등록 실패:', error);
        
        if (error.response && error.response.data) {
          // 서버에서 반환한 에러 메시지 표시
          const errorData = error.response.data;
          if (typeof errorData === 'object') {
            // 필드별 에러 메시지 구성
            const messages = [];
            for (const field in errorData) {
              messages.push(`${field}: ${errorData[field]}`);
            }
            this.errorMessage = messages.join('\n');
          } else {
            this.errorMessage = errorData;
          }
        } else {
          this.errorMessage = '서버와 통신 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    confirmDelete() {
      if (confirm('글을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
        this.deletePost();
      }
    },
    async deletePost() {
      this.isSubmitting = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.errorMessage = '로그인이 필요합니다.';
          this.$router.push('/login');
          return;
        }
        
        // 새 글인 경우는 그냥 홈으로 이동
        if (!this.postForm.id) {
          this.$router.push('/');
          return;
        }
        
        // 기존 글 삭제 API 호출
        await axios.delete(
          `http://localhost:8001/api/posts/${this.postForm.id}/`, 
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );
        
        // 삭제 성공 후 홈페이지로 이동
        this.$router.push('/');
      } catch (error) {
        console.error('글 삭제 실패:', error);
        this.errorMessage = '글 삭제 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
/* 티스토리 스타일 에디터 */
.editor-content {
  min-height: 400px;
  padding: 0;
  margin-bottom: 1rem;
  border: none;
  font-size: 16px;
  line-height: 1.8;
  outline: none;
  background-color: #fff;
}

.editor-content:focus {
  border-color: #ddd;
}

/* 툴바 상단 고정 및 스타일 개선 */
.editor-toolbar {
  background-color: #f8f9fa !important;
  border-color: #eee !important;
}

.editor-toolbar .btn-light {
  background-color: transparent;
  border-color: transparent;
}

.editor-toolbar .btn-light:hover {
  background-color: rgba(0,0,0,0.05);
}

/* 버튼 스타일 개선 */
.btn-primary {
  background-color: #1eb4eb !important;
  border-color: #1eb4eb !important;
  color: #fff !important;
}

.btn-primary:hover {
  background-color: #1a9ed0 !important;
  border-color: #1a9ed0 !important;
}

.btn-light {
  background-color: #fff !important;
}

.btn-outline-danger {
  color: #dc3545 !important;
  background-color: #fff !important;
}

/* 티스토리 스타일 태그 */
.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  background-color: #f8f9fa;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.85rem;
  color: #495057;
}

.tag-remove {
  background: none;
  border: none;
  color: #6c757d;
  margin-left: 0.25rem;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  line-height: 0;
}

.tag-remove:hover {
  color: #dc3545;
}

/* 썸네일 스타일 유지 */
.thumbnail-container {
  position: relative;
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
  aspect-ratio: 16/9;
  cursor: pointer;
  transition: all 0.2s ease;
}

.thumbnail-container:hover {
  border-color: #ccc;
}

.thumbnail-preview {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
}

.thumbnail-empty {
  width: 100%;
  height: 100%;
  font-size: 2rem;
  color: #dee2e6;
}

.thumbnail-btn {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 0;
  opacity: 0;
  transition: opacity 0.3s;
}

.thumbnail-container:hover .thumbnail-btn {
  opacity: 1;
}
</style> 