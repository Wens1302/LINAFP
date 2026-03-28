import { useEffect, useState } from 'react';
import {
  getMatches, createMatch, updateMatch, deleteMatch,
  getTeams, getSeasons,
} from '../services/api';

const EMPTY = {
  home_team_id: '', away_team_id: '', date: '', stade: '',
  journee: '', status: 'scheduled', home_score: 0, away_score: 0,
  season_id: '',
};

const STATUS_LABELS = {
  scheduled: 'Programmé',
  in_progress: 'En cours',
  finished: 'Terminé',
  postponed: 'Reporté',
  cancelled: 'Annulé',
};

export default function Matches() {
  const [matches, setMatches] = useState([]);
  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);
  const [filterSeason, setFilterSeason] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState('');
  const role = localStorage.getItem('role');
  const canEdit = role === 'admin' || role === 'editor';

  const load = (seasonId, status) => {
    const params = {};
    if (seasonId) params.season_id = seasonId;
    if (status) params.status = status;
    return getMatches(params)
      .then((r) => setMatches(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    Promise.all([getTeams(), getSeasons()])
      .then(([t, s]) => { setTeams(t.data); setSeasons(s.data); })
      .catch(console.error);
    load('', '');
  }, []);

  const openCreate = () => { setEditing(null); setForm(EMPTY); setShowForm(true); setError(''); };
  const openEdit = (m) => {
    setEditing(m);
    setForm({
      home_team_id: m.home_team_id,
      away_team_id: m.away_team_id,
      date: m.date ? m.date.slice(0, 16) : '',
      stade: m.stade,
      journee: m.journee ?? '',
      status: m.status,
      home_score: m.home_score,
      away_score: m.away_score,
      season_id: m.season_id ?? '',
    });
    setShowForm(true);
    setError('');
  };
  const closeForm = () => setShowForm(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const payload = {
      ...form,
      home_team_id: Number(form.home_team_id),
      away_team_id: Number(form.away_team_id),
      home_score: Number(form.home_score),
      away_score: Number(form.away_score),
      journee: form.journee ? Number(form.journee) : null,
      season_id: form.season_id ? Number(form.season_id) : null,
    };
    try {
      if (editing) {
        await updateMatch(editing.id, payload);
      } else {
        await createMatch(payload);
      }
      closeForm();
      load(filterSeason, filterStatus);
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Erreur lors de la sauvegarde.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer ce match ?')) return;
    try {
      await deleteMatch(id);
      load(filterSeason, filterStatus);
    } catch (err) {
      alert(err.response?.data?.detail ?? 'Erreur lors de la suppression.');
    }
  };

  const handleFilter = (season, status) => {
    setFilterSeason(season);
    setFilterStatus(status);
    setLoading(true);
    load(season, status);
  };

  const teamName = (id) => teams.find((t) => t.id === id)?.nom ?? id;

  if (loading) return <div className="loading">Chargement…</div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Matchs</h1>
        {canEdit && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nouveau match</button>
        )}
      </div>

      <div className="filters">
        <select
          value={filterSeason}
          onChange={(e) => handleFilter(e.target.value, filterStatus)}
        >
          <option value="">Toutes les saisons</option>
          {seasons.map((s) => (
            <option key={s.id} value={s.id}>{s.nom}</option>
          ))}
        </select>
        <select
          value={filterStatus}
          onChange={(e) => handleFilter(filterSeason, e.target.value)}
        >
          <option value="">Tous les statuts</option>
          {Object.entries(STATUS_LABELS).map(([v, l]) => (
            <option key={v} value={v}>{l}</option>
          ))}
        </select>
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={closeForm}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Modifier le match' : 'Nouveau match'}</h2>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit} className="form">
              <div className="form-row">
                <div className="form-group">
                  <label>Équipe domicile *</label>
                  <select value={form.home_team_id} onChange={(e) => setForm({ ...form, home_team_id: e.target.value })} required>
                    <option value="">-- Choisir --</option>
                    {teams.map((t) => <option key={t.id} value={t.id}>{t.nom}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Équipe extérieur *</label>
                  <select value={form.away_team_id} onChange={(e) => setForm({ ...form, away_team_id: e.target.value })} required>
                    <option value="">-- Choisir --</option>
                    {teams.map((t) => <option key={t.id} value={t.id}>{t.nom}</option>)}
                  </select>
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Date *</label>
                  <input type="datetime-local" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} required />
                </div>
                <div className="form-group">
                  <label>Stade *</label>
                  <input value={form.stade} onChange={(e) => setForm({ ...form, stade: e.target.value })} required />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Journée</label>
                  <input type="number" min={1} value={form.journee} onChange={(e) => setForm({ ...form, journee: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Saison</label>
                  <select value={form.season_id} onChange={(e) => setForm({ ...form, season_id: e.target.value })}>
                    <option value="">-- Aucune --</option>
                    {seasons.map((s) => <option key={s.id} value={s.id}>{s.nom}</option>)}
                  </select>
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Score domicile</label>
                  <input type="number" min={0} value={form.home_score} onChange={(e) => setForm({ ...form, home_score: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Score extérieur</label>
                  <input type="number" min={0} value={form.away_score} onChange={(e) => setForm({ ...form, away_score: e.target.value })} />
                </div>
              </div>
              <div className="form-group">
                <label>Statut</label>
                <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                  {Object.entries(STATUS_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                </select>
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-outline" onClick={closeForm}>Annuler</button>
                <button type="submit" className="btn btn-primary">Enregistrer</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <table className="table">
        <thead>
          <tr>
            <th>J.</th>
            <th>Date</th>
            <th>Domicile</th>
            <th>Score</th>
            <th>Extérieur</th>
            <th>Stade</th>
            <th>Statut</th>
            {canEdit && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {matches.map((m) => (
            <tr key={m.id}>
              <td>{m.journee ?? '–'}</td>
              <td>{new Date(m.date).toLocaleDateString('fr-FR')}</td>
              <td>{m.home_team?.nom ?? teamName(m.home_team_id)}</td>
              <td className="score">{m.home_score} – {m.away_score}</td>
              <td>{m.away_team?.nom ?? teamName(m.away_team_id)}</td>
              <td>{m.stade}</td>
              <td>
                <span className={`badge badge-${m.status}`}>
                  {STATUS_LABELS[m.status] ?? m.status}
                </span>
              </td>
              {canEdit && (
                <td>
                  <button className="btn btn-sm btn-outline" onClick={() => openEdit(m)}>Modifier</button>{' '}
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(m.id)}>Supprimer</button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
      {matches.length === 0 && <p className="empty">Aucun match trouvé.</p>}
    </div>
  );
}
