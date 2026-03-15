import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

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
