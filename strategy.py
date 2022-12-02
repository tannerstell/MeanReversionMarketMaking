from FTX import _FTX
import CCXT
import ta
from ta import volatility, trend
from matplotlib import pyplot as plt
import time

def bollinger(symbol):
    data = CCXT.get_price_history(symbol, "1m", 120)
    bb2 = volatility.BollingerBands(data['C'], window=20, window_dev=2)
    bb4 = volatility.BollingerBands(data['C'], window=20, window_dev=4)

    data['upper2'] = bb2.bollinger_hband()
    data['middle'] = bb2.bollinger_mavg()
    data['lower2'] = bb2.bollinger_lband()

    data['upper4'] = bb4.bollinger_hband()
    data['lower4'] = bb4.bollinger_lband()

    # data['range'] = data['upper']-data['lower']
    #data['volatility'] = data['range']/(data['range'].max()-data['range'].min())

    # data['normalized_range'] = (data['C']-data['lower'])/(data['middle']-data['lower'])
    #
    # data['buy_market_spread'] = (1-((data['normalized_range'])*0.001))*data['C']

    # plt.plot(data['upper'])
    # plt.plot(data['lower'])
    # plt.plot(data['middle'])
    # plt.plot(data['C'])
    # # plt.plot(data['buy_market_spread'])
    #
    # # plt.plot(data['range'])
    # plt.show()

    return data

def macd(symbol):
    data = CCXT.get_price_history(symbol, "1m", 100)
    data["macd"] = trend.macd(data['C'], 26, 12)
    data["macd_signal"] = trend.macd_signal(data['C'], 26, 12)

    # plt.plot(data["macd"])
    # plt.plot(data["macd_signal"])
    # plt.show()

def bollinger_mm_strategy(symbol, buy_market_spread):
    data = bollinger(symbol)


    upper2 = data["upper2"].iloc[-1]
    middle = data["middle"].iloc[-1]
    lower2 = data["lower2"].iloc[-1]

    upper4 = data["upper4"].iloc[-1]
    lower4 = data["lower4"].iloc[-1]

    price = data["C"].iloc[-1]

    #volatility = (upper-lower)/(data['range'].max()-data['range'].min())

    # if price<middle:

    normalized_range = max((price-lower2)/((middle-lower2)), 0)
    # print("Before:", buy_market_spread)
    buy_market_spread = max((normalized_range)*buy_market_spread, 0.0002)

    # print(normalized_range, buy_market_spread)
    # size = round(max((1-normalized_range)*0.007, 0.001), 3)

    # spread_range = [price-lower2, price-lower4]

    return spread_range

    # else:
    #     time.sleep(5)

