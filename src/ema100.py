# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 20:01:08 2020

@author: stellajin
"""

import pandas as pd
import talib.abstract as ta

def calculate_EMA(df, time_period, field):
    return ta.EMA(df, timeperiod=time_period, price=field)

def condition(low, close, ema):
    if low <= ema and close >= ema:
        return 1
    else:
        return 0

def calculate_score(df):
    df['score_ema_100'] = df.apply(lambda x: condition(x.low, x.close, x.ema100),axis = 1)
    return df

if __name__ == "__main__":
    
    stock_price = pd.read_csv("../data/daily_price/601318.SH.csv", index_col = 0)
    stock_price = stock_price.sort_index(ascending=False)
    
    EMA100 = calculate_EMA(stock_price, 100, 'close')
    stock_price['ema100'] = EMA100
    
    stock_price = calculate_score(stock_price)
    
    stock_price.to_csv('../data/trading_signal/ema100.csv', index=False)