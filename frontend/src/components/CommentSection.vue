<template>
  <div>
    <!-- Llista de comentaris existents per la tasca -->
    <ul>
      <li v-for="comment in comments" :key="comment.created_at" class="comment-li">
        {{ comment.author }}: {{ comment.content }}
      </li>
    </ul>

    <!-- Formulari per afegir un nou comentari -->
    <form @submit.prevent="submit">
      <input v-model="newComment" placeholder="Afegeix un comentari..." required />
      <button type="submit">Publica</button>
    </form>
  </div>
</template>

<script setup>
// Importem les funcions i hooks necessaris de Vue i l'API
import { ref, onMounted } from 'vue'
import { fetchComments, postComment } from '../services/api.js'  // ajusta ruta segons ubicació

// Definim la propietat que s'espera rebre: l'ID de la tasca (task)
const props = defineProps({ taskId: String })

// Variables reactives per emmagatzemar els comentaris i el nou comentari
const comments = ref([])
const newComment = ref('')

// Obtenim el token d'autenticació desat al localStorage per autoritzar les peticions
const token = localStorage.getItem('token')

// Funció per carregar els comentaris de la tasca quan el component es munta
async function load() {
  try {
    // Fem la crida a l'API per obtenir els comentaris i els guardem
    comments.value = await fetchComments(props.taskId, token)
  } catch (error) {
    console.error("Error carregant comentaris:", error)
  }
}

// Funció per enviar un nou comentari
async function submit() {
  try {
    // Enviem el nou comentari a l'API, i actualitzem la llista amb la resposta
    comments.value = await postComment(props.taskId, newComment.value, token)
    // Netejem el camp del comentari nou
    newComment.value = ''
  } catch (error) {
    console.error("Error publicant comentari:", error)
  }
}

// Quan el component es carrega, cridem a la funció load per obtenir els comentaris
onMounted(load)
</script>
