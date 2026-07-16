# Database

# Overview

Card Game Plus uses **SQLite** during development with **SQLAlchemy** as its Object Relational Mapper (ORM).

The database stores only persistent application data.

Gameplay objects are never stored directly. Instead, the Service Layer reconstructs runtime objects from database records whenever gameplay begins.

---

# Design Philosophy

The database follows a normalized relational design.

Each table stores one type of persistent entity while relationships are represented using foreign keys.

This design keeps the schema:

- Easy to query
- Easy to maintain
- Easy to extend

The database is intentionally independent of gameplay.

Runtime reconstruction follows this flow:

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

The GameEngine never interacts directly with SQLAlchemy models.

---

# Database Schema

The V1 database consists of the following tables.

---

## User

Stores player accounts and persistent player progression.

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

Cards are created from one immutable Card template and zero or more unlocked Effect templates.

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

Stores every Effect attached to a persistent Card.

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

Although V1 does not currently include search Effects, the schema is included to support future expansion without requiring database changes.

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
- Contains many Cards through DeckCard

---

## DeckCard

Join table implementing the many-to-many relationship between Decks and Cards.

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

A User may unlock many Effect templates, but each template may only be owned once.

---

# Runtime Reconstruction

The database never stores runtime gameplay objects.

Whenever gameplay begins, the Service Layer reconstructs the complete runtime object hierarchy from persistent records.

Deck reconstruction follows this process:

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
    ├── Query Condition records
    │
    └── Query SearchCriteria records
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

The reconstructed Deck is then passed into the GameEngine to create the runtime Player.

During gameplay, the GameEngine interacts only with runtime objects and has no knowledge of SQLAlchemy or the underlying database.

---

# Runtime vs Persistence

Persistent data and gameplay state are intentionally separated.

Persistent data includes:

- Users
- Custom Cards
- Effects
- Conditions
- SearchCriteria
- Decks
- Purchased Effect templates

Runtime objects include:

- Player
- Deck
- Hand
- Field
- Graveyard
- Card
- Effect
- Condition
- SearchCriteria

Runtime objects exist only while a game is active.

---

# AI

The V1 AI opponent is never stored in the database.

Instead, the GameService constructs a default runtime AI Deck directly from immutable templates whenever a game begins.

This keeps the database focused entirely on player-owned content.

---

# Service Responsibilities

Each database table has a corresponding service responsible for persistence and runtime reconstruction.

| Service | Responsibility |
|----------|----------------|
| AuthService | Authentication and JWT management |
| UserService | User persistence |
| ShopService | Gold management and unlocked Effect templates |
| EffectService | Effect persistence and runtime reconstruction |
| CardService | Card persistence and runtime reconstruction |
| DeckService | Deck persistence and runtime reconstruction |
| GameService | Runtime game orchestration |

This separation keeps persistence independent from gameplay.

---

# Design Decisions

## Immutable Card Templates

Standard playing Cards are never stored in the database.

Instead, custom Cards are created from immutable templates defined in `standard_deck.py`.

This eliminates duplicated card data while allowing unlimited customization.

---

## Immutable Effect Templates

Purchasable Effects are defined once inside `effect_templates.py`.

The Shop stores only the template key identifying which Effect templates a User has permanently unlocked.

Custom Cards may reuse any unlocked template without purchasing it again.

---

## Runtime Reconstruction

Runtime gameplay objects are reconstructed by the Service Layer whenever gameplay begins.

This allows the GameEngine to operate entirely on Python objects without any dependency on SQLAlchemy.

---

## Active Games

Games are never persisted.

Each authenticated User may have one active GameEngine instance stored in memory by the GameService.

Once a game ends, the runtime GameEngine is discarded.

---

# Current Status

✅ SQLite database implemented

✅ SQLAlchemy ORM models complete

✅ Relational schema complete

✅ Runtime reconstruction complete

✅ Authentication complete

✅ Service layer complete

✅ REST API complete

⏳ React frontend

⏳ Integration testing

⏳ Production deployment