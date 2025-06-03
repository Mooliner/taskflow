<template>
  <ul>
    <!-- Llista de tasques del projecte -->
    <li v-for="task in tasks" :key="task._id">
      <!-- Mostrem el títol i l’estat de la tasca -->
      <b>{{ task.title }}</b> — {{ task.status }}
      
      <!-- Botó per emetre esdeveniment d’edició -->
      <button @click="edit(task)">Editar</button>

      <!-- Component que mostra els comentaris associats a la tasca -->
      <CommentSection :taskId="task._id" />
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CommentSection from './CommentSection.vue'
import { loadTasks } from '../services/api.js'

// Rebem l’ID del projecte com a propietat
const props = defineProps({ projectId: String })

// Llista reactiva de tasques
const tasks = ref([])

// Estat opcional per controlar si s’estan mostrant comentaris (no utilitzat ara mateix però pot servir per millores)
const showingComments = ref({})

// Emetem l’esdeveniment ‘edit’ quan es fa clic a “Editar”
const emit = defineEmits(['edit'])

// Carreguem les tasques del projecte actual des del backend
async function load() {
  try {
    const token = localStorage.getItem('token')
    tasks.value = await loadTasks(props.projectId, token)
  } catch (error) {
    alert(error.message)
  }
}

// Funció per emetre la tasca seleccionada per ser editada
function edit(task) {
  emit('edit', task)
}

// Aquesta funció es podria utilitzar per mostrar/ocultar comentaris individualment per tasca
function toggleComments(taskId) {
  showingComments.value[taskId] = !showingComments.value[taskId]
}

// Carreguem les tasques quan el component es monta
onMounted(load)
</script>
