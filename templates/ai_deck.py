from enums.effect_duration import EffectDuration
from enums.effect_type import EffectType
from enums.rank import Rank
from enums.suit import Suit
from enums.target import Target
from enums.trigger import Trigger

from models.card import Card
from models.deck import Deck
from models.effect import Effect

"""
AI Deck Template

Constructs the default runtime Deck used by the V1 AI.

Unlike player Decks, this Deck is never persisted to the
database. A fresh Deck is created at the start of every
game and passed directly to the GameEngine.

The AI follows a very simple strategy in V1:

- Shuffle its Deck.
- Draw its opening hand.
- Always play the first Card in its Hand.

Some Cards have attached Effects to make gameplay more
interesting, but the AI does not make decisions based on
game state.
"""


def create_ai_deck() -> Deck:
    """
    Construct the default runtime Deck used by the V1 AI.
    """

    #
    # Runtime Effects
    #

    rank_up_1 = Effect(
        effect_type=EffectType.RANK_UP,
        trigger=Trigger.ON_PLAY,
        target=Target.SELF,
        value=1,
        duration=EffectDuration.IMMEDIATE,
    )

    rank_up_2 = Effect(
        effect_type=EffectType.RANK_UP,
        trigger=Trigger.ON_PLAY,
        target=Target.SELF,
        value=2,
        duration=EffectDuration.IMMEDIATE,
    )

    heal_1 = Effect(
        effect_type=EffectType.HEAL,
        trigger=Trigger.ON_PLAY,
        target=Target.SELF,
        value=1,
        duration=EffectDuration.IMMEDIATE,
    )

    heal_2 = Effect(
        effect_type=EffectType.HEAL,
        trigger=Trigger.ON_PLAY,
        target=Target.SELF,
        value=2,
        duration=EffectDuration.IMMEDIATE,
    )

    draw_1 = Effect(
        effect_type=EffectType.DRAW_CARD,
        trigger=Trigger.ON_PLAY,
        target=Target.SELF,
        value=1,
        duration=EffectDuration.IMMEDIATE,
    )

    stun = Effect(
        effect_type=EffectType.STUN,
        trigger=Trigger.ON_DEATH,
        target=Target.OPPONENT,
        value=1,
        duration=EffectDuration.IMMEDIATE,
    )

    cards = [

        #
        # Cards with Effects
        #

        Card(
            suit=Suit.SPADES,
            rank=Rank.ACE,
            effects=[rank_up_2],
        ),

        Card(
            suit=Suit.HEARTS,
            rank=Rank.ACE,
            effects=[heal_2],
        ),

        Card(
            suit=Suit.SPADES,
            rank=Rank.KING,
            effects=[draw_1],
        ),

        Card(
            suit=Suit.HEARTS,
            rank=Rank.KING,
            effects=[rank_up_1],
        ),

        Card(
            suit=Suit.SPADES,
            rank=Rank.QUEEN,
            effects=[stun],
        ),

        Card(
            suit=Suit.HEARTS,
            rank=Rank.QUEEN,
            effects=[heal_1],
        ),

        Card(
            suit=Suit.SPADES,
            rank=Rank.JACK,
            effects=[rank_up_2],
        ),

        Card(
            suit=Suit.HEARTS,
            rank=Rank.JACK,
            effects=[draw_1],
        ),

        #
        # Standard Cards
        #

        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.CLUBS, Rank.ACE),

        Card(Suit.DIAMONDS, Rank.KING),
        Card(Suit.CLUBS, Rank.KING),

        Card(Suit.DIAMONDS, Rank.QUEEN),
        Card(Suit.CLUBS, Rank.QUEEN),

        Card(Suit.DIAMONDS, Rank.JACK),
        Card(Suit.CLUBS, Rank.JACK),

        Card(Suit.SPADES, Rank.TEN),
        Card(Suit.HEARTS, Rank.TEN),
        Card(Suit.DIAMONDS, Rank.TEN),
        Card(Suit.CLUBS, Rank.TEN),

        Card(Suit.SPADES, Rank.NINE),
        Card(Suit.HEARTS, Rank.NINE),
        Card(Suit.DIAMONDS, Rank.NINE),
        Card(Suit.CLUBS, Rank.NINE),

        Card(Suit.SPADES, Rank.EIGHT),
        Card(Suit.HEARTS, Rank.EIGHT),
        Card(Suit.DIAMONDS, Rank.EIGHT),
        Card(Suit.CLUBS, Rank.EIGHT),

        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.HEARTS, Rank.SEVEN),
        Card(Suit.DIAMONDS, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.SEVEN),

        Card(Suit.SPADES, Rank.SIX),
        Card(Suit.HEARTS, Rank.SIX),
        Card(Suit.DIAMONDS, Rank.SIX),
        Card(Suit.CLUBS, Rank.SIX),

        Card(Suit.SPADES, Rank.FIVE),
        Card(Suit.HEARTS, Rank.FIVE),
        Card(Suit.DIAMONDS, Rank.FIVE),
        Card(Suit.CLUBS, Rank.FIVE),
    ]

    return Deck(cards)