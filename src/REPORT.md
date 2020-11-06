---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Portfolio Report
### Huifeng Jin


## Abstract
In this project, I select 20 stocks from the companies recorded in north money to form a portfolio. The idea behind is to use histroy data to predict which stock would perform better based on four indicators: net flow, money rank, change in price and moving average crossover times. The evalution method is comparing my portfolio with the benchmark HS300.


## I. Data Exploration
The database I use is [Tushare](https://tushare.pro/document/2), where I can get real time and various kinds of stock data. The way I fetch them is through tushare api with python:
1. hsgt_top10: get top 10 stock name list from north money, along with net_amount, change and rank.
2. index_daily: get data of HS300 stocks


## II. Data preprocessing
To avoid spending too much time on getting data from tushare api, I store the each year's top 10 stocks with how many times they appear on the list into txt files(from 2016 to 2019).Then, I select the top 35 stocks each year with highest frequency. A total of 61 stocks is chosen.

For dataframes obtained from api, I replace NaN with 0 for the convience of calculating return.


## III. Creating Portfolio
The main idea of creating this portfolio is using past 4 years' north money stock data to predict how they would perform in the following 2 months. In this project, I use data since 2016 to 2019 to predict performence from the beginning of January 2020 to the end of February 2020. With 4 indicators having different weights, a final score is calculated for each stock. 20 stocks with highest scores will be selected to form a portfolio.
### 1. Net Flow
    The net transaction amount is considered a important factor of a potential candidate is because net amount = active buying volume - active selling volume, a higher net amount shows that the market is optimistic about this company.
    
    After getting 4 years' net amount, I take the mean of them and standardize to [0,10].
    
### 2. Money Rank
    The rank indicator is the funds rank of the company ib the top 10 stock list. As more funds would better support a company's long-term development, I include it as a criterion of portfolio. I use take the average of 4 years' rank.
    
### 3. Change in Price
    The most obvious indicator of how a stock performs is its change in price. A positive value signifies that people can profit from this change. I sum up the 4 years' price change to generate a final amount.

### 4. Moving Average Crossover
    The last indicator is using the moving average crossover strategy to determine how many times a buy signal appears on a certain stock. I count the total buy signal over 4 years for each stock.

### 5. Total Score & Ranking
    I assign different weight to each indicator: net amount(0.3), rank(0.2), change(0.3), moving average crossover(0.2). These value are based on the importance of the indicator.
    
    When the final score is calculated, I sort the 61 stocks and choose the top 20 stocks into the portfolio.


## IV. Evaluation
The evaluation method is computing the return value of the 20 selected stocks, and compare it to the HS300 stocks return.

Portfolio stocks:

| code | name  | code | name   |
|------|------|------|------|
|  600048  | 保利地产|  600690  | 海尔智家|
|   601901  | 方正证券|  601668  | 中国建筑|
|   600585  | 海螺水泥|  600031 | 三一重工|
|   600029  | 南方航空|   603993  | 洛阳钼业|
|   600050  | 中国联通|   601888  | 中国中免|
|   600104  | 上汽集团|   600309  | 万华化学|
|   600036  | 招商银行|   600030  | 中信证券|
|   601138  | 工业富联|   600019  | 宝钢股份|
|   600519  | 贵州茅台|   600183  | 生益科技|
|   600741  | 华域汽车|   601318  | 中国平安|

The return of Portfolio and HS300:

<img src=../images/return_plot.jpg width=700>

We can see that Portfolio stocks have higher return in the first two, but lower return in the rest seven compared to HS300. 6 out of 20 portfolio stocks win the HS300 entirely, but the rest 14 stocks do not win HS300 in return.

The equity curve of Portfolio stocks:

<img src=../images/equity_curve.jpg width=700>

The total equity of 20 stocks decreases 7*10^8 to 6.4*10^8 from 2020/01/01 to 2020/02/28

If I buy 100 share of each stock in the portfolio, the price change in the two months:

<img src=../images/100share_price.jpg width=700>

I lose about 10000 yuan in total.


## V. Conclusion & Improvement
The portfolio I have created does not win the HS300, one reason could be that I use past 4 years' data to predict next 2 months, instead using past one year's data to predict next year might be more reasonable. Another reason is that we have COVID-19 pandemic in the biginning of 2020, which may add instability to the market, and I have not take this factor into consideration.

There are some improvements that can be made to create a better portfolio is to add background information as a criteria. For example, when the currenct trend is a specific field like technology or new energy automobile, we can add stocks in related fields into the portfolio. Also, the portfolio can be created dynamically. It can be updated every two months, replacing poor stocks with new candidates.
