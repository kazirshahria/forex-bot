import os
from .utils.stonex_utils import send_request


class Client(object):
    """# Forex.com Client

    A class that verify and stores client information with
    [Forex.com](#https://www.forex.com/en-us/).

    The information available to access includes but not limited to:
        - Number of accounts with the broker
        - Balance
        - Margin requirements
        - and much more!

    This class is meant to only verify and store information about a specific
    user. Verification will be necessary for access to other instances.
    If necessary, there are functions that can find additional
    information about the user.

    ---

    Attributes:
        username (str): The username to login to the broker account.
        password (str): The password to login to the broker account.
        app_key (str): The secret app key to interact with the StoneX\
        [API](#https://docs.labs.gaincapital.com/).
    """

    def __init__(self, username: str = os.environ.get('USERNAME'),
                 password: str = os.environ.get('PASSWORD'),
                 app_key: str = os.environ.get('APP_KEY')):

        """Initialize the instance with the client's account information.

        The credentials are case-sensitive and must match exactly with the
        login on Forex.com. If values are not provided, the values
        will be retrieved from the environment variables: USERNAME,
        PASSWORD, and APP_KEY.

        Parameters:
            username (str): The username to login to the broker account.
            password (str): The password to login to the broker account.
            app_key (str): The secret app key to interact with the StoneX API.
        """
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
        return f'Account(username={self.username},\
                password={self.password},\
                app_key={self.app_key})'

    def open_new_session(self):
        response_code, response = send_request(
            method='POST',
            url=self.url,
            path='/v2/Session',
            json={
                'Password': self.password,
                'UserName': self.username,
                'AppKey': self.app_key
            }
        )
        
        if (response_code == 200) & (self.session_id is None):
            session = response.get("session")
            self.session_id = session
            self.locate_trading_accounts()
            self.current_account_balance()
            return session

    def close_existing_session(self):
        response_code, response = send_request(
            method='POST',
            url=self.url,
            path='/TradingAPI/session/deleteSession',
            params={
                'UserName': self.username,
                'Session': self.session_id

            }
        )

        if (response_code == 200) & (response.get("LoggedOut") is True):
            print('Session closed')
            exit()

    def locate_trading_accounts(self):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path='/v2/userAccount/ClientAndTradingAccount',
            params={
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

    def current_account_balance(self):
        response_code, response = send_request(
            method='GET',
            url=self.url,
            path='/v2/margin/clientAccountMargin',
            params={
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
                f'Cash: ${self.cash} \nMargin: ${self.margin}\
                    \nMargin Requirements: ${self.margin_requirements}\
                    \nEquity: ${self.equity} \nP/L: ${self.pnl}'
            )
