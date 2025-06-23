from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import get_settings
from app.api.routers import register_routers
from app.services.train_service import train

MODEL_FILES = [
    "./model/faiss_index.bin",
    "./model/embeddings.npy",
    "./model/endpoints_meta.json"
]

def model_files_exist() -> bool:
    return all(os.path.exists(path) for path in MODEL_FILES)

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    settings = get_settings()
    
    app = FastAPI(
        title = "Endpoint Hub",
        version = "1.0",
        description = "API para gestión y búsqueda semántica de endpoints Postman",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.ALLOWED_ORIGINS,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )

    # Routers
    register_routers(app)

    @app.on_event("startup")
    async def startup_event():
        if model_files_exist():
            print("Model exists. No training required.")
        else:
            print("Model not found. Starting training...")
            success, message = train()
            print(f"🔧 Training completed: {message if success else '❌ ' + message}")

    return app

app = create_app()