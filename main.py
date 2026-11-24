import json
import os
from datetime import datetime

DATA_FILE = "data.json"


# Load saved transactions
def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data.")
        return []


# Save transactions
def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)
        return True

    except OSError:
        print("Error: Could not save data.")
        return False


# Get a valid positive amount
def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return round(amount, 2)

        except ValueError:
            print("Please enter a valid number.")


# Add income
def add_income():
    print("\n--- ADD INCOME ---")

    amount = get_amount()
    description = input("Enter description: ").strip()

    if not description:
        description = "Income"

    transaction = {
        "id": get_next_id(),
        "type": "income",
        "amount": amount,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    transactions.append(transaction)

    if save_data():
        print("\nIncome added successfully!")


# Add expense
def add_expense():
    print("\n--- ADD EXPENSE ---")

    amount = get_amount()
    description = input("Enter description: ").strip()

    if not description:
        description = "Expense"

    transaction = {
        "id": get_next_id(),
        "type": "expense",
        "amount": amount,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    transactions.append(transaction)

    if save_data():
        print("\nExpense added successfully!")


# Generate transaction ID
def get_next_id():
    if not transactions:
        return 1

    return max(item["id"] for item in transactions) + 1


# View all transactions
def view_transactions():
    print("\n--- TRANSACTIONS ---")

    if not transactions:
        print("No transactions found.")
        return

    for item in transactions:
        print("-" * 40)
        print(f"ID: {item['id']}")
        print(f"Type: {item['type'].capitalize()}")
        print(f"Amount: {item['amount']:.2f}")
        print(f"Description: {item['description']}")
        print(f"Date: {item['date']}")

    print("-" * 40)


# Calculate and display balance
def view_balance():
    total_income = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "income"
    )

    total_expense = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "expense"
    )

    balance = total_income - total_expense

    print("\n--- BALANCE SUMMARY ---")
    print(f"Total Income:  {total_income:.2f} TL")
    print(f"Total Expense: {total_expense:.2f} TL")
    print("-" * 30)
    print(f"Current Balance: {balance:.2f} TL")


# Delete a transaction
def delete_transaction():
    print("\n--- DELETE TRANSACTION ---")

    if not transactions:
        print("There are no transactions to delete.")
        return

    view_transactions()

    try:
        transaction_id = int(input("\nEnter transaction ID to delete: "))

    except ValueError:
        print("Please enter a valid ID.")
        return

    for item in transactions:
        if item["id"] == transaction_id:
            transactions.remove(item)

            if save_data():
                print("Transaction deleted successfully!")

            return

    print("Transaction ID not found.")


# Display application menu
def show_menu():
    print("\n" + "=" * 45)
    print("          PERSONAL EXPENSE TRACKER")
    print("=" * 45)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Delete Transaction")
    print("6. Exit")

    print("=" * 45)


# Main application
transactions = load_data()


def main():
    print("\nWelcome to Personal Expense Tracker!")

    while True:
        show_menu()

        choice = input("Please choose an option (1-6): ").strip()

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_balance()

        elif choice == "5":
            delete_transaction()

        elif choice == "6":
            print("\nThank you for using Personal Expense Tracker!")
            print("Your data has been saved.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()