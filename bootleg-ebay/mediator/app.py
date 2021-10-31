import requests
from flask import Flask, Response, request
import json
import socket
import os

socket_name = socket.gethostbyname(socket.gethostname())

# getting IP Address of items container
# The following functions call the items microservice
itemsServiceHost = os.getenv('ITEMSAPIHOST', "localhost")

app = Flask(__name__)


def get_and_post(socket_url):
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')


@app.route('/Items/', methods=['GET'])
def ItemsServiceStatus():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/")
    r = requests.get(url = socket_url)
    return r.content

@app.route('/Items/ViewFlaggedItems', methods=['GET'])
def ViewFlaggedItems():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/ViewFlaggedItems")
    r = requests.get(url = socket_url)
    return r.content

@app.route('/Items/SearchItem', methods=['POST'])
def SearchItem():
    socket_url = ("http://" +itemsServiceHost +
                     ":8099" + "/SearchItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route('/Items/AddUserToWatchlist', methods = ['POST'])
def AddUserToWarchlist():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/AddUserToWatchlist")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route('/Items/RemoveItem', methods = ['POST'])
def RemoveItem():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/RemoveItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route('/Items/ReportItem', methods = ['POST'])
def ReportItem():
    socket_url = ("http://" + itemsServiceHost+
                     ":8099" + "/ReportItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/GetItem", methods = ['POST'])
def GetItem():
    socket_url = ("http://" + itemsServiceHost +
                     ":8099" + "/GetItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/ModifyItem", methods = ['POST'])
def ModifyItem():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/ModifyItem")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route("/Items/AddItem", methods = ['POST'])
def AddItem():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/AddItem")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/EditCategories", methods = ['POST'])
def EditCategories():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/EditCategories")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/ModifyAvailability", methods = ['POST'])
def ModifyAvailability():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/EditCategories")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content






# getting IP Address of carts container
# The following are functions for the carts microservice
cartsServiceHost = os.getenv('CARTSAPIHOST', "localhost")

@app.route("/Carts/CreateCart", methods = ['POST'])
def CreateCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/CreateCart")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/AddItemToCart", methods = ['POST'])
def AddItemToCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/AddItemToCart")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/DeleteItemFromCart", methods = ['POST'])
def DeleteItemFromCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/DeleteItemFromCart")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/GetItemsFromCart", methods = ['POST'])
def GetItemsFromCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/GetItemsFromCart")
    data_content = requests.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/Checkout", methods = ['POST'])
def Checkout():
    data_content = requests.get_json()
    get_items_url = ("http://" + cartsServiceHost +
                    ":3211" + "/GetItemsFromCart")
    item = requests.post(url = get_items_url, json = data_content)

    


    checkout_url = ("http://" + cartsServiceHost +
                    ":3211" + "/Checkout")
    
    
    r = requests.post(url = carts_url, json = data_content)
    return r.content



# getting IP Address of users container
# The following are functions for the users microservice
usersServiceHost = os.getenv('USERSDBHOST', "localhost")
usersName = 'Users'
usersPort = ':1001'

@app.route("/{}/ViewUser".format(usersName), methods = ['POST'])
def ViewUser():
    socket_url = ("http://" + usersServiceHost + usersPort + "/ViewUser")
    return get_and_post(socket_url)

@app.route("/{}/Login".format(usersName), methods = ['POST'])
def Login():
    socket_url = ("http://" + usersServiceHost + usersPort + "/Login")
    return get_and_post(socket_url)

@app.route("/{}/Logout".format(usersName), methods = ['POST'])
def Logout():
    socket_url = ("http://" + usersServiceHost + usersPort + "/Logout")
    return get_and_post(socket_url)

@app.route("/{}/CreateAccount".format(usersName), methods = ['POST'])
def CreateAccount():
    socket_url = ("http://" + usersServiceHost + usersPort + "/CreateAccount")
    return get_and_post(socket_url)

@app.route("/{}/SuspendAccount".format(usersName), methods = ['POST'])
def SuspendAccount():
    socket_url = ("http://" + usersServiceHost + usersPort + "/SuspendAccount")
    return get_and_post(socket_url)


@app.route("/{}/ModifyProfile".format(usersName), methods = ['POST'])
def ModifyProfile():
    socket_url = ("http://" + usersServiceHost + usersPort + "/ModifyProfile")
    return get_and_post(socket_url)

@app.route("/{}/DeleteAccount".format(usersName), methods = ['POST'])
def DeleteAccount():
    socket_url = ("http://" + usersServiceHost + usersPort + "/DeleteAccount")
    return get_and_post(socket_url)


# getting IP Address of auctions container
# The following are functions for the auctions microservice
auctionsServiceHost = os.getenv('AUCTIONSDBHOST', "localhost")
auctionsName = 'Auctions'
auctionsPort = ':1002'

@app.route("/{}/CreateAuction".format(auctionsName), methods = ['POST'])
def CreateAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/CreateAuction")
    return get_and_post(socket_url)

@app.route("/{}/GetAuction".format(auctionsName), methods = ['POST'])
def GetAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/GetAuction")
    return get_and_post(socket_url)

@app.route("/{}/ViewCurrentAuctions".format(auctionsName), methods = ['POST'])
def ViewCurrentAuctions():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/GetAuction")
    return get_and_post(socket_url)

@app.route("/{}/RemoveAuction".format(auctionsName), methods = ['POST'])
def RemoveAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/RemoveAuction")
    return get_and_post(socket_url)

@app.route("/{}/CompleteAuction".format(auctionsName), methods = ['POST'])
def CompleteAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/CompleteAuction")
    return get_and_post(socket_url)

@app.route("/{}/BidsByUser".format(auctionsName), methods = ['POST'])
def BidsByUser():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/BidsByUser")
    return get_and_post(socket_url)

@app.route("/{}/CreateBid".format(auctionsName), methods = ['POST'])
def CreateBid():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/CreateBid")
    return get_and_post(socket_url)

@app.route("/{}/ViewBids".format(auctionsName), methods = ['POST'])
def ViewBids():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/ViewBids")
    return get_and_post(socket_url)

@app.route("/{}/BuyNow".format(auctionsName), methods = ['POST'])
def BuyNow():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/BuyNow")
    return get_and_post(socket_url)

if __name__ == '__main__':
    app.run(debug = True, port = 8011, host = socket_name)
