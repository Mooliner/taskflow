<template>
  <div>
    <!-- Capçalera amb botó de tornar enrere i títol -->
    <div class="tasks-header">
      <button class="back-button" @click="goBack">← Torna enrere</button>
      <h1>Project Tasks</h1>
    </div>

    <!-- Llista de notificacions (resum) -->
    <div class="notifications">
      <h3>Notificacions</h3>
      <ul>
        <li v-for="(msg, idx) in notifications" :key="idx">
          {{ formatNotification(msg) }}
        </li>
      </ul>
    </div>

    <!-- Botó per veure historial complet -->
    <button @click="toggleNotificationModal">Historial complet</button>

    <!-- ➕ Botó per afegir una nova tasca -->
    <div style="margin: 10px 0;">
      <button @click="toggleCreateForm" :disabled="editingTask !== null">
        {{ showCreateForm ? 'Cancel·la' : 'Crea una nova tasca' }}
      </button>
    </div>

    <!-- Formulari per crear tasca nova -->
    <TaskForm
      v-if="showCreateForm && editingTask === null"
      :projectId="projectId"
      @saved="onTaskSaved"
      @cancel="onCancelEdit"
    />

    <!-- Llista de tasques amb edició i comentaris -->
    <ul>
      <li v-for="task in tasks" :key="task._id" class="task-li" style="margin-bottom: 20px;">
        <!-- Informació bàsica de la tasca + botó editar -->
        <div style="display: flex; align-items: center; gap: 10px;">
          <b>{{ task.title }}</b> — {{ task.status }}
          <button @click="editTask(task)" :disabled="editingTask !== null && editingTask._id !== task._id">
            Edita
          </button>
        </div>

        <!-- Descripció de la tasca -->
        <p style="margin: 5px 0 0 10px; text-align: left;"><b>Descripció:</b> {{ task.description }}</p>

        <!-- Formulari per editar una tasca (en línia) -->
        <div
          v-if="editingTask && editingTask._id === task._id"
          style="margin-top: 10px; padding-left: 10px; border-left: 2px solid #ddd;"
        >
          <TaskForm
            :projectId="projectId"
            :initialTask="editingTask"
            @saved="onTaskSaved"
            @cancel="onCancelEdit"
          />
        </div>

        <!-- Secció de comentaris -->
        <div style="margin-top: 10px; padding-left: 10px; border-left: 2px solid #ddd;">
          <CommentSection :taskId="task._id" />
        </div>
      </li>
    </ul>
  </div>

  <!-- Modal de notificacions completes -->
  <div v-if="showNotificationModal" class="modal-overlay" @click.self="toggleNotificationModal">
    <div class="modal-content">
      <h2>Totes les notificacions</h2>
      <ul>
        <li v-for="(msg, idx) in notifications" :key="idx" style="margin-bottom: 10px;">
          <div><b>{{ formatNotification(msg) }}</b></div>
          <div style="font-size: 0.8em; color: gray;">{{ formatTimestamp(msg.timestamp) }}</div>
        </li>
      </ul>
      <button @click="toggleNotificationModal">Tanca</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'
import CommentSection from '../components/CommentSection.vue'
import TaskForm from '../components/TaskForm.vue'
import {
  loadTasks,
  loadComments,
  loadNotifications,
} from '@/services/api.js'

// Props (si cal passar l'id de forma externa)
const props = defineProps({ id: String })

// Ruta activa per obtenir l’ID del projecte
const route = useRoute()
const token = ref(localStorage.getItem('token') || '')
const projectId = ref(route.params.id)

// Llistes i estats
const tasks = ref([])
const editingTask = ref(null)
const showCreateForm = ref(false)
const showNotificationModal = ref(false)
const comments = ref({})
const notifications = ref([])
let socket = null

// Mostra o oculta el formulari de crear
function toggleCreateForm() {
  if (editingTask.value) return
  showCreateForm.value = !showCreateForm.value
}

// Funció per tornar enrere
function goBack() {
  window.history.back()
}

// Formata una notificació per mostrar-la
function formatNotification(msg) {
  if (msg.content) return msg.content
  if (msg.message) return msg.message
  return JSON.stringify(msg)
}

// Carrega tasques i els seus comentaris
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

// Connexió WebSocket per notificacions en temps real
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
    console.warn('WebSocket desconectat, reconnectant...')
    setTimeout(connectWebSocket, 3000)
  }
}

// Edita una tasca (formulari en línia)
function editTask(task) {
  editingTask.value = { ...task } // Clonem per evitar mutació directa
  showCreateForm.value = false
}

// Cancel·la l’edició
function onCancelEdit() {
  editingTask.value = null
  showCreateForm.value = false
}

// Després de guardar, actualitza o afegeix la tasca
async function onTaskSaved(task) {
  const idx = tasks.value.findIndex(t => t._id === task._id)
  if (idx !== -1) {
    tasks.value[idx] = task
  } else {
    tasks.value.push(task)
  }
  onCancelEdit()
}

// Mostra o oculta modal de notificacions detallades
async function toggleNotificationModal() {
  if (!showNotificationModal.value) {
    try {
      notifications.value = await loadNotifications(token.value, projectId.value)
    } catch (error) {
      alert('No s’han pogut carregar les notificacions: ' + error.message)
    }
  }
  showNotificationModal.value = !showNotificationModal.value
}

// Format de timestamp llegible
function formatTimestamp(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleString()
}

// Inicia càrrega de dades i socket al muntar
onMounted(() => {
  if (token.value) {
    loadAllTasksAndComments()
    connectWebSocket()
  }
})

// Tanca socket si es desmunta el component
onBeforeUnmount(() => {
  if (socket) socket.close()
})

// Reacciona si canvia l’id del projecte
watch(() => route.params.id, async (newId) => {
  projectId.value = newId
  await loadAllTasksAndComments()
})
</script>
