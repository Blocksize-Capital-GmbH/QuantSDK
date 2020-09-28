import requests
import datetime
import pandas as pd
from typing import Union, Iterable


class BlockSize:

    def __init__(self, token: str):
        self.token = token
        self.direction = {0: 'SELL', 2: 'BUY'}
        self.order_type = {0: 'MARKET'}
        self.intervals = {0: '1s', 1: '5s', 2: '30s', 3: '60s', 4: '1m', 5: '5m', 6: '15m', 7: '30m', 8: '1h', 9: '2h',
                          10: '6h', 11: '12h', 12: '24h'}

    def get_orderbook_data(self, exchanges: str, base: str, quote: str, depth: int = 1):
        try:
            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/orderbook?exchanges={exchanges}"
                                    f"&ticker={pair}&limit={depth}", headers={"x-api-key": self.token})
            if response.json()[0]['asks'] is None:
                return 'Exchange/Pair Not Available'
            elif float(response.json()[0]['asks'][0][0]) > 0:
                return response.json()
            else:
                pass
        except Exception:
            print('An Error occurred running this function')

    def get_vwap(self, base: str, quote: str, interval: int):
        """

        :param base:
        :param quote:
        :param interval:    (0, '1s'), (1, '5s'), (2, '30s'), (3, '60s'), (4, '1m'), (5, '5m'), (6, '15m'), (7, '30m'),
                            (8, '1h'), (9, '2h'), (10, '6h'), (11, '12h'), (12, '24h')
        :return:
        """
        try:
            pair = base + quote
            response = requests.get(
                f"https://api.blocksize.capital/v1/data/vwap/latest/{pair}/{self.intervals[interval]}",
                headers={"x-api-key": self.token})
            return response.json()
        except Exception:
            print('An Error occurred running this function')

    def get_ohlc(self, base: str, quote: str, interval: int):
        """

        :param base:
        :param quote:
        :param interval:    (0, '1s'), (1, '5s'), (2, '30s'), (3, '60s'), (4, '1m'), (5, '5m'), (6, '15m'), (7, '30m'),
                            (8, '1h'), (9, '2h'), (10, '6h'), (11, '12h'), (12, '24h')
        :return:
        """

        try:
            pair = base + quote
            response = requests.get(
                f"https://api.blocksize.capital/v1/data/ohlc/latest/{pair}/{self.intervals[interval]}",
                headers={"x-api-key": self.token})
            return response.json()
        except Exception:
            print('An Error occurred running this function')

    def get_historical_vwap(self, base: str, quote: str, interval: int, start_date: str, end_date: str):
        """

        :param base:
        :param quote:
        :param interval:    (0, '1s'), (1, '5s'), (2, '30s'), (3, '60s'), (4, '1m'), (5, '5m'), (6, '15m'), (7, '30m'),
                            (8, '1h'), (9, '2h'), (10, '6h'), (11, '12h'), (12, '24h')
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
                                    f"{self.intervals[interval]}?from={start_timestamp}&to={end_timestamp}",
                                    headers={"x-api-key": self.token})
            df = pd.DataFrame(response.json())
            df.rename(columns={'timestamp': 'Time', 'price': 'Price', 'volume': 'Volume'}, inplace=True)
            df['Time'] = pd.to_datetime(df['Time'], unit='s')
            df.set_index('Time', inplace=True)
            return df
        except Exception:
            print('An Error occurred running this function')

    def get_historic_ohlc(self, base: str, quote: str, interval: int, start_date: str, end_date: str):

        try:
            start_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_timestamp = start_time_obj.strftime('%s')
            end_time_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            end_timestamp = end_time_obj.strftime('%s')

            pair = base + quote

            response = requests.get(f"https://api.blocksize.capital/v1/data/ohlc/historic/"
                                    f"{pair}/{self.intervals[interval]}?from={start_timestamp}&to={end_timestamp}",
                                    headers={"x-api-key": self.token})
            df = pd.DataFrame(response.json())
            df.rename(columns={'timestamp': 'Time',
                               'open': 'Open',
                               'high': 'High',
                               'low': 'Low',
                               'close': 'Close'}, inplace=True)
            df.set_index('Time', inplace=True)

            return df
        except Exception:
            print('An Error occurred running this function')

    def post_simulated_order(self, base: str, quote: str, direction: str, quantity: Union[str, float],
                             exchange: str = None, unlimited_funds: bool = False):

        # If no exchange is specified => S.O.R

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
                                     headers={"x-api-key": self.token})
            return response.json()
        except Exception:
            print('An Error occurred running this function')

    def post_real_order(self, base: str, quote: str, direction: int, quantity: Union[str, float], order_type: int = 0,
                        exchange: str = None):

        if order_type == (0 or 1) and not exchange:
            print('For Market adn Limit orders please select one or multiple exchanges. In case u want to ')

        try:
            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': self.direction[direction],
                'Type': self.order_type[order_type],
                'ExchangeList': exchange.upper(),
            }

            response = requests.post("https://api.blocksize.capital/v1/trading/orders?", data=params,
                                     headers={"x-api-key": self.token})

            return response.json()
        except Exception:
            print('An Error occurred running this function')

    def order_status(self, order_id: str):

        try:
            response = requests.get(f"https://api.blocksize.capital/v1/trading/orders/id/{order_id}",
                                    headers={"x-api-key": self.token})
            return response.json()

        except Exception:
            print('An Error occurred running this function')

    def order_logs(self, order_id: str):

        try:
            response = requests.get(f'https://api.blocksize.capital/v1/trading/orders/id/{order_id}/logs',
                                    headers={"x-api-key": self.token})
            return response.json()
        except Exception:
            print('An Error occurred running this function')

    def get_exchange_balances(self):

        try:
            response = requests.get('https://api.blocksize.capital/v1/positions/exchanges',
                                    headers={"x-api-key": self.token})
            return response.json()
        except Exception:
            print('An Error occurred running this function')

    @staticmethod
    def convert_to_unix(year, month, day, hour=0, second=0):
        unix = datetime.datetime(year, month, day, hour, second).strftime('%s')
        return unix
