<template>
  <form @submit.prevent="submit">
    <!-- Input per al títol de la tasca, camp obligatori -->
    <input v-model="task.title" placeholder="Title" required />
    <!-- Input per a la descripció de la tasca, opcional -->
    <input v-model="task.description" placeholder="Description" />
    <!-- Selector per a l'estat de la tasca -->
    <select v-model="task.status">
      <option value="pending">Pendent</option>
      <option value="in progress">En curs</option>
      <option value="completed">Completat</option>
    </select>
    <!-- Botó que canvia el text segons si és creació o edició -->
    <button type="submit">{{ isEditing ? 'Actualitza' : 'Crear' }}</button>
    <!-- Botó per cancel·lar l'edició, només visible si estem editant -->
    <button v-if="isEditing" @click.prevent="cancel">Cancel·la</button>
  </form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { createTask, updateTask } from '@/services/api.js'

// Propietats rebudes: id del projecte i tasca inicial per editar (opcional)
const props = defineProps({
  projectId: String,
  initialTask: Object
})

// Emissions d'esdeveniments per notificar la creació/actualització o cancel·lació
const emit = defineEmits(['saved', 'cancel'])

// Objecte reactiu que representa la tasca que estem creant o editant
const task = ref({
  title: '',
  description: '',
  status: 'pending'
})

// Computada que indica si estem en mode edició (hi ha tasca inicial)
const isEditing = computed(() => !!props.initialTask)

// Observem canvis a la tasca inicial per actualitzar el formulari quan sigui necessari
watch(() => props.initialTask, (newTask) => {
  if (newTask) {
    // Si rebem una tasca per editar, la copiem al nostre objecte reactiu
    task.value = { ...newTask }
  } else {
    // Si no, resetejem el formulari a valors per defecte
    task.value = { title: '', description: '', status: 'pending' }
  }
}, { immediate: true })

// Funció que s'executa quan es fa submit al formulari
async function submit() {
  const token = localStorage.getItem('token')
  try {
    let savedTask
    if (isEditing.value) {
      // Si estem editant, enviem una petició per actualitzar la tasca existent
      savedTask = await updateTask(token, task.value._id, { 
        title: task.value.title,
        description: task.value.description,
        status: task.value.status,
        project_id: props.projectId
      })
    } else {
      // Si no, creem una nova tasca
      savedTask = await createTask(token, { 
        title: task.value.title,
        description: task.value.description,
        status: task.value.status,
        project_id: props.projectId
      })
    }
    // Emitim l'esdeveniment 'saved' amb la tasca retornada
    emit('saved', savedTask)
  } catch (error) {
    // Si hi ha error, mostrem alerta amb el missatge
    alert(error.message)
  }
}

// Funció per cancel·lar l'edició, emet un esdeveniment 'cancel'
function cancel() {
  emit('cancel')
}
</script>
