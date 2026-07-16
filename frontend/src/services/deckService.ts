import { apiClient } from './apiClient';
import type {
  AddCardRequest,
  CreateDeckRequest,
  CreateDeckResponse,
  DeckCollectionResponse,
  DeckDetails,
  MessageResponse,
} from '../types/api';

export async function getDecks() {
  const response = await apiClient.get<DeckCollectionResponse>('/decks/');
  return response.data.decks;
}

export async function getDeck(deckId: number) {
  const response = await apiClient.get<DeckDetails>(`/decks/${deckId}`);
  return response.data;
}

export async function createDeck(request: CreateDeckRequest) {
  const response = await apiClient.post<CreateDeckResponse>('/decks/', request);
  return response.data;
}

export async function deleteDeck(deckId: number) {
  const response = await apiClient.delete<MessageResponse>(`/decks/${deckId}`);
  return response.data;
}

export async function addCardToDeck(deckId: number, request: AddCardRequest) {
  const response = await apiClient.post<MessageResponse>(`/decks/${deckId}/cards`, request);
  return response.data;
}

export async function removeCardFromDeck(deckId: number, cardId: number) {
  const response = await apiClient.delete<MessageResponse>(`/decks/${deckId}/cards/${cardId}`);
  return response.data;
}
