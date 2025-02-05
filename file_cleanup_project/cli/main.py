import sys
import os
import subprocess

# Add project path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Tasks.cleanup import delete_all_files
from Tasks.compression import compress_files

def show_menu():
    print("\n📂 File Management CLI")
    print("1️⃣ Cleanup all files in a directory")
    print("2️⃣ Compress files in a directory")
    print("3️⃣ Exit")

def cleanup_menu():
    directory = input("📁 Enter the directory path: ").strip()
    if not os.path.isdir(directory):
        print("❌ Invalid directory!")
        return
    delete_all_files(directory)

def compress_menu():
    directory = input("📁 Enter the directory path: ").strip()
    compressed_file_name = input("📦 Enter compressed file name: ").strip()
    single_file = input("📄 Enter file to compress (or leave blank for all files): ").strip()
    format = input("🔄 Compression format (zip/tar): ").strip().lower()
    delete_original = input("❌ Delete original files after compression? (yes/no): ").strip().lower() == 'yes'
    
    compress_files(directory, compressed_file_name, single_file if single_file else None, format, delete_original)

def main():
    while True:
        show_menu()
        choice = input("📝 Enter your choice: ").strip()
        if choice == '1':
            cleanup_menu()
        elif choice == '2':
            compress_menu()
        elif choice == '3':
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
