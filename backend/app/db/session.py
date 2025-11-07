"""MongoDB client configuration."""
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


def get_mongo_client() -> AsyncIOMotorClient:
    """Create and return a MongoDB client instance."""
    return AsyncIOMotorClient(settings.mongo_connection_string)
