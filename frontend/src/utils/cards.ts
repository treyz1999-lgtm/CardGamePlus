const suitSymbols: Record<string, string> = {
  HEARTS: '♥',
  DIAMONDS: '♦',
  CLUBS: '♣',
  SPADES: '♠',
};

const rankLabels: Record<number, string> = {
  11: 'J',
  12: 'Q',
  13: 'K',
  14: 'A',
};

export function formatRank(rank: number) {
  return rankLabels[rank] ?? String(rank);
}

export function formatSuit(suit: string) {
  return suitSymbols[suit.toUpperCase()] ?? suit;
}

export function isRedSuit(suit: string) {
  const normalized = suit.toUpperCase();
  return normalized === 'HEARTS' || normalized === 'DIAMONDS';
}

export function humanizeKey(key: string) {
  return key
    .split('_')
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}
