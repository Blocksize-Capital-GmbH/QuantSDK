import requests
import datetime
import pandas as pd
from typing import Union


class BlockSize:

    def __init__(self, token: str):
        self.blocksize_token = token

    def get_orderbook_data(self, exchanges: str, base: str, quote: str, depth: int = 1):
        try:
            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/orderbook?exchanges={exchanges}"
                                    f"&ticker={pair}&limit={depth}", headers={"x-api-key": self.blocksize_token})
            if response.json()[0]['asks'] is None:
                return 'Exchange/Pair Not Available'
            elif float(response.json()[0]['asks'][0][0]) > 0:
                return response.json()
            else:
                pass

        except TypeError:
            return 'Type Error'

    def get_vwap(self, base: str, quote: str, interval: str):
        """

        :param base:
        :param quote:
        :param interval: 1s, 5s, 30s, 60s, 1m, 5m, 30m, 60m
        :return:
        """
        try:
            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/vwap/latest/{pair}/{interval}",
                                    headers={"x-api-key": self.blocksize_token})
            return response.json()

        except (NameError, TypeError, SyntaxError):
            return 'Error'

    def get_ohlc(self, base: str, quote: str, interval: str):
        """

        :param base:
        :param quote:
        :param interval: 1s, 5s, 30s, 60s, 1m, 5m, 30m, 60m
        :return:
        """
        try:

            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/ohlc/latest/{pair}/{interval}",
                                    headers={"x-api-key": self.blocksize_token})
            return response.json()

        except (NameError, TypeError, SyntaxError):
            return 'Type Error'

    def get_historical_vwap(self, base: str, quote: str, interval: str, start_date: str, end_date: str):
        """

        :param base:
        :param quote:
        :param interval: 1s, 5s, 30s, 60s, 1m, 5m, 30m, 60m
        :param start_date: yyyy-mm-dd
        :param end_date: yyyy-mm-dd
        :return:
        """
        try:
            start_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_timestamp = start_time_obj.strftime('%s')
            end_time_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            end_timestamp = end_time_obj.strftime('%s')
            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/vwap/historic/{pair}/"
                                    f"{interval}?from={start_timestamp}&to={end_timestamp}",
                                    headers={"x-api-key": self.blocksize_token})
            df = pd.DataFrame(response.json())
            if df.empty:
                return 'No Data Available - Check Base & Quote Currency'
            else:
                df.rename(columns={'timestamp': 'Timestamp', 'price': 'Price', 'volume': 'Volume'}, inplace=True)
                df.set_index('Timestamp', inplace=True)
                return df

        except ValueError:
            return 'Value Error'

    def get_historic_ohlc(self, base: str, quote: str, interval: str, start_date: str, end_date: str):
        """

        :param base:
        :param quote:
        :param interval: 1s, 5s, 30s, 60s, 1m, 5m, 30m, 60m
        :param start_date: yyyy-mm-dd
        :param end_date: yyyy-mm-dd
        :return:
        """
        try:
            start_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_timestamp = start_time_obj.strftime('%s')
            end_time_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            end_timestamp = end_time_obj.strftime('%s')

            pair = base + quote

            response = requests.get(f"https://api.blocksize.capital/v1/data/ohlc/historic/"
                                    f"{pair}/{interval}?from={start_timestamp}&to={end_timestamp}",
                                    headers={"x-api-key": self.blocksize_token})
            df = pd.DataFrame(response.json())
            if df.empty:
                return 'Empty DataFrame'
            else:
                df.rename(columns={'timestamp': 'Timestamp',
                                   'open': 'Open',
                                   'high': 'High',
                                   'low': 'Low',
                                   'close': 'Close'}, inplace=True)
                df.set_index('Timestamp', inplace=True)
        except ValueError:
            return 'Value Error'
        return df

    def post_simulated_order(self, base: str, quote: str, direction: str, quantity: Union[str, float],
                             exchange: str = None, unlimited_funds: bool = False):
        """
        :param base:
        :param quote:
        :param direction: buy or sell
        :param quantity:
        :param exchange:
        :param unlimited_funds:
        :return:
        """
        try:
            if exchange is None:
                pass
            else:
                exchange = exchange.upper()
            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction.upper(),
                'Type': 'Market',
                'ExchangeList': exchange,
                'Unlimited': unlimited_funds,
            }

            response = requests.post("https://api.blocksize.capital/v1/trading/orders/simulated", data=params,
                                 headers={"x-api-key": self.blocksize_token})
            return response.json()
        except AttributeError:
            return 'Malformatted Variables'

    # https://api.blocksize.capital/v1/trading/orders?BaseCurrency=ETH&QuoteCurrency=EUR&Quantity=0.1&Direction=SELL&Type=MARKET&ExchangeList=BITTREX
    def post_market_order(self, base: str, quote: str, direction: str, quantity: Union[str, float],
                          exchange: str = None):

        """
        :param base:
        :param quote:
        :param direction: buy or sell
        :param quantity:
        :param exchange:
        :return:
        """
        try:
            if exchange is None:
                pass
            else:
                exchange = exchange.upper()
            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction.upper(),
                'Type': 'Market',
                'ExchangeList': exchange,
            }

            response = requests.post("https://api.blocksize.capital/v1/trading/orders?", data=params,
                                     headers={"x-api-key": self.blocksize_token})

            return response.json()
        except AttributeError:
            return 'Malformatted Variables'

    def order_status(self, order_id: str):
        """

        :param order_id:
        :return:
        """
        response = requests.get(f"https://api.blocksize.capital/v1/trading/orders/id/{order_id}",
                                headers={"x-api-key": self.blocksize_token})
        return response.json()

    def order_logs(self, order_id: str):
        """

        :param order_id:
        :return:
        """
        response = requests.get(f'https://api.blocksize.capital/v1/trading/orders/id/{order_id}/logs',
                                headers={"x-api-key": self.blocksize_token})
        return response.json()

    def get_exchange_balances(self):
        """

        :return:
        """
        response = requests.get('https://api.blocksize.capital/v1/positions/exchanges',
                                headers={"x-api-key": self.blocksize_token})
        return response.json()
