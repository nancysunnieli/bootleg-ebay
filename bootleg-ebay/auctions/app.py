import json
import socket

from flask import Flask, Response, request, jsonify


import auctions_functions
from auction import APIError

app = Flask(__name__)
socket_name = socket.gethostbyname(socket.gethostname())

@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for server error"""
    response = {"error": str(err)}
    return jsonify(response), 500

@app.errorhandler(APIError)
def handle_api_error(err):
    """Return custom JSON when APIError"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
        
    return jsonify(response), err.code

@app.route('/')
def base():
    return Response(response = json.dumps({"Status": "UP"}),
                    status = 200,
                    mimetype = 'application/json')


@app.route('/auction', methods=['POST'])
def create_auction():
    data = request.get_json()
    return auctions_functions.create_auction(data)

@app.route('/auction/<auction_id>', methods=['GET'])
def get_auction(auction_id):
    return auctions_functions.get_auction(auction_id)

@app.route('/auctions_by_item/<item_id>', methods=['GET'])
def get_auctions_by_item_id(item_id):
    return auctions_functions.get_auctions_by_item_id(item_id)

@app.route('/auction_metrics', methods=['POST'])
def get_auction_metrics():
    data = request.get_json()
    start = data['start']
    end = data['end']
    return auctions_functions.get_auction_metrics(start, end)


@app.route('/current_auctions', methods=['GET'])
def view_current_auctions():
    return auctions_functions.view_current_auctions()

@app.route('/auction/<auction_id>', methods=['DELETE'])
def remove_auction(auction_id):
    return auctions_functions.remove_auction(auction_id)


@app.route('/bids/<user_id>', methods=['GET'])
def user_bids(user_id):
    return auctions_functions.user_bids(user_id)

@app.route('/bid', methods=['POST'])
def create_bid():
    data = request.get_json()
    auction_id = data['auction_id']
    return auctions_functions.create_bid(auction_id, data['price'], data['buyer_id'])

@app.route('/<auction_id>/bids', methods=['GET'])
def view_bids(auction_id):
    # data = request.get_json()
    # auction_id = data['auction_id']
    return auctions_functions.view_bids(auction_id)

if __name__ == '__main__':
    app.run(debug = True, port = 2222, host = socket_name)