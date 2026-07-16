# Architecture

# Overview

Card Game Plus follows a layered architecture that separates user interaction, business logic, persistence, and gameplay.

Each layer has a single responsibility and communicates only with the layer directly above or below it.

```
React Frontend
        │
        ▼
FastAPI Routers
        │
        ▼
Service Layer
        │
        ├──────────────┐
        ▼              ▼
Database         Runtime Objects
(SQLAlchemy)           │
        │              ▼
        └──────► GameEngine
                       │
                       ▼
                 EffectEngine
```

Persistence and gameplay are intentionally independent.

Services bridge the gap between persistent database records and the runtime objects required by the game engine.

---

# Project Structure

```
CardGamePlus/
│
├── assets/
├── database/
├── dependencies/
├── docs/
├── engines/
├── enums/
├── frontend/
├── models/
├── routers/
├── schemas/
├── services/
├── templates/
├── tests/
│
├── config.py
├── main.py
└── README.md
```

---

# Layer Responsibilities

## Frontend (React)

Responsible for:

- Login / Registration
- Deck Builder
- Collection
- Shop
- Battle UI
- Displaying game state

The frontend never contains gameplay rules.

Its responsibility is presenting data and sending player actions to the backend.

---

## FastAPI Routers

Responsible for:

- HTTP endpoints
- Authentication
- Request validation
- Response serialization

Routers remain intentionally thin.

They validate requests, call the appropriate service, and return serialized responses.

---

## Service Layer

The Service Layer bridges persistence and runtime gameplay.

Services have two primary responsibilities:

- Persist application data.
- Reconstruct runtime objects.

Each service owns one portion of the application.

---

### AuthService

Responsible for:

- Registering Users
- Authenticating Users
- Password hashing
- JWT creation
- JWT validation

---

### UserService

Responsible for:

- User persistence
- User retrieval
- Updating persistent User information

---

### ShopService

Responsible for:

- Shop inventory
- Purchasing Effect templates
- Gold management
- Tracking permanently unlocked Effects

The ShopService never creates Cards.

---

### EffectService

Responsible for:

- Persisting Effects
- Persisting Conditions
- Persisting SearchCriteria
- Reconstructing runtime Effect objects

---

### CardService

Responsible for:

- Creating starter collections
- Creating custom Cards
- Persisting Cards
- Reconstructing runtime Card objects

Cards are created from:

- One immutable Card template
- Zero or more unlocked Effect templates

---

### DeckService

Responsible for:

- Persisting Decks
- Maintaining Deck/Card relationships
- Reconstructing runtime Deck objects

---

### GameService

Responsible for:

- Creating runtime games
- Reconstructing the User's runtime Deck
- Constructing the default AI Deck
- Managing active games
- Coordinating the GameEngine
- Awarding post-game rewards

The GameService orchestrates persistence services but contains no gameplay rules.

---

## Database Layer

Responsible for storing persistent application data.

The database stores:

- Users
- Custom Cards
- Effects
- Conditions
- SearchCriteria
- Decks
- Deck/Card relationships
- Purchased Effect templates

The database never stores runtime gameplay objects.

---

## Runtime Models

Runtime models represent the objects used during gameplay.

These include:

- Card
- Effect
- Condition
- SearchCriteria
- Deck
- Hand
- Field
- Graveyard
- Player

Runtime models contain game state but are never persisted directly.

---

## Game Engine

The GameEngine is responsible for:

- Creating runtime Players
- Initializing matches
- Coordinating turn flow
- Executing the User's turn
- Executing the AI's turn
- Combat resolution
- Win condition detection
- Trigger detection
- Delegating Effects to the EffectEngine

The GameEngine owns gameplay but never interacts with the database.

---

## Effect Engine

The EffectEngine is responsible for:

- Evaluating Conditions
- Resolving Effect Targets
- Executing Effect behavior
- Tracking temporary Effect durations

The EffectEngine never determines when Effects trigger.

The GameEngine identifies triggered Effects and delegates only those Effects to the EffectEngine.

---

## AI

V1 includes a simple built-in AI opponent.

The AI:

- Uses a fixed runtime Deck.
- Shuffles its Deck at the beginning of each match.
- Draws Cards normally.
- Always plays the first Card in its hand.

The AI exists entirely in runtime and is never persisted to the database.

---

# Runtime Reconstruction

Runtime gameplay objects are never persisted directly.

Whenever gameplay begins, the GameService reconstructs the User's runtime Deck from the database while constructing the default runtime AI Deck from immutable templates.

Both runtime Decks are then passed to the GameEngine to create the two runtime Player objects used throughout the match.

The reconstruction flow is:

```
Database
        │
        ▼
Service Layer
        │
        ▼
Runtime Objects
        │
        ▼
GameEngine
```

Loading a Deck follows this process:

```
Deck
    │
    ▼
DeckCard
    │
    ▼
Card
    │
    ▼
Effect
    │
    ├── Condition
    └── SearchCriteria
```

Resulting runtime hierarchy:

```
Deck
│
├── Card
│     ├── Effect
│     │      ├── Condition
│     │      └── SearchCriteria
│     └── Effect
│
├── Card
└── ...
```

The GameEngine operates entirely on runtime objects without any knowledge of SQLAlchemy or database models.

---

## Active Games

Games exist entirely in memory.

Each authenticated User may have one active GameEngine instance managed by the GameService.

Runtime games are never persisted.

Once a game ends, the GameEngine instance is discarded.

---

# Design Decisions

## Immutable Templates

The application uses immutable templates for both standard playing Cards and purchasable Effect definitions.

Templates are never modified directly.

Instead, services construct new runtime objects from template data whenever gameplay objects are required.

Users never own template Cards.

Instead, persistent custom Cards are created by combining:

- One standard Card template
- Zero or more unlocked Effect templates

This minimizes duplicated data while allowing unlimited customization.

---

## Data-Driven Effects

Effects describe gameplay entirely through data.

Each Effect answers four questions:

| Question | Property |
|-----------|----------|
| What happens? | EffectType |
| When does it happen? | Trigger |
| Who does it affect? | Target |
| How long does it remain active? | EffectDuration |

Optional properties include:

- Condition
- SearchCriteria
- Value

Because Effects are data-driven, most new cards can be created without modifying the GameEngine.

---

## Separation of Responsibilities

Each layer owns exactly one responsibility.

- Routers expose the REST API.
- Services manage persistence and runtime reconstruction.
- Runtime models represent game state.
- The GameEngine coordinates gameplay.
- The EffectEngine executes Effects.

This separation keeps the application modular, testable, and easy to extend.

---

# Guiding Principles

- Keep gameplay independent of persistence.
- Keep persistence independent of gameplay.
- Store only persistent data.
- Reconstruct runtime objects when needed.
- Prefer composition over inheritance.
- Keep services focused on a single responsibility.
- Keep the GameEngine independent of the frontend and database.
- Design new Cards and Effects to require minimal engine changes.

---

# Current Status

✅ Runtime models complete

✅ SQLAlchemy models complete

✅ Runtime reconstruction complete

✅ Standard Card templates complete

✅ Effect templates complete

✅ AI runtime deck complete

✅ GameEngine complete

✅ EffectEngine complete

✅ Service layer complete

✅ Authentication complete

✅ FastAPI routers complete

✅ REST API complete

⏳ React frontend

⏳ Integration testing

⏳ Production deployment