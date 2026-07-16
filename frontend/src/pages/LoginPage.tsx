import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { AuthCard } from '../components/AuthCard';
import { useAuth } from '../contexts/AuthContext';
import { getErrorMessage } from '../utils/errors';

export function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const redirectPath =
    typeof location.state === 'object' &&
    location.state !== null &&
    'from' in location.state &&
    typeof location.state.from === 'object' &&
    location.state.from !== null &&
    'pathname' in location.state.from &&
    typeof location.state.from.pathname === 'string'
      ? location.state.from.pathname
      : '/';

  async function handleLogin() {
    setIsSubmitting(true);
    setError(null);

    try {
      await login(username, password);
      navigate(redirectPath, { replace: true });
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard
      title="Login"
      username={username}
      password={password}
      submitLabel="Login"
      isSubmitting={isSubmitting}
      error={error}
      onUsernameChange={setUsername}
      onPasswordChange={setPassword}
      onSubmit={handleLogin}
      secondaryAction={
        <Link className="button button-secondary" to="/register">
          Register
        </Link>
      }
    />
  );
}
