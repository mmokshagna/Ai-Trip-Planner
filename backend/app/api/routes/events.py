"""Routes for retrieving live event data."""
from fastapi import APIRouter, Query

from app.services.events import fetch_events

router = APIRouter(tags=["Events"])


@router.get("/events")
async def get_events(
    destination: str = Query(..., description="City or location to search"),
    start_date: str = Query(..., description="Trip start date"),
    end_date: str = Query(..., description="Trip end date"),
) -> dict:
    """Fetch live events for the travel destination."""

    events = await fetch_events(destination, start_date, end_date)
    return {"events": events}
