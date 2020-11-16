# Stock Price Reactions to Earnings Announcements

Matthew Frechette, [fa20-523-336](https://github.com/cybertraining-dsc/fa20-523-336/), [Project.md](https://github.com/cybertraining-dsc/fa20-523-312/blob/master/project/project.md)


### I. Table of Contents
I. Table of Contents
II. INTRODUCTION  
III. BACKGROUND AND PREVIOUS WORK  
IV. THE DATA  
V. THE IDEA  
VI. THE PROCESS  
	• VI 1. Data Collection  
	• VI 2. Finding Earnings Data  
	• VI 3. Calculations and Results  
VII. THE RESULTS  
	• Test Results - Calculation1  
	• Full Results - Calculation2  
VIII. CONCLUSION  
IX. REFERENCES  
X. ACKNOWLEDGEMENTS  
	

### II. INTRODUCTION
For the final project I chose to do something that related to what is most interesting to me, and also something that is wildly popular in today’s world. The stock markets. Mathematicians and data scientists for decades upon decades have dedicated billions of dollars to study market patterns, movements, and company predictions. With the stock market providing so much potential for riches, it is no doubt that it has gained the attention and spending dollars of some of the most influential and richest companies in the world. Although this project comes nowhere near to what some hedge funds and data scientists are currently doing, my idea for the project was thought of in hopes to get a slightly better understanding on the ways the prices move after a company releases their earnings reports. Earnings reports are issued by companies after each fiscal quarter (4 months) and provide some interesting insight into how the company is doing, if they have improved, and whether or not they have reached their goals. Earnings also provide great opportunities for investors as they can find companies with good or bad earnings to profit off of (either short or long).
For this final project, I chose to do both a report and a piece of software as an undergraduate student, because I thought that writing the code and calculating the computations myself would make the project more interesting and hands on. I have always enjoyed coding and sitting down and writing software about a project allows me to grasp and understand the material at hand better than solely writing a report about data. 

### III. BACKGROUND AND PREVIOUS WORK
After reviewing other data studies and public ideas on the topic, I wasn’t able to find any major studies done specifically on the price reaction during earnings and get accurate results on the subject. Most of the studies that were done focused more on the technical side of price movements and price patterns, but not a lot on the fundamental earnings on a company. Back testing, is the act of testing a strategy in the past to see how it would perform. (Finding the success rate, return on investment, investment hold time, etc.) Since I was not particularly looking to find the best investment strategy, but to find how price and earnings announcements interact with one another, I chose not to incorporate a back testing strategy into my software, but use percentage test analysis and evaluate multiple areas of price changes during the earnings day. These tests were dependent on the trend of the stock price and the earnings results from the announcement. In addition to determining the price reaction from these announcements, it would also provide and insight into how buyer sentiment changes during these times as a price drop usually indicates negative buyer/investor interest in the security. 

### IV. THE DATA
For this project I chose to go with data from Financial Modeling Prep, or FMP as I refer to it in the code and documentation. Financial Modeling Prep is roughly a three-year-old internet company headquartered in France that provides financial data to other organizations around the globe. Their data is reliable and has a fast pull speed which allowed my software to capture company data quickly and efficiently. Additionally, since my company works with the FMP API, I am most familiar with which allowed me to access the data more quickly from the API that I needed due to familiarity. FMP supported all of the data requirements that I needed for this project: Company Historical Prices, Earnings Dates, Earnings per share, and company expected earnings.

### V. THE IDEA
Going into this project, I wanted to find a way to best measure and capture buyer / investor sentiment about a company but wasn’t sure exactly where to start. I had a wide range of ideas that included evaluating price changes due to executive changes, price changes during days of the week/month/year, and even price changes based on the weather that day. Although some ideas may have been more intricate and harder to calculate than others, I thought that the best idea to capture the sentiment of investors was to further investigate price changes in stocks around their earning dates. Many investors are hesitant to invest in companies in the short term during these periods as it is sometimes cause for uncertainty and harsh volatility in the stock’s price, but I figured that better understanding the price changes during earnings periods would help me become a better and more knowledgeable investor.
For this project I chose to look at markets as a whole and had the ability to access over 7000 US based stock’s data to get more broad and hopefully accurate results. The idea for the software included finding the historical stock price on the days that earnings were being released and capturing how the actual earnings per share (EPS) compared to the predicted earnings per share. If the actual EPS is equal to or greater than the predicted EPS that advisors publish, which is all public data, the stock price is thought to increase during the trading day. The program developed tested this theory. Additionally, I wanted to see how these stock prices were affected by stocks in certain trends. A stock is typically said to be in an uptrend if it is making higher highs, and high lows, and also above either the 20 period and 50 period moving averages. A stock making lower lows and lower highs it said to be in a downtrend. The software was able to capture this by comparing the stock’s historical price data and moving averages at the time of the earnings release. My original prediction was that stocks in an uptrend that underperformed on earnings would recover faster / have a lower loss% than that of stocks in a downtrend that underperformed on earnings. All of the resulting data is shown in the results section of this report. 

### VI. THE PROCESS 
1.	Data Collection  
The first and simplest part of the project was to gather the data from FMP. As this is a generally routine task and would need to be completed for every stock that was needed to be accessed, a function was created to move effectively gather this data. FMPgetStockHistoricalData(ticker, apiKey). The function took in a stock ticker and API key. The stock ticker must be reflective of a currently listed company on the one of the US stock-exchanges. For example, entering a company that has been delisted (STGC: Startech Global) would result in an invalid result. The function also requires an FMP API key which can be purchased with unlimited pull requests for less than $20/month. This function returns a list of OHLC objects which store the stock’s open, high, low and close prices for the day, in addition to the month day and year of the price data. This is incredibly valuable data as it allows the software quick access to specific days in the company’s history. 
2.	Finding Earnings Data  
Secondly, the earnings data from the company must be gathered, FMP has the ability to pull earnings results going back roughly 20 years depending on the company, this is more than adequate for this software as I will not solely be using the earnings reports from only one company or industry. After the earnings dates, eps, and expected eps is pulled from the API call, it is stored in an earningsData object which possessed the date, eps, expected eps, revenue, and expected revenue for that specific earning call. A function in the software called FMPfindStockEarningData() returns a list of all earningsData object for further analysis. 
3.	Calculations and Results  
	The final and most complex area of the software’s processes include the calculations and results formulations functions. This is where all of the company’s stock data is computed to better understand the price action after the company exhibits an earnings call. This function formulates 10 main calculations listed below:
	Finds the likelihood of a company beating earnings solely on what the trend of the stock is doing.
	This would be used to identify stocks that are projected to beat earnings based of the historical trend accuracy and price correlation. Using a strategy like this is not recommended and most likely will not be very accurate as a trend does not always correlate to the company actually being profitable.  
	   
	•	A. % of (+) beat earnings when the stock is in an uptrend  
	•	B. % of (-) missed earnings when the stock is in a downtrend  

	Finds the likelihood of a stock’s price movement based on earnings results
	Stocks the perform well (or beat earnings) are typically looked at by investors as buying opportunities, and thus the security’s price increases. This is not always the case however, and the results of this will be shown later in the report. Sometimes, investors project the stock to beat earnings by more than others and in turn find even some positive earnings results bearish. This can cause major stockholder to sell their shares and bring the price down.

	•	C. % of (+) beat earnings, where price increases from open  
	•	D. % of (+) beat earnings, where price increase from the previous day’s close  
	•	E. % of (-) missed earnings, where price decreases from open  
	•	F. % of (-) missed earnings, where price decreases from the previous day’s close  

	Finds the likelihood of a stock’s price movement based on earnings results and stock trend
	The final set of calculations the software is performing looks at all parts of the stock and its trend. It identifies the likelihood of a stock price increasing due to (+) beat or (-) missed earnings, while it is in a specific type of trend reflective of the earnings direction. This can be used by investors to find stocks in an uptrend or downtrend, who also want to play the earnings direction and try to profit from it.

	•	G. % of (+) beat earnings, where price increases from open and is in a current uptrend  
	•	H. % of (+) beat earnings, where price increases from the previous day’s close and is in an uptrend  
	•	I. % of (-) missed earnings, where price decreases from open and is in a current downtrend  
	•	J. % of (-) missed earnings, where price decreases from the previous day’s close and is in a downtrend  

### VII. THE RESULTS
For the first results scan I picked 5 popular companies within the S&P500, within the technology and energy sector. This first test was meant to get a baseline of calculations of strong stocks in this index and get an estimated calculation time for the operation. After running the first calculation I got the results as followed. The total calculation time clocked in at just over 8 seconds for the 5 stock calculations (1.6 seconds/stock). At this rate, calculating all 500 stocks from the S&P500 should take around 13:20 minutes. 


##### Test Results - Calculation1
Stocks Scanned: AAPL, MSFT, TWLO, GE, NVDA 
   
From the 5 stocks scanned, there were over 36,170 data points evaluated, 222 earnings beats, and 98 earnings misses. When stocks are in a current uptrend, the company is expected to beat earnings expectations 78.6% of the time, and when the stock is in a current downtrend the company is expected to miss earnings 59.7% of the time. This means that if the stock is in an uptrend, investors predicting a company will beat earnings would be correct more than 3/4 of the time. Of the stocks evaluated, if the company beat earnings, the price would increase from the open 42.3% of the time, and increase from the past close 61.3% of the time. Additionally, if a company missed earnings expectations, the stock price closed below the open 59% of the time, and below the previous close 60% of the time. This leads to the prediction that investors are more concerned about the company missing earnings, rather than the company beating earnings. The company missing earning expectations is more detrimental to the stock price than the company beating earnings recommendations. Lastly, of these 5 stocks, the price increases from open when earnings have been beat and the stock is in an uptrend 43.5% of the time. Notice since we added the uptrend filter on this scan, it results a higher calculation than calculation C. but only slightly. Stocks that are in an uptrend and beat earnings, increase from the previous close 63.9% of the time. Again, these results are only slightly higher than calculation D. If the stock is in a downtrend and the company misses earnings, the stock price will decrease from the open 60.1% of the time and will decrease from the previous close 54.3% of the time. This means that stocks that are in a downtrend and miss earnings, tend to actually have a spike up in premarket hours (before open 9:30amET) and then crash further throughout the day, since the decrease from open % is greater than the decrease from past close %.  
Below are test1 results formatted more neatly:  
  
•	Total Data Points Evaluated: 36,170  
•	Total Beat Earnings: 222  
•	Total Missed Earnings: 98  
•	Calculation Total in Seconds: 8  
•	A. % of (+) beat earnings when the stock is in an uptrend: 78.60%  
•	B. % of (-) missed earnings when the stock is in a downtrend: 59.74%  
•	C. % of (+) beat earnings, where price increases from open: 42.34%  
•	D. % of (+) beat earnings, where price increase from the previous day’s close: 61.26%  
•	E. % of (-) missed earnings, where price decreases from open: 59.18%  
•	F. % of (-) missed earnings, where price decreases from the previous day’s close: 60.2%  
•	G. % of (+) beat earnings, where price increases from open and is in a current uptrend: 43.46%  
•	H. % of (+) beat earnings, where price increases from the previous day’s close and is in an uptrend: 63.87%  
•	I. % of (-) missed earnings, where price decreases from open and is in a current downtrend: 60.87%  
•	J. % of (-) missed earnings, where price decreases from the previous day’s close and is in a downtrend: 54.35%  


##### Full Results - Calculation2
The final results scanned all stocks in the S&P500 and took roughly 17 minutes (1023 seconds in total). This was one of the things that originally surprised me as I thought that the calculations were going to take significantly less time based on the first test calculation done. The total data points scanned totaled 3.7 million. From the results gathered on the full results pull, I was able to identify the changes between the first test scan and the full scan. The calculation result percentages seemed to average out an begin to navigate towards the 50% or random mark, although there were a few scan results that yielded some potential advantage across the board.  
Below are the results of the full scan, and the result differences compared to the 5-stock scan above:  
  
•	Total Data Points Evaluated: 3,704,001  
•	Total Beat Earnings: 20,789 (62.3%)  
•	Total Missed Earnings: 12,577 (37.7%)  
•	Calculation Total in Seconds: 1023 (17 minutes)  
•	A. % of (+) beat earnings when the stock is in an uptrend: 61.6% (-17% difference)  
•	B. % of (-) missed earnings when the stock is in a downtrend: 34.54% (-25.2% difference)  
•	C. % of (+) beat earnings, where price increases from open: 51.8% (+9.46% difference)  
•	D. % of (+) beat earnings, where price increases from the previous day’s close: 56.74% (-4.52% difference)  
•	E. % of (-) missed earnings, where price decreases from open: 50.92% (-8.26% difference)  
•	F. % of (-) missed earnings, where price decreases from the previous day’s close: 56.92% (-3.28% difference)  
•	G. % of (+) beat earnings, where price increases from open and is in a current uptrend: 52.84% (+9.38% difference)  
•	H. % of (+) beat earnings, where price increases from the previous day’s close and is in an uptrend: 57.68% (-6.19% difference)  
•	I. % of (-) missed earnings, where price decreases from open and is in a current downtrend: 53.76% (-7.11% difference)  
•	J. % of (-) missed earnings, where price decreases from the previous day’s close and is in a downtrend: 58.48% (-4.13% difference)  
  
Although these results tend to show more randomness than the 5 scanned in the first results, there are a few scans that could yield a profitable and predictive strategy for investors, and or provide some insight into what the price of a security may do. One area where the software is still able to somewhat accurately able to predict events is in scan A, where we are evaluating the probability that the company will beat earning solely based on what the stock price trend is doing. If we only looked while investing in S&P500 stocks, an investor would be able to assume the company will beat earnings 61.6% of the time. Of these times, the stock price will increase from the past close 57.68% of the time.  

### VIII. CONCLUSION
To conclude, as more and more companies are evaluated in our softwares calculations, the change of unusual and unique events increase. Theoretically, if a company outperforms their expected earnings and shows number better than what financial advisors predict the company to earn, investors should be encouraged to buy more shares in the company and in turn drive the price of the security higher. Sometimes however, stock prices act in the opposite effect during earnings times as large hedge funds and corporations sell of large volume shares of stock during earnings times to fear other investors into selling and snowball the stock price down to where large institutions can repurchase massive amount of those shares again. (In a sort of dollar cost averaging method) Because of this, and many other market manipulation activities that occur on stock markets across the globe, positive earnings announcements do not always yield positive buyer sentiment. Concluded from this research, it can be said that the strongest correlation to a stock beating earnings estimates, is the price trend on the security. If the stock is in a current uptrend, the chance of that security beating earnings is over 60% (based on SP500 Stock Calculations) With this, earnings announcements are something that many investors should and could look at while investing both short term and long term in companies, however to develop a truly profitable trading strategy, more work and analysis would need to be included. The market moves in ways that few can truly explain, and as more stocks were scanned and analyzed, the randomness and factor of luck began to show through.

### IX. REFERENCES
[FinancialModelingPrep.com](https://www.financialmodelingprep.com)

### X. ACKNOWLEDGEMENTS
Thank you to Dr. Gregor Von Laszewski, Dr. Geoffrey Fox and all other AI staff that helped with the planning and teaching of the I423 class during the COVID-19 pandemic though the fall 2020 semester. This class helped allow me to better understand areas of big data and the science behind it. Additionally, the class gave me the ability to learn more about a topic that has been interesting to me and I am very grateful for that.  


