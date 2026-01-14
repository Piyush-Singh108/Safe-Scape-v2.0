# config.py
from pydantic_settings import BaseSettings # <--- THIS IS THE CRITICAL CHANGE

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str
    EXTERNAL_ROUTING_API_KEY: str
    
    # Load default values from .env
    ROUTE_BUFFER_METERS: int 
    MAX_CRIME_FETCH: int 

    class Config:
        env_file = ".env"

settings = Settings()