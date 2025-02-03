import os
import zipfile
import tarfile
from db import log_compression

def compress_files(directory, single_file=None, format='zip', delete_original=False):
    if single_file:
        files_to_compress = [single_file]
    else:
        files_to_compress = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    compressed_filename = os.path.join(directory, f"compressed.{format}")
    if format == 'zip':
        with zipfile.ZipFile(compressed_filename, 'w') as zipf:
            for file in files_to_compress:
                zipf.write(file, os.path.basename(file))
    elif format == 'tar':
        with tarfile.open(compressed_filename, 'w:gz') as tarf:
            for file in files_to_compress:
                tarf.add(file, arcname=os.path.basename(file))

    for file in files_to_compress:
        file_size = os.path.getsize(file) / (1024 * 1024)  # MB
        compressed_size = os.path.getsize(compressed_filename) / (1024 * 1024)  # MB
        log_compression(os.path.basename(file), compressed_filename, format, file_size, compressed_size)
        if delete_original:
            os.remove(file)