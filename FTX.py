import datetime
import requests
from requests import Request, Session
from typing import Optional, Dict, Any
import json
import random
import websockets
import asyncio
import time
import hmac

class _FTX:


    endpoint = 'https://ftx.com/api'

    def __init__(self):

        self.session = Session()
	self.api_key = ""
	

    def _request(self, method, path, headers : Optional[Dict[str, Any]]):

        request = Request(method, self.endpoint+path, json=headers)
        self._signature_request(request)
        response = self.session.send(request.prepare())
        return response

    def _signature_request(self, request):

        # resp = requests.get('https://otc.ftx.com/api/time')
        # ftx_t = resp.json()
        # time = ftx_t['result']
        # date_format = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")
        # unix_time = datetime.datetime.timestamp(date_format)
        # ts = unix_time * 1000
        ts = int(time.time() * 1000)

        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode(
        )
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self.api_secret.encode(),
                             signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self.api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
        request.headers['FTX-SUBACCOUNT'] = ''

    def get_orderbook(self, symbol, depth):
        response = json.loads(self._request('GET', '/markets/{}/orderbook?depth={}'.format(symbol, depth), headers=None).text)
        bids, asks = float(response['result']['bids'][0][0]), float(response['result']['asks'][0][0])
        return bids, asks

    def get_market(self, symbol):

        response = json.loads(self._request('GET', '/markets/{}'.format(symbol), headers=None).text)['result']

        return response

    def place_order(self, symbol, side, price, size, postOnly, reduceOnly):

        headers = {
            "market": symbol,
            "side": side,
            "price": price,
            "type": "limit",
            "size": size,
            "reduceOnly": reduceOnly,
            "ioc": False,
            "postOnly": postOnly
        }

        response = self._request('POST', "/orders", headers)

        return response

    def fills(self, market, order_id):
        # t1 = datetime.now(timezone.utc)  # end time
        # t0 = t1 - timedelta(minutes=10)  # start time

        # if you need UNIX time:
        # start_ts, end_ts = t0.timestamp(), t1.timestamp()


        response = json.loads(self._request("GET", "/fills?market={}&orderId={}".format(market, order_id), headers=None).text)['result']

        return response

    def get_account(self):

        response = json.loads(self._request("GET", "/account", headers=None).text)['result']

        return response


    def cancel_orders(self, symbol, side):

        headers = {
            "market" : symbol,
            "side" : side
        }

        response = self._request('DELETE', '/orders', headers=headers)
        return response

    def get_open_orders(self, symbol):

        response = json.loads(self._request("GET", "/orders?market={}".format(symbol), headers=None).text)

        return response

    def open_order_size(self, symbol, side):

        try:
            open_orders = _FTX().get_open_orders(symbol)['result']
            size = 0
            if open_orders != None:

                for order in open_orders:
                    if order['status'] == 'open' and order['side'] == side:
                        size+=order['size']
                return size

        except Exception as e:
            print(e)
            pass

    def get_position_size(self, symbol):

        try:

            response = json.loads(self._request("GET", "/positions?showAvgPrice=true", headers=None).text)['result']

            position = [i for i in response if i['future'] == symbol]

            size = float(position[0]['netSize'])

            return size

        except:
            size = 0
            return size

    def get_breakeven_price(self, symbol):
        try:
            response = json.loads(self._request("GET", "/positions?showAvgPrice=true", headers=None).text)['result']

            position = [i for i in response if i['future'] == symbol]

            break_even_price = position[0]['recentBreakEvenPrice']

            return break_even_price

        except IndexError:
            break_even_price = 0
            return break_even_price