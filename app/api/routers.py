from fastapi import FastAPI
from app.api.endpoints import train, search, export, add

def register_routers(app: FastAPI) -> None:
    app.include_router(train.router, prefix = "/train", tags = ["Train"])
    app.include_router(search.router, prefix = "/search", tags = ["Search"])
    app.include_router(export.router, prefix = "/export-endpoint", tags = ["Export"])
    app.include_router(add.router, prefix = "/add-endpoint", tags = ["Add"])