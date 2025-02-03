import os
from file_cleanup_project.db.db import log_deletion

def delete_all_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                print(f"Deleting {filepath}")
                file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                os.remove(filepath)
                log_deletion(filename, filepath, "Deleted all files", file_size)
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    delete_all_files(directory)