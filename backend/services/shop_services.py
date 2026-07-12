from enums.rank import Rank

RANK_COST = { #this dict will store the gold value for a card based on their rank - this probably shouldn't be in this file; I will move it to the shop service when its time
    Rank.JOKER: 1500,
    Rank.ACE: 1400,
    Rank.KING: 1300,
    Rank.QUEEN: 1200,
    Rank.JACK: 1100,
    Rank.TEN: 1000,
    Rank.NINE: 900,
    Rank.EIGHT: 800,
    Rank.SEVEN: 700,
    Rank.SIX: 600,
    Rank.FIVE: 500,
    Rank.FOUR: 400,
    Rank.THREE: 300,
    Rank.TWO: 200,
}