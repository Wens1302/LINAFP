import { useEffect, useState } from 'react';
import { getStandings, getSeasons } from '../services/api';

export default function Standings() {
  const [standings, setStandings] = useState([]);
  const [seasons, setSeasons] = useState([]);
  const [seasonId, setSeasonId] = useState('');
  const [loading, setLoading] = useState(true);

  const load = (id) =>
    getStandings(id || undefined)
      .then((r) => setStandings(r.data))
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

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Classement</h1>
        <select value={seasonId} onChange={handleSeasonChange}>
          <option value="">Toutes les saisons</option>
          {seasons.map((s) => (
            <option key={s.id} value={s.id}>{s.nom}</option>
          ))}
        </select>
      </div>

      {standings.length === 0 ? (
        <p className="empty">Aucune donnée de classement disponible.</p>
      ) : (
        <table className="table standings-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Équipe</th>
              <th title="Points">Pts</th>
              <th title="Matchs joués">J</th>
              <th title="Victoires">V</th>
              <th title="Matchs nuls">N</th>
              <th title="Défaites">D</th>
              <th title="Buts marqués">BP</th>
              <th title="Buts encaissés">BC</th>
              <th title="Différence de buts">+/-</th>
            </tr>
          </thead>
          <tbody>
            {standings.map((s, i) => (
              <tr key={s.team_id} className={i === 0 ? 'leader' : ''}>
                <td>{i + 1}</td>
                <td><strong>{s.team_name}</strong></td>
                <td><strong>{s.points}</strong></td>
                <td>{s.played}</td>
                <td>{s.won}</td>
                <td>{s.drawn}</td>
                <td>{s.lost}</td>
                <td>{s.goals_for}</td>
                <td>{s.goals_against}</td>
                <td className={s.goal_difference > 0 ? 'positive' : s.goal_difference < 0 ? 'negative' : ''}>
                  {s.goal_difference > 0 ? '+' : ''}{s.goal_difference}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
