<template>
  <div class="form-container">
    <form @submit.prevent="createProject">
      <input v-model="projectName" placeholder="Nom del projecte" required /> <br>
      <input v-model="projectDescription" placeholder="Descripció del projecte" />
      <button type="submit">Crea un projecte</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createProject } from '../services/api.js' // ajusta ruta

const emit = defineEmits(['project-created'])
const projectName = ref('')
const projectDescription = ref('')

async function handleCreateProject() {
  const token = localStorage.getItem('token')
  const email = localStorage.getItem('userEmail')

  try {
    const project = await createProject(
      {
        name: projectName.value,
        description: projectDescription.value,
        owner_email: email,
      },
      token
    )
    emit('project-created', project)
    projectName.value = ''
    projectDescription.value = ''
  } catch (error) {
    alert(error.message)
  }
}
</script>
