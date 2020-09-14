"""
Use this file to create functions to get stock universe.

"""

import tushare as ts
import datetime

#set token
ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
#initialize pro api
pro = ts.pro_api()

#get date
end_day = datetime.datetime.now()
start_day = end_day + datetime.timedelta(days = -100)

#get recent 300 stocks
df = pro.index_weight(index_code='399300.SZ', start_date=start_day.strftime('%Y%m%d'), end_date=end_day.strftime('%Y%m%d'))
hs300 = df[0:300]
hs300.to_csv("../data/universe/hs300_stock.csv")