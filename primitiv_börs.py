import time
startTid = time.time()
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

bgColor = 'darkslategray'


while True:
    stockTicker = input("(q för att avsluta)\nAnge en aktieticker (ex. AAPL för Apple Inc.): ")
    if stockTicker == "q":
        print("Avslutar programmet.")
        exit()
    yearsData = input("Ange antal år av historisk data att använda (ex. 5): ")
    simHorizon = int(input("Ange antal år att simulera: ")) 
    simNumber = int(input("Ange antal simuleringar: "))
    try:
        prices = yf.download(stockTicker, period=f'{yearsData}y', interval="1d")['Close']
        if not prices.empty:
            break
        else:
            print("Ogiltig aktieticker. Försök igen.")
    except Exception:
        print(f"Fel vid hämtning av data. Försök igen.")

currency = yf.Ticker(stockTicker).info.get('currency', 'N/A')

logReturns = np.log(prices / prices.shift(1)).dropna()

# Parameters for GBM
S0 = prices.iloc[-1].item()                                        # initial stock price
simDays = 255                                   # number of trading days for a year   # number of years to simulate
my = (logReturns.mean() * simDays).item()       # expected return of the stock (drift)  
sigma = (logReturns.std() * np.sqrt(252)).item() # standard deviation of the stock's returns (volatility)
dt = 1/simDays    # Delta t (step for one year on the stock market (255 trading days))

numSteps = int(simHorizon/dt)

# price array
S = np.zeros(numSteps)
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
plt.show()


# dag = calendar.day_name[time.localtime().tm_wday]
# klockslag = f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
# datum = datetime.datetime.now(zoneinfo.ZoneInfo()).strftime("%Y-%m-%d")

# def rand_utveckling():
#     if random.randint(1, 20)+random.randint(1, 20) <35:
#         # slump procent
#         r = random.normal(loc=0, scale=0.0314, size = 1).item()
#     else:
#         r = random.normal(loc=0, scale=0.2, size = 1).item()
#     return r

# antalDagar = 255*3
# startKapital = 1000
# kapital = startKapital
# utvecklingKapital = np.zeros(antalDagar)
# insettningMånadsvis = 0

# for i in range(antalDagar):
#     print(f"{i%30}")    
#     if(i%30==0):
#         kapital *= (1+rand_utveckling())
#         kapital += insettningMånadsvis
#     else:
#         kapital *= (1+rand_utveckling())
#     utvecklingKapital[i] = kapital

print("Process finished --- %s seconds ---" % (time.time() - startTid))