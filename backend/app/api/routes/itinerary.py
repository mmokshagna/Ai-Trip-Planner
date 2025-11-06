"""Routes for itinerary generation."""
from fastapi import APIRouter

from app.models.itinerary import Itinerary
from app.services.openai_client import OPENAI_ITINERARY_FUNCTION, build_itinerary_prompt

router = APIRouter(tags=["Itinerary"])


@router.post("/plan-trip", response_model=Itinerary)
async def plan_trip(payload: dict) -> Itinerary:
    """Generate a new itinerary using OpenAI function calling.

    The implementation should call the OpenAI Chat Completions endpoint with the
    function schema provided in ``OPENAI_ITINERARY_FUNCTION`` and parse the returned
    JSON into the ``Itinerary`` model.
    """

    prompt = build_itinerary_prompt(payload)
    _ = OPENAI_ITINERARY_FUNCTION, prompt  # Document intended usage for implementers.
    itinerary_data = {
        "destination": payload.get("destination", "Unknown"),
        "start_date": payload.get("start_date", "2024-01-01"),
        "end_date": payload.get("end_date", "2024-01-07"),
        "persona": payload.get("persona", "Adventurer"),
        "summary": "This is a sample itinerary generated for demonstration purposes.",
        "daily_plans": [],
    }
    return Itinerary(**itinerary_data)
