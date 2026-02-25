import respx
from httpx import Response

from app.services.pokeapi import POKEAPI_BASE_URL


@respx.mock
def test_get_pokemon_returns_404_when_not_found(client):
    respx.get(f"{POKEAPI_BASE_URL}/pokemon/naoexiste").mock(
        return_value=Response(404, json={"detail": "Not found"})
    )

    r = client.get("/pokemons/api/naoexiste")
    assert r.status_code == 404
    assert r.json()["detail"] == "Pokémon não encontrado"

@respx.mock
def test_get_pokemon_returns_502_when_pokeapi_fails(client):
    respx.get(f"{POKEAPI_BASE_URL}/pokemon/pikachu").mock(
        return_value=Response(503, json={"detail": "Service Unavailable"})
    )

    r = client.get("/pokemons/api/pikachu")
    assert r.status_code == 502
    assert r.json()["detail"] == "Erro ao acessar a PokeAPI"