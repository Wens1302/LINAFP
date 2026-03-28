import { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { getStats, getSeasons } from '../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Stats() {
  const [stats, setStats] = useState(null);
  const [seasons, setSeasons] = useState([]);
  const [seasonId, setSeasonId] = useState('');
  const [loading, setLoading] = useState(true);

  const load = (id) =>
    getStats(id || undefined)
      .then((r) => setStats(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));

  useEffect(() => {
    getSeasons().then((r) => setSeasons(r.data)).catch(console.error);
    load('');
  }, []);

  const handleSeasonChange = (e) => {
    setSeasonId(e.target.value);
    setLoading(true);
    load(e.target.value);
  };

  if (loading) return <div className="loading">Chargement…</div>;
  if (!stats) return <div className="empty">Statistiques indisponibles.</div>;

  const scorerData = {
    labels: stats.top_scorers.map((p) => p.player_name),
    datasets: [
      {
        label: 'Buts',
        data: stats.top_scorers.map((p) => p.goals),
        backgroundColor: 'rgba(34, 197, 94, 0.7)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 1,
      },
    ],
  };

  const teamGoalsData = {
    labels: stats.teams_goals.map((t) => t.team_name),
    datasets: [
      {
        label: 'Buts marqués',
        data: stats.teams_goals.map((t) => t.goals_for),
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
      {
        label: 'Buts encaissés',
        data: stats.teams_goals.map((t) => t.goals_against),
        backgroundColor: 'rgba(239, 68, 68, 0.5)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: { legend: { position: 'top' } },
    scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Statistiques</h1>
        <select value={seasonId} onChange={handleSeasonChange}>
          <option value="">Toutes les saisons</option>
          {seasons.map((s) => (
            <option key={s.id} value={s.id}>{s.nom}</option>
          ))}
        </select>
      </div>

      <div className="stats-charts-grid">
        {/* Top scorers chart */}
        <section className="card">
          <h2 className="card-title">Meilleurs buteurs</h2>
          {stats.top_scorers.length === 0 ? (
            <p className="empty">Aucun buteur enregistré.</p>
          ) : (
            <Bar data={scorerData} options={{ ...chartOptions, plugins: { ...chartOptions.plugins, title: { display: false } } }} />
          )}
        </section>

        {/* Goals per team chart */}
        <section className="card">
          <h2 className="card-title">Buts par équipe</h2>
          {stats.teams_goals.length === 0 ? (
            <p className="empty">Aucune statistique disponible.</p>
          ) : (
            <Bar data={teamGoalsData} options={chartOptions} />
          )}
        </section>
      </div>

      {/* Top scorers table */}
      {stats.top_scorers.length > 0 && (
        <section className="card" style={{ marginTop: '1.5rem' }}>
          <h2 className="card-title">Classement des buteurs</h2>
          <table className="table">
            <thead>
              <tr>
                <th>#</th>
                <th>Joueur</th>
                <th>Équipe</th>
                <th>Buts</th>
              </tr>
            </thead>
            <tbody>
              {stats.top_scorers.map((p, i) => (
                <tr key={p.player_id}>
                  <td>{i + 1}</td>
                  <td>{p.player_name}</td>
                  <td>{p.team_name}</td>
                  <td><strong>{p.goals}</strong></td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}
