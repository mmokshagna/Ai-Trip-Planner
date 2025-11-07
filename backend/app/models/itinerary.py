"""Pydantic models representing itinerary data structures."""
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class Activity(BaseModel):
    """An individual itinerary activity or recommendation."""

    name: str = Field(..., description="Name of the activity")
    description: str = Field(..., description="Short summary of the experience")
    category: str = Field(..., description="Activity category such as Eat, Explore, or Stay")
    location: Optional[str] = Field(None, description="Address or location identifier")
    start_time: Optional[str] = Field(None, description="Planned start time")
    end_time: Optional[str] = Field(None, description="Planned end time")
    weather_advice: Optional[str] = Field(None, description="Guidance based on forecast")


class DayPlan(BaseModel):
    """A collection of activities for a given day."""

    date: date
    theme: Optional[str] = Field(None, description="Summary theme for the day")
    activities: List[Activity] = Field(default_factory=list)


class Itinerary(BaseModel):
    """Full itinerary representation returned from GPT and stored in MongoDB."""

    destination: str
    start_date: date
    end_date: date
    persona: str
    summary: str
    daily_plans: List[DayPlan]
