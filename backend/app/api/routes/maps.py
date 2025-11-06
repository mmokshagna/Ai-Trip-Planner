"""Routes for map data and place discovery."""
from typing import List

from fastapi import APIRouter, Query

from app.services.maps import fetch_map_points

router = APIRouter(tags=["Maps"])


@router.get("/map")
async def get_map_data(
    destination: str = Query(..., description="Destination name"),
    categories: List[str] | None = Query(None, description="Optional list of categories"),
) -> dict:
    """Fetch map pins for a destination."""

    pins = await fetch_map_points(destination, categories)
    return {"pins": pins}
