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

# Domain Models

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