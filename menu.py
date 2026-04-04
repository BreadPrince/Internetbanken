import Filhantering as filhantering  # modul för användare och inlogg
# as filhantering behövs pga stort F på filnamnet
import accounts # modul för kontotyper och saldon

def user_dashboard(user_id):
    """Meny för inloggad användare"""
    while True:
        print(f"\nInloggad som: {user_id}")
        print("1. Se konton och saldo")
        print("2. Öppna nytt konto")
        print("3. Insättning och uttag")
        print("4. Visa grafer")
        print("5. Logga ut")
        
        val = input("Välj ett alternativ: ")
        
        if val == "1":
            # hämtar data från accounts.py
            user_accounts = accounts.get_accounts(user_id)
            if not user_accounts:
                print("Inga aktiva konton hittades")
            else:
                for acc in user_accounts:
                    # skriver ut varje konto på egna rader med skilje-streck emellan
                    print("-" * 20)
                    print(f"Konto: {acc['account_type']}")
                    print(f"Saldo: {acc['balance']} kr")
                print("-" * 20)
        
        elif val == "2":
            print("1. Debitkonto") # konstant ränta
            print("2. Sparkonto")
            print("3. Aktiefondkonto") # slumpad ränta
            typ_val = input("Välj typ: ")
            
            # matchar användarens val med rätt kontotyp
            if typ_val == "1": acc_type = "Debitkonto"
            elif typ_val == "2": acc_type = "Sparkonto"
            elif typ_val == "3": acc_type = "Aktiefondkonto"
            else:
                print("Ogiltigt val, inget konto skapades")
                continue
            
            accounts.create_account(user_id, acc_type, 0)
            print(f"{acc_type} har öppnats")
            
        elif val == "3":
            # updaterar när någon skrivit denna delen av koden
            print("Den här funktionen är under utveckling")
            pass
            
        elif val == "4":
            # updaterar när någon skrivit denna delen av koden
            print("Den här funktionen (graferna) är under utveckling")
            pass
            
        elif val == "5":
            print("Loggar ut")
            break
        else:
            print("Ogiltigt val, försök igen")

def main_menu():
    """Startmeny för programmet"""
    while True:
        print("\nVälkommen till internetbanken")
        print("1. Logga in")
        print("2. Skapa konto")
        print("3. Avsluta")
        
        val = input("Välj ett alternativ: ")
        
        if val == "1":
            u_id = input("Ange användar-id: ")
            pwd = input("Ange lösenord: ")
            
            # anropar validering i Filhantering.py
            if filhantering.check_login(u_id, pwd):
                print("Inloggning lyckades")
                user_dashboard(u_id)
            else:
                print("Felaktigt id eller lösenord")
                
        elif val == "2":
            f_name = input("Förnamn: ")
            l_name = input("Efternamn: ")
            pwd = input("Välj lösenord: ")
            
            # skapar användare och return id
            new_id = filhantering.create_user(f_name, l_name, pwd)
            
            # skapar ett debitkonto som default vid registrering, ändrar ksk sen
            # 
            accounts.create_account(new_id, "Debitkonto", 0)
            
            print(f"\nNytt konto skapat")
            print(f"Ditt användar-id är: {new_id}")
            print("Spara ID:t för framtida inloggning")

        elif val == "3":
            print("Tack för idag")
            break
        else:
            print("Ogiltigt val, försök igen")

if __name__ == "__main__":
    # startar menyn endast om filen körs direkt och inte vid import
    main_menu()