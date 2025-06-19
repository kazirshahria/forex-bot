from typing import Literal
from .client import Client
from .utils.stonex_utils import send_request
import pandas as pd
from plotly import graph_objects as go
import datetime
from zoneinfo import ZoneInfo


class Instrument(object):

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

    def price_bars(self,
                   interval: Literal['TICK', 'MINUTE', 'HOUR', 'DAY', 'WEEK'] = 'DAY',
                   span: str = '1',
                   price_bars: int = 30,
                   price_type: Literal['ASK', 'MID', 'BID'] = 'MID'):

        """
        The historic price bars for a instrument in OHLC (open, high, low, and close) format. The price type is set to MID
        because that is the price that closely represents the candlestick formations on TradingView.

        Parameters:
            interval (str):  The timeframe for each candlestick. For example, for the hourly interval, input would be HOURLY.

            span (str): The number of each interval per price bar. Default is set to 1.
                    - MINUTE: 1, 2, 3, 5, 10, 15, 30
                    - HOUR: 1, 2, 4, 8
                    - TICK or DAY or WEEK: 1

            price_bars (int): The total number of candles to look back. Default is set to 360 or YTD.
            price_type (str): The price types of the candles. Default is set to BID.

        Returns:
            candlesticks (list): A list of candlestick values.
        """
        def fix_date(date_str):
            date_str: str = date_str.replace('/Date(', '').replace(')/', '')
            date_float: float = float(date_str)/1000
            date_utc = datetime.datetime.fromtimestamp(timestamp=date_float, tz=datetime.UTC)
            eastern_tz = ZoneInfo('America/New_York')
            return date_utc.astimezone(eastern_tz)

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
            previous_candles = response.get('PriceBars')
            current_candle = response.get('PartialPriceBar')

            for previous_candle in previous_candles:
                previous_candle['BarDate'] = fix_date(previous_candle.get('BarDate'))

            current_candle['BarDate'] = fix_date(current_candle.get('BarDate'))
            return previous_candles, current_candle

    def plot_candlesticks(self, candles):
        df = pd.DataFrame(candles).set_index('BarDate')
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    increasing_line_color='#000000',
                    decreasing_line_color='#000000',
                    increasing_fillcolor='#ffffff',
                    decreasing_fillcolor='#000000'
                )
            ]
        )
        fig.update_layout(title=f'{self.name}', xaxis_rangeslider_visible=False, plot_bgcolor='#dbdbdb')
        fig.show()
        return fig
