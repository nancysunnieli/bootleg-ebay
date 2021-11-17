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

@app.route('/create_cart', methods=['POST'])
def create_cart():
    data = request.get_json()
    user_id = int(data["user_id"])
    return carts_functions.create_cart(user_id)

@app.route('/add_item_to_cart', methods=['POST'])
def add_item_to_cart():
    data = request.get_json()
    user_id = data["user_id"]
    item_id = data["item_id"]
    return carts_functions.add_item_to_cart(user_id, item_id)

@app.route('/delete_item_from_cart', methods = ['POST'])
def delete_item_from_cart():
    data = request.get_json()
    user_id = int(data["user_id"])
    item_id = data["item_id"]
    return carts_functions.delete_item_from_cart(user_id, item_id)

@app.route('/get_items_from_cart', methods = ['POST'])
def get_items_from_cart():
    data = request.get_json()
    user_id = data["user_id"]
    return carts_functions.get_items(user_id)

@app.route('/empty_cart', methods = ['POST'])
def empty_cart():
    data = request.get_json()
    user_id = data["user_id"]
    return carts_functions.empty_cart(user_id)

@app.route('/remove_cart', methods = ['POST'])
def remove_cart():
    data = request.get_json()
    user_id = data["user_id"]
    return carts_functions.remove_cart(user_id)


if __name__ == '__main__':
    app.run(debug = True, port = 3211, host = socket.gethostbyname(socket.gethostname()), threaded=True)