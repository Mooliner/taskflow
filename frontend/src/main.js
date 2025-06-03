import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles.css'  // Importem l’estil unificat

createApp(App).use(router).mount('#app')
