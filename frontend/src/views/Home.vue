<template>
  <div>
    <!-- Capçalera amb títol i botó de logout -->
    <div class="header-bg">
      <h1>TaskFlow</h1>
      <button
        v-if="token"
        class="logout-button"
        @click="logout"
      >
        Tanca la sessió
      </button>
    </div>

    <!-- Formulari d’autenticació si no hi ha token -->
    <AuthForm v-if="!token" @authenticated="onAuthenticated" />

    <!-- Si hi ha token, mostra formulari per crear projectes i la llista -->
    <div v-else>
      <CreateProjectForm :userEmail="userEmail" @project-created="onProjectCreated" />
      <ProjectList :projects="projects" :userEmail="userEmail" @reload="loadProjects" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AuthForm from '@/components/AuthForm.vue'
import CreateProjectForm from '@/components/CreateProjectForm.vue'
import ProjectList from '@/components/ProjectList.vue'
import { loadProjects } from '@/services/api.js'

// Referència reactiva al token i correu, obtinguts del localStorage
const token = ref(localStorage.getItem('token') || '')
const userEmail = ref(localStorage.getItem('userEmail') || '')

// Projectes de l’usuari autenticat
const projects = ref([])

/**
 * Carrega els projectes des del servidor utilitzant el token.
 */
async function fetchProjects() {
  try {
    projects.value = await loadProjects(token.value)
  } catch (error) {
    alert(error.message)
  }
}

/**
 * Tanca la sessió: esborra token, email i reinicia dades.
 */
function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('userEmail')
  token.value = ''
  userEmail.value = ''
  projects.value = []
}

/**
 * Gestiona l’autenticació correcta: desa token/email i carrega projectes.
 */
function onAuthenticated(data) {
  token.value = data.token
  userEmail.value = data.email
  fetchProjects()
}

/**
 * Afegeix un projecte nou a la llista després de la seva creació.
 */
function onProjectCreated(project) {
  projects.value.push(project)
}

// Si hi ha token en muntar el component, carrega els projectes
onMounted(() => {
  if (token.value) fetchProjects()
})
</script>
