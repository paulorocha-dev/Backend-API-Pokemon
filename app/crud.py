# Operações no banco de dados

from sqlalchemy.orm import Session
from app.models import Pokemon
from app.schemas import PokemonCreate, PokemonUpdate
from sqlalchemy.exc import IntegrityError

def create_pokemon(db: Session, pokemon: PokemonCreate):
    db_pokemon = Pokemon(**pokemon.model_dump())
    db.add(db_pokemon)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None
    db.refresh(db_pokemon)
    return db_pokemon

def get_pokemons(db: Session, limit: int, offset: int):
    total = db.query(Pokemon).count()
    items = (
        db.query(Pokemon)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return total, items

def get_pokemon_by_id(db: Session, pokemon_id: int):
    return db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

def update_pokemon(db: Session, pokemon_id: int, data: PokemonUpdate):
    pokemon = get_pokemon_by_id(db, pokemon_id)
    if not pokemon:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pokemon, field, value)

    db.commit()
    db.refresh(pokemon)
    return pokemon

def delete_pokemon(db: Session, pokemon_id: int):
    pokemon = get_pokemon_by_id(db, pokemon_id)
    if not pokemon:
        return None

    db.delete(pokemon)
    db.commit()
    return pokemon