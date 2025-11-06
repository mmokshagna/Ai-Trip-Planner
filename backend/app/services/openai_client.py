"""Client helpers for interacting with the OpenAI Chat Completions API."""
from typing import Any, Dict


OPENAI_ITINERARY_FUNCTION = {
    "name": "create_itinerary",
    "description": "Return a structured itinerary for the user",
    "parameters": {
        "type": "object",
        "properties": {
            "destination": {"type": "string"},
            "summary": {"type": "string"},
            "daily_plans": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "format": "date"},
                        "theme": {"type": "string"},
                        "activities": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "category": {"type": "string"},
                                    "location": {"type": ["string", "null"]},
                                    "start_time": {"type": ["string", "null"]},
                                    "end_time": {"type": ["string", "null"]},
                                    "weather_advice": {"type": ["string", "null"]},
                                },
                                "required": ["name", "description", "category"],
                            },
                        },
                    },
                    "required": ["date", "activities"],
                },
            },
        },
        "required": ["destination", "summary", "daily_plans"],
    },
}


def build_itinerary_prompt(payload: Dict[str, Any]) -> str:
    """Create a base system prompt for itinerary generation."""
    persona = payload.get("persona", "Adventurer")
    destination = payload.get("destination", "")
    start_date = payload.get("start_date", "")
    end_date = payload.get("end_date", "")

    return (
        "You are an expert travel planner. Create a JSON itinerary that matches the user's "
        f"persona of {persona} for a trip to {destination} between {start_date} and {end_date}. "
        "Balance activities across Eat, Explore, and Stay categories, and provide short summaries."
    )
