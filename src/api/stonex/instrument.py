from .client import Client
from .utils.stonex_utils import send_request

class Instrument():
    
    def __init__(self, client: Client, market_id: str, name: str, margin: float, min_margin: float, max_margin: float, client_margin: float, bid_price: float, ask_price: float, spread: float):
        self.client = client
        self.market_id = market_id
        self.name = name
        self.margin = margin
        self.min_margin = min_margin
        self.max_margin = max_margin
        self.client_margin = client_margin
        self.bid_price = bid_price
        self.ask_price = ask_price
        self.spread = spread
