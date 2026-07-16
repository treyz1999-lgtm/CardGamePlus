# Frontend Integration Notes

The V1 frontend uses only the existing FastAPI REST routes and does not add or assume new endpoints.

## Backend gaps found during integration

1. `routers/game_router.py` calls `GameService.get_game_state(...)`, but `services/game_service.py` does not currently define that method.
   - Minimal backend change: add `GameService.get_game_state(user_id)` that serializes the active `GameEngine` into the existing `schemas.game.GameStateResponse` shape.

2. `GET /shop/` returns `effect_key`, `cost`, and `owned`, but the V1 screen requirement asks for effect name and description.
   - Minimal backend change: include display metadata such as `name` and `description` in `ShopInventoryItem`.

3. Card creation requires a `card_key`, but there is no endpoint that exposes valid standard card templates.
   - Minimal backend change: add a read-only endpoint that returns standard card template keys and display metadata from `templates/standard_deck.py`.

Until those are available, the frontend:

- Calls `/game/state` and `/game/play` as designed, but depends on the missing backend serializer.
- Displays humanized effect keys as names and notes that descriptions are unavailable.
- Lets the user enter a two-character `card_key` instead of presenting a backend-populated template picker.
