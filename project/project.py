
# AUTHOR: Matthew Frechette

import os
import requests

# Open High Low Close - stores the data of that current stock's day
class OHLC:

    # initiates the OHLC object, these will store the historical data from the stock
    def __init__ (self, open, high, low, close, month, day, year, hour=0, minute=0, volume=None):
        self.open = open
        self.high = high
        self.low = low 
        self.close = close
        self.month = month
        self.day = day
        self.year = year
        self.hour = hour
        self.minute = minute
        self.volume = volume

# stores data about a stock's earning, expected, actual, date, etc. 
class EarningsDay:

    def __init__ (self, month, day, year, eps, expectedEps=None, revenue=None, expectedRevenue=None):
        self.month = month
        self.day = day
        self.year = year
        self.eps = eps
        self.expectedEps = expectedEps
        self.revenue = revenue
        self.expectedRevenue = expectedRevenue

    
# returns a list of OHLC objects relative to the stock ticker
def FMPgetStockHistoricalData(stockTicker, apiKey):

    historicalDataUrl = "https://financialmodelingprep.com/api/v3/historical-price-full/" + stockTicker + "?apikey=" + apiKey

    try:
        historicalDataJSON = requests.get(historicalDataUrl).json()
        historicalDataJSON = historicalDataJSON["historical"] # gets all of the historical json data from the page
    except:
        return None

    
    historicalData = [] # list of OHLC objects
    for i in range(len(historicalDataJSON)):
        dayData = historicalDataJSON[i]

        date = dayData["date"]
        date = date.replace("-"," ").split()
        year = date[0]
        month = date[1]
        day = date[2]

        open = dayData["open"]
        high = dayData["high"]
        low = dayData["low"]
        close = dayData["close"]
        volume = dayData["volume"]

        historicalData.insert(0, OHLC(open, high, low, close, month, day, year, volume=volume))

    return historicalData # []


# typically, stocks are looked to be in an uptrend when the price of the equity is currently greater than the 20 and 50 period moving averages. 
# this function will help me get move information of the stocks and use it to compare another variable to the change in price during earnings
def calculateStockMovingAverage (listOfOHLC, period):

    listOfMovingAverages = [] # in the same order as the list of the OHLC history 
    # calculates the moving average of all the days
    currentMovingAverage = 0
    for i in range(period,len(listOfOHLC)):
        for p in range(1,period+1):
            currentMovingAverage += listOfOHLC[i-p].close
        currentMovingAverage /= period
        listOfMovingAverages += [currentMovingAverage]

    return listOfMovingAverages

# finds out whether of not the current stock price is above or below the N period moving average
def aboveMovingAverage (listOfOHLC, period):
    listOfMovingAverages = calculateStockMovingAverage(listOfOHLC, period)

    currentDayClose = listOfOHLC[-1].close
    if (currentDayClose > listOfMovingAverages[-1]):
        return True
    else:
        return False

def belowMovingAverage (listOfOHLC, period):
    if (aboveMovingAverage(listOfOHLC, period)):
        return False
    else:
        return True

def FMPfindStockEarningsData (stockTicker, apiKey):
    
    earningsURL = "https://financialmodelingprep.com/api/v3/historical/earning_calendar/AAPL?limit=80&apikey=" + apiKey

    try:
        earningsDataJSON = requests.get(earningsURL).json()
    except:
        return None
      
    allEarningsDays = [] # list holds all of the earningsday objects and returns them to the user
    for earningsData in earningsDataJSON:

        date = earningsData["date"]
        date = date.split("-")
        month = date[1]
        day = date[2]
        year = date[0]

        symbol = earningsData["symbol"] # this isn't used yet but as the program progresses I will also store the ticker name within these objects
        eps = earningsData["eps"] # earnings per share
        epsEstimate = earningsData["epsEstimated"]
        revenue = earningsData["revenue"]
        revenueEstimated = earningsData["revenueEstimated"]

        allEarningsDays.insert(0, EarningsDay(month, day, year, eps, epsEstimate, revenue, revenueEstimated))

    return allEarningsDays


if __name__ == "__main__":
    # main function
    
    apiKey = None
    # if there is an apikey file/data read from the file
    if (os.path.exists("apiKey.dat")): 
        file = open("apiKey.dat","r")
        apiKey = file.readline()
        file.close()
    # if there is no apikey file, ask the user and write to file
    else:
        apiKey = input("Enter your FMP API key:") 
        file = open("apiKey.dat","w")
        file.write(apiKey)
        file.close()
        
    

    # TESTING FUNCTIONS AS THEY ARE CREATED 

    # GATHERS THE STOCK DATA
    stockTicker = input("Enter a stock ticker: ") # asks the user for a stock ticker
    stockHistoricalData = FMPgetStockHistoricalData(stockTicker, apiKey) # gets all of the historical stock data
    
    # this doesn't go back all the way, while doing the full project we will pull data from the begining of the stock IPO
    print(len(stockHistoricalData), "data pieces found for", stockTicker) # returns the # of data points

    print("\n")

    # MOVING AVERAGES 
    # if the currentPriceIsAbove N periods of moving averages 
    if (aboveMovingAverage(stockHistoricalData, 20)): # 20 period MA
        print ("20 MA: ▲")
    else:
        print("20 MA: ▼")

    if (aboveMovingAverage(stockHistoricalData, 50)): # 20 period MA
        print ("50 MA: ▲")
    else:
        print("50 MA: ▼")

    print("\n")

    # EARNINGS DATA
    # gives a list of the most recent earnings from the stock that you picked
    allEarningsData = FMPfindStockEarningsData(stockTicker, apiKey)
    mostRecentEarningsData = allEarningsData[-1]
    print("The most recent earnings day was: " + mostRecentEarningsData.month + "-" + mostRecentEarningsData.day + "-" + mostRecentEarningsData.year)
    print("EPS:", mostRecentEarningsData.eps)
    print("Expected EPS:", mostRecentEarningsData.expectedEps)




    # below / further in the project I will be comparing price changes on the days that earnings released and see the changes in prices etc.
    # TO DO
    
    
    
    