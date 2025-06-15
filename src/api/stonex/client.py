import os
from .utils.stonex_utils import send_request

class Client():
    """
    # Forex.com Client
    
    A class that verifys and stores client information with Forex.com.
    
    Information includes:
        - Number of accounts with the broker
        - Balance
        - Margin requirements
        - and much more!

    Args:
        
    """
    def __init__(self, username: str=os.environ.get('USERNAME'), password: str=os.environ.get('PASSWORD'), app_key: str=os.environ.get('APP_KEY')):
        self.username: str = username
        self.password: str = password
        self.app_key: str = app_key

        self.url: str = os.environ.get('HOST')
        self.accounts: list = None
        self.balance_data: dict = None
        self.cash: float = None
        self.margin: float = None
        self.margin_requirements: float = None
        self.equity: float = None
        self.pnl: float = None

        self.session_id: str = None
        self.client_id: str = None

    def __repr__(self):
        return f'Account(username={self.username}, password={self.password}, app_key={self.app_key})'

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
            self.locate_trading_accounts()
            self.update_account_balance()
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
    
    def locate_trading_accounts(self):
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
            self.client_id = client_account_id
            return print(
                f'Number of accounts: {len(trading_accounts)}'
            )
        
    def update_account_balance(self):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path='/v2/margin/clientAccountMargin',
            params=\
            {
                'UserName': self.username,
                "Session": self.session_id,
                'ClientAccountId': self.client_id
            }
        )

        if response_code == 200:
            self.balance_data = response
            self.cash = response.get('cash')
            self.margin = response.get('margin')
            self.margin_requirements = response.get('totalMarginRequirement')
            self.equity = response.get('netEquity')
            self.pnl = response.get('openTradeEquity')
            return print(
                f'Cash: ${self.cash} \nMargin: ${self.margin} \nMargin Requirements: ${self.margin_requirements}\
                \nEquity: ${self.equity} \nP/L: ${self.pnl}'
            )