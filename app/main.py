from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def seed_users():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            print("No users found in database. Seeding default admin/agent accounts...")
            admin_user = User(
                username="admin",
                hashed_password=get_password_hash("admin"),
                role="admin"
            )
            agent_user = User(
                username="agent",
                hashed_password=get_password_hash("agent"),
                role="agent"
            )
            db.add_all([admin_user, agent_user])
            db.commit()
            print("Default users seeded successfully!")
    except Exception as e:
        print(f"Error seeding default users: {e}")
    finally:
        db.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    # Expose Prometheus metrics on /metrics endpoint
    Instrumentator().instrument(app).expose(app)

    @app.on_event("startup")
    def startup_event():
        configure_logging()
        seed_users()

    return app



app = create_app()
