from database.base import Base
from database import engine

# Import every model so SQLAlchemy knows about them


def init_db():

    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")