from FTX import _FTX
import CCXT
import time
import os
import random
import strategy
import json
import numpy

number_of_orders = 5
refresh_time = 60

symbol = "BTC-PERP"

# beginning_btc_price = sum(_FTX().get_orderbook(symbol, 1))/2

caution_symbols = "BTC-PERP"

order_ids = {"orders": []}

price_increments = {"BTC-PERP": 1, "LUNC-PERP": 0.00000005, "ETC-PERP":0.0005, "SOL-PERP": 0.0025}

def opening(symbol, market, spread_range):

    price = float(market['price'])
    priceIncrement = float(market['priceIncrement'])
    minProvideSize = float(market['minProvideSize'])
    sizeIncrement = float(market['sizeIncrement'])

    account = _FTX().get_account()
    collateral = float(account['collateral'])
    free_collateral = float(account['freeCollateral'])
    collateral_pct = free_collateral / collateral
    notional_position_size = (_FTX().get_position_size(symbol) * price)
    laddered_price = price
    try:
        ladder_spread = ((max(spread_range)-min(spread_range))/5)
        size = 0
        for i in range(1, 5):
            if i ==1:
                laddered_price = laddered_price-min(spread_range)
            else:
                laddered_price = (numpy.round((laddered_price - ladder_spread)/priceIncrement, 0)*priceIncrement)
            if symbol != "BTC-PERP":
                if notional_position_size < 300:
                    size = max(50 / price, minProvideSize)
            else:
                rate = 2.6591479484724942

                if i==1:
                    size = 0.001
                else:
                    size = round((size*rate)/sizeIncrement)*sizeIncrement
                _FTX().place_order(symbol, "buy", laddered_price, size, True, False)

    except Exception as e:
        # print(e)
        pass

def position_diff(symbol, beginning_btc_balance, beginning_btc_order_size):
    try:
        position_size = _FTX().get_position_size(symbol)
        open_order_size = _FTX().open_order_size(symbol, "sell")

        current_btc_balance = (_FTX().get_position_size(symbol)-open_order_size)

        diff = round(current_btc_balance-beginning_btc_balance, 3)
        # print(beginning_btc_balance, current_btc_balance, diff)
        return diff

    except:
        return 0

def execution(symbol):
    beginning_btc_order_size = _FTX().open_order_size(symbol, "sell")
    beginning_btc_balance = (_FTX().get_position_size(symbol) - beginning_btc_order_size)

    runtime = 0
    while True:
        try:

            market = _FTX().get_market(symbol)
            _FTX().cancel_orders(symbol, "buy")  # Cancel buy orders

            spread_range = strategy.bollinger_mm_strategy(symbol)
            # standard_deviation = CCXT.standard_deviation(symbol)
            # spread_range = [standard_deviation*2, standard_deviation*4]

            opening(symbol, market, spread_range)

            start_time = time.time()
            end_time = 0
            counter = 0
            while end_time - start_time < refresh_time:
                try:
                    if counter !=1:
                        counter += 1

                        price = market['price']
                        if symbol!="BTC-PERP":
                            break_even_price = float(_FTX().get_breakeven_price(symbol))
                            position_size = _FTX().get_position_size(symbol)
                            notional_position_size = (position_size * (sum(_FTX().get_orderbook(symbol, 1)) / 2))

                            if price > break_even_price * 1.0005 or (notional_position_size>3000 and price>break_even_price):
                                _FTX().cancel_orders(symbol, "sell")  # Cancel sell orders
                                size = _FTX().get_position_size(symbol)
                                price_increment = price_increments[symbol]
                                sell_price = round((price * 1.0001) / price_increment, 1)
                                sell_price = sell_price * price_increment
                                _FTX().place_order(symbol, "sell", sell_price, size, True, True)
                        else:
                            diff = position_diff(symbol, beginning_btc_balance, beginning_btc_order_size)
                            order = _FTX().place_order(symbol, "sell", price*1.0005, diff, True, True)

                    time.sleep(60)
                    end_time = time.time()
                except:
                    pass

        except Exception as e:
            time.sleep(0.2)
            pass