import requests
import os

API_URL = "http://localhost:8080"

def show_menu():
    while True:
        print("\n📂 File Management CLI")
        print("1️⃣ Cleanup files")
        print("2️⃣ View cleanup logs")
        print("3️⃣ Exit")
        choice = input("📝 Enter your choice: ")

        if choice == "1":
            directory = input("📂 Enter directory path: ")
            if not os.path.exists(directory) or not os.path.isdir(directory):
                print("❌ Invalid directory path.")
                continue

            try:
                response = requests.post(f"{API_URL}/cleanup", json={"directory": directory})
                response.raise_for_status()
                print("✅ Cleanup triggered. Check the output for details.") # Let user know to check output
                print(response.json()) # Print the full JSON response, including output
            except requests.exceptions.RequestException as e:
                print(f"❌ Cleanup failed: {e}")
                try:
                    error_data = response.json()
                    print(f"   Details: {error_data.get('details', 'N/A')}")
                    print(f"   Error: {error_data.get('error', 'N/A')}")
                except (ValueError, AttributeError):
                    pass

        elif choice == "2":
            try:
                logs_response = requests.get(f"{API_URL}/logs")
                logs_response.raise_for_status()
                logs = logs_response.json()
                print("\n📝 Cleanup Logs:")
                for log in logs:
                    print(f"- {log}")
            except requests.exceptions.RequestException as e:
                print(f"❌ Error retrieving logs: {e}")

        elif choice == "3":
            print("🚀 Exiting CLI. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select again.")

if __name__ == "__main__":
    show_menu()