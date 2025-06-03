<template>
  <div>
    <ul>
      <li v-for="comment in comments" :key="comment.created_at" class="comment-li">
        {{ comment.author }}: {{ comment.content }}
      </li>
    </ul>
    <form @submit.prevent="submit">
      <input v-model="newComment" placeholder="Afegeix un comentari..." required />
      <button type="submit">Publica</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchComments, postComment } from '../services/api.js'  // ajusta ruta

const props = defineProps({ taskId: String })
const comments = ref([])
const newComment = ref('')
const token = localStorage.getItem('token')

async function load() {
  try {
    comments.value = await fetchComments(props.taskId, token)
  } catch (error) {
    console.error(error)
  }
}

async function submit() {
  try {
    comments.value = await postComment(props.taskId, newComment.value, token)
    newComment.value = ''
  } catch (error) {
    console.error(error)
  }
}

onMounted(load)
</script>
