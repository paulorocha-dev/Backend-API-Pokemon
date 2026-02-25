import respx
from httpx import Response

from app.services.pokeapi import POKEAPI_BASE_URL


@respx.mock
def test_list_pokemons_pagination(client):
    # Mock da listagem da PokeAPI
    respx.get(f"{POKEAPI_BASE_URL}/pokemon").mock(
        return_value=Response(
            200,
            json={
                "count": 50,
                "results": [
                    {"name": "pikachu"},
                    {"name": "bulbasaur"},
                ],
            },
        )
    )

    # Mock dos detalhes (a rota chama detail para cada item)
    respx.get(f"{POKEAPI_BASE_URL}/pokemon/pikachu").mock(
        return_value=Response(
            200,
            json={
                "id": 25,
                "name": "pikachu",
                "height": 4,
                "weight": 60,
                "types": [],
                "sprites": {"front_default": None, "back_default": None},
            },
        )
    )

    respx.get(f"{POKEAPI_BASE_URL}/pokemon/bulbasaur").mock(
        return_value=Response(
            200,
            json={
                "id": 1,
                "name": "bulbasaur",
                "height": 7,
                "weight": 69,
                "types": [],
                "sprites": {"front_default": None, "back_default": None},
            },
        )
    )

    r = client.get("/pokemons/?limit=2&offset=0")
    assert r.status_code == 200

    body = r.json()
    assert body["pagination"]["next"] == "/pokemons?limit=2&offset=2"
    assert body["pagination"]["previous"] is None