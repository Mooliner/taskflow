<template>
  <div>
    <div class="tasks-header">
      <button class="back-button" @click="goBack">← Torna enrere</button>
      <h1>Project Tasks</h1>
    </div>

    <!-- 🔔 Notificacions -->
    <div class="notifications">
      <h3>🔔 Notificacions</h3>
      <ul>
        <li v-for="(msg, idx) in notifications" :key="idx">
          {{ formatNotification(msg) }}
        </li>
      </ul>
    </div>

    <!-- ➕ Botó per mostrar/ocultar el formulari de crear -->
    <div style="margin: 10px 0;">
      <button @click="toggleCreateForm" :disabled="editingTask !== null">
        {{ showCreateForm ? 'Cancel·la' : '➕ Crea una nova tasca' }}
      </button>
    </div>

    <!-- Formulari de creació (només si no estem editant cap tasca) -->
    <TaskForm
      v-if="showCreateForm && editingTask === null"
      :projectId="projectId"
      @saved="onTaskSaved"
      @cancel="onCancelEdit"
    />

    <!-- 🔁 Llista de tasques -->
    <ul>
      <li v-for="task in tasks" :key="task._id" class="task-li" style="margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <b>{{ task.title }}</b> — {{ task.status }}
          <button @click="editTask(task)" :disabled="editingTask !== null && editingTask._id !== task._id">
            Edita
          </button>
        </div>
        <p style="margin: 5px 0 0 10px; text-align: left;"><b>Descripció:</b> {{ task.description }}</p>

        <!-- Formulari in-place d’edició -->
        <div v-if="editingTask && editingTask._id === task._id" style="margin-top: 10px; padding-left: 10px; border-left: 2px solid #ddd;">
          <TaskForm
            :projectId="projectId"
            :initialTask="editingTask"
            @saved="onTaskSaved"
            @cancel="onCancelEdit"
          />
        </div>

        <div style="margin-top: 10px; padding-left: 10px; border-left: 2px solid #ddd;">
          <CommentSection :taskId="task._id" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'
import CommentSection from '../components/CommentSection.vue'
import TaskForm from '../components/TaskForm.vue'
import { loadTasks, loadComments } from '@/services/api.js'

const route = useRoute()
const token = ref(localStorage.getItem('token') || '')
const projectId = ref(route.params.id)

const tasks = ref([])
const editingTask = ref(null)
const showCreateForm = ref(false)
const comments = ref({})
const notifications = ref([])
let socket = null

function toggleCreateForm() {
  // Si estem editant, no es pot mostrar el formulari de crear
  if (editingTask.value) return
  showCreateForm.value = !showCreateForm.value
}

function goBack() {
  window.history.back()
}

function formatNotification(msg) {
  if (msg.content) return msg.content
  if (msg.message) return msg.message
  return JSON.stringify(msg)
}

async function loadAllTasksAndComments() {
  try {
    tasks.value = await loadTasks(token.value, projectId.value)
    for (const task of tasks.value) {
      comments.value[task._id] = await loadComments(token.value, task._id)
    }
  } catch (error) {
    alert(error.message)
  }
}

function connectWebSocket() {
  if (!token.value) return

  socket = new WebSocket(`ws://localhost:8000/ws/notifications?token=${token.value}`)

  socket.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      if (!msg.project_id || msg.project_id === projectId.value) {
        notifications.value.unshift(msg)
      }
    } catch (err) {
      console.error('Error parsing notification:', err)
    }
  }

  socket.onclose = () => {
    console.warn('WebSocket disconnected, reconnecting...')
    setTimeout(connectWebSocket, 3000)
  }
}

function editTask(task) {
  editingTask.value = { ...task }  // Clonar per evitar modificar directe
  showCreateForm.value = false
}

function onCancelEdit() {
  editingTask.value = null
  showCreateForm.value = false
}

async function onTaskSaved(task) {
  const idx = tasks.value.findIndex(t => t._id === task._id)
  if (idx !== -1) {
    tasks.value[idx] = task
  } else {
    tasks.value.push(task)
  }
  onCancelEdit()
}

onMounted(() => {
  if (token.value) {
    loadAllTasksAndComments()
    connectWebSocket()
  }
})

onBeforeUnmount(() => {
  if (socket) socket.close()
})

watch(() => route.params.id, async (newId) => {
  projectId.value = newId
  await loadAllTasksAndComments()
})
</script>
