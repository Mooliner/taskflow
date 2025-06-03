<template>
  <div class="projects-container">
    <ul>
      <li v-for="project in projects" :key="project.id" class="project-item">
        <!-- Títol -->
        <div style="font-weight: bold;">
          <router-link :to="`/project/${project.id}`">{{ project.name }}</router-link>
        </div>

        <!-- Descripció -->
        <p style="white-space: pre-line; margin: 0.5em 0;">
          {{ project.description }}
        </p>

        <!-- Formulari per convidar -->
        <div v-if="project.owner_email === userEmail">
          <form @submit.prevent="invite(project.id)">
            <input v-model="emails[project.id]" placeholder="Correu de l'usuari" />
            <button type="submit">Convida</button>
          </form>
          <p v-if="inviteMessage" style="color: green; margin-top: 0.5em;">
            {{ inviteMessage }}
          </p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { inviteUserToProject } from '../services/api.js' // ajusta la ruta si cal

const props = defineProps({ projects: Array, userEmail: String })
const emit = defineEmits(['reload'])
const emails = ref({})
const inviteMessage = ref('')

async function invite(projectId) {
  const token = localStorage.getItem('token')
  const email = emails.value[projectId]

  try {
    await inviteUserToProject(projectId, email, token)
    inviteMessage.value = `Usuari ${email} convidat correctament!`
    emails.value[projectId] = ''
    emit('reload')

    setTimeout(() => {
      inviteMessage.value = ''
    }, 3000)
  } catch (error) {
    inviteMessage.value = `Error: ${error.message}`
  }
}
</script>

