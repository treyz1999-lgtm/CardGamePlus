from enums.trigger import Trigger
from models.card import Card
from models.deck import Deck
from models.effect import Effect
from engines.effect_engine import EffectEngine
from models.player import Player

"""
Game Engine

Coordinates a single match between two players.

The GameEngine acts as the central controller of gameplay. It
does not implement the behavior of individual game objects;
instead, it orchestrates interactions between them based on
the current game state.

During a match, the GameEngine owns both Player objects and
determines the order in which gameplay phases occur. Whenever
a game event takes place, the GameEngine identifies any relevant
effects and delegates their execution to the EffectEngine.

Initialized Attributes
----------------------
- user
    The human player's Player object.

- ai
    The AI player's Player object.

- turn_number
    The current turn of the match.

- game_over
    Indicates whether the match has ended.

- winner
    The winning Player object once the game concludes.

- effect_engine
    Responsible for evaluating and executing card effects.

Game Responsibilities
---------------------
The GameEngine is responsible for:

- Creating both Player objects.
- Starting the game.
- Managing turn order.
- Running each gameplay phase.
- Coordinating card movement between game zones.
- Collecting triggered effects.
- Delegating effect execution to the EffectEngine.
- Resolving combat.
- Determining the winner.
- Ending the game.

The GameEngine is NOT responsible for:

- Executing card effects.
- Determining how individual models perform their actions.
- Managing database operations.
- Authentication.
- Building decks.
- Creating custom cards.
- Shop functionality.

Game Flow
---------
A typical match follows the sequence:

start_game()

while not game_over:

    start_turn()

    human_phase()

    ai_phase()

    combat_phase()

    end_turn()

    check_winner()

    next_turn()
"""

class GameEngine:

    STARTING_HAND_SIZE = 3

    def __init__(self):

        self.user: Player | None = None
        self.ai: Player | None = None
        #really these aren't optional, the game doesn't work without two players

        self.turn_number = 0 #turn 0 is the 'setup' turn
        self.game_over = False
        self.winner = None
        self.effect_engine = EffectEngine() #this doesn't do anything at the moment

    def start_game(self, user_deck: Deck, ai_deck: Deck): #when we actually call this function, we need to pass in these Deck objects, meaning they need to be created via a service beforehand. Serives are WIP

        self.turn_number = 1
        self.game_over = False
        self.winner = None

        self.user = Player(user_deck)
        self.ai = Player(ai_deck)
        #create the two Player objects

        self.user.deck.shuffle()
        self.ai.deck.shuffle()
        #shuffle both decks

        self.user.draw_cards(self.STARTING_HAND_SIZE)
        self.ai.draw_cards(self.STARTING_HAND_SIZE)
        #give them their starting hands

    def start_turn(self, player: Player) -> None:
        player.reset_actions()
        player.draw_cards(1)

        effects = self.get_effects(player)

        if effects:
            self.effect_engine.resolve(
                player=player,
                trigger=Trigger.TURN_START,
                effects=effects
            )

            self.effect_engine.resolve(
                player=player,
                trigger=Trigger.ON_DRAW,
                effects=effects
            )

    def play_phase(self, player: Player, card: Card) -> None:
        # The Player model validates whether the card can legally be played.
        player.play_card(card)

        effects = self.get_effects(player)

        if effects:
            self.effect_engine.resolve(
                player=player,
                trigger=Trigger.ON_PLAY,
                effects=effects
            )

            self.effect_engine.resolve(
                player=player,
                trigger=Trigger.ON_DISCARD,
                effects=effects
            )

            self.effect_engine.resolve(
                player=player,
                trigger=Trigger.ON_HEAL,
                effects=effects
            )

    def combat_phase(self):
       pass

    def end_turn(self):
        # ON_DEATH = 'On Death' -this might need to be checked at turn end instead because for V1 cards will only ever leave the field at the end of the turn
        # ON_DAMAGE = 'On Damage' - this will go to end phase because damage occurs there
       pass


    def check_winner(self):
        pass

    def next_turn(self):
        pass

    def get_effects(self, player: Player) -> list[Effect]:
        """
        Return every Effect currently owned by the player's cards.

        The GameEngine does not distinguish between immediate and
        persistent effects. It simply gathers all effects and
        delegates trigger, duration, condition, registration,
        and execution logic to the EffectEngine.
        """
        pass
