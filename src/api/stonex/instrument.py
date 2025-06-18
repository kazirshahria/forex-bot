from typing import Literal
from .client import Client
from .utils.stonex_utils import send_request


class Instrument():

    def __init__(self, client: Client, market_id: str, name: str,
                 margin: float, min_margin: float, max_margin: float,
                 client_margin: float, bid_price: float, ask_price: float,
                 spread: float):
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

    def price_bars(self,
                   interval: Literal['TICK', 'MINUTE', 'HOUR', 'DAY', 'WEEK'],
                   span: str = '1',
                   price_bars: int = 360,
                   price_type: Literal['ASK', 'MID', 'BID'] = 'BID'):

        """Get the historic price bars for a instrument in
        OHLC (open, high, low, and close) format.

        Parameters:
            interval (str):  The price bar interval.
            span (str): The number of each interval per price bar.\
            Valid values depend on the interval:
                    - 'MINUTE': '1', '2', '3', '5', '10', '15', '30'
                    - 'HOUR': '1', '2', '4', '8'
                    - 'TICK', 'DAY', 'WEEK': '1'
            price_bars (int): The total number of candles to look back at.
            price_type (str): The price types of the candles.

        Returns:
            candlesticks (list): A list of candlestick values.
        """
        response_code, response = send_request(
            method='GET',
            url=self.client.url,
            path=f'/TradingAPI/market/{self.market_id}/barhistory',
            params={
                'UserName': self.client.username,
                'Session': self.client.session_id,
                'interval': interval,
                'span': span,
                'PriceBars': price_bars,
                'priceType': price_type
            }
        )

        if response_code == 200:
            print(response)
