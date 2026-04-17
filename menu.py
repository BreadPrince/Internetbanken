import Filhantering as filhantering  # Modul för användare och inlogg
import accounts # Modul för kontotyper och saldon
import logic # Modul för beräkningar

def user_dashboard(userId):
    """Meny för inloggad användare"""
    while True:
        print(f"\nInloggad som: {userId}")
        print("1. Se konton och saldo")
        print("2. Öppna nytt konto")
        print("3. Insättning och uttag")
        print("4. Visa grafer")
        print("5. Logga ut")
        
        userChoice = input("Välj ett alternativ (1-5): ")
        
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
            typeChoice = input("Välj typ (1-3): ")
            
            # Matchar användarens val med rätt kontotyp
            if typeChoice == "1": accountType = "Debitkonto"
            elif typeChoice == "2": accountType = "Sparkonto"
            elif typeChoice == "3": accountType = "Aktiefondkonto"
            else:
                print("Ogiltigt val, inget konto skapades")
                continue
            
            # Ska behålla följande del aktiv om vi ska implementera en maxgräns på 3 konton:
            result = accounts.create_account(userId, accountType, 0)
            if result == "success":
                print(f"Ett {accountType} har öppnats")
            elif result == "limit":
                print("Fel: Du har redan nått maxantalet på 3 konton")
            elif result == "duplicate":
                print(f"Fel: Du har redan ett {accountType}")
            elif result =="invalid":
                print("Fel: Ogiltig kontotyp")
            
        elif userChoice == "3":
            userAccounts = accounts.get_accounts(userId)

            if not userAccounts:
                print("Du har inga konton")
                continue

            # Visa konton
            print("\nDina konton:")
            for i, konto in enumerate(userAccounts):
                print(f"{i + 1}. {konto['account_type']} - {konto['balance']} kr")

            try:
                kontoVal = int(input("Välj konto: ")) - 1

                if kontoVal < 0 or kontoVal >= len(userAccounts):
                    print("Ogiltigt kontoval")
                    continue

                valtKonto = userAccounts[kontoVal]
            except:
                print("Ogiltigt val")
                continue

            print("\n1. Insättning")
            print("2. Uttag")
            val = input("Välj: ")

            try:
                belopp = float(input("Ange belopp: "))
            except:
                print("Felaktigt belopp")
                continue

            konto = float(valtKonto["balance"])

            # Anropa logic funktion
            if val == "1":
                nyttSaldo = logic.insattning(konto, belopp)
            elif val == "2":
                if belopp > konto:
                    print("Otillräckligt saldo")
                    continue
                nyttSaldo = logic.uttag(konto, belopp)
            else:
                print("Ogiltigt val")
                continue

            # Uppdatera saldo
            valtKonto["balance"] = nyttSaldo

            # Spara ändringen
            accounts.save_accounts(userAccounts)

            print("\nTransaktion genomförd")
            print(f"Nytt saldo: {round(nyttSaldo, 2)} kr")
            
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
        
        userChoice = input("Välj ett alternativ (1-3): ")
        
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
                    print("Lösenord godkänt. Spara det för framtida inloggning")
                    break # loopen bryts endast när status är valid
                elif status == "too_short":
                    print("Fel: Lösenordet är för kort")
                elif status == "too_long":
                    print("Fel: Lösenordet är för långt")
                elif status == "ingen_bokstav":
                    print("Fel: Lösenordet måste innehålla minst en bokstav")
                elif status == "ingen_siffra":
                    print("Fel: Lösenordet måste innehålla minst en siffra")

            # Skapar användare och hämtar unikt id
            newId = filhantering.create_user(firstName, lastName, password)
            
            # Skapar ett debitkonto som default vid registrering
            accounts.create_account(newId, "Debitkonto", 0)
            
            print(f"\nNytt konto skapat. Du kan nu logga in.")
            print(f"Ditt användar-id är: {newId}")
            print("Spara ID:t för framtida inloggning")

        elif userChoice == "3":
            print("Avslutar programmet. Tack för idag")
            break
        else:
            print("Ogiltigt val, försök igen")

if __name__ == "__main__":
    # Startar menyn endast om filen körs direkt och inte vid import
    main_menu()