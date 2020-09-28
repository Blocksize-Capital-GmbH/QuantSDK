# Quant SDK 

The Quant SDK is the third pillar of Blocksize Capital's product offer.
It is a Python interface fully integrated with Blocksize CORE™. It allows the easy automation
of algorithmic trading strategies, as well as accessing historical market data.

The functionality of the quant SDK is divided into two parts:


**Market Data**

The Quant SDK seamlessly connects with the Blocksize CORE™ websocket and allows the collection of real-time market data of
dozens of cryptocurrencies across all connected exchanges. Additionally, functionalities such as the retrieval of customizable
historical data using Blocksize CORE™ RESTful API are accessible in a single line of code.

**Trading**

The core part of the Quant SDK is the ability to automate trading strategies. The potential applications of strategies are vast: while simple portfolio rebalancing
mechanisms can be easily implemented, higher-frequency quantitative strategies may be deployed as well.


The following documentation will serve as a walkthrough of the functionalities of the Quant SDK, starting with the setup of the SDK.
Reading this tutorial is recommended as it delivers insights into the data structure used and explains some non-trivial parts of the
Quant SDK

Disclaimer: to use the Quant SDK, you need to authenticate yourself using your personalized Blocksize CORE™ API-Token.
A Blocksize CORE™ API-Token can be generated in the Blocksize MATRIX™ API Token Settings. 

## Table of Contents

- [Installation](#installation)
- [Real Time Market Data](#real time market data)
- [Historical Market Data](#historical market data)
- [Trading](#trading)
- [Balances](#balances)
## Installation

### Requirments
- Details of the requirements to successfully download the QuantSDK
### Clone

- Clone this repo to your local machine using `https://github.com/Blocksize-Capital-GmbH/QuantSDK`

### Create Your Blocksize Token
 - In order to utilize the capabilites of the QuantSDK we must first generate a Blocksize API Token.
 - A Blocksize API Token can be generated in the Blocksize MATRIX™ API Token Settings.
 - https://matrix.blocksize.capital/dashboard
 
![Recordit GIF](https://recordit.co/8FlDpEcM74.gif)
- We will now initialize the Blocksize Class using this API Token which will allow us to
 utilize all the capabilites of the Quant SDK.
```python


from quantsdklite import BlockSize

sdk = BlockSize('lAaUoVwxr2aOFhdS9QHa4hoVkpNPPHln99DsllOWusTLeqK2NVdIR0Ginltzr8tL5YdEGOEwIiXIHmXaUzPCYQEMbYWvwAbAyYoU9GVlPHvWq5nzxAvQZdYSzMmtj64h')

```
- We are now ready to utilize all the functionalities of the QuantSDK.
#  Real Time Market Data
- The QuantSDK enables users to access real-time data using the Blocksize Infrastructure. The following chapter 
contains information regarding how to use the specific functions in order to receive real-time market data.
 
 ### Real Time Orderbook Data
 ```python
get_orderbook_data(self, exchanges: str, base: str, quote: str, depth: int = 1)
```
- The following example will show how the QuantSDK can be used to access real-time orderbook data in one line of code.
- In order to utilize this function `get_orderbook_data` we need to provide four pieces of information, namely:
- (1) The Exchange you wish to get orderbook data from.
- (2) The Base Currency
- (3) The Quote Currency
- (4) Ordebook Depth - This determines how deep we look in the orderbook. If this value is not specified by the user,
the function will automatically set this value to 1, which will return the best Bid/Ask price & assossiated volume.

- In the following example, we look for the top two Bid & Ask prices for the BTC/EUR pair on the Bittrex exchange.
 ```python
sdk.get_orderbook_data('Bittrex', 'BTC', 'EUR', 2)
```
- This function returns the current Bittrex Orderbook best Bid / Ask prices, 
as well as the volume assossiated with those orders.
 ```python
[{'exchange': 'BITTREX', 'asks': [['9188.093', '0.01'], ['9189.999', '0.54465044']], 'bids': [['9136.065', '4.1373157'], ['9136.064', '0.05457277']]}]
```
### VWAP - Volume Weighted Average Price
 ```python
get_vwap(self, base: str, quote: str, interval: str)
```
- Volume Weighted Average Price refers to the average price of a stock, weighted by the total trading volume.
It's used to calculate the average price of a stock over a specific timeframe. We can utilize the QuantSDK
to gain an insight into the average price of different cryptocurrencies across multiple timeframes. In order to utilize
this feature, we need to decide three attributes:

- (1) Base Currency

- (2) Quote Currency

- (3) Time Frame (1s , 5s, 30s, 1m, 5m, 30m, 60m)

- In the following example, we get the VWAP of the ETH/EUR pair over a time horizon of 60 minutes.
 ```python
sdk.get_vwap('ETH', 'EUR', '60m')
```
- This function returns a dictionary which includes the VWAP, Ticker, Timestamp & Volume. This data can be parsed
and used for signals within a more sophisticated trading algorithm.
```python
{'price': 298.3631794349796, 'ticker': 'ETHEUR', 'timestamp': 1601046000, 'volume': 3962.29888435}
``` 
### OHLC - Open High Low Close 

```python
get_ohlc(self, base: str, quote: str, interval: str)
```

We need to input three variables in order to execute the OHLC function:
- (1) Base Currency

- (2) Quote Currency

- (3) Time Interval (1s , 5s, 30s, 1m, 5m, 30m, 60m)

- In the following example, we will find the OHLC of the XRP/EUR pair for the proceeding 60mins.

```python
sdk.get_ohlc('XRP','EUR','60m')
```
- This function returns a dictionary which includes the OHLC Prices, Ticker & Timestamp. Furthermore, this data can
be used to determine entry / exit points as part of a more sophisticated trading algorithm.
```python
{'close': 0.2064, 'high': 0.20866, 'low': 0.20587, 'open': 0.2069, 'ticker': 'XRPEUR', 'timestamp': 1601049600}
```

# Historical Market Data
- One major issue for Traders/Investors is access to accurate historical market data. The QuantSDK solves this
issue by accessing historical market data in one line of code. Historical market data is a crucial tool for
data scientists who wish to analyse market data, as well as test trading strategies.

### Historical OHLC 
```python
get_historic_ohlc(self, base: str, quote: str, interval: str, start_date: str, end_date: str)
```
- The Historical OHLC function can be used to access these important metrics across all pairs as well
as multiple time intervals. Five input variables are required to successfully execute this function.

- (1) Base Currency
- (2) Quote Currency
- (3) Time Interval (1s , 5s, 30s, 1m, 5m, 30m, 60m)
- (4) Start Date (YYYY-MM-DD)
- (5) End Date (YYYY-MM-DD)
- In the following example, we will find the historic OHLC of the BTC/EUR pair,
 every hour, for ten days in September 2020.
```python
sdk.get_historic_ohlc('BTC', 'EUR', '60m', '2020-09-10', '2020-09-20')
```
- This function returns a DataFrame which can be used for further analysis.
```python
2020-09-10 00:00:00  8675.20  8784.900000  8665.84  8717.40
2020-09-10 01:00:00  8717.40  8866.130268  8693.68  8795.20
2020-09-10 02:00:00  8789.06  8855.550000  8775.05  8784.20
```
### Historical VWAP - Volume Weighted Average Price
```python
get_historical_vwap(self, base: str, quote: str, interval: str, start_date: str, end_date: str)
```
- The Historical VWAP function can be used to access the historical Volume Weighted Average Prices of all the connected
digital assets, across multiple different time intervals. Five input variables are required to successful execute this function.
- (1) Base Currency

- (2) Quote Currency

- (3) Time Interval (1s , 5s, 30s, 1m, 5m, 30m, 60m)

- (4) Start Date (YYYY-MM-DD)

- (5) End Date (YYYY-MM-DD)
- The following example returns the VWAP of the BTC/EUR pair, every 30 seconds, from Sept 4th - Sept 5th
```python
sdk.get_historical_vwap('BTC', 'EUR', '30s', '2020-09-04', '2020-09-05')
```
- This function returns a DataFrame consisting of Time, Price & Volume.

```python
2020-09-04 21:58:00  8945.685272  0.143362
2020-09-04 21:58:30  8940.873619  1.212943
2020-09-04 21:59:00  8936.649064  0.321675
2020-09-04 21:59:30  8945.942044  0.193300
2020-09-04 22:00:00  8939.740021  0.738045
```

# Trading
- One of the most impressive features of the QuantSDK is the ability to post real as well as simulated orders.
This feautre allows users to buy/sell every tradeable digital asset across all the connected exchanges.

### Simulated Orders

```python
post_simulated_order(self, base: str, quote: str, direction: str, quantity: Union[str, float], exchange: str = None, unlimited_funds: bool = False)
```
- The Simualted Orders function can be utilized for a variety of purposes. It takes 6 input variables:
- (1) Base Currency

- (2) Quote Currency

- (3) Direction ( Buy or Sell)

- (4) Quantity (Amount of the Base Currency you wish to Buy/Sell)

- (5) Exchange (If left unspecified, it will automatically place the trade on the
exchange which offers the best price)

- (6) Unlimited Funds (True or False - If left unspecified, default setting is False)

- In the following example, we will simulate a Buy Order of 0.2 BTC on the Bittrex Exchange.

```python
sdk.post_simulated_order('BTC','EUR','BUY',0.2,'Bittrex')
```
- Notice the ``unlimited_funds`` variable was left unspecified, as a result, it was set to the default ```False```.
This is because we wanted to simulate an order which would also check if there was enough funds in the account
to successfully place the trade. The result of this function is printed below.
```python
{'order': {'order_id': '6c8b37d1-b621-4f73-8e64-a529cb338f7b', 'base_currency': 'BTC', 'quote_currency': 'EUR', 'direction': 2, 'type': 1, 'quantity': '0.2', 'bsc_token_id': 'd5d08125-795a-4edf-bfc7-2db5b1240b37', 'user_id': 'Zh4WxmYDNihRbFLIBQk6w4QjNul1'}, 'failed_reason': 'FAILED_REASON_INSUFFICIENT_FUNDS', 'elapsed_time_retrieval': 0, 'elapsed_time_calculation': 0, 'average_execution_price': '', 'trading_fees': '', 'trades': None}
```
- Notice this simulated order was unsuccessful `'failed_reason': 'FAILED_REASON_INSUFFICIENT_FUNDS'`

- We will now simulate an order which assumes we have an infinite amount of funds our account.

- The following example will simulate a Sell Order of 10 BTC on the Binance Exchange.
```python
sdk.post_simulated_order('BTC','EUR','SELL',10,'Binance',True)
```

- In this example, we set `unlimited_funds`as `True`

- As a result, we have simulated an order which assumes infinite funds in our account.

```python
{'order': {'order_id': '8f1b1ce1-b8ad-4b09-897a-fe35c3ec3eaf', 'base_currency': 'BTC', 'quote_currency': 'EUR', 'direction': 1, 'type': 1, 'quantity': '10', 'bsc_token_id': 'd5d08125-795a-4edf-bfc7-2db5b1240b37', 'user_id': 'Zh4WxmYDNihRbFLIBQk6w4QjNul1'}, 'elapsed_time_retrieval': 22910, 'elapsed_time_calculation': 177, 'average_execution_price': '9215.402037268002', 'trading_fees': '0.01', 'trades': [{'exchange': 'BINANCE', 'quantity': '10.0', 'apikey_id': '00000000-0000-0000-0000-000000000000', 'average_execution_price': '9215.402037268002', 'trading_fees': '0.01', 'funds': '-1', 'fee_bp': '10', 'trade_id': '4a363f00-9e6b-4c6e-a61b-47e4a2676f88', 'buffer_bp': '25'}]}

```
### Real Orders

```python
post_market_order(self, base: str, quote: str, direction: str, quantity: Union[str, float], exchange: str)
```
- Another feauter of the QuantSDK is the ability to place orders on individual exchanges, as well as taking
 advantage of the Blocksize SOR trading algorithm. It takes 5 input variables:

- (1) Base Currency

- (2) Quote Currency

- (3) Direction ( Buy or Sell)

- (4) Quantity (Amount of the Base Currency you wish to Buy/Sell)

- (5) Exchange (If left unspecified, it will automatically place the trade on the
exchange which offers the best price)

- In the following example, we will sell 0.15 ETH on the Bittrex Exchange.
```python
sdk.post_market_order('eth', 'eur', 'sell', 0.15, 'bittrex')
```
 The function returns the unique order-ID, as well as other details about the trade.
```python
{'order': {'order_id': '02963299-f1e2-4ca6-b34a-2a89940ed42a', 'base_currency': 'ETH', 'quote_currency': 'EUR', 'direction': 1, 'type': 1, 'quantity': '0.15', 'bsc_token_id': '4a68e081-de91-4b40-a615-85e472a8fa75', 'user_id': 'Zh4WxmYDNihRbFLIBQk6w4QjNul1'}}
```
In the following example, we will attempt to buy 1 BTC on the Binance Exchange:
```python
sdk.post_market_order('BTC', 'EUR', 'BUY', 1, 'BINANCE')
```
The purpose of this example is to show that if the balance is not sufficient to successfully execute the trade,
the function will return ``'failed_reason': 'FAILED_REASON_INSUFFICIENT_FUNDS'``. This can be seen in the response below.
 
```python
{'order': {'order_id': 'f8faeccb-47d9-46b0-ba28-81d54a073e46', 'base_currency': 'BTC', 'quote_currency': 'EUR', 'direction': 2, 'type': 1, 'quantity': '1', 'bsc_token_id': '4a68e081-de91-4b40-a615-85e472a8fa75', 'user_id': 'Zh4WxmYDNihRbFLIBQk6w4QjNul1'}, 'failed_reason': 'FAILED_REASON_INSUFFICIENT_FUNDS'}

```
### Order Status

```python
order_status(self, order_id: str)
```
- We can check the status of individual orders by using the ``order_stauts()`` function. The only input is
the unique order-id.

- In the following example we will check the status of the 0.15 ETH Buy Order which we placed earlier.

```python
sdk.order_status('02963299-f1e2-4ca6-b34a-2a89940ed42a')
```

- This function will returns several details about the trade. Most noteably we can see the trade status.
- The ``aggregated_status:`` can be interpreted as follows:
- (1) Open Order, (2) Closed Order, (3) Failed Order, (4) Partially Filled Order.
- We can also see the ``timestamp`` assosiated with the trade  as well as the `executed_price`.

```python
{'aggregated_status': 2, 'order': {'order_id': '02963299-f1e2-4ca6-b34a-2a89940ed42a', 'base_currency': 'ETH', 'quote_currency': 'EUR', 'direction': 1, 'type': 1, 'quantity': '0.15', 'bsc_token_id': '4a68e081-de91-4b40-a615-85e472a8fa75', 'user_id': 'Zh4WxmYDNihRbFLIBQk6w4QjNul1', 'order_timestamp': 1601289889745}, 'orderid': '02963299-f1e2-4ca6-b34a-2a89940ed42a', 'trade_status': [{'trade': {'trade_id': '30c6edae-0928-4986-acf9-2d6946c22b91', 'exchange': 'BITTREX', 'trade_quantity': '0.15'}, 'execution_status': 2, 'status_report': {'trade_status': 3, 'exchange_trade_id': '8c0b7d3c-1d22-4169-aef7-c31327582588', 'placed_timestamp': 1601289890114, 'closed_timestamp': 1601289890050, 'executed_quantity': '0.15', 'executed_price': '307.131', 'status_timestamp': 1601289896067}}], 'userid': 'Zh4WxmYDNihRbFLIBQk6w4QjNul1'}

```
## Balances
- The Quant SDK makes it very simple to check the balances of your connected exchanges.
```python
sdk.get_exchange_balances()
```
- The response will be a list which displays the total value of each cryptocurrency on each connected exchange.
- If you have no funds on your connected exchanges, the response will simply be: `None`



