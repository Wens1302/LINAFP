import { useEffect, useState } from 'react';
import { getPlayers, createPlayer, updatePlayer, deletePlayer, getTeams } from '../services/api';

const EMPTY = {
  nom: '', nationalite: '', poste: '', numero: '', goals: 0,
  statut: 'active', team_id: '', date_naissance: '',
};

const STATUS_LABELS = { active: 'Actif', injured: 'Blessé', suspended: 'Suspendu' };
const POSTES = ['Gardien', 'Défenseur', 'Milieu', 'Attaquant'];

export default function Players() {
  const [players, setPlayers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [filterTeam, setFilterTeam] = useState('');
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState('');
  const role = localStorage.getItem('role');
  const canEdit = role === 'admin' || role === 'editor';

  const load = (teamId) =>
    getPlayers(teamId || undefined)
      .then((r) => setPlayers(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));

  useEffect(() => {
    getTeams().then((r) => setTeams(r.data)).catch(console.error);
    load('');
  }, []);

  const handleFilterChange = (e) => {
    setFilterTeam(e.target.value);
    setLoading(true);
    load(e.target.value);
  };

  const openCreate = () => { setEditing(null); setForm(EMPTY); setShowForm(true); setError(''); };
  const openEdit = (p) => {
    setEditing(p);
    setForm({
      nom: p.nom, nationalite: p.nationalite, poste: p.poste,
      numero: p.numero, goals: p.goals, statut: p.statut,
      team_id: p.team_id, date_naissance: p.date_naissance ?? '',
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
      numero: Number(form.numero),
      goals: Number(form.goals),
      team_id: Number(form.team_id),
      date_naissance: form.date_naissance || null,
    };
    try {
      if (editing) {
        await updatePlayer(editing.id, payload);
      } else {
        await createPlayer(payload);
      }
      closeForm();
      load(filterTeam);
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Erreur lors de la sauvegarde.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer ce joueur ?')) return;
    try {
      await deletePlayer(id);
      load(filterTeam);
    } catch (err) {
      alert(err.response?.data?.detail ?? 'Erreur lors de la suppression.');
    }
  };

  if (loading) return <div className="loading">Chargement…</div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Joueurs</h1>
        {canEdit && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nouveau joueur</button>
        )}
      </div>

      <div className="filters">
        <select value={filterTeam} onChange={handleFilterChange}>
          <option value="">Toutes les équipes</option>
          {teams.map((t) => (
            <option key={t.id} value={t.id}>{t.nom}</option>
          ))}
        </select>
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={closeForm}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Modifier le joueur' : 'Nouveau joueur'}</h2>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit} className="form">
              <div className="form-row">
                <div className="form-group">
                  <label>Nom *</label>
                  <input value={form.nom} onChange={(e) => setForm({ ...form, nom: e.target.value })} required />
                </div>
                <div className="form-group">
                  <label>Nationalité *</label>
                  <input value={form.nationalite} onChange={(e) => setForm({ ...form, nationalite: e.target.value })} required />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Poste *</label>
                  <select value={form.poste} onChange={(e) => setForm({ ...form, poste: e.target.value })} required>
                    <option value="">-- Choisir --</option>
                    {POSTES.map((p) => <option key={p} value={p}>{p}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Numéro *</label>
                  <input type="number" min={1} max={99} value={form.numero} onChange={(e) => setForm({ ...form, numero: e.target.value })} required />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Équipe *</label>
                  <select value={form.team_id} onChange={(e) => setForm({ ...form, team_id: e.target.value })} required>
                    <option value="">-- Choisir --</option>
                    {teams.map((t) => <option key={t.id} value={t.id}>{t.nom}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Statut</label>
                  <select value={form.statut} onChange={(e) => setForm({ ...form, statut: e.target.value })}>
                    {Object.entries(STATUS_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                  </select>
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Date de naissance</label>
                  <input type="date" value={form.date_naissance} onChange={(e) => setForm({ ...form, date_naissance: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Buts</label>
                  <input type="number" min={0} value={form.goals} onChange={(e) => setForm({ ...form, goals: e.target.value })} />
                </div>
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
            <th>#</th>
            <th>Nom</th>
            <th>Poste</th>
            <th>Équipe</th>
            <th>Nationalité</th>
            <th>Buts</th>
            <th>Statut</th>
            {canEdit && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {players.map((p) => (
            <tr key={p.id}>
              <td>{p.numero}</td>
              <td>{p.nom}</td>
              <td>{p.poste}</td>
              <td>{p.team?.nom ?? p.team_id}</td>
              <td>{p.nationalite}</td>
              <td>{p.goals}</td>
              <td>
                <span className={`badge badge-${p.statut}`}>
                  {STATUS_LABELS[p.statut] ?? p.statut}
                </span>
              </td>
              {canEdit && (
                <td>
                  <button className="btn btn-sm btn-outline" onClick={() => openEdit(p)}>Modifier</button>{' '}
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(p.id)}>Supprimer</button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
      {players.length === 0 && <p className="empty">Aucun joueur trouvé.</p>}
    </div>
  );
}
