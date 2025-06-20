import pandas as pd
from .client import Client
from .instrument import Instrument
from .utils.stonex_utils import send_request


class Market(object):

    def __init__(self, client: Client):
        self.client: Client = client
        self.url = client.url

    def export_markets(self, file_name: str):
        """Available markets and unique identifiers for a client to trade in
        """
        response_code, response = send_request(
            method='GET',
            url=self.client.url,
            path='/v2/market/tagLookup',
            params={
                'UserName': self.client.username,
                'Session': self.client.session_id,
                'ClientAccountId': self.client.client_id
            }
        )
        if response_code == 200:
            markets = response['tags'][0]['children']
            df = pd.DataFrame(markets).set_index('marketTagId')
            df.to_csv(f'./data/{file_name}')
            return df

    def market_information(self, market_id: str):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path=f'/v2/market/{market_id}/information',
            params={
                'UserName': self.client.username,
                'Session': self.client.session_id,
                'ClientAccountId': self.client.client_id
            }
        )

        if response_code == 200:
            print(response)

    def currency_pairs(self, currency: str = 'USD', market: str = '81'):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path='/v2/market/fullSearchWithTags',
            params={
                'tagId': market,
                'query': currency,
                'maxResults': 200,

                'UserName': self.client.username,
                'Session': self.client.session_id,
                'ClientAccountId': self.client.client_id,
            }
        )

        if response_code == 200:
            currency_pair_dict = {}
            market_information = response['marketInformation']
            for information in market_information:
                market_id = information.get('marketId')
                name = information.get('name')
                margin = information.get('marginFactor')
                min_margin = information.get('minMarginFactor')
                max_margin = information.get('maxMarginFactor')
                client_margin = information.get('clientMarginFactor')
                
                prices = information.get('prices')
                bid_price = prices.get('bidPrice')
                ask_price = prices.get('offerPrice')
                spread = ask_price - bid_price

                currency_pair_dict[name] = Instrument(
                    client=self.client,
                    market_id=market_id,
                    name=name,
                    margin=margin,
                    min_margin=min_margin,
                    max_margin=max_margin,
                    client_margin=client_margin,
                    bid_price=bid_price,
                    ask_price=ask_price,
                    spread=spread
                )
        return currency_pair_dict
