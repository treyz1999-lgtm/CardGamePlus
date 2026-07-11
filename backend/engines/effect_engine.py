from models.effect import Effect
from models.player import Player
from models.deck import Deck


class EffectEngine:
    def __init__(self):
        # Tracks immediate effects that have already been
        # resolved during the current turn.
        self.resolved_effects: set[Effect] = set()

    def resolve(self, player: Player, effects: list[Effect]) -> None:
        """
        Resolve every Effect available to the given Player.

        The EffectEngine determines how each Effect behaves
        based on its Trigger, EffectDuration, Condition,
        Target, and EffectType.

        The GameEngine is responsible only for deciding when
        this function should be called.
        """
        for effect in effects:
            self._resolve_effect(player, effect)

    def _resolve_effect(self, player: Player, effect: Effect) -> None:
        """
        Resolve a single Effect.
        """
        pass

    def _resolve_immediate(self, player: Player, effect: Effect) -> None:
        """
        Resolve a one-time Effect.
        """
        pass

    def _resolve_persistent(self, player: Player, effect: Effect) -> None:
        """
        Resolve a WHILE_IN_PLAY Effect.
        """
        pass

    def _check_conditions(self, player: Player, effect: Effect) -> bool:
        """
        Determine whether an Effect's conditions are satisfied.
        """
        pass

    def _execute_effect(self, player: Player, effect: Effect) -> None:
        """
        Execute an Effect based on its EffectType.
        """
        pass

    def reset_turn(self) -> None:
        """
        Clear all runtime state that lasts for a single turn.
        """
        self.resolved_effects.clear()