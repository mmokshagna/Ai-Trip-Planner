"""Map and place discovery helpers."""
from typing import Any, Dict, List


async def fetch_map_points(destination: str, categories: List[str] | None = None) -> List[Dict[str, Any]]:
    """Return sample map pins for rendering on the frontend."""
    categories = categories or ["Explore", "Eat", "Stay"]

    return [
        {
            "name": "Central Plaza",
            "category": categories[0],
            "coordinates": {"lat": 41.3874, "lng": 2.1686},
            "description": "Historic city square with popular landmarks.",
        },
        {
            "name": "Tapas Alley",
            "category": "Eat",
            "coordinates": {"lat": 41.3809, "lng": 2.1854},
            "description": "Neighborhood packed with tapas bars and nightlife.",
        },
    ]
