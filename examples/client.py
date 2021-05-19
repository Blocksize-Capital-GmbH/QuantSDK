from quant_sdk import Client


API_KEY = "<Blocksize API token>"
client = Client(API_KEY)


# gets the 6 best bids/asks for the BTC-EUR pair on both Binance and Bitpanda exchange.
orderbook_data = client.get_order_book(exchanges=['Binance', 'Bitpanda'], base='BTC', quote='EUR', depth=6)


# gets the vwap price for the last 30s for BTC-EUR.
vwap = client.get_vwap(base="BTC", quote="EUR", interval=Client.INTERVAL_30S)


# gets the open, high, low and close price of the ETH-USDT pair for the past 6 hours.
ohlc = client.get_ohlc(base='ETH', quote='USDT', interval=client.INTERVAL_6H)


# gets the historic volume weighted average price of ETH-USDT hourly from 1621295177 until 1621327577 (unix timestamps)
hist_vwap = client.get_historic_vwap(base='ETH',
                                     quote='USDT',
                                     interval=client.INTERVAL_1H,
                                     start_time=1621295177,
                                     end_time=1621327577)


# gets the historic open high low close prices of BTC-EUR every 5 min from 1621311001 until 1621321801 (unix timestamps)
hist_ohlc = client.get_historic_ohlc(base='BTC',
                                     quote='EUR',
                                     interval=client.INTERVAL_5M,
                                     start_time=1621311001,
                                     end_time=1621321801)


# places a market buy order of 0.001 BTC on the Binance exchange
# make sure you have the exhcange connected in Matrix and that it is funded
market_order = client.place_order(order_type=client.MARKET_ORDER,
                                  base='BTC',
                                  quote='EUR',
                                  direction='BUY',
                                  quantity=0.001,
                                  exchanges='BINANCE')


# places a limit order to sell 0.001 BTC at a price of 45000 EUR on the Binance exchange
# make sure you have the exchange connected in Matrix and that it is funded
limit_order = client.place_order(order_type=client.LIMIT_ORDER,
                                 base='BTC',
                                 quote='EUR',
                                 direction='SELL',
                                 quantity=0.001,
                                 limit_price=45000,
                                 exchanges='BINANCE')


# places a simulated sell order of 50 XRP on the Bitpanda Exchange.
simulated_order = client.simulated_order(base='XRP',
                                         quote='EUR',
                                         direction='SELL',
                                         quantity=50,
                                         exchanges='BITPANDA',
                                         unlimited_funds=True)


# cancels a placed limit order
cancel_order = client.cancel_order('<order_id>')

# returns the last 50 orders placed
get_orders = client.get_orders(limit=50)

# returns an individual order status
order_status = client.order_status('<order_id>')

# returns the last closed order
order_by_status = client.get_orders_by_status(status=client.ORDER_STATUS_CLOSED, limit=1)

# returns the logs of an order
order_logs = client.order_logs('<order_id>')

# returns the funds on all connected exchanges
query_funds = client.query_funds()
