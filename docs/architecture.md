# Architecture

## Overview

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
        ▼
SQLAlchemy Models
        │
        ▼
SQLite / PostgreSQL
```

Runtime gameplay is completely separated from persistence.

```
GameService
        │
        ▼
DeckService
        │
        ▼
CardService
        │
        ▼
EffectService
        │
        ▼
Runtime Objects
        │
        ▼
GameEngine
        │
        ▼
EffectEngine
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

The frontend never contains game rules.

Its only responsibility is presenting data and sending user actions to the backend.

---

## FastAPI Routers

Responsible for:

- HTTP endpoints
- Authentication
- Request validation
- Response serialization

Routers should remain extremely thin.

They receive requests, validate payloads, call the appropriate service, and return the response.

---

## Service Layer

The service layer acts as the bridge between the database and the runtime game engine.

Services have two primary responsibilities:

- Persist application data.
- Reconstruct runtime objects.

Each service owns one area of the application.

### AuthService

Responsible for:

- Registering users
- Authenticating users
- Password hashing
- JWT creation
- JWT validation

---

### UserService

Responsible for:

- User persistence
- User retrieval
- Updating persistent player information

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

Cards are created from one immutable Card template plus zero or more unlocked Effect templates.

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
- Reconstructing runtime Decks
- Managing active games
- Coordinating the GameEngine

The GameService orchestrates the other services but contains no gameplay rules.

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
- Player
- Field
- Graveyard

Runtime models contain game state but are never stored directly in the database.

---

## Game Engine

The GameEngine is responsible for:

- Turn flow
- Combat
- Win conditions
- Trigger detection
- Calling the EffectEngine

The GameEngine contains no database logic.

---

## Effect Engine

The EffectEngine is responsible for:

- Resolving Effects
- Evaluating Conditions
- Applying gameplay actions
- Executing Effect behavior

Effects themselves are data.

The EffectEngine interprets and executes them.

---

# Runtime Reconstruction

Runtime gameplay objects are never persisted directly.

Instead, services reconstruct them from database records whenever they are required.

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

For example, loading a Deck follows this process:

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

The resulting runtime hierarchy becomes:

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

The GameEngine operates entirely on these runtime objects without any knowledge of the underlying database.

---

# Design Decisions

## Immutable Templates

Standard playing cards are stored as immutable templates.

Players never own template cards.

Instead, users create persistent custom Cards by combining:

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

Because Effects are data-driven, most new cards can be created without modifying the game engine.

---

## Separation of Responsibilities

Each layer owns exactly one responsibility.

- Routers expose the API.
- Services manage persistence.
- Runtime models store game state.
- GameEngine controls gameplay.
- EffectEngine executes Effects.

This separation makes the application easier to maintain, test, and extend.

---

# Guiding Principles

- Keep game logic independent of persistence.
- Keep persistence independent of gameplay.
- Store only persistent data.
- Reconstruct runtime objects when needed.
- Prefer composition over inheritance.
- Keep services focused on a single responsibility.
- Keep the GameEngine independent of the frontend and database.
- Design new cards and effects to require minimal engine changes.

---

# Current Status

✅ Runtime domain models complete

✅ GameEngine complete

✅ EffectEngine complete

✅ SQLAlchemy models complete

✅ Service layer complete

✅ Authentication complete

⏳ FastAPI routers

⏳ REST API

⏳ React frontend