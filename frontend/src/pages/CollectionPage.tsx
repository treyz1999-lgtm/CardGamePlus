import { useCallback, useEffect, useMemo, useState } from 'react';
import { Button } from '../components/Button';
import { EmptyState, ErrorMessage, LoadingState } from '../components/States';
import { Panel } from '../components/Panel';
import { PlayingCard } from '../components/PlayingCard';
import * as cardService from '../services/cardService';
import * as shopService from '../services/shopService';
import type { Card, CardTemplate, ShopItem } from '../types/api';
import { getErrorMessage } from '../utils/errors';

export function CollectionPage() {
  const [cards, setCards] = useState<Card[]>([]);
  const [shopItems, setShopItems] = useState<ShopItem[]>([]);
  const [cardTemplates, setCardTemplates] = useState<CardTemplate[]>([]);
  const [cardKey, setCardKey] = useState('');
  const [selectedEffects, setSelectedEffects] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ownedEffects = useMemo(
    () => shopItems.filter((item) => item.owned),
    [shopItems],
  );

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [cardData, inventory, templates] = await Promise.all([
        cardService.getCards(),
        shopService.getShopInventory(),
        cardService.getCardTemplates(),
      ]);
      setCards(cardData);
      setShopItems(inventory);
      setCardTemplates(templates);
      setCardKey((current) => current || templates[0]?.card_key || '');
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
            <span>Standard Card</span>
            <select
              value={cardKey}
              onChange={(event) => setCardKey(event.target.value)}
            >
              {cardTemplates.map((template) => (
                <option value={template.card_key} key={template.card_key}>
                  {template.display_name}
                </option>
              ))}
            </select>
          </label>
          <Button disabled={isSaving || !cardKey} onClick={handleCreateCard}>
            {isSaving ? 'Creating...' : 'Create Card'}
          </Button>
        </div>
        <div className="effect-picker">
          {ownedEffects.length > 0 ? (
            ownedEffects.map((effect) => (
              <label className="check-pill" key={effect.effect_key}>
                <input
                  type="checkbox"
                  checked={selectedEffects.includes(effect.effect_key)}
                  onChange={() => toggleEffect(effect.effect_key)}
                />
                <span>{effect.name}</span>
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
