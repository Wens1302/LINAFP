import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getTeams, getMatches, getStandings, getArticles } from '../services/api';

const STATUS_LABELS = {
  scheduled: 'Programmé',
  in_progress: 'En cours',
  finished: 'Terminé',
  postponed: 'Reporté',
  cancelled: 'Annulé',
};

export default function Dashboard() {
  const [teams, setTeams] = useState([]);
  const [matches, setMatches] = useState([]);
  const [standings, setStandings] = useState([]);
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getTeams(),
      getMatches({ status: 'finished' }),
      getStandings(),
      getArticles(),
    ])
      .then(([t, m, s, a]) => {
        setTeams(t.data);
        setMatches(m.data.slice(0, 5));
        setStandings(s.data.slice(0, 5));
        setArticles(a.data.slice(0, 3));
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Chargement…</div>;

  return (
    <div className="page-container">
      <h1 className="page-title">Tableau de bord</h1>

      {/* Summary cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{teams.length}</span>
          <span className="stat-label">Équipes</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{matches.length}</span>
          <span className="stat-label">Derniers matchs</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{standings.length}</span>
          <span className="stat-label">Équipes au classement</span>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* Recent matches */}
        <section className="card">
          <h2 className="card-title">Derniers matchs</h2>
          {matches.length === 0 ? (
            <p className="empty">Aucun match terminé.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Domicile</th>
                  <th>Score</th>
                  <th>Extérieur</th>
                  <th>Statut</th>
                </tr>
              </thead>
              <tbody>
                {matches.map((m) => (
                  <tr key={m.id}>
                    <td>{m.home_team?.nom ?? m.home_team_id}</td>
                    <td className="score">
                      {m.home_score} – {m.away_score}
                    </td>
                    <td>{m.away_team?.nom ?? m.away_team_id}</td>
                    <td>
                      <span className={`badge badge-${m.status}`}>
                        {STATUS_LABELS[m.status] ?? m.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          <Link to="/matches" className="card-link">Voir tous les matchs →</Link>
        </section>

        {/* Mini standings */}
        <section className="card">
          <h2 className="card-title">Classement (top 5)</h2>
          {standings.length === 0 ? (
            <p className="empty">Classement indisponible.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Équipe</th>
                  <th>Pts</th>
                  <th>J</th>
                  <th>+/-</th>
                </tr>
              </thead>
              <tbody>
                {standings.map((s, i) => (
                  <tr key={s.team_id}>
                    <td>{i + 1}</td>
                    <td>{s.team_name}</td>
                    <td><strong>{s.points}</strong></td>
                    <td>{s.played}</td>
                    <td>{s.goal_difference > 0 ? '+' : ''}{s.goal_difference}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          <Link to="/standings" className="card-link">Voir le classement complet →</Link>
        </section>
      </div>

      {/* Articles */}
      {articles.length > 0 && (
        <section className="card" style={{ marginTop: '1.5rem' }}>
          <h2 className="card-title">Dernières actualités</h2>
          <div className="articles-grid">
            {articles.map((a) => (
              <div key={a.id} className="article-card">
                <span className="article-category">{a.categorie}</span>
                <h3 className="article-title">{a.titre}</h3>
                <p className="article-excerpt">
                  {a.contenu.length > 120 ? a.contenu.slice(0, 120) + '…' : a.contenu}
                </p>
                <span className="article-date">
                  {new Date(a.date_publication).toLocaleDateString('fr-FR')}
                </span>
              </div>
            ))}
          </div>
          <Link to="/articles" className="card-link">Voir toutes les actualités →</Link>
        </section>
      )}
    </div>
  );
}
