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

def save_email_schedule(emails, subject, message, schedule_time):
    schedules = db['greeting_schedules']
    schedule_entry = {
        "emails": emails,
        "subject": subject,
        "message": message,
        "schedule_time": schedule_time,
        "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }
    schedules.insert_one(schedule_entry)

def log_sent_email(recipient, subject, message, status):
    logs = db['email_logs']
    log_entry = {
        "recipient": recipient,
        "subject": subject,
        "message": message,
        "sent_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "status": status
    }
    logs.insert_one(log_entry)

def get_scheduled_emails():
    schedules = db['greeting_schedules']
    return list(schedules.find())
