# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 21:58:16 2020

@author: stellajin
"""

import tushare as ts
import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import ma_crossover
import matplotlib.pyplot as plt


ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
pro = ts.pro_api()

def get_north_stock(start_year, end_year):
    stock_set = set()
    for year in range(start_year,end_year+1):
        with open(str(year)+'_name_list.txt','r') as f:
            dic=[]
            for line in f.readlines():
                line=line.strip('\n')
                data=line.split(' ')
                dic.append(data)
            dic=dict(dic)
        sort_dict = sorted(dic.items(), key=lambda x: int(x[1]), reverse=True)
        top = sort_dict[0:36]
        for item in top:
            stock_set.add(item[0])
    return stock_set

def net_flow(ts_code):
    df = pro.hsgt_top10(ts_code=ts_code,start_date = '20160101', end_date='20191231', market_type='1')
    return np.mean(df.net_amount.values)

def cal_rank(ts_code):
    df = pro.hsgt_top10(ts_code=ts_code,start_date = '20160101', end_date='20191231', market_type='1')
    return np.mean(df['rank'])

def cal_change(ts_code):
    df = pro.hsgt_top10(ts_code=ts_code,start_date = '20160101', end_date='20191231', market_type='1')
    df = df.fillna(0)
    return sum(df.change.values)

def cal_ma(ts_code):
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date='20160101', end_date='20191231', adjfactor=True)
    s = ma_crossover.ma_crossover(df)
    return list(s.calculate_signal()).count(1)

def cal_score(net_flow_std,money_rank,change,ma_crossover):
    score = (net_flow_std*10)*0.3 + (10-money_rank)*0.2 + (change)*0.3 +(ma_crossover/10)*0.2
    return score


def select_stock(stocks):
    stock_df = pd.DataFrame(data=stocks, index=range(0,len(stocks)), columns=['ts_code'])
    stock_df['net_flow'] = stock_df.apply(lambda x: net_flow(x.ts_code),axis = 1)
    f = stock_df.net_flow.values
    stock_df['net_flow_std'] = (f - np.min(f)) / (np.max(f) - np.min(f))*10
    stock_df['rank'] = stock_df.apply(lambda x: cal_rank(x.ts_code),axis = 1)
    stock_df['change'] = stock_df.apply(lambda x: cal_change(x.ts_code),axis = 1)
    stock_df['ma_crossover'] = stock_df.apply(lambda x: cal_ma(x.ts_code),axis = 1)
    stock_df['score'] = stock_df.apply(lambda x: cal_score(x.net_flow_std,x['rank'],x.change,x.ma_crossover),axis = 1)
    return stock_df
        
def top_20_stocks(df):
    df = df.sort_values(by='score',ascending = False)
    df = df[0:20]
    
    return df.ts_code.values

def cal_return(df):
    df['date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
    df.set_index('date', inplace=True)
    df = df.iloc[::-1]
        
    for i in range(1, 1 + 1):
        df['t{}open'.format(str(i))] = df.open.shift(-i)
        for n in range(1, 10, 1):
            df['t{}_ret_on_t{}open'.format(str(n), str(i))] = (df.close.shift(-n) /
                                                               df['t{}open'.format(str(i))] - 1) * 100
    df = df.fillna(0)
    re_data = []
    for n in range(1, 10, 1):
        re_data.append(df['t{}_ret_on_t1open'.format(str(n))].mean())
    return np.array(re_data)
    
    

def update_top_20(start_date, end_date, old_stock, old_data, hs300):
    new_stock = set()
    begin = datetime.date(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:]))
    end = datetime.date(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]))
    
    for i in tqdm(range((end - begin).days + 1)):
        day = begin + datetime.timedelta(days=i)
        trade_day = day.strftime('%Y%m%d')
        name_df = pro.hsgt_top10(trade_date = trade_day, market_type='1')
        if name_df.empty == False:
            stock_name_list = name_df.ts_code.values
            for stock_name in stock_name_list:
                new_stock.add(stock_name)

    new = list()
    for stock in list(new_stock):
        if stock not in old_stock:
            new.append(stock)
    new_stock_data = select_stock(new)
    new_stock_data = new_stock_data.sort_values(by='score',ascending = False)
    
    #old worse than hs300, replace with new
    

if __name__ == "__main__":
    init_stocks = get_north_stock(2016,2019)

    stock_data = select_stock(init_stocks)
    
    stocks = top_20_stocks(stock_data)
    
    return_list = []
    for stock in stocks:
        df = ts.pro_bar(ts_code=stock, adj='qfq', start_date='20200101', end_date='20200230', adjfactor=True)
        re = cal_return(df)
        return_list.append(re)
    top20_result = np.array(return_list).mean(axis=0)
    
    hs300_df = pro.index_daily(ts_code = '399300.SZ',start_date='20200101', end_date='20200230')
    hs300_result = cal_return(hs300_df)
    print(stocks)
    print(return_list-hs300_result)
    print(hs300_result)
    
    #new_stocks = update_top_20('20200101', '20200230', stocks, return_list, hs300_result)
    

