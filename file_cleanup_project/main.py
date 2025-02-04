import click
import threading
from cleanup import delete_all_files
from compression import compress_files
from email_service import schedule_email_sending, configure_email

def show_menu():
    print("\nFile Management CLI")
    print("1. Cleanup all files")
    print("2. Compress files")
    print("3. Configure Email Greetings")
    print("4. Start Email Scheduler (Runs in Background)")
    print("5. Exit")

def cleanup_menu():
    directory = input("Enter the directory path: ")
    delete_all_files(directory)

def compress_menu():
    directory = input("Enter the directory path: ")
    single_file = input("Enter the file to compress (leave blank to compress all files): ")
    format = input("Enter the compression format (zip, tar): ")
    delete_original = input("Delete original files after compression? (yes/no): ").lower() == 'yes'
    compress_files(directory, single_file if single_file else None, format, delete_original)

def start_email_scheduler():
    print("Email Scheduler started in the background.")
    thread = threading.Thread(target=schedule_email_sending, daemon=True)
    thread.start()

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            cleanup_menu()
        elif choice == '2':
            compress_menu()
        elif choice == '3':
            configure_email()
        elif choice == '4':
            start_email_scheduler()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
