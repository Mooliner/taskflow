// src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import ProjectView from './components/ProjectView.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/project/:id', component: ProjectView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
