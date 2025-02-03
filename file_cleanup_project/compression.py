import os
import zipfile
import tarfile
from db import log_compression

def compress_files(directory, compressed_file_name, single_file=None, format='zip', delete_original=False):
    if single_file:
        file_path = os.path.join(directory, single_file)
        if not os.path.isfile(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return
        files_to_compress = [file_path]
    else:
        files_to_compress = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    compressed_filename = os.path.join(directory, f"{compressed_file_name}.{format}")

    try:
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
        print(f"Files compressed successfully into {compressed_filename}")
    except Exception as e:
        print(f"Error during compression: {e}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    compressed_file_name = input("Enter the name for the compressed file: ")
    single_file = input("Enter the file to compress (leave blank to compress all files): ")
    format = input("Enter the compression format (zip, tar): ")
    delete_original = input("Delete original files after compression? (yes/no): ").lower() == 'yes'
    compress_files(directory, compressed_file_name, single_file if single_file else None, format, delete_original)