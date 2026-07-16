from engines.game_engine import GameEngine

from models.card import Card
from models.player import Player

from services.deck_service import DeckService
from services.shop_services import ShopService

from templates.ai_deck import create_ai_deck


class GameService:
    """
    Responsible for orchestrating runtime games.

    Responsibilities
    ----------------
    - Reconstruct the User's runtime Deck.
    - Construct the default runtime AI Deck.
    - Create GameEngine instances.
    - Manage active games.
    - Process gameplay.
    - Award post-game rewards.

    The GameService coordinates persistence services to
    reconstruct runtime objects required by the GameEngine.

    The GameService never directly interacts with database
    models.
    """

    WIN_REWARD = 1000

    _active_games: dict[int, GameEngine] = {}
    _completed_game_states: dict[int, dict] = {}

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
    ) -> None:
        """
        Create a new runtime game for the authenticated User.

        The User's Deck is reconstructed from the database while
        the AI always receives the default runtime Deck.
        """

        user_deck = self.deck_service.get_deck(
            user_deck_id,
        )

        ai_deck = create_ai_deck()

        engine = GameEngine()

        engine.initialize_game(
            user_deck,
            ai_deck,
        )

        self._active_games[user_id] = engine
        self._completed_game_states.pop(
            user_id,
            None,
        )

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

        The GameEngine executes the remainder of the turn,
        including the AI's move.
        """

        engine = self.get_game(
            user_id,
        )

        engine.play_turn(
            hand_index,
        )

        if engine.game_over:
            self._completed_game_states[user_id] = self._build_game_state(
                engine,
            )

            self.end_game(
                user_id,
            )

        return engine

    def get_game_state(
        self,
        user_id: int,
    ) -> dict:
        """
        Retrieve the serialized state for the authenticated User's game.
        """

        engine = self._active_games.get(
            user_id,
        )

        if engine is not None:
            return self._build_game_state(
                engine,
            )

        completed_state = self._completed_game_states.pop(
            user_id,
            None,
        )

        if completed_state is not None:
            return completed_state

        raise ValueError(
            "No active game."
        )

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

    def _build_game_state(
        self,
        engine: GameEngine,
    ) -> dict:
        winner = None

        if engine.winner == engine.user:
            winner = "USER"

        elif engine.winner == engine.ai:
            winner = "AI"

        return {
            "turn_number": engine.turn_number,
            "game_over": engine.game_over,
            "winner": winner,
            "user": self._build_user_state(
                engine.user,
            ),
            "ai": self._build_ai_state(
                engine.ai,
            ),
        }

    def _build_user_state(
        self,
        player: Player,
    ) -> dict:
        return {
            "hp": player.health,
            "deck_size": player.deck.deck_size,
            "hand": self._build_cards(
                player.hand,
                100000,
            ),
            "field": self._build_cards(
                player.field.cards,
                200000,
            ),
            "graveyard": self._build_cards(
                player.graveyard.grave,
                300000,
            ),
        }

    def _build_ai_state(
        self,
        player: Player,
    ) -> dict:
        return {
            "hp": player.health,
            "deck_size": player.deck.deck_size,
            "hand_size": player.hand_size,
            "field": self._build_cards(
                player.field.cards,
                400000,
            ),
            "graveyard": self._build_cards(
                player.graveyard.grave,
                500000,
            ),
        }

    def _build_cards(
        self,
        cards: list[Card],
        fallback_start: int,
    ) -> list[dict]:
        return [
            self._build_card(
                card,
                fallback_start + index,
            )
            for index, card in enumerate(cards)
        ]

    def _build_card(
        self,
        card: Card,
        fallback_id: int,
    ) -> dict:
        return {
            "card_id": card.card_id or fallback_id,
            "suit": card.get_suit().name,
            "rank": card.get_rank(),
            "health": card.get_health(),
            "effects": [
                getattr(
                    effect,
                    "effect_key",
                    effect.effect_type.name.lower(),
                )
                for effect in card.get_effects()
            ],
        }
