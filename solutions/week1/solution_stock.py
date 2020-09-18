"""
Use this file to create functions to get stock universe.

"""

import tushare as ts
import datetime
import pandas as pd
from tqdm import tqdm

# set token
ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
# initialize pro api
pro = ts.pro_api()


def get_stock_list(path):
    df = pd.read_csv(path, index_col=0)
    return df.con_code.tolist()


def get_5_year_price_data(ts_code, start_date, end_date):
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date, adjfactor=True)
    return df


if __name__ == "__main__":
    # get date
    end_day = '20200831'
    start_day = '20150101'

    stock_list_path = '../../data/universe/hs300_stock.csv'
    stock_list = get_stock_list(stock_list_path)

    error_list = []
    for stock in tqdm(stock_list):
        try:
            price_data = get_5_year_price_data(stock, start_day, end_day)
            price_data.to_csv(f'solution_daily_price/{stock}.csv')
        except Exception as e:
            print(e)
            error_list.append(stock)
            print(error_list)

    if len(error_list) > 0:
        for stock in tqdm(error_list):
            price_data = get_5_year_price_data(stock, start_day, end_day)
            price_data.to_csv(f'solution_daily_price/{stock}.csv')
    else:
        print('Nice, all data pulled in one go!')