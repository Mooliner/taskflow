<template>
  <div>
    <ul>
      <li v-for="comment in comments" :key="comment.created_at">
        <i>{{ comment.author }}</i>: {{ comment.content }}
      </li>
    </ul>
    <form @submit.prevent="submit">
      <input v-model="newComment" placeholder="Add comment..." required />
      <button type="submit">Post</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const props = defineProps({ taskId: String })
const comments = ref([])
const newComment = ref('')

async function load() {
  const res = await fetch(`http://localhost:8000/tasks/${props.taskId}/comments`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
  })
  comments.value = await res.json()
}

async function submit() {
  const res = await fetch(`http://localhost:8000/tasks/${props.taskId}/comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify({ content: newComment.value }),
  })
  comments.value = await res.json()
  newComment.value = ''
}

onMounted(load)
</script>