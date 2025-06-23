from pymongo import MongoClient
from app.core.config import get_settings

settings = get_settings()
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
endpoints_collection = db[settings.ENDPOINTS_COLLECTION]
modules_collection = db[settings.MODULES_COLLECTION]