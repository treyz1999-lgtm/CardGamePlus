# Game Rules

# Overview

Card Game Plus is a customizable strategy card game inspired by the traditional game of War.

Players build custom Decks by combining standard playing Cards with permanently unlocked Effect templates. During a match, both players play one Card each turn while Effects modify combat, health, and gameplay.

The objective is to reduce the opposing Player's Health to zero.

---

# Victory Condition

A Player loses when their Health reaches **0**.

The remaining Player immediately wins the game.

The GameEngine checks for a winner after every combat phase.

---

# Starting a Game

When a new game begins:

1. The User selects one of their Decks.
2. The GameService reconstructs the User's runtime Deck.
3. The GameService constructs the default AI Deck.
4. Both Decks are shuffled.
5. Both Players draw three Cards.
6. The User takes the first turn.

---

# Turn Structure

Each round consists of one complete User turn immediately followed by one complete AI turn.

The GameEngine coordinates every phase of gameplay.

```
User Turn
        │
        ▼
Play Card
        │
        ▼
Resolve ON_PLAY Effects
        │
        ▼
AI Turn
        │
        ▼
Play Card
        │
        ▼
Resolve ON_PLAY Effects
        │
        ▼
Combat
        │
        ▼
Resolve ON_DAMAGE Effects
        │
        ▼
End Turn
        │
        ▼
Resolve ON_DEATH Effects
        │
        ▼
Next Turn
```

---

# Turn Phases

## Start Turn

At the beginning of a Player's turn:

- Action counters are reset.
- One Card is drawn.
- All `TURN_START` Effects are resolved.

---

## Play Phase

The active Player selects one Card from their Hand.

The Card is moved from the Hand to the Field.

After the Card enters play:

- All `ON_PLAY` Effects are resolved.

---

## AI Turn

The V1 AI is intentionally simple.

The AI:

- Draws normally.
- Always plays the first Card in its Hand.
- Does not evaluate board state.

Future versions may introduce more advanced decision making.

---

## Combat Phase

Combat compares the total combat power of both Fields.

```
Higher Combat Power
        │
        ▼
Opponent loses 1 Health
```

If combat power is equal:

- No damage is dealt.

After combat:

- The GameEngine checks for a winner.
- If the game ends, the remaining phases are skipped.

---

## End Turn

At the end of each turn:

- Every Card on both Fields loses one Health.
- Defeated Cards are identified.
- `ON_DEATH` Effects are resolved.
- Defeated Cards move to the Graveyard.
- Temporary Effects are cleared.
- Turn counters advance.

---

# Cards

Each Card consists of:

- Suit
- Rank
- Health
- Zero or more Effects

Combat power is determined by the Card's Rank and any active modifiers.

Cards move between gameplay zones throughout the match.

---

# Gameplay Zones

Each Player owns four gameplay zones.

```
Deck
   │
   ▼
Hand
   │
   ▼
Field
   │
   ▼
Graveyard
```

## Deck

Stores Cards that have not yet been drawn.

---

## Hand

Stores Cards available to play.

Only the owning Player may view the contents of their Hand.

---

## Field

Stores Cards currently participating in combat.

Effects may target Cards on the Field.

---

## Graveyard

Stores defeated Cards.

Future Effects may interact with the Graveyard.

---

# Effects

Effects modify gameplay.

Effects are entirely data-driven and are interpreted by the EffectEngine.

Each Effect defines:

- EffectType
- Trigger
- Target
- EffectDuration
- Optional Condition
- Optional SearchCriteria
- Value

---

# Triggers

V1 supports the following triggers:

- TURN_START
- TURN_END
- ON_PLAY
- ON_DRAW
- ON_DISCARD
- ON_DAMAGE
- ON_DEATH
- ON_HEAL

Not every Trigger is currently used by V1 cards, but all are supported by the runtime architecture.

---

# Conditions

Effects may include optional Conditions.

Conditions determine whether an Effect should activate.

Examples include:

- Card Rank
- Suit
- Player Health
- Hand Size

Conditions are evaluated by the EffectEngine immediately before an Effect executes.

---

# Search Effects

The runtime architecture supports search-based Effects through SearchCriteria.

Although no V1 cards currently use search Effects, the system has been fully implemented for future expansion.

---

# AI

The V1 AI is intentionally predictable.

The AI:

- Uses a fixed runtime Deck.
- Shuffles every game.
- Draws Cards normally.
- Always plays the first Card in its Hand.

This provides a simple opponent while allowing the gameplay systems to be tested.

---

# Rewards

When a User wins a game:

- The GameService awards a fixed amount of Gold.

Losing a game provides no reward.

Future versions may introduce:

- Experience
- Ranked progression
- Daily rewards
- Achievements

---

# Design Philosophy

The game follows several core principles.

- Keep gameplay deterministic.
- Separate gameplay from persistence.
- Keep Effects data-driven.
- Minimize engine changes when adding new Cards.
- Build reusable systems rather than hardcoded card behavior.
- Keep the frontend responsible only for presentation.

---

# Current V1 Scope

Implemented:

- Runtime gameplay engine
- Effect engine
- Deck construction
- Custom Cards
- Shop and permanent Effect unlocks
- AI opponent
- FastAPI backend
- REST API

Planned after V1:

- Additional Effect types
- Search-based Cards
- Improved AI
- Multiplayer
- Ranked matchmaking
- Seasonal content