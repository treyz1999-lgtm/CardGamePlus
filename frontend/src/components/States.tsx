interface StateProps {
  label: string;
}

export function LoadingState({ label }: StateProps) {
  return (
    <div className="state-card">
      <div className="spinner" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
}

export function EmptyState({ label }: StateProps) {
  return (
    <div className="state-card state-empty">
      <p>{label}</p>
    </div>
  );
}

export function ErrorMessage({ label }: StateProps) {
  return (
    <div className="notice notice-error" role="alert">
      {label}
    </div>
  );
}
