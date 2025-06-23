import json
from bson import ObjectId
from app.utils.text_processing import clean_text

def extract_endpoints_from_postman(postman_json: dict, metadata: dict) -> list:
    """
    Extracts endpoints from a Postman collection JSON object.
    
    Args:
        postman_json (dict): The Postman collection JSON.
        metadata (dict): Additional metadata to attach to each endpoint.
    
    Returns:
        list: A list of dictionaries representing endpoints.
    """

    results = []
    
    for item in postman_json.get("item", []):
        try:
            name = item.get("name", "")
            request = item.get("request", {})
            method = request.get("method", "")
            url_obj = request.get("url", {})
            path = url_obj.get("raw", "").split("?")[0] if isinstance(url_obj, dict) else str(url_obj)

            full_text = f"{method} {path} {name} {metadata.get('keywords', '')} {metadata.get('visibility', '')}"
            cleaned = clean_text(full_text)

            results.append({
                "_id": str(ObjectId()),
                "method": method,
                "moduleId": metadata.get("moduleId", ""),
                "path": path,
                "visibility": metadata.get("visibility", ""),
                "operationId": name,
                "keywords": cleaned,
                "cleaned_text": cleaned,
                "original_text": full_text,
                "is_indexed": False,
                "author": metadata.get("created_by"),
                "team": None,
                "createdAt": metadata.get("createdAt"),
                "updatedAt": metadata.get("updatedAt")
            })
        except Exception as e:
            print(f"Error parsing item: {e}")
            continue

    return results