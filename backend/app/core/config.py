"""Application configuration and settings management."""
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Centralized application configuration loaded from environment variables."""

    environment: str = Field(default="development", description="Runtime environment name")
    openai_api_key: str = Field(default="", description="OpenAI API key for GPT access")
    mongo_connection_string: str = Field(default="", description="MongoDB Atlas connection URI")
    mongo_database: str = Field(default="trip_planner", description="MongoDB database name")
    weather_api_key: str = Field(default="", description="OpenWeatherMap API key")
    events_api_key: str = Field(default="", description="Ticketmaster/Eventbrite API key")
    maps_api_key: str = Field(default="", description="Google Maps Places API key")
    rapidapi_key: str = Field(default="", description="RapidAPI key for Airbnb or other services")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


settings = get_settings()
