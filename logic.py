#Test
def summera_x_y(x,y):
    tot = x
    while x < y:
        x = x + 1
        tot = tot + x
    return tot

#Ränta på ränta
def ranta_pa_ranta(startkapital, ranta, ar):
    """
    startkapital: initialt belopp (t.ex. 1000)
    ranta: årlig ränta i procent (t.ex. 5 för 5%)
    ar: antal år (t.ex. 10)
    """
    slutbelopp = startkapital * (1 + ranta / 100) ** ar
    return slutbelopp