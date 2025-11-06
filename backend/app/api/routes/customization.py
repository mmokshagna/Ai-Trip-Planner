"""Routes for itinerary customization and prompt tuning."""
from fastapi import APIRouter

from app.models.itinerary import Itinerary
from app.services.chat import itinerary_adjustment_prompt

router = APIRouter(tags=["Customization"])


@router.post("/customize-trip", response_model=Itinerary)
async def customize_trip(payload: dict) -> Itinerary:
    """Regenerate an itinerary based on user feedback and persona adjustments."""

    feedback = payload.get("feedback", "")
    itinerary_payload = payload.get("itinerary", {})
    prompt = await itinerary_adjustment_prompt(feedback, itinerary_payload)
    _ = prompt  # Prevent unused variable warning in stub implementation.

    itinerary_data = {
        "destination": itinerary_payload.get("destination", payload.get("destination", "Unknown")),
        "start_date": itinerary_payload.get("start_date", payload.get("start_date", "2024-01-01")),
        "end_date": itinerary_payload.get("end_date", payload.get("end_date", "2024-01-07")),
        "persona": itinerary_payload.get("persona", payload.get("persona", "Adventurer")),
        "summary": (
            itinerary_payload.get("summary", "Base itinerary summary placeholder.")
            + f"\nCustomization requested: {feedback or 'No additional notes.'}"
        ),
        "daily_plans": itinerary_payload.get("daily_plans", []),
    }
    return Itinerary(**itinerary_data)
