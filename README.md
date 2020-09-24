# Assignment

- Week 1 - Warm Up:
    1. How git works and why it is crucial to learn git.
    2. First glimpse on Financial data for China Equity.
    3. First step to build a workable data pipeline.

- Assignment:
    1. Get yourself familiar with TuShare API and datasets.
    2. Get yourself familiar with git version control.
    3. Create a function to get hs300 stock dataframe and store it under /data/universe/ as csv
    4. Given a universe file, create a function to get daily stock price data and store them to /data/daily_price as csv
        - data of past 5 years is desirable
    5. Now you have stock price data of past 5 years, but you need a function to update them on daily base. Please create a function to update the files.
        - Please do not repeat previous steps to get full data, as getting 5-year data daily from API is slow and not optimal. 
        - There are several ways you could update the data, just pick up one that works for you.
    
- Bonus point:
    - How to check whether new data is loaded on server side before updating?
    - Be aware to avoid hard-coded parameters, such as date.
    - Get an idea of how long it takes to update data on daily base. 
    - How to deal with stock split, dividend, etc..

---

Week 2 - Build your trading signal(1):
##### In this week, you will learn to build a trading signal based on the data you gathered in week 1.
##### You may encounter several issues and you need to make sensible decisions in order to move forward.
##### Good luck!

- What we will cover:
    - what is MA/EMA, and in general how traders trade on it.
    - Extract EMA signals from data.
    - Calculate returns from data.
    - Combine to a panel data for further analysis.

- Signals we would like to capture:
    ![image info](images/iShot2020-09-1608.59.24.png)

- Assignment:
    1. Understand what is MA and how it works.
        - https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp#:~:text=The%20moving%20average%20(MA)%20is,time%20period%20the%20trader%20chooses.
    2. Understand what is EMA, and then install ta-lib package, use it to get EMA with price data.
        - https://github.com/mrjbq7/ta-lib
        - if ta-lib doesn't work on your computer, which happens time to time, you will have to calculate MA by yourself.
    3. Pick 中国平安 as example, calculate and append **EMA100** values
    4. Based on below conditions, create a new column called 'score_ema_100', in which value equals to 1 if signal detected, otherwise 0.
        - condition: (low <= EMA100) & (close >= EMA100) for a single day price
    5. Calculate and append return data
        - return calculation: t+x_return = ((t+x_close - t+1_open) / t+1_open) - 1
        - x = range(1,10)
    6. Combine price data, signal data, return data to a panel data, which will be used for further analysis.
        - I will show you an example of how it should look like.
    

---

Week 3 - Build your trading signal(2):
##### Last week, you built your first trading signal based on moving average, and applied it to ticker 601318.
##### This week, we will evaluate the signal.

- Assignment:
    1. Plot the return distribution. You could use Jupyter notebook.
    2. Calculate metrics
        - signal breath: number of time signal detected per month/year.
        - win rate: percentage of time signal produces positive return
        - biggest drawback: biggest negative return
        - avg return: average return
    3. Write a reusable class for step 2 and each metrics should be a method in the class.
    4. (extra) You can break down above metrics by year, month, to get more informed insight.
    5. (extra) You can also visualize the result by plotting. We will not cover visualization topics for now.
    
---

Week 4 - Mid-term recap and lecture:


Week 5 - Alternative data:
- TBD


Week 6 - Utilization of alternative data :
- TBD


Week 7 - Portfolio: 
- concept
- construct one


Week 8 - Capstone:
- TBD


