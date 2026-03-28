import { useEffect, useState } from 'react';
import { getArticles, createArticle, updateArticle, deleteArticle } from '../services/api';

const EMPTY = { titre: '', contenu: '', image_url: '', categorie: 'news', auteur: 'Rédaction LINAFP', publie: true };
const CATEGORIES = ['news', 'match', 'transfert'];

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState('');
  const role = localStorage.getItem('role');
  const canEdit = role === 'admin';

  const load = () =>
    getArticles()
      .then((r) => setArticles(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));

  useEffect(() => { load(); }, []);

  const openCreate = () => { setEditing(null); setForm(EMPTY); setShowForm(true); setError(''); };
  const openEdit = (a) => {
    setEditing(a);
    setForm({ titre: a.titre, contenu: a.contenu, image_url: a.image_url ?? '', categorie: a.categorie, auteur: a.auteur, publie: a.publie });
    setShowForm(true);
    setError('');
  };
  const closeForm = () => setShowForm(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (editing) {
        await updateArticle(editing.id, form);
      } else {
        await createArticle(form);
      }
      closeForm();
      load();
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Erreur lors de la sauvegarde.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer cet article ?')) return;
    try {
      await deleteArticle(id);
      load();
    } catch (err) {
      alert(err.response?.data?.detail ?? 'Erreur lors de la suppression.');
    }
  };

  if (loading) return <div className="loading">Chargement…</div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Actualités</h1>
        {canEdit && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nouvel article</button>
        )}
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={closeForm}>
          <div className="modal modal-wide" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Modifier l\'article' : 'Nouvel article'}</h2>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label>Titre *</label>
                <input value={form.titre} onChange={(e) => setForm({ ...form, titre: e.target.value })} required />
              </div>
              <div className="form-group">
                <label>Contenu *</label>
                <textarea rows={6} value={form.contenu} onChange={(e) => setForm({ ...form, contenu: e.target.value })} required />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Catégorie</label>
                  <select value={form.categorie} onChange={(e) => setForm({ ...form, categorie: e.target.value })}>
                    {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Auteur</label>
                  <input value={form.auteur} onChange={(e) => setForm({ ...form, auteur: e.target.value })} />
                </div>
              </div>
              <div className="form-group">
                <label>Image (URL)</label>
                <input value={form.image_url} onChange={(e) => setForm({ ...form, image_url: e.target.value })} placeholder="https://…" />
              </div>
              <div className="form-group">
                <label>
                  <input type="checkbox" checked={form.publie} onChange={(e) => setForm({ ...form, publie: e.target.checked })} />
                  {' '}Publié
                </label>
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-outline" onClick={closeForm}>Annuler</button>
                <button type="submit" className="btn btn-primary">Enregistrer</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="articles-list">
        {articles.map((a) => (
          <div key={a.id} className="article-item card">
            {a.image_url && (
              <img src={a.image_url} alt={a.titre} className="article-image" />
            )}
            <div className="article-body">
              <div className="article-meta">
                <span className="article-category">{a.categorie}</span>
                <span className="article-date">{new Date(a.date_publication).toLocaleDateString('fr-FR')}</span>
                {!a.publie && <span className="badge badge-draft">Brouillon</span>}
              </div>
              <h2 className="article-title">{a.titre}</h2>
              <p className="article-content">{a.contenu}</p>
              <p className="article-author">Par {a.auteur}</p>
            </div>
            {canEdit && (
              <div className="card-actions">
                <button className="btn btn-sm btn-outline" onClick={() => openEdit(a)}>Modifier</button>
                <button className="btn btn-sm btn-danger" onClick={() => handleDelete(a.id)}>Supprimer</button>
              </div>
            )}
          </div>
        ))}
      </div>
      {articles.length === 0 && <p className="empty">Aucun article publié.</p>}
    </div>
  );
}
