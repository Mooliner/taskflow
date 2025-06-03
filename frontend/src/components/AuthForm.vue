<template>
  <div class="auth-container">
    <!-- Formulari d'inici de sessió (visible quan no estem registrant) -->
    <form v-if="!isRegistering" @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Correu electrònic" required />
      <input v-model="password" type="password" placeholder="Contrasenya" required />
      <!-- Mostra error si hi ha problema al login -->
      <p v-if="loginError" class="error-message">{{ loginError }}</p>
      <button type="submit">Inici de sessió</button>
      <p>No tens un compte?
        <!-- Botó per canviar a formulari de registre -->
        <button type="button" @click="switchToRegister">Registra</button>
      </p>
    </form>

    <!-- Formulari de registre (visible quan estem registrant) -->
    <form v-else @submit.prevent="signup">
      <input v-model="name" type="text" placeholder="Nom" required />
      <input v-model="email" type="email" placeholder="Correu electrònic" required />
      <input v-model="password" type="password" placeholder="Contrasenya" required />
      <!-- Mostra error si hi ha problema al registre -->
      <p v-if="signupError" class="error-message">{{ signupError }}</p>
      <button type="submit">Registra</button>
      <p>Ja teniu un compte?
        <!-- Botó per canviar a formulari de login -->
        <button type="button" @click="switchToLogin">Inici de sessió</button>
      </p>
    </form>
  </div>
</template>

<script setup>
// Importem funcions reactives i mètodes per fer peticions a l'API
import { ref } from 'vue'
import { loginUser, signupUser } from '../services/api.js'  // ajusta la ruta segons sigui necessari

// Definim l'event que emetrem quan l'usuari s'autentiqui correctament
const emit = defineEmits(['authenticated'])

// Variables reactives que emmagatzemen les dades dels formularis i estats d'error
const email = ref('')
const password = ref('')
const name = ref('')
const isRegistering = ref(false)  // controla quin formulari es mostra: login o registre
const loginError = ref('')         // error de login, si n'hi ha
const signupError = ref('')        // error de registre, si n'hi ha

// Canvia a formulari de registre i neteja errors de login
function switchToRegister() {
  isRegistering.value = true
  loginError.value = ''
}

// Canvia a formulari de login i neteja errors de registre
function switchToLogin() {
  isRegistering.value = false
  signupError.value = ''
}

// Procés d'inici de sessió
async function login() {
  loginError.value = ''  // netegem errors previs
  try {
    // Intentem autenticar l'usuari mitjançant la funció del servei API
    const data = await loginUser(email.value, password.value)
    // Guardem el token i email a localStorage per mantenir la sessió
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('userEmail', email.value)
    // Emem un event per notificar a components pares que l'usuari està autenticat
    emit('authenticated', { token: data.access_token, email: email.value })
  } catch (error) {
    // Si hi ha error, el mostrem a l'usuari
    loginError.value = error.message
  }
}

// Procés de registre d'un nou usuari
async function signup() {
  signupError.value = ''  // netegem errors previs
  try {
    // Intentem registrar l'usuari a l'API
    await signupUser(name.value, email.value, password.value)
    // Si funciona, tornem al formulari de login i netegem camps
    isRegistering.value = false
    email.value = ''
    password.value = ''
    name.value = ''
  } catch (error) {
    // Si hi ha error, el mostrem a l'usuari
    signupError.value = error.message
  }
}
</script>
