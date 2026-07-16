import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Logo } from './Logo';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/collection', label: 'Collection' },
  { to: '/decks', label: 'Deck Builder' },
  { to: '/shop', label: 'Shop' },
  { to: '/battle', label: 'Battle' },
];

export function AppLayout() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <Logo compact />
        <nav className="main-nav" aria-label="Main navigation">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.to === '/'}>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="topbar-profile">
          {user ? (
            <span>
              {user.username} · {user.gold} gold
            </span>
          ) : null}
          <button className="button button-ghost" type="button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>
      <main className="page-frame">
        <Outlet />
      </main>
    </div>
  );
}
