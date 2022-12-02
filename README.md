# mean-reversion-market-making

Developed a market maker that uses stochastic modeling to algorithmically trade cryptocurrencies, placing scaled limit orders at a three standard deviation Bollinger band. Dependent upon the position of the price within the upper and lower Bollinger bands, the buy market spread may dynamically increase or decrease.

The script uses multithreading to simultaneously run a websockets fills server and trading logic script. There is the ability to run on multiple trading pairs.


CCXT.py - Used to gather pricing data and alternative brokerage connection thanks to the CCXT library.

FTX.py - Access to account and trading-level functions (cancel orders, placing orders, etc). Due to the recent circumstances with FTX and their overcollateralization of FTT, the logic of this file is sound, but it is deprecated.

Requirements.txt - Discusses what I might choose to update next.

launch.bat - Batch launcher script

main.py - Main function calls other files

strategy.py - Strategy logic for the market maker

trading_algorithm.py - Where the continuous refreshing of orders are updated and risk management-level functions reside.

ws_server.py - Websocket fills of orders and simultaneous calculation of closing orders are placed.
