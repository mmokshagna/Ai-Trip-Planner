"""Routes for saving and retrieving itineraries."""
from fastapi import APIRouter

from app.services.storage import list_itineraries, save_itinerary

router = APIRouter(tags=["Storage"])


@router.post("/save")
async def save_trip(payload: dict) -> dict:
    """Persist an itinerary payload to MongoDB."""

    itinerary = payload.get("itinerary", {})
    itinerary["user_id"] = payload.get("user_id", "demo-user")
    itinerary.setdefault("daily_plans", [])
    itinerary_id = await save_itinerary(itinerary)
    return {"itinerary_id": itinerary_id}


@router.get("/trips/{user_id}")
async def get_trips(user_id: str) -> dict:
    """List saved itineraries for a user."""

    trips = await list_itineraries(user_id)
    return {"trips": trips}
