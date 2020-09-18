import pandas as pd
import talib as ta
import tushare as ts
from tqdm import tqdm

pd.set_option('display.max_columns', None)

# set token
ts.set_token('303f0dbbabfad0fd3f9465368bdc62fc775bde6711d6b59c2ca10109')
# initialize pro api
pro = ts.pro_api()


def get_transform_data(path):
    df = pd.read_csv(path, index_col=0)
    df['date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
    df.set_index('date', inplace=True)
    df = df.iloc[::-1]
    return df


def append_return(df, start=1, end=10, step=1, max_entry_delay=1):
    for i in range(1, max_entry_delay + 1):
        df['t{}open'.format(str(i))] = df.open.shift(-i)
        for n in range(start, end, step):
            df['t{}_ret_on_t{}open'.format(str(n), str(i))] = (df.close.shift(-n) / df[
                't{}open'.format(str(i))] - 1) * 100

    return df


# noinspection PyUnresolvedReferences
def calculate_signal(df, window):
    closed = df['close'].values
    df['ema' + str(window)] = ta.MA(closed, timeperiod=window, matype=1)

    # Condition
    df['ema_low<=ma' + str(window)] = df.low <= df['ema' + str(window)]
    df['ema_close>=ma' + str(window)] = df.close >= df['ema' + str(window)]

    # Combined Conditions
    df['ema_score_ma' + str(window)] = (df['ema_low<=ma' + str(window)] &
                                        df['ema_close>=ma' + str(window)]).astype(int)

    return df


if __name__ == "__main__":
    # 中国平安 601318
    ts_codes = ['601318.SH']

    for ts_code in tqdm(ts_codes):
        file_path = f'../week1/solution_daily_price/{ts_code}.csv'

        data = get_transform_data(file_path)

        # append signal
        win = 100
        data_w_signal = calculate_signal(data, window=win)

        # append returns
        data_panel = append_return(data_w_signal)

        data_panel.to_csv(f'panel_EMA/PANEL_{ts_code}.csv')
