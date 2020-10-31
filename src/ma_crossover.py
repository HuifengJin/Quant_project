
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:10:57 2020

@author: stellajin
"""
import pandas as pd
import talib.abstract as ta
import matplotlib.pyplot as plt

class ma_crossover:
    
    def __init__(self,df):
        self.df = df.fillna(0).sort_index(ascending = False)

    def calculate_SMA(self, time_period, field):
        return ta.SMA(self.df, timeperiod=time_period, price=field)
    
    def calculate_MACD(self, fastperiod, slowperiod, signalperiod, field):
        return ta.MACD(self.df[field],fastperiod = fastperiod,slowperiod = slowperiod,signalperiod = signalperiod)
    
    def calculate_RSI(self, time_period, field):
        return ta.RSI(self.df[field], timeperiod=time_period)
    
    def sma_condition(self,sma50, sma200):
        if sma50 >= sma200:
            return 1
        else:
            return 0
    
    def sma_price_condition(self,sma_signal, close, sma200):
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
        
    def macd_condition(self,macdhist):
        if macdhist >= 0:
            return 1
        else:
            return 0
    
    def rsi_condition(self,rsi):
        if rsi >= 70:
            return -1
        elif rsi <= 30:
            return 1
        else:
            return 0
    
    def overall_condition(self,sma_price_signal,macdhist_signal,rsi_signal):
        if sma_price_signal + macdhist_signal + rsi_signal > 0:
            return 1
        elif sma_price_signal + macdhist_signal + rsi_signal < 0:
            return -1
        else:
            return 0
    
    def calculate_signal(self):
        self.df['sma50'] = self.calculate_SMA(50, 'close')
        self.df['sma200'] = self.calculate_SMA(200, 'close')
        self.df['macd'],self.df['macdsignal'],self.df['macdhist'] = self.calculate_MACD(12,26,9,'close')
        self.df['rsi'] = self.calculate_RSI(12, 'close')
        self.df['sma_score'] = self.df.apply(lambda x: self.sma_condition(x.sma50,x.sma200),axis = 1)
        # 1 when sma50 become bigger then sma200
        # -1 when sma50 become smaller then sma200
        self.df['sma_signal'] = self.df['sma_score'].diff()
        self.df['sma_price_signal'] = self.df.apply(lambda x: self.sma_price_condition(x.sma_signal,x.close,x.sma200),axis = 1)
        
        self.df['macdhist_score'] = self.df.apply(lambda x: self.macd_condition(x.macdhist),axis = 1)
        self.df['macdhist_signal'] = self.df['macdhist_score'].diff()
        
        self.df['rsi_signal'] = self.df.apply(lambda x: self.rsi_condition(x.rsi),axis = 1)
        
        self.df = self.df.drop(columns=['sma_score', 'macdhist_score'])
        self.df['overall_signal'] = self.df.apply(lambda x: self.overall_condition(x.sma_price_signal,x.macdhist_signal,x.rsi_signal),axis = 1)
        
        return self.df.overall_signal.values

    
    
    
    