# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:41:36 2020

@author: stellajin
"""

import numpy as np
import pandas as pd

class stock_metrics:
    def __init__(self,df):
        self.DF = df.fillna(0)
        
    def signal_breath(self):
        signal = dict()
        for index, row in self.DF.iterrows():
            mon_year = str(row.trade_date)[0:6]
            if row.score_ema_100 == 1:
                if mon_year in list(signal.keys()):
                    signal[mon_year] += 1
                else:
                    signal[mon_year] = 1
            else:
                if mon_year not in list(signal.keys()):
                    signal[mon_year] = 0
        print(signal)
        
    def win_rate(self):
        signal_list = self.DF.score_ema_100.values
        win = np.count_nonzero(signal_list)/signal_list.size
        print(win)
        
    def biggest_drawback(self, time_period):
        drawback = dict()
        min_ret = self.DF.iloc[:,-9:].min(axis = 1)
        tp = ''
        
        for index, row in self.DF.iterrows():
            if time_period == 'year':
                tp = str(row.trade_date)[0:4]
            elif time_period == 'month':
                tp = str(row.trade_date)[0:6]
                
            if tp in list(drawback.keys()):
                drawback[tp].append(min_ret[index])
            else:
                drawback[tp] = [min_ret[index]]
                
        for key, value in drawback.items():
            drawback[key] = np.min(value)
        
        print(drawback)
        
    def avg_return(self, time_period):
        avg_ret = dict()
        avg = self.DF.iloc[:,-9:].mean(axis = 1)
        tp = ''
        
        for index, row in self.DF.iterrows():
            if time_period == 'year':
                tp = str(row.trade_date)[0:4]
            elif time_period == 'month':
                tp = str(row.trade_date)[0:6]
            
            if tp in list(avg_ret.keys()):
                avg_ret[tp].append(avg[index])
            else:
                avg_ret[tp] = [avg[index]]
        
        for key, value in avg_ret.items():
            avg_ret[key] = np.mean(value)
        
        print(avg_ret)

if __name__ == "__main__":
    stock_price = pd.read_csv('../data/panel_data/ema100.csv')
    
    metrics = stock_metrics(stock_price)
    
    metrics.signal_breath()
    metrics.win_rate()
    metrics.biggest_drawback('year')
    metrics.biggest_drawback('month')
    metrics.avg_return('year')
    metrics.avg_return('month')
    