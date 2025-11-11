"""Routes for itinerary generation."""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

from app.models.itinerary import Itinerary
from app.services.events import fetch_events
from app.services.openai_client import generate_itinerary
from app.services.weather import fetch_weather_forecast

LOGGER = logging.getLogger(__name__)

router = APIRouter(tags=["Itinerary"])


@router.post("/plan-trip", response_model=Itinerary)
async def plan_trip(payload: dict) -> Itinerary:
    """Generate a new itinerary using OpenAI function calling with contextual data."""
    LOGGER.info("plan my trip")
    destination = str(payload.get("destination", ""))
    start_date = str(payload.get("start_date", ""))
    end_date = str(payload.get("end_date", ""))

    context: Dict[str, Any] = {}
    try:
        context["weather"] = await fetch_weather_forecast(destination, start_date, end_date)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.warning("Weather lookup failed: %s", exc)

    try:
        context["events"] = await fetch_events(destination, start_date, end_date)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.warning("Event lookup failed: %s", exc)

    try:
        itinerary_data = await generate_itinerary(payload, context=context)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to generate itinerary at this time.",
        ) from exc

    return Itinerary(**itinerary_data)
