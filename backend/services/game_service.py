import uuid

from engines.game_engine import GameEngine

from services.deck_service import DeckService
from services.shop_services import ShopService


class GameService:
    """
    Game Service

    Responsible for orchestrating runtime games.

    Responsibilities
    ----------------
    - Reconstruct runtime Decks.
    - Create GameEngine instances.
    - Manage active games.
    - Process player actions.
    - End games and award rewards.

    The GameService coordinates the persistence services to
    reconstruct runtime objects required by the GameEngine.

    The GameService never directly interacts with database
    models.
    """

    def __init__(
        self,
        deck_service: DeckService,
        shop_service: ShopService,
    ):
        self.deck_service = deck_service
        self.shop_service = shop_service

        # Active runtime games.
        self.active_games: dict[str, GameEngine] = {}

    def start_game(
        self,
        user_deck_id: int,
        ai_deck_id: int,
    ) -> str:
        """
        Create a new runtime game.

        Returns
        -------
        The generated game identifier.
        """

        user_deck = self.deck_service.get_deck(
            user_deck_id
        )

        ai_deck = self.deck_service.get_deck(
            ai_deck_id
        )

        engine = GameEngine()

        engine.initialize_match(
            user_deck,
            ai_deck,
        )

        game_id = str(uuid.uuid4())

        self.active_games[game_id] = engine

        return game_id

    def get_game(
        self,
        game_id: str,
    ) -> GameEngine:
        """
        Retrieve an active runtime game.
        """

        engine = self.active_games.get(game_id)

        if engine is None:
            raise ValueError(
                "Game not found."
            )

        return engine

    def process_action(
        self,
        game_id: str,
        action: dict,
    ) -> GameEngine:
        """
        Process a frontend action.

        The router will deserialize the incoming JSON payload
        and pass it here. This method will dispatch the action
        to the appropriate GameEngine method.

        V1 implementation is intentionally left minimal until
        the API payloads are finalized.
        """

        engine = self.get_game(game_id)

        #
        # Examples:
        #
        # engine.play_phase(...)
        # engine.combat_phase(...)
        # engine.end_turn(...)
        #

        return engine

    def end_game(
        self,
        game_id: str,
        winner_user_id: int,
        gold_reward: int,
    ) -> None:
        """
        Finish a game and award post-game rewards.
        """

        self.shop_service.add_gold(
            winner_user_id,
            gold_reward,
        )

        self.active_games.pop(
            game_id,
            None,
        )