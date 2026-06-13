from fastapi import APIRouter, Depends

from app.ml.model_loader import analyzer
from app.api.deps import get_current_admin

router = APIRouter(dependencies=[Depends(get_current_admin)])


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
