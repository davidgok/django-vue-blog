import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api';

// axios 인스턴스 생성
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 15000, // 15초로 타임아웃 연장
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
});

// 요청 인터셉터 추가 - 모든 요청에 토큰과 타임스탬프 자동 첨부
apiClient.interceptors.request.use(
    config => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
            console.log(`요청 헤더 설정: ${config.url} - Bearer ${token.substring(0, 15)}...`);
        } else {
            console.warn(`인증 토큰 없음: ${config.url}`);
        }

        // GET 요청에 자동으로 타임스탬프 추가 (캐시 방지)
        if (config.method === 'get') {
            config.params = config.params || {};
            config.params.t = new Date().getTime();
        }

        return config;
    },
    error => {
        console.error('API 요청 인터셉터 오류:', error);
        return Promise.reject(error);
    }
);

// 응답 인터셉터 추가 - 에러 처리 개선 및 토큰 갱신 처리
apiClient.interceptors.response.use(
    response => {
        return response;
    },
    async error => {
        // 에러 세부 정보 로깅
        if (error.response) {
            // 서버가 응답을 반환한 경우 (404, 500 등)
            console.error('API 응답 에러:', {
                status: error.response.status,
                statusText: error.response.statusText,
                url: error.config.url,
                method: error.config.method,
                data: error.response.data
            });

            // 토큰이 만료된 경우 리프레시 토큰으로 갱신 시도
            if (error.response.status === 401 && !error.config._retry) {
                if (!error.config.url.includes('/auth/login/') && !error.config.url.includes('/auth/token/refresh/')) {
                    try {
                        error.config._retry = true; // 재시도 플래그 설정
                        const refreshToken = localStorage.getItem('refreshToken');

                        if (refreshToken) {
                            console.log('액세스 토큰 갱신 시도');
                            const response = await apiClient.post('/auth/token/refresh/', {
                                refresh: refreshToken
                            });

                            if (response.data.access) {
                                // 새 토큰 저장
                                localStorage.setItem('accessToken', response.data.access);

                                // 원래 요청 재시도
                                error.config.headers.Authorization = `Bearer ${response.data.access}`;
                                return apiClient(error.config);
                            }
                        }
                    } catch (refreshError) {
                        console.error('토큰 갱신 실패, 로그아웃 처리:', refreshError);
                        // 갱신 실패시 로그아웃 처리
                        localStorage.removeItem('accessToken');
                        localStorage.removeItem('refreshToken');
                        localStorage.removeItem('username');
                        // 로그인 페이지로 리다이렉션
                        window.location.href = '/login';
                        return Promise.reject(refreshError);
                    }
                }
            }

            if (error.response.status === 404) {
                console.warn(`리소스를 찾을 수 없습니다: ${error.config.url}`);
            } else if (error.response.status === 400) {
                console.warn(`잘못된 요청: ${error.config.url}`, error.response.data);
            }
        } else if (error.request) {
            // 요청이 만들어졌으나 응답이 없는 경우
            console.error('API 요청 에러 (응답 없음):', error.request);
        } else {
            // 요청 설정 중 오류가 발생한 경우
            console.error('API 요청 설정 에러:', error.message);
        }

        return Promise.reject(error);
    }
);

// API 서비스 정의
export default {
    // 인증 관련
    auth: {
        login(credentials) {
            return apiClient.post('/auth/login/', credentials);
        },
        register(userData) {
            return apiClient.post('/auth/register/', userData);
        },
        refreshToken() {
            const refreshToken = localStorage.getItem('refreshToken');
            return apiClient.post('/auth/token/refresh/', { refresh: refreshToken });
        },
        verifyToken(token) {
            return apiClient.post('/auth/token/verify/', { token });
        },
        logout() {
            const refreshToken = localStorage.getItem('refreshToken');
            // 토큰 블랙리스트에 추가
            if (refreshToken) {
                apiClient.post('/auth/token/blacklist/', { refresh: refreshToken })
                    .catch(error => console.error('로그아웃 중 오류:', error));
            }
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('username');
        },
        forgotPassword(email) {
            return apiClient.post('/auth/password-reset/', { email });
        },
        resetPassword(data) {
            return apiClient.post('/auth/password-reset/confirm/', data);
        }
    },

    // 게시글 관련
    posts: {
        getAll() {
            return apiClient.get('/posts/');
        },
        get(slug) {
            return apiClient.get(`/posts/${slug}/`);
        },
        create(postData) {
            return apiClient.post('/posts/', postData);
        },
        update(slug, postData) {
            return apiClient.put(`/posts/${slug}/`, postData);
        },
        delete(slug) {
            return apiClient.delete(`/posts/${slug}/`);
        },
        // 내 글 목록 조회
        getMyPosts() {
            return apiClient.get('/posts/my_posts/');
        },
        // 임시 저장 기능
        saveDraft(postData) {
            return apiClient.post('/posts/draft/', postData);
        }
    },

    // 카테고리 관련
    categories: {
        getAll() {
            return apiClient.get('/categories/');
        },
        get(slug) {
            return apiClient.get(`/categories/${slug}/`);
        },
        create(categoryData) {
            return apiClient.post('/categories/', categoryData);
        },
        update(slug, categoryData) {
            return apiClient.put(`/categories/${slug}/`, categoryData);
        },
        delete(slug) {
            return apiClient.delete(`/categories/${slug}/`);
        }
    },

    // 통계 관련
    stats: {
        get() {
            return apiClient.get('/stats/');
        }
    },

    // 사용자 관련
    user: {
        getProfile() {
            return apiClient.get('/user/profile/');
        },
        updateProfile(profileData) {
            return apiClient.put('/user/profile/', profileData);
        }
    },

    // 블로그 설정 관련
    settings: {
        get() {
            return apiClient.get('/settings/');
        },
        update(settingsData) {
            return apiClient.put('/settings/update/', settingsData);
        }
    },

    // 기타 유틸리티 함수
    createFormData(data) {
        const formData = new FormData();
        Object.keys(data).forEach(key => {
            if (data[key] !== null && data[key] !== undefined) {
                formData.append(key, data[key]);
            }
        });
        return formData;
    }
}; 