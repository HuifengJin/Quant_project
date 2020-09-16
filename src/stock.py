"""
Use this file to create functions to get price data
"""

import tushare as ts
import datetime
import pandas as pd
from time import *

# initialize pro api
pro = ts.pro_api()

def get_daily_stock_price(path, start_date, end_date):
    
    #get ts_code
    hs300 = pd.read_csv(path)
    code_list = hs300.con_code.values
    
    #get past years daily stock price
    df = pd.DataFrame()
    for code in code_list:
        df = df.append(pro.daily(ts_code=code, start_date=start_date, end_date=end_date.strftime('%Y%m%d')),ignore_index=True)
    
    return df

def update_daily_stock_price(hs300_path, price_path, date):
    
    begin_time = time()
    
    #read original stock price and ts_code
    hs300 = pd.read_csv(hs300_path)
    code_list = hs300.con_code.values
    new_df = pd.read_csv(price_path, index_col = 0)
    
    #get today's data and choose those in hs300
    df = pro.daily(trade_date=date.strftime('%Y%m%d'))
    df = df[df.ts_code.isin(code_list)]
    new_df = new_df.append(df,ignore_index=True)
    new_df.to_csv(price_path)
    
    #calculate update time
    end_time = time()
    run_time = end_time-begin_time
    print("更新时间为：",run_time) #约5秒
    

if __name__ == "__main__":
    
    file_path = '../data/universe/hs300_stock.csv'
    end_date = datetime.datetime.now()
    years = 5
    #get start date
    start_date = str(end_date.year-years)+end_date.strftime('%Y%m%d')[-4:]
    
    daily_stock_price = get_daily_stock_price(file_path, start_date, end_date)
    daily_stock_price.to_csv('../data/daily_price/daily_stock_price.csv')