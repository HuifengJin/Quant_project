import tushare as ts
import datetime
import pandas as pd
from tqdm import tqdm
from pandas.tseries.offsets import BDay
from datetime import date, timedelta

# set token
ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
# initialize pro api
pro = ts.pro_api()


def get_stock_list(path):
    df = pd.read_csv(path, index_col=0)
    return df.con_code.tolist()


def price_daily_update(ts_code, start_day, end_day):

    old_data = pd.read_csv('{}{}.csv'.format('solution_daily_price/', ts_code), index_col=0)

    new_data = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_day, end_date=end_day, adjfactor=True)
    new_data = new_data.dropna(subset=['close'])

    today = date.today().strftime('%Y%m%d')
    new_data.to_csv(f'daily_update_cache/{today}_{ts_code}.csv')

    # Merge data, drop duplicates
    temp_df = pd.concat([new_data, old_data])
    temp_df['trade_date'] = temp_df['trade_date'].apply(str)
    data = temp_df.drop_duplicates(subset=['trade_date'], keep='first').reset_index(drop=True)

    return data


if __name__ == "__main__":
    # get date
    delta = 7
    end_date = date.today().strftime('%Y%m%d')
    start_date = (date.today() - datetime.timedelta(days=delta)).strftime('%Y%m%d')

    stock_list_path = '../../data/universe/hs300_stock.csv'
    stock_list = get_stock_list(stock_list_path)

    error_list = []
    for stock in tqdm(stock_list):
        try:
            price_data = price_daily_update(stock, start_date, end_date)
            price_data.to_csv(f'solution_daily_price/{stock}.csv')
        except Exception as e:
            print(e)
            error_list.append(stock)
            print(error_list)

    if len(error_list) > 0:
        for stock in tqdm(error_list):
            price_data = price_daily_update(stock, start_date, end_date)
            price_data.to_csv(f'solution_daily_price/{stock}.csv')
    else:
        print('Nice, all data pulled in one go!')