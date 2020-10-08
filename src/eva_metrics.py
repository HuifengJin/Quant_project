# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:57:13 2020

@author: stellajin
"""

import pandas as pd

pd.set_option('display.max_columns', None)

class SignalMetrics:

    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path
        self.data = self._get_data

    @property
    def _get_data(self):
        return pd.read_csv(self.file_path, index_col=0, parse_dates=True)

    def signal_breath_year(self):
        return self.data.groupby([self.data.index.year]).overall_signal.sum()

    def signal_breath_month(self):
        return self.data.groupby([self.data.index.year, self.data.index.month]).overall_signal.sum()

    def win_rate(self):
        cols = [f't{i}_ret_on_t1open' for i in range(1, 10)]
        df = self.data[self.data.overall_signal == 1][cols]
        return df[df > 0].count()/len(df)

    def draw_back(self):
        cols = [f't{i}_ret_on_t1open' for i in range(1, 10)]
        return self.data[cols].min()

    def biggest_win(self):
        cols = [f't{i}_ret_on_t1open' for i in range(1, 10)]
        return self.data[cols].max()

    def avg_return(self):
        cols = [f't{i}_ret_on_t1open' for i in range(1, 10)]
        return self.data[cols].mean()
