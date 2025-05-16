import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import './assets/styles.css'

// Add Google Fonts
const link1 = document.createElement('link');
link1.rel = 'stylesheet';
link1.href = 'https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic';
document.head.appendChild(link1);

const link2 = document.createElement('link');
link2.rel = 'stylesheet';
link2.href = 'https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800';
document.head.appendChild(link2);

// Add Font Awesome
const link3 = document.createElement('script');
link3.src = 'https://use.fontawesome.com/releases/v6.3.0/js/all.js';
link3.crossOrigin = 'anonymous';
document.head.appendChild(link3);

const app = createApp(App)
app.use(router)
app.mount('#app')
