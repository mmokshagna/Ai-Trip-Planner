"""Integration helpers for Eventbrite or Ticketmaster."""
from typing import Any, Dict, List


async def fetch_events(destination: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Return placeholder event data for the specified travel window.

    Replace this stub with API calls to Eventbrite or Ticketmaster using the configured
    API key. Structure the data to include title, description, venue, and start time.
    """

    return [
        {
            "title": "Sample Jazz Festival",
            "description": "A lively evening with local jazz artists.",
            "venue": "Downtown Arts Center",
            "start_time": f"{start_date}T19:00:00",
            "url": "https://www.eventbrite.com/sample",
        }
    ]
