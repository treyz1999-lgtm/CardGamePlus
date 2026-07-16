interface LogoProps {
  compact?: boolean;
}

export function Logo({ compact = false }: LogoProps) {
  return (
    <div className={compact ? 'logo logo-compact' : 'logo'}>
      <img src="/assets/logo.png" alt="CardGamePlus" />
      {!compact ? <span>CardGamePlus</span> : null}
    </div>
  );
}
