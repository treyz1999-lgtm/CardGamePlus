from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from database.base import Base
from database.database import engine

from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.shop_router import router as shop_router
from routers.card_router import router as card_router
from routers.deck_router import router as deck_router
from routers.game_router import router as game_router

"""
Application Entry Point

Responsibilities
----------------
- Configure the FastAPI application.
- Configure middleware.
- Initialize the database.
- Register API routers.

Business logic belongs in the service layer.
Gameplay logic belongs in the GameEngine.
"""


app = FastAPI(
    title="Card Game API",
    description="Backend API for the customizable card game.",
    version="1.0.0",
)


#
# Allow the frontend to communicate with the API.
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://card-game-plus.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#
# Create database tables.
#
Base.metadata.create_all(
    bind=engine,
)


#
# Register API routers.
#
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(shop_router)
app.include_router(card_router)
app.include_router(deck_router)
app.include_router(game_router)


@app.get(
    "/",
    tags=["Health"],
)
def health_check():
    """
    Verify that the API is running.
    """

    return {
        "status": "ok",
        "message": "Card Game API is running.",
    }