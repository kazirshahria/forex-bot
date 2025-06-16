import pandas as pd
from .client import Client
from .utils.stonex_utils import send_request

class Market():
    """
    
    """
    def __init__(self, client: Client):
        self.client: Client = client
    
    def available_market_tags(self, file_name: str='avaliable_markets.csv'):
        """
        The market tags available in a client's account
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
