import time
startTid = time.time()
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

bgColor = 'darkslategray'

def simulate_stock():
    while True:
        stockTicker = '^OMX'
        yearsData = input("(q för att avsluta) \n Ange antal år av historisk data att använda (ex. 5): ")
        if yearsData == "q":
            print("Avslutar programmet.")
            exit()
        # ber användaren skriva in hur många år att simulera
        simHorizon = input("Ange antal år att simulera: ")

        # ber användaren skriva hur många utfall ska simuleras
        simNumber = input("Ange antal simuleringar: ")

        try:
            # omvandlar input till int
            simHorizon = int(simHorizon)
            simNumber = int(simNumber)
            yearsData = int(yearsData)
            # hämtar prisdata från OMX index från Yahoo Finance
            prices = yf.download(stockTicker, period=f'{yearsData}y', interval="1d")['Close']
            # ifall data finns och input är korrekt, bryt
            if not prices.empty and isinstance(simHorizon, int)  and isinstance(simNumber, int):
                break
            # annars, be användaren att försöka igen
            else:
                print("\n Ogiltig input. Försök igen.")
        # fångar andra undantag
        except Exception:
            print(f"Fel vid hämtning av data. Försök igen.")

    # hämtar valuta för aktien/indexet
    currency = yf.Ticker(stockTicker).info.get('currency', 'N/A')

    # beräknar logaritmiska avkastningar
    # prices / prices.shift(1) ger prisförändringen i procent mellan varje element
    logReturns = np.log(prices / prices.shift(1)).dropna()

    # startpris från datan
    S0 = prices.iloc[-1].item()
    # antal handelsdagar per år
    simDays = 255
    # väntad vinst per år (drift)
    my = (logReturns.mean() * simDays).item()
    # standardavvikelse per år (volatilitet)
    sigma = (logReturns.std() * np.sqrt(252)).item()
    # Delta t, tidssteg per simDays
    dt = 1/simDays

    # antal tidssteg i simuleringen
    numSteps = int(simHorizon/dt)

    # gör array av nollor för att lagra simulerade priser i
    S = np.zeros(numSteps)
    # första elementet i arrayen är startpriset
    S[0] = S0

    Z = np.random.standard_normal((numSteps, simNumber))
    pricePaths = np.zeros((numSteps+1, simNumber))
    pricePaths[0, :] = S0
    dailyFactors = np.exp((my - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
 
    # Simulate stock price using Geometric Brownian Motion
    for t in range(1, numSteps+1):
        pricePaths[t, :] = pricePaths[t-1, :] * dailyFactors[t-1, :]

    plt.figure(figsize=(12, 6)).set_facecolor(bgColor)
    ax = plt.gca()
    ax.set_facecolor(bgColor)
    historicalPrices = prices.index
    plt.plot(historicalPrices, prices, color = 'blue', label = 'Historical Data')

    lastHistoricalDate = historicalPrices[-1]
    futureDates = pd.date_range(start=lastHistoricalDate, periods = numSteps + 1)[1:]

    # Plot price paths with color based on direction (up/down)
    for i in range(simNumber):
        if pricePaths[-1, i] > pricePaths[0, i]:
            color = 'lime'  # price went up
        else:
            color = 'red'    # price went down
        plt.plot(futureDates, pricePaths[1:, i], color=color, alpha=0.5)
    plt.axvline(x=lastHistoricalDate, color='indigo', linestyle='--', label='Last Date From Dataset')
    plt.legend()
    plt.title(f"Simulering av {stockTicker} över {simHorizon} år med {simNumber} simuleringar")

simulate_stock()
plt.show()

# dag = calendar.day_name[time.localtime().tm_wday]
# klockslag = f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
# datum = datetime.datetime.now(zoneinfo.ZoneInfo()).strftime("%Y-%m-%d")

print("Process finished --- %s seconds ---" % (time.time() - startTid))