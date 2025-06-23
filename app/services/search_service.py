import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.db import endpoints_collection
from app.schemas.schemas import QueryModel
from app.utils.text_processing import clean_text
from app.utils.intent_resolver import IntentResolver

MODEL_DIR = "./model"
INDEX_FILE = os.path.join(MODEL_DIR, "faiss_index.bin")
META_FILE = os.path.join(MODEL_DIR, "endpoints_meta.json")

# -----------------------------
# Load the model
# -----------------------------
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

intent_resolver = IntentResolver()

def load_index_and_metadata():
    """
    Load the FAISS index and metadata from disk.
    """
    if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
        raise FileNotFoundError("Index or metadata file not found. Please train the model first.")

    index = faiss.read_index(INDEX_FILE)
    
    with open(META_FILE, "r", encoding = "utf-8") as f:
        metadata = json.load(f)

    return index, metadata

def search(query: QueryModel):
    """
    Search the most relevant endpoints using semantic similarity.
    """
    cleaned = clean_text(query.query)
    #embedding = model.encode([cleaned], convert_to_tensor = True).cpu().numpy()
    embedding = model.encode([cleaned], convert_to_numpy = True)

    index, metadata = load_index_and_metadata()

    distances, indices = index.search(embedding, query.top_k)

    preferred_methods = intent_resolver.resolve(query.query)

    results = []
    for i, idx in enumerate(indices[0]):
        str_idx = str(idx)
        if str_idx not in metadata:
            continue
        if idx < len(metadata):
            endpoint_meta = metadata[str_idx]
            score = float(distances[0][i])

            if preferred_methods and endpoint_meta["method"].lower() not in preferred_methods:
                score += 0.3
            endpoint_meta["score"] = score
            results.append(endpoint_meta)

    return sorted(results, key = lambda x: x["score"])