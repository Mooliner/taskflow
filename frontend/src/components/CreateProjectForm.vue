<template>
  <div class="form-container">
    <!-- Formulari per crear un projecte nou -->
    <form @submit.prevent="handleCreateProject">
      <!-- Input per al nom del projecte (obligatori) -->
      <input v-model="projectName" placeholder="Nom del projecte" required /> <br>
      <!-- Input per a la descripció del projecte (opcional) -->
      <input v-model="projectDescription" placeholder="Descripció del projecte" />
      <button type="submit">Crea un projecte</button>
    </form>
  </div>
</template>

<script setup>
// Importem ref per crear variables reactives i la funció API per crear projectes
import { ref } from 'vue'
import { createProject } from '../services/api.js' // ajusta la ruta segons la ubicació real

// Definim un event que s'emet quan es crea un projecte amb èxit
const emit = defineEmits(['project-created'])

// Variables reactives per emmagatzemar les dades introduïdes per l'usuari
const projectName = ref('')
const projectDescription = ref('')

// Funció que es crida quan es fa submit al formulari per crear un projecte
async function handleCreateProject() {
  // Recuperem el token i email de l'usuari guardats al localStorage per autoritzar la petició
  const token = localStorage.getItem('token')
  const email = localStorage.getItem('userEmail')

  try {
    // Cridem a l'API per crear el projecte, enviant nom, descripció i email del propietari
    const project = await createProject(
      {
        name: projectName.value,
        description: projectDescription.value,
        owner_email: email,
      },
      token
    )
    // Emitim un esdeveniment amb la informació del projecte creat per si algun altre component vol reaccionar
    emit('project-created', project)
    // Netejem els camps del formulari per facilitar la creació d'altres projectes
    projectName.value = ''
    projectDescription.value = ''
  } catch (error) {
    // En cas d'error, mostrem un missatge alertant a l'usuari
    alert(error.message)
  }
}
</script>
