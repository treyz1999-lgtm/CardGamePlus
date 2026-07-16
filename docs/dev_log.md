---

# Current Status

The architecture evolved significantly after the initial prototype.

Major changes since the early development logs include:

## Architecture

- Introduced a layered architecture separating Routers, Services, Runtime Models, and Game Engines.
- Separated persistent SQLAlchemy models from runtime gameplay objects.
- Added runtime reconstruction through the Service Layer.

## Runtime Models

Implemented:

- Card
- Effect
- Condition
- SearchCriteria
- Deck
- Hand
- Field
- Graveyard
- Player

## Engines

Completed:

- GameEngine
- EffectEngine

Gameplay is now fully coordinated by the GameEngine while the EffectEngine executes data-driven Effects.

## Persistence

Implemented a normalized SQLAlchemy schema consisting of:

- User
- Card
- Effect
- Condition
- SearchCriteria
- Deck
- DeckCard
- UserEffect

## Backend

Completed a FastAPI REST API including:

- Authentication
- User
- Shop
- Card Collection
- Deck Builder
- Gameplay

## AI

Implemented a V1 AI opponent.

The AI:

- Uses a fixed runtime Deck.
- Shuffles its Deck at the beginning of each match.
- Draws normally.
- Always plays the first Card in its hand.

## Current Focus

The backend architecture is complete.

Current development has shifted toward:

- React frontend
- Integration testing
- Gameplay balancing
- Additional card effects