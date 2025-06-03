<template>
  <div>
    <h3>Notificacions</h3>
    <ul>
      <!-- Mostrem la llista de notificacions rebudes -->
      <li v-for="(notif, i) in notifications" :key="i">{{ notif }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
// Importem la funció per crear la connexió websocket de notificacions
import { createNotificationsSocket } from '../services/notificationsSocket.js'

// Array reactiu on guardarem les notificacions rebudes
const notifications = ref([])
// Variable per guardar la connexió websocket
const ws = ref(null)

onMounted(() => {
  // Quan el component es monta, agafem el token desat al localStorage
  const token = localStorage.getItem('token')
  if (!token) return  // Si no hi ha token, no fem res

  // Creem la connexió websocket i definim com gestionar els missatges rebuts
  ws.value = createNotificationsSocket(
    token,
    (message) => {
      // Afegim la notificació rebuda a la llista per mostrar-la
      notifications.value.push(message)
    },
    () => {
      // Quan el websocket es tanca, fem un log a la consola
      console.log('WebSocket closed')
    }
  )
})

onBeforeUnmount(() => {
  // Quan el component es destrueix, tanquem la connexió websocket
  if (ws.value) ws.value.close()
})
</script>
