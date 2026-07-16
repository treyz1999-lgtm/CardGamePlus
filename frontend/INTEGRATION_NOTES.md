# Frontend Integration Notes

The V1 frontend uses only the existing FastAPI REST routes and does not add or assume new endpoints.

## Backend integration status

Resolved during integration:

- `GameService.get_game_state(user_id)` now serializes active runtime games into the existing `schemas.game.GameStateResponse` shape.
- Completed matches now preserve the final serialized game state long enough for `/game/play` to return Victory or Defeat before the completed state is cleared.
- Runtime Deck and Card reconstruction now match the existing runtime model constructors and response schemas.
- Deck mutation router/service signatures now match.
- `GET /shop/` now includes backend-derived Effect display `name` and `description` fields while preserving `effect_key`, `cost`, and `owned`.
- `GET /cards/templates` now exposes immutable standard Card templates for the Collection card-creation picker.

There are no known frontend API gaps remaining for the V1 screens.
