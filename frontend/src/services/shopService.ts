import { apiClient } from './apiClient';
import type {
  PurchaseEffectRequest,
  PurchaseEffectResponse,
  ShopInventoryResponse,
} from '../types/api';

export async function getShopInventory() {
  const response = await apiClient.get<ShopInventoryResponse>('/shop/');
  return response.data.inventory;
}

export async function purchaseEffect(request: PurchaseEffectRequest) {
  const response = await apiClient.post<PurchaseEffectResponse>('/shop/purchase', request);
  return response.data;
}
