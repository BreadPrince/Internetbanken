import Filhantering as filhantering  # Modul för användare och inlogg
import accounts # Modul för kontotyper och saldon
import logic # Modul för berävningar

def user_dashboard(userId):
    """Meny för inloggad användare"""
    while True:
        print(f"\nInloggad som: {userId}")
        print("1. Se konton och saldo")
        print("2. Öppna nytt konto")
        print("3. Insättning och uttag")
        print("4. Visa grafer")
        print("5. Logga ut")
        
        userChoice = input("Välj ett alternativ: ")
        
        if userChoice == "1":
            print(f"\nDina aktiva konton")

            # Hämtar data från accounts.py
            userAccounts = accounts.get_accounts(userId)
            if not userAccounts:
                print("Inga aktiva konton hittades")
            else:
                for account in userAccounts:
                    # Skriver ut varje konto på egna rader med skilje-streck emellan
                    print("-" * 20)
                    print(f"Konto: {account['account_type']}")
                    print(f"Saldo: {account['balance']} kr")
                print("-" * 20)
        
        elif userChoice == "2":
            print(f"\nÖppna nytt konto")
            print("1. Debitkonto")
            print("2. Sparkonto")
            print("3. Aktiefondkonto")
            typeChoice = input("Välj typ: ")
            
            # Matchar användarens val med rätt kontotyp
            if typeChoice == "1": accountType = "Debitkonto"
            elif typeChoice == "2": accountType = "Sparkonto"
            elif typeChoice == "3": accountType = "Aktiefondkonto"
            else:
                print("Ogiltigt val, inget konto skapades")
                continue
            
            # ska ta bort följande rad om vi ska implementera en maxgräns på 3 konton
            # accounts.create_account(userId, accountType, 0)

            # ska göra följande del aktiv om vi ska implementera en maxgräns på 3 konton
            result = accounts.create_account(userId, accountType, 0)
            if result == "success":
                print("ett {accountType} har öppnats")
            elif result == "limit":
                print("du har redan nått maxantalet på 3 konton")
            elif result == "duplicate":
                print("du har redan ett {accountType}")
            elif result =="invalid":
                print("ogiltigkontotyp")
                
            # ska ta bort följande rad om vi ska implementera en maxgräns på 3 konton
            # print(f"{accountType} har öppnats")
            
        elif userChoice == "3":
            # Updaterar när någon skrivit denna delen av koden
            print("Den här funktionen är under utveckling")
            pass
            
        elif userChoice == "4":
            # Updaterar när någon skrivit denna delen av koden
            print("Den här funktionen (graferna) är under utveckling")
            pass
            
        elif userChoice == "5":
            print("Loggar ut")
            break
        else:
            print("Ogiltigt val, försök igen")

def main_menu():
    """Startmeny för programmet"""
    while True:
        print("\nVälkommen till din internetbank")
        print("1. Logga in")
        print("2. Skapa konto")
        print("3. Avsluta")
        
        userChoice = input("Välj ett alternativ: ")
        
        if userChoice == "1":
            userId = input("Ange användar-id: ")
            password = input("Ange lösenord: ")
            
            # Anropar validering i Filhantering.py
            if filhantering.check_login(userId, password):
                print("Inloggning lyckades")
                user_dashboard(userId)
            else:
                print("Felaktigt id eller lösenord")
                
        elif userChoice == "2":
            firstName = input("Förnamn: ")
            lastName = input("Efternamn: ")

            while True:
                password = input("Välj lösenord (6-10 tecken, minst 1 bokstav, och 1 siffra): ")
                # Anropar funktionen validate_password från Filhantering.py:
                status = filhantering.validate_password(password)

                if status == "valid":
                    print("Lösenord godkänt.Spara det för framtida inloggning")
                    break # loopen bryts endast när status är valid
                elif status == "too_short":
                    print("Lösenordet är för kort")
                elif status == "too_long":
                    print("Lösenordet är för långt")
                elif status == "ingen_bokstav":
                    print("Lösenordet måste innehålla minst en bokstav")
                elif status == "ingen_siffra":
                    print("Lösenordet måste innehålla minst en siffra")

            # Skapar användare och hämtar unikt id
            newId = filhantering.create_user(firstName, lastName, password)
            
            # Skapar ett debitkonto som default vid registrering
            accounts.create_account(newId, "Debitkonto", 0)
            
            print(f"\nNytt konto skapat")
            print(f"Ditt användar-id är: {newId}")
            print("Spara ID:t för framtida inloggning")

        elif userChoice == "3":
            print("Tack för idag")
            break
        else:
            print("Ogiltigt val, försök igen")

if __name__ == "__main__":
    # Startar menyn endast om filen körs direkt och inte vid import
    main_menu()