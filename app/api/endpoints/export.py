from fastapi import APIRouter, HTTPException, Response
from bson import ObjectId
import bson.json_util as bson_json
from app.core.db import endpoints_collection

router = APIRouter()

@router.get("/{id}")
def export_endpoint(id: str):
    """
    Export an endpoint by its ID in Postman collection format.
    """
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code = 400, detail = "Invalid ID")

    doc = endpoints_collection.find_one({"_id": obj_id})
    if not doc or "raw" not in doc:
        raise HTTPException(status_code = 404, detail = "Endpoint not found")

    raw = doc.get("raw")
    if not raw:
        raise HTTPException(status_code = 500, detail="Document does not contain 'raw'")

    filename = f"{doc.get('operationId', 'endpoint')}.json"

    return Response(
        content = bson_json.dumps(raw, indent = 2),
        media_type = "application/json",
        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    )