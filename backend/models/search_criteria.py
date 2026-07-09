from enums.effect_type import EffectType
from enums.rank import Rank
from enums.suit import Suit

"""
SearchCriteria Model

Represents the search parameters used when searching a Deck
for matching Card objects.

A SearchCriteria object does not perform the search itself.
Instead, it simply describes what characteristics a Card
must have in order to be considered a match.

Any attribute left as None is ignored during the search.

Required Attributes
-------------------
None.

All search parameters are optional.

Optional Attributes
-------------------
- rank
    Match cards with the specified Rank.

- suit
    Match cards with the specified Suit.

- effect
    Match cards containing the specified EffectType.
"""

"""
SearchCriteria Responsibilities
-------------------------------
A SearchCriteria object is responsible for:

- Storing search parameters.
- Describing what constitutes a matching Card.

A SearchCriteria object is NOT responsible for:

- Searching a Deck.
- Removing cards from a Deck.
- Returning search results.
- Modifying Card objects.

Example
-------
criteria = SearchCriteria(
    rank=Rank.KING,
    suit=Suit.HEARTS
)

This describes the search:

"Find all King of Hearts cards."
"""

class SearchCriteria:

    def __init__(self, rank: Rank | None = None, suit: Suit | None = None, effect: EffectType | None = None,):
        self.rank = rank
        self.suit = suit
        self.effect = effect