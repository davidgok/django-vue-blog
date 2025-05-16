<template>
  <div class="tistory-editor">
    <!-- 상단 내비게이션 바 -->
    <div class="editor-header">
      <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center py-2">
          <div>
            <span class="logo">tistory</span>
          </div>
          <div>
            <button 
              type="button" 
              class="btn btn-sm btn-outline-secondary me-2" 
              @click="$router.push('/')"
            >
              취소
            </button>
            <button 
              type="button" 
              class="btn btn-sm btn-dark" 
              @click="submitPost"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              완료
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 에디터 영역 -->
    <div class="editor-content-wrapper">
      <div class="container-fluid px-4 py-3">
        <!-- Alert Messages -->
        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>

        <!-- 카테고리 선택 -->
        <div class="mb-3">
          <select 
            class="form-select form-select-sm w-auto" 
            id="category" 
            v-model="postForm.category" 
            required
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
        </div>
        
        <!-- 제목 입력 -->
        <div class="title-input mb-3">
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
        <div class="editor-toolbar mb-2 d-flex border-top border-bottom py-1">
          <div class="btn-toolbar flex-wrap" role="toolbar">
            <!-- 글꼴 설정 -->
            <div class="btn-group me-3" role="group">
              <button type="button" class="btn btn-sm btn-toolbar">본문</button>
            </div>
            
            <!-- 텍스트 서식 -->
            <div class="btn-group me-3" role="group">
              <button @click.prevent="formatDoc('bold')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="bold" />
              </button>
              <button @click.prevent="formatDoc('italic')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="italic" />
              </button>
              <button @click.prevent="formatDoc('underline')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="underline" />
              </button>
              <button @click.prevent="formatDoc('strikeThrough')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="strikethrough" />
              </button>
            </div>
            
            <!-- 텍스트 정렬 -->
            <div class="btn-group me-3" role="group">
              <button @click.prevent="formatDoc('justifyLeft')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="align-left" />
              </button>
              <button @click.prevent="formatDoc('justifyCenter')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="align-center" />
              </button>
              <button @click.prevent="formatDoc('justifyRight')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="align-right" />
              </button>
            </div>
            
            <!-- 목록 -->
            <div class="btn-group me-3" role="group">
              <button @click.prevent="formatDoc('insertUnorderedList')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="list-ul" />
              </button>
              <button @click.prevent="formatDoc('insertOrderedList')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="list-ol" />
              </button>
            </div>
            
            <!-- 링크 및 이미지 -->
            <div class="btn-group me-3" role="group">
              <button @click.prevent="formatDoc('createLink')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="link" />
              </button>
              <button @click.prevent="formatDoc('insertImage')" type="button" class="btn btn-sm btn-toolbar">
                <font-awesome-icon icon="image" />
              </button>
            </div>
            
            <!-- 헤딩 -->
            <div class="btn-group me-3" role="group">
              <button @click.prevent="formatDoc('formatBlock', '<h2>')" type="button" class="btn btn-sm btn-toolbar fw-bold">가</button>
              <button @click.prevent="formatDoc('formatBlock', '<h3>')" type="button" class="btn btn-sm btn-toolbar">가</button>
              <button @click.prevent="formatDoc('formatBlock', '<h4>')" type="button" class="btn btn-sm btn-toolbar small">가</button>
            </div>
            
            <!-- 기타 도구 -->
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-sm btn-toolbar">기본모드</button>
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
        
        <!-- 태그 및 발행 설정 영역 -->
        <div class="post-options mt-4 pt-3 border-top">
          <div class="row">
            <div class="col-md-8">
              <div class="tags-input">
                <div class="d-flex align-items-center">
                  <span class="tags-icon me-2">#</span>
                  <input
                    type="text"
                    class="form-control form-control-sm border-0"
                    v-model="tagInput"
                    @keydown.enter.prevent="addTag"
                    placeholder="태그를 입력하세요"
                  />
                </div>
                <div class="tags-list mt-2">
                  <span v-for="(tag, index) in tags" :key="index" class="tag-item">
                    {{ tag }}
                    <button @click.prevent="removeTag(index)" class="tag-remove">×</button>
                  </span>
                </div>
              </div>
            </div>
            <div class="col-md-4 text-end">
              <div class="form-check form-switch">
                <input 
                  type="checkbox" 
                  class="form-check-input" 
                  id="publish" 
                  v-model="postForm.is_published"
                >
                <label class="form-check-label" for="publish">즉시 발행</label>
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
        tags: ''
      },
      categories: [],
      isSubmitting: false,
      errorMessage: '',
      successMessage: '',
      tagInput: '',
      tags: []
    };
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
    formatDoc(command, value = null) {
      document.execCommand(command, false, value);
      this.$refs.editorContent.focus();
      this.handleEditorInput();
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
.logo {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #000;
}

.tistory-editor {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #fff;
}

.editor-header {
  background-color: #fff;
  border-bottom: 1px solid #e9ecef;
  padding: 0.5rem 1rem;
}

.editor-content-wrapper {
  flex: 1;
  overflow-y: auto;
  background-color: #fff;
  max-width: 820px;
  margin: 0 auto;
  box-shadow: none;
  padding-top: 1rem;
}

.title-input input {
  font-size: 1.5rem;
  font-weight: 500;
  padding: 0.5rem 0;
  background-color: transparent;
  border-color: transparent;
}

.title-input input:focus {
  box-shadow: none;
  background-color: transparent;
  border-color: transparent;
}

.editor-toolbar {
  background-color: #fff;
  border-color: #e9ecef !important;
}

.editor-toolbar .btn-toolbar {
  color: #333;
  font-size: 14px;
  border: none;
  background: transparent;
  padding: 0.25rem 0.5rem;
}

.editor-toolbar .btn-toolbar:hover {
  background-color: #f1f3f5;
  border-radius: 2px;
}

.editor-content {
  min-height: 500px;
  padding: 1rem 0;
  overflow-y: auto;
  outline: none;
  line-height: 1.6;
  color: #333;
}

.post-options {
  color: #495057;
}

.tags-input {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 0.5rem;
}

.tags-icon {
  font-size: 1.2rem;
  color: #868e96;
  font-weight: bold;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  background-color: #e9ecef;
  border-radius: 30px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  color: #495057;
}

.tag-remove {
  background: none;
  border: none;
  color: #adb5bd;
  margin-left: 0.25rem;
  padding: 0 0.25rem;
  cursor: pointer;
  font-size: 1rem;
}

.tag-remove:hover {
  color: #495057;
}

.form-check-input:checked {
  background-color: #000;
  border-color: #000;
}

.btn-outline-secondary {
  border-color: #ced4da;
  color: #495057;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  color: #212529;
  border-color: #ced4da;
}

.btn-dark {
  background-color: #000;
  border-color: #000;
  padding: 0.25rem 0.75rem;
}

.btn-dark:hover, .btn-dark:focus {
  background-color: #333;
  border-color: #333;
}

.form-switch .form-check-input {
  width: 2.5em;
  height: 1.25em;
}
</style> 