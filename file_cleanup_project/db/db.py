from pymongo import MongoClient
import time

client = MongoClient('mongodb://localhost:27017/')
db = client['file_management']

def log_deletion(filename, filepath, reason, size_MB):
    logs = db['deletion_logs']
    log_entry = {
        "filename": filename,
        "filepath": filepath,
        "deleted_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "reason": reason,
        "size_MB": size_MB
    }
    logs.insert_one(log_entry)

def log_compression(original_filename, compressed_filename, format, original_size_MB, compressed_size_MB):
    logs = db['compression_logs']
    log_entry = {
        "original_filename": original_filename,
        "compressed_filename": compressed_filename,
        "compression_format": format,
        "original_size_MB": original_size_MB,
        "compressed_size_MB": compressed_size_MB,
        "compressed_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }
    logs.insert_one(log_entry)