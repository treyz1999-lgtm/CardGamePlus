# Database

## Overview

Card Game Plus uses **SQLite** during development with **SQLAlchemy** as the Object Relational Mapper (ORM).

The database is responsible only for storing persistent application data.

Runtime gameplay objects are never stored directly. Instead, the service layer reconstructs runtime objects from database records whenever they are needed.

---

# Design Philosophy

The database follows a normalized relational design.

Each table stores a single type of persistent entity while relationships between entities are represented using foreign keys.

This keeps the schema:

- Easy to query
- Easy to maintain
- Easy to extend

The database is **not** responsible for gameplay.

Instead, the application follows this architecture:

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

The services reconstruct runtime objects before they are passed into the game engines.

---

# Database Schema

The current database consists of the following tables.

---

## User

Stores player accounts and persistent player information.

### Attributes

- user_id (Primary Key)
- username
- password_hash
- gold

### Relationships

- Owns many Cards
- Owns many Decks
- Owns many unlocked Effect templates

---

## Card

Stores every persistent custom Card owned by a User.

Cards are created from immutable Card templates plus zero or more purchased Effect templates.

### Attributes

- card_id (Primary Key)
- user_id (Foreign Key → User)
- suit
- rank
- health

### Relationships

- Belongs to one User
- Owns zero or more Effects

---

## Effect

Stores every Effect attached to a Card.

### Attributes

- effect_id (Primary Key)
- card_id (Foreign Key → Card)
- effect_type
- trigger
- target
- duration
- value

### Relationships

- Belongs to one Card
- May own one Condition
- May own one SearchCriteria

---

## Condition

Stores optional activation requirements for an Effect.

### Attributes

- condition_id (Primary Key)
- effect_id (Foreign Key → Effect)
- attribute
- comparison
- value

### Relationships

- Belongs to one Effect

---

## SearchCriteria

Stores optional search filters used by search-related Effects.

### Attributes

- search_id (Primary Key)
- effect_id (Foreign Key → Effect)
- rank
- suit
- effect_type

### Relationships

- Belongs to one Effect

---

## Deck

Stores user-created Decks.

### Attributes

- deck_id (Primary Key)
- user_id (Foreign Key → User)
- name

### Relationships

- Belongs to one User
- Contains Cards through the DeckCard table

---

## DeckCard

Join table representing the many-to-many relationship between Decks and Cards.

### Attributes

- deck_card_id (Primary Key)
- deck_id (Foreign Key → Deck)
- card_id (Foreign Key → Card)

### Relationships

- Associates Cards with Decks

---

## UserEffect

Stores permanently unlocked Effect templates purchased from the Shop.

The table stores only the template key.

The template definitions themselves are stored in `effect_templates.py`.

### Attributes

- user_effect_id (Primary Key)
- user_id (Foreign Key → User)
- effect_key

### Relationships

- Belongs to one User

A user may unlock many Effect templates, but each template may only be owned once.

---

# Runtime Reconstruction

The database never stores runtime objects directly.

Instead, services reconstruct the object hierarchy whenever gameplay begins.

For example, loading a Deck follows this process:

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
Query Condition records
    │
    ▼
Query SearchCriteria records
    │
    ▼
Construct runtime objects
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

The GameEngine operates entirely on runtime objects and has no knowledge of the database.

---

# Service Responsibilities

Each database table has a corresponding service responsible for persisting and reconstructing its runtime model.

| Service | Primary Responsibility |
|----------|------------------------|
| AuthService | Authentication and JWT |
| UserService | User persistence |
| ShopService | Gold and unlocked Effect templates |
| CardService | Card persistence and reconstruction |
| EffectService | Effect persistence and reconstruction |
| DeckService | Deck persistence and reconstruction |
| GameService | Runtime game orchestration |

This separation keeps persistence independent from gameplay.

---

# Design Decisions

## Immutable Card Templates

Standard playing cards are never stored in the database.

Instead, custom Cards reference immutable templates defined in `standard_deck.py`.

This eliminates duplicated card data while allowing unlimited customization.

---

## Immutable Effect Templates

Purchasable Effects are defined once inside `effect_templates.py`.

The Shop stores only the template key that identifies which templates a User has unlocked.

Custom Cards may freely reuse any unlocked template without purchasing it again.

---

## Runtime Objects

Runtime models are reconstructed by the service layer whenever a game begins.

This allows the GameEngine to operate entirely on Python objects without any dependency on SQLAlchemy or the database.

---

# Current Status

✅ SQLite database implemented

✅ SQLAlchemy ORM models complete

✅ Relational schema complete

✅ Authentication complete

✅ Service layer complete

⏳ FastAPI routers

⏳ REST API

⏳ React frontend