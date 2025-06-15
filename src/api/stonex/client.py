import os
from .utils.stonex_utils import send_request

class Account(object):
    
    def __init__(self, username: str=os.environ.get('USERNAME'), password: str=os.environ.get('PASSWORD'), app_key: str=os.environ.get('APP_KEY')):
        self.username: str = username
        self.password: str = password
        self.app_key: str = app_key

        self.url: str = os.environ.get('HOST')
        self.accounts: list = None
        self.balance: dict = None

        self.session_id: str = None
        self.client_id: str = None

    def open_new_session(self):
        response_code, response = send_request(
            method='POST',
            url=self.url,
            path='/v2/Session',
            json=\
            {
                'Password': self.password,
                'UserName': self.username,
                'AppKey': self.app_key
            }
        )

        if (response_code == 200) & (self.session_id == None):
            session = response.get("session")
            self.session_id = session
            return session

    def close_existing_session(self):
        response_code, response = send_request(
            method='POST',
            url=self.url,
            path='/TradingAPI/session/deleteSession',
            params=\
            {
                'UserName': self.username,
                'Session': self.session_id

            }
        )

        if (response_code == 200) & (response.get("LoggedOut") == True):
            print(f'Session closed')
            exit()

    def client_trading_accounts(self):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path='/v2/userAccount/ClientAndTradingAccount',
            params=\
            {
                'UserName': self.username,
                'Session': self.session_id
            }
        )
        
        if response_code == 200:
            trading_accounts = response.get('tradingAccounts')
            self.accounts = trading_accounts

            client_account_id = trading_accounts[0].get('clientAccountId')
            self.client_account_id = client_account_id

            return trading_accounts, client_account_id
    
    def balance_information(self) -> dict:
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path='/v2/margin/clientAccountMargin',
            params=\
            {
                'UserName': self.username,
                "Session": self.session_id,
                'ClientAccountId': self.client_account_id
            }
        )

        if response_code == 200:
            self.balance = response
            return response