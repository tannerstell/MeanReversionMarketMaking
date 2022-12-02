import ccxt
import pandas
import numpy
import matplotlib.pyplot as plt
import math
from statistics import stdev

exchange = ccxt.ftx()

def get_price_history(symbol, candle_duration, num_candles):

    history = exchange.fetch_ohlcv(symbol, candle_duration, limit=num_candles)

    df = pandas.DataFrame(history)
    df.columns= (["Timestamp", "O", "H", "L", "C", "V"])
    df["TP"] = (df["L"]+df["C"]+df["H"])/3

    return df

def range_calculation(symbol, refresh_time):

    price_history = get_price_history(symbol, '1m', 60)
    df = pandas.DataFrame(price_history)

    df['spread'] = numpy.nan
    df['avg_spread'] = numpy.nan

    df['spread'] = (df['H'].rolling(window=1).max()-df['L'].rolling(window=1).min())
    df['avg_spread'] = df['spread'].mean()

    # df.plot(x='Timestamp', y=['spread', 'avg_spread'])
    # plt.show()

    # df['normalized_range'] = numpy.nan
    # df['normalized_range'] = (df['C'][::-1]-df['C'].min())/(df['C'].max()-df['C'].min()) primary

    # df['normalized_range'] = (df['C'][::-1]-df['C'].rolling(24,1).min()[::-1])/(df['C'].rolling(24,1).max()[::-1]-df['C'].rolling(24,1).min()[::-1])

    # df.plot(x='Timestamp', y='normalized_range')
    # plt.show()

    return df['spread'], df['avg_spread'].iloc[-1]

def get_underlying_price(symbol):
    response = ccxt.ftx().fetch_order_book(symbol, limit=1)
    # print(response)
    response = float((response['bids'][0][0]+response['asks'][0][0])/2)
    # print(response)
    return response

def standard_deviation(symbol):

    price_history = get_price_history(symbol, '1m', 20)
    df = pandas.DataFrame(price_history)

    close = df['C']
    mean = close.mean()
    close = close.tolist()

    std_deviation = stdev(close, mean)

    return std_deviation

