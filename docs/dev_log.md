# Dev Log

## Day 1

### Completed

- Created `Card` class
- Added default card health system
- Implemented `Suit` enum
- Implemented `Rank` enum
- Created `Effect` class
- Designed `EffectEngine`
- Established initial project architecture
- Created project folder structure


---

### Design Decisions

- Separated card data from game logic.
- Chose to make `Effect` a data object rather than allowing it to execute logic directly.
- Centralized effect execution inside the `EffectEngine` to improve maintainability and simplify adding future card effects.
- Added a base health value to every card to support future mechanics beyond traditional War.

---

### Lessons Learned

- Thinking through architecture before writing large amounts of code makes implementation much easier.
- Separating responsibilities early should make future expansion (new effects, AI, multiplayer, etc.) significantly easier.

---

### Next Steps

- Finish the `Deck` class.
- Create the `Player` class.
- Implement basic game setup (shuffle, deal, draw).
- Build a playable command-line prototype before moving to the web application.

---

### Future Ideas

- Conditional effects
- Status effects
- Equipment cards
- Currency and progression system
- User accounts and saved collections
- AI opponents with multiple difficulty levels


## Day 2

### Completed

- Implemented the `Deck` model.
- Added deck validation using configurable minimum and maximum deck sizes.
- Implemented deck shuffling.
- Implemented multi-card drawing with graceful empty-deck handling.
- Added card searching using the `SearchCriteria` model.
- Implemented searching by:
  - Rank
  - Suit
  - Effect Type
  - Multiple criteria simultaneously
- Added `peek()` functionality.
- Added `remove_card()` and `contains()` methods.
- Created the `SearchCriteria` model.
- Added the `EffectDuration` enum.
- Refactored the `Effect` model to support effect duration.
- Expanded the project's unit tests with a complete `Deck` test suite.

---

### Design Decisions

- Kept `Deck` responsible only for deck-related behavior (shuffle, draw, search, peek, etc.).
- Designed `SearchCriteria` as a dedicated model instead of passing numerous optional parameters to `Deck.search()`.
- Chose to search using explicit model attributes rather than a generic dictionary-based search system to improve readability and type safety.
- Distinguished **Trigger** ("when an effect activates") from **EffectDuration** ("how long an effect remains registered").
- Decided not to create a `Hand` model for V1; a player's hand will simply be a `list[Card]` maintained by the `Player`.
- Treated `Card` objects as persistent game entities that move between zones rather than being created and destroyed throughout gameplay.

---

### Lessons Learned

- Collections should search based on the properties of the objects they contain rather than duplicating those properties themselves.
- `any()` provides a clean and efficient way to search nested collections.
- Not every concept needs its own class—built-in types such as `list` are often sufficient until additional behavior is required.
- Separating data models from engine logic continues to simplify the architecture and makes future expansion easier.
- Spending time refining responsibilities before implementation reduces the amount of code that needs to be rewritten later.

---

### Architecture Progress

Current model hierarchy:

Player (WIP)
│
├── Deck
│ │
│ └── Card
│ │
│ └── Effect
│ │
│ └── Condition
│
└── Hand (list[Card])

Current game zones:

- Deck
- Hand (Player)
- Graveyard (planned)
- Field (planned)

Cards are persistent objects that move between zones throughout a match.

---

### Next Steps

- Implement the `Player` model.
- Build the initial game setup flow.
- Create the `GameEngine`.
- Implement effect registration and resolution.
- Begin a playable command-line prototype.

---

### Future Ideas

- Persistent effect registration system.
- Event-driven effect resolution.
- More advanced effect durations.
- Status effects.
- Equipment cards.
- AI opponents.
- Multiplayer support.
- Database-backed user accounts and saved collections.