import os

CARTS_SERVICE_HOST = os.getenv('CARTSAPIHOST', "localhost")

ITEMS_SERVICE_HOST = os.getenv('ITEMSAPIHOST', "localhost")

USERS_SERVICE_HOST = os.getenv('USERAPIHOST', "localhost")
USERS_NAME = 'users'
USERS_PORT = ':1001'

AUCTIONS_SERVICE_HOST = os.getenv('AUCTIONSDBHOST', "localhost")
AUCTIONS_NAME = 'auctions'
AUCTIONS_PORT = ':2222'

PAYMENTS_SERVICE_HOST = os.getenv('PAYMENTSDBHOST', "localhost")
PAYMENTS_NAME = 'payments'
PAYMENTS_PORT = ':1003'