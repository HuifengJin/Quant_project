# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:58:12 2020

@author: stellajin
"""

import pandas as pd
import talib.abstract as ta
import eva_metrics

def calculate_SMA(df, time_period, field):
    return ta.SMA(df, timeperiod=time_period, price=field)

def calculate_MACD(df, fastperiod, slowperiod, signalperiod, field):
    return ta.MACD(df[field],fastperiod = fastperiod,slowperiod = slowperiod,signalperiod = signalperiod)

def calculate_RSI(df, time_period, field):
    return ta.RSI(df[field], timeperiod=time_period)

def sma_condition(sma50, sma200):
    if sma50 >= sma200:
        return 1
    else:
        return 0

def sma_price_condition(sma_signal, close, sma200):
    if sma_signal == 1:
        if close < sma200:
            return 0
        else:
            return 1
    elif sma_signal == -1:
        if close >= sma200:
            return 0
        else:
            return -1
    else:
        return 0
    
def macd_condition(macdhist):
    if macdhist >= 0:
        return 1
    else:
        return 0

def rsi_condition(rsi):
    if rsi >= 70:
        return -1
    elif rsi <= 30:
        return 1
    else:
        return 0

def overall_condition(sma_price_signal,macdhist_signal,rsi_signal):
    if sma_price_signal + macdhist_signal + rsi_signal > 0:
        return 1
    elif sma_price_signal + macdhist_signal + rsi_signal < 0:
        return -1
    else:
        return 0

def calculate_signal(df):
    df['sma_score'] = df.apply(lambda x: sma_condition(x.sma50,x.sma200),axis = 1)
    # 1 when sma50 become bigger then sma200
    # -1 when sma50 become smaller then sma200
    df['sma_signal'] = df['sma_score'].diff()
    df['sma_price_signal'] = df.apply(lambda x: sma_price_condition(x.sma_signal,x.close,x.sma200),axis = 1)
    
    df['macdhist_score'] = df.apply(lambda x: macd_condition(x.macdhist),axis = 1)
    df['macdhist_signal'] = df['macdhist_score'].diff()
    
    df['rsi_signal'] = df.apply(lambda x: rsi_condition(x.rsi),axis = 1)
    
    df = df.drop(columns=['sma_score', 'macdhist_score'])
    df['overall_signal'] = df.apply(lambda x: overall_condition(x.sma_price_signal,x.macdhist_signal,x.rsi_signal),axis = 1)
    return df

if __name__ == "__main__":
    stock_price = pd.read_csv('../data/panel_data/ema100.csv', index_col=0)
    stock_price = stock_price.drop(columns=['ema100', 'score_ema_100'])

    stock_price['sma50'] = calculate_SMA(stock_price, 50, 'close')
    stock_price['sma200'] = calculate_SMA(stock_price, 200, 'close')
    stock_price['macd'],stock_price['macdsignal'],stock_price['macdhist'] = calculate_MACD(stock_price,12,26,9,'close')
    stock_price['rsi'] = calculate_RSI(stock_price, 12, 'close')
    
    stock_price = calculate_signal(stock_price)
    
    stock_price.to_csv('../data/panel_data/ma_crossover_signal.csv', index=False)
    
    # evaluation
    signal_metric = eva_metrics.SignalMetrics('601318.SH','../data/panel_data/ma_crossover_signal.csv')
    print(signal_metric.win_rate())
    
    