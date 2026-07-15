from pydantic import BaseModel
from pydantic import Field

from schemas.card import CardResponse


class StartGameRequest(BaseModel):
    """
    Request to begin a new game.
    """

    deck_id: int = Field(
        ge=1,
        description="Deck to use for the new game.",
        examples=[1],
    )


class StartGameResponse(BaseModel):
    """
    Response returned after starting a new game.
    """

    message: str = Field(
        description="Confirmation that the game has started successfully.",
        examples=["Game started successfully."],
    )


class PlayCardRequest(BaseModel):
    """
    Request to play a Card from the User's hand.
    """

    hand_index: int = Field(
        ge=0,
        description="Index of the Card in the User's hand.",
        examples=[0],
    )


class PlayerStateResponse(BaseModel):
    """
    Runtime state of a Player.
    """

    hp: int = Field(
        ge=0,
        description="Current Player health.",
        examples=[20],
    )

    deck_size: int = Field(
        ge=0,
        description="Number of Cards remaining in the Deck.",
        examples=[17],
    )

    hand: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently in the Player's hand.",
    )

    field: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently on the battlefield.",
    )

    graveyard: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently in the graveyard.",
    )


class GameStateResponse(BaseModel):
    """
    Current runtime game state.
    """

    turn_number: int = Field(
        ge=1,
        description="Current turn number.",
        examples=[3],
    )

    game_over: bool = Field(
        description="Whether the game has ended.",
        examples=[False],
    )

    user: PlayerStateResponse

    ai: PlayerStateResponse


class EndGameResponse(BaseModel):
    """
    Response returned after ending a game.
    """

    message: str = Field(
        description="Confirmation that the game has ended.",
        examples=["Game ended successfully."],
    )