import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getArticles, getStandings, getMatches } from '../services/api.js'

const CATEGORIES = [
  { key: '', label: 'Tout' },
  { key: 'news', label: 'Actualités' },
  { key: 'match', label: 'Matchs' },
  { key: 'transfert', label: 'Transferts' },
]

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric',
  })
}

function ArticleCard({ article, featured = false }) {
  const catLabel = CATEGORIES.find((c) => c.key === article.categorie)?.label || article.categorie

  if (featured) {
    return (
      <div style={{
        position: 'relative', borderRadius: '16px', overflow: 'hidden',
        minHeight: '420px', display: 'flex', flexDirection: 'column',
        justifyContent: 'flex-end',
        background: 'var(--f1-dark)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.25)',
      }}>
        {article.image_url && (
          <img
            src={article.image_url}
            alt={article.titre}
            style={{
              position: 'absolute', inset: 0, width: '100%', height: '100%',
              objectFit: 'cover', opacity: 0.45,
            }}
          />
        )}
        <div style={{
          position: 'absolute', inset: 0,
          background: 'linear-gradient(to top, rgba(21,21,30,0.97) 0%, rgba(21,21,30,0.3) 60%, transparent 100%)',
        }} />
        <div style={{ position: 'relative', padding: '2rem', zIndex: 1 }}>
          <span style={{
            display: 'inline-block', background: 'var(--f1-red)', color: '#fff',
            fontSize: '0.7rem', fontWeight: '800', textTransform: 'uppercase',
            letterSpacing: '0.08em', padding: '0.25rem 0.75rem', borderRadius: '99px',
            marginBottom: '0.75rem',
          }}>{catLabel}</span>
          <h2 style={{
            color: '#fff', fontSize: '1.6rem', fontWeight: '900',
            lineHeight: 1.25, marginBottom: '0.75rem',
          }}>{article.titre}</h2>
          <p style={{
            color: 'rgba(255,255,255,0.65)', fontSize: '0.9rem',
            lineHeight: 1.6, marginBottom: '1.25rem',
            display: '-webkit-box', WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical', overflow: 'hidden',
          }}>{article.contenu}</p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.8rem' }}>
              {article.auteur} · {formatDate(article.date_publication)}
            </span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="article-card">
      {article.image_url ? (
        <img className="article-card-img" src={article.image_url} alt={article.titre} />
      ) : (
        <div className="article-card-img" style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '2.5rem', background: 'var(--f1-dark)',
        }}>⚽</div>
      )}
      <div className="article-card-body">
        <span className="article-card-category">{catLabel}</span>
        <h3 className="article-card-title">{article.titre}</h3>
        <p style={{
          fontSize: '0.8125rem', color: 'var(--gray-500)', lineHeight: 1.5,
          display: '-webkit-box', WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical', overflow: 'hidden',
        }}>{article.contenu}</p>
        <div className="article-card-meta">
          <span>{article.auteur}</span>
          <span>·</span>
          <span>{formatDate(article.date_publication)}</span>
        </div>
      </div>
    </div>
  )
}

function StandingsMini({ standings }) {
  if (!standings.length) return null
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ fontSize: '0.82rem' }}>
        <thead>
          <tr>
            <th style={{ width: '30px', textAlign: 'center' }}>#</th>
            <th>Équipe</th>
            <th style={{ textAlign: 'center' }}>PJ</th>
            <th style={{ textAlign: 'center' }}>Pts</th>
          </tr>
        </thead>
        <tbody>
          {standings.slice(0, 5).map((s, i) => (
            <tr key={s.team_id}>
              <td style={{ textAlign: 'center', fontWeight: '700', color: i === 0 ? 'var(--f1-red)' : 'var(--gray-500)' }}>
                {i + 1}
              </td>
              <td style={{ fontWeight: '700', color: 'var(--f1-dark)' }}>{s.team_name}</td>
              <td style={{ textAlign: 'center', color: 'var(--gray-500)' }}>{s.played}</td>
              <td style={{ textAlign: 'center' }}>
                <span style={{
                  display: 'inline-block',
                  background: i === 0 ? 'var(--f1-red)' : 'var(--f1-dark)',
                  color: '#fff', borderRadius: '99px',
                  padding: '0.15rem 0.6rem', fontWeight: '800', fontSize: '0.8rem',
                }}>{s.points}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function RecentMatchesMini({ matches }) {
  if (!matches.length) return null
  const recent = [...matches]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 3)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      {recent.map((m) => {
        const homeWin = m.home_score > m.away_score
        const awayWin = m.away_score > m.home_score
        return (
          <div key={m.id} style={{
            background: 'var(--off-white)', borderRadius: '10px',
            padding: '0.75rem 1rem', border: '1px solid var(--gray-200)',
          }}>
            <div style={{ fontSize: '0.7rem', color: 'var(--gray-500)', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              {formatDate(m.date)}
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontWeight: homeWin ? '800' : '500', fontSize: '0.85rem', color: homeWin ? 'var(--f1-dark)' : 'var(--gray-500)', textAlign: 'right' }}>
                {m.home_team?.nom || `Équipe ${m.home_team_id}`}
              </span>
              <span style={{
                background: 'var(--f1-dark)', color: '#fff',
                padding: '0.25rem 0.75rem', borderRadius: '6px',
                fontWeight: '900', fontSize: '1rem', letterSpacing: '0.1em',
                whiteSpace: 'nowrap',
              }}>
                {m.home_score} – {m.away_score}
              </span>
              <span style={{ fontWeight: awayWin ? '800' : '500', fontSize: '0.85rem', color: awayWin ? 'var(--f1-dark)' : 'var(--gray-500)' }}>
                {m.away_team?.nom || `Équipe ${m.away_team_id}`}
              </span>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default function Home() {
  const [articles, setArticles] = useState([])
  const [standings, setStandings] = useState([])
  const [matches, setMatches] = useState([])
  const [activeCat, setActiveCat] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getArticles(),
      getStandings().catch(() => ({ data: [] })),
      getMatches().catch(() => ({ data: [] })),
    ]).then(([artRes, standRes, matchRes]) => {
      setArticles(artRes.data)
      setStandings(standRes.data)
      setMatches(matchRes.data)
    }).finally(() => setLoading(false))
  }, [])

  const filtered = activeCat
    ? articles.filter((a) => a.categorie === activeCat)
    : articles

  const featured = filtered[0]
  const rest = filtered.slice(1)

  return (
    <div style={{ flex: 1, background: 'var(--off-white)' }}>
      {/* ── Hero Banner ─────────────────────────────────────────────────────── */}
      <div className="home-hero" style={{ padding: '4rem 1.5rem 5rem' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          {/* Championship badge */}
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
            background: 'rgba(232,0,45,0.18)', border: '1px solid rgba(232,0,45,0.4)',
            borderRadius: '99px', padding: '0.35rem 1rem',
            marginBottom: '1.5rem',
          }}>
            <span style={{ color: 'var(--f1-red)', fontSize: '0.75rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              🏆 Championnat National · Saison 2024
            </span>
          </div>

          <h1 style={{
            color: '#fff', fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: '900', lineHeight: 1.1,
            textTransform: 'uppercase', letterSpacing: '0.02em',
            marginBottom: '0.75rem',
          }}>
            GabonFoot<span style={{ color: 'var(--f1-red)' }}>Stats</span>
          </h1>
          <p style={{
            color: 'rgba(255,255,255,0.55)', fontSize: '1.1rem',
            maxWidth: '540px', lineHeight: 1.6,
          }}>
            Toute l'actualité, les résultats et le classement du championnat national de football du Gabon.
          </p>
        </div>
      </div>

      {/* ── Main content ─────────────────────────────────────────────────────── */}
      <div style={{ maxWidth: '1280px', margin: '-2.5rem auto 0', padding: '0 1.5rem 4rem', position: 'relative' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: '2rem', alignItems: 'start' }}
          className="home-grid">

          {/* Left column – Articles */}
          <div>
            {/* Category pills */}
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
              {CATEGORIES.map((c) => (
                <button
                  key={c.key}
                  className={`cat-pill${activeCat === c.key ? ' active' : ''}`}
                  onClick={() => setActiveCat(c.key)}
                >
                  {c.label}
                </button>
              ))}
            </div>

            {loading ? (
              <div className="loading-container">
                <div className="spinner" />
                <p>Chargement des actualités…</p>
              </div>
            ) : filtered.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--gray-500)' }}>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📰</div>
                <p style={{ fontWeight: '700' }}>Aucun article pour cette catégorie.</p>
              </div>
            ) : (
              <>
                {featured && (
                  <div style={{ marginBottom: '1.5rem' }}>
                    <ArticleCard article={featured} featured />
                  </div>
                )}
                {rest.length > 0 && (
                  <>
                    <div className="section-title" style={{ marginBottom: '1rem' }}>
                      Dernières actualités
                    </div>
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
                      gap: '1.25rem',
                    }}>
                      {rest.map((a) => (
                        <ArticleCard key={a.id} article={a} />
                      ))}
                    </div>
                  </>
                )}
              </>
            )}
          </div>

          {/* Right column – Sidebar */}
          <aside style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {/* Classement widget */}
            <div style={{
              background: 'var(--white)', borderRadius: 'var(--radius-lg)',
              boxShadow: 'var(--shadow-sm)', border: '1px solid var(--gray-200)',
              overflow: 'hidden',
            }}>
              <div style={{
                background: 'var(--f1-dark)', padding: '1rem 1.25rem',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              }}>
                <span style={{
                  color: '#fff', fontWeight: '800', fontSize: '0.85rem',
                  textTransform: 'uppercase', letterSpacing: '0.06em',
                }}>🏆 Classement</span>
                <Link to="/standings" style={{
                  color: 'var(--f1-red)', fontSize: '0.75rem', fontWeight: '700',
                  textTransform: 'uppercase', letterSpacing: '0.04em',
                }}>Voir tout →</Link>
              </div>
              <div style={{ padding: '1rem' }}>
                {standings.length > 0
                  ? <StandingsMini standings={standings} />
                  : <p style={{ color: 'var(--gray-500)', fontSize: '0.875rem', textAlign: 'center', padding: '1rem 0' }}>Aucune donnée</p>
                }
              </div>
            </div>

            {/* Derniers résultats widget */}
            <div style={{
              background: 'var(--white)', borderRadius: 'var(--radius-lg)',
              boxShadow: 'var(--shadow-sm)', border: '1px solid var(--gray-200)',
              overflow: 'hidden',
            }}>
              <div style={{
                background: 'var(--f1-dark)', padding: '1rem 1.25rem',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              }}>
                <span style={{
                  color: '#fff', fontWeight: '800', fontSize: '0.85rem',
                  textTransform: 'uppercase', letterSpacing: '0.06em',
                }}>⚽ Derniers résultats</span>
                <Link to="/matches" style={{
                  color: 'var(--f1-red)', fontSize: '0.75rem', fontWeight: '700',
                  textTransform: 'uppercase', letterSpacing: '0.04em',
                }}>Voir tout →</Link>
              </div>
              <div style={{ padding: '1rem' }}>
                {matches.length > 0
                  ? <RecentMatchesMini matches={matches} />
                  : <p style={{ color: 'var(--gray-500)', fontSize: '0.875rem', textAlign: 'center', padding: '1rem 0' }}>Aucun résultat</p>
                }
              </div>
            </div>
          </aside>
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .home-grid {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </div>
  )
}
