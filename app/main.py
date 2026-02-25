from fastapi import FastAPI
from app.database import Base, engine
from app.routers import pokemons

from contextlib import asynccontextmanager
from app.cache.redis_client import create_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = create_redis_client()
    try:
        yield
    finally:
        await app.state.redis.aclose()

app = FastAPI(
    title="API de Pokémons",
    description="Uma API para gerenciar pokémons usando dados da PokeAPI",
    version="1.0.0",
    contact={
        "name": "Paulo Henrique",
        "email": "paulo.souzarocha27@gmail.com",
    },
    lifespan=lifespan
)

Base.metadata.create_all(bind=engine)

app.include_router(pokemons.router)