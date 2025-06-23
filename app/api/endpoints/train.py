from fastapi import APIRouter
from app.services.train_service import train

router = APIRouter()

@router.post("/")
def train_model():
    """
    Endpoint to trigger the training of the model.
    """
    try:
        success, message = train()
        return {"success": success, "message": message}
    except Exception as e:
        return {"success": False, "message": str(e)}