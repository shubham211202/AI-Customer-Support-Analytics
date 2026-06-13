from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, model, tickets

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(model.router, prefix="/model", tags=["model"])
