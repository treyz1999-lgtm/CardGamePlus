import { useCallback, useEffect, useMemo, useState } from 'react';
import { Button } from '../components/Button';
import { Panel } from '../components/Panel';
import { PlayingCard } from '../components/PlayingCard';
import { EmptyState, ErrorMessage, LoadingState } from '../components/States';
import * as cardService from '../services/cardService';
import * as deckService from '../services/deckService';
import type { Card, Deck, DeckDetails } from '../types/api';
import { getErrorMessage } from '../utils/errors';

export function DeckBuilderPage() {
  const [decks, setDecks] = useState<Deck[]>([]);
  const [collection, setCollection] = useState<Card[]>([]);
  const [selectedDeck, setSelectedDeck] = useState<DeckDetails | null>(null);
  const [newDeckName, setNewDeckName] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const deckCardIds = useMemo(
    () => new Set(selectedDeck?.cards.map((card) => card.card_id) ?? []),
    [selectedDeck],
  );

  const loadData = useCallback(async (deckId?: number) => {
    setIsLoading(true);
    setError(null);

    try {
      const [deckList, cards] = await Promise.all([
        deckService.getDecks(),
        cardService.getCards(),
      ]);
      setDecks(deckList);
      setCollection(cards);

      const nextDeckId = deckId ?? selectedDeck?.deck_id ?? deckList[0]?.deck_id;
      if (nextDeckId) {
        setSelectedDeck(await deckService.getDeck(nextDeckId));
      } else {
        setSelectedDeck(null);
      }
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setIsLoading(false);
    }
  }, [selectedDeck?.deck_id]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  async function handleCreateDeck() {
    setError(null);

    try {
      const response = await deckService.createDeck({
        name: newDeckName.trim(),
        card_ids: [],
      });
      setNewDeckName('');
      await loadData(response.deck_id);
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  async function handleDeleteDeck(deckId: number) {
    setError(null);

    try {
      await deckService.deleteDeck(deckId);
      await loadData();
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  async function handleSelectDeck(deckId: number) {
    setError(null);

    try {
      setSelectedDeck(await deckService.getDeck(deckId));
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  async function handleAddCard(cardId: number) {
    if (!selectedDeck) {
      return;
    }

    setError(null);

    try {
      await deckService.addCardToDeck(selectedDeck.deck_id, { card_id: cardId });
      setSelectedDeck(await deckService.getDeck(selectedDeck.deck_id));
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  async function handleRemoveCard(cardId: number) {
    if (!selectedDeck) {
      return;
    }

    setError(null);

    try {
      await deckService.removeCardFromDeck(selectedDeck.deck_id, cardId);
      setSelectedDeck(await deckService.getDeck(selectedDeck.deck_id));
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  if (isLoading) {
    return <LoadingState label="Loading decks..." />;
  }

  return (
    <div className="deck-builder">
      <Panel title="Existing Decks">
        {error ? <ErrorMessage label={error} /> : null}
        <div className="form-row">
          <label>
            <span>Create Deck</span>
            <input
              value={newDeckName}
              placeholder="Moonlit Aces"
              onChange={(event) => setNewDeckName(event.target.value)}
            />
          </label>
          <Button disabled={!newDeckName.trim()} onClick={handleCreateDeck}>
            Create Deck
          </Button>
        </div>
        <div className="deck-list">
          {decks.length > 0 ? (
            decks.map((deck) => (
              <div
                className={`deck-row ${selectedDeck?.deck_id === deck.deck_id ? 'is-active' : ''}`}
                key={deck.deck_id}
              >
                <button type="button" onClick={() => handleSelectDeck(deck.deck_id)}>
                  {deck.name}
                </button>
                <Button variant="danger" onClick={() => handleDeleteDeck(deck.deck_id)}>
                  Delete
                </Button>
              </div>
            ))
          ) : (
            <EmptyState label="No decks created yet." />
          )}
        </div>
      </Panel>

      <Panel title={selectedDeck ? selectedDeck.name : 'Selected Deck'}>
        {selectedDeck ? (
          <div className="split-zones">
            <section>
              <h3>Cards in Deck</h3>
              {selectedDeck.cards.length > 0 ? (
                <div className="card-grid compact">
                  {selectedDeck.cards.map((card) => (
                    <div className="card-action-wrap" key={card.card_id}>
                      <PlayingCard card={card} />
                      <Button variant="secondary" onClick={() => handleRemoveCard(card.card_id)}>
                        Remove Card
                      </Button>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState label="This deck is empty." />
              )}
            </section>
            <section>
              <h3>Collection</h3>
              {collection.length > 0 ? (
                <div className="card-grid compact">
                  {collection.map((card) => (
                    <div className="card-action-wrap" key={card.card_id}>
                      <PlayingCard card={card} disabled={deckCardIds.has(card.card_id)} />
                      <Button
                        disabled={deckCardIds.has(card.card_id)}
                        onClick={() => handleAddCard(card.card_id)}
                      >
                        Add Card
                      </Button>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState label="Create cards in the Collection first." />
              )}
            </section>
          </div>
        ) : (
          <EmptyState label="Select or create a deck." />
        )}
      </Panel>
    </div>
  );
}
