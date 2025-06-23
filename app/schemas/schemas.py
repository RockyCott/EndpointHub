from fastapi import Query
from pydantic import BaseModel, Field

class QueryModel(BaseModel):
    query: str
    top_k: int = 5

class EndpointMetaModel(BaseModel):
    module: str = Field(..., description = "Nombre del módulo que contiene el endpoint")
    created_by: str = Field(..., description = "Persona o sistema que lo creó")
