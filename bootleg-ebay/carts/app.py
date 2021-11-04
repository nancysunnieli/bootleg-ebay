from flask import Flask, Response, request
import json
app = Flask(__name__)
import carts_functions
import socket

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')

@app.route('/CreateCart', methods=['POST'])
def CreateCart():
    data = request.get_json()
    user_id = data["user_id"]
    return carts_functions.create_cart(user_id)

@app.route('/AddItemToCart', methods=['POST'])
def AddItemToCart():
    data = request.get_json()
    user_id = data["user_id"]
    item_id = data["item_id"]
    return carts_functions.add_item_to_cart(user_id, item_id)

@app.route('/DeleteItemFromCart', methods = ['POST'])
def DeleteItemFromCart():
    data = request.get_json()
    user_id = data["user_id"]
    item_id = data["item_id"]
    return carts_functions.delete_item_from_cart(user_id, item_id)

@app.route('/GetItemsFromCart', methods = ['POST'])
def GetItemsFromCart():
    data = request.get_json()
    user_id = data["user_id"]
    return carts_functions.get_items(user_id)

@app.route('/EmptyCart', methods = ['POST'])
def EmptyCart():
    data = request.get_json()
    user_id = data["user_id"]
    return carts_functions.empty_cart(user_id)


if __name__ == '__main__':
    app.run(debug = True, port = 3211, host = socket.gethostbyname(socket.gethostname()))