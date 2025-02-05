import os
import zipfile
import tarfile
from db.db import log_compression

def compress_files(directory, compressed_file_name, single_file=None, format='zip', delete_original=False):
    """Compress files in a given directory into ZIP or TAR format"""
    if not os.path.isdir(directory):
        print(f"❌ Error: {directory} is not a valid directory.")
        return

    if single_file:
        files_to_compress = [os.path.join(directory, single_file)]
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
        else:
            print("❌ Unsupported format! Use 'zip' or 'tar'.")
            return

        # Log and delete original files if required
        for file in files_to_compress:
            file_size = os.path.getsize(file) / (1024 * 1024)  # MB
            compressed_size = os.path.getsize(compressed_filename) / (1024 * 1024)  # MB
            log_compression(os.path.basename(file), compressed_filename, format, file_size, compressed_size)

            if delete_original:
                os.remove(file)

        print(f"✅ Files compressed into: {compressed_filename}")

    except Exception as e:
        print(f"❌ Error during compression: {e}")

if __name__ == "__main__":
    directory = input("📁 Enter directory: ").strip()
    compressed_file_name = input("📦 Compressed file name: ").strip()
    single_file = input("📄 File to compress (leave blank for all): ").strip()
    format = input("🔄 Format (zip/tar): ").strip().lower()
    delete_original = input("❌ Delete originals? (yes/no): ").strip().lower() == 'yes'

    compress_files(directory, compressed_file_name, single_file if single_file else None, format, delete_original)
