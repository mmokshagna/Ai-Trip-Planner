"""Map and place discovery helpers."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import httpx

from app.core.config import settings

LOGGER = logging.getLogger(__name__)
PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


def _fallback_points(destination: str, categories: List[str]) -> List[Dict[str, Any]]:
    """Return deterministic fallback points when API access is unavailable."""

    base_coordinates = {
        "lat": 41.3851,
        "lng": 2.1734,
    }
    return [
        {
            "name": f"{destination} {category} highlight",
            "category": category,
            "coordinates": base_coordinates,
            "description": f"Suggested {category.lower()} experience near {destination}.",
        }
        for category in categories
    ]


async def fetch_map_points(destination: str, categories: List[str] | None = None) -> List[Dict[str, Any]]:
    """Search for map pins using Google Places Text Search with graceful fallback."""

    if not destination:
        return []

    categories = categories or ["Explore", "Eat", "Stay"]

    if not settings.maps_api_key:
        return _fallback_points(destination, categories)

    pins: List[Dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
        for category in categories:
            params = {"query": f"{category} in {destination}", "key": settings.maps_api_key}
            try:
                response = await client.get(PLACES_URL, params=params)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                LOGGER.warning("Map lookup failed for %s: %s", category, exc)
                continue

            payload = response.json()
            for place in payload.get("results", [])[:3]:
                location = place.get("geometry", {}).get("location")
                if not location:
                    continue
                pins.append(
                    {
                        "name": place.get("name"),
                        "category": category,
                        "coordinates": {"lat": location.get("lat"), "lng": location.get("lng")},
                        "description": place.get("formatted_address") or place.get("vicinity"),
                        "rating": place.get("rating"),
                    }
                )

    if pins:
        return pins

    return _fallback_points(destination, categories)
