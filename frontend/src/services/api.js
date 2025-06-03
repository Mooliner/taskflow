// src/services/api.js

// URL base de l’API backend
const API_URL = 'http://localhost:8000'

/**
 * Inicia sessió amb email i contrasenya.
 * Retorna un token JWT si l’autenticació és correcta.
 */
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

/**
 * Registra un nou usuari amb nom, email i contrasenya.
 */
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

// -------------------- Comentaris --------------------

/**
 * Carrega els comentaris d’una tasca donada.
 */
export async function fetchComments(taskId, token) {
  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Failed to load comments')
  return await res.json()
}

/**
 * Publica un nou comentari a una tasca.
 */
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

// -------------------- Projectes --------------------

/**
 * Crea un nou projecte amb nom, descripció i correu de l’usuari propietari.
 */
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

/**
 * Convida un usuari a un projecte mitjançant el seu email.
 */
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

// -------------------- Notificacions --------------------

/**
 * Crea una connexió WebSocket per rebre notificacions en temps real.
 * Accepta funcions de callback per gestionar missatges i tancaments.
 */
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

// -------------------- Carrega de dades --------------------

/**
 * Carrega la llista de projectes associats a l’usuari autenticat.
 */
export async function loadProjects(token) {
  const res = await fetch(`${API_URL}/projects`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error loading projects')
  return await res.json()
}

/**
 * Carrega les tasques d’un projecte concret.
 */
export async function loadTasks(token, projectId) {
  const res = await fetch(`${API_URL}/tasks?project_id=${projectId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error loading tasks')
  return await res.json()
}

/**
 * Carrega els comentaris d’una tasca concreta.
 * (Funció duplicada, també existeix com `fetchComments`)
 */
export async function loadComments(token, taskId) {
  const res = await fetch(`${API_URL}/tasks/${taskId}/comments`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error loading comments')
  return await res.json()
}

// -------------------- Tasques --------------------

/**
 * Crea una nova tasca associada a un projecte.
 */
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

/**
 * Actualitza una tasca existent amb els camps modificats.
 */
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

/**
 * Carrega notificacions associades a un projecte.
 */
export async function loadNotifications(token, projectId) {
  const res = await fetch(`${API_URL}/projects/${projectId}/notifications`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (!res.ok) throw new Error('Error carregant notificacions')
  return await res.json()
}
