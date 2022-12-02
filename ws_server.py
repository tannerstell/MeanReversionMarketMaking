import time
import hmac
import websocket
import json
from FTX import _FTX

api_key = #
api_secret = #
endpoint = "wss://ftx.com/ws/"

price_increments = {"BTC-PERP": 1, "LUNC-PERP": 0.00000005, "ETC-PERP":0.0005, "SOL-PERP": 0.0025}

def on_open(self):
    time_ms = int(time.time() * 1000)  # in milliseconds
    auth = json.dumps(
        {
            "op": "login",
            "args": {
                "key": api_key,
                "time": time_ms,
                "sign": hmac.new(api_secret.encode(),
                                 f"{time_ms}websocket_login".encode(),
                                 "sha256").hexdigest(),
                "subaccount": "LongTerm"
            }
        }
    )
    ws.send(auth)
    data = json.dumps({"op": "subscribe",
                       "channel": "fills"})
    ws.send(data)

    print("Connected to websocket endpoint: wss://ftx.com/ws/")

def on_message(self, message):

    if message!='{"type":"subscribed","channel":"fills"}':
        try:
            response = json.loads(message)['data']
            symbol = response['market']
            side = response['side']
            buy_price = float(response['price'])
            size = float(response['size'])
            order_id = response['orderId']
            price_increment = price_increments[symbol]
            sell_price = round((buy_price*1.0005)/price_increment, 1)*price_increment
            if side == "buy":
                response = _FTX().place_order(symbol, "sell", sell_price, size, True, True)

            elif side == "sell":
                ws.profit = ws.profit + (sell_price * size)*0.0005
                print("Profit: ${}".format(round(ws.profit, 2)))

        except Exception as e:
            print(e)
            pass

def on_error(self, error):
    print(f"Error: {error}")
    main()

def on_close(self, close_status_code, close_msg):
    main()
    print(f"Connection close")

ws = websocket.WebSocketApp(endpoint,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.profit = 0

def main():

    ws.run_forever(ping_interval=15)