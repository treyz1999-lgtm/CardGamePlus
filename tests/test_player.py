from models import Card
from models import Graveyard
from models import SearchCriteria

from enums import Rank
from enums import Suit


# --------------------------------------------------
# Test Setup
# --------------------------------------------------

king_hearts = Card(Suit.HEARTS, Rank.KING)
king_spades = Card(Suit.SPADES, Rank.KING)
queen_hearts = Card(Suit.HEARTS, Rank.QUEEN)
ace_clubs = Card(Suit.CLUBS, Rank.ACE)

graveyard = Graveyard()


# --------------------------------------------------
# Initialization
# --------------------------------------------------

assert graveyard.size == 0, "New graveyard should be empty."


# --------------------------------------------------
# add_cards
# --------------------------------------------------

graveyard.add_cards([
    king_hearts,
    king_spades,
    queen_hearts,
    ace_clubs
])

assert graveyard.size == 4, "Graveyard should contain four cards."


# --------------------------------------------------
# contains
# --------------------------------------------------

assert graveyard.contains(king_hearts), "King of Hearts should exist in the graveyard."
assert not graveyard.contains(Card(Suit.HEARTS, Rank.TWO)), "Two of Hearts should not exist."


# --------------------------------------------------
# remove_card
# --------------------------------------------------

removed = graveyard.remove_card(queen_hearts)

assert removed == queen_hearts, "remove_card() should return the removed card."
assert graveyard.size == 3, "Graveyard should contain three cards."
assert not graveyard.contains(queen_hearts), "Queen of Hearts should no longer be present."


# --------------------------------------------------
# search by rank
# --------------------------------------------------

criteria = SearchCriteria(rank=Rank.KING)

results = graveyard.search(criteria)

assert len(results) == 2, "Should find both Kings."


# --------------------------------------------------
# search by suit
# --------------------------------------------------

criteria = SearchCriteria(suit=Suit.HEARTS)

results = graveyard.search(criteria)

assert len(results) == 1, "Only King of Hearts should remain."


# --------------------------------------------------
# search by multiple criteria
# --------------------------------------------------

criteria = SearchCriteria(
    rank=Rank.KING,
    suit=Suit.SPADES
)

results = graveyard.search(criteria)

assert len(results) == 1, "Should find only the King of Spades."
assert results[0] == king_spades, "Returned card should be the King of Spades."


print("All Graveyard tests passed!")