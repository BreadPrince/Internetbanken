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

def deposit(user_id, account_type, amount):
    accounts = load_accounts()
    amount = float(amount)

    if amount <= 0:
        return False

    for account in accounts:
        if account["user_id"] == user_id and account["account_type"] == account_type:
            current_balance = float(account["balance"])
            account["balance"] = current_balance + amount
            save_accounts(accounts)
            return True

    return False


def withdraw(user_id, account_type, amount):
    accounts = load_accounts()
    amount = float(amount)

    if amount <= 0:
        return False

    for account in accounts:
        if account["user_id"] == user_id and account["account_type"] == account_type:
            current_balance = float(account["balance"])

            if current_balance >= amount:
                account["balance"] = current_balance - amount
                save_accounts(accounts)
                return True
            else:
                return False

    return False

def transfer(user_id, from_account, to_account, amount):
    accounts = load_accounts()
    amount = float(amount)

    if amount <= 0:
        return False

    from_found = None
    to_found = None

    for account in accounts:
        if account["user_id"] == user_id and account["account_type"] == from_account:
            from_found = account
        if account["user_id"] == user_id and account["account_type"] == to_account:
            to_found = account

    if from_found is None or to_found is None:
        return False

    from_balance = float(from_found["balance"])
    to_balance = float(to_found["balance"])

    if from_balance < amount:
        return False

    from_found["balance"] = from_balance - amount
    to_found["balance"] = to_balance + amount

    save_accounts(accounts)
    return True