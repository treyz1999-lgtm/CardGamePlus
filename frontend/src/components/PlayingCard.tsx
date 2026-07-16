import type { Card } from '../types/api';
import { formatRank, formatSuit, isRedSuit } from '../utils/cards';

interface PlayingCardProps {
  card: Card;
  selected?: boolean;
  disabled?: boolean;
  onClick?: () => void;
}

export function PlayingCard({ card, selected = false, disabled = false, onClick }: PlayingCardProps) {
  const rank = formatRank(card.rank);
  const suit = formatSuit(card.suit);
  const colorClass = isRedSuit(card.suit) ? 'card-red' : 'card-black';
  const isInteractive = Boolean(onClick) && !disabled;

  return (
    <button
      className={[
        'playing-card',
        colorClass,
        selected ? 'is-selected' : '',
        disabled ? 'is-disabled' : '',
      ]
        .filter(Boolean)
        .join(' ')}
      type="button"
      disabled={disabled}
      onClick={onClick}
      aria-pressed={selected}
    >
      <span className="card-corner card-corner-top">
        <strong>{rank}</strong>
        <span>{suit}</span>
      </span>
      <span className="card-center-suit">{suit}</span>
      <span className="card-health">HP: {card.health}</span>
      <span className="card-effects">
        <strong>Effects</strong>
        {card.effects.length > 0 ? (
          <ul>
            {card.effects.map((effect) => (
              <li key={effect}>{effect}</li>
            ))}
          </ul>
        ) : (
          <span className="muted">None</span>
        )}
      </span>
      <span className="card-corner card-corner-bottom" aria-hidden="true">
        <strong>{rank}</strong>
        <span>{suit}</span>
      </span>
      {isInteractive ? <span className="sr-only">Select card</span> : null}
    </button>
  );
}
