// src/services/api.js
const API_URL = 'http://localhost:8000'

export async function loginUser(email, password) {
  const res = await fetch(`${API_URL}/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) throw new Error('Login failed')
  return await res.json()
}

// Similar per signup, loadProjects, createProject, etc.
