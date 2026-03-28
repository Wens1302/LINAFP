import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await login(form.username, form.password);
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('role', res.data.role);
      navigate('/');
    } catch {
      setError('Identifiants invalides. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container" style={{ maxWidth: 420, margin: '80px auto' }}>
      <div className="card">
        <h2 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>⚽ Connexion</h2>
        {error && <div className="alert alert-error">{error}</div>}
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label>Nom d&apos;utilisateur</label>
            <input
              type="text"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              required
              placeholder="admin"
            />
          </div>
          <div className="form-group">
            <label>Mot de passe</label>
            <input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
              placeholder="••••••••"
            />
          </div>
          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Connexion…' : 'Se connecter'}
          </button>
        </form>
        <p style={{ marginTop: '1rem', textAlign: 'center', color: '#64748b', fontSize: '0.85rem' }}>
          Comptes de démo : admin / admin1234 · editor / editor1234 · reader / reader1234
        </p>
      </div>
    </div>
  );
}
