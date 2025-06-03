// src/services/api.js
const API_URL = 'http://localhost:8000'

export async function loginUser(email, password) {
  const res = await fetch(`${API_URL}/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) {
    const errorData = await res.json()
    throw new Error(errorData.detail || 'Login failed')
  }
  return await res.json()
}

export async function signupUser(name, email, password) {
  const res = await fetch(`${API_URL}/users/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password }),
  })
  if (!res.ok) {
    const errorData = await res.json()
    throw new Error(errorData.detail || 'Signup failed')
  }
  return await res.json()
}

//Comment
export async function fetchComments(taskId, token) {
  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Failed to load comments')
  return await res.json()
}

export async function postComment(taskId, content, token) {
  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ content }),
  })
  if (!res.ok) throw new Error('Failed to post comment')
  return await res.json()
}

//CreateProject

export async function createProject({ name, description, owner_email }, token) {
  const res = await fetch(`${API_URL}/projects`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name, description, owner_email }),
  })

  if (!res.ok) {
    const errorData = await res.json()
    throw new Error(errorData.detail || 'Failed to create project')
  }

  return await res.json()
}

//ProjectList

export async function inviteUserToProject(projectId, email, token) {
  const res = await fetch(`${API_URL}/projects/${projectId}/members?user_email=${email}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })

  if (!res.ok) {
    const errorData = await res.json()
    throw new Error(errorData.detail || 'Error convidant usuari')
  }

  return await res.json()
}

//ProjectNotificactions
export function createNotificationsSocket(token, onMessageCallback, onCloseCallback) {
  if (!token) throw new Error('Token is required')

  const ws = new WebSocket(`ws://localhost:8000/ws/notifications?token=${token}`)

  ws.onmessage = event => {
    onMessageCallback(event.data)
  }

  ws.onclose = () => {
    if (onCloseCallback) onCloseCallback()
  }

  return ws
}

//TaskForm




//TaskList


//Home
export async function loadProjects(token) {
  const res = await fetch(`${API_URL}/projects`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error loading projects')
  return await res.json()
}

//ProjectList
export async function loadTasks(token, projectId) {
  const res = await fetch(`${API_URL}/tasks?project_id=${projectId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error loading tasks')
  return await res.json()
}

export async function loadComments(token, taskId) {
  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error loading comments')
  return await res.json()
}

export async function createTask(token, task) {
  const res = await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(task),
  })
  if (!res.ok) throw new Error('Error creating task')
  return await res.json()
}

export async function updateTask(token, taskId, task) {
  const res = await fetch(`${API_URL}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(task),
  })
  if (!res.ok) throw new Error('Error updating task')
  return await res.json()
}