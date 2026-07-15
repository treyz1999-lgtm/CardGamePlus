from enums.trigger import Trigger

from engines.effect_engine import EffectEngine

from models.card import Card
from models.deck import Deck
from models.effect import Effect
from models.player import Player

"""
Game Engine

Coordinates a single match between two players.

The GameEngine is responsible for managing the flow of a game.
It owns both Player objects, tracks the current game state,
determines when gameplay events occur, and delegates effect
execution to the EffectEngine.

Unlike the EffectEngine, the GameEngine understands gameplay
events (such as playing a card, combat, or a card dying). When
an event occurs, it identifies every Effect whose Trigger matches
that event and passes only those Effects to the EffectEngine.

The EffectEngine is therefore responsible only for resolving
Effects—not determining when they should activate.

Initialized Attributes
----------------------
- user
    The human Player.

- ai
    The AI Player.

- turn_number
    Current turn of the match.

- game_over
    Indicates whether the match has ended.

- winner
    The winning Player once the game concludes.

- effect_engine
    Executes triggered Effects.

Game Responsibilities
---------------------
The GameEngine is responsible for:

- Creating Player objects.
- Starting a game.
- Managing turn order.
- Running each gameplay phase.
- Coordinating movement between game zones.
- Determining which Effects are triggered by each game event.
- Delegating triggered Effects to the EffectEngine.
- Resolving combat.
- Determining the winner.
- Ending the game.

The GameEngine is NOT responsible for:

- Executing Effects.
- Evaluating Effect Conditions.
- Determining Effect Targets.
- Executing individual Card behavior.
- Database operations.
- Authentication.
- Building decks.
- Shop functionality.

Game Flow
---------
Each gameplay event follows the same pipeline.

Gameplay Event
    │
    ▼
GameEngine phase executes
    │
    ├── Determine which Trigger occurred.
    ├── Collect every matching (Card, Effect) pair.
    │
    ▼
EffectEngine.resolve(...)
    │
    ├── Evaluate Conditions.
    ├── Resolve Duration.
    ├── Execute Effect.
    │
    ▼
Updated game state

Typical Turn
------------
start_turn()

↓

play_phase()

↓

combat_phase()

↓

end_turn()

↓

check_winner()

↓

next_turn()
"""

class GameEngine:

    STARTING_HAND_SIZE = 3

    def __init__(self):

        self.user: Player | None = None
        self.ai: Player | None = None

        self.turn_number = 0
        self.game_over = False
        self.winner: Player | None = None

        self.effect_engine = EffectEngine()

    def start_game(self, user_deck: Deck, ai_deck: Deck,) -> None:

        self.turn_number = 1
        self.game_over = False
        self.winner = None

        self.user = Player(user_deck)
        self.ai = Player(ai_deck)

        self.user.deck.shuffle()
        self.ai.deck.shuffle()

        self.user.draw_cards(self.STARTING_HAND_SIZE)
        self.ai.draw_cards(self.STARTING_HAND_SIZE)

    def start_turn(self,source: Player, target: Player,) -> None:

        source.reset_actions()
        source.draw_cards(1)

        effects = self.get_triggered_effects(source.field.cards, Trigger.TURN_START,)

        self.effect_engine.resolve(source_player=source, target_player=target, effects=effects,)

    def play_phase(self, source: Player, target: Player, card: Card,) -> None:

        source.play_card(card)

        effects = self.get_triggered_effects(source.field.cards, Trigger.ON_PLAY,)

        self.effect_engine.resolve(source_player=source, target_player=target, effects=effects,)

    def combat_phase(self, user: Player, ai: Player,) -> None:

        user_power = user.field.combat_power
        ai_power = ai.field.combat_power

        if user_power > ai_power:
            ai.take_damage(1)

        elif ai_power > user_power:
            user.take_damage(1)

        self.check_winner()

        if self.game_over:
            return

        user_effects = self.get_triggered_effects(user.field.cards, Trigger.ON_DAMAGE,)

        ai_effects = self.get_triggered_effects(ai.field.cards, Trigger.ON_DAMAGE,)

        self.effect_engine.resolve(source_player=user, target_player=ai, effects=user_effects,)

        self.effect_engine.resolve(source_player=ai, target_player=user, effects=ai_effects,)

    def end_turn(self, user: Player, ai: Player,) -> None:

        user.field.damage_all_cards()

        effects = self.get_triggered_effects(user.field.defeated_cards, Trigger.ON_DEATH,)

        self.effect_engine.resolve(source_player=user, target_player=ai, effects=effects,)

        for card in user.field.defeated_cards:
            moved = user.field.remove_card_from_deck(card)
            user.graveyard.add_card_to_deck(moved)

        ai.field.damage_all_cards()

        effects = self.get_triggered_effects(ai.field.defeated_cards, Trigger.ON_DEATH,)

        self.effect_engine.resolve(source_player=ai, target_player=user, effects=effects,)

        for card in ai.field.defeated_cards:
            moved = ai.field.remove_card_from_deck(card)
            ai.graveyard.add_card_to_deck(moved)

        self.effect_engine.reset_turn()

    def check_winner(self) -> Player | None:

        if not self.user.is_alive:
            self.winner = self.ai

        elif not self.ai.is_alive:
            self.winner = self.user

        self.game_over = self.winner is not None

        return self.winner

    def next_turn(self) -> None:

        if not self.game_over:
            self.turn_number += 1

    def get_triggered_effects(self, cards: list[Card], trigger: Trigger,) -> list[tuple[Card, Effect]]:
        """
        Return every (Card, Effect) pair matching the given Trigger.
        """

        triggered_effects: list[tuple[Card, Effect]] = []

        for card in cards:

            for effect in card.get_effects():

                if effect.trigger == trigger:
                    triggered_effects.append((card, effect))

        return triggered_effects

    def initialize_match(
            self,
            user_deck,
            ai_deck,
    ):
        self.start_game(user_deck, ai_deck)
        self.start_turn(self.user, self.ai)