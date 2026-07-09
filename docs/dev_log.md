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