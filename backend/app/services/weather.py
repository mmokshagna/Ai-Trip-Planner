"""OpenWeatherMap integration helpers."""
from typing import Any, Dict, List


async def fetch_weather_forecast(destination: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Return placeholder weather forecast data.

    The implementation should call the OpenWeatherMap One Call API or forecast endpoint
    and normalize results into a simple array of day -> condition mappings.
    """

    return [
        {
            "date": start_date,
            "condition": "Rain",
            "temperature_high": 22,
            "temperature_low": 17,
        },
        {
            "date": end_date,
            "condition": "Clear",
            "temperature_high": 26,
            "temperature_low": 19,
        },
    ]
