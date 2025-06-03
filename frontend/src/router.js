import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'           // ruta corregida
import ProjectView from './views/ProjectView.vue' // ruta corregida

const routes = [
  { path: '/', component: Home },
  { path: '/project/:id', component: ProjectView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router