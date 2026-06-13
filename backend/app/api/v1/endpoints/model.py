from fastapi import APIRouter

from app.ml.model_loader import analyzer

router = APIRouter()


@router.post("/reload")
def reload_models():
    """
    Trigger the backend to reload the latest registered models from MLflow registry.
    """
    analyzer.load_models()
    return {
        "status": "success",
        "model_version": analyzer.model_version,
    }
