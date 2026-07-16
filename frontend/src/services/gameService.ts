import { apiClient } from './apiClient';
import type {
  GameState,
  MessageResponse,
  PlayCardRequest,
  StartGameRequest,
} from '../types/api';

export async function startGame(request: StartGameRequest) {
  const response = await apiClient.post<MessageResponse>('/game/start', request);
  return response.data;
}

export async function playCard(request: PlayCardRequest) {
  const response = await apiClient.post<GameState>('/game/play', request);
  return response.data;
}

export async function getGameState() {
  const response = await apiClient.get<GameState>('/game/state');
  return response.data;
}
