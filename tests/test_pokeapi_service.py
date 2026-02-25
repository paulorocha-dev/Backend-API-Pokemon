import pytest
import respx
from httpx import Response
import fakeredis.aioredis as fakeredis_async

from app.services.pokeapi import fetch_pokemon_raw_from_api, POKEAPI_BASE_URL


@pytest.mark.asyncio
@respx.mock
async def test_fetch_pokemon_raw_caches_result():
    redis = fakeredis_async.FakeRedis(decode_responses=True)

    respx.get(f"{POKEAPI_BASE_URL}/pokemon/pikachu").mock(
        return_value=Response(
            200,
            json={
                "id": 25,
                "name": "pikachu",
                "height": 4,
                "weight": 60,
                "base_experience": 112,
                "types": [],
                "sprites": {"front_default": None, "back_default": None},
            },
        )
    )

    data1 = await fetch_pokemon_raw_from_api(redis, "pikachu")
    data2 = await fetch_pokemon_raw_from_api(redis, "pikachu")

    assert data1["name"] == "pikachu"
    assert data2["id"] == 25

    await redis.aclose()