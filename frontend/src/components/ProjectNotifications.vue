<template>
  <div>
    <h3>Notifications</h3>
    <ul>
      <li v-for="(notif, i) in notifications" :key="i">{{ notif }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const notifications = ref([])
const ws = ref(null)

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) return

  ws.value = new WebSocket(`ws://localhost:8000/ws/notifications?token=${token}`)

  ws.value.onmessage = event => {
    notifications.value.push(event.data)
  }

  ws.value.onclose = () => {
    console.log('WebSocket closed')
  }
})

onBeforeUnmount(() => {
  if (ws.value) ws.value.close()
})
</script>
