import React, { useEffect, useState } from 'react'
import { getStandings } from '../services/api.js'

const ROW_COLORS = [
  { bg: '#fffbeb', border: '#FCD116', badge: { bg: '#FCD116', color: '#78350f' }, label: '🥇' },
  { bg: '#f9fafb', border: '#9ca3af', badge: { bg: '#e5e7eb', color: '#374151' }, label: '🥈' },
  { bg: '#fff7ed', border: '#fb923c', badge: { bg: '#ffedd5', color: '#9a3412' }, label: '🥉' },
]

export default function Standings() {
  const [standings, setStandings] = useState([])
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)

  useEffect(() => {
    getStandings()
      .then((res) => setStandings(res.data))
      .catch(() => setError('Impossible de charger le classement.'))
      .finally(() => setLoading(false))
  }, [])

  const val = (s, ...keys) => {
    for (const k of keys) if (s[k] != null) return s[k]
    return 0
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title"><span>🏆</span> Classement</h1>
        {!loading && !error && (
          <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            {standings.length} équipe{standings.length !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
        {[
          { color: '#FCD116', bg: '#fffbeb', label: '1re place' },
          { color: '#9ca3af', bg: '#f9fafb', label: '2e place' },
          { color: '#fb923c', bg: '#fff7ed', label: '3e place' },
        ].map(({ color, bg, label }) => (
          <div key={label} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#6b7280' }}>
            <div style={{ width: '14px', height: '14px', borderRadius: '3px', background: bg, border: `2px solid ${color}` }} />
            {label}
          </div>
        ))}
      </div>

      {error && <div className="error-box">{error}</div>}

      {loading ? (
        <div className="loading-container">
          <div className="spinner" />
          <p>Chargement du classement…</p>
        </div>
      ) : standings.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📋</div>
          <p style={{ fontWeight: '600' }}>Classement indisponible.</p>
          <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>Ajoutez des équipes et des matchs pour générer le classement.</p>
        </div>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th style={{ textAlign: 'center', width: '56px' }}>Pos</th>
                <th>Équipe</th>
                <th style={{ textAlign: 'center' }}>PJ</th>
                <th style={{ textAlign: 'center' }}>V</th>
                <th style={{ textAlign: 'center' }}>N</th>
                <th style={{ textAlign: 'center' }}>D</th>
                <th style={{ textAlign: 'center' }}>BP</th>
                <th style={{ textAlign: 'center' }}>BC</th>
                <th style={{ textAlign: 'center' }}>Diff</th>
                <th style={{ textAlign: 'center', background: '#007a35' }}>Pts</th>
              </tr>
            </thead>
            <tbody>
              {standings.map((s, idx) => {
                const medal = ROW_COLORS[idx]
                const pj   = val(s, 'played', 'pj', 'games_played')
                const wins  = val(s, 'won', 'wins', 'v', 'victories')
                const draws = val(s, 'drawn', 'draws', 'n', 'nuls')
                const loss  = val(s, 'lost', 'losses', 'd', 'defaites')
                const bp    = val(s, 'goals_for', 'bp', 'buts_pour')
                const bc    = val(s, 'goals_against', 'bc', 'buts_contre')
                const diff  = bp - bc
                const pts   = val(s, 'points', 'pts')
                const name  = s.team_name || s.team?.nom || `Équipe ${s.team}`

                return (
                  <tr
                    key={s.id ?? s.team ?? idx}
                    style={medal ? { backgroundColor: medal.bg, borderLeft: `4px solid ${medal.border}` } : {}}
                  >
                    <td style={{ textAlign: 'center', fontWeight: '800', fontSize: '1rem' }}>
                      {medal ? (
                        <span title={`${idx + 1}e`}>{medal.label}</span>
                      ) : (
                        <span style={{ color: '#6b7280' }}>{idx + 1}</span>
                      )}
                    </td>
                    <td>
                      <span style={{
                        fontWeight: '700',
                        color: '#111827',
                        fontSize: idx < 3 ? '0.95rem' : '0.875rem',
                      }}>
                        {name}
                      </span>
                    </td>
                    <td style={{ textAlign: 'center', color: '#6b7280' }}>{pj}</td>
                    <td style={{ textAlign: 'center', color: '#009A44', fontWeight: '600' }}>{wins}</td>
                    <td style={{ textAlign: 'center', color: '#854d0e', fontWeight: '600' }}>{draws}</td>
                    <td style={{ textAlign: 'center', color: '#dc2626', fontWeight: '600' }}>{loss}</td>
                    <td style={{ textAlign: 'center' }}>{bp}</td>
                    <td style={{ textAlign: 'center' }}>{bc}</td>
                    <td style={{
                      textAlign: 'center',
                      fontWeight: '700',
                      color: diff > 0 ? '#009A44' : diff < 0 ? '#dc2626' : '#6b7280',
                    }}>
                      {diff > 0 ? `+${diff}` : diff}
                    </td>
                    <td style={{ textAlign: 'center' }}>
                      <span style={{
                        display: 'inline-block',
                        background: medal ? medal.badge.bg : '#009A44',
                        color: medal ? medal.badge.color : '#ffffff',
                        borderRadius: '99px',
                        padding: '0.2rem 0.7rem',
                        fontWeight: '800',
                        fontSize: '0.9rem',
                        minWidth: '36px',
                        textAlign: 'center',
                      }}>
                        {pts}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Footer note */}
      {!loading && standings.length > 0 && (
        <p style={{ marginTop: '1rem', fontSize: '0.75rem', color: '#9ca3af' }}>
          PJ = Matchs joués · V = Victoires · N = Nuls · D = Défaites · BP = Buts pour · BC = Buts contre · Diff = Différence · Pts = Points
        </p>
      )}
    </div>
  )
}
