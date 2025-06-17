import pandas as pd
from .client import Client
from .instrument import Instrument
from .utils.stonex_utils import send_request

class Market():
    """
    
    """
    def __init__(self, client: Client):
        self.client: Client = client
        self.url = client.url
    
    def available_market_tags(self, file_name: str='avaliable_markets.csv'):
        """
        Avaliable markets and unique identifiers for a client to trade in
        """
        response_code, response = send_request(
            method='GET',
            url=self.client.url,
            path='/v2/market/tagLookup',
            params=\
            {
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

    def search_currency_pairs(self, query: str='USD', market_tag: str='81'):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path='/v2/market/fullSearchWithTags',
            params=\
            {
                'tagId': market_tag,
                'query': query,
                'maxResults': 200,

                'UserName': self.client.username,
                'Session': self.client.session_id,
                'ClientAccountId': self.client.client_id,
            }
        )

        if response_code == 200:
            currency_pair_dict = {}
            market_informations = response['marketInformation']
            for market_information in market_informations:
                market_id = market_information.get('marketId')
                name = market_information.get('name')
                margin = market_information.get('marginFactor')
                min_margin = market_information.get('minMarginFactor')
                max_margin = market_information.get('maxMarginFactor')
                client_margin = market_information.get('clientMarginFactor')
                
                prices = market_information.get('prices')
                bid_price = prices.get('bidPrice')
                ask_price = prices.get('offerPrice')
                spread = ask_price - bid_price

                currency_pair_dict[name] = Instrument(
                    client=self.client,
                    market_id=market_id,
                    name = name, 
                    margin=margin,
                    min_margin=min_margin,
                    max_margin=max_margin,
                    client_margin=client_margin,
                    bid_price=bid_price,
                    ask_price=ask_price,
                    spread=spread
                )
        return currency_pair_dict

    def market_information(self, market_id: str):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path=f'/v2/market/{market_id}/information',
            params=\
            {
                'UserName': self.client.username,
                'Session': self.client.session_id,
                'ClientAccountId': self.client.client_id
            }
        )
        
        if response_code == 200:
            print(response)

