from typing import Literal
from .client import Client
from .utils.stonex_utils import send_request
from plotly import graph_objects as go
from plotly import io as pio
import pandas as pd
import datetime


class Instrument(object):
    pio.renderers.default = "browser"

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
                   candles: int = 60,
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

            candles (int): The total number of candles to look back. Default is set to 60 or last 2 months.
            price_type (str): The price types of the candles. Default is set to BID.

        Returns:
            current_candles (pd.DataFrame): A dataframe containing historical price action.
            previous_candles (list): A list with a single item containing the current price action.
        """
        def fix_date(date_str):
            date_str: str = date_str.replace('/Date(', '').replace(')/', '')
            date_float: float = float(date_str)/1000
            date_utc = datetime.datetime.fromtimestamp(timestamp=date_float, tz=datetime.UTC)
            return date_utc

        response_code, response = send_request(
            method='GET',
            url=self.client.url,
            path=f'/TradingAPI/market/{self.market_id}/barhistory',
            params={
                'UserName': self.client.username,
                'Session': self.client.session_id,
                'interval': interval,
                'span': span,
                'PriceBars': candles,
                'priceType': price_type
            }
        )

        if response_code == 200:
            previous_candles = response.get('PriceBars')
            current_candles = response.get('PartialPriceBar')

            for previous_candle in previous_candles:
                previous_candle['BarDate'] = fix_date(previous_candle.get('BarDate'))

            current_candles['BarDate'] = fix_date(current_candles.get('BarDate'))
            
            return pd.DataFrame(previous_candles + [current_candles]).set_index('BarDate'), current_candles


    def plot_price(self, df: pd.DataFrame):
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
        fig.update_layout(title=f'{self.name}: Price Action', xaxis_rangeslider_visible=False, plot_bgcolor='#dbdbdb')
        fig.show()
        return fig
