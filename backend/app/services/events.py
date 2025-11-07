"""Integration helpers for Eventbrite or Ticketmaster."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List

import httpx

from app.core.config import settings

LOGGER = logging.getLogger(__name__)
TICKETMASTER_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def _format_ticketmaster_date(value: str, *, end: bool = False) -> str:
    """Convert an ISO date string into the format expected by the API."""

    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        # Value already contains time—assume correct formatting.
        return value
    time_part = "23:59:59" if end else "00:00:00"
    return parsed.strftime(f"%Y-%m-%dT{time_part}Z")


async def fetch_events(destination: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Fetch live events for the travel window using the Ticketmaster Discovery API."""

    if not settings.events_api_key:
        return []

    city = destination.split(",")[0].strip() if destination else destination

    params = {
        "apikey": settings.events_api_key,
        "locale": "*",
        "sort": "date,asc",
        "size": 25,
        "city": city,
        "startDateTime": _format_ticketmaster_date(start_date, end=False),
        "endDateTime": _format_ticketmaster_date(end_date, end=True),
    }

    if not params["startDateTime"]:
        params.pop("startDateTime")
    if not params["endDateTime"]:
        params.pop("endDateTime")

    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
        try:
            response = await client.get(TICKETMASTER_URL, params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            LOGGER.warning("Event lookup failed: %s", exc)
            return []

    payload = response.json()
    events_raw = payload.get("_embedded", {}).get("events", [])

    events: List[Dict[str, Any]] = []
    for item in events_raw:
        dates = item.get("dates", {}).get("start", {})
        venues = item.get("_embedded", {}).get("venues", [])
        venue = venues[0] if venues else {}
        events.append(
            {
                "title": item.get("name"),
                "description": item.get("info") or item.get("pleaseNote"),
                "venue": venue.get("name"),
                "address": venue.get("address", {}).get("line1"),
                "start_time": dates.get("dateTime") or dates.get("localDate"),
                "url": item.get("url"),
            }
        )

    return events
