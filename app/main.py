"""
main.py
-------
Root server entrypoint for Analytics Engine v2.

Run with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from app.routers import metrics

app = FastAPI(
    title="Analytics Engine v2",
    description=(
        "Production-grade analytics microservice with Pydantic v2 validation. "
        "Enforces strict request schemas and returns structured nested JSON responses."
    ),
    version="2.0.0",
    contact={
        "name": "Rahul – MCA, BMSIT",
    },
)

# Register routers
app.include_router(metrics.router)


@app.get("/", tags=["Health"])
def root() -> dict:
    """Health-check endpoint."""
    return {
        "service": "Analytics Engine v2",
        "status": "running",
        "docs": "/docs",
    }
