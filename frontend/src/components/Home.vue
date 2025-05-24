<template>
  <div>
    <h1>TaskFlow</h1>

    <div v-if="!token">
      <!-- Formulari login -->
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
    </div>

    <div v-else>
      <button @click="logout">Logout</button>

      <!-- Crear projecte -->
      <h2>Create Project</h2>
      <form @submit.prevent="createProject">
        <input v-model="newProjectName" placeholder="Project name" required />
        <button type="submit">Create Project</button>
      </form>

      <!-- Llista de projectes -->
      <h2>Your Projects</h2>
      <ul>
        <li v-for="project in projects" :key="project.id">
          <router-link :to="`/project/${project.id}`">{{ project.name }}</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Variables reactives
const token = ref(localStorage.getItem('token') || '')
const projects = ref([])
const newProjectName = ref('')
const userEmail = ref('')
const email = ref('')
const password = ref('')

const API_URL = 'http://localhost:8000'

// Funció per carregar projectes
async function loadProjects() {
  const res = await fetch(`${API_URL}/projects`, {
    headers: { Authorization: `Bearer ${token.value}` },
  })
  const data = await res.json()
  projects.value = data
}

// Funció per fer login
async function login() {
  const res = await fetch(`${API_URL}/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value, password: password.value }),
  })

  if (!res.ok) {
    alert('Error de login')
    return
  }

  const data = await res.json()
  localStorage.setItem('token', data.access_token)
  token.value = data.access_token
  userEmail.value = email.value
  loadProjects()
}
// Funció per crear projecte
async function createProject() {
  const res = await fetch(`${API_URL}/projects`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`,
    },
    body: JSON.stringify({ name: newProjectName.value, owner_email: userEmail.value }),
  })
  const project = await res.json()
  projects.value.push(project)
  router.push(`/project/${project.id}`)
}

// Funció per logout
function logout() {
  localStorage.removeItem('token')
  token.value = ''
  userEmail.value = ''
  projects.value = []
}

// Quan el component s'inicia, si hi ha token, carrega projectes
onMounted(() => {
  if (token.value) {
    loadProjects()
  }
})
</script>
