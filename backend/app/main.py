"""FastAPI application entry point for the AI Trip Planner backend."""
from fastapi import FastAPI

from app.api.routes import itinerary, customization, events, weather, chat, maps, storage
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware



def create_application() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    application = FastAPI(
        title="AI Trip Planner",
        description="Backend services for the AI-powered trip planning experience.",
        version="0.1.0",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    

    application.include_router(itinerary.router, prefix="/api")
    application.include_router(customization.router, prefix="/api")
    application.include_router(events.router, prefix="/api")
    application.include_router(weather.router, prefix="/api")
    application.include_router(chat.router, prefix="/api")
    application.include_router(maps.router, prefix="/api")
    application.include_router(storage.router, prefix="/api")

    return application


app = create_application()



@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Simple health check endpoint to verify the service is running."""
    return {"status": "ok", "environment": settings.environment}
