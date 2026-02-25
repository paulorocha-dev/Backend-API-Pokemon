import os

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/pokemons.db"
    )

settings = Settings()