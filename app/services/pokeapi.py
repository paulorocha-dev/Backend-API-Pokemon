# Criar pokémons no banco a partir da API

import httpx
from fastapi import HTTPException
from redis.asyncio.client import Redis
from app.cache.cache_helpers import get_or_set_json

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"

async def fetch_pokemons_from_api(
    redis: Redis,
    limit: int = 20,
    offset: int = 0
) -> dict:
    key = f"pokeapi:pokemon:list:{limit}:{offset}"
    ttl = 60  
    
    async def factory():
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{POKEAPI_BASE_URL}/pokemon",
                params={"limit": limit, "offset": offset},
            )

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao acessar a PokeAPI")

        return response.json()

    return await get_or_set_json(redis, key, ttl, factory)


async def fetch_pokemon_raw_from_api(
    redis: Redis,
    name_or_id: str | int
) -> dict:
    key = f"pokeapi:pokemon:raw:{str(name_or_id).lower()}"
    ttl = 60 * 60  # 1 hora

    async def factory():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{POKEAPI_BASE_URL}/pokemon/{name_or_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Pokémon não encontrado")

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao acessar a PokeAPI")

        return response.json()

    return await get_or_set_json(redis, key, ttl, factory)


async def fetch_pokemon_for_db(redis: Redis, name_or_id: str | int) -> dict:
    data = await fetch_pokemon_raw_from_api(redis, name_or_id)
    return {
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "base_experience": data["base_experience"],
    }