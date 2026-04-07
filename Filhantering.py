import csv # för att kunna läsa och skriva i csv filer
import random # för att kunna generera slumpmässiga ID
 

USERS_FILE = "users.csv" # filnamn för att lagra användardata
def load_users():

    users = [] 
    try:
        with open(USERS_FILE, encoding='utf-8') as file: 
            reader = csv.DictReader(file) 
            for row in reader: 
                users.append(row) 
    except FileNotFoundError:
        return[] # om filen inte finns, returnera en tom lista          
    return users # returnera listan med användarnamn och lösenord


def save_users(users):
    with open(USERS_FILE, 'w', newline='', encoding='utf-8') as file: # öppna filen i skrivläge w
        fieldnames = ["user_id", "first_name", "last_name", "password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames) 
        writer.writeheader() 
        writer.writerows(users)


def create_user_id(first_name, last_name):
    users = load_users()
    while True: # loop för att generera unika användarnamn
        numbers = random.randint(1000, 9999) # generera ett slumpmässigt 4-siffrigt nummer
        user_id = first_name[0].upper() + last_name[0].upper() + str(numbers)
        exists = False
        for user in users: 
            if user['user_id'] == user_id: # kolla om det genererade användarnamnet redan finns
                exists = True
                break
        if not exists:
            return user_id # om det inte finns, bryt loopen och använd det genererade användarnamnet 

def create_user(first_name, last_name, password):
    users = load_users() # ladda befintliga användare
    user_id = create_user_id(first_name, last_name) # generera ett unikt användarnamn
    new_user = {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "password": password
    }
    users.append(new_user) # lägg till den nya användaren i listan
    save_users(users) # spara den uppdaterade listan av användare till filen
    return user_id 
   

def check_login(user_id, password):
    users = load_users() 
    for user in users: 
        if user['user_id'] == user_id and user['password'] == password: 
            return True 
    return False 

