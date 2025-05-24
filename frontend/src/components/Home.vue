<template>
  <div>
    <h1>TaskFlow</h1>

    <div v-if="!token">
      <div v-if="!isRegistering">
        <!-- Formulari login -->
        <form @submit.prevent="login">
          <input v-model="email" type="email" placeholder="Email" required />
          <input v-model="password" type="password" placeholder="Password" required />
          <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <button @click="isRegistering = true">Register here</button></p>
      </div>

      <div v-else>
        <!-- Formulari registre -->
        <form @submit.prevent="signup">
          <input v-model="name" type="text" placeholder="Name" required />
          <input v-model="email" type="email" placeholder="Email" required />
          <input v-model="password" type="password" placeholder="Password" required />
          <button type="submit">Register</button>
        </form>
        <p>Already have an account? <button @click="isRegistering = false">Login here</button></p>
      </div>
    </div>

    <div v-else>
      <!-- Usuari autenticat -->
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

          <!-- Form per convidar usuaris (només pel propietari) -->
          <div v-if="project.owner_email === userEmail">
            <form @submit.prevent="inviteUser(project.id)">
              <input v-model="inviteEmail[project.id]" placeholder="Invite user email" />
              <button type="submit">Invite</button>
            </form>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const token = ref(localStorage.getItem('token') || '')
const projects = ref([])
const newProjectName = ref('')
const userEmail = ref('')
const email = ref('')
const password = ref('')
const name = ref('')
const isRegistering = ref(false)
const inviteEmail = ref({})

const API_URL = 'http://localhost:8000'

async function loadProjects() {
  try {
    const res = await fetch(`${API_URL}/projects`, {
      headers: { Authorization: `Bearer ${token.value}` },
    })
    if (!res.ok) throw new Error('Error carregant projectes')
    const data = await res.json()
    projects.value = data
  } catch (error) {
    alert(error.message)
  }
}

async function login() {
  try {
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
    email.value = ''
    password.value = ''
    await loadProjects()
  } catch (error) {
    alert('Error de connexió')
  }
}

async function signup() {
  try {
    const res = await fetch(`${API_URL}/users/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name.value, email: email.value, password: password.value }),
    })
    if (!res.ok) {
      const errorData = await res.json()
      alert(`Error de registre: ${errorData.detail || 'Unknown error'}`)
      return
    }
    alert('Usuari registrat correctament. Pots iniciar sessió.')
    isRegistering.value = false
    name.value = ''
    email.value = ''
    password.value = ''
  } catch (error) {
    alert('Error de connexió')
  }
}

async function createProject() {
  try {
    const res = await fetch(`${API_URL}/projects`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`,
      },
      body: JSON.stringify({ name: newProjectName.value, owner_email: userEmail.value }),
    })
    if (!res.ok) {
      alert('Error creant projecte')
      return
    }
    const project = await res.json()
    projects.value.push(project)
    newProjectName.value = ''
    router.push(`/project/${project.id}`)
  } catch (error) {
    alert('Error de connexió')
  }
}

async function inviteUser(projectId) {
  const emailToInvite = inviteEmail.value[projectId]
  if (!emailToInvite) {
    alert("Introdueix un email vàlid")
    return
  }

  try {
    const res = await fetch(`${API_URL}/projects/${projectId}/members?user_email=${encodeURIComponent(emailToInvite)}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    })

    if (!res.ok) {
      const errorData = await res.json()
      alert(`Error: ${errorData.detail || 'No s’ha pogut afegir l’usuari'}`)
      return
    }

    alert(`Usuari ${emailToInvite} afegit correctament`)
    inviteEmail.value[projectId] = ''
    await loadProjects()
  } catch (error) {
    alert("Error de connexió")
  }
}

function logout() {
  localStorage.removeItem('token')
  token.value = ''
  userEmail.value = ''
  projects.value = []
}

onMounted(() => {
  if (token.value) {
    loadProjects()
  }
})
</script>
