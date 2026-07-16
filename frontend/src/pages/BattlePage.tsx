import { useCallback, useEffect, useState } from 'react';
import { Button } from '../components/Button';
import { CardBack } from '../components/CardBack';
import { Panel } from '../components/Panel';
import { PlayingCard } from '../components/PlayingCard';
import { EmptyState, ErrorMessage } from '../components/States';
import { useAuth } from '../contexts/AuthContext';
import * as deckService from '../services/deckService';
import * as gameService from '../services/gameService';
import type { Card, Deck, GameState } from '../types/api';
import { getErrorMessage } from '../utils/errors';

function Zone({ title, cards }: { title: string; cards: Card[] }) {
  return (
    <section className="battle-zone">
      <h4>{title}</h4>
      {cards.length > 0 ? (
        <div className="card-grid compact">
          {cards.map((card) => (
            <PlayingCard card={card} key={card.card_id} />
          ))}
        </div>
      ) : (
        <EmptyState label="Empty" />
      )}
    </section>
  );
}

export function BattlePage() {
  const [decks, setDecks] = useState<Deck[]>([]);
  const [selectedDeckId, setSelectedDeckId] = useState('');
  const [selectedHandIndex, setSelectedHandIndex] = useState<number | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { refreshUser } = useAuth();

  const loadDecks = useCallback(async () => {
    try {
      const deckList = await deckService.getDecks();
      setDecks(deckList);
      setSelectedDeckId((current) => current || String(deckList[0]?.deck_id ?? ''));
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }, []);

  useEffect(() => {
    loadDecks();
  }, [loadDecks]);

  async function handleStartGame() {
    if (!selectedDeckId) {
      return;
    }

    setError(null);

    try {
      await gameService.startGame({ deck_id: Number(selectedDeckId) });
      setGameState(await gameService.getGameState());
      setSelectedHandIndex(null);
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  async function handleRefresh() {
    setError(null);

    try {
      setGameState(await gameService.getGameState());
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  async function handlePlayCard() {
    if (selectedHandIndex === null) {
      return;
    }

    setError(null);

    try {
      const nextGameState = await gameService.playCard({ hand_index: selectedHandIndex });
      setGameState(nextGameState);
      setSelectedHandIndex(null);

      if (nextGameState.game_over && nextGameState.winner === 'USER') {
        await refreshUser();
      }
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  const result =
    gameState?.game_over && gameState.winner
      ? gameState.winner === 'USER'
        ? 'Victory'
        : 'Defeat'
      : null;

  return (
    <div className="stack">
      <Panel title="Battle Controls">
        {error ? <ErrorMessage label={error} /> : null}
        <div className="form-row battle-controls">
          <label>
            <span>Deck</span>
            <select
              value={selectedDeckId}
              onChange={(event) => setSelectedDeckId(event.target.value)}
            >
              {decks.map((deck) => (
                <option value={deck.deck_id} key={deck.deck_id}>
                  {deck.name}
                </option>
              ))}
            </select>
          </label>
          <Button disabled={!selectedDeckId} onClick={handleStartGame}>
            Start Game
          </Button>
          <Button
            disabled={!gameState || selectedHandIndex === null || gameState.game_over}
            onClick={handlePlayCard}
          >
            Play Card
          </Button>
          <Button variant="secondary" onClick={handleRefresh}>
            Refresh Game State
          </Button>
        </div>
        {result ? <div className="result-banner">{result}</div> : null}
      </Panel>

      {gameState ? (
        <div className="battle-board">
          <Panel title="AI">
            <div className="stat-strip">
              <span>HP {gameState.ai.hp}</span>
              <span>Deck {gameState.ai.deck_size}</span>
              <span>Hand {gameState.ai.hand_size}</span>
              <span>Turn {gameState.turn_number}</span>
            </div>
            <section className="battle-zone">
              <h4>Hand</h4>
              <div className="card-back-row">
                {Array.from({ length: gameState.ai.hand_size }, (_, index) => (
                  <CardBack key={index} />
                ))}
              </div>
            </section>
            <Zone title="Field" cards={gameState.ai.field} />
            <Zone title="Graveyard" cards={gameState.ai.graveyard} />
          </Panel>

          <Panel title="Player">
            <div className="stat-strip">
              <span>HP {gameState.user.hp}</span>
              <span>Deck {gameState.user.deck_size}</span>
              <span>Hand {gameState.user.hand.length}</span>
              <span>Graveyard {gameState.user.graveyard.length}</span>
            </div>
            <section className="battle-zone">
              <h4>Hand</h4>
              {gameState.user.hand.length > 0 ? (
                <div className="card-grid compact">
                  {gameState.user.hand.map((card, index) => (
                    <PlayingCard
                      card={card}
                      key={`${card.card_id}-${index}`}
                      selected={selectedHandIndex === index}
                      disabled={gameState.game_over}
                      onClick={() => setSelectedHandIndex(index)}
                    />
                  ))}
                </div>
              ) : (
                <EmptyState label="No cards in hand." />
              )}
            </section>
            <Zone title="Field" cards={gameState.user.field} />
            <Zone title="Graveyard" cards={gameState.user.graveyard} />
          </Panel>
        </div>
      ) : (
        <Panel>
          <EmptyState label="Start a game to see the battlefield." />
        </Panel>
      )}
    </div>
  );
}
