from stonex.account import Account

acc = Account()
acc.open_new_session()
trading_accounts, client_id = acc.client_trading_accounts()
acc.margin_information()
acc.close_existing_session()
