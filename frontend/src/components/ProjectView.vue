<!-- src/views/ProjectView.vue -->
<template>
  <div>
    <h2>Project Tasks</h2>
    <ul>
      <li v-for="task in tasks" :key="task._id">
        <b>{{ task.title }}</b> — {{ task.status }}
        <button @click="editTask(task)">Edit</button>
      </li>
    </ul>

    <form @submit.prevent="editingTask ? updateTask() : createTask()">
      <input v-model="taskForm.title" placeholder="Title" required />
      <input v-model="taskForm.description" placeholder="Description" />
      <select v-model="taskForm.status">
        <option>pending</option>
        <option>in progress</option>
        <option>completed</option>
      </select>
      <button type="submit">{{ editingTask ? 'Update' : 'Create' }}</button>
      <button v-if="editingTask" @click.prevent="cancelEdit">Cancel</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const token = ref(localStorage.getItem('token') || '')
const projectId = ref(route.params.id)

const tasks = ref([])
const taskForm = ref({ title: '', description: '', status: 'pending' })
const editingTask = ref(null)
const API_URL = 'http://localhost:8000'

async function loadTasks() {
  const res = await fetch(`${API_URL}/tasks?project_id=${projectId.value}`, {
    headers: { Authorization: `Bearer ${token.value}` },
  })
  tasks.value = await res.json()
}

onMounted(() => {
  if (token.value) loadTasks()
})

watch(() => route.params.id, newId => {
  projectId.value = newId
  loadTasks()
})

async function createTask() {
  const res = await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`,
    },
    body: JSON.stringify({ ...taskForm.value, project_id: projectId.value }),
  })
  const newTask = await res.json()
  tasks.value.push(newTask)
  taskForm.value = { title: '', description: '', status: 'pending' }
}

function editTask(task) {
  editingTask.value = task
  taskForm.value = { ...task }
}

function cancelEdit() {
  editingTask.value = null
  taskForm.value = { title: '', description: '', status: 'pending' }
}

async function updateTask() {
  const res = await fetch(`${API_URL}/tasks/${editingTask.value._id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`,
    },
    body: JSON.stringify({ ...taskForm.value, project_id: projectId.value }),
  })
  const updated = await res.json()
  const idx = tasks.value.findIndex(t => t._id === updated._id)
  if (idx !== -1) tasks.value[idx] = updated
  cancelEdit()
}
</script>
