from tqdm import tqdm_notebook  # (Optional, used for progress-bars)
from dateutil import parser
from datetime import timedelta, datetime
from binance.client import Client
from bitmex import bitmex
import datetime as dt
import time
import os.path
import math
import pandas as pd
import os
from tqdm import tqdm

# Source: https://medium.com/swlh/retrieving-full-historical-data-for-every-cryptocurrency-on-binance-bitmex-using-the-python-apis-27b47fd8137f
# IMPORTS
# API
bitmex_api_key = ''  # Enter your own API-key here
# Enter your own API-secret here
bitmex_api_secret = ''
# Enter your own API-key here
binance_api_key = ''
# Enter your own API-secret here
binance_api_secret = ''

# CONSTANTS
binsizes = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "2h": 120, "4h": 240, "1d": 1440}
batch_size = 750
bitmex_client = bitmex(test=False, api_key=bitmex_api_key,
                       api_secret=bitmex_api_secret)
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

def delete_last_row(timeframe="1d", currency="BTCUSDT"):
    filepath = "data/raw_history/crypto/"
    #filepath = ""
    ending = "-data.csv"
    complete = filepath + currency + "-" + timeframe + ending

    if os.path.isfile(complete):
        df = pd.read_csv(complete)
        df = df.iloc[:-10]
        print(f"removing last 10 rows...")
        df.to_csv(complete, index=None)
    else:
        print("error while deleting last rows")

# FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:
        old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance":
        old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    elif source == "bitmex":
        old = bitmex_client.Trade.Trade_getBucketed(
            symbol=symbol, binSize=kline_size, count=1, reverse=False).result()[0][0]['timestamp']
    if source == "binance":
        new = pd.to_datetime(binance_client.get_klines(
            symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    if source == "bitmex":
        new = bitmex_client.Trade.Trade_getBucketed(
            symbol=symbol, binSize=kline_size, count=1, reverse=True).result()[0][0]['timestamp']
    return old, new


def get_all_binance(symbol, kline_size, save=False):

    filepath = "data/raw_history/crypto/"
    filename = filepath + '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename):
        data_df = pd.read_csv(filename)
        data_df = data_df[:-10]
    else:
        data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(
        symbol, kline_size, data_df, source="binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'):
        print('Downloading all available %s data for %s. Be patient..!' %
              (kline_size, symbol))
    else:
        print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (
            delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime(
        "%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close',
                                         'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else:
        data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save:
        data_df.to_csv(filename)
    print('All caught up..!')
    return data_df


def get_all_bitmex(symbol, kline_size, save=False):
    filename = 'data/raw_history/crypto/%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename):
        data_df = pd.read_csv(filename)
        data_df = data_df[:-10]
    else:
        data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(
        symbol, kline_size, data_df, source="bitmex")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    rounds = math.ceil(available_data / batch_size)
    if rounds > 0:
        print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data in %d rounds.' % (
            delta_min, symbol, available_data, kline_size, rounds))
        for round_num in tqdm(range(rounds)):
            time.sleep(1)
            new_time = (oldest_point + timedelta(minutes=round_num *
                                                 batch_size * binsizes[kline_size]))
            data = bitmex_client.Trade.Trade_getBucketed(
                symbol=symbol, binSize=kline_size, count=batch_size, startTime=new_time).result()[0]
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)

    # Fredi START
    data_df['timestamp'] = pd.to_datetime(data_df['timestamp'], format='%Y-%m-%d %H:%M:%S+00:00').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Fredi END

    data_df.set_index('timestamp', inplace=True)

    if save and rounds > 0:
        data_df.to_csv(filename)
    print('All caught up..!')
    return data_df

# Fredi START
def refresh():
    binance_symbols = ["BTCUSDT", "ETHUSDT"]
    timeframes = ["1d", "4h", "1h"]
    #timeframes = ["1d", "4h", "2h", "1h", "30m"]
    timeframesbitmex = ["1d"]
    bitmex_symbols = ["XBT"]

    for symbol in binance_symbols:
        for time in timeframes:
            delete_last_row(time, symbol)
            get_all_binance(symbol, time, save=True)

def getBitmexWithBXB(symbol, time):
    filepath = "data/raw_history/crypto/"

    data = get_all_bitmex(symbol, time, save=False)
    bxbtDF = get_all_bitmex(".BXBT", time, save=False)

    # just selecting needed columns & changing their name
    bxbtDF = bxbtDF[['open', 'high', 'low', 'close']]
    bxbtDF = bxbtDF.rename(columns={"open": "BXBT_open", "high": "BXBT_high", "low": "BXBT_low", "close": "BXBT_close"})
    data = data.merge(bxbtDF, on='timestamp')
    data.to_csv(f"{filepath}{symbol}-{time}-data.csv")
    return data

def refreshall():
    binance_symbols = ["BTCUSDT", "ETHUSDT"]
    timeframes = ["1d", "4h", "1h", "30m", "15m", "5m"]
    timeframesbitmex = ["1d", "1h"]      # minimum is 1h
    # TODO Bitmex cant accept 4h candles --> compiler from 1h to 4h
    bitmex_symbols = ["XBT", "XBTU20"]
    bitmex_symbols = ["XBT"]

    for symbol in binance_symbols:
        for time in timeframes:
            delete_last_row(time, symbol)
            get_all_binance(symbol, time, save=True)

    for symbol in bitmex_symbols:
        for time in timeframesbitmex:
            delete_last_row(time, symbol)
            getBitmexWithBXB(symbol, time)

def refreshBitmex():
    timeframesbitmex = ["1d"]
    bitmex_symbols = ["XBT", ".BXBT", "XBTU20"]

    for symbol in bitmex_symbols:
        for time in timeframesbitmex:
            delete_last_row(time, symbol)
            get_all_bitmex(symbol, time, save=True)

def combineData(symbol1, symbol2, timeframe, deleteOldFiles=False):
    dfTEMP = pd.DataFrame()
    filepath = "data/raw_history/crypto/"
    df1 = pd.read_csv(f"{filepath}{symbol1}-{timeframe}-data.csv")
    df2 = pd.read_csv(f"{filepath}{symbol2}-{timeframe}-data.csv")
    names = ["timestamp", "symbol", "open", "high", "low", "close", "trades", "volume",
             "vwap", "lastSize", "turnover", "homeNotional", "foreignNotional"]

    dfTEMP["timestamp"] = df2["timestamp"]
    for name in names:
        # changing names to symbol1
        df1[f"{symbol1}111-{name}"] = df1[f"{name}"]

        # changing names to symbol2
        dfTEMP[f"{symbol2}-{name}"] = df2[f"{name}"]
        if name != "timestamp":
            df1 = df1.drop(columns=[f"{name}"])

        """        
        dfTEMP = pd.concat([dfTEMP, df1[f"{name}"]])
        dfTEMP = dfTEMP.rename(columns={f"{name}": f"{symbol1}-{name}"}, inplace=True)

        dfTEMP = pd.concat([dfTEMP, df2[f"{name}"]])
        dfTEMP = dfTEMP.rename(columns={f"{name}": f"{symbol2}-{name}"}, inplace=True)
        """

    df1 = df1.merge(dfTEMP, on="timestamp")
    print(f"saving combined data with name: {filepath}{symbol1}+{symbol2}-{timeframe}-data.csv")
    df1.to_csv(f"{filepath}{symbol1}+{symbol2}-{timeframe}-data.csv")
    print(f"finished saving file")

    if deleteOldFiles:
        os.remove(f"{filepath}{symbol1}-{timeframe}-data.csv")
        os.remove(f"{filepath}{symbol2}-{timeframe}-data.csv")



if __name__ == "__main__":
    refreshall()
    #refreshBitmex()
    #combineData("XBT", ".BXBT", "1d")

    # Fredi END