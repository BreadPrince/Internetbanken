import csv
import datetime

HISTORY_FILE = "saldo.historik.csv"

def load_history():
    history = []

    try:
        with open(HISTORY_FILE, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                history.append(row)
    except FileNotFoundError:
        return []

    return history


def save_history(history):
    with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["user_id", "account_type", "amount", "action", "time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(history)


def add_history(user_id, account_type, amount, action):

    history = load_history()

    days = {
        "Monday": "Måndag",
        "Tuesday": "Tisdag",
        "Wednesday": "Onsdag",
        "Thursday": "Torsdag",
        "Friday": "Fredag",
        "Saturday": "Lördag",
        "Sunday": "Söndag"
    }

    now = datetime.datetime.now()
    day_name = days[now.strftime("%A")]

    time_str = f"{day_name} {now.strftime('%Y-%m-%d %H:%M')}"

    new_row = {
        "user_id": user_id,
        "account_type": account_type,
        "amount": amount,
        "action": action,
        "time": time_str
    }

    history.append(new_row)
    save_history(history)

def get_history(user_id):
    history = load_history()
    user_history = []

    for row in history:
        if row["user_id"] == user_id:
            user_history.append(row)

    return user_history