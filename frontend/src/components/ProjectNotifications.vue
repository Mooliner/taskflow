<template>
  <div>
    <h3>Notificacions</h3>
    <ul>
      <li v-for="(notif, i) in notifications" :key="i">{{ notif }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { createNotificationsSocket } from '../services/notificationsSocket.js'

const notifications = ref([])
const ws = ref(null)

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) return

  ws.value = createNotificationsSocket(token, (message) => {
    notifications.value.push(message)
  }, () => {
    console.log('WebSocket closed')
  })
})

onBeforeUnmount(() => {
  if (ws.value) ws.value.close()
})
</script>
