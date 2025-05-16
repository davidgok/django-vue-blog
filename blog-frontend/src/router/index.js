import { createRouter, createWebHistory } from 'vue-router'

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

export default router 