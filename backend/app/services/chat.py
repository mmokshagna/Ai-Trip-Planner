"""GPT-powered travel companion helpers."""
from typing import Any, Dict

from app.services.openai_client import build_itinerary_prompt


async def chat_response(message: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return a placeholder chat response.

    Implementations should call OpenAI with relevant context (e.g., itinerary summary,
    current location data) and return streamed or synchronous responses for the chat UI.
    """

    persona = (context or {}).get("persona", "Local Expert")
    return {
        "message": (
            f"({persona}) I received your message: '{message}'. "
            "This is a placeholder response from the AI travel companion."
        )
    }


async def itinerary_adjustment_prompt(feedback: str, payload: Dict[str, Any]) -> str:
    """Generate a customization prompt using existing itinerary data and user feedback."""

    base_prompt = build_itinerary_prompt(payload)
    return base_prompt + f" Update the plan with this traveler feedback: {feedback}."
