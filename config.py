# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str
    COLLECTION_NAME: str

    ORS_API_KEY: str   # OpenRouteService key

    ROUTE_BUFFER_METERS: int = 150
    MAX_CRIME_FETCH: int = 200

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()
