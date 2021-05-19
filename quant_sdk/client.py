from typing import Union, List

import requests


class Client:
    BUY = "BUY"
    SELL = "SELL"

    MARKET_ORDER = "MARKET"
    LIMIT_ORDER = "LIMIT"

    ORDER_STATUS_OPEN = "OPEN"
    ORDER_STATUS_CLOSED = "CLOSED"
    ORDER_STATUS_FAILED = "FAILED"
    ORDER_STATUS_PARTIALLY_FILLED = "PARTIALLYFILLED"

    ORDER_STATUS_CODE_OPEN = 1
    ORDER_STATUS_CODE_CLOSED = 2
    ORDER_STATUS_CODE_FAILED = 3
    ORDER_STATUS_CODE_PARTIALLY_FILLED = 4

    INTERVAL_1S = 1
    INTERVAL_5S = 5
    INTERVAL_30S = 30

    INTERVAL_1M = 60
    INTERVAL_5M = 300
    INTERVAL_15M = 900
    INTERVAL_30M = 1800

    INTERVAL_1H = 3600
    INTERVAL_2H = 7200
    INTERVAL_6H = 21600
    INTERVAL_12H = 43200
    INTERVAL_24H = 86400

    _ORDER_TYPES = (MARKET_ORDER, LIMIT_ORDER)

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key
        }
        self.base_url = "https://api.blocksize.capital/v1"

    def make_api_call(self, route: str, method: str, params=None, data=None, raw: bool = False):
        url = f'{self.base_url}{route}'
        response = requests.request(method=method, url=url, params=params, data=data, headers=self.headers)
        if raw:
            return response
        else:
            return response.json()

    ##########################################################################################
    # Market Data
    ##########################################################################################
    def get_order_book(self, exchanges: Union[str, List[str]], base: str, quote: str, depth: int = 1):

        # clean exchange list
        exchanges = self.extract_exchanges(exchanges=exchanges)

        pair = self.get_pair(base, quote)

        params = {
            'exchanges': exchanges,
            'ticker': pair,
            'limit': depth,
        }
        url_extension = f'/data/orderbook'
        return self.make_api_call(route=url_extension, method='GET', params=params)

    def get_vwap(self, base: str, quote: str, interval: Union[str, int]):
        pair = self.get_pair(base, quote)
        if type(interval) == str:
            interval = self.interval_converter(interval)
        url_extension = f'/data/vwap/latest/{pair}/{interval}'
        return self.make_api_call(method='GET', route=url_extension, params=None)

    def get_ohlc(self, base: str, quote: str, interval: Union[str, int]):
        pair = self.get_pair(base, quote)
        if type(interval) == str:
            interval = self.interval_converter(interval)
        url_extension = f'/data/ohlc/latest/{pair}/{interval}'
        return self.make_api_call(method='GET', route=url_extension, params=None)

    def get_historic_vwap(self, base: str, quote: str, interval: Union[str, int], start_time: int = None,
                          end_time: int = None):
        pair = self.get_pair(base, quote)
        if type(interval) == str:
            interval = self.interval_converter(interval)

        params = {
            'from': start_time,
            'to': end_time
        }
        url_extension = f'/data/vwap/historic/{pair}/{interval}'
        return self.make_api_call(method='GET', route=url_extension, params=params)

    def get_historic_ohlc(self, base: str, quote: str, interval: Union[str, int], start_time: int = None,
                          end_time: int = None):
        pair = self.get_pair(base, quote)
        if type(interval) == str:
            interval = self.interval_converter(interval)

        params = {
            'from': start_time,
            'to': end_time
        }
        url_extension = f'/data/ohlc/historic/{pair}/{interval}'
        return self.make_api_call(method='GET', route=url_extension, params=params)

    ##########################################################################################
    # Trading
    ##########################################################################################
    def place_order(self,
                    order_type: str,
                    base: str,
                    quote: str,
                    direction: str,
                    quantity: Union[str, float, int],
                    limit_price: Union[str, float, int] = None,
                    exchanges: Union[str, List[str]] = None):

        order_type = order_type.upper()

        if order_type not in self._ORDER_TYPES:
            raise ValueError(f"unsupported order type; "
                             f"order_type {order_type} doesn't match any of the following {self._ORDER_TYPES}")

        exchanges = self.extract_exchanges(exchanges=exchanges)

        if order_type == self.MARKET_ORDER:
            data = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction,
                'Type': order_type,
                'ExchangeList': exchanges,
            }
        elif order_type == self.LIMIT_ORDER:
            if limit_price is None:
                raise ValueError("need to specify limit_price for Limit Orders.")
            data = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction,
                'Type': order_type,
                'LimitPrice': limit_price,
                'ExchangeList': exchanges,
            }
        else:
            raise ValueError(f"Wrong order type use {self._ORDER_TYPES}")
        url_extension = f'/trading/orders'
        return self.make_api_call(method='POST', route=url_extension, data=data)

    def simulated_order(self,
                        base: str,
                        quote: str,
                        direction: str,
                        quantity: Union[str, float, int],
                        exchanges: Union[str, List[str]] = None,
                        unlimited_funds: bool = False,
                        disable_logging=False):

        exchanges = self.extract_exchanges(exchanges=exchanges)

        data = {
            'BaseCurrency': base.upper(),
            'QuoteCurrency': quote.upper(),
            'Direction': direction.upper(),
            'Quantity': quantity,
            'ExchangeList': exchanges,
            'Unlimited': unlimited_funds,
            'Type': "MARKET",
            'DisableLogging': disable_logging,
        }
        url_extension = f'/trading/orders/simulated'
        return self.make_api_call(method='POST', route=url_extension, data=data)

    def get_orders(self, limit: int = 100, offset: int = 0):
        params = {
            'limit': limit,
            'offset': offset
        }
        url_extension = f'/trading/orders'
        return self.make_api_call(method='GET', route=url_extension, params=params)

    def get_orders_by_status(self, status: str, limit: int = 100, offset: int = 0):
        """
        possible order states ('OPEN', 'CLOSED', 'FAILED', 'PARTIALLY_FILLED')
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        url_extension = f'/trading/orders/status/{status.upper()}'
        return self.make_api_call(method='GET', route=url_extension, params=params)

    def order_status(self, order_id: str):
        url_extension = f'/trading/orders/id/{order_id}'
        return self.make_api_call(method='GET', route=url_extension)

    def order_logs(self, order_id: str):
        url_extension = f'/trading/orders/id/{order_id}/logs'
        return self.make_api_call(method='GET', route=url_extension)

    def cancel_order(self, order_id: str):
        url_extension = f'/trading/orders/id/{order_id}/cancel'
        raise self.make_api_call(method='PUT', route=url_extension)

    def query_funds(self, quote_currency: str = 'EUR'):
        url_extension = f"/positions/exchanges?quotecurrency={quote_currency}"
        return self.make_api_call(method='GET', route=url_extension)

    @classmethod
    def parse_order_status_code(cls, code: int) -> str:
        if code == cls.ORDER_STATUS_CODE_OPEN:
            return cls.ORDER_STATUS_OPEN
        elif code == cls.ORDER_STATUS_CODE_CLOSED:
            return cls.ORDER_STATUS_CLOSED
        elif code == cls.ORDER_STATUS_CODE_FAILED:
            return cls.ORDER_STATUS_FAILED
        elif code == cls.ORDER_STATUS_CODE_PARTIALLY_FILLED:
            return cls.ORDER_STATUS_PARTIALLY_FILLED
        else:
            raise ValueError(f"order status code {code} cannot be parsed")

    @staticmethod
    def get_pair(base: str, quote: str) -> str:
        return f"{base}{quote}"

    @staticmethod
    def extract_exchanges(exchanges: Union[str, List[str]]):
        if type(exchanges) == list:
            exchanges = list(map(lambda exchange: exchange.upper(), exchanges))
            exchanges = ','.join(exchanges)
        if type(exchanges) == str:
            exchanges = exchanges.upper()
            exchanges = exchanges.replace(' ', '')
        return exchanges

    @staticmethod
    def interval_converter(interval_string: str) -> str:
        if interval_string[-1] == 's':
            return interval_string
        elif interval_string[-1] == 'm':
            return str(f'{int(interval_string[:-1]) * 60}s')
        elif interval_string[-1] == 'h':
            return str(f'{int(interval_string[:-1]) * 60 * 60}s')
        else:
            raise IntervalFormatError


class IntervalFormatError(Exception):
    """
    Raised when a time interval could not be parsed correctly.
    """
