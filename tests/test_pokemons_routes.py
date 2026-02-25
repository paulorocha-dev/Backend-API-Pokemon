import respx
from httpx import Response
from app.services.pokeapi import POKEAPI_BASE_URL


@respx.mock
def test_get_pokemon_route_returns_mapped_detail(client):
    respx.get(f"{POKEAPI_BASE_URL}/pokemon/pikachu").mock(
        return_value=Response(
            200,
            json={
                "id": 25,
                "name": "pikachu",
                "height": 4,
                "weight": 60,
                "types": [{"type": {"name": "electric"}}],
                "sprites": {"front_default": "x", "back_default": "y"},
            },
        )
    )

    r = client.get("/pokemons/api/pikachu")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "pikachu"
    assert body["types"] == ["electric"]