import axios from 'axios';

const TOKEN_KEY = 'gfs_admin_token';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// Attach token to every request when present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Auth ──────────────────────────────────────────────────────────────────────
export const adminLogin = (data) => api.post('/auth/login', data);

// ── Competitions ──────────────────────────────────────────────────────────────
export const getCompetitions = () => api.get('/competitions');
export const getCompetition = (id) => api.get(`/competitions/${id}`);
export const createCompetition = (data) => api.post('/competitions', data);
export const updateCompetition = (id, data) => api.put(`/competitions/${id}`, data);
export const deleteCompetition = (id) => api.delete(`/competitions/${id}`);

// ── Seasons ───────────────────────────────────────────────────────────────────
export const getSeasons = (competitionId) =>
  api.get('/seasons', { params: competitionId ? { competition_id: competitionId } : {} });
export const getSeason = (id) => api.get(`/seasons/${id}`);
export const createSeason = (data) => api.post('/seasons', data);
export const updateSeason = (id, data) => api.put(`/seasons/${id}`, data);
export const deleteSeason = (id) => api.delete(`/seasons/${id}`);

// ── Teams ─────────────────────────────────────────────────────────────────────
export const getTeams = () => api.get('/teams');
export const getTeam = (id) => api.get(`/teams/${id}`);
export const createTeam = (data) => api.post('/teams', data);
export const updateTeam = (id, data) => api.put(`/teams/${id}`, data);
export const deleteTeam = (id) => api.delete(`/teams/${id}`);

// ── Players ───────────────────────────────────────────────────────────────────
export const getPlayers = (teamId) =>
  api.get('/players', { params: teamId ? { team_id: teamId } : {} });
export const getPlayer = (id) => api.get(`/players/${id}`);
export const createPlayer = (data) => api.post('/players', data);
export const updatePlayer = (id, data) => api.put(`/players/${id}`, data);
export const deletePlayer = (id) => api.delete(`/players/${id}`);

// ── Squad memberships ─────────────────────────────────────────────────────────
export const getSquadMemberships = (params) =>
  api.get('/squad-memberships', { params });
export const createSquadMembership = (data) => api.post('/squad-memberships', data);
export const updateSquadMembership = (id, data) => api.put(`/squad-memberships/${id}`, data);
export const deleteSquadMembership = (id) => api.delete(`/squad-memberships/${id}`);

// ── Matches ───────────────────────────────────────────────────────────────────
export const getMatches = (params) =>
  api.get('/matches', { params });
export const getMatch = (id) => api.get(`/matches/${id}`);
export const createMatch = (data) => api.post('/matches', data);
export const updateMatch = (id, data) => api.put(`/matches/${id}`, data);
export const deleteMatch = (id) => api.delete(`/matches/${id}`);

// ── Match Events ──────────────────────────────────────────────────────────────
export const getMatchEvents = (matchId) => api.get(`/matches/${matchId}/events`);
export const createMatchEvent = (matchId, data) => api.post(`/matches/${matchId}/events`, data);
export const updateMatchEvent = (matchId, eventId, data) =>
  api.put(`/matches/${matchId}/events/${eventId}`, data);
export const deleteMatchEvent = (matchId, eventId) =>
  api.delete(`/matches/${matchId}/events/${eventId}`);

// ── Standings ─────────────────────────────────────────────────────────────────
export const getStandings = (seasonId) =>
  api.get('/standings', { params: seasonId ? { season_id: seasonId } : {} });

// ── Stats ─────────────────────────────────────────────────────────────────────
export const getStats = (seasonId) =>
  api.get('/stats', { params: seasonId ? { season_id: seasonId } : {} });

// ── Articles ──────────────────────────────────────────────────────────────────
export const getArticles = () => api.get('/articles');
export const getArticle = (id) => api.get(`/articles/${id}`);
export const createArticle = (data) => api.post('/articles', data);
export const updateArticle = (id, data) => api.put(`/articles/${id}`, data);
export const deleteArticle = (id) => api.delete(`/articles/${id}`);

export default api;
