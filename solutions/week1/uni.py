"""
Use this file to create functions to get stock universe.

"""

import tushare as ts
import datetime

# set token
ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
# initialize pro api
pro = ts.pro_api()


def get_index_weight(index_code, start_date, end_date):
    # get recent 300 stocks
    df = pro.index_weight(index_code=index_code,
                          start_date=start_date.strftime('%Y%m%d'),
                          end_date=end_date.strftime('%Y%m%d'))

    # Get latest available date
    latest_date = df.trade_date[0]
    df = df[df.trade_date == latest_date]
    print(df.shape)

    return df


if __name__ == "__main__":
    # get date
    end_day = datetime.datetime.now()
    start_day = end_day + datetime.timedelta(days=-100)
    ticker = '399300.SZ'

    hs300 = get_index_weight(ticker, start_day, end_day)

    hs300.to_csv("../data/universe/hs300_stock.csv")
