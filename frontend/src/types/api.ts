export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type?: string;
}

export interface MessageResponse {
  message: string;
}

export interface User {
  user_id: number;
  username: string;
  gold: number;
}

export interface Card {
  card_id: number;
  suit: string;
  rank: number;
  health: number;
  effects: string[];
}

export interface CardCollectionResponse {
  cards: Card[];
}

export interface CreateCardRequest {
  card_key: string;
  effect_keys: string[];
}

export interface CreateCardResponse extends MessageResponse {
  card_id: number;
}

export interface CardTemplate {
  card_key: string;
  suit: string;
  rank: number;
  display_name: string;
}

export interface CardTemplateCollectionResponse {
  templates: CardTemplate[];
}

export interface Deck {
  deck_id: number;
  name: string;
}

export interface DeckDetails extends Deck {
  cards: Card[];
}

export interface DeckCollectionResponse {
  decks: Deck[];
}

export interface CreateDeckRequest {
  name: string;
  card_ids: number[];
}

export interface CreateDeckResponse extends MessageResponse {
  deck_id: number;
}

export interface AddCardRequest {
  card_id: number;
}

export interface ShopItem {
  effect_key: string;
  name: string;
  description: string;
  cost: number;
  owned: boolean;
}

export interface ShopInventoryResponse {
  inventory: ShopItem[];
}

export interface PurchaseEffectRequest {
  effect_key: string;
}

export interface PurchaseEffectResponse extends MessageResponse {
  gold: number;
}

export interface StartGameRequest {
  deck_id: number;
}

export interface PlayCardRequest {
  hand_index: number;
}

export interface UserGameState {
  hp: number;
  deck_size: number;
  hand: Card[];
  field: Card[];
  graveyard: Card[];
}

export interface AIGameState {
  hp: number;
  deck_size: number;
  hand_size: number;
  field: Card[];
  graveyard: Card[];
}

export interface GameState {
  turn_number: number;
  game_over: boolean;
  winner: string | null;
  user: UserGameState;
  ai: AIGameState;
}
