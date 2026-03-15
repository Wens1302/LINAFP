import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'

const NAV_LINKS = [
  { to: '/dashboard',  label: 'Dashboard',      icon: '📊' },
  { to: '/teams',      label: 'Équipes',         icon: '🛡️' },
  { to: '/players',    label: 'Joueurs',         icon: '👟' },
  { to: '/matches',    label: 'Matchs',          icon: '⚽' },
  { to: '/standings',  label: 'Classement',      icon: '🏆' },
  { to: '/stats',      label: 'Statistiques',    icon: '📈' },
]

const styles = {
  nav: {
    background: 'linear-gradient(135deg, #009A44 0%, #007a35 100%)',
    boxShadow: '0 2px 8px rgba(0,0,0,0.18)',
    position: 'sticky',
    top: 0,
    zIndex: 500,
  },
  inner: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1.5rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: '64px',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    textDecoration: 'none',
  },
  logoFlag: {
    display: 'flex',
    flexDirection: 'column',
    width: '22px',
    height: '16px',
    borderRadius: '2px',
    overflow: 'hidden',
    flexShrink: 0,
    boxShadow: '0 1px 3px rgba(0,0,0,0.3)',
  },
  flagGreen: { flex: 1, backgroundColor: '#009A44' },
  flagYellow: { flex: 1, backgroundColor: '#FCD116' },
  flagBlue: { flex: 1, backgroundColor: '#003189' },
  logoText: {
    fontSize: '1.25rem',
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: '0.02em',
    whiteSpace: 'nowrap',
  },
  logoSub: {
    fontSize: '0.65rem',
    color: '#FCD116',
    fontWeight: '600',
    letterSpacing: '0.1em',
    textTransform: 'uppercase',
  },
  links: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem',
    listStyle: 'none',
  },
  hamburger: {
    background: 'none',
    border: 'none',
    color: '#ffffff',
    fontSize: '1.5rem',
    padding: '0.25rem',
    display: 'none',
    cursor: 'pointer',
  },
}

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false)

  const linkStyle = ({ isActive }) => ({
    display: 'flex',
    alignItems: 'center',
    gap: '0.35rem',
    padding: '0.45rem 0.75rem',
    borderRadius: '6px',
    fontSize: '0.875rem',
    fontWeight: '600',
    color: isActive ? '#FCD116' : 'rgba(255,255,255,0.88)',
    backgroundColor: isActive ? 'rgba(255,255,255,0.12)' : 'transparent',
    textDecoration: 'none',
    transition: 'background-color 0.2s, color 0.2s',
    borderBottom: isActive ? '2px solid #FCD116' : '2px solid transparent',
  })

  return (
    <nav style={styles.nav}>
      <div style={styles.inner}>
        {/* Logo */}
        <NavLink to="/dashboard" style={styles.logo}>
          <div style={styles.logoFlag}>
            <div style={styles.flagGreen} />
            <div style={styles.flagYellow} />
            <div style={styles.flagBlue} />
          </div>
          <div>
            <div style={styles.logoText}>GabonFootStats</div>
            <div style={styles.logoSub}>Ligue nationale</div>
          </div>
        </NavLink>

        {/* Desktop links */}
        <ul style={styles.links} className="nav-links-desktop">
          {NAV_LINKS.map(({ to, label, icon }) => (
            <li key={to}>
              <NavLink to={to} style={linkStyle}
                onMouseEnter={(e) => {
                  if (!e.currentTarget.style.backgroundColor.includes('0.12')) {
                    e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.08)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (!e.currentTarget.style.backgroundColor.includes('0.12')) {
                    e.currentTarget.style.backgroundColor = 'transparent'
                  }
                }}
              >
                <span style={{ fontSize: '0.95rem' }}>{icon}</span>
                {label}
              </NavLink>
            </li>
          ))}
        </ul>

        {/* Mobile hamburger */}
        <button
          style={{ ...styles.hamburger, display: 'block' }}
          className="hamburger-btn"
          onClick={() => setMenuOpen((o) => !o)}
          aria-label="Menu"
        >
          {menuOpen ? '✕' : '☰'}
        </button>
      </div>

      {/* Mobile dropdown */}
      {menuOpen && (
        <div style={{
          background: '#007a35',
          padding: '0.75rem 1.5rem 1rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.25rem',
          borderTop: '1px solid rgba(255,255,255,0.15)',
        }}
          className="mobile-menu"
        >
          {NAV_LINKS.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              style={linkStyle}
              onClick={() => setMenuOpen(false)}
            >
              <span>{icon}</span> {label}
            </NavLink>
          ))}
        </div>
      )}

      <style>{`
        @media (min-width: 769px) {
          .hamburger-btn { display: none !important; }
          .mobile-menu { display: none !important; }
        }
        @media (max-width: 768px) {
          .nav-links-desktop { display: none !important; }
        }
      `}</style>
    </nav>
  )
}
