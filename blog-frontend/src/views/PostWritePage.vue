<template>
  <div>
    <!-- Page Header-->
    <header class="masthead" :style="{ backgroundImage: `url('${backgroundImage}')` }">
      <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-md-10 col-lg-8 col-xl-7">
            <div class="site-heading">
              <h1>글쓰기</h1>
              <span class="subheading">블로그에 새 글을 작성합니다</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 메인 에디터 영역 -->
    <div class="container px-4 px-lg-5">
      <!-- Alert Messages -->
      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>

      <div class="row gx-4 gx-lg-5">
        <!-- 왼쪽 에디터 영역 -->
        <div class="col-md-8">
          <div class="card mb-4">
            <div class="card-body">
              <!-- 제목 입력 -->
              <div class="mb-3">
                <input 
                  type="text" 
                  class="form-control form-control-lg border-0" 
                  id="title" 
                  v-model="postForm.title" 
                  placeholder="제목을 입력하세요" 
                  required
                >
              </div>
              
              <!-- 에디터 툴바 -->
              <div class="editor-toolbar d-flex border-top border-bottom py-1 mb-3">
                <div class="btn-toolbar flex-wrap" role="toolbar">
                  <!-- 글꼴 설정 -->
                  <div class="btn-group me-2" role="group">
                    <select class="form-select form-select-sm" @change="formatFont($event.target.value)">
                      <option value="">글꼴</option>
                      <option value="Arial">Arial</option>
                      <option value="Verdana">Verdana</option>
                      <option value="Helvetica">Helvetica</option>
                      <option value="Times New Roman">Times New Roman</option>
                      <option value="Courier New">Courier New</option>
                      <option value="맑은 고딕">맑은 고딕</option>
                      <option value="나눔고딕">나눔고딕</option>
                    </select>
                  </div>
                  
                  <div class="btn-group me-2" role="group">
                    <select class="form-select form-select-sm" @change="formatHeading($event.target.value)">
                      <option value="">본문</option>
                      <option value="h2">제목 1</option>
                      <option value="h3">제목 2</option>
                      <option value="h4">제목 3</option>
                    </select>
                  </div>
                  
                  <!-- 텍스트 서식 -->
                  <div class="btn-group me-2" role="group">
                    <button @click.prevent="formatDoc('bold')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-bold"></i>
                    </button>
                    <button @click.prevent="formatDoc('italic')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-italic"></i>
                    </button>
                    <button @click.prevent="formatDoc('underline')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-underline"></i>
                    </button>
                    <button @click.prevent="formatDoc('strikeThrough')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-strikethrough"></i>
                    </button>
                  </div>
                  
                  <!-- 텍스트 정렬 -->
                  <div class="btn-group me-2" role="group">
                    <button @click.prevent="formatDoc('justifyLeft')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-align-left"></i>
                    </button>
                    <button @click.prevent="formatDoc('justifyCenter')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-align-center"></i>
                    </button>
                    <button @click.prevent="formatDoc('justifyRight')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-align-right"></i>
                    </button>
                  </div>
                  
                  <!-- 목록 -->
                  <div class="btn-group me-2" role="group">
                    <button @click.prevent="formatDoc('insertUnorderedList')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-list-ul"></i>
                    </button>
                    <button @click.prevent="formatDoc('insertOrderedList')" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-list-ol"></i>
                    </button>
                  </div>
                  
                  <!-- 링크 및 이미지 -->
                  <div class="btn-group me-2" role="group">
                    <button @click.prevent="insertLink()" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-link"></i>
                    </button>
                    <button @click.prevent="insertImage()" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-image"></i>
                    </button>
                    <button @click.prevent="insertTable()" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-table"></i>
                    </button>
                    <button @click.prevent="insertHr()" type="button" class="btn btn-sm btn-outline-secondary">
                      <i class="fas fa-minus"></i>
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- 에디터 콘텐츠 영역 -->
              <div 
                id="editor-content" 
                class="editor-content"
                contenteditable="true"
                @input="handleEditorInput"
                ref="editorContent"
              ></div>
            </div>
          </div>
          
          <!-- 버튼 영역 -->
          <div class="d-flex justify-content-end mb-4">
            <button 
              type="button" 
              class="btn btn-outline-secondary me-2" 
              @click="$router.push('/')"
            >
              취소
            </button>
            <button 
              type="button" 
              class="btn btn-outline-primary me-2" 
              @click="saveAsDraft"
              :disabled="isSubmitting"
            >
              임시저장
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="submitPost"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              발행
            </button>
          </div>
        </div>
        
        <!-- 오른쪽 설정 영역 -->
        <div class="col-md-4">
          <!-- 글 설정 -->
          <div class="card mb-4">
            <div class="card-header">글 설정</div>
            <div class="card-body">
              <div class="mb-3">
                <label for="category" class="form-label">카테고리</label>
                <select 
                  class="form-select" 
                  id="category" 
                  v-model="postForm.category" 
                  required
                >
                  <option value="" disabled selected>카테고리 선택</option>
                  <option 
                    v-for="category in categories" 
                    :key="category.id" 
                    :value="category.id"
                  >
                    {{ category.name }}
                  </option>
                </select>
              </div>
              
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
              
              <div class="mb-3">
                <label class="form-label d-block">발행 설정</label>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" name="publish-options" id="publish-public" 
                    v-model="postForm.is_published" :value="true">
                  <label class="form-check-label" for="publish-public">공개</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" name="publish-options" id="publish-private" 
                    v-model="postForm.is_published" :value="false">
                  <label class="form-check-label" for="publish-private">비공개</label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 썸네일 설정 -->
          <div class="card mb-4">
            <div class="card-header">썸네일 이미지</div>
            <div class="card-body">
              <div class="thumbnail-container mb-2" @click="selectCoverImage">
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
          
          <!-- 태그 설정 -->
          <div class="card mb-4">
            <div class="card-header">태그</div>
            <div class="card-body">
              <div class="tags-input">
                <input
                  type="text"
                  class="form-control mb-2"
                  v-model="tagInput"
                  @keydown.enter.prevent="addTag"
                  placeholder="태그 입력 후 Enter"
                />
                <div class="tags-list">
                  <span v-for="(tag, index) in tags" :key="index" class="tag-item">
                    #{{ tag }}
                    <button @click.prevent="removeTag(index)" class="tag-remove">×</button>
                  </span>
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
    }
  }
}
</script>

<style scoped>
.editor-content {
  min-height: 400px;
  padding: 1rem;
  overflow-y: auto;
  margin-bottom: 1rem;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
}

.editor-content:focus {
  outline: none;
  border-color: var(--bs-primary);
}

.thumbnail-container {
  position: relative;
  border: 1px dashed #ccc;
  border-radius: 4px;
  overflow: hidden;
  height: 150px;
  cursor: pointer;
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

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  background-color: rgba(0, 133, 161, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--bs-primary);
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

/* 색상 선택기 */
.color-picker {
  min-width: 150px;
}

.color-swatch {
  width: 25px;
  height: 25px;
  margin: 2px;
  border-radius: 2px;
  cursor: pointer;
  border: 1px solid #ccc;
}

.color-swatch:hover {
  transform: scale(1.1);
}
</style> 