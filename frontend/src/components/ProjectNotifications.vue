<!-- src/components/ProjectNotifications.vue -->
<template>
  <div class="notifications">
    <h3>🔔 Notificacions</h3>
    <ul>
      <li v-for="(msg, idx) in messages" :key="idx">
        {{ formatMessage(msg) }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const messages = ref([])
let socket = null

function connectWebSocket() {
  const token = localStorage.getItem('token')
  socket = new WebSocket(`ws://localhost:8000/ws/notifications?token=${token}`)

  socket.onmessage = event => {
    try {
      const message = JSON.parse(event.data)
      messages.value.unshift(message)
    } catch {
      messages.value.unshift({ content: event.data })
    }
  }

  socket.onclose = () => {
    console.warn('WebSocket tancat. Reintentant en 3s...')
    setTimeout(connectWebSocket, 3000)
  }
}

function formatMessage(msg) {
  return msg?.content || JSON.stringify(msg)
}

onMounted(connectWebSocket)
onBeforeUnmount(() => {
  if (socket) socket.close()
})
</script>

<style scoped>
.notifications {
  background: #eef;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 20px;
  max-height: 200px;
  overflow-y: auto;
}
</style>
