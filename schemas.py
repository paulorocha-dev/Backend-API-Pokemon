# Esquemas Pydantic - entrada e saída de dados

from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Banco (CRUD)

class PokemonBase(BaseModel):
    name: str
    height: int
    weight: int
    base_experience: int

class PokemonCreate(PokemonBase):
    pass

class PokemonUpdate(BaseModel):
    height: Optional[int] = None
    weight: Optional[int] = None
    base_experience: Optional[int] = None

class PokemonOut(PokemonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# GET público (/pokemons) — PokeAPI (detalhado + paginação)

class Pagination(BaseModel):
    total: int
    limit: int
    offset: int
    next: Optional[str]
    previous: Optional[str]

class PokemonSprites(BaseModel):
    front_default: Optional[str]
    back_default: Optional[str]

class PokemonAPIListItem(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]
    sprites: PokemonSprites

class PokemonListResponse(BaseModel):
    data: List[PokemonAPIListItem]
    pagination: Pagination

# Lista do banco (pra ver o que foi salvo)

class PokemonDBListResponse(BaseModel):
    data: List[PokemonOut]
    pagination: Pagination