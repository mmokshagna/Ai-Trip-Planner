"""OpenWeatherMap integration helpers."""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List

import httpx

from app.core.config import settings

LOGGER = logging.getLogger(__name__)


async def _geocode_destination(client: httpx.AsyncClient, destination: str) -> tuple[float, float] | None:
    params = {"q": destination, "limit": 1, "appid": settings.weather_api_key}
    response = await client.get("https://api.openweathermap.org/geo/1.0/direct", params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        return None
    first = data[0]
    return float(first["lat"]), float(first["lon"])


def _daterange(start: datetime, end: datetime) -> List[str]:
    days: List[str] = []
    cursor = start
    while cursor <= end:
        days.append(cursor.date().isoformat())
        cursor += timedelta(days=1)
    return days


async def fetch_weather_forecast(destination: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Fetch a five-day forecast and group data by day."""

    if not settings.weather_api_key or not destination:
        return []

    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        start = datetime.utcnow()
        end = start + timedelta(days=4)

    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
        try:
            coordinates = await _geocode_destination(client, destination)
        except httpx.HTTPError as exc:
            LOGGER.warning("Failed to geocode destination %s: %s", destination, exc)
            return []

        if not coordinates:
            return []

        lat, lon = coordinates
        params = {"lat": lat, "lon": lon, "appid": settings.weather_api_key, "units": "metric"}
        try:
            response = await client.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            LOGGER.warning("Failed to fetch weather forecast: %s", exc)
            return []

    forecast = response.json()
    grouped: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"temps": [], "conditions": []})
    for entry in forecast.get("list", []):
        timestamp = entry.get("dt")
        if timestamp is None:
            continue
        day = datetime.utcfromtimestamp(timestamp).date().isoformat()
        grouped[day]["temps"].append(entry.get("main", {}).get("temp"))
        condition = entry.get("weather", [{}])[0].get("main")
        if condition:
            grouped[day]["conditions"].append(condition)

    results: List[Dict[str, Any]] = []
    for day in _daterange(start, end):
        bucket = grouped.get(day)
        if not bucket or not bucket["temps"]:
            continue
        temps = [temp for temp in bucket["temps"] if temp is not None]
        if not temps:
            continue
        conditions = bucket["conditions"] or ["Clear"]
        dominant_condition = max(set(conditions), key=conditions.count)
        results.append(
            {
                "date": day,
                "condition": dominant_condition,
                "temperature_high": round(max(temps)),
                "temperature_low": round(min(temps)),
            }
        )

    return results
