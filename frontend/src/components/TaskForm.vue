<template>
  <form @submit.prevent="submit">
    <input v-model="task.title" placeholder="Title" required />
    <input v-model="task.description" placeholder="Description" />
    <select v-model="task.status">
      <option value="pending">Pendent</option>
      <option value="in progress">En curs</option>
      <option value="completed">Completat</option>
    </select>
    <button type="submit">{{ isEditing ? 'Actualitza' : 'Crear' }}</button>
    <button v-if="isEditing" @click.prevent="cancel">Cancel·la</button>
  </form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { createTask, updateTask } from '@/services/api.js'

const props = defineProps({
  projectId: String,
  initialTask: Object
})

const emit = defineEmits(['saved', 'cancel'])

const task = ref({
  title: '',
  description: '',
  status: 'pending'
})

const isEditing = computed(() => !!props.initialTask)

watch(() => props.initialTask, (newTask) => {
  if (newTask) {
    task.value = { ...newTask }
  } else {
    task.value = { title: '', description: '', status: 'pending' }
  }
}, { immediate: true })

async function submit() {
  const token = localStorage.getItem('token')
  try {
    let savedTask
    if (isEditing.value) {
      savedTask = await updateTask(token, task.value._id, { 
        title: task.value.title,
        description: task.value.description,
        status: task.value.status,
        project_id: props.projectId
      })
    } else {
      savedTask = await createTask(token, { 
        title: task.value.title,
        description: task.value.description,
        status: task.value.status,
        project_id: props.projectId
      })
    }
    emit('saved', savedTask)
  } catch (error) {
    alert(error.message)
  }
}

function cancel() {
  emit('cancel')
}
</script>
