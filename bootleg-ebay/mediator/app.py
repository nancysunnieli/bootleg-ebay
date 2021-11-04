import requests
import json
import socket
import os

from flask import Flask, Response, request
from flask_expects_json import expects_json
from flask_cors import CORS

socket_name = socket.gethostbyname(socket.gethostname())

# getting IP Address of items container
# The following functions call the items microservice
itemsServiceHost = os.getenv('ITEMSAPIHOST', "localhost")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def get_and_post(socket_url):
    data_content = request.get_json()
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
    if ViewBids().length == 0:
        return """There are already bids on 
                this item! It cannot be deleted"""
    
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
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@app.route("/Items/AddItem", methods = ['POST'])
def AddItem():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/AddItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/EditCategories", methods = ['POST'])
def EditCategories():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/EditCategories")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Items/ModifyAvailability", methods = ['POST'])
def ModifyAvailability():
    socket_url = ("http://" + itemsServiceHost +
                    ":8099" + "/ModifyAvailability")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

# getting IP Address of carts container
# The following are functions for the carts microservice
cartsServiceHost = os.getenv('CARTSAPIHOST', "localhost")

@app.route("/Carts/CreateCart", methods = ['POST'])
def CreateCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/CreateCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/AddItemToCart", methods = ['POST'])
def AddItemToCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/AddItemToCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/DeleteItemFromCart", methods = ['POST'])
def DeleteItemFromCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/DeleteItemFromCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/GetItemsFromCart", methods = ['POST'])
def GetItemsFromCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/GetItemsFromCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@app.route("/Carts/EmptyCart", methods = ['POST'])
def EmptyCart():
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/EmptyCart")
    data_content = request.get_json()
    r = requests.post(socket_url, json = data_content)
    return r.content

@app.route("/Carts/Checkout", methods = ['POST'])
def Checkout():
    data_content = request.get_json()

    # gets all items in user's cart
    get_items_url = ("http://" + cartsServiceHost +
                    ":3211" + "/GetItemsFromCart")
    items = json.loads((requests.post(url = get_items_url, json = data_content)).content)


    # checks availability of all items
    items_availability_url = ("http://" + itemsServiceHost +
                            ":8099" + "/GetItemsFromCart")
    available_items = []
    unavailable_items = []
    for item in items:
        availability = (requests.post(url = items_availability_url, data = {"item_id" : item})).content
        if availability == "Was unable to adjust availability. Item is no longer available.":
            unavailable_items.append(item)
        else:
            available_items.append(item)
    
    # GET CREDIT CARD INFO

    # CREATE PAYMENT INFO

    # DELETE ALL ITEMS FROM CART
    empty_cart_url = ("http://" + cartsServiceHost +
                    ":3211" + "/EmptyCart")
    r = requests.post(empty_cart_url, json = data_content)
    return r.content



# getting IP Address of users container
# The following are functions for the users microservice
usersServiceHost = os.getenv('USERAPIHOST', "localhost")
usersName = 'Users'
usersPort = ':1001'

UserIDSchema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'int'},
    },
    'required': ['user_id']
}

UserNamePassWordSchema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['username', 'password']
}

NoneSchema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}

UserInfoSchema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string'},
        'suspended': {'type': 'boolean'},
        'is_admin': {'type': 'boolean'}
    },
    'required': ["username", "password", "email", "suspended", "is_admin"]
}

@app.route("/{}/ViewUser".format(usersName), methods = ['POST'])
@expects_json(UserIDSchema)
def ViewUser():
    socket_url = ("http://" + usersServiceHost + usersPort + "/ViewUser")
    return get_and_post(socket_url)

@app.route("/{}/Login".format(usersName), methods = ['POST'])
@expects_json(UserNamePassWordSchema)
def Login():
    socket_url = ("http://" + usersServiceHost + usersPort + "/Login")
    return get_and_post(socket_url)

@app.route("/{}/Logout".format(usersName), methods = ['POST'])
@expects_json(NoneSchema)
def Logout():
    socket_url = ("http://" + usersServiceHost + usersPort + "/Logout")
    return get_and_post(socket_url)

@app.route("/{}/CreateAccount".format(usersName), methods = ['POST'])
@expects_json(UserInfoSchema)
def CreateAccount():
    # CREATING ACCOUNT
    data_content = request.get_json()
    socket_url = ("http://" + usersServiceHost + usersPort + "/CreateAccount")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    
    new_user_info = r.content.decode('utf-8')
    
    new_user_dict = json.loads(new_user_info)
    new_user_id = new_user_dict["id"]
    
    # CREATING CART
    socket_url = ("http://" + cartsServiceHost +
                    ":3211" + "/CreateCart")
    data_content = new_user_info
    requests.post(url = socket_url, json ={"user_id": new_user_id})
    
    return Response(response = new_user_info,
                    status = 200,
                    mimetype = 'application/json')
    

    
    return new_user_info


@app.route("/{}/SuspendAccount".format(usersName), methods = ['POST'])
@expects_json(UserIDSchema)
def SuspendAccount():
    socket_url = ("http://" + usersServiceHost + usersPort + "/SuspendAccount")
    return get_and_post(socket_url)


@app.route("/{}/ModifyProfile".format(usersName), methods = ['POST'])
@expects_json(UserInfoSchema)
def ModifyProfile():
    socket_url = ("http://" + usersServiceHost + usersPort + "/ModifyProfile")
    return get_and_post(socket_url)

@app.route("/{}/DeleteAccount".format(usersName), methods = ['POST'])
@expects_json(UserIDSchema)
def DeleteAccount():
    socket_url = ("http://" + usersServiceHost + usersPort + "/DeleteAccount")
    return get_and_post(socket_url)


# getting IP Address of auctions container
# The following are functions for the auctions microservice
auctionsServiceHost = os.getenv('AUCTIONSDBHOST', "localhost")
auctionsName = 'Auctions'
auctionsPort = ':2222'

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
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/ViewCurrentAuctions")
    return get_and_post(socket_url)

@app.route("/{}/RemoveAuction".format(auctionsName), methods = ['POST'])
def RemoveAuction():
    socket_url = ("http://" + auctionsServiceHost + auctionsPort + "/RemoveAuction")
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


# getting IP Address of payments container
# The following are functions for the payments microservice
paymentsServiceHost = os.getenv('PAYMENTSDBHOST', "localhost")
paymentsName = 'Payments'
paymentsPort = ':1003'

@app.route("/{}/CreatePaymentCard".format(paymentsName), methods = ['POST'])
def CreatePaymentCard():
    socket_url = ("http://" + paymentsServiceHost + paymentsPort + "/CreatePaymentCard")
    return get_and_post(socket_url)

@app.route("/{}/GetPaymentCard".format(paymentsName), methods = ['POST'])
def GetPaymentCard():
    socket_url = ("http://" + paymentsServiceHost + paymentsPort + "/GetPaymentCard")
    return get_and_post(socket_url)

@app.route("/{}/DeleteAccount".format(paymentsName), methods = ['POST'])
def PaymentsDeleteAccount():
    socket_url = ("http://" + paymentsServiceHost + paymentsPort + "/DeleteAccount")
    return get_and_post(socket_url)


if __name__ == '__main__':
    app.run(debug = True, port = 8011, host = socket_name)
