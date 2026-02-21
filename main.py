from fastapi import FastAPI
from database import Base, engine
from routers import pokemons

app = FastAPI(
    title="API de Pokémons",
    description="Uma API para gerenciar pokémons usando dados da PokeAPI",
    version="1.0.0",
    contact={
        "name": "Paulo Henrique",
        "email": "paulo.souzarocha27@gmail.com",
    },
)

Base.metadata.create_all(bind=engine)

app.include_router(pokemons.router)