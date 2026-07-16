# CardGamePlus

CardGamePlus is a full-stack collectible card game built around a customizable, data-driven gameplay engine.

Players build unique decks by combining standard playing cards with permanently unlocked Effect templates, then battle against an AI opponent. The project demonstrates layered backend architecture, runtime object reconstruction, REST API design, and a modern React frontend.

---

# Features

## Gameplay

- Customizable card system
- Data-driven Effect engine
- Turn-based battle system
- AI opponent
- Runtime game engine
- Permanent card progression

## Backend

- FastAPI REST API
- JWT authentication
- Layered service architecture
- SQLAlchemy ORM
- Runtime object reconstruction
- SQLite development database
- PostgreSQL-ready design

## Player Systems

- User registration and login
- Deck builder
- Card collection
- Shop system
- Permanent Effect unlocks
- Gold rewards

---

# Tech Stack

## Backend

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Pydantic

## Frontend

- React
- TypeScript
- Vite

## Development

- Git
- GitHub
- PyCharm
- Swagger / OpenAPI

---

# Architecture

The project follows a layered architecture that separates persistence from gameplay.

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

Gameplay operates entirely on runtime objects while persistent data remains isolated inside the database layer.

---

# Documentation

Additional documentation can be found in the `docs/` directory.

- Architecture
- Database Design
- Game Rules
- Development Log

---

# Current Status

## Backend

- ✅ Runtime gameplay engine
- ✅ Effect engine
- ✅ SQLAlchemy database
- ✅ Authentication
- ✅ REST API
- ✅ AI opponent
- ✅ Deck builder
- ✅ Shop system

## In Progress

- 🚧 React frontend
- 🚧 Integration testing

## Planned

- Multiplayer
- Advanced AI
- Additional Effect templates
- Ranked matchmaking

---

# Project Goals

This project was built to demonstrate software engineering principles including:

- Object-Oriented Programming
- Layered Architecture
- REST API Design
- Database Design
- Runtime Object Reconstruction
- Separation of Concerns
- Data-Driven Game Systems

---

# License

This project is intended for educational and portfolio purposes.