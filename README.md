# AI Trip Planner

A boilerplate project for an AI-powered travel planning web application combining FastAPI, React, Tailwind CSS, and Mapbox. The architecture integrates GPT-driven itinerary generation, weather-aware adjustments, live event recommendations, and collaborative trip management.

## Features
- Dynamic itinerary creation and customization via OpenAI GPT function calling.
- Eventbrite/Ticketmaster event discovery during travel dates.
- Weather-aware replanning using OpenWeatherMap forecasts.
- GPT-powered travel companion chatbot with Google Places search hooks.
- Interactive Mapbox dashboard with filters for Eat, Explore, and Stay categories.
- Offline-first Progressive Web App shell with service worker support.
- Social collaboration through shared trips and co-editing stubs.
- MongoDB persistence for saving and reusing itineraries.

## Project Structure
```
backend/
  app/
    api/                # FastAPI routers for each domain
    core/               # Application configuration
    db/                 # MongoDB client helpers
    models/             # Pydantic schemas
    services/           # External API integration stubs
  main.py               # FastAPI entrypoint
  requirements.txt      # Python dependencies
frontend/
  public/               # Static assets and service worker
  src/                  # React application source
Dockerfile              # Container configuration for backend service
.env.example            # Sample environment configuration
```

## Getting Started

### Backend
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Copy `.env.example` to `.env` and populate keys for OpenAI, MongoDB Atlas, OpenWeatherMap, Ticketmaster/Eventbrite, Google Maps, and Mapbox.
3. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

### Frontend
The frontend is scaffolded with Vite-compatible structure and Tailwind CSS configuration placeholders. Install dependencies and start the dev server once packages are defined:
```bash
cd frontend
npm install
npm run dev
```

## Docker
Build and run the backend service using Docker:
```bash
docker build -t ai-trip-planner .
docker run -p 8000:8000 --env-file .env ai-trip-planner
```

## Environment Variables
Refer to `.env.example` for the required keys. These include third-party APIs like OpenAI, OpenWeatherMap, Ticketmaster/Eventbrite, Google Maps, Mapbox, and optional RapidAPI integrations.

## Next Steps
- Implement concrete API calls in the service layer files.
- Connect the React frontend to the FastAPI backend via the defined endpoints.
- Configure Tailwind CSS, service workers, and PWA manifest files in the frontend.
- Add authentication and user management for collaborative trip editing.
