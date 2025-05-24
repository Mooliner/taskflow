<template>
  <form @submit.prevent="createProject">
    <input v-model="projectName" placeholder="Project name" required />
    <button type="submit">Create Project</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['project-created'])
const props = defineProps({ userEmail: String })
const projectName = ref('')
const API_URL = 'http://localhost:8000'

async function createProject() {
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/projects`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name: projectName.value, owner_email: props.userEmail }),
  })
  const project = await res.json()
  emit('project-created', project)
  projectName.value = ''
}
</script>