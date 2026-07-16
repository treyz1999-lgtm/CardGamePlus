from enums.trigger import Trigger

from engines.effect_engine import EffectEngine

from models.card import Card
from models.deck import Deck
from models.effect import Effect
from models.player import Player

"""
Game Engine

Coordinates a single match between two Players.

The GameEngine owns both runtime Player objects and is
responsible for executing the complete flow of a match.

Unlike the EffectEngine, the GameEngine understands gameplay
events (playing Cards, combat, death, turn progression, etc.).
When an event occurs, it identifies every Effect whose Trigger
matches that event and delegates those Effects to the
EffectEngine for resolution.

The frontend never manipulates runtime objects directly.
Instead, it simply tells the GameEngine which Card the User
wishes to play each turn.

V1 AI
-----
The AI uses a fixed runtime Deck that is recreated for every
game. The Deck is shuffled at the start of each match.

During its turn the AI always plays the first Card currently
in its Hand.

Responsibilities
----------------
- Create Player objects.
- Start a game.
- Execute complete turns.
- Coordinate gameplay phases.
- Resolve combat.
- Determine the winner.
- Delegate Effect execution.

The GameEngine never performs database operations.
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

    def start_game(
        self,
        user_deck: Deck,
        ai_deck: Deck,
    ) -> None:
        """
        Initialize a new game.
        """

        self.turn_number = 1
        self.game_over = False
        self.winner = None

        self.user = Player(user_deck)
        self.ai = Player(ai_deck)

        self.user.deck.shuffle()
        self.ai.deck.shuffle()

        self.user.draw_cards(self.STARTING_HAND_SIZE)
        self.ai.draw_cards(self.STARTING_HAND_SIZE)

    def start_turn(
        self,
        source: Player,
        target: Player,
    ) -> None:
        """
        Execute the start of a Player's turn.
        """

        source.reset_actions()
        source.draw_cards(1)

        effects = self.get_triggered_effects(
            source.field.cards,
            Trigger.TURN_START,
        )

        self.effect_engine.resolve(
            source_player=source,
            target_player=target,
            effects=effects,
        )

    def play_phase(
        self,
        source: Player,
        target: Player,
        card: Card,
    ) -> None:
        """
        Play a Card from the Player's Hand.
        """

        source.play_card(card)

        effects = self.get_triggered_effects(
            source.field.cards,
            Trigger.ON_PLAY,
        )

        self.effect_engine.resolve(
            source_player=source,
            target_player=target,
            effects=effects,
        )

    def combat_phase(
        self,
        user: Player,
        ai: Player,
    ) -> None:
        """
        Resolve combat between both Players.
        """

        user_power = user.field.combat_power
        ai_power = ai.field.combat_power

        if user_power > ai_power:
            ai.take_damage(1)

        elif ai_power > user_power:
            user.take_damage(1)

        self.check_winner()

        if self.game_over:
            return

        user_effects = self.get_triggered_effects(
            user.field.cards,
            Trigger.ON_DAMAGE,
        )

        ai_effects = self.get_triggered_effects(
            ai.field.cards,
            Trigger.ON_DAMAGE,
        )

        self.effect_engine.resolve(
            source_player=user,
            target_player=ai,
            effects=user_effects,
        )

        self.effect_engine.resolve(
            source_player=ai,
            target_player=user,
            effects=ai_effects,
        )

    def end_turn(
        self,
        user: Player,
        ai: Player,
    ) -> None:
        """
        Resolve end-of-turn gameplay.
        """

        user.field.damage_all_cards()

        effects = self.get_triggered_effects(
            user.field.defeated_cards,
            Trigger.ON_DEATH,
        )

        self.effect_engine.resolve(
            source_player=user,
            target_player=ai,
            effects=effects,
        )

        for card in user.field.defeated_cards:
            moved = user.field.remove_card_from_deck(card)
            user.graveyard.add_card_to_deck(moved)

        ai.field.damage_all_cards()

        effects = self.get_triggered_effects(
            ai.field.defeated_cards,
            Trigger.ON_DEATH,
        )

        self.effect_engine.resolve(
            source_player=ai,
            target_player=user,
            effects=effects,
        )

        for card in ai.field.defeated_cards:
            moved = ai.field.remove_card_from_deck(card)
            ai.graveyard.add_card_to_deck(moved)

        self.effect_engine.reset_turn()

    def check_winner(
        self,
    ) -> Player | None:
        """
        Determine whether either Player has won.
        """

        if not self.user.is_alive:
            self.winner = self.ai

        elif not self.ai.is_alive:
            self.winner = self.user

        self.game_over = self.winner is not None

        return self.winner

    def next_turn(
        self,
    ) -> None:
        """
        Advance to the next turn.
        """

        if not self.game_over:
            self.turn_number += 1

    def get_triggered_effects(
        self,
        cards: list[Card],
        trigger: Trigger,
    ) -> list[tuple[Card, Effect]]:
        """
        Return every (Card, Effect) pair matching the given Trigger.
        """

        triggered_effects: list[tuple[Card, Effect]] = []

        for card in cards:

            for effect in card.get_effects():

                if effect.trigger == trigger:
                    triggered_effects.append(
                        (
                            card,
                            effect,
                        )
                    )

        return triggered_effects

    def play_turn(
        self,
        hand_index: int,
    ) -> None:
        """
        Execute one complete turn.

        The frontend specifies which Card the User wishes to
        play. The GameEngine executes every remaining gameplay
        phase, including the AI turn.
        """

        if self.game_over:
            raise ValueError(
                "The game has already ended."
            )

        if hand_index < 0 or hand_index >= len(self.user.hand.cards):
            raise ValueError(
                "Invalid hand index."
            )

        #
        # User turn
        #

        user_card = self.user.hand.cards[hand_index]

        self.play_phase(
            self.user,
            self.ai,
            user_card,
        )

        #
        # V1 AI
        #
        # The AI always plays the first Card
        # currently in its Hand.
        #

        if self.ai.hand.cards:

            ai_card = self.ai.hand.cards[0]

            self.play_phase(
                self.ai,
                self.user,
                ai_card,
            )

        #
        # Combat
        #

        self.combat_phase(
            self.user,
            self.ai,
        )

        if self.game_over:
            return

        #
        # End Turn
        #

        self.end_turn(
            self.user,
            self.ai,
        )

        self.next_turn()

        self.start_turn(
            self.user,
            self.ai,
        )

        self.start_turn(
            self.ai,
            self.user,
        )

    def initialize_game(
        self,
        user_deck: Deck,
        ai_deck: Deck,
    ) -> None:
        """
        Initialize a new match and execute the opening turn.
        """

        self.start_game(
            user_deck,
            ai_deck,
        )

        self.start_turn(
            self.user,
            self.ai,
        )