from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.database import get_db
from database.models.user_model import UserModel

from dependencies.auth import get_current_user

from schemas.game import (
    StartGameRequest,
    StartGameResponse,
    PlayCardRequest,
    GameStateResponse,
)

from services.user_service import UserService
from services.shop_services import ShopService
from services.effect_service import EffectService
from services.card_service import CardService
from services.deck_service import DeckService
from services.game_service import GameService


router = APIRouter(
    prefix="/game",
    tags=["Game"],
)


def get_game_service(
    session: Session,
) -> GameService:
    """
    Construct a GameService and its dependencies.
    """

    user_service = UserService(session)

    shop_service = ShopService(
        session,
        user_service,
    )

    effect_service = EffectService(session)

    card_service = CardService(
        session,
        effect_service,
        shop_service,
    )

    deck_service = DeckService(
        session,
        card_service,
    )

    return GameService(
        deck_service,
        shop_service,
    )


@router.post(
    "/start",
    response_model=StartGameResponse,
)
def start_game(
    request: StartGameRequest,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> StartGameResponse:
    """
    Start a new game.
    """

    game_service = get_game_service(session)

    #
    # V1:
    # AI always uses Deck 1.
    #
    ai_deck_id = 1

    game_service.start_game(
        current_user.user_id,
        request.deck_id,
        ai_deck_id,
    )

    return StartGameResponse(
        message="Game started successfully.",
    )


@router.post(
    "/play",
    response_model=GameStateResponse,
)
def play_card(
    request: PlayCardRequest,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> GameStateResponse:
    """
    Play a Card from the User's hand.
    """

    game_service = get_game_service(session)

    game_service.play_card(
        current_user.user_id,
        request.hand_index,
    )

    return game_service.get_game_state(
        current_user.user_id,
    )


@router.get(
    "/state",
    response_model=GameStateResponse,
)
def get_game_state(
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> GameStateResponse:
    """
    Retrieve the current game state.
    """

    game_service = get_game_service(session)

    return game_service.get_game_state(
        current_user.user_id,
    )