<template>
  <div>
    <form v-if="!isRegistering" @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
      <p>Don't have an account? <button @click="isRegistering = true">Register</button></p>
    </form>

    <form v-else @submit.prevent="signup">
      <input v-model="name" type="text" placeholder="Name" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Register</button>
      <p>Already have an account? <button @click="isRegistering = false">Login</button></p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['authenticated'])

const email = ref('')
const password = ref('')
const name = ref('')
const isRegistering = ref(false)
const API_URL = 'http://localhost:8000'

async function login() {
  const res = await fetch(`${API_URL}/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value, password: password.value }),
  })
  if (!res.ok) return alert('Login failed')
  const data = await res.json()
  localStorage.setItem('token', data.access_token)
  emit('authenticated', { token: data.access_token, email: email.value })
}

async function signup() {
  const res = await fetch(`${API_URL}/users/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: name.value, email: email.value, password: password.value }),
  })
  if (!res.ok) return alert('Signup failed')
  alert('Account created, please login.')
  isRegistering.value = false
}
</script>