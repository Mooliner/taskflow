<template>
  <div>
    <h1>TaskFlow</h1>

    <ProjectNotifications />

    <AuthForm v-if="!token" @authenticated="onAuthenticated" />

    <div v-else>
      <button @click="logout">Logout</button>
      <CreateProjectForm :userEmail="userEmail" @project-created="onProjectCreated" />
      <ProjectList :projects="projects" :userEmail="userEmail" @reload="loadProjects" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProjectNotifications from '@/components/ProjectNotifications.vue'
import AuthForm from '@/components/AuthForm.vue'
import CreateProjectForm from '@/components/CreateProjectForm.vue'
import ProjectList from '@/components/ProjectList.vue'

const token = ref(localStorage.getItem('token') || '')
const userEmail = ref('')
const projects = ref([])
const API_URL = 'http://localhost:8000'

async function loadProjects() {
  const res = await fetch(`${API_URL}/projects`, {
    headers: { Authorization: `Bearer ${token.value}` },
  })
  projects.value = await res.json()
}

function logout() {
  localStorage.removeItem('token')
  token.value = ''
  userEmail.value = ''
  projects.value = []
}

function onAuthenticated(data) {
  token.value = data.token
  userEmail.value = data.email
  loadProjects()
}

function onProjectCreated(project) {
  projects.value.push(project)
}

onMounted(() => {
  if (token.value) loadProjects()
})
</script>