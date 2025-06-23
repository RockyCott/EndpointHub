from fastapi import APIRouter, Query
from app.services.search_service import search
from app.schemas.schemas import QueryModel

router = APIRouter()

@router.get("/")
def search_endpoint(q: str = Query(..., description = "Consulta de búsqueda"), top_k: int = 5):
    """
    Search the most relevant endpoints using semantic similarity.
    """
    print(f"Received query: {q} with top_k: {top_k}")
    model = QueryModel(query = q, top_k = top_k)
    res = search(model)
    # delete score keywords original_text cleaned_text
    for item in res:
        item.pop("score", None)
        item.pop("original_text", None)
        item.pop("cleaned_text", None)
    
    return res