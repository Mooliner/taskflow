<template>
  <form @submit.prevent="submit">
    <input v-model="task.title" placeholder="Title" required />
    <input v-model="task.description" placeholder="Description" />
    <select v-model="task.status">
      <option>pending</option>
      <option>in progress</option>
      <option>completed</option>
    </select>
    <button type="submit">{{ editing ? 'Update' : 'Create' }}</button>
    <button v-if="editing" @click.prevent="cancel">Cancel</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ projectId: String })
const task = ref({ title: '', description: '', status: 'pending' })
const editing = ref(false)

function cancel() {
  editing.value = false
  task.value = { title: '', description: '', status: 'pending' }
}

async function submit() {
  const token = localStorage.getItem('token')
  const url = editing.value ? `http://localhost:8000/tasks/${task.value._id}` : `http://localhost:8000/tasks`
  const method = editing.value ? 'PATCH' : 'POST'

  const res = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ ...task.value, project_id: props.projectId }),
  })

  if (!res.ok) return alert('Error')
  task.value = { title: '', description: '', status: 'pending' }
  editing.value = false
}
</script>