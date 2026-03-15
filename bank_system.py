import json
import os

DATA_FILE = "bank_data.json"


# ---------------- ACCOUNT CLASS ----------------
class BankAccount:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Invalid amount.")
            return
        self.balance += amount
        self.history.append(f"Deposited ₹{amount}")
        print("✅ Deposit successful.")

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Invalid amount.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return
        self.balance -= amount
        self.history.append(f"Withdrew ₹{amount}")
        print("✅ Withdrawal successful.")

    def show_balance(self):
        print(f"💰 Current Balance: ₹{self.balance}")

    def show_history(self):
        if not self.history:
            print("No transactions yet.")
        else:
            print("📜 Transaction History:")
            for h in self.history:
                print("-", h)

    def to_dict(self):
        return {
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "history": self.history
        }


# ---------------- DATA HANDLING ----------------
def load_accounts():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    accounts = {}
    for name, acc in data.items():
        obj = BankAccount(acc["name"], acc["pin"], acc["balance"])
        obj.history = acc["history"]
        accounts[name] = obj
    return accounts


def save_accounts(accounts):
    data = {name: acc.to_dict() for name, acc in accounts.items()}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- MAIN SYSTEM ----------------
def main():
    accounts = load_accounts()

    while True:
        print("\n🏦 BANK MENU")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        # -------- CREATE ACCOUNT --------
        if choice == "1":
            name = input("Enter username: ")
            if name in accounts:
                print("❌ Account already exists.")
                continue

            pin = input("Set 4-digit PIN: ")
            accounts[name] = BankAccount(name, pin)
            save_accounts(accounts)
            print("✅ Account created successfully.")

        # -------- LOGIN --------
        elif choice == "2":
            name = input("Enter username: ")
            pin = input("Enter PIN: ")

            if name not in accounts or accounts[name].pin != pin:
                print("❌ Invalid credentials.")
                continue

            user = accounts[name]
            print(f"✅ Welcome, {user.name}")

            # ----- USER MENU -----
            while True:
                print("\n📋 ACCOUNT MENU")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Transaction History")
                print("5. Logout")

                opt = input("Enter option: ")

                if opt == "1":
                    amt = float(input("Enter amount: "))
                    user.deposit(amt)
                    save_accounts(accounts)

                elif opt == "2":
                    amt = float(input("Enter amount: "))
                    user.withdraw(amt)
                    save_accounts(accounts)

                elif opt == "3":
                    user.show_balance()

                elif opt == "4":
                    user.show_history()

                elif opt == "5":
                    print("🔒 Logged out.")
                    break

                else:
                    print("❌ Invalid option.")

        # -------- EXIT --------
        elif choice == "3":
            print("👋 Thank you for using the bank system.")
            break

        else:
            print("❌ Invalid choice.")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()