import requests

API_URL = "http://localhost:8080/cleanup"

def show_menu():
    """Display the CLI menu."""
    while True:
        print("\n📂 File Management CLI")
        print("1️⃣ Cleanup files")
        print("2️⃣ View cleanup logs")
        print("3️⃣ Exit")
        choice = input("📝 Enter your choice: ")

        if choice == "1":
            directory = input("📂 Enter directory path: ")
            response = requests.post(API_URL, json={"directory": directory})
            print(f"✅ API Response: {response.json()}")

        elif choice == "2":
            logs_response = requests.get("http://localhost:8080/logs")
            logs = logs_response.json()
            print("\n📝 Cleanup Logs:")
            for log in logs:
                print(f"- {log}")

        elif choice == "3":
            print("🚀 Exiting CLI. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select again.")

if __name__ == "__main__":
    show_menu()
