<template>
  <ul>
    <li v-for="project in projects" :key="project.id">
      <router-link :to="`/project/${project.id}`">{{ project.name }}</router-link>
      <div v-if="project.owner_email === userEmail">
        <form @submit.prevent="invite(project.id)">
          <input v-model="emails[project.id]" placeholder="Invite email" />
          <button type="submit">Invite</button>
        </form>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ projects: Array, userEmail: String })
const emit = defineEmits(['reload'])
const emails = ref({})
const API_URL = 'http://localhost:8000'

async function invite(projectId) {
  const token = localStorage.getItem('token')
  const email = emails.value[projectId]
  await fetch(`${API_URL}/projects/${projectId}/members?user_email=${email}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })
  alert(`Invited ${email}`)
  emails.value[projectId] = ''
  emit('reload')
}
</script>