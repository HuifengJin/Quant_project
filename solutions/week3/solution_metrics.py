import pandas as pd
import talib as ta
import tushare as ts
from tqdm import tqdm

pd.set_option('display.max_columns', None)

# set token
ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
# initialize pro api
pro = ts.pro_api()


class SignalMetrics:

    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path
        self.data = self._get_data

    @property
    def _get_data(self):
        return pd.read_csv(self.file_path, index_col=0, parse_dates=True)

    def signal_breath_year(self):
        return self.data.groupby([self.data.index.year]).ema_score_ma100.sum()

    def signal_breath_month(self):
        return self.data.groupby([self.data.index.year, self.data.index.month]).ema_score_ma100.sum()

    def win_rate(self):
        cols = [f't{i}_ret_on_t1open' for i in range(1, 10)]
        df = self.data[self.data.ema_score_ma100 == 1][cols]
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


if __name__ == "__main__":
    # 中国平安 601318
    ts_codes = '601318.SH'
    panel_path = '../week2/panel_EMA/PANEL_601318.SH.csv'

    signal_metric = SignalMetrics(ts_codes, panel_path)

    # print out the metrics.
