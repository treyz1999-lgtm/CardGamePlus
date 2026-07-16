from models import Card
from enums import Suit
from enums import Rank


def test_card_name():

    card = Card(Suit.HEARTS, Rank.THREE)

    print(card)
    print(card.get_rank())

    assert card.name == "Three of Hearts"
    assert card.get_rank() == 3
    assert card.get_health() == 1


test_card_name()