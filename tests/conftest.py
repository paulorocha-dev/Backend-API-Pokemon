import pytest
from fastapi.testclient import TestClient

import fakeredis.aioredis as fakeredis_async

from app.main import app
from app.services.auth import autenticar_meu_usuario
from app.deps import get_redis


def auth_ok():
    # Apenas “passa” a autenticação nos testes
    return None


@pytest.fixture
def client():
    # Override da autenticação
    app.dependency_overrides[autenticar_meu_usuario] = auth_ok

    # Override do Redis
    fake = fakeredis_async.FakeRedis(decode_responses=True)
    app.dependency_overrides[get_redis] = lambda: fake

    with TestClient(app) as c:
        yield c

    # limpa overrides ao final
    app.dependency_overrides.clear()