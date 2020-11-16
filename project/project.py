
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

        self.movingAverage20 = None
        self.movingAverage50 = None

        return


# stores data about a stock's earning, expected, actual, date, etc. 
class EarningsDay:

    def __init__ (self, month, day, year, eps, time, expectedEps=None, revenue=None, expectedRevenue=None):
        self.month = month
        self.day = day
        self.year = year
        self.eps = eps
        self.expectedEps = expectedEps
        self.revenue = revenue
        self.expectedRevenue = expectedRevenue
        self.time = time

    
# returns a list of OHLC objects relative to the stock ticker
def FMPgetStockHistoricalData(stockTicker, apiKey):

    historicalDataUrl = "https://financialmodelingprep.com/api/v3/historical-price-full/" + stockTicker + "?timeseries=10000&apikey=" + apiKey

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

        # this is the OHLC object that will be inserted into the list
        ohlcData = OHLC(open, high, low, close, month, day, year, volume=volume)

        # checks to see if we can calculate the moving average for this data
        if (len(historicalData) >= 20): # perform 20 period moving average calc on this data piece
            ohlcData.movingAverage20 = getAverageOfClose(historicalData[-20:]) # gets the last 20 objects in the list

        if (len(historicalData) >= 50): # perform 50 period moving average calc on this data piece
            ohlcData.movingAverage50 = getAverageOfClose(historicalData[-50:]) # gets the last 50 objects in the list



        historicalData.insert(0, ohlcData)

    return historicalData # []


# gets the average close price of all data pieces in the list (used for moving average function within the data pull function)
def getAverageOfClose(listOfOHLC):
    total = 0
    average = 0
    lenOfList = len(listOfOHLC)
    for data in listOfOHLC:
        total += data.close

    average = total / lenOfList
    return average

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
    
    earningsURL = "https://financialmodelingprep.com/api/v3/historical/earning_calendar/" + stockTicker + "?limit=1000&apikey=" + apiKey

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
        time = earningsData["time"] # either AMC (after market close) or BMO (before market open)
        revenue = earningsData["revenue"]
        revenueEstimated = earningsData["revenueEstimated"]

        allEarningsDays.insert(0, EarningsDay(month, day, year, eps, time, epsEstimate, revenue, revenueEstimated))

    return allEarningsDays


def earningsCalculations (stockHistory, earningsHistory):

    earningsAndPriceChanges = []

    for earning in earningsHistory: # runs through all the earnings objects that the stock has
        for i in range(len(stockHistory)): # runs through all the stock days in order to find the day that the earning occured
            dayData = stockHistory[i]
            if (earning.day == dayData.day
                and earning.month == dayData.month
                and earning.year == dayData.year): # finding the earning day 
                if (earning.time == "bmo"): # before market open
                    # compare the past days close with the current day's open and close price
                    previousEarningsDayOHLC = stockHistory[i-1]
                    earningDayOHLC = dayData
                elif (earning.time == "amc"): # after market close
                    # compare the current days close with the next day's open and close prices
                    previousEarningsDayOHLC = dayData
                    earningDayOHLC = stockHistory[i+1] # if the earnings happens after the market closes then we want to see how the next day responds

                # here are the stats from the earning day
                changeFromPastClose = earningDayOHLC.close - previousEarningsDayOHLC.close
                changeFromOpen = earningDayOHLC.close - earningDayOHLC.open
                earningsAndPriceChanges += [[earning, dayData, changeFromPastClose, changeFromOpen]] 
                break

    # returns [[earningobj, OHLC from earning day, changeFromPastClose, changeFromOpen], ...]
    return earningsAndPriceChanges


    

    return None



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


    # EARNINGS DATA... CALCULATIONS
    # gives a list of the most recent earnings from the stock that you picked
    allEarningsData = FMPfindStockEarningsData(stockTicker, apiKey)
    mostRecentEarningsData = allEarningsData[-1]
    earningsCalcs = earningsCalculations(stockHistoricalData, allEarningsData)

    print("Total Earnings Data Found:", len(allEarningsData))
    print("Earnings Calculations Completed:", len(earningsCalcs)) # should result the same number as len(allEarningsData)
    #print("The most recent earnings day was: " + mostRecentEarningsData.month + "-" + mostRecentEarningsData.day + "-" + mostRecentEarningsData.year)
    #print("EPS:", mostRecentEarningsData.eps)
    #print("Expected EPS:", mostRecentEarningsData.expectedEps, "\n\n")

    inUptrend = [] # all the earnings days when the stock is in an uptrend
    inDowntrend = [] # all the earning days when the stock is in a downtrend

    print("Historical Earnings") # 26 total comparissons
    goodEarnings = [] # the earnings where the actual EPS is higher than the expected EPS
    goodEarningsPriceIncreaseFromOpen = [] # if we have good earnings, and the price of the stock increases from market open
    goodEarningsPriceIncreaseFromPastClose = [] # if we have good earnings, and the price of the stock increases from the last market days close
    goodEarningsPriceDecreaseFromOpen = [] # if we have good earnings, and the price of the stock decreases from the market open
    goodEarningsPriceDecreaseFromPastClose = [] # if we have good earnings, and the price of the stock decreases from the last market day close

    goodEarningsPriceIncreaseFromOpenUptrend = [] # if we have good earnings, price increase from open, and stock is in an uptrend
    goodEarningsPriceIncreaseFromPastCloseUptrend = [] # if we have good earnings, price increased from close, and stock is in an uptrend
    goodEarningsPriceIncreaseFromOpenDowntrend = [] # if we have good earnings, price increased from open, and stock is in a downtrend
    goodEarningsPriceIncreaseFromPastCloseDowntrend = [] # if we have good earnings, price increased from the past close, and the stock is in a downtrend
    goodEarningsPriceDecreaseFromOpenUptrend = [] # if we have good earnings, price decreases from open, and the stock is in an uptrend 
    goodEarningsPriceDecreaseFromPastCloseUptrend = [] # if we have good earnings, price decreases from past close, and the stock is in an uptrend
    goodEarningsPriceDecreaseFromOpenDowntrend = [] # if we have good earnings, price decreses from open, and the stock is in a downtrend
    goodEarningsPriceDecreaseFromPastCloseDowntrend = [] # if we have good earnings, price decreased from the past close, and the stock is in a downtrend

    goodEarningsUptrend = []
    goodEarningsDowntrend = []

    badEarnings = [] # earnings where actual EPS is lower than the expected EPS
    badEarningsPriceIncreaseFromOpen = [] # SEE DESCRIPTIONS ABOVE. 
    badEarningsPriceIncreaseFromPastClose = [] # ALL THESE FOR BAD EARNINGS
    badEarningsPriceDecreaseFromOpen = []
    badEarningsPriceDecreaseFromPastClose = []
    
    badEarningsPriceIncreaseFromOpenUptrend = []
    badEarningsPriceIncreaseFromPastCloseUptrend = []
    badEarningsPriceIncreaseFromOpenDowntrend = []
    badEarningsPriceIncreaseFromPastCloseDowntrend = []
    badEarningsPriceDecreaseFromOpenUptrend = []
    badEarningsPriceDecreaseFromPastCloseUptrend = []
    badEarningsPriceDecreaseFromOpenDowntrend = []
    badEarningsPriceDecreaseFromPastCloseDowntrend = []

    badEarningsUptrend = []
    badEarningsDowntrend = []

    # runs through all calculations of earnings days of the stock
    for earningData in earningsCalcs:

        earningDay = earningData[0] # returns the earnings days object, stores the day, time, expected eps etc
        ohlcData = earningData[1]
        changeFromPastClose = earningData[2] # gets the price change from the past close. This is useful becasue sometimes a stock will gap up during premarket trading
        changeFromOpen = earningData[3] # change during the open market hours

        # TYPICALLY, PRICES WILL MOVE UP WITH GOOD EARNINGS... HOWEVER THIS IS NOT ALWAYS THE CASE

        if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
            and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
            inUptrend += [earningData]
        else: # downtrend
            inDowntrend += [earningData]
            print(ohlcData.movingAverage20)
            print(ohlcData.movingAverage50)

        # GOOD EARNINGS! --- EPS is more than expected EPS 
        if (earningDay.eps > earningDay.expectedEps):
            goodEarnings += [earningData]

            if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                goodEarningsUptrend += [earningData]
            else: # downtrend
                goodEarningsDowntrend += [earningData]

            if (changeFromPastClose > 0): # (+) positive price change from last close (this includes the afterhours market)
                goodEarningsPriceIncreaseFromPastClose += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    goodEarningsPriceIncreaseFromPastCloseUptrend += [earningData]
                else: # downtrend
                    goodEarningsPriceIncreaseFromPastCloseDowntrend += [earningData]

            else: # (-) negative price movement from the last close (this includes the afterhours market)
                goodEarningsPriceDecreaseFromPastClose += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    goodEarningsPriceDecreaseFromPastCloseUptrend += [earningData]
                else: # downtrend
                    goodEarningsPriceDecreaseFromPastCloseDowntrend += [earningData]

            if (changeFromOpen > 0): # (+) positive price change from the current days open (this does not account from premarket activity / price gaps at open)
                goodEarningsPriceIncreaseFromOpen += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    goodEarningsPriceIncreaseFromOpenUptrend += [earningData]
                else: # downtrend
                    goodEarningsPriceIncreaseFromOpenDowntrend += [earningData]
            else:
                goodEarningsPriceDecreaseFromOpen += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    goodEarningsPriceDecreaseFromOpenUptrend += [earningData]
                else: # downtrend
                    goodEarningsPriceDecreaseFromOpenDowntrend += [earningData]


        # BAD EARNINGS! --- EPS is less than expected EPS 
        else: 
            badEarnings += [earningData]

            if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                badEarningsUptrend += [earningData]
            else: # downtrend
                badEarningsDowntrend += [earningData]

            if (changeFromPastClose > 0): # (+) positive price change from last close (this includes the afterhours market)
                badEarningsPriceIncreaseFromPastClose += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    badEarningsPriceIncreaseFromPastCloseUptrend += [earningData]
                else: # downtrend
                    badEarningsPriceIncreaseFromPastCloseDowntrend += [earningData]
            else: # (-) negative price movement from the last close (this includes the afterhours market)
                badEarningsPriceIncreaseFromPastClose += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    badEarningsPriceIncreaseFromPastCloseUptrend += [earningData]
                else: # downtrend
                    badEarningsPriceIncreaseFromPastCloseDowntrend += [earningData]

            if (changeFromOpen > 0): # (+) positive price change from the current days open (this does not account from premarket activity / price gaps at open)
                badEarningsPriceIncreaseFromOpen += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    badEarningsPriceIncreaseFromOpenUptrend += [earningData]
                else: # downtrend
                    badEarningsPriceIncreaseFromOpenDowntrend += [earningData]
            else:
                badEarningsPriceDecreaseFromOpen += [earningData]

                if (ohlcData.movingAverage20 != None and ohlcData.movingAverage20 > ohlcData.open
                    and ohlcData.movingAverage50 != None and ohlcData.movingAverage50 > ohlcData.open): # the stock is above the 20 and 50 moving average and is said to be in an uptrend
                    badEarningsPriceDecreaseFromOpenUptrend += [earningData]
                else: # downtrend
                    badEarningsPriceDecreaseFromOpenDowntrend += [earningData]


    
    # prints out the percentage of price increases/decrease to positive/negative earnings
    print("\n\n")

    print("Total Good Earnings:", len(goodEarnings))
    print("Total Bad Earnings:", len(badEarnings))
    
    percGoodEarningsUptrend = len(goodEarningsUptrend) / len(inUptrend) * 100
    print("% of beat earnings while stock is in an uptrend:", str(percGoodEarningsUptrend) + "%")
    percBadEarningsDowntrend = len(badEarningsDowntrend) / len(inDowntrend) * 100
    print("% of missed earnings while stock is in a downtrend:", str(percBadEarningsDowntrend) + "%")

    print("\n\n")

    percGoodEarningsPriceIncreaseOpen = len(goodEarningsPriceIncreaseFromOpen) / len(goodEarnings) * 100
    print("% of beat earnings where price increases from open:", str(percGoodEarningsPriceIncreaseOpen) + "%")
    percGoodEarningsPriceIncreasePreviousClose = len(goodEarningsPriceIncreaseFromPastClose) / len(goodEarnings) * 100
    print("% of beat earnings where price increases from previous close:", str(percGoodEarningsPriceIncreasePreviousClose) + "%")
    percBadEarningsPriceDecreaseOpen = len(badEarningsPriceDecreaseFromOpen) / len(badEarnings) * 100
    print("% of missed earnings where price decreases from open:", str(percBadEarningsPriceDecreaseOpen) + "%")
    percBadEarningsPriceDecreasePreviousClose = len(badEarningsPriceDecreaseFromPastClose) / len(badEarnings) * 100
    print("% of missed earnings where price decreases from previous close:", str(percBadEarningsPriceDecreasePreviousClose) + "%")

    print("\n\n")

    percGoodEarningsPriceIncreaseOpenUptrend = len(goodEarningsPriceIncreaseFromOpenUptrend) / len(goodEarningsUptrend) * 100
    print("% of beat earnings where price increases from open and is in uptrend:", str(percGoodEarningsPriceIncreaseOpenUptrend) + "%")
    percGoodEarningsPriceIncreasePreviousCLoseUptrend = len(goodEarningsPriceIncreaseFromPastCloseUptrend) / len(goodEarningsUptrend) * 100
    print("% of beat earnings where price increases from previous close and is in uptrend:", str(percGoodEarningsPriceIncreasePreviousCLoseUptrend) + "%")
    percBadEarningsPriceDecreaseOpenDowntrend = len(badEarningsPriceDecreaseFromOpenDowntrend) / len(badEarningsDowntrend) * 100 
    print("% of missed earnings where price decreases from open and is in downtrend:", str(percBadEarningsPriceDecreaseOpenDowntrend) + "%")
    percBadEarningsPriceDecreasePreviousCloseDowntrend = len(badEarningsPriceDecreaseFromPastCloseDowntrend) / len(badEarningsDowntrend) * 100
    print("% of missed earnings where price decreases from previous close and is in downtrend:", str(percBadEarningsPriceDecreasePreviousCloseDowntrend) + "%")




    # below / further in the project I will be comparing price changes on the days that earnings released and see the changes in prices etc.
    # TO DO
    
    
    
    