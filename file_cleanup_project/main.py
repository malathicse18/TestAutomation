import click
from cleanup import delete_all_files
from compression import compress_files

def show_menu():
    print("File Management CLI")
    print("1. Cleanup all files")
    print("2. Compress files")
    print("3. Exit")

def cleanup_menu():
    directory = input("Enter the directory path: ")
    delete_all_files(directory)

def compress_menu():
    directory = input("Enter the directory path: ")
    single_file = input("Enter the file to compress (leave blank to compress all files): ")
    format = input("Enter the compression format (zip, tar): ")
    delete_original = input("Delete original files after compression? (yes/no): ").lower() == 'yes'
    compress_files(directory, single_file if single_file else None, format, delete_original)

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            cleanup_menu()
        elif choice == '2':
            compress_menu()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()