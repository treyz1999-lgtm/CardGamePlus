import { useCallback, useEffect, useState } from 'react';
import { Button } from '../components/Button';
import { Panel } from '../components/Panel';
import { EmptyState, ErrorMessage, LoadingState } from '../components/States';
import { useAuth } from '../contexts/AuthContext';
import * as shopService from '../services/shopService';
import type { ShopItem } from '../types/api';
import { getErrorMessage } from '../utils/errors';

export function ShopPage() {
  const [inventory, setInventory] = useState<ShopItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { refreshUser } = useAuth();

  const loadInventory = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      setInventory(await shopService.getShopInventory());
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadInventory();
  }, [loadInventory]);

  async function handlePurchase(effectKey: string) {
    setError(null);

    try {
      await shopService.purchaseEffect({ effect_key: effectKey });
      await Promise.all([loadInventory(), refreshUser()]);
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    }
  }

  if (isLoading) {
    return <LoadingState label="Opening shop..." />;
  }

  return (
    <Panel title="Effect Shop">
      {error ? <ErrorMessage label={error} /> : null}
      {inventory.length > 0 ? (
        <div className="shop-grid">
          {inventory.map((item) => (
            <article className="shop-item" key={item.effect_key}>
              <div>
                <h3>{item.name}</h3>
                <p className="muted">{item.description}</p>
              </div>
              <div className="shop-item-footer">
                <strong>{item.cost} gold</strong>
                <span className={item.owned ? 'owned-badge' : 'unowned-badge'}>
                  {item.owned ? 'Owned' : 'Available'}
                </span>
                <Button disabled={item.owned} onClick={() => handlePurchase(item.effect_key)}>
                  Purchase
                </Button>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <EmptyState label="No effects are available." />
      )}
    </Panel>
  );
}
