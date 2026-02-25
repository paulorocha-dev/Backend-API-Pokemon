from fastapi.testclient import TestClient

from app.main import app


def test_protected_route_requires_auth():
    client = TestClient(app)

    r = client.get("/pokemons/db")  # rota protegida por autenticar_meu_usuario
    assert r.status_code == 401
    assert r.headers.get("www-authenticate") == "Basic"