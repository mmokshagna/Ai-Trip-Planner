"""Persistence helpers for itineraries."""
from typing import Any, Dict, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.db.session import get_mongo_client


def _serialize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB specific fields into JSON-friendly values."""
    serialized = document.copy()
    if isinstance(serialized.get("_id"), ObjectId):
        serialized["id"] = str(serialized.pop("_id"))
    return serialized


async def save_itinerary(data: Dict[str, Any]) -> str:
    """Persist itinerary data and return the inserted document ID."""
    client: AsyncIOMotorClient = get_mongo_client()
    collection = client[settings.mongo_database]["itineraries"]
    result = await collection.insert_one(data)
    return str(result.inserted_id)


async def list_itineraries(user_id: str) -> List[Dict[str, Any]]:
    """Retrieve itineraries for a given user."""
    client: AsyncIOMotorClient = get_mongo_client()
    collection = client[settings.mongo_database]["itineraries"]
    cursor = collection.find({"user_id": user_id})
    return [_serialize_document(document) async for document in cursor]
