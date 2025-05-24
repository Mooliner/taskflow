<template>
  <div>
    <h2>Project Tasks</h2>

    <!-- 🔔 Notificacions en temps real -->
    <div class="notifications">
      <h3>🔔 Notificacions</h3>
      <ul>
        <li v-for="(msg, idx) in notifications" :key="idx">
          {{ formatNotification(msg) }}
        </li>
      </ul>
    </div>

    <!-- 📝 Llistat de tasques -->
    <ul>
      <li v-for="task in tasks" :key="task._id">
        <b>{{ task.title }}</b> — {{ task.status }}
        <button @click="editTask(task)">Edit</button>
        <button @click="toggleComments(task._id)">Comments</button>

        <!-- 💬 Comentaris -->
        <div v-if="showingComments[task._id]" style="margin-top: 10px;">
          <ul>
            <li
              v-for="comment in comments[task._id] || []"
              :key="comment.created_at"
            >
              <i>{{ comment.author }}</i>: {{ comment.content }}
            </li>
          </ul>
          <form @submit.prevent="submitComment(task._id)" style="margin-top: 5px;">
            <input
              v-model="newComments[task._id]"
              placeholder="Add a comment..."
              required
            />
            <button type="submit">Post</button>
          </form>
        </div>
      </li>
    </ul>

    <!-- ➕ Formulari per afegir/editar tasques -->
    <form @submit.prevent="editingTask ? updateTask() : createTask()" style="margin-top: 20px;">
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
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const token = ref(localStorage.getItem('token') || '')
const projectId = ref(route.params.id)

const API_URL = 'http://localhost:8000'

const tasks = ref([])
const taskForm = ref({ title: '', description: '', status: 'pending' })
const editingTask = ref(null)

// 💬 Comentaris
const comments = ref({})
const newComments = ref({})
const showingComments = ref({})

// 🔔 Notificacions
const notifications = ref([])
let socket = null

function connectWebSocket() {
  if (!token.value) return

  socket = new WebSocket(`ws://localhost:8000/ws/notifications?token=${token.value}`)

  socket.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      // Mostra només les notificacions relacionades amb aquest projecte
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

function formatNotification(msg) {
  if (msg.content) return msg.content
  if (msg.message) return msg.message
  return JSON.stringify(msg)
}

// 🚀 Inicialització
onMounted(() => {
  if (token.value) {
    loadTasks()
    connectWebSocket()
  }
})

onBeforeUnmount(() => {
  if (socket) socket.close()
})

// Reacciona a canvis de projecte
watch(() => route.params.id, newId => {
  projectId.value = newId
  loadTasks()
})

// 📌 CRUD de tasques
async function loadTasks() {
  const res = await fetch(`${API_URL}/tasks?project_id=${projectId.value}`, {
    headers: { Authorization: `Bearer ${token.value}` },
  })
  tasks.value = await res.json()
}

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

// 💬 Comentaris
async function toggleComments(taskId) {
  if (showingComments.value[taskId]) {
    showingComments.value[taskId] = false
    return
  }

  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    headers: { Authorization: `Bearer ${token.value}` },
  })
  const data = await res.json()
  comments.value[taskId] = data
  showingComments.value[taskId] = true
}

async function submitComment(taskId) {
  const content = newComments.value[taskId]
  if (!content) return

  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`,
    },
    body: JSON.stringify({ content }),
  })
  const data = await res.json()
  comments.value[taskId] = data
  newComments.value[taskId] = ''
}
</script>

<style scoped>
.notifications {
  background-color: #f0f8ff;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 6px;
  max-height: 150px;
  overflow-y: auto;
}
</style>
