<template>
  <ul>
    <li v-for="task in tasks" :key="task._id">
      <b>{{ task.title }}</b> — {{ task.status }}
      <button @click="edit(task)">Editar</button>
      <CommentSection :taskId="task._id" />

    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CommentSection from './CommentSection.vue'
import { loadTasks } from '../services/api.js'

const props = defineProps({ projectId: String })
const tasks = ref([])
const showingComments = ref({})

const emit = defineEmits(['edit'])

async function load() {
  try {
    const token = localStorage.getItem('token')
    tasks.value = await loadTasks(props.projectId, token)
  } catch (error) {
    alert(error.message)
  }
}

function edit(task) {
  emit('edit', task)
}

function toggleComments(taskId) {
  showingComments.value[taskId] = !showingComments.value[taskId]
}

onMounted(load)
</script>
