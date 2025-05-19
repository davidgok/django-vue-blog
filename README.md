# Django-Vue-Blog

## 프로젝트 소개
블로그 플랫폼을 위한 Django 백엔드와 Vue.js 프론트엔드 기반의 풀스택 웹 애플리케이션입니다. 사용자는 개인 블로그를 생성하고 관리할 수 있으며, 글 작성 및 카테고리 관리 등의 기능을 제공합니다.

## 데모 영상
프로젝트의 주요 기능을 시연한 영상입니다:
- [데모 영상 1 보기](https://github.com/davidgok/django-vue-blog/issues/1)
- [데모 영상 2 보기](https://github.com/davidgok/django-vue-blog/issues/1)
- 
## 기술 스택

### 백엔드
- **Django**: 웹 프레임워크
- **Django REST Framework**: RESTful API 구현
- **JWT 인증**: 사용자 인증 및 보안
- **SQLite**: 데이터베이스 (개발용)

### 프론트엔드
- **Vue.js**: 프론트엔드 프레임워크
- **Bootstrap**: UI 디자인
- **Axios**: API 요청 처리

## 주요 기능

### 사용자 관리
- 회원가입 및 로그인
- JWT 토큰 기반 인증
- 비밀번호 재설정 (이메일 기능)
- 사용자 프로필 관리

### 게시글 관리
- 게시글 작성, 수정, 삭제
- 글 임시 저장 기능
- 마크다운 에디터
- 썸네일 이미지 업로드
- 태그 관리
- 게시글 검색

### 카테고리 관리
- 사용자별 카테고리 생성 및 관리
- 카테고리별 게시글 필터링

### 블로그 관리
- 대시보드에서 통계 확인
- 게시글 및 카테고리 관리
- 블로그 설정 관리

### 성능 최적화
- 캐싱 시스템 구현
- 데이터베이스 쿼리 최적화
- 페이지네이션

## 설치 및 실행 방법

### 백엔드 설정
```bash
cd blog_backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 프론트엔드 설정
```bash
cd blog-frontend
npm install
npm run serve
```

## 보안 기능
- CSRF 보호
- XSS 방지
- SQL 인젝션 방지
- JWT 토큰 블랙리스트 
