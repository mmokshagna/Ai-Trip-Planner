"""Client helpers for interacting with the OpenAI Chat Completions API."""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, Iterable, List, Sequence

import httpx

from app.core.config import settings

LOGGER = logging.getLogger(__name__)
OPENAI_MODEL = "gpt-4o-mini"

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


async def _call_openai_chat(
    messages: Sequence[Dict[str, Any]],
    *,
    functions: Sequence[Dict[str, Any]] | None = None,
    function_call: Dict[str, str] | None = None,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    """Call the OpenAI chat completions endpoint and return the raw payload."""

    if not settings.openai_api_key:
        raise RuntimeError("OpenAI API key is not configured.")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": list(messages),
        "temperature": temperature,
    }

    if functions:
        payload["functions"] = list(functions)
    if function_call:
        payload["function_call"] = function_call

    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()


def _coerce_date(value: Any, *, default: date | None = None) -> date:
    """Convert a string/date input into a ``date`` instance."""

    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str) and value:
        try:
            return datetime.fromisoformat(value.replace("Z", "")).date()
        except ValueError:
            pass
    if default is not None:
        return default
    return datetime.utcnow().date()


def _date_range(start: date, end: date) -> Iterable[date]:
    """Yield each date between ``start`` and ``end`` inclusive."""

    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def _weather_tip(entry: Dict[str, Any] | None) -> str | None:
    if not entry:
        return None
    condition = (entry.get("condition") or "").lower()
    if "rain" in condition:
        return "Expect showers—plan indoor highlights or carry a light jacket."
    if "snow" in condition:
        return "Snow is possible, leave extra transit time and wear warm layers."
    if "cloud" in condition:
        return "Cloud cover is expected; perfect for museums or relaxed walks."
    if "clear" in condition:
        return "Clear skies make it ideal for outdoor adventures."
    return None


def _event_activity(event: Dict[str, Any]) -> Dict[str, Any]:
    start_time = event.get("start_time")
    return {
        "name": event.get("title", "Featured Event"),
        "description": event.get("description", "Highlighted experience during your trip."),
        "category": "Experience",
        "location": event.get("venue"),
        "start_time": start_time,
        "end_time": None,
        "weather_advice": None,
    }


def _persona_theme(persona: str, day_index: int) -> str:
    adjective = persona.split()[0] if persona else "Adventurous"
    return f"{adjective} day {day_index + 1}"


def _default_activities(
    destination: str,
    persona: str,
    date_str: str,
    weather_entry: Dict[str, Any] | None,
) -> List[Dict[str, Any]]:
    """Generate baseline activities for a given day."""

    tips = _weather_tip(weather_entry)
    explore_desc = (
        f"Guided exploration of {destination}'s must-see highlights tailored for {persona.lower()} travelers."
    )
    cuisine_desc = f"Sample beloved local flavors across {destination}."
    unwind_desc = f"Unwind with a handpicked evening suggestion in {destination}."

    return [
        {
            "name": f"Morning discovery walk in {destination}",
            "description": explore_desc,
            "category": "Explore",
            "location": destination,
            "start_time": f"{date_str}T09:00:00",
            "end_time": f"{date_str}T12:00:00",
            "weather_advice": tips,
        },
        {
            "name": "Culinary immersion",
            "description": cuisine_desc,
            "category": "Eat",
            "location": f"{destination} food district",
            "start_time": f"{date_str}T13:00:00",
            "end_time": f"{date_str}T15:00:00",
            "weather_advice": tips,
        },
        {
            "name": "Evening wind-down",
            "description": unwind_desc,
            "category": "Stay",
            "location": f"{destination} boutique stay",
            "start_time": f"{date_str}T19:00:00",
            "end_time": f"{date_str}T21:00:00",
            "weather_advice": tips,
        },
    ]


def _fallback_itinerary(
    payload: Dict[str, Any],
    *,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Generate a deterministic itinerary when OpenAI is unavailable."""

    context = context or {}
    destination = payload.get("destination", "Destination")
    persona = payload.get("persona", "Adventurer")
    start_date = _coerce_date(payload.get("start_date"))
    end_date = _coerce_date(payload.get("end_date"), default=start_date + timedelta(days=2))

    events = context.get("events", [])
    weather = {str(item.get("date")): item for item in context.get("weather", [])}

    events_by_date: Dict[str, List[Dict[str, Any]]] = {}
    for event in events:
        start_time = event.get("start_time")
        if not start_time:
            continue
        event_date = str(start_time)[:10]
        events_by_date.setdefault(event_date, []).append(event)

    daily_plans: List[Dict[str, Any]] = []
    for index, current_date in enumerate(_date_range(start_date, end_date)):
        date_str = current_date.isoformat()
        weather_entry = weather.get(date_str)
        activities: List[Dict[str, Any]] = []

        for event in events_by_date.get(date_str, []):
            activities.append(_event_activity(event))

        activities.extend(_default_activities(destination, persona, date_str, weather_entry))

        if weather_entry and (weather_entry.get("condition") or "").lower().startswith("rain"):
            activities.append(
                {
                    "name": "Cozy cultural afternoon",
                    "description": "Shift outdoor plans indoors with museums, markets, or cafes.",
                    "category": "Explore",
                    "location": destination,
                    "start_time": f"{date_str}T15:00:00",
                    "end_time": f"{date_str}T17:00:00",
                    "weather_advice": _weather_tip(weather_entry),
                }
            )

        daily_plans.append(
            {
                "date": date_str,
                "theme": _persona_theme(persona, index),
                "activities": activities,
            }
        )

    summary_parts = [
        f"{persona} itinerary for {destination} spanning {start_date.isoformat()} to {end_date.isoformat()}.",
    ]
    if events:
        summary_parts.append(f"Includes {len(events)} featured event(s) found for your travel window.")
    if weather:
        summary_parts.append("Weather insights are woven into daily suggestions.")

    return {
        "destination": destination,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "persona": persona,
        "summary": " ".join(summary_parts),
        "daily_plans": daily_plans,
    }


def _fallback_adjustment(
    itinerary: Dict[str, Any],
    feedback: str,
    *,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Apply lightweight adjustments to an itinerary when GPT is unavailable."""

    context = context or {}
    updated = json.loads(json.dumps(itinerary, default=str))  # deep copy
    persona = updated.get("persona", context.get("persona", "Traveler"))

    feedback_lower = feedback.lower()
    for day in updated.get("daily_plans", []):
        if "rest" in feedback_lower and day.get("activities"):
            day["activities"].insert(
                1,
                {
                    "name": "Intentional downtime",
                    "description": "Set aside time to recharge and enjoy the accommodation amenities.",
                    "category": "Stay",
                    "location": updated.get("destination"),
                    "start_time": f"{day['date']}T14:00:00",
                    "end_time": f"{day['date']}T16:00:00",
                    "weather_advice": None,
                },
            )
        if "food" in feedback_lower:
            day.setdefault("activities", []).append(
                {
                    "name": "Local food crawl",
                    "description": "Discover neighborhood eateries curated for food lovers.",
                    "category": "Eat",
                    "location": updated.get("destination"),
                    "start_time": f"{day['date']}T17:30:00",
                    "end_time": f"{day['date']}T19:00:00",
                    "weather_advice": None,
                }
            )
        if "adventure" in feedback_lower:
            day.setdefault("activities", []).insert(
                0,
                {
                    "name": "Thrill-seeking highlight",
                    "description": "Add an outdoor adventure tailored to adrenaline seekers.",
                    "category": "Explore",
                    "location": updated.get("destination"),
                    "start_time": f"{day['date']}T08:00:00",
                    "end_time": f"{day['date']}T10:00:00",
                    "weather_advice": None,
                },
            )

    summary = updated.get("summary", "")
    modifier_sentence = (
        f"Feedback applied: {feedback}. Persona focus remains {persona}."
        if feedback
        else f"Persona focus remains {persona}."
    )
    updated["summary"] = summary + (" " if summary else "") + modifier_sentence
    return updated


async def generate_itinerary(
    payload: Dict[str, Any],
    *,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Generate an itinerary using OpenAI with a deterministic fallback."""

    context = context or {}
    if not settings.openai_api_key:
        return _fallback_itinerary(payload, context=context)

    system_prompt = build_itinerary_prompt(payload)
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": json.dumps({
                "trip_preferences": payload,
                "weather": context.get("weather", []),
                "events": context.get("events", []),
            }),
        },
    ]

    response = await _call_openai_chat(
        messages,
        functions=[OPENAI_ITINERARY_FUNCTION],
        function_call={"name": OPENAI_ITINERARY_FUNCTION["name"]},
    )

    try:
        choice = response["choices"][0]
        arguments = choice["message"]["function_call"]["arguments"]
        itinerary = json.loads(arguments)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive
        LOGGER.exception("Failed to parse OpenAI itinerary response; falling back", exc_info=exc)
        return _fallback_itinerary(payload, context=context)

    itinerary.setdefault("destination", payload.get("destination"))
    itinerary.setdefault("persona", payload.get("persona"))
    itinerary.setdefault("start_date", payload.get("start_date"))
    itinerary.setdefault("end_date", payload.get("end_date"))
    if context.get("events"):
        itinerary.setdefault("summary", "")
        itinerary["summary"] += (
            " " if itinerary["summary"] else ""
        ) + f"Includes {len(context['events'])} highlighted events."
    return itinerary


async def adjust_itinerary(
    itinerary: Dict[str, Any],
    feedback: str,
    *,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Customize an existing itinerary using GPT with graceful fallback."""

    context = context or {}
    context.setdefault("feedback", feedback)

    if not settings.openai_api_key:
        return _fallback_adjustment(itinerary, feedback, context=context)

    prompt = context.get("prompt") or build_itinerary_prompt(itinerary)
    messages = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": json.dumps({
                "current_itinerary": itinerary,
                "feedback": feedback,
                "events": context.get("events", []),
                "weather": context.get("weather", []),
            }),
        },
    ]

    response = await _call_openai_chat(
        messages,
        functions=[OPENAI_ITINERARY_FUNCTION],
        function_call={"name": OPENAI_ITINERARY_FUNCTION["name"]},
    )

    try:
        choice = response["choices"][0]
        arguments = choice["message"]["function_call"]["arguments"]
        adjusted = json.loads(arguments)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:  # pragma: no cover - defensive
        LOGGER.exception("Failed to parse customized itinerary; falling back", exc_info=exc)
        return _fallback_adjustment(itinerary, feedback, context=context)

    adjusted.setdefault("persona", itinerary.get("persona"))
    adjusted.setdefault("start_date", itinerary.get("start_date"))
    adjusted.setdefault("end_date", itinerary.get("end_date"))
    adjusted.setdefault("destination", itinerary.get("destination"))
    adjusted.setdefault("summary", itinerary.get("summary", ""))
    adjusted["summary"] += (
        " " if adjusted["summary"] else ""
    ) + f"Feedback applied: {feedback}."
    return adjusted


def _fallback_chat_message(message: str, context: Dict[str, Any]) -> str:
    itinerary = context.get("itinerary") or {}
    persona = itinerary.get("persona") or context.get("persona") or "Travel Companion"

    next_activity = None
    for day in itinerary.get("daily_plans", []):
        activities = day.get("activities", [])
        if activities:
            next_activity = (day.get("date"), activities[0].get("name"))
            break

    if next_activity:
        date_str, activity = next_activity
        schedule_note = f"Next on your itinerary for {date_str} is {activity}."
    else:
        schedule_note = "Let me know if you'd like suggestions for your upcoming plans."

    return (
        f"({persona}) {schedule_note} You asked: '{message}'. "
        "This offline assistant is summarizing from your saved trip."
    )


async def generate_chat_reply(message: str, context: Dict[str, Any] | None = None) -> str:
    """Return a GPT-powered chat reply with deterministic fallback."""

    context = context or {}
    if not settings.openai_api_key:
        return _fallback_chat_message(message, context)

    itinerary = context.get("itinerary")
    persona = itinerary.get("persona") if isinstance(itinerary, dict) else None
    system_prompt = (
        "You are an enthusiastic travel companion. Reference the itinerary details when responding, "
        "offer actionable suggestions, and keep answers concise."
    )
    if persona:
        system_prompt += f" Adopt the tone of a {persona} guide."

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": json.dumps({"message": message, "context": context}),
        },
    ]

    response = await _call_openai_chat(messages, temperature=0.6)

    try:
        return response["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):  # pragma: no cover - defensive
        LOGGER.exception("OpenAI chat response missing content; using fallback")
        return _fallback_chat_message(message, context)
