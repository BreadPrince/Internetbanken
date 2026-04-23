import Filhantering as filhantering  # Modul för användare och inlogg
import accounts # Modul för kontotyper och saldon
import logic # Modul för beräkningar
import primitiv_börs # Modul för aktiekurser och simuleringar
import datetime
import os
import history

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait():
    input("\nTryck Enter för att gå tillbaka")

today = "2026-04-16" #datetime.datetime.now().strftime("%Y-%m-%d")
lastISKdate = filhantering.read_date()

def user_dashboard(userId):

    # # uppdaterar ISK-kontot när programmet startas, och returnerar dagens procentändring för kursen
    # for account in accounts.get_accounts(userId):
    #     print(account["account_type"], account["balance"])
    #     if account["account_type"] == "Aktiefondkonto" and today != lastISKdate:
    #         iskChange = primitiv_börs.update_ISK(account["balance"])
    #         accounts.update_for_ISK(userId, iskChange[0])
    #         account["balance"] = iskChange[0]
    #         filhantering.update_date()
    #         print("Ditt ISK-konto har uppdaterats till " + str(iskChange[0]) + " kr" + "med kursen " + str(iskChange[1]))
    #     elif account["account_type"] == "Aktiefondkonto" and today == lastISKdate:
    #         print("Ditt ISK-konto är uppdaterat")

    """Meny för inloggad användare"""
    while True:
        clear_terminal()
        print(f"\nInloggad som: {userId}")
        print("1. Se konton och saldo")
        print("2. Öppna nytt konto")
        print("3. Insättning och uttag")
        print("4. Överföringar")
        print("5. Prognos verktyg")
        print("6. Visa transaktionshistorik")
        print("7. Logga ut")
        
        userChoice = input("Välj ett alternativ (1-7): ")
        
        if userChoice == "1":
            clear_terminal()
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
            wait()
        
        elif userChoice == "2":
            clear_terminal()
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
                wait()
                continue
            
            # Ska behålla följande del aktiv om vi ska implementera en maxgräns på 3 konton:
            result = accounts.create_account(userId, accountType, 0)
            if result == "success":
                print(f"Ett {accountType} har öppnats")
                wait()
            elif result == "limit":
                print("Fel: Du har redan nått maxantalet på 3 konton")
                wait()
            elif result == "duplicate":
                print(f"Fel: Du har redan ett {accountType}")
                wait()
            elif result =="invalid":
                print("Fel: Ogiltig kontotyp")
                wait()
            
        elif userChoice == "3":
            clear_terminal()

            userAccounts = accounts.get_accounts(userId)
            if not userAccounts:
                print("Du har inga konton")
                wait()
                continue

            # Visa konton
            print("\nDina konton:")
            for i, konto in enumerate(userAccounts):
                print(f"{i + 1}. {konto['account_type']} - {konto['balance']} kr")

            try:
                kontoVal = int(input("Välj konto: ")) - 1

                if kontoVal < 0 or kontoVal >= len(userAccounts):
                    print("Ogiltigt kontoval")
                    wait()
                    continue
                valtKonto = userAccounts[kontoVal]

            except:
                print("Ogiltigt val")
                wait()
                continue

            print("\n1. Insättning")
            print("2. Uttag")
            val = input("Välj: ")

            try:
                belopp = float(input("Ange belopp: "))
            except:
                print("Felaktigt belopp")
                wait()
                continue

            konto = float(valtKonto["balance"])

            # Anropa logic funktion
            if val == "1":
                nyttSaldo = logic.insattning(konto, belopp)
                history.add_history(userId, valtKonto["account_type"], belopp, "insättning")
            elif val == "2":
                if belopp > konto:
                    print("Otillräckligt saldo")
                    wait()
                    continue
                nyttSaldo = logic.uttag(konto, belopp)
                history.add_history(userId, valtKonto["account_type"], belopp, "uttag")
            else:
                print("Ogiltigt val")
                wait()
                continue

            # Uppdatera saldo
            valtKonto["balance"] = nyttSaldo

            # Spara ändringen
            allAccounts = accounts.load_accounts()

            for acc in allAccounts:
                if acc["user_id"] == userId and acc["account_type"] == valtKonto["account_type"]:
                    acc["balance"] = nyttSaldo

            accounts.save_accounts(allAccounts)

            print("\nTransaktion genomförd")
            print(f"Nytt saldo: {round(nyttSaldo, 2)} kr")
            wait()
            
        elif userChoice == "4":
            clear_terminal()
            # Updaterar när någon skrivit denna delen av koden
            primitiv_börs.simulate_stock()
            wait()
            continue

        elif userChoice == "5":
            while True:
                clear_terminal()
                print("1. Ränta på ränta")
                print("2. Börs simulering")
                print("3. Tillbaka")
        
                saveChoice = input("Välj ett alternativ (1-3): ")
        
                if saveChoice == "1":
                    clear_terminal()
                    userAccounts = accounts.get_accounts(userId)

                    # Filtrera fram endast sparkonton
                    sparkonton = [konto for konto in userAccounts if konto["account_type"] == "Sparkonto"]

                    if not sparkonton:
                        print("Du har inga sparkonton")
                        wait()
                        continue

                    # Visa sparkonton
                    print("\nDina sparkonton:")
                    for i, konto in enumerate(sparkonton):
                        print(f"{i + 1}. Saldo: {konto['balance']} kr")

                    try:
                        val = int(input("Välj sparkonto: ")) - 1

                        if val < 0 or val >= len(sparkonton):
                            print("Ogiltigt val")
                            wait()
                            continue

                        valtKonto = sparkonton[val]
                        startkapital = float(valtKonto["balance"])

                        ranta = float(input("Årlig ränta (%): "))
                        ar = int(input("Antal år: "))

                        # Anropa logic funktion
                        resultat = logic.ranta_pa_ranta(startkapital, ranta, ar)

                        print(f"\nStartkapital (från konto): {startkapital} kr")
                        print(f"Ränta: {ranta} %")
                        print(f"Antal år: {ar}")
                        print(f"Slutbelopp: {round(resultat, 2)} kr")
                        wait()

                    except:
                        print("Felaktig inmatning")
                        wait()

                elif saveChoice == "2":
                    clear_terminal()
                    primitiv_börs.simulate_stock()
        
                elif saveChoice == "3":
                    break
                else:
                    print("Ogiltigt val")
                    wait()

            continue
        elif userChoice == "6":
            clear_terminal()
            print("Din Transaktionshistorik\n")

            # Hämtar historik från history.py
            user_history = history.get_history(userId)
            
            if not user_history:
                print("Ingen historik hittades")
            else:
                for row in user_history:
                    print("-" * 30) 
                    print(f"Tid: {row['time']}")
                    print(f"Konto: {row['account_type']}")
                    print(f"Typ: {row['action']}")
                    print(f"Belopp: {row['amount']} kr")
                print("-" * 30) 
            wait()    
        elif userChoice == "7":
            print("Loggar ut")
            break

        else:
            print("Ogiltigt val, försök igen")

def main_menu():
    """Startmeny för programmet"""
    while True:
        clear_terminal()
        print("\nVälkommen till din internetbank")
        print("1. Logga in")
        print("2. Skapa konto")
        print("3. Avsluta")
        
        userChoice = input("Välj ett alternativ (1-3): ")
        
        if userChoice == "1":
            clear_terminal()
            print("Logga in")
            userId = input("Ange användar-id: ")
            password = input("Ange lösenord: ")
            
            # Anropar validering i Filhantering.py
            if filhantering.check_login(userId, password):
                print("Inloggning lyckades")
                user_dashboard(userId)
            else:
                print("Felaktigt id eller lösenord")
                wait()
                
        elif userChoice == "2":
            clear_terminal()
            print("Skapa nytt konto")
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
                    wait()
                elif status == "too_long":
                    print("Fel: Lösenordet är för långt")
                    wait()
                elif status == "ingen_bokstav":
                    print("Fel: Lösenordet måste innehålla minst en bokstav")
                    wait()
                elif status == "ingen_siffra":
                    print("Fel: Lösenordet måste innehålla minst en siffra")
                    wait()

            # Skapar användare och hämtar unikt id
            newId = filhantering.create_user(firstName, lastName, password)
            
            # Skapar ett debitkonto som default vid registrering
            accounts.create_account(newId, "Debitkonto", 0)
            
            print(f"\nNytt konto skapat. Du kan nu logga in.")
            print(f"Ditt användar-id är: {newId}")
            print("Spara ID:t för framtida inloggning")
            wait()

        elif userChoice == "3":
            clear_terminal()
            print("Avslutar programmet. Tack för idag")
            break
        else:
            print("Ogiltigt val, försök igen")
            wait()

if __name__ == "__main__":
    # Startar menyn endast om filen körs direkt och inte vid import
    main_menu()