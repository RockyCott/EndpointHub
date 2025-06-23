from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import json
from app.core.db import endpoints_collection
from app.utils import postman_parser
from app.schemas.schemas import EndpointMetaModel

router = APIRouter()

@router.post("/")
async def add_endpoint(file: UploadFile = File(...), metadata: str = Form(...)):
    """
    Accepts a Postman collection and associated metadata, then parses and stores each endpoint in MongoDB.
    """
    try:
        meta_obj = EndpointMetaModel.parse_raw(metadata)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = f"Invalid metadata: {e}")

    try:
        contents = await file.read()
        postman_json = json.loads(contents)
    except Exception:
        raise HTTPException(status_code = 400, detail = "Invalid JSON file")

    endpoints = postman_parser(postman_json, meta_obj.dict())

    if not endpoints:
        return JSONResponse(status_code = 400, content = {"message": "No endpoints extracted."})

    endpoints_collection.insert_many(endpoints)

    return {
        "message": "Endpoints saved successfully",
        "total": len(endpoints),
        "metadata": meta_obj.dict()
    }