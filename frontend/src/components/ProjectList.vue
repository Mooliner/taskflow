<template>
  <div class="projects-container">
    <ul>
      <!-- Iterem sobre la llista de projectes i mostrem cada un -->
      <li v-for="project in projects" :key="project.id" class="project-item">
        <!-- Nom del projecte amb enllaç a la pàgina del projecte -->
        <div style="font-weight: bold;">
          <router-link :to="`/project/${project.id}`">{{ project.name }}</router-link>
        </div>

        <!-- Descripció del projecte, respectant salts de línia -->
        <p style="white-space: pre-line; margin: 0.5em 0;">
          {{ project.description }}
        </p>

        <!-- Formulari per convidar usuaris, només visible si ets propietari -->
        <div v-if="project.owner_email === userEmail">
          <form @submit.prevent="invite(project.id)">
            <!-- Input per afegir el correu de l’usuari a convidar -->
            <input v-model="emails[project.id]" placeholder="Correu de l'usuari" />
            <button type="submit">Convida</button>
          </form>
          <!-- Missatge d’èxit o error després d’intentar convidar -->
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
// Importem la funció que crida l’API per convidar un usuari a un projecte
import { inviteUserToProject } from '../services/api.js' // ajusta la ruta si cal

// Definim les propietats que rebem: llista de projectes i email de l’usuari actual
const props = defineProps({ projects: Array, userEmail: String })

// Definim un event per notificar a components pares que han de recarregar dades
const emit = defineEmits(['reload'])

// Variable reactiva per guardar els correus introduïts per projecte
const emails = ref({})

// Missatge que mostra si la invitació ha anat bé o hi ha hagut un error
const inviteMessage = ref('')

// Funció que s’executa quan es vol convidar un usuari a un projecte
async function invite(projectId) {
  // Agafem el token d’autenticació i el correu introduït
  const token = localStorage.getItem('token')
  const email = emails.value[projectId]

  try {
    // Cridem l’API per convidar l’usuari
    await inviteUserToProject(projectId, email, token)
    // Mostrem missatge d’èxit
    inviteMessage.value = `Usuari ${email} convidat correctament!`
    // Netejem el camp del correu per aquell projecte
    emails.value[projectId] = ''
    // Emitim esdeveniment per que el component pare recarregui la llista de projectes
    emit('reload')

    // Netejem el missatge després de 3 segons
    setTimeout(() => {
      inviteMessage.value = ''
    }, 3000)
  } catch (error) {
    // Mostrem missatge d’error si falla la invitació
    inviteMessage.value = `Error: ${error.message}`
  }
}
</script>
