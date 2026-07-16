import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthCard } from '../components/AuthCard';
import { useAuth } from '../contexts/AuthContext';
import { getErrorMessage } from '../utils/errors';

export function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  async function handleRegister() {
    setIsSubmitting(true);
    setError(null);

    try {
      await register(username, password);
      navigate('/login');
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard
      title="Create Account"
      username={username}
      password={password}
      submitLabel="Create Account"
      isSubmitting={isSubmitting}
      error={error}
      onUsernameChange={setUsername}
      onPasswordChange={setPassword}
      onSubmit={handleRegister}
      secondaryAction={
        <Link className="button button-ghost" to="/login">
          Back to Login
        </Link>
      }
    />
  );
}
