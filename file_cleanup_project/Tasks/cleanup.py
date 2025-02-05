import os
from db.db import log_deletion
import sys
import os

# Add the parent directory of the script to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def delete_all_files(directory):
    """Deletes all files in a specified directory"""
    if not os.path.isdir(directory):
        print(f"❌ Error: {directory} is not a valid directory.")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                file_size = os.path.getsize(filepath) / (1024 * 1024)  # Convert bytes to MB
                os.remove(filepath)
                log_deletion(filename, filepath, "Deleted all files", file_size)
                print(f"✅ Deleted: {filepath}")
            except Exception as e:
                print(f"❌ Error deleting {filepath}: {e}")

if __name__ == "__main__":
    directory = input("📁 Enter directory to cleanup: ").strip()
    delete_all_files(directory)
