from models.card import Card
from models.deck import Deck
from models.effect import Effect
from models.search_criteria import SearchCriteria

from enums.rank import Rank
from enums.suit import Suit
from enums.target import Target
from enums.trigger import Trigger
from enums.effect_type import EffectType
from enums.effect_duration import EffectDuration


# --------------------------------------------------
# Test Setup
# --------------------------------------------------

heal_effect = Effect(
    effect_type=EffectType.HEAL,
    trigger=Trigger.ON_PLAY,
    target=Target.SELF,
    value=2,
    duration=EffectDuration.IMMEDIATE
)

king_hearts = Card(Suit.HEARTS, Rank.KING)
king_spades = Card(Suit.SPADES, Rank.KING)
queen_hearts = Card(Suit.HEARTS, Rank.QUEEN)
ace_clubs = Card(Suit.CLUBS, Rank.ACE)

healer = Card(
    Suit.DIAMONDS,
    Rank.FIVE,
    effects=[heal_effect]
)

cards = [
    king_hearts,
    king_spades,
    queen_hearts,
    ace_clubs,
    healer
]

deck = Deck(cards)


# --------------------------------------------------
# deck_size
# --------------------------------------------------

print("Deck Size")
print(deck.deck_size == 5)


# --------------------------------------------------
# is_valid
# --------------------------------------------------

print("\nDeck Validation")

valid_deck = Deck(cards * 8)      # 40 cards
invalid_deck = Deck(cards)        # 5 cards

print(valid_deck.is_valid)
print(invalid_deck.is_valid)


# --------------------------------------------------
# contains
# --------------------------------------------------

print("\nContains")

print(deck.contains(king_hearts))                      # True
print(deck.contains(Card(Suit.HEARTS, Rank.KING)))     # False


# --------------------------------------------------
# peek
# --------------------------------------------------

print("\nPeek")

peeked = deck.peek(3)

print(len(peeked) == 3)
print(deck.deck_size == 5)      # ensure nothing removed


# --------------------------------------------------
# draw
# --------------------------------------------------

print("\nDraw")

drawn = deck.draw(2)

print(len(drawn) == 2)
print(deck.deck_size == 3)

"""deck.draw has drawn and thus removed the top two cards which will cause the next test to be inaccurate so we will add this two cards back in"""
deck.add_cards(drawn)

print('\nCards in deck by this point')
for card in deck.cards:
    print(card)


# --------------------------------------------------
# search by rank
# --------------------------------------------------

print("\nSearch Rank")

criteria = SearchCriteria(rank=Rank.KING)

results = deck.search(criteria)

print(len(results) == 2)


# --------------------------------------------------
# search by suit
# --------------------------------------------------

print("\nSearch Suit")

criteria = SearchCriteria(suit=Suit.HEARTS)

results = deck.search(criteria)

print(len(results) == 2)


# --------------------------------------------------
# search by effect
# --------------------------------------------------

print("\nSearch Effect")

criteria = SearchCriteria(effect=EffectType.HEAL)

results = deck.search(criteria)

print(len(results) == 1)
print(results[0].rank == Rank.FIVE)


# --------------------------------------------------
# search by multiple criteria
# --------------------------------------------------

print("\nSearch Rank + Suit")

criteria = SearchCriteria(
    rank=Rank.KING,
    suit=Suit.HEARTS
)

results = deck.search(criteria)

print(len(results) == 1)
print(results[0] == king_hearts)

# --------------------------------------------------
# search for card not in deck
# --------------------------------------------------
print("\nSearch for card not in deck")
criteria = SearchCriteria(
    rank=Rank.TWO,
    suit=Suit.JOKER
)

results = deck.search(criteria)

print(len(results) == 0)#this might be a bit confusing but this should return true because the card is not in the deck so the results are empty

# --------------------------------------------------
# remove_card
# --------------------------------------------------

print("\nRemove Card")

removed = deck.remove_card(queen_hearts)

print(removed == queen_hearts)
print(deck.deck_size == 4)
print(not deck.contains(queen_hearts))