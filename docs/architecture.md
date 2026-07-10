# Architecture

## Overview

Card Game Plus follows a layered architecture that separates user interaction, business logic, and data persistence.

```
React Frontend
        │
 REST API (HTTP)
        │
 FastAPI Backend
        │
 ├── Game Engine
 ├── Authentication
 └── Database Layer
        │
 PostgreSQL
```

The application is divided into four primary layers:

- **Frontend (React)** — User interface and player interaction
- **Backend (FastAPI)** — API endpoints, authentication, and game orchestration
- **Database (PostgreSQL)** — Persistent storage for users, collections, and progression
- **Game Engine (Python)** — Core game rules, effects, and battle logic

---

# Core Domain Models
Core game objects:

- Card
- Effect
- EffectEngine
- Deck
- Player
- Game
- GameState

Future models:

- User
- Collection
- Match
- Shop
- Currency
- Inventory

---

# Layer Responsibilities

## Frontend

Responsible for:

- Login / Registration
- Deck Builder
- Battle UI
- Shop
- Collection
- Player Profile

The frontend should **never** contain game logic.

---

## Backend

Responsible for:

- Authentication
- API endpoints
- User validation
- Saving/loading games
- Calling the Game Engine
- Communicating with PostgreSQL

The backend acts as the bridge between the UI, database, and game engine.

---

## Game Engine

Responsible for:

- Turn resolution
- Card effects
- Damage calculation
- Win conditions
- AI decisions
- Rule enforcement

The Game Engine contains all gameplay logic and remains independent of the frontend.

---

## Database

Responsible for storing:

- Users
- Password hashes
- Card collections
- Decks
- Currency
- Match history
- Progression
- Shop inventory

---

# Design Decisions

## Card Templates

All standard cards exist as templates.

Players only own custom cards that reference those templates.

Reason:

- Eliminates duplicate data
- Simplifies balance updates
- Reduces database storage
- Makes future card updates significantly easier

---

## Effect Execution

Effects do **not** execute themselves.

Each Effect simply describes:

- Trigger
- Conditions
- Parameters

The `EffectEngine` is responsible for evaluating and executing all effects.

Reason:

- Single location for game rules
- Easier debugging
- Easier testing
- Supports future conditional effects

---

## Separation of Responsibilities

Domain models should primarily contain data.

Business logic belongs in specialized systems such as:

- EffectEngine
- Game
- AI Engine

Reason:

- Easier maintenance
- Better scalability
- Cleaner object design

---

# Guiding Principles

- Keep game logic independent of the UI.
- Keep database code independent of gameplay.
- Avoid duplicated data whenever possible.
- Favor composition over large, monolithic classes.
- Design systems so new cards and effects can be added with minimal code changes.

# Gameplay Architecture

## Game Zones

Cards exist in one of several game zones throughout a match.

Current zones:

- Deck
- Hand
- Field (planned)
- Graveyard (planned)

Cards are **persistent objects** that move between these zones rather than being created and destroyed during gameplay.

Example:

```
Deck
   ↓
Hand
   ↓
Field
   ↓
Graveyard
```

The Game Engine is responsible for moving cards between zones.

---

## Event-Driven Effects

Gameplay is event-driven.

When a game event occurs (playing a card, drawing, taking damage, etc.), the Game Engine notifies the `EffectEngine`.

Example:

```
Card Played
      │
      ▼
 Game Engine
      │
      ▼
 Effect Engine
      │
      ▼
 Resolve matching effects
```

The Game Engine detects events.

The Effect Engine determines which effects should activate.

---

## Effect Registration

Effects may remain registered after a card enters play depending on their duration.

Immediate effects:

- Resolve immediately.
- Are discarded after execution.

Persistent effects:

- Remain registered while their source card is in play.
- Continue listening for matching triggers.

This allows passive behavior without requiring a separate "PassiveEffect" model.

---

# Object Relationships

```
Game
│
├── Player
│      │
│      ├── Deck
│      │      │
│      │      └── Card
│      │              │
│      │              └── Effect
│      │                      │
│      │                      └── Condition
│      │
│      └── Hand (list[Card])
│
└── EffectEngine
```

Each layer is responsible only for the objects directly beneath it.

---

# Search System

The `Deck` supports flexible searching through the `SearchCriteria` model.

Rather than exposing numerous search methods, all searches are performed using a single criteria object.

Example:

```python
criteria = SearchCriteria(
    rank=Rank.KING,
    suit=Suit.HEARTS
)

results = deck.search(criteria)
```

Benefits:

- Easily extended with new search fields.
- Cleaner method signatures.
- Supports combining multiple search filters.
- Keeps search logic centralized.

---

# Effect Model

Each `Effect` completely describes a game mechanic through data.

An Effect answers four questions:

| Question | Property |
|-----------|----------|
| What happens? | `EffectType` |
| When does it happen? | `Trigger` |
| Who does it affect? | `Target` |
| How long does it remain active? | `EffectDuration` |

Optional properties:

- Condition
- Value

Because effects are data-driven, new cards can typically be added without modifying the engine itself.

---

# Collections vs Models

Not every collection requires its own model.

A dedicated model should exist only when it owns meaningful behavior.

Examples:

- `Deck` is a model because it can shuffle, search, draw, validate, and peek.
- A player's hand is currently implemented as a `list[Card]` because it only stores cards in V1.

This keeps the object model simple while allowing future refactoring if additional behavior is needed.