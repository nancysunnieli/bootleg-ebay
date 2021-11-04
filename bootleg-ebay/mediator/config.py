import os

cartsServiceHost = os.getenv('CARTSAPIHOST', "localhost")

itemsServiceHost = os.getenv('ITEMSAPIHOST', "localhost")

usersServiceHost = os.getenv('USERAPIHOST', "localhost")
usersName = 'Users'
usersPort = ':1001'

auctionsServiceHost = os.getenv('AUCTIONSDBHOST', "localhost")
auctionsName = 'Auctions'
auctionsPort = ':2222'

paymentsServiceHost = os.getenv('PAYMENTSDBHOST', "localhost")
paymentsName = 'Payments'
paymentsPort = ':1003'