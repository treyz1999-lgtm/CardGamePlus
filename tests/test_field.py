from models import Card
from models import Field

from enums import Rank
from enums import Suit


# --------------------------------------------------
# Test Setup
# --------------------------------------------------

king = Card(Suit.HEARTS, Rank.KING)
queen = Card(Suit.CLUBS, Rank.QUEEN)
five = Card(Suit.DIAMONDS, Rank.FIVE)

field = Field()


# --------------------------------------------------
# field_size
# --------------------------------------------------

assert field.field_size == 0, "New field should be empty."


# --------------------------------------------------
# add_cards
# --------------------------------------------------

field.add_cards([king, queen, five])

assert field.field_size == 3, "Field should contain three cards after adding."


# --------------------------------------------------
# combat_power
# --------------------------------------------------

expected = (
    king.get_rank()
    + queen.get_rank()
    + five.get_rank()
)

assert field.combat_power == expected, "Combat power should equal the sum of all card ranks."


# --------------------------------------------------
# damage_all_cards
# --------------------------------------------------

field.damage_all_cards()

assert king.health == 0, "King should have 0 HP."
assert queen.health == 0, "Queen should have 0 HP."
assert five.health == 0, "Five should have 0 HP."


# --------------------------------------------------
# defeated_cards
# --------------------------------------------------

dead = field.defeated_cards()

assert len(dead) == 3, "All three cards should be defeated."


# --------------------------------------------------
# remove_card
# --------------------------------------------------

removed = field.remove_card(king)

assert removed == king, "remove_card() should return the removed card."
assert field.field_size == 2, "Field should contain two cards after removal."


print("All Field tests passed!")