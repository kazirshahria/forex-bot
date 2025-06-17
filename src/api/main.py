from stonex.client import Client
from stonex.market import Market

account = Client()
try:
    account.open_new_session()
    market = Market(account)
    pairs = market.search_currency_pairs()
    print(pairs)
except Exception as e:
    print(f"Exception: {e}")
    pass
finally:
    account.close_existing_session()

