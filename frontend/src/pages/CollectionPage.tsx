import { useCallback, useEffect, useMemo, useState } from 'react';
import { Button } from '../components/Button';
import { EmptyState, ErrorMessage, LoadingState } from '../components/States';
import { Panel } from '../components/Panel';
import { PlayingCard } from '../components/PlayingCard';
import * as cardService from '../services/cardService';
import * as shopService from '../services/shopService';
import type { Card, ShopItem } from '../types/api';
import { getErrorMessage } from '../utils/errors';
import { humanizeKey } from '../utils/cards';

export function CollectionPage() {
  const [cards, setCards] = useState<Card[]>([]);
  const [shopItems, setShopItems] = useState<ShopItem[]>([]);
  const [cardKey, setCardKey] = useState('');
  const [selectedEffects, setSelectedEffects] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ownedEffects = useMemo(
    () => shopItems.filter((item) => item.owned).map((item) => item.effect_key),
    [shopItems],
  );

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [cardData, inventory] = await Promise.all([
        cardService.getCards(),
        shopService.getShopInventory(),
      ]);
      setCards(cardData);
      setShopItems(inventory);
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  function toggleEffect(effectKey: string) {
    setSelectedEffects((current) =>
      current.includes(effectKey)
        ? current.filter((key) => key !== effectKey)
        : [...current, effectKey],
    );
  }

  async function handleCreateCard() {
    setIsSaving(true);
    setError(null);

    try {
      await cardService.createCard({
        card_key: cardKey.trim().toUpperCase(),
        effect_keys: selectedEffects,
      });
      setCardKey('');
      setSelectedEffects([]);
      await loadData();
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setIsSaving(false);
    }
  }

  if (isLoading) {
    return <LoadingState label="Loading collection..." />;
  }

  return (
    <div className="stack">
      <Panel title="Create Custom Card">
        {error ? <ErrorMessage label={error} /> : null}
        <div className="form-row">
          <label>
            <span>Card Key</span>
            <input
              value={cardKey}
              maxLength={2}
              placeholder="KH"
              onChange={(event) => setCardKey(event.target.value)}
            />
          </label>
          <Button disabled={isSaving || cardKey.trim().length !== 2} onClick={handleCreateCard}>
            {isSaving ? 'Creating...' : 'Create Card'}
          </Button>
        </div>
        <div className="effect-picker">
          {ownedEffects.length > 0 ? (
            ownedEffects.map((effectKey) => (
              <label className="check-pill" key={effectKey}>
                <input
                  type="checkbox"
                  checked={selectedEffects.includes(effectKey)}
                  onChange={() => toggleEffect(effectKey)}
                />
                <span>{humanizeKey(effectKey)}</span>
              </label>
            ))
          ) : (
            <p className="muted">Purchase effects in the Shop to attach them to custom cards.</p>
          )}
        </div>
      </Panel>

      <Panel title="Owned Cards">
        {cards.length > 0 ? (
          <div className="card-grid">
            {cards.map((card) => (
              <PlayingCard card={card} key={card.card_id} />
            ))}
          </div>
        ) : (
          <EmptyState label="No custom cards yet." />
        )}
      </Panel>
    </div>
  );
}
