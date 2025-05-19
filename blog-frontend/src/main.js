import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import './assets/styles.css'

// 외부 리소스 추가를 위한 헬퍼 함수
const addExternalResource = (type, attributes) => {
    const element = document.createElement(type);
    Object.entries(attributes).forEach(([key, value]) => {
        element[key] = value;
    });
    document.head.appendChild(element);
};

// Google Fonts 추가
['https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic',
    'https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800'
].forEach(href => {
    addExternalResource('link', { rel: 'stylesheet', href });
});

// Font Awesome 추가
addExternalResource('script', {
    src: 'https://use.fontawesome.com/releases/v6.3.0/js/all.js',
    crossOrigin: 'anonymous'
});

createApp(App).use(router).mount('#app')
