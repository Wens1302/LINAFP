import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const NAV_LINKS = [
  { to: '/', label: 'Tableau de bord' },
  { to: '/teams', label: 'Équipes' },
  { to: '/players', label: 'Joueurs' },
  { to: '/matches', label: 'Matchs' },
  { to: '/standings', label: 'Classement' },
  { to: '/stats', label: 'Statistiques' },
  { to: '/articles', label: 'Actualités' },
];

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  const isActive = (path) =>
    path === '/' ? location.pathname === '/' : location.pathname.startsWith(path);

  const closeMenu = () => setMenuOpen(false);

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/" onClick={closeMenu}>⚽ GabonFootStats</Link>
      </div>

      {/* Desktop links */}
      <div className="navbar-links">
        {NAV_LINKS.map(({ to, label }) => (
          <Link key={to} to={to} className={isActive(to) ? 'active' : ''}>
            {label}
          </Link>
        ))}
      </div>

      <div className="navbar-auth">
        {token ? (
          <>
            <span className="role-badge">{role}</span>
            <button onClick={handleLogout} className="btn btn-outline btn-nav">Déconnexion</button>
          </>
        ) : (
          <Link to="/login" className="btn btn-primary btn-nav">Connexion</Link>
        )}
      </div>

      {/* Hamburger button (mobile only) */}
      <button
        className="navbar-hamburger"
        aria-label="Menu"
        aria-expanded={menuOpen}
        onClick={() => setMenuOpen((o) => !o)}
      >
        <span /><span /><span />
      </button>

      {/* Mobile drawer */}
      {menuOpen && (
        <div className="navbar-mobile-menu">
          {NAV_LINKS.map(({ to, label }) => (
            <Link key={to} to={to} className={isActive(to) ? 'active' : ''} onClick={closeMenu}>
              {label}
            </Link>
          ))}
          <hr />
          {token ? (
            <button onClick={() => { handleLogout(); closeMenu(); }} className="btn btn-outline">
              Déconnexion
            </button>
          ) : (
            <Link to="/login" className="btn btn-primary" onClick={closeMenu}>Connexion</Link>
          )}
        </div>
      )}
    </nav>
  );
}
