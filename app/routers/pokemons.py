# Endpoints CRUD

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio.client import Redis
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth import autenticar_meu_usuario
from app import crud, schemas
from app.deps import get_redis

from app.services.pokeapi import (
    fetch_pokemons_from_api,
    fetch_pokemon_raw_from_api,
    fetch_pokemon_for_db,
)

router = APIRouter(prefix="/pokemons")

# -------------------------
# Helpers
# -------------------------

def build_pagination(base_path: str, total: int, limit: int, offset: int) -> dict:
    next_offset = offset + limit
    prev_offset = offset - limit if offset - limit >= 0 else None

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "next": f"{base_path}?limit={limit}&offset={next_offset}" if next_offset < total else None,
        "previous": f"{base_path}?limit={limit}&offset={prev_offset}" if prev_offset is not None else None,
    }

def map_pokeapi_detail(detail: dict) -> dict:
    return {
        "id": detail["id"],
        "name": detail["name"],
        "height": detail["height"],
        "weight": detail["weight"],
        "types": [t["type"]["name"] for t in detail["types"]],
        "sprites": {
            "front_default": detail["sprites"]["front_default"],
            "back_default": detail["sprites"]["back_default"],
        },
    }


# ============================================================
# 🟢 PokeAPI (EXTERNO)
# ============================================================

@router.get(
    "/",
    response_model=schemas.PokemonListResponse,
    tags=["PokeAPI (Externo)"],
)
async def list_pokemons(
    limit: int = 20,
    offset: int = 0,
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario),
    redis: Redis = Depends(get_redis),
):
    pokeapi_list = await fetch_pokemons_from_api(redis, limit=limit, offset=offset)

    total = pokeapi_list["count"]
    items = pokeapi_list["results"]

    data = []
    for item in items:
        detail = await fetch_pokemon_raw_from_api(redis, item["name"])
        data.append(map_pokeapi_detail(detail))

    return {
        "data": data,
        "pagination": build_pagination("/pokemons", total, limit, offset),
    }


@router.get(
    "/api/{name_or_id}",
    response_model=schemas.PokemonAPIListItem,
    tags=["PokeAPI (Externo)"]
)
async def get_pokemon_from_pokeapi(
    name_or_id: str,
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario),
    redis: Redis = Depends(get_redis),
):
    detail = await fetch_pokemon_raw_from_api(redis, name_or_id)
    return map_pokeapi_detail(detail)


# ============================================================
# 🔵 BANCO DE DADOS (LEITURA)
# ============================================================

@router.get(
    "/db",
    response_model=schemas.PokemonDBListResponse,
    tags=["Banco de Dados (CRUD)"]
)
def list_pokemons_db(limit: int = 20, offset: int = 0, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    """Lista os Pokémon salvos no banco."""
    total, pokemons = crud.get_pokemons(db, limit, offset)

    return {
        "data": pokemons,
        "pagination": build_pagination("/pokemons/db", total, limit, offset),
    }


@router.get(
    "/{pokemon_id}",
    response_model=schemas.PokemonOut,
    tags=["Banco de Dados (CRUD)"]
)
def get_pokemon_db(pokemon_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    """Busca um Pokémon salvo no banco pelo ID."""
    pokemon = crud.get_pokemon_by_id(db, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado no banco")
    return pokemon


# ============================================================
# 🔵 BANCO DE DADOS (ESCRITA)
# ============================================================

@router.post(
    "/",
    response_model=schemas.PokemonOut,
    status_code=201,
    tags=["Banco de Dados (CRUD)"]
)
async def create_pokemon(
    name: str,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario),
    redis: Redis = Depends(get_redis),
):
    data = await fetch_pokemon_for_db(redis, name)

    created = crud.create_pokemon(db, schemas.PokemonCreate(**data))
    if not created:
        raise HTTPException(status_code=409, detail="Pokémon já existe no banco")

    return created


@router.put(
    "/{pokemon_id}",
    response_model=schemas.PokemonOut,
    tags=["Banco de Dados (CRUD)"]
)
def update_pokemon(pokemon_id: int, data: schemas.PokemonUpdate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    """Atualiza um Pokémon salvo no banco."""
    pokemon = crud.update_pokemon(db, pokemon_id, data)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado no banco")
    return pokemon


@router.delete(
    "/{pokemon_id}",
    tags=["Banco de Dados (CRUD)"]
)
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    """Remove um Pokémon do banco."""
    pokemon = crud.delete_pokemon(db, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado no banco")
    return {"detail": "Pokémon removido com sucesso"}