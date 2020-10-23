# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:23:27 2020

@author: stellajin
"""


'''
招商银行 600036.SH
贵州茅台 600519.SH
中国平安 601318.SH
恒瑞医药 600276.SH
伊利股份 600887.SH
'''

import tushare as ts
import datetime
import pandas as pd
from tqdm import tqdm
from pandas.tseries.offsets import BDay
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import talib.abstract as ta

# set token
ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
# initialize pro api
pro = ts.pro_api()

def get_price_data(ts_code, start_date, end_date):
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date, adjfactor=True)
    df.to_csv(f'../data/stock_price_data/{ts_code}.csv')
    
def price_daily_update(ts_code, start_day, end_day):

    old_data = pd.read_csv('{}{}.csv'.format('../data/stock_price_data/', ts_code), index_col=0)

    new_data = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_day, end_date=end_day, adjfactor=True)
    new_data = new_data.dropna(subset=['close'])

    today = date.today().strftime('%Y%m%d')
    new_data.to_csv(f'../data/daily_update_cache/{today}_{ts_code}.csv')

    # Merge data, drop duplicates
    temp_df = pd.concat([new_data, old_data])
    temp_df['trade_date'] = temp_df['trade_date'].apply(str)
    data = temp_df.drop_duplicates(subset=['trade_date'], keep='first').reset_index(drop=True)

    return data

def sma_condition(sma25, sma100):
    if sma25 >= sma100:
        return 1
    else:
        return 0

def calculate_MA(df):
    df['sma25'] = ta.SMA(df, timeperiod=25, price='close')
    df['sma100'] = ta.SMA(df, timeperiod=100, price='close')
    df['sma_score'] = df.apply(lambda x: sma_condition(x.sma25,x.sma100),axis = 1)
    df['sma_signal'] = df['sma_score'].diff()
    return df

def send_email(ts_code_list,sender,receiver,password):
    for stock in tqdm(ts_code_list):
        fromaddr = sender
        password = password
        toaddrs = receiver
    
        #company info
        df1 = pro.stock_company(ts_code=stock)
        df1.to_csv(f'../data/stock_company_info/{stock}.csv')
        csvFile1 = f'../data/stock_company_info/{stock}.csv'
        csvApart1 = MIMEApplication(open(csvFile1, 'rb').read())
        csvApart1["Content-Disposition"] = 'attachment; filename="stock_company_info.csv"'
        #north data
        df2 = pro.hk_hold(trade_date=date.today().strftime('%Y%m%d'),ts_code=stock)
        df2.to_csv(f'../data/north_data/{stock}.csv')
        csvFile2 = f'../data/north_data/{stock}.csv'
        csvApart2 = MIMEApplication(open(csvFile2, 'rb').read())
        csvApart2["Content-Disposition"] = 'attachment; filename="north_data.csv"'
        #MA signal
        stock_price = pd.read_csv(f'stock_price_data/{stock}.csv', index_col=0)
        df3 = calculate_MA(stock_price)
        df3.to_csv(f'../data/ma_signal/{stock}.csv')
        csvFile3 = f'../data/ma_signal/{stock}.csv'
        csvApart3 = MIMEApplication(open(csvFile3, 'rb').read())
        csvApart3["Content-Disposition"] = 'attachment; filename="ma_signal.csv"'
        
        m = MIMEMultipart()
        m.attach(csvApart1)
        m.attach(csvApart2)
        m.attach(csvApart3)
        m['Subject'] = 'Daily report for '+ stock +' on '+ date.today().strftime('%Y%m%d')
        
        try:
            server = smtplib.SMTP()
            server.connect('smtp.163.com', '25')
            server.login(fromaddr,password)
            server.sendmail(fromaddr, toaddrs, m.as_string())
            print('success')
            server.quit()
        except smtplib.SMTPException as e:
            print('error:',e)
        

if __name__ == "__main__":
    
    ts_code_list = ['600036.SH', '600519.SH', '601318.SH', '600276.SH', '600887.SH']
    '''
    for ts_code in ts_code_list:
        price_data = get_price_data(ts_code,'20200101','20200930')
    '''
    
    # get date
    delta = 7
    end_date = date.today().strftime('%Y%m%d')
    start_date = (date.today() - datetime.timedelta(days=delta)).strftime('%Y%m%d')
        
    error_list = []
    for stock in tqdm(ts_code_list):
        try:
            price_data = price_daily_update(stock, start_date, end_date)
            price_data.to_csv(f'../data/stock_price_data/{stock}.csv')
        except Exception as e:
            print(e)
            error_list.append(stock)
            print(error_list)

    if len(error_list) > 0:
        for stock in tqdm(error_list):
            price_data = price_daily_update(stock, start_date, end_date)
            price_data.to_csv(f'../data/stock_price_data/{stock}.csv')
    else:
        print('Nice, all data pulled in one go!')
    
    sender = 'xxx@163.com'
    receiver = ['xxx@163.com']
    password = '****'
    send_email(ts_code_list,sender,receiver,password)
        
    