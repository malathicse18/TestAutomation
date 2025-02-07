from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["file_cleanup_db"]
logs_collection = db["cleanup_logs"]

def log_cleanup(directory, status, details=""):
    """Log cleanup operation in MongoDB."""
    log_entry = {
        "directory": directory,
        "status": status,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    logs_collection.insert_one(log_entry)

def get_cleanup_logs():
    """Retrieve cleanup logs from MongoDB."""
    return list(logs_collection.find({}, {"_id": 0}))
