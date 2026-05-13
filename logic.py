import primitiv_börs

#Ränta på ränta
def ranta_pa_ranta(startkapital, ranta, ar):
    """
    startkapital: initialt belopp (t.ex. 1000)
    ranta: årlig ränta i procent (t.ex. 5 för 5%)
    ar: antal år (t.ex. 10)
    """
    rantaGraf = []
    for i in range(ar):
        rantaGraf.append(startkapital)
        startkapital += startkapital * (ranta / 100)
    return rantaGraf

primitiv_börs.graf_för_ränta(ranta_pa_ranta(10000, 15, 10), 15)

#Sätta in på konto
def insattning(konto, belopp):
    """
    konto: välj konto
    belopp: ange belopp
    """
    if belopp <= 0:
        print("Beloppet måste vara större än 0.")
        return konto
    
    konto += belopp
    return konto

#Ta ut från konto
def uttag(konto, belopp):
    """
    konto: välj konto
    belopp: ange belopp
    """
    if belopp <= 0:
        print("Beloppet måste vara större än 0.")
        return konto
    
    if belopp > konto:
        print("Otillräckligt saldo.")
        return konto
    
    konto -= belopp
    return konto

#Överföring mellan konton
def overforing(fran_konto, till_konto, belopp):
    """
    fran_konto: konto för uttag
    till_konto: konto för insättning
    belopp: ange belopp
    """
    if belopp <= 0:
        print("Beloppet måste vara större än 0.")
        return fran_konto, till_konto
    
    if belopp > fran_konto:
        print("Otillräckligt saldo på frånkontot.")
        return fran_konto, till_konto
    
    fran_konto -= belopp
    till_konto += belopp
    
    return fran_konto, till_konto