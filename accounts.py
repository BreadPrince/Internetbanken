import csv

ACCOUNTS_FILE = "konto.csv"

def load_accounts():
    accounts = []

    try:
        with open(ACCOUNTS_FILE) as file:
            reader = csv.DictReader(file)
            for row in reader:
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

    new_account = {
        'user_id': user_id,
        'account_type': account_type,
        'balance': balance
    }

    accounts.append(new_account)
    save_accounts(accounts)


def get_accounts(user_id):
    accounts = load_accounts()
    user_accounts = []

    for account in accounts:
        if account['user_id'] == user_id:
            user_accounts.append(account)

    return user_accounts
