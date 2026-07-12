from enums.condition import ConditionAttribute, Comparison
from enums.effect_duration import EffectDuration
from enums.effect_type import EffectType
from enums.target import Target

from models.card import Card
from models.effect import Effect
from models.player import Player

"""
Effect Engine

Responsible for resolving every Effect currently active on a
Player's Field.

The EffectEngine does not determine when effects should be
resolved. Instead, the GameEngine invokes this engine whenever
a gameplay event occurs (such as the start of a turn, after a
card is played, or at the end of a turn).

The GameEngine supplies:

- The Player whose Effects are being resolved.
- That Player's opponent.
- The Cards currently on the source Player's Field.

The EffectEngine is responsible only for determining whether
those Effects should activate and how they modify the game state.

Pipeline
--------
The EffectEngine resolves effects using the following pipeline:

resolve(source_player, target_player, field.cards)
    │
    ├── Iterate through every Card on the source Player's Field.
    │
    ▼
_resolve_card(source_player, target_player, card)
    │
    ├── Retrieve every Effect attached to the Card.
    │
    ▼
_resolve_effect(source_player, target_player, card, effect)
    │
    ├── Skip already resolved immediate Effects.
    ├── Evaluate any Conditions.
    ├── Determine the EffectDuration.
    │
    ▼
_resolve_immediate()
        or
_resolve_persistent()
    │
    ├── Route the Effect to the appropriate target.
    ├── Execute the Effect.
    │
    ▼
_execute_effect()
    │
    ├── Resolve the Effect's Target.
    ├── Execute the EffectType.
    │
    ▼
Player / Card / Deck updated

Responsibilities
----------------
The EffectEngine is responsible for:

- Resolving Effects attached to Cards.
- Evaluating Effect Conditions.
- Determining Effect Targets.
- Tracking immediate Effects already resolved this turn.
- Executing gameplay logic associated with each EffectType.

The EffectEngine is NOT responsible for:

- Managing turn order.
- Determining when effects should be checked.
- Combat resolution.
- Moving cards between game zones.
- Creating Players or Cards.
- Database operations.
- Authentication.
"""

class EffectEngine:
    """
    Resolves all card effects currently active on a player's field.
    """

    def __init__(self):
        self.resolved_effects: set[Effect] = set()

    def resolve(self, source_player: Player, target_player: Player, cards: list[Card],) -> None:
        """
        Resolve every Card currently on the source Player's field.
        """
        for card in cards:
            self._resolve_card(source_player, target_player, card)

    def _resolve_card(self, source_player: Player, target_player: Player, card: Card,) -> None:
        """
        Resolve every Effect attached to a Card.
        """
        for effect in card.get_effects():
            self._resolve_effect( source_player, target_player, card, effect,)

    def _resolve_effect(self, source_player: Player, target_player: Player, card: Card, effect: Effect,) -> None:

        if effect in self.resolved_effects:
            return

        if not self._check_conditions(source_player, card, effect):
            return

        match effect.duration:

            case EffectDuration.IMMEDIATE:
                self._resolve_immediate(source_player, target_player, card, effect,)

            case EffectDuration.WHILE_IN_PLAY:
                self._resolve_persistent(source_player, target_player, card, effect,)

    def _resolve_immediate(self, source_player: Player, target_player: Player, card: Card, effect: Effect,) -> None:

        self._execute_effect(source_player, target_player, card, effect,)

        self.resolved_effects.add(effect)

    def _resolve_persistent(self,source_player: Player, target_player: Player, card: Card, effect: Effect,) -> None:

        self._execute_effect(source_player, target_player, card, effect,)

    def _check_conditions(self, player: Player, card: Card, effect: Effect,) -> bool:
        """
        Determine whether an Effect's conditions are satisfied.
        """
        condition = effect.condition #we need to get the Condition object from the Effect

        if condition is None: # Effects without a Condition always resolve.
            return True

        match condition.attribute:

            case ConditionAttribute.BASE_RANK:
                current = card.get_rank()

            case ConditionAttribute.HEALTH:
                current = card.get_health()

            case ConditionAttribute.SUIT:
                current = card.get_suit()

            case ConditionAttribute.HAND_SIZE:
                current = player.hand_size #this is a property of the Player class

            case ConditionAttribute.PLAYER_HP:
                current = player.health

            case ConditionAttribute.OPPONENT_HP:
                # WIP for now -this is not in V1, but we would need to pass in both Players and then use the get_target to determine how this effect is about and have a branch for each option
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
        Execute an Effect based on its EffectType.
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