from api.client import Client
from api.market import Market
from api.instrument import Instrument
from api.utils.stonex_utils import log


account = Client()
try:
    account.open_new_session()
    market = Market(account)

    pairs = market.currency_pairs()

    pair: Instrument
    for _, pair in pairs.items():
        previous_candles, current_candle = pair.price_bars(candles=60)
        pair.plot_price(previous_candles)

except Exception as e:
    log(
        level='ERROR',
        event='Exception Error',
        msg=e
    )
finally:
    account.close_existing_session()
