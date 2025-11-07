"""Routes for itinerary customization and prompt tuning."""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

from app.models.itinerary import Itinerary
from app.services.chat import itinerary_adjustment_prompt
from app.services.events import fetch_events
from app.services.openai_client import adjust_itinerary
from app.services.weather import fetch_weather_forecast

LOGGER = logging.getLogger(__name__)

router = APIRouter(tags=["Customization"])


@router.post("/customize-trip", response_model=Itinerary)
async def customize_trip(payload: dict) -> Itinerary:
    """Regenerate an itinerary based on user feedback and persona adjustments."""

    feedback = payload.get("feedback", "")
    itinerary_payload = payload.get("itinerary", {})
    prompt = await itinerary_adjustment_prompt(feedback, itinerary_payload)

    destination = str(itinerary_payload.get("destination") or payload.get("destination", ""))
    start_date = str(itinerary_payload.get("start_date") or payload.get("start_date", ""))
    end_date = str(itinerary_payload.get("end_date") or payload.get("end_date", ""))

    context: Dict[str, Any] = {"prompt": prompt}
    try:
        context["weather"] = await fetch_weather_forecast(destination, start_date, end_date)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.warning("Weather lookup failed during customization: %s", exc)

    try:
        context["events"] = await fetch_events(destination, start_date, end_date)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.warning("Event lookup failed during customization: %s", exc)

    try:
        itinerary_data = await adjust_itinerary(itinerary_payload, feedback, context=context)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to customize itinerary at this time.",
        ) from exc

    return Itinerary(**itinerary_data)
