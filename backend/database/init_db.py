from database.base import Base
from database.database import engine

# Import every model so SQLAlchemy knows about them
from database.models.user_model import UserModel
from database.models.card_model import CardModel


def init_db():

    Base.metadata.create_all(bind=engine)