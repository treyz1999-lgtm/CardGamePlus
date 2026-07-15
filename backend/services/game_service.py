from engines.game_engine import GameEngine

from services.deck_service import DeckService
from services.shop_services import ShopService


class GameService:
    """
    Responsible for orchestrating runtime games.

    Responsibilities
    ----------------
    - Reconstruct runtime Decks.
    - Create GameEngine instances.
    - Manage active games.
    - Process gameplay.
    - End games and award rewards.

    The GameService coordinates persistence services to
    reconstruct runtime objects required by the GameEngine.

    The GameService never directly interacts with database
    models.
    """

    WIN_REWARD = 1000

    _active_games: dict[int, GameEngine] = {}

    def __init__(
        self,
        deck_service: DeckService,
        shop_service: ShopService,
    ):
        self.deck_service = deck_service
        self.shop_service = shop_service

    def start_game(
        self,
        user_id: int,
        user_deck_id: int,
        ai_deck_id: int,
    ) -> None:
        """
        Create a new runtime game for the authenticated User.
        """

        user_deck = self.deck_service.get_deck(
            user_deck_id,
        )

        ai_deck = self.deck_service.get_deck(
            ai_deck_id,
        )

        engine = GameEngine()

        engine.initialize_game(
            user_deck,
            ai_deck,
        )

        self._active_games[user_id] = engine

    def get_game(
        self,
        user_id: int,
    ) -> GameEngine:
        """
        Retrieve the authenticated User's active game.
        """

        engine = self._active_games.get(
            user_id,
        )

        if engine is None:
            raise ValueError(
                "No active game."
            )

        return engine

    def play_card(
        self,
        user_id: int,
        hand_index: int,
    ) -> GameEngine:
        """
        Play a Card from the User's hand.
        """

        engine = self.get_game(
            user_id,
        )

        engine.play_turn(
            hand_index,
        )

        if engine.game_over:
            self.end_game(
                user_id,
            )

        return engine

    def end_game(
        self,
        user_id: int,
    ) -> None:
        """
        Finish the active game and award post-game rewards.
        """

        engine = self.get_game(
            user_id,
        )

        if engine.winner == engine.user:

            self.shop_service.add_gold(
                user_id,
                self.WIN_REWARD,
            )

        self._active_games.pop(
            user_id,
            None,
        )