import alpaca_trade_api as tradeapi
from _keys import api_key, api_secret, base_url

api = tradeapi.REST(api_key, api_secret, base_url)
clock = api.get_clock()
account = api.get_account()