<template>
  <ul>
    <li v-for="task in tasks" :key="task._id">
      <b>{{ task.title }}</b> — {{ task.status }}
      <button @click="edit(task)">Edit</button>
      <button @click="toggleComments(task._id)">Comments</button>
      <CommentSection v-if="showingComments[task._id]" :taskId="task._id" />
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CommentSection from './CommentSection.vue'
const props = defineProps({ projectId: String })
const tasks = ref([])
const showingComments = ref({})

const emit = defineEmits(['edit'])

async function load() {
  const res = await fetch(`http://localhost:8000/tasks?project_id=${props.projectId}`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
  })
  tasks.value = await res.json()
}

function edit(task) {
  emit('edit', task)
}

function toggleComments(taskId) {
  showingComments.value[taskId] = !showingComments.value[taskId]
}

onMounted(load)
</script>