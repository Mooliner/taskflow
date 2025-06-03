<template>
  <div class="auth-container">
    <!-- Login Form -->
    <form v-if="!isRegistering" @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Correu electrònic" required />
      <input v-model="password" type="password" placeholder="Contrasenya" required />
      <p v-if="loginError" class="error-message">{{ loginError }}</p>
      <button type="submit">Inici de sessió</button>
      <p>No tens un compte?
        <button type="button" @click="switchToRegister">Registra</button>
      </p>
    </form>

    <!-- Signup Form -->
    <form v-else @submit.prevent="signup">
      <input v-model="name" type="text" placeholder="Nom" required />
      <input v-model="email" type="email" placeholder="Correu electrònic" required />
      <input v-model="password" type="password" placeholder="Contrasenya" required />
      <p v-if="signupError" class="error-message">{{ signupError }}</p>
      <button type="submit">Registra</button>
      <p>Ja teniu un compte?
        <button type="button" @click="switchToLogin">Inici de sessió</button>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { loginUser, signupUser } from '../services/api.js'  // ajusta la ruta segons sigui necessari

const emit = defineEmits(['authenticated'])

const email = ref('')
const password = ref('')
const name = ref('')
const isRegistering = ref(false)
const loginError = ref('')
const signupError = ref('')

function switchToRegister() {
  isRegistering.value = true
  loginError.value = ''
}

function switchToLogin() {
  isRegistering.value = false
  signupError.value = ''
}

async function login() {
  loginError.value = ''
  try {
    const data = await loginUser(email.value, password.value)
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('userEmail', email.value)
    emit('authenticated', { token: data.access_token, email: email.value })
  } catch (error) {
    loginError.value = error.message
  }
}

async function signup() {
  signupError.value = ''
  try {
    await signupUser(name.value, email.value, password.value)
    isRegistering.value = false
    email.value = ''
    password.value = ''
    name.value = ''
  } catch (error) {
    signupError.value = error.message
  }
}
</script>

