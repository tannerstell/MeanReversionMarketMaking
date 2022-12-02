import multiprocessing
import os
import time
import trading_algorithm

path = "C:\\Users\\tanne\\PycharmProjects\\Market_Maker_v3.3\\"

def execute(task):

    os.chdir(path)

    if task != "":
        os.system(task)

if __name__ == "__main__":

    tasks = ['py -c "import ws_server; ws_server.main()']

    symbols = ["BTC-PERP", 'LUNC-PERP', 'ETC-PERP', 'SOL-PERP', 'ETH-PERP']
    for symbol in symbols:
        task = """py -c "import trading_algorithm; trading_algorithm.symbol = '{}'; trading_algorithm.execution('{}')""".format(symbol, symbol)
        tasks.append(task)

    for task in tasks:
        if tasks.index(task)>1:
            time.sleep(trading_algorithm.refresh_time/len(symbols))

        p = multiprocessing.Process(target=execute, args=(task, ))
        p.start()
