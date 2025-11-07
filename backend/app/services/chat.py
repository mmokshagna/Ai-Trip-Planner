"""GPT-powered travel companion helpers."""

from __future__ import annotations

from typing import Any, Dict

from app.services.openai_client import build_itinerary_prompt, generate_chat_reply


async def chat_response(message: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return a chat response powered by OpenAI or deterministic fallback."""

    reply = await generate_chat_reply(message, context=context)
    return {"message": reply}


async def itinerary_adjustment_prompt(feedback: str, payload: Dict[str, Any]) -> str:
    """Generate a customization prompt using existing itinerary data and user feedback."""

    base_prompt = build_itinerary_prompt(payload)
    return base_prompt + f" Update the plan with this traveler feedback: {feedback}."
