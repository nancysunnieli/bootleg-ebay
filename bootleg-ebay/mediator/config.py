import os

CARTS_SERVICE_HOST = os.getenv('CARTSAPIHOST', "localhost")
CARTS_PORT = ":3211"
CARTS_URL = "http://" + CARTS_SERVICE_HOST + CARTS_PORT

ITEMS_SERVICE_HOST = os.getenv('ITEMSAPIHOST', "localhost")
ITEMS_PORT = ":8099"
ITEMS_URL = "http://" + ITEMS_SERVICE_HOST + ITEMS_PORT

USERS_SERVICE_HOST = os.getenv('USERAPIHOST', "localhost")
USERS_PORT = ':1001'
USERS_URL = "http://" + USERS_SERVICE_HOST + USERS_PORT

AUCTIONS_SERVICE_HOST = os.getenv('AUCTIONSAPIHOST', "localhost")
AUCTIONS_PORT = ':2222'
AUCTIONS_URL = "http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT

PAYMENTS_SERVICE_HOST = os.getenv('PAYMENTSAPIHOST', "localhost")
PAYMENTS_PORT = ':1003'
PAYMENTS_URL = "http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT

NOTIFS_SERVICE_HOST = os.getenv('NOTIFSAPIHOST', 'localhost')
NOTIFS_PORT = ':8012'
NOTIFS_URL = "http://" + NOTIFS_SERVICE_HOST + NOTIFS_PORT