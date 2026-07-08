# Architecture

## Overview

The application is divided into four primary layers:

- Frontend (React)
- Backend (FastAPI)
- Database (PostgreSQL)
- Game Engine (Python)

---

## Domain Models

- Card
- Effect
- Deck
- Player
- Game
- GameState

---

## Design Decisions

### Card Templates

All standard cards exist as templates.

Players only own custom cards that reference those templates.

Reason:
- Eliminates duplicate data
- Simplifies updates
- Reduces storage