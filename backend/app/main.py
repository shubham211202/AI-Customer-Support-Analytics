from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.models.ticket import Base
from app.api.v1.router import api_router
from prometheus_fastapi_instrumentator import Instrumentator

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Customer Support Analytics",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Register all API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def home():
    return {"message": "AI Customer Support Analytics API"}


@app.get("/health")
def health():
    return {"status": "healthy"}