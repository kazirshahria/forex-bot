from stonex.client import Client
from stonex.market import Market
from stonex.instrument import Instrument


account = Client()
try:
    account.open_new_session()
    market = Market(account)
    pairs = market.search_currency_pairs()

    eur_usd_pair: Instrument = pairs.get('EUR/USD')
    previous_candles, current_candle = eur_usd_pair.price_bars(price_bars=50)
    eur_usd_pair.plot_candlesticks(previous_candles)

except Exception as e:
    print(f"Exception: {e}")
    pass
finally:
    account.close_existing_session()
