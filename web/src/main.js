import { createApp } from 'vue';
import './assets/base.css'; // Import global theme styles
import App from './App.vue';
import router from './router'; // 确保路径正确

const app = createApp(App);
app.use(router);
app.mount('#app');
