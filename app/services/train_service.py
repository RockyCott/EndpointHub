import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from app.core.db import endpoints_collection, modules_collection
from app.utils.text_processing import clean_text

MODEL_DIR = "./model"
EMBEDDINGS_FILE = os.path.join(MODEL_DIR, "embeddings.npy")
INDEX_FILE = os.path.join(MODEL_DIR, "faiss_index.bin")
META_FILE = os.path.join(MODEL_DIR, "endpoints_meta.json")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

STOPWORDS = {
    "endpoint", "controller", "api", "path", "data", "request",
    "response", "read", "write", "object", "info", "service",
    "method", "param", "params", "default", "input", "output",
    "doc", "docs", "value", "boolean"
}

def clean_stopwords(text):
    """
    Cleans the input text by removing stopwords and unnecessary characters.
    """
    words = text.lower().split()
    cleaned_words = [word for word in words if word not in STOPWORDS]
    return " ".join(cleaned_words)

def extract_data():
    """
    Extracts endpoints and their embeddings from the database.
    """
    endpoints = []

    modules = {str(doc["_id"]): doc.get("name", "unknown") for doc in modules_collection.find({})}
    if not modules:
        print("❌ No modules found in the database.")
        return []
    
    for doc in endpoints_collection.find({}):
        try:
            operation_id = doc.get("operationId", "")
            method = doc.get("method", "")
            path = doc.get("path", "")
            module_id = str(doc.get("moduleId", ""))
            visibility = doc.get("visibility", "")
            keywords = clean_stopwords(doc.get("keywords", ""))
            description = doc.get("description", "") or ""
            module_name = modules.get(module_id, "unknown")
            full_text = f"{method.lower()} {method.lower()} {path} {operation_id} {description} {keywords} {visibility} {module_name}"
            cleaned = clean_stopwords(clean_text(full_text))

            endpoints.append({
                "_id": str(doc["_id"]),
                "moduleId": module_id,
                "moduleName": module_name,
                "method": method,
                "url": path,
                "name": operation_id,
                "visibility": visibility,
                "keywords": keywords,
                "cleaned_text": cleaned,
                "original_text": full_text,
                "description": description,
            })
        except Exception as e:
            print(f"❌ Error with {doc.get('_id')}: {e}")

    return endpoints

def train():
    """
    Trains the indexs with endpoint embeddings.
    """
    endpoints = extract_data()
    if not endpoints:
        return False, "No data extracted"

    texts = [e["cleaned_text"] for e in endpoints]
    embeddings = model.encode(texts, convert_to_numpy = True)

    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    os.makedirs(MODEL_DIR, exist_ok = True)

    # Save the index and metadata
    faiss.write_index(index, INDEX_FILE)
    
    with open(META_FILE, "w", encoding = "utf-8") as f:
        json.dump({str(i): ep for i, ep in enumerate(endpoints)}, f, ensure_ascii = False, indent = 2)

    np.save(EMBEDDINGS_FILE, embeddings)

    return True, f"Model trained successfully with {len(endpoints)} endpoints."