# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:42:35 2020

@author: stellajin
"""


import tushare as ts
import pandas as pd
import datetime
from tqdm import tqdm

def name(start_year, end_year):
    ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
    pro = ts.pro_api()
    name_year_list = dict()
    for year in range(start_year,end_year+1):
        name_list = dict()
        name_year_list[str(year)] = name_list
        begin = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 31)
        
        try:
            for i in tqdm(range((end - begin).days + 1)):
                day = begin + datetime.timedelta(days=i)
                trade_day = day.strftime('%Y%m%d')
                name_df = pro.hsgt_top10(trade_date = trade_day, market_type='1')
                if name_df.empty == False:
                    stock_name_list = name_df.name.values
                    for stock_name in stock_name_list:
                        if stock_name in list(name_list.keys()):
                            name_list[stock_name] += 1
                        else:
                            name_list[stock_name] = 1
        except Exception:
            break
    
    return name_year_list
    
        


if __name__ == "__main__":

    name_dict = name(2016,2020)
    for key in list(name_dict.keys()):
        file = open('../data/name/'+key+'_name_list.txt', 'w') 
        for k,v in name_dict[key].items():
            file.write(str(k)+' '+str(v)+'\n')
        file.close()