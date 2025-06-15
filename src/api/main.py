from stonex.client import Client

acc = Client()
print(acc)
acc.open_new_session()
acc.close_existing_session()
