import os
import shutil
from db import log_cleanup

def cleanup_directory(directory):
    """Delete all files from the given directory."""
    if not os.path.exists(directory):
        log_cleanup(directory, "Failed", "Directory does not exist")
        return {"error": "Directory does not exist"}

    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Delete file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Delete directory
        log_cleanup(directory, "Success")
        return {"message": "Cleanup successful"}
    except Exception as e:
        log_cleanup(directory, "Failed", str(e))
        return {"error": "Error during cleanup", "details": str(e)}
