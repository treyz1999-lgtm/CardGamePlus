import { apiClient } from './apiClient';
import type {
  CardCollectionResponse,
  CreateCardRequest,
  CreateCardResponse,
  MessageResponse,
} from '../types/api';

export async function getCards() {
  const response = await apiClient.get<CardCollectionResponse>('/cards/');
  return response.data.cards;
}

export async function createCard(request: CreateCardRequest) {
  const response = await apiClient.post<CreateCardResponse>('/cards/', request);
  return response.data;
}

export async function deleteCard(cardId: number) {
  const response = await apiClient.delete<MessageResponse>(`/cards/${cardId}`);
  return response.data;
}
