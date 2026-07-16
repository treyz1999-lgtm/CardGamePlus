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


class UserStateResponse(BaseModel):
    """
    Runtime state of the authenticated User.
    """

    hp: int = Field(
        ge=0,
        description="Current User health.",
        examples=[20],
    )

    deck_size: int = Field(
        ge=0,
        description="Number of Cards remaining in the User's Deck.",
        examples=[17],
    )

    hand: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently in the User's hand.",
    )

    field: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently on the battlefield.",
    )

    graveyard: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently in the User's graveyard.",
    )


class AIStateResponse(BaseModel):
    """
    Runtime state of the AI opponent.

    The contents of the AI's hand remain hidden from the User.
    Only the number of Cards in the AI's hand is exposed.
    """

    hp: int = Field(
        ge=0,
        description="Current AI health.",
        examples=[20],
    )

    deck_size: int = Field(
        ge=0,
        description="Number of Cards remaining in the AI Deck.",
        examples=[17],
    )

    hand_size: int = Field(
        ge=0,
        description="Number of Cards currently in the AI's hand.",
        examples=[4],
    )

    field: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently on the battlefield.",
    )

    graveyard: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently in the AI's graveyard.",
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

    winner: str | None = Field(
        default=None,
        description="Winner of the game once it has concluded.",
        examples=["USER"],
    )

    user: UserStateResponse

    ai: AIStateResponse


class EndGameResponse(BaseModel):
    """
    Response returned after ending a game.
    """

    message: str = Field(
        description="Confirmation that the game has ended.",
        examples=["Game ended successfully."],
    )