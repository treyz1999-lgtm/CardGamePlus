import { apiClient } from './apiClient';
import type {
  LoginRequest,
  MessageResponse,
  RegisterRequest,
  TokenResponse,
  User,
} from '../types/api';

export async function login(request: LoginRequest) {
  const response = await apiClient.post<TokenResponse>('/auth/login', request);
  return response.data;
}

export async function register(request: RegisterRequest) {
  const response = await apiClient.post<MessageResponse>('/auth/register', request);
  return response.data;
}

export async function getCurrentUser() {
  const response = await apiClient.get<User>('/users/me');
  return response.data;
}
