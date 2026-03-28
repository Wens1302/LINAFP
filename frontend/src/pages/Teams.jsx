import { useEffect, useState } from 'react';
import { getTeams, createTeam, updateTeam, deleteTeam } from '../services/api';

const EMPTY = { nom: '', ville: '', stade: '', logo: '' };

export default function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState('');
  const role = localStorage.getItem('role');
  const canEdit = role === 'admin' || role === 'editor';

  const load = () =>
    getTeams()
      .then((r) => setTeams(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));

  useEffect(() => { load(); }, []);

  const openCreate = () => { setEditing(null); setForm(EMPTY); setShowForm(true); setError(''); };
  const openEdit = (t) => { setEditing(t); setForm({ nom: t.nom, ville: t.ville, stade: t.stade, logo: t.logo ?? '' }); setShowForm(true); setError(''); };
  const closeForm = () => setShowForm(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (editing) {
        await updateTeam(editing.id, form);
      } else {
        await createTeam(form);
      }
      closeForm();
      load();
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Erreur lors de la sauvegarde.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer cette équipe ?')) return;
    try {
      await deleteTeam(id);
      load();
    } catch (err) {
      alert(err.response?.data?.detail ?? 'Erreur lors de la suppression.');
    }
  };

  if (loading) return <div className="loading">Chargement…</div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Équipes</h1>
        {canEdit && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nouvelle équipe</button>
        )}
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={closeForm}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Modifier l\'équipe' : 'Nouvelle équipe'}</h2>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label>Nom *</label>
                <input value={form.nom} onChange={(e) => setForm({ ...form, nom: e.target.value })} required />
              </div>
              <div className="form-group">
                <label>Ville *</label>
                <input value={form.ville} onChange={(e) => setForm({ ...form, ville: e.target.value })} required />
              </div>
              <div className="form-group">
                <label>Stade *</label>
                <input value={form.stade} onChange={(e) => setForm({ ...form, stade: e.target.value })} required />
              </div>
              <div className="form-group">
                <label>Logo (URL)</label>
                <input value={form.logo} onChange={(e) => setForm({ ...form, logo: e.target.value })} placeholder="https://…" />
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-outline" onClick={closeForm}>Annuler</button>
                <button type="submit" className="btn btn-primary">Enregistrer</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="teams-grid">
        {teams.map((t) => (
          <div key={t.id} className="team-card">
            {t.logo ? (
              <img src={t.logo} alt={t.nom} className="team-logo" />
            ) : (
              <div className="team-logo-placeholder">🏟️</div>
            )}
            <h3 className="team-name">{t.nom}</h3>
            <p className="team-info">📍 {t.ville}</p>
            <p className="team-info">🏟️ {t.stade}</p>
            {canEdit && (
              <div className="card-actions">
                <button className="btn btn-sm btn-outline" onClick={() => openEdit(t)}>Modifier</button>
                <button className="btn btn-sm btn-danger" onClick={() => handleDelete(t.id)}>Supprimer</button>
              </div>
            )}
          </div>
        ))}
      </div>
      {teams.length === 0 && <p className="empty">Aucune équipe enregistrée.</p>}
    </div>
  );
}
