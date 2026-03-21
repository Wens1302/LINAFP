import axios from 'axios'

const TOKEN_KEY = 'gfs_admin_token'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// Attach token to every request when present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Auth ───────────────────────────────────────────────────────────────────
export const adminLogin = (data) => api.post('/auth/login', data)

// ── Articles ───────────────────────────────────────────────────────────────
export const getArticles = (params = {}) => api.get('/articles', { params })
export const getArticle = (id) => api.get(`/articles/${id}`)
export const createArticle = (data) => api.post('/articles', data)
export const updateArticle = (id, data) => api.put(`/articles/${id}`, data)
export const deleteArticle = (id) => api.delete(`/articles/${id}`)

// ── Teams ──────────────────────────────────────────────────────────────────
export const getTeams = () => api.get('/teams/')
export const getTeam = (id) => api.get(`/teams/${id}/`)
export const createTeam = (data) => api.post('/teams/', data)
export const updateTeam = (id, data) => api.put(`/teams/${id}/`, data)
export const deleteTeam = (id) => api.delete(`/teams/${id}/`)

// ── Players ────────────────────────────────────────────────────────────────
export const getPlayers = (params = {}) => api.get('/players/', { params })
export const getPlayer = (id) => api.get(`/players/${id}/`)
export const createPlayer = (data) => api.post('/players/', data)
export const updatePlayer = (id, data) => api.put(`/players/${id}/`, data)
export const deletePlayer = (id) => api.delete(`/players/${id}/`)

// ── Matches ────────────────────────────────────────────────────────────────
export const getMatches = () => api.get('/matches/')
export const getMatch = (id) => api.get(`/matches/${id}/`)
export const createMatch = (data) => api.post('/matches/', data)
export const updateMatch = (id, data) => api.put(`/matches/${id}/`, data)
export const deleteMatch = (id) => api.delete(`/matches/${id}/`)

// ── Standings ──────────────────────────────────────────────────────────────
export const getStandings = () => api.get('/standings/')

// ── Stats ──────────────────────────────────────────────────────────────────
export const getStats = () => api.get('/stats/')

export default api
