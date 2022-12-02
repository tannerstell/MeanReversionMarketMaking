# mean-reversion-market-making

Developed a market maker that uses stochastic modeling to algorithmically trade cryptocurrencies, placing scaled limit orders at a three standard deviation Bollinger band. Dependent upon the position of the price within the upper and lower Bollinger bands, the buy market spread may dynamically increase or decrease.

The script uses multithreading to simultaneously run a websockets fills server and trading logic script. There is the ability to run on multiple trading pairs.
