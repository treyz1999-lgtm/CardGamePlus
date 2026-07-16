import type { FormEvent, ReactNode } from 'react';
import { Logo } from './Logo';
import { Button } from './Button';
import { ErrorMessage } from './States';

interface AuthCardProps {
  title: string;
  username: string;
  password: string;
  submitLabel: string;
  isSubmitting: boolean;
  error: string | null;
  secondaryAction?: ReactNode;
  onUsernameChange: (value: string) => void;
  onPasswordChange: (value: string) => void;
  onSubmit: () => void;
}

export function AuthCard({
  title,
  username,
  password,
  submitLabel,
  isSubmitting,
  error,
  secondaryAction,
  onUsernameChange,
  onPasswordChange,
  onSubmit,
}: AuthCardProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <main className="auth-page">
      <form className="auth-panel" onSubmit={handleSubmit}>
        <Logo />
        <h1>{title}</h1>
        {error ? <ErrorMessage label={error} /> : null}
        <label>
          <span>Username</span>
          <input
            value={username}
            minLength={3}
            maxLength={20}
            autoComplete="username"
            onChange={(event) => onUsernameChange(event.target.value)}
          />
        </label>
        <label>
          <span>Password</span>
          <input
            value={password}
            type="password"
            minLength={8}
            maxLength={128}
            autoComplete={title === 'Login' ? 'current-password' : 'new-password'}
            onChange={(event) => onPasswordChange(event.target.value)}
          />
        </label>
        <div className="auth-actions">
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Working...' : submitLabel}
          </Button>
          {secondaryAction}
        </div>
      </form>
    </main>
  );
}
