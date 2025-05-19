import { createRouter, createWebHistory } from 'vue-router'

// 인증이 필요한 라우트 정의
const authRequiredRoutes = ['PostWrite', 'Manage', 'CategoryManage'];

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/PostList.vue')
    },
    {
        path: '/post/:slug',
        name: 'PostDetail',
        component: () => import('../views/PostDetail.vue')
    },
    {
        path: '/categories',
        name: 'Categories',
        component: () => import('../views/CategoryList.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/LoginPage.vue')
    },
    {
        path: '/write',
        name: 'PostWrite',
        component: () => import('../views/PostWritePage.vue')
    },
    {
        path: '/manage',
        name: 'Manage',
        component: () => import('../views/ManagePage.vue')
    },
    {
        path: '/manage/categories',
        name: 'CategoryManage',
        component: () => import('../views/CategoryManagePage.vue')
    },
    {
        path: '/forgot-password',
        name: 'ForgotPassword',
        component: () => import('../views/ForgotPasswordPage.vue')
    },
    {
        path: '/reset-password',
        name: 'ResetPassword',
        component: () => import('../views/ResetPasswordPage.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/RegisterPage.vue')
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

// 네비게이션 가드 설정: 인증이 필요한 페이지 접근 제어
router.beforeEach((to, from, next) => {
    const isAuthRequired = authRequiredRoutes.includes(to.name);
    const isLoggedIn = !!localStorage.getItem('accessToken');

    if (isAuthRequired && !isLoggedIn) {
        // 인증이 필요한 페이지인데 로그인이 안 되어 있으면 로그인 페이지로 리다이렉트
        next({ name: 'Login', query: { redirect: to.fullPath } });
    } else {
        // 그렇지 않으면 요청한 페이지로 이동
        next();
    }
});

export default router 