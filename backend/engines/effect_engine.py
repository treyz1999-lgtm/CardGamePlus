from enums.condition import ConditionAttribute, Comparison
from enums.effect_duration import EffectDuration
from enums.effect_type import EffectType
from enums.target import Target

from models.card import Card
from models.effect import Effect
from models.player import Player

"""
Effect Engine

Responsible for resolving Effects supplied by the GameEngine.

Unlike the GameEngine, the EffectEngine has no knowledge of
gameplay events or timing. It simply resolves the Effects it
is given.

The GameEngine determines when Effects should activate by
collecting every (Card, Effect) pair whose Trigger matches the
current gameplay event and passing those pairs into this engine.

Pipeline
--------

GameEngine
    │
    ├── Determine current gameplay event.
    ├── Collect triggered (Card, Effect) pairs.
    │
    ▼
resolve(source_player, target_player, effects)
    │
    ├── Iterate through every (Card, Effect).
    │
    ▼
_resolve_effect()
    │
    ├── Skip already resolved immediate Effects.
    ├── Evaluate Conditions.
    ├── Determine EffectDuration.
    │
    ▼
_resolve_immediate()
        or
_resolve_persistent()
    │
    ▼
_execute_effect()
    │
    ├── Resolve target.
    ├── Execute EffectType.
    │
    ▼
Player / Card / Deck updated

Responsibilities
----------------

The EffectEngine is responsible for:

- Resolving Effects.
- Evaluating Conditions.
- Determining Effect Targets.
- Tracking immediate Effects already resolved this turn.
- Executing gameplay logic for each EffectType.

The EffectEngine is NOT responsible for:

- Determining gameplay events.
- Determining Effect Triggers.
- Turn order.
- Combat.
- Moving cards between zones.
- Database operations.
"""

class EffectEngine:

    def __init__(self):
        self.resolved_effects: set[Effect] = set()

    def resolve(self, source_player: Player, target_player: Player, effects: list[tuple[Card, Effect]],) -> None:
        """
        Resolve every triggered Effect supplied by the GameEngine.
        """

        if not effects:
            return

        for card, effect in effects:
            self._resolve_effect(source_player, target_player, card, effect,)

    def _resolve_effect(self, source_player: Player, target_player: Player, card: Card, effect: Effect,) -> None:

        if effect in self.resolved_effects:
            return

        if not self._check_conditions(source_player, card, effect,):
            return

        match effect.duration:

            case EffectDuration.IMMEDIATE:
                self._resolve_immediate(source_player, target_player, card, effect,)

            case EffectDuration.WHILE_IN_PLAY:
                self._resolve_persistent(source_player, target_player, card, effect,)

    def _resolve_immediate(self, source_player: Player, target_player: Player, card: Card, effect: Effect,) -> None:

        self._execute_effect(source_player, target_player, card, effect,)

        self.resolved_effects.add(effect)

    def _resolve_persistent(self, source_player: Player, target_player: Player, card: Card, effect: Effect,) -> None:

        self._execute_effect(source_player, target_player, card, effect,)

    def _check_conditions(self, player: Player, card: Card, effect: Effect,) -> bool:
        """
        Determine whether an Effect's Conditions are satisfied.
        """

        condition = effect.condition

        if condition is None:
            return True

        match condition.attribute:

            case ConditionAttribute.BASE_RANK:
                current = card.get_rank()

            case ConditionAttribute.HEALTH:
                current = card.get_health()

            case ConditionAttribute.SUIT:
                current = card.get_suit()

            case ConditionAttribute.HAND_SIZE:
                current = player.hand_size

            case ConditionAttribute.PLAYER_HP:
                current = player.health

            case ConditionAttribute.OPPONENT_HP:
                # V2
                return False

            case _:
                raise ValueError(
                    f"Unsupported condition attribute: {condition.attribute}"
                )

        match condition.comparison:

            case Comparison.EQUAL:
                return current == condition.value

            case Comparison.NOT_EQUAL:
                return current != condition.value

            case Comparison.LESS_THAN:
                return current < condition.value

            case Comparison.GREATER_THAN:
                return current > condition.value

            case Comparison.LESS_EQUAL:
                return current <= condition.value

            case Comparison.GREATER_EQUAL:
                return current >= condition.value

            case _:
                raise ValueError(
                    f"Unsupported comparison: {condition.comparison}"
                )

    def _get_target_player(self, source_player: Player, target_player: Player, effect: Effect,) -> Player:
        """
        Determine which Player an Effect should target.
        """

        match effect.target:

            case Target.SELF:
                return source_player

            case Target.OPPONENT:
                return target_player

            case _:
                raise ValueError(
                    f"Unsupported target: {effect.target}"
                )

    def _execute_effect(self, source_player: Player, target_player: Player, card: Card, effect: Effect,) -> None:
        """
        Execute an Effect.
        """

        player = self._get_target_player(source_player, target_player, effect,)

        match effect.effect_type:

            case EffectType.HEAL:
                player.heal(effect.value)

            case EffectType.DRAW_CARD:
                player.draw_cards(effect.value)

            case EffectType.RANK_UP:
                card.increase_rank(effect.value)

            case EffectType.SEARCH_DECK:
                cards = player.deck.search(effect.search_criteria)
                player.add_to_hand(cards)

            case EffectType.STUN:
                player.actions = 0

            case _:
                raise ValueError(
                    f"Unsupported effect type: {effect.effect_type}"
                )

    def reset_turn(self) -> None:
        """
        Clear all runtime state that lasts for a single turn.
        """
        self.resolved_effects.clear()