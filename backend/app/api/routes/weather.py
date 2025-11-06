"""Routes for weather-aware itinerary planning."""
from fastapi import APIRouter, Query

from app.services.weather import fetch_weather_forecast

router = APIRouter(tags=["Weather"])


@router.get("/weather")
async def get_weather(
    destination: str = Query(..., description="City to fetch forecast for"),
    start_date: str = Query(..., description="Trip start date"),
    end_date: str = Query(..., description="Trip end date"),
) -> dict:
    """Return a weather forecast for the travel dates."""

    forecast = await fetch_weather_forecast(destination, start_date, end_date)
    return {"forecast": forecast}
