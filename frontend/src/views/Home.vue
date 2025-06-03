<template>
  <div>
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

    <AuthForm v-if="!token" @authenticated="onAuthenticated" />

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

const token = ref(localStorage.getItem('token') || '')
const userEmail = ref(localStorage.getItem('userEmail') || '')
const projects = ref([])

async function fetchProjects() {
  try {
    projects.value = await loadProjects(token.value)
  } catch (error) {
    alert(error.message)
  }
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('userEmail')
  token.value = ''
  userEmail.value = ''
  projects.value = []
}

function onAuthenticated(data) {
  token.value = data.token
  userEmail.value = data.email
  fetchProjects()
}

function onProjectCreated(project) {
  projects.value.push(project)
}

onMounted(() => {
  if (token.value) fetchProjects()
})
</script>
