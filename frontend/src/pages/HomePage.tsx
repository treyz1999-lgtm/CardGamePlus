import { Link } from 'react-router-dom';
import { Panel } from '../components/Panel';
import { useAuth } from '../contexts/AuthContext';

const actions = [
  { to: '/collection', label: 'Collection' },
  { to: '/decks', label: 'Deck Builder' },
  { to: '/shop', label: 'Shop' },
  { to: '/battle', label: 'Battle' },
];

export function HomePage() {
  const { user } = useAuth();

  return (
    <div className="home-grid">
      <Panel className="hero-panel">
        <div>
          <p className="eyebrow">Welcome back</p>
          <h1>{user?.username}</h1>
          <p className="gold-balance">{user?.gold ?? 0} gold</p>
        </div>
      </Panel>
      <div className="action-grid">
        {actions.map((action) => (
          <Link className="home-action" to={action.to} key={action.to}>
            {action.label}
          </Link>
        ))}
      </div>
    </div>
  );
}
