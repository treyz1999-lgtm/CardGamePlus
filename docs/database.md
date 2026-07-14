# Database

## Overview

War+ uses **SQLite** with **SQLAlchemy** to persist game data between sessions.

The database is responsible only for storing persistent information such as users, custom cards, effects, decks, and other player-owned resources.

Runtime gameplay objects are **not** stored directly in the database. Instead, services reconstruct runtime models from the stored data whenever they are needed.

---

# Design Philosophy

The database follows a normalized relational design.

Each table stores a single type of persistent entity, while relationships between entities are represented using foreign keys.

This keeps the database easy to query, maintain, and extend.

The database is **not** responsible for gameplay.

Instead:

```
Database
        │
        ▼
Service Layer
        │
        ▼
Runtime Models
        │
        ▼
GameEngine
        │
        ▼
EffectEngine
```

Services reconstruct runtime objects from database records before they are passed into the game engines.

---

# Database Schema

The current database consists of the following tables.

## User

Stores player accounts and persistent player information.

Attributes

- user_id (Primary Key)
- username
- password
- gold

Relationships

- Owns many Cards
- Owns many Decks

---

## Card

Stores every custom card owned by a user.

Attributes

- card_id (Primary Key)
- user_id (Foreign Key → User)
- suit
- rank
- health

Relationships

- Belongs to one User
- Owns zero or more Effects

---

## Effect

Stores every Effect attached to a Card.

Attributes

- effect_id (Primary Key)
- card_id (Foreign Key → Card)
- effect_type
- trigger
- target
- duration
- value

Relationships

- Belongs to one Card
- May own one Condition
- May own one SearchCriteria

---

## Condition

Stores optional activation requirements for an Effect.

Attributes

- condition_id (Primary Key)
- effect_id (Foreign Key → Effect)
- attribute
- comparison
- value

Relationships

- Belongs to one Effect

---

## SearchCriteria

Stores optional search filters used by search-related Effects.

Attributes

- search_id (Primary Key)
- effect_id (Foreign Key → Effect)
- rank
- suit
- effect_type

Relationships

- Belongs to one Effect

---

## Deck

Stores user-created decks.

Attributes

- deck_id (Primary Key)
- user_id (Foreign Key → User)
- name

Relationships

- Belongs to one User
- Contains Cards through the DeckCard table

---

## DeckCard

Join table representing the relationship between Decks and Cards.

Attributes

- deck_card_id (Primary Key)
- deck_id (Foreign Key → Deck)
- card_id (Foreign Key → Card)

Relationships

- Associates Cards with Decks

---

# Runtime Reconstruction

The database never stores runtime objects directly.

Instead, services rebuild the object hierarchy when needed.

For example, loading a Deck follows the general process:

```
Load Deck
    │
    ▼
Query DeckCard records
    │
    ▼
Query Card records
    │
    ▼
Query Effect records
    │
    ▼
Query Condition / SearchCriteria records
    │
    ▼
Construct runtime objects
```

The final runtime hierarchy becomes:

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

This separation allows the game engines to operate entirely on runtime models without any knowledge of the underlying database.

---

# Current Status

✅ SQLite database implemented

✅ SQLAlchemy ORM models complete

✅ Relational schema complete

⏳ Service layer (reconstruct runtime objects)

⏳ Authentication

⏳ API routers