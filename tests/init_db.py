from database.base import Base
from database.database import engine

# Import every model so SQLAlchemy knows about them
from database.models.user_model import UserModel
from database.models.card_model import CardModel
from database.models.effect_model import EffectModel
from database.models.condition_model import ConditionModel
from database.models.search_model import SearchCriteriaModel
from database.models.deck_model import DeckModel
from database.models.deck_card_model import DeckCardModel
from database.models.Owned_Effect_Model import OwnedEffectModel


def init_db():

    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")