import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from curl_cffi import requests
import time

# skapar en session som imiterar en Chrome-webbläsare för att undvika att blockeras av Yahoo Finance
session = requests.Session(impersonate="chrome")

# simulerar börsen/aktiekurs med hjälp av Geometric Brownian Motion (GBM) med kursdata
def simulate_stock():
    # anger bakgrundsfärg för grafen
    bgColor = 'darkslategray'
    
    # loopar tills giltig input ges
    while True:
        # stockholmsbörsen används för simuleringen
        stockTicker = '^OMX'
        yearsData = input("Ange antal år av historisk data att använda (ex. 5): ")
        # ber användaren skriva in hur många år att simulera
        simHorizon = input("Ange antal år att simulera: ")
        # ber användaren skriva hur många utfall ska simuleras
        simNumber = input("Ange antal simuleringar: ")
        # try-except block för att fånga ogiltig input
        try:
            # omvandlar input till int
            simHorizon = int(simHorizon)
            simNumber = int(simNumber)
            yearsData = int(yearsData)
            # hämtar prisdata från OMX-index från Yahoo Finance
            prices = yf.download(stockTicker, period=f'{yearsData}y', interval="1d", threads = False, session = session)['Close']
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

    # startpris från datan, pris för sista datapunkten
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

    # genererar slumpade normalfördelade tal för varje tidssteg och simulering
    Z = np.random.standard_normal((numSteps, simNumber))
    # skapar en array för att lagra prisbanorna, där varje kolumn representerar en simulering
    pricePaths = np.zeros((numSteps+1, simNumber))
    # första raden i pricePaths är startpriset för alla simuleringar
    pricePaths[0, :] = S0
    # GBM
    dailyFactors = np.exp((my - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
 
    # simulerar prisbanorna genom att multiplicera det föregående priset med den dagliga faktorn
    for t in range(1, numSteps+1):
        pricePaths[t, :] = pricePaths[t-1, :] * dailyFactors[t-1, :]

    # plottar de simulerade prisbanorna tillsammans med den historiska datan
    plt.figure(figsize=(12, 6)).set_facecolor(bgColor)
    ax = plt.gca()
    ax.set_facecolor(bgColor)
    historicalPrices = prices.index
    plt.plot(historicalPrices, prices, color = 'blue', label = 'Historical Data')
    lastHistoricalDate = historicalPrices[-1]
    futureDates = pd.date_range(start=lastHistoricalDate, periods = numSteps + 1)[1:]

    # plottar simuleringar i rött eller grönt beroende på om priset gick upp eller ner jämfört med startpriset
    for i in range(simNumber):
        if pricePaths[-1, i] > pricePaths[0, i]:
            color = 'lime'  # price went up
        else:
            color = 'red'    # price went down
        plt.plot(futureDates, pricePaths[1:, i], color=color, alpha=0.5)
    plt.axvline(x=lastHistoricalDate, color='indigo', linestyle='--', label='Last Date From Dataset')
    plt.legend()
    plt.title(f"Simulering av {stockTicker} över {simHorizon} år med {simNumber} simuleringar")
    plt.show()

# uppdaterar ISK-kontot samt returnerar dagens procentändring för kursen
def update_ISK(kontoISK):
    # OMX indexets ticker symbol
    stockTicker = '^OMX'
    # Är börsen öppen?
    if time.localtime().tm_hour > 9 and time.localtime().tm_hour < 17.5:
        # Hämtar dagens pris för index/aktie
        todayPrice = yf.download(stockTicker, period=f'{2}d', interval="1d", threads = False, session = session)['Close']
        todayPercent = todayPrice.iloc[-1].item()/todayPrice.iloc[-2].item() - 1
        currency = yf.Ticker(stockTicker).info.get('currency', 'N/A')
        kontoISK *= (1 + todayPercent)
        return kontoISK, todayPercent