"""Routes for the travel companion chatbot."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.services.chat import chat_response

router = APIRouter(tags=["Chat"])


@router.post("/chat")
async def chat(payload: dict) -> dict:
    """Send a message to the AI travel companion and receive a response."""

    message = payload.get("message", "")
    context = payload.get("context", {})
    try:
        response = await chat_response(message, context)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to contact the travel companion at this time.",
        ) from exc
    return response
