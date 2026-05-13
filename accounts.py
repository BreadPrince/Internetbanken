import csv

ACCOUNTS_FILE = "konto.csv"

def load_accounts():
    accounts = []

    try:
        with open(ACCOUNTS_FILE) as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["balance"] = float(row["balance"])
                accounts.append(row)
    except FileNotFoundError:
        return []

    return accounts


def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w', newline='') as file:
        fieldnames = ['user_id', 'account_type', 'balance']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(accounts)


def create_account(user_id, account_type, balance):
    accounts = load_accounts()

    allowed_account_types = ["Debitkonto", "Sparkonto", "Aktiefondkonto"]

    if account_type not in allowed_account_types:
        return "invalid"

    for acc in accounts:
        if acc["user_id"] == user_id and acc["account_type"] == account_type:
            return "duplicate"

    user_accounts = [acc for acc in accounts if acc["user_id"] == user_id]
    if len(user_accounts) >= 3:
        return "limit"

    new_account = {
        "user_id": user_id,
        "account_type": account_type,
        "balance": float(balance)
    }

    accounts.append(new_account)
    save_accounts(accounts)

    return "success"

def get_accounts(user_id):
    accounts = load_accounts()
    user_accounts = []

    for account in accounts:
        if account['user_id'] == user_id:
            user_accounts.append(account)

    return user_accounts


def update_for_ISK(user_id, updatedBalance):
    accounts = load_accounts()
    for account in accounts:
        if account["user_id"] == user_id and account["account_type"] == "Aktiefondkonto":
            balance = float(account["balance"])
            account["balance"] = updatedBalance
    save_accounts(accounts)