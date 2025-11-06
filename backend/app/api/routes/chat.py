"""Routes for the travel companion chatbot."""
from fastapi import APIRouter

from app.services.chat import chat_response

router = APIRouter(tags=["Chat"])


@router.post("/chat")
async def chat(payload: dict) -> dict:
    """Send a message to the AI travel companion and receive a response."""

    message = payload.get("message", "")
    context = payload.get("context", {})
    response = await chat_response(message, context)
    return response
